import pytest
from django.core import mail
from organisations.factories import (
    OrganisationFactory,
    OrganisationProposalFactory,
    PersonFactory,
    UserFactory,
)

from common.tests.utils import assert_mails_match_snapshot


@pytest.mark.django_db
def test_myprofile_creation_email(
    snapshot,
    settings,
    notification_template_myprofile_creation_fi,
    notification_template_myprofile_creation_en,
):
    settings.SITE_URL = "https://test-domain"
    person = PersonFactory(id=123)
    OrganisationProposalFactory.create_batch(2, applicant=person)
    UserFactory.create_batch(2, is_admin=True)
    person.notify_myprofile_creation(custom_message="custom message")
    assert len(mail.outbox) == 2
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_myprofile_accepted_email(
    snapshot,
    notification_template_myprofile_accepted_fi,
    notification_template_myprofile_accepted_en,
):
    organisations = OrganisationFactory.create_batch(2)
    person = PersonFactory(organisations=organisations)
    person.notify_myprofile_accepted(custom_message="custom message")
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)
