import graphene
import graphene_linked_events.schema


class Mutation(graphene_linked_events.schema.Mutation, graphene.ObjectType):
    pass


class Query(graphene_linked_events.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
