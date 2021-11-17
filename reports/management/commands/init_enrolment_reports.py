from django.core.management.base import BaseCommand
from occurrences.models import Enrolment
from reports.models import EnrolmentReport


class Command(BaseCommand):
    help = "Initialize enrolment reports"

    def handle(self, *args, **kwargs):
        if EnrolmentReport.objects.exists():
            raise RuntimeError(
                "Cannot initialize the enrolment reports "
                + "when the database table is not empty!"
            )

        reports = [
            EnrolmentReport(enrolment=enrolment)
            for enrolment in Enrolment.objects.all()
        ]
        EnrolmentReport.objects.bulk_create(reports)
