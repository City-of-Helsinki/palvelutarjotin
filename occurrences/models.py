from datetime import timedelta

from django.db import models, transaction
from django.db.models import Q, Sum
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _
from graphene_linked_events.utils import retrieve_linked_events_data
from occurrences.consts import (
    NOTIFICATION_TYPE_EMAIL,
    NOTIFICATION_TYPES,
    NotificationTemplate,
)
from occurrences.utils import send_event_notifications_to_contact_person
from parler.models import TranslatedFields

from common.models import TimestampedModel, TranslatableModel
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
    duration = models.PositiveSmallIntegerField(verbose_name=_("duration"))
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

    class Meta:
        verbose_name = _("palvelutarjotin event")
        verbose_name_plural = _("palvelutarjotin events")

    def __str__(self):
        return f"{self.id} {self.linked_event_id}"

    def get_event_data(self):
        # We need query event location as well
        params = {"include": "location"}
        return retrieve_linked_events_data("event", self.linked_event_id, params=params)

    def is_editable_by_user(self, user):
        if self.organisation:
            return user.person.organisations.filter(id=self.organisation.id).exists()
        return True

    def get_end_time_from_occurrences(self):
        # Return the latest time that teacher can enrol to the event
        try:
            last_occurrence = self.occurrences.latest("start_time")
        except Occurrence.DoesNotExist:
            raise ValueError("Palvelutarjotin event has no occurrence")
        return last_occurrence.start_time - timedelta(days=self.enrolment_end_days)


class Language(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(verbose_name=_("name"), max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")


class Occurrence(TimestampedModel):
    p_event = models.ForeignKey(
        PalvelutarjotinEvent,
        verbose_name=_("palvelutarjotin event"),
        related_name="occurrences",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    min_group_size = models.PositiveSmallIntegerField(verbose_name=_("min group size"))
    max_group_size = models.PositiveSmallIntegerField(verbose_name=_("max group size"))
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
    auto_acceptance = models.BooleanField(
        default=False, verbose_name=_("auto acceptance")
    )
    amount_of_seats = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("amount of seats")
    )

    languages = models.ManyToManyField(
        "Language", verbose_name=_("languages"), blank=True, related_name="occurrences"
    )
    cancelled = models.BooleanField(verbose_name=_("cancelled"), default=False)

    class Meta:
        verbose_name = _("occurrence")
        verbose_name_plural = _("occurrences")

    def __str__(self):
        return f"{self.id} {self.place_id}"

    def add_languages(self, languages):
        self.languages.clear()
        for lang in languages:
            l, _ = Language.objects.get_or_create(id=lang["id"])
            self.languages.add(l)

    @property
    def seats_approved(self):
        return (
            self.enrolments.filter(status=Enrolment.STATUS_APPROVED).aggregate(
                seats_taken=Sum("study_group__group_size")
            )["seats_taken"]
            or 0
        )

    @property
    def seats_taken(self):
        return (
            self.enrolments.filter(
                Q(status=Enrolment.STATUS_APPROVED) | Q(status=Enrolment.STATUS_PENDING)
            ).aggregate(seats_taken=Sum("study_group__group_size"))["seats_taken"]
            or 0
        )

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

    class Meta:
        verbose_name = _("venue custom data")
        verbose_name_plural = _("venue custom data")

    def __str__(self):
        return f"{self.place_id}"


class StudyGroup(TimestampedModel):
    STUDY_LEVEL_PRESCHOOL = "preschool"
    STUDY_LEVEL_GRADE_1 = "grade_1"
    STUDY_LEVEL_GRADE_2 = "grade_2"
    STUDY_LEVEL_GRADE_3 = "grade_3"
    STUDY_LEVEL_GRADE_4 = "grade_4"
    STUDY_LEVEL_GRADE_5 = "grade_5"
    STUDY_LEVEL_GRADE_6 = "grade_6"
    STUDY_LEVEL_GRADE_7 = "grade_7"
    STUDY_LEVEL_GRADE_8 = "grade_8"
    STUDY_LEVEL_GRADE_9 = "grade_9"
    STUDY_LEVEL_GRADE_10 = "grade_10"
    STUDY_LEVEL_SECONDARY = "secondary"
    STUDY_LEVELS = (
        (STUDY_LEVEL_PRESCHOOL, _("preschool")),
        (STUDY_LEVEL_GRADE_1, _("first grade")),
        (STUDY_LEVEL_GRADE_2, _("second grade")),
        (STUDY_LEVEL_GRADE_3, _("third grade")),
        (STUDY_LEVEL_GRADE_4, _("fourth grade")),
        (STUDY_LEVEL_GRADE_5, _("fifth grade")),
        (STUDY_LEVEL_GRADE_6, _("sixth grade")),
        (STUDY_LEVEL_GRADE_7, _("seventh grade")),
        (STUDY_LEVEL_GRADE_8, _("eighth grade")),
        (STUDY_LEVEL_GRADE_9, _("ninth grade")),
        (STUDY_LEVEL_GRADE_10, _("tenth grade")),
        (STUDY_LEVEL_SECONDARY, _("secondary")),
    )
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

    study_level = models.CharField(
        max_length=255, blank=True, verbose_name=_("study level"), choices=STUDY_LEVELS
    )
    extra_needs = models.CharField(max_length=1000, blank=True, verbose_name=_("name"))

    # TODO: Add audience/keyword/target group

    class Meta:
        verbose_name = _("study group")
        verbose_name_plural = _("study groups")

    def __str__(self):
        return f"{self.id} {self.name}"


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

    class Meta:
        verbose_name = _("enrolment")
        verbose_name_plural = _("enrolments")
        constraints = [
            models.UniqueConstraint(
                fields=["study_group", "occurrence"], name="unq_group_occurrence"
            )
        ]

    def __str__(self):
        return f"{self.id} {self.occurrence} {self.study_group}"

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
