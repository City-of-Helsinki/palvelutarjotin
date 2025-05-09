from graphene import ObjectType, Schema
from graphene_django import DjangoConnectionField

from organisations.models import Person
from organisations.schema import PublicPersonNode


class TestQuery(ObjectType):
    all_public_person_nodes = DjangoConnectionField(PublicPersonNode)

    def resolve_all_public_person_nodes(root, info):
        return PublicPersonNode.get_queryset(Person.objects.all(), info)


test_schema = Schema(query=TestQuery)
