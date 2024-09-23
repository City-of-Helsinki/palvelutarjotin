import factory
from django.contrib.auth import get_user_model

from common.mixins import SaveAfterPostGenerationMixin
from organisations.models import Organisation, OrganisationProposal, Person


def fake_id_array():
    from faker import Faker

    fake = Faker()
    return fake.pylist(3, True, "str")


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username_base = factory.Faker("user_name")
    username_suffix = factory.Faker("password", length=6, special_chars=False)
    username = factory.LazyAttribute(lambda u: f"{u.username_base}_{u.username_suffix}")
    email = factory.Faker("email")

    class Meta:
        model = get_user_model()
        exclude = ("username_base", "username_suffix")
        skip_postgeneration_save = True  # Not needed after factory v4.0.0


class PersonFactory(SaveAfterPostGenerationMixin, factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    phone_number = factory.Faker("phone_number")
    email_address = factory.Faker("email")
    place_ids = factory.LazyFunction(fake_id_array)

    class Meta:
        model = Person

    @factory.post_generation
    def organisations(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of organisations were passed in, use them
            for organisation in extracted:
                self.organisations.add(organisation)


class OrganisationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("company")
    phone_number = factory.Faker("phone_number")
    type = factory.Faker(
        "random_element",
        elements=[t[0] for t in Organisation.ORGANISATION_TYPES],
    )
    publisher_id = factory.Faker("pystr", max_chars=5)

    class Meta:
        model = Organisation
        skip_postgeneration_save = True  # Not needed after factory v4.0.0


class OrganisationProposalFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("company")
    description = factory.Faker("text", max_nb_chars=255)
    phone_number = factory.Faker("phone_number")
    applicant = factory.SubFactory(PersonFactory)

    class Meta:
        model = OrganisationProposal
        skip_postgeneration_save = True  # Not needed after factory v4.0.0
