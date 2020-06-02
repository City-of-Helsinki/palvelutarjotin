from copy import deepcopy

import pytest
from graphql_relay import to_global_id
from occurrences.factories import OccurrenceFactory
from occurrences.models import Occurrence, VenueCustomData
from organisations.factories import PersonFactory

from common.tests.utils import assert_permission_denied


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
query Occurrences{
  occurrences{
    edges{
      node{
        placeId
        amountOfSeats
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
        organisation {
          name
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
    organisation {
      name
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
          organisation{
            name
          }
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
        "organisationId": "",
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
      organisation{
        name
      }
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
        "organisationId": "",
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


def test_add_occurrence_unauthenticated(api_client, user_api_client):
    executed = api_client.execute(
        ADD_OCCURRENCE_MUTATION, variables=ADD_OCCURRENCE_VARIABLES
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        ADD_OCCURRENCE_MUTATION, variables=ADD_OCCURRENCE_VARIABLES
    )
    assert_permission_denied(executed)


def test_add_occurrence(snapshot, staff_api_client, organisation, person, p_event):
    variables = deepcopy(ADD_OCCURRENCE_VARIABLES)
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
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
    executed = staff_api_client.execute(ADD_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)


def test_update_occurrence_unauthenticated(api_client, user_api_client, occurrence):
    variables = deepcopy(UPDATE_OCCURRENCE_VARIABLES)
    variables["input"]["id"] = to_global_id("OccurrenceNode", occurrence.id)
    executed = api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = user_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)


def test_update_occurrence(snapshot, staff_api_client, organisation, p_event, person):
    variables = deepcopy(UPDATE_OCCURRENCE_VARIABLES)
    occurrence = OccurrenceFactory(contact_persons=[person])
    variables["input"]["id"] = to_global_id("OccurrenceNode", occurrence.id)
    # Change p_event, organisation
    variables["input"]["organisationId"] = to_global_id(
        "OrganisationNode", organisation.id
    )
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

    executed = staff_api_client.execute(UPDATE_OCCURRENCE_MUTATION, variables=variables)
    snapshot.assert_match(executed)


def test_delete_occurrence_unauthenticated(api_client, user_api_client, occurrence):
    variables = {"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}}
    executed = api_client.execute(DELETE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)

    executed = user_api_client.execute(DELETE_OCCURRENCE_MUTATION, variables=variables)
    assert_permission_denied(executed)
    assert Occurrence.objects.count() == 1


def test_delete_occurrence(snapshot, staff_api_client, occurrence):
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
