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
    extra_needs = factory.Faker("text", max_nb_chars=100)
    group_name = factory.Faker("text", max_nb_chars=100)
    amount_of_adult = factory.Faker("random_int", max=10)
    study_level = factory.Faker(
        "random_element", elements=[l[0] for l in StudyGroup.STUDY_LEVELS]
    )

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
