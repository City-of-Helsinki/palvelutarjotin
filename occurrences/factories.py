import factory
import pytz
from occurrences.models import (
    Enrolment,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    VenueCustomData,
)
from organisations.factories import OrganisationFactory, PersonFactory


class PalvelutarjotinEventFactory(factory.django.DjangoModelFactory):
    linked_event_id = factory.Faker("text", max_nb_chars=64)
    enrolment_start = factory.Faker(
        "date_time", tzinfo=pytz.timezone("Europe/Helsinki"),
    )
    enrolment_end_days = factory.Faker("random_int", max=2)
    duration = factory.Faker("random_int", max=300)
    needed_occurrences = factory.Faker("random_int", max=10)

    class Meta:
        model = PalvelutarjotinEvent


class OccurrenceFactory(factory.django.DjangoModelFactory):
    place_id = factory.Faker("text", max_nb_chars=64)
    min_group_size = factory.Faker("random_int", max=1000)
    max_group_size = factory.Faker("random_int", max=1000)
    start_time = factory.Faker("date_time", tzinfo=pytz.timezone("Europe/Helsinki"))
    end_time = factory.Faker("date_time", tzinfo=pytz.timezone("Europe/Helsinki"))
    organisation = factory.SubFactory(OrganisationFactory)
    p_event = factory.SubFactory(PalvelutarjotinEventFactory)
    auto_acceptance = factory.Faker("boolean")
    amount_of_seats = factory.Faker("random_int", max=50)

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


class StudyGroupFactory(factory.django.DjangoModelFactory):
    person = factory.SubFactory(PersonFactory)
    name = factory.Faker("text", max_nb_chars=100)
    group_size = factory.Faker("random_int", max=1000)

    class Meta:
        model = StudyGroup


class EnrolmentFactory(factory.django.DjangoModelFactory):
    study_group = factory.SubFactory(StudyGroupFactory)
    occurrence = factory.SubFactory(OccurrenceFactory)

    class Meta:
        model = Enrolment


class VenueCustomDataFactory(factory.django.DjangoModelFactory):
    place_id = factory.Faker("pystr", max_chars=5)
    description = factory.Faker("text", max_nb_chars=100)
    has_clothing_storage = factory.Faker("boolean")
    has_snack_eating_place = factory.Faker("boolean")

    class Meta:
        model = VenueCustomData
