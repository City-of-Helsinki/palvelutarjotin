import graphene
from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.utils.translation import get_language
from graphene import InputObjectType, relay
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphql_jwt.decorators import staff_member_required
from occurrences.models import (
    Language,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    VenueCustomData,
)
from organisations.models import Organisation, Person
from organisations.schema import PersonNodeInput

from common.utils import (
    get_node_id_from_global_id,
    update_object,
    update_object_with_translations,
)
from palvelutarjotin.exceptions import ObjectDoesNotExistError

LanguageEnum = graphene.Enum(
    "Language", [(l[0].upper(), l[0]) for l in settings.LANGUAGES]
)

VenueTranslation = apps.get_model("occurrences", "VenueCustomDataTranslation")


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


class VenueTranslationType(DjangoObjectType):
    language_code = LanguageEnum(required=True)

    class Meta:
        model = VenueTranslation
        exclude = ("id", "master")


class VenueTranslationsInput(InputObjectType):
    description = graphene.String()
    language_code = LanguageEnum(required=True)


class VenueNode(DjangoObjectType):
    description = graphene.String(
        description="Translated field in the language "
        "defined in request "
        "ACCEPT-LANGUAGE header "
    )
    id = graphene.GlobalID(
        source="place_id",
        description="Venue custom data ID is "
        "the encoded place_id from "
        "linkedEvent",
    )

    class Meta:
        model = VenueCustomData
        interfaces = (relay.Node,)
        exclude = ("place_id",)

    @classmethod
    def get_queryset(cls, queryset, info):
        lang = get_language()
        return queryset.language(lang)

    @classmethod
    def get_node(cls, info, id):
        return super().get_node(info, id)


class VenueNodeInput(InputObjectType):
    translations = graphene.List(VenueTranslationsInput)


class OccurrenceNode(DjangoObjectType):
    class Meta:
        model = Occurrence
        interfaces = (relay.Node,)


def validate_occurrence_data(kwargs):
    # TODO: Validate place_id, languages ...
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


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language


class OccurrenceLanguageInput(InputObjectType):
    id = LanguageEnum(required=True)


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
        auto_acceptance = graphene.Boolean(required=True)
        amount_of_seats = graphene.Int(required=True)
        languages = graphene.NonNull(graphene.List(OccurrenceLanguageInput))

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        validate_occurrence_data(kwargs)
        contact_persons = kwargs.pop("contact_persons", None)
        languages = kwargs.pop("languages", None)
        kwargs["organisation_id"] = get_node_id_from_global_id(
            kwargs["organisation_id"], "OrganisationNode"
        )
        kwargs["p_event_id"] = get_node_id_from_global_id(
            kwargs["p_event_id"], "PalvelutarjotinEventNode"
        )
        occurrence = Occurrence.objects.create(**kwargs)

        if contact_persons:
            add_contact_persons_to_object(contact_persons, occurrence)

        if languages:
            occurrence.add_languages(languages)

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
        auto_acceptance = graphene.Boolean()
        amount_of_seats = graphene.Int()
        languages = graphene.NonNull(
            graphene.List(OccurrenceLanguageInput),
            description="If present, should include all languages of the occurrence",
        )

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
        languages = kwargs.pop("languages", None)
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
        if languages:
            occurrence.add_languages(languages)

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


class AddVenueMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(description="Place id from linked event")
        translations = graphene.List(VenueTranslationsInput)

    venue = graphene.Field(VenueNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # TODO: Add validation
        kwargs["place_id"] = get_node_id_from_global_id(kwargs.pop("id"), "VenueNode")
        translations = kwargs.pop("translations")
        venue, _ = VenueCustomData.objects.get_or_create(**kwargs)
        venue.create_or_update_translations(translations)
        return AddVenueMutation(venue=venue)


class UpdateVenueMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(description="Place id from linked event")
        translations = graphene.List(VenueTranslationsInput)

    venue = graphene.Field(VenueNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # TODO: Add validation
        venue_global_id = kwargs.pop("id")
        try:
            venue = VenueCustomData.objects.get(
                pk=get_node_id_from_global_id(venue_global_id, "VenueNode")
            )
            update_object_with_translations(venue, kwargs)
        except VenueCustomData.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        return UpdateVenueMutation(venue=venue)


class DeleteVenueMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID(description="Place id from linked event")

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        venue_global_id = kwargs.pop("id")
        venue_id = get_node_id_from_global_id(venue_global_id, "VenueNode")
        try:
            venue = VenueCustomData.objects.get(pk=venue_id)
            venue.delete()
        except VenueCustomData.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        return DeleteVenueMutation()


class Query:
    occurrences = DjangoConnectionField(OccurrenceNode)
    occurrence = relay.Node.Field(OccurrenceNode)

    study_groups = DjangoConnectionField(StudyGroupNode)
    study_group = relay.Node.Field(StudyGroupNode)

    venues = DjangoConnectionField(VenueNode)
    venue = relay.Node.Field(VenueNode)


class Mutation:
    add_occurrence = AddOccurrenceMutation.Field()
    update_occurrence = UpdateOccurrenceMutation.Field()
    delete_occurrence = DeleteOccurrenceMutation.Field()

    add_venue = AddVenueMutation.Field()
    update_venue = UpdateVenueMutation.Field()
    delete_venue = DeleteVenueMutation.Field()
