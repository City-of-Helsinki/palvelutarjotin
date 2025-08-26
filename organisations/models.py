import logging

from auditlog.context import disable_auditlog
from auditlog.models import LogEntry
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models, router, transaction
from django.db.models import Q
from django.db.models.deletion import Collector
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from helsinki_gdpr.models import SerializableMixin
from helusers.models import AbstractUser

from common.models import TimestampedModel, UUIDPrimaryKeyModel
from gdpr.models import GDPRModel
from organisations.services import (
    send_myprofile_creation_notification_to_admins,
    send_myprofile_organisations_accepted_notification,
)

logger = logging.getLogger(__name__)


class PersonQuerySet(models.QuerySet):
    def user_can_view(self, user):
        # Only return profile of logged in user if he's not staff
        if getattr(user, "is_event_staff", False):
            return self
        elif getattr(user, "is_authenticated", False):
            return self.filter(user=user)
        else:
            return self.none()

    def retention_period_exceeded(self):
        """
        Return queryset of Person objects whose personal data
        retention period has exceeded.

        This excludes:
        - Persons with a user account
        - Persons with any valid (recent) enrolments
        """
        earliest_valid_timestamp = timezone.now() - relativedelta(
            months=settings.PERSONAL_DATA_RETENTION_PERIOD_MONTHS
        )

        # Return persons who:
        # 1. Don't have a user account
        # 2. Don't have any valid enrolments (either as person or study group contact)
        # 3. Don't have any valid event queue enrolments
        return (
            self.exclude(user__isnull=False)
            .exclude(enrolment__occurrence__end_time__gt=earliest_valid_timestamp)
            .exclude(
                studygroup__enrolments__occurrence__end_time__gt=earliest_valid_timestamp
            )
            .exclude(
                studygroup__queued_enrolments__p_event__occurrences__end_time__gt=earliest_valid_timestamp
            )
            .exclude(
                eventqueueenrolment__p_event__occurrences__end_time__gt=earliest_valid_timestamp
            )
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


class CustomUserManager(
    UserManager.from_queryset(UserQueryset),
    SerializableMixin.SerializableManager,
):
    pass


class User(AbstractUser, GDPRModel, SerializableMixin):
    """
    Custom user model extending Django's AbstractUser with additional fields
    for administrative and event staff roles.

    The save method is overridden to automatically manage the 'is_event_staff'
    and 'is_staff' flags based on the 'is_admin' status to enforce business rules.
    The delete method is also overridden to handle deletion of related objects
    and create audit logs.
    """

    is_admin = models.BooleanField(
        default=False,
        verbose_name=_("Admin status"),
        help_text=_(
            "Designates whether the user actively administrates the provider users. "
            "Admins receives some administrative emails, e.g, "
            "whenever a user requests a provider user status and an access to "
            "the Kultus Admin UI. "
            "Note that admin users are automatically also staff members."
        ),
    )
    is_event_staff = models.BooleanField(
        default=False,
        verbose_name=_("Event Admin (in Kultus Admin UI)"),
        help_text=_(
            "Designates whether the user can access the Kultus Admin UI (React app) "
            "as an event provider to manage events and their enrolments. "
            "Note that staff users are automatically also event staff members."
        ),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Staff Status (Django Admin)"),
        help_text=_(
            "Designates whether the user can log into the Django Admin site. "
            "This permission is primarily intended for internal Django "
            "administration tasks. "
            "Note that staff users are automatically also event staff members."
        ),
    )

    objects = CustomUserManager()

    serialize_fields = (
        {"name": "uuid", "accessor": lambda uuid: str(uuid)},
        {"name": "username"},
        {"name": "first_name"},
        {"name": "last_name"},
        {"name": "email"},
        {"name": "last_login", "accessor": lambda t: t.isoformat() if t else None},
        {"name": "date_joined", "accessor": lambda t: t.isoformat() if t else None},
        {"name": "person"},
    )
    gdpr_sensitive_data_fields = ["first_name", "last_name", "email"]

    # When creating an user, the name and the email can be left to blank.
    # In those cases, return username.
    def __str__(self):
        """
        Returns the display name of the user. If first and last names are
        blank, returns the username.
        """
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

    def _delete_related_objects(self, using=None, keep_parents=False):
        """
        Deletes all related objects of the current instance.

        Based on Django's Model.delete method:
        https://github.com/django/django/blob/4.2.20/django/db/models/base.py#L1123-L1132

        Args:
            using (str, optional): The database alias to use. Defaults to None.
            keep_parents (bool, optional): If True, prevents deletion of parent objects
                in multi-table inheritance. Defaults to False.
        """
        if self.pk is None:
            raise ValueError(
                "%s object can't be deleted because its %s attribute is set "
                "to None." % (self._meta.object_name, self._meta.pk.attname)
            )
        using = using or router.db_for_write(self.__class__, instance=self)
        collector = Collector(using=using, origin=self)
        # Don't include `self` in objs-parameter,
        # so the User instance itself won't get deleted.
        collector.collect([], keep_parents=keep_parents)
        collector.delete()

    def delete_related_p_event_contact_info(self):
        """
        Deletes the contact information associated with the user's related
        Person object's events (assuming a ForeignKey relationship exists).
        """
        if hasattr(self, "person"):
            self.person.p_event.delete_contact_info()

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to enforce business rules for
        automatically managing the 'is_staff' (Django Admin access) and
        'is_event_staff' (Kultus Admin UI access) flags.

        The following logic is applied:
        - **Admin Implies Staff:** If a user's 'is_admin' flag is True and their
        'is_staff' flag is False, the 'is_staff' flag is automatically set to
        True, granting them access to the Django Admin site.
        - **Staff Implies Event Staff:** If a user's 'is_staff' flag is True and
        their 'is_event_staff' flag is False, the 'is_event_staff' flag is
        automatically set to True, granting them access to the Kultus Admin UI.

        These rules ensure a consistent permission flow where administrators
        inherently have staff privileges for the Django Admin, and any user
        with staff privileges also gains access to the Kultus Admin UI. Actions
        taken by this method to modify 'is_staff' and 'is_event_staff' are
        logged for auditing purposes.
        """
        # User who is admin, is also staff
        if self.is_admin and not self.is_staff:
            self.is_staff = True
            logger.info(f"User '{self.username}' is admin, setting is_staff to True")

        # User who is staff is also event staff
        if self.is_staff and not self.is_event_staff:
            self.is_event_staff = True
            logger.info(
                f"User '{self.username}' is staff, setting is_event_staff to True"
            )

        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        """
        Deletes the user and related objects, ensuring audit logs are created.

        This method:
        1.  Deletes related event contact information.
        2.  Creates an audit log entry for the user deletion.
        3.  Deletes all related objects of the user.
        4.  Deletes the user object itself, disabling audit logging for this step.
            (to prevent foreign key constraint violations).
        """
        # Anonymize contact info data in event details
        self.delete_related_p_event_contact_info()

        # Manually create a log entry of the user deletion.
        # User cannot be a foreignkey in LogEntry when it's already deleted
        LogEntry.objects.log_create(
            self, force_log=True, action=LogEntry.Action.DELETE
        ).save()

        # Delete all the related objects before disabling the auditlog,
        # so auditlog will automatically create and persist LogEntry objects of them.
        self._delete_related_objects(*args, **kwargs)

        # Delete the user without creating an auditlog entry,
        # because the log entry is already created above and
        # there would be a foreign key constraint violation
        # if the log entry is not created before the user is deleted.
        with disable_auditlog():
            super().delete(*args, **kwargs)


class Organisation(GDPRModel, SerializableMixin, models.Model):
    TYPE_USER = "user"
    TYPE_PROVIDER = "provider"
    ORGANISATION_TYPES = (
        (TYPE_USER, _("User")),
        (TYPE_PROVIDER, _("Provider")),
    )
    name = models.CharField(max_length=255, verbose_name=_("name"), db_index=True)
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
        max_length=255, verbose_name=_("publisher id"), db_index=True
    )

    objects = SerializableMixin.SerializableManager()

    serialize_fields = (
        {"name": "name"},
        {"name": "phone_number"},
        {"name": "type"},
        {"name": "publisher_id"},
    )

    gdpr_sensitive_data_fields = []

    class Meta:
        verbose_name = _("organisation")
        verbose_name_plural = _("organisations")
        constraints = [
            models.CheckConstraint(
                check=~Q(publisher_id__regex=r"^\s*$"),
                name="publisher_id_neq_empty_or_whitespace_only_string",
            )
        ]
        # Ordering by name is the major use case, but ordering by other
        # secondary fields to make sort order more predictable.
        ordering = ["name", "publisher_id", "id"]

    def __str__(self):
        return f"{self.name} ({self.id})"

    def is_editable_by_user(self, user):
        return user.person.organisations.filter(id=self.id).exists()


class OrganisationProposal(GDPRModel, SerializableMixin, models.Model):
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

    objects = SerializableMixin.SerializableManager()

    serialize_fields = (
        {"name": "name"},
        {"name": "phone_number"},
        {"name": "description"},
    )

    # NOTE: should the `gdpr_sensitive_data_fields` be an empty list?
    gdpr_sensitive_data_fields = ["name", "phone_number", "description"]

    class Meta:
        verbose_name = _("organisation proposal")
        verbose_name_plural = _("organisation proposals")

    def __str__(self):
        return f"{self.id} {self.name}"


class Person(GDPRModel, SerializableMixin, UUIDPrimaryKeyModel, TimestampedModel):
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

    objects = SerializableMixin.SerializableManager.from_queryset(PersonQuerySet)()

    serialize_fields = (
        {"name": "name"},
        {"name": "phone_number"},
        {"name": "email_address"},
        {"name": "language"},
        {"name": "place_ids", "accessor": lambda ids: ", ".join(ids)},
        {"name": "organisations"},
        {"name": "organisationproposal_set"},
        {"name": "studygroup_set"},
        {"name": "eventqueueenrolment_set"},
        {"name": "enrolment_set"},
    )
    gdpr_sensitive_data_fields = ["name", "phone_number", "email_address"]

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")
        ordering = ["name", "user"]

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
        from occurrences.models import Enrolment, EventQueueEnrolment, StudyGroup

        now = timezone.now()
        Enrolment.objects.filter(person=self).update(person_deleted_at=now)
        StudyGroup.objects.filter(person=self).update(person_deleted_at=now)
        EventQueueEnrolment.objects.filter(person=self).update(person_deleted_at=now)

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
