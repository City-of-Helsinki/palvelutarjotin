import graphene
from django.db import transaction
from graphene import InputObjectType, relay
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphql_jwt.decorators import staff_member_required
from occurrences.models import (
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    VenueCustomData,
)
from organisations.models import Organisation, Person
from organisations.schema import PersonNodeInput

from common.utils import get_node_id_from_global_id, update_object
from palvelutarjotin.exceptions import ObjectDoesNotExistError


class PalvelutarjotinEventNode(DjangoObjectType):
    class Meta:
        model = PalvelutarjotinEvent
        interfaces = (relay.Node,)


class PalvelutarjotinEventInput(InputObjectType):
    enrolment_start = graphene.DateTime()
    enrolment_end = graphene.DateTime()
    duration = graphene.Int(required=True)
    needed_occurrences = graphene.Int(required=True)


class StudyGroupNode(DjangoObjectType):
    class Meta:
        model = StudyGroup
        interfaces = (relay.Node,)


class OccurrenceNode(DjangoObjectType):
    class Meta:
        model = Occurrence
        interfaces = (relay.Node,)


class VenueCustomDataNode(DjangoObjectType):
    class Meta:
        model = VenueCustomData
        interfaces = (relay.Node,)


def validate_occurrence_data(kwargs):
    # TODO: Validate place_id, ...
    p_event_global_id = kwargs.get("p_event_id", None)
    if p_event_global_id:
        p_event_id = get_node_id_from_global_id(
            p_event_global_id, "PalvelutarjotinEventNode"
        )
        if not PalvelutarjotinEvent.objects.filter(id=p_event_id).exists():
            raise ObjectDoesNotExistError("Palvelutarjotin event does not exist")
    organisation_global_id = kwargs.get("organisation_id", None)
    if organisation_global_id:
        organisation_id = get_node_id_from_global_id(
            organisation_global_id, "OrganisationNode"
        )
        if not Organisation.objects.filter(id=organisation_id).exists():
            raise ObjectDoesNotExistError("Organisation does not exist")


@transaction.atomic
def add_contact_persons_to_object(contact_persons, obj):
    obj.contact_persons.clear()
    for p in contact_persons:
        p_global_id = p.get("id", None)
        if p_global_id:
            try:
                person = Person.objects.get(
                    id=get_node_id_from_global_id(p_global_id, "PersonNode")
                )
            except Person.DoesNotExist as e:
                raise ObjectDoesNotExistError(e)
        else:
            person = Person.objects.create(**p)
        obj.contact_persons.add(person)


class AddOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        place_id = graphene.String(required=True)
        min_group_size = graphene.Int(required=True)
        max_group_size = graphene.Int(required=True)
        start_time = graphene.DateTime(required=True)
        end_time = graphene.DateTime(required=True)
        organisation_id = graphene.ID(required=True)
        contact_persons = graphene.List(PersonNodeInput)
        p_event_id = graphene.ID(required=True)

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        validate_occurrence_data(kwargs)
        contact_persons = kwargs.pop("contact_persons", None)
        kwargs["organisation_id"] = get_node_id_from_global_id(
            kwargs["organisation_id"], "OrganisationNode"
        )
        kwargs["p_event_id"] = get_node_id_from_global_id(
            kwargs["p_event_id"], "PalvelutarjotinEventNode"
        )
        occurrence = Occurrence.objects.create(**kwargs)
        if contact_persons:
            add_contact_persons_to_object(contact_persons, occurrence)
        return AddOccurrenceMutation(occurrence=occurrence)


class UpdateOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        place_id = graphene.String()
        min_group_size = graphene.Int()
        max_group_size = graphene.Int()
        start_time = graphene.DateTime()
        end_time = graphene.DateTime()
        organisation_id = graphene.ID()
        contact_persons = graphene.List(
            PersonNodeInput,
            description="Should include "
            "all contact "
            "persons of "
            "the "
            "occurrence, "
            "missing contact "
            "persons will be "
            "removed during "
            "mutation",
        )
        p_event_id = graphene.ID()

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            occurrence = Occurrence.objects.get(
                id=get_node_id_from_global_id(kwargs.pop("id"), "OccurrenceNode")
            )
        except Occurrence.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        contact_persons = kwargs.pop("contact_persons", None)
        validate_occurrence_data(kwargs)
        kwargs["organisation_id"] = get_node_id_from_global_id(
            kwargs["organisation_id"], "OrganisationNode"
        )
        kwargs["p_event_id"] = get_node_id_from_global_id(
            kwargs["p_event_id"], "PalvelutarjotinEventNode"
        )

        update_object(occurrence, kwargs)
        # Nested update
        if contact_persons:
            add_contact_persons_to_object(contact_persons, occurrence)
        return UpdateOccurrenceMutation(occurrence=occurrence)


class DeleteOccurrenceMutation(graphene.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            occurrence = Occurrence.objects.get(
                id=get_node_id_from_global_id(kwargs.pop("id"), "OccurrenceNode")
            )
        except Occurrence.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        occurrence.delete()
        return DeleteOccurrenceMutation()


class Query:
    occurrences = DjangoConnectionField(OccurrenceNode)
    occurrence = relay.Node.Field(OccurrenceNode)

    study_groups = DjangoConnectionField(StudyGroupNode)
    study_group = relay.Node.Field(StudyGroupNode)

    venues = DjangoConnectionField(VenueCustomDataNode)
    venue = relay.Node.Field(VenueCustomDataNode)


class Mutation:
    add_occurrence = AddOccurrenceMutation.Field()
    update_occurrence = UpdateOccurrenceMutation.Field()
    delete_occurrence = DeleteOccurrenceMutation.Field()
