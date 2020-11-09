from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone
from graphene import (
    Boolean,
    Enum,
    Field,
    Float,
    ID,
    InputField,
    InputObjectType,
    Int,
    List,
    Mutation,
    NonNull,
    ObjectType,
    String,
)
from graphene_file_upload.scalars import Upload
from graphene_linked_events.utils import (
    api_client,
    format_request,
    format_response,
    json2obj,
)
from graphql_jwt.decorators import staff_member_required
from occurrences.models import PalvelutarjotinEvent, VenueCustomData
from occurrences.schema import (
    PalvelutarjotinEventInput,
    PalvelutarjotinEventNode,
    VenueNode,
)
from organisations.models import Organisation, Person

from common.utils import (
    format_linked_event_datetime,
    get_editable_obj_from_global_id,
    get_obj_from_global_id,
    update_object,
)
from palvelutarjotin.exceptions import ApiUsageError, ObjectDoesNotExistError
from palvelutarjotin.settings import KEYWORD_SET_ID_MAPPING, LINKED_EVENTS_API_CONFIG

PublicationStatusEnum = Enum(
    "PublicationStatus",
    [(s[0].upper(), s[0]) for s in PalvelutarjotinEvent.PUBLICATION_STATUSES],
)

KeywordSetEnum = Enum(
    "KeywordSetType", [(s.upper(), s) for s in KEYWORD_SET_ID_MAPPING.keys()]
)


class IdObject(ObjectType):
    id = String()
    internal_id = ID(required=True)
    internal_context = String()
    internal_type = String()
    created_time = String()
    last_modified_time = String()
    data_source = String()
    publisher = String()


class LocalisedObject(ObjectType):
    fi = String()
    sv = String()
    en = String()


class LocalisedObjectInput(InputObjectType):
    fi = String()
    sv = String()
    en = String()


class Division(ObjectType):
    type = String(required=True)
    ocdId = String(description="Open Civic Data ID")
    municipality = String()
    name = Field(LocalisedObject)


class Image(IdObject):
    license = String()
    name = String(required=True)
    url = String(required=True)
    cropping = String()
    photographer_name = String()
    alt_text = String()


class PlacePosition(ObjectType):
    type = String(required=True)
    coordinates = NonNull(List(NonNull(Float)))


class Place(IdObject):
    divisions = List(Division)
    custom_data = String()
    email = String()
    contact_type = String()
    address_region = String()
    postal_code = String()
    post_office_box_num = String()
    address_country = String()
    deleted = Boolean()
    n_events = Int()
    image = Int()
    parent = ID()
    replaced_by = String()
    position = Field(PlacePosition)
    name = Field(LocalisedObject)
    description = String()
    telephone = Field(LocalisedObject)
    address_locality = Field(LocalisedObject)
    street_address = Field(LocalisedObject)
    info_url = Field(LocalisedObject)


class Keyword(IdObject):
    alt_labels = List(String)
    aggregate = Boolean()
    deprecated = Boolean()
    n_events = Int()
    image = Int()
    data_source = String()
    publisher = ID()
    name = Field(LocalisedObject)


class KeywordSet(IdObject):
    usage = String()
    keywords = NonNull(List(NonNull(Keyword)))
    name = Field(LocalisedObject)


class ExternalLink(ObjectType):
    name = String()
    link = String()
    language = String()


class Offer(ObjectType):
    is_free = Boolean()
    description = Field(LocalisedObject)
    price = Field(LocalisedObject)
    info_url = Field(LocalisedObject)


class OfferInput(InputObjectType):
    is_free = Boolean()
    description = Field(LocalisedObjectInput)
    price = Field(LocalisedObjectInput)
    info_url = Field(LocalisedObjectInput)


class InLanguage(IdObject):
    translation_available = Boolean()
    name = Field(LocalisedObject)


class ExtensionCourse(ObjectType):
    enrolment_start_time = String()
    enrolment_end_time = String()
    maximum_attendee_capacity = Int()
    minimum_attendee_capacity = Int()
    remaining_attendee_capacity = Int()


class Event(IdObject):
    id = String(required=True)
    location = Field(Place, required=True)
    keywords = NonNull(List(NonNull(Keyword)))
    super_event = Field(IdObject)
    event_status = String()
    external_links = NonNull(List(NonNull(ExternalLink)))
    offers = NonNull(List(NonNull(Offer)))
    sub_events = NonNull(List(NonNull(IdObject)))
    images = NonNull(List(NonNull(Image)))
    in_language = NonNull(List(NonNull(InLanguage)))
    audience = NonNull(List(NonNull(Keyword)))
    date_published = String()
    start_time = String()
    end_time = String()
    custom_data = String()
    audience_min_age = String()
    audience_max_age = String()
    super_event_type = String()
    extension_course = Field(ExtensionCourse)
    name = Field(LocalisedObject, required=True)
    localization_extra_info = Field(LocalisedObject)
    short_description = Field(LocalisedObject, required=True)
    provider = Field(LocalisedObject)
    info_url = Field(LocalisedObject)
    provider_contact_info = String()
    description = Field(LocalisedObject, required=True)
    p_event = Field(PalvelutarjotinEventNode, required=True)
    venue = Field(VenueNode)
    publication_status = String()

    def resolve_p_event(self, info, **kwargs):
        try:
            return PalvelutarjotinEvent.objects.get(linked_event_id=self.id)
        except PalvelutarjotinEvent.DoesNotExist:
            return None

    def resolve_venue(self, info, **kwargs):
        if hasattr(self.location, "id"):
            try:
                return VenueCustomData.objects.get(pk=self.location.id)
            except VenueCustomData.DoesNotExist:
                pass
        return None


class Meta(ObjectType):
    count = Int()
    next = String()
    previous = String()


class Response(ObjectType):
    meta = Field(Meta, required=True)


class EventListResponse(Response):
    data = NonNull(List(NonNull(Event)))


class PlaceListResponse(Response):
    data = NonNull(List(NonNull(Place)))


class KeywordListResponse(Response):
    data = NonNull(List(NonNull(Keyword)))


class EventSearchListResponse(Response):
    data = NonNull(List(NonNull(Event)))


class PlaceSearchListResponse(Response):
    data = NonNull(List(NonNull(Place)))


class ImageListResponse(Response):
    data = NonNull(List(NonNull(Image)))


class Query:
    events = Field(
        EventListResponse,
        divisions=List(String),
        end=String(),
        include=List(String),
        in_language=String(),
        is_free=Boolean(),
        keywords=List(String),
        keyword_not=List(String),
        language=String(),
        location=String(),
        page=Int(),
        page_size=Int(),
        publisher=ID(),
        sort=String(),
        start=String(),
        super_event=ID(),
        super_event_type=List(String),
        text=String(),
        translation=String(),
        organisation_id=String(),
        show_all=Boolean(),
        publication_status=String(),
    )
    event = Field(Event, id=ID(required=True), include=List(String))

    places = Field(
        PlaceListResponse,
        data_source=String(),
        divisions=List(String),
        page=Int(),
        page_size=Int(),
        show_all_places=Boolean(),
        sort=String(),
        text=String(),
    )
    place = Field(Place, id=ID(required=True))

    images = Field(ImageListResponse)

    image = Field(Image, id=ID(required=True))

    keywords = Field(
        KeywordListResponse,
        data_source=String(),
        page=Int(),
        page_size=Int(),
        show_all_keywords=Boolean(),
        sort=String(),
        text=String(),
    )
    keyword = Field(Keyword, id=ID(required=True))

    keyword_set = Field(KeywordSet, set_type=KeywordSetEnum(required=True))

    # TODO: Add support for start-end filter
    events_search = Field(
        EventSearchListResponse, input=String(required=True), include=List(String)
    )
    places_search = Field(
        PlaceSearchListResponse, input=String(required=True), include=List(String)
    )

    @staticmethod
    def resolve_event(parent, info, **kwargs):
        if kwargs.get("include"):
            params = {"include": ",".join(kwargs["include"])}
            response = api_client.retrieve(
                "event",
                kwargs["id"],
                params=params,
                is_staff=info.context.user.is_staff,
            )
        else:
            response = api_client.retrieve(
                "event", kwargs["id"], is_staff=info.context.user.is_staff
            )
        obj = json2obj(format_response(response))
        return obj

    @staticmethod
    def resolve_events(parent, info, **kwargs):
        organisation_global_id = kwargs.pop("organisation_id", None)
        if organisation_global_id:
            # Filter events by organisation id
            organisation = get_obj_from_global_id(
                info, organisation_global_id, Organisation
            )
            kwargs["publisher"] = organisation.publisher_id
        else:
            # If no organisation id specified, return all events from
            # palvelutarjotin data source
            kwargs["data_source"] = LINKED_EVENTS_API_CONFIG["DATA_SOURCE"]
        response = api_client.list(
            "event", filter_list=kwargs, is_staff=info.context.user.is_staff
        )
        return json2obj(format_response(response))

    @staticmethod
    def resolve_place(parent, info, **kwargs):
        response = api_client.retrieve("place", kwargs["id"])
        return json2obj(format_response(response))

    @staticmethod
    def resolve_places(parent, info, **kwargs):
        response = api_client.list("place", filter_list=kwargs)
        return json2obj(format_response(response))

    @staticmethod
    def resolve_keyword(parent, info, **kwargs):
        response = api_client.retrieve("keyword", kwargs["id"])
        return json2obj(format_response(response))

    @staticmethod
    def resolve_keywords(parent, info, **kwargs):
        response = api_client.list("keyword", filter_list=kwargs)
        return json2obj(format_response(response))

    @staticmethod
    def resolve_keyword_set(parent, info, **kwargs):
        set_type = kwargs["set_type"]
        keyword_set_id = KEYWORD_SET_ID_MAPPING.get(set_type)
        response = api_client.retrieve(
            "keyword_set", keyword_set_id, params={"include": "keywords"}
        )
        return json2obj(format_response(response))

    @staticmethod
    def resolve_image(parent, info, **kwargs):
        response = api_client.retrieve("image", kwargs["id"])
        return json2obj(format_response(response))

    @staticmethod
    def resolve_images(parent, info, **kwargs):
        response = api_client.list("image", filter_list=kwargs)
        return json2obj(format_response(response))

    @staticmethod
    def resolve_events_search(parent, info, **kwargs):
        search_params = {"type": "event", **kwargs}
        response = api_client.search(search_params=search_params)
        return json2obj(format_response(response))

    @staticmethod
    def resolve_places_search(parent, info, **kwargs):
        search_params = {"type": "place", **kwargs}
        response = api_client.search(search_params=search_params)
        return json2obj(format_response(response))


class EventMutationResponse(ObjectType):
    status_code = Int(required=True)
    body = Field(Event)
    result_text = String()


class IdObjectInput(InputObjectType):
    internal_id = String()


class EventMutationInput(InputObjectType):
    location = IdObjectInput(required=True)
    keywords = NonNull(List(NonNull(IdObjectInput)))
    super_event = String()
    event_status = String()
    external_links = List(NonNull(String))
    offers = NonNull(List(NonNull(OfferInput)))
    sub_events = List(NonNull(String))
    images = List(NonNull(IdObjectInput))
    in_language = List(NonNull(IdObjectInput))
    audience = List(NonNull(IdObjectInput))
    date_published = String()
    start_time = String()
    end_time = String()
    custom_data = String()
    audience_min_age = String()
    audience_max_age = String()
    super_event_type = String()
    extension_course = InputField(IdObjectInput)
    name = InputField(LocalisedObjectInput, required=True)
    localization_extra_info = InputField(LocalisedObjectInput)
    short_description = InputField(LocalisedObjectInput, required=True)
    provider = InputField(LocalisedObjectInput)
    info_url = InputField(LocalisedObjectInput)
    provider_contact_info = String()
    description = InputField(LocalisedObjectInput, required=True)
    organisation_id = String(
        description="Organisation global id which the created event belongs to",
        required=True,
    )


class AddEventMutationInput(EventMutationInput):
    draft = Boolean(
        description="Set to `true` to save event as draft version, when draft is true, "
        "event data validation will be skipped",
        default_value=False,
    )
    start_time = String(required=True)
    p_event = InputField(
        PalvelutarjotinEventInput,
        required=True,
        description="Palvelutarjotin event data",
    )


class UpdateEventMutationInput(EventMutationInput):
    id = String(required=True)
    start_time = String(required=True)
    p_event = InputField(
        PalvelutarjotinEventInput, description="Palvelutarjotin event data",
    )
    draft = Boolean(
        description="Set to `true` to save event as draft version, when draft is true, "
        "event data validation will be skipped",
        default_value=False,
    )


class PublishEventMutationInput(EventMutationInput):
    id = String(required=True)
    p_event = InputField(
        PalvelutarjotinEventInput, description="Palvelutarjotin event data",
    )


class AddEventMutation(Mutation):
    class Arguments:
        event = AddEventMutationInput()

    response = Field(EventMutationResponse)

    @staff_member_required
    @transaction.atomic
    def mutate(root, info, **kwargs):
        # Format to JSON POST body
        p_event_data = kwargs["event"].pop("p_event")

        organisation_gid = kwargs["event"].pop("organisation_id")
        organisation = get_editable_obj_from_global_id(
            info, organisation_gid, Organisation
        )
        person_gid = p_event_data.pop("contact_person_id", None)
        if person_gid:
            person = get_obj_from_global_id(info, person_gid, Person)
            if not organisation.persons.filter(id=person.id).exists():
                raise PermissionDenied("Contact person does not belong to organisation")
            p_event_data["contact_person_id"] = person.id
        if organisation.publisher_id:
            # If publisher id does not exist, LinkedEvent will decide the
            # publisher id which is the API key root publisher
            kwargs["event"]["publisher"] = organisation.publisher_id
        if kwargs["event"]["draft"]:
            kwargs["event"][
                "publication_status"
            ] = PalvelutarjotinEvent.PUBLICATION_STATUS_DRAFT

        body = format_request(kwargs["event"])
        # TODO: proper validation if necessary
        result = api_client.create("event", body)
        event_obj = json2obj(format_response(result))
        if result.status_code == 201:
            # Create palvelutarjotin event if event created successful
            p_event_data["linked_event_id"] = event_obj.id
            p_event_data["organisation_id"] = organisation.id
            PalvelutarjotinEvent.objects.create(**p_event_data)
        response = EventMutationResponse(
            status_code=result.status_code, body=event_obj, result_text=result.text
        )
        return AddEventMutation(response=response)


class UpdateEventMutation(Mutation):
    class Arguments:
        event = UpdateEventMutationInput()

    response = Field(EventMutationResponse)

    @staff_member_required
    @transaction.atomic
    def mutate(root, info, **kwargs):
        # Format to JSON POST body
        event_id = kwargs["event"].pop("id")
        p_event_data = kwargs["event"].pop("p_event", None)

        organisation_gid = kwargs["event"].pop("organisation_id")

        organisation = get_editable_obj_from_global_id(
            info, organisation_gid, Organisation
        )
        if p_event_data:
            person_gid = p_event_data.pop("contact_person_id", None)
            if person_gid:
                person = get_obj_from_global_id(info, person_gid, Person)
                if not organisation.persons.filter(id=person.id).exists():
                    raise PermissionDenied(
                        "Contact person does not belong to organisation"
                    )
                p_event_data["contact_person_id"] = person.id
        try:
            p_event = PalvelutarjotinEvent.objects.get(
                linked_event_id=event_id, organisation=organisation
            )
        except PalvelutarjotinEvent.DoesNotExist:
            raise PermissionDenied(
                f"User does not have permission to edit this "
                f"{PalvelutarjotinEvent.__name__}"
            )

        if organisation.publisher_id:
            # If publisher id does not exist, LinkedEvent will decide the
            # publisher id which is the API key root publisher
            kwargs["event"]["publisher"] = organisation.publisher_id

        if kwargs["event"].get("draft", False):
            kwargs["event"][
                "publication_status"
            ] = PalvelutarjotinEvent.PUBLICATION_STATUS_DRAFT

        body = format_request(kwargs["event"])
        # TODO: proper validation if necessary
        result = api_client.update("event", event_id, body)
        if result.status_code == 200 and p_event_data:
            update_object(p_event, p_event_data)
        response = EventMutationResponse(
            status_code=result.status_code,
            body=json2obj(format_response(result)),
            result_text=result.text,
        )
        return UpdateEventMutation(response=response)


def _prepare_published_event_data(event_id):
    # Only care about getting published event data, no permission/authorization check
    # here
    p_event = PalvelutarjotinEvent.objects.get(linked_event_id=event_id)
    if not p_event.occurrences.exists():
        raise ApiUsageError("Cannot publish event without event occurrences")
    body = {
        "publication_status": PalvelutarjotinEvent.PUBLICATION_STATUS_PUBLIC,
        "start_time": format_linked_event_datetime(timezone.now()),
        "end_time": format_linked_event_datetime(
            p_event.get_end_time_from_occurrences()
        ),
    }
    return body


class PublishEventMutation(UpdateEventMutation):
    class Arguments:
        event = PublishEventMutationInput()

    response = Field(EventMutationResponse)

    @staff_member_required
    @transaction.atomic
    def mutate(root, info, **kwargs):
        event_id = kwargs["event"].get("id")
        try:
            kwargs["event"].update(_prepare_published_event_data(event_id))
        except PalvelutarjotinEvent.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        # Publish event is actually update event, reuse UpdateEventMutation
        response = UpdateEventMutation.mutate(root, info, **kwargs).response
        return PublishEventMutation(response=response)


class UnpublishEventMutation(UpdateEventMutation):
    class Arguments:
        event = PublishEventMutationInput()

    response = Field(EventMutationResponse)

    @staff_member_required
    @transaction.atomic
    def mutate(root, info, **kwargs):
        try:
            kwargs["event"].update(
                {"publication_status": PalvelutarjotinEvent.PUBLICATION_STATUS_DRAFT}
            )
        except PalvelutarjotinEvent.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        # Unpublish event is actually update event, reuse UpdateEventMutation
        response = UpdateEventMutation.mutate(root, info, **kwargs).response
        return UnpublishEventMutation(response=response)


class DeleteEventMutation(Mutation):
    class Arguments:
        event_id = String(required=True)

    response = Field(EventMutationResponse)

    @staff_member_required
    def mutate(root, info, **kwargs):
        event_id = kwargs["event_id"]
        # TODO: proper validation if necessary
        result = api_client.delete("event", event_id)
        if result.status_code == 204:
            try:
                p_event = PalvelutarjotinEvent.objects.get(linked_event_id=event_id)
                p_event.delete()
            except PalvelutarjotinEvent.DoesNotExist:
                pass
        response = EventMutationResponse(
            status_code=result.status_code, body=None, result_text=result.text
        )
        return DeleteEventMutation(response=response)


class UploadImageMutationInput(InputObjectType):
    license = String()
    alt_text = String()
    name = String(required=True)
    cropping = String()
    photographer_name = String()
    image = Upload(
        description="Following GraphQL file upload specs here: "
        "https://github.com/jaydenseric/graphql-multipart-request-spec"
    )


class UpdateImageMutationInput(UploadImageMutationInput):
    id = String(required=True)


class ImageMutationResponse(ObjectType):
    status_code = Int(required=True)
    body = Field(Image)
    result_text = String()


class UploadImageMutation(Mutation):
    class Arguments:
        image = UploadImageMutationInput()

    response = Field(ImageMutationResponse)

    @staff_member_required
    def mutate(root, info, **kwargs):
        image = kwargs["image"].pop("image")
        body = kwargs["image"]
        result = api_client.upload(
            "image", body, files={"image": (image.name, image.file, image.content_type)}
        )
        image_obj = json2obj(format_response(result))
        response = ImageMutationResponse(
            status_code=result.status_code, body=image_obj, result_text=result.text
        )
        return UploadImageMutation(response=response)


class UpdateImageMutation(Mutation):
    class Arguments:
        image = UpdateImageMutationInput()

    response = Field(ImageMutationResponse)

    @staff_member_required
    def mutate(root, info, **kwargs):
        image_id = kwargs["image"].pop("id")
        body = format_request(kwargs["image"])
        result = api_client.update("image", image_id, body)
        image_obj = json2obj(format_response(result))
        response = ImageMutationResponse(
            status_code=result.status_code, body=image_obj, result_text=result.text
        )
        return UpdateImageMutation(response=response)


class DeleteImageMutation(Mutation):
    class Arguments:
        image_id = String(required=True)

    response = Field(ImageMutationResponse)

    @staff_member_required
    def mutate(root, info, **kwargs):
        image_id = kwargs["image_id"]
        result = api_client.delete("image", image_id)
        response = ImageMutationResponse(
            status_code=result.status_code, body=None, result_text=result.text
        )
        return DeleteImageMutation(response=response)


class Mutation:
    add_event_mutation = AddEventMutation.Field()
    update_event_mutation = UpdateEventMutation.Field()
    publish_event_mutation = PublishEventMutation.Field(
        description="Using this mutation will update event publication status and "
        "also set the `start_time`, `end_time` of linkedEvent"
    )
    unpublish_event_mutation = UnpublishEventMutation.Field()
    delete_event_mutation = DeleteEventMutation.Field()

    upload_image_mutation = UploadImageMutation.Field()
    update_image_mutation = UpdateImageMutation.Field()
    delete_image_mutation = DeleteImageMutation.Field()
