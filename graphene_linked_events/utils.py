# https://stackoverflow.com/questions/6578986/how-to-convert-json-data
# -into-a-python-object/15882054#15882054
import json
from collections import namedtuple
from django.conf import settings
from geopy import distance as geopy_distance
from geopy import Point
from typing import List

from graphene_linked_events.rest_client import LinkedEventsApiClient
from palvelutarjotin.exceptions import ApiBadRequestError, ObjectDoesNotExistError

api_client = LinkedEventsApiClient(config=settings.LINKED_EVENTS_API_CONFIG)


def format_response(response):
    """Remove @ sign from API response JSON keys."""

    def format_values(value):
        if isinstance(value, list):
            return [format_values(v) for v in value]
        elif isinstance(value, dict):
            return {
                key.replace("@", "internal_"): format_values(value)
                for key, value in value.items()
            }
        return value

    formatted = format_values(json.loads(response.text))
    return json.dumps(formatted)


def json_object_hook(d):
    return namedtuple("X", d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=json_object_hook)


def format_request(request):
    # TODO: Find better way to replace internal_id key
    return json.dumps(request).replace("internal_", "@")


def retrieve_linked_events_data(resource, resource_id, params=None, is_staff=False):
    response = api_client.retrieve(
        resource, resource_id, params=params, is_staff=is_staff
    )

    if response.status_code == 400:
        raise ApiBadRequestError("Could not establish a connection to the API.")

    if response.status_code == 404:
        raise ObjectDoesNotExistError("Could not find the event from the API.")

    # Raise any other errors
    response.raise_for_status()

    return json2obj(format_response(response))


def get_keyword_set_by_id(keyword_set_id):
    params = {"include": "keywords"}
    return retrieve_linked_events_data(
        "keyword_set",
        keyword_set_id,
        params=params,
    )


def bbox_for_coordinates(
    longitude: float, latitude: float, distance: float
) -> List[float]:
    """
    Calculate bounding box for the given coordinates so that the
    bounding box corner is at the given distance (in km).
    """
    sw_bearing = 225
    ne_bearing = 45
    d = geopy_distance.distance(kilometers=distance)

    starting_point = Point(latitude=latitude, longitude=longitude)
    sw_point = d.destination(starting_point, bearing=sw_bearing)
    ne_point = d.destination(starting_point, bearing=ne_bearing)

    return [
        sw_point.longitude,
        sw_point.latitude,
        ne_point.longitude,
        ne_point.latitude,
    ]
