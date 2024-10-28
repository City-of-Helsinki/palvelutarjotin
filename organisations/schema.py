import graphene
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from graphene import Boolean, InputObjectType, relay
from graphene_django import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required, superuser_required

from common.utils import (
    get_node_id_from_global_id,
    LanguageEnum,
    map_enums_to_values_in_kwargs,
    update_object,
)
from organisations.models import Organisation, OrganisationProposal, Person
from palvelutarjotin.exceptions import (
    ApiUsageError,
    InvalidEmailFormatError,
    MissingMantatoryInformationError,
    ObjectDoesNotExistError,
)

User = get_user_model()


class PersonNode(DjangoObjectType):
    language = LanguageEnum(required=True)
    is_staff = Boolean(required=True)

    class Meta:
        model = Person
        exclude = ("p_event",)
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        # Allow access to person related to added study group in AddStudyGroupMutation
        if info.path.as_list() == ["addStudyGroup", "studyGroup", "person"]:
            return queryset
        return queryset.user_can_view(info.context.user).order_by("name")

    def resolve_is_staff(self, info, **kwargs):
        try:
            return self.user.is_staff if self.user else False
        # Contact person sharing the same Person model so it doesn't have user
        except User.DoesNotExist:
            return False


class PersonNodeInput(InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    phone_number = graphene.String()
    email_address = graphene.String(required=True)
    language = LanguageEnum(description="Default `fi`")
    place_ids = graphene.List(graphene.String)


class OrganisationNode(DjangoObjectType):
    class Meta:
        model = Organisation
        filter_fields = ["type"]
        exclude = ("p_event",)
        interfaces = (relay.Node,)

    persons = DjangoConnectionField(PersonNode, max_limit=None)


class OrganisationProposalNode(DjangoObjectType):
    class Meta:
        model = OrganisationProposal
        fields = "__all__"
        interfaces = (relay.Node,)


class OrganisationProposalNodeInput(InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    phone_number = graphene.String()


def validate_person_data(kwargs):
    if "email_address" in kwargs:
        try:
            validate_email(kwargs["email_address"])
        except ValidationError:
            raise InvalidEmailFormatError("Invalid email format")


class CreateMyProfileMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        phone_number = graphene.String()
        email_address = graphene.String(required=True)
        organisations = graphene.List(graphene.ID)
        organisation_proposals = graphene.List(
            OrganisationProposalNodeInput,
            description="Propose a new organisation being added. "
            + "Used with 3rd party organisations",
        )
        language = LanguageEnum(description="Default `fi`")
        place_ids = graphene.List(graphene.String)

    my_profile = graphene.Field(PersonNode)

    @classmethod
    @login_required
    @transaction.atomic
    @map_enums_to_values_in_kwargs
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user
        if Person.objects.filter(user=user).exists():
            raise ApiUsageError("User profile already exists")
        kwargs["user_id"] = user.id
        validate_person_data(kwargs)
        organisation_ids = kwargs.pop("organisations", None)
        organisation_proposals_data = kwargs.pop("organisation_proposals", None)
        person = Person.objects.create(**kwargs)
        if organisation_proposals_data:
            cls._set_organisation_proposals(organisation_proposals_data, person)
        if organisation_ids:
            cls._set_person_organisations(organisation_ids, person)
        person.notify_myprofile_creation()
        return CreateMyProfileMutation(my_profile=person)

    @staticmethod
    def _set_organisation_proposals(organisation_proposals_data, person):
        if organisation_proposals_data and person:
            for organisation_proposal_data in organisation_proposals_data:
                person.organisationproposal_set.create(**organisation_proposal_data)

    @staticmethod
    def _set_person_organisations(organisation_ids, person):
        if organisation_ids and person:
            for org_global_id in organisation_ids:
                org_id = get_node_id_from_global_id(org_global_id, "OrganisationNode")
                try:
                    organisation = Organisation.objects.get(id=org_id)
                except Organisation.DoesNotExist as e:
                    raise ObjectDoesNotExistError(e)
                person.organisations.add(organisation)


class UpdateMyProfileMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String()
        phone_number = graphene.String()
        email_address = graphene.String()
        language = LanguageEnum(description="Default `fi`")
        place_ids = graphene.List(graphene.String)

    my_profile = graphene.Field(PersonNode)

    @classmethod
    @login_required
    @transaction.atomic
    @map_enums_to_values_in_kwargs
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
            cls._set_person_organisations(organisation_ids, person)

        return UpdateMyProfileMutation(my_profile=person)

    @staticmethod
    def _set_person_organisations(organisation_ids, person):
        if organisation_ids and person:
            person.organisations.clear()
            for org_global_id in organisation_ids:
                org_id = get_node_id_from_global_id(org_global_id, "OrganisationNode")
                try:
                    organisation = Organisation.objects.get(id=org_id)
                except Organisation.DoesNotExist as e:
                    raise ObjectDoesNotExistError(e)
                person.organisations.add(organisation)


class OrganisationTypeEnum(graphene.Enum):
    USER = "user"
    PROVIDER = "provider"


def validate_organisation_data(**kwargs):
    if "publisher_id" in kwargs and (
        not kwargs["publisher_id"] or not str(kwargs["publisher_id"]).strip()
    ):
        raise MissingMantatoryInformationError("Missing/invalid publisher_id")


class AddOrganisationMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        phone_number = graphene.String()
        type = OrganisationTypeEnum(required=True)
        publisher_id = graphene.String(required=True)

    organisation = graphene.Field(OrganisationNode)

    @classmethod
    @superuser_required
    @transaction.atomic
    @map_enums_to_values_in_kwargs
    def mutate_and_get_payload(cls, root, info, **kwargs):
        validate_organisation_data(**kwargs)
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
    @map_enums_to_values_in_kwargs
    def mutate_and_get_payload(cls, root, info, **kwargs):
        organisation_id = get_node_id_from_global_id(
            kwargs.pop("id"), "OrganisationNode"
        )
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

        validate_organisation_data(**kwargs)
        update_object(organisation, kwargs)
        # TODO: Add support to related fields update: e.g group/persons

        return UpdateOrganisationMutation(organisation=organisation)


class UpdatePersonMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        name = graphene.String()
        phone_number = graphene.String()
        email_address = graphene.String()
        language = LanguageEnum()

    person = graphene.Field(PersonNode)

    @classmethod
    @superuser_required
    @transaction.atomic
    @map_enums_to_values_in_kwargs
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
    organisations = DjangoFilterConnectionField(OrganisationNode, max_limit=None)

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
