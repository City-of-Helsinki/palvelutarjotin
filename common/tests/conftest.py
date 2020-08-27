import factory.random
import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from freezegun import freeze_time
from graphene.test import Client
from occurrences.factories import (
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
    VenueCustomDataFactory,
)
from organisations.factories import OrganisationFactory, PersonFactory, UserFactory

from common.tests.json_fixtures import *  # noqa
from common.tests.notification_template_fixtures import *  # noqa
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


def _create_api_client_with_user(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    client = Client(
        schema, context=request, format_error=SentryGraphQLView.format_error
    )
    client.user = user
    return client
