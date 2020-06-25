from copy import deepcopy
from datetime import datetime

import pytest
from django.utils import timezone
from graphql_relay import to_global_id
from occurrences.factories import (
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from occurrences.models import Occurrence, StudyGroup, VenueCustomData
from organisations.factories import PersonFactory

from common.tests.utils import assert_match_error_code, assert_permission_denied
from palvelutarjotin.consts import (
    ALREADY_JOINED_EVENT_ERROR,
    ENROLMENT_CLOSED_ERROR,
    ENROLMENT_NOT_STARTED_ERROR,
    INVALID_STUDY_GROUP_SIZE_ERROR,
    NOT_ENOUGH_CAPACITY_ERROR,
)


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


STUDY_GROUPS_QUERY = """
query StudyGroups{
  studyGroups{
    edges{
      node{
        name
        person {
          name
        }
        updatedAt
        groupSize
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
    name
    person {
      name
    }
    updatedAt
    groupSize
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
query Occurrences($upcoming: Boolean, $date: Date, $time: Time){
  occurrences(upcoming: $upcoming, date: $date, time: $time){
    edges{
      node{
        placeId
        amountOfSeats
        remainingSeats
        seatsTaken
        autoAcceptance
        pEvent{
            linkedEventId
            enrolmentStart
            enrolmentEndDays
        }
        startTime
        endTime
        studyGroups {
          edges {
            node {
              name
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
        linkedEventId
        enrolmentStart
        enrolmentEndDays
    }
    startTime
    endTime
    studyGroups {
      edges {
        node {
          name
        }
      }
    }
    amountOfSeats
    remainingSeats
    seatsTaken
    autoAcceptance
    minGroupSize
    maxGroupSize
    contactPersons {
      edges {
        node {
          name
        }
      }
    }
    languages
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
            duration
            neededOccurrences
            enrolmentEndDays
            enrolmentStart
            linkedEventId
          }
          languages{
            id
            name
          }
        }
      }
    }
"""

ADD_OCCURRENCE_VARIABLES = {
    "input": {
        "placeId": "place_id",
        "minGroupSize": 10,
        "maxGroupSize": 20,
        "startTime": "2020-05-05T00:00:00+00",
        "endTime": "2020-05-05T00:00:00+00",
        "contactPersons": [
            {"name": "New name", "emailAddress": "newname@email.address"},
        ],
        "pEventId": "",
        "amountOfSeats": 40,
        "autoAcceptance": True,
        "languages": [{"id": "EN"}, {"id": "SV"}],
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
        duration
        neededOccurrences
        enrolmentEndDays
        enrolmentStart
        linkedEventId
      }
      languages{
        id
        name
      }
    }
  }
}
"""

UPDATE_OCCURRENCE_VARIABLES = {
    "input": {
        "placeId": "place_id",
        "minGroupSize": 10,
        "maxGroupSize": 20,
        "startTime": "2020-05-05T00:00:00+00",
        "endTime": "2020-05-05T00:00:00+00",
        "contactPersons": [
            {"id": "", "name": "New name", "emailAddress": "newname@email.address"},
        ],
        "pEventId": "",
        "amountOfSeats": 40,
        "autoAcceptance": True,
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


def test_study_groups_query(snapshot, study_group, api_client):
    executed = api_client.execute(STUDY_GROUPS_QUERY)
    snapshot.assert_match(executed)


def test_study_group_query(snapshot, study_group, api_client):
    executed = api_client.execute(
        STUDY_GROUP_QUERY,
        variables={"id": to_global_id("StudyGroupNode", study_group.id)},
    )
    snapshot.assert_match(executed)


def test_occurrences_query(snapshot, occurrence, api_client):
    executed = api_client.execute(OCCURRENCES_QUERY)
    snapshot.assert_match(executed)


def test_occurrence_query(snapshot, occurrence, api_client):
    executed = api_client.execute(
        OCCURRENCES_QUERY,
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


def test_add_occurrence(snapshot, staff_api_client, organisation, person):
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


def test_update_occurrence_unauthorized(
    api_client, user_api_client, occurrence, staff_api_client
):
    variables = deepcopy(UPDATE_OCCURRENCE_VARIABLES)
    variables["input"]["id"] = to_global_id("OccurrenceNode", occurrence.id)
    executed = api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = user_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = staff_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)


def test_update_occurrence(snapshot, staff_api_client, organisation, person):
    variables = deepcopy(UPDATE_OCCURRENCE_VARIABLES)
    occurrence = OccurrenceFactory(
        contact_persons=[person], p_event__organisation=organisation
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


def test_delete_occurrence_unauthorized(
    api_client, user_api_client, staff_api_client, occurrence
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


def test_delete_occurrence(snapshot, staff_api_client, occurrence):
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
        DELETE_VENUE_MUTATION, variables={"input": {"id": venue.place_id}},
    )
    assert VenueCustomData.objects.count() == 0


ADD_STUDY_GROUP_MUTATION = """
mutation addStudyGroup($input: AddStudyGroupMutationInput!){
  addStudyGroup(input:$input) {
    studyGroup{
      name
      person{
        name
        emailAddress
        phoneNumber
      }
      groupSize
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
        },
        "name": "Sample study group name",
        "groupSize": 20,
    }
}


def test_add_study_group(snapshot, api_client, occurrence, person):
    variables = deepcopy(ADD_STUDY_GROUP_VARIABLES)
    executed = api_client.execute(ADD_STUDY_GROUP_MUTATION, variables=variables)
    snapshot.assert_match(executed)

    # Add study group with pre-defined person)
    variables["input"]["person"]["id"] = to_global_id("PersonNode", person.id)
    executed = api_client.execute(ADD_STUDY_GROUP_MUTATION, variables=variables)
    snapshot.assert_match(executed)


UPDATE_STUDY_GROUP_MUTATION = """
mutation updateStudyGroup($input: UpdateStudyGroupMutationInput!){
  updateStudyGroup(input:$input) {
    studyGroup{
      name
      person{
        name
        emailAddress
        phoneNumber
      }
      groupSize
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
        "name": "Sample study group name",
        "groupSize": 20,
    }
}


def test_update_study_group_unauthenticated(api_client, user_api_client):
    variables = deepcopy(UPDATE_STUDY_GROUP_VARIABLES)
    executed = api_client.execute(UPDATE_STUDY_GROUP_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = user_api_client.execute(UPDATE_STUDY_GROUP_MUTATION, variables=variables)
    assert_permission_denied(executed)


def test_update_study_group_staff_user(snapshot, staff_api_client, study_group, person):
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
    enrolment{
      studyGroup{
        name
      }
      occurrence{
        startTime
        seatsTaken
        remainingSeats
        amountOfSeats
      }
    }
  }
}
"""


def test_enrol_not_started_occurrence(snapshot, api_client):
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
            "occurrenceId": to_global_id("OccurrenceNode", not_started_occurrence.id),
            "studyGroupId": to_global_id("StudyGroupNode", study_group.id),
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, ENROLMENT_NOT_STARTED_ERROR)


def test_enrol_past_occurrence(snapshot, api_client, occurrence):
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
            "occurrenceId": to_global_id("OccurrenceNode", past_occurrence.id),
            "studyGroupId": to_global_id("StudyGroupNode", study_group.id),
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, ENROLMENT_CLOSED_ERROR)


def test_enrol_invalid_group_size(snapshot, api_client, occurrence):
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
        min_group_size=10,
        max_group_size=20,
    )

    variables = {
        "input": {
            "occurrenceId": to_global_id("OccurrenceNode", occurrence.id),
            "studyGroupId": to_global_id("StudyGroupNode", study_group_21.id),
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, INVALID_STUDY_GROUP_SIZE_ERROR)

    variables["input"]["studyGroupId"] = to_global_id(
        "StudyGroupNode", study_group_9.id
    )
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, INVALID_STUDY_GROUP_SIZE_ERROR)


def test_enrol_full_occurrence(snapshot, api_client, occurrence):
    study_group_15 = StudyGroupFactory(group_size=15)
    study_group_20 = StudyGroupFactory(group_size=20)
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
        amount_of_seats=34,
    )

    occurrence.study_groups.add(study_group_20)

    variables = {
        "input": {
            "occurrenceId": to_global_id("OccurrenceNode", occurrence.id),
            "studyGroupId": to_global_id("StudyGroupNode", study_group_15.id),
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, NOT_ENOUGH_CAPACITY_ERROR)


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

    variables = {
        "input": {
            "occurrenceId": to_global_id("OccurrenceNode", occurrence.id),
            "studyGroupId": to_global_id("StudyGroupNode", study_group_15.id),
        }
    }
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)

    # Cannot join another occurrence of the same event
    another_occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    variables["input"]["occurrenceId"] = to_global_id(
        "OccurrenceNode", another_occurrence.id
    )
    executed = api_client.execute(ENROL_OCCURRENCE_MUTATION, variables=variables)
    assert_match_error_code(executed, ALREADY_JOINED_EVENT_ERROR)


UNENROL_OCCURRENCE_MUTATION = """
mutation unenrolOccurrence($input: UnenrolOccurrenceMutationInput!){
  unenrolOccurrence(input: $input){
    occurrence{
       startTime
       seatsTaken
       remainingSeats
       amountOfSeats
    }
    studyGroup{
      name
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
    occurrence.study_groups.add(study_group_15)
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
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=50,
    )
    occurrence.study_groups.add(study_group_15)
    assert occurrence.study_groups.count() == 1

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


def test_occurrences_filter_by_date(api_client, snapshot):
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


def test_occurrences_filter_by_time(api_client, snapshot):
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


def test_occurrences_filter_by_upcoming(snapshot, api_client):
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 5, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=1,
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

    executed = api_client.execute(OCCURRENCES_QUERY, variables={"upcoming": True})
    snapshot.assert_match(executed)
    assert len(executed["data"]["occurrences"]["edges"]) == 2
