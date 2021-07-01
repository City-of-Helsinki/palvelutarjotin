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
