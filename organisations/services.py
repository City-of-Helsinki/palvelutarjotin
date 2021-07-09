from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_ilmoitin.utils import send_notification
from organisations.consts import NotificationTemplate

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from organisations.models import Person


def get_user_change_form_url(person: Person, domain=settings.SITE_URL):
    return domain + reverse("admin:organisations_user_change", args=(person.id,))


def get_user_list_url(domain=settings.SITE_URL):
    return domain + reverse("admin:organisations_user_changelist")


def get_admin_emails():
    return list(
        get_user_model().objects.filter(is_admin=True).values_list("email", flat=True)
    )


def send_myprofile_creation_notification_to_admins(person: Person, **kwargs):
    """
    Notify the admins about a new user creation.
    """

    admin_emails = get_admin_emails()

    context = {
        "person": person,
        "user_change_form_url": get_user_change_form_url(person, settings.SITE_URL),
        "user_list_url": get_user_list_url(settings.SITE_URL),
        **kwargs,
    }

    for admin_email in admin_emails:
        # TODO: Send notification based on admin user's language
        send_notification(
            admin_email, NotificationTemplate.MYPROFILE_CREATION, context=context,
        )


def send_myprofile_organisations_accepted_notification(person: Person, **kwargs):
    """
    Notify the person about his / her account is accepted and ready to use.
    This notification should be sent at least when the user has
    write permissions for events (the  is_staff -flag is set to True)
    and he has been linked to some organisations.
    """
    context = {"person": person, **kwargs}
    # TODO: Send notification based on admin user's language
    send_notification(
        person.email_address, NotificationTemplate.MYPROFILE_ACCEPTED, context=context
    )
