import pytest
from django.test import Client


@pytest.mark.django_db(transaction=True)
def test_cors_allowed_origin(settings, live_server, client: Client):
    settings.CORS_ALLOWED_ORIGINS = [
        live_server.url,
    ]
    settings.CORS_ORIGIN_ALLOW_ALL = False
    response = client.get("/admin/login/", HTTP_ORIGIN=live_server.url)
    assert response.status_code == 200
    assert response["Access-Control-Allow-Origin"] == live_server.url


@pytest.mark.django_db(transaction=True)
def test_cors_disallowed_origin(settings, live_server, client: Client):
    settings.CORS_ALLOWED_ORIGINS = [live_server.url]
    settings.CORS_ORIGIN_ALLOW_ALL = False
    response = client.get("/admin/login/", HTTP_ORIGIN="http://malicious.com")
    assert response.status_code == 200  # The request still succeeds...
    assert (
        "Access-Control-Allow-Origin" not in response.headers
    )  # ...but CORS headers are not present
