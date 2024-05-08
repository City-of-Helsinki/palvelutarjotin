from django.conf import settings

from servicemap.rest_client import ServicemapApiClient

service_map_api_client = ServicemapApiClient(config=settings.SERVICEMAP_API_CONFIG)


class UnitService:
    @staticmethod
    def __normalize_service_unit_node(units: list):
        return [
            {
                # unit.id is not a valid place_id with LinkedEvents.
                # The TPREK specific id is needed.
                "id": "{data_source}:{place_id}".format(
                    data_source=service_map_api_client.DATA_SOURCE,
                    place_id=unit["id"],
                ),
                "name": {
                    "fi": unit["name_fi"],
                    "en": unit["name_en"] if "name_en" in unit else unit["name_fi"],
                    "sv": unit["name_sv"] if "name_sv" in unit else unit["name_fi"],
                },
            }
            for unit in units
        ]

    @staticmethod
    def get_schools_and_kindergartens_list(**kwargs):
        from servicemap.schema import ServiceUnitNameListResponse

        response = service_map_api_client.list_helsinki_schools_and_kindergartens(
            filters=kwargs
        )
        json_data = response.json()
        normalized_data = UnitService.__normalize_service_unit_node(json_data)

        return ServiceUnitNameListResponse(
            meta={
                "count": len(json_data),
            },
            data=normalized_data,
        )
