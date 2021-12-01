from math import asin, cos, radians, sin, sqrt
from typing import List, Optional

LINKED_EVENTS_GEOS_PROJECTION_SRID = 3067

"""
FIXME: get_distance would be better alternative to haversine(),
since it calculates the 3d distance.
Can the 3d distance really be twice the 2d distance or why is the number so much bigger?
"""
# from django.contrib.gis.measure import Distance
# from django.contrib.gis.geos import Point
# def get_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
#     """Get a 3D distance in meters between the 2 coordinates."""
#     start = Point(lon1, lat1, srid=LINKED_EVENTS_GEOS_PROJECTION_SRID)
#     end = Point(lon2, lat2, srid=LINKED_EVENTS_GEOS_PROJECTION_SRID)
#     return Distance(km=start.distance(end) * 100).km


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    HAversine formula: https://en.wikipedia.org/wiki/Haversine_formula.
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Determines return value units.
    return c * r


def get_event_provider(event_json: dict, language: str = "fi") -> Optional[str]:
    """Return a provider name in preferred language from given event json.

    Args:
        event_json (dict): [description]
        language (str, optional): [description]. Defaults to "fi".

    Returns:
        Optional[str]: [description]
    """
    return event_json["provider"]["fi"] if event_json["provider"] else None


def get_event_keywords(event_json: dict, language: str = "fi") -> List[str]:
    """Return event keywords in a format that is supported by EnrolmentReport model.

    Args:
        event_json (dict): event json fetched from LinkedEvents API
        language (str, optional): [description]. Defaults to "fi".

    Returns:
        List[str]: First argument is an index, second is a translation or an empty list
    """
    return (
        [
            (kw["id"], kw.get("name", {language: ""})[language]) if kw else ""
            for kw in event_json["keywords"]
        ]
        if event_json["keywords"]
        else []
    )
