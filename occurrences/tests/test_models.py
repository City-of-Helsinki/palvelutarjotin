import pytest
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from freezegun import freeze_time
from unittest.mock import patch

from graphene_linked_events.tests.mock_data import EVENT_DATA
from occurrences.consts import StudyGroupStudyLevels
from occurrences.factories import (
    EnrolmentFactory,
    EventQueueEnrolmentFactory,
    LanguageFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
    StudyLevelFactory,
)
from occurrences.models import (
    Enrolment,
    EventQueueEnrolment,
    Language,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    StudyLevel,
)
from organisations.factories import PersonFactory, UserFactory
from organisations.models import Organisation, Person
from palvelutarjotin.exceptions import EnrolmentNotEnoughCapacityError
from verification_token.models import VerificationToken

User = get_user_model()


@pytest.mark.django_db
def test_palvelutarjotin_event(mock_get_event_data):
    p_event = PalvelutarjotinEventFactory()
    assert p_event.enrolment_start is not None
    assert p_event.external_enrolment_url is None
    assert PalvelutarjotinEvent.objects.count() == 1
    assert Organisation.objects.count() == 1
    assert Person.objects.count() == 1


@pytest.mark.django_db
def test_palvelutarjotin_event_translations(mock_get_event_data):
    p_event = PalvelutarjotinEventFactory(auto_acceptance_message="automaattiviesti")
    assert PalvelutarjotinEvent.objects.count() == 1
    p_event.get_current_language() == "fi"
    assert p_event.auto_acceptance_message == "automaattiviesti"
    p_event.set_current_language("en")
    p_event.auto_acceptance_message = "auto acceptance message"
    p_event.save()
    PalvelutarjotinEvent.objects.active_translations(
        auto_acceptance_message="auto acceptance message"
    ).count() == 1
    PalvelutarjotinEvent.objects.active_translations(
        auto_acceptance_message="automaattiviesti"
    ).count() == 0
    PalvelutarjotinEvent.objects.translated(
        auto_acceptance_message="automaattiviesti"
    ).count() == 1


@pytest.mark.django_db
def test_palvelutarjotin_event_with_external_enrolment(mock_get_event_data):
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=None, external_enrolment_url="http://test.org"
    )
    assert p_event.enrolment_start is None
    assert p_event.external_enrolment_url == "http://test.org"
    assert PalvelutarjotinEvent.objects.count() == 1
    assert Organisation.objects.count() == 1
    assert Person.objects.count() == 1


@pytest.mark.django_db
def test_palvelutarjotin_event_with_valid_external_enrolment_url(mock_get_event_data):
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
def test_study_group_save_resolves_unit_name_from_unit_id(mock_get_place_data):
    study_group = StudyGroupFactory(unit_id=EVENT_DATA["id"], unit_name=None)
    study_group.unit_name is not None


@pytest.mark.django_db
@pytest.mark.parametrize("use_name_only", [False, True])
def test_study_group_with_enrolment_count(
    use_name_only, mock_get_place_data, mock_get_event_data
):
    study_group_1 = StudyGroupFactory(group_name="group1")
    study_group_2 = StudyGroupFactory(group_name="group2")
    EnrolmentFactory.create_batch(2, study_group=study_group_1)
    EnrolmentFactory.create_batch(5, study_group=study_group_2)
    groups_with_two_enrolments = StudyGroup.objects.with_enrolments_count(
        use_name_only=use_name_only
    ).filter(enrolments_count=2)
    groups_with_five_enrolments = StudyGroup.objects.with_enrolments_count(
        use_name_only=use_name_only
    ).filter(enrolments_count=5)
    assert groups_with_two_enrolments.count() == 1
    assert groups_with_five_enrolments.count() == 1
    assert groups_with_two_enrolments[0] == study_group_1
    assert groups_with_five_enrolments[0] == study_group_2


@pytest.mark.django_db
def test_study_group_with_enrolment_count_by_name(
    mock_get_place_data, mock_get_event_data
):
    school = "the school"
    the_school_1st_instance = StudyGroupFactory(group_name=school)
    the_school_2nd_instance = StudyGroupFactory(group_name=school)
    EnrolmentFactory.create_batch(2, study_group=the_school_1st_instance)
    EnrolmentFactory.create_batch(5, study_group=the_school_2nd_instance)
    groups_with_seven_enrolments = StudyGroup.objects.with_enrolments_count(
        use_name_only=True
    ).filter(enrolments_count=7)
    assert groups_with_seven_enrolments.count() == 2
    assert the_school_1st_instance in groups_with_seven_enrolments
    assert the_school_2nd_instance in groups_with_seven_enrolments


@pytest.mark.django_db
def test_study_group_with_organisation_ids(mock_get_place_data, mock_get_event_data):
    EnrolmentFactory.create_batch(10)
    groups = StudyGroup.objects.all()

    # Without annotation
    for group in groups:
        assert hasattr(group, "organisation_ids") is False

    groups = StudyGroup.objects.with_organisation_ids().all()

    # With annotation
    for group in groups:
        assert hasattr(group, "organisation_ids") is True
        assert group.organisation_ids is not None

    group_without_enrolment = StudyGroupFactory()

    # Without enrolment, so without organisation
    StudyGroup.objects.with_organisation_ids().get(
        id=group_without_enrolment.id
    ).organisation_ids is None

    # With multiple enrolments to multiple organisations
    group_with_multiple_organisations = StudyGroupFactory()
    enrolments = EnrolmentFactory.create_batch(
        2, study_group=group_with_multiple_organisations
    )
    enrolments_organisation_ids = [
        enrolment.occurrence.p_event.organisation.id for enrolment in enrolments
    ]
    group_organisation_ids = (
        StudyGroup.objects.with_organisation_ids()
        .get(id=group_with_multiple_organisations.id)
        .organisation_ids
    )
    assert len(group_organisation_ids) == 2
    assert all(
        (org_id in enrolments_organisation_ids) for org_id in group_organisation_ids
    )


@pytest.mark.django_db
def test_study_group_user_can_view(
    mock_get_place_data, mock_get_event_data, organisation
):
    person = PersonFactory(user=UserFactory())
    person.organisations.add(organisation)
    organisation_enrolments = EnrolmentFactory.create_batch(
        5, occurrence__p_event__organisation=organisation
    )
    organisation_groups = [
        enrolment.study_group for enrolment in organisation_enrolments
    ]
    StudyGroupFactory.create_batch(5)
    assert StudyGroup.objects.all().count() == 10
    assert StudyGroup.objects.user_can_view(person.user).count() == len(
        organisation_groups
    )


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
def test_occurrence_creation(mock_get_event_data):
    OccurrenceFactory()
    assert Occurrence.objects.count() == 1
    assert Organisation.objects.count() == 1
    assert PalvelutarjotinEvent.objects.count() == 1
    assert Person.objects.count() == 1


@pytest.mark.django_db
def test_event_queue_enrolment_creation(mock_get_event_data):
    EventQueueEnrolmentFactory()
    assert EventQueueEnrolment.objects.count() == 1
    assert PalvelutarjotinEvent.objects.count() == 1
    assert StudyGroup.objects.count() == 1


@pytest.mark.django_db
def test_event_queue_enrolment_enrolled_in_last_days(mock_get_event_data):
    EventQueueEnrolmentFactory()
    with freeze_time(timezone.now() - timedelta(days=1)):
        EventQueueEnrolmentFactory()
    with freeze_time(timezone.now() - timedelta(days=2)):
        EventQueueEnrolmentFactory()
    with freeze_time(timezone.now() - timedelta(days=3)):
        EventQueueEnrolmentFactory()
    assert EventQueueEnrolment.objects.enrolled_in_last_days(days=1).count() == 2
    assert EventQueueEnrolment.objects.enrolled_in_last_days(days=2).count() == 3
    assert EventQueueEnrolment.objects.enrolled_in_last_days(days=3).count() == 4


@pytest.mark.django_db
def test_creating_enrolment_from_event_queue_enrolment(mock_get_event_data):
    """
    The event queue enrolment can be easily used as a base
    for an enrolment to an occurrence.
    """
    occurrence = OccurrenceFactory()
    queue = EventQueueEnrolmentFactory()
    enrolment = queue.create_enrolment(occurrence)
    assert Enrolment.objects.count() == 1
    assert enrolment.occurrence == occurrence
    assert enrolment.study_group == queue.study_group
    assert enrolment.person == queue.person
    assert enrolment.notification_type == queue.notification_type


@pytest.mark.django_db
def test_event_queue_enrolment_with_group_occurrence_enrolment_count(
    mock_get_event_data,
):
    """
    The EventQueueEnrolment manager can use with_group_occurrence_enrolment_count
    to annotate the count of the done occurrence enrolments to the returned instance.
    """
    p_event = PalvelutarjotinEventFactory()
    [occ1, occ2, occ3] = OccurrenceFactory.create_batch(3, p_event=p_event)
    person = PersonFactory()
    # Person has 2 groups
    group1 = StudyGroupFactory(person=person)
    group2 = StudyGroupFactory(person=person)
    # Person has 2 enrolments which occurrences are related to the event for group 1
    EnrolmentFactory(person=person, study_group=group1, occurrence=occ1)
    EnrolmentFactory(person=person, study_group=group1, occurrence=occ2)
    # Person has 1 enrolment which occurrence is related to the event for group 2
    EnrolmentFactory(person=person, study_group=group2, occurrence=occ3)
    # Person has 1 enrolment in another event
    EnrolmentFactory(person=person)
    # There are some other enrolments also made by unknown persons
    EnrolmentFactory.create_batch(5, occurrence=occ1)
    EnrolmentFactory.create_batch(5, occurrence=occ2)
    assert Enrolment.objects.filter(person=person).count() == 4
    assert Enrolment.objects.filter(study_group=group1).count() == 2
    assert Enrolment.objects.filter(study_group=group2).count() == 1
    assert PalvelutarjotinEvent.objects.count() == 2
    assert Occurrence.objects.count() == 4
    # Person is also in queue to the p_event where there are some enrolments already
    EventQueueEnrolmentFactory(p_event=p_event, study_group=group1)
    # Person is also in another queue where he does not have any enrolments yet
    EventQueueEnrolmentFactory(study_group=group1)
    event_queue_enrolments = (
        EventQueueEnrolment.objects.with_group_occurrence_enrolment_count().filter(
            occurrence_enrolments_count__gt=0
        )
    )
    assert EventQueueEnrolment.objects.count() == 2
    assert EventQueueEnrolment.objects.filter(p_event=p_event).count() == 1
    assert event_queue_enrolments.count() == 1
    assert event_queue_enrolments[0].study_group == group1
    # When the group2 is added to the event queue, the count is increased
    EventQueueEnrolmentFactory(p_event=p_event, study_group=group2)
    assert event_queue_enrolments.count() == 2


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
def test_enrolment_create_cancellation_token_with_deactivation(
    mock_get_event_data,
):
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
    assert cancellation_url.startswith(
        (
            "http://",
            "https://",
        )
    )
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
def test_enrolment_approve(
    api_client, mock_update_event_data, mock_get_event_data, occurrence
):
    study_group_15 = StudyGroupFactory(group_size=15)
    study_group_20 = StudyGroupFactory(group_size=20)
    # Current date froze on 2020-01-04:
    p_event_1 = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        enrolment_end_days=2,
        auto_acceptance=True,
    )
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        p_event=p_event_1,
        min_group_size=10,
        max_group_size=20,
        amount_of_seats=34,
    )

    # After 20 people there are 14 seats left
    enrolment1 = EnrolmentFactory(occurrence=occurrence, study_group=study_group_20)
    enrolment1.approve()
    assert occurrence.amount_of_seats - occurrence.seats_taken == 14

    # pending occurrence can "overbook", but it cannot be approved
    # study group of 15 overbooks the occurrence by 1 after group of 20
    enrolment2 = EnrolmentFactory(occurrence=occurrence, study_group=study_group_15)
    with pytest.raises(EnrolmentNotEnoughCapacityError):
        enrolment2.approve()


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
    [lang for lang in Language.objects.all()] == sorted(
        languages, key=lambda x: (x.name, x.id)
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "occurrence_start_time,occurrence_end_time",
    [
        # new starting occurrence
        (
            datetime(2020, 1, 10, 0, 0, 0, tzinfo=timezone.now().tzinfo),
            datetime(2020, 1, 11, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        ),
        # new ending occurrence
        (
            datetime(2020, 1, 25, 0, 0, 0, tzinfo=timezone.now().tzinfo),
            datetime(2020, 1, 26, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        ),
    ],
)
@patch("occurrences.models.send_event_republish")
def test_republish_event_to_sync_times_on_save_calls_republish_when_published(
    mock_send_event_republish,
    occurrence_start_time,
    occurrence_end_time,
    mock_get_event_data,
):
    enrolment_start = datetime(2020, 1, 10, 0, 0, 0, tzinfo=timezone.now().tzinfo)
    enrolment_end_days = 1
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=enrolment_start,
        enrolment_end_days=enrolment_end_days,
    )

    # First occurrence, starts earliest possible, is a 1 day event
    OccurrenceFactory(
        p_event=p_event,
        start_time=datetime(2020, 1, 11, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        end_time=datetime(2020, 1, 12, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )

    # Last occurrence, starts 10 days after first one, is a 1 day event
    OccurrenceFactory(
        p_event=p_event,
        start_time=datetime(2020, 1, 21, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        end_time=datetime(2020, 1, 22, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )

    # new parametrized occurrence
    OccurrenceFactory(
        p_event=p_event,
        start_time=occurrence_start_time,
        end_time=occurrence_end_time,
    )
    assert Occurrence.objects.count() == 3
    assert mock_send_event_republish.call_count == 3


@pytest.mark.django_db
@patch("occurrences.models.send_event_republish")
def test_republish_event_to_sync_times_on_update_calls_republish_when_published(
    mock_send_event_republish,
    mock_get_event_data,
):
    enrolment_start = datetime(2020, 1, 10, 0, 0, 0, tzinfo=timezone.now().tzinfo)
    enrolment_end_days = 1
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=enrolment_start,
        enrolment_end_days=enrolment_end_days,
    )

    # First occurrence, starts earliest possible, is a 1 day event
    occurrence1 = OccurrenceFactory(
        p_event=p_event,
        start_time=datetime(2020, 1, 11, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        end_time=datetime(2020, 1, 12, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )

    # Last occurrence, starts 10 days after first one, is a 1 day event
    occurrence2 = OccurrenceFactory(
        p_event=p_event,
        start_time=datetime(2020, 1, 21, 0, 0, 0, tzinfo=timezone.now().tzinfo),
        end_time=datetime(2020, 1, 22, 0, 0, 0, tzinfo=timezone.now().tzinfo),
    )

    assert Occurrence.objects.count() == 2
    assert mock_send_event_republish.call_count == 2

    assert (
        occurrence1 == sorted([occurrence1, occurrence2], key=lambda o: o.start_time)[0]
    )

    # Moving the occurrence to be the first affects on event time range
    occurrence2.start_time = occurrence1.start_time - timedelta(days=1)
    occurrence2.end_time = occurrence1.end_time - timedelta(days=1)
    occurrence2.save()
    assert mock_send_event_republish.call_count == 3

    assert (
        occurrence2 == sorted([occurrence1, occurrence2], key=lambda o: o.start_time)[0]
    )
    assert (
        occurrence2 == sorted([occurrence1, occurrence2], key=lambda o: o.end_time)[0]
    )

    # changing the first occurrence start time affects on event time range
    occurrence2.start_time = occurrence2.start_time - timedelta(days=1)
    occurrence2.save()
    assert mock_send_event_republish.call_count == 4

    # changing the last occurrence end time affects on event time range
    occurrence1.end_time = occurrence1.end_time + timedelta(days=1)
    occurrence1.save()
    assert mock_send_event_republish.call_count == 5

    # changing the last occurrence start time does not affect on event time range
    occurrence1.start_time = occurrence1.start_time - timedelta(days=1)
    occurrence1.save()
    assert mock_send_event_republish.call_count == 5

    assert (
        occurrence2 == sorted([occurrence1, occurrence2], key=lambda o: o.start_time)[0]
    )
    assert (
        occurrence2 == sorted([occurrence1, occurrence2], key=lambda o: o.end_time)[0]
    )

    # old occurrence to become the last one
    occurrence2.end_time = occurrence1.end_time + timedelta(days=1)
    occurrence2.start_time = occurrence1.start_time + timedelta(days=1)
    occurrence2.save()
    assert mock_send_event_republish.call_count == 6


@pytest.mark.django_db
@patch("occurrences.models.send_event_unpublish")
def test_unpublish_event_to_sync_times_on_delete_does_nothing_when_many_occurrences(
    mock_send_event_unpublish,
    mock_get_event_data,
    p_event,
):
    OccurrenceFactory(p_event=p_event)
    occurrence = OccurrenceFactory(p_event=p_event)
    assert Occurrence.objects.count() == 2
    occurrence.delete()
    assert Occurrence.objects.count() == 1
    assert not mock_send_event_unpublish.called


@pytest.mark.django_db
@patch("occurrences.models.send_event_unpublish")
def test_unpublish_event_to_sync_times_on_delete_does_nothing_when_draft(
    mock_send_event_unpublish,
    mock_get_draft_event_data,
    mock_update_event_data,
    p_event,
):
    occurrence = OccurrenceFactory(p_event=p_event)
    assert Occurrence.objects.count() == 1
    occurrence.delete()
    assert Occurrence.objects.count() == 0
    assert not mock_send_event_unpublish.called


@pytest.mark.django_db
@patch("occurrences.models.send_event_unpublish")
def test_unpublish_event_to_sync_times_on_delete_when_last_occurrence_is_cancelled(
    mock_send_event_unpublish,
    mock_get_event_data,
    p_event,
):
    OccurrenceFactory(p_event=p_event, cancelled=True)
    occurrence = OccurrenceFactory(p_event=p_event)
    assert Occurrence.objects.count() == 2
    occurrence.delete()
    assert Occurrence.objects.count() == 1
    assert Occurrence.objects.filter(cancelled=False).count() == 0
    assert mock_send_event_unpublish.called


@pytest.mark.django_db
@patch("occurrences.models.send_event_unpublish")
def test_unpublish_event_to_sync_times_on_delete_when_last_occurrence(
    mock_send_event_unpublish,
    mock_get_event_data,
    p_event,
):
    occurrence = OccurrenceFactory(p_event=p_event)
    assert Occurrence.objects.count() == 1
    occurrence.delete()
    assert Occurrence.objects.count() == 0
    assert mock_send_event_unpublish.called


@pytest.mark.django_db
@patch("occurrences.models.send_event_unpublish")
def test_delete_queryset(mock_send_event_unpublish, mock_get_event_data):
    OccurrenceFactory.create_batch(10)
    Occurrence.objects.all().delete()
    assert mock_send_event_unpublish.call_count == 10


@pytest.mark.django_db
def test_enrolment_pending_enrolments_by_email(mock_get_event_data):
    email = "test@test-example.com"
    enrolment = EnrolmentFactory(
        occurrence=OccurrenceFactory(
            p_event=PalvelutarjotinEventFactory(contact_email=email)
        ),
        status=Enrolment.STATUS_PENDING,
    )
    # approved - should be excluded
    EnrolmentFactory(
        occurrence=OccurrenceFactory(
            p_event=PalvelutarjotinEventFactory(contact_email=email)
        ),
        status=Enrolment.STATUS_APPROVED,
    )
    # email does not match - should be excluded
    EnrolmentFactory(status=Enrolment.STATUS_PENDING)
    assert list(Enrolment.objects.all().pending_enrolments_by_email(email=email)) == [
        enrolment
    ]


@pytest.mark.django_db
def test_enrolment_approved_enrolments_by_email(mock_get_event_data):
    email = "test@test-example.com"
    enrolment = EnrolmentFactory(
        occurrence=OccurrenceFactory(
            p_event=PalvelutarjotinEventFactory(contact_email=email)
        ),
        status=Enrolment.STATUS_APPROVED,
    )
    # pending - should be excluded
    EnrolmentFactory(
        occurrence=OccurrenceFactory(
            p_event=PalvelutarjotinEventFactory(contact_email=email)
        ),
        status=Enrolment.STATUS_PENDING,
    )
    # email does not match - should be excluded
    EnrolmentFactory(status=Enrolment.STATUS_APPROVED)
    assert list(Enrolment.objects.all().approved_enrolments_by_email(email=email)) == [
        enrolment
    ]


@pytest.mark.django_db
@pytest.mark.parametrize("delete_via_queryset", (False, True))
@pytest.mark.parametrize(
    "enrolment_base_child_object_factory, expected_factory_object_type",
    [
        (EnrolmentFactory, Enrolment),
        (EventQueueEnrolmentFactory, EventQueueEnrolment),
    ],
)
def test_enrolment_base_child_object_and_study_group_person_deletion(
    delete_via_queryset,
    enrolment_base_child_object_factory,
    expected_factory_object_type,
    mock_get_event_data,
):
    person = PersonFactory()
    study_group = StudyGroupFactory(person=person)
    enrolment_base_child_object = enrolment_base_child_object_factory(
        study_group=study_group, person=person
    )
    assert isinstance(enrolment_base_child_object, expected_factory_object_type)

    if delete_via_queryset:
        Person.objects.filter(pk=person.pk).delete()
    else:
        person.delete()

    enrolment_base_child_object.refresh_from_db()
    study_group.refresh_from_db()

    assert not Person.objects.filter(pk=person.pk).exists()
    assert enrolment_base_child_object.person is None
    assert enrolment_base_child_object.person_deleted_at is not None
    assert study_group.person is None
    assert study_group.person_deleted_at is not None


@pytest.mark.django_db
def test_palvelutarjotin_event_contact_info_deletion(mock_update_event_data):
    event_1 = PalvelutarjotinEventFactory(contact_person=PersonFactory())
    event_2 = PalvelutarjotinEventFactory(
        contact_email="shouldbedeleted@example.com", contact_phone_number="12345"
    )
    event_3 = PalvelutarjotinEventFactory(
        contact_email="contact@example.com", contact_phone_number="54321"
    )

    PalvelutarjotinEvent.objects.filter(
        id__in=[event_1.pk, event_2.pk]
    ).delete_contact_info()

    event_1.refresh_from_db()
    event_2.refresh_from_db()
    event_3.refresh_from_db()

    assert event_1.contact_person is None
    assert event_1.contact_email == event_1.contact_phone_number == ""
    assert event_1.contact_info_deleted_at
    assert event_2.contact_person is None
    assert event_2.contact_email == event_2.contact_phone_number == ""
    assert event_2.contact_info_deleted_at

    assert event_3.contact_person is not None
    assert event_3.contact_email == "contact@example.com"
    assert event_3.contact_phone_number == "54321"
    assert not event_3.contact_info_deleted_at


@pytest.mark.django_db
def test_palvelutarjotin_event_filter_with_contact_info(mock_get_event_data):
    def _sort(queryset):
        return sorted(list(queryset), key=lambda e: e.id)

    # Some random events to database
    random_events = PalvelutarjotinEventFactory.create_batch(10)

    # Own events
    person = PersonFactory()
    events_matches_contact_person = PalvelutarjotinEventFactory.create_batch(
        5, contact_person=person
    )
    events_matches_contact_email = PalvelutarjotinEventFactory.create_batch(
        5, contact_email=person.email_address
    )
    events_matches_contact_phone_number = PalvelutarjotinEventFactory.create_batch(
        5, contact_phone_number=person.phone_number
    )

    # Test database's initial data state
    assert (
        PalvelutarjotinEvent.objects.all().count()
        == (
            len(random_events)
            + len(events_matches_contact_person)
            + len(events_matches_contact_email)
            + len(events_matches_contact_phone_number)
        )
        == 10 + 5 + 5 + 5
    )

    # Filter with the related person
    assert _sort(
        PalvelutarjotinEvent.objects.filter_with_contact_info(person)
    ) == _sort(
        events_matches_contact_person
        + events_matches_contact_email
        + events_matches_contact_phone_number
    )

    # Filter with the person's email
    person_with_email = Person(email_address=person.email_address)
    assert _sort(
        PalvelutarjotinEvent.objects.filter_with_contact_info(person_with_email)
    ) == _sort(events_matches_contact_person + events_matches_contact_email)

    # Filter with the person's phone
    person_with_phone_number = Person(phone_number=person.phone_number)
    assert _sort(
        PalvelutarjotinEvent.objects.filter_with_contact_info(person_with_phone_number)
    ) == _sort((events_matches_contact_person + events_matches_contact_phone_number))


@pytest.mark.django_db
def test_palvelutarjotin_event_filter_with_contact_info_value_error():
    person_without_contact_info = Person(
        name="Test Guy", email_address=None, phone_number=None
    )
    with pytest.raises(ValueError) as exc_info:
        PalvelutarjotinEvent.objects.filter_with_contact_info(
            person_without_contact_info
        )
    assert (
        exc_info.value.args[0]
        == "The person must have at least an email address or a phone number."
    )
