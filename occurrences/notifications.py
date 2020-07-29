from django.utils.translation import ugettext_lazy as _
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.registry import notifications
from graphene_linked_events.tests.mock_data import EVENT_DATA
from occurrences.consts import NotificationTemplate
from occurrences.factories import (
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
]
for template in TEMPLATES:
    notifications.register(template[0], template[1])

person = PersonFactory.build()
study_group = StudyGroupFactory.build(person=person)
p_event = PalvelutarjotinEventFactory.build()
occurrence = OccurrenceFactory.build(p_event=p_event)

dummy_context.update(
    {
        NotificationTemplate.OCCURRENCE_ENROLMENT: {
            "study_group": study_group,
            "occurrence": occurrence,
            "event": EVENT_DATA,
        },
        NotificationTemplate.OCCURRENCE_ENROLMENT_SMS: {
            "study_group": study_group,
            "occurrence": occurrence,
            "event": EVENT_DATA,
        },
        NotificationTemplate.OCCURRENCE_UNENROLMENT: {
            "study_group": study_group,
            "occurrence": occurrence,
            "event": EVENT_DATA,
        },
        NotificationTemplate.OCCURRENCE_UNENROLMENT_SMS: {
            "study_group": study_group,
            "occurrence": occurrence,
            "event": EVENT_DATA,
        },
        NotificationTemplate.ENROLMENT_APPROVED: {
            "study_group": study_group,
            "occurrence": occurrence,
            "event": EVENT_DATA,
        },
        NotificationTemplate.ENROLMENT_APPROVED_SMS: {
            "study_group": study_group,
            "occurrence": occurrence,
            "event": EVENT_DATA,
        },
        NotificationTemplate.ENROLMENT_DECLINED: {
            "study_group": study_group,
            "occurrence": occurrence,
            "event": EVENT_DATA,
        },
        NotificationTemplate.ENROLMENT_DECLINED_SMS: {
            "study_group": study_group,
            "occurrence": occurrence,
            "event": EVENT_DATA,
        },
    }
)
