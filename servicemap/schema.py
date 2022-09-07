import graphene

from servicemap.utils import api_client, get_params_from_url, json2obj, json_object_hook


class Response(graphene.ObjectType):
    meta = graphene.Field("graphene_linked_events.schema.Meta", required=True)


class ServiceUnitNode(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.Field("graphene_linked_events.schema.LocalisedObject")


class ServiceUnitNameListResponse(Response):
    data = graphene.NonNull(graphene.List(graphene.NonNull(ServiceUnitNode)))


class Query:
    schools_and_kindergartens_list = graphene.Field(ServiceUnitNameListResponse)

    @staticmethod
    def normalize_service_unit_node(units: list):

        return [
            {
                "id": "{data_source}:{place_id}".format(
                    data_source=api_client.DATA_SOURCE,
                    place_id=unit.id,
                ),
                "name": {
                    "en": getattr(unit.name, "en", unit.name.fi).capitalize(),
                    "fi": unit.name.fi.capitalize(),
                    "sv": getattr(unit.name, "sv", unit.name.fi).capitalize(),
                },
            }
            for unit in units
        ]

    @staticmethod
    def resolve_schools_and_kindergartens_list(parent, info, **kwargs):
        response = api_client.list_helsinki_schools_and_kindergartens(
            # Use the max page size when the pages are queried
            # to make minimun amount of API requests.
            filter_list=kwargs
            or {"page_size": 1000}
        )
        json_data = json2obj(response.content)

        normalized_data = Query.normalize_service_unit_node(json_data.results)
        next_page_url = json_data.next

        if json_data.next:
            # Recursive call to fetch a next page data from a paginated result list.
            next_page_response = Query.resolve_schools_and_kindergartens_list(
                parent, info, **get_params_from_url(json_data.next)
            )
            normalized_data.extend(next_page_response.data)

            # Because all pages are combined,
            # the next_page_url should be set to None
            # after the last response is retrieved.
            next_page_url = None

        result = {
            "meta": {
                "count": json_data.count,
                "next": next_page_url,
                "previous": json_data.previous,
            },
            "data": normalized_data,
        }

        return json_object_hook(result)
