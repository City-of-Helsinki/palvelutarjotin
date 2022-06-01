import csv
import datetime
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Min
from django.db.models.query import Prefetch
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from occurrences.models import Enrolment, PalvelutarjotinEvent
from organisations.models import Organisation, Person
from reports.models import EnrolmentReport
from reports.serializers import EnrolmentReportSerializer
from reports.services import sync_enrolment_reports
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from rest_framework.views import APIView

from common.utils import get_node_id_from_global_id
from palvelutarjotin.oidc import KultusApiTokenAuthentication

logger = logging.getLogger(__name__)


def naive_datetime_to_tz_aware(datetime: str) -> str:
    return datetime + "T00:00:00.000Z" if datetime else None


class ExportReportViewMixin:
    """
    Pass a list of selected objects in the GET query string (ids-parameter):
    example:
        return HttpResponseRedirect(
            "/reports/organisation/persons?ids=%s"
            % (",".join(str(pk) for pk in selected),)
        )
    """

    def get_queryset(self):
        # Get URL parameter as a string, if exists
        ids = self.request.GET.get("ids", None)
        # Get organisations for ids if they exist
        if ids is not None:
            # Convert parameter string to list of integers
            ids = [int(x) for x in ids.split(",")]
            # Get objects for all parameter ids
            queryset = self.model.objects.filter(pk__in=ids)
        else:
            # Else no parameters, return all objects
            queryset = self.model.objects.all()

        return queryset


class OrganisationPersonsMixin(ExportReportViewMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        # TODO: Prefetching persons might just be enough.
        # It may be needless to filter persons without users.
        return queryset.prefetch_related(
            Prefetch(
                "persons",
                queryset=Person.objects.filter(user__isnull=False).order_by("name"),
            )
        )


class PalvelutarjotinEventEnrolmentsMixin(ExportReportViewMixin):

    max_results = 2000

    def message_max_result(self, request):
        # Inform the user if not all the data was included
        if len(self.get_queryset()) == self.max_results:
            logger.warning(
                "Queryset items maximum count exceeded "
                + "when fetching data for events enrolments report."
            )
            messages.add_message(
                request,
                messages.WARNING,
                _(
                    "Maximum count exceeded (%(max_results)s) "
                    + "when exporting events enrolments: "
                    + "Some of the data (older) might be missing."
                )
                % {"max_results": self.max_results},
            )

    def get_node_id(self, query_id):
        try:
            return int(query_id)
        except ValueError:
            # resolve the database id
            return get_node_id_from_global_id(query_id, "PalvelutarjotinEventNode")

    def get_queryset(self):
        """
        Fetch enrolments instead of palvelutarjotineEvent instances.
        This means that events and occurrences without any enrolments
        wont be included!
        """
        queryset = Enrolment.objects.filter(status=Enrolment.STATUS_APPROVED)

        # Get URL parameter as a string, if exists
        event_ids = self.request.GET.get("ids", None)
        # Get organisations for ids if they exist
        if event_ids is not None:
            # Convert parameter string to list of integers
            event_ids = [self.get_node_id(x) for x in event_ids.split(",")]
            # Get objects for all parameter ids
            queryset = queryset.filter(occurrence__p_event__id__in=event_ids)

        start_date = naive_datetime_to_tz_aware(self.request.GET.get("start", None))
        end_date = naive_datetime_to_tz_aware(self.request.GET.get("end", None))

        if start_date and end_date:
            queryset = queryset.filter(
                occurrence__p_event__enrolment_start__range=[start_date, end_date]
            )
        elif start_date:
            queryset = queryset.filter(
                occurrence__p_event__enrolment_start__gte=start_date
            )
        elif end_date:
            queryset = queryset.filter(
                occurrence__p_event__enrolment_start__lte=end_date
            )

        if not event_ids and not start_date and not end_date:
            # Get this years enrolments
            today = datetime.datetime.now(tz=timezone.utc)
            queryset = queryset.filter(
                occurrence__p_event__enrolment_start__year=today.year
            )

        # Order by occurrence start time
        # and select all related content that is needed in report.
        # In case a whole db is trying to be fetched, limit the amount of fetched items
        return queryset.order_by(
            "-occurrence__p_event__enrolment_start"
        ).select_related("occurrence__p_event", "study_group", "person")[
            : self.max_results
        ]


"""
Admin views...
"""


@method_decorator(staff_member_required, name="dispatch")
class OrganisationPersonsAdminView(OrganisationPersonsMixin, ListView):
    """
    The admin view which renders a table of organisations persons.
    """

    model = Organisation
    template_name = "reports/admin/organisation_persons.html"
    context_object_name = "organisations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["opts"] = self.model._meta
        return context

    # @staff_member_required
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@method_decorator(staff_member_required, name="dispatch")
class PalvelutarjotinEventEnrolmentsAdminView(
    PalvelutarjotinEventEnrolmentsMixin, ListView
):
    """
    The admin view which renders a table of events occurrences and enrolments.
    """

    model = PalvelutarjotinEvent
    template_name = "reports/admin/event_enrolments.html"
    context_object_name = "enrolments"

    def get(self, request, *args, **kwargs):

        # Inform the user if not all the data was included
        self.message_max_result(request)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["linked_events_root"] = settings.LINKED_EVENTS_API_CONFIG["ROOT"]
        context["total_children"] = sum(
            enrolment.study_group.group_size for enrolment in self.get_queryset()
        )
        context["total_adults"] = sum(
            enrolment.study_group.amount_of_adult for enrolment in self.get_queryset()
        )
        context["opts"] = self.model._meta
        return context


"""
CSV Views...
"""


class ExportReportCsvView(ExportReportViewMixin, APIView):
    """
    A generic way to create csv reports from models.
    """

    model = None
    authentication_classes = [KultusApiTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]
    csv_dialect = csv.excel
    csv_delimiter = ";"

    def _create_csv_response_writer(self, filename):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(filename)

        """
        Adding BOM is not advicable, and UTF-8 shouldn't even have that,
        but Microsoft product seems to sometimes need it.
        """
        response.write("\ufeff")

        """
        CSV is a delimited text file that uses a comma to separate values
        (many implementations of CSV import/export tools allow other
        separators to be used; for example, the use of a "Sep=^" row
        as the first row in the csv file will cause Excel to open
        the file expecting caret "^" to be the separator instead of comma ",").
        ~ https://en.wikipedia.org/wiki/Comma-separated_values.
        NOTE: At least when using a comma as a delimiter,
        the separator is needed to be defined for Microsoft Excel.
        NOTE: When tested with Microsoft Excel for Mac, strangely,
        it seems to help Excel to choose the delimiter, but seems to break encoding
        and the scandinavian letters are not shown properly.
        """
        # response.write(f"sep={self.csv_delimiter}{self.csv_dialect.lineterminator}")

        """
        The CSV library uses Excel as the default dialect,
        but Excel still seems not to work properly with it,
        since there were issues with the separator and the encoding.
        Using the semicolon (";") as a delimiter
        seems to fix UTF-8 issues with Microsoft Excel.
        """
        writer = csv.writer(
            response, dialect=self.csv_dialect, delimiter=self.csv_delimiter
        )

        return (writer, response)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        writer, response = self._create_csv_response_writer(meta)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response


class OrganisationPersonsCsvView(OrganisationPersonsMixin, ExportReportCsvView):
    """
    A csv of organisations persons.
    """

    model = Organisation

    def get(self, request, *args, **kwargs):
        writer, response = self._create_csv_response_writer(
            "kultus_organisations_persons"
        )
        writer.writerow([_("Organisation"), _("Name"), _("Email"), _("Phone")])
        for organisation in self.get_queryset():
            for person in organisation.persons.all().order_by("name"):
                writer.writerow(
                    [
                        organisation.name,
                        person.name,
                        person.email_address,
                        person.phone_number,
                    ]
                )
        return response


class PalvelutarjotinEventEnrolmentsCsvView(
    PalvelutarjotinEventEnrolmentsMixin, ExportReportCsvView
):
    """
    A csv of organisations persons.
    """

    model = PalvelutarjotinEvent

    def get(self, request, *args, **kwargs):
        # Inform the user if not all the data was included
        self.message_max_result(request)
        writer, response = self._create_csv_response_writer(
            "kultus_events_approved_enrolments"
        )
        writer.writerow(
            [
                _("Enrolment id"),
                _("LinkedEvents id"),
                _("LinkedEvents uri"),
                _("Occurrence starting (date)"),
                _("Enrolment date"),
                _("Group name"),
                _("Study levels"),
                _("Amount of children"),
                _("Amount of adults"),
                _("Extra needs"),
                _("Contact mail"),
            ]
        )
        for enrolment in self.get_queryset():
            writer.writerow(
                [
                    enrolment.id,
                    enrolment.occurrence.p_event.linked_event_id,
                    "{linked_events_root}event/{linked_event_id}".format(
                        linked_events_root=settings.LINKED_EVENTS_API_CONFIG["ROOT"],
                        linked_event_id=enrolment.occurrence.p_event.linked_event_id,
                    ),
                    enrolment.occurrence.start_time,
                    enrolment.enrolment_time,
                    enrolment.study_group.name,
                    ", ".join(
                        [
                            study_level.label
                            for study_level in enrolment.study_group.study_levels.all()
                        ]
                    ),
                    enrolment.study_group.group_size,
                    enrolment.study_group.amount_of_adult,
                    enrolment.study_group.extra_needs,
                    enrolment.person.email_address,
                ]
            )
        return response


class EnrolmentReportCsvView(ExportReportCsvView):
    model = EnrolmentReport


@staff_member_required
@require_http_methods(["POST"])
def sync_enrolment_reports_view(request):
    create_from = Enrolment.objects.aggregate(Min("enrolment_time"))[
        "enrolment_time__min"
    ]
    sync_enrolment_reports(hydrate_linkedevents_event=True, create_from=create_from)
    messages.add_message(request, messages.SUCCESS, _("Enrolment reports synced!"))
    return HttpResponseRedirect(reverse("admin:reports_enrolmentreport_changelist"))


class EnrolmentReportListView(generics.ListAPIView):
    """
    Return a list of all the enrolment reports.

    There are some query parameters available that can be used as filters to
    narrow the result of the queryset.
    E.g you can use `?updated_at__gte=2021-11-23` to filter the results where
    the updated_at -field value should be greater than or equal to the given
    date in ISO-format (2021-11-23). The `__lte` stands for less than or equal.

    The available filters:
        - `updated_at__gte`, to filter with a report update date
        - `updated_at__lte`,
        - `created_at__gte`, to filter with a report creation date
        - `created_at__lte`
        - `enrolment_time__gte`, to filter with a report enrolment time
        - `enrolment_time__lte`
        - `enrolment_start_time__gte`, to filter with a report enrolment start time
        - `enrolment_start_time__lte`
        - `enrolment_status`, to filter with an enrolment status:
        approved, pending. cancelled. declined

    The result set can also be ordered by with an `order_by` -query parameter.
    E.g `?order_by=updated_at` will order the resultset by updated_at -field.
    The order will be ascending by default but can be set to be descending,
    by adding a "-" (minus) in front of the field name,
    e.g `?order_by=-updated_at`.
    """

    serializer_class = EnrolmentReportSerializer
    # Must be allowed only with model permissions (for 1 power bi user).
    # Should not be allowed for every staff member,
    # but only the ones with special permission.
    permission_classes = [DjangoModelPermissions]
    # It is wanted from Power bi reports creator,
    # that there should be no pagination
    pagination_class = None

    def get_queryset(self):
        # Allow the following filter parameters
        allowed_filter_keys = [
            "updated_at__gte",
            "updated_at__lte",
            "created_at__gte",
            "created_at__lte",
            "enrolment_status",
            "enrolment_start_time__gte",
            "enrolment_start_time__lte",
            "enrolment_time__gte",
            "enrolment_time__lte",
        ]
        queryset = EnrolmentReport.objects.all()
        filter_params = {
            k: self.request.query_params.get(k)
            for k in allowed_filter_keys
            if self.request.query_params.get(k)
        }
        if filter_params:
            # Filter with allowed params
            queryset = queryset.filter(**filter_params)

        return queryset.order_by(self.request.query_params.get("order_by", "id"))
