# Generated by Django 3.2.13 on 2023-01-05 08:24

from django.db import migrations
import organisations.models


class Migration(migrations.Migration):
    dependencies = [
        ("organisations", "0009_alter_user_managers"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", organisations.models.CustomUserManager()),
            ],
        ),
    ]
