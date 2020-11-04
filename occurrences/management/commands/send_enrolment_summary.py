from django.core.management.base import BaseCommand
from occurrences.models import Enrolment


class Command(BaseCommand):
    help = "Send enrolments summary report to provider"

    def handle(self, *args, **kwargs):
        Enrolment.objects.filter(status=Enrolment.STATUS_PENDING).select_related(
            "occurrence__p_event"
        ).send_enrolment_summary_report_to_providers()
