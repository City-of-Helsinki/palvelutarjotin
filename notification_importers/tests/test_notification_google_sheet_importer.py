import pytest
import responses
from django.conf import settings
from django_ilmoitin.models import NotificationTemplate
from occurrences.consts import NotificationTemplate as NotificationType

from common.tests.utils import create_notification_template_in_language

from ..notification_importer import NotificationGoogleSheetImporter
from .utils import serialize_notifications

LANGUAGES = ("fi", "sv", "en")

MOCK_CSV = """,SUBJECT | FI,SUBJECT | SV,SUBJECT | EN,BODY_TEXT | FI,BODY_TEXT | SV,BODY_TEXT | EN\r\n
enrolment_approved,enrolment_approved fi updated subject,enrolment_approved sv updated subject,enrolment_approved en updated subject,enrolment_approved fi updated body_text,enrolment_approved sv updated body_text,enrolment_approved en updated body_text\r\n
occurrence_enrolment,occurrence_enrolment fi updated subject,occurrence_enrolment sv updated subject,occurrence_enrolment en updated subject,occurrence_enrolment fi updated body_text,occurrence_enrolment sv updated body_text,occurrence_enrolment en updated body_text"""  # noqa


@pytest.fixture(autouse=True)
def setup(settings, mocked_responses):
    settings.NOTIFICATIONS_SHEET_ID = "mock-sheet-id"
    settings.PARLER_SUPPORTED_LANGUAGE_CODES = LANGUAGES
    mocked_responses.add(
        responses.GET,
        "https://docs.google.com/spreadsheets/d/mock-sheet-id/export?format=csv",
        body=MOCK_CSV,
        status=200,
        content_type="application/json",
    )


@pytest.fixture
def enrolment_approved_notification():
    for language in LANGUAGES:
        create_notification_template_in_language(
            NotificationType.ENROLMENT_APPROVED,
            language,
            subject=f"{NotificationType.ENROLMENT_APPROVED} "
            f"{language} original subject",
            body_text=f"{NotificationType.ENROLMENT_APPROVED} "
            f"{language} original body_text",
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
            body_text=f"{NotificationType.OCCURRENCE_ENROLMENT} "
            f"{language} original body_text",
        )
    return NotificationTemplate.objects.get(type=NotificationType.OCCURRENCE_ENROLMENT)


@pytest.mark.django_db
def test_create_non_existing_and_update_existing_notifications(
    enrolment_approved_notification, occurrence_enrolment_notification, snapshot
):
    (
        num_of_created,
        num_of_updated,
    ) = (
        NotificationGoogleSheetImporter().create_missing_and_update_existing_notifications()  # noqa: E501
    )
    assert num_of_created == 0
    assert num_of_updated == 2
    snapshot.assert_match(serialize_notifications(NotificationTemplate.objects.all()))


@pytest.mark.django_db
def test_create_non_existing_notifications(enrolment_approved_notification, snapshot):
    NotificationGoogleSheetImporter().create_missing_notifications()
    snapshot.assert_match(serialize_notifications(NotificationTemplate.objects.all()))


@pytest.mark.django_db
def test_update_notifications(enrolment_approved_notification, snapshot):
    NotificationGoogleSheetImporter().update_notifications(
        [enrolment_approved_notification]
    )
    snapshot.assert_match(serialize_notifications(NotificationTemplate.objects.all()))


@pytest.mark.django_db
def test_is_notification_in_sync(enrolment_approved_notification):
    importer = NotificationGoogleSheetImporter()

    assert not importer.is_notification_in_sync(enrolment_approved_notification)

    # set the notification to match the csv
    for language in settings.PARLER_SUPPORTED_LANGUAGE_CODES:
        translation_obj, _ = enrolment_approved_notification.translations.get_or_create(
            language_code=language
        )
        for field in ("subject", "body_text", "body_html"):
            setattr(
                translation_obj,
                field,
                getattr(translation_obj, field).replace("original", "updated"),
            )
        translation_obj.save()

    assert importer.is_notification_in_sync(enrolment_approved_notification)
