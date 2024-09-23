from typing import Optional

import requests


class ServicemapApiClient:
    CONNECTION_TIMEOUT = 20
    DATA_SOURCE = "tprek"

    def __init__(self, config) -> None:
        self.root = config["ROOT"]

    def list_helsinki_schools_and_kindergartens(self, filters: Optional[dict] = None):
        """
        List of names and ids' of schools, colleges and kindergardens.
        The Servicemap Query (the old deprecated implementation --
        too slow and does not have search functionality):
        - https://api.hel.fi/servicemap/v2/unit/
        ?municipality=helsinki&only=name&service_node=2118,868,2179,1088,1257,1097
        The Palvelukarttaws Query (has a search functionality):
        - https://www.hel.fi/palvelukarttaws/rest/v4/unit/?
        arealcity=91&ontologytree=2118+868+2179+1088+1257+1097
        """

        # NOTE: The service_nodes of the Servicemap matches
        # with the ontologytrees in the Palvelukarttaws.
        # To check, An example:
        # - https://api.hel.fi/servicemap/v2/service_node/2118/
        # - https://www.hel.fi/palvelukarttaws/rest/v4/ontologytree/2118
        service_nodes = [
            2118,  # Pre-primary education
            868,  # Day care
            2179,  # Vocational education
            1088,  # Pre-primary education
            1257,  # General upper secondary education
            1097,  # Basic education
        ]
        payload = filters or {}
        payload["arealcity"] = (
            "91"  # Helsinki - https://www.hel.fi/palvelukarttaws/rest/v4/arealcity/
        )
        payload["ontologytree"] = "+".join(str(node) for node in service_nodes)
        # NOTE: It is important that the "+" is not encoded to "%2B" in the URL.
        payload_str = "&".join("%s=%s" % (k, v) for k, v in payload.items())
        return requests.request(
            "GET",
            self.root,
            params=payload_str,
            timeout=self.CONNECTION_TIMEOUT,
        )
