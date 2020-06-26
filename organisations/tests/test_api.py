from copy import deepcopy

import pytest
from graphql_relay import to_global_id
from organisations.factories import OrganisationFactory, PersonFactory

from common.tests.utils import assert_match_error_code, assert_permission_denied
from palvelutarjotin.consts import API_USAGE_ERROR


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


PERSONS_QUERY = """
query Persons{
  persons{
    edges{
      node{
        name
        phoneNumber
        emailAddress
        language
        organisations{
          edges{
            node{
              name
            }
          }
        }
      }
    }
  }
}
"""

PERSON_QUERY = """
query Person($id:ID!){
  person(id: $id){
    name
    phoneNumber
    emailAddress
    language
    organisations{
      edges{
        node{
          name
        }
      }
    }
  }
}
"""

ORGANISATIONS_QUERY = """
query Organisations{
  organisations{
    edges{
      node{
        publisherId
        name
        phoneNumber
        type
        persons {
          edges {
            node {
              id
            }
          }
        }
      }
    }
  }
}
"""

ORGANISATION_QUERY = """
query Organisation($id : ID!){
  organisation(id: $id){
    publisherId
    name
    phoneNumber
    type
    persons {
      edges {
        node {
          id
        }
      }
    }
  }
}
"""

MY_PROFILE_QUERY = """
query myProfile{
  myProfile{
    name
    phoneNumber
    emailAddress
    language
    organisations{
         edges{
             node{
                 name
             }
         }
      }
  }
}
"""

UPDATE_MY_PROFILE_MUTATION = """
mutation updateMyProfileMutation($input: UpdateMyProfileMutationInput!){
  updateMyProfile(input: $input){
    myProfile{
      name
      phoneNumber
      emailAddress
      language
      organisations{
         edges{
             node{
                 name
             }
         }
      }
    }
  }
}
"""

UPDATE_MY_PROFILE_VARIABLES = {
    "input": {
        "name": "New name",
        "emailAddress": "newEmail@address.com",
        "language": "SV",
    }
}

CREATE_MY_PROFILE_MUTATION = """
mutation createMyProfileMutation($input: CreateMyProfileMutationInput!){
  createMyProfile(input: $input){
    myProfile{
      name
      phoneNumber
      emailAddress
      language
      organisations{
         edges{
             node{
                 name
             }
         }
      }
    }
  }
}
"""

CREATE_MY_PROFILE_VARIABLES = {
    "input": {
        "name": "New name",
        "emailAddress": "newEmail@address.com",
        "language": "EN",
    }
}

UPDATE_PERSON_MUTATION = """
mutation updatePersonMutation($input: UpdatePersonMutationInput!){
  updatePerson(input: $input){
    person{
      name
      organisations {
        edges {
          node {
            name
          }
        }
      }
      phoneNumber
      emailAddress
      language
    }
  }
}
"""

UPDATE_PERSON_VARIABLES = {"input": {"id": "", "name": "New name", "language": "SV"}}

ADD_ORGANISATION_MUTATION = """
mutation addOrganisationMutation($input:AddOrganisationMutationInput!){
  addOrganisation(input: $input){
    organisation{
      name
      type
      phoneNumber
      publisherId
    }
  }
}
"""

ADD_ORGANISATION_VARIABLES = {
    "input": {
        "name": "New organisation",
        "type": "PROVIDER",
        "phoneNumber": "012345678",
        "publisherId": "publisher_id",
    }
}

UPDATE_ORGANISATION_MUTATION = """
mutation updateOrganisationMutation($input:UpdateOrganisationMutationInput!){
  updateOrganisation(input: $input){
    organisation{
      name
      type
      phoneNumber
      publisherId
    }
  }
}
"""

UPDATE_ORGANISATION_VARIABLES = {
    "input": {"id": "", "name": "New name", "publisherId": "publisher_id"}
}


def test_persons_query(snapshot, api_client, user_api_client, staff_api_client, person):
    # Anonymous user should see any person info
    executed = api_client.execute(PERSONS_QUERY)
    snapshot.assert_match(executed)

    # Logged in user should see their own info
    executed = user_api_client.execute(PERSONS_QUERY)
    snapshot.assert_match(executed)

    PersonFactory(user=user_api_client.user)
    executed = user_api_client.execute(PERSONS_QUERY)
    snapshot.assert_match(executed)

    # Staff user should see every person info
    executed = staff_api_client.execute(PERSONS_QUERY)
    snapshot.assert_match(executed)


def test_person_query(snapshot, api_client, user_api_client, staff_api_client, person):
    person_id = to_global_id("PersonNode", person.id)
    # Anonymous user should see any person info
    executed = api_client.execute(PERSON_QUERY, variables={"id": person_id})
    snapshot.assert_match(executed)

    # Logged in user should see their own info
    executed = user_api_client.execute(PERSON_QUERY, variables={"id": person_id})
    snapshot.assert_match(executed)

    p = PersonFactory(user=user_api_client.user)
    executed = user_api_client.execute(
        PERSON_QUERY, variables={"id": to_global_id("PersonNode", p.id)}
    )
    snapshot.assert_match(executed)

    # Staff user should see every person info
    executed = staff_api_client.execute(PERSON_QUERY, variables={"id": person_id})
    snapshot.assert_match(executed)


def test_organisations_query(snapshot, api_client, organisation):
    executed = api_client.execute(ORGANISATIONS_QUERY)
    snapshot.assert_match(executed)


def test_organisation_query(snapshot, api_client, organisation):
    executed = api_client.execute(
        ORGANISATION_QUERY,
        variables={"id": to_global_id("OrganisationNode", organisation.id)},
    )
    snapshot.assert_match(executed)


def test_my_profile_query_unauthenticated(snapshot, api_client, organisation):
    executed = api_client.execute(MY_PROFILE_QUERY)
    assert_permission_denied(executed)


def test_my_profile_query(snapshot, person_api_client, organisation):
    organisation.persons.add(person_api_client.user.person)
    executed = person_api_client.execute(MY_PROFILE_QUERY)
    snapshot.assert_match(executed)


def test_create_my_profile(snapshot, user_api_client, person_api_client, organisation):
    variables = deepcopy(CREATE_MY_PROFILE_VARIABLES)
    variables["input"]["organisations"] = [
        to_global_id("OrganisationNode", organisation.id),
    ]
    # Should raise error if profile already exists
    executed = person_api_client.execute(
        CREATE_MY_PROFILE_MUTATION, variables=variables
    )
    assert_match_error_code(executed, API_USAGE_ERROR)

    executed = user_api_client.execute(CREATE_MY_PROFILE_MUTATION, variables=variables)
    snapshot.assert_match(executed)


def test_update_my_profile(snapshot, person_api_client, organisation):
    person_api_client.user.person.organisations.add(
        OrganisationFactory(name="old organisation")
    )
    variables = deepcopy(UPDATE_MY_PROFILE_VARIABLES)
    variables["input"]["organisations"] = [
        to_global_id("OrganisationNode", organisation.id),
    ]
    executed = person_api_client.execute(
        UPDATE_MY_PROFILE_MUTATION, variables=variables
    )
    snapshot.assert_match(executed)


def test_update_person_mutation_unauthorized(
    api_client, user_api_client, staff_api_client
):
    # Only superusers are allowed to update person data
    executed = api_client.execute(
        UPDATE_PERSON_MUTATION, variables=UPDATE_PERSON_VARIABLES
    )
    assert_permission_denied(executed)
    executed = user_api_client.execute(
        UPDATE_PERSON_MUTATION, variables=UPDATE_PERSON_VARIABLES
    )
    assert_permission_denied(executed)
    executed = staff_api_client.execute(
        UPDATE_PERSON_MUTATION, variables=UPDATE_PERSON_VARIABLES
    )
    assert_permission_denied(executed)


def test_update_person_mutation(snapshot, superuser_api_client, person):
    variables = deepcopy(UPDATE_PERSON_VARIABLES)
    variables["input"]["id"] = to_global_id("PersonNode", person.id)
    executed = superuser_api_client.execute(UPDATE_PERSON_MUTATION, variables=variables)
    snapshot.assert_match(executed)


def test_add_organisation_unauthorized(api_client, user_api_client, staff_api_client):
    # Only superusers are allowed to create/update organisation
    executed = api_client.execute(
        ADD_ORGANISATION_MUTATION, variables=ADD_ORGANISATION_VARIABLES
    )
    assert_permission_denied(executed)
    executed = user_api_client.execute(
        ADD_ORGANISATION_MUTATION, variables=ADD_ORGANISATION_VARIABLES
    )
    assert_permission_denied(executed)
    executed = staff_api_client.execute(
        ADD_ORGANISATION_MUTATION, variables=ADD_ORGANISATION_VARIABLES
    )
    assert_permission_denied(executed)


def test_add_organisation(snapshot, superuser_api_client):
    executed = superuser_api_client.execute(
        ADD_ORGANISATION_MUTATION, variables=ADD_ORGANISATION_VARIABLES
    )
    snapshot.assert_match(executed)


def test_update_organisation_unauthorized(
    api_client, user_api_client, staff_api_client
):
    # Only superusers are allowed to create/update organisation
    executed = api_client.execute(
        UPDATE_ORGANISATION_MUTATION, variables=UPDATE_ORGANISATION_VARIABLES
    )
    assert_permission_denied(executed)
    executed = user_api_client.execute(
        UPDATE_ORGANISATION_MUTATION, variables=UPDATE_ORGANISATION_VARIABLES
    )
    assert_permission_denied(executed)
    executed = staff_api_client.execute(
        UPDATE_ORGANISATION_MUTATION, variables=UPDATE_ORGANISATION_VARIABLES
    )
    assert_permission_denied(executed)


def test_update_organisation(snapshot, superuser_api_client, organisation):
    variables = deepcopy(UPDATE_ORGANISATION_VARIABLES)
    variables["input"]["id"] = to_global_id("OrganisationNode", organisation.id)
    executed = superuser_api_client.execute(
        UPDATE_ORGANISATION_MUTATION, variables=variables
    )
    snapshot.assert_match(executed)
