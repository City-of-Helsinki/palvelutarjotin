import requests


class LinkedEventsApiClient(object):
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
        }

    def retrieve(self, resource, id, params=None):
        actions = self.get_actions(resource)
        return requests.request(
            actions["retrieve"]["method"],
            actions["retrieve"]["url"].format(id),
            params=params,
        )

    def list(self, resource, filter_list=None):
        actions = self.get_actions(resource)
        filter_params = filter_list
        return requests.request(
            actions["list"]["method"], actions["list"]["url"], params=filter_params
        )

    def create(self, resource, body):
        actions = self.get_actions(resource)
        headers = {"apikey": self.api_key, "Content-Type": "application/json"}
        return requests.request(
            actions["create"]["method"],
            actions["create"]["url"],
            data=body,
            headers=headers,
        )

    def update(self, resource, id, body):
        actions = self.get_actions(resource)
        headers = {"apikey": self.api_key, "Content-Type": "application/json"}
        return requests.request(
            actions["update"]["method"],
            actions["update"]["url"].format(id),
            data=body,
            headers=headers,
        )

    def delete(self, resource, id):
        actions = self.get_actions(resource)
        headers = {"apikey": self.api_key, "Content-Type": "application/json"}
        return requests.request(
            actions["delete"]["method"],
            actions["delete"]["url"].format(id),
            headers=headers,
        )

    # Special action to full-text search generic resources
    def search(self, search_params):
        action = self.get_actions("search")["search"]
        response = requests.request(
            action["method"], action["url"], params=search_params
        )
        return response
