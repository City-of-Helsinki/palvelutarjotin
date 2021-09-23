import requests


class LinkedEventsApiClient(object):

    CONNECTION_TIMEOUT = 5

    def __init__(self, config) -> None:
        self.root = config["ROOT"]
        self.api_key = config["API_KEY"]
        super().__init__()

    def get_actions(self, resource=None):
        url = self.root + resource
        return {
            "list": {"method": "GET", "url": url + "/"},
            "create": {"method": "POST", "url": url + "/"},
            "retrieve": {"method": "GET", "url": url + "/{}/"},
            "update": {"method": "PUT", "url": url + "/{}/"},
            "delete": {"method": "DELETE", "url": url + "/{}/"},
            "search": {"method": "GET", "url": self.root + "search/"},
            "upload": {"method": "POST", "url": url + "/"},
        }

    def retrieve(self, resource, id, params=None, is_staff=False):
        actions = self.get_actions(resource)
        formatted_params = self.convert_to_string_param(params)
        if is_staff:
            headers = {"apikey": self.api_key, "Cache-Control": "no-cache"}
            cookies = dict(nocache="meow")
            return requests.request(
                actions["retrieve"]["method"],
                actions["retrieve"]["url"].format(id),
                params=formatted_params,
                headers=headers,
                cookies=cookies,
                timeout=self.CONNECTION_TIMEOUT,
            )
        return requests.request(
            actions["retrieve"]["method"],
            actions["retrieve"]["url"].format(id),
            params=formatted_params,
            timeout=self.CONNECTION_TIMEOUT,
        )

    def list(self, resource, filter_list=None, is_staff=False):
        actions = self.get_actions(resource)
        filter_params = self.convert_to_string_param(filter_list)
        if is_staff:
            headers = {"apikey": self.api_key, "Cache-Control": "no-cache"}
            cookies = dict(nocache="meow")
            return requests.request(
                actions["list"]["method"],
                actions["list"]["url"],
                params=filter_params,
                headers=headers,
                cookies=cookies,
                timeout=self.CONNECTION_TIMEOUT,
            )
        return requests.request(
            actions["list"]["method"],
            actions["list"]["url"],
            params=filter_params,
            timeout=self.CONNECTION_TIMEOUT,
        )

    def create(self, resource, body):
        actions = self.get_actions(resource)
        headers = {"apikey": self.api_key, "Content-Type": "application/json"}
        return requests.request(
            actions["create"]["method"],
            actions["create"]["url"],
            data=body,
            headers=headers,
            timeout=self.CONNECTION_TIMEOUT,
        )

    def update(self, resource, id, body):
        actions = self.get_actions(resource)
        headers = {"apikey": self.api_key, "Content-Type": "application/json"}
        return requests.request(
            actions["update"]["method"],
            actions["update"]["url"].format(id),
            data=body,
            headers=headers,
            timeout=self.CONNECTION_TIMEOUT,
        )

    def delete(self, resource, id):
        actions = self.get_actions(resource)
        headers = {"apikey": self.api_key, "Content-Type": "application/json"}
        return requests.request(
            actions["delete"]["method"],
            actions["delete"]["url"].format(id),
            headers=headers,
            timeout=self.CONNECTION_TIMEOUT,
        )

    # Special action to full-text search generic resources
    def search(self, params):
        search_params = self.convert_to_string_param(params)
        action = self.get_actions()["search"]
        response = requests.request(
            action["method"],
            action["url"],
            params=search_params,
            timeout=self.CONNECTION_TIMEOUT,
        )
        return response

    def upload(self, resource, body, files):
        action = self.get_actions(resource)["upload"]
        headers = {"apikey": self.api_key}
        return requests.request(
            action["method"],
            action["url"],
            data=body,
            files=files,
            headers=headers,
            timeout=self.CONNECTION_TIMEOUT,
        )

    @staticmethod
    def convert_to_string_param(params):
        if not params:
            return None
        for k, v in params.items():
            if type(v) == list:
                list_to_string = ",".join(v)
                params[k] = list_to_string
        return params
