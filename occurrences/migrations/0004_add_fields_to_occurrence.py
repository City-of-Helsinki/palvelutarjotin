# Generated by Django 2.2.10 on 2020-05-27 08:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("occurrences", "0003_add_palvelutarjotin_event"),
    ]

    operations = [
        migrations.RenameField(
            model_name="enrolment",
            old_name="group",
            new_name="study_group",
        ),
        migrations.RemoveField(
            model_name="occurrence",
            name="groups",
        ),
        migrations.AddField(
            model_name="occurrence",
            name="amount_of_seats",
            field=models.PositiveSmallIntegerField(
                default=0, verbose_name="amount of seats"
            ),
        ),
        migrations.AddField(
            model_name="occurrence",
            name="auto_acceptance",
            field=models.BooleanField(default=False, verbose_name="auto acceptance"),
        ),
        migrations.AddField(
            model_name="occurrence",
            name="study_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="occurrences",
                through="occurrences.Enrolment",
                to="occurrences.StudyGroup",
                verbose_name="study group",
            ),
        ),
    ]
