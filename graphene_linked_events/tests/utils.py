import json

from requests.exceptions import HTTPError


class MockResponse:
    status_code = None
    exception = None
    text = None

    def __init__(self, json_data, status_code, exception=None):
        self.text = json.dumps(json_data)
        self.status_code = status_code
        self.exception = exception

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        if not self.exception and self.status_code != 200:
            raise HTTPError("A mocked generic HTTP error")

        if self.exception:
            raise self.exception
