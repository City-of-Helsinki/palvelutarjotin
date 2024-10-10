from unittest import mock

import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from organisations.admin import PersonAdmin, PersonAdminForm, UserAdmin, UserAdminForm
from organisations.factories import (
    OrganisationFactory,
    OrganisationProposalFactory,
    PersonFactory,
    UserFactory,
)
from organisations.models import Person


@pytest.mark.usefixtures("notification_template_myprofile_accepted_fi")
class UserAdminViewTest(TestCase):
    def setUp(self):
        site = AdminSite()
        self.admin = UserAdmin(model=get_user_model(), admin_site=site)

    @pytest.mark.django_db
    def test_user_admin_has_person(self):
        person = PersonFactory()
        user = UserFactory()
        assert self.admin.has_person(person.user) is True
        assert self.admin.has_person(user) is False

    @pytest.mark.django_db
    def test_user_admin_organisation_proposals(self):
        person = PersonFactory()
        OrganisationProposalFactory(applicant=person, name="Org1")
        OrganisationProposalFactory(applicant=person, name="Org2")
        assert self.admin.organisation_proposals(person.user) == "Org1, Org2"

    @pytest.mark.django_db
    def test_user_admin_get_readonly_fields(self):
        readonly_fields = (
            "username",
            "is_superuser",
            "groups",
            "user_permissions",
        )
        superuser = UserFactory(is_superuser=True)
        user = UserFactory(is_staff=True)
        superuser_fields = self.admin.get_readonly_fields(MockRequest(user=superuser))
        user_fields = self.admin.get_readonly_fields(MockRequest(user=user))
        assert all(
            i in (set(superuser_fields) ^ set(user_fields)) for i in readonly_fields
        )

    @pytest.mark.django_db
    def test_user_admin_has_organisations_changed(self):
        organisations = OrganisationFactory.create_batch(2)
        person = PersonFactory(organisations=organisations)
        user_admin_form = UserAdminForm(person.user.__dict__)
        user_admin_form.is_valid()  # Call is_valid to populate cleaned_data
        user_admin_form.instance = person.user
        user_admin_form.cleaned_data["organisations"] = organisations
        assert self.admin._has_organisations_changed(person, user_admin_form) is False
        user_admin_form.cleaned_data["organisations"] = [organisations[0]]
        assert self.admin._has_organisations_changed(person, user_admin_form) is True
        assert self.admin._has_organisations_changed(None, user_admin_form) is False

    @pytest.mark.django_db
    def test_user_admin_has_is_staff_changed(self):
        user_admin_form = UserAdminForm()
        assert self.admin._has_is_staff_changed(user_admin_form) is False
        user_admin_form.changed_data = ["is_staff"]
        assert self.admin._has_is_staff_changed(user_admin_form) is True

    @pytest.mark.django_db
    @mock.patch("django.contrib.messages.add_message")
    def test_user_admin_notify_user_of_account_activation(self, add_message):
        person = PersonFactory()
        user = person.user
        superuser = UserFactory(is_superuser=True)
        user_admin_form = UserAdminForm(user.__dict__)
        user_admin_form.instance = user
        request = MockRequest(user=superuser)
        self.admin._notify_user_of_account_activation(request, user_admin_form)
        assert len(mail.outbox) == 1
        assert add_message.called

    @pytest.mark.django_db
    @mock.patch("django.contrib.messages.add_message")
    def test_save_form(self, add_message):
        person = PersonFactory()
        user = person.user
        superuser = UserFactory(is_superuser=True)
        """
        Test without organisation and is_staff changes -
        Then the email should not be sent.
        """
        user_admin_form = UserAdminForm(user.__dict__, instance=user)
        assert user_admin_form.is_valid()  # Call is_valid to populate cleaned_data
        request = MockRequest(user=superuser)
        assert self.admin.save_form(request, user_admin_form, True) == user
        assert add_message.called is False
        """
        Test with organisation and is_staff changes - Then the email should be sent.
        """
        organisations = OrganisationFactory.create_batch(2)
        user_admin_form = UserAdminForm(
            {**user.__dict__, **{"is_staff": True, "organisations": organisations}},
            instance=user,
        )
        assert user_admin_form.is_valid()  # Call is_valid to populate cleaned_data
        assert self.admin.save_form(request, user_admin_form, True) == user
        assert add_message.called
        assert len(mail.outbox) == 1


class PersonAdminViewTest(TestCase):
    def setUp(self):
        site = AdminSite()
        self.admin = PersonAdmin(model=Person, admin_site=site)

    def test_person_admin_form_user(self):
        UserFactory.create_batch(5)
        PersonFactory.create_batch(5)
        person = PersonFactory()
        assert get_user_model().objects.all().count() == 11
        assert person.user is not None

        person_admin_form = PersonAdminForm()
        user_field = person_admin_form.fields["user"]
        assert user_field.initial is None
        assert user_field.queryset.count() == 5

        person_admin_form = PersonAdminForm(person.__dict__, instance=person)
        user_field = person_admin_form.fields["user"]
        assert user_field.initial == person.user
        assert user_field.queryset.count() == 6


class MockRequest(object):
    def __init__(self, user=None):
        self.user = user
