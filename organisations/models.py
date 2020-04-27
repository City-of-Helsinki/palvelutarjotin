from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from helusers.models import AbstractUser

from common.models import TimestampedModel, UUIDPrimaryKeyModel


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
    type = models.CharField(choices=ORGANISATION_TYPES, max_length=64)
    persons = models.ManyToManyField("Person", related_name="organisations", blank=True)

    class Meta:
        verbose_name = _("organisation")
        verbose_name_plural = _("organisations")

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

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    def __str__(self):
        return f"{self.name}"
