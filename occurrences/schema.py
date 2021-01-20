from datetime import timedelta

import graphene
import requests
from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import get_language
from graphene import Connection, Field, InputObjectType, NonNull, relay
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
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
    VenueCustomData,
)
from organisations.models import Organisation, Person
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
    ApiUsageError,
    CaptchaValidationFailedError,
    DataValidationError,
    EnrolCancelledOccurrenceError,
    EnrolmentClosedError,
    EnrolmentMaxNeededOccurrenceReached,
    EnrolmentNotEnoughCapacityError,
    EnrolmentNotStartedError,
    InvalidStudyGroupSizeError,
    MissingMantatoryInformationError,
    ObjectDoesNotExistError,
)

VenueTranslation = apps.get_model("occurrences", "VenueCustomDataTranslation")
StudyLevelEnum = graphene.Enum(
    "StudyLevel", [(l[0].upper(), l[0]) for l in StudyGroup.STUDY_LEVELS]
)
NotificationTypeEnum = graphene.Enum(
    "NotificationType", [(t[0].upper(), t[0]) for t in NOTIFICATION_TYPES]
)

EnrolmentStatusEnum = graphene.Enum(
    "EnrolmentStatus", [(s[0].upper(), s[0]) for s in Enrolment.STATUSES]
)

OccurrenceSeatTypeEnum = graphene.Enum(
    "SeatType", [(t[0].upper(), t[0]) for t in Occurrence.OCCURRENCE_SEAT_TYPES]
)


class PalvelutarjotinEventNode(DjangoObjectType):
    next_occurrence_datetime = graphene.DateTime()
    last_occurrence_datetime = graphene.DateTime()

    class Meta:
        model = PalvelutarjotinEvent
        interfaces = (relay.Node,)

    def resolve_next_occurrence_datetime(self, info, **kwargs):
        try:
            return (
                self.occurrences.filter(start_time__gte=timezone.now())
                .earliest("start_time")
                .start_time
            )
        except Occurrence.DoesNotExist:
            return None

    def resolve_last_occurrence_datetime(self, info, **kwargs):
        try:
            return self.occurrences.latest("start_time").start_time
        except Occurrence.DoesNotExist:
            return None


class PalvelutarjotinEventInput(InputObjectType):
    enrolment_start = graphene.DateTime()
    enrolment_end_days = graphene.Int()
    needed_occurrences = graphene.Int(required=True)
    contact_person_id = graphene.ID()
    contact_phone_number = graphene.String()
    contact_email = graphene.String()
    auto_acceptance = graphene.Boolean()
    mandatory_additional_information = graphene.Boolean()


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
        description="Translated field in the language defined in request "
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
    remaining_seats = graphene.Int(required=True)
    seats_taken = graphene.Int(required=True)
    seats_approved = graphene.Int(required=True)
    linked_event = Field("graphene_linked_events.schema.Event")

    def resolve_linked_event(self, info, **kwargs):
        response = api_client.retrieve(
            "event", self.p_event.linked_event_id, is_staff=info.context.user.is_staff
        )
        obj = json2obj(format_response(response))
        return obj

    class Meta:
        model = Occurrence
        interfaces = (relay.Node,)
        filterset_class = OccurrenceFilter

    @classmethod
    def get_queryset(cls, queryset, info):
        return super().get_queryset(queryset, info).order_by("start_time")

    def resolve_remaining_seats(self, info, **kwargs):
        return self.amount_of_seats - self.seats_taken


def validate_occurrence_data(kwargs, updated_obj=None):
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
        min_group_size = graphene.Int()
        max_group_size = graphene.Int()
        start_time = graphene.DateTime(required=True)
        end_time = graphene.DateTime(required=True)
        contact_persons = graphene.List(PersonNodeInput)
        p_event_id = graphene.ID(required=True)
        amount_of_seats = graphene.Int(required=True)
        seat_type = OccurrenceSeatTypeEnum()
        languages = NonNull(graphene.List(OccurrenceLanguageInput))

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        validate_occurrence_data(kwargs)
        contact_persons = kwargs.pop("contact_persons", None)
        languages = kwargs.pop("languages", None)
        p_event = get_editable_obj_from_global_id(
            info, kwargs["p_event_id"], PalvelutarjotinEvent
        )
        if p_event.is_published():
            raise ApiUsageError("Cannot add occurrence to published event")
        kwargs["p_event_id"] = p_event.id
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
        amount_of_seats = graphene.Int()
        languages = NonNull(
            graphene.List(OccurrenceLanguageInput),
            description="If present, should include all languages of the occurrence",
        )
        seat_type = OccurrenceSeatTypeEnum()

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence = get_editable_obj_from_global_id(info, kwargs.pop("id"), Occurrence)
        validate_occurrence_data(kwargs, occurrence)
        contact_persons = kwargs.pop("contact_persons", None)
        languages = kwargs.pop("languages", None)
        p_event = occurrence.p_event
        if kwargs.get("p_event_id"):
            p_event = get_editable_obj_from_global_id(
                info, kwargs["p_event_id"], PalvelutarjotinEvent
            )
            kwargs["p_event_id"] = p_event.id
        if p_event.is_published():
            raise ApiUsageError("Cannot update occurrence of published event")
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


class EnrolmentConnectionWithCount(Connection):
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
        interfaces = (relay.Node,)
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
        group_size = (
            1
            if occurrence.seat_type == Occurrence.OCCURRENCE_SEAT_TYPE_ENROLMENT_COUNT
            else study_group.group_size_with_adults()
        )
        if occurrence.seats_taken + group_size > occurrence.amount_of_seats:
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
        description="If person input doesn't include person id, "
        "a new person "
        "object will be created",
    )
    name = graphene.String()
    group_size = graphene.Int(required=True)
    group_name = graphene.String()
    extra_needs = graphene.String()
    amount_of_adult = graphene.Int()
    study_level = StudyLevelEnum()


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
        occurrence_ids = NonNull(
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
        enrolment = get_editable_obj_from_global_id(
            info, kwargs["enrolment_id"], Enrolment
        )
        custom_message = kwargs.pop("custom_message", None)

        # Need to approve all related occurrences of the study group
        enrolments = Enrolment.objects.filter(
            occurrence__p_event=enrolment.occurrence.p_event,
            study_group=enrolment.study_group,
        )
        for e in enrolments:
            if e.occurrence.cancelled:
                raise EnrolCancelledOccurrenceError(
                    "Cannot approve enrolment to cancelled occurrence"
                )
            e.approve(custom_message=custom_message)
        enrolment.refresh_from_db()
        return ApproveEnrolmentMutation(enrolment=enrolment)


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

    cancelling_enrolment = graphene.Field(EnrolmentNode, id=graphene.ID(required=True))

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

    enrolments = DjangoConnectionField(EnrolmentNode)
    enrolment = relay.Node.Field(EnrolmentNode)

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
            qs = qs.filter(status=kwargs["status"])
        return qs


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
    decline_enrolment = DeclineEnrolmentMutation.Field()
