import logging
import warnings
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models, transaction
from django.db.models import Count, F, Max, OuterRef, Q, Subquery, Sum
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _
from graphql_relay import to_global_id
from helsinki_gdpr.models import SerializableMixin
from parler.models import TranslatedFields
from requests.exceptions import HTTPError
from typing import List, Optional

import occurrences.notification_services as occurrences_services
from common.models import (
    SubqueryCount,
    TimestampedModel,
    TranslatableModel,
    TranslatableQuerySet,
    WithDeletablePersonModel,
)
from common.utils import get_node_id_from_global_id
from gdpr.models import GDPRModel
from graphene_linked_events.utils import retrieve_linked_events_data
from occurrences.consts import (
    NOTIFICATION_TYPE_EMAIL,
    NOTIFICATION_TYPES,
    NotificationTemplate,
)
from occurrences.event_api_services import (
    get_event_time_range_from_occurrences,
    resolve_unit_name_with_unit_id,
    send_event_republish,
    send_event_unpublish,
)
from organisations.models import Person, User
from palvelutarjotin.exceptions import (
    ApiUsageError,
    EnrolmentNotEnoughCapacityError,
    ObjectDoesNotExistError,
)
from verification_token.models import VerificationToken

logger = logging.getLogger(__name__)


class Language(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(verbose_name=_("name"), max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")
        ordering = (
            "name",
            "id",
        )


class PalvelutarjotinEventQueryset(TranslatableQuerySet):
    def contact_info_retention_period_exceeded(self):
        earliest_valid_timestamp = timezone.now() - relativedelta(
            months=settings.PERSONAL_DATA_RETENTION_PERIOD_MONTHS
        )

        return (
            self.annotate(max_occurrence_end_time=Max("occurrences__end_time"))
            .filter(contact_info_deleted_at=None)
            .filter(
                Q(max_occurrence_end_time__lt=earliest_valid_timestamp)
                | (
                    Q(max_occurrence_end_time=None)
                    & Q(created_at__lt=earliest_valid_timestamp)
                )
            )
        )

    def filter_with_contact_info(self, person: Person):
        if not person.email_address and not person.phone_number:
            raise ValueError(
                "The person must have at least an email address or a phone number."
            )
        return self.filter(
            Q(contact_person__email_address=person.email_address)
            | Q(contact_person__phone_number=person.phone_number)
            | Q(contact_email=person.email_address)
            | Q(contact_phone_number=person.phone_number)
        ).order_by("contact_person", "contact_email", "contact_phone_number")

    def delete_contact_info(self, now=None):
        if not now:
            now = timezone.now()
        return self.update(
            contact_person=None,
            contact_email="",
            contact_phone_number="",
            contact_info_deleted_at=now,
        )

    def with_next_occurrence_start_time(self):
        next_occurrences = Occurrence.objects.filter(
            p_event=OuterRef("pk"), start_time__gte=timezone.now(), cancelled=False
        ).order_by("start_time")

        return self.annotate(
            next_occurrence_start_time=Subquery(
                next_occurrences.values("start_time")[:1]
            )
        )


class PalvelutarjotinEvent(
    GDPRModel, SerializableMixin, TranslatableModel, TimestampedModel
):
    PUBLICATION_STATUS_PUBLIC = "public"
    PUBLICATION_STATUS_DRAFT = "draft"
    PUBLICATION_STATUSES = (
        (PUBLICATION_STATUS_PUBLIC, _("public")),
        (PUBLICATION_STATUS_DRAFT, _("draft")),
    )
    linked_event_id = models.CharField(
        max_length=255, verbose_name=_("linked event id"), unique=True
    )
    # TODO: enrolment_start should be replaces with LinkedEvents V2 Event model's field
    enrolment_start = models.DateTimeField(
        verbose_name=_("enrolment start"), blank=True, null=True
    )
    # Enrolment will be close x days before the occurrence start
    enrolment_end_days = models.PositiveSmallIntegerField(
        verbose_name=_("enrolment end days"), blank=True, null=True
    )
    external_enrolment_url = models.URLField(
        verbose_name=_("enrolment url"), blank=True, null=True
    )
    needed_occurrences = models.PositiveSmallIntegerField(
        verbose_name=_("needed occurrence"), default=1
    )
    organisation = models.ForeignKey(
        "organisations.Organisation",
        verbose_name=_("organisation"),
        related_name="p_event",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    contact_person = models.ForeignKey(
        "organisations.Person",
        verbose_name=_("contact person"),
        related_name="p_event",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    contact_phone_number = models.CharField(
        verbose_name=_("contact phone number"), max_length=64, blank=True
    )
    contact_email = models.EmailField(
        max_length=255, verbose_name=_("contact email"), blank=True
    )
    contact_info_deleted_at = models.DateTimeField(
        verbose_name=_("contact info deleted at"), blank=True, null=True
    )
    auto_acceptance = models.BooleanField(
        default=False, verbose_name=_("auto acceptance")
    )
    mandatory_additional_information = models.BooleanField(
        default=False, verbose_name=_("mandatory additional information")
    )
    is_queueing_allowed = models.BooleanField(
        default=True, verbose_name=_("is queueing to event allowed?")
    )

    translations = TranslatedFields(
        auto_acceptance_message=models.TextField(
            _("custom message in auto acceptance"),
            blank=True,
            null=True,
            help_text=_(
                "A custom message included in notification template when auto acceptance is set on."  # noqa
            ),
        )
    )

    objects = SerializableMixin.SerializableManager.from_queryset(
        PalvelutarjotinEventQueryset
    )()

    serialize_fields = (
        {"name": "linked_event_id"},
        {"name": "organisation", "accessor": lambda org: org.name},
        {
            "name": "contact_person",
            "accessor": lambda p: f"{p.name}, {p.phone_number}, {p.email_address}",
        },  # avoid bidirectional serialization, because it wil lend in a forever lopp.
    )
    gdpr_sensitive_data_fields = []

    class Meta:
        verbose_name = _("palvelutarjotin event")
        verbose_name_plural = _("palvelutarjotin events")
        indexes = [
            models.Index(fields=["enrolment_start"], name="enrolment_start_idx"),
            models.Index(
                fields=["is_queueing_allowed"], name="is_queueing_allowed_idx"
            ),
        ]

    def __str__(self):
        return f"{self.id} {self.linked_event_id}"

    def save(self, *args, **kwargs):
        if self.contact_info_deleted_at and (
            self.contact_person or self.contact_email or self.contact_phone_number
        ):
            self.contact_info_deleted_at = None
        return super().save(*args, **kwargs)

    def get_event_data(self, is_staff=False):
        # We need query event location as well
        params = {"include": "location"}
        try:
            data = retrieve_linked_events_data(
                "event", self.linked_event_id, params=params, is_staff=is_staff
            )
        except ObjectDoesNotExistError:
            return None
        except HTTPError as e:
            logger.warning(
                "Could not retrieve the linked events data "
                f"with linked_event_id {self.linked_event_id}. Error: {e}"
            )
            return None

        return data

    def is_editable_by_user(self, user):
        if self.organisation:
            return user.person.organisations.filter(id=self.organisation.id).exists()
        return True

    def is_published(self):
        event = self.get_event_data(is_staff=True)
        if not event:
            return False
        return (
            event.publication_status == PalvelutarjotinEvent.PUBLICATION_STATUS_PUBLIC
        )

    def get_link_to_provider_ui(self, language=settings.LANGUAGE_CODE):
        return (
            f"{settings.KULTUS_PROVIDER_UI_BASE_URL}{language}/events/"
            f"{self.linked_event_id}"
        )

    def get_link_to_teacher_ui(self, language=settings.LANGUAGE_CODE):
        return (
            f"{settings.KULTUS_TEACHER_UI_BASE_URL}{language}/events/"
            f"{self.linked_event_id}"
        )

    def get_event_languages_from_occurrence(self):
        return Language.objects.filter(
            occurrences__in=self.occurrences.all()
        ).distinct()


class OccurrenceQueryset(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()


class Occurrence(GDPRModel, SerializableMixin, TimestampedModel):
    OCCURRENCE_SEAT_TYPE_CHILDREN_COUNT = "children_count"
    OCCURRENCE_SEAT_TYPE_ENROLMENT_COUNT = "enrolment_count"

    OCCURRENCE_SEAT_TYPES = (
        (OCCURRENCE_SEAT_TYPE_CHILDREN_COUNT, _("children count")),
        (OCCURRENCE_SEAT_TYPE_ENROLMENT_COUNT, _("enrolment count")),
    )
    p_event = models.ForeignKey(
        PalvelutarjotinEvent,
        verbose_name=_("palvelutarjotin event"),
        related_name="occurrences",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    min_group_size = models.PositiveSmallIntegerField(
        verbose_name=_("min group size"), blank=True, null=True
    )
    max_group_size = models.PositiveSmallIntegerField(
        verbose_name=_("max group size"), blank=True, null=True
    )
    start_time = models.DateTimeField(verbose_name=_("start time"))
    end_time = models.DateTimeField(verbose_name=_("end time"))
    contact_persons = models.ManyToManyField(
        "organisations.Person",
        related_name="occurrences",
        verbose_name=_("contact persons"),
        blank=True,
    )
    study_groups = models.ManyToManyField(
        "StudyGroup",
        through="Enrolment",
        related_name="occurrences",
        verbose_name=_("study group"),
        blank=True,
    )
    place_id = models.CharField(max_length=255, verbose_name=_("place id"), blank=True)
    amount_of_seats = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("amount of seats")
    )

    languages = models.ManyToManyField(
        "Language", verbose_name=_("languages"), blank=True, related_name="occurrences"
    )
    cancelled = models.BooleanField(verbose_name=_("cancelled"), default=False)
    seat_type = models.CharField(
        max_length=64,
        verbose_name=_("seat type"),
        choices=OCCURRENCE_SEAT_TYPES,
        default=OCCURRENCE_SEAT_TYPE_CHILDREN_COUNT,
    )

    objects = SerializableMixin.SerializableManager.from_queryset(OccurrenceQueryset)()

    serialize_fields = (
        {"name": "start_time", "accessor": lambda t: t.isoformat() if t else None},
        {"name": "end_time", "accessor": lambda t: t.isoformat() if t else None},
        {"name": "created_at", "accessor": lambda t: t.isoformat() if t else None},
        {"name": "updated_at", "accessor": lambda t: t.isoformat() if t else None},
        {"name": "p_event"},
    )
    gdpr_sensitive_data_fields = []

    class Meta:
        verbose_name = _("occurrence")
        verbose_name_plural = _("occurrences")

    def __post_save_republish_event(self):
        """
        Republish the event end time to LinkedEvents API when an occurrence is saved
        and linked to a published event.
        NOTE: `The graphene_linked_events.PublishEventMutation` and
        `graphene_linked_events._prepare_published_event_data`
        sets the start time of the event to time it is at the moment of the publishment.
        """

        if (
            self.p_event_id
            and self.p_event.is_published()
            and self.p_event.occurrences.filter(cancelled=False).count() > 0
        ):
            # Republish
            send_event_republish(self.p_event)

    def __post_delete_unpublish_event(self):
        """
        If the event is published,
        handle the event update of last existing occurrence
        by calling "unpublish" which means resetting the end time of the event.
        """
        if (
            self.p_event.is_published()
            and self.p_event.occurrences.filter(cancelled=False).count() == 0
        ):
            send_event_unpublish(self.p_event)

    def save(self, *args, **kwargs):
        # Resolve the event time range before the save
        pre_start_time, pre_end_time = get_event_time_range_from_occurrences(
            self.p_event
        )

        # Save the occurrence instance
        super().save(*args, **kwargs)

        # Resolve the event time range after the save
        post_start_time, post_end_time = get_event_time_range_from_occurrences(
            self.p_event
        )

        if not (pre_start_time, pre_end_time) == (post_start_time, post_end_time):
            self.__post_save_republish_event()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.__post_delete_unpublish_event()

    def __str__(self):
        return f"{self.p_event.linked_event_id} {self.start_time}" f" {self.place_id}"

    @property
    def seats_approved(self):
        qs = self.enrolments.filter(status=Enrolment.STATUS_APPROVED)
        if self.seat_type == self.OCCURRENCE_SEAT_TYPE_CHILDREN_COUNT:
            return (
                qs.aggregate(
                    seats_taken=Sum(
                        F("study_group__group_size") + F("study_group__amount_of_adult")
                    )
                )["seats_taken"]
                or 0
            )
        else:
            return qs.count()

    @property
    def seats_taken(self):
        qs = self.enrolments.filter(
            Q(status=Enrolment.STATUS_APPROVED) | Q(status=Enrolment.STATUS_PENDING)
        )
        if self.seat_type == self.OCCURRENCE_SEAT_TYPE_CHILDREN_COUNT:
            return (
                qs.aggregate(
                    seats_taken=Sum(
                        F("study_group__group_size") + F("study_group__amount_of_adult")
                    )
                )["seats_taken"]
                or 0
            )
        else:
            return qs.count()

    def is_editable_by_user(self, user):
        return user.person.organisations.filter(
            id=self.p_event.organisation.id
        ).exists()

    @transaction.atomic
    def cancel(self, reason=None):
        self.cancelled = True
        self.save()
        for e in self.enrolments.filter(
            status__in=[Enrolment.STATUS_PENDING, Enrolment.STATUS_APPROVED]
        ):
            e.set_status(Enrolment.STATUS_CANCELLED)
            e.send_event_notifications_to_contact_people(
                NotificationTemplate.OCCURRENCE_CANCELLED,
                NotificationTemplate.OCCURRENCE_CANCELLED_SMS,
                custom_message=reason,
            )

    @property
    def local_start_time(self):
        return localtime(self.start_time)

    def get_link_to_provider_ui(self, language=settings.LANGUAGE_CODE):
        global_id = to_global_id("OccurrenceNode", self.id)
        return (
            f"{settings.KULTUS_PROVIDER_UI_BASE_URL}{language}/events/"
            f"{self.p_event.linked_event_id}/occurrences/{global_id}"
        )

    def pending_enrolments(self):
        return self.enrolments.filter(status=Enrolment.STATUS_PENDING)

    def new_enrolments(self, days=1):
        return self.enrolments.filter(
            status=Enrolment.STATUS_APPROVED,
            enrolment_time__gte=timezone.now() - timedelta(days=days),
        )


class VenueCustomData(TranslatableModel):
    # Primary reference to LinkedEvent place_id
    place_id = models.CharField(
        primary_key=True, max_length=255, verbose_name=_("place id")
    )
    translations = TranslatedFields(
        description=models.TextField(verbose_name=_("description"), blank=True)
    )
    has_clothing_storage = models.BooleanField(
        default=False, verbose_name=_("has outer clothing storage")
    )
    has_snack_eating_place = models.BooleanField(
        default=False, verbose_name=_("has snack eating place")
    )
    outdoor_activity = models.BooleanField(
        default=False, verbose_name=_("outdoor activity")
    )
    has_toilet_nearby = models.BooleanField(
        default=False, verbose_name=_("has toilet nearby")
    )
    has_area_for_group_work = models.BooleanField(
        default=False, verbose_name=_("has area for group work")
    )
    has_indoor_playing_area = models.BooleanField(
        default=False, verbose_name=_("has indoor playing area")
    )
    has_outdoor_playing_area = models.BooleanField(
        default=False, verbose_name=_("has outdoor playing area")
    )

    class Meta:
        verbose_name = _("venue custom data")
        verbose_name_plural = _("venue custom data")

    def __str__(self):
        return f"{self.place_id}"


class StudyLevel(TranslatableModel):
    """
    The Study Level is intended to be a hierarchical list of teaching degrees.
    """

    id = models.CharField(
        max_length=255, primary_key=True
    )  # PT-678 needs migration for 255 chars.
    translations = TranslatedFields(
        label=models.CharField(max_length=255, verbose_name=_("label"))
    )  # Labels can have custom language translations.
    level = models.PositiveIntegerField(
        _("level"), help_text=_("Used to make a hierarchy between study levels.")
    )  # Level is used make a hierarchy between different StudyLevel instances.

    class Meta:
        verbose_name = _("study level")
        verbose_name_plural = _("study levels")
        ordering = ["level"]

    def get_label_with_fallback(self):
        return self.safe_translation_getter("label", any_language=True)

    def __str__(self):
        return f"{self.get_label_with_fallback()} (id: {self.id}, level: {self.level})"


class StudyGroupQuerySet(models.QuerySet):
    def with_enrolments_count(self, use_name_only=False):
        """Get the count of the enrolments that the group has done.
        NOTE: This method is good for investigation for any support task.

        Args:
            use_name_only (bool, optional): compare with the group name
            instead of the instance. Defaults to False.

        Returns:
            a query set with enrolments_count -field as annotated with the count
        """
        if use_name_only:
            groups_enrolments = Enrolment.objects.filter(
                study_group__group_name=OuterRef("group_name"),
            ).values("pk")
            return self.annotate(
                enrolments_count=SubqueryCount(Subquery(groups_enrolments))
            )
        return self.annotate(enrolments_count=Count("enrolments", distinct=True))

    def user_can_view(self, user: User):
        if not user.person:
            return self.none
        organisation_ids = [
            entry[0] for entry in user.person.organisations.values_list("id")
        ]
        return self.with_organisation_ids().filter(
            organisation_ids__overlap=organisation_ids
        )

    def with_organisation_ids(self):
        return self.annotate(
            organisation_ids=ArrayAgg(
                "enrolments__occurrence__p_event__organisation__pk"
            )
        )


class StudyGroup(
    GDPRModel, SerializableMixin, TimestampedModel, WithDeletablePersonModel
):
    # Tprek / Service map id for school or kindergarten from the city of Helsinki
    unit_id = models.CharField(max_length=255, verbose_name=_("unit id"), null=True)
    unit_name = models.CharField(
        max_length=1000, blank=True, verbose_name=_("unit name")
    )
    group_size = models.PositiveSmallIntegerField(verbose_name=_("group size"))
    amount_of_adult = models.PositiveSmallIntegerField(
        verbose_name=_("amount of adult"), default=0
    )
    group_name = models.CharField(
        max_length=255, blank=True, verbose_name=_("group name")
    )
    study_levels = models.ManyToManyField(
        StudyLevel,
        verbose_name=_("study levels"),
        blank=True,
        related_name="study_groups",
    )
    extra_needs = models.TextField(
        max_length=1000, blank=True, verbose_name=_("extra needs")
    )
    preferred_times = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name=_("preferred times"),
        help_text=_("Preferred times for the event"),
    )

    # TODO: Add audience/keyword/target group

    objects = SerializableMixin.SerializableManager.from_queryset(StudyGroupQuerySet)()

    serialize_fields = (
        {"name": "unit_id"},
        {"name": "unit_name"},
        {"name": "group_size"},
        {"name": "amount_of_adult"},
        {"name": "group_name"},
        {"name": "extra_needs"},
        {"name": "preferred_times"},
        {
            "name": "study_levels",
            "accessor": lambda manager: ", ".join([str(obj) for obj in manager.all()]),
        },
        {
            "name": "enrolments",
            "accessor": lambda manager: ", ".join([str(obj) for obj in manager.all()]),
        },  # avoid bidirectional serialization, because it wil lend in a forever lopp.
    )
    gdpr_sensitive_data_fields = [
        "unit_id",
        "unit_name",
        "group_name",
        "extra_needs",
    ]

    class Meta:
        verbose_name = _("study group")
        verbose_name_plural = _("study groups")
        ordering = [
            "created_at",
        ]

    @property
    def name(self):
        warnings.warn("Deprecated!", DeprecationWarning, stacklevel=2)
        return self.unit_name

    @name.setter
    def name(self, value):
        warnings.warn("Deprecated!", DeprecationWarning, stacklevel=2)
        self.unit_name = value

    def __str__(self):
        return f"{self.id} {self.unit_name}"

    def group_size_with_adults(self):
        """
        Sum an amount of adults to a size of group.
        """
        return self.group_size + self.amount_of_adult

    def save(self, *args, **kwargs):
        # Resolve the (school or kindergarten) unit name if it is not given
        if not self.unit_name and self.unit_id:
            resolve_unit_name_with_unit_id(self)

        # Save the study group instance
        super().save(*args, **kwargs)

    def is_editable_by_user(self, user):
        return user.person.organisations.filter(
            id__in=self.with_organisation_ids().value("organisation_ids")
        ).exists()


class EnrolmentQuerySet(models.QuerySet):
    def approved_enrolments_occurring_after_days(self, days_to_occurrence: int):
        """
        Approved enrolments whose occurrences start <days_to_occurrence> days from today
        i.e. today + <days_to_occurrence> == occurrence.start_time.date()
        """
        if days_to_occurrence < 0:
            raise ValueError("days_to_occurrence must be zero or greater")
        return self.filter(
            status=Enrolment.STATUS_APPROVED,
            occurrence__start_time__date=(
                timezone.now() + timedelta(days=days_to_occurrence)
            ).date(),
        )

    def get_by_unique_id(self, unique_id):
        compound_id = get_node_id_from_global_id(unique_id, "EnrolmentNode")
        enrolment_id, enrolment_time = compound_id.split("_")
        return self.get(id=enrolment_id, enrolment_time=enrolment_time)

    def pending_and_auto_accepted_enrolments(self, days=1):
        """
        Query all pending enrolments and
        any new auto accepted enrolments during the last `days`
        """
        return self.filter(occurrence__start_time__gte=(timezone.now())).filter(
            Q(
                enrolment_time__gte=(timezone.now() - timedelta(days=days)),
                status=Enrolment.STATUS_APPROVED,
                occurrence__p_event__auto_acceptance=True,
            )
            | Q(status=Enrolment.STATUS_PENDING)
        )

    def pending_enrolments_by_email(self, email: str):
        return self.filter(
            occurrence__p_event__contact_email=email,
            status=Enrolment.STATUS_PENDING,
        )

    def approved_enrolments_by_email(self, email: str):
        return self.filter(
            occurrence__p_event__contact_email=email,
            status=Enrolment.STATUS_APPROVED,
        )

    def user_can_view(self, user: User):
        if not user.person:
            return self.none
        organisation_ids = user.person.organisations.values("id")
        return self.filter(occurrence__p_event__organisation__in=organisation_ids)


class EnrolmentBase(WithDeletablePersonModel):
    notification_type = models.CharField(
        max_length=250,
        choices=NOTIFICATION_TYPES,
        default=NOTIFICATION_TYPE_EMAIL,
        verbose_name=_("notification type"),
    )
    enrolment_time = models.DateTimeField(
        verbose_name=_("enrolment time"), auto_now_add=True
    )
    updated_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True)

    class Meta:
        abstract = True


class EventQueueEnrolmentQuerySet(models.QuerySet):
    def with_group_occurrence_enrolment_count(self):
        """
        Annotate the amount of enrolments done to any occurrences
        of the same event with the same study group name.

        NOTE: The study group name is a free text field,
        so typos in the name may affect in the result.
        """
        occurrence_enrolments = Enrolment.objects.filter(
            occurrence__p_event=OuterRef("p_event"),
            study_group__group_name=OuterRef("study_group__group_name"),
        ).values("pk")[:1]
        return self.annotate(
            occurrence_enrolments_count=Count(
                Subquery(occurrence_enrolments), distinct=True
            )
        )

    def user_can_view(self, user: User):
        if not user.person:
            return self.none
        organisation_ids = user.person.organisations.values("id")
        return self.filter(p_event__organisation__in=organisation_ids)

    def enrolled_in_last_days(self, days=1):
        """
        Query all pending queued enrolments during the last `days`
        """
        return self.filter(enrolment_time__gte=(timezone.now() - timedelta(days=days)))


class EventQueueEnrolment(GDPRModel, SerializableMixin, EnrolmentBase):
    STATUS_HAS_NO_ENROLMENTS = "has_no_enrolments"
    STATUS_HAS_ENROLMENTS = "has_enrolments"
    QUEUE_STATUSES = (
        (
            STATUS_HAS_NO_ENROLMENTS,
            _("there are no enrolments to any occurrences of the event"),
        ),
        (
            STATUS_HAS_ENROLMENTS,
            _("there is at least one enrolment to an occurrence of the event"),
        ),
    )

    study_group = models.ForeignKey(
        "StudyGroup",
        verbose_name=_("study group"),
        related_name="queued_enrolments",
        on_delete=models.CASCADE,
    )
    p_event = models.ForeignKey(
        "PalvelutarjotinEvent",
        verbose_name=_("event"),
        related_name="queued_enrolments",
        on_delete=models.CASCADE,
    )

    objects = SerializableMixin.SerializableManager.from_queryset(
        EventQueueEnrolmentQuerySet
    )()

    serialize_fields = (
        {"name": "enrolment_time", "accessor": lambda t: t.isoformat() if t else None},
        {"name": "updated_at", "accessor": lambda t: t.isoformat() if t else None},
        {"name": "notification_type"},
        {
            "name": "study_group",
            "accessor": lambda group: str(group),
        },  # avoid bidirectional serialization, because it wil lend in a forever lopp.
        {"name": "p_event"},
    )
    gdpr_sensitive_data_fields = []

    class Meta:
        verbose_name = _("event queue enrolment")
        verbose_name_plural = _("event queue enrolments")
        constraints = [
            models.UniqueConstraint(
                fields=["study_group", "p_event"], name="unq_group_event"
            )
        ]

    def __str__(self):
        return f"{self.id} {self.p_event.linked_event_id} {self.study_group.name}"

    def is_editable_by_user(self, user):
        return user.person.organisations.filter(
            id=self.p_event.organisation.id
        ).exists()

    @property
    def status(self):
        has_enrolments = Enrolment.objects.filter(
            study_group__group_name=self.study_group.group_name,
            occurrence__p_event=self.p_event,
        ).exists()
        return (
            self.STATUS_HAS_ENROLMENTS
            if has_enrolments
            else self.STATUS_HAS_NO_ENROLMENTS
        )

    def create_enrolment(self, occurrence: Occurrence):
        enrolment = Enrolment(
            occurrence=occurrence,
            study_group=self.study_group,
            notification_type=self.notification_type,
            person=self.person,
        )
        enrolment.save()
        return enrolment


class Enrolment(GDPRModel, SerializableMixin, EnrolmentBase):
    STATUS_APPROVED = "approved"
    STATUS_PENDING = "pending"
    STATUS_CANCELLED = "cancelled"
    STATUS_DECLINED = "declined"
    STATUSES = (
        (STATUS_APPROVED, _("approved")),
        (STATUS_PENDING, _("pending")),
        (STATUS_CANCELLED, _("cancelled")),
        (STATUS_DECLINED, _("declined")),
    )
    study_group = models.ForeignKey(
        "StudyGroup",
        verbose_name=_("study group"),
        related_name="enrolments",
        on_delete=models.CASCADE,
    )
    occurrence = models.ForeignKey(
        "Occurrence",
        verbose_name=_("occurrences"),
        related_name="enrolments",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        choices=STATUSES,
        default=STATUS_PENDING,
        verbose_name=_("status"),
        max_length=255,
    )
    verification_tokens = GenericRelation(
        VerificationToken, related_query_name="enrolment"
    )

    objects = SerializableMixin.SerializableManager.from_queryset(EnrolmentQuerySet)()

    serialize_fields = (
        {"name": "enrolment_time", "accessor": lambda t: t.isoformat() if t else None},
        {"name": "updated_at", "accessor": lambda t: t.isoformat() if t else None},
        {"name": "status"},
        {"name": "occurrence"},
    )
    gdpr_sensitive_data_fields = []

    class Meta:
        verbose_name = _("enrolment")
        verbose_name_plural = _("enrolments")
        constraints = [
            models.UniqueConstraint(
                fields=["study_group", "occurrence"], name="unq_group_occurrence"
            )
        ]
        ordering = ["occurrence", "enrolment_time"]

    def __str__(self):
        return f"{self.id} {self.occurrence.start_time} {self.study_group.name}"

    def is_editable_by_user(self, user):
        return user.person.organisations.filter(
            id=self.occurrence.p_event.organisation.id
        ).exists()

    def set_status(self, status):
        if self.status == status:
            raise ApiUsageError(f"Enrolment status is already set to {status}")
        self.status = status
        self.save()

    def get_contact_people(self) -> List[Person]:
        contact_people = [self.person]
        if self.person != self.study_group.person:
            contact_people.append(self.study_group.person)
        return contact_people

    def send_event_notifications_to_contact_people(
        self,
        notification_template_id: Optional[NotificationTemplate],
        notification_template_id_sms: Optional[NotificationTemplate],
        custom_message: Optional[str] = None,
    ):
        for person in self.get_contact_people():
            occurrences_services.send_event_notifications_to_person(
                person,
                self.occurrence,
                self.study_group,
                self.notification_type,
                notification_template_id,
                notification_template_id_sms,
                event=self.occurrence.p_event.get_event_data(),
                custom_message=custom_message,
                enrolment=self,
            )

    def approve(self, send_notification=True, custom_message: Optional[str] = None):
        """Set the enrolment status to approved.
        In some cases e.g. in multi enrolment situations,
        the approvance notification sending should be called separately.

        Args:
            send_notification (bool, optional): should a notification be sent
            after approvance. Defaults to True.
            custom_message (Optional[str], optional): should there be a custom message.
            Defaults to None.

        Raises:
            EnrolmentNotEnoughCapacityError: Not enough space for the group
        """
        if self.occurrence.seats_taken > self.occurrence.amount_of_seats:
            raise EnrolmentNotEnoughCapacityError(
                "Not enough space for this study group"
            )
        self.set_status(self.STATUS_APPROVED)

        # In some cases e.g. in multi enrolment situations,
        # the approvance notification sending should be called separately.
        if send_notification:
            self.send_approve_notification(custom_message)

    def send_approve_notification(self, custom_message: Optional[str] = None):
        """
        Send the approvance notification. In some cases e.g. in multi
        enrolment situations, the approvance notification sending should
        be called separated from the actual approvance process.
        """
        self.send_event_notifications_to_contact_people(
            NotificationTemplate.ENROLMENT_APPROVED,
            NotificationTemplate.ENROLMENT_APPROVED_SMS,
            custom_message=custom_message,
        )

    def send_upcoming_occurrence_sms_reminder(
        self, custom_message: Optional[str] = None
    ):
        self.send_event_notifications_to_contact_people(
            notification_template_id=None,
            notification_template_id_sms=NotificationTemplate.OCCURRENCE_UPCOMING_SMS,
            custom_message=custom_message,
        )

    def decline(self, custom_message: Optional[str] = None):
        self.set_status(self.STATUS_DECLINED)
        self.send_event_notifications_to_contact_people(
            NotificationTemplate.ENROLMENT_DECLINED,
            NotificationTemplate.ENROLMENT_DECLINED_SMS,
            custom_message=custom_message,
        )

    def ask_cancel_confirmation(self, custom_message: Optional[str] = None):
        self.send_event_notifications_to_contact_people(
            NotificationTemplate.ENROLMENT_CANCELLATION,
            NotificationTemplate.ENROLMENT_CANCELLATION_SMS,
            custom_message=custom_message,
        )

    def cancel(self, custom_message: Optional[str] = None):
        """
        Deactivate the used cancellation tokens and
        notify about successful cancellation.
        """

        self.set_status(self.STATUS_CANCELLED)
        # Deactivate active cancellation tokens
        self.get_active_verification_tokens(
            verification_type=VerificationToken.VERIFICATION_TYPE_CANCELLATION
        ).update(is_active=False)

        # Notify with email and sms
        self.send_event_notifications_to_contact_people(
            NotificationTemplate.ENROLMENT_CANCELLED,
            NotificationTemplate.ENROLMENT_CANCELLED_SMS,
            custom_message=custom_message,
        )

    def get_unique_id(self):
        # Unique id is the base64 encoded enrolment_id and enrolment timestamp
        # Added object timestamp so it'll be harder to guess, otherwise anyone can
        # build the unique id after reading this
        return to_global_id(
            "EnrolmentNode", "_".join([str(self.id), str(self.enrolment_time)])
        )

    def get_link_to_cancel_ui(self, language=settings.LANGUAGE_CODE):
        return settings.VERIFICATION_TOKEN_URL_MAPPING[
            "occurrences.enrolment.CANCELLATION"
        ].format(lang=language, unique_id=self.get_unique_id())

    def get_active_verification_tokens(self, verification_type=None):
        """Filter active verification tokens"""

        return VerificationToken.objects.filter_active_tokens(
            self, verification_type=verification_type, person=self.person
        )

    def get_cancellation_url(
        self, language=settings.LANGUAGE_CODE, cancellation_token=None
    ):
        """
        Get a cancellation (confirmation) url.
        If the cancellation token is not given as a parameter,
        it will be fetched from the database.
        """
        try:
            if not cancellation_token:
                cancellation_token = self.get_active_verification_tokens(
                    verification_type=VerificationToken.VERIFICATION_TYPE_CANCELLATION
                )[0]
        except IndexError:
            logger.warning(
                "No cancellation token created when there should be one!"
                + f" Enrolment id: {self.id}"
            )
            return ""

        token = (
            cancellation_token.key
            if isinstance(cancellation_token, VerificationToken)
            else cancellation_token
        )

        return (
            settings.VERIFICATION_TOKEN_URL_MAPPING[
                "occurrences.enrolment.CANCELLATION.confirmation"
            ].format(lang=language, unique_id=self.get_unique_id(), token=token)
            if settings.VERIFICATION_TOKEN_URL_MAPPING
            and "occurrences.enrolment.CANCELLATION.confirmation"
            in settings.VERIFICATION_TOKEN_URL_MAPPING
            else ""
        )

    def create_cancellation_token(self, deactivate_existing=False):
        """
        Create a cancellation verification token for an enrolment.
        """
        if deactivate_existing:
            return VerificationToken.objects.deactivate_and_create_token(
                self,
                self.person,
                verification_type=VerificationToken.VERIFICATION_TYPE_CANCELLATION,
            )

        return VerificationToken.objects.create_token(
            self, self.person, VerificationToken.VERIFICATION_TYPE_CANCELLATION
        )
