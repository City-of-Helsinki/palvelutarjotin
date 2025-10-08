from django.core.management import BaseCommand

from notification_importers.notification_importer import (
    NotificationGoogleSheetImporter,
    NotificationImporterExceptionError,
)


class Command(BaseCommand):
    help = "Import notifications from Google Sheets."

    def handle(self, *args, **options):
        self.stdout.write("Importing notifications from Google Sheets...")

        try:
            importer = NotificationGoogleSheetImporter()
            (
                num_of_created,
                num_of_updated,
            ) = importer.create_missing_and_update_existing_notifications()
        except NotificationImporterExceptionError as e:
            self.stdout.write(self.style.ERROR(e))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Great success! Created {num_of_created} new notification(s) and "
                f"updated {num_of_updated} already existing notification(s)."
            )
        )
