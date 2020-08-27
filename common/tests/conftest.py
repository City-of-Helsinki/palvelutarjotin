import factory.random
import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from freezegun import freeze_time
from graphene.test import Client
from occurrences.consts import NotificationTemplate
from occurrences.factories import (
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
    VenueCustomDataFactory,
)
from organisations.factories import OrganisationFactory, PersonFactory, UserFactory

from common.tests.json_fixtures import *  # noqa
from common.tests.utils import create_notification_template_in_language
from palvelutarjotin.schema import schema
from palvelutarjotin.views import SentryGraphQLView


@pytest.fixture(autouse=True)
def setup_test_environment():
    factory.random.reseed_random("777")
    with freeze_time("2020-01-04"):
        yield


@pytest.fixture
def api_client():
    return _create_api_client_with_user(AnonymousUser())


@pytest.fixture
def user_api_client():
    return _create_api_client_with_user(UserFactory())


@pytest.fixture
def staff_api_client(person):
    return _create_api_client_with_user(
        PersonFactory(user=UserFactory(is_staff=True)).user
    )


@pytest.fixture
def superuser_api_client():
    return _create_api_client_with_user(UserFactory(is_superuser=True))


@pytest.fixture
def person_api_client():
    return _create_api_client_with_user(PersonFactory(user=UserFactory()).user)


@pytest.fixture
def person():
    return PersonFactory(organisations=[OrganisationFactory()])


@pytest.fixture
def person_without_organisation():
    return PersonFactory()


@pytest.fixture
def organisation():
    return OrganisationFactory()


@pytest.fixture
def study_group():
    return StudyGroupFactory()


@pytest.fixture
def occurrence():
    return OccurrenceFactory()


@pytest.fixture
def p_event():
    return PalvelutarjotinEventFactory()


@pytest.fixture
def venue():
    return VenueCustomDataFactory()


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
        {% if custom_message %}
        Custom message: {{ custom_message }}
        {% endif %}
""",
        body_html="""
            <p>
            Event EN: {{ event.name.en }}
            Extra event info: {{ occurrence.p_event.linked_event_id }}
            Study group: {{ study_group.name }}
            Occurrence: {{ occurrence.start_time }}
            Person: {{ study_group.person.email_address}}
            {% if custom_message %}
            Custom message: {{ custom_message }}
            {% endif %}
            </p>
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
        {% if custom_message %}
        Custom message: {{ custom_message }}
        {% endif %}
""",
        body_html="""
            <p>
            Event FI: {{ event.name.fi }}
            Extra event info: {{ occurrence.p_event.linked_event_id }}
            Study group: {{ study_group.name }}
            Occurrence: {{ occurrence.start_time }}
            Person: {{ study_group.person.email_address}}
            {% if custom_message %}
            Custom message: {{ custom_message }}
            {% endif %}
            </p>
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
        {% if custom_message %}
        Custom message: {{ custom_message }}
        {% endif %}
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
        {% if custom_message %}
        Custom message: {{ custom_message }}
        {% endif %}
""",
    )


def _create_api_client_with_user(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    client = Client(
        schema, context=request, format_error=SentryGraphQLView.format_error
    )
    client.user = user
    return client
