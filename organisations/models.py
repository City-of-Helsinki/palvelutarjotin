from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from helusers.models import AbstractUser

from common.models import TimestampedModel, UUIDPrimaryKeyModel


class PersonQuerySet(models.QuerySet):
    def user_can_view(self, user):
        # Only return profile of logged in user if he's not staff
        if user.is_staff:
            return self
        elif user.is_authenticated:
            return self.filter(user=user)
        else:
            return self.none()


class User(AbstractUser):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


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
        return f"{self.id} {self.name}"

    def is_editable_by_user(self, user):
        return user.person.organisations.filter(id=self.id).exists()


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

    objects = PersonQuerySet.as_manager()

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    def __str__(self):
        return f"{self.name}"
