import graphene
import linked_events_gql_wrapper.schema


class Mutation(linked_events_gql_wrapper.schema.Mutation, graphene.ObjectType):
    pass


class Query(linked_events_gql_wrapper.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
