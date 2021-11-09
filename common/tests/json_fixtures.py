import pytest
import requests
from graphene_linked_events.rest_client import LinkedEventsApiClient
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
    POPULAR_KEYWORD_SET_DATA,
    RECAPTCHA_DATA,
    UNPUBLISH_EVENT_DATA,
    UPDATE_EVENT_DATA,
)
from graphene_linked_events.tests.utils import MockResponse
from servicemap.rest_client import ServicemapApiClient
from servicemap.tests.mock_data import SCHOOL_AND_KINDERGARTEN_NAMES_DATA


def _get_mock_function(data, status_code=200):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=status_code, json_data=data)

    return mock_data


@pytest.fixture
def mock_get_event_data(monkeypatch):
    """
    Mocks a published event data fetch from LinkedEvents API.
    Also mocks the update, because Occurrences app's signals
    updates the event status to LinkedEvents API,
    when the event is published
    """
    monkeypatch.setattr(
        LinkedEventsApiClient, "retrieve", _get_mock_function(EVENT_DATA),
    )
    # Mock the published event update
    monkeypatch.setattr(
        LinkedEventsApiClient, "update", _get_mock_function(EVENT_DATA),
    )


@pytest.fixture
def mock_get_draft_event_data(monkeypatch):
    """
    Mocks an unpublished / draft event data fetch from LinkedEvents API.
    """
    monkeypatch.setattr(
        LinkedEventsApiClient, "retrieve", _get_mock_function(DRAFT_EVENT_DATA),
    )


@pytest.fixture
def mock_get_events_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "list", _get_mock_function(EVENTS_DATA),
    )


@pytest.fixture
def mock_get_image_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "retrieve", _get_mock_function(IMAGE_DATA),
    )


@pytest.fixture
def mock_get_images_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "list", _get_mock_function(IMAGES_DATA),
    )


@pytest.fixture
def mock_get_place_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "retrieve", _get_mock_function(PLACE_DATA),
    )


@pytest.fixture
def mock_get_places_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "list", _get_mock_function(PLACES_DATA),
    )


@pytest.fixture
def mock_get_keyword_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "retrieve", _get_mock_function(KEYWORD_DATA),
    )


@pytest.fixture
def mock_get_keywords_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "list", _get_mock_function(KEYWORDS_DATA),
    )


@pytest.fixture
def mock_search_places_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "search", _get_mock_function(PLACES_DATA),
    )


@pytest.fixture
def mock_search_events_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "search", _get_mock_function(EVENTS_DATA),
    )


@pytest.fixture
def mock_create_event_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient,
        "create",
        _get_mock_function(CREATED_EVENT_DATA, status_code=201),
    )


@pytest.fixture
def mock_update_event_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "update", _get_mock_function(UPDATE_EVENT_DATA),
    )


@pytest.fixture
def mock_unpublish_event_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "update", _get_mock_function(UNPUBLISH_EVENT_DATA),
    )


@pytest.fixture
def mock_delete_event_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "delete", _get_mock_function(None, status_code=204),
    )


@pytest.fixture
def mock_delete_image_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "delete", _get_mock_function(None, status_code=204),
    )


@pytest.fixture
def mock_update_image_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "update", _get_mock_function(IMAGE_DATA),
    )


@pytest.fixture
def mock_recaptcha_data(monkeypatch):
    monkeypatch.setattr(
        requests, "post", _get_mock_function(RECAPTCHA_DATA),
    )


@pytest.fixture
def mock_get_keyword_set_data(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "retrieve", _get_mock_function(KEYWORD_SET_DATA),
    )


@pytest.fixture
def mock_get_popular_kultus_keywords(monkeypatch):
    monkeypatch.setattr(
        LinkedEventsApiClient, "retrieve", _get_mock_function(POPULAR_KEYWORD_SET_DATA),
    )


@pytest.fixture
def mock_get_servicemap_schools_and_kindergartens_data(monkeypatch):
    monkeypatch.setattr(
        ServicemapApiClient,
        "list_helsinki_schools_and_kindergartens",
        _get_mock_function(SCHOOL_AND_KINDERGARTEN_NAMES_DATA),
    )
