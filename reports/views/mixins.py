import datetime
import logging
from typing import Optional

from auditlog.context import set_actor
from auditlog.signals import accessed
from django.contrib import messages
from django.db.models.query import Prefetch
from django.utils.translation import gettext as _

from common.utils import (
    get_client_ip,
    get_node_id_from_global_id,
)
from occurrences.models import Enrolment
from organisations.models import Organisation, Person

logger = logging.getLogger(__name__)


def naive_datetime_to_tz_aware(datetime: str) -> Optional[str]:
    return datetime + "T00:00:00.000Z" if datetime else None


class LogAccessMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        # write access logs to auditlog
        with set_actor(
            actor=self.request.user, remote_addr=get_client_ip(self.request)
        ):
            for obj in queryset:
                accessed.send(sender=obj.__class__, instance=obj)
        return queryset


class ExportReportViewMixin:
    """
    Pass a list of selected objects in the GET query string (ids-parameter):
    example:
        return HttpResponseRedirect(
            "/reports/organisation/persons?ids=%s"
            % (",".join(str(pk) for pk in selected),)
        )
    """

    def _convert_id_value(self, value):
        try:
            return int(value)
        except ValueError:
            return value

    def get_queryset(self):
        # Get URL parameter as a string, if exists
        ids = self.request.GET.get("ids", None)
        # Get organisations for ids if they exist
        if ids is not None:
            # Convert parameter string to list of integers
            ids = [self._convert_id_value(x) for x in ids.split(",")]
            # Get objects for all parameter ids
            queryset = self.model.objects.filter(pk__in=ids)
        else:
            # Else no parameters, return all objects
            queryset = self.model.objects.all()

        return queryset


class PersonsMixin(ExportReportViewMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related(
            Prefetch(
                "organisations",
                queryset=Organisation.objects.all().order_by("name"),
            )
        )


class OrganisationPersonsMixin(ExportReportViewMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
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
            today = datetime.datetime.now(tz=datetime.timezone.utc)
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
