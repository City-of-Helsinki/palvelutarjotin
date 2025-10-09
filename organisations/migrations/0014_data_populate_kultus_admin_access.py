from django.db import migrations
from django.db.models import F


def data_populate_kultus_admin_access(apps, schema_editor):
    User = apps.get_model("organisations", "User")

    # Update non-superusers: Set is_event_staff based on is_staff and set is_staff to False
    User.objects.filter(is_superuser=False).update(
        is_event_staff=F("is_staff"), is_staff=False
    )

    # Update superusers: Set is_staff and is_event_staff to True
    User.objects.filter(is_superuser=True).update(is_staff=True, is_event_staff=True)


def reverse_data_populate_kultus_admin_access(apps, schema_editor):
    User = apps.get_model("organisations", "User")

    # WARNING: Reversing this data migration might lead to data loss in the
    # 'is_staff' field for non-superusers if the 'is_event_staff' field has
    # been modified after the forward migration.

    # Reverse for non-superusers: Set is_staff based on is_event_staff
    User.objects.filter(is_superuser=False).update(is_staff=F("is_event_staff"))

    # Reverse for all users: Set is_event_staff to False (as it was the new field)
    User.objects.all().update(is_event_staff=False)


class Migration(migrations.Migration):
    dependencies = [
        ("organisations", "0013_user_is_event_staff_alter_user_is_admin_and_more"),
    ]

    operations = [
        migrations.RunPython(
            data_populate_kultus_admin_access, reverse_data_populate_kultus_admin_access
        ),
    ]
