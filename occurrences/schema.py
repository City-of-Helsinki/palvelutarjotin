import graphene
from graphene import InputObjectType, relay
from graphene_django import DjangoObjectType
from occurrences.models import PalvelutarjotinEvent


class PalvelutarjotinEventNode(DjangoObjectType):
    class Meta:
        model = PalvelutarjotinEvent
        interfaces = (relay.Node,)


class PalvelutarjotinEventInput(InputObjectType):
    enrolment_start = graphene.DateTime()
    enrolment_end = graphene.DateTime()
    duration = graphene.Int(required=True)
    needed_occurrences = graphene.Int(required=True)
