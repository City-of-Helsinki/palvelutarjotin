import requests


class LinkedEventsApiClient(object):
    def __init__(self, config) -> None:
        self.root = config["ROOT"]
        self.api_key = config["API_KEY"]
        super().__init__()

    def get_actions(self, resource):
        return {
            "list": {"method": "GET", "url": self.root + resource + "/"},
            "create": {"method": "POST", "url": self.root + resource + "/"},
            "retrieve": {"method": "GET", "url": self.root + resource + "/{}/"},
            "update": {"method": "PUT", "url": self.root + resource + "/{}/"},
            "destroy": {"method": "DELETE", "url": self.root + resource + "/{}/"},
        }

    def get_search_action(self):
        return {"method": "GET", "url": self.root + "search/"}

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
            actions["destroy"]["method"],
            actions["destroy"]["url"].format(id),
            headers=headers,
        )

    # Special action to full-text search generic resources
    def search(self, search_params):
        action = self.get_search_action()
        # search_params = {"type": type, "input": query}
        response = requests.request(
            action["method"], action["url"], params=search_params
        )
        return response
