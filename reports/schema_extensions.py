from typing import TYPE_CHECKING

from drf_spectacular.extensions import (
    OpenApiAuthenticationExtension,
    OpenApiSerializerFieldExtension,
)
from drf_spectacular.plumbing import (
    build_array_type,
    build_basic_type,
    build_object_type,
)

if TYPE_CHECKING:
    from drf_spectacular.openapi import AutoSchema
    from drf_spectacular.utils import Direction


class Size2ArrayFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "reports.serializers.Size2ArrayField"  # Replace 'your_app'

    def map_serializer_field(self, auto_schema: "AutoSchema", direction: "Direction"):
        field = self.target
        return {
            "type": "array",
            "items": build_object_type(
                properties={
                    field.first_value_name: build_basic_type(str),
                    field.second_value_name: build_basic_type(str),
                },
                required=[field.first_value_name, field.second_value_name],
            ),
            "nullable": field.allow_null,
            "example": [
                {
                    field.first_value_name: "value1_id",
                    field.second_value_name: "value1_label",
                },
                {
                    field.first_value_name: "value2_id",
                    field.second_value_name: "value2_label",
                },
            ],
        }


class PositionFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "reports.serializers.PositionField"

    def map_serializer_field(self, auto_schema: "AutoSchema", direction: "Direction"):
        field = self.target
        return {
            "type": "object",
            "properties": {
                "longitude": build_basic_type(float),
                "latitude": build_basic_type(float),
            },
            "nullable": field.allow_null,
            "example": {"longitude": 24.945831, "latitude": 60.192059},
        }


class OCDIDFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "reports.serializers.OCDIDField"  # Replace 'your_app'

    def map_serializer_field(self, auto_schema: "AutoSchema", direction: "Direction"):
        field = self.target
        properties = {
            "ocd_ids": build_array_type(build_basic_type(str)),
            "country": build_basic_type(str),
            "municipality": build_basic_type(str),
            "sub_district": build_basic_type(str),
            "neighborhood": build_basic_type(str),
            "district": build_basic_type(str),
            **{key: build_basic_type(str) for key, value in field.translations.items()},
        }
        if field.allow_null:
            for key in properties:
                properties[key]["nullable"] = True

        return {
            "type": "object",
            "properties": properties,
            "nullable": field.allow_null,
            "example": {
                "ocd_ids": [
                    "ocd-division/country:fi/kunta:helsinki/osa-alue:keski-pasila",
                    "ocd-division/country:fi/kunta:helsinki/kaupunginosa:pasila",
                    "ocd-division/country:fi/kunta:helsinki/peruspiiri:pasila",
                    "ocd-division/country:fi/kunta:helsinki",
                ],
                "country": "FI",
                "municipality": "Helsinki",
                "sub_district": "Keski-pasila",
                "neighborhood": "Pasila",
                "district": "Pasila",
            },
        }


class KultusApiTokenAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = "palvelutarjotin.oidc.KultusApiTokenAuthentication"
    name = "Kultus API token authentication"

    def get_security_definition(self, auto_schema: "AutoSchema"):
        return {
            "header_name": "Authorization",
            "token_prefix": "Bearer",  #  Most common prefix for Bearer authentication
            "description": "Authentication using a Kultus API token. "
            + "The token should be included in the Authorization header "
            + "as a Bearer token.",
        }
