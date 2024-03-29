# Generated by Django 2.2.10 on 2020-06-02 13:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("occurrences", "0006_add_enrolment_end_days"),
    ]

    operations = [
        migrations.AddField(
            model_name="venuecustomdata",
            name="has_clothing_storage",
            field=models.BooleanField(
                default=False, verbose_name="has outer clothing storage"
            ),
        ),
        migrations.AddField(
            model_name="venuecustomdata",
            name="has_snack_eating_place",
            field=models.BooleanField(
                default=False, verbose_name="has snack eating place"
            ),
        ),
    ]
