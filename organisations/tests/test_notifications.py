import pytest
from django.contrib.auth import get_user_model
from django.core import mail

from common.tests.utils import assert_mails_match_snapshot
from organisations.factories import (
    OrganisationFactory,
    OrganisationProposalFactory,
    PersonFactory,
    UserFactory,
)


@pytest.mark.django_db
def test_myprofile_creation_email(
    snapshot,
    settings,
    notification_template_myprofile_creation_fi,
    notification_template_myprofile_creation_en,
):
    settings.SITE_URL = "https://test-domain"
    user = UserFactory(id=123)
    person = PersonFactory(user=user)
    OrganisationProposalFactory.create_batch(2, applicant=person)
    PersonFactory(user=UserFactory(is_admin=True))
    PersonFactory(user=UserFactory(is_admin=True), language="fi")
    PersonFactory(user=UserFactory(is_admin=True), language="en")
    assert get_user_model().objects.filter(is_admin=True).count() == 3

    person.notify_myprofile_creation(custom_message="custom message")
    assert len(mail.outbox) == 3
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
@pytest.mark.parametrize("language", ["fi", "en"])
def test_myprofile_accepted_email(
    language,
    snapshot,
    notification_template_myprofile_accepted_fi,
    notification_template_myprofile_accepted_en,
):
    organisations = OrganisationFactory.create_batch(2)
    person = PersonFactory(organisations=organisations, language=language)
    person.notify_myprofile_accepted(custom_message="custom message")
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)
