# Generated by Django 3.2.5 on 2021-07-14 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organisations", "0006_user_is_admin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
