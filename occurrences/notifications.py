from django.utils.translation import ugettext_lazy as _
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.registry import notifications
from graphene_linked_events.tests.mock_data import EVENT_DATA
from occurrences.consts import NotificationTemplate
from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from organisations.factories import PersonFactory

TEMPLATES = [
    (NotificationTemplate.OCCURRENCE_ENROLMENT, _("occurrence enrolment")),
    (NotificationTemplate.OCCURRENCE_UNENROLMENT, _("occurrence unenrolment")),
    (NotificationTemplate.ENROLMENT_APPROVED, _("enrolment approved")),
    (NotificationTemplate.ENROLMENT_DECLINED, _("enrolment declined")),
    (NotificationTemplate.OCCURRENCE_ENROLMENT_SMS, _("occurrence enrolment sms")),
    (NotificationTemplate.OCCURRENCE_UNENROLMENT_SMS, _("occurrence unenrolment sms")),
    (NotificationTemplate.ENROLMENT_APPROVED_SMS, _("enrolment approved sms")),
    (NotificationTemplate.ENROLMENT_DECLINED_SMS, _("enrolment declined sms")),
    (NotificationTemplate.OCCURRENCE_CANCELLED, _("occurrence cancelled")),
    (NotificationTemplate.OCCURRENCE_CANCELLED_SMS, _("occurrence cancelled sms")),
]
for template in TEMPLATES:
    notifications.register(template[0], template[1])

person = PersonFactory.build()
study_group = StudyGroupFactory.build(person=person)
p_event = PalvelutarjotinEventFactory.build()
occurrence = OccurrenceFactory.build(p_event=p_event)
enrolment = EnrolmentFactory.build()

DEFAULT_DUMMY_CONTEXT = {
    "preview_mode": False,
    "study_group": study_group,
    "occurrence": occurrence,
    "event": EVENT_DATA,
    "enrolment": enrolment,
    "custom_message": "custom_message",
}
dummy_context.update(
    {
        NotificationTemplate.OCCURRENCE_ENROLMENT: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.OCCURRENCE_ENROLMENT_SMS: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.OCCURRENCE_UNENROLMENT: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.OCCURRENCE_UNENROLMENT_SMS: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.ENROLMENT_APPROVED: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.ENROLMENT_APPROVED_SMS: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.ENROLMENT_DECLINED: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.ENROLMENT_DECLINED_SMS: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.OCCURRENCE_CANCELLED: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.OCCURRENCE_CANCELLED_SMS: DEFAULT_DUMMY_CONTEXT,
    }
)
