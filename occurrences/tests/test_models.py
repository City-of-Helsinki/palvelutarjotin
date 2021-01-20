import pytest
from django.contrib.auth import get_user_model
from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from occurrences.models import Enrolment, Occurrence, PalvelutarjotinEvent, StudyGroup
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
def test_enrolment_create_cancellation_token():
    enrolment = EnrolmentFactory()
    user = enrolment.person.user
    token = enrolment.create_cancellation_token()
    assert token.user == user
    assert token.key is not None
    assert token.content_object.__class__ == Enrolment
    assert token.content_object.id is not None


@pytest.mark.django_db
def test_enrolment_create_cancellation_url():
    enrolment = EnrolmentFactory()
    cancellation_url = enrolment.create_cancellation_url()
    token = enrolment.verification_tokens.all()[0]
    assert token.key is not None and token.key != ""
    assert token.key in cancellation_url
    assert cancellation_url.startswith(("http://", "https://",))


@pytest.mark.django_db
def test_study_group_size_with_adults():
    study_group1 = StudyGroupFactory(group_size=10, amount_of_adult=2)
    study_group2 = StudyGroupFactory(group_size=10, amount_of_adult=0)
    assert study_group1.group_size_with_adults() == 12
    assert study_group2.group_size_with_adults() == 10


@pytest.mark.django_db
def test_occurrence_seat_taken():
    enrolment = EnrolmentFactory()
    occurrence = enrolment.occurrence
    study_group = enrolment.study_group
    assert occurrence.seats_taken > 0
    assert (
        occurrence.seats_taken == study_group.group_size + study_group.amount_of_adult
    )


@pytest.mark.django_db
def test_occurrence_seat_approved():
    enrolment = EnrolmentFactory(status=Enrolment.STATUS_APPROVED)
    occurrence = enrolment.occurrence
    study_group = enrolment.study_group
    assert occurrence.seats_approved > 0
    assert (
        occurrence.seats_approved
        == study_group.group_size + study_group.amount_of_adult
    )
