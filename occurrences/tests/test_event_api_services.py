from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from django.utils import timezone

from common.tests.utils import mocked_json_response
from common.utils import format_linked_event_datetime
from occurrences.event_api_services import api_client as le_api_client
from occurrences.event_api_services import (
    fetch_event_as_json,
    fetch_place_as_json,
    get_enrollable_event_time_range_from_occurrences,
    resolve_unit_name_with_unit_id,
    send_event_republish,
    send_event_unpublish,
    update_event_to_linkedevents_api,
)
from occurrences.factories import OccurrenceFactory, PalvelutarjotinEventFactory
from palvelutarjotin.exceptions import ApiBadRequestError, ObjectDoesNotExistError


class TestSendEventRepublish:
    @pytest.mark.django_db
    @patch("occurrences.event_api_services.update_event_to_linkedevents_api")
    def test_republish_with_occurrences(
        self,
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


class TestSendEventUnpublish:
    @pytest.mark.django_db
    @patch("occurrences.event_api_services.update_event_to_linkedevents_api")
    def test_unpublish_sets_draft_status(
        self,
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


class TestGetEnrollableEventTimeRangeFromOccurrences:
    @pytest.mark.django_db
    def test_no_active_occurrences(self, mock_get_event_data):
        p_event = PalvelutarjotinEventFactory()
        assert p_event.occurrences.count() == 0
        assert get_enrollable_event_time_range_from_occurrences(p_event) == (None, None)
        OccurrenceFactory(p_event=p_event, cancelled=True)
        assert get_enrollable_event_time_range_from_occurrences(p_event) == (None, None)

    @pytest.mark.django_db
    def test_without_enrolment_start(self, mock_get_event_data):
        p_event = PalvelutarjotinEventFactory(enrolment_start=None)
        OccurrenceFactory(p_event=p_event, cancelled=False)
        assert get_enrollable_event_time_range_from_occurrences(p_event) == (None, None)

    @pytest.mark.django_db
    def test_with_active_occurrences(self, mock_get_event_data):
        p_event = PalvelutarjotinEventFactory(enrolment_start=timezone.now())
        OccurrenceFactory(p_event=p_event, cancelled=False)
        (start, _) = get_enrollable_event_time_range_from_occurrences(p_event)
        assert start == p_event.enrolment_start


class TestFetchPlaceAsJson:
    @patch("occurrences.event_api_services.api_client")
    def test_400_raises_bad_request_error(self, mock_api_client):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_api_client.retrieve.return_value = mock_response

        with pytest.raises(ApiBadRequestError):
            fetch_place_as_json("place_123")

    @patch("occurrences.event_api_services.api_client")
    def test_404_raises_not_found_error(self, mock_api_client):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_api_client.retrieve.return_value = mock_response

        with pytest.raises(ObjectDoesNotExistError):
            fetch_place_as_json("place_123")

    @patch("occurrences.event_api_services.api_client")
    def test_410_raises_gone_error(self, mock_api_client):
        mock_response = Mock()
        mock_response.status_code = 410
        mock_api_client.retrieve.return_value = mock_response

        with pytest.raises(ObjectDoesNotExistError, match="no longer available"):
            fetch_place_as_json("place_123")


class TestFetchEventAsJson:
    @patch("occurrences.event_api_services.api_client")
    def test_400_raises_bad_request_error(self, mock_api_client):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_api_client.retrieve.return_value = mock_response

        with pytest.raises(ApiBadRequestError):
            fetch_event_as_json("event_123")

    @patch("occurrences.event_api_services.api_client")
    def test_404_raises_not_found_error(self, mock_api_client):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_api_client.retrieve.return_value = mock_response

        with pytest.raises(ObjectDoesNotExistError):
            fetch_event_as_json("event_123")

    @patch("occurrences.event_api_services.api_client")
    def test_410_raises_gone_error(self, mock_api_client):
        mock_response = Mock()
        mock_response.status_code = 410
        mock_api_client.retrieve.return_value = mock_response

        with pytest.raises(ObjectDoesNotExistError, match="no longer available"):
            fetch_event_as_json("event_123")


class TestUpdateEventToLinkedeventsApi:
    @patch("occurrences.event_api_services.api_client")
    def test_400_raises_bad_request_error(self, mock_api_client):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_api_client.update.return_value = mock_response

        with pytest.raises(ApiBadRequestError):
            update_event_to_linkedevents_api("event_123", {"name": "Test"})

    @patch("occurrences.event_api_services.api_client")
    def test_404_raises_not_found_error(self, mock_api_client):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_api_client.update.return_value = mock_response

        with pytest.raises(ObjectDoesNotExistError):
            update_event_to_linkedevents_api("event_123", {"name": "Test"})

    @patch("occurrences.event_api_services.api_client")
    def test_410_raises_gone_error(self, mock_api_client):
        mock_response = Mock()
        mock_response.status_code = 410
        mock_api_client.update.return_value = mock_response

        with pytest.raises(ObjectDoesNotExistError, match="no longer available"):
            update_event_to_linkedevents_api("event_123", {"name": "Test"})


class TestResolveUnitNameWithUnitId:
    @pytest.mark.django_db
    @patch("occurrences.event_api_services.update_event_to_linkedevents_api")
    def test_raises_valueerror_without_unit_id(
        self, mock_update_event_to_linkedevents_api, study_group
    ):
        study_group.unit_id = None
        with pytest.raises(ValueError):
            resolve_unit_name_with_unit_id(study_group)

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "status_code,error_cls",
        [(400, ApiBadRequestError), (404, ObjectDoesNotExistError)],
    )
    @patch("occurrences.event_api_services.update_event_to_linkedevents_api")
    def test_raises_error_from_server_faults(
        self, mock_update_event_to_linkedevents_api, status_code, error_cls, study_group
    ):
        study_group.unit_id = "kultus:123"
        with patch.object(
            le_api_client,
            "retrieve",
            return_value=mocked_json_response(data=None, status_code=status_code),
        ):
            with pytest.raises(error_cls):
                resolve_unit_name_with_unit_id(study_group)

    @patch("occurrences.event_api_services.api_client")
    def test_410_raises_gone_error(self, mock_api_client):
        mock_response = Mock()
        mock_response.status_code = 410
        mock_api_client.retrieve.return_value = mock_response

        mock_study_group = Mock()
        mock_study_group.unit_id = "unit_123"

        with pytest.raises(ObjectDoesNotExistError, match="no longer available"):
            resolve_unit_name_with_unit_id(mock_study_group)
