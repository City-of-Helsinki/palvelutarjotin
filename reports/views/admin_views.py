import logging

from auditlog.context import set_actor
from auditlog.signals import accessed
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Min
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from common.utils import (
    get_client_ip,
)
from occurrences.models import Enrolment, PalvelutarjotinEvent
from organisations.models import Organisation, Person
from reports.services import sync_enrolment_reports
from reports.views.mixins import (
    LogAccessMixin,
    OrganisationPersonsMixin,
    PalvelutarjotinEventEnrolmentsMixin,
    PersonsMixin,
)

logger = logging.getLogger(__name__)


@staff_member_required
@require_http_methods(["POST"])
def sync_enrolment_reports_view(request):
    create_from = Enrolment.objects.aggregate(Min("enrolment_time"))[
        "enrolment_time__min"
    ]
    sync_enrolment_reports(hydrate_linkedevents_event=True, create_from=create_from)
    messages.add_message(request, messages.SUCCESS, _("Enrolment reports synced!"))
    return HttpResponseRedirect(reverse("admin:reports_enrolmentreport_changelist"))


@method_decorator(staff_member_required, name="dispatch")
class PersonsAdminView(LogAccessMixin, PersonsMixin, ListView):
    """
    The admin view which renders a table of organisations persons.
    """

    model = Person
    template_name = "reports/admin/persons.html"
    context_object_name = "persons"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["opts"] = self.model._meta
        return context

    # @staff_member_required
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@method_decorator(staff_member_required, name="dispatch")
class OrganisationPersonsAdminView(LogAccessMixin, OrganisationPersonsMixin, ListView):
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
        queryset = self.get_queryset()
        context["linked_events_root"] = settings.LINKED_EVENTS_API_CONFIG["ROOT"]
        context["total_children"] = sum(
            enrolment.study_group.group_size for enrolment in queryset
        )
        context["total_adults"] = sum(
            enrolment.study_group.amount_of_adult for enrolment in queryset
        )
        context["opts"] = self.model._meta

        with set_actor(
            actor=self.request.user, remote_addr=get_client_ip(self.request)
        ):
            for enrolment in queryset:
                accessed.send(sender=enrolment.__class__, instance=enrolment)

        return context
