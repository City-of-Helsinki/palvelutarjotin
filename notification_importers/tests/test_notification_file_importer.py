import pytest
from django_ilmoitin.models import NotificationTemplate
from occurrences.consts import NotificationTemplate as NotificationType

from common.tests.utils import create_notification_template_in_language

from ..notification_importer import NotificationFileImporter
from .utils import serialize_notifications

LANGUAGES = ("fi", "sv", "en")


@pytest.fixture(autouse=True)
def setup(settings):
    settings.PARLER_SUPPORTED_LANGUAGE_CODES = LANGUAGES


@pytest.fixture
def enrolment_approved_notification():
    for language in LANGUAGES:
        create_notification_template_in_language(
            NotificationType.ENROLMENT_APPROVED,
            language,
            subject=f"{NotificationType.ENROLMENT_APPROVED} "
            f"{language} original subject",
            body_html=f"{NotificationType.ENROLMENT_APPROVED} "
            f"{language} original body_html",
        )
    return NotificationTemplate.objects.get(type=NotificationType.ENROLMENT_APPROVED)


@pytest.fixture
def occurrence_enrolment_notification():
    for language in ("fi", "en"):
        create_notification_template_in_language(
            NotificationType.OCCURRENCE_ENROLMENT,
            language,
            subject=f"{NotificationType.OCCURRENCE_ENROLMENT} "
            f"{language} original subject",
            body_html=f"{NotificationType.OCCURRENCE_ENROLMENT} "
            f"{language} original body_html",
        )
    return NotificationTemplate.objects.get(type=NotificationType.OCCURRENCE_ENROLMENT)


@pytest.mark.django_db
def test_create_non_existing_and_update_existing_notifications(
    enrolment_approved_notification, occurrence_enrolment_notification, snapshot
):
    (
        num_of_created,
        num_of_updated,
    ) = NotificationFileImporter().create_missing_and_update_existing_notifications()

    assert num_of_created == 7
    assert num_of_updated == 2
    snapshot.assert_match(serialize_notifications(NotificationTemplate.objects.all()))


@pytest.mark.django_db
def test_create_non_existing_notifications(enrolment_approved_notification, snapshot):
    NotificationFileImporter().create_missing_notifications()
    assert "original" in enrolment_approved_notification.subject
    assert "original" in enrolment_approved_notification.body_html
    snapshot.assert_match(serialize_notifications(NotificationTemplate.objects.all()))


@pytest.mark.django_db
def test_update_notifications(enrolment_approved_notification, snapshot):
    NotificationFileImporter().update_notifications([enrolment_approved_notification])
    assert "original" not in enrolment_approved_notification.subject
    assert "original" not in enrolment_approved_notification.body_html
    snapshot.assert_match(serialize_notifications(NotificationTemplate.objects.all()))


@pytest.mark.django_db
def test_is_notification_in_sync(enrolment_approved_notification):
    importer = NotificationFileImporter()

    assert not importer.is_notification_in_sync(enrolment_approved_notification)

    NotificationFileImporter().update_notifications([enrolment_approved_notification])

    assert importer.is_notification_in_sync(enrolment_approved_notification)
