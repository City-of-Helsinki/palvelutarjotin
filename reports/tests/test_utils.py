import pytest
from reports.utils import get_event_keywords, get_event_provider


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


def test_get_event_keywords(events_json):
    assert get_event_keywords(events_json) == [
        ("yso:p10727", "osallistuminen"),
        ("yso:p14004", "keskustelu"),
    ]


def test_get_event_provider(events_json):
    assert get_event_provider(events_json) == "Organisaatio"
