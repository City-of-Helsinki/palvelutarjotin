import json


class MockResponse:
    def __init__(self, json_data, status_code):
        self.text = json.dumps(json_data)
        self.status_code = status_code

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        return None
