import uuid

import django
from django.conf import settings
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from parler.managers import TranslatableQuerySet as ParlerTranslatableQuerySet
from parler.models import TranslatableModel as ParlerTranslatableModel

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
    def create_translatable_object(self, **kwargs):
        translations = kwargs.pop("translations")
        obj = self.create(**kwargs)
        obj.create_or_update_translations(translations)
        return obj

    def _extract_model_params(self, defaults, **kwargs):
        # FIXME: Remove this method when it's possible to update to django-parler 2.0,
        # (which is not compatible with django-ilmoitin atm). This function is cherry
        # picked from django-parler 2.0 to fix a bug when calling
        # queryset.get_or_create(**params)
        translated_defaults = {}
        if defaults:
            for field in self.model._parler_meta.get_all_fields():
                try:
                    translated_defaults[field] = defaults.pop(field)
                except KeyError:
                    pass

        if django.VERSION < (2, 2):
            lookup, params = super(
                ParlerTranslatableQuerySet, self
            )._extract_model_params(defaults, **kwargs)
            params.update(translated_defaults)
            return lookup, params
        else:
            params = super(ParlerTranslatableQuerySet, self)._extract_model_params(
                defaults, **kwargs
            )
            params.update(translated_defaults)
            return params


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
            language_code = translation.pop("language_code")
            if language_code not in settings.PARLER_SUPPORTED_LANGUAGE_CODES:
                continue
            self.create_translation(language_code=language_code, **translation)

    def clear_translations(self):
        for code in self.get_available_languages():
            self.delete_translation(code)
