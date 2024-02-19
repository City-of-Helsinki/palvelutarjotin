import logging
from django.conf import settings
from django.db import models
from django.db.models import Q
from django_ilmoitin.models import NotificationTemplate, NotificationTemplateException
from django_ilmoitin.utils import render_notification_template, send_notification
from typing import List, Optional, Union

import occurrences.models as occurrences_models
from common.notification_service import NotificationService
from occurrences.consts import NOTIFICATION_TYPE_EMAIL, NOTIFICATION_TYPE_SMS
from occurrences.consts import NotificationTemplate as NotificationTemplateConstants
from organisations.models import Person

notification_service = NotificationService(
    settings.NOTIFICATION_SERVICE_API_TOKEN, settings.NOTIFICATION_SERVICE_API_URL
)
logger = logging.getLogger(__name__)


def _get_enrolments_for_summary_report(days=1):
    return occurrences_models.Enrolment.objects.pending_and_auto_accepted_enrolments(
        days=days
    ).select_related("occurrence", "occurrence__p_event")


def _get_queued_enrolments_for_summary_report(days=1):
    return occurrences_models.EventQueueEnrolment.objects.enrolled_in_last_days(
        days=days
    )


def send_enrolment_summary_report_to_providers_from_days(days=1):
    send_enrolment_summary_report_to_providers(
        enrolments=_get_enrolments_for_summary_report(days),
        queued_enrolments=_get_queued_enrolments_for_summary_report(days),
    )


def send_enrolment_summary_report_to_providers(
    enrolments: Union[models.QuerySet, List["occurrences_models.Enrolment"]],
    queued_enrolments: Union[
        models.QuerySet, List["occurrences_models.EventQueueEnrolment"]
    ],
):
    logger.info("Creating enrolment report summaries...")
    reports = {}
    p_events = (
        occurrences_models.PalvelutarjotinEvent.objects.filter(
            Q(occurrences__enrolments__in=enrolments)
            | Q(queued_enrolments__in=queued_enrolments)
        )
        .order_by("enrolment_start")
        .prefetch_related("occurrences__enrolments", "queued_enrolments")
        .distinct()
    )
    logger.debug(f"Collected {len(p_events)} PalvelutarjotinEvents.")
    for p_event in p_events:
        # Group by contact_email address:
        reports.setdefault(p_event.contact_email, []).append(p_event)

    context_for_address = {}

    for address, report in reports.items():
        context_report = []
        for p_event in report:
            linked_events_event_data = p_event.get_event_data()
            if linked_events_event_data:
                context_report.append(
                    {
                        "event": linked_events_event_data,
                        "p_event": p_event,
                        "occurrences": p_event.occurrences.filter(
                            enrolments__in=enrolments
                        )
                        .order_by("start_time")
                        .distinct(),
                        "queued_enrolments": [
                            queued_enrolment
                            for queued_enrolment in queued_enrolments
                            if queued_enrolment.p_event == p_event
                        ],
                    }
                )

        context = {
            "report": context_report,
            "total_pending_enrolments": enrolments.pending_enrolments_by_email(
                address
            ).count(),
            "total_new_enrolments": enrolments.approved_enrolments_by_email(
                address
            ).count(),
            "total_new_queued_enrolments": sum(
                (len(report["queued_enrolments"]) for report in context_report)
            ),
        }
        context_for_address[address] = context

    emails = ",".join([address for address in context_for_address.keys()])
    logger.debug(f"Reports will be sent to these addresses: {emails}")

    # NOTE: Instead of sending the notification in the previous loop,
    # lets first collect the mail contexts to a dictionary and
    # send the mails after all the contexts have been handled properly.
    # This way we can prevent flooding the recipients with the mails
    # when some of the contexts cannot be handled because of any reason.
    # For more details, see https://helsinkisolutionoffice.atlassian.net/browse/PT-1414.
    for address, context in context_for_address.items():
        logger.debug(f"Sending enrolment summary report to {address}.")
        send_notification(
            address, NotificationTemplateConstants.ENROLMENT_SUMMARY_REPORT, context
        )
        logger.info(f"Enrolment summary report sent to {address}.")


def send_event_notifications_to_person(
    person: "Person",
    occurrence: "occurrences_models.Occurrence",
    study_group: "occurrences_models.StudyGroup",
    notification_type,
    notification_template_id: Optional[NotificationTemplateConstants],
    notification_sms_template_id: Optional[NotificationTemplateConstants],
    **kwargs,
):
    def translation(field_translation_map: object, language=None):
        """
        Get a field value translation from an objects instance.
        Try all the supported languages Parler languages as a fallback language.
        """
        if language is None:
            language = study_group.person.language

        languages = settings.PARLER_LANGUAGES["default"]["fallbacks"].copy()
        languages.insert(0, language)
        translated_value = ""
        for lang in languages:
            try:
                translated_value = field_translation_map.__getattribute__(lang)
                break
            except AttributeError:
                continue

        return translated_value

    if (
        NOTIFICATION_TYPE_EMAIL in notification_type
        and notification_template_id
        and person.email_address
    ):
        context = {
            "person": person,
            "occurrence": occurrence,
            "study_group": study_group,
            "preview_mode": False,
            "trans": translation,
            **kwargs,
        }
        # TODO: Send notification based on user language
        send_notification(
            person.email_address,
            notification_template_id,
            language=study_group.person.language,
            context=context,
        )

    if settings.NOTIFICATION_SERVICE_SMS_ENABLED:
        if (
            NOTIFICATION_TYPE_SMS in notification_type
            and notification_sms_template_id
            and person.phone_number
        ):
            context = {
                "person": person,
                "occurrence": occurrence,
                "study_group": study_group,
                "preview_mode": False,
                "trans": translation,
                **kwargs,
            }
            destinations = [
                person.phone_number,
            ]
            send_sms_notification(
                destinations,
                notification_sms_template_id,
                context,
                study_group.person.language,
            )
    else:
        logger.info(
            "Not sending SMS, because the service disabled. "
            "Enable it from the settings. NOTIFICATION_SERVICE_SMS_ENABLED=True"
        )


def send_sms_notification(
    destinations, notification_template_id, context=None, language=None
) -> bool:
    """
    Send SMS notification to the given destinations.
    @return True if the SMS was sent successfully, otherwise False.
    """
    if not language:
        language = settings.LANGUAGES[0][0]
    if not settings.NOTIFICATION_SERVICE_API_URL:
        logger.warning(
            "Notification sms service settings is missing, not sending any SMS"
        )
        return False
    if context is None:
        context = {}

    template = NotificationTemplate.objects.filter(
        type=notification_template_id
    ).first()
    if not template:
        logger.warning(
            'No notification template created for "{}" event, '
            "not sending anything.".format(notification_template_id)
        )
        return False

    try:
        _, _, body_text = render_notification_template(template, context, language)
    except NotificationTemplate.DoesNotExist:
        logger.debug(
            'NotificationTemplate "{}" does not exist, not sending anything.'.format(
                notification_template_id
            )
        )
        return False
    except NotificationTemplateException as e:
        logger.error(e, exc_info=True)
        return False

    if language in getattr(settings, "TRANSLATED_SMS_SENDER", {}):
        sender = settings.TRANSLATED_SMS_SENDER[language]
    else:
        sender = settings.DEFAULT_SMS_SENDER

    resp = notification_service.send_sms(
        sender=sender, destinations=destinations, text=body_text
    )
    # TODO: Do we need to store the delivery log in Palvelutarjotin
    sms_sent_ok = resp.status_code == 200
    if not sms_sent_ok:
        logger.warning("SMS message sent failed")
    return sms_sent_ok
