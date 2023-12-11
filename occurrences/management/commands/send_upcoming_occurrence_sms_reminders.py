from django.core.management.base import BaseCommand

from occurrences.models import Enrolment


class Command(BaseCommand):
    help = "Send upcoming occurrences' SMS reminders"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            "-d",
            help="Number of days to event's occurrence",
            required=True,
            type=int,
        )

    def handle(self, *args, **options):
        days_to_occurrence = options["days"]
        enrolments = Enrolment.objects.approved_enrolments_occurring_after_days(
            days_to_occurrence=days_to_occurrence
        )
        self.stdout.write(
            f"{len(enrolments)} approved enrolments found "
            f"{days_to_occurrence} days before the occurrence."
        )
        for enrolment in enrolments:
            enrolment.send_upcoming_occurrence_sms_reminder()
        self.stdout.write(
            self.style.SUCCESS("The upcoming occurrences' SMS reminders are now sent!")
        )
