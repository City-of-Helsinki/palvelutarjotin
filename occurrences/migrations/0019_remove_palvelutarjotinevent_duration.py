# Generated by Django 2.2.13 on 2020-10-20 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("occurrences", "0018_move_auto_acceptance_to_p_event"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="palvelutarjotinevent",
            name="duration",
        ),
    ]
