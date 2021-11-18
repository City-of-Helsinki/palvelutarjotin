import pytest
from django.core.management import call_command
from django.test import TestCase
from occurrences.factories import EnrolmentFactory
from reports.models import EnrolmentReport


@pytest.mark.usefixtures("mock_get_event_data")
class CommandsTestCase(TestCase):
    def setUp(self) -> None:
        EnrolmentFactory()

    def test_sync_enrolment_reports(self):
        args = []
        opts = {}
        call_command("sync_enrolment_reports", *args, **opts)
        assert EnrolmentReport.objects.count() == 1

    def test_sync_enrolment_reports_with_including_sync_from_param(self):
        args = []
        opts = {"sync_from": ["2020-01-01"]}
        call_command("sync_enrolment_reports", *args, **opts)
        assert EnrolmentReport.objects.count() == 1

    def test_sync_enrolment_reports_with_excluding_sync_from_param(self):
        args = []
        opts = {"sync_from": ["2999-01-01"]}
        call_command("sync_enrolment_reports", *args, **opts)
        assert EnrolmentReport.objects.count() == 0
