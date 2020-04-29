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

    def retrieve(self, resource, id):
        actions = self.get_actions(resource)
        response = requests.request(
            actions["retrieve"]["method"], actions["retrieve"]["url"].format(id)
        )
        return response

    def list(self, resource, filter=None):
        actions = self.get_actions(resource)
        response = requests.request(actions["list"]["method"], actions["list"]["url"])
        return response

    def post(self, resource, id=None):
        pass

    def delete(self, resource, id):
        pass

    #
    # def _build_resource_url(self, resource, filter=None):
    #     # TODO: Add filter
    #     return "{root}/{resource}/{id}".format(
    #         root=self.root,
    #         resource=self.resource
    #     )
