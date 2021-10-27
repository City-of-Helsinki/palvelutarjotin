from django.core import mail
from django_ilmoitin.models import NotificationTemplate
from parler.utils.context import switch_language
from requests.exceptions import HTTPError

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
        status_code = None
        json_data = None
        exception = None

        def __init__(self, json_data, status_code, exception=None):
            self.json_data = json_data
            self.status_code = status_code
            self.exception = exception

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if not self.exception and self.status_code != 200:
                raise HTTPError("A mocked generic HTTP error")
            if self.exception:
                raise self.exception

        @property
        def text(self):
            return str(self.json())

    return MockResponse(data, status_code, **kwargs)
