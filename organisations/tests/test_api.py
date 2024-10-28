from copy import deepcopy

import pytest
from django.core import mail
from graphql_relay import to_global_id

from common.tests.utils import assert_match_error_code, assert_permission_denied
from occurrences.factories import (
    EnrolmentFactory,
    EventQueueEnrolmentFactory,
    PalvelutarjotinEventFactory,
)
from organisations.factories import OrganisationFactory, PersonFactory, UserFactory
from organisations.models import Organisation, Person
from palvelutarjotin.consts import (
    API_USAGE_ERROR,
    INVALID_EMAIL_FORMAT_ERROR,
    OBJECT_DOES_NOT_EXIST_ERROR,
)


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
    placeIds
  }
}
"""

ORGANISATIONS_QUERY = """
query Organisations($type : OrganisationsOrganisationTypeChoices){
  organisations(type:$type) {
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
    isStaff
    organisations{
        edges{
            node{
                name
            }
        }
    }
    placeIds
  }
}
"""

MY_PROFILE_QUERY_WITH_ORGANISATIONS_PERSONS = """
query myProfile {
  myProfile {
    organisations {
      edges {
        node {
          persons {
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
      isStaff
      organisations{
         edges{
             node{
                 name
             }
         }
      }
      placeIds
    }
  }
}
"""

UPDATE_MY_PROFILE_VARIABLES = {
    "input": {
        "name": "New name",
        "emailAddress": "newEmail@address.com",
        "language": "SV",
        "placeIds": ["xyz:123", "xxx:123"],
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
      isStaff
      organisations{
         edges{
             node{
                 name
             }
         }
      }
      organisationproposalSet{
        edges{
          node{
            name
          }
        }
      }
      placeIds
    }
  }
}
"""

CREATE_ORGANISATION_PROPOSAL_VARIABLES = {
    "name": "3rd party org",
    "description": "Description about 3rd party org.",
    "phoneNumber": "1234567890",
}

CREATE_MY_PROFILE_VARIABLES = {
    "input": {
        "name": "New name",
        "emailAddress": "newEmail@address.com",
        "language": "EN",
        "organisationProposals": [CREATE_ORGANISATION_PROPOSAL_VARIABLES],
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


def test_persons_query_should_not_include_deactivated_users(staff_api_client):
    (active_person, deactivated_person) = PersonFactory.create_batch(2)
    deactivated_person.user.is_active = False
    deactivated_person.user.save()
    executed = staff_api_client.execute(PERSONS_QUERY)
    assert deactivated_person.name not in [
        e["node"]["name"] for e in executed["data"]["persons"]["edges"]
    ]
    assert all(
        (name in (e["node"]["name"] for e in executed["data"]["persons"]["edges"]))
        for name in [active_person.name, staff_api_client.user.person.name]
    )


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


def test_organisations_query_large_max_limit(staff_api_client, organisation):
    persons = PersonFactory.create_batch(size=250, organisations=[organisation]) + [
        staff_api_client.user.person
    ]
    organisation.persons.add(*persons)
    executed = staff_api_client.execute(ORGANISATIONS_QUERY)
    organisation_edges = executed["data"]["organisations"]["edges"]
    assert any(
        len(organisation_edge["node"]["persons"]["edges"]) == 251
        for organisation_edge in organisation_edges
    )


@pytest.mark.django_db
def test_organisations_query_type_filter(snapshot, api_client):
    OrganisationFactory.create_batch(3, type=Organisation.TYPE_PROVIDER)
    OrganisationFactory.create_batch(2, type=Organisation.TYPE_USER)
    # Graphene converts choices to uppercase
    # https://github.com/graphql-python/graphene-django/issues/280
    # so that's why we need to convert them to uppercase here:
    executed = api_client.execute(
        ORGANISATIONS_QUERY, variables={"type": Organisation.TYPE_PROVIDER.upper()}
    )
    snapshot.assert_match(executed)
    executed = api_client.execute(
        ORGANISATIONS_QUERY, variables={"type": Organisation.TYPE_USER.upper()}
    )
    snapshot.assert_match(executed)


def test_organisation_query(snapshot, api_client, organisation):
    executed = api_client.execute(
        ORGANISATION_QUERY,
        variables={"id": to_global_id("OrganisationNode", organisation.id)},
    )
    snapshot.assert_match(executed)


def test_organisation_persons_should_not_be_publicly_readable(
    api_client, staff_api_client, organisation
):
    PERSONS_COUNT = 3
    PersonFactory.create_batch(PERSONS_COUNT, organisations=[organisation])
    variables = {"id": to_global_id("OrganisationNode", organisation.id)}
    anonym_executed = api_client.execute(
        ORGANISATION_QUERY,
        variables=variables,
    )
    assert len(anonym_executed["data"]["organisation"]["persons"]["edges"]) == 0
    staff_executed = staff_api_client.execute(ORGANISATION_QUERY, variables=variables)
    assert (
        len(staff_executed["data"]["organisation"]["persons"]["edges"]) == PERSONS_COUNT
    )


def test_organisation_deactivated_persons_should_not_be_listed(
    staff_api_client, person
):
    organisation = person.organisations.first()
    p_event = PalvelutarjotinEventFactory(organisation=organisation)
    deactivated_person = PersonFactory(
        user__is_active=False, organisations=[organisation]
    )
    study_group_person = EnrolmentFactory(
        occurrence__p_event=p_event
    ).study_group.person
    study_group_person.user = None
    study_group_person.organisations.add(organisation)
    study_group_person.save()

    org_persons = Person.objects.filter(organisations=organisation)
    assert org_persons.count() == 3
    assert all(
        (p in org_persons) for p in [person, deactivated_person, study_group_person]
    )

    executed = staff_api_client.execute(
        ORGANISATION_QUERY,
        variables={"id": to_global_id("OrganisationNode", organisation.id)},
    )
    assert len(executed["data"]["organisation"]["persons"]["edges"]) == 2
    # deactivated person is not listed
    assert to_global_id("PersonNode", deactivated_person.id) not in (
        e["node"]["id"] for e in executed["data"]["organisation"]["persons"]["edges"]
    )
    # active person and study group person are listed
    assert all(
        (
            person_id
            in (
                e["node"]["id"]
                for e in executed["data"]["organisation"]["persons"]["edges"]
            )
        )
        for person_id in [
            to_global_id("PersonNode", person.id),
            to_global_id("PersonNode", study_group_person.id),
        ]
    )


def test_my_profile_query_unauthenticated(snapshot, api_client, organisation):
    executed = api_client.execute(MY_PROFILE_QUERY)
    assert_permission_denied(executed)


def test_my_profile_query(snapshot, person_api_client, organisation, staff_api_client):
    organisation.persons.add(staff_api_client.user.person)
    organisation.persons.add(person_api_client.user.person)
    executed = person_api_client.execute(MY_PROFILE_QUERY)
    snapshot.assert_match(executed)
    executed = staff_api_client.execute(MY_PROFILE_QUERY)
    snapshot.assert_match(executed)


def test_my_profile_query_persons_large_max_limit(staff_api_client, organisation):
    persons = PersonFactory.create_batch(size=300, organisations=[organisation]) + [
        staff_api_client.user.person
    ]
    organisation.persons.add(*persons)
    executed = staff_api_client.execute(MY_PROFILE_QUERY_WITH_ORGANISATIONS_PERSONS)
    organisation_edges = executed["data"]["myProfile"]["organisations"]["edges"]
    assert len(organisation_edges) == 1
    assert len(organisation_edges[0]["node"]["persons"]["edges"]) == 301


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


def test_create_my_profile_with_place_ids(
    snapshot, user_api_client, person_api_client, organisation
):
    variables = deepcopy(CREATE_MY_PROFILE_VARIABLES)
    variables["input"]["organisations"] = [
        to_global_id("OrganisationNode", organisation.id),
    ]
    variables["input"]["placeIds"] = ["xyz:123", "abc321"]
    executed = user_api_client.execute(CREATE_MY_PROFILE_MUTATION, variables=variables)
    snapshot.assert_match(executed)


def test_create_my_profile_sends_mail_to_admins(
    snapshot,
    user_api_client,
    organisation,
    notification_template_myprofile_creation_fi,
    notification_template_myprofile_creation_en,
):
    UserFactory.create_batch(3, is_admin=True)
    variables = deepcopy(CREATE_MY_PROFILE_VARIABLES)
    variables["input"]["organisations"] = [
        to_global_id("OrganisationNode", organisation.id),
    ]
    user_api_client.execute(CREATE_MY_PROFILE_MUTATION, variables=variables)
    assert len(mail.outbox) == 3


def test_create_profile_with_deleted_organisation(user_api_client, organisation):
    variables = deepcopy(CREATE_MY_PROFILE_VARIABLES)
    variables["input"]["organisations"] = [
        to_global_id("OrganisationNode", organisation.id),
    ]
    organisation.delete()
    executed = user_api_client.execute(CREATE_MY_PROFILE_MUTATION, variables=variables)
    assert_match_error_code(executed, OBJECT_DOES_NOT_EXIST_ERROR)


def test_update_my_profile(snapshot, person_api_client):
    variables = deepcopy(UPDATE_MY_PROFILE_VARIABLES)
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


@pytest.mark.parametrize(
    "email, is_valid",
    [
        ("firstlast@example.com", True),
        ("INVALID_EMAIL", False),
        ("", False),
        (None, False),
    ],
)
def test_update_person_mutation(
    snapshot, superuser_api_client, person, email, is_valid
):
    variables = deepcopy(UPDATE_PERSON_VARIABLES)
    variables["input"]["id"] = to_global_id("PersonNode", person.id)
    variables["input"]["emailAddress"] = email
    executed = superuser_api_client.execute(UPDATE_PERSON_MUTATION, variables=variables)
    if is_valid:
        snapshot.assert_match(executed)
    else:
        assert_match_error_code(executed, INVALID_EMAIL_FORMAT_ERROR)


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


def test_add_organisation_without_publisher_id(superuser_api_client):
    variables = deepcopy(ADD_ORGANISATION_VARIABLES)
    del variables["input"]["publisherId"]
    assert "publisherId" not in variables["input"]
    executed = superuser_api_client.execute(
        ADD_ORGANISATION_MUTATION, variables=variables
    )
    assert executed.get("errors")
    assert executed["errors"][0]["extensions"]["code"] == "GENERAL_ERROR"
    assert (
        "Field 'publisherId' of required type 'String!' was not provided."
        in executed["errors"][0]["message"]
    )


def test_add_organisation_with_null_publisher_id(superuser_api_client):
    variables = deepcopy(ADD_ORGANISATION_VARIABLES)
    variables["input"]["publisherId"] = None
    executed = superuser_api_client.execute(
        ADD_ORGANISATION_MUTATION, variables=variables
    )
    assert executed.get("errors")
    assert executed["errors"][0]["extensions"]["code"] == "GENERAL_ERROR"
    assert (
        "Variable '$input' got invalid value None at 'input.publisherId'; "
        + "Expected non-nullable type 'String!' not to be None."
    ) in executed["errors"][0]["message"]


@pytest.mark.parametrize("publisher_id", ["", " ", " " * 10])
def test_add_organisation_with_empty_or_whitespace_only_publisher_id(
    superuser_api_client, publisher_id
):
    variables = deepcopy(ADD_ORGANISATION_VARIABLES)
    variables["input"]["publisherId"] = publisher_id
    executed = superuser_api_client.execute(
        ADD_ORGANISATION_MUTATION, variables=variables
    )
    assert executed.get("errors")
    assert (
        executed["errors"][0]["extensions"]["code"]
        == "MISSING_MANDATORY_INFORMATION_ERROR"
    )
    assert executed["errors"][0]["message"] == "Missing/invalid publisher_id"


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


def test_update_organisation_without_publisher_id(superuser_api_client, organisation):
    variables = deepcopy(UPDATE_ORGANISATION_VARIABLES)
    variables["input"]["id"] = to_global_id("OrganisationNode", organisation.id)
    del variables["input"]["publisherId"]
    assert "publisherId" not in variables["input"]
    assert organisation.publisher_id
    executed = superuser_api_client.execute(
        UPDATE_ORGANISATION_MUTATION, variables=variables
    )
    assert (
        executed["data"]["updateOrganisation"]["organisation"]["publisherId"]
        == organisation.publisher_id
    )


@pytest.mark.parametrize("publisher_id", [None, "", " ", " " * 10])
def test_update_organisation_with_null_empty_or_whitespace_only_publisher_id(
    superuser_api_client, organisation, publisher_id
):
    variables = deepcopy(UPDATE_ORGANISATION_VARIABLES)
    variables["input"]["id"] = to_global_id("OrganisationNode", organisation.id)
    variables["input"]["publisherId"] = publisher_id
    executed = superuser_api_client.execute(
        UPDATE_ORGANISATION_MUTATION, variables=variables
    )
    assert executed.get("errors")
    assert (
        executed["errors"][0]["extensions"]["code"]
        == "MISSING_MANDATORY_INFORMATION_ERROR"
    )
    assert executed["errors"][0]["message"] == "Missing/invalid publisher_id"


PERSON_QUEUED_ENROLMENTS_QUERY = """
query Person($id:ID!){
  person(id: $id){
    name
    eventqueueenrolmentSet {
      edges {
        node {
          studyGroup {
            groupName
          }
        }
      }
    }
  }
}
"""


def test_person_queued_enrolments(snapshot, staff_api_client, person, organisation):
    person = staff_api_client.user.person
    person.organisations.add(organisation)
    p_event = PalvelutarjotinEventFactory(organisation=organisation)
    EventQueueEnrolmentFactory.create_batch(5, person=person, p_event=p_event)
    assert person.eventqueueenrolment_set.all().count() == 5
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(
        PERSON_QUEUED_ENROLMENTS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert len(executed["data"]["person"]["eventqueueenrolmentSet"]["edges"]) == 5
    snapshot.assert_match(executed)


def test_person_queued_enrolments_unauthorized(
    api_client, staff_api_client, person, organisation
):
    EventQueueEnrolmentFactory.create_batch(5, person=person)
    assert person.eventqueueenrolment_set.all().count() == 5

    # with public API
    executed = api_client.execute(
        PERSON_QUEUED_ENROLMENTS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert executed["data"]["person"] is None

    # with staff API without organisation
    assert staff_api_client.user.person.organisations.count() == 0
    executed = staff_api_client.execute(
        PERSON_QUEUED_ENROLMENTS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert executed["data"]["person"]["eventqueueenrolmentSet"]["edges"] == []

    # with staff API with other organisation
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(
        PERSON_QUEUED_ENROLMENTS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert executed["data"]["person"]["eventqueueenrolmentSet"]["edges"] == []


PERSON_ENROLMENTS_QUERY = """
query Person($id:ID!){
  person(id: $id){
    name
    enrolmentSet {
      edges {
        node {
          studyGroup {
            groupName
          }
        }
      }
    }
  }
}
"""


def test_person_enrolments(
    snapshot, mock_get_event_data, staff_api_client, organisation
):
    person = staff_api_client.user.person
    person.organisations.add(organisation)
    p_event = PalvelutarjotinEventFactory(organisation=organisation)
    EnrolmentFactory.create_batch(
        5, study_group__person=person, person=person, occurrence__p_event=p_event
    )
    assert person.enrolment_set.all().count() == 5
    executed = staff_api_client.execute(
        PERSON_ENROLMENTS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert len(executed["data"]["person"]["enrolmentSet"]["edges"]) == 5
    snapshot.assert_match(executed)


def test_person_enrolments_unauthorized(
    mock_get_event_data, api_client, staff_api_client, person, organisation
):
    EnrolmentFactory.create_batch(5, person=person)
    assert person.enrolment_set.count() == 5

    # with public API
    executed = api_client.execute(
        PERSON_ENROLMENTS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert executed["data"]["person"] is None

    # with staff API without organisations
    assert staff_api_client.user.person.organisations.count() == 0
    executed = staff_api_client.execute(
        PERSON_ENROLMENTS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert executed["data"]["person"]["enrolmentSet"]["edges"] == []

    # with staff API with other organisation
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(
        PERSON_ENROLMENTS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert executed["data"]["person"]["enrolmentSet"]["edges"] == []


PERSON_STUDY_GROUPS_QUERY = """
query Person($id:ID!){
  person(id: $id){
    name
    studygroupSet {
      edges {
        node {
          groupName
        }
      }
    }
  }
}
"""


def test_person_study_groups(
    snapshot, mock_get_event_data, staff_api_client, organisation
):
    person = staff_api_client.user.person
    person.organisations.add(organisation)
    p_event = PalvelutarjotinEventFactory(organisation=organisation)
    EnrolmentFactory.create_batch(
        5, study_group__person=person, person=person, occurrence__p_event=p_event
    )
    assert person.studygroup_set.count() == 5
    executed = staff_api_client.execute(
        PERSON_STUDY_GROUPS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert len(executed["data"]["person"]["studygroupSet"]["edges"]) == 5
    snapshot.assert_match(executed)


def test_person_study_groups_unauthorized(
    mock_get_event_data, api_client, staff_api_client, person, organisation
):
    EnrolmentFactory.create_batch(5, study_group__person=person, person=person)
    assert person.studygroup_set.count() == 5

    # with public API
    executed = api_client.execute(
        PERSON_STUDY_GROUPS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert executed["data"]["person"] is None

    # with staff API without organisations
    assert staff_api_client.user.person.organisations.count() == 0
    executed = staff_api_client.execute(
        PERSON_STUDY_GROUPS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert executed["data"]["person"]["studygroupSet"]["edges"] == []

    # with staff API with other organisation
    staff_api_client.user.person.organisations.add(organisation)
    executed = staff_api_client.execute(
        PERSON_STUDY_GROUPS_QUERY,
        variables={"id": to_global_id("PersonNode", person.id)},
    )
    assert executed["data"]["person"]["studygroupSet"]["edges"] == []
