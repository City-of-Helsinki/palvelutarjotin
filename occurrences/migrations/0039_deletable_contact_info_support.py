# Generated by Django 3.2.13 on 2022-12-29 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organisations", "0008_person_place_ids"),
        ("occurrences", "0038_deletable_person_support"),
    ]

    operations = [
        migrations.AddField(
            model_name="palvelutarjotinevent",
            name="contact_info_deleted_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="contact info deleted at"
            ),
        ),
        migrations.AlterField(
            model_name="palvelutarjotinevent",
            name="contact_person",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="p_event",
                to="organisations.person",
                verbose_name="contact person",
            ),
        ),
    ]
