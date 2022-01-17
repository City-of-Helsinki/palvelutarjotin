from django.conf import settings
from django.core.management.base import BaseCommand
from occurrences.models import Enrolment


class Command(BaseCommand):
    help = "Send enrolments summary report to provider"

    def handle(self, *args, **kwargs):
        if settings.ENABLE_SUMMARY_REPORT:
            Enrolment.send_enrolment_summary_report_to_providers()
