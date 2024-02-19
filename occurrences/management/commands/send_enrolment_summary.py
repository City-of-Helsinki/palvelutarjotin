from django.conf import settings
from django.core.management.base import BaseCommand

from occurrences.notification_services import (
    send_enrolment_summary_report_to_providers_from_days,
)


class Command(BaseCommand):
    help = "Send enrolments summary report to provider"

    def handle(self, *args, **kwargs):
        if settings.ENABLE_SUMMARY_REPORT:
            send_enrolment_summary_report_to_providers_from_days(days=1)
