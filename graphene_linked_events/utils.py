# https://stackoverflow.com/questions/6578986/how-to-convert-json-data
# -into-a-python-object/15882054#15882054
import datetime
import json
from collections import namedtuple

from django.conf import settings
from django.utils import timezone
from graphene_linked_events.rest_client import LinkedEventsApiClient

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
    return json2obj(format_response(response))


def get_keyword_set_by_id(keyword_set_id):
    params = {"include": "keywords"}
    return retrieve_linked_events_data("keyword_set", keyword_set_id, params=params,)


def get_linked_events_date_support(dt_value):
    if dt_value == "now":
        return datetime.datetime.now(tz=timezone.utc)
    if dt_value == "today":
        return datetime.date.today(tz=timezone.utc)
    return dt_value
