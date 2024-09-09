import factory.random
import pytest
import responses
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from freezegun import freeze_time
from graphene.test import Client
from unittest.mock import patch
from uuid import UUID

import occurrences.signals
from common.tests.json_fixtures import *  # noqa
from occurrences.factories import (
    EnrolmentFactory,
    LanguageFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
    VenueCustomDataFactory,
)
from occurrences.models import Enrolment
from occurrences.tests.notification_template_fixtures import *  # noqa
from organisations.factories import OrganisationFactory, PersonFactory, UserFactory
from organisations.tests.notification_template_fixtures import *  # noqa
from palvelutarjotin.schema import schema
from palvelutarjotin.views import SentryGraphQLView
from verification_token.factories import EnrolmentVerificationTokenFactory


@pytest.fixture(autouse=True)
def setup_test_environment(settings):
    settings.NOTIFICATION_SERVICE_SMS_ENABLED = True
    settings.CAPTCHA_ENABLED = False
    settings.PERSONAL_DATA_RETENTION_PERIOD_MONTHS = 24
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
def user():
    return UserFactory(uuid=UUID("26850000-2e85-11ea-b347-acde48001122"))


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
def enrolment():
    return EnrolmentFactory()


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
def enrolment_verification_token():
    return EnrolmentVerificationTokenFactory()


@pytest.fixture
def language():
    return LanguageFactory()


def _create_api_client_with_user(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    client = Client(
        schema, context=request, format_error=SentryGraphQLView.format_error
    )
    client.user = user
    return client


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def disconnect_send_enrolment_email():
    occurrences.signals.post_save.disconnect(
        sender=Enrolment, dispatch_uid="send_enrolment_email"
    )


@pytest.fixture
def mock_enrolment_cancel_link():
    with patch.object(
        Enrolment,
        "get_link_to_cancel_ui",
        return_value="mock-enrolment-cancel-link-abc123xyz456",
    ) as _fixture:
        yield _fixture


@pytest.fixture
def mock_enrolment_unique_id():
    with patch.object(
        Enrolment, "get_unique_id", return_value="mock-enrolment-unique-id-abc123xyz456"
    ) as _fixture:
        yield _fixture


@pytest.fixture(params=["true", "True", "TRUE", "1", 1, True])
def true_value(request):
    return request.param


@pytest.fixture(params=["false", "False", "FALSE", "0", 0, False])
def false_value(request):
    return request.param
