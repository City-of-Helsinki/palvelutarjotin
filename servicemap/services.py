from django.conf import settings

from servicemap.rest_client import ServicemapApiClient

service_map_api_client = ServicemapApiClient(config=settings.SERVICEMAP_API_CONFIG)


class UnitService:
    @staticmethod
    def unit_id(unit):
        """
        The ID of the unit for LinkedEvents, e.g. "tprek:123"
        """
        return "{data_source}:{place_id}".format(
            data_source=service_map_api_client.DATA_SOURCE,
            place_id=unit["id"],
        )

    @staticmethod
    def unit_name(unit):
        """
        The localized name of the unit.
        """
        name_fi = unit["name_fi"]
        return {
            "fi": name_fi,
            "en": unit.get("name_en", name_fi),
            "sv": unit.get("name_sv", name_fi),
        }

    @staticmethod
    def normalize_unit(unit):
        """
        Normalize a unit received from palvelukarttaws's unit endpoint.
        """
        return {
            "id": UnitService.unit_id(unit),
            "name": UnitService.unit_name(unit),
        }

    @staticmethod
    def normalize_units(units: list):
        """
        Normalize the list of units received from palvelukarttaws's unit endpoint.
        """
        return [UnitService.normalize_unit(unit) for unit in units]

    @staticmethod
    def get_schools_and_kindergartens_list(**kwargs):
        from servicemap.schema import ServiceUnitNameListResponse

        response = service_map_api_client.list_helsinki_schools_and_kindergartens(
            filters=kwargs
        )
        json_data = response.json()
        normalized_data = UnitService.normalize_units(json_data)
        return ServiceUnitNameListResponse(
            meta={"count": len(json_data)},
            data=normalized_data,
        )
