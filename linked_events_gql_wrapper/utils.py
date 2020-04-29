# stolen from https://stackoverflow.com/questions/6578986/how-to-convert-json-data
# -into-a-python-object/15882054#15882054
import json
from collections import namedtuple

# def format_keys(keys):
#     return [format_key(k) for k in keys]

#
# def format_key(k):
#     k.replace("@", "internal_")
#     return k


def _json_object_hook(d):
    return namedtuple("X", d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)
