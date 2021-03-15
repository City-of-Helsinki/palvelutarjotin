from django.core import mail
from django_ilmoitin.models import NotificationTemplate
from parler.utils.context import switch_language

from palvelutarjotin.consts import PERMISSION_DENIED_ERROR


def assert_permission_denied(response):
    assert_match_error_code(response, PERMISSION_DENIED_ERROR)


def assert_mails_match_snapshot(snapshot):
    snapshot.assert_match(
        [f"{m.from_email}|{m.to}|{m.subject}|{m.body}" for m in mail.outbox]
    )


def assert_match_error_code(response, error_code):
    assert response["errors"][0].get("extensions").get("code") == error_code


def create_notification_template_in_language(
    notification_template_id, language, **translations
):
    try:
        template = NotificationTemplate.objects.get(type=notification_template_id)
    except NotificationTemplate.DoesNotExist:
        template = NotificationTemplate(type=notification_template_id)
    with switch_language(template, language):
        for field, value in translations.items():
            setattr(template, field, value)
            template.save()

    return template


def mocked_json_response(data=None, status_code=200, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(data, status_code)
