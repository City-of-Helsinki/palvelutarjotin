from datetime import timedelta
from typing import List

import graphene
import requests
from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import get_language
from graphene.utils.str_converters import to_snake_case
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_linked_events.schema import Place
from graphene_linked_events.utils import api_client, format_response, json2obj
from graphql_jwt.decorators import staff_member_required
from occurrences.consts import NOTIFICATION_TYPES
from occurrences.filters import OccurrenceFilter
from occurrences.models import (
    Enrolment,
    Language,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    StudyLevel,
    VenueCustomData,
)
from organisations.models import Organisation, Person
from organisations.schema import PersonNodeInput
from verification_token.models import VerificationToken

from common.utils import (
    get_editable_obj_from_global_id,
    get_node_id_from_global_id,
    get_obj_from_global_id,
    LanguageEnum,
    update_object,
    update_object_with_translations,
)
from palvelutarjotin.exceptions import (
    ApiUsageError,
    CaptchaValidationFailedError,
    DataValidationError,
    EnrolCancelledOccurrenceError,
    EnrolmentClosedError,
    EnrolmentMaxNeededOccurrenceReached,
    EnrolmentNotEnoughCapacityError,
    EnrolmentNotStartedError,
    InvalidStudyGroupSizeError,
    InvalidTokenError,
    MissingMantatoryInformationError,
    ObjectDoesNotExistError,
)


# TODO: Get rid of this when the graphene and django_filters gives the support.
class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    """
    OrderedDjangoFilterConnectionField makes it possible to use
    a filter to order the result nodes.
    Example:
    --------
    query {
        posts(orderBy: "-createdAt") {
            title
        }
    }

    In newer versions of
    graphene, django-graphene and django-filters this feature comes out of the box:
    https://docs.graphene-python.org/projects/django/en/latest/filtering/#ordering

    Example:
    --------
    class UserFilter(FilterSet):
        class Meta:
            model = UserModel

        order_by = OrderingFilter(
            fields=(
                ('name', 'created_at'),
            )
        )
    """

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        order = args.get("orderBy", None)
        if order:
            if type(order) is str:
                snake_order = to_snake_case(order)
            else:
                snake_order = [to_snake_case(o) for o in order]
            qs = qs.order_by(*snake_order)
        return qs


StudyLevelTranslation = apps.get_model("occurrences", "StudyLevelTranslation")
VenueTranslation = apps.get_model("occurrences", "VenueCustomDataTranslation")

NotificationTypeEnum = graphene.Enum(
    "NotificationType", [(t[0].upper(), t[0]) for t in NOTIFICATION_TYPES]
)

EnrolmentStatusEnum = graphene.Enum(
    "EnrolmentStatus", [(s[0].upper(), s[0]) for s in Enrolment.STATUSES]
)

OccurrenceSeatTypeEnum = graphene.Enum(
    "SeatType", [(t[0].upper(), t[0]) for t in Occurrence.OCCURRENCE_SEAT_TYPES]
)


class OccurrenceNode(DjangoObjectType):
    remaining_seats = graphene.Int(required=True)
    seats_taken = graphene.Int(required=True)
    seats_approved = graphene.Int(required=True)
    linked_event = graphene.Field(
        "graphene_linked_events.schema.Event",
        description="Only use this field in single event query for "
        + "best performance.",
    )

    def resolve_linked_event(self, info, **kwargs):
        response = api_client.retrieve(
            "event", self.p_event.linked_event_id, is_staff=info.context.user.is_staff
        )
        obj = json2obj(format_response(response))
        return obj

    class Meta:
        model = Occurrence
        interfaces = (graphene.relay.Node,)
        filterset_class = OccurrenceFilter

    @classmethod
    def get_queryset(cls, queryset, info):
        return super().get_queryset(queryset, info).order_by("start_time")

    def resolve_remaining_seats(self, info, **kwargs):
        return self.amount_of_seats - self.seats_taken


class PalvelutarjotinEventNode(DjangoObjectType):
    next_occurrence_datetime = graphene.DateTime()
    last_occurrence_datetime = graphene.DateTime()
    occurrences = DjangoFilterConnectionField(OccurrenceNode, max_limit=400)

    class Meta:
        model = PalvelutarjotinEvent
        interfaces = (graphene.relay.Node,)

    def resolve_next_occurrence_datetime(self, info, **kwargs):
        try:
            return (
                self.occurrences.filter(start_time__gte=timezone.now(), cancelled=False)
                .earliest("start_time")
                .start_time
            )
        except Occurrence.DoesNotExist:
            return None

    def resolve_last_occurrence_datetime(self, info, **kwargs):
        try:
            return (
                self.occurrences.filter(cancelled=False).latest("start_time").start_time
            )
        except Occurrence.DoesNotExist:
            return None


class PalvelutarjotinEventInput(graphene.InputObjectType):
    enrolment_start = graphene.DateTime()
    enrolment_end_days = graphene.Int()
    external_enrolment_url = graphene.String()
    needed_occurrences = graphene.Int(required=True)
    contact_person_id = graphene.ID()
    contact_phone_number = graphene.String()
    contact_email = graphene.String()
    auto_acceptance = graphene.Boolean()
    mandatory_additional_information = graphene.Boolean()


class StudyLevelTranslationType(DjangoObjectType):
    language_code = LanguageEnum(required=True)

    class Meta:
        model = StudyLevelTranslation
        exclude = ("id", "master")


class StudyLevelNode(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)
    label = graphene.String(
        description="Translated field in the language defined in request "
        "ACCEPT-LANGUAGE header "
    )

    class Meta:
        model = StudyLevel
        interfaces = (graphene.relay.Node,)
        exclude = ("study_groups",)

    @classmethod
    def get_queryset(cls, queryset, info):
        lang = get_language()
        return queryset.language(lang)


class ExternalPlace(graphene.ObjectType):
    name = graphene.Field("graphene_linked_events.schema.LocalisedObject")


class UnitNode(graphene.Union):
    class Meta:

        types = (ExternalPlace, Place)

    @classmethod
    def resolve_type(cls, instance, info):
        if getattr(instance, "_meta", None) == "ExternalPlace":
            return ExternalPlace
        if getattr(instance, "id", None):
            return Place
        return ExternalPlace


class StudyGroupNode(DjangoObjectType):
    class Meta:
        model = StudyGroup
        interfaces = (graphene.relay.Node,)

    unit = graphene.Field(UnitNode)

    @staticmethod
    def resolve_unit(parent, info, **kwargs):
        if parent.unit_id:
            response = api_client.retrieve("place", parent.unit_id)
            return json2obj(format_response(response))
        if parent.unit_name:
            return ExternalPlace(
                name={
                    "fi": parent.unit_name,
                    "sv": parent.unit_name,
                    "en": parent.unit_name,
                }
            )
        return None


class VenueTranslationType(DjangoObjectType):
    language_code = LanguageEnum(required=True)

    class Meta:
        model = VenueTranslation
        exclude = ("id", "master")


class VenueTranslationsInput(graphene.InputObjectType):
    description = graphene.String()
    language_code = LanguageEnum(required=True)


class VenueNode(DjangoObjectType):
    description = graphene.String(
        description="Translated field in the language defined in request "
        "ACCEPT-LANGUAGE header "
    )
    id = graphene.ID(
        source="place_id", description="place_id from linkedEvent", required=True
    )

    class Meta:
        model = VenueCustomData
        interfaces = (graphene.relay.Node,)
        exclude = ("place_id",)

    @classmethod
    def get_queryset(cls, queryset, info):
        lang = get_language()
        return queryset.language(lang)

    @classmethod
    def get_node(cls, info, id):
        return super().get_node(info, id)


class VenueNodeInput(graphene.InputObjectType):
    translations = graphene.List(VenueTranslationsInput)


def validate_occurrence_data(p_event, kwargs, updated_obj=None):
    end_time = (
        kwargs.get("end_time", updated_obj.end_time)
        if updated_obj
        else kwargs["end_time"]
    )
    start_time = (
        kwargs.get("start_time", updated_obj.start_time)
        if updated_obj
        else kwargs["start_time"]
    )
    if end_time <= start_time:
        raise DataValidationError("End time must be after start time")
    minimum_time = (
        (p_event.enrolment_start + timedelta(days=p_event.enrolment_end_days))
        if p_event.enrolment_end_days
        else p_event.enrolment_start
    )
    if minimum_time is not None and start_time < minimum_time:
        raise DataValidationError("Start time cannot be before the enrolment ends")


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


class LanguageNode(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = Language
        exclude = ("occurrences",)
        interfaces = (graphene.relay.Node,)


class LanguageInput(graphene.InputObjectType):
    id = graphene.String()


class AddOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        place_id = graphene.String()
        min_group_size = graphene.Int()
        max_group_size = graphene.Int()
        start_time = graphene.DateTime(required=True)
        end_time = graphene.DateTime(required=True)
        contact_persons = graphene.List(PersonNodeInput)
        p_event_id = graphene.ID(required=True)
        amount_of_seats = graphene.Int(required=True)
        seat_type = OccurrenceSeatTypeEnum()
        languages = graphene.NonNull(graphene.List(LanguageInput))

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        p_event = get_editable_obj_from_global_id(
            info, kwargs["p_event_id"], PalvelutarjotinEvent
        )
        validate_occurrence_data(p_event, kwargs)
        contact_persons = kwargs.pop("contact_persons", None)
        languages = kwargs.pop("languages", None)
        kwargs["p_event_id"] = p_event.id
        occurrence = Occurrence.objects.create(**kwargs)

        if contact_persons:
            add_contact_persons_to_object(info, contact_persons, occurrence)

        if languages:
            occurrence.languages.set(
                _get_instance_list(Language, map(lambda x: x.id.lower(), languages))
            )

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
            description="Should include all contact "
            "persons of the occurrence, "
            "missing contact persons will be "
            "removed during mutation",
        )
        p_event_id = graphene.ID()
        amount_of_seats = graphene.Int()
        languages = graphene.NonNull(
            graphene.List(LanguageInput),
            description="If present, should include all languages of the occurrence",
        )
        seat_type = OccurrenceSeatTypeEnum()

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence = get_editable_obj_from_global_id(info, kwargs.pop("id"), Occurrence)
        p_event = occurrence.p_event
        validate_occurrence_data(p_event, kwargs, occurrence)
        contact_persons = kwargs.pop("contact_persons", None)
        languages = kwargs.pop("languages", None)
        if kwargs.get("p_event_id"):
            p_event = get_editable_obj_from_global_id(
                info, kwargs["p_event_id"], PalvelutarjotinEvent
            )
            kwargs["p_event_id"] = p_event.id
        """
        1. If there are no enrolments done to the occurrence of a published event,
        it should be possible to edit it.
        2. If there are some enrolments done to the published event,
        it should not be editable.
        """
        if p_event.is_published() and occurrence.seats_taken > 0:
            raise ApiUsageError(
                "Cannot update occurrence of published event with enrolments"
            )
        update_object(occurrence, kwargs)
        # Nested update
        if contact_persons:
            add_contact_persons_to_object(info, contact_persons, occurrence)
        if languages:
            occurrence.languages.set(
                _get_instance_list(Language, map(lambda x: x.id.lower(), languages))
            )

        return UpdateOccurrenceMutation(occurrence=occurrence)


class DeleteOccurrenceMutation(graphene.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence = get_editable_obj_from_global_id(info, kwargs.pop("id"), Occurrence)
        if occurrence.p_event.is_published() and not occurrence.cancelled:
            raise ApiUsageError(
                "Cannot delete published occurrence. Event is "
                "published or occurrence is not cancelled"
            )
        occurrence.delete()
        return DeleteOccurrenceMutation()


class CancelOccurrenceMutation(graphene.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        reason = graphene.String()

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence = get_editable_obj_from_global_id(info, kwargs.pop("id"), Occurrence)
        if occurrence.cancelled:
            raise ApiUsageError("Occurrence is already cancelled")
        occurrence.cancel(reason=kwargs.pop("reason", None))

        return CancelOccurrenceMutation(occurrence)


class AddVenueMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(description="Place id from linked event", required=True)
        translations = graphene.List(VenueTranslationsInput)
        has_clothing_storage = graphene.Boolean(required=True)
        has_snack_eating_place = graphene.Boolean(required=True)
        outdoor_activity = graphene.Boolean(required=True)
        has_toilet_nearby = graphene.Boolean(required=True)
        has_area_for_group_work = graphene.Boolean(required=True)
        has_indoor_playing_area = graphene.Boolean(required=True)
        has_outdoor_playing_area = graphene.Boolean(required=True)

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
        outdoor_activity = graphene.Boolean()
        has_toilet_nearby = graphene.Boolean()
        has_area_for_group_work = graphene.Boolean()
        has_indoor_playing_area = graphene.Boolean()
        has_outdoor_playing_area = graphene.Boolean()

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


class EnrolmentConnectionWithCount(graphene.Connection):
    class Meta:
        abstract = True

    count = graphene.Int()

    def resolve_count(root, info, **kwargs):
        return root.length


class EnrolmentNode(DjangoObjectType):
    notification_type = NotificationTypeEnum()
    status = EnrolmentStatusEnum()

    class Meta:
        model = Enrolment
        filter_fields = ["status"]
        interfaces = (graphene.relay.Node,)
        connection_class = EnrolmentConnectionWithCount


def validate_enrolment(study_group, occurrence, new_enrolment=True):
    # Expensive validation are sorted to bottom
    if (
        occurrence.p_event.mandatory_additional_information
        and not study_group.extra_needs
    ):
        raise MissingMantatoryInformationError(
            "This event requires additional information of study group"
        )
    if occurrence.cancelled:
        raise EnrolCancelledOccurrenceError("Cannot enrol cancelled occurrence")
    if (
        occurrence.max_group_size
        and study_group.group_size_with_adults() > occurrence.max_group_size
    ) or (
        occurrence.min_group_size
        and study_group.group_size_with_adults() < occurrence.min_group_size
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
            study_group.occurrences.filter(
                p_event=occurrence.p_event, cancelled=False
            ).count()
            >= occurrence.p_event.needed_occurrences
        ):
            raise EnrolmentMaxNeededOccurrenceReached(
                "Number of enrolled occurrences is greater than the needed occurrences"
            )
    else:
        if occurrence.seats_taken > occurrence.amount_of_seats:
            raise EnrolmentNotEnoughCapacityError(
                "Not enough space for this study group"
            )


class StudyGroupInput(graphene.InputObjectType):
    person = graphene.NonNull(
        PersonNodeInput,
        description="If person input doesn't include person id, "
        "a new person "
        "object will be created",
    )
    unit_id = graphene.String()
    unit_name = graphene.String()
    group_size = graphene.Int(required=True)
    group_name = graphene.String()
    extra_needs = graphene.String()
    amount_of_adult = graphene.Int()
    study_levels = graphene.List(graphene.String)


def verify_captcha(key):
    if not key:
        raise CaptchaValidationFailedError("Missing captcha verification data")
    secret_key = settings.RECAPTCHA_SECRET_KEY
    verify_url = settings.RECAPTCHA_VALIDATION_URL

    # captcha verification
    data = {"response": key, "secret": secret_key}
    resp = requests.post(verify_url, data=data, timeout=5)
    result_json = resp.json()

    if result_json.get("success"):
        return True
    else:
        raise CaptchaValidationFailedError(
            f"Captcha verification failed: {result_json.get('error-codes')}"
        )


class EnrolOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        occurrence_ids = graphene.NonNull(
            graphene.List(graphene.ID), description="Occurrence ids of event"
        )
        study_group = StudyGroupInput(description="Study group data", required=True)
        notification_type = NotificationTypeEnum()
        person = PersonNodeInput(
            description="Leave blank if the contact person is "
            "the same with group contact person"
        )
        captcha_key = graphene.String(
            description="The user response token provided "
            "by the reCAPTCHA client-side "
            "integration",
        )

    enrolments = graphene.List(EnrolmentNode)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        if settings.CAPTCHA_ENABLED:
            verify_captcha(kwargs.pop("captcha_key", None))
        else:
            # UI will always send the captcha,
            # and if it is not removed,
            # it will raise an error.
            kwargs.pop("captcha_key", None)
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

            if occurrence.p_event.auto_acceptance:
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
        # Need to unenrol all related occurrence of the study group
        enrolments = study_group.enrolments.filter(
            occurrence__p_event=occurrence.p_event
        )
        for e in enrolments:
            e.delete()
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

        # Update all related enrolments
        enrolments = Enrolment.objects.filter(
            occurrence__p_event=enrolment.occurrence.p_event,
            study_group=enrolment.study_group,
        )
        for enrolment in enrolments:
            validate_enrolment(study_group, enrolment.occurrence, new_enrolment=False)
            update_object(enrolment, kwargs)

        return UpdateEnrolmentMutation(enrolment=enrolment)


class ApproveEnrolmentMutation(graphene.relay.ClientIDMutation):
    class Input:
        enrolment_id = graphene.GlobalID()
        custom_message = graphene.String()

    enrolment = graphene.Field(EnrolmentNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        e = get_editable_obj_from_global_id(info, kwargs["enrolment_id"], Enrolment)
        custom_message = kwargs.pop("custom_message", None)

        # Do not allow manual approvement if enrolment require more than 1 occurrences
        if e.occurrence.p_event.needed_occurrences > 1:
            raise ApiUsageError(
                "Cannot approve enrolment that requires more than 1 occurrence"
            )
        if e.occurrence.cancelled:
            raise EnrolCancelledOccurrenceError(
                "Cannot approve enrolment to cancelled occurrence"
            )
        e.approve(custom_message=custom_message)
        e.refresh_from_db()
        return ApproveEnrolmentMutation(enrolment=e)


class MassApproveEnrolmentsMutation(graphene.relay.ClientIDMutation):
    class Input:
        enrolment_ids = graphene.NonNull(graphene.List(graphene.ID))
        custom_message = graphene.String()

    enrolments = graphene.NonNull(graphene.List(EnrolmentNode))

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        enrolments = []
        custom_message = kwargs.pop("custom_message", None)
        for enrolment_global_id in kwargs["enrolment_ids"]:
            e = get_editable_obj_from_global_id(info, enrolment_global_id, Enrolment)
            if e.occurrence.p_event.needed_occurrences > 1:
                raise ApiUsageError(
                    "Cannot mass approve enrolment that requires more than 1 "
                    "occurrence"
                )
            if e.occurrence.cancelled:
                raise EnrolCancelledOccurrenceError(
                    "Cannot approve enrolment to cancelled occurrence"
                )
            e.approve(custom_message=custom_message)
            e.refresh_from_db()
            enrolments.append(e)
        return MassApproveEnrolmentsMutation(enrolments=enrolments)


class DeclineEnrolmentMutation(graphene.relay.ClientIDMutation):
    class Input:
        enrolment_id = graphene.GlobalID()
        custom_message = graphene.String()

    enrolment = graphene.Field(EnrolmentNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        enrolment = get_editable_obj_from_global_id(
            info, kwargs["enrolment_id"], Enrolment
        )
        custom_message = kwargs.pop("custom_message", None)
        # Need to decline all related occurrences of the study group
        enrolments = Enrolment.objects.filter(
            occurrence__p_event=enrolment.occurrence.p_event,
            study_group=enrolment.study_group,
        )
        for e in enrolments:
            e.decline(custom_message=custom_message)
        enrolment.refresh_from_db()
        return DeclineEnrolmentMutation(enrolment=enrolment)


class AddStudyGroupMutation(graphene.relay.ClientIDMutation):
    class Input:
        person = graphene.NonNull(
            PersonNodeInput,
            description="If person input doesn't include person id, "
            "a new person "
            "object will be created",
        )
        unit_id = graphene.String()
        unit_name = graphene.String()
        group_size = graphene.Int(required=True)
        group_name = graphene.String()
        extra_needs = graphene.String()
        amount_of_adult = graphene.Int()
        study_levels = graphene.List(graphene.String)

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
        unit_id = graphene.String()
        unit_name = graphene.String()
        group_size = graphene.Int()
        group_name = graphene.String()
        extra_needs = graphene.String()
        amount_of_adult = graphene.Int()
        study_levels = graphene.List(graphene.String)

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


class CancelEnrolmentMutation(graphene.relay.ClientIDMutation):
    class Input:
        unique_id = graphene.ID(required=True)
        token = graphene.String(
            description="Need to be included to actually cancel the enrolment,"
            "without this token, BE only initiate the"
            "cancellation process by sending a confirmation "
            "email to teacher"
        )

    enrolment = graphene.Field(EnrolmentNode)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        unique_id = kwargs["unique_id"]
        token = kwargs.get("token")
        try:
            enrolment = Enrolment.objects.get_by_unique_id(unique_id)
        except Enrolment.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

        if enrolment.occurrence.p_event.needed_occurrences > 1:
            raise ApiUsageError("Cannot cancel multiple-occurrence enrolment")
        if enrolment.status == enrolment.STATUS_CANCELLED:
            raise ApiUsageError(
                f"Enrolment status is already set to {enrolment.status}"
            )

        if not token:
            # Start cancellation process, sending email including token, deactivate
            # old token
            enrolment.create_cancellation_token(deactivate_existing=True)
            enrolment.ask_cancel_confirmation()
        else:
            # Finish cancellation process, change enrolment status
            _verify_enrolment_token(enrolment, token)
            enrolment.cancel()

        return CancelEnrolmentMutation(enrolment=enrolment)


def _verify_enrolment_token(enrolment, token):
    try:
        token_obj = VerificationToken.objects.get(key=token)
    except VerificationToken.DoesNotExist:
        raise InvalidTokenError("Token is invalid or expired")
    if token_obj.content_object != enrolment or not token_obj.is_valid():
        raise InvalidTokenError("Token is invalid or expired")


class Query:
    occurrences = OrderedDjangoFilterConnectionField(
        OccurrenceNode, orderBy=graphene.List(of_type=graphene.String)
    )
    occurrence = graphene.relay.Node.Field(OccurrenceNode)

    study_groups = DjangoConnectionField(StudyGroupNode)
    study_group = graphene.relay.Node.Field(StudyGroupNode)

    study_levels = DjangoConnectionField(StudyLevelNode)
    study_level = graphene.Field(StudyLevelNode, id=graphene.ID(required=True))

    venues = DjangoConnectionField(VenueNode)
    venue = graphene.Field(VenueNode, id=graphene.ID(required=True))

    cancelling_enrolment = graphene.Field(EnrolmentNode, id=graphene.ID(required=True))

    languages = DjangoConnectionField(LanguageNode)
    language = graphene.Field(LanguageNode, id=graphene.ID(required=True))

    @staticmethod
    def resolve_language(parent, info, **kwargs):
        try:
            return Language.objects.get(pk=kwargs["id"])
        except Language.DoesNotExist:
            return None

    @staticmethod
    def resolve_cancelling_enrolment(parent, info, **kwargs):
        try:
            return Enrolment.objects.get_by_unique_id(kwargs["id"])
        except Enrolment.DoesNotExist:
            return None

    @staticmethod
    def resolve_venue(parent, info, **kwargs):
        try:
            return VenueCustomData.objects.get(pk=kwargs.pop("id"))
        except VenueCustomData.DoesNotExist:
            return None

    @staticmethod
    def resolve_study_level(parent, info, **kwargs):
        try:
            return StudyLevel.objects.get(pk=kwargs.pop("id"))
        except StudyLevel.DoesNotExist:
            return None

    enrolments = DjangoConnectionField(EnrolmentNode)
    enrolment = graphene.relay.Node.Field(EnrolmentNode)

    enrolment_summary = DjangoConnectionField(
        EnrolmentNode,
        organisation_id=graphene.ID(required=True),
        status=EnrolmentStatusEnum(),
    )

    @staff_member_required
    def resolve_enrolment_summary(self, info, **kwargs):
        try:
            organisation = get_editable_obj_from_global_id(
                info, kwargs["organisation_id"], Organisation
            )
        except ObjectDoesNotExistError:
            return None
        qs = Enrolment.objects.filter(occurrence__p_event__organisation=organisation)
        if kwargs.get("status"):
            qs = qs.filter(status=kwargs["status"]).order_by("status")
        return qs


def _create_study_group(study_group_data):
    study_levels_data = study_group_data.pop("study_levels")

    person_data = study_group_data.pop("person")
    person = _get_or_create_contact_person(person_data)
    study_group_data["person_id"] = person.id

    study_group = StudyGroup.objects.create(**study_group_data)
    study_group.study_levels.set(
        _get_instance_list(StudyLevel, map(lambda x: x.lower(), study_levels_data))
    )

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

    # Handle a person
    person_data = study_group_data.pop("person", None)
    if person_data:
        person = _get_or_create_contact_person(person_data)
        study_group_data["person_id"] = person.id

    # Handle study levels
    study_levels_data = study_group_data.pop("study_levels", None)
    if study_levels_data:
        study_group_obj.study_levels.set(
            _get_instance_list(StudyLevel, map(lambda x: x.lower(), study_levels_data))
        )

    # update the populated object
    update_object(study_group_obj, study_group_data)
    return study_group_obj


def _get_or_create_contact_person(contact_person_data):
    """
    If a contact person id is given,
    get a contact person with a given non-assignable id
    or else, create a contact person with a given data.
    """
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


def _get_instance_list(ModelClass, instance_pks: List[str]):
    result = []
    for instance_pk in instance_pks:
        try:
            instance = ModelClass.objects.get(pk=instance_pk)
            result.append(instance)
        except ModelClass.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
    return result


class Mutation:
    add_occurrence = AddOccurrenceMutation.Field()
    update_occurrence = UpdateOccurrenceMutation.Field()
    delete_occurrence = DeleteOccurrenceMutation.Field()
    cancel_occurrence = CancelOccurrenceMutation.Field()

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
    mass_approve_enrolments = MassApproveEnrolmentsMutation.Field()
    decline_enrolment = DeclineEnrolmentMutation.Field()

    cancel_enrolment = CancelEnrolmentMutation.Field()
