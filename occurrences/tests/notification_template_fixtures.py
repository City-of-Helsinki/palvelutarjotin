import os

import pytest

from common.tests.utils import create_notification_template_in_language
from occurrences.consts import NotificationTemplate

DEFAULT_NOTIFICATION_BODY_TEXT_FI = """
    Event FI: {{ event.name.fi }}
    Extra event info: {{ occurrence.p_event.linked_event_id }}
    Study group: {{ study_group.unit_name }}
    {% if preview_mode %}
    Occurrence: {{ occurrence.start_time }}
    {% else %}
    Occurrence: {{ occurrence.local_start_time.strftime('%d.%m.%Y %H.%M') }}
    {% endif%}
    Person: {{ person.email_address}}
    {% if occurrence.p_event.needed_occurrences == 1 %}
    Click this link to cancel the enrolment:
    {{ enrolment.get_link_to_cancel_ui()}}
    {% endif %}
"""

NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI = (
    DEFAULT_NOTIFICATION_BODY_TEXT_FI
    + """
    {% if custom_message %}
    Custom message: {{ custom_message }}
    {% endif %}
"""
)

NOTIFICATION_WITH_CUSTOM_MESSAGE_HTML_FI = (
    "<p>" + NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI + "</p>"
)

DEFAULT_NOTIFICATION_BODY_TEXT_EN = """
    Event EN: {{ event.name.en }}
    Extra event info: {{ occurrence.p_event.linked_event_id }}
    Study group: {{ study_group.unit_name }}
    {% if preview_mode %}
    Occurrence: {{ occurrence.start_time }}
    {% else %}
    Occurrence: {{ occurrence.local_start_time.strftime('%d.%m.%Y %H.%M') }}
    {% endif%}
    Person: {{ study_group.person.email_address}}
"""

NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN = (
    DEFAULT_NOTIFICATION_BODY_TEXT_EN
    + """
    {% if custom_message %}
    Custom message: {{ custom_message }}
    {% endif %}
"""
)

NOTIFICATION_WITH_CUSTOM_MESSAGE_HTML_EN = (
    "<p>" + NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN + "</p>"
)


def load_sms_template(filename):
    sms_templates_dir = os.path.join(
        os.path.dirname(__file__), "../../notification_importers/templates/sms/"
    )
    return open(os.path.join(sms_templates_dir, filename), "rt", encoding="utf8").read()


OCCURRENCE_UPCOMING_SMS_EN = load_sms_template("occurrence_upcoming_sms-en.j2")
OCCURRENCE_UPCOMING_SMS_FI = load_sms_template("occurrence_upcoming_sms-fi.j2")
OCCURRENCE_UPCOMING_SMS_SV = load_sms_template("occurrence_upcoming_sms-sv.j2")


@pytest.fixture
def notification_sms_template_occurrence_upcoming_en():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UPCOMING_SMS,
        "en",
        subject="Occurrence upcoming SMS EN",
        body_text=OCCURRENCE_UPCOMING_SMS_EN,
    )


@pytest.fixture
def notification_sms_template_occurrence_upcoming_fi():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UPCOMING_SMS,
        "fi",
        subject="Occurrence upcoming SMS FI",
        body_text=OCCURRENCE_UPCOMING_SMS_FI,
    )


@pytest.fixture
def notification_sms_template_occurrence_upcoming_sv():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UPCOMING_SMS,
        "sv",
        subject="Occurrence upcoming SMS SV",
        body_text=OCCURRENCE_UPCOMING_SMS_SV,
    )


@pytest.fixture
def notification_template_occurrence_enrolment_fi():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_ENROLMENT,
        "fi",
        subject="Occurrence enrolment FI",
        body_text=DEFAULT_NOTIFICATION_BODY_TEXT_FI,
    )


@pytest.fixture
def notification_template_occurrence_unenrolment_fi():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UNENROLMENT,
        "fi",
        subject="Occurrence unenrolment FI",
        body_text=DEFAULT_NOTIFICATION_BODY_TEXT_FI,
    )


@pytest.fixture
def notification_template_occurrence_enrolment_en():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_ENROLMENT,
        "en",
        subject="Occurrence enrolment EN",
        body_text=DEFAULT_NOTIFICATION_BODY_TEXT_EN,
    )


@pytest.fixture
def notification_template_occurrence_unenrolment_en():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UNENROLMENT,
        "en",
        subject="Occurrence unenrolment EN",
        body_text=DEFAULT_NOTIFICATION_BODY_TEXT_EN,
    )


@pytest.fixture
def notification_sms_template_occurrence_enrolment_en():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_ENROLMENT_SMS,
        "en",
        subject="Occurrence enrolment SMS EN",
        body_text=DEFAULT_NOTIFICATION_BODY_TEXT_EN,
    )


@pytest.fixture
def notification_sms_template_occurrence_unenrolment_en():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UNENROLMENT_SMS,
        "en",
        subject="Occurrence unenrolment SMS EN",
        body_text=DEFAULT_NOTIFICATION_BODY_TEXT_EN,
    )


@pytest.fixture
def notification_sms_template_occurrence_enrolment_fi():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_ENROLMENT_SMS,
        "fi",
        subject="Occurrence enrolment SMS FI",
        body_text=DEFAULT_NOTIFICATION_BODY_TEXT_FI,
    )


@pytest.fixture
def notification_sms_template_occurrence_unenrolment_fi():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_UNENROLMENT_SMS,
        "fi",
        subject="Occurrence unenrolment SMS FI",
        body_text=DEFAULT_NOTIFICATION_BODY_TEXT_FI,
    )


@pytest.fixture
def notification_template_enrolment_approved_en():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_APPROVED,
        "en",
        subject="Enrolment approved EN",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN,
        body_html=NOTIFICATION_WITH_CUSTOM_MESSAGE_HTML_EN,
    )


@pytest.fixture
def notification_template_enrolment_approved_fi():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_APPROVED,
        "fi",
        subject="Enrolment approved FI",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI,
        body_html=NOTIFICATION_WITH_CUSTOM_MESSAGE_HTML_FI,
    )


@pytest.fixture
def notification_sms_template_enrolment_approved_fi():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_APPROVED_SMS,
        "fi",
        subject="Enrolment approved SMS FI",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI,
        body_html=NOTIFICATION_WITH_CUSTOM_MESSAGE_HTML_FI,
    )


@pytest.fixture
def notification_sms_template_enrolment_approved_en():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_APPROVED_SMS,
        "en",
        subject="Enrolment approved SMS EN",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN,
        body_html=NOTIFICATION_WITH_CUSTOM_MESSAGE_HTML_EN,
    )


@pytest.fixture
def notification_template_enrolment_declined_en():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_DECLINED,
        "en",
        subject="Enrolment declined EN",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN,
    )


@pytest.fixture
def notification_template_enrolment_declined_fi():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_DECLINED,
        "fi",
        subject="Enrolment declined FI",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI,
    )


@pytest.fixture
def notification_template_enrolment_cancellation_confirmation_en():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_CANCELLATION,
        "en",
        subject="Enrolment cancellation confirmation EN",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN,
    )


@pytest.fixture
def notification_template_enrolment_cancellation_confirmation_fi():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_CANCELLATION,
        "fi",
        subject="Enrolment cancellation confirmation FI",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI,
    )


@pytest.fixture
def notification_template_enrolment_cancelled_en():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_CANCELLED,
        "en",
        subject="Enrolment cancelled EN",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN,
    )


@pytest.fixture
def notification_template_enrolment_cancelled_fi():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_CANCELLED,
        "fi",
        subject="Enrolment cancelled FI",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI,
    )


@pytest.fixture
def notification_template_cancel_occurrence_fi():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_CANCELLED,
        "fi",
        subject="Occurrence cancelled FI",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_FI,
    )


@pytest.fixture
def notification_template_cancel_occurrence_en():
    return create_notification_template_in_language(
        NotificationTemplate.OCCURRENCE_CANCELLED,
        "fi",
        subject="Occurrence cancelled EN",
        body_text=NOTIFICATION_WITH_CUSTOM_MESSAGE_TEXT_EN,
    )


@pytest.fixture
def notification_template_enrolment_summary_report_fi():
    return create_notification_template_in_language(
        NotificationTemplate.ENROLMENT_SUMMARY_REPORT,
        "fi",
        subject="Enrolment approved FI",
        body_text="""
        Total pending enrolments: {{ total_pending_enrolments }}
        Total new accepted enrolments: {{ total_new_enrolments }}
        {% for item in report %}
            Event name: {{ item.event.name.fi }}
            Event link: {{ item.p_event.get_link_to_provider_ui() }}
            {% for occurrence in item.occurrences %}
                {% if item.p_event.auto_acceptance %}
                    Occurrence: #{{occurrence.start_time}} ({{
                    occurrence.new_enrolments() |
                    length }} new enrolments)
                {% else %}
                    Occurrence: #{{occurrence.start_time}} ({{
                    occurrence.pending_enrolments() |
                    length }} pending)
                {%endif %}
                    Link to occurrence: {{
                    occurrence.get_link_to_provider_ui()}}
            {% endfor %}
        {% endfor %}
        """,
    )
