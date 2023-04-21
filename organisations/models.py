from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.db.models import Max, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from helusers.models import AbstractUser

from common.models import TimestampedModel, UUIDPrimaryKeyModel
from organisations.services import (
    send_myprofile_creation_notification_to_admins,
    send_myprofile_organisations_accepted_notification,
)


class PersonQuerySet(models.QuerySet):
    def user_can_view(self, user):
        # Only return profile of logged in user if he's not staff
        if user.is_staff:
            return self
        elif user.is_authenticated:
            return self.filter(user=user)
        else:
            return self.none()

    def retention_period_exceeded(self):
        earliest_valid_timestamp = timezone.now() - relativedelta(
            months=settings.PERSONAL_DATA_RETENTION_PERIOD_MONTHS
        )

        all_enrolments_too_old = Q(max_enrolment_end_time=None) | Q(
            max_enrolment_end_time__lt=earliest_valid_timestamp
        )
        all_study_groups_too_old = Q(max_studygroup_end_time=None) | Q(
            max_studygroup_end_time__lt=earliest_valid_timestamp
        )

        return (
            # At least for now returns only unauthenticated Person's
            self.filter(user=None)
            .annotate(
                max_enrolment_end_time=Max("enrolment__occurrence__end_time"),
                max_studygroup_end_time=Max(
                    "studygroup__enrolments__occurrence__end_time"
                ),
            )
            .filter(all_enrolments_too_old & all_study_groups_too_old)
        )

    @transaction.atomic
    def delete(self):
        for obj in self:
            obj.set_related_objects_person_deleted_at()
        return super().delete()


class UserQueryset(models.QuerySet):
    @transaction.atomic
    def delete(self):
        for obj in self:
            obj.delete_related_p_event_contact_info()
        return super().delete()


class CustomUserManager(UserManager.from_queryset(UserQueryset)):
    pass


class User(AbstractUser):
    is_admin = models.BooleanField(_("admin status"), default=False)

    objects = CustomUserManager()

    # When creating an user, the name and the email can be left to blank.
    # In those cases, return username.
    def __str__(self):
        display_name = super().__str__()
        if not display_name:
            return self.username
        return display_name

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        permissions = [
            (
                "can_administrate_user_permissions",
                "Can administrate user permissions",
            ),
        ]

    @transaction.atomic
    def delete(self, *args, **kwargs):
        self.delete_related_p_event_contact_info()
        return super().delete(*args, **kwargs)

    def delete_related_p_event_contact_info(self):
        if hasattr(self, "person"):
            self.person.p_event.delete_contact_info()


class Organisation(models.Model):
    TYPE_USER = "user"
    TYPE_PROVIDER = "provider"
    ORGANISATION_TYPES = (
        (TYPE_USER, _("User")),
        (TYPE_PROVIDER, _("Provider")),
    )
    name = models.CharField(max_length=255, verbose_name=_("name"))
    phone_number = models.CharField(
        verbose_name=_("phone number"), max_length=64, blank=True
    )
    type = models.CharField(
        choices=ORGANISATION_TYPES, verbose_name=_("type"), max_length=64
    )
    persons = models.ManyToManyField(
        "Person", verbose_name=_("persons"), related_name="organisations", blank=True
    )
    publisher_id = models.CharField(
        max_length=255, verbose_name=_("publisher id"), blank=True
    )

    class Meta:
        verbose_name = _("organisation")
        verbose_name_plural = _("organisations")

    def __str__(self):
        return f"{self.name} ({self.id})"

    def is_editable_by_user(self, user):
        return user.person.organisations.filter(id=self.id).exists()


class OrganisationProposal(models.Model):
    """
    When a member of a 3rd party organisation registers
    to the API from the providers UI, he can make a proposal to add
    a new 3rd party organisation.
    NOTE: Since the process is still quite unclear, the proposals and
    and 3rd party organisation wishes can be collected with this model
    and stored in database as detached. The use case is that an admin can
    see which organisation the new user likes to represent and then
    the real organisation.Organisation instance can be created
    (if necessary and not yet done) and linked to the user.
    """

    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.CharField(
        max_length=255, verbose_name=_("description"), blank=True
    )
    phone_number = models.CharField(
        verbose_name=_("phone number"), max_length=64, blank=True
    )
    applicant = models.ForeignKey(
        "Person", verbose_name=_("applicant"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("organisation proposal")
        verbose_name_plural = _("organisation proposals")

    def __str__(self):
        return f"{self.id} {self.name}"


class Person(UUIDPrimaryKeyModel, TimestampedModel):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255, verbose_name=_("name"))
    phone_number = models.CharField(
        verbose_name=_("phone number"), max_length=64, blank=True
    )
    email_address = models.EmailField(max_length=255, verbose_name=_("email"))
    language = models.CharField(
        verbose_name=_("language"), max_length=10, default=settings.LANGUAGES[0][0]
    )
    place_ids = ArrayField(
        models.CharField(max_length=250),
        verbose_name=_("own places"),
        blank=True,
        default=list,
    )

    objects = PersonQuerySet.as_manager()

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    def __str__(self):
        username = self.user.username if self.user else None
        if username:
            return f"{self.name} ({username})"
        return f"{self.name}"

    @transaction.atomic
    def delete(self, *args, **kwargs):
        self.set_related_objects_person_deleted_at()
        return super().delete(*args, **kwargs)

    def set_related_objects_person_deleted_at(self):
        from occurrences.models import Enrolment, StudyGroup

        now = timezone.now()
        Enrolment.objects.filter(person=self).update(person_deleted_at=now)
        StudyGroup.objects.filter(person=self).update(person_deleted_at=now)

    def is_editable_by_user(self, user):
        return (
            user.person.organisations.get_queryset()
            .intersection(self.organisations.get_queryset())
            .exists()
        )

    def notify_myprofile_creation(self, custom_message=None):
        send_myprofile_creation_notification_to_admins(
            self,
            custom_message=custom_message,
        )

    def notify_myprofile_accepted(self, custom_message=None):
        send_myprofile_organisations_accepted_notification(
            self, custom_message=custom_message
        )


class EnrolleePersonalDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user=None)


class EnrolleePersonalData(Person):
    objects = EnrolleePersonalDataManager.from_queryset(PersonQuerySet)()

    class Meta:
        proxy = True
        # Move these under "occurrences" group in the admin UI. That is not a perfect
        # place for these either, but "organisations" would have been misleading
        # because these have nothing to do with organisations.
        app_label = "occurrences"
        verbose_name = pgettext_lazy("singular", "Enrollee personal data")
        verbose_name_plural = pgettext_lazy("plural", "Enrollee personal data")
