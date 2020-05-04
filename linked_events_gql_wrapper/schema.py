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
from graphql_jwt.decorators import staff_member_required
from linked_events_gql_wrapper.rest_client import LinkedEventsApiClient
from linked_events_gql_wrapper.utils import format_request, format_response, json2obj

from palvelutarjotin import settings

api_client = LinkedEventsApiClient(config=settings.LINKED_EVENTS_API_CONFIG)


class IdObject(ObjectType):
    id = ID(required=True)
    internal_id = String()
    internal_context = String()
    internal_type = String()
    created_time = String()
    last_modified_time = String()
    data_source = String()
    publisher = ID()


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
    ocdId = String()
    municipality = String()
    name = Field(LocalisedObject)


class Image(IdObject):
    license = String()
    name = String(required=True)
    url = String(required=True)
    cropping = String()
    photographer_name = String()


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
    image = Field(Image)
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
    image = Field(Image)
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
    audience = NonNull(List(NonNull(IdObject)))
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
    place = Field(Event, id=ID(required=True))

    keywords = Field(
        KeywordListResponse,
        data_source=String(),
        page=Int(),
        page_size=Int(),
        show_all_keywords=Boolean(),
        sort=String(),
        text=String(),
    )
    keyword = Field(Event, id=ID(required=True))

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
            params = {"include": kwargs["include"]}
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


class UpdateEventMutationInput(AddEventMutationInput):
    id = String(required=True)


class AddEventMutation(Mutation):
    class Arguments:
        event = AddEventMutationInput()

    response = Field(EventMutationResponse)

    @staff_member_required
    def mutate(root, info, **kwargs):
        # Format to JSON POST body
        body = format_request(kwargs["event"])
        # TODO: proper validation if necessary
        result = api_client.create("event", body)
        response = EventMutationResponse(
            status_code=result.status_code, body=json2obj(format_response(result))
        )
        return AddEventMutation(response=response)


class UpdateEventMutation(Mutation):
    class Arguments:
        event = UpdateEventMutationInput()

    response = Field(EventMutationResponse)

    @staff_member_required
    def mutate(root, info, **kwargs):
        # Format to JSON POST body
        event_id = kwargs["event"].pop("id")
        body = format_request(kwargs["event"])
        # TODO: proper validation if necessary
        result = api_client.update("event", event_id, body)
        response = EventMutationResponse(status_code=result.status_code, body=None)
        return AddEventMutation(response=response)


class DeleteEventMutation(Mutation):
    class Arguments:
        event_id = String()

    response = Field(EventMutationResponse)

    @staff_member_required
    def mutate(root, info, **kwargs):
        event_id = kwargs["event_id"]
        # TODO: proper validation if necessary
        result = api_client.delete("event", event_id)
        response = EventMutationResponse(status_code=result.status_code, body=None)
        return AddEventMutation(response=response)


class Mutation:
    add_event_mutation = AddEventMutation.Field()
    update_event_mutation = UpdateEventMutation.Field()
    delete_event_mutation = DeleteEventMutation.Field()
