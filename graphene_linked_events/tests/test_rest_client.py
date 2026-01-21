from unittest.mock import Mock, patch

from graphene_linked_events.rest_client import LinkedEventsApiClient


class TestLinkedEventsApiClientTimeout:
    """Tests for LinkedEventsApiClient timeout configuration."""

    def get_base_config(self, timeout=None):
        """Return a base config dict, optionally with timeout."""
        config = {
            "ROOT": "https://api.example.com/v1/",
            "API_KEY": "test-api-key",
            "DATA_SOURCE": "test-source",
        }
        if timeout is not None:
            config["TIMEOUT"] = timeout
        return config

    def test_timeout_from_config(self):
        """Client should use timeout value from config."""
        config = self.get_base_config(timeout=90)
        client = LinkedEventsApiClient(config)
        assert client.timeout == 90

    def test_timeout_default_when_not_in_config(self):
        """Client should use default timeout (60s) when not in config."""
        config = self.get_base_config()
        client = LinkedEventsApiClient(config)
        assert client.timeout == 60

    def test_timeout_zero_is_allowed(self):
        """Client should accept zero timeout from config."""
        config = self.get_base_config(timeout=0)
        client = LinkedEventsApiClient(config)
        assert client.timeout == 0

    @patch("graphene_linked_events.rest_client.requests.request")
    def test_retrieve_uses_configured_timeout(self, mock_request):
        """Retrieve method should pass configured timeout to requests."""
        mock_request.return_value = Mock(status_code=200)
        config = self.get_base_config(timeout=45)
        client = LinkedEventsApiClient(config)

        client.retrieve("event", "123")

        mock_request.assert_called_once()
        assert mock_request.call_args.kwargs["timeout"] == 45

    @patch("graphene_linked_events.rest_client.requests.request")
    def test_list_uses_configured_timeout(self, mock_request):
        """List method should pass configured timeout to requests."""
        mock_request.return_value = Mock(status_code=200)
        config = self.get_base_config(timeout=45)
        client = LinkedEventsApiClient(config)

        client.list("event")

        mock_request.assert_called_once()
        assert mock_request.call_args.kwargs["timeout"] == 45

    @patch("graphene_linked_events.rest_client.requests.request")
    def test_create_uses_configured_timeout(self, mock_request):
        """Create method should pass configured timeout to requests."""
        mock_request.return_value = Mock(status_code=201)
        config = self.get_base_config(timeout=45)
        client = LinkedEventsApiClient(config)

        client.create("event", '{"name": "Test"}')

        mock_request.assert_called_once()
        assert mock_request.call_args.kwargs["timeout"] == 45

    @patch("graphene_linked_events.rest_client.requests.request")
    def test_update_uses_configured_timeout(self, mock_request):
        """Update method should pass configured timeout to requests."""
        mock_request.return_value = Mock(status_code=200)
        config = self.get_base_config(timeout=45)
        client = LinkedEventsApiClient(config)

        client.update("event", "123", '{"name": "Updated"}')

        mock_request.assert_called_once()
        assert mock_request.call_args.kwargs["timeout"] == 45

    @patch("graphene_linked_events.rest_client.requests.request")
    def test_delete_uses_configured_timeout(self, mock_request):
        """Delete method should pass configured timeout to requests."""
        mock_request.return_value = Mock(status_code=204)
        config = self.get_base_config(timeout=45)
        client = LinkedEventsApiClient(config)

        client.delete("event", "123")

        mock_request.assert_called_once()
        assert mock_request.call_args.kwargs["timeout"] == 45

    @patch("graphene_linked_events.rest_client.requests.request")
    def test_search_uses_configured_timeout(self, mock_request):
        """Search method should pass configured timeout to requests."""
        mock_request.return_value = Mock(status_code=200)
        config = self.get_base_config(timeout=45)
        client = LinkedEventsApiClient(config)

        # Mock get_actions to return a valid search action
        # (search is a special action that doesn't use resource param)
        with patch.object(
            client,
            "get_actions",
            return_value={"search": {"method": "GET", "url": client.root + "search/"}},
        ):
            client.search({"q": "test"})

        mock_request.assert_called_once()
        assert mock_request.call_args.kwargs["timeout"] == 45

    @patch("graphene_linked_events.rest_client.requests.request")
    def test_upload_uses_configured_timeout(self, mock_request):
        """Upload method should pass configured timeout to requests."""
        mock_request.return_value = Mock(status_code=201)
        config = self.get_base_config(timeout=45)
        client = LinkedEventsApiClient(config)

        client.upload("image", {"name": "test"}, {"file": b"data"})

        mock_request.assert_called_once()
        assert mock_request.call_args.kwargs["timeout"] == 45


class TestLinkedEventsApiClientConfig:
    """Tests for LinkedEventsApiClient configuration."""

    def test_client_stores_root_url(self):
        """Client should store root URL from config."""
        config = {
            "ROOT": "https://api.example.com/v1/",
            "API_KEY": "test-key",
            "DATA_SOURCE": "test-source",
        }
        client = LinkedEventsApiClient(config)
        assert client.root == "https://api.example.com/v1/"

    def test_client_stores_api_key(self):
        """Client should store API key from config."""
        config = {
            "ROOT": "https://api.example.com/v1/",
            "API_KEY": "my-secret-key",
            "DATA_SOURCE": "test-source",
        }
        client = LinkedEventsApiClient(config)
        assert client.api_key == "my-secret-key"

    def test_client_stores_data_source(self):
        """Client should store data source from config."""
        config = {
            "ROOT": "https://api.example.com/v1/",
            "API_KEY": "test-key",
            "DATA_SOURCE": "palvelutarjotin",
        }
        client = LinkedEventsApiClient(config)
        assert client.data_source == "palvelutarjotin"
