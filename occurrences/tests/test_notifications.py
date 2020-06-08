import pytest
from django.core import mail
from occurrences.consts import NotificationType
from occurrences.models import Enrolment

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


@pytest.mark.django_db
def test_occurrence_enrolment_notifications(
    snapshot,
    user_api_client,
    notification_template_occurrence_unenrolment_fi,
    notification_template_occurrence_enrolment_fi,
    mock_get_event_data,
    occurrence,
    study_group,
):
    Enrolment.objects.create(study_group=study_group, occurrence=occurrence)
    occurrence.study_groups.remove(study_group)
    assert len(mail.outbox) == 2
    assert_mails_match_snapshot(snapshot)
