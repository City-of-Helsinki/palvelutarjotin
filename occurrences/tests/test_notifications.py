import pytest
from django.core import mail
from occurrences.consts import NotificationType
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
        NotificationType.OCCURRENCE_ENROLMENT,
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
        NotificationType.OCCURRENCE_UNENROLMENT,
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
        NotificationType.OCCURRENCE_ENROLMENT,
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
        NotificationType.OCCURRENCE_UNENROLMENT,
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


@pytest.mark.django_db
def test_occurrence_enrolment_notifications(
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
