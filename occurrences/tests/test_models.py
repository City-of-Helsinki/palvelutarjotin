import pytest
from django.contrib.auth import get_user_model
from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from occurrences.models import Occurrence, PalvelutarjotinEvent, StudyGroup
from organisations.models import Organisation, Person

User = get_user_model()


@pytest.mark.django_db
def test_palvelutarjotin_event():
    PalvelutarjotinEventFactory()
    assert PalvelutarjotinEvent.objects.count() == 1
    assert Organisation.objects.count() == 1
    assert Person.objects.count() == 1


@pytest.mark.django_db
def test_study_group_creation():
    StudyGroupFactory()
    assert StudyGroup.objects.count() == 1
    assert Person.objects.count() == 1
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_occurrence_creation():
    OccurrenceFactory()
    assert Occurrence.objects.count() == 1
    assert Organisation.objects.count() == 1
    assert PalvelutarjotinEvent.objects.count() == 1
    assert Person.objects.count() == 1


@pytest.mark.django_db
def test_enrolment_creation(mock_get_event_data):
    EnrolmentFactory()
    assert Occurrence.objects.count() == 1
    assert StudyGroup.objects.count() == 1


@pytest.mark.django_db
def test_occurrence_seat_taken():
    EnrolmentFactory()
    occurrence = Occurrence.objects.all()[0]
    study_group = occurrence.study_groups.all()[0]
    assert (
        occurrence.seats_taken == study_group.group_size + study_group.amount_of_adult
    )
