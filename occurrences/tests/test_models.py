import pytest
from django.contrib.auth import get_user_model
from occurrences.factories import (
    EnrolmentFactory,
    LanguageFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
    StudyLevelFactory,
)
from occurrences.models import (
    Enrolment,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    StudyLevel,
)
from organisations.models import Organisation, Person
from verification_token.models import VerificationToken

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
def test_study_level_creation():
    assert StudyLevel.objects.count() == 12
    StudyLevelFactory()
    assert StudyLevel.objects.count() == 13


@pytest.mark.django_db
def test_study_level_creation_via_study_group():
    assert StudyLevel.objects.count() == 12
    StudyGroupFactory(study_levels=(StudyLevelFactory(),))
    assert StudyGroup.objects.count() == 1
    assert StudyLevel.objects.count() == 13


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
    person = enrolment.person
    token = enrolment.create_cancellation_token()
    assert token.person == person
    assert token.key is not None
    assert token.content_object.__class__ == Enrolment
    assert token.content_object.id is not None


@pytest.mark.django_db
def test_enrolment_create_cancellation_token_with_deactivation():
    enrolment = EnrolmentFactory()
    enrolment.create_cancellation_token()
    VerificationToken.objects.count() == 1
    token2 = enrolment.create_cancellation_token(deactivate_existing=True)
    VerificationToken.objects.count() == 1
    VerificationToken.objects.filter(pk=token2.pk).exists()


@pytest.mark.django_db
def test_enrolment_get_cancellation_url():
    enrolment = EnrolmentFactory()
    token = enrolment.create_cancellation_token()
    cancellation_url = enrolment.get_cancellation_url()
    assert token.key is not None and token.key != ""
    assert token.key in cancellation_url
    assert cancellation_url.startswith(("http://", "https://",))
    # test with a given token
    cancellation_url = enrolment.get_cancellation_url(cancellation_token=token)
    assert token.key in cancellation_url


@pytest.mark.django_db
def test_enrolment_cancel_deactivates_tokens(mock_get_event_data):
    enrolment = EnrolmentFactory()
    enrolment.create_cancellation_token()
    assert VerificationToken.objects.filter(is_active=True).count() == 1
    enrolment.cancel()
    assert VerificationToken.objects.filter(is_active=True).count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "group_size,amount_of_adult,result",
    [(10, 2, 12), (10, 0, 10), (0, 10, 10), (0, 0, 0)],
)
def test_study_group_size_with_adults(group_size, amount_of_adult, result):
    assert (
        StudyGroupFactory(
            group_size=group_size, amount_of_adult=amount_of_adult
        ).group_size_with_adults()
        == result
    )


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


@pytest.mark.django_db
def test_get_event_languages_from_occurrence(mock_update_event_data):
    lng1 = LanguageFactory()
    lng2 = LanguageFactory()
    lng3 = LanguageFactory()
    lng4 = LanguageFactory()
    p_event = PalvelutarjotinEventFactory()
    OccurrenceFactory(p_event=p_event, languages=[lng1, lng2])
    OccurrenceFactory(p_event=p_event, languages=[lng2, lng3])
    OccurrenceFactory(p_event=p_event, languages=[lng4])
    assert set(p_event.get_event_languages_from_occurrence()) - set(
        [lng1, lng2, lng3, lng4]
    ) == set([])
