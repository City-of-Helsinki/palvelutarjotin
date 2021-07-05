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


def send_myprofile_creation_notification_to_admins(person: Person, **kwargs):
    """
    Notify the admins about a new user creation.
    """
    admins = get_user_model().objects.filter(is_admin=True)

    user_change_form_url = settings.SITE_URL + reverse(
        "admin:organisations_user_change", args=(person.id,)
    )
    user_list_url = settings.SITE_URL + reverse("admin:organisations_user_changelist")

    context = {
        "person": person,
        "user_change_form_url": user_change_form_url,
        "user_list_url": user_list_url,
        **kwargs,
    }
    for admin in admins:
        # TODO: Send notification based on admin user's language
        send_notification(
            admin.email, NotificationTemplate.MYPROFILE_CREATION, context=context,
        )
