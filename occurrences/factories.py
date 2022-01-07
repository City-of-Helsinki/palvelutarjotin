import factory
import pytz
from occurrences.models import (
    Enrolment,
    Language,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    StudyLevel,
    VenueCustomData,
)
from organisations.factories import OrganisationFactory, PersonFactory


class LanguageFactory(factory.django.DjangoModelFactory):
    id = factory.Faker("pystr", max_chars=10)
    name = factory.Faker("text", max_nb_chars=20)

    class Meta:
        model = Language


class PalvelutarjotinEventFactory(factory.django.DjangoModelFactory):
    linked_event_id = factory.Faker("pystr", max_chars=5)
    enrolment_start = factory.Faker(
        "date_time", tzinfo=pytz.timezone("Europe/Helsinki"),
    )
    enrolment_end_days = factory.Faker("random_int", max=2)
    needed_occurrences = factory.Faker("random_int", max=10)
    contact_phone_number = factory.Faker("phone_number")
    contact_email = factory.Faker("email")
    organisation = factory.SubFactory(OrganisationFactory)
    contact_person = factory.SubFactory(PersonFactory)

    class Meta:
        model = PalvelutarjotinEvent


class OccurrenceFactory(factory.django.DjangoModelFactory):
    place_id = factory.Faker("text", max_nb_chars=64)
    min_group_size = factory.Faker("random_int", max=1000)
    max_group_size = factory.Faker("random_int", max=1000)
    start_time = factory.Faker("date_time", tzinfo=pytz.timezone("Europe/Helsinki"))
    end_time = factory.Faker("date_time", tzinfo=pytz.timezone("Europe/Helsinki"))
    p_event = factory.SubFactory(PalvelutarjotinEventFactory)
    amount_of_seats = factory.Faker("random_int", max=50)
    seat_type = Occurrence.OCCURRENCE_SEAT_TYPE_CHILDREN_COUNT

    class Meta:
        model = Occurrence

    @factory.post_generation
    def contact_persons(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of organisations were passed in, use them
            for person in extracted:
                self.contact_persons.add(person)

    @factory.post_generation
    def languages(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of organisations were passed in, use them
            for language in extracted:
                self.languages.add(language)


class StudyLevelFactory(factory.django.DjangoModelFactory):
    label = factory.Faker("text", max_nb_chars=20)
    level = factory.Faker("random_int", min=0, max=15)

    class Meta:
        model = StudyLevel


class StudyGroupFactory(factory.django.DjangoModelFactory):
    person = factory.SubFactory(PersonFactory)
    unit_name = factory.Faker("text", max_nb_chars=100)
    group_size = factory.Faker("random_int", max=1000)
    extra_needs = factory.Faker("text", max_nb_chars=100)
    group_name = factory.Faker("text", max_nb_chars=100)
    amount_of_adult = 0

    @factory.post_generation
    def study_levels(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of organisations were passed in, use them
            for study_level in extracted:
                self.study_levels.add(study_level)

    class Meta:
        model = StudyGroup


class EnrolmentFactory(factory.django.DjangoModelFactory):
    study_group = factory.SubFactory(StudyGroupFactory)
    occurrence = factory.SubFactory(OccurrenceFactory)
    person = factory.SubFactory(PersonFactory)

    class Meta:
        model = Enrolment


class VenueCustomDataFactory(factory.django.DjangoModelFactory):
    place_id = factory.Faker("pystr", max_chars=5)
    description = factory.Faker("text", max_nb_chars=100)
    has_clothing_storage = factory.Faker("boolean")
    has_snack_eating_place = factory.Faker("boolean")
    outdoor_activity = factory.Faker("boolean")

    class Meta:
        model = VenueCustomData
