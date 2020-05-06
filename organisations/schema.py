import graphene
from django.contrib.auth import get_user_model
from django.db import transaction
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required, staff_member_required
from graphql_relay import from_global_id
from organisations.models import Organisation, Person

from common.utils import update_object
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


class UpdatePersonMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        name = graphene.String()
        phone_number = graphene.String()
        email_address = graphene.String()

    person = graphene.Field(PersonNode)

    @classmethod
    @staff_member_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        person_id = from_global_id(kwargs.pop("id"))[1]
        try:
            person = Person.objects.get(pk=person_id)
            validate_person_data(kwargs)
            update_object(person, kwargs)
        except Person.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

        return UpdateMyProfileMutation(my_profile=person)


class Query:
    my_profile = graphene.Field(
        PersonNode, description="Query personal data of " "logged user"
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
