import uuid
from copy import deepcopy

from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from parler.managers import TranslatableQuerySet as ParlerTranslatableQuerySet
from parler.models import TranslatableModel as ParlerTranslatableModel

from common.utils import map_enums_to_values_in_kwargs
from palvelutarjotin.exceptions import MissingDefaultTranslationError


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"), auto_now=True)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModel(models.Model):
    id = models.UUIDField(
        verbose_name=_("UUID"), primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True


class TranslatableQuerySet(ParlerTranslatableQuerySet):
    @transaction.atomic
    @map_enums_to_values_in_kwargs
    def create_translatable_object(self, **kwargs):
        translations = kwargs.pop("translations")
        obj = self.create(**kwargs)
        obj.create_or_update_translations(translations)
        return obj


class TranslatableModel(ParlerTranslatableModel):
    objects = TranslatableQuerySet.as_manager()

    class Meta:
        abstract = True

    @transaction.atomic
    def create_or_update_translations(self, translations):
        if (
            settings.PARLER_REQUIRE_DEFAULT_TRANSLATION
            and settings.LANGUAGE_CODE
            not in [translation["language_code"] for translation in translations]
        ):
            raise MissingDefaultTranslationError("Default translation is missing")
        self.clear_translations()
        for translation in translations:
            translation = deepcopy(translation)
            language_code = translation.pop("language_code")
            if language_code not in settings.PARLER_SUPPORTED_LANGUAGE_CODES:
                continue
            self.create_translation(language_code=language_code, **translation)

    def clear_translations(self):
        for code in self.get_available_languages():
            self.delete_translation(code)


class WithDeletablePersonModel(models.Model):
    person = models.ForeignKey(
        "organisations.Person",
        verbose_name=_("person"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    person_deleted_at = models.DateTimeField(
        verbose_name=_("person deleted at"), blank=True, null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.person and self.person_deleted_at:
            # Make sure person_deleted_at is nullified if person is set again for some
            # reason. Should not be needed in normal usage.
            self.person_deleted_at = None
        return super().save(*args, **kwargs)


class SubqueryCount(models.Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = models.IntegerField()
