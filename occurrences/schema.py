from datetime import timedelta

import graphene
from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import get_language
from graphene import InputObjectType, relay
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphql_jwt.decorators import login_required, staff_member_required
from occurrences.models import (
    Enrolment,
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
from palvelutarjotin.exceptions import (
    AlreadyJoinedEventError,
    EnrolmentClosedError,
    EnrolmentNotEnoughCapacityError,
    EnrolmentNotStartedError,
    InvalidStudyGroupSizeError,
    ObjectDoesNotExistError,
)

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
    enrolment_end_days = graphene.Int()
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
    id = graphene.ID(
        source="place_id", description="place_id from linkedEvent", required=True
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
    remaining_seats = graphene.Int()
    seats_taken = graphene.Int()

    class Meta:
        model = Occurrence
        interfaces = (relay.Node,)

    def resolve_remaining_seats(self, info, **kwargs):
        return self.amount_of_seats - self.seats_taken


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
        id = graphene.ID(description="Place id from linked event", required=True)
        translations = graphene.List(VenueTranslationsInput)
        has_clothing_storage = graphene.Boolean(required=True)
        has_snack_eating_place = graphene.Boolean(required=True)

    venue = graphene.Field(VenueNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # TODO: Add validation
        kwargs["place_id"] = kwargs.pop("id")
        translations = kwargs.pop("translations")
        venue, _ = VenueCustomData.objects.get_or_create(**kwargs)
        venue.create_or_update_translations(translations)
        return AddVenueMutation(venue=venue)


class UpdateVenueMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(description="Place id from linked event", required=True)
        translations = graphene.List(VenueTranslationsInput)
        has_clothing_storage = graphene.Boolean()
        has_snack_eating_place = graphene.Boolean()

    venue = graphene.Field(VenueNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # TODO: Add validation
        try:
            venue = VenueCustomData.objects.get(pk=kwargs.pop("id"))
            update_object_with_translations(venue, kwargs)
        except VenueCustomData.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        return UpdateVenueMutation(venue=venue)


class DeleteVenueMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(description="Place id from linked event", required=True)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            venue = VenueCustomData.objects.get(pk=kwargs.pop("id"))
            venue.delete()
        except VenueCustomData.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        return DeleteVenueMutation()


class EnrolmentNode(DjangoObjectType):
    class Meta:
        model = Enrolment
        interfaces = (relay.Node,)


def validate_enrolment(study_group, occurrence):
    # Expensive validation are sorted to bottom
    if (
        study_group.group_size > occurrence.max_group_size
        or study_group.group_size < occurrence.min_group_size
    ):
        raise InvalidStudyGroupSizeError(
            "Study group size not match occurrence group " "size"
        )
    if timezone.now() < occurrence.p_event.enrolment_start:
        raise EnrolmentNotStartedError("Enrolment is not opened")
    if timezone.now() > occurrence.start_time - timedelta(
        days=occurrence.p_event.enrolment_end_days
    ):
        raise EnrolmentClosedError("Enrolment has been closed")
    if study_group.occurrences.filter(p_event=occurrence.p_event).exists():
        raise AlreadyJoinedEventError("Study group already joined this event")
    if occurrence.seats_taken + study_group.group_size > occurrence.amount_of_seats:
        raise EnrolmentNotEnoughCapacityError("Not enough space for this study group")


class EnrolOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        occurrence_id = graphene.GlobalID(description="Occurrence id of event")
        study_group_id = graphene.GlobalID(description="Study group id")

    enrolment = graphene.Field(EnrolmentNode)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence_id = get_node_id_from_global_id(
            kwargs["occurrence_id"], "OccurrenceNode"
        )
        group_id = get_node_id_from_global_id(
            kwargs["study_group_id"], "StudyGroupNode"
        )
        try:
            occurrence = Occurrence.objects.get(pk=occurrence_id)
        except Occurrence.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        try:
            study_group = StudyGroup.objects.get(pk=group_id)
        except StudyGroup.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        validate_enrolment(study_group, occurrence)
        enrolment = Enrolment.objects.create(
            study_group=study_group, occurrence=occurrence
        )

        return EnrolOccurrenceMutation(enrolment=enrolment)


class UnenrolOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        occurrence_id = graphene.GlobalID(description="Occurrence id of event")
        study_group_id = graphene.GlobalID(description="Study group id")

    occurrence = graphene.Field(OccurrenceNode)
    study_group = graphene.Field(StudyGroupNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # TODO: Authorize if user has permission to unenrol the occurrence
        occurrence_id = get_node_id_from_global_id(
            kwargs["occurrence_id"], "OccurrenceNode"
        )
        group_id = get_node_id_from_global_id(
            kwargs["study_group_id"], "StudyGroupNode"
        )
        try:
            study_group = StudyGroup.objects.get(pk=group_id)
        except StudyGroup.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        try:
            occurrence = study_group.occurrences.get(pk=occurrence_id)
            occurrence.study_groups.remove(study_group)
        except Occurrence.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        return UnenrolOccurrenceMutation(study_group=study_group, occurrence=occurrence)


class AddStudyGroupMutation(graphene.relay.ClientIDMutation):
    class Input:
        person = graphene.NonNull(
            PersonNodeInput,
            description="If person input doesn't include person"
            " id, a new person object will be "
            "created",
        )
        name = graphene.String()
        group_size = graphene.Int(required=True)

    study_group = graphene.Field(StudyGroupNode)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        person_data = kwargs.pop("person")
        if person_data.get("id"):
            person_id = get_node_id_from_global_id(person_data.get("id"), "PersonNode")
            try:
                person = Person.objects.get(id=person_id)
            except Person.DoesNotExist as e:
                raise ObjectDoesNotExistError(e)
        else:
            person = Person.objects.create(**person_data)
        kwargs["person_id"] = person.id
        study_group = StudyGroup.objects.create(**kwargs)
        return AddStudyGroupMutation(study_group=study_group)


class UpdateStudyGroupMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        person = PersonNodeInput()
        name = graphene.String()
        group_size = graphene.Int()

    study_group = graphene.Field(StudyGroupNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        study_group_global_id = kwargs.pop("id")
        study_group_id = get_node_id_from_global_id(
            study_group_global_id, "StudyGroupNode"
        )
        try:
            study_group = StudyGroup.objects.get(id=study_group_id)
        except StudyGroup.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

        person_data = kwargs.pop("person", None)
        if person_data:
            if person_data.get("id"):
                person_id = get_node_id_from_global_id(
                    person_data.get("id"), "PersonNode"
                )
                try:
                    person = Person.objects.get(id=person_id)
                except Person.DoesNotExist as e:
                    raise ObjectDoesNotExistError(e)
            else:
                person = Person.objects.create(**person_data)
            kwargs["person_id"] = person.id
        update_object(study_group, kwargs)
        return UpdateStudyGroupMutation(study_group=study_group)


class DeleteStudyGroupMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        study_group_global_id = kwargs.pop("id")
        study_group_id = get_node_id_from_global_id(
            study_group_global_id, "StudyGroupNode"
        )
        try:
            study_group = StudyGroup.objects.get(id=study_group_id)
        except StudyGroup.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        study_group.delete()
        return DeleteStudyGroupMutation()


class Query:
    occurrences = DjangoConnectionField(OccurrenceNode)
    occurrence = relay.Node.Field(OccurrenceNode)

    study_groups = DjangoConnectionField(StudyGroupNode)
    study_group = relay.Node.Field(StudyGroupNode)

    venues = DjangoConnectionField(VenueNode)
    venue = graphene.Field(VenueNode, id=graphene.ID(required=True))

    @staticmethod
    def resolve_venue(parent, info, **kwargs):
        return VenueCustomData.objects.get(pk=kwargs.pop("id"))

    enrolments = DjangoConnectionField(EnrolmentNode)
    enrolment = relay.Node.Field(EnrolmentNode)


class Mutation:
    add_occurrence = AddOccurrenceMutation.Field()
    update_occurrence = UpdateOccurrenceMutation.Field()
    delete_occurrence = DeleteOccurrenceMutation.Field()

    add_venue = AddVenueMutation.Field()
    update_venue = UpdateVenueMutation.Field()
    delete_venue = DeleteVenueMutation.Field()

    add_study_group = AddStudyGroupMutation.Field()
    update_study_group = UpdateStudyGroupMutation.Field(
        description="Mutation for admin only"
    )
    delete_study_group = DeleteStudyGroupMutation.Field(
        description="Mutation for admin only"
    )
    enrol_occurrence = EnrolOccurrenceMutation.Field()
    unenrol_occurrence = UnenrolOccurrenceMutation.Field(
        description="Required logged in user for authorization"
    )
