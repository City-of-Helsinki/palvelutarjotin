from decimal import Decimal

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry

LINKED_EVENTS_GEOS_PROJECTION_SRID = 3067


def get_distance(
    long1: Decimal, lat1: Decimal, long2: Decimal, lat2: Decimal
) -> Decimal:
    """Get a 3D distance in meters between the 2 coordinates."""
    start_coordinates = GEOSGeometry(
        f"SRID={LINKED_EVENTS_GEOS_PROJECTION_SRID};POINT({long1} {lat1})"
    )
    end_coordinates = GEOSGeometry(
        f"SRID={LINKED_EVENTS_GEOS_PROJECTION_SRID};POINT({long2} {lat2})"
    )
    return Distance(m=start_coordinates.distance(end_coordinates))
