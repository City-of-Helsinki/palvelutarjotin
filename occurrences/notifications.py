from django.utils.translation import gettext_lazy as _
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.registry import notifications

from graphene_linked_events.tests.mock_data import EVENT_DATA
from occurrences.consts import NotificationTemplate
from occurrences.factories import (
    EnrolmentFactory,
    EventQueueEnrolmentFactory,
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
    (NotificationTemplate.ENROLMENT_CANCELLATION, _("enrolment cancellation")),
    (NotificationTemplate.ENROLMENT_CANCELLED, _("enrolment cancelled")),
    (NotificationTemplate.OCCURRENCE_ENROLMENT_SMS, _("occurrence enrolment sms")),
    (NotificationTemplate.OCCURRENCE_UNENROLMENT_SMS, _("occurrence unenrolment sms")),
    (NotificationTemplate.ENROLMENT_APPROVED_SMS, _("enrolment approved sms")),
    (NotificationTemplate.ENROLMENT_DECLINED_SMS, _("enrolment declined sms")),
    (NotificationTemplate.ENROLMENT_CANCELLATION_SMS, _("enrolment cancellation sms")),
    (NotificationTemplate.ENROLMENT_CANCELLED_SMS, _("enrolment cancelled sms")),
    (NotificationTemplate.OCCURRENCE_CANCELLED, _("occurrence cancelled")),
    (NotificationTemplate.OCCURRENCE_CANCELLED_SMS, _("occurrence cancelled sms")),
    (NotificationTemplate.OCCURRENCE_UPCOMING_SMS, _("occurrence upcoming sms")),
    (NotificationTemplate.ENROLMENT_SUMMARY_REPORT, _("Enrolments summary report")),
]
for template in TEMPLATES:
    notifications.register(template[0], template[1])

person = PersonFactory.build()
study_group = StudyGroupFactory.build(person=person)
p_event = PalvelutarjotinEventFactory.build()
occurrence = OccurrenceFactory.build(id=1, p_event=p_event)
enrolment = EnrolmentFactory.build(occurrence=occurrence)
queued_enrolment = EventQueueEnrolmentFactory.build(p_event=p_event)

DEFAULT_DUMMY_CONTEXT = {
    "preview_mode": False,
    "person": person,
    "study_group": study_group,
    "occurrence": occurrence,
    "event": EVENT_DATA,
    "enrolment": enrolment,
    "queued_enrolment": queued_enrolment,
    "custom_message": "custom_message",
    "trans": lambda field_translation_map: field_translation_map["fi"],
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
        NotificationTemplate.ENROLMENT_CANCELLATION: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.ENROLMENT_CANCELLATION_SMS: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.ENROLMENT_CANCELLED: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.ENROLMENT_CANCELLED_SMS: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.OCCURRENCE_CANCELLED: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.OCCURRENCE_CANCELLED_SMS: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.OCCURRENCE_UPCOMING_SMS: DEFAULT_DUMMY_CONTEXT,
        NotificationTemplate.ENROLMENT_SUMMARY_REPORT: {
            "report": [
                {
                    "event": EVENT_DATA,
                    "p_event": p_event,
                    "occurrences": [occurrence],
                    "queued_enrolments": [queued_enrolment],
                }
            ],
            "total_pending_enrolments": 1,
            "total_new_enrolments": 2,
            "total_new_queued_enrolments": 1,
        },
    }
)
