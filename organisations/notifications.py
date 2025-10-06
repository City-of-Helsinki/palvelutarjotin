from django.utils.translation import gettext_lazy as _
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.registry import notifications

from organisations.consts import NotificationTemplate
from organisations.factories import (
    OrganisationFactory,
    OrganisationProposalFactory,
    PersonFactory,
)
from organisations.services import get_user_change_form_url, get_user_list_url

TEMPLATES = [
    (NotificationTemplate.MYPROFILE_CREATION, _("My profile creation")),
    (NotificationTemplate.MYPROFILE_ACCEPTED, _("My profile accepted")),
]
for template in TEMPLATES:
    notifications.register(template[0], template[1])

organisation = OrganisationFactory.build()
person = PersonFactory.build(organisations=[organisation])
organisation_proposal = OrganisationProposalFactory.build(applicant=person)

DEFAULT_DUMMY_CONTEXT = {
    "preview_mode": False,
    "person": person,
    "custom_message": "Custom message.",
}

dummy_context.update(
    {
        NotificationTemplate.MYPROFILE_CREATION: {
            **DEFAULT_DUMMY_CONTEXT,
            "user_change_form_url": get_user_change_form_url(person),
            "user_list_url": get_user_list_url(),
        },
        NotificationTemplate.MYPROFILE_ACCEPTED: DEFAULT_DUMMY_CONTEXT,
    }
)
