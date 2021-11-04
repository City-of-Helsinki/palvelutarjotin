import requests


class ServicemapApiClient:

    CONNECTION_TIMEOUT = 20
    DATA_SOURCE = "tprek"

    def __init__(self, config) -> None:
        self.root = config["ROOT"]

    def list_helsinki_schools_and_kindergartens(self, filter_list=None):
        """
        List of names and ids' of schools, colleges and kindergardens.
        Query:
        https://api.hel.fi/servicemap/v2/unit/?municipality=helsinki&only=name&service_node=2118,868,2179,1088,1257,1097
        """
        service_nodes = [2118, 868, 2179, 1088, 1257, 1097]

        filter_params = (
            self.__convert_to_string_param(filter_list) if filter_list else {}
        )

        return requests.request(
            "GET",
            self.root,
            params={
                **filter_params,
                "municipality": "helsinki",
                "only": "name",
                "service_node": ",".join([str(node) for node in service_nodes]),
            },
            timeout=self.CONNECTION_TIMEOUT,
        )

    @staticmethod
    def __convert_to_string_param(params):
        converted_params = dict(params)
        if not converted_params:
            return None
        for k, v in converted_params.items():
            if type(v) == list:
                list_to_string = ",".join(v)
                converted_params[k] = list_to_string
        return converted_params
