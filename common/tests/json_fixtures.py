import graphene_linked_events.rest_client
import pytest
import requests
from graphene_linked_events.tests.mock_data import (
    CREATED_EVENT_DATA,
    DRAFT_EVENT_DATA,
    EVENT_DATA,
    EVENTS_DATA,
    IMAGE_DATA,
    IMAGES_DATA,
    KEYWORD_DATA,
    KEYWORD_SET_DATA,
    KEYWORDS_DATA,
    PLACE_DATA,
    PLACES_DATA,
    RECAPTCHA_DATA,
    UPDATE_EVENT_DATA,
)
from graphene_linked_events.tests.utils import MockResponse


def _get_mock_function(data, status_code=200):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=status_code, json_data=data)

    return mock_data


@pytest.fixture
def mock_get_event_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "retrieve",
        _get_mock_function(EVENT_DATA),
    )


@pytest.fixture
def mock_get_draft_event_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "retrieve",
        _get_mock_function(DRAFT_EVENT_DATA),
    )


@pytest.fixture
def mock_get_events_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "list",
        _get_mock_function(EVENTS_DATA),
    )


@pytest.fixture
def mock_get_image_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "retrieve",
        _get_mock_function(IMAGE_DATA),
    )


@pytest.fixture
def mock_get_images_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "list",
        _get_mock_function(IMAGES_DATA),
    )


@pytest.fixture
def mock_get_place_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "retrieve",
        _get_mock_function(PLACE_DATA),
    )


@pytest.fixture
def mock_get_places_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "list",
        _get_mock_function(PLACES_DATA),
    )


@pytest.fixture
def mock_get_keyword_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "retrieve",
        _get_mock_function(KEYWORD_DATA),
    )


@pytest.fixture
def mock_get_keywords_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "list",
        _get_mock_function(KEYWORDS_DATA),
    )


@pytest.fixture
def mock_search_places_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "search",
        _get_mock_function(PLACES_DATA),
    )


@pytest.fixture
def mock_search_events_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "search",
        _get_mock_function(EVENTS_DATA),
    )


@pytest.fixture
def mock_create_event_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "create",
        _get_mock_function(CREATED_EVENT_DATA, status_code=201),
    )


@pytest.fixture
def mock_update_event_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "update",
        _get_mock_function(UPDATE_EVENT_DATA),
    )


@pytest.fixture
def mock_delete_event_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "delete",
        _get_mock_function(None, status_code=204),
    )


@pytest.fixture
def mock_delete_image_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "delete",
        _get_mock_function(None, status_code=204),
    )


@pytest.fixture
def mock_update_image_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "update",
        _get_mock_function(IMAGE_DATA),
    )


@pytest.fixture
def mock_recaptcha_data(monkeypatch):
    monkeypatch.setattr(
        requests, "post", _get_mock_function(RECAPTCHA_DATA),
    )


@pytest.fixture
def mock_get_keyword_set_data(monkeypatch):
    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "retrieve",
        _get_mock_function(KEYWORD_SET_DATA),
    )
