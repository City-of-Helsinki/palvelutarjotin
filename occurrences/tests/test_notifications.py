from unittest.mock import patch

import pytest
from django.core import mail
from occurrences.consts import (
    NOTIFICATION_TYPE_ALL,
    NOTIFICATION_TYPE_SMS,
    NotificationTemplate,
)
from occurrences.factories import StudyGroupFactory
from occurrences.models import Enrolment
from organisations.factories import PersonFactory

from common.tests.utils import (
    assert_mails_match_snapshot,
    create_notification_template_in_language,
)


@pytest.fixture
def notification_template_occurrence_enrolment_fi():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_ENROLMENT,
        "fi",
        subject="Occurrence enrolment FI",
        body_text="""
        Event FI: {{ event.name.fi }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_template_occurrence_unenrolment_fi():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UNENROLMENT,
        "fi",
        subject="Occurrence unenrolment FI",
        body_text="""
        Event FI: {{ event.name.fi }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_template_occurrence_enrolment_en():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_ENROLMENT,
        "en",
        subject="Occurrence enrolment EN",
        body_text="""
        Event EN: {{ event.name.en }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_template_occurrence_unenrolment_en():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UNENROLMENT,
        "en",
        subject="Occurrence unenrolment EN",
        body_text="""
        Event EN: {{ event.name.en }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_sms_template_occurrence_enrolment_en():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_ENROLMENT_SMS,
        "en",
        subject="Occurrence enrolment SMS EN",
        body_text="""
        Event EN: {{ event.name.en }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_sms_template_occurrence_unenrolment_en():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UNENROLMENT_SMS,
        "en",
        subject="Occurrence unenrolment SMS EN",
        body_text="""
        Event EN: {{ event.name.en }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_sms_template_occurrence_enrolment_fi():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_ENROLMENT_SMS,
        "fi",
        subject="Occurrence enrolment SMS FI",
        body_text="""
        Event FI: {{ event.name.fi }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_sms_template_occurrence_unenrolment_fi():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UNENROLMENT_SMS,
        "fi",
        subject="Occurrence unenrolment SMS FI",
        body_text="""
        Event FI: {{ event.name.fi }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_template_enrolment_approved_en():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_APPROVED,
        "en",
        subject="Enrolment approved EN",
        body_text="""
        Event EN: {{ event.name.en }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_template_enrolment_approved_fi():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_APPROVED,
        "fi",
        subject="Enrolment approved FI",
        body_text="""
        Event FI: {{ event.name.fi }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_template_enrolment_declined_en():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_DECLINED,
        "en",
        subject="Enrolment declined EN",
        body_text="""
        Event EN: {{ event.name.en }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


@pytest.fixture
def notification_template_enrolment_declined_fi():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_DECLINED,
        "fi",
        subject="Enrolment declined FI",
        body_text="""
        Event FI: {{ event.name.fi }}
        Extra event info: {{ occurrence.p_event.linked_event_id }}
        Study group: {{ study_group.name }}
        Occurrence: {{ occurrence.start_time }}
        Person: {{ study_group.person.email_address}}
""",
    )


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
    enrolment.approve()
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
    enrolment.decline()
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)
