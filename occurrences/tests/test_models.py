import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from occurrences.consts import StudyGroupStudyLevels
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
    Language,
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
    p_event = PalvelutarjotinEventFactory()
    assert p_event.enrolment_start is not None
    assert p_event.external_enrolment_url is None
    assert PalvelutarjotinEvent.objects.count() == 1
    assert Organisation.objects.count() == 1
    assert Person.objects.count() == 1


@pytest.mark.django_db
def test_palvelutarjotin_event_with_external_enrolment():
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=None, external_enrolment_url="http://test.org"
    )
    assert p_event.enrolment_start is None
    assert p_event.external_enrolment_url == "http://test.org"
    assert PalvelutarjotinEvent.objects.count() == 1
    assert Organisation.objects.count() == 1
    assert Person.objects.count() == 1


@pytest.mark.django_db
def test_palvelutarjotin_event_with_valid_external_enrolment_url():

    PalvelutarjotinEventFactory(external_enrolment_url="https://123.fi").full_clean()
    PalvelutarjotinEventFactory(
        external_enrolment_url="ftp://file-transfer-protocol.com/"
    ).full_clean()
    PalvelutarjotinEventFactory(
        external_enrolment_url="http://äåöxyz.org/"
    ).full_clean()

    # URLField validation is not triggered in DB level
    assert PalvelutarjotinEvent.objects.count() == 3


@pytest.mark.django_db
def test_palvelutarjotin_event_with_invalid_external_enrolment_url():

    p_events = [
        PalvelutarjotinEventFactory(external_enrolment_url="./asdfasdf"),
        PalvelutarjotinEventFactory(external_enrolment_url="//org/"),
        PalvelutarjotinEventFactory(external_enrolment_url="chrome://flags"),
        PalvelutarjotinEventFactory(external_enrolment_url="tättärää/"),
        PalvelutarjotinEventFactory(external_enrolment_url="http://%¶€#.org/"),
        PalvelutarjotinEventFactory(external_enrolment_url="http://asdfasdf"),
    ]

    for p_event in p_events:
        with pytest.raises(ValidationError):
            p_event.full_clean()

    # URLField validation is not triggered in DB level
    assert PalvelutarjotinEvent.objects.count() == 6


@pytest.mark.django_db
def test_palvelutarjotin_event_without_enrolments():
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=None, external_enrolment_url=None
    )
    assert p_event.enrolment_start is None
    assert p_event.external_enrolment_url is None
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
    assert StudyLevel.objects.count() == len(StudyGroupStudyLevels.STUDY_LEVELS)
    StudyLevelFactory()
    assert StudyLevel.objects.count() == len(StudyGroupStudyLevels.STUDY_LEVELS) + 1


@pytest.mark.django_db
def test_study_level_creation_via_study_group():
    assert StudyLevel.objects.count() == len(StudyGroupStudyLevels.STUDY_LEVELS)
    StudyGroupFactory(study_levels=(StudyLevelFactory(),))
    assert StudyGroup.objects.count() == 1
    assert StudyLevel.objects.count() == len(StudyGroupStudyLevels.STUDY_LEVELS) + 1


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
def test_enrolment_create_cancellation_token(mock_get_event_data):
    enrolment = EnrolmentFactory()
    person = enrolment.person
    token = enrolment.create_cancellation_token()
    assert token.person == person
    assert token.key is not None
    assert token.content_object.__class__ == Enrolment
    assert token.content_object.id is not None


@pytest.mark.django_db
def test_enrolment_create_cancellation_token_with_deactivation(mock_get_event_data,):
    enrolment = EnrolmentFactory()
    enrolment.create_cancellation_token()
    VerificationToken.objects.count() == 1
    token2 = enrolment.create_cancellation_token(deactivate_existing=True)
    VerificationToken.objects.count() == 1
    VerificationToken.objects.filter(pk=token2.pk).exists()


@pytest.mark.django_db
def test_enrolment_get_cancellation_url(mock_get_event_data):
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
def test_occurrence_seat_taken(mock_get_event_data):
    enrolment = EnrolmentFactory(status=Enrolment.STATUS_APPROVED)
    occurrence = enrolment.occurrence
    study_group = enrolment.study_group
    assert occurrence.seats_taken > 0
    assert (
        occurrence.seats_taken == study_group.group_size + study_group.amount_of_adult
    )


@pytest.mark.django_db
def test_occurrence_seat_approved(mock_get_event_data):
    enrolment = EnrolmentFactory(status=Enrolment.STATUS_APPROVED)
    occurrence = enrolment.occurrence
    study_group = enrolment.study_group
    assert occurrence.seats_approved > 0
    assert (
        occurrence.seats_approved
        == study_group.group_size + study_group.amount_of_adult
    )


@pytest.mark.django_db
def test_get_event_languages_from_occurrence(
    mock_update_event_data, mock_get_event_data
):
    lng1, lng2, lng3, lng4 = LanguageFactory.create_batch(4)
    p_event = PalvelutarjotinEventFactory()
    OccurrenceFactory(p_event=p_event, languages=[lng1, lng2])
    OccurrenceFactory(p_event=p_event, languages=[lng2, lng3])
    OccurrenceFactory(p_event=p_event, languages=[lng4])
    assert set(p_event.get_event_languages_from_occurrence()) - set(
        [lng1, lng2, lng3, lng4]
    ) == set([])


@pytest.mark.django_db
def test_languages_are_sorted_by_name_and_id(mock_get_event_data):
    languages = LanguageFactory.create_batch(size=10)
    Language.objects.count() == 10
    [l for l in Language.objects.all()] == sorted(
        languages, key=lambda x: (x.name, x.id)
    )
