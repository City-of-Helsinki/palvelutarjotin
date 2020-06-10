import graphene
from django.contrib.auth import get_user_model
from django.db import transaction
from graphene import InputObjectType, relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required, superuser_required
from organisations.models import Organisation, Person

from common.utils import get_node_id_from_global_id, update_object
from palvelutarjotin.exceptions import ApiUsageError, ObjectDoesNotExistError

User = get_user_model()


class PersonNode(DjangoObjectType):
    class Meta:
        model = Person
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.user_can_view(info.context.user).order_by("name")


class PersonNodeInput(InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    phone_number = graphene.String()
    email_address = graphene.String(required=True)


class OrganisationNode(DjangoObjectType):
    class Meta:
        model = Organisation
        interfaces = (relay.Node,)


def validate_person_data(kwargs):
    # TODO: Add validation
    pass


class CreateMyProfileMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        phone_number = graphene.String()
        email_address = graphene.String(required=True)
        organisations = graphene.List(graphene.ID)

    my_profile = graphene.Field(PersonNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user
        if Person.objects.filter(user=user).exists():
            raise ApiUsageError("User profile already exists")
        validate_person_data(kwargs)
        organisation_ids = kwargs.pop("organisations", None)
        kwargs["user_id"] = user.id
        person = Person.objects.create(**kwargs)
        if organisation_ids:
            for org_global_id in organisation_ids:
                org_id = get_node_id_from_global_id(org_global_id, "OrganisationNode")
                try:
                    organisation = Organisation.objects.get(id=org_id)
                except Organisation.DoesNotExist as e:
                    raise ObjectDoesNotExistError(e)
                person.organisations.add(organisation)
        return CreateMyProfileMutation(my_profile=person)


class UpdateMyProfileMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String()
        phone_number = graphene.String()
        email_address = graphene.String()
        organisations = graphene.List(
            graphene.ID,
            description="If present, should include all organisation ids of user",
        )

    my_profile = graphene.Field(PersonNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        validate_person_data(kwargs)
        user = info.context.user
        organisation_ids = kwargs.pop("organisations", None)
        try:
            person = user.person
        except Person.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

        update_object(person, kwargs)
        if organisation_ids:
            person.organisations.clear()
            for org_global_id in organisation_ids:
                org_id = get_node_id_from_global_id(org_global_id, "OrganisationNode")
                try:
                    organisation = Organisation.objects.get(id=org_id)
                except Organisation.DoesNotExist as e:
                    raise ObjectDoesNotExistError(e)
                person.organisations.add(organisation)

        return UpdateMyProfileMutation(my_profile=person)


class OrganisationTypeEnum(graphene.Enum):
    USER = "user"
    PROVIDER = "provider"


def validate_organisation_data(kwargs):
    # TODO: Add validation
    pass


class AddOrganisationMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        phone_number = graphene.String()
        type = OrganisationTypeEnum(required=True)
        publisher_id = graphene.String()

    organisation = graphene.Field(OrganisationNode)

    @classmethod
    @superuser_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        validate_organisation_data(kwargs)
        organisation = Organisation.objects.create(**kwargs)
        return AddOrganisationMutation(organisation=organisation)


class UpdateOrganisationMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        name = graphene.String()
        phone_number = graphene.String()
        type = OrganisationTypeEnum()
        publisher_id = graphene.String()

    organisation = graphene.Field(OrganisationNode)

    @classmethod
    @superuser_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        organisation_id = get_node_id_from_global_id(
            kwargs.pop("id"), "OrganisationNode"
        )
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

        validate_organisation_data(kwargs)
        update_object(organisation, kwargs)
        # TODO: Add support to related fields update: e.g group/persons

        return UpdateOrganisationMutation(organisation=organisation)


class UpdatePersonMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        name = graphene.String()
        phone_number = graphene.String()
        email_address = graphene.String()

    person = graphene.Field(PersonNode)

    @classmethod
    @superuser_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        person_id = get_node_id_from_global_id(kwargs.pop("id"), "PersonNode")
        try:
            person = Person.objects.get(pk=person_id)
        except Person.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        validate_person_data(kwargs)
        update_object(person, kwargs)
        # TODO: Add support to related fields update: e.g organisation/studyGroup

        return UpdatePersonMutation(person=person)


class Query:
    my_profile = graphene.Field(
        PersonNode, description="Query personal data of logged user"
    )

    person = relay.Node.Field(PersonNode)
    persons = DjangoConnectionField(PersonNode)

    organisation = relay.Node.Field(OrganisationNode)
    organisations = DjangoConnectionField(OrganisationNode)

    @staticmethod
    @login_required
    def resolve_my_profile(parent, info, **kwargs):
        return Person.objects.filter(user=info.context.user).first()


class Mutation:
    create_my_profile = CreateMyProfileMutation.Field()
    update_my_profile = UpdateMyProfileMutation.Field()

    add_organisation = AddOrganisationMutation.Field()
    update_organisation = UpdateOrganisationMutation.Field()

    update_person = UpdatePersonMutation.Field()
