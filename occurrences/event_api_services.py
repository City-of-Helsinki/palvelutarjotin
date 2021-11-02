import json
import logging
from typing import List, Optional, TYPE_CHECKING

from graphene_linked_events.utils import api_client

from common.utils import format_linked_event_datetime
from palvelutarjotin.exceptions import ApiBadRequestError, ObjectDoesNotExistError

if TYPE_CHECKING:
    from occurrences.models import PalvelutarjotinEvent, StudyGroup


logger = logging.getLogger(__name__)


def fetch_event_as_json(linked_event_id: str):
    result = api_client.retrieve("event", linked_event_id, is_staff=True)

    if result.status_code == 400:
        raise ApiBadRequestError("Bad request to LinkedEvents API.")

    if result.status_code == 404:
        raise ObjectDoesNotExistError("Could not find the event from the API.")

    result.raise_for_status()

    event_obj = json.loads(result.text)
    return event_obj


def update_event_to_linkedevents_api(linked_event_id: str, event_obj) -> None:
    # Call API to update event
    result = api_client.update("event", linked_event_id, json.dumps(event_obj))

    if result.status_code == 400:
        raise ApiBadRequestError("Bad request to LinkedEvents API.")

    if result.status_code == 404:
        raise ObjectDoesNotExistError("Could not find the event from the API.")

    result.raise_for_status()


def send_event_languages_update(
    p_event: "PalvelutarjotinEvent", event_language_ids: List[str]
) -> None:
    """
    Update event languages to LinkedEvents.
    """

    # FIXME: This is a needless call if LE would not need a full event data.
    # Since the LE needs at least all the required fields when an event is updated,
    # we first need to fetch the current event object.
    event_obj = fetch_event_as_json(p_event.linked_event_id)

    # Updated languages
    in_language_body = [
        {"@id": "/v1/language/{language}/".format(language=language)}
        for language in event_language_ids
    ]
    event_obj["in_language"] = in_language_body

    update_event_to_linkedevents_api(p_event.linked_event_id, event_obj)


def send_event_republish(p_event: "PalvelutarjotinEvent"):

    # FIXME: This is a needless call if LE would not need a full event data.
    # Since the LE needs at least all the required fields when an event is updated,
    # we first need to fetch the current event object.
    event_obj = fetch_event_as_json(p_event.linked_event_id)

    # NOTE: Event creation date is set as a start_time,
    # by `_prepare_published_event_data` in `graphene_linked_events.schema.py.
    # That should not be changed.
    event_obj["end_time"] = format_linked_event_datetime(
        p_event.get_enrolment_end_time_from_occurrences()
    )

    update_event_to_linkedevents_api(p_event.linked_event_id, event_obj)


def send_event_unpublish(p_event: "PalvelutarjotinEvent"):
    # FIXME: This is a needless call if LE would not need a full event data.
    # Since the LE needs at least all the required fields when an event is updated,
    # we first need to fetch the current event object.
    event_obj = fetch_event_as_json(p_event.linked_event_id)

    event_obj[
        "publication_status"
    ] = p_event.__class__.PUBLICATION_STATUS_DRAFT  # prevent cyclic import

    update_event_to_linkedevents_api(p_event.linked_event_id, event_obj)


def get_event_time_range_from_occurrences(p_event: Optional["PalvelutarjotinEvent"]):

    if not p_event:
        return None, None

    occurrences = p_event.occurrences.filter(cancelled=False)
    first_occurrence = occurrences.order_by("start_time").first()
    last_occurrence = occurrences.order_by("end_time").last()
    if first_occurrence and last_occurrence:
        return first_occurrence.start_time, last_occurrence.end_time
    return None, None


def resolve_unit_name_with_unit_id(study_group: "StudyGroup"):
    if not study_group.unit_id:
        raise ValueError(
            """Resolve_unit_name_with_unit_id cannot resolve
            the name when the unit id is not given."""
        )

    result = api_client.retrieve("place", study_group.unit_id)

    if result.status_code == 400:
        raise ApiBadRequestError("Bad request to LinkedEvents API.")

    if result.status_code == 404:
        raise ObjectDoesNotExistError("Could not find the event from the API.")

    result.raise_for_status()

    if result.name:
        study_group.unit_name = result.name
