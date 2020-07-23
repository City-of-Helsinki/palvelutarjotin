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

notifications.register(
    NotificationTemplate.OCCURRENCE_ENROLMENT, _("occurrence enrolment")
)
notifications.register(
    NotificationTemplate.OCCURRENCE_UNENROLMENT, _("occurrence unenrolment")
)
notifications.register(
    NotificationTemplate.OCCURRENCE_ENROLMENT_SMS, _("occurrence enrolment sms")
)
notifications.register(
    NotificationTemplate.OCCURRENCE_UNENROLMENT_SMS, _("occurrence unenrolment sms")
)

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
    }
)
