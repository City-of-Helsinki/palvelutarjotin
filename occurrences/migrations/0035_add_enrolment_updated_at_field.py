# Generated by Django 3.2.5 on 2021-11-17 19:48

from django.db import migrations, models
from django.db.models import F


def set_enrolment_time_tom_updated_at(apps, schema_editor):
    """Set enrolment time to Enrolment instances empty updated at fields."""
    Enrolment = apps.get_model("occurrences", "Enrolment")
    Enrolment.objects.all().update(updated_at=F("enrolment_time"))


class Migration(migrations.Migration):

    dependencies = [
        ("occurrences", "0034_alter_studygroup_unit_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="enrolment",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="updated at"),
        ),
        migrations.AlterField(
            model_name="enrolment",
            name="enrolment_time",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="enrolment time"
            ),
        ),
        migrations.RunPython(set_enrolment_time_tom_updated_at),
    ]
