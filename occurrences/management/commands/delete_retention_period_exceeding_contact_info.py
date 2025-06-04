from django.core.management.base import BaseCommand

from occurrences.models import PalvelutarjotinEvent
from organisations.models import EnrolleePersonalData


class Command(BaseCommand):
    help = (
        "Delete retention period exceeding contact info from PalveluTarjotinEvents "
        "and EnrolleePersonalData."
    )

    def add_arguments(self, parser):
        """
        Adds arguments to the command to allow selective execution of deletion methods.
        """
        parser.add_argument(
            "--delete-event-contact-info",
            action="store_true",
            default=False,
            help="Only delete contact info from PalveluTarjotinEvents. "
            "(NOTE: This can be stacked with other flags)",
        )
        parser.add_argument(
            "--delete-enrollee-personal-data",
            action="store_true",
            default=False,
            help="Only delete personal data from EnrolleePersonalData. "
            "(NOTE: This can be stacked with other flags)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Perform a dry run without actually deleting any data. "
            "Shows what would be deleted.",
        )

    def handle(self, *args, **kwargs):
        """
        Handles the execution of the command based on the provided arguments.
        If no flags are provided, both deletion methods are run.
        If at least one flag is provided, only the methods corresponding to the
        set flags will be executed.
        The --dry-run flag prevents actual deletions.
        """
        delete_event_contact_info = kwargs["delete_event_contact_info"]
        delete_enrollee_personal_data = kwargs["delete_enrollee_personal_data"]
        dry_run = kwargs["dry_run"]

        if dry_run:
            self.stdout.write(self.style.WARNING("--- DRY RUN MODE ---"))
            self.stdout.write(self.style.WARNING("No data will be deleted."))

        # Determine which methods to run
        if delete_event_contact_info or delete_enrollee_personal_data:
            self.stdout.write(
                self.style.NOTICE("Running selected deletion methods based on flags.")
            )
            if delete_event_contact_info:
                self.__delete_p_event_contact_info(dry_run=dry_run)
            if delete_enrollee_personal_data:
                self.__delete_enrollee_personal_data(dry_run=dry_run)
        else:
            # No flags provided, run both (default behavior)
            self.stdout.write(
                self.style.NOTICE(
                    "Running: Both deletion methods "
                    "(default behavior as no flags were provided)."
                )
            )
            self.__delete_p_event_contact_info(dry_run=dry_run)
            self.__delete_enrollee_personal_data(dry_run=dry_run)

    def __delete_p_event_contact_info(self, dry_run=False):
        """
        Deletes contact information from PalvelutarjotinEvent objects
        that have exceeded their retention period.
        If dry_run is True, it only reports what would be deleted.
        """
        self.stdout.write(
            "Checking contact info from PalveluTarjotinEvents that are exceeding "
            "the retention period..."
        )

        try:
            events = (
                PalvelutarjotinEvent.objects.contact_info_retention_period_exceeded()
            )
            count_to_delete = events.count()

            if dry_run:
                msg_prefix = "Would delete"
                deleted_contact_info_count = 0  # No actual deletion in dry run
            else:
                msg_prefix = "Deleted"
                deleted_contact_info_count = events.delete_contact_info()

            if count_to_delete == 0:
                msg = "No events are exceeding the retention period."
            else:
                if dry_run:
                    msg = f"{msg_prefix} contact info from {count_to_delete} event(s)."
                else:
                    msg = f"{msg_prefix} contact info from {deleted_contact_info_count} event(s)."  # noqa: E501

            self.stdout.write(self.style.SUCCESS(msg))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error checking/deleting event contact info: {e}")
            )

    def __delete_enrollee_personal_data(self, dry_run=False):
        """
        Deletes EnrolleePersonalData objects (persons) that have exceeded
        their retention period.
        If dry_run is True, it only reports what would be deleted.
        """
        self.stdout.write("Checking persons that are exceeding the retention period...")

        try:
            persons = EnrolleePersonalData.objects.retention_period_exceeded()
            count_to_delete = persons.count()

            if dry_run:
                msg_prefix = "Would delete"
                deleted_personal_data_count = 0  # No actual deletion in dry run
            else:
                msg_prefix = "Deleted"
                deleted_personal_data_count, _ = persons.delete()

            if count_to_delete == 0:
                msg = "No personal data are exceeding the retention period."
            else:
                if dry_run:
                    msg = f"{msg_prefix} {count_to_delete} person(s)."
                else:
                    msg = f"{msg_prefix} {deleted_personal_data_count} person(s)."

            self.stdout.write(self.style.SUCCESS(msg))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error checking/deleting enrollee personal data: {e}")
            )
