import json
import logging
from datetime import timedelta
from typing import TYPE_CHECKING, List, Optional

from django.utils import timezone

from common.utils import format_linked_event_datetime
from graphene_linked_events.utils import api_client, format_response, json2obj
from palvelutarjotin.exceptions import (
    ApiBadRequestError,
    ApiUsageError,
    ObjectDoesNotExistError,
)

if TYPE_CHECKING:
    from occurrences.models import PalvelutarjotinEvent, StudyGroup


logger = logging.getLogger(__name__)


def fetch_place_as_json(place_id: str, **filter_params):
    if not place_id:
        return None

    result = api_client.retrieve(
        "place", place_id, params=filter_params, is_event_staff=True
    )

    if result.status_code == 400:
        raise ApiBadRequestError("Bad request to LinkedEvents API.")

    if result.status_code == 404:
        raise ObjectDoesNotExistError("Could not find the place from the API.")

    result.raise_for_status()

    place_obj = json.loads(result.text)
    return place_obj


def fetch_event_as_json(linked_event_id: str, **filter_params):
    if not linked_event_id:
        return None

    result = api_client.retrieve(
        "event", linked_event_id, params=filter_params, is_event_staff=True
    )

    if result.status_code == 400:
        raise ApiBadRequestError("Bad request to LinkedEvents API.")

    if result.status_code == 404:
        raise ObjectDoesNotExistError("Could not find the event from the API.")

    result.raise_for_status()

    event_obj = json.loads(result.text)
    return event_obj


def update_event_to_linkedevents_api(linked_event_id: str, event_obj) -> None:
    if not linked_event_id:
        raise ObjectDoesNotExistError(
            "Could not find the event from the API. No linked_event_id given!"
        )

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


def send_event_publish(
    p_event: "PalvelutarjotinEvent", linked_events_data: Optional[dict]
):
    body = prepare_published_event_data(p_event, linked_events_data)
    response = api_client.create("event", body)
    response.raise_for_status()


def send_event_republish(p_event: "PalvelutarjotinEvent"):
    # FIXME: This is a needless call if LE would not need a full event data.
    # Since the LE needs at least all the required fields when an event is updated,
    # we first need to fetch the current event object.
    event_obj = fetch_event_as_json(p_event.linked_event_id)
    event_obj.update(prepare_published_event_data(p_event))
    update_event_to_linkedevents_api(p_event.linked_event_id, event_obj)


def send_event_unpublish(p_event: "PalvelutarjotinEvent"):
    # FIXME: This is a needless call if LE would not need a full event data.
    # Since the LE needs at least all the required fields when an event is updated,
    # we first need to fetch the current event object.
    event_obj = fetch_event_as_json(p_event.linked_event_id)

    event_obj["publication_status"] = (
        p_event.__class__.PUBLICATION_STATUS_DRAFT
    )  # prevent cyclic import

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
        raise ObjectDoesNotExistError("Could not find the place from the API.")

    result.raise_for_status()

    unit = json2obj(format_response(result))

    if unit.name and unit.name.fi:
        study_group.unit_name = unit.name.fi


def prepare_published_event_data(
    p_event: "PalvelutarjotinEvent", event_data: Optional[dict] = None
):
    # Only care about getting published event data, no permission/authorization
    # check here
    if not p_event.occurrences.exists():
        raise ApiUsageError("Cannot publish event without event occurrences")

    start_time, end_time = get_event_time_range_from_occurrences(p_event)
    (
        enrolment_start_time,
        enrolment_end_time,
    ) = get_enrollable_event_time_range_from_occurrences(p_event)

    data = {
        "publication_status": p_event.__class__.PUBLICATION_STATUS_PUBLIC,
        "start_time": format_linked_event_datetime(start_time or timezone.now()),
        "end_time": format_linked_event_datetime(end_time) if end_time else None,
        "enrolment_start_time": (
            format_linked_event_datetime(enrolment_start_time)
            if enrolment_start_time
            else None
        ),
        "enrolment_end_time": (
            format_linked_event_datetime(enrolment_end_time)
            if enrolment_end_time
            else None
        ),
    }

    if event_data:
        data.update(event_data)

    return data
