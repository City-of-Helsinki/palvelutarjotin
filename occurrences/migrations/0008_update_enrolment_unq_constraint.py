# Generated by Django 2.2.10 on 2020-06-01 09:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("occurrences", "0007_add_fields_to_venues"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="enrolment",
            name="unq_group_occurrence",
        ),
        migrations.AddConstraint(
            model_name="enrolment",
            constraint=models.UniqueConstraint(
                fields=("study_group", "occurrence"), name="unq_group_occurrence"
            ),
        ),
    ]
