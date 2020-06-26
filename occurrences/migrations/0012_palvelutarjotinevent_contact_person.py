# Generated by Django 2.2.10 on 2020-06-26 07:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organisations", "0004_person_language"),
        ("occurrences", "0011_add_contact_fields_to_p_event"),
    ]

    operations = [
        migrations.AddField(
            model_name="palvelutarjotinevent",
            name="contact_person",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="p_event",
                to="organisations.Person",
                verbose_name="contact person",
            ),
        ),
    ]
