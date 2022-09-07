import pytest
import pytz
from datetime import datetime, timedelta
from django.core import mail
from django.utils import timezone
from graphql_relay import to_global_id
from unittest.mock import patch

from common.tests.utils import assert_mails_match_snapshot
from occurrences.consts import NOTIFICATION_TYPE_ALL, NOTIFICATION_TYPE_SMS
from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from occurrences.models import Enrolment
from occurrences.tests.test_api import MASS_APPROVE_ENROLMENTS_MUTATION
from organisations.factories import PersonFactory


@pytest.mark.django_db
def test_occurrence_enrolment_notifications_email_only(
    snapshot,
    notification_template_occurrence_unenrolment_fi,
    notification_template_occurrence_enrolment_fi,
    notification_template_occurrence_unenrolment_en,
    notification_template_occurrence_enrolment_en,
    mock_get_event_data,
    occurrence,
    study_group,
):
    EnrolmentFactory(
        study_group=study_group, occurrence=occurrence, person=study_group.person
    )
    occurrence.study_groups.remove(study_group)
    # Test notification language
    en_study_group = StudyGroupFactory(person=PersonFactory(language="en"))
    EnrolmentFactory(
        study_group=en_study_group, occurrence=occurrence, person=study_group.person
    )
    occurrence.study_groups.remove(en_study_group)
    assert len(mail.outbox) == 4
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "sms_service_enabled",
    [True, False],
)
@patch("occurrences.services.notification_service.send_sms")
def test_occurrence_enrolment_notification_sms_only(
    mock_send_sms,
    sms_service_enabled,
    settings,
    snapshot,
    notification_sms_template_occurrence_enrolment_en,
    notification_sms_template_occurrence_enrolment_fi,
    notification_sms_template_occurrence_unenrolment_en,
    notification_sms_template_occurrence_unenrolment_fi,
    mock_get_event_data,
    occurrence,
    study_group,
    caplog,
):
    settings.NOTIFICATION_SERVICE_SMS_ENABLED = sms_service_enabled
    EnrolmentFactory(
        study_group=study_group,
        occurrence=occurrence,
        notification_type=NOTIFICATION_TYPE_SMS,
        person=study_group.person,
    )
    occurrence.study_groups.remove(study_group)
    assert len(mail.outbox) == 0
    if sms_service_enabled:
        assert mock_send_sms.call_count == 2
    else:
        # The SMS are not sent if the service is disabled
        assert mock_send_sms.call_count == 0
        # assert "Not sending SMS, because the service disabled." in caplog.text


@pytest.mark.django_db
@patch("occurrences.services.notification_service.send_sms")
def test_occurrence_enrolment_notification_sms_and_email(
    mock_send_sms,
    snapshot,
    notification_template_occurrence_unenrolment_fi,
    notification_template_occurrence_enrolment_fi,
    notification_template_occurrence_unenrolment_en,
    notification_template_occurrence_enrolment_en,
    notification_sms_template_occurrence_enrolment_en,
    notification_sms_template_occurrence_enrolment_fi,
    notification_sms_template_occurrence_unenrolment_en,
    notification_sms_template_occurrence_unenrolment_fi,
    mock_get_event_data,
    occurrence,
    study_group,
):
    Enrolment.objects.create(
        study_group=study_group,
        occurrence=occurrence,
        notification_type=NOTIFICATION_TYPE_ALL,
        person=study_group.person,
    )
    occurrence.study_groups.remove(study_group)
    assert len(mail.outbox) == 2
    assert mock_send_sms.call_count == 2


@pytest.mark.django_db
def test_approve_enrolment_notification_email(
    mock_get_event_data,
    mock_enrolment_unique_id,
    notification_template_enrolment_approved_en,
    notification_template_enrolment_approved_fi,
    snapshot,
):
    study_group = StudyGroupFactory(group_size=5)
    occurrence = OccurrenceFactory(amount_of_seats=10)
    enrolment = EnrolmentFactory(
        study_group=study_group, occurrence=occurrence, person=study_group.person
    )
    p_event = occurrence.p_event
    # To test the cancel link generated only if event only requires 1 occurrence per
    # enrolment
    p_event.needed_occurrences = 1
    p_event.save()
    enrolment.approve(custom_message="custom message")
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_decline_enrolment_notification_email(
    mock_get_event_data,
    mock_enrolment_unique_id,
    notification_template_enrolment_declined_en,
    notification_template_enrolment_declined_fi,
    snapshot,
    occurrence,
    study_group,
):
    enrolment = EnrolmentFactory(
        study_group=study_group, occurrence=occurrence, person=study_group.person
    )
    enrolment.decline(custom_message="custom message")
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_cancel_enrolment_notification_email(
    mock_get_event_data,
    mock_enrolment_unique_id,
    notification_template_enrolment_cancellation_confirmation_en,
    notification_template_enrolment_cancellation_confirmation_fi,
    snapshot,
    occurrence,
    study_group,
):
    enrolment = EnrolmentFactory(
        study_group=study_group, occurrence=occurrence, person=study_group.person
    )
    enrolment.ask_cancel_confirmation(custom_message="custom message")
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_cancelled_enrolment_notification_email(
    mock_get_event_data,
    notification_template_enrolment_cancelled_en,
    notification_template_enrolment_cancelled_fi,
    snapshot,
    occurrence,
    study_group,
):
    person = PersonFactory(email_address="email_me@dommain.com")
    study_group = StudyGroupFactory(person=person)
    enrolment = EnrolmentFactory(
        study_group=study_group, occurrence=occurrence, person=person
    )
    enrolment.cancel(custom_message="custom message")
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_occurrence_enrolment_notifications_to_contact_person(
    snapshot,
    notification_template_occurrence_unenrolment_fi,
    notification_template_occurrence_enrolment_fi,
    notification_template_occurrence_unenrolment_en,
    notification_template_occurrence_enrolment_en,
    mock_get_event_data,
    occurrence,
    study_group,
):
    contact_person = PersonFactory(email_address="email_me@dommain.com")
    Enrolment.objects.create(
        study_group=study_group, occurrence=occurrence, person=contact_person
    )
    occurrence.study_groups.remove(study_group)
    # Test notification language
    en_study_group = StudyGroupFactory(
        person=PersonFactory(language="en", email_address="do_not_email_me@domain.com")
    )
    Enrolment.objects.create(
        study_group=en_study_group, occurrence=occurrence, person=contact_person
    )
    occurrence.study_groups.remove(en_study_group)
    assert len(mail.outbox) == 4
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_cancel_occurrence_notification(
    snapshot,
    mock_get_event_data,
    occurrence,
    notification_template_cancel_occurrence_en,
    notification_template_cancel_occurrence_fi,
):
    for status in Enrolment.STATUSES:
        for s in StudyGroupFactory.create_batch(2):
            EnrolmentFactory(
                study_group=s, occurrence=occurrence, person=s.person, status=status[0]
            )
    notifiable_enrolments_count = occurrence.enrolments.all().count() - (
        occurrence.enrolments.filter(
            status__in=[Enrolment.STATUS_CANCELLED, Enrolment.STATUS_DECLINED]
        ).count()
    )
    occurrence.cancel(reason="Occurrence cancel reason")
    # Cancellation messages should not be sent to enrolments
    # that are already cancelled or declined.
    assert len(mail.outbox) == notifiable_enrolments_count
    assert_mails_match_snapshot(snapshot)


@pytest.mark.parametrize(
    "tz",
    [pytz.timezone("Europe/Helsinki"), pytz.utc, pytz.timezone("US/Eastern")],
)
@pytest.mark.django_db
def test_local_time_notification(
    tz,
    snapshot,
    mock_get_event_data,
    notification_template_occurrence_enrolment_en,
    notification_template_occurrence_enrolment_fi,
    study_group,
):
    dt = datetime.now()
    occurrence = OccurrenceFactory(start_time=dt.astimezone(tz))
    EnrolmentFactory(
        study_group=study_group, occurrence=occurrence, person=study_group.person
    )
    # Different timezone should result same localtime in email
    assert_mails_match_snapshot(snapshot)


@pytest.mark.parametrize(
    "auto_acceptance",
    [True, False],
)
@pytest.mark.django_db
def test_only_send_approved_notification(
    auto_acceptance,
    snapshot,
    mock_get_event_data,
    notification_template_occurrence_enrolment_en,
    notification_template_enrolment_approved_en,
    notification_template_occurrence_enrolment_fi,
    notification_template_enrolment_approved_fi,
):
    study_group = StudyGroupFactory(group_size=5)
    occurrence = OccurrenceFactory(
        p_event__auto_acceptance=auto_acceptance, amount_of_seats=10
    )
    enrol = EnrolmentFactory(
        study_group=study_group, occurrence=occurrence, person=study_group.person
    )
    assert len(mail.outbox) == (0 if auto_acceptance else 1)
    # Fake auto approval because it can only be triggered from approve mutation
    enrol.approve()
    assert len(mail.outbox) == (1 if auto_acceptance else 2)
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_send_enrolment_summary_report(
    snapshot,
    mock_get_event_data,
    notification_template_enrolment_summary_report_fi,
):
    date_in_future = datetime.now() + timedelta(days=10)
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

    EnrolmentFactory.create(status=Enrolment.STATUS_APPROVED, occurrence=occurrence_1_1)
    EnrolmentFactory.create_batch(
        3, status=Enrolment.STATUS_PENDING, occurrence=occurrence_1_1
    )
    EnrolmentFactory.create(status=Enrolment.STATUS_PENDING, occurrence=occurrence_1_2)
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

    EnrolmentFactory.create(status=Enrolment.STATUS_PENDING, occurrence=occurrence_2_1)
    EnrolmentFactory.create(status=Enrolment.STATUS_PENDING, occurrence=occurrence_2_2)

    # Event with same contact person with event 2
    p_event_3 = PalvelutarjotinEventFactory.create(
        contact_email=p_event_2.contact_email
    )
    occurrence_3_1 = OccurrenceFactory.create(
        id=31, p_event=p_event_3, start_time=date_in_future
    )
    EnrolmentFactory.create(status=Enrolment.STATUS_PENDING, occurrence=occurrence_3_1)

    # Event with auto_acceptance is True
    p_event_4 = PalvelutarjotinEventFactory.create(
        auto_acceptance=True, contact_email=p_event_2.contact_email
    )
    occurrence_4_1 = OccurrenceFactory.create(
        id=41, p_event=p_event_4, start_time=date_in_future
    )
    EnrolmentFactory.create(status=Enrolment.STATUS_APPROVED, occurrence=occurrence_4_1)
    old_enrolment = EnrolmentFactory.create(
        status=Enrolment.STATUS_APPROVED, occurrence=occurrence_4_1
    )
    old_enrolment.enrolment_time = timezone.now() - timedelta(days=10)
    old_enrolment.save()
    Enrolment.send_enrolment_summary_report_to_providers()
    assert len(mail.outbox) == 2
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_old_pending_enrolments_excluded_from_enrolment_summary_report(
    mock_get_event_data, notification_template_enrolment_summary_report_fi
):
    occurrence = OccurrenceFactory.create(start_time=datetime.now() - timedelta(days=1))
    EnrolmentFactory.create(status=Enrolment.STATUS_PENDING, occurrence=occurrence)
    Enrolment.send_enrolment_summary_report_to_providers()
    assert len(mail.outbox) == 0

    occurrence = OccurrenceFactory.create(start_time=datetime.now() + timedelta(days=1))
    EnrolmentFactory.create(status=Enrolment.STATUS_PENDING, occurrence=occurrence)
    Enrolment.send_enrolment_summary_report_to_providers()
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_event_not_found_from_linkedevents_when_sending_enrolment_summary_report(
    mock_get_event_data_not_found, notification_template_enrolment_summary_report_fi
):
    occurrence = OccurrenceFactory.create(start_time=datetime.now() + timedelta(days=1))
    EnrolmentFactory.create(status=Enrolment.STATUS_PENDING, occurrence=occurrence)
    Enrolment.send_enrolment_summary_report_to_providers()
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_decline_enrolment_notification_email_to_multiple_contact_person(
    mock_get_event_data,
    notification_template_enrolment_declined_en,
    notification_template_enrolment_declined_fi,
    snapshot,
    occurrence,
    study_group,
):
    # Single contact person
    enrolment = EnrolmentFactory(
        study_group=study_group, occurrence=occurrence, person=study_group.person
    )
    enrolment.decline(custom_message="custom message")
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)
    # Enrolment of two different contact person
    enrolment_2 = EnrolmentFactory()
    enrolment_2.decline(custom_message="custom message")
    assert len(mail.outbox) == 3
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_mass_approve_enrolment_mutation(
    snapshot,
    staff_api_client,
    mock_get_event_data,
    mock_enrolment_unique_id,
    notification_template_enrolment_approved_en,
    notification_template_enrolment_approved_fi,
):
    occurrence = OccurrenceFactory(
        p_event__needed_occurrences=1,
        p_event__auto_acceptance=False,
        amount_of_seats=100,
    )
    enrolment_1 = EnrolmentFactory(occurrence=occurrence, study_group__group_size=10)
    enrolment_2 = EnrolmentFactory(occurrence=occurrence, study_group__group_size=10)
    enrolment_3 = EnrolmentFactory(occurrence=occurrence, study_group__group_size=10)
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    staff_api_client.execute(
        MASS_APPROVE_ENROLMENTS_MUTATION,
        variables={
            "input": {
                "enrolmentIds": [
                    to_global_id("EnrolmentNode", enrolment_1.id),
                    to_global_id("EnrolmentNode", enrolment_2.id),
                    to_global_id("EnrolmentNode", enrolment_3.id),
                ],
                "customMessage": "Custom message",
            }
        },
    )

    # Two people got email for each enrolment
    # (study group contact person & enrolment teacher)
    assert len(mail.outbox) == 6
    assert_mails_match_snapshot(snapshot)
