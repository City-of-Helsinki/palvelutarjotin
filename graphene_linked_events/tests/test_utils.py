import math

from graphene_linked_events.utils import bbox_for_coordinates


def test_bbox_for_coordinates():
    """
    Bounding box for Katri Valan puisto with a distance of 3 km from center to corner.
    """
    bbox = bbox_for_coordinates(24.963692, 60.186687, 3)

    assert math.isclose(bbox[0], 24.925482025464998)
    assert math.isclose(bbox[1], 60.16764173276239)
    assert math.isclose(bbox[2], 25.00194624440269)
    assert math.isclose(bbox[3], 60.20572118886215)
