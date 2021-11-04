import json
import logging
from datetime import timedelta
from typing import List, Optional, TYPE_CHECKING

from graphene_linked_events.utils import api_client

from common.utils import format_linked_event_datetime
from palvelutarjotin.exceptions import ApiBadRequestError, ObjectDoesNotExistError

if TYPE_CHECKING:
    from occurrences.models import PalvelutarjotinEvent


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

    start_time, end_time = get_event_time_range_from_occurrences(p_event)
    (
        enrolment_start_time,
        enrolment_end_time,
    ) = get_enrollable_event_time_range_from_occurrences(p_event)

    event_obj["publication_status"] = p_event.__class__.PUBLICATION_STATUS_PUBLIC
    event_obj["start_time"] = (
        format_linked_event_datetime(start_time) if start_time else None
    )
    event_obj["end_time"] = format_linked_event_datetime(end_time) if end_time else None
    event_obj["enrolment_start_time"] = (
        format_linked_event_datetime(enrolment_start_time)
        if enrolment_start_time
        else None
    )
    event_obj["enrolment_end_time"] = (
        format_linked_event_datetime(enrolment_end_time) if enrolment_end_time else None
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


def get_enrollable_event_time_range_from_occurrences(
    p_event: Optional["PalvelutarjotinEvent"],
):
    if not p_event or not p_event.enrolment_start:
        """
        1. No p_event set yet
        2. 2nd step of the UI's form wizard, that includes the occurrences
        and enrolment data, is not yet full filled.
        3. The event is externally enrollable
        4. The event is not enrollable at all
        """
        return None, None

    try:
        occurrences = p_event.occurrences.filter(cancelled=False).order_by("end_time")
        end_time = occurrences.last().start_time
    except AttributeError:
        return None, None

    # Enrolment end days sets the last day for enrolment
    if p_event.enrolment_end_days is not None and p_event.enrolment_end_days > 0:
        end_time = end_time - timedelta(days=p_event.enrolment_end_days)

    # NOTE: originally the start time has been timezone.now(),
    # because something needs to be set on UI wizards first step,
    # when there are no occurrences or enrolment start time set yet.
    # Event's enrolment start time should be in sync
    # with p_event.enrolment_start, or `p_event.enrolment_start`
    # should be fully replaced with
    # `occurrence.start_time - timedelta(days=p_event.enrolment_end_days)`
    # TODO: Remove p_event.enrolment_start and
    # start using the one from LinkedEvents Event API,
    # so there would be one field less to sync between the APIs
    return (p_event.enrolment_start, end_time)
