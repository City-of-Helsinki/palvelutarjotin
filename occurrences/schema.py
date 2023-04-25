import graphene
from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import get_language
from graphene.utils.str_converters import to_snake_case
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import staff_member_required
from typing import List

from common.utils import (
    get_editable_obj_from_global_id,
    get_node_id_from_global_id,
    LanguageEnum,
    update_object,
    update_object_with_translations,
)
from graphene_linked_events.schema import LocalisedObject, Place
from graphene_linked_events.utils import api_client, format_response, json2obj
from occurrences.consts import NOTIFICATION_TYPES
from occurrences.filters import OccurrenceFilter
from occurrences.models import (
    Enrolment,
    EventQueueEnrolment,
    Language,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    StudyLevel,
    VenueCustomData,
)
from occurrences.schema_services import (
    add_contact_persons_to_object,
    create_study_group,
    enrol_to_event_queue,
    enrol_to_occurrence,
    get_instance_list,
    get_node_with_permission_check,
    get_or_create_contact_person,
    update_study_group,
    validate_enrolment,
    validate_occurrence_data,
    verify_captcha,
    verify_enrolment_token,
)
from organisations.models import Organisation
from organisations.schema import PersonNodeInput
from palvelutarjotin.exceptions import (
    ApiUsageError,
    EnrolCancelledOccurrenceError,
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
PalvelutarjotinEventTranslation = apps.get_model(
    "occurrences", "PalvelutarjotinEventTranslation"
)

NotificationTypeEnum = graphene.Enum(
    "NotificationType", [(t[0].upper(), t[0]) for t in NOTIFICATION_TYPES]
)

EnrolmentStatusEnum = graphene.Enum(
    "EnrolmentStatus", [(s[0].upper(), s[0]) for s in Enrolment.STATUSES]
)

EventQueueEnrolmentStatusEnum = graphene.Enum(
    "EventQueueEnrolmentStatus",
    [(s[0].upper(), s[0]) for s in EventQueueEnrolment.QUEUE_STATUSES],
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


class PalvelutarjotinEventTranslationType(DjangoObjectType):
    language_code = LanguageEnum(required=True)
    auto_acceptance_message = graphene.String(required=True)

    class Meta:
        model = PalvelutarjotinEventTranslation
        exclude = ("id", "master")


class PalvelutarjotinEventNode(DjangoObjectType):
    next_occurrence_datetime = graphene.DateTime()
    last_occurrence_datetime = graphene.DateTime()
    occurrences = OrderedDjangoFilterConnectionField(
        OccurrenceNode, orderBy=graphene.List(of_type=graphene.String), max_limit=400
    )
    auto_acceptance_message = graphene.String(
        description="Translated field in the language defined in request "
        "ACCEPT-LANGUAGE header "
    )
    translations = graphene.List(PalvelutarjotinEventTranslationType)

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

    def resolve_translations(self, info, **kwargs):
        return self.translations.all()

    @classmethod
    def get_queryset(cls, queryset, info):
        lang = get_language()
        return queryset.language(lang)

    @classmethod
    def get_node(cls, info, id):
        return super().get_node(info, id)


class PalvelutarjotinEventTranslationsInput(graphene.InputObjectType):
    auto_acceptance_message = graphene.String(
        description="A custom message included in notification template "
        "when auto acceptance is set on.",
    )
    language_code = LanguageEnum(required=True)


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
    translations = graphene.List(PalvelutarjotinEventTranslationsInput)


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
    name = graphene.Field(LocalisedObject)


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

    @classmethod
    @staff_member_required
    def get_queryset(cls, queryset, info):
        """
        The study groups are available only for the staff members.
        Also the staff member should get only the study groups
        participating in event of an organisation
        he has access to. So, the study groups list should be
        filtered by the organisation
        """
        return (
            super()
            .get_queryset(queryset, info)
            .filter_by_current_user_organisations(info.context.user)
        )

    @classmethod
    @staff_member_required
    def get_node(cls, info, id):
        """
        The study group is available only for the staff members.
        Also the staff member should get only the study groups
        participating in event of an organisation
        he has access to. So, the study groups list should be
        filtered by the organisation
        """
        node = super().get_node(info, id)
        return get_node_with_permission_check(node, info)


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
                get_instance_list(Language, map(lambda x: x.id.lower(), languages))
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
                get_instance_list(Language, map(lambda x: x.id.lower(), languages))
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
        filter_fields = ["status", "occurrence_id"]
        interfaces = (graphene.relay.Node,)
        connection_class = EnrolmentConnectionWithCount

    @classmethod
    @staff_member_required
    def get_queryset(cls, queryset, info):
        """
        The enrolments are available only for the staff members.
        Also the staff member should get only the enrolments
        done to the occurrences provided by an organisation
        he has access to. So, the enrolments list should be
        filtered by the organisation
        """
        return (
            super()
            .get_queryset(queryset, info)
            .filter_by_current_user_organisations(info.context.user)
        )

    @classmethod
    @staff_member_required
    def get_node(cls, info, id):
        """
        The enrolment is available only for the staff members.
        Also the staff member should get only the enrolments
        done to the occurrences provided by an organisation
        he has access to. So, the enrolments list should be
        filtered by the organisation
        """
        node = super().get_node(info, id)
        return get_node_with_permission_check(node, info)


class EventQueueEnrolmentNode(DjangoObjectType):
    notification_type = NotificationTypeEnum()
    status = EventQueueEnrolmentStatusEnum()

    class Meta:
        model = EventQueueEnrolment
        filter_fields = ["p_event_id"]
        interfaces = (graphene.relay.Node,)
        connection_class = EnrolmentConnectionWithCount

    @classmethod
    @staff_member_required
    def get_queryset(cls, queryset, info):
        return super().get_queryset(queryset, info)


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


class EnrolInputBase:
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


class EnrolEventQueueMutation(graphene.relay.ClientIDMutation):
    class Input(EnrolInputBase):
        p_event_id = graphene.ID(
            required=True, description="The event that a group would like to queue to"
        )

    event_queue_enrolment = graphene.Field(EventQueueEnrolmentNode)

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
        p_event_id = get_node_id_from_global_id(
            kwargs.pop("p_event_id"), "PalvelutarjotinEventNode"
        )
        p_event = PalvelutarjotinEvent.objects.get(id=p_event_id)
        study_group = create_study_group(kwargs.pop("study_group"))
        contact_person_data = kwargs.pop("person", None)
        notification_type = kwargs.pop(
            "notification_type",
            EventQueueEnrolment._meta.get_field("notification_type").get_default(),
        )
        # Use group contact person if person data not submitted
        if contact_person_data:
            person = get_or_create_contact_person(contact_person_data)
        else:
            person = study_group.person
        event_queue_enrolment = enrol_to_event_queue(
            study_group=study_group,
            p_event=p_event,
            person=person,
            notification_type=notification_type,
        )
        return EnrolEventQueueMutation(event_queue_enrolment=event_queue_enrolment)


class UnenrolEventQueueMutation(graphene.relay.ClientIDMutation):
    class Input:
        p_event_id = graphene.GlobalID()
        study_group_id = graphene.GlobalID(description="Study group id")

    p_event = graphene.Field(PalvelutarjotinEventNode)
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
        p_event = get_editable_obj_from_global_id(
            info, kwargs["p_event_id"], PalvelutarjotinEvent
        )
        # Need to unenrol all related occurrence of the study group
        enrolments = study_group.queued_enrolments.filter(p_event=p_event)
        for e in enrolments:
            e.delete()
        return UnenrolEventQueueMutation(study_group=study_group, p_event=p_event)


class EnrolOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input(EnrolInputBase):
        occurrence_ids = graphene.NonNull(
            graphene.List(graphene.ID), description="Occurrence ids of event"
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
        study_group = create_study_group(kwargs.pop("study_group"))
        contact_person_data = kwargs.pop("person", None)
        notification_type = kwargs.pop(
            "notification_type",
            Enrolment._meta.get_field("notification_type").get_default(),
        )
        occurrence_ids = [
            get_node_id_from_global_id(occurrence_gid, "OccurrenceNode")
            for occurrence_gid in kwargs.pop("occurrence_ids")
        ]
        occurrences = get_instance_list(Occurrence, occurrence_ids)
        # Use group contact person if person data not submitted
        if contact_person_data:
            person = get_or_create_contact_person(contact_person_data)
        else:
            person = study_group.person

        enrolments = enrol_to_occurrence(
            study_group=study_group,
            occurrences=occurrences,
            person=person,
            notification_type=notification_type,
        )
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
            update_study_group(study_group_data, study_group)

        contact_person_data = kwargs.pop("person", None)
        # Use latest group contact person if person data not submitted
        if contact_person_data:
            person = get_or_create_contact_person(contact_person_data)
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
        enrolments: List[Enrolment] = []
        custom_message = kwargs.pop("custom_message", None)
        for enrolment_global_id in kwargs["enrolment_ids"]:
            e: Enrolment = get_editable_obj_from_global_id(
                info, enrolment_global_id, Enrolment
            )
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
        study_group = create_study_group(kwargs)
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
        study_group = update_study_group(kwargs)
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
            verify_enrolment_token(enrolment, token)
            enrolment.cancel()

        return CancelEnrolmentMutation(enrolment=enrolment)


class Query:
    occurrences = OrderedDjangoFilterConnectionField(
        OccurrenceNode, orderBy=graphene.List(of_type=graphene.String)
    )
    occurrence = graphene.relay.Node.Field(OccurrenceNode)

    study_levels = DjangoConnectionField(StudyLevelNode)
    study_level = graphene.Field(StudyLevelNode, id=graphene.ID(required=True))

    venues = DjangoConnectionField(VenueNode)
    venue = graphene.Field(VenueNode, id=graphene.ID(required=True))

    cancelling_enrolment = graphene.Field(EnrolmentNode, id=graphene.ID(required=True))

    languages = DjangoConnectionField(LanguageNode)
    language = graphene.Field(LanguageNode, id=graphene.ID(required=True))

    # TODO: Remove this as unused
    enrolments = OrderedDjangoFilterConnectionField(
        EnrolmentNode,
        orderBy=graphene.List(of_type=graphene.String),
        description="Query for admin only",
    )
    # TODO: Get rid of this. It seems it's still in use in Admin-UI.
    enrolment = graphene.relay.Node.Field(
        EnrolmentNode, description="Query for admin only"
    )

    enrolment_summary = DjangoConnectionField(
        EnrolmentNode,
        organisation_id=graphene.ID(required=True),
        status=EnrolmentStatusEnum(),
    )

    # TODO: Check the organisation permissions
    event_queue_enrolments = OrderedDjangoFilterConnectionField(
        EventQueueEnrolmentNode,
        orderBy=graphene.List(of_type=graphene.String),
        description="Query for admin only",
    )
    # TODO: Check the organisation permissions
    event_queue_enrolment = graphene.relay.Node.Field(
        EventQueueEnrolmentNode, description="Query for admin only"
    )

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

    @staticmethod
    @staff_member_required
    def resolve_enrolments(parent, info, **kwargs):
        qs = Enrolment.objects.all()
        if kwargs.get("occurrence_id"):
            try:
                occurrence = Occurrence.objects.get(
                    pk=get_node_id_from_global_id(
                        kwargs["occurrence_id"], "OccurrenceNode"
                    )
                )
            except Occurrence.DoesNotExist:
                return None
            qs = qs.filter(occurrence=occurrence)
        if kwargs.get("status"):
            status = kwargs["status"].lower()
            qs = qs.filter(status=status)
        return qs

    @staff_member_required
    def resolve_enrolment_summary(self, info, **kwargs):
        try:
            organisation = get_editable_obj_from_global_id(
                info, kwargs["organisation_id"], Organisation
            )
        except ObjectDoesNotExistError:
            return None
        qs = Enrolment.objects.filter(
            occurrence__p_event__organisation=organisation
        ).order_by("status")
        if kwargs.get("status"):
            qs = qs.filter(status=kwargs["status"])
        return qs


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
    enrol_event_queue = EnrolEventQueueMutation.Field()
    unenrol_event_queue = UnenrolEventQueueMutation.Field()
