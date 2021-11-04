import json
from collections import namedtuple

from django.conf import settings
from servicemap.rest_client import ServicemapApiClient

api_client = ServicemapApiClient(config=settings.SERVICEMAP_API_CONFIG)


def json_object_hook(d):
    return namedtuple("X", d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=json_object_hook)


def format_request(request):
    return json.dumps(request)
