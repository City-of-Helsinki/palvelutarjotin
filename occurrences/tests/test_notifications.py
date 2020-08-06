from unittest.mock import patch

import pytest
from django.core import mail
from occurrences.consts import NOTIFICATION_TYPE_ALL, NOTIFICATION_TYPE_SMS
from occurrences.factories import StudyGroupFactory
from occurrences.models import Enrolment
from organisations.factories import PersonFactory

from common.tests.utils import assert_mails_match_snapshot


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
    Enrolment.objects.create(study_group=study_group, occurrence=occurrence)
    occurrence.study_groups.remove(study_group)
    # Test notification language
    en_study_group = StudyGroupFactory(person=PersonFactory(language="en"))
    Enrolment.objects.create(study_group=en_study_group, occurrence=occurrence)
    occurrence.study_groups.remove(en_study_group)
    assert len(mail.outbox) == 4
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
@patch("occurrences.utils.notification_service.send_sms")
def test_occurrence_enrolment_notification_sms_only(
    mock_send_sms,
    snapshot,
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
        notification_type=NOTIFICATION_TYPE_SMS,
    )
    occurrence.study_groups.remove(study_group)
    assert len(mail.outbox) == 0
    assert mock_send_sms.call_count == 2


@pytest.mark.django_db
@patch("occurrences.utils.notification_service.send_sms")
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
    )
    occurrence.study_groups.remove(study_group)
    assert len(mail.outbox) == 2
    assert mock_send_sms.call_count == 2


@pytest.mark.django_db
def test_approve_enrolment_notification_email(
    mock_get_event_data,
    notification_template_enrolment_approved_en,
    notification_template_enrolment_approved_fi,
    snapshot,
    occurrence,
    study_group,
):
    enrolment = Enrolment.objects.create(
        study_group=study_group, occurrence=occurrence,
    )
    enrolment.approve(custom_message="custom message")
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_decline_enrolment_notification_email(
    mock_get_event_data,
    notification_template_enrolment_declined_en,
    notification_template_enrolment_declined_fi,
    snapshot,
    occurrence,
    study_group,
):
    enrolment = Enrolment.objects.create(
        study_group=study_group, occurrence=occurrence,
    )
    enrolment.decline(custom_message="custom message")
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)
