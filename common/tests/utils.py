from django.core import mail

from palvelutarjotin.consts import PERMISSION_DENIED_ERROR


def assert_permission_denied(response):
    assert_match_error_code(response, PERMISSION_DENIED_ERROR)


def assert_mails_match_snapshot(snapshot):
    snapshot.assert_match(
        [f"{m.from_email}|{m.to}|{m.subject}|{m.body}" for m in mail.outbox]
    )


def assert_match_error_code(response, error_code):
    assert response["errors"][0].get("extensions").get("code") == error_code
