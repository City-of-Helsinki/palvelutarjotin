import graphene
from django.contrib.auth import get_user_model
from django.db import transaction
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required, superuser_required
from organisations.models import Organisation, Person

from common.utils import get_node_id_from_global_id, update_object
from palvelutarjotin.exceptions import ObjectDoesNotExistError

User = get_user_model()


class PersonNode(DjangoObjectType):
    class Meta:
        model = Person
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.user_can_view(info.context.user).order_by("name")


class OrganisationNode(DjangoObjectType):
    class Meta:
        model = Organisation
        interfaces = (relay.Node,)


class UpdateMyProfileMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String()
        phone_number = graphene.String()
        email_address = graphene.String()

    my_profile = graphene.Field(PersonNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user

        try:
            person = user.person
        except Person.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

        update_object(person, kwargs)

        return UpdateMyProfileMutation(my_profile=person)


def validate_person_data(kwargs):
    # TODO: Add validation
    pass


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
    update_my_profile = UpdateMyProfileMutation.Field()
    add_organisation = AddOrganisationMutation.Field()
    update_organisation = UpdateOrganisationMutation.Field()

    update_person = UpdatePersonMutation.Field()