from django.db import models
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatedFields

from common.models import TimestampedModel, TranslatableModel


class PalvelutarjotinEvent(TimestampedModel):
    linked_event_id = models.CharField(
        max_length=255, verbose_name=_("linked event " "id")
    )
    enrolment_start = models.DateTimeField(
        verbose_name=_("enrolment start"), blank=True, null=True
    )
    enrolment_end = models.DateTimeField(
        verbose_name=_("enrolment end"), blank=True, null=True
    )
    duration = models.PositiveSmallIntegerField(verbose_name=_("duration"))
    needed_occurrences = models.PositiveSmallIntegerField(
        verbose_name=_("needed " "occurrence"), default=1
    )

    class Meta:
        verbose_name = _("palvelutarjotin event")
        verbose_name_plural = _("palvelutarjotin events")

    def __str__(self):
        return f"{self.id} {self.linked_event_id}"


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
    organisation = models.ForeignKey(
        "organisations.Organisation",
        verbose_name=_("organisation"),
        on_delete=models.PROTECT,
    )
    contact_persons = models.ManyToManyField(
        "organisations.Person",
        related_name="occurrences",
        verbose_name=_("contact persons"),
        blank=True,
    )
    groups = models.ManyToManyField(
        "StudyGroup",
        through="Enrolment",
        related_name="occurrences",
        verbose_name=_("group"),
        blank=True,
    )
    place_id = models.CharField(max_length=255, verbose_name=_("place id"), blank=True)

    class Meta:
        verbose_name = _("occurrence")
        verbose_name_plural = _("occurrences")

    def __str__(self):
        return f"{self.id} {self.place_id}"


class VenueCustomData(TranslatableModel):
    # Primary reference to LinkedEvent place_id
    place_id = models.CharField(
        primary_key=True, max_length=255, verbose_name=_("place id")
    )
    translations = TranslatedFields(
        description=models.TextField(verbose_name=_("description"), blank=True)
    )

    class Meta:
        verbose_name = _("venue custom data")
        verbose_name_plural = _("venue custom data")

    def __str__(self):
        return f"{self.place_id}"


class StudyGroup(TimestampedModel):
    person = models.ForeignKey(
        "organisations.Person", verbose_name=_("person"), on_delete=models.PROTECT
    )
    name = models.CharField(max_length=1000, blank=True, verbose_name=_("name"))
    group_size = models.PositiveSmallIntegerField(verbose_name=_("group size"))

    # TODO: Add audience/keyword/target group

    class Meta:
        verbose_name = _("study group")
        verbose_name_plural = _("study groups")

    def __str__(self):
        return f"{self.id} {self.name}"


class Enrolment(models.Model):
    group = models.ForeignKey(
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

    class Meta:
        verbose_name = _("enrolment")
        verbose_name_plural = _("enrolments")
        constraints = [
            models.UniqueConstraint(
                fields=["group", "occurrence"], name="unq_group_occurrence"
            )
        ]

    def __str__(self):
        return f"{self.id} {self.occurrence} {self.group}"
