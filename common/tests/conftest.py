import factory.random
import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from freezegun import freeze_time
from graphene.test import Client
from organisations.factories import UserFactory

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
def staff_api_client():
    return _create_api_client_with_user(UserFactory(is_staff=True))


def _create_api_client_with_user(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    client = Client(
        schema, context=request, format_error=SentryGraphQLView.format_error
    )
    client.user = user
    return client
