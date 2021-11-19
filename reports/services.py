from datetime import datetime

import reports.models as report_models
from occurrences.event_api_services import fetch_event_as_json, fetch_place_as_json

from palvelutarjotin.exceptions import ApiBadRequestError, ObjectDoesNotExistError


def sync_enrolment_reports(hydrate_linkedevents_event=True, sync_from: datetime = None):
    """
    Synchronize the enrolemnts report table with enrolments table:
    1. Update the unsynced enrolment report instances.
    2. Create the missing enrolment report instances.
    NOTE: This function fetches data
    for each event of the enrolments from LinkedEvents API
    """
    sync_from = sync_from or report_models.EnrolmentReport.objects.latest_sync()
    if report_models.EnrolmentReport.objects.exists():
        report_models.EnrolmentReport.objects.update_unsynced(
            sync_from=sync_from, hydrate_linkedevents_event=hydrate_linkedevents_event
        )
    report_models.EnrolmentReport.objects.create_missing(
        hydrate_linkedevents_event=hydrate_linkedevents_event, sync_from=sync_from
    )


def get_event_json_from_linkedevents(linked_event_id: str):
    try:
        return fetch_event_as_json(linked_event_id, include=["keywords", "location"])
    except (ApiBadRequestError, ObjectDoesNotExistError):
        return None


def get_place_location_data(place_id: str) -> tuple:
    place_json = get_place_json_from_linkedevents(place_id)
    coordinates = resolve_place_coordinates(place_json)
    divisions = resolve_place_divisions(place_json)
    return (coordinates, divisions)


def get_place_json_from_linkedevents(place_id: str):
    try:
        return fetch_place_as_json(place_id)
    except (ApiBadRequestError, ObjectDoesNotExistError):
        return None


def resolve_place_divisions(place_json) -> list:
    if not place_json:
        return None
    try:
        divisions = place_json["location"]["divisions"]
        return [d["ocd_id"] for d in divisions]
    except KeyError:
        return None


def resolve_place_coordinates(place_json) -> tuple:
    if not place_json:
        return None
    try:
        return place_json["location"]["position"]["coordinates"]
    except KeyError:
        return None
