# Generated by Django 3.2.5 on 2021-12-30 06:43

import django.db.models.deletion
import parler.fields
import parler.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("occurrences", "0036_alter_studygroup_extra_needs"),
    ]

    operations = [
        migrations.CreateModel(
            name="TranslatedPalvelutarjotinEvent",
            fields=[],
            options={"proxy": True, "indexes": [], "constraints": []},
            bases=(
                parler.models.TranslatableModelMixin,
                "occurrences.palvelutarjotinevent",
                models.Model,
            ),
        ),
        migrations.AlterField(
            model_name="occurrence",
            name="p_event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="occurrences",
                to="occurrences.translatedpalvelutarjotinevent",
                verbose_name="palvelutarjotin event",
            ),
        ),
        migrations.CreateModel(
            name="TranslatedPalvelutarjotinEventTranslation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                (
                    "auto_acceptance_message",
                    models.TextField(
                        blank=True,
                        help_text="A custom message included in notification template when auto acceptance is set on.",  # noqa
                        null=True,
                        verbose_name="custom message in auto acceptance",
                    ),
                ),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="occurrences.translatedpalvelutarjotinevent",
                    ),
                ),
            ],
            options={
                "verbose_name": "translated palvelutarjotin event Translation",
                "db_table": "occurrences_translatedpalvelutarjotinevent_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
                "unique_together": {("language_code", "master")},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
