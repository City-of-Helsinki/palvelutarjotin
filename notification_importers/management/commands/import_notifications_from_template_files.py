from django.core.management import BaseCommand

from notification_importers.notification_importer import (
    NotificationFileImporter,
    NotificationImporterException,
)


class Command(BaseCommand):

    help = "Import notifications from template files."

    def handle(self, *args, **options):
        self.stdout.write("Importing notifications from template files...")

        try:
            importer = NotificationFileImporter()
            (
                num_of_created,
                num_of_updated,
            ) = importer.create_missing_and_update_existing_notifications()
        except NotificationImporterException as e:
            self.stdout.write(self.style.ERROR(e))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Great success! Created {num_of_created} new notification(s) and "
                f"updated {num_of_updated} already existing notification(s)."
            )
        )
