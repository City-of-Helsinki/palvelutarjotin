import logging

from django.conf import settings
from django_ilmoitin.models import NotificationTemplate, NotificationTemplateException
from django_ilmoitin.utils import render_notification_template, send_notification
from occurrences.consts import NOTIFICATION_TYPE_EMAIL, NOTIFICATION_TYPE_SMS

from common.notification_service import NotificationService
from palvelutarjotin.settings import (
    NOTIFICATION_SERVICE_API_TOKEN,
    NOTIFICATION_SERVICE_API_URL,
)

notification_service = NotificationService(
    NOTIFICATION_SERVICE_API_TOKEN, NOTIFICATION_SERVICE_API_URL
)
logger = logging.getLogger(__name__)


def send_event_notifications_to_contact_person(
    person,
    occurrence,
    study_group,
    notification_type,
    notification_template_id,
    notification_sms_template_id,
    **kwargs,
):
    if not person:
        person = study_group.person
    if NOTIFICATION_TYPE_EMAIL in notification_type:
        context = {
            "occurrence": occurrence,
            "study_group": study_group,
            **kwargs,
        }
        # TODO: Send notification based on user language
        send_notification(
            person.email_address,
            notification_template_id,
            language=study_group.person.language,
            context=context,
        )
    if NOTIFICATION_TYPE_SMS in notification_type:
        context = {
            "occurrence": occurrence,
            "study_group": study_group,
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


def send_sms_notification(
    destinations, notification_template_id, context=None, language=None
):
    if not language:
        language = settings.LANGUAGES[0][0]
    if not settings.NOTIFICATION_SERVICE_API_URL:
        logger.warning(
            "Notification sms service settings is missing, not sending any" "SMS"
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
        logger.warning(f"SMS message sent failed")
