from unittest.mock import patch

import pytest
from occurrences.event_api_services import send_event_republish, send_event_unpublish
from occurrences.factories import OccurrenceFactory

from common.utils import format_linked_event_datetime


@pytest.mark.django_db
@patch("occurrences.event_api_services.update_event_to_linkedevents_api")
def test_send_event_republish(
    mock_update_event_to_linkedevents_api,
    mock_get_event_data,
    mock_update_event_data,
    p_event,
):
    OccurrenceFactory(p_event=p_event)
    send_event_republish(p_event)

    called_linked_event_id = mock_update_event_to_linkedevents_api.call_args[0][0]
    event_obj = mock_update_event_to_linkedevents_api.call_args[0][1]
    assert called_linked_event_id == p_event.linked_event_id
    assert event_obj["end_time"] == format_linked_event_datetime(
        p_event.get_end_time_from_occurrences()
    )


@pytest.mark.django_db
@patch("occurrences.event_api_services.update_event_to_linkedevents_api")
def test_send_event_unpublish(
    mock_update_event_to_linkedevents_api,
    mock_get_event_data,
    mock_update_event_data,
    p_event,
):
    send_event_unpublish(p_event)

    called_linked_event_id = mock_update_event_to_linkedevents_api.call_args[0][0]
    event_obj = mock_update_event_to_linkedevents_api.call_args[0][1]
    assert called_linked_event_id == p_event.linked_event_id
    assert event_obj["publication_status"] is False
    assert event_obj["start_time"] == ""
    assert event_obj["end_time"] == ""
