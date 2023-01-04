from django.core.management.base import BaseCommand

from occurrences.models import PalvelutarjotinEvent


class Command(BaseCommand):
    help = "Delete retention period exceeding contact info from PalveluTarjotinEvents"

    def handle(self, *args, **kwargs):
        self.stdout.write(
            "Deleting contact info from PalveluTarjotinEvents that are exceeding "
            "the retention period..."
        )

        num_of_deleted_contact_info = (
            PalvelutarjotinEvent.objects.contact_info_retention_period_exceeded().delete_contact_info()  # noqa: E501
        )

        msg = (
            "No events are exceeding the retention period."
            if num_of_deleted_contact_info == 0
            else f"Deleted contact info from {num_of_deleted_contact_info} event(s)."
        )
        self.stdout.write(self.style.SUCCESS(msg))
