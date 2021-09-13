import requests


class NeighborhoodApiClient:
    def __init__(self, config) -> None:
        self.root = config["ROOT"]
        self.jsonParams = {"outputFormat": "json"}

    def neighborhood_list(self):
        return requests.request(
            "GET",
            self.root,
            params={
                "request": "getFeature",
                "typeName": "avoindata:Kaupunginosajako",
                **self.jsonParams,
            },
        )
