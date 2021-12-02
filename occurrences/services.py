from typing import List, Union

import occurrences.models as occurrences_models
from django.db import models
from django_ilmoitin.utils import send_notification
from occurrences.consts import NotificationTemplate


def send_enrolment_summary_report_to_providers(
    enrolments: Union[models.QuerySet, List["occurrences_models.Enrolment"]]
):
    reports = {}
    p_events = (
        occurrences_models.PalvelutarjotinEvent.objects.filter(
            occurrences__enrolments__in=enrolments
        )
        .prefetch_related("occurrences__enrolments")
        .distinct()
    )

    for p_event in p_events:
        # Group by contact_email address:
        reports.setdefault(p_event.contact_email, []).append(p_event)

    for address, report in reports.items():
        context_report = []
        for p_event in report:
            context_report.append(
                {
                    "event": p_event.get_event_data(),
                    "p_event": p_event,
                    "occurrences": p_event.occurrences.filter(
                        enrolments__in=enrolments
                    ).distinct(),
                }
            )
        context = {
            "report": context_report,
            "total_pending_enrolments": enrolments.pending_enrolments_by_email(
                address
            ).count(),
            "total_new_enrolments": enrolments.new_enrolments_by_email(address).count(),
        }
        send_notification(
            address, NotificationTemplate.ENROLMENT_SUMMARY_REPORT, context
        )
