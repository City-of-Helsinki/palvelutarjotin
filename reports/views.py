import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.query import Prefetch
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.views.generic.base import View
from organisations.models import Organisation, Person


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

        meta = self.model._meta

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
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
