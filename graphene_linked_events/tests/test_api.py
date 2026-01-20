import itertools
import json
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Optional
from unittest.mock import patch

import pytest
import responses
from django.utils import timezone
from graphene.utils.str_converters import to_snake_case
from graphql_relay import to_global_id
from requests.models import HTTPError

import graphene_linked_events
from common.tests.utils import (
    assert_match_error_code,
    assert_permission_denied,
    mocked_json_response,
)
from graphene_linked_events.rest_client import LinkedEventsApiClient
from graphene_linked_events.schema import Query
from graphene_linked_events.schema import (
    api_client as graphene_linked_events_api_client,
)
from graphene_linked_events.tests.mock_data import (
    EVENT_DATA,
    EVENTS_DATA,
    KEYWORD_SET_DATA,
    POPULAR_KEYWORD_SET_DATA,
    UPDATE_EVENT_DATA,
)
from graphene_linked_events.tests.utils import MockResponse
from graphene_linked_events.utils import retrieve_linked_events_data
from occurrences.event_api_services import update_event_to_linkedevents_api
from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
)
from occurrences.models import Occurrence, PalvelutarjotinEvent
from palvelutarjotin.consts import API_USAGE_ERROR, DATA_VALIDATION_ERROR
from palvelutarjotin.exceptions import ApiBadRequestError, ObjectDoesNotExistError


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
    $keywordOrSet1: [String],
    $keywordOrSet2: [String],
    $keywordOrSet3: [String],
    $keywordNot: [String],
    $allOngoingAnd: [String],
    $allOngoingOr: [String]
){
  events(
      organisationId: $organisationId,
      keywordAnd: $keywordAnd,
      keywordOrSet1: $keywordOrSet1,
      keywordOrSet2: $keywordOrSet2,
      keywordOrSet3: $keywordOrSet3,
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
        ("keywordOrSet1", "keyword_OR_set1"),
        ("keywordOrSet2", "keyword_OR_set2"),
        ("keywordOrSet3", "keyword_OR_set3"),
    ],
)
def test_resolve_events_parameter_mapping(
    given, expected, api_client, mock_get_events_data, organisation
):
    linked_event_id = EVENTS_DATA["data"][0]["id"]
    organisation_id = to_global_id("OrganisationNode", organisation.id)
    PalvelutarjotinEventFactory(linked_event_id=linked_event_id)
    with patch.object(LinkedEventsApiClient, "list") as linked_events_api_client_mock:
        api_client.execute(
            GET_EVENTS_QUERY,
            variables={"organisationId": organisation_id, given: ["test"]},
        )

    linked_events_api_client_mock.assert_called_with(
        "event",
        filter_list={"publisher": organisation.publisher_id, expected: ["test"]},
        is_event_staff=False,
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


def test_get_event_without_location(api_client, snapshot, monkeypatch):
    def _get_mock_function(event_data, keyword_data, status_code=200):
        def mock_data(*args, **kwargs):
            if args[1] == "event":
                data = event_data.copy()
                del event_data["location"]
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


def test_get_event_not_found(api_client, snapshot, monkeypatch):
    def _get_mock_function(event_data, keyword_data, status_code=404):
        def mock_data(*args, **kwargs):
            return MockResponse(status_code=status_code, json_data={})

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
          autoAcceptanceMessage
          translations {
            autoAcceptanceMessage
            languageCode
          }
          mandatoryAdditionalInformation
          isQueueingAllowed
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
            "translations": [
                {
                    "autoAcceptanceMessage": "Automaattisen hyväksynnän viesti",
                    "languageCode": "FI",
                },
                {
                    "autoAcceptanceMessage": "Custom message of auto approvance",
                    "languageCode": "EN",
                },
            ],
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
    api_client, user_api_client, event_staff_api_client, person, organisation
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

    executed = event_staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=variables
    )
    assert_permission_denied(executed)
    # Still contact person doesn't belong to organisation
    event_staff_api_client.user.person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=variables
    )
    assert_permission_denied(executed)


def test_create_invalid_event(
    event_staff_api_client, snapshot, person, mock_create_event_data, organisation
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
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=variables
    )
    assert_match_error_code(executed, DATA_VALIDATION_ERROR)


def test_create_event_without_organisation_id(
    event_staff_api_client, person, mock_create_event_data, organisation
):
    variables = deepcopy(CREATE_EVENT_VARIABLES)
    del variables["input"]["organisationId"]
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    assert "organisationId" not in variables["input"]
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=variables
    )
    assert PalvelutarjotinEvent.objects.count() == 0
    assert executed.get("errors")
    assert executed["errors"][0]["extensions"]["code"] == "GENERAL_ERROR"
    assert (
        "Field 'organisationId' of required type 'String!' was not provided."
        in executed["errors"][0]["message"]
    )


def test_create_event_with_null_organisation_id(
    event_staff_api_client, person, mock_create_event_data, organisation
):
    variables = deepcopy(CREATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = None
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=variables
    )
    assert PalvelutarjotinEvent.objects.count() == 0
    assert executed.get("errors")
    assert executed["errors"][0]["extensions"]["code"] == "GENERAL_ERROR"
    assert (
        "Variable '$input' got invalid value None at 'input.organisationId'; "
        + "Expected non-nullable type 'String!' not to be None."
    ) in executed["errors"][0]["message"]


@pytest.mark.parametrize("organisation_id", ["", " ", " " * 10])
def test_create_event_with_empty_or_whitespace_only_organisation_id(
    event_staff_api_client,
    person,
    mock_create_event_data,
    organisation,
    organisation_id,
):
    variables = deepcopy(CREATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = organisation_id
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=variables
    )
    assert PalvelutarjotinEvent.objects.count() == 0
    assert executed.get("errors")
    assert executed["errors"][0]["extensions"]["code"] == "GENERAL_ERROR"
    assert "Invalid Global ID" in executed["errors"][0]["message"]


def test_create_event(
    event_staff_api_client, snapshot, person, mock_create_event_data, organisation
):
    variables = deepcopy(CREATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=variables
    )
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
    event_staff_api_client, snapshot, person, mock_create_event_data, organisation
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

    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=variables
    )
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
    event_staff_api_client, snapshot, person, mock_create_event_data, organisation
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

    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=variables
    )
    assert PalvelutarjotinEvent.objects.count() == 1
    snapshot.assert_match(executed)


def test_create_event_without_p_event_translations(
    event_staff_api_client, snapshot, person, mock_create_event_data, organisation
):
    variables = deepcopy(CREATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    del variables["input"]["pEvent"]["translations"]
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        CREATE_EVENT_MUTATION, variables=variables
    )
    assert PalvelutarjotinEvent.objects.count() == 1
    snapshot.assert_match(executed)


@patch("graphene_linked_events.schema.api_client.delete")
def test_create_event_with_p_event_creation_exception_raised(
    spy_api_client_delete,
    event_staff_api_client,
    person,
    mock_create_event_data,
    mock_delete_event_data,
    organisation,
):
    def mock_get_or_create(p_event_data):
        raise Exception("A creation exception from get_or_create -method.")

    variables = deepcopy(CREATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    del variables["input"]["pEvent"]["translations"]
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)

    with patch(
        "occurrences.models.PalvelutarjotinEvent.objects.get_or_create",
        mock_get_or_create,
    ):
        event_staff_api_client.execute(CREATE_EVENT_MUTATION, variables=variables)
        spy_api_client_delete.assert_called_once()
    assert PalvelutarjotinEvent.objects.count() == 0


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
          autoAcceptanceMessage
          translations {
            autoAcceptanceMessage
            languageCode
          }
          mandatoryAdditionalInformation
          isQueueingAllowed
        }
      }
    }
  }
}
"""

UPDATE_EVENT_VARIABLES = {
    "input": {
        "id": "helsinki:afy6aghr2y",
        "organisationId": "",
        "pEvent": {
            "enrolmentStart": "2020-06-06T16:40:48+00:00",
            "enrolmentEndDays": 2,
            "neededOccurrences": 1,
            "contactPhoneNumber": "123123",
            "contactEmail": "contact@email.me",
            "autoAcceptance": True,
            "translations": [
                {"autoAcceptanceMessage": "Päivitetty viesti", "languageCode": "FI"},
                {
                    "autoAcceptanceMessage": "Updated custom message",
                    "languageCode": "EN",
                },
            ],
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
    api_client, user_api_client, person, event_staff_api_client, organisation
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
    executed = event_staff_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=variables
    )
    assert_permission_denied(executed)
    # Still contact person doesn't belong to organisation
    event_staff_api_client.user.person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=variables
    )
    assert_permission_denied(executed)


def test_update_event(
    event_staff_api_client, snapshot, person, mock_update_event_data, organisation
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
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=variables
    )
    snapshot.assert_match(executed)


def test_update_event_without_organisation_id(
    event_staff_api_client, person, mock_update_event_data, organisation
):
    variables = deepcopy(UPDATE_EVENT_VARIABLES)
    del variables["input"]["organisationId"]
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    assert "organisationId" not in variables["input"]
    PalvelutarjotinEventFactory(
        linked_event_id=UPDATE_EVENT_VARIABLES["input"]["id"],
        organisation=organisation,
        auto_acceptance=True,
    )
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=variables
    )
    assert executed.get("errors")
    assert executed["errors"][0]["extensions"]["code"] == "GENERAL_ERROR"
    assert (
        "Field 'organisationId' of required type 'String!' was not provided."
        in executed["errors"][0]["message"]
    )


def test_update_event_with_null_organisation_id(
    event_staff_api_client, person, mock_update_event_data, organisation
):
    variables = deepcopy(UPDATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = None
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    PalvelutarjotinEventFactory(
        linked_event_id=UPDATE_EVENT_VARIABLES["input"]["id"],
        organisation=organisation,
        auto_acceptance=True,
    )
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=variables
    )
    assert executed.get("errors")
    assert executed["errors"][0]["extensions"]["code"] == "GENERAL_ERROR"
    assert (
        "Variable '$input' got invalid value None at 'input.organisationId'; "
        + "Expected non-nullable type 'String!' not to be None."
    ) in executed["errors"][0]["message"]


@pytest.mark.parametrize("organisation_id", ["", " ", " " * 10])
def test_update_event_with_empty_or_whitespace_only_organisation_id(
    event_staff_api_client,
    person,
    mock_update_event_data,
    organisation,
    organisation_id,
):
    variables = deepcopy(UPDATE_EVENT_VARIABLES)
    variables["input"]["organisationId"] = organisation_id
    variables["input"]["pEvent"]["contactPersonId"] = to_global_id(
        "PersonNode", person.id
    )
    PalvelutarjotinEventFactory(
        linked_event_id=UPDATE_EVENT_VARIABLES["input"]["id"],
        organisation=organisation,
        auto_acceptance=True,
    )
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=variables
    )
    assert executed.get("errors")
    assert executed["errors"][0]["extensions"]["code"] == "GENERAL_ERROR"
    assert "Invalid Global ID" in executed["errors"][0]["message"]


DELETE_EVENT_MUTATION = """
mutation deleteEvent{
  deleteEventMutation(eventId:  "helsinki:afy57kkxdm"){
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


def test_delete_event(event_staff_api_client, snapshot, mock_delete_event_data):
    PalvelutarjotinEventFactory(linked_event_id="helsinki:afy57kkxdm")
    assert PalvelutarjotinEvent.objects.count() == 1
    executed = event_staff_api_client.execute(DELETE_EVENT_MUTATION)
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


def test_update_image(event_staff_api_client, snapshot, mock_update_image_data):
    executed = event_staff_api_client.execute(
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


def test_delete_image(event_staff_api_client, snapshot, mock_delete_image_data):
    executed = event_staff_api_client.execute(DELETE_IMAGE_MUTATION)
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
    event_staff_api_client,
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
    executed = event_staff_api_client.execute(
        PUBLISH_EVENT_MUTATION, variables=variables
    )
    assert_permission_denied(executed)
    # Still contact person doesn't belong to organisation
    event_staff_api_client.user.person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        PUBLISH_EVENT_MUTATION, variables=variables
    )
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
    event_staff_api_client,
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
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        PUBLISH_EVENT_MUTATION, variables=variables
    )
    # cannot publish event without occurrence
    assert_match_error_code(executed, API_USAGE_ERROR)
    occurrence = OccurrenceFactory(p_event=p_event)
    assert occurrence.start_time is not None
    assert occurrence.end_time is not None
    executed = event_staff_api_client.execute(
        PUBLISH_EVENT_MUTATION, variables=variables
    )
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
    event_staff_api_client,
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
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    OccurrenceFactory(p_event=p_event)
    executed = event_staff_api_client.execute(
        PUBLISH_EVENT_MUTATION, variables=variables
    )
    snapshot.assert_match(executed)


def test_publish_event_without_enrolments(
    snapshot,
    api_client,
    user_api_client,
    event_staff_api_client,
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
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    OccurrenceFactory(p_event=p_event)
    executed = event_staff_api_client.execute(
        PUBLISH_EVENT_MUTATION, variables=variables
    )
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
    event_staff_api_client,
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
    executed = event_staff_api_client.execute(
        UNPUBLISH_EVENT_MUTATION, variables=variables
    )
    assert_permission_denied(executed)
    # Still contact person doesn't belong to organisation
    event_staff_api_client.user.person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        UNPUBLISH_EVENT_MUTATION, variables=variables
    )
    assert_permission_denied(executed)


def test_unpublish_event(
    snapshot,
    api_client,
    event_staff_api_client,
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
    event_staff_api_client.user.person.organisations.add(organisation)
    person.organisations.add(organisation)
    executed = event_staff_api_client.execute(
        UNPUBLISH_EVENT_MUTATION, variables=variables
    )
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


@pytest.mark.parametrize("occurrences_count", [5, 400, 500])
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
    pageInfo {
      totalCount
      page
      pages
      pageSize
      hasNextPage
      hasPreviousPage
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
    upcoming_mocked_events = []

    for i in range(1, 4):
        p_event = PalvelutarjotinEventFactory(
            linked_event_id=f"kultus:{i}", organisation=organisation
        )
        mock_event_data = {**EVENT_DATA, "id": p_event.linked_event_id}
        mocked_responses.add(
            responses.GET,
            url=settings.LINKED_EVENTS_API_CONFIG["ROOT"]
            + f"event/{p_event.linked_event_id}/",
            json=mock_event_data,
        )
        mocked_responses.add(
            responses.PUT,
            url=settings.LINKED_EVENTS_API_CONFIG["ROOT"]
            + f"event/{p_event.linked_event_id}/",
            json=mock_event_data,
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

            upcoming_mocked_events.append(mock_event_data)

    if upcoming:
        ds = settings.LINKED_EVENTS_API_CONFIG["DATA_SOURCE"]
        query_string = f"ids=kultus:3,kultus:2,kultus:1&data_source={ds}"
        mocked_responses.add(
            responses.GET,
            url=f"{settings.LINKED_EVENTS_API_CONFIG['ROOT']}event/?{query_string}",
            json={
                "meta": {
                    "count": len(upcoming_mocked_events),
                    "next": None,
                    "previous": None,
                },
                "data": upcoming_mocked_events,
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


GET_NEARBY_EVENTS_QUERY = """
query NearbyEvents($placeId: ID, $distance: Float) {
  events(nearbyPlaceId: $placeId, nearbyDistance: $distance) {
    meta {
      count
      next
      previous
    }
    data {
      id
      internalId
      name {
        fi
        sv
        en
      }
    }
  }
}
"""


def test_nearby_events(
    api_client,
    organisation,
    snapshot,
    mocked_responses,
    mock_get_place_data,
    settings,
):
    """
    Searching for nearby events by place ID should put bbox parameter to the
    LinkedEvents query.
    """
    mocked_responses.add(
        responses.GET,
        url=settings.LINKED_EVENTS_API_CONFIG["ROOT"] + "event/",
        json=EVENTS_DATA,
    )
    linked_event_id = EVENTS_DATA["data"][0]["id"]
    PalvelutarjotinEventFactory(
        linked_event_id=linked_event_id, organisation=organisation
    )

    executed = api_client.execute(
        GET_NEARBY_EVENTS_QUERY,
        variables={"placeId": "tprek:15417", "distance": 3.0},
    )

    snapshot.assert_match(executed)
    assert "bbox" in mocked_responses.calls[0].request.params


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


def test_get_keyword_set(api_client, snapshot, mock_get_keyword_set_data, settings):
    for set_type in settings.KEYWORD_SET_ID_MAPPING:
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


def test_get_popular_kultus_keywords_with_timeout(api_client, monkeypatch, settings):
    """Test that popularKultusKeywords handles ConnectTimeout gracefully."""
    from requests.exceptions import ConnectTimeout

    def mock_retrieve_with_timeout(
        self, resource, id, params=None, is_event_staff=False
    ):
        # Simulate timeout for the first keyword set
        if id == settings.KEYWORD_SET_ID_MAPPING["CATEGORY"]:
            raise ConnectTimeout("Connection to api.hel.fi timed out")
        # Return valid data for other keyword sets
        return MockResponse(status_code=200, json_data=POPULAR_KEYWORD_SET_DATA)

    monkeypatch.setattr(
        LinkedEventsApiClient,
        "retrieve",
        mock_retrieve_with_timeout,
    )

    executed = api_client.execute(
        POPULAR_KULTUS_KEYWORDS_QUERY,
        variables={"amount": None, "showAllKeywords": True},
    )

    # Should not error out, should return partial results
    assert "errors" not in executed
    assert executed["data"]["popularKultusKeywords"] is not None
    # Should still have keywords from the other two sets
    assert executed["data"]["popularKultusKeywords"]["meta"]["count"] >= 0


def test_get_popular_kultus_keywords_continues_after_timeout(
    api_client, monkeypatch, settings
):
    """Test that resolver continues processing after one keyword set times out."""
    from requests.exceptions import ConnectTimeout

    call_count = {"count": 0}
    set_ids_called = []

    def mock_retrieve_with_partial_timeout(
        self, resource, id, params=None, is_event_staff=False
    ):
        call_count["count"] += 1
        set_ids_called.append(id)
        # Timeout on ADDITIONAL_CRITERIA (middle set)
        if id == settings.KEYWORD_SET_ID_MAPPING["ADDITIONAL_CRITERIA"]:
            raise ConnectTimeout("Connection timeout")
        return MockResponse(status_code=200, json_data=POPULAR_KEYWORD_SET_DATA)

    monkeypatch.setattr(
        LinkedEventsApiClient,
        "retrieve",
        mock_retrieve_with_partial_timeout,
    )

    executed = api_client.execute(
        POPULAR_KULTUS_KEYWORDS_QUERY,
        variables={"amount": None, "showAllKeywords": True},
    )

    # All 3 keyword sets should have been attempted
    assert call_count["count"] == 3
    assert len(set_ids_called) == 3
    # Should not error
    assert "errors" not in executed
    # Should return results from the 2 successful requests
    assert executed["data"]["popularKultusKeywords"]["meta"]["count"] > 0


def test_get_popular_kultus_keywords_partial_results(api_client, monkeypatch, settings):
    """Test partial results when some API requests fail."""
    from requests.exceptions import Timeout

    def mock_retrieve_with_mixed_results(
        self, resource, id, params=None, is_event_staff=False
    ):
        # Fail TARGET_GROUP request
        if id == settings.KEYWORD_SET_ID_MAPPING["TARGET_GROUP"]:
            raise Timeout("Request timeout")
        # Return data with different keywords for other sets
        keyword_data = {
            **POPULAR_KEYWORD_SET_DATA,
            "keywords": [
                {
                    **POPULAR_KEYWORD_SET_DATA["keywords"][0],
                    "id": f"keyword:{id}",
                }
            ],
        }
        return MockResponse(status_code=200, json_data=keyword_data)

    monkeypatch.setattr(
        LinkedEventsApiClient,
        "retrieve",
        mock_retrieve_with_mixed_results,
    )

    executed = api_client.execute(
        POPULAR_KULTUS_KEYWORDS_QUERY,
        variables={"amount": None, "showAllKeywords": True},
    )

    # Should return partial results from successful requests
    assert "errors" not in executed
    assert executed["data"]["popularKultusKeywords"] is not None
    # Should have keywords from 2 out of 3 sets
    assert executed["data"]["popularKultusKeywords"]["meta"]["count"] == 2


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


HAS_SPACE_LEFT_QUERY = """
  query UpcomingEvents {
    upcomingEvents {
      data {
        id
        pEvent {
          linkedEventId
          hasSpaceForEnrolments
        }
      }
    }
  }
"""


def test_has_space_for_enrolments(
    api_client, mock_get_event_data, mock_get_events_data
):
    """
    Test PalvelutarjotinEvent resolve_space_left_for_enrolments when internal enrolments
    are enabled. Also test that the `seat_type` should not matter.
    """

    def _get_first(executed):
        return executed["data"]["upcomingEvents"]["data"][0]["pEvent"]

    p_event = PalvelutarjotinEventFactory(linked_event_id=EVENTS_DATA["data"][0]["id"])
    # Occurrence in past should not be picked
    OccurrenceFactory(
        p_event=p_event,
        start_time=timezone.now() - timedelta(days=1),
        cancelled=False,
        amount_of_seats=2,
    )
    # test with seat_type set to OCCURRENCE_SEAT_TYPE_CHILDREN_COUNT
    occurrence1 = OccurrenceFactory(
        p_event=p_event,
        start_time=timezone.now() + timedelta(days=1),
        seat_type=Occurrence.OCCURRENCE_SEAT_TYPE_CHILDREN_COUNT,
        cancelled=False,
        amount_of_seats=2,
    )
    # cancelled, so won't be picked
    OccurrenceFactory(
        p_event=p_event,
        start_time=timezone.now() + timedelta(days=2),
        cancelled=True,
        amount_of_seats=2,
    )

    # when no enrolments are created and occurrence1 has 2 spaces left
    executed = api_client.execute(HAS_SPACE_LEFT_QUERY)
    # then there should be space for enrolments
    assert _get_first(executed)["linkedEventId"] == p_event.linked_event_id
    assert _get_first(executed)["hasSpaceForEnrolments"] is True

    # when enrolments are added and all space is filled
    EnrolmentFactory.create_batch(2, occurrence=occurrence1)
    executed = api_client.execute(HAS_SPACE_LEFT_QUERY)
    # then there should be no space left for enrolments
    assert _get_first(executed)["hasSpaceForEnrolments"] is False

    # test with seat_type set to OCCURRENCE_SEAT_TYPE_ENROLMENT_COUNT
    occurrence2 = OccurrenceFactory(
        p_event=p_event,
        start_time=timezone.now() + timedelta(days=3),
        seat_type=Occurrence.OCCURRENCE_SEAT_TYPE_ENROLMENT_COUNT,
        cancelled=False,
        amount_of_seats=2,
    )

    # when there is another occurrence with some space left
    executed = api_client.execute(HAS_SPACE_LEFT_QUERY)
    # then there should be space for enrolments
    assert _get_first(executed)["hasSpaceForEnrolments"] is True

    # when enrolments are added and all space is filled
    EnrolmentFactory.create_batch(2, occurrence=occurrence2)
    executed = api_client.execute(HAS_SPACE_LEFT_QUERY)
    # then there should be no space left for enrolments
    assert _get_first(executed)["hasSpaceForEnrolments"] is False


def test_has_space_for_external_enrolments(
    api_client, mock_get_event_data, mock_get_events_data
):
    """
    Test PalvelutarjotinEvent resolve_space_left_for_enrolments when external enrolments
    are enabled.
    """

    def _get_first(executed):
        return executed["data"]["upcomingEvents"]["data"][0]["pEvent"]

    # when event has external enrolments enabled
    p_event = PalvelutarjotinEventFactory(
        linked_event_id=EVENTS_DATA["data"][0]["id"],
        external_enrolment_url="https://external-enrolment-url.com",
    )
    OccurrenceFactory(
        p_event=p_event,
        start_time=timezone.now() + timedelta(days=1),
        cancelled=False,
        amount_of_seats=2,
    )

    # ...and no enrolments are created and occurrence has many spaces left
    executed = api_client.execute(HAS_SPACE_LEFT_QUERY)
    # then `None`` should be given,
    # because status cannot be resolved for external events.
    assert _get_first(executed)["linkedEventId"] == p_event.linked_event_id
    assert _get_first(executed)["hasSpaceForEnrolments"] is None


def test_has_space_for_no_enrolments_system(
    api_client, mock_get_event_data, mock_get_events_data
):
    """
    Test PalvelutarjotinEvent resolve_space_left_for_enrolments when no enrolments
    are enabled.
    """

    def _get_first(executed):
        return executed["data"]["upcomingEvents"]["data"][0]["pEvent"]

    # when event has no enrolment system enabled
    p_event = PalvelutarjotinEventFactory(
        linked_event_id=EVENTS_DATA["data"][0]["id"],
        external_enrolment_url=None,
        enrolment_start=None,
    )
    OccurrenceFactory(
        p_event=p_event,
        start_time=timezone.now() + timedelta(days=1),
        cancelled=False,
        amount_of_seats=2,
    )
    executed = api_client.execute(HAS_SPACE_LEFT_QUERY)
    # then `None`` should be given,
    # because status cannot be resolved when enrolments are not counted.
    assert _get_first(executed)["linkedEventId"] == p_event.linked_event_id
    assert _get_first(executed)["hasSpaceForEnrolments"] is None
