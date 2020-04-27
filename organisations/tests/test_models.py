import pytest
from django.contrib.auth import get_user_model
from organisations.factories import OrganisationFactory, PersonFactory
from organisations.models import Organisation, Person

User = get_user_model()


@pytest.mark.django_db
def test_person_creation():
    PersonFactory()
    assert User.objects.count() == 1
    assert Person.objects.count() == 1


@pytest.mark.django_db
def test_organisation_creation():
    OrganisationFactory()

    assert Organisation.objects.count() == 1


@pytest.mark.django_db
def test_membership_creation():
    organisations = OrganisationFactory.create_batch(3)
    person = PersonFactory(organisations=organisations)
    assert person.organisations.count() == 3
    assert Organisation.objects.count() == 3
    assert Person.objects.count() == 1
