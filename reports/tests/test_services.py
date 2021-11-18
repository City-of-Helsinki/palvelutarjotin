import pytest
import reports.services as report_services
from freezegun import freeze_time
from occurrences.factories import EnrolmentFactory
from occurrences.models import Enrolment
from reports.factories import EnrolmentReportFactory
from reports.models import EnrolmentReport


@pytest.mark.django_db
def test_sync_enrolment_reports_initializes_reports_table(mock_get_event_data):
    EnrolmentFactory.create_batch(10)
    report_services.sync_enrolment_reports()
    EnrolmentReport.objects.all().count() == 10


@pytest.mark.django_db
def test_sync_enrolment_reports_makes_full_sync(mock_get_event_data):
    """ it fully syncs (creates and updates) the enrolment report with enrolments"""
    with freeze_time("2020-01-01"):
        enrolments = EnrolmentFactory.create_batch(10, status=Enrolment.STATUS_PENDING)
        for e in enrolments:
            EnrolmentReportFactory(enrolment=e)
        assert (
            EnrolmentReport.objects.filter(
                enrolment_status=Enrolment.STATUS_PENDING
            ).count()
            == 10
        )
    with freeze_time("2020-01-02"):
        for e in enrolments:
            e.status = Enrolment.STATUS_APPROVED
            e.save()
        EnrolmentFactory.create_batch(10, status=Enrolment.STATUS_APPROVED)

    report_services.sync_enrolment_reports()
    assert (
        EnrolmentReport.objects.filter(
            enrolment_status=Enrolment.STATUS_APPROVED
        ).count()
        == 20
    )
