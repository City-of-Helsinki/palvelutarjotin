import logging
from django.conf import settings
from django.db import models
from django_ilmoitin.models import NotificationTemplate, NotificationTemplateException
from django_ilmoitin.utils import render_notification_template, send_notification
from typing import List, Union

import occurrences.models as occurrences_models
from common.notification_service import NotificationService
from occurrences.consts import NOTIFICATION_TYPE_EMAIL, NOTIFICATION_TYPE_SMS
from occurrences.consts import NotificationTemplate as NotificationTemplateConstants

notification_service = NotificationService(
    settings.NOTIFICATION_SERVICE_API_TOKEN, settings.NOTIFICATION_SERVICE_API_URL
)
logger = logging.getLogger(__name__)


def send_enrolment_summary_report_to_providers(
    enrolments: Union[models.QuerySet, List["occurrences_models.Enrolment"]]
):
    logger.info("Creating enrolment report summaries...")
    reports = {}
    p_events = (
        occurrences_models.PalvelutarjotinEvent.objects.filter(
            occurrences__enrolments__in=enrolments
        )
        .prefetch_related("occurrences__enrolments")
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
                        ).distinct(),
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
    person,
    occurrence,
    study_group,
    notification_type,
    notification_template_id,
    notification_sms_template_id,
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

    if NOTIFICATION_TYPE_EMAIL in notification_type:
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
        if NOTIFICATION_TYPE_SMS in notification_type and person.phone_number:
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
):
    if not language:
        language = settings.LANGUAGES[0][0]
    if not settings.NOTIFICATION_SERVICE_API_URL:
        logger.warning(
            "Notification sms service settings is missing, not sending any SMS"
        )
        return
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
        return

    try:
        _, _, body_text = render_notification_template(template, context, language)
    except NotificationTemplate.DoesNotExist:
        logger.debug(
            'NotificationTemplate "{}" does not exist, not sending anything.'.format(
                notification_template_id
            )
        )
        return
    except NotificationTemplateException as e:
        logger.error(e, exc_info=True)
        return

    if language in getattr(settings, "TRANSLATED_SMS_SENDER", {}):
        sender = settings.TRANSLATED_SMS_SENDER[language]
    else:
        sender = settings.DEFAULT_SMS_SENDER

    resp = notification_service.send_sms(
        sender=sender, destinations=destinations, text=body_text
    )
    # TODO: Do we need to store the delivery log in Palvelutarjotin
    if resp.status_code != 200:
        logger.warning("SMS message sent failed")
