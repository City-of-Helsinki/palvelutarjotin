# Generated by Django 2.2.13 on 2021-02-09 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("occurrences", "0025_palvelutarjotinevent_payment_instruction"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="palvelutarjotinevent",
            name="payment_instruction",
        ),
    ]
