import pytest
from reports.utils import haversine

# from reports.utils import get_distance
# @pytest.mark.parametrize(
#     "lon1,lat1,lon2,lat2,distance_km",
#     [
#         [24.9384, 60.1699, 22.2666, 60.4518, 150.44]
#     ],  # Helsinki  # Turku  # Distance in km
# )
# def test_get_distance(
#     lon1: float, lat1: float, lon2: float, lat2: float, distance_km: float
# ):
#     assert get_distance(lon1, lat1, lon2, lat2) == distance_km


@pytest.mark.parametrize(
    "lon1,lat1,lon2,lat2,distance_km",
    [
        [24.9384, 60.1699, 22.2666, 60.4518, 150.4375814968687]
    ],  # From Helsinki to Turku, it's 150.4km
)
def test_haversine(
    lon1: float, lat1: float, lon2: float, lat2: float, distance_km: float
):
    assert haversine(lon1, lat1, lon2, lat2) == distance_km
