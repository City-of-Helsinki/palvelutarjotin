from graphene import Field, ID, List, NonNull, ObjectType
from graphene_linked_events.schema import LocalisedObject, Response
from neighborhood.utils import api_client, format_response, json2obj, json_object_hook


class Neighborhood(ObjectType):
    id = ID(required=True)
    name = Field(LocalisedObject)


class NeighborhoodListResponse(Response):
    data = NonNull(List(NonNull(Neighborhood)))


class Query:
    neighborhood_list = Field(NeighborhoodListResponse)

    @staticmethod
    def normalize_neighborhood(features: list):
        return [
            {
                "id": "{division}:{name_fi}".format(
                    division=feature.properties.aluejako.lower(),
                    name_fi=feature.properties.nimi_fi.lower(),
                ),
                "name": {
                    "en": feature.properties.nimi_fi.capitalize(),
                    "fi": feature.properties.nimi_fi.capitalize(),
                    "sv": feature.properties.nimi_se.capitalize(),
                },
            }
            for feature in features
        ]

    @staticmethod
    def resolve_neighborhood_list(parent, info, **kwargs):
        response = api_client.neighborhood_list()
        json_data = json2obj(format_response(response))
        normalized_data = Query.normalize_neighborhood(json_data.features)
        result = {
            "meta": {
                "count": json_data.numberReturned,
                "next": None,
                "previous": None,
            },
            "data": normalized_data,
        }
        return json_object_hook(result)
