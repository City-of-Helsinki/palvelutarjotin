from datetime import datetime

from django.core.management.base import BaseCommand
from reports.services import sync_enrolment_reports


class Command(BaseCommand):
    help = (
        "Synchronize enrolment reports from enrolment table. "
        + "Latest sync time will be determined from "
        + "updated_at -field in a enrolment_reports table. "
        + "Enrolments after that date will be updated "
        + "if the enrolment status has changed "
        + "and created if they are totally missing from the table content."
    )

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--sync_from",
            nargs=1,
            type=str,
            help="Determine the date from where to start the sync",
        )

    def handle(self, *args, **options):
        sync_from = None
        if options["sync_from"]:
            sync_from = datetime.fromisoformat(options["sync_from"][0])
        sync_enrolment_reports(sync_from=sync_from)

        self.stdout.write(
            self.style.SUCCESS("Successfully synced the enrolment reports!")
        )
