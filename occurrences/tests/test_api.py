import pytest
from copy import deepcopy
from datetime import datetime, timedelta
from django.core import mail
from django.utils import timezone
from graphql_relay import to_global_id
from unittest.mock import patch

from common.tests.utils import (
    assert_mails_match_snapshot,
    assert_match_error_code,
    assert_permission_denied,
)
from graphene_linked_events.tests.mock_data import EVENT_DATA, PLACE_DATA
from occurrences.consts import NOTIFICATION_TYPE_EMAIL
from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from occurrences.models import (
    Enrolment,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    StudyLevel,
    VenueCustomData,
)
from occurrences.schema import StudyGroupNode
from organisations.factories import PersonFactory
from palvelutarjotin.consts import (
    API_USAGE_ERROR,
    CAPTCHA_VALIDATION_FAILED_ERROR,
    DATA_VALIDATION_ERROR,
    ENROL_CANCELLED_OCCURRENCE_ERROR,
    ENROLMENT_CLOSED_ERROR,
    ENROLMENT_NOT_STARTED_ERROR,
    INVALID_STUDY_GROUP_SIZE_ERROR,
    INVALID_STUDY_GROUP_UNIT_INFO_ERROR,
    INVALID_TOKEN_ERROR,
    MAX_NEEDED_OCCURRENCES_REACHED_ERROR,
    MISSING_MANDATORY_INFORMATION_ERROR,
    NOT_ENOUGH_CAPACITY_ERROR,
)
from verification_token.models import VerificationToken


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


LANGUAGES_QUERY = """
    query Languages{
        languages {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
"""

LANGUAGE_QUERY = """
    query Language($id: ID!){
        language(id: $id) {
            id
            name
        }
    }
"""


def test_languagess_query(snapshot, language, api_client):
    executed = api_client.execute(LANGUAGES_QUERY)
    snapshot.assert_match(executed)


def test_language_query(snapshot, language, api_client):
    executed = api_client.execute(
        LANGUAGE_QUERY,
        variables={"id": language.id},
    )
    snapshot.assert_match(executed)


STUDY_LEVELS_QUERY = """
    query StudyLevels{
        studyLevels {
            edges {
                node {
                    id
                    label
                    level
                    translations {
                        languageCode
                        label
                    }
                }
            }
        }
    }
"""

STUDY_LEVEL_QUERY = """
    query StudyLevel($id: ID!){
        studyLevel(id: $id){
            id
            label
            level
            translations {
                languageCode
                label
            }
        }
    }
"""

STUDY_GROUPS_QUERY = """
query StudyGroups{
  studyGroups{
    edges{
      node{
        unit {
            ... on ExternalPlace {
                name {
                    fi
                }
            }
            ... on Place {
                internalId
                name {
                    fi
                }
            }
        }
        person {
          name
        }
        updatedAt
        groupSize
        groupName
        amountOfAdult
        studyLevels {
            edges {
                node {
                    id
                    label
                    level
                    translations {
                        languageCode
                        label
                    }
                }
            }
        }
        extraNeeds
        occurrences {
          edges {
            node {
              placeId
            }
          }
        }
      }
    }
  }
}
"""

STUDY_GROUP_QUERY = """
query StudyGroup($id: ID!){
  studyGroup(id: $id){
    unitId
    unitName
    unit {
        ... on ExternalPlace {
            name {
                fi
            }
        }
        ... on Place {
            internalId
            name {
                fi
            }
        }
    }
    person {
      name
    }
    updatedAt
    groupSize
    groupName
    amountOfAdult
    studyLevels {
        edges {
            node {
                id
                label
                level
                translations {
                    languageCode
                    label
                }
            }
        }
    }
    extraNeeds
    occurrences {
      edges {
        node {
          placeId
        }
      }
    }
  }
}
"""

OCCURRENCES_QUERY = """
query Occurrences(
    $upcoming: Boolean,
    $enrollable: Boolean,
    $date: Date,
    $time: Time,
    $cancelled: Boolean,
    $pEvent: ID,
    $orderBy: [String]
){
  occurrences(
      upcoming: $upcoming,
      enrollable: $enrollable,
      date: $date,
      time: $time,
      cancelled: $cancelled,
      pEvent: $pEvent,
      orderBy: $orderBy
  ){
    edges{
      node{
        placeId
        amountOfSeats
        remainingSeats
        seatsTaken
        seatsApproved
        seatType
        pEvent{
            contactEmail
            contactPhoneNumber
            neededOccurrences
            enrolmentEndDays
            enrolmentStart
            externalEnrolmentUrl
            linkedEventId
            autoAcceptance
            mandatoryAdditionalInformation
        }
        startTime
        endTime
        studyGroups {
          edges {
            node {
              unitName
            }
          }
        }
        minGroupSize
        maxGroupSize
        contactPersons {
          edges {
            node {
              name
            }
          }
        }
      }
    }
  }
}
"""

OCCURRENCE_QUERY = """
query Occurrence($id: ID!){
  occurrence(id: $id){
    placeId
    pEvent{
        contactEmail
        contactPhoneNumber
        neededOccurrences
        enrolmentEndDays
        enrolmentStart
        externalEnrolmentUrl
        linkedEventId
        autoAcceptance
        mandatoryAdditionalInformation
    }
    linkedEvent{
        name {
           en
           fi
           sv
        }
    }
    startTime
    endTime
    studyGroups {
      edges {
        node {
          unitName
        }
      }
    }
    amountOfSeats
    remainingSeats
    seatsTaken
    seatsApproved
    minGroupSize
    maxGroupSize
    contactPersons {
      edges {
        node {
          name
        }
      }
    }
    languages{
        edges {
            node {
                id
                name
            }
        }
    }
  }
}
"""

ADD_OCCURRENCE_MUTATION = """
    mutation addOccurrence($input: AddOccurrenceMutationInput!){
      addOccurrence(input: $input){
        occurrence{
          minGroupSize
          maxGroupSize
          contactPersons{
            edges {
              node {
                name
              }
            }
          }
          startTime
          endTime
          pEvent{
            contactEmail
            contactPhoneNumber
            neededOccurrences
            enrolmentEndDays
            enrolmentStart
            externalEnrolmentUrl
            linkedEventId
            autoAcceptance
            mandatoryAdditionalInformation
          }
          languages{
            edges {
              node {
                id
                name
              }
            }
          }
        }
      }
    }
"""

ADD_OCCURRENCE_VARIABLES = {
    "input": {
        "placeId": "place_id",
        "minGroupSize": 10,
        "startTime": "2020-05-05T00:00:00+00",
        "endTime": "2020-05-06T00:00:00+00",
        "contactPersons": [
            {"name": "New name", "emailAddress": "newname@email.address"},
        ],
        "pEventId": "",
        "amountOfSeats": 40,
        "languages": [
            {"id": "EN"},
            {"id": "sv"},
            {"id": "AR"},
            {"id": "RU"},
            {"id": "zh_hans"},
        ],
    }
}

UPDATE_OCCURRENCE_MUTATION = """
mutation updateOccurrence($input: UpdateOccurrenceMutationInput!){
  updateOccurrence(input: $input){
    occurrence{
      minGroupSize
      maxGroupSize
      contactPersons{
        edges {
          node {
            name
          }
        }
      }
      startTime
      endTime
      pEvent{
        contactEmail
        contactPhoneNumber
        neededOccurrences
        enrolmentEndDays
        enrolmentStart
        externalEnrolmentUrl
        linkedEventId
        mandatoryAdditionalInformation
      }
      languages{
        edges {
          node {
            id
            name
          }
        }
      }
    }
  }
}
"""

UPDATE_OCCURRENCE_VARIABLES = {
    "input": {
        "placeId": "place_id",
        "minGroupSize": 10,
        "startTime": "2020-05-05T00:00:00+00",
        "endTime": "2020-05-06T00:00:00+00",
        "contactPersons": [
            {"id": "", "name": "New name", "emailAddress": "newname@email.address"},
        ],
        "pEventId": "",
        "amountOfSeats": 40,
        "languages": [{"id": "FI"}, {"id": "EN"}, {"id": "SV"}],
    }
}

DELETE_OCCURRENCE_MUTATION = """
mutation DeleteOccurrence($input: DeleteOccurrenceMutationInput!) {
  deleteOccurrence(input: $input) {
    __typename
  }
}
"""


def test_study_levels_query(snapshot, api_client):
    executed = api_client.execute(STUDY_LEVELS_QUERY)
    snapshot.assert_match(executed)


def test_study_level_query(snapshot, api_client):
    study_level = StudyLevel.objects.first()
    executed = api_client.execute(
        STUDY_LEVEL_QUERY,
        variables={"id": study_level.id},
    )
    snapshot.assert_match(executed)


def test_study_groups_query(snapshot, study_group, api_client):
    executed = api_client.execute(STUDY_GROUPS_QUERY)
    snapshot.assert_match(executed)


def test_study_group_query(snapshot, study_group, api_client):
    executed = api_client.execute(
        STUDY_GROUP_QUERY,
        variables={"id": to_global_id("StudyGroupNode", study_group.id)},
    )
    snapshot.assert_match(executed)


def test_study_group_query_without_unit(snapshot, api_client):
    study_group = StudyGroupFactory(unit_name="", unit_id="")
    executed = api_client.execute(
        STUDY_GROUP_QUERY,
        variables={"id": to_global_id("StudyGroupNode", study_group.id)},
    )
    assert executed["data"]["studyGroup"]["unit"] is None
    snapshot.assert_match(executed)


def test_studygroup_resolve_unit_with_id(mock_get_place_data):
    study_group = StudyGroupFactory(unit_id=PLACE_DATA["id"], unit_name="testname")
    unit = StudyGroupNode.resolve_unit(study_group, None)
    assert unit.id == PLACE_DATA["id"]
    assert unit.name.fi == PLACE_DATA["name"]["fi"]
    assert unit.name.sv == PLACE_DATA["name"]["sv"]
    assert unit.name.en == PLACE_DATA["name"]["en"]


def test_studygroup_resolve_unit_without_id(mock_get_place_data):
    study_group = StudyGroupFactory(unit_id=None, unit_name="testname")
    unit = StudyGroupNode.resolve_unit(study_group, None)
    assert unit.name["fi"] == unit.name["sv"] == unit.name["en"] == "testname"


def test_occurrences_query(
    snapshot, mock_update_event_data, mock_get_event_data, occurrence, api_client
):
    executed = api_client.execute(OCCURRENCES_QUERY)
    snapshot.assert_match(executed)


def test_occurrence_query(
    snapshot, mock_update_event_data, mock_get_event_data, occurrence, api_client
):
    executed = api_client.execute(
        OCCURRENCE_QUERY,
        variables={"id": to_global_id("OccurrenceNode", occurrence.id)},
    )
    snapshot.assert_match(executed)


def test_add_occurrence_unauthorized(
    api_client, user_api_client, organisation, p_event, staff_api_client
):
    executed = api_client.execute(
        ADD_OCCURRENCE_MUTATION, variables=ADD_OCCURRENCE_VARIABLES
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        ADD_OCCURRENCE_MUTATION, variables=ADD_OCCURRENCE_VARIABLES
    )
    assert_permission_denied(executed)

    variables = deepcopy(ADD_OCCURRENCE_VARIABLES)
    variables["input"]["pEventId"] = to_global_id(
        "PalvelutarjotinEventNode", p_event.id
    )
    executed = staff_api_client.execute(ADD_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)


def test_add_occurrence_to_published_event(
    snapshot,
    staff_api_client,
    organisation,
    person,
    mock_get_event_data,
    mock_update_event_data,
):
    variables = deepcopy(ADD_OCCURRENCE_VARIABLES)
    p_event = PalvelutarjotinEventFactory(organisation=organisation)
    variables["input"]["pEventId"] = to_global_id(
        "PalvelutarjotinEventNode", p_event.id
    )
    # Add one more pre-made contact person to the variable
    variables["input"]["contactPersons"].append(
        {
            "id": to_global_id("PersonNode", person.id),
            "emailAddress": person.email_address,
            "name": person.name,
        }
    )
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(ADD_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)
    # test validation
    variables["input"]["endTime"] = variables["input"]["startTime"]
    executed = staff_api_client.execute(ADD_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, DATA_VALIDATION_ERROR)


def test_add_occurrence_to_unpublished_event(
    snapshot,
    staff_api_client,
    organisation,
    person,
    mock_get_draft_event_data,
    mock_update_event_data,
):
    variables = deepcopy(ADD_OCCURRENCE_VARIABLES)
    p_event = PalvelutarjotinEventFactory(organisation=organisation)
    variables["input"]["pEventId"] = to_global_id(
        "PalvelutarjotinEventNode", p_event.id
    )
    # Add one more pre-made contact person to the variable
    variables["input"]["contactPersons"].append(
        {
            "id": to_global_id("PersonNode", person.id),
            "emailAddress": person.email_address,
            "name": person.name,
        }
    )
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(ADD_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)
    # test validation
    variables["input"]["endTime"] = variables["input"]["startTime"]
    executed = staff_api_client.execute(ADD_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, DATA_VALIDATION_ERROR)


def test_add_occurrence_to_date_when_enrolling_has_not_started(
    staff_api_client,
    organisation,
    person,
    mock_get_draft_event_data,
    mock_update_event_data,
):
    variables = deepcopy(ADD_OCCURRENCE_VARIABLES)
    p_event = PalvelutarjotinEventFactory(
        organisation=organisation, enrolment_end_days=2
    )
    variables["input"]["pEventId"] = to_global_id(
        "PalvelutarjotinEventNode", p_event.id
    )
    # Add one more pre-made contact person to the variable
    variables["input"]["contactPersons"].append(
        {
            "id": to_global_id("PersonNode", person.id),
            "emailAddress": person.email_address,
            "name": person.name,
        }
    )
    staff_api_client.user.person.organisations.add(organisation)
    variables["input"]["startTime"] = p_event.enrolment_start
    variables["input"]["endTime"] = p_event.enrolment_start + timedelta(days=4)

    executed = staff_api_client.execute(ADD_OCCURRENCE_MUTATION, variables=variables)
    assert "errors" in executed
    assert_match_error_code(executed, DATA_VALIDATION_ERROR)

    variables["input"]["startTime"] = p_event.enrolment_start + timedelta(days=3)
    variables["input"]["endTime"] = p_event.enrolment_start + timedelta(days=4)

    executed = staff_api_client.execute(ADD_OCCURRENCE_MUTATION, variables=variables)
    assert "errors" not in executed


def test_update_occurrence_unauthorized(
    api_client,
    user_api_client,
    mock_get_event_data,
    mock_update_event_data,
    occurrence,
    staff_api_client,
):
    variables = deepcopy(UPDATE_OCCURRENCE_VARIABLES)
    variables["input"]["id"] = to_global_id("OccurrenceNode", occurrence.id)
    executed = api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = user_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = staff_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)


@pytest.mark.parametrize("group_size,amount_of_adult", [(1, 0), (0, 1), (2, 3)])
def test_update_occurrence_of_published_event_with_enrolments(
    group_size,
    amount_of_adult,
    staff_api_client,
    organisation,
    person,
    mock_get_event_data,
):
    variables = deepcopy(UPDATE_OCCURRENCE_VARIABLES)
    occurrence = OccurrenceFactory(
        contact_persons=[person],
        p_event__organisation=organisation,
        amount_of_seats=100,
        min_group_size=1,
        max_group_size=10,
    )

    # enrolment for occurrence
    study_group_20 = StudyGroupFactory(
        group_size=group_size, amount_of_adult=amount_of_adult
    )
    EnrolmentFactory(occurrence=occurrence, study_group=study_group_20)

    p_event = PalvelutarjotinEventFactory(
        linked_event_id=EVENT_DATA["id"], organisation=organisation
    )
    variables["input"]["id"] = to_global_id("OccurrenceNode", occurrence.id)
    # Change p_event
    variables["input"]["pEventId"] = to_global_id(
        "PalvelutarjotinEventNode", p_event.id
    )
    # Change contact person, remove old one
    new_person = PersonFactory()
    variables["input"]["contactPersons"] = [
        {
            "id": to_global_id("PersonNode", new_person.id),
            "emailAddress": new_person.email_address,
            "name": new_person.name,
        },
    ]
    staff_api_client.user.person.organisations.add(organisation)
    assert occurrence.seats_taken > 0
    executed = staff_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, API_USAGE_ERROR)


def test_update_occurrence_of_published_event_without_enrolments(
    snapshot,
    staff_api_client,
    organisation,
    person,
    mock_get_event_data,
    mock_update_event_data,
):
    variables = deepcopy(UPDATE_OCCURRENCE_VARIABLES)
    occurrence = OccurrenceFactory(
        contact_persons=[person],
        p_event__organisation=organisation,
        amount_of_seats=100,
        min_group_size=1,
        max_group_size=10,
    )

    p_event = PalvelutarjotinEventFactory(
        linked_event_id=EVENT_DATA["id"], organisation=organisation
    )
    variables["input"]["id"] = to_global_id("OccurrenceNode", occurrence.id)
    # Change p_event
    variables["input"]["pEventId"] = to_global_id(
        "PalvelutarjotinEventNode", p_event.id
    )
    # Change contact person, remove old one
    new_person = PersonFactory()
    variables["input"]["contactPersons"] = [
        {
            "id": to_global_id("PersonNode", new_person.id),
            "emailAddress": new_person.email_address,
            "name": new_person.name,
        },
    ]
    assert occurrence.seats_taken == 0
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)
    # test validation
    variables["input"]["endTime"] = variables["input"].pop("startTime")
    executed = staff_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, DATA_VALIDATION_ERROR)


def test_update_unpublished_occurrence(
    snapshot,
    staff_api_client,
    organisation,
    person,
    mock_get_draft_event_data,
    mock_update_event_data,
):
    variables = deepcopy(UPDATE_OCCURRENCE_VARIABLES)
    occurrence = OccurrenceFactory(
        contact_persons=[person],
        p_event__organisation=organisation,
        start_time=datetime(2020, 1, 1, 12, 0, tzinfo=timezone.utc),
    )
    p_event = PalvelutarjotinEventFactory(organisation=organisation)
    variables["input"]["id"] = to_global_id("OccurrenceNode", occurrence.id)
    # Change p_event
    variables["input"]["pEventId"] = to_global_id(
        "PalvelutarjotinEventNode", p_event.id
    )
    # Change contact person, remove old one
    new_person = PersonFactory()
    variables["input"]["contactPersons"] = [
        {
            "id": to_global_id("PersonNode", new_person.id),
            "emailAddress": new_person.email_address,
            "name": new_person.name,
        },
    ]
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)
    # test validation
    variables["input"]["endTime"] = variables["input"].pop("startTime")
    executed = staff_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, DATA_VALIDATION_ERROR)


def test_delete_occurrence_unauthorized(
    api_client,
    user_api_client,
    staff_api_client,
    mock_update_event_data,
    mock_get_event_data,
    occurrence,
):
    # TODO: paremeterize
    variables = {"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}}
    executed = api_client.execute(DELETE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = user_api_client.execute(DELETE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = staff_api_client.execute(DELETE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)
    assert Occurrence.objects.count() == 1


def test_delete_cancelled_occurrence(
    snapshot, staff_api_client, mock_get_event_data, mock_update_event_data, occurrence
):
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(
        DELETE_OCCURRENCE_MUTATION,
        variables={"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}},
    )
    assert_match_error_code(executed, API_USAGE_ERROR)
    occurrence.cancelled = True
    occurrence.save()
    executed = staff_api_client.execute(
        DELETE_OCCURRENCE_MUTATION,
        variables={"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}},
    )
    snapshot.assert_match(executed)


def test_delete_unpublished_occurrence(
    snapshot,
    staff_api_client,
    mock_get_draft_event_data,
    mock_update_event_data,
    occurrence,
):
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(
        DELETE_OCCURRENCE_MUTATION,
        variables={"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}},
    )
    snapshot.assert_match(executed)
    assert Occurrence.objects.count() == 0


VENUES_QUERY = """
query Venues {
  venues {
    edges {
      node {
        id
        description
        translations {
          description
        }
        hasClothingStorage
        hasSnackEatingPlace
        outdoorActivity
        hasToiletNearby
        hasAreaForGroupWork
        hasIndoorPlayingArea
        hasOutdoorPlayingArea
      }
    }
  }
}
"""

VENUE_QUERY = """
query venue($id:ID!){
  venue(id: $id){
    id
    description,
    translations{
      description
    }
    hasClothingStorage
    hasSnackEatingPlace
    outdoorActivity
    hasToiletNearby
    hasAreaForGroupWork
    hasIndoorPlayingArea
    hasOutdoorPlayingArea
  }
}
"""

ADD_VENUE_MUTATION = """
mutation AddVenue($input: AddVenueMutationInput!) {
  addVenue(input: $input) {
    venue {
        id
        description
        translations {
          description
        }
        hasClothingStorage
        hasSnackEatingPlace
        outdoorActivity
        hasToiletNearby
        hasAreaForGroupWork
        hasIndoorPlayingArea
        hasOutdoorPlayingArea
    }
  }
}
"""

ADD_VENUE_VARIABLES = {
    "input": {
        "id": "place_id",
        "translations": [
            {"description": "Venue description in FI", "languageCode": "FI"},
            {"description": "Venue description in EN", "languageCode": "EN"},
        ],
        "hasClothingStorage": True,
        "hasSnackEatingPlace": True,
        "outdoorActivity": True,
        "hasToiletNearby": True,
        "hasAreaForGroupWork": True,
        "hasIndoorPlayingArea": True,
        "hasOutdoorPlayingArea": True,
    }
}

UPDATE_VENUE_MUTATION = """
mutation updateVenue($input: UpdateVenueMutationInput!) {
  updateVenue(input: $input) {
    venue {
        id
        description
        translations {
          description
        }
        hasClothingStorage
        hasSnackEatingPlace
        outdoorActivity
        hasToiletNearby
        hasAreaForGroupWork
        hasIndoorPlayingArea
        hasOutdoorPlayingArea
    }
  }
}
"""

UPDATE_VENUE_VARIABLES = {
    "input": {
        "id": "",
        "translations": [
            {"description": "Venue description", "languageCode": "FI"},
            {"description": "Venue description in EN", "languageCode": "EN"},
        ],
        "hasClothingStorage": True,
        "hasSnackEatingPlace": True,
        "outdoorActivity": True,
        "hasToiletNearby": True,
        "hasAreaForGroupWork": True,
        "hasIndoorPlayingArea": True,
        "hasOutdoorPlayingArea": True,
    }
}

DELETE_VENUE_MUTATION = """
mutation DeleteVenue($input: DeleteVenueMutationInput!) {
  deleteVenue(input: $input) {
    __typename
  }
}
"""


def test_venues_query(snapshot, user_api_client, venue):
    executed = user_api_client.execute(VENUES_QUERY)

    snapshot.assert_match(executed)


def test_venue_query(snapshot, user_api_client, venue):
    variables = {"id": venue.place_id}
    executed = user_api_client.execute(VENUE_QUERY, variables=variables)

    snapshot.assert_match(executed)


def test_add_venue_permission_denied(api_client, user_api_client):
    executed = api_client.execute(ADD_VENUE_MUTATION, variables=ADD_VENUE_VARIABLES)
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        ADD_VENUE_MUTATION, variables=ADD_VENUE_VARIABLES
    )
    assert_permission_denied(executed)


def test_add_venue_staff_user(snapshot, staff_api_client):
    venue_variables = deepcopy(ADD_VENUE_VARIABLES)
    executed = staff_api_client.execute(ADD_VENUE_MUTATION, variables=venue_variables)
    snapshot.assert_match(executed)


def test_update_venue_permission_denied(api_client, user_api_client):
    executed = api_client.execute(
        UPDATE_VENUE_MUTATION, variables=UPDATE_VENUE_VARIABLES
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        UPDATE_VENUE_MUTATION, variables=UPDATE_VENUE_VARIABLES
    )
    assert_permission_denied(executed)


def test_update_venue_staff_user(snapshot, staff_api_client, venue):
    venue_variables = deepcopy(UPDATE_VENUE_VARIABLES)
    venue_variables["input"]["id"] = venue.place_id
    executed = staff_api_client.execute(
        UPDATE_VENUE_MUTATION, variables=venue_variables
    )
    snapshot.assert_match(executed)


def test_delete_venue_permission_denied(api_client, user_api_client):
    executed = api_client.execute(
        DELETE_VENUE_MUTATION, variables={"input": {"id": ""}}
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        DELETE_VENUE_MUTATION, variables={"input": {"id": ""}}
    )
    assert_permission_denied(executed)


def test_delete_venue_staff_user(staff_api_client, venue):
    staff_api_client.execute(
        DELETE_VENUE_MUTATION,
        variables={"input": {"id": venue.place_id}},
    )
    assert VenueCustomData.objects.count() == 0


ADD_STUDY_GROUP_MUTATION = """
mutation addStudyGroup($input: AddStudyGroupMutationInput!){
  addStudyGroup(input:$input) {
    studyGroup{
      unitId
      unitName
      unit {
        ... on ExternalPlace {
            name {
                fi
            }
        }
        ... on Place {
            internalId
            name {
                fi
            }
        }
      }
      person{
        name
        emailAddress
        phoneNumber
        language
      }
      groupSize
      groupName
      amountOfAdult
      studyLevels {
        edges {
            node {
                id
                label
                level
                translations {
                    languageCode
                    label
                }
            }
        }
      }
      extraNeeds
    }
  }
}
"""

ADD_STUDY_GROUP_VARIABLES = {
    "input": {
        "person": {
            "name": "Name",
            "emailAddress": "email@address.com",
            "phoneNumber": "123123",
            "language": "SV",
        },
        "unitId": EVENT_DATA["id"],
        "unitName": "Sample study group name",
        "groupSize": 20,
        "amountOfAdult": 1,
        "studyLevels": ["GRADE_1"],
        "groupName": "Sample group name",
        "extraNeeds": "Extra needs",
    }
}


def test_add_study_group(
    snapshot,
    api_client,
    mock_update_event_data,
    mock_get_event_data,
    occurrence,
    person,
):
    variables = deepcopy(ADD_STUDY_GROUP_VARIABLES)
    executed = api_client.execute(ADD_STUDY_GROUP_MUTATION, variables=variables)
    snapshot.assert_match(executed)

    # Add study group with pre-defined person
    variables["input"]["person"]["id"] = to_global_id("PersonNode", person.id)
    executed = api_client.execute(ADD_STUDY_GROUP_MUTATION, variables=variables)
    snapshot.assert_match(executed)


def test_add_study_group_without_unit_info_raises_error(
    api_client,
    mock_update_event_data,
    mock_get_event_data,
    occurrence,
    person,
):
    variables = deepcopy(ADD_STUDY_GROUP_VARIABLES)
    variables["input"]["unitName"] = None
    variables["input"]["unitId"] = None
    executed = api_client.execute(ADD_STUDY_GROUP_MUTATION, variables=variables)
    assert_match_error_code(executed, INVALID_STUDY_GROUP_UNIT_INFO_ERROR)


UPDATE_STUDY_GROUP_MUTATION = """
mutation updateStudyGroup($input: UpdateStudyGroupMutationInput!){
  updateStudyGroup(input:$input) {
    studyGroup{
      unitId
      unitName
      unit {
        ... on ExternalPlace {
            name {
                fi
            }
        }
        ... on Place {
            internalId
            name {
                fi
            }
        }
      }
      person{
        name
        emailAddress
        phoneNumber
        language
      }
      groupSize
      groupName
      amountOfAdult
      studyLevels {
        edges {
            node {
                id
                label
                level
                translations {
                    languageCode
                    label
                }
            }
        }
      }
      extraNeeds
    }
  }
}
"""

UPDATE_STUDY_GROUP_VARIABLES = {
    "input": {
        "id": "",
        "person": {
            "name": "Name",
            "emailAddress": "email@address.com",
            "phoneNumber": "123123",
        },
        "unitId": EVENT_DATA["id"],
        "unitName": "Sample study group name",
        "groupSize": 20,
        "amountOfAdult": 2,
        "studyLevels": ["GRADE_2"],
        "groupName": "Sample group name",
        "extraNeeds": "Extra needs",
    }
}


def test_update_study_group_unauthenticated(api_client, user_api_client):
    variables = deepcopy(UPDATE_STUDY_GROUP_VARIABLES)
    executed = api_client.execute(UPDATE_STUDY_GROUP_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = user_api_client.execute(UPDATE_STUDY_GROUP_MUTATION, variables=variables)
    assert_permission_denied(executed)


def test_update_study_group_staff_user(
    snapshot, staff_api_client, study_group, person, mock_get_place_data
):
    variables = deepcopy(UPDATE_STUDY_GROUP_VARIABLES)
    variables["input"]["id"] = to_global_id("StudyGroupNode", study_group.id)
    executed = staff_api_client.execute(
        UPDATE_STUDY_GROUP_MUTATION, variables=variables
    )
    snapshot.assert_match(executed)

    variables["input"]["person"]["id"] = to_global_id("PersonNode", person.id)
    executed = staff_api_client.execute(
        UPDATE_STUDY_GROUP_MUTATION, variables=variables
    )
    snapshot.assert_match(executed)


def test_update_study_group_without_unit_info_raises_error(
    staff_api_client, study_group, person, mock_get_place_data
):
    variables = deepcopy(UPDATE_STUDY_GROUP_VARIABLES)
    variables["input"]["id"] = to_global_id("StudyGroupNode", study_group.id)
    variables["input"]["person"]["id"] = to_global_id("PersonNode", person.id)
    variables["input"]["unitName"] = None
    variables["input"]["unitId"] = None
    executed = staff_api_client.execute(
        UPDATE_STUDY_GROUP_MUTATION, variables=variables
    )
    assert_match_error_code(executed, INVALID_STUDY_GROUP_UNIT_INFO_ERROR)


DELETE_STUDY_GROUP_MUTATION = """
mutation deleteStudyGroup($input: DeleteStudyGroupMutationInput!){
  deleteStudyGroup(input: $input){
    __typename
  }
}
"""


def test_delete_study_group_permission_denied(api_client, user_api_client):
    executed = api_client.execute(
        DELETE_STUDY_GROUP_MUTATION, variables={"input": {"id": ""}}
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        DELETE_STUDY_GROUP_MUTATION, variables={"input": {"id": ""}}
    )
    assert_permission_denied(executed)


def test_delete_study_group_staff_user(staff_api_client, study_group):
    staff_api_client.execute(
        DELETE_STUDY_GROUP_MUTATION,
        variables={"input": {"id": to_global_id("StudyGroupNode", study_group.id)}},
    )
    assert StudyGroup.objects.count() == 0


ENROL_OCCURRENCE_MUTATION = """
mutation enrolOccurrence($input: EnrolOccurrenceMutationInput!){
  enrolOccurrence(input: $input){
    enrolments{
      studyGroup{
        unitName
      }
      occurrence{
        startTime
        seatsTaken
        seatsApproved
        remainingSeats
        amountOfSeats
        seatType
      }
      notificationType
      status
    }
  }
}
"""


def test_enrol_not_started_occurrence(
    api_client, mock_update_event_data, mock_get_event_data
):
    # Current date froze on 2020-01-04:
    study_group = StudyGroupFactory(group_size=10)
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    not_started_occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 8, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=5,
        max_group_size=15,
        amount_of_seats=100,
    )

    variables = {
        "input": {
            "occurrenceIds": [
                to_global_id("OccurrenceNode", not_started_occurrence.id),
            ],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group.person.id),
                    "name": study_group.person.name,
                    "emailAddress": study_group.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group.group_size,
                "groupName": study_group.group_name,
                "studyLevels": [sl.id.upper() for sl in StudyLevel.objects.all()],
                "amountOfAdult": study_group.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, ENROLMENT_NOT_STARTED_ERROR)


def test_enrol_past_occurrence(
    api_client, mock_update_event_data, mock_get_event_data, occurrence
):
    # Current date froze on 2020-01-04:
    study_group = StudyGroupFactory(group_size=10)
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    past_occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=5,
        max_group_size=15,
        amount_of_seats=100,
    )

    variables = {
        "input": {
            "occurrenceIds": [to_global_id("OccurrenceNode", past_occurrence.id)],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group.person.id),
                    "name": study_group.person.name,
                    "emailAddress": study_group.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group.group_size,
                "groupName": study_group.group_name,
                "studyLevels": [sl.id.upper() for sl in StudyLevel.objects.all()],
                "amountOfAdult": study_group.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, ENROLMENT_CLOSED_ERROR)


def test_enrol_invalid_group_size(
    api_client, mock_update_event_data, mock_get_event_data, occurrence
):
    study_group_21 = StudyGroupFactory(group_size=21)
    study_group_9 = StudyGroupFactory(group_size=9)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=16,
        max_group_size=20,
    )

    variables = {
        "input": {
            "occurrenceIds": [to_global_id("OccurrenceNode", occurrence.id)],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_21.person.id),
                    "name": study_group_21.person.name,
                    "emailAddress": study_group_21.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group_21.group_size,
                "groupName": study_group_21.group_name,
                "studyLevels": [sl.upper() for sl in study_group_21.study_levels.all()],
                "amountOfAdult": study_group_21.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, INVALID_STUDY_GROUP_SIZE_ERROR)

    variables = {
        "input": {
            "occurrenceIds": [to_global_id("OccurrenceNode", occurrence.id)],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_9.person.id),
                    "name": study_group_9.person.name,
                    "emailAddress": study_group_9.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group_9.group_size,
                "groupName": study_group_9.group_name,
                "studyLevels": [sl.upper() for sl in study_group_9.study_levels.all()],
                "amountOfAdult": study_group_9.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, INVALID_STUDY_GROUP_SIZE_ERROR)


def test_enrol_without_participants(
    api_client, mock_update_event_data, mock_get_event_data
):
    empty_study_group = StudyGroupFactory(group_size=0, amount_of_adult=0)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
    )

    variables = {
        "input": {
            "occurrenceIds": [to_global_id("OccurrenceNode", occurrence.id)],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", empty_study_group.person.id),
                    "name": empty_study_group.person.name,
                    "emailAddress": empty_study_group.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": empty_study_group.group_size,
                "groupName": empty_study_group.group_name,
                "studyLevels": [
                    sl.upper() for sl in empty_study_group.study_levels.all()
                ],
                "amountOfAdult": empty_study_group.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, INVALID_STUDY_GROUP_SIZE_ERROR)


# The auto_acceptance calls Enrolment.approve,
# so it needs to be tested with both the boolean values.
@pytest.mark.parametrize("auto_acceptance", [True, False])
@pytest.mark.parametrize("is_multi_enrolment", [True, False])
@patch("occurrences.services.notification_service.send_sms")
def test_enrol_full_people_count_seat_type_occurrence(
    mock_send_sms,
    auto_acceptance,
    is_multi_enrolment,
    api_client,
    mock_update_event_data,
    mock_get_event_data,
    occurrence,
    notification_template_enrolment_approved_en,
    notification_template_enrolment_approved_fi,
    notification_sms_template_enrolment_approved_en,
    notification_sms_template_enrolment_approved_fi,
):
    study_group_15 = StudyGroupFactory(group_size=15)
    study_group_20 = StudyGroupFactory(group_size=20)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        auto_acceptance=auto_acceptance,
        needed_occurrences=2,
    )

    # Invalid occurrence which does not support such a large study group
    invalid_occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=34,
    )

    # if is_multi_enrolment is True, multiple occurrences are needed
    if is_multi_enrolment:
        valid_occurrence = OccurrenceFactory(
            start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
            p_event=p_event_1,
            min_group_size=10,
            max_group_size=20,
            amount_of_seats=100,  # enough for 2 enrolments
        )
        occurrence_ids = [
            to_global_id("OccurrenceNode", valid_occurrence.id),
            to_global_id("OccurrenceNode", invalid_occurrence.id),
        ]
    else:
        occurrence_ids = [
            to_global_id("OccurrenceNode", invalid_occurrence.id),
        ]
    # After 20 people there are 14 seats left
    EnrolmentFactory(occurrence=invalid_occurrence, study_group=study_group_20)

    # A group of 15 woul make the event over booked by 1!
    variables = {
        "input": {
            "occurrenceIds": occurrence_ids,
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_15.person.id),
                    "name": study_group_15.person.name,
                    "emailAddress": study_group_15.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group_15.group_size,
                "groupName": study_group_15.group_name,
                "studyLevels": [sl.upper() for sl in study_group_15.study_levels.all()],
                "amountOfAdult": study_group_15.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, NOT_ENOUGH_CAPACITY_ERROR)
    assert mock_send_sms.call_count == 0
    assert len(mail.outbox) == 0


# The auto_acceptance calls Enrolment.approve,
# so it needs to be tested with both the boolean values.
@pytest.mark.parametrize("auto_acceptance", [True, False])
def test_enrol_full_enrolment_count_seat_type_occurrence(
    auto_acceptance, api_client, mock_update_event_data, mock_get_event_data, occurrence
):
    study_group_15 = StudyGroupFactory(group_size=15)
    study_group_100 = StudyGroupFactory(group_size=100)
    study_group_20 = StudyGroupFactory(group_size=20)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        auto_acceptance=auto_acceptance,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=101,
        amount_of_seats=2,
        seat_type=Occurrence.OCCURRENCE_SEAT_TYPE_ENROLMENT_COUNT,
    )

    # 2 enrolments makes the occurrence full!
    EnrolmentFactory(occurrence=occurrence, study_group=study_group_20)
    EnrolmentFactory(occurrence=occurrence, study_group=study_group_100)

    # 3rd enrolment will make the occurrence over booked
    variables = {
        "input": {
            "occurrenceIds": [to_global_id("OccurrenceNode", occurrence.id)],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_15.person.id),
                    "name": study_group_15.person.name,
                    "emailAddress": study_group_15.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group_15.group_size,
                "groupName": study_group_15.group_name,
                "studyLevels": [sl.upper() for sl in study_group_15.study_levels.all()],
                "amountOfAdult": study_group_15.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, NOT_ENOUGH_CAPACITY_ERROR)


def test_enrol_cancelled_occurrence(
    api_client, mock_update_event_data, mock_get_event_data, occurrence
):
    study_group = StudyGroupFactory(group_size=10)
    occurrence.cancelled = True
    occurrence.save()

    variables = {
        "input": {
            "occurrenceIds": [to_global_id("OccurrenceNode", occurrence.id)],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group.person.id),
                    "name": study_group.person.name,
                    "emailAddress": study_group.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group.group_size,
                "groupName": study_group.group_name,
                "studyLevels": [sl.id.upper() for sl in StudyLevel.objects.all()],
                "amountOfAdult": study_group.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, ENROL_CANCELLED_OCCURRENCE_ERROR)


def test_enrol_occurrence_without_required_information(
    api_client, mock_update_event_data, mock_get_event_data, occurrence
):
    study_group = StudyGroupFactory(group_size=10, extra_needs="")
    p_event = occurrence.p_event
    p_event.mandatory_additional_information = True
    p_event.save()

    assert study_group.extra_needs == ""

    variables = {
        "input": {
            "occurrenceIds": [to_global_id("OccurrenceNode", occurrence.id)],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group.person.id),
                    "name": study_group.person.name,
                    "emailAddress": study_group.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group.group_size,
                "groupName": study_group.group_name,
                "studyLevels": [sl.id.upper() for sl in StudyLevel.objects.all()],
                "amountOfAdult": study_group.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, MISSING_MANDATORY_INFORMATION_ERROR)


def test_enrol_occurrence(snapshot, api_client, mock_get_event_data):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )

    occurrence_2 = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=2,
        seat_type=Occurrence.OCCURRENCE_SEAT_TYPE_ENROLMENT_COUNT,
    )

    variables = {
        "input": {
            "occurrenceIds": [
                to_global_id("OccurrenceNode", occurrence.id),
                to_global_id("OccurrenceNode", occurrence_2.id),
            ],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_15.person.id),
                    "name": study_group_15.person.name,
                    "emailAddress": study_group_15.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group_15.group_size,
                "groupName": study_group_15.group_name,
                "studyLevels": [sl.upper() for sl in study_group_15.study_levels.all()],
                "amountOfAdult": study_group_15.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)


def test_enrol_occurrence_without_unit_info_should_raise_error(
    snapshot, api_client, mock_get_event_data
):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )

    occurrence_2 = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=2,
        seat_type=Occurrence.OCCURRENCE_SEAT_TYPE_ENROLMENT_COUNT,
    )

    variables = {
        "input": {
            "occurrenceIds": [
                to_global_id("OccurrenceNode", occurrence.id),
                to_global_id("OccurrenceNode", occurrence_2.id),
            ],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_15.person.id),
                    "name": study_group_15.person.name,
                    "emailAddress": study_group_15.person.email_address,
                },
                "groupSize": study_group_15.group_size,
                "groupName": study_group_15.group_name,
                "studyLevels": [sl.upper() for sl in study_group_15.study_levels.all()],
                "amountOfAdult": study_group_15.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, INVALID_STUDY_GROUP_UNIT_INFO_ERROR)


def test_enrol_occurrence_with_captcha(
    snapshot, api_client, mock_get_event_data, settings, mock_recaptcha_data
):
    settings.CAPTCHA_ENABLED = True
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )

    variables = {
        "input": {
            "occurrenceIds": [to_global_id("OccurrenceNode", occurrence.id)],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_15.person.id),
                    "name": study_group_15.person.name,
                    "emailAddress": study_group_15.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group_15.group_size,
                "groupName": study_group_15.group_name,
                "studyLevels": [sl.upper() for sl in study_group_15.study_levels.all()],
                "amountOfAdult": study_group_15.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, CAPTCHA_VALIDATION_FAILED_ERROR)
    variables["input"]["captchaKey"] = "captcha_key"
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)


def test_enrol_auto_acceptance_occurrence(snapshot, api_client, mock_get_event_data):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    auto_accept_p_event = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        auto_acceptance=True,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )

    auto_accept_occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=auto_accept_p_event,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )

    variables = {
        "input": {
            "occurrenceIds": [to_global_id("OccurrenceNode", occurrence.id)],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_15.person.id),
                    "name": study_group_15.person.name,
                    "emailAddress": study_group_15.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group_15.group_size,
                "groupName": study_group_15.group_name,
                "studyLevels": [sl.upper() for sl in study_group_15.study_levels.all()],
                "amountOfAdult": study_group_15.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)

    variables = {
        "input": {
            "occurrenceIds": [
                to_global_id("OccurrenceNode", auto_accept_occurrence.id),
            ],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_15.person.id),
                    "name": study_group_15.person.name,
                    "emailAddress": study_group_15.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group_15.group_size,
                "groupName": study_group_15.group_name,
                "studyLevels": [sl.upper() for sl in study_group_15.study_levels.all()],
                "amountOfAdult": study_group_15.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)


def test_enrol_max_needed_occurrences(snapshot, api_client, mock_get_event_data):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        needed_occurrences=2,
    )

    occurrences = OccurrenceFactory.create_batch(
        3,
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )

    occurrence_ids = [to_global_id("OccurrenceNode", o.id) for o in occurrences]

    variables = {
        "input": {
            "occurrenceIds": occurrence_ids,
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_15.person.id),
                    "name": study_group_15.person.name,
                    "emailAddress": study_group_15.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group_15.group_size,
                "groupName": study_group_15.group_name,
                "studyLevels": [sl.upper() for sl in study_group_15.study_levels.all()],
                "amountOfAdult": study_group_15.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, MAX_NEEDED_OCCURRENCES_REACHED_ERROR)


@pytest.mark.django_db
def test_auto_accept_message_is_used_as_custom_message_in_auto_approved_enrolments(
    snapshot,
    api_client,
    mock_get_event_data,
    notification_template_enrolment_approved_en,
    notification_template_enrolment_approved_fi,
):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    auto_acceptance_message = "Testing auto acceptance message"
    auto_accept_p_event: PalvelutarjotinEvent = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        auto_acceptance=True,
        auto_acceptance_message=auto_acceptance_message,
    )
    auto_accept_occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=auto_accept_p_event,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    variables = {
        "input": {
            "occurrenceIds": [
                to_global_id("OccurrenceNode", auto_accept_occurrence.id),
            ],
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_15.person.id),
                    "name": study_group_15.person.name,
                    "emailAddress": study_group_15.person.email_address,
                },
                "unitName": "To be created group",
                "groupSize": study_group_15.group_size,
                "groupName": study_group_15.group_name,
                "studyLevels": [sl.upper() for sl in study_group_15.study_levels.all()],
                "amountOfAdult": study_group_15.amount_of_adult,
            },
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)
    assert len(mail.outbox) == 1
    body = mail.outbox[0].body
    assert auto_acceptance_message in body
    assert_mails_match_snapshot(snapshot)


UNENROL_OCCURRENCE_MUTATION = """
mutation unenrolOccurrence($input: UnenrolOccurrenceMutationInput!){
  unenrolOccurrence(input: $input){
    occurrence{
       startTime
       seatsTaken
       seatsApproved
       remainingSeats
       amountOfSeats
    }
    studyGroup{
        unitName
    }
  }
}
"""


def test_unenrol_occurrence_unauthorized(
    snapshot, api_client, user_api_client, staff_api_client, mock_get_event_data
):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    EnrolmentFactory(occurrence=occurrence, study_group=study_group_15)
    assert occurrence.study_groups.count() == 1

    variables = {
        "input": {
            "occurrenceId": to_global_id("OccurrenceNode", occurrence.id),
            "studyGroupId": to_global_id("StudyGroupNode", study_group_15.id),
        }
    }

    executed = api_client.execute(UNENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)
    executed = user_api_client.execute(UNENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)
    executed = staff_api_client.execute(
        UNENROL_OCCURRENCE_MUTATION, variables=variables
    )
    assert_permission_denied(executed)
    assert occurrence.study_groups.count() == 1


def test_unenrol_occurrence(snapshot, staff_api_client, mock_get_event_data):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        needed_occurrences=2,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    occurrence_2 = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    EnrolmentFactory(occurrence=occurrence, study_group=study_group_15)
    EnrolmentFactory(occurrence=occurrence_2, study_group=study_group_15)
    assert occurrence.study_groups.count() == 1
    assert occurrence_2.study_groups.count() == 1
    assert study_group_15.occurrences.count() == 2

    variables = {
        "input": {
            "occurrenceId": to_global_id("OccurrenceNode", occurrence.id),
            "studyGroupId": to_global_id("StudyGroupNode", study_group_15.id),
        }
    }
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(
        UNENROL_OCCURRENCE_MUTATION, variables=variables
    )
    snapshot.assert_match(executed)
    assert occurrence.study_groups.count() == 0
    assert occurrence_2.study_groups.count() == 0
    assert study_group_15.occurrences.count() == 0


APPROVE_ENROLMENT_MUTATION = """
mutation approveEnrolmentMutation($input: ApproveEnrolmentMutationInput!){
  approveEnrolment(input: $input){
    enrolment{
       status
    }
  }
}
"""

DECLINE_ENROLMENT_MUTATION = """
mutation declineEnrolmentMutation($input: DeclineEnrolmentMutationInput!){
  declineEnrolment(input: $input){
    enrolment{
       status
    }
  }
}
"""


def test_approve_cancelled_occurrence_enrolment(
    snapshot, staff_api_client, mock_get_event_data
):
    study_group = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        needed_occurrences=1,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )

    EnrolmentFactory(occurrence=occurrence, study_group=study_group)
    occurrence.cancelled = True
    occurrence.save()
    enrolment = occurrence.enrolments.first()

    variables = {"input": {"enrolmentId": to_global_id("EnrolmentNode", enrolment.id)}}
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(APPROVE_ENROLMENT_MUTATION, variables=variables)
    assert_match_error_code(executed, ENROL_CANCELLED_OCCURRENCE_ERROR)


def test_approve_enrolment(
    snapshot,
    staff_api_client,
    mock_get_event_data,
    notification_template_enrolment_approved_en,
    notification_template_enrolment_approved_fi,
):
    study_group_15 = StudyGroupFactory(group_size=15)
    study_group_10 = StudyGroupFactory(group_size=10)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        needed_occurrences=1,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    EnrolmentFactory(
        occurrence=occurrence, study_group=study_group_15, person=study_group_15.person
    )
    enrolment = occurrence.enrolments.first()
    EnrolmentFactory(
        occurrence=occurrence, study_group=study_group_10, person=study_group_10.person
    )
    assert occurrence.study_groups.count() == 2
    assert enrolment.status == Enrolment.STATUS_PENDING

    variables = {"input": {"enrolmentId": to_global_id("EnrolmentNode", enrolment.id)}}
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(APPROVE_ENROLMENT_MUTATION, variables=variables)
    snapshot.assert_match(executed)
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)
    for e in study_group_15.enrolments.all():
        # Check if related enrolments change
        assert e.status == Enrolment.STATUS_APPROVED
    for e in study_group_10.enrolments.all():
        # Check if unrelated enrolments do not change
        assert e.status == Enrolment.STATUS_PENDING

    executed = staff_api_client.execute(APPROVE_ENROLMENT_MUTATION, variables=variables)
    assert_match_error_code(executed, API_USAGE_ERROR)


def test_approve_enrolment_with_custom_message(
    snapshot,
    staff_api_client,
    mock_get_event_data,
    notification_template_enrolment_approved_en,
    notification_template_enrolment_approved_fi,
):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        needed_occurrences=1,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    EnrolmentFactory(
        occurrence=occurrence, study_group=study_group_15, person=study_group_15.person
    )
    assert occurrence.study_groups.count() == 1
    enrolment = occurrence.enrolments.first()
    assert enrolment.status == Enrolment.STATUS_PENDING

    variables = {
        "input": {
            "enrolmentId": to_global_id("EnrolmentNode", enrolment.id),
            "customMessage": "custom message",
        }
    }
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(APPROVE_ENROLMENT_MUTATION, variables=variables)
    snapshot.assert_match(executed)
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)


def test_approve_enrolment_with_single_enrolment_when_multiple_needed(
    snapshot, staff_api_client, mock_get_event_data
):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        needed_occurrences=2,
        auto_acceptance=False,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    enrolment = EnrolmentFactory(
        occurrence=occurrence, study_group=study_group_15, person=study_group_15.person
    )
    variables = {"input": {"enrolmentId": to_global_id("EnrolmentNode", enrolment.id)}}
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(APPROVE_ENROLMENT_MUTATION, variables=variables)
    # Do not approve enrolment if needed_occurrences > 1
    assert_match_error_code(executed, API_USAGE_ERROR)


def test_decline_enrolment(
    snapshot,
    staff_api_client,
    mock_get_event_data,
    notification_template_enrolment_declined_en,
    notification_template_enrolment_declined_fi,
):
    study_group_15 = StudyGroupFactory(group_size=15)
    study_group_10 = StudyGroupFactory(group_size=10)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        needed_occurrences=2,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    occurrence_2 = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    EnrolmentFactory(
        occurrence=occurrence, study_group=study_group_15, person=study_group_15.person
    )
    enrolment = occurrence.enrolments.first()
    EnrolmentFactory(
        occurrence=occurrence_2,
        study_group=study_group_15,
        person=study_group_15.person,
    )
    EnrolmentFactory(
        occurrence=occurrence, study_group=study_group_10, person=study_group_10.person
    )
    EnrolmentFactory(
        occurrence=occurrence_2,
        study_group=study_group_10,
        person=study_group_10.person,
    )

    assert occurrence.study_groups.count() == 2
    assert occurrence_2.study_groups.count() == 2
    assert enrolment.status == Enrolment.STATUS_PENDING

    variables = {"input": {"enrolmentId": to_global_id("EnrolmentNode", enrolment.id)}}
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(DECLINE_ENROLMENT_MUTATION, variables=variables)
    snapshot.assert_match(executed)
    assert len(mail.outbox) == 2
    assert_mails_match_snapshot(snapshot)
    for e in study_group_15.enrolments.all():
        # Check if related enrolments change
        assert e.status == Enrolment.STATUS_DECLINED
    for e in study_group_10.enrolments.all():
        # Check if unrelated enrolments do not change
        assert e.status == Enrolment.STATUS_PENDING

    executed = staff_api_client.execute(DECLINE_ENROLMENT_MUTATION, variables=variables)
    assert_match_error_code(executed, API_USAGE_ERROR)


def test_decline_enrolment_with_custom_message(
    snapshot,
    staff_api_client,
    mock_get_event_data,
    notification_template_enrolment_declined_en,
    notification_template_enrolment_declined_fi,
):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    EnrolmentFactory(
        occurrence=occurrence, study_group=study_group_15, person=study_group_15.person
    )
    assert occurrence.study_groups.count() == 1
    enrolment = occurrence.enrolments.first()
    assert enrolment.status == Enrolment.STATUS_PENDING

    variables = {
        "input": {
            "enrolmentId": to_global_id("EnrolmentNode", enrolment.id),
            "customMessage": "custom message",
        }
    }
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(DECLINE_ENROLMENT_MUTATION, variables=variables)
    snapshot.assert_match(executed)
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)


UPDATE_ENROLMENT_MUTATION = """
mutation updateEnrolmentMutation($input: UpdateEnrolmentMutationInput!){
  updateEnrolment(input: $input){
    enrolment{
      studyGroup{
        unitName
        groupName
        amountOfAdult
        groupSize
        enrolments{
            edges{
               node{
                   notificationType
               }
            }
        }
      }
      occurrence{
        startTime
        seatsTaken
        seatsApproved
        remainingSeats
        amountOfSeats
      }
      notificationType
      status
    }
  }
}
"""


def test_update_enrolment_unauthorized(
    api_client, user_api_client, mock_get_event_data
):
    study_group_15 = StudyGroupFactory(group_size=15)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    EnrolmentFactory(occurrence=occurrence, study_group=study_group_15)
    assert Enrolment.objects.count() == 1
    enrolment = Enrolment.objects.first()
    variables = {"input": {"enrolmentId": to_global_id("EnrolmentNode", enrolment.id)}}

    executed = api_client.execute(UPDATE_ENROLMENT_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = user_api_client.execute(UPDATE_ENROLMENT_MUTATION, variables=variables)
    assert_permission_denied(executed)


def test_update_enrolment(
    snapshot, staff_api_client, mock_get_event_data, mock_update_event_data
):
    study_group_15 = StudyGroupFactory(group_size=15)
    study_group_10 = StudyGroupFactory(group_size=10)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        needed_occurrences=2,
    )
    occurrence_1 = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=35,
    )
    occurrence_2 = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=35,
    )
    EnrolmentFactory(occurrence=occurrence_1, study_group=study_group_15)
    staff_api_client.user.person.organisations.add(occurrence_1.p_event.organisation)
    enrolment = Enrolment.objects.first()
    EnrolmentFactory(occurrence=occurrence_2, study_group=study_group_15)
    EnrolmentFactory(occurrence=occurrence_1, study_group=study_group_10)
    EnrolmentFactory(occurrence=occurrence_2, study_group=study_group_10)
    assert Enrolment.objects.count() == 4
    variables = {
        "input": {
            "enrolmentId": to_global_id("EnrolmentNode", enrolment.id),
            "notificationType": "SMS",
            "studyGroup": {
                "person": {
                    "id": to_global_id("PersonNode", study_group_15.person.id),
                    "name": study_group_15.person.name,
                    "emailAddress": study_group_15.person.email_address,
                },
                "unitName": "Updated name",
                "groupSize": 16,
                "groupName": "Updated study group name",
                "studyLevels": [sl.upper() for sl in study_group_15.study_levels.all()],
                "amountOfAdult": 3,
            },
        }
    }

    executed = staff_api_client.execute(UPDATE_ENROLMENT_MUTATION, variables=variables)
    snapshot.assert_match(executed)
    unrelated_enrolments = Enrolment.objects.filter(study_group=study_group_10)
    for e in unrelated_enrolments:
        # Check if unrelated enrolments do not change
        assert e.notification_type == NOTIFICATION_TYPE_EMAIL


def test_occurrences_filter_by_date(
    api_client, snapshot, mock_get_event_data, mock_update_event_data
):
    OccurrenceFactory(
        start_time=datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    OccurrenceFactory(
        start_time=datetime(2020, 1, 2, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    variables = {"date": "2020-01-02"}
    executed = api_client.execute(OCCURRENCES_QUERY, variables=variables)

    assert len(executed["data"]["occurrences"]["edges"]) == 1
    snapshot.assert_match(executed)
    OccurrenceFactory(
        start_time=datetime(2020, 1, 2, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    executed = api_client.execute(OCCURRENCES_QUERY, variables=variables)
    assert len(executed["data"]["occurrences"]["edges"]) == 2
    snapshot.assert_match(executed)


def test_occurrences_filter_by_time(
    api_client, snapshot, mock_get_event_data, mock_update_event_data
):
    for i in range(10, 12):
        OccurrenceFactory(
            start_time=datetime(2020, 1, 1, i, 0, 0, tzinfo=timezone.now().tzinfo),
        )
        OccurrenceFactory(
            start_time=datetime(2020, 1, 2, i + 1, 0, 0, tzinfo=timezone.now().tzinfo),
        )
    OccurrenceFactory(
        start_time=datetime(2020, 1, 1, 13, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    variables_1 = {"time": "12:00:00"}
    variables_2 = {"time": "14:00:00+02:00"}
    variables_3 = {"time": "11:00:00+00:00"}

    executed = api_client.execute(OCCURRENCES_QUERY, variables=variables_1)
    snapshot.assert_match(executed)
    assert len(executed["data"]["occurrences"]["edges"]) == 1
    executed = api_client.execute(OCCURRENCES_QUERY, variables=variables_2)
    snapshot.assert_match(executed)
    assert len(executed["data"]["occurrences"]["edges"]) == 1
    executed = api_client.execute(OCCURRENCES_QUERY, variables=variables_3)
    snapshot.assert_match(executed)
    assert len(executed["data"]["occurrences"]["edges"]) == 2
    snapshot.assert_match(executed)


def test_occurrences_filter_by_upcoming(
    snapshot,
    api_client,
    mock_get_event_data,
    mock_update_event_data,
):
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=10,
    )
    # Current date froze on 2020-01-04:
    # Past occurrences
    OccurrenceFactory(
        start_time=datetime(2020, 1, 2, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        end_time=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
    )
    OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        end_time=datetime(2020, 1, 7, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
    )
    OccurrenceFactory(
        start_time=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        end_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
    )
    OccurrenceFactory(
        start_time=datetime(2020, 1, 4, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        end_time=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
    )

    executed = api_client.execute(OCCURRENCES_QUERY, variables={"upcoming": True})
    snapshot.assert_match(executed)
    assert len(executed["data"]["occurrences"]["edges"]) == 3


@pytest.mark.parametrize("enrolment_end_days,count", [(None, 3), (0, 3), (1, 2)])
def test_occurrences_filter_by_enrollable(
    enrolment_end_days,
    count,
    snapshot,
    api_client,
    mock_get_event_data,
    mock_update_event_data,
):
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=enrolment_end_days,
    )

    OccurrenceFactory(
        start_time=datetime(2020, 1, 7, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
    )

    OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
    )

    # Past occurrences
    OccurrenceFactory(
        start_time=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
    )

    executed = api_client.execute(OCCURRENCES_QUERY, variables={"enrollable": True})
    snapshot.assert_match(executed)
    assert len(executed["data"]["occurrences"]["edges"]) == count


def test_occurrences_filter_by_cancelled(
    snapshot, api_client, mock_get_event_data, mock_update_event_data
):
    p_event_1 = PalvelutarjotinEventFactory()
    OccurrenceFactory(
        p_event=p_event_1,
        cancelled=True,
    )
    OccurrenceFactory.create_batch(2, p_event=p_event_1, cancelled=False)

    executed = api_client.execute(OCCURRENCES_QUERY, variables={"cancelled": False})
    snapshot.assert_match(executed)
    assert len(executed["data"]["occurrences"]["edges"]) == 2

    executed = api_client.execute(OCCURRENCES_QUERY, variables={"cancelled": True})
    snapshot.assert_match(executed)
    assert len(executed["data"]["occurrences"]["edges"]) == 1


def test_occurrences_filter_by_p_event(
    snapshot, api_client, mock_get_event_data, mock_update_event_data
):
    p_event_1 = PalvelutarjotinEventFactory()
    p_event_2 = PalvelutarjotinEventFactory()
    OccurrenceFactory.create_batch(2, p_event=p_event_1)
    OccurrenceFactory(p_event=p_event_2)

    executed = api_client.execute(
        OCCURRENCES_QUERY,
        variables={"pEvent": to_global_id("PalvelutarjotinNode", p_event_1.id)},
    )
    snapshot.assert_match(executed)
    assert len(executed["data"]["occurrences"]["edges"]) == 2

    executed = api_client.execute(
        OCCURRENCES_QUERY,
        variables={"pEvent": to_global_id("PalvelutarjotinNode", p_event_2.id)},
    )
    snapshot.assert_match(executed)
    assert len(executed["data"]["occurrences"]["edges"]) == 1


def test_occurrences_ordering_by_order_by_start_time(
    snapshot, api_client, mock_get_event_data, mock_update_event_data
):
    OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    OccurrenceFactory(
        start_time=datetime(2020, 1, 7, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    OccurrenceFactory(
        start_time=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )

    executed_asc = api_client.execute(
        OCCURRENCES_QUERY, variables={"orderBy": ["startTime"]}
    )
    snapshot.assert_match(executed_asc)

    executed_desc = api_client.execute(
        OCCURRENCES_QUERY, variables={"orderBy": ["-startTime"]}
    )
    snapshot.assert_match(executed_desc)

    # Its easier to see the difference when a list of ids is compared
    assert executed_asc["data"]["occurrences"]["edges"] == list(
        reversed(executed_desc["data"]["occurrences"]["edges"])
    )


def test_occurrences_order_by_with_different_input_types(
    api_client, mock_get_event_data, mock_update_event_data
):
    OccurrenceFactory.create_batch(10)
    execute_asc1 = api_client.execute(
        OCCURRENCES_QUERY, variables={"orderBy": ["startTime"]}
    )
    execute_asc2 = api_client.execute(
        OCCURRENCES_QUERY, variables={"orderBy": ["start_time"]}
    )
    assert execute_asc1 == execute_asc2

    execute_desc1 = api_client.execute(
        OCCURRENCES_QUERY, variables={"orderBy": ["-startTime"]}
    )
    execute_desc2 = api_client.execute(
        OCCURRENCES_QUERY, variables={"orderBy": ["-start_time"]}
    )
    assert execute_desc1 == execute_desc2

    assert execute_asc1 != execute_desc1

    execute_asc3 = api_client.execute(
        OCCURRENCES_QUERY, variables={"orderBy": "startTime"}
    )

    execute_desc3 = api_client.execute(
        OCCURRENCES_QUERY, variables={"orderBy": "-startTime"}
    )
    assert execute_asc1 == execute_asc3
    assert execute_desc1 == execute_desc3


def test_occurrences_ordering_by_order_by_end_time(
    snapshot, api_client, mock_get_event_data, mock_update_event_data
):
    OccurrenceFactory(
        end_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    OccurrenceFactory(
        end_time=datetime(2020, 1, 7, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    OccurrenceFactory(
        end_time=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )

    executed_asc = api_client.execute(
        OCCURRENCES_QUERY, variables={"orderBy": ["endTime"]}
    )
    snapshot.assert_match(executed_asc)

    executed_desc = api_client.execute(
        OCCURRENCES_QUERY, variables={"orderBy": ["-endTime"]}
    )
    snapshot.assert_match(executed_desc)

    # Its easier to see the difference when a list of ids is compared
    assert executed_asc["data"]["occurrences"]["edges"] == list(
        reversed(executed_desc["data"]["occurrences"]["edges"])
    )


def test_occurrences_next_and_last_occurrence(
    api_client, mock_get_event_data, mock_update_event_data
):
    p_event = PalvelutarjotinEventFactory()
    # Current date froze on 2020-01-04:
    OccurrenceFactory(
        p_event=p_event,
        start_time=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    OccurrenceFactory(
        p_event=p_event,
        start_time=datetime(2020, 1, 7, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    OccurrenceFactory(
        p_event=p_event,
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )
    # next, but cancelled, so won't be picked
    OccurrenceFactory(
        p_event=p_event,
        start_time=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        cancelled=True,
    )
    # last, but cancelled, so won't be picked
    OccurrenceFactory(
        p_event=p_event,
        start_time=datetime(2020, 1, 8, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        cancelled=True,
    )

    executed = api_client.execute(
        """
            query Occurrences(
                $pEvent: ID,
            ){
            occurrences(
                pEvent: $pEvent,
            ){
                edges{
                node{
                    pEvent{
                        linkedEventId
                        nextOccurrenceDatetime
                        lastOccurrenceDatetime
                    }
                }
                }
            }
            }
        """,
        variables={"pEvent": to_global_id("PalvelutarjotinNode", p_event.id)},
    )

    assert len(executed["data"]["occurrences"]["edges"]) == 5

    for edge in executed["data"]["occurrences"]["edges"]:
        assert (
            edge["node"]["pEvent"]["nextOccurrenceDatetime"]
            == "2020-01-06T00:00:00+00:00"
        )
        assert (
            edge["node"]["pEvent"]["lastOccurrenceDatetime"]
            == "2020-01-07T00:00:00+00:00"
        )


NOTIFICATION_TEMPLATE_QUERY = """
query NotificationTemplate($type: NotificationTemplateType!, $language: Language!,
$context:JSONString!){
  notificationTemplate(templateType: $type, language: $language, context: $context){
    template{
        type
    }
    customContextPreviewHtml
    customContextPreviewText
  }
}
"""


def test_notification_template_query_error(
    snapshot, api_client, notification_template_enrolment_approved_en
):
    variables = {
        "type": "ENROLMENT_APPROVED",
        "language": "EN",
        "context": '{"event":{"name":{"fi":"This should be `en`"}},'
        '"study_group":{'
        '"name":"group name","person":{'
        '"email_address":"email@me.com"}},"occurrence":{'
        '"start_time":"2020-12-12","p_event":{'
        '"linked_event_id":"linked_event_id"}},'
        '"custom_message":"custom_message"}',
    }

    # Raise error because context var is invalid
    executed = api_client.execute(NOTIFICATION_TEMPLATE_QUERY, variables=variables)
    assert_match_error_code(executed, API_USAGE_ERROR)


def test_notification_template_query(
    snapshot,
    api_client,
    notification_template_enrolment_approved_en,
    notification_template_enrolment_approved_fi,
):
    variables = {
        "type": "ENROLMENT_APPROVED",
        "language": "EN",
        "context": '{"event":{"name":{"en":"Name in english"}},'
        '"study_group":{'
        '"name":"group name","person":{'
        '"email_address":"email@me.com"}},"occurrence":{'
        '"start_time":"2020-12-12","p_event":{'
        '"linked_event_id":"linked_event_id"}},'
        '"custom_message":"custom_message"}',
    }
    executed = api_client.execute(NOTIFICATION_TEMPLATE_QUERY, variables=variables)
    snapshot.assert_match(executed)


CANCEL_OCCURRENCE_MUTATION = """
mutation cancelOccurrenceMutation($input: CancelOccurrenceMutationInput!){
    cancelOccurrence(input: $input){
        occurrence{
            cancelled
        }
    }
}
"""


def test_cancel_occurrence_unauthorized(
    api_client,
    user_api_client,
    staff_api_client,
    mock_get_event_data,
    mock_update_event_data,
    occurrence,
):
    executed = api_client.execute(
        CANCEL_OCCURRENCE_MUTATION,
        variables={"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}},
    )
    assert_permission_denied(executed)
    executed = user_api_client.execute(
        CANCEL_OCCURRENCE_MUTATION,
        variables={"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}},
    )
    assert_permission_denied(executed)
    executed = staff_api_client.execute(
        CANCEL_OCCURRENCE_MUTATION,
        variables={"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}},
    )
    assert_permission_denied(executed)


def test_cancel_occurrence(
    snapshot, staff_api_client, mock_get_event_data, mock_update_event_data, occurrence
):
    assert not occurrence.cancelled
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(
        CANCEL_OCCURRENCE_MUTATION,
        variables={"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}},
    )
    snapshot.assert_match(executed)
    executed = staff_api_client.execute(
        CANCEL_OCCURRENCE_MUTATION,
        variables={"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}},
    )
    for e in occurrence.enrolments.all():
        assert e.status == Enrolment.STATUS_CANCELLED
    assert_match_error_code(executed, API_USAGE_ERROR)


ENROLMENTS_SUMMARY_QUERY = """
query enrolmentSummary($organisationId: ID!, $status: EnrolmentStatus){
  enrolmentSummary(organisationId: $organisationId, status:$status){
    count
    edges{
      node{
        status
      }
    }
  }
}
"""


def test_enrolments_summary_unauthorized(
    snapshot, api_client, user_api_client, staff_api_client, organisation
):
    organisation_gid = to_global_id("OrganisationNode", organisation.id)
    executed = api_client.execute(
        ENROLMENTS_SUMMARY_QUERY, variables={"organisationId": organisation_gid}
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        ENROLMENTS_SUMMARY_QUERY, variables={"organisationId": organisation_gid}
    )
    assert_permission_denied(executed)

    # assert organisation not in staff_api_client.user.person.organisations
    executed = staff_api_client.execute(
        ENROLMENTS_SUMMARY_QUERY, variables={"organisationId": organisation_gid}
    )
    assert_permission_denied(executed)


def test_enrolments_summary(
    snapshot, staff_api_client, mock_get_event_data, occurrence
):
    organisation_gid = to_global_id(
        "OrganisationNode", occurrence.p_event.organisation.id
    )
    EnrolmentFactory(occurrence=occurrence)
    EnrolmentFactory(
        occurrence=occurrence,
        status=Enrolment.STATUS_APPROVED,
    )
    EnrolmentFactory(
        occurrence=occurrence,
        status=Enrolment.STATUS_DECLINED,
    )
    EnrolmentFactory(
        occurrence=occurrence,
        status=Enrolment.STATUS_CANCELLED,
    )

    assert Enrolment.objects.count() == 4
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(
        ENROLMENTS_SUMMARY_QUERY, variables={"organisationId": organisation_gid}
    )
    snapshot.assert_match(executed)
    for status, _ in Enrolment.STATUSES:
        executed = staff_api_client.execute(
            ENROLMENTS_SUMMARY_QUERY,
            variables={"organisationId": organisation_gid, "status": status.upper()},
        )
        snapshot.assert_match(executed)


CANCEL_ENROLMENT_QUERY = """
query cancellingEnrolment($id: ID!){
    cancellingEnrolment(id: $id){
        enrolmentTime
        status
        occurrence{
            seatsTaken
        }
        studyGroup{
            unitName
            groupSize
        }
    }
}
"""


def test_cancel_enrolment_query(
    snapshot, api_client, mock_get_event_data, occurrence, study_group
):
    enrolment = EnrolmentFactory(occurrence=occurrence, study_group=study_group)
    executed = api_client.execute(
        CANCEL_ENROLMENT_QUERY, variables={"id": enrolment.get_unique_id()}
    )
    snapshot.assert_match(executed)


CANCEL_ENROLMENT_MUTATION = """
    mutation cancelEnrolmentMutation($input: CancelEnrolmentMutationInput!){
        cancelEnrolment(input: $input){
            enrolment{
                status
            }
        }
    }
"""


def test_ask_for_cancelled_confirmation_mutation_error(
    snapshot, api_client, study_group, mock_get_event_data
):
    occurrence = OccurrenceFactory(p_event__needed_occurrences=1)
    occurrence_2 = OccurrenceFactory(p_event__needed_occurrences=2)

    enrolment = EnrolmentFactory(occurrence=occurrence, study_group=study_group)
    enrolment_2 = EnrolmentFactory(occurrence=occurrence_2, study_group=study_group)

    enrolment.set_status(Enrolment.STATUS_CANCELLED)
    executed = api_client.execute(
        CANCEL_ENROLMENT_MUTATION,
        variables={"input": {"uniqueId": enrolment.get_unique_id()}},
    )

    # Enrolment already cancelled
    assert_match_error_code(executed, API_USAGE_ERROR)

    executed = api_client.execute(
        CANCEL_ENROLMENT_MUTATION,
        variables={"input": {"uniqueId": enrolment_2.get_unique_id()}},
    )

    # Cannot cancel multi-occurrences enrolment
    assert_match_error_code(executed, API_USAGE_ERROR)


def test_ask_for_cancelled_confirmation_mutation(
    snapshot, api_client, study_group, mock_get_event_data
):
    occurrence = OccurrenceFactory(p_event__needed_occurrences=1)

    enrolment = EnrolmentFactory(occurrence=occurrence, study_group=study_group)
    assert enrolment.verification_tokens.count() == 0
    executed = api_client.execute(
        CANCEL_ENROLMENT_MUTATION,
        variables={"input": {"uniqueId": enrolment.get_unique_id()}},
    )

    snapshot.assert_match(executed)

    token_qs = enrolment.get_active_verification_tokens(
        verification_type=VerificationToken.VERIFICATION_TYPE_CANCELLATION
    )
    assert token_qs.count() == 1
    token = token_qs[0]
    api_client.execute(
        CANCEL_ENROLMENT_MUTATION,
        variables={"input": {"uniqueId": enrolment.get_unique_id()}},
    )

    # Verify if token changed
    enrolment.refresh_from_db()
    new_token = enrolment.get_active_verification_tokens(
        verification_type=VerificationToken.VERIFICATION_TYPE_CANCELLATION
    )[0]
    assert not token.id == new_token.id


def test_cancel_enrolment_mutation_invalid_token(
    snapshot, api_client, study_group, mock_get_event_data
):
    occurrence = OccurrenceFactory(p_event__needed_occurrences=1)

    enrolment = EnrolmentFactory(occurrence=occurrence, study_group=study_group)

    # Token does not exist
    invalid_token_key = "invalid_token_key"
    executed = api_client.execute(
        CANCEL_ENROLMENT_MUTATION,
        variables={
            "input": {"uniqueId": enrolment.get_unique_id(), "token": invalid_token_key}
        },
    )
    assert_match_error_code(executed, INVALID_TOKEN_ERROR)

    invalid_token_key = EnrolmentFactory().create_cancellation_token().key
    executed = api_client.execute(
        CANCEL_ENROLMENT_MUTATION,
        variables={
            "input": {"uniqueId": enrolment.get_unique_id(), "token": invalid_token_key}
        },
    )
    assert_match_error_code(executed, INVALID_TOKEN_ERROR)

    token = enrolment.create_cancellation_token()
    # Expired token
    token.expiry_date = timezone.now() - timedelta(days=1)
    token.save()
    assert token.is_active
    executed = api_client.execute(
        CANCEL_ENROLMENT_MUTATION,
        variables={
            "input": {"uniqueId": enrolment.get_unique_id(), "token": token.key}
        },
    )
    assert_match_error_code(executed, INVALID_TOKEN_ERROR)

    # Deactivated token
    token.expiry_date = timezone.now() + timedelta(days=1)
    token.is_active = False
    token.save()
    executed = api_client.execute(
        CANCEL_ENROLMENT_MUTATION,
        variables={
            "input": {"uniqueId": enrolment.get_unique_id(), "token": token.key}
        },
    )
    assert_match_error_code(executed, INVALID_TOKEN_ERROR)


def test_cancel_enrolment_mutation(
    snapshot, api_client, study_group, mock_get_event_data
):
    occurrence = OccurrenceFactory(p_event__needed_occurrences=1)

    enrolment = EnrolmentFactory(occurrence=occurrence, study_group=study_group)

    token = enrolment.create_cancellation_token()
    executed = api_client.execute(
        CANCEL_ENROLMENT_MUTATION,
        variables={
            "input": {"uniqueId": enrolment.get_unique_id(), "token": token.key}
        },
    )
    snapshot.assert_match(executed)


MASS_APPROVE_ENROLMENTS_MUTATION = """
mutation massApproveEnrolmentsMutation($input: MassApproveEnrolmentsMutationInput!){
  massApproveEnrolments(input: $input){
    enrolments{
       status
    }
  }
}
"""


def test_mass_approve_enrolment_mutation(
    snapshot, staff_api_client, mock_get_event_data
):
    occurrence = OccurrenceFactory(
        p_event__needed_occurrences=1,
        p_event__auto_acceptance=False,
        amount_of_seats=100,
    )
    enrolment_1 = EnrolmentFactory(occurrence=occurrence, study_group__group_size=10)
    enrolment_2 = EnrolmentFactory(occurrence=occurrence, study_group__group_size=10)
    enrolment_3 = EnrolmentFactory(occurrence=occurrence, study_group__group_size=10)
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(
        MASS_APPROVE_ENROLMENTS_MUTATION,
        variables={
            "input": {
                "enrolmentIds": [
                    to_global_id("EnrolmentNode", enrolment_1.id),
                    to_global_id("EnrolmentNode", enrolment_2.id),
                    to_global_id("EnrolmentNode", enrolment_3.id),
                ],
                "customMessage": "Custom message",
            }
        },
    )
    snapshot.assert_match(executed)


def test_mass_approve_multi_occurrences_enrolment_mutation(
    snapshot, staff_api_client, mock_get_event_data
):
    occurrence = OccurrenceFactory(
        p_event__needed_occurrences=2,
        p_event__auto_acceptance=False,
        amount_of_seats=100,
    )
    enrolment_1 = EnrolmentFactory(occurrence=occurrence, study_group__group_size=10)
    enrolment_2 = EnrolmentFactory(occurrence=occurrence, study_group__group_size=10)
    enrolment_3 = EnrolmentFactory(occurrence=occurrence, study_group__group_size=10)
    staff_api_client.user.person.organisations.add(occurrence.p_event.organisation)
    executed = staff_api_client.execute(
        MASS_APPROVE_ENROLMENTS_MUTATION,
        variables={
            "input": {
                "enrolmentIds": [
                    to_global_id("EnrolmentNode", enrolment_1.id),
                    to_global_id("EnrolmentNode", enrolment_2.id),
                    to_global_id("EnrolmentNode", enrolment_3.id),
                ],
                "customMessage": "Custom message",
            }
        },
    )
    # Do not approve enrolment if needed_occurrences > 1
    assert_match_error_code(executed, API_USAGE_ERROR)
