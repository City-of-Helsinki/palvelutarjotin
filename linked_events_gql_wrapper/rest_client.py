import requests


class LinkedEventsApiClient(object):
    def __init__(self, root, headers=None) -> None:
        self.headers = headers
        self.root = root
        super().__init__()

    def get_actions(self, resource):
        return {
            "list": {"method": "GET", "url": self.root + resource},
            "create": {"method": "POST", "url": self.root + resource},
            "retrieve": {"method": "GET", "url": self.root + resource + "/{}"},
            "update": {"method": "PUT", "url": self.root + resource + "/{}"},
            "partial_update": {"method": "PATCH", "url": self.root + resource + "/{}"},
            "destroy": {"method": "DELETE", "url": self.root + resource + "/{}"},
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

    def post(self, resource, id=None):
        pass

    def delete(self, resource, id):
        pass

    # Special action to full-text search generic resources
    def search(self, search_params):
        action = self.get_search_action()
        # search_params = {"type": type, "input": query}
        response = requests.request(
            action["method"], action["url"], params=search_params
        )
        return response
