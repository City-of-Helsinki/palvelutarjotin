import pytest
from django.contrib.auth import get_user_model
from occurrences.factories import EnrolmentFactory, OccurrenceFactory, StudyGroupFactory
from occurrences.models import Occurrence, StudyGroup
from organisations.factories import PersonFactory
from organisations.models import Organisation, Person

User = get_user_model()


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
    OccurrenceFactory(contact_persons=PersonFactory.create_batch(3))
    assert Occurrence.objects.count() == 2
    assert Organisation.objects.count() == 2
    assert Person.objects.count() == 3


@pytest.mark.django_db
def test_enrolment_creation():
    EnrolmentFactory()
    assert Occurrence.objects.count() == 1
    assert StudyGroup.objects.count() == 1
