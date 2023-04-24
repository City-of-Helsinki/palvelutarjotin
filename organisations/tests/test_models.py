import pytest
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.utils import timezone

from occurrences.factories import EnrolmentFactory, PalvelutarjotinEventFactory
from organisations.factories import (
    OrganisationFactory,
    OrganisationProposalFactory,
    PersonFactory,
    UserFactory,
)
from organisations.models import Organisation, OrganisationProposal, Person

User = get_user_model()


@pytest.mark.django_db
def test_person_creation():
    person = PersonFactory()
    assert User.objects.count() == 1
    assert Person.objects.count() == 1
    assert person.__str__() == f"{person.name} ({person.user.username})"


@pytest.mark.django_db
def test_organisation_creation():
    OrganisationFactory()
    assert Organisation.objects.count() == 1


@pytest.mark.django_db
def test_organisation_proposal_creation():
    person = PersonFactory()
    organisation_proposal = OrganisationProposalFactory(applicant=person)
    assert OrganisationProposal.objects.count() == 1
    assert person.organisationproposal_set.count() == 1
    assert OrganisationProposal.objects.filter(applicant=person).count() == 1
    assert (
        organisation_proposal.__str__()
        == f"{organisation_proposal.id} {organisation_proposal.name}"
    )


@pytest.mark.django_db
def test_membership_creation():
    organisations = OrganisationFactory.create_batch(3)
    person = PersonFactory(organisations=organisations)
    assert person.organisations.count() == 3
    assert Organisation.objects.count() == 3
    assert Person.objects.count() == 1


@pytest.mark.django_db
def test_own_places():
    place1 = "abc:123"
    place2 = "xyz:321"
    place3 = "jkl:999"
    person_without_places = PersonFactory(name="person without places", place_ids=[])
    assert len(person_without_places.place_ids) == 0
    person1 = PersonFactory(name="person1", place_ids=[place1, place2])
    person2 = PersonFactory(name="person2", place_ids=[place1])
    person3 = PersonFactory(name="person3", place_ids=[place3, place2])
    assert person1.place_ids == [place1, place2]
    assert Person.objects.all().count() == 4
    assert list(
        Person.objects.filter(place_ids__contains=[place1]).order_by("name")
    ) == [person1, person2]
    assert list(
        Person.objects.filter(place_ids__contains=[place2]).order_by("name")
    ) == [person1, person3]
    assert list(Person.objects.filter(place_ids__contains=[place1, place2])) == [
        person1
    ]
    assert (
        Person.objects.filter(place_ids__contains=[place1, place2, place3]).count() == 0
    )

    # NOTE: This stopped working after Python 3.9 update and it's package upgrades
    # - also the empty set is included, when it should not be.
    # However, it should still be supported the same way:
    # https://docs.djangoproject.com/en/4.2/ref/contrib/postgres/fields/.
    # Currently the exclude-query is always needed as a part of the query.
    # assert list(
    #     Person.objects.filter(
    #         place_ids__contained_by=[place1, place2]
    #     ).order_by("name")
    # ) == [person1, person2]
    assert list(
        Person.objects.exclude(place_ids=[])
        .filter(place_ids__contained_by=[place1, place2])
        .order_by("name")
    ) == [person1, person2]
    assert (
        Person.objects.exclude(place_ids=[])
        .filter(place_ids__contained_by=[place1, place2, place3])
        .count()
        == 3
    )

    assert list(
        Person.objects.filter(place_ids__overlap=[place1]).order_by("name")
    ) == [person1, person2]
    assert list(
        Person.objects.filter(place_ids__overlap=[place1, place3]).order_by("name")
    ) == [person1, person2, person3]

    assert list(Person.objects.filter(place_ids__len=1)) == [person2]


@pytest.mark.django_db
def test_user_str():
    user_with_name_and_email = UserFactory.create(
        first_name="first_name",
        last_name="last_name",
        username="user_with_name_and_email",
        email="user_with_name_and_email@email.com",
    )
    assert user_with_name_and_email.__str__() == "%s %s (%s)" % (
        user_with_name_and_email.last_name,
        user_with_name_and_email.first_name,
        user_with_name_and_email.email,
    )

    user_without_full_name_but_email = UserFactory.create(
        first_name="",
        last_name="last_name",
        username="user_without_full_name_but_email",
        email="user_without_full_name_but_email@email.com",
    )
    assert (
        user_without_full_name_but_email.__str__()
        == user_without_full_name_but_email.email
    )

    user_without_name_and_email = UserFactory.create(
        first_name="",
        last_name="last_name",
        username="user_without_name_and_email",
        email="",
    )
    assert user_without_name_and_email.__str__() == user_without_name_and_email.username


@pytest.mark.django_db
def test_too_old_personal_data(mock_get_event_data):
    too_old = timezone.now() - relativedelta(months=24, days=1)
    still_valid = timezone.now() - relativedelta(months=24, days=-1)

    # ### EXPECTED PERSON OBJECTS IN RESULTS

    (
        old_enrolment_person,
        old_study_group_person,
        old_enrolment_and_study_group_person,
        no_enrolment_or_study_group_person,
    ) = expected_people = PersonFactory.create_batch(4, user=None)

    # person with a too old enrolment
    EnrolmentFactory(person=old_enrolment_person, occurrence__end_time=too_old)

    # person with a too old study group
    EnrolmentFactory(
        study_group__person=old_study_group_person, occurrence__end_time=too_old
    )

    # person with too old enrolment and study group
    EnrolmentFactory(
        person=old_enrolment_and_study_group_person,
        study_group__person=old_enrolment_and_study_group_person,
        occurrence__end_time=too_old,
    )

    # no_enrolment_or_study_group_person has no enrolment nor study group

    # ### NOT EXPECTED PERSON OBJECTS IN RESULTS

    (
        valid_enrolment_person,
        valid_study_group_person,
        valid_enrolment_and_study_group_person,
    ) = PersonFactory.create_batch(3, user=None)
    PersonFactory(user=UserFactory())  # person with a user

    # person with a valid enrolment
    EnrolmentFactory(person=valid_enrolment_person, occurrence__end_time=still_valid)

    # person with a valid study group
    EnrolmentFactory(
        study_group__person=valid_study_group_person, occurrence__end_time=still_valid
    )

    # person with valid enrolment and study group
    EnrolmentFactory(
        person=valid_enrolment_and_study_group_person,
        study_group__person=valid_enrolment_and_study_group_person,
        occurrence__end_time=still_valid,
    )

    results = Person.objects.retention_period_exceeded()
    assert len(results) == len(expected_people)
    assert all(person in results for person in expected_people)


@pytest.mark.django_db
@pytest.mark.parametrize("delete_via_queryset", (False, True))
def test_user_deletion_deletes_palvelutarjotin_event_contact_info(delete_via_queryset):
    event = PalvelutarjotinEventFactory(
        contact_email="test_event@example.com", contact_phone_number="1234567"
    )
    another_event = PalvelutarjotinEventFactory(
        contact_email="test_another_event@example.com", contact_phone_number="7654321"
    )

    if delete_via_queryset:
        User.objects.filter(pk=event.contact_person.user.pk).delete()
    else:
        event.contact_person.user.delete()

    event.refresh_from_db()
    another_event.refresh_from_db()

    assert event.contact_person is None
    assert event.contact_email == event.contact_phone_number == ""
    assert event.contact_info_deleted_at

    assert another_event.contact_person
    assert another_event.contact_email == "test_another_event@example.com"
    assert another_event.contact_phone_number == "7654321"
    assert not another_event.contact_info_deleted_at
