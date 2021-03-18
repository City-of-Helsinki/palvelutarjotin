# Generated by Django 2.2.13 on 2021-03-08 09:04
from django.db import migrations
from django.utils.translation import ugettext_lazy as _
from occurrences.models import Language

LANGUAGES = (("ar", _("Arabic")), ("ru", _("Russia")), ("zh_hans", _("Chinese")))


def add_new_languages(apps, schema_editor):
    for code, name in LANGUAGES:
        Language.objects.create(id=code, name=name)


def reverse_language_additions(apps, schema_editor):
    Language.objects.filter(id__in=[code for code, _ in LANGUAGES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("occurrences", "0028_add_new_fields_to_venue"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="language",
            options={
                "ordering": ("name", "id"),
                "verbose_name": "language",
                "verbose_name_plural": "languages",
            },
        ),
        migrations.RunPython(
            add_new_languages, reverse_code=reverse_language_additions
        ),
    ]
