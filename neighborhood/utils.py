import json
from collections import namedtuple

from django.conf import settings
from neighborhood.rest_client import NeighborhoodApiClient

api_client = NeighborhoodApiClient(config=settings.NEIGHBORHOOD_API_CONFIG)


def format_response(response):
    return response.text


def json_object_hook(d):
    return namedtuple("X", d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=json_object_hook)


def format_request(request):
    return json.dumps(request)
