from datetime import timedelta

import pytest
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
)
from occurrences.models import Enrolment


@pytest.mark.usefixtures(
    "mock_get_event_data", "notification_template_enrolment_summary_report_fi"
)
@pytest.mark.django_db
class CommandsTestCase(TestCase):
    def setUp(self) -> None:
        date_in_future = timezone.now() + timedelta(days=10)
        p_event_1 = PalvelutarjotinEventFactory.create()
        occurrence_1_1 = OccurrenceFactory.create(
            id=11, p_event=p_event_1, start_time=date_in_future
        )
        occurrence_1_2 = OccurrenceFactory.create(
            id=12, p_event=p_event_1, start_time=date_in_future
        )
        occurrence_1_3 = OccurrenceFactory.create(
            id=13, p_event=p_event_1, start_time=date_in_future
        )

        EnrolmentFactory.create(
            status=Enrolment.STATUS_APPROVED, occurrence=occurrence_1_1
        )
        EnrolmentFactory.create_batch(
            3, status=Enrolment.STATUS_PENDING, occurrence=occurrence_1_1
        )
        EnrolmentFactory.create(
            status=Enrolment.STATUS_PENDING, occurrence=occurrence_1_2
        )
        EnrolmentFactory.create(
            status=Enrolment.STATUS_CANCELLED, occurrence=occurrence_1_3
        )

        p_event_2 = PalvelutarjotinEventFactory.create()
        occurrence_2_1 = OccurrenceFactory.create(
            id=21, p_event=p_event_2, start_time=date_in_future
        )
        occurrence_2_2 = OccurrenceFactory.create(
            id=22, p_event=p_event_2, start_time=date_in_future
        )

        EnrolmentFactory.create(
            status=Enrolment.STATUS_PENDING, occurrence=occurrence_2_1
        )
        EnrolmentFactory.create(
            status=Enrolment.STATUS_PENDING, occurrence=occurrence_2_2
        )

        # Event with same contact person with event 2
        p_event_3 = PalvelutarjotinEventFactory.create(
            contact_email=p_event_2.contact_email
        )
        occurrence_3_1 = OccurrenceFactory.create(
            id=31, p_event=p_event_3, start_time=date_in_future
        )
        EnrolmentFactory.create(
            status=Enrolment.STATUS_PENDING, occurrence=occurrence_3_1
        )

        # Event with auto_acceptance is True
        p_event_4 = PalvelutarjotinEventFactory.create(
            auto_acceptance=True, contact_email=p_event_2.contact_email
        )
        occurrence_4_1 = OccurrenceFactory.create(
            id=41, p_event=p_event_4, start_time=date_in_future
        )
        EnrolmentFactory.create(
            status=Enrolment.STATUS_APPROVED, occurrence=occurrence_4_1
        )
        old_enrolment = EnrolmentFactory.create(
            status=Enrolment.STATUS_APPROVED, occurrence=occurrence_4_1
        )
        old_enrolment.enrolment_time = timezone.now() - timedelta(days=10)
        old_enrolment.save()

    def test_send_enrolment_summary(self):
        args = []
        opts = {}
        with self.settings(ENABLE_SUMMARY_REPORT=True):
            call_command("send_enrolment_summary", *args, **opts)
            assert len(mail.outbox) == 2
