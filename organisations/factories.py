import factory
from django.contrib.auth import get_user_model
from organisations.models import Organisation, OrganisationProposal, Person


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    email = factory.Faker("email")

    class Meta:
        model = get_user_model()


class PersonFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    phone_number = factory.Faker("phone_number")
    email_address = factory.Faker("email")

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
    name = factory.Faker("name")
    phone_number = factory.Faker("phone_number")
    type = factory.Faker(
        "random_element", elements=[t[0] for t in Organisation.ORGANISATION_TYPES],
    )
    publisher_id = factory.Faker("pystr", max_chars=5)

    class Meta:
        model = Organisation


class OrganisationProposalFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text", max_nb_chars=255)
    phone_number = factory.Faker("phone_number")
    applicant = factory.SubFactory(PersonFactory)

    class Meta:
        model = OrganisationProposal
