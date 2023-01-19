from datetime import datetime
from django.db import models
from typing import List, Optional, Union

import occurrences.models as occurrences_models
import reports.models as report_models
from occurrences.event_api_services import fetch_event_as_json, fetch_place_as_json
from palvelutarjotin.exceptions import ApiBadRequestError, ObjectDoesNotExistError


def sync_enrolment_reports(
    hydrate_linkedevents_event=True,
    sync_from: datetime = None,
    create_from: datetime = None,
):
    """
    Synchronize the enrolemnts report table with enrolments table:
    1. Update the unsynced enrolment report instances.
    2. Create the missing enrolment report instances.
    NOTE: This function fetches data
    for each event of the enrolments from LinkedEvents API
    """
    sync_from = sync_from or report_models.EnrolmentReport.objects.latest_sync()
    if not create_from and sync_from is not None:
        create_from = sync_from
    if report_models.EnrolmentReport.objects.exists():
        report_models.EnrolmentReport.objects.update_unsynced(
            sync_from=sync_from, hydrate_linkedevents_event=hydrate_linkedevents_event
        )
    report_models.EnrolmentReport.objects.create_missing(
        hydrate_linkedevents_event=hydrate_linkedevents_event, sync_from=create_from
    )


def get_unsynced_enrollments(
    sync_from: datetime = None,
) -> Union[models.QuerySet, List[occurrences_models.Enrolment]]:
    """Get a list of enrolments which are updated after latest report updates."""
    sync_from = sync_from or report_models.EnrolmentReport.objects.latest_sync()
    if sync_from:
        return occurrences_models.Enrolment.objects.filter(updated_at__gte=sync_from)
    return occurrences_models.Enrolment.objects.all()


def get_missing_enrollments(
    sync_from: datetime = None,
) -> Union[models.QuerySet, List[occurrences_models.Enrolment]]:
    """Get a list of enrolments which are missing from EnrolmentReport db-table."""
    enrolments = get_unsynced_enrollments(sync_from=sync_from)
    reports_enrolment_ids = report_models.EnrolmentReport.objects.filter(
        _enrolment_id__in=[e.id for e in enrolments]
    ).values_list("_enrolment_id", flat=True)
    return enrolments.exclude(id__in=reports_enrolment_ids)


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


def resolve_place_divisions(place_json) -> Optional[list]:
    # When fetching the event, the division field is under location
    # NOTE: Some places, e.g helsinki:internet, might not have divisions
    try:
        return [d["ocd_id"] for d in place_json["location"]["divisions"]]
    except (IndexError, KeyError, TypeError):
        return None


def resolve_place_coordinates(place_json) -> Optional[list]:
    # When fetching the event, the position field is under location
    # NOTE: Some places, e.g helsinki:internet, might not have coordinates
    if "location" in place_json:
        place_json = place_json["location"]
    try:
        return place_json["position"]["coordinates"]
    except (IndexError, KeyError, TypeError):
        return None
