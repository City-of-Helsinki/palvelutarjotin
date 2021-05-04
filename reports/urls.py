from django.urls import path
from reports.views import (
    OrganisationPersonsAdminView,
    OrganisationPersonsCsvView,
    PalvelutarjotinEventEnrolmentsAdminView,
    PalvelutarjotinEventEnrolmentsCsvView,
)

# Admin views
urlpatterns = [
    path(
        "organisation/persons/",
        OrganisationPersonsAdminView.as_view(),
        name="report_organisation_persons",
    ),
    path(
        "palvelutarjotinevent/enrolments/",
        PalvelutarjotinEventEnrolmentsAdminView.as_view(),
        name="report_event_enrolments",
    ),
]

# CSV views
urlpatterns += [
    path(
        "organisation/persons/csv/",
        OrganisationPersonsCsvView.as_view(),
        name="report_organisation_persons_csv",
    ),
    path(
        "palvelutarjotinevent/enrolments/csv/",
        PalvelutarjotinEventEnrolmentsCsvView.as_view(),
        name="report_event_enrolments_csv",
    ),
]
