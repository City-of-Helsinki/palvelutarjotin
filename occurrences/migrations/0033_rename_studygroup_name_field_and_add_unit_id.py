# Generated by Django 3.2.5 on 2021-11-02 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("occurrences", "0032_palvelutarjotinevent_external_enrolment_url"),
    ]

    operations = [
        migrations.RenameField(
            model_name="studygroup", old_name="name", new_name="unit_name",
        ),
        migrations.AddField(
            model_name="studygroup",
            name="unit_id",
            field=models.CharField(
                blank=False, max_length=255, null=True, verbose_name="unit id"
            ),
        ),
    ]