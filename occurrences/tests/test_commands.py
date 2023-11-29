import json
import pytest
import responses
from dateutil.relativedelta import relativedelta
from django.core.management import call_command
from django.test import override_settings
from django.utils import timezone
from django.utils.timezone import localtime
from io import StringIO

from occurrences.consts import NOTIFICATION_TYPE_SMS
from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from occurrences.models import Enrolment, PalvelutarjotinEvent
from occurrences.notification_services import notification_service
from organisations.factories import PersonFactory


@pytest.mark.django_db
def test_delete_retention_period_exceeding_contact_info_command(mock_get_event_data):
    too_old_1 = timezone.now() - relativedelta(months=24, days=1, minutes=60)
    too_old_2 = timezone.now() - relativedelta(months=24, days=1)
    still_valid_1 = timezone.now() - relativedelta(months=24, days=-1)
    still_valid_2 = timezone.now() - relativedelta(months=24, days=-1, minutes=60)
    output = StringIO()

    # ### CONTACT INFO SHOULD BE DELETED FROM THESE 2

    event_1 = PalvelutarjotinEventFactory()
    OccurrenceFactory(p_event=event_1, start_time=too_old_1, end_time=too_old_2)

    event_2 = PalvelutarjotinEventFactory()
    PalvelutarjotinEvent.objects.filter(pk=event_2.pk).update(created_at=too_old_1)

    # ### THESE 5 SHOULD NOT BE AFFECTED

    event_3 = PalvelutarjotinEventFactory()
    OccurrenceFactory(p_event=event_3, start_time=still_valid_1, end_time=still_valid_2)

    event_4 = PalvelutarjotinEventFactory()
    OccurrenceFactory(p_event=event_4, start_time=too_old_1, end_time=still_valid_1)

    event_5 = PalvelutarjotinEventFactory()
    PalvelutarjotinEvent.objects.filter(pk=event_5.pk).update(
        contact_info_deleted_at=timezone.now()
    )
    OccurrenceFactory(p_event=event_5, start_time=too_old_1, end_time=too_old_2)

    event_6 = PalvelutarjotinEventFactory()
    OccurrenceFactory(p_event=event_6, start_time=too_old_1, end_time=too_old_2)
    OccurrenceFactory(p_event=event_6, start_time=still_valid_1, end_time=still_valid_2)

    event_7 = PalvelutarjotinEventFactory()
    PalvelutarjotinEvent.objects.filter(pk=event_7.pk).update(created_at=still_valid_1)

    call_command("delete_retention_period_exceeding_contact_info", stdout=output)

    events_with_deleted_contact_info = PalvelutarjotinEvent.objects.filter(
        contact_info_deleted_at__isnull=False
    )
    assert events_with_deleted_contact_info.count() == 3
    assert event_1 in events_with_deleted_contact_info
    assert event_2 in events_with_deleted_contact_info
    # this had already contact_info_deleted_at set
    assert event_5 in events_with_deleted_contact_info

    output.seek(0)
    assert "Deleted contact info from 2 event(s)" in output.read()

    # Run the command again, expect no events to be affected
    call_command("delete_retention_period_exceeding_contact_info", stdout=output)
    output.seek(0)
    assert "No events are exceeding the retention period." in output.read()


@override_settings(NOTIFICATION_SERVICE_SMS_ENABLED=True)
@pytest.mark.django_db
@pytest.mark.parametrize(
    "enrolment_status,days,expected_sms_count",
    [
        # Only approved enrolments should be reminded of
        (Enrolment.STATUS_PENDING, 0, 0),
        (Enrolment.STATUS_CANCELLED, 0, 0),
        (Enrolment.STATUS_DECLINED, 0, 0),
        # Expected SMS count is double the enrolment count because
        # one SMS for study_group.person and another for enrolment.person
        (Enrolment.STATUS_APPROVED, 0, 3 * 2),  # 1st day's enrolments x 2
        (Enrolment.STATUS_APPROVED, 1, 4 * 2),  # 2nd day's enrolments x 2
        (Enrolment.STATUS_APPROVED, 2, 5 * 2),  # 3rd day's enrolments x 2
        (Enrolment.STATUS_APPROVED, 3, 6 * 2),  # 4th day's enrolments x 2
        (Enrolment.STATUS_APPROVED, 4, 7 * 2),  # 5th day's enrolments x 2
    ],
)
def test_send_upcoming_occurrence_sms_reminders_command_count(
    mocked_responses,
    mock_get_event_data,
    notification_sms_template_occurrence_upcoming_en,
    notification_sms_template_occurrence_upcoming_fi,
    notification_sms_template_occurrence_upcoming_sv,
    enrolment_status: str,
    days: int,
    expected_sms_count: int,
):
    """
    Test send_upcoming_occurrence_sms_reminders command's sent SMS count
    """
    mocked_responses.assert_all_requests_are_fired = expected_sms_count > 0
    today = localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    start_times = [
        # 1st day: 3 occurrences
        today + relativedelta(days=0),
        today + relativedelta(days=0, hours=1),
        today + relativedelta(days=0, hours=23, minutes=59),
        # 2nd day: 4 occurrences
        today + relativedelta(days=1),
        today + relativedelta(days=1, hours=1),
        today + relativedelta(days=1, hours=2),
        today + relativedelta(days=1, hours=23, minutes=59),
        # 3rd day: 5 occurrences
        today + relativedelta(days=2),
        today + relativedelta(days=2, hours=1),
        today + relativedelta(days=2, hours=2),
        today + relativedelta(days=2, hours=3),
        today + relativedelta(days=2, hours=23, minutes=59),
        # 4th day: 6 occurrences
        today + relativedelta(days=3),
        today + relativedelta(days=3, hours=1),
        today + relativedelta(days=3, hours=2),
        today + relativedelta(days=3, hours=3),
        today + relativedelta(days=3, hours=4),
        today + relativedelta(days=3, hours=23, minutes=59),
        # 5th day: 7 occurrences
        today + relativedelta(days=4),
        today + relativedelta(days=4, hours=1),
        today + relativedelta(days=4, hours=2),
        today + relativedelta(days=4, hours=3),
        today + relativedelta(days=4, hours=4),
        today + relativedelta(days=4, hours=5),
        today + relativedelta(days=4, hours=23, minutes=59),
    ]

    for start_time in start_times:
        occurrence = OccurrenceFactory(
            start_time=start_time, end_time=start_time + relativedelta(days=1)
        )
        EnrolmentFactory(
            occurrence=occurrence,
            notification_type=NOTIFICATION_TYPE_SMS,
            status=enrolment_status,
        )

    mocked_responses.add(
        responses.POST,
        url=notification_service.url,
        body="{}",
        status=200,
        content_type="application/json",
    )

    call_command("send_upcoming_occurrence_sms_reminders", days=days)

    assert len(mocked_responses.calls) == expected_sms_count


@override_settings(NOTIFICATION_SERVICE_SMS_ENABLED=True)
@pytest.mark.django_db
@pytest.mark.parametrize(
    "language,expected_sent_message",
    [
        (
            "fi",
            (
                "Muistathan ilmoittautumisesi tapahtumaan "
                "Raija Malka & Kaija Saariaho: Blick. "
                "04.01.2020 klo 02.00. "  # Timezone offset is +2 hours
                "Test study group unit name. "
                "Mikäli et pääse paikalle, peruutathan varauksesi sähköpostilla: "
                "contact_email@example.org."
            ),
        ),
        (
            "en",
            (
                "Please remember your enrolment for "
                "Raija Malka & Kaija Saariaho: Blick. "
                "04.01.2020 at 02.00. "  # Timezone offset is +2 hours
                "Test study group unit name. "
                "If you are unable to attend, please cancel your place by email: "
                "contact_email@example.org."
            ),
        ),
        (
            "sv",
            (
                "Kom ihåg din anmälan till evenemanget "
                "Raija Malka & Kaija Saariaho: Blick. "  #
                "04.01.2020 kl 02.00. "  # Timezone offset is +2 hours
                "Test study group unit name. "
                "Om du inte kan delta, vänligen avboka din bokning via e-post: "
                "contact_email@example.org."
            ),
        ),
    ],
)
def test_send_upcoming_occurrence_sms_reminders_command_content(
    mocked_responses,
    mock_get_event_data,
    notification_sms_template_occurrence_upcoming_en,
    notification_sms_template_occurrence_upcoming_fi,
    notification_sms_template_occurrence_upcoming_sv,
    language: str,
    expected_sent_message: str,
):
    """
    Test send_upcoming_occurrence_sms_reminders command's sent SMS content
    """
    person = PersonFactory(
        name="Test person name",
        phone_number="123456789",
        language=language,
    )
    study_group = StudyGroupFactory(
        group_name="Test study group name",
        unit_name="Test study group unit name",
        person=person,
    )
    event = PalvelutarjotinEventFactory(
        contact_email="contact_email@example.org",
        contact_person=person,
    )
    occurrence = OccurrenceFactory(
        p_event=event,
        start_time=localtime(),
        end_time=localtime() + relativedelta(days=1),
    )
    EnrolmentFactory(
        occurrence=occurrence,
        notification_type=NOTIFICATION_TYPE_SMS,
        status=Enrolment.STATUS_APPROVED,
        study_group=study_group,
        person=person,
    )

    mocked_responses.add(
        responses.POST,
        url=notification_service.url,
        body="{}",
        status=200,
        content_type="application/json",
    )

    call_command("send_upcoming_occurrence_sms_reminders", days=0)

    assert len(mocked_responses.calls) == 1
    sent_body = json.loads(mocked_responses.calls[0].request.body)
    assert (len(sent_body["to"])) == 1
    assert sent_body["to"][0]["destination"] == person.phone_number
    assert sent_body["text"] == expected_sent_message
