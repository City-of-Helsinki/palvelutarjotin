from datetime import timedelta
from secrets import token_urlsafe

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from palvelutarjotin import settings


class VerificationTokenManager(models.Manager):
    def create_token(self, obj, user, verification_type, email=None, expiry_days=None):

        key = self.model.generate_key()

        if expiry_days is None:  # can be False
            expiry_days = getattr(settings, "VERIFICATION_TOKEN_VALID_DAYS", 14)

        if expiry_days:
            expiry_date = timezone.now() + timedelta(days=expiry_days)
        else:
            expiry_date = None

        if email is None and user is not None:
            email = user.email

        return self.create(
            content_type=ContentType.objects.get_for_model(obj.__class__),
            object_id=obj.id,
            user=user,
            verification_type=verification_type,
            email=email,
            key=key,
            expiry_date=expiry_date,
        )


class VerificationToken(models.Model):

    VERIFICATION_TYPE_CANCELLATION = "CANCELLATION"

    VERIFICATION_TOKEN_TYPE_CHOICES = [
        (VERIFICATION_TYPE_CANCELLATION, _("Cancellation")),
    ]

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # NOTE: TextField object_id might have some issues with postgre (so far so good):
    # - https://code.djangoproject.com/ticket/16055
    # - https://stackoverflow.com/a/49768257/784642
    object_id = models.TextField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    key = models.CharField(_("verification key"), max_length=255)
    expiry_date = models.DateTimeField(null=True, blank=True)
    verification_type = models.CharField(
        max_length=64,
        verbose_name=_("verification type"),
        choices=VERIFICATION_TOKEN_TYPE_CHOICES,
    )
    email = models.EmailField(_("e-mail address"), null=True, blank=True)
    # is_active can be used to determine whether or not the token was already used.
    # is_active makes the difference between used and non-existing token.
    is_active = models.BooleanField(null=False, blank=False, default=True)

    objects = VerificationTokenManager()

    def __unicode__(self):
        return self.key

    @classmethod
    def generate_key(cls):
        """ Generates a new key for a verification token. """
        return token_urlsafe(getattr(settings, "VERIFICATION_TOKEN_LENGTH", 32))

    def is_valid(self):
        """ Validates token state. """
        return bool(
            self.is_active
            and self.key
            and (self.expiry_date is None or timezone.now() <= self.expiry_date)
        )
