from unittest.mock import patch

import pytest
from occurrences.event_api_services import api_client as le_api_client
from occurrences.event_api_services import (
    resolve_unit_name_with_unit_id,
    send_event_republish,
    send_event_unpublish,
)
from occurrences.factories import OccurrenceFactory

from common.tests.utils import mocked_json_response
from common.utils import format_linked_event_datetime
from palvelutarjotin.exceptions import ApiBadRequestError, ObjectDoesNotExistError


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
        p_event.get_enrolment_end_time_from_occurrences()
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
    assert event_obj["publication_status"] == "draft"


@pytest.mark.django_db
@patch("occurrences.event_api_services.update_event_to_linkedevents_api")
def test_resolve_unit_name_with_unit_id_raises_valueerror_without_unit_id(
    mock_update_event_to_linkedevents_api, study_group
):
    study_group.unit_id = None
    with pytest.raises(ValueError):
        resolve_unit_name_with_unit_id(study_group)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "status_code,error_cls", [(400, ApiBadRequestError), (404, ObjectDoesNotExistError)]
)
@patch("occurrences.event_api_services.update_event_to_linkedevents_api")
def test_resolve_unit_name_with_unit_id_raises_error_from_server_faults(
    mock_update_event_to_linkedevents_api, status_code, error_cls, study_group
):
    study_group.unit_id = "kultus:123"
    with patch.object(
        le_api_client,
        "retrieve",
        return_value=mocked_json_response(data=None, status_code=status_code),
    ):
        with pytest.raises(error_cls):
            resolve_unit_name_with_unit_id(study_group)
