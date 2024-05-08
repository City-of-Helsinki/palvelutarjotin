import graphene

from servicemap.services import UnitService


class Response(graphene.ObjectType):
    meta = graphene.Field("graphene_linked_events.schema.Meta", required=True)


class ServiceUnitNode(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.Field("graphene_linked_events.schema.LocalisedObject")


class ServiceUnitNameListResponse(Response):
    data = graphene.NonNull(graphene.List(graphene.NonNull(ServiceUnitNode)))


class Query:
    schools_and_kindergartens_list = graphene.Field(
        ServiceUnitNameListResponse, search=graphene.String()
    )

    @staticmethod
    def resolve_schools_and_kindergartens_list(parent, info, **kwargs):
        return UnitService.get_schools_and_kindergartens_list(**kwargs)
