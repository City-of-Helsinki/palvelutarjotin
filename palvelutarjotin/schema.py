import django_ilmoitin.api.schema as django_ilmoitin_schema
import graphene
import graphene_linked_events.schema
import occurrences.schema
import organisations.schema


class Mutation(
    graphene_linked_events.schema.Mutation,
    organisations.schema.Mutation,
    occurrences.schema.Mutation,
    graphene.ObjectType,
):
    pass


class Query(
    django_ilmoitin_schema.Query,
    graphene_linked_events.schema.Query,
    organisations.schema.Query,
    occurrences.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
