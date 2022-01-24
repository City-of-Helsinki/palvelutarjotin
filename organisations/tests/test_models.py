import pytest
from django.contrib.auth import get_user_model
from organisations.factories import (
    OrganisationFactory,
    OrganisationProposalFactory,
    PersonFactory,
    UserFactory,
)
from organisations.models import Organisation, OrganisationProposal, Person

User = get_user_model()


@pytest.mark.django_db
def test_person_creation():
    person = PersonFactory()
    assert User.objects.count() == 1
    assert Person.objects.count() == 1
    assert person.__str__() == f"{person.name} ({person.user.username})"


@pytest.mark.django_db
def test_organisation_creation():
    OrganisationFactory()
    assert Organisation.objects.count() == 1


@pytest.mark.django_db
def test_organisation_proposal_creation():
    person = PersonFactory()
    organisation_proposal = OrganisationProposalFactory(applicant=person)
    assert OrganisationProposal.objects.count() == 1
    assert person.organisationproposal_set.count() == 1
    assert OrganisationProposal.objects.filter(applicant=person).count() == 1
    assert (
        organisation_proposal.__str__()
        == f"{organisation_proposal.id} {organisation_proposal.name}"
    )


@pytest.mark.django_db
def test_membership_creation():
    organisations = OrganisationFactory.create_batch(3)
    person = PersonFactory(organisations=organisations)
    assert person.organisations.count() == 3
    assert Organisation.objects.count() == 3
    assert Person.objects.count() == 1


@pytest.mark.django_db
def test_own_places():
    place1 = "abc:123"
    place2 = "xyz:321"
    place3 = "jkl:999"
    PersonFactory(name="person without places")
    person1 = PersonFactory(name="person1", place_ids=[place1, place2])
    person2 = PersonFactory(name="person2", place_ids=[place1])
    person3 = PersonFactory(name="person3", place_ids=[place3, place2])
    assert person1.place_ids == [place1, place2]
    assert Person.objects.all().count() == 4
    assert list(
        Person.objects.filter(place_ids__contains=[place1]).order_by("name")
    ) == [person1, person2]
    assert list(
        Person.objects.filter(place_ids__contains=[place2]).order_by("name")
    ) == [person1, person3]
    assert list(Person.objects.filter(place_ids__contains=[place1, place2])) == [
        person1
    ]
    assert (
        Person.objects.filter(place_ids__contains=[place1, place2, place3]).count() == 0
    )

    assert list(
        Person.objects.filter(place_ids__contained_by=[place1, place2]).order_by("name")
    ) == [person1, person2]
    assert list(
        Person.objects.exclude(place_ids=[])
        .filter(place_ids__contained_by=[place1, place2])
        .order_by("name")
    ) == [person1, person2]
    assert (
        Person.objects.filter(place_ids__contained_by=[place1, place2, place3]).count()
        == 3
    )

    assert list(
        Person.objects.filter(place_ids__overlap=[place1]).order_by("name")
    ) == [person1, person2]
    assert list(
        Person.objects.filter(place_ids__overlap=[place1, place3]).order_by("name")
    ) == [person1, person2, person3]

    assert list(Person.objects.filter(place_ids__len=1)) == [person2]


@pytest.mark.django_db
def test_user_str():
    user_with_name_and_email = UserFactory.create(
        first_name="first_name",
        last_name="last_name",
        username="user_with_name_and_email",
        email="user_with_name_and_email@email.com",
    )
    assert user_with_name_and_email.__str__() == "%s %s (%s)" % (
        user_with_name_and_email.last_name,
        user_with_name_and_email.first_name,
        user_with_name_and_email.email,
    )

    user_without_full_name_but_email = UserFactory.create(
        first_name="",
        last_name="last_name",
        username="user_without_full_name_but_email",
        email="user_without_full_name_but_email@email.com",
    )
    assert (
        user_without_full_name_but_email.__str__()
        == user_without_full_name_but_email.email
    )

    user_without_name_and_email = UserFactory.create(
        first_name="",
        last_name="last_name",
        username="user_without_name_and_email",
        email="",
    )
    assert user_without_name_and_email.__str__() == user_without_name_and_email.username
