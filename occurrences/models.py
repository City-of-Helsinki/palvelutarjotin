from datetime import timedelta

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models, transaction
from django.db.models import F, Q, Sum
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _
from django_ilmoitin.utils import send_notification
from graphene_linked_events.utils import retrieve_linked_events_data
from graphql_relay import to_global_id
from occurrences.consts import (
    NOTIFICATION_TYPE_EMAIL,
    NOTIFICATION_TYPES,
    NotificationTemplate,
)
from occurrences.utils import send_event_notifications_to_contact_person
from parler.models import TranslatedFields
from verification_token.models import VerificationToken

from common.models import TimestampedModel, TranslatableModel
from common.utils import get_node_id_from_global_id
from palvelutarjotin import settings
from palvelutarjotin.exceptions import ApiUsageError


class PalvelutarjotinEvent(TimestampedModel):
    PUBLICATION_STATUS_PUBLIC = "public"
    PUBLICATION_STATUS_DRAFT = "draft"
    PUBLICATION_STATUSES = (
        (PUBLICATION_STATUS_PUBLIC, _("public")),
        (PUBLICATION_STATUS_DRAFT, _("draft")),
    )
    linked_event_id = models.CharField(
        max_length=255, verbose_name=_("linked event id")
    )
    enrolment_start = models.DateTimeField(
        verbose_name=_("enrolment start"), blank=True, null=True
    )

    # Enrolment will be close x days before the occurrence start
    enrolment_end_days = models.PositiveSmallIntegerField(
        verbose_name=_("enrolment end days"), blank=True, null=True
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
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    contact_phone_number = models.CharField(
        verbose_name=_("contact phone number"), max_length=64, blank=True
    )
    contact_email = models.EmailField(
        max_length=255, verbose_name=_("contact email"), blank=True
    )
    auto_acceptance = models.BooleanField(
        default=False, verbose_name=_("auto acceptance")
    )

    mandatory_additional_information = models.BooleanField(
        default=False, verbose_name=_("mandatory additional information")
    )

    class Meta:
        verbose_name = _("palvelutarjotin event")
        verbose_name_plural = _("palvelutarjotin events")

    def __str__(self):
        return f"{self.id} {self.linked_event_id}"

    def get_event_data(self, is_staff=False):
        # We need query event location as well
        params = {"include": "location"}
        return retrieve_linked_events_data(
            "event", self.linked_event_id, params=params, is_staff=is_staff
        )

    def is_editable_by_user(self, user):
        if self.organisation:
            return user.person.organisations.filter(id=self.organisation.id).exists()
        return True

    def is_published(self):
        return (
            self.get_event_data(is_staff=True).publication_status
            == PalvelutarjotinEvent.PUBLICATION_STATUS_PUBLIC
        )

    def get_end_time_from_occurrences(self):
        # Return the latest time that teacher can enrol to the event
        try:
            last_occurrence = self.occurrences.latest("start_time")
        except Occurrence.DoesNotExist:
            raise ValueError("Palvelutarjotin event has no occurrence")
        return last_occurrence.start_time - timedelta(days=self.enrolment_end_days)

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


class Language(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(verbose_name=_("name"), max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")


class Occurrence(TimestampedModel):
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

    class Meta:
        verbose_name = _("occurrence")
        verbose_name_plural = _("occurrences")

    def __str__(self):
        return f"{self.p_event.linked_event_id} {self.start_time}" f" {self.place_id}"

    def add_languages(self, languages):
        self.languages.clear()
        for lang in languages:
            l, _ = Language.objects.get_or_create(id=lang["id"])
            self.languages.add(l)

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
        for e in self.enrolments.all():
            e.set_status(Enrolment.STATUS_CANCELLED)
            send_event_notifications_to_contact_person(
                e.person,
                self,
                e.study_group,
                e.notification_type,
                NotificationTemplate.OCCURRENCE_CANCELLED,
                NotificationTemplate.OCCURRENCE_CANCELLED_SMS,
                event=e.occurrence.p_event.get_event_data(),
                custom_message=reason,
                enrolment=e,
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

    def __str__(self):
        return f"{self.id}"


class StudyGroup(TimestampedModel):
    person = models.ForeignKey(
        "organisations.Person", verbose_name=_("person"), on_delete=models.PROTECT
    )
    name = models.CharField(max_length=1000, blank=True, verbose_name=_("name"))
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
    extra_needs = models.CharField(max_length=1000, blank=True, verbose_name=_("name"))

    # TODO: Add audience/keyword/target group

    class Meta:
        verbose_name = _("study group")
        verbose_name_plural = _("study groups")

    def __str__(self):
        return f"{self.id} {self.name}"

    def group_size_with_adults(self):
        """
        Sum an amount of adults to a size of group.
        """
        if self.group_size:
            return self.group_size + (
                self.amount_of_adult if self.amount_of_adult is not None else 0
            )
        return None


class EnrolmentQuerySet(models.QuerySet):
    def send_enrolment_summary_report_to_providers(self, days=1):
        reports = {}
        # Query all pending enrolments and
        # any new auto accepted enrolments during the last `days`
        enrolments = self.filter(
            Q(
                enrolment_time__gte=(timezone.now() - timedelta(days=days)),
                status=Enrolment.STATUS_APPROVED,
                occurrence__p_event__auto_acceptance=True,
            )
            | Q(status=Enrolment.STATUS_PENDING)
        ).select_related("occurrence", "occurrence__p_event")
        p_events = (
            PalvelutarjotinEvent.objects.filter(occurrences__enrolments__in=enrolments)
            .prefetch_related("occurrences__enrolments")
            .distinct()
        )

        for p_event in p_events:
            # Group by contact_email address:
            reports.setdefault(p_event.contact_email, []).append(p_event)

        for address, report in reports.items():
            context_report = []
            for p_event in report:
                context_report.append(
                    {
                        "event": p_event.get_event_data(),
                        "p_event": p_event,
                        "occurrences": p_event.occurrences.filter(
                            enrolments__in=enrolments
                        ).distinct(),
                    }
                )

            context = {
                "report": context_report,
                "total_pending_enrolments": enrolments.filter(
                    occurrence__p_event__contact_email=address,
                    status=Enrolment.STATUS_PENDING,
                ).count(),
                "total_new_enrolments": enrolments.filter(
                    occurrence__p_event__contact_email=address,
                    status=Enrolment.STATUS_APPROVED,
                ).count(),
            }
            send_notification(
                address, NotificationTemplate.ENROLMENT_SUMMARY_REPORT, context
            )

    def get_by_unique_id(self, unique_id):
        compound_id = get_node_id_from_global_id(unique_id, "EnrolmentNode")
        enrolment_id, ts = compound_id.split("_")
        return self.get(id=enrolment_id, enrolment_time=ts)


class Enrolment(models.Model):
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
    enrolment_time = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(
        "organisations.Person",
        verbose_name=_("person"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    notification_type = models.CharField(
        max_length=250,
        choices=NOTIFICATION_TYPES,
        default=NOTIFICATION_TYPE_EMAIL,
        verbose_name=_("notification type"),
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
    objects = EnrolmentQuerySet.as_manager()

    class Meta:
        verbose_name = _("enrolment")
        verbose_name_plural = _("enrolments")
        constraints = [
            models.UniqueConstraint(
                fields=["study_group", "occurrence"], name="unq_group_occurrence"
            )
        ]

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

    def approve(self, custom_message=None):
        self.set_status(self.STATUS_APPROVED)
        send_event_notifications_to_contact_person(
            self.person,
            self.occurrence,
            self.study_group,
            self.notification_type,
            NotificationTemplate.ENROLMENT_APPROVED,
            NotificationTemplate.ENROLMENT_APPROVED_SMS,
            event=self.occurrence.p_event.get_event_data(),
            custom_message=custom_message,
            enrolment=self,
        )

    def decline(self, custom_message=None):
        self.set_status(self.STATUS_DECLINED)
        send_event_notifications_to_contact_person(
            self.person,
            self.occurrence,
            self.study_group,
            self.notification_type,
            NotificationTemplate.ENROLMENT_DECLINED,
            NotificationTemplate.ENROLMENT_DECLINED_SMS,
            event=self.occurrence.p_event.get_event_data(),
            custom_message=custom_message,
            enrolment=self,
        )

    def ask_cancel_confirmation(self, custom_message=None):
        send_event_notifications_to_contact_person(
            self.person,
            self.occurrence,
            self.study_group,
            self.notification_type,
            NotificationTemplate.ENROLMENT_CANCELLATION,
            NotificationTemplate.ENROLMENT_CANCELLATION_SMS,
            event=self.occurrence.p_event.get_event_data(),
            custom_message=custom_message,
            enrolment=self,
        )

    def cancel(self, custom_message=None):
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
        send_event_notifications_to_contact_person(
            self.person,
            self.occurrence,
            self.study_group,
            self.notification_type,
            NotificationTemplate.ENROLMENT_CANCELLED,
            NotificationTemplate.ENROLMENT_CANCELLED_SMS,
            event=self.occurrence.p_event.get_event_data(),
            custom_message=custom_message,
            enrolment=self,
        )

    def get_unique_id(self):
        # Unique id is the base64 encoded of enrolment_id and enrolment timestamp
        # Added object timestamp so it'll be harder to guess, otherwise any one can
        # build the unique id after reading this
        return to_global_id(
            "EnrolmentNode", "_".join([str(self.id), str(self.enrolment_time)])
        )

    def get_link_to_cancel_ui(self, language=settings.LANGUAGE_CODE):
        return settings.VERIFICATION_TOKEN_URL_MAPPING[
            "occurrences.enrolment.CANCELLATION"
        ].format(lang=language, unique_id=self.get_unique_id())

    def get_active_verification_tokens(self, verification_type=None):
        """ Filter active verification tokens """

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
        if not cancellation_token:
            cancellation_token = self.get_active_verification_tokens(
                verification_type=VerificationToken.VERIFICATION_TYPE_CANCELLATION
            )[0]

        token = (
            cancellation_token.key
            if isinstance(cancellation_token, VerificationToken)
            else cancellation_token
        )

        return settings.VERIFICATION_TOKEN_URL_MAPPING[
            "occurrences.enrolment.CANCELLATION.confirmation"
        ].format(lang=language, unique_id=self.get_unique_id(), token=token)

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
