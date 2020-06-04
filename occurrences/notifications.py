from django.utils.translation import ugettext_lazy as _
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.registry import notifications
from graphene_linked_events.tests.mock_data import EVENT_DATA
from occurrences.consts import NotificationType
from occurrences.factories import (
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from organisations.factories import PersonFactory

notifications.register(NotificationType.OCCURRENCE_ENROLMENT, _("occurrence enrolment"))
notifications.register(
    NotificationType.OCCURRENCE_UNENROLMENT, _("occurrence unenrolment")
)

person = PersonFactory.build()
study_group = StudyGroupFactory.build(person=person)
p_event = PalvelutarjotinEventFactory.build()
occurrence = OccurrenceFactory.build(p_event=p_event)


dummy_context.update(
    {
        NotificationType.OCCURRENCE_ENROLMENT: {
            "study_group": study_group,
            "occurrence": occurrence,
            "event": EVENT_DATA,
        },
        NotificationType.OCCURRENCE_UNENROLMENT: {
            "study_group": study_group,
            "occurrence": occurrence,
            "event": EVENT_DATA,
        },
    }
)
