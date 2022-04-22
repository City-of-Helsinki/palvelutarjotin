import json
import math

import requests
import responses
from graphene_linked_events.utils import bbox_for_coordinates, format_response


def test_bbox_for_coordinates():
    """
    Bounding box for Katri Valan puisto with a distance of 3 km from center to corner.
    """
    bbox = bbox_for_coordinates(24.963692, 60.186687, 3)

    assert math.isclose(bbox[0], 24.925482025464998)
    assert math.isclose(bbox[1], 60.16764173276239)
    assert math.isclose(bbox[2], 25.00194624440269)
    assert math.isclose(bbox[3], 60.20572118886215)


def test_format_response(mocked_responses, snapshot):
    url = "http://localhost"
    response_data = {
        "data": [
            {
                "@id": 123,
                "email": "email1@example.com",
                "emails": ["email2@example.com", "email3@example.com"],
            },
            {"@key": "@@@", "@keys": [{"@key": "value"}, {"key": "@value"}]},
        ]
    }
    mocked_responses.add(responses.GET, url=url, json=response_data)

    response = requests.get(url)
    formatted = format_response(response)

    snapshot.assert_match(json.loads(formatted))
