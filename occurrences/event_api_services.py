import json
import logging
from typing import List

from graphene_linked_events.utils import api_client
from occurrences.models import PalvelutarjotinEvent

from common.utils import format_linked_event_datetime
from palvelutarjotin.exceptions import (
    ApiConnectionError,
    ApiUsageError,
    ObjectDoesNotExistError,
)

logger = logging.getLogger(__name__)


def fetch_event_as_json(linked_event_id: str):
    result = api_client.retrieve("event", linked_event_id, is_staff=True)

    if result.status_code == 400:
        raise ApiConnectionError("Could not establish a connection to the API.")

    if result.status_code == 404:
        raise ObjectDoesNotExistError("Could not find the event from the API.")

    event_obj = json.loads(result.text)
    return event_obj


def update_event_to_linkedevents_api(linked_event_id: str, event_obj) -> None:
    # Call API to update event
    result = api_client.update("event", linked_event_id, json.dumps(event_obj))

    if result.status_code == 400:
        raise ApiConnectionError("Could not establish a connection to the API.")

    if result.status_code == 404:
        raise ObjectDoesNotExistError("Could not find the event from the API.")

    elif result.status_code != 200:
        raise ApiUsageError("Could not update event to LinkedEvents API.")


def send_event_languages_update(
    p_event: PalvelutarjotinEvent, event_language_ids: List[str]
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


def send_event_republish(p_event: PalvelutarjotinEvent):

    # FIXME: This is a needless call if LE would not need a full event data.
    # Since the LE needs at least all the required fields when an event is updated,
    # we first need to fetch the current event object.
    event_obj = fetch_event_as_json(p_event.linked_event_id)

    try:
        event_obj["end_time"] = format_linked_event_datetime(
            p_event.get_end_time_from_occurrences()
        )
    except ValueError as e:
        logger.warning(
            f"""Could not republish the event {p_event.linked_event_id}
            because of an ValueError:{e}."""
        )
    else:
        update_event_to_linkedevents_api(p_event.linked_event_id, event_obj)


def send_event_unpublish(p_event: PalvelutarjotinEvent):
    # FIXME: This is a needless call if LE would not need a full event data.
    # Since the LE needs at least all the required fields when an event is updated,
    # we first need to fetch the current event object.
    event_obj = fetch_event_as_json(p_event.linked_event_id)

    event_obj["publication_status"] = False
    event_obj["start_time"] = ""
    event_obj["end_time"] = ""

    update_event_to_linkedevents_api(p_event.linked_event_id, event_obj)
