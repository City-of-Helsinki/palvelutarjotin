from unittest.mock import patch

import pytest
from graphene_linked_events.utils import api_client
from occurrences.factories import LanguageFactory, OccurrenceFactory
from occurrences.models import Occurrence
from occurrences.signals import update_event_languages_on_occurrence_delete

from common.tests.utils import mocked_json_response
from palvelutarjotin.exceptions import ApiConnectionError, ObjectDoesNotExistError


@pytest.mark.django_db
@patch.object(
    api_client, "update", return_value=mocked_json_response(data=None, status_code=200)
)
def test_update_event_languages(
    mock_api_client_update, mock_get_draft_event_data, mock_update_event_data, p_event
):
    def language_link_nodes(languages):
        return ['{"@id": "/v1/language/' + lang.pk + '/"}' for lang in languages]

    lng1, lng2, lng3 = LanguageFactory.create_batch(3)
    occurrence = OccurrenceFactory(p_event=p_event)
    # When languages are added...
    languages = [lng1, lng2]
    occurrence.languages.set(languages)
    # ...then api should be called once
    call_count = 1
    assert mock_api_client_update.call_count == call_count
    # ...and language links should be included in the update body
    assert all(
        link in mock_api_client_update.call_args[0][2]
        for link in language_link_nodes(languages)
    )
    # When languages are added and removed...
    languages = [lng1, lng3]
    occurrence.languages.set(languages)
    # ...then api should be called twice;
    # once from remove and once from addition
    call_count += 2
    assert mock_api_client_update.call_count == call_count
    # ...and language links should be included in the update body
    assert all(
        link in mock_api_client_update.call_args[0][2]
        for link in language_link_nodes(languages)
    )
    # When languages are removed...
    occurrence.languages.remove(lng3)
    # ...then api should be called once
    call_count += 1
    assert mock_api_client_update.call_count == call_count
    # ...and api update call should not contain removed attribute
    assert lng3.pk not in mock_api_client_update.call_args[0][2]
    # ...but it should contain the remaining languages
    assert lng1.pk in mock_api_client_update.call_args[0][2]
    # When lanaguages are cleared
    occurrence.languages.clear()
    # ...then api should be called once
    call_count += 1
    assert mock_api_client_update.call_count == call_count
    # ...and api should be called with empty list
    assert '"in_language": []' in mock_api_client_update.call_args[0][2]


@pytest.mark.django_db
@patch.object(
    api_client, "update", return_value=mocked_json_response(data=None, status_code=200)
)
def test_update_event_languages_should_not_update_if_language_still_exists(
    mock_api_client_update, mock_get_draft_event_data, mock_update_event_data, p_event
):
    lng1, lng2, lng3 = LanguageFactory.create_batch(3)
    OccurrenceFactory(p_event=p_event, languages=[lng1, lng2])
    occurrence = OccurrenceFactory(p_event=p_event, languages=[lng2, lng3])
    assert mock_api_client_update.call_count == 4
    occurrence.languages.remove(lng2)
    assert mock_api_client_update.call_count == 4
    occurrence.languages.remove(lng3)
    assert mock_api_client_update.call_count == 5


@pytest.mark.django_db
@patch.object(
    api_client, "update", return_value=mocked_json_response(data=None, status_code=200)
)
def test_update_event_languages_when_occurrence_is_deleted(
    mock_api_client_update, mock_get_draft_event_data, mock_update_event_data, p_event
):
    lng1, lng2, lng3 = LanguageFactory.create_batch(3)
    OccurrenceFactory(p_event=p_event, languages=[lng1, lng2])
    occurrence = OccurrenceFactory(p_event=p_event, languages=[lng2, lng3])
    assert mock_api_client_update.call_count == 4
    occurrence.delete()
    assert mock_api_client_update.call_count == 5


@pytest.mark.django_db
@patch.object(
    api_client, "update", return_value=mocked_json_response(data=None, status_code=400)
)
def test_update_event_languages_cannot_reach_api(
    mock_api_client_update, mock_get_draft_event_data, mock_update_event_data, p_event
):
    with pytest.raises(ApiConnectionError):
        OccurrenceFactory(p_event=p_event, languages=LanguageFactory.create_batch(2))


@pytest.mark.django_db
@patch.object(
    api_client, "update", return_value=mocked_json_response(data=None, status_code=404)
)
def test_update_event_languages_cannot_find_event(
    mock_api_client_update, mock_update_event_data, p_event
):
    with pytest.raises(ObjectDoesNotExistError):
        OccurrenceFactory(p_event=p_event, languages=LanguageFactory.create_batch(2))


@pytest.mark.django_db
@patch.object(
    api_client, "update", return_value=mocked_json_response(data=None, status_code=200)
)
def test_occurrence_delete_should_ignore(
    mock_api_client_update, mock_get_draft_event_data, mock_update_event_data, p_event
):
    occurrence = OccurrenceFactory(
        p_event=p_event, languages=LanguageFactory.create_batch(2)
    )
    Occurrence.objects.count() == 1
    assert mock_api_client_update.call_count == 2

    mock_api_client_update.return_value = mocked_json_response(
        data=None, status_code=404
    )

    occurrence.delete()
    assert mock_api_client_update.call_count == 3
    assert Occurrence.objects.count() == 0


@pytest.mark.django_db
@patch.object(
    api_client, "update", return_value=mocked_json_response(data=None, status_code=404)
)
def test_occurrence_without_p_event_should_not_call_API(mock_api_client_update):
    occurrence = OccurrenceFactory()

    # Test p_Event does not exist
    occurrence.p_event_id = 0  # object which does not exist
    update_event_languages_on_occurrence_delete(Occurrence, occurrence)
    assert mock_api_client_update.call_count == 0

    # Test no p_event attr
    d = occurrence.__dict__
    d["p_event"] = None
    update_event_languages_on_occurrence_delete(Occurrence, d)
    assert mock_api_client_update.call_count == 0
