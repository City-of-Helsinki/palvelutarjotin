import pytest
from graphene_linked_events.tests.mock_data import (
    CREATED_EVENT_DATA,
    EVENT_DATA,
    EVENTS_DATA,
    IMAGE_DATA,
    IMAGES_DATA,
    KEYWORD_DATA,
    KEYWORDS_DATA,
    PLACE_DATA,
    PLACES_DATA,
    UPDATE_EVENT_DATA,
)
from graphene_linked_events.tests.utils import MockResponse
from occurrences.factories import PalvelutarjotinEventFactory
from occurrences.models import PalvelutarjotinEvent

from common.tests.utils import assert_permission_denied


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


GET_EVENTS_QUERY = """
query Events{
  events{
    meta {
      count
      next
      previous
    }
    data{
      id
      internalId
      internalContext
      internalType
      createdTime
      lastModifiedTime
      dataSource
      publisher
      location {
        internalId
      }
      keywords {
        internalId
      }
      superEvent {
        internalId
      }
      eventStatus
      externalLinks {
        name
        link
        language
      }
      offers {
        isFree
      }
      subEvents {
        internalId
      }
      images {
        internalId
      }
      inLanguage {
        internalId
      }
      audience {
        internalId
      }
      datePublished
      startTime
      endTime
      customData
      audienceMinAge
      audienceMaxAge
      superEventType
      extensionCourse {
        enrolmentStartTime
        enrolmentEndTime
        maximumAttendeeCapacity
        minimumAttendeeCapacity
        remainingAttendeeCapacity
      }
      name {
        fi
        sv
        en
      }
      localizationExtraInfo {
        fi
        sv
        en
      }
      shortDescription {
        fi
        sv
        en
      }
      provider {
        fi
        sv
        en
      }
      infoUrl {
        fi
        sv
        en
      }
      providerContactInfo
      description {
        fi
        sv
        en
      }
    }
  }
}
"""

GET_EVENT_QUERY = """
query Event{
  event(id: "helmet:210309"){
      id
      internalId
      internalContext
      internalType
      createdTime
      lastModifiedTime
      dataSource
      publisher
      location {
        internalId
      }
      keywords {
        internalId
      }
      superEvent {
        internalId
      }
      eventStatus
      externalLinks {
        name
        link
        language
      }
      offers {
        isFree
      }
      subEvents {
        internalId
      }
      images {
        internalId
      }
      inLanguage {
        internalId
      }
      audience {
        internalId
      }
      datePublished
      startTime
      endTime
      customData
      audienceMinAge
      audienceMaxAge
      superEventType
      extensionCourse {
        enrolmentStartTime
        enrolmentEndTime
        maximumAttendeeCapacity
        minimumAttendeeCapacity
        remainingAttendeeCapacity
      }
      name {
        fi
        sv
        en
      }
      localizationExtraInfo {
        fi
        sv
        en
      }
      shortDescription {
        fi
        sv
        en
      }
      provider {
        fi
        sv
        en
      }
      infoUrl {
        fi
        sv
        en
      }
      providerContactInfo
      description {
        fi
        sv
        en
      }
  }
}
"""

GET_PLACES_QUERY = """
query Places{
  places(showAllPlaces: true){
    meta {
      count
      next
      previous
    }
    data{
      id
      internalId
      internalContext
      internalType
      createdTime
      lastModifiedTime
      dataSource
      publisher
      divisions {
        ocdId
        municipality
      }
      customData
      email
      contactType
      addressRegion
      postalCode
      postOfficeBoxNum
      addressCountry
      deleted
      nEvents
      image
      parent
      replacedBy
      position{
        type
        coordinates
      }
      name {
        fi
        sv
        en
      }
      description
      telephone {
        fi
        sv
        en
      }
      addressLocality {
        fi
        sv
        en
      }
      streetAddress {
        fi
        sv
        en
      }
      infoUrl {
        fi
        sv
        en
      }
    }
  }
}
"""

GET_PLACE_QUERY = """
query Place{
  place(id: "tprek:23253"){
      id
      internalId
      internalContext
      internalType
      createdTime
      lastModifiedTime
      dataSource
      publisher
      divisions {
        ocdId
        municipality
      }
      customData
      email
      contactType
      addressRegion
      postalCode
      postOfficeBoxNum
      addressCountry
      deleted
      nEvents
      image
      parent
      replacedBy
      position{
        type
        coordinates
      }
      name {
        fi
        sv
        en
      }
      description
      telephone {
        fi
        sv
        en
      }
      addressLocality {
        fi
        sv
        en
      }
      streetAddress {
        fi
        sv
        en
      }
      infoUrl {
        fi
        sv
        en
      }
  }
}
"""

GET_KEYWORDS_QUERY = """
query Keywords{
  keywords(showAllKeywords:true){
    meta {
      count
      next
      previous
    }
    data {
      id
      internalId
      internalType
      internalContext
      createdTime
      lastModifiedTime
      dataSource
      publisher
      altLabels
      aggregate
      deprecated
      nEvents
      image
      name {
        fi
        sv
        en
      }
    }
  }
}
"""

GET_KEYWORD_QUERY = """
query Keyword{
  keyword(id: "yso:p17411"){
      id
      internalId
      internalType
      internalContext
      createdTime
      lastModifiedTime
      dataSource
      publisher
      altLabels
      aggregate
      deprecated
      nEvents
      image
      name {
        fi
        sv
        en
      }
    }
}
"""

SEARCH_PLACES_QUERY = """
query placesSearch{
  placesSearch(input:"sib"){
    meta {
      count
      next
      previous
    }
    data{
      id
      internalId
      internalContext
      internalType
      createdTime
      lastModifiedTime
      dataSource
      publisher
      divisions {
        ocdId
        municipality
      }
      customData
      email
      contactType
      addressRegion
      postalCode
      postOfficeBoxNum
      addressCountry
      deleted
      nEvents
      image
      parent
      replacedBy
      position{
        type
        coordinates
      }
      name {
        fi
        sv
        en
      }
      description
      telephone {
        fi
        sv
        en
      }
      addressLocality {
        fi
        sv
        en
      }
      streetAddress {
        fi
        sv
        en
      }
      infoUrl {
        fi
        sv
        en
      }
    }
  }
}
"""

SEARCH_EVENTS_QUERY = """
query eventsSearch{
  eventsSearch(input:"sib"){
    meta {
      count
      next
      previous
    }
    data{
      id
      internalId
      internalContext
      internalType
      createdTime
      lastModifiedTime
      dataSource
      publisher
      location {
        internalId
      }
      keywords {
        internalId
      }
      superEvent {
        internalId
      }
      eventStatus
      externalLinks {
        name
        link
        language
      }
      offers {
        isFree
      }
      subEvents {
        internalId
      }
      images {
        internalId
      }
      inLanguage {
        internalId
      }
      audience {
        internalId
      }
      datePublished
      startTime
      endTime
      customData
      audienceMinAge
      audienceMaxAge
      superEventType
      extensionCourse {
        enrolmentStartTime
        enrolmentEndTime
        maximumAttendeeCapacity
        minimumAttendeeCapacity
        remainingAttendeeCapacity
      }
      name {
        fi
        sv
        en
      }
      localizationExtraInfo {
        fi
        sv
        en
      }
      shortDescription {
        fi
        sv
        en
      }
      provider {
        fi
        sv
        en
      }
      infoUrl {
        fi
        sv
        en
      }
      providerContactInfo
      description {
        fi
        sv
        en
      }
    }
  }
}
"""


def test_get_events(api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=EVENTS_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "list", mock_data
    )
    executed = api_client.execute(GET_EVENTS_QUERY)
    snapshot.assert_match(executed)


def test_get_event(api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=EVENT_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "retrieve", mock_data
    )
    executed = api_client.execute(GET_EVENT_QUERY)
    snapshot.assert_match(executed)


def test_get_places(api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=PLACES_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "list", mock_data
    )
    executed = api_client.execute(GET_PLACES_QUERY)
    snapshot.assert_match(executed)


def test_get_place(api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=PLACE_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "retrieve", mock_data
    )
    executed = api_client.execute(GET_PLACE_QUERY)
    snapshot.assert_match(executed)


def test_get_keywords(api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=KEYWORDS_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "list", mock_data
    )
    executed = api_client.execute(GET_KEYWORDS_QUERY)
    snapshot.assert_match(executed)


def test_get_keyword(api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=KEYWORD_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "retrieve", mock_data
    )
    executed = api_client.execute(GET_KEYWORD_QUERY)
    snapshot.assert_match(executed)


def test_search_places(api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=PLACES_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "search", mock_data
    )
    executed = api_client.execute(SEARCH_PLACES_QUERY)
    snapshot.assert_match(executed)


def test_search_events(api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=EVENTS_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "search", mock_data
    )
    executed = api_client.execute(SEARCH_EVENTS_QUERY)
    snapshot.assert_match(executed)


CREATE_EVENT_MUTATION = """
mutation addEvent($input: AddEventMutationInput!){
  addEventMutation(event: $input){
    response{
      statusCode
      body {
        id
        startTime
        location {
          id
        }
        keywords {
          id
        }
        description {
          fi
          sv
          en
        }
        shortDescription {
          fi
          sv
          en
        }
        offers {
          isFree
        }
        infoUrl {
          fi
          sv
          en
        }
        pEvent {
          enrolmentEnd
          enrolmentStart
          duration
          neededOccurrences
          linkedEventId
        }
      }
    }
  }
}
"""

CREATE_EVENT_VARIABLES = {
    "input": {
        "pEvent": {
            "enrolmentStart": "2020-06-06T16:40:48+00:00",
            "enrolmentEnd": "2021-06-06T16:40:48+00:00",
            "duration": 60,
            "neededOccurrences": 1,
        },
        "name": {"fi": "testaus"},
        "startTime": "2020-05-05",
        "location": {"internalId": "http://testserver/v1/place/tprek:9972/"},
        "keywords": [{"internalId": "http://testserver/v1/keyword/yso:p9999/"}],
        "shortDescription": {
            "fi": "short desc",
            "sv": "short desc sv",
            "en": "short desc en",
        },
        "description": {"fi": "desc", "sv": "desc sv", "en": "desc en"},
        "offers": [
            {
                "isFree": False,
                "price": {"en": "testing", "sv": "testning", "fi": "testaus"},
                "description": {"en": "testing", "sv": "testning", "fi": "testaus"},
                "infoUrl": {
                    "en": "http://localhost",
                    "sv": "http://localhost",
                    "fi": "http://localhost",
                },
            }
        ],
    }
}


def test_create_event_unauthorized(api_client, user_api_client):
    executed = api_client.execute(
        CREATE_EVENT_MUTATION, variables=CREATE_EVENT_VARIABLES
    )
    assert_permission_denied(executed)
    executed = user_api_client.execute(
        CREATE_EVENT_MUTATION, variables=CREATE_EVENT_VARIABLES
    )
    assert_permission_denied(executed)


def test_create_event(staff_api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=201, json_data=CREATED_EVENT_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "create", mock_data
    )

    executed = staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=CREATE_EVENT_VARIABLES
    )
    assert PalvelutarjotinEvent.objects.count() == 1
    snapshot.assert_match(executed)


UPDATE_EVENT_MUTATION = """
mutation addEvent($input: UpdateEventMutationInput!){
  updateEventMutation(event: $input){
    response{
      statusCode
      body {
        id
        startTime
        location {
          id
        }
        keywords {
          id
        }
        description {
          fi
          sv
          en
        }
        shortDescription {
          fi
          sv
          en
        }
        offers {
          isFree
        }
        infoUrl {
          fi
          sv
          en
        }
        pEvent {
          enrolmentEnd
          enrolmentStart
          duration
          neededOccurrences
          linkedEventId
        }
      }
    }
  }
}
"""

UPDATE_EVENT_VARIABLES = {
    "input": {
        "id": "qq:afy6aghr2y",
        "pEvent": {
            "enrolmentStart": "2020-06-06T16:40:48+00:00",
            "enrolmentEnd": "2021-06-06T16:40:48+00:00",
            "duration": 60,
            "neededOccurrences": 1,
        },
        "name": {"fi": "testaus"},
        "startTime": "2020-05-07",
        "location": {"internalId": "http://testserver/v1/place/tprek:9972/"},
        "keywords": [{"internalId": "http://testserver/v1/keyword/yso:p9999/"}],
        "shortDescription": {
            "fi": "short desc",
            "sv": "short desc sv",
            "en": "short desc en",
        },
        "description": {"fi": "desc", "sv": "desc sv", "en": "desc en"},
        "offers": [
            {
                "isFree": False,
                "price": {"en": "testing", "sv": "testning", "fi": "testaus"},
                "description": {"en": "testing", "sv": "testning", "fi": "testaus"},
                "infoUrl": {
                    "en": "http://localhost",
                    "sv": "http://localhost",
                    "fi": "http://localhost",
                },
            }
        ],
    }
}


def test_update_event_unauthorized(api_client, user_api_client):
    executed = api_client.execute(
        UPDATE_EVENT_MUTATION, variables=UPDATE_EVENT_VARIABLES
    )
    assert_permission_denied(executed)
    executed = user_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=UPDATE_EVENT_VARIABLES
    )
    assert_permission_denied(executed)


def test_update_event(staff_api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=UPDATE_EVENT_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "update", mock_data
    )

    PalvelutarjotinEventFactory(linked_event_id=UPDATE_EVENT_VARIABLES["input"]["id"],)

    executed = staff_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=UPDATE_EVENT_VARIABLES
    )
    snapshot.assert_match(executed)


DELETE_EVENT_MUTATION = """
mutation deleteEvent{
  deleteEventMutation(eventId:  "qq:afy57kkxdm"){
    response{
      statusCode
      body {
        name {
          fi
          sv
          en
        }
      }
    }
  }
}
"""


def test_delete_event_unauthorized(api_client, user_api_client):
    executed = api_client.execute(DELETE_EVENT_MUTATION)
    assert_permission_denied(executed)
    executed = user_api_client.execute(DELETE_EVENT_MUTATION)
    assert_permission_denied(executed)


def test_delete_event(staff_api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=204, json_data=None)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "delete", mock_data
    )

    executed = staff_api_client.execute(DELETE_EVENT_MUTATION)
    snapshot.assert_match(executed)


GET_IMAGES_QUERY = """
query Images{
  images{
    meta {
      count
      next
      previous
    }
    data {
      id
      url
      name
      photographerName
      altText
      cropping
      dataSource
    }
  }
}
"""


def test_images_query(api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=IMAGES_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "list", mock_data
    )
    executed = api_client.execute(GET_IMAGES_QUERY)
    snapshot.assert_match(executed)


GET_IMAGE_QUERY = """
query Image($id: ID!){
  image(id: $id){
      id
      url
      name
      photographerName
      altText
      cropping
      dataSource
  }
}
"""


def test_image_query(api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=IMAGE_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "retrieve", mock_data
    )
    executed = api_client.execute(GET_IMAGE_QUERY, variables={"id": "2036"})
    snapshot.assert_match(executed)


UPDATE_IMAGE_MUTATION = """
mutation updateImage($image: UpdateImageMutationInput!){
  updateImageMutation(image:  $image){
    response{
      statusCode
      body{
          id
          url
          name
          photographerName
          altText
          cropping
          dataSource
      }
    }
  }
}
"""

UPDATE_IMAGE_VARIABLES = {
    "image": {
        "id": "image_id",
        "license": "event_only",
        "name": "Image name",
        "cropping": "0,478,1920,2399",
        "altText": "Kaksi naista istuu tien laidassa",
    }
}


def test_update_image_unauthorized(api_client, user_api_client):
    executed = api_client.execute(
        UPDATE_IMAGE_MUTATION, variables=UPDATE_IMAGE_VARIABLES
    )
    assert_permission_denied(executed)
    executed = user_api_client.execute(
        UPDATE_IMAGE_MUTATION, variables=UPDATE_IMAGE_VARIABLES
    )
    assert_permission_denied(executed)


def test_update_image(staff_api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=200, json_data=IMAGE_DATA)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "update", mock_data
    )
    executed = staff_api_client.execute(
        UPDATE_IMAGE_MUTATION, variables=UPDATE_IMAGE_VARIABLES
    )
    snapshot.assert_match(executed)


DELETE_IMAGE_MUTATION = """
mutation deleteImage{
  deleteImageMutation(imageId:  "1"){
    response{
      statusCode
    }
  }
}
"""


def test_delete_image_unauthorized(api_client, user_api_client):
    executed = api_client.execute(DELETE_IMAGE_MUTATION)
    assert_permission_denied(executed)
    executed = user_api_client.execute(DELETE_IMAGE_MUTATION)
    assert_permission_denied(executed)


def test_delete_image(staff_api_client, snapshot, monkeypatch):
    def mock_data(*args, **kwargs):
        return MockResponse(status_code=204, json_data=None)

    import graphene_linked_events.rest_client

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient, "delete", mock_data
    )

    executed = staff_api_client.execute(DELETE_IMAGE_MUTATION)
    snapshot.assert_match(executed)
