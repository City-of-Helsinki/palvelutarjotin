from django.utils.translation import ugettext_lazy as _
from django_ilmoitin.registry import notifications
from organisations.consts import NotificationTemplate

TEMPLATES = [
    (NotificationTemplate.MYPROFILE_CREATION, _("My profile creation")),
]
for template in TEMPLATES:
    notifications.register(template[0], template[1])
