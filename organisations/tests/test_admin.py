import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from organisations.admin import UserAdmin
from organisations.factories import (
    OrganisationProposalFactory,
    PersonFactory,
    UserFactory,
)


@pytest.mark.django_db
def test_user_admin_has_person():
    user_admin = UserAdmin(model=get_user_model(), admin_site=AdminSite())
    person = PersonFactory()
    user = UserFactory()
    assert user_admin.has_person(person.user) is True
    assert user_admin.has_person(user) is False


@pytest.mark.django_db
def test_user_admin_organisation_proposals():
    user_admin = UserAdmin(model=get_user_model(), admin_site=AdminSite())
    person = PersonFactory()
    OrganisationProposalFactory(applicant=person, name="Org1")
    OrganisationProposalFactory(applicant=person, name="Org2")
    assert user_admin.organisation_proposals(person.user) == "Org1, Org2"


@pytest.mark.django_db
def test_user_admin_get_readonly_Fields():
    user_admin = UserAdmin(model=get_user_model(), admin_site=AdminSite())
    readonly_fields = (
        "username",
        "is_superuser",
        "groups",
        "user_permissions",
    )
    superuser = UserFactory(is_superuser=True)
    user = UserFactory(is_staff=True)
    superuser_fields = user_admin.get_readonly_fields(MockRequest(user=superuser))
    user_fields = user_admin.get_readonly_fields(MockRequest(user=user))
    assert all(i in (set(superuser_fields) ^ set(user_fields)) for i in readonly_fields)


class MockRequest(object):
    def __init__(self, user=None):
        self.user = user
