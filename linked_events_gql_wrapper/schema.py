from graphene import Boolean, Field, Float, ID, Int, List, NonNull, ObjectType, String
from linked_events_gql_wrapper.rest_client import LinkedEventsApiClient
from linked_events_gql_wrapper.utils import format_response, json2obj

from palvelutarjotin import settings

api_client = LinkedEventsApiClient(root=settings.LINKED_EVENTS_API_ROOT)


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
    events = Field(EventListResponse,)
    event = Field(Event, id=ID(required=True))

    places = Field(PlaceListResponse)
    place = Field(Event, id=ID(required=True))

    keywords = Field(KeywordListResponse)
    keyword = Field(Event, id=ID(required=True))

    # TODO: Add support for start-end filter
    events_search = Field(EventSearchListResponse, input=String(required=True))
    places_search = Field(PlaceSearchListResponse, input=String(required=True))

    @staticmethod
    def resolve_event(parent, info, **kwargs):
        response = api_client.retrieve("event", kwargs["id"])
        obj = json2obj(format_response(response))
        return obj

    @staticmethod
    def resolve_events(parent, info, **kwargs):
        response = api_client.list("event")
        return json2obj(format_response(response))

    @staticmethod
    def resolve_place(parent, info, **kwargs):
        response = api_client.retrieve("place", kwargs["id"])
        return json2obj(format_response(response))

    @staticmethod
    def resolve_places(parent, info, **kwargs):
        response = api_client.list("place")
        return json2obj(format_response(response))

    @staticmethod
    def resolve_keyword(parent, info, **kwargs):
        response = api_client.retrieve("keyword", kwargs["id"])
        return json2obj(format_response(response))

    @staticmethod
    def resolve_keywords(parent, info, **kwargs):
        response = api_client.list("keyword")
        return json2obj(format_response(response))

    @staticmethod
    def resolve_events_search(parent, info, **kwargs):
        response = api_client.search("event", kwargs["input"])
        return json2obj(format_response(response))

    @staticmethod
    def resolve_places_search(parent, info, **kwargs):
        response = api_client.search("place", kwargs["input"])
        return json2obj(format_response(response))


class Mutation:
    # TODO: Add support for graphql mutation
    pass
