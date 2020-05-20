from django.db import transaction
from graphene import (
    Boolean,
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
from graphene_linked_events.rest_client import LinkedEventsApiClient
from graphene_linked_events.utils import format_request, format_response, json2obj
from graphql_jwt.decorators import staff_member_required
from occurrences.models import PalvelutarjotinEvent
from occurrences.schema import PalvelutarjotinEventInput, PalvelutarjotinEventNode

from common.utils import update_object
from palvelutarjotin import settings
from palvelutarjotin.exceptions import ObjectDoesNotExistError

api_client = LinkedEventsApiClient(config=settings.LINKED_EVENTS_API_CONFIG)


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
    location = Field(Place)
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
    short_description = Field(LocalisedObject)
    provider = Field(LocalisedObject)
    info_url = Field(LocalisedObject)
    provider_contact_info = String()
    description = Field(LocalisedObject)
    p_event = Field(PalvelutarjotinEventNode)

    def resolve_p_event(self, info, **kwargs):
        return PalvelutarjotinEvent.objects.get(linked_event_id=self.id)


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
        locations=String(),
        page=Int(),
        page_size=Int(),
        publisher=ID(),
        sort=String(),
        start=String(),
        super_event=ID(),
        super_event_type=List(String),
        text=String(),
        translation=String(),
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
            response = api_client.retrieve("event", kwargs["id"], params=params)
        else:
            response = api_client.retrieve("event", kwargs["id"])
        obj = json2obj(format_response(response))
        return obj

    @staticmethod
    def resolve_events(parent, info, **kwargs):
        response = api_client.list("event", filter_list=kwargs)
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


class IdObjectInput(InputObjectType):
    internal_id = String()


class AddEventMutationInput(InputObjectType):
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
    start_time = String(required=True)
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
    p_event = InputField(
        PalvelutarjotinEventInput,
        required=True,
        description="Palvelutarjotin event data",
    )


class UpdateEventMutationInput(AddEventMutationInput):
    id = String(required=True)


class AddEventMutation(Mutation):
    class Arguments:
        event = AddEventMutationInput()

    response = Field(EventMutationResponse)

    @staff_member_required
    @transaction.atomic
    def mutate(root, info, **kwargs):
        # Format to JSON POST body
        p_event_data = kwargs["event"].pop("p_event")
        body = format_request(kwargs["event"])
        # TODO: proper validation if necessary
        result = api_client.create("event", body)
        event_obj = json2obj(format_response(result))
        if result.status_code == 201:
            # Create palvelutarjotin event if event created successful
            p_event_data["linked_event_id"] = event_obj.id
            PalvelutarjotinEvent.objects.create(**p_event_data)
        response = EventMutationResponse(status_code=result.status_code, body=event_obj)
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
        p_event_data = kwargs["event"].pop("p_event")
        body = format_request(kwargs["event"])
        # TODO: proper validation if necessary
        result = api_client.update("event", event_id, body)
        if result.status_code == 200:
            # Only update p_event if main event updated successfully
            try:
                p_event = PalvelutarjotinEvent.objects.get(linked_event_id=event_id)
            except PalvelutarjotinEvent.DoesNotExist as e:
                raise ObjectDoesNotExistError(e)
            update_object(p_event, p_event_data)
        response = EventMutationResponse(
            status_code=result.status_code, body=json2obj(format_response(result))
        )
        return UpdateEventMutation(response=response)


class DeleteEventMutation(Mutation):
    class Arguments:
        event_id = String(required=True)

    response = Field(EventMutationResponse)

    @staff_member_required
    def mutate(root, info, **kwargs):
        event_id = kwargs["event_id"]
        # TODO: proper validation if necessary
        result = api_client.delete("event", event_id)
        response = EventMutationResponse(status_code=result.status_code, body=None)
        return DeleteEventMutation(response=response)


class UploadImageMutationInput(InputObjectType):
    license = String()
    name = String(required=True)
    cropping = String()
    photographer_name = String()
    image = Upload(
        description="Following GraphQL file upload specs here: "
        "https://github.com/jaydenseric/graphql-multipart-request-spec"
    )


class ImageMutationResponse(ObjectType):
    status_code = Int(required=True)
    body = Field(Image)


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
        response = ImageMutationResponse(status_code=result.status_code, body=image_obj)
        return UploadImageMutation(response=response)


class DeleteImageMutation(Mutation):
    class Arguments:
        image_id = String(required=True)

    response = Field(ImageMutationResponse)

    @staff_member_required
    def mutate(root, info, **kwargs):
        image_id = kwargs["image_id"]
        result = api_client.delete("image", image_id)
        response = ImageMutationResponse(status_code=result.status_code, body=None)
        return DeleteImageMutation(response=response)


class Mutation:
    add_event_mutation = AddEventMutation.Field()
    update_event_mutation = UpdateEventMutation.Field()
    delete_event_mutation = DeleteEventMutation.Field()

    upload_image_mutation = UploadImageMutation.Field()
    delete_image_mutation = DeleteImageMutation.Field()
