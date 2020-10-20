from copy import deepcopy
from datetime import timedelta

import pytest
from django.utils import timezone
from graphene_linked_events.tests.mock_data import EVENTS_DATA
from graphql_relay import to_global_id
from occurrences.factories import OccurrenceFactory, PalvelutarjotinEventFactory
from occurrences.models import PalvelutarjotinEvent

from common.tests.utils import assert_match_error_code, assert_permission_denied
from palvelutarjotin.consts import API_USAGE_ERROR


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


GET_EVENTS_QUERY = """
query Events($organisationId: String){
  events(organisationId: $organisationId){
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
      publicationStatus
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
      publicationStatus
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
      publicationStatus
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


def test_get_events(api_client, snapshot, mock_get_events_data, organisation):
    # Because of mock data, this test might not return correct result,
    # but the goal is to test if organisation argument work in `resolve_events`
    executed = api_client.execute(
        GET_EVENTS_QUERY,
        variables={"organisationId": to_global_id("OrganisationNode", organisation.id)},
    )
    snapshot.assert_match(executed)


def test_get_event(api_client, snapshot, mock_get_event_data):
    executed = api_client.execute(GET_EVENT_QUERY)
    snapshot.assert_match(executed)


def test_get_places(api_client, snapshot, mock_get_places_data):
    executed = api_client.execute(GET_PLACES_QUERY)
    snapshot.assert_match(executed)


def test_get_place(api_client, snapshot, mock_get_place_data):
    executed = api_client.execute(GET_PLACE_QUERY)
    snapshot.assert_match(executed)


def test_get_keywords(api_client, snapshot, mock_get_keywords_data):
    executed = api_client.execute(GET_KEYWORDS_QUERY)
    snapshot.assert_match(executed)


def test_get_keyword(api_client, snapshot, mock_get_keyword_data):
    executed = api_client.execute(GET_KEYWORD_QUERY)
    snapshot.assert_match(executed)


def test_search_places(api_client, snapshot, mock_search_places_data):
    executed = api_client.execute(SEARCH_PLACES_QUERY)
    snapshot.assert_match(executed)


def test_search_events(api_client, snapshot, mock_search_events_data):
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
          contactEmail
          contactPhoneNumber
          contactPerson
          {
            name
          }
          enrolmentEndDays
          enrolmentStart
          neededOccurrences
          linkedEventId
          organisation{
              name
          }
          autoAcceptance
        }
      }
    }
  }
}
"""

CREATE_EVENT_VARIABLES = {
    "input": {
        "organisationId": "",
        "pEvent": {
            "enrolmentStart": "2020-06-06T16:40:48+00:00",
            "enrolmentEndDays": 2,
            "neededOccurrences": 1,
            "contactPersonId": "",
            "contactPhoneNumber": "123123",
            "contactEmail": "contact@email.me",
            "autoAcceptance": True,
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
        "draft": True,
    }
}


def test_create_event_unauthorized(
    api_client, user_api_client, staff_api_client, person, organisation
):
    executed = api_client.execute(
        CREATE_EVENT_MUTATION, variables=CREATE_EVENT_VARIABLES
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        CREATE_EVENT_MUTATION, variables=CREATE_EVENT_VARIABLES
    )
    assert_permission_denied(executed)

    variables = deepcopy(CREATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )

    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )

    executed = staff_api_client.execute(CREATE_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)
    # Still contact person doesn't belong to organisation
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(CREATE_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)


def test_create_event(
    staff_api_client, snapshot, person, mock_create_event_data, organisation
):
    variables = deepcopy(CREATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = staff_api_client.execute(CREATE_EVENT_MUTATION, variables=variables)
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
          contactEmail
          contactPhoneNumber
          enrolmentEndDays
          enrolmentStart
          neededOccurrences
          linkedEventId
          organisation{
              name
          }
          contactPerson{
              name
          }
          autoAcceptance
        }
      }
    }
  }
}
"""

UPDATE_EVENT_VARIABLES = {
    "input": {
        "id": "qq:afy6aghr2y",
        "organisationId": "",
        "pEvent": {
            "enrolmentStart": "2020-06-06T16:40:48+00:00",
            "enrolmentEndDays": 2,
            "neededOccurrences": 1,
            "contactPhoneNumber": "123123",
            "contactEmail": "contact@email.me",
            "autoAcceptance": True,
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
        "draft": True,
    }
}


def test_update_event_unauthorized(
    api_client, user_api_client, person, staff_api_client, organisation
):
    executed = api_client.execute(
        UPDATE_EVENT_MUTATION, variables=UPDATE_EVENT_VARIABLES
    )
    assert_permission_denied(executed)
    executed = user_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=UPDATE_EVENT_VARIABLES
    )
    assert_permission_denied(executed)

    variables = deepcopy(UPDATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    executed = staff_api_client.execute(UPDATE_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)
    # Still contact person doesn't belong to organisation
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(UPDATE_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)


def test_update_event(
    staff_api_client, snapshot, person, mock_update_event_data, organisation
):
    variables = deepcopy(UPDATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    PalvelutarjotinEventFactory(
        linked_event_id=UPDATE_EVENT_VARIABLES["input"]["id"], organisation=organisation
    )
    staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = staff_api_client.execute(UPDATE_EVENT_MUTATION, variables=variables)
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


def test_delete_event(staff_api_client, snapshot, mock_delete_event_data):
    PalvelutarjotinEventFactory(linked_event_id="qq:afy57kkxdm")
    assert PalvelutarjotinEvent.objects.count() == 1
    executed = staff_api_client.execute(DELETE_EVENT_MUTATION)
    snapshot.assert_match(executed)
    assert PalvelutarjotinEvent.objects.count() == 0


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


def test_images_query(api_client, snapshot, mock_get_images_data):
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


def test_image_query(api_client, snapshot, mock_get_image_data):
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


def test_update_image(staff_api_client, snapshot, mock_update_image_data):
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


def test_delete_image(staff_api_client, snapshot, mock_delete_image_data):
    executed = staff_api_client.execute(DELETE_IMAGE_MUTATION)
    snapshot.assert_match(executed)


PUBLISH_EVENT_MUTATION = """
mutation publishEvent($input: PublishEventMutationInput!){
  publishEventMutation(event: $input){
    response{
      statusCode
      body {
        id
        startTime
        endTime
        publicationStatus
      }
    }
  }
}
"""


def test_publish_event_unauthorized(
    snapshot,
    api_client,
    user_api_client,
    staff_api_client,
    mock_update_event_data,
    organisation,
    person,
):
    # Reuse update event variables
    variables = deepcopy(UPDATE_EVENT_VARIABLES)
    del variables["input"]["draft"]
    executed = api_client.execute(PUBLISH_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)
    executed = user_api_client.execute(PUBLISH_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)

    variables = deepcopy(UPDATE_EVENT_VARIABLES)
    del variables["input"]["draft"]
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    p_event = PalvelutarjotinEventFactory(
        linked_event_id=UPDATE_EVENT_VARIABLES["input"]["id"], organisation=organisation
    )
    OccurrenceFactory(p_event=p_event)
    executed = staff_api_client.execute(PUBLISH_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)
    # Still contact person doesn't belong to organisation
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(PUBLISH_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)


def test_publish_event(
    snapshot,
    api_client,
    user_api_client,
    staff_api_client,
    mock_update_event_data,
    organisation,
    person,
):
    # Reuse update event variables
    variables = deepcopy(UPDATE_EVENT_VARIABLES)
    del variables["input"]["draft"]
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    p_event = PalvelutarjotinEventFactory(
        linked_event_id=UPDATE_EVENT_VARIABLES["input"]["id"], organisation=organisation
    )
    staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = staff_api_client.execute(PUBLISH_EVENT_MUTATION, variables=variables)
    # cannot publish event without occurrence
    assert_match_error_code(executed, API_USAGE_ERROR)
    OccurrenceFactory(p_event=p_event)
    executed = staff_api_client.execute(PUBLISH_EVENT_MUTATION, variables=variables)
    snapshot.assert_match(executed)


GET_EVENTS_QUERY_WITH_OCCURRENCES = """
query Events($organisationId: String){
  events(organisationId: $organisationId){
    meta {
      count
      next
      previous
    }
    data{
      id
      internalId
      pEvent{
          nextOccurrenceDatetime
          lastOccurrenceDatetime
      }
    }
  }
}
"""


def test_get_events_with_occurrences(
    api_client, snapshot, mock_get_events_data, organisation
):
    for e in EVENTS_DATA["data"]:
        p_event = PalvelutarjotinEventFactory(
            linked_event_id=e["id"], organisation=organisation
        )
        OccurrenceFactory.create(
            p_event=p_event, start_time=timezone.now() - timedelta(days=1)
        )
        OccurrenceFactory.create(
            p_event=p_event, start_time=timezone.now() + timedelta(days=1)
        )
        OccurrenceFactory.create(
            p_event=p_event, start_time=timezone.now() + timedelta(days=2)
        )
    executed = api_client.execute(
        GET_EVENTS_QUERY_WITH_OCCURRENCES,
        variables={"organisationId": to_global_id("OrganisationNode", organisation.id)},
    )
    snapshot.assert_match(executed)
