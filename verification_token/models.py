from datetime import timedelta
from secrets import token_urlsafe

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from organisations.models import Person


class VerificationTokenManager(models.Manager):
    def deactivate_token(
        self, obj_or_class, key=None, verification_type=None, person=None
    ):
        """
        Deactivate a token. Key parameters is used and must be given
        when using a model class instead of model instance.
        """
        qs = self.filter_active_tokens(obj_or_class, key, verification_type, person)
        qs.update(is_active=False)

    def deactivate_and_create_token(
        self,
        obj,
        person,
        verification_type,
        expiry_minutes=getattr(settings, "VERIFICATION_TOKEN_VALID_MINUTES", 15),
    ):
        """
        Deactivate old tokens (of a type) and create a new one.
        """
        self.deactivate_token(obj, verification_type=verification_type, person=person)
        return self.create_token(obj, person, verification_type, expiry_minutes)

    def create_token(
        self,
        obj,
        person,
        verification_type,
        email=None,
        expiry_minutes=getattr(settings, "VERIFICATION_TOKEN_VALID_MINUTES", 15),
    ):

        key = self.model.generate_key()

        if expiry_minutes:
            expiry_date = timezone.now() + timedelta(minutes=expiry_minutes)
        else:
            expiry_date = None

        # If there is no given email, use the person's email
        if email is None and person is not None:
            email = person.email_address

        return self.create(
            content_type=ContentType.objects.get_for_model(obj.__class__),
            object_id=obj.id,
            person=person,
            verification_type=verification_type,
            email=email,
            key=key,
            expiry_date=expiry_date,
        )

    def filter_active_tokens(
        self, obj_or_class, key=None, verification_type=None, person=None
    ):
        """
        Filter active tokens given for a class (of an instance).
        """
        qs = self.filter(
            is_active=True,
            content_type=ContentType.objects.get_for_model(obj_or_class),
        )

        if verification_type:
            qs = qs.filter(verification_type=verification_type)

        if person:
            qs = qs.filter(person=person)

        # If the given parameter is a model instance, use it in query
        if isinstance(obj_or_class, models.Model):
            qs = qs.filter(object_id=obj_or_class.pk)

        # If the given parameter is a class and not an instance of it,
        # use the key parameter in a query
        return qs.filter(key=key) if key else qs

    def clean_invalid_tokens(self, clean_inactive=True, clean_expired=True):
        """
        Clean inactive and expired tokens.
        """
        if clean_inactive and clean_expired:
            self.filter(
                Q(is_active=False) | Q(expiry_date__lte=timezone.now())
            ).delete()
        elif clean_inactive:
            self.filter(is_active=False).delete()
        elif clean_expired:
            self.filter(expiry_date__lte=timezone.now()).delete()


class VerificationToken(models.Model):

    VERIFICATION_TYPE_CANCELLATION = "CANCELLATION"

    VERIFICATION_TOKEN_TYPE_CHOICES = [
        (VERIFICATION_TYPE_CANCELLATION, _("Cancellation")),
    ]

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    person = models.ForeignKey(Person, null=True, on_delete=models.CASCADE)
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
