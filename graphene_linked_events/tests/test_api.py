import itertools
import json
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Optional
from unittest.mock import patch

import graphene_linked_events
import pytest
import responses
from django.utils import timezone
from graphene.utils.str_converters import to_snake_case
from graphene_linked_events.rest_client import LinkedEventsApiClient
from graphene_linked_events.schema import (
    api_client as graphene_linked_events_api_client,
)
from graphene_linked_events.schema import Query
from graphene_linked_events.tests.mock_data import (
    EVENT_DATA,
    EVENTS_DATA,
    KEYWORD_SET_DATA,
    UPDATE_EVENT_DATA,
)
from graphene_linked_events.tests.utils import MockResponse
from graphene_linked_events.utils import retrieve_linked_events_data
from graphql_relay import to_global_id
from occurrences.event_api_services import update_event_to_linkedevents_api
from occurrences.factories import OccurrenceFactory, PalvelutarjotinEventFactory
from occurrences.models import PalvelutarjotinEvent
from requests.models import HTTPError

from common.tests.utils import (
    assert_match_error_code,
    assert_permission_denied,
    mocked_json_response,
)
from palvelutarjotin.consts import API_USAGE_ERROR, DATA_VALIDATION_ERROR
from palvelutarjotin.exceptions import ApiBadRequestError, ObjectDoesNotExistError
from palvelutarjotin.settings import KEYWORD_SET_ID_MAPPING


def __eq_dt_with_tz(dt1: Optional[datetime], dt2: Optional[datetime]) -> bool:
    if dt1 and dt2:
        if isinstance(dt1, str):
            dt1 = datetime.fromisoformat(dt1)
        if isinstance(dt2, str):
            dt2 = datetime.fromisoformat(dt2)

        return dt1.utctimetuple() == dt2.utctimetuple()
    return dt1 == dt2


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


GET_EVENTS_QUERY = """
query Events(
    $organisationId: String,
    $keywordAnd: [String],
    $keywordNot: [String],
    $allOngoingAnd: [String],
    $allOngoingOr: [String]
){
  events(
      organisationId: $organisationId,
      keywordAnd: $keywordAnd,
      keywordNot: $keywordNot,
      allOngoingAnd: $allOngoingAnd,
      allOngoingOr: $allOngoingOr
  ){
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
      enrolmentStartTime
      enrolmentEndTime
      maximumAttendeeCapacity
      minimumAttendeeCapacity
      remainingAttendeeCapacity
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
      enrolmentStartTime
      enrolmentEndTime
      maximumAttendeeCapacity
      minimumAttendeeCapacity
      remainingAttendeeCapacity
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
      categories{
        id
      }
      additionalCriteria{
        id
      }
      activities{
        id
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
      enrolmentStartTime
      enrolmentEndTime
      maximumAttendeeCapacity
      minimumAttendeeCapacity
      remainingAttendeeCapacity
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


@pytest.mark.django_db
def test_get_events(api_client, snapshot, mock_get_events_data, organisation):
    # Because of mock data, this test might not return correct result,
    # but the goal is to test if organisation argument work in `resolve_events`

    # NOTE: Only events that have a p_event in database should be returned.
    linked_event_id = EVENTS_DATA["data"][0]["id"]
    PalvelutarjotinEventFactory(linked_event_id=linked_event_id)
    executed = api_client.execute(
        GET_EVENTS_QUERY,
        variables={"organisationId": to_global_id("OrganisationNode", organisation.id)},
    )
    assert EVENTS_DATA["meta"]["count"] == 151775
    assert len(EVENTS_DATA["data"]) == 2
    # NOTE: LinkedEvents paginates the results, but Kultus API filters
    # the paginated sets. This leads to a situation where the events
    # count in meta data, easily does not match with the fact.
    assert executed["data"]["events"]["meta"]["count"] == 151775
    assert executed["data"]["events"]["data"][0]["id"] == linked_event_id
    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_pevent_preadded_with_test_events_p_event_relations():
    p_event = PalvelutarjotinEventFactory(linked_event_id=EVENTS_DATA["data"][0]["id"])
    result = Query._test_events_p_event_relations(json.dumps(EVENTS_DATA))
    assert result.data[0].p_event.id == p_event.id


@pytest.mark.django_db
@pytest.mark.parametrize(
    "given,expected",
    [
        ("keywordAnd", "keyword_AND"),
        ("keywordNot", "keyword!"),
        ("allOngoingAnd", "all_ongoing_AND"),
        ("allOngoingOr", "all_ongoing_OR"),
    ],
)
def test_resolve_events_unsupported_parameter_mapping(
    given, expected, api_client, mock_get_events_data, organisation
):
    linked_event_id = EVENTS_DATA["data"][0]["id"]
    organisation_id = to_global_id("OrganisationNode", organisation.id)
    PalvelutarjotinEventFactory(linked_event_id=linked_event_id)
    with patch.object(LinkedEventsApiClient, "list") as linkedEventsApiClientMock:
        api_client.execute(
            GET_EVENTS_QUERY,
            variables={"organisationId": organisation_id, given: ["test"]},
        )

    linkedEventsApiClientMock.assert_called_with(
        "event",
        filter_list={"publisher": organisation.publisher_id, expected: ["test"]},
        is_staff=False,
    )


def test_get_event(api_client, snapshot, monkeypatch):
    def _get_mock_function(event_data, keyword_data, status_code=200):
        def mock_data(*args, **kwargs):
            if args[1] == "event":
                data = event_data
            else:
                data = keyword_data
            return MockResponse(status_code=status_code, json_data=data)

        return mock_data

    monkeypatch.setattr(
        graphene_linked_events.rest_client.LinkedEventsApiClient,
        "retrieve",
        _get_mock_function(EVENT_DATA, KEYWORD_SET_DATA),
    )
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
          externalEnrolmentUrl
          neededOccurrences
          linkedEventId
          organisation{
              name
          }
          autoAcceptance
          mandatoryAdditionalInformation
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
            "mandatoryAdditionalInformation": True,
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


def test_create_invalid_event(
    staff_api_client, snapshot, person, mock_create_event_data, organisation
):
    variables = deepcopy(CREATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"] = {
        "contactPersonId": to_global_id("PersonNode", person.id),
        "neededOccurrences": 2,
        "autoAcceptance": False,
    }
    staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = staff_api_client.execute(CREATE_EVENT_MUTATION, variables=variables)
    assert_match_error_code(executed, DATA_VALIDATION_ERROR)


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


P_EVENT_WITH_EXTERNAL_ENROLMENT_VARIABLES = {
    "externalEnrolmentUrl": "http://test.org",
    "enrolmentStart": None,
    "enrolmentEndDays": None,
    "neededOccurrences": 0,
    "autoAcceptance": False,
}


def test_create_event_with_external_enrolment(
    staff_api_client, snapshot, person, mock_create_event_data, organisation
):
    variables = deepcopy(CREATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    variables["input"]["pEvent"] = {
        **variables["input"]["pEvent"],
        **P_EVENT_WITH_EXTERNAL_ENROLMENT_VARIABLES,
    }

    staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = staff_api_client.execute(CREATE_EVENT_MUTATION, variables=variables)
    assert PalvelutarjotinEvent.objects.count() == 1
    snapshot.assert_match(executed)


P_EVENT_WITHOUT_ENROLMENT_VARIABLES = {
    "externalEnrolmentUrl": None,
    "enrolmentStart": None,
    "enrolmentEndDays": None,
    "neededOccurrences": 0,
    "autoAcceptance": False,
}


def test_create_event_without_enrolment(
    staff_api_client, snapshot, person, mock_create_event_data, organisation
):
    variables = deepcopy(CREATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )

    variables["input"]["pEvent"] = {
        **variables["input"]["pEvent"],
        **P_EVENT_WITHOUT_ENROLMENT_VARIABLES,
    }

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
          externalEnrolmentUrl
          neededOccurrences
          linkedEventId
          organisation{
              name
          }
          contactPerson{
              name
          }
          autoAcceptance
          mandatoryAdditionalInformation
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
            "mandatoryAdditionalInformation": True,
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
        linked_event_id=UPDATE_EVENT_VARIABLES["input"]["id"],
        organisation=organisation,
        auto_acceptance=True,
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
    mock_get_draft_event_data,
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


@patch.object(
    graphene_linked_events_api_client,
    "update",
    return_value=MockResponse(status_code=200, json_data=UPDATE_EVENT_DATA),
)
@pytest.mark.parametrize("p_event_enrolment_start", [None, timezone.now()])
def test_publish_event(
    mocked_update_event_data,
    p_event_enrolment_start,
    snapshot,
    api_client,
    user_api_client,
    staff_api_client,
    mock_get_draft_event_data,
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
        linked_event_id=UPDATE_EVENT_VARIABLES["input"]["id"],
        organisation=organisation,
        enrolment_start=p_event_enrolment_start,
    )
    staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = staff_api_client.execute(PUBLISH_EVENT_MUTATION, variables=variables)
    # cannot publish event without occurrence
    assert_match_error_code(executed, API_USAGE_ERROR)
    occurrence = OccurrenceFactory(p_event=p_event)
    assert occurrence.start_time is not None
    assert occurrence.end_time is not None
    executed = staff_api_client.execute(PUBLISH_EVENT_MUTATION, variables=variables)
    event_response = json.loads(mocked_update_event_data.call_args[0][2])
    assert __eq_dt_with_tz(event_response["start_time"], occurrence.start_time)
    assert __eq_dt_with_tz(event_response["end_time"], occurrence.end_time)
    assert __eq_dt_with_tz(
        event_response["enrolment_start_time"], p_event.enrolment_start
    )
    if p_event.enrolment_start:
        assert __eq_dt_with_tz(
            event_response["enrolment_end_time"],
            occurrence.start_time - timedelta(days=p_event.enrolment_end_days),
        )

    snapshot.assert_match(executed)


def test_publish_event_with_external_enrolments(
    snapshot,
    api_client,
    user_api_client,
    staff_api_client,
    mock_update_event_data,
    mock_get_draft_event_data,
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
    p_event = PalvelutarjotinEventFactory.create(
        **{
            "linked_event_id": UPDATE_EVENT_VARIABLES["input"]["id"],
            "organisation": organisation,
            **{
                to_snake_case(key): value
                for key, value in P_EVENT_WITH_EXTERNAL_ENROLMENT_VARIABLES.items()
            },
        }
    )
    staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    OccurrenceFactory(p_event=p_event)
    executed = staff_api_client.execute(PUBLISH_EVENT_MUTATION, variables=variables)
    snapshot.assert_match(executed)


def test_publish_event_without_enrolments(
    snapshot,
    api_client,
    user_api_client,
    staff_api_client,
    mock_update_event_data,
    mock_get_draft_event_data,
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
    p_event = PalvelutarjotinEventFactory.create(
        **{
            "linked_event_id": UPDATE_EVENT_VARIABLES["input"]["id"],
            "organisation": organisation,
            **{
                to_snake_case(key): value
                for key, value in P_EVENT_WITHOUT_ENROLMENT_VARIABLES.items()
            },
        }
    )
    staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    OccurrenceFactory(p_event=p_event)
    executed = staff_api_client.execute(PUBLISH_EVENT_MUTATION, variables=variables)
    snapshot.assert_match(executed)


UNPUBLISH_EVENT_MUTATION = """
mutation unpublishEvent($input: PublishEventMutationInput!){
  unpublishEventMutation(event: $input){
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


def test_unpublish_event_unauthorized(
    snapshot,
    api_client,
    user_api_client,
    staff_api_client,
    mock_update_event_data,
    mock_get_event_data,
    organisation,
    person,
):
    # Reuse update event variables
    variables = deepcopy(UPDATE_EVENT_VARIABLES)
    del variables["input"]["draft"]
    executed = api_client.execute(UNPUBLISH_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)
    executed = user_api_client.execute(UNPUBLISH_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)

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
    executed = staff_api_client.execute(UNPUBLISH_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)
    # Still contact person doesn't belong to organisation
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(UNPUBLISH_EVENT_MUTATION, variables=variables)
    assert_permission_denied(executed)


def test_unpublish_event(
    snapshot,
    api_client,
    staff_api_client,
    mock_unpublish_event_data,
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
    PalvelutarjotinEventFactory(
        linked_event_id=UPDATE_EVENT_VARIABLES["input"]["id"], organisation=organisation
    )
    staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = staff_api_client.execute(UNPUBLISH_EVENT_MUTATION, variables=variables)
    # Mock data might not reflect correct publication status
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
    api_client, snapshot, mock_get_events_data, mock_get_event_data, organisation
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


@pytest.mark.parametrize("occurrences_count", [5, 100, 150, 400, 500])
def test_get_event_with_occurrences_limit(
    occurrences_count, api_client, mock_get_event_data, organisation
):
    p_event = PalvelutarjotinEventFactory(
        linked_event_id=EVENT_DATA["id"], organisation=organisation
    )

    OccurrenceFactory.create_batch(occurrences_count, p_event=p_event)

    executed = api_client.execute(
        """
        query Event{
          event(id: "helmet:210309"){
            pEvent{
              occurrences {
                edges {
                  node {
                    id
                  }
                }
              }
              nextOccurrenceDatetime
              lastOccurrenceDatetime
            }
          }
        }
        """,
        variables={"organisationId": to_global_id("OrganisationNode", organisation.id)},
    )
    if occurrences_count > 400:
        assert len(executed["data"]["event"]["pEvent"]["occurrences"]["edges"]) == 400
    else:
        assert (
            len(executed["data"]["event"]["pEvent"]["occurrences"]["edges"])
            == occurrences_count
        )


GET_UPCOMING_EVENTS_QUERY = """
query UpcomingEvents {
  upcomingEvents {
    meta {
      count
    }
    data {
      id
      pEvent {
        linkedEventId
      }
    }
  }
}
"""


@pytest.mark.parametrize(
    "upcoming,past,cancelled", itertools.product((True, False), repeat=3)
)
def test_get_upcoming_events(
    api_client,
    organisation,
    mocked_responses,
    settings,
    snapshot,
    upcoming,
    past,
    cancelled,
):
    """
    Event are ordered so that the event with the next upcoming occurrence is first.
    """
    mocked_responses.assert_all_requests_are_fired = False
    UPCOMING_MOCKED_EVENTS = []

    for i in range(1, 4):
        p_event = PalvelutarjotinEventFactory(
            linked_event_id=f"kultus:{i}", organisation=organisation
        )
        MOCK_EVENT_DATA = {**EVENT_DATA, "id": p_event.linked_event_id}
        mocked_responses.add(
            responses.GET,
            url=settings.LINKED_EVENTS_API_CONFIG["ROOT"]
            + f"event/{p_event.linked_event_id}/",
            json=MOCK_EVENT_DATA,
        )
        mocked_responses.add(
            responses.PUT,
            url=settings.LINKED_EVENTS_API_CONFIG["ROOT"]
            + f"event/{p_event.linked_event_id}/",
            json=MOCK_EVENT_DATA,
        )

        if cancelled:
            # Cancelled but would be next
            start = timezone.now() + timedelta(days=i)
            end = start + timedelta(hours=1)
            OccurrenceFactory.create(
                p_event=p_event, start_time=start, end_time=end, cancelled=True
            )

        if past:
            # In the past
            start = timezone.now() - timedelta(days=5) + timedelta(days=i)
            end = start + timedelta(hours=1)
            OccurrenceFactory.create(p_event=p_event, start_time=start, end_time=end)

        if upcoming:
            # Event should be ordered reverse to the creation order.
            start = timezone.now() + timedelta(days=8) - timedelta(days=i)
            end = start + timedelta(hours=1)
            OccurrenceFactory.create(p_event=p_event, start_time=start, end_time=end)

            UPCOMING_MOCKED_EVENTS.append(MOCK_EVENT_DATA)

    if upcoming:
        query_string = "ids=kultus:3,kultus:2,kultus:1"
        mocked_responses.add(
            responses.GET,
            url=f"{settings.LINKED_EVENTS_API_CONFIG['ROOT']}event/?{query_string}",
            json={
                "meta": {
                    "count": len(UPCOMING_MOCKED_EVENTS),
                    "next": None,
                    "previous": None,
                },
                "data": UPCOMING_MOCKED_EVENTS,
            },
        )

    executed = api_client.execute(GET_UPCOMING_EVENTS_QUERY)

    if upcoming:
        assert executed["data"]["upcomingEvents"]["data"][0]["id"] == "kultus:3"
        assert executed["data"]["upcomingEvents"]["data"][1]["id"] == "kultus:2"
        assert executed["data"]["upcomingEvents"]["data"][2]["id"] == "kultus:1"
    else:
        assert executed["data"]["upcomingEvents"]["data"] == []

    snapshot.assert_match(executed)


GET_KEYWORD_SET_QUERY = """
query getKeywordSet($setType: KeywordSetType!){
  keywordSet(setType: $setType){
    id
    internalId
    keywords{
      name {
        fi
        sv
        en
      }
      id
      internalId
    }
  }
}
"""


def test_get_keyword_set(api_client, snapshot, mock_get_keyword_set_data):
    for set_type in KEYWORD_SET_ID_MAPPING:
        executed = api_client.execute(
            GET_KEYWORD_SET_QUERY, variables={"setType": set_type}
        )
        snapshot.assert_match(executed)


POPULAR_KULTUS_KEYWORDS_QUERY = """
query kws($amount: Int, $showAllKeywords: Boolean) {
  popularKultusKeywords(amount: $amount, showAllKeywords: $showAllKeywords) {
    meta {
      count
    }
    data {
      name {
        fi
        sv
        en
      }
      id
      internalId
      dataSource
      nEvents
    }
  }
}
"""


@pytest.mark.parametrize(
    "all_keywords,amount,expected_results",
    [(None, None, 1), (True, None, 2), (True, 1, 1)],
)
def test_get_popular_kultus_keywords(
    api_client,
    snapshot,
    mock_get_popular_kultus_keywords,
    all_keywords,
    amount,
    expected_results,
):

    executed = api_client.execute(
        POPULAR_KULTUS_KEYWORDS_QUERY,
        variables={"amount": amount, "showAllKeywords": all_keywords},
    )
    # All keyword sets return the same keyword, duplicates should get removed.
    assert (
        executed["data"]["popularKultusKeywords"]["meta"]["count"] == expected_results
    )
    snapshot.assert_match(executed)


@pytest.mark.parametrize(
    "status_code,error_cls",
    [(400, ApiBadRequestError), (404, ObjectDoesNotExistError)],
)
def test_linkedevents_api_retrieve_errors(status_code, error_cls):
    with patch.object(
        LinkedEventsApiClient,
        "retrieve",
        return_value=mocked_json_response(data=None, status_code=status_code),
    ):
        with pytest.raises(error_cls):
            retrieve_linked_events_data("event", 1)


@pytest.mark.parametrize(
    "status_code,error_cls",
    [(400, ApiBadRequestError), (404, ObjectDoesNotExistError), (500, HTTPError)],
)
def test_linkedevents_api_update_errors(status_code, error_cls):
    with patch.object(
        LinkedEventsApiClient,
        "update",
        return_value=mocked_json_response(data=None, status_code=status_code),
    ):
        with pytest.raises(error_cls):
            update_event_to_linkedevents_api("linked_event_id", {})
