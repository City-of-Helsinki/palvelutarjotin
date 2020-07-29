from datetime import timedelta

import graphene
from django.apps import apps
from django.db import transaction
from django.utils import timezone
from django.utils.translation import get_language
from graphene import InputObjectType, NonNull, relay
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import staff_member_required
from occurrences.consts import NOTIFICATION_TYPES
from occurrences.filters import OccurrenceFilter
from occurrences.models import (
    Enrolment,
    Language,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    VenueCustomData,
)
from organisations.models import Person
from organisations.schema import PersonNodeInput

from common.utils import (
    get_editable_obj_from_global_id,
    get_node_id_from_global_id,
    get_obj_from_global_id,
    LanguageEnum,
    update_object,
    update_object_with_translations,
)
from palvelutarjotin.exceptions import (
    EnrolmentClosedError,
    EnrolmentMaxNeededOccurrenceReached,
    EnrolmentNotEnoughCapacityError,
    EnrolmentNotStartedError,
    InvalidStudyGroupSizeError,
    ObjectDoesNotExistError,
)

VenueTranslation = apps.get_model("occurrences", "VenueCustomDataTranslation")
StudyLevelEnum = graphene.Enum(
    "StudyLevel", [(l[0].upper(), l[0]) for l in StudyGroup.STUDY_LEVELS]
)
NotificationTypeEnum = graphene.Enum(
    "NotificationType", [(t[0].upper(), t[0]) for t in NOTIFICATION_TYPES]
)


class PalvelutarjotinEventNode(DjangoObjectType):
    class Meta:
        model = PalvelutarjotinEvent
        interfaces = (relay.Node,)


class PalvelutarjotinEventInput(InputObjectType):
    enrolment_start = graphene.DateTime()
    enrolment_end_days = graphene.Int()
    duration = graphene.Int(required=True)
    needed_occurrences = graphene.Int(required=True)
    contact_person_id = graphene.ID()
    contact_phone_number = graphene.String()
    contact_email = graphene.String()


class StudyGroupNode(DjangoObjectType):
    study_level = StudyLevelEnum()

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
        filterset_class = OccurrenceFilter

    @classmethod
    def get_queryset(cls, queryset, info):
        return super().get_queryset(queryset, info).order_by("start_time")

    def resolve_remaining_seats(self, info, **kwargs):
        return self.amount_of_seats - self.seats_taken


def validate_occurrence_data(kwargs):
    # TODO: Validate place_id, languages ...
    pass


@transaction.atomic
def add_contact_persons_to_object(info, contact_persons, obj):
    obj.contact_persons.clear()
    for p in contact_persons:
        p_global_id = p.get("id", None)
        if p_global_id:
            person = get_obj_from_global_id(info, p_global_id, Person)
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
        place_id = graphene.String()
        min_group_size = graphene.Int(required=True)
        max_group_size = graphene.Int(required=True)
        start_time = graphene.DateTime(required=True)
        end_time = graphene.DateTime(required=True)
        contact_persons = graphene.List(PersonNodeInput)
        p_event_id = graphene.ID(required=True)
        auto_acceptance = graphene.Boolean(required=True)
        amount_of_seats = graphene.Int(required=True)
        languages = NonNull(graphene.List(OccurrenceLanguageInput))

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        validate_occurrence_data(kwargs)
        contact_persons = kwargs.pop("contact_persons", None)
        languages = kwargs.pop("languages", None)
        kwargs["p_event_id"] = get_editable_obj_from_global_id(
            info, kwargs["p_event_id"], PalvelutarjotinEvent
        ).id
        occurrence = Occurrence.objects.create(**kwargs)

        if contact_persons:
            add_contact_persons_to_object(info, contact_persons, occurrence)

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
        contact_persons = graphene.List(
            PersonNodeInput,
            description="Should include all contact persons of the occurrence, "
            "missing contact persons will be removed during mutation",
        )
        p_event_id = graphene.ID()
        auto_acceptance = graphene.Boolean()
        amount_of_seats = graphene.Int()
        languages = NonNull(
            graphene.List(OccurrenceLanguageInput),
            description="If present, should include all languages of the occurrence",
        )

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence = get_editable_obj_from_global_id(info, kwargs.pop("id"), Occurrence)
        contact_persons = kwargs.pop("contact_persons", None)
        languages = kwargs.pop("languages", None)
        kwargs["p_event_id"] = get_editable_obj_from_global_id(
            info, kwargs["p_event_id"], PalvelutarjotinEvent
        ).id

        update_object(occurrence, kwargs)
        # Nested update
        if contact_persons:
            add_contact_persons_to_object(info, contact_persons, occurrence)
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
        occurrence = get_editable_obj_from_global_id(info, kwargs.pop("id"), Occurrence)
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
    notification_type = NotificationTypeEnum()

    class Meta:
        model = Enrolment
        interfaces = (relay.Node,)


def validate_enrolment(study_group, occurrence, new_enrolment=True):
    # Expensive validation are sorted to bottom
    if (
        study_group.group_size > occurrence.max_group_size
        or study_group.group_size < occurrence.min_group_size
    ):
        raise InvalidStudyGroupSizeError(
            "Study group size not match occurrence group size"
        )
    if not occurrence.p_event.enrolment_start or (
        timezone.now() < occurrence.p_event.enrolment_start
    ):
        raise EnrolmentNotStartedError("Enrolment is not opened")
    if timezone.now() > occurrence.start_time - timedelta(
        days=occurrence.p_event.enrolment_end_days
    ):
        raise EnrolmentClosedError("Enrolment has been closed")
    # Skip these validations when updating enrolment
    if new_enrolment:
        if (
            study_group.occurrences.filter(p_event=occurrence.p_event).count()
            >= occurrence.p_event.needed_occurrences
        ):
            raise EnrolmentMaxNeededOccurrenceReached(
                "Number of enroled occurrences greater than needed occurrences"
            )
        if occurrence.seats_taken + study_group.group_size > occurrence.amount_of_seats:
            raise EnrolmentNotEnoughCapacityError(
                "Not enough space for this study group"
            )
    else:
        if occurrence.seats_taken > occurrence.amount_of_seats:
            raise EnrolmentNotEnoughCapacityError(
                "Not enough space for this study group"
            )


class StudyGroupInput(InputObjectType):
    person = NonNull(
        PersonNodeInput,
        description="If person input doesn't include person id, a new person "
        "object will be created",
    )
    name = graphene.String()
    group_size = graphene.Int(required=True)
    group_name = graphene.String()
    extra_needs = graphene.String()
    amount_of_adult = graphene.Int()
    study_level = StudyLevelEnum()


class EnrolOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        occurrence_ids = NonNull(
            graphene.List(graphene.ID), description="Occurrence ids of event"
        )
        study_group = StudyGroupInput(description="Study group data", required=True)
        notification_type = NotificationTypeEnum()
        person = PersonNodeInput(
            description="Leave blank if the contact person is "
            "the same with group contact person"
        )

    enrolments = graphene.List(EnrolmentNode)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence_gids = kwargs.pop("occurrence_ids")
        study_group = _create_study_group(kwargs.pop("study_group"))
        contact_person_data = kwargs.pop("person", None)
        enrolments = []
        for occurrence_gid in occurrence_gids:
            occurrence_id = get_node_id_from_global_id(occurrence_gid, "OccurrenceNode")
            try:
                occurrence = Occurrence.objects.get(pk=occurrence_id)
            except Occurrence.DoesNotExist as e:
                raise ObjectDoesNotExistError(e)
            # Use group contact person if person data not submitted
            if contact_person_data:
                person = _get_or_create_contact_person(contact_person_data)
            else:
                person = study_group.person

            validate_enrolment(study_group, occurrence)

            enrolment = Enrolment.objects.create(
                study_group=study_group, occurrence=occurrence, person=person, **kwargs
            )

            if occurrence.auto_acceptance:
                enrolment.approve()
            enrolments.append(enrolment)

        return EnrolOccurrenceMutation(enrolments=enrolments)


class UnenrolOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        occurrence_id = graphene.GlobalID(description="Occurrence id of event")
        study_group_id = graphene.GlobalID(description="Study group id")

    occurrence = graphene.Field(OccurrenceNode)
    study_group = graphene.Field(StudyGroupNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        group_id = get_node_id_from_global_id(
            kwargs["study_group_id"], "StudyGroupNode"
        )
        try:
            study_group = StudyGroup.objects.get(pk=group_id)
        except StudyGroup.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        occurrence = get_editable_obj_from_global_id(
            info, kwargs["occurrence_id"], Occurrence
        )
        occurrence.study_groups.remove(study_group)
        return UnenrolOccurrenceMutation(study_group=study_group, occurrence=occurrence)


class UpdateEnrolmentMutation(graphene.relay.ClientIDMutation):
    class Input:
        enrolment_id = graphene.GlobalID()
        notification_type = NotificationTypeEnum()
        study_group = StudyGroupInput(description="Study group input")
        person = PersonNodeInput(
            description="Leave blank if the contact person is "
            "the same with group contact person"
        )

    enrolment = graphene.Field(EnrolmentNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        enrolment = get_editable_obj_from_global_id(
            info, kwargs.pop("enrolment_id"), Enrolment
        )
        study_group = enrolment.study_group
        study_group_data = kwargs.pop("study_group", None)
        if study_group_data:
            _update_study_group(study_group_data, study_group)

        contact_person_data = kwargs.pop("person", None)
        # Use latest group contact person if person data not submitted
        if contact_person_data:
            person = _get_or_create_contact_person(contact_person_data)
        else:
            person = study_group.person
        kwargs["person_id"] = person.id

        validate_enrolment(study_group, enrolment.occurrence, new_enrolment=False)
        update_object(enrolment, kwargs)
        return UpdateEnrolmentMutation(enrolment=enrolment)


class ApproveEnrolmentMutation(graphene.relay.ClientIDMutation):
    class Input:
        enrolment_id = graphene.GlobalID()

    enrolment = graphene.Field(EnrolmentNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        enrolment = get_editable_obj_from_global_id(
            info, kwargs["enrolment_id"], Enrolment
        )
        enrolment.approve()
        return ApproveEnrolmentMutation(enrolment=enrolment)


class DeclineEnrolmentMutation(graphene.relay.ClientIDMutation):
    class Input:
        enrolment_id = graphene.GlobalID()

    enrolment = graphene.Field(EnrolmentNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        enrolment = get_editable_obj_from_global_id(
            info, kwargs["enrolment_id"], Enrolment
        )
        enrolment.decline()
        return DeclineEnrolmentMutation(enrolment=enrolment)


class AddStudyGroupMutation(graphene.relay.ClientIDMutation):
    class Input:
        person = NonNull(
            PersonNodeInput,
            description="If person input doesn't include person id, a new person "
            "object will be created",
        )
        name = graphene.String()
        group_size = graphene.Int(required=True)
        group_name = graphene.String()
        extra_needs = graphene.String()
        amount_of_adult = graphene.Int()
        study_level = StudyLevelEnum()

    study_group = graphene.Field(StudyGroupNode)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        study_group = _create_study_group(kwargs)
        return AddStudyGroupMutation(study_group=study_group)


class UpdateStudyGroupMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        person = PersonNodeInput()
        name = graphene.String()
        group_size = graphene.Int()
        group_name = graphene.String()
        extra_needs = graphene.String()
        amount_of_adult = graphene.Int()
        study_level = StudyLevelEnum()

    study_group = graphene.Field(StudyGroupNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        study_group = _update_study_group(kwargs)
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
    occurrences = DjangoFilterConnectionField(OccurrenceNode)
    occurrence = relay.Node.Field(OccurrenceNode)

    study_groups = DjangoConnectionField(StudyGroupNode)
    study_group = relay.Node.Field(StudyGroupNode)

    venues = DjangoConnectionField(VenueNode)
    venue = graphene.Field(VenueNode, id=graphene.ID(required=True))

    @staticmethod
    def resolve_venue(parent, info, **kwargs):
        try:
            return VenueCustomData.objects.get(pk=kwargs.pop("id"))
        except VenueCustomData.DoesNotExist:
            return None

    enrolments = DjangoConnectionField(EnrolmentNode)
    enrolment = relay.Node.Field(EnrolmentNode)


def _create_study_group(study_group_data):
    person_data = study_group_data.pop("person")
    person = _get_or_create_contact_person(person_data)
    study_group_data["person_id"] = person.id
    study_group = StudyGroup.objects.create(**study_group_data)
    return study_group


def _update_study_group(study_group_data, study_group_obj=None):
    if not study_group_obj:
        study_group_global_id = study_group_data.pop("id")
        study_group_id = get_node_id_from_global_id(
            study_group_global_id, "StudyGroupNode"
        )
        try:
            study_group_obj = StudyGroup.objects.get(id=study_group_id)
        except StudyGroup.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

    person_data = study_group_data.pop("person", None)
    if person_data:
        person = _get_or_create_contact_person(person_data)
        study_group_data["person_id"] = person.id
    update_object(study_group_obj, study_group_data)
    return study_group_obj


def _get_or_create_contact_person(contact_person_data):
    if contact_person_data.get("id"):
        person_id = get_node_id_from_global_id(
            contact_person_data.get("id"), "PersonNode"
        )
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
    else:
        person = Person.objects.create(**contact_person_data)
    return person


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
        description="Only staff can unenrol study group"
    )

    update_enrolment = UpdateEnrolmentMutation.Field()
    approve_enrolment = ApproveEnrolmentMutation.Field()
    decline_enrolment = DeclineEnrolmentMutation.Field()
