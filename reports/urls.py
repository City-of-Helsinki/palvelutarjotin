from django.urls import path
from reports.views import OrganisationPersonsAdminView, OrganisationPersonsCsvView

urlpatterns = [
    path(
        "organisation/persons/",
        OrganisationPersonsAdminView.as_view(),
        name="report_organisation_persons",
    ),
    path(
        "organisation/persons/csv/",
        OrganisationPersonsCsvView.as_view(),
        name="report_organisation_persons_csv",
    ),
]
