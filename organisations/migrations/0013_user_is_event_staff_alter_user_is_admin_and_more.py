# Generated by Django 4.2.20 on 2025-05-05 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0012_alter_person_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_event_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can access the Kultus Admin UI (React app) as an event provider to manage events and their enrolments. Note that staff users are automatically also event staff members.', verbose_name='Event Admin (in Kultus Admin UI)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, help_text='Designates whether the user actively administrates the provider users. Admins receives some administrative emails, e.g, whenever a user requests a provider user status and an access to the Kultus Admin UI. Note that admin users are automatically also staff members.', verbose_name='Admin status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into the Django Admin site. This permission is primarily intended for internal Django administration tasks. Note that staff users are automatically also event staff members.', verbose_name='Staff Status (Django Admin)'),
        ),
    ]
