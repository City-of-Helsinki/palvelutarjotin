import csv
import datetime
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.query import Prefetch
from django.http.response import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.views.generic.base import View
from occurrences.models import Enrolment, PalvelutarjotinEvent
from organisations.models import Organisation, Person

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
        queryset = super(OrganisationPersonsMixin, self).get_queryset()
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
            event_ids = [int(x) for x in event_ids.split(",")]
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
        ).select_related("occurrence__p_event", "study_group")[: self.max_results]


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
        context = super(OrganisationPersonsAdminView, self).get_context_data(**kwargs)
        context["opts"] = self.model._meta
        return context


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

        return super(PalvelutarjotinEventEnrolmentsAdminView, self).get(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super(PalvelutarjotinEventEnrolmentsAdminView, self).get_context_data(
            **kwargs
        )
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


@method_decorator(staff_member_required, name="dispatch")
class ExportReportCsvView(ExportReportViewMixin, View):
    """
    A generic way to create csv reports from models.
    """

    model = None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response


@method_decorator(staff_member_required, name="dispatch")
class OrganisationPersonsCsvView(OrganisationPersonsMixin, ExportReportCsvView):
    """
    A csv of organisations persons.
    """

    model = Organisation

    def get(self, request, *args, **kwargs):

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(
            "kultus_organisations_persons"
        )
        writer = csv.writer(response)

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


@method_decorator(staff_member_required, name="dispatch")
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

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(
            "kultus_events_approved_enrolments"
        )
        writer = csv.writer(response)

        writer.writerow(
            [
                _("LinkedEvents id"),
                _("LinkedEvents uri"),
                _("Occurrence starting (date)"),
                _("Enrolment date"),
                _("Group name"),
                _("Study levels"),
                _("Amount of children"),
                _("Amount of adults"),
            ]
        )
        for enrolment in self.get_queryset():
            writer.writerow(
                [
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
                ]
            )
        return response
