import pytest
from django.test import Client


@pytest.fixture
def client():
    """Pytest fixture to provide a Django test client."""
    return Client()


def test_csp_header_present(client):
    """Test that the Content-Security-Policy header is present."""
    response = client.get("/")
    assert "Content-Security-Policy" in response.headers


def test_csp_header_content(client):
    """Test that the CSP header has the expected directives."""
    response = client.get("/")
    csp_header = response.headers["Content-Security-Policy"]
    # Adjust assertions based on your actual CSP configuration
    assert "default-src 'self'" in csp_header
    # The style-src needs 'unsafe-inline', because the django-helusers
    # adds some inline styles when it overrides
    # the default django admin base site template.
    assert "style-src 'self' 'unsafe-inline'" in csp_header
