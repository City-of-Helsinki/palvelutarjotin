import math

import pytest
from reports.utils import get_event_keywords, get_event_provider, haversine


@pytest.fixture()
def events_json():
    return {
        "publisher": "ahjo:u541000",
        "provider": {"fi": "Organisaatio"},
        "keywords": [
            {
                "id": "yso:p10727",
                "data_source": "yso",
                "publisher": "hy:kansalliskirjasto",
                "name": {
                    "fi": "osallistuminen",
                    "sv": "deltagande",
                    "en": "participation",
                },
                "@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p10727/",
                "@type": "Keyword",
            },
            {
                "id": "yso:p14004",
                "data_source": "yso",
                "publisher": "hy:kansalliskirjasto",
                "name": {"fi": "keskustelu", "sv": "samtal", "en": "conversation"},
                "@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p14004/",
                "@type": "Keyword",
            },
        ],
    }


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
    assert math.isclose(haversine(lon1, lat1, lon2, lat2), distance_km)


def test_get_event_keywords(events_json):
    assert get_event_keywords(events_json) == [
        ("yso:p10727", "osallistuminen"),
        ("yso:p14004", "keskustelu"),
    ]


def test_get_event_provider(events_json):
    assert get_event_provider(events_json) == "Organisaatio"
