# https://stackoverflow.com/questions/6578986/how-to-convert-json-data
# -into-a-python-object/15882054#15882054
import json
from collections import namedtuple

from django.conf import settings
from graphene_linked_events.rest_client import LinkedEventsApiClient

from palvelutarjotin.exceptions import ApiConnectionError, ObjectDoesNotExistError

api_client = LinkedEventsApiClient(config=settings.LINKED_EVENTS_API_CONFIG)


def format_response(response):
    # Some fields from api have @prefix that need to be converted
    return response.text.replace("@", "internal_")


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
        raise ApiConnectionError("Could not establish a connection to the API.")

    if response.status_code == 404:
        raise ObjectDoesNotExistError("Could not find the event from the API.")

    return json2obj(format_response(response))


def get_keyword_set_by_id(keyword_set_id):
    params = {"include": "keywords"}
    return retrieve_linked_events_data("keyword_set", keyword_set_id, params=params,)
