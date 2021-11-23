from django.urls import path
from reports.views import (
    EnrolmentReportCsvView,
    EnrolmentReportListView,
    OrganisationPersonsAdminView,
    OrganisationPersonsCsvView,
    PalvelutarjotinEventEnrolmentsAdminView,
    PalvelutarjotinEventEnrolmentsCsvView,
    sync_enrolment_reports_view,
)

# Report views
urlpatterns = [
    path(
        "enrolmentreport/", EnrolmentReportListView.as_view(), name="enrolment_reports",
    ),
]

# Admin views
urlpatterns += [
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
    path(
        "enrolmentreport/sync_enrolment_reports/",
        sync_enrolment_reports_view,
        name="sync_enrolment_reports",
    ),
]

# Admin commands
urlpatterns += [
    path(
        "enrolmentreport/sync_enrolment_reports/",
        sync_enrolment_reports_view,
        name="sync_enrolment_reports",
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
    path(
        "enrolmentreports/csv/",
        EnrolmentReportCsvView.as_view(),
        name="report_enrolment_report_csv",
    ),
]
