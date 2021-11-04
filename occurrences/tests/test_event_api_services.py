from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from occurrences.event_api_services import (
    get_enrollable_event_time_range_from_occurrences,
    send_event_republish,
    send_event_unpublish,
)
from occurrences.factories import OccurrenceFactory, PalvelutarjotinEventFactory

from common.utils import format_linked_event_datetime


@pytest.mark.django_db
@patch("occurrences.event_api_services.update_event_to_linkedevents_api")
def test_send_event_republish(
    mock_update_event_to_linkedevents_api,
    mock_get_event_data,
    mock_update_event_data,
    p_event,
):
    OccurrenceFactory.create_batch(3, p_event=p_event, cancelled=False)

    first_occurrence = p_event.occurrences.earliest("start_time")
    last_occurrence = p_event.occurrences.latest("end_time")
    event_start = first_occurrence.start_time
    event_end = last_occurrence.end_time

    # Set a logic enrolment_start
    p_event.enrolment_start = first_occurrence.start_time
    p_event.save()

    enrolling_ends = last_occurrence.start_time - timedelta(
        days=p_event.enrolment_end_days
    )
    send_event_republish(p_event)

    called_linked_event_id = mock_update_event_to_linkedevents_api.call_args[0][0]
    event_obj = mock_update_event_to_linkedevents_api.call_args[0][1]
    assert called_linked_event_id == p_event.linked_event_id
    assert event_obj["start_time"] == format_linked_event_datetime(event_start)
    assert event_obj["end_time"] == format_linked_event_datetime(event_end)
    assert event_obj["enrolment_start_time"] == format_linked_event_datetime(
        p_event.enrolment_start
    )
    assert event_obj["enrolment_end_time"] == format_linked_event_datetime(
        enrolling_ends
    )
    assert event_obj["enrolment_end_time"] is not None


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
    assert event_obj["publication_status"] == "draft"


@pytest.mark.django_db
def test_get_enrollable_event_time_range_from_occurrences_with_no_active_occurrences(
    mock_get_event_data,
):
    p_event = PalvelutarjotinEventFactory()
    assert p_event.occurrences.count() == 0
    assert get_enrollable_event_time_range_from_occurrences(p_event) == (None, None)
    OccurrenceFactory(p_event=p_event, cancelled=True)
    assert get_enrollable_event_time_range_from_occurrences(p_event) == (None, None)


@pytest.mark.django_db
def test_get_enrollable_event_time_range_from_occurrences_without_enrolment_start(
    mock_get_event_data,
):
    p_event = PalvelutarjotinEventFactory(enrolment_start=None)
    OccurrenceFactory(p_event=p_event, cancelled=False)
    assert get_enrollable_event_time_range_from_occurrences(p_event) == (None, None)


@pytest.mark.django_db
def test_get_enrollable_event_time_range_from_occurrences_with_active_occurrences(
    mock_get_event_data,
):
    p_event = PalvelutarjotinEventFactory(enrolment_start=timezone.now())
    OccurrenceFactory(p_event=p_event, cancelled=False)
    (start, _) = get_enrollable_event_time_range_from_occurrences(p_event)
    assert start == p_event.enrolment_start
