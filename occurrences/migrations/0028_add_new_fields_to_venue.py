# Generated by Django 2.2.13 on 2021-02-26 10:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("occurrences", "0027_add_unq_index_to_p_event_le_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="venuecustomdata",
            name="has_area_for_group_work",
            field=models.BooleanField(
                default=False, verbose_name="has area for group work"
            ),
        ),
        migrations.AddField(
            model_name="venuecustomdata",
            name="has_indoor_playing_area",
            field=models.BooleanField(
                default=False, verbose_name="has indoor playing area"
            ),
        ),
        migrations.AddField(
            model_name="venuecustomdata",
            name="has_outdoor_playing_area",
            field=models.BooleanField(
                default=False, verbose_name="has outdoor playing area"
            ),
        ),
        migrations.AddField(
            model_name="venuecustomdata",
            name="has_toilet_nearby",
            field=models.BooleanField(default=False, verbose_name="has toilet nearby"),
        ),
    ]
