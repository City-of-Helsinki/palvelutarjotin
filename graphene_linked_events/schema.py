import json
import logging
import math
from types import SimpleNamespace

import requests
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from graphene import (
    ID,
    Boolean,
    Enum,
    Field,
    Float,
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

from common.utils import (
    get_editable_obj_from_global_id,
    get_obj_from_global_id,
    map_enums_to_values_in_kwargs,
    update_object_with_translations,
)
from graphene_linked_events.utils import (
    api_client,
    bbox_for_coordinates,
    format_request,
    format_response,
    get_keyword_set_by_id,
    json2obj,
    json_object_hook,
    retrieve_linked_events_data,
)
from occurrences.event_api_services import prepare_published_event_data
from occurrences.models import PalvelutarjotinEvent, VenueCustomData
from organisations.decorators import event_staff_member_required
from organisations.models import Organisation, Person
from palvelutarjotin.exceptions import (
    DataValidationError,
    MissingMantatoryInformationError,
    ObjectDoesNotExistError,
    UploadImageSizeExceededError,
)
from reports.services import get_place_location_data

logger = logging.getLogger(__name__)

PublicationStatusEnum = Enum(
    "PublicationStatus",
    [(s[0].upper(), s[0]) for s in PalvelutarjotinEvent.PUBLICATION_STATUSES],
)

KeywordSetEnum = Enum(
    "KeywordSetType", [(s.upper(), s) for s in settings.KEYWORD_SET_ID_MAPPING.keys()]
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
    ocd_id = String(description="Open Civic Data ID")
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


def _get_event_keyword_sets(event, keyword_set_id):
    kw_set = get_keyword_set_by_id(keyword_set_id)
    return [
        kw
        for kw in kw_set.keywords
        if kw.id in list(map(lambda x: x.id, event.keywords))
    ]


class Event(IdObject):
    id = String(required=True)
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
    enrolment_start_time = String()
    enrolment_end_time = String()
    maximum_attendee_capacity = Int()
    minimum_attendee_capacity = Int()
    remaining_attendee_capacity = Int()
    name = Field(LocalisedObject, required=True)
    localization_extra_info = Field(LocalisedObject)
    short_description = Field(LocalisedObject, required=True)
    provider = Field(LocalisedObject)
    info_url = Field(LocalisedObject)
    provider_contact_info = String()
    description = Field(LocalisedObject, required=True)
    p_event = Field("occurrences.schema.PalvelutarjotinEventNode", required=True)
    venue = Field("occurrences.schema.VenueNode")
    publication_status = String()
    categories = NonNull(
        List(NonNull(Keyword)),
        description="Only use this field in single event query for "
        "best performance. This field only work if "
        "`keywords` is included in the query argument",
    )
    additional_criteria = NonNull(
        List(NonNull(Keyword)),
        description="Only use this field in single event query for "
        "best performance. This field only work if "
        "`keywords` is included in the query argument",
    )

    activities = NonNull(
        List(NonNull(Keyword)),
        description="Only use this field in single event query for "
        "best performance. This field only work if "
        "`keywords` is included in the query argument",
    )

    def resolve_p_event(self, info, **kwargs):
        # Avoid needless palvelutarjotin event queries.
        if hasattr(self, "p_event"):
            return self.p_event

        try:
            return PalvelutarjotinEvent.objects.prefetch_related("occurrences").get(
                linked_event_id=self.id
            )
        except PalvelutarjotinEvent.DoesNotExist:
            return None

    def resolve_venue(self, info, **kwargs):
        if hasattr(self.location, "id") and self.location.id:
            try:
                return VenueCustomData.objects.get(pk=self.location.id)
            except VenueCustomData.DoesNotExist:
                pass
        return None

    def resolve_categories(self, info, **kwargs):
        return _get_event_keyword_sets(
            self, settings.KEYWORD_SET_ID_MAPPING["CATEGORY"]
        )

    def resolve_additional_criteria(self, info, **kwargs):
        # FIXME: Remove this after client switched to use activities
        return _get_event_keyword_sets(
            self, settings.KEYWORD_SET_ID_MAPPING["ADDITIONAL_CRITERIA"]
        )

    def resolve_activities(self, info, **kwargs):
        return _get_event_keyword_sets(
            self, settings.KEYWORD_SET_ID_MAPPING["ACTIVITIES"]
        )


class Meta(ObjectType):
    count = Int()
    next = String()
    previous = String()


class Response(ObjectType):
    meta = Field(Meta, required=True)


class PaginatedType(ObjectType):
    total_count = Int()
    page_size = Int()
    page = Int()
    pages = Int()
    has_next_page = Boolean()
    has_previous_page = Boolean()


class PaginatedTypeResponse(ObjectType):
    class Meta:
        description = _(
            "The custom `PageInfo` type, containing data necessary to"
            " paginate this connection."
        )

    page_info = Field(PaginatedType, required=True)


class EventListResponse(Response):
    data = NonNull(List(NonNull(Event)))


class EventListPaginatedTypeResponse(PaginatedTypeResponse):
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
        division=List(String),
        end=String(),
        include=List(
            String,
            description=_(
                "Include the complete data from related resources in the current "
                "response e.g. keywords or location."
            ),
        ),
        in_language=String(),
        is_free=Boolean(),
        keyword=List(String),
        keyword_and=List(String),
        keyword_not=List(String),
        keyword_or_set1=List(
            String,
            description="Search for a combination of keywords as in "
            "(yso:p1235 OR yso:p1947) AND (yso:p14004 OR yso:p11185) "
            "use keyword_OR_setX parameter, where X is a number. "
            "Can be used for example with "
            "target group, category, activity or additional criteria keywords.",
        ),
        keyword_or_set2=List(
            String,
            description="Search for a combination of keywords as in "
            "(yso:p1235 OR yso:p1947) AND (yso:p14004 OR yso:p11185) "
            "use keyword_OR_setX parameter, where X is a number. "
            "Can be used for example with "
            "target group, category, activity or additional criteria keywords.",
        ),
        keyword_or_set3=List(
            String,
            description="Search for a combination of keywords as in "
            "(yso:p1235 OR yso:p1947) AND (yso:p14004 OR yso:p11185) "
            "use keyword_OR_setX parameter, where X is a number. "
            "Can be used for example with "
            "target group, category, activity or additional criteria keywords.",
        ),
        all_ongoing_and=List(String),
        all_ongoing_or=List(String),
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
        nearby_place_id=ID(description=_("Get nearby events for the given place.")),
        nearby_distance=Float(
            default_value=3,
            description=_(
                "Distance (km) to the bounding box corner, which will be used to limit "
                "the search area for nearby events."
            ),
        ),
    )
    event = Field(Event, id=ID(required=True), include=List(String))
    upcoming_events = Field(
        EventListPaginatedTypeResponse,
        page=Int(default_value=1),
        page_size=Int(default_value=10),
        include=List(
            String,
            description=_(
                "Include the complete data from related resources in the current "
                "response e.g. keywords or location."
            ),
        ),
        description=_("Get upcoming events sorted by the next occurrence."),
    )
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

    popular_kultus_keywords = Field(
        KeywordListResponse,
        description=_("Keywords related to Kultus ordered by the number of events"),
        amount=Int(description=_("Maximum number of results to return")),
        show_all_keywords=Boolean(
            description=_("Include keywords without events"), default_value=False
        ),
    )

    keyword_set = Field(KeywordSet, set_type=KeywordSetEnum(required=True))

    # TODO: Add support for start-end filter
    events_search = Field(
        EventSearchListResponse, input=String(required=True), include=List(String)
    )
    places_search = Field(
        PlaceSearchListResponse, input=String(required=True), include=List(String)
    )

    @staticmethod
    def _test_events_p_event_relations(events_json):
        """
        Prune events that does not have a PalvelutarjotinEvent in our database.
        """

        events = json.loads(events_json, object_hook=lambda d: SimpleNamespace(**d))

        # Get related palvelutarjotin events
        p_events = PalvelutarjotinEvent.objects.prefetch_related("occurrences").filter(
            linked_event_id__in=[e.id for e in events.data]
        )

        # Prune a list of events which have a link to a palvelutarjotin event
        tested_events = [
            e for e in events.data if e.id in [p.linked_event_id for p in p_events]
        ]

        # Attach prefetched palvelutarjotin events to event instances
        for t in tested_events:
            t.p_event = next((p for p in p_events if p.linked_event_id == t.id), None)

        # Create a (new) mutated immutable X-object of the event results.
        return json_object_hook(
            # NOTE: LinkedEvents paginates the results, but Kultus API filters
            # the paginated sets. This leads to a situation where the events
            # count in meta data, easily does not match with the fact.
            # If events.meta is used, the count is bigger than the filtered result.
            # If a length of tested_events is used,
            # it works only for unpaginated results. Events.meta is better!
            {"meta": events.meta, "data": tested_events}
        )

    @staticmethod
    def resolve_event(parent, info, **kwargs):
        event_id = kwargs.pop("id")
        is_event_staff = getattr(info.context.user, "is_event_staff", False)
        return retrieve_linked_events_data(
            "event", event_id, params=kwargs, is_event_staff=is_event_staff
        )

    @staticmethod
    def resolve_events(parent, info, **kwargs):  # noqa: C901
        def _handle_publisher(**kwargs):
            organisation_global_id = kwargs.pop("organisation_id", None)
            if organisation_global_id:
                # Filter events by organisation id
                organisation = get_obj_from_global_id(
                    info, organisation_global_id, Organisation
                )
                kwargs["publisher"] = organisation.publisher_id
            return kwargs

        def _handle_keywords(**kwargs):
            if kwargs.get("keyword_and"):
                kwargs["keyword_AND"] = kwargs.pop("keyword_and")
            if kwargs.get("keyword_or_set1"):
                kwargs["keyword_OR_set1"] = kwargs.pop("keyword_or_set1")
            if kwargs.get("keyword_or_set2"):
                kwargs["keyword_OR_set2"] = kwargs.pop("keyword_or_set2")
            if kwargs.get("keyword_or_set3"):
                kwargs["keyword_OR_set3"] = kwargs.pop("keyword_or_set3")
            if kwargs.get("keyword_not"):
                kwargs["keyword!"] = kwargs.pop("keyword_not")
            return kwargs

        def _handle_text(**kwargs):
            if kwargs.get("all_ongoing_and"):
                kwargs["all_ongoing_AND"] = kwargs.pop("all_ongoing_and")
            if kwargs.get("all_ongoing_or"):
                kwargs["all_ongoing_OR"] = kwargs.pop("all_ongoing_or")
            return kwargs

        def _handle_nearby_filter(**kwargs):
            # Nearby events from a place
            nearby_distance_km = kwargs.pop("nearby_distance")
            if kwargs.get("nearby_place_id"):
                place_id = kwargs.pop("nearby_place_id")
                coordinates, _ = get_place_location_data(place_id)

                if not coordinates:
                    raise DataValidationError(
                        f"Cannot determine coordinates for place {place_id}."
                    )
                bbox = bbox_for_coordinates(
                    coordinates[0], coordinates[1], nearby_distance_km
                )
                kwargs["bbox"] = bbox
            return kwargs

        # Some arguments in LinkedEvent are not fully supported in graphene argument
        kwargs = _handle_nearby_filter(
            **_handle_text(**_handle_keywords(**_handle_publisher(**kwargs)))
        )

        response = api_client.list(
            "event",
            filter_list=kwargs,
            is_event_staff=getattr(info.context.user, "is_event_staff", False),
        )
        response.raise_for_status()
        events_json = format_response(response)
        return Query._test_events_p_event_relations(events_json)

    @staticmethod
    def resolve_upcoming_events(parent, info, **kwargs):
        """Return a list of upcoming events based on occurrence start time."""
        page = kwargs.get("page")
        page_size = kwargs.get("page_size")
        include = kwargs.get("include")

        start = page_size * (page - 1)
        end = page * page_size

        p_events = (
            PalvelutarjotinEvent.objects.with_next_occurrence_start_time()
            .filter(next_occurrence_start_time__isnull=False)
            .order_by("next_occurrence_start_time")
            .prefetch_related("occurrences")
        )
        count = p_events.count()
        linked_event_ids = [p_event.linked_event_id for p_event in p_events[start:end]]

        if linked_event_ids:
            params = {"ids": linked_event_ids}
            if include:
                params["include"] = include

            response = api_client.list("event", filter_list=params)

            events = json.loads(
                format_response(response), object_hook=lambda d: SimpleNamespace(**d)
            )
            events = [e for e in events.data if e.id in linked_event_ids]
            events.sort(key=lambda x: linked_event_ids.index(x.id))

            for event in events:
                event.p_event = next(
                    (p for p in p_events if p.linked_event_id == event.id), None
                )
        else:
            events = []

        return {
            "data": events,
            "page_info": {
                "total_count": count,
                "page": page if count > 0 else 0,
                "pages": math.ceil(count / page_size),
                "page_size": page_size,
                "has_next_page": count > end,
                "has_previous_page": start >= page_size,
            },
        }

    @staticmethod
    def resolve_place(parent, info, **kwargs):
        place_id = kwargs["id"]
        if not place_id:
            return None
        return retrieve_linked_events_data("place", place_id)

    @staticmethod
    def resolve_places(parent, info, **kwargs):
        response = api_client.list("place", filter_list=kwargs)
        response.raise_for_status()
        return json2obj(format_response(response))

    @staticmethod
    def resolve_keyword(parent, info, **kwargs):
        keyword_id = kwargs["id"]
        if not keyword_id:
            return None
        response = api_client.retrieve("keyword", keyword_id)
        response.raise_for_status()
        return json2obj(format_response(response))

    @staticmethod
    def resolve_keywords(parent, info, **kwargs):
        response = api_client.list("keyword", filter_list=kwargs)
        response.raise_for_status()
        return json2obj(format_response(response))

    @staticmethod
    def resolve_popular_kultus_keywords(parent, info, **kwargs):
        """Returns Kultus related keywords ordered by popularity.

        Fetches keywords for keyword sets: category, additional criteria and
        target group. Keywords are ordered in descending order by the number of events
        and returned.
        """
        amount = kwargs.get("amount")
        show_all_keywords = kwargs.get("show_all_keywords")
        set_ids = [
            settings.KEYWORD_SET_ID_MAPPING["CATEGORY"],
            settings.KEYWORD_SET_ID_MAPPING["ADDITIONAL_CRITERIA"],
            settings.KEYWORD_SET_ID_MAPPING["TARGET_GROUP"],
        ]
        keywords = {}

        # Graceful degradation: Continue processing remaining keyword sets
        # even if one API request fails due to timeout or other errors.
        # This prevents the entire query from failing when the LinkedEvents API
        # is slow or experiencing issues.
        for set_id in set_ids:
            try:
                response = api_client.retrieve(
                    "keyword_set", set_id, params={"include": "keywords"}
                )
                response = json2obj(format_response(response))
                for keyword in response.keywords:
                    if show_all_keywords or keyword.n_events > 0:
                        keywords[keyword.id] = keyword
            except (
                requests.exceptions.ConnectTimeout,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException,
            ) as e:
                # Log the error but continue processing other keyword sets
                logger.warning(
                    f"Failed to fetch keyword set '{set_id}' from LinkedEvents API: {e}"
                )
                continue

        unique_keywords = sorted(
            keywords.values(), key=lambda x: x.n_events, reverse=True
        )
        if amount:
            unique_keywords = unique_keywords[:amount]

        return {"data": unique_keywords, "meta": {"count": len(unique_keywords)}}

    @staticmethod
    def resolve_keyword_set(parent, info, **kwargs):
        set_type = kwargs["set_type"]
        keyword_set_id = settings.KEYWORD_SET_ID_MAPPING.get(set_type.value)
        response = api_client.retrieve(
            "keyword_set", keyword_set_id, params={"include": "keywords"}
        )
        response.raise_for_status()
        return json2obj(format_response(response))

    @staticmethod
    def resolve_image(parent, info, **kwargs):
        image_id = kwargs["id"]
        if not image_id:
            return None
        response = api_client.retrieve("image", image_id)
        response.raise_for_status()
        return json2obj(format_response(response))

    @staticmethod
    def resolve_images(parent, info, **kwargs):
        response = api_client.list("image", filter_list=kwargs)
        response.raise_for_status()
        return json2obj(format_response(response))

    @staticmethod
    def resolve_events_search(parent, info, **kwargs):
        search_params = {"type": "event", **kwargs}
        response = api_client.search(search_params=search_params)
        response.raise_for_status()
        return json2obj(format_response(response))

    @staticmethod
    def resolve_places_search(parent, info, **kwargs):
        search_params = {"type": "place", **kwargs}
        response = api_client.search(search_params=search_params)
        response.raise_for_status()
        return json2obj(format_response(response))


class EventMutationResponse(ObjectType):
    status_code = Int(required=True)
    body = Field(Event)
    result_text = String()


class IdObjectInput(InputObjectType):
    internal_id = String()


class EventMutationInput(InputObjectType):
    location = IdObjectInput()
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
    enrolment_start_time = String()
    enrolment_end_time = String()
    maximum_attendee_capacity = Int()
    minimum_attendee_capacity = Int()
    remaining_attendee_capacity = Int()
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
    is_queueing_allowed = Boolean()


class AddEventMutationInput(EventMutationInput):
    draft = Boolean(
        description="Set to `true` to save event as draft version, when draft is true, "
        "event data validation will be skipped",
        default_value=False,
    )
    start_time = String(required=True)
    p_event = InputField(
        "occurrences.schema.PalvelutarjotinEventInput",
        required=True,
        description="Palvelutarjotin event data",
    )


class UpdateEventMutationInput(EventMutationInput):
    id = String(required=True)
    start_time = String(required=True)
    p_event = InputField(
        "occurrences.schema.PalvelutarjotinEventInput",
        description="Palvelutarjotin event data",
    )
    draft = Boolean(
        description="Set to `true` to save event as draft version, when draft is true, "
        "event data validation will be skipped",
        default_value=False,
    )


class PublishEventMutationInput(EventMutationInput):
    id = String(required=True)
    p_event = InputField(
        "occurrences.schema.PalvelutarjotinEventInput",
        description="Palvelutarjotin event data",
    )


def validate_p_event_data(p_event_data):
    # By default auto_acceptance is False
    if p_event_data["needed_occurrences"] > 1 and not p_event_data.get(
        "auto_acceptance", False
    ):
        raise DataValidationError(
            "Cannot create manual approval for multi-occurrences enrolment event"
        )


class AddEventMutation(Mutation):
    class Arguments:
        event = AddEventMutationInput()

    response = Field(EventMutationResponse)

    @event_staff_member_required
    @transaction.atomic
    @map_enums_to_values_in_kwargs
    def mutate(self, info, **kwargs):
        # Format to JSON POST body
        p_event_data = kwargs["event"].pop("p_event")
        validate_p_event_data(p_event_data)

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
        if not organisation.publisher_id or not str(organisation.publisher_id).strip():
            raise MissingMantatoryInformationError("Missing/invalid publisher_id")
        kwargs["event"]["publisher"] = organisation.publisher_id
        if kwargs["event"]["draft"]:
            kwargs["event"]["publication_status"] = (
                PalvelutarjotinEvent.PUBLICATION_STATUS_DRAFT
            )

        body = format_request(kwargs["event"])
        # TODO: proper validation if necessary
        result = api_client.create("event", body)
        event_obj = json2obj(format_response(result))
        if result.status_code == 201:
            # Create palvelutarjotin event if event created successful
            try:
                AddEventMutation._create_p_event(event_obj, organisation, p_event_data)
            except Exception:
                logger.exception(
                    "An error raised while creating PalvelutarjotinEvent "
                    "after the event was created to the LinkedEvents API, "
                    "so the event was left one sided."
                )
                logger.info(
                    "Deleting the (one sided) event from the LinkedEvents API. "
                    f"id: {event_obj.id}. organisation: {organisation.id}"
                )
                api_client.delete("event", event_obj.id)
                raise

        response = EventMutationResponse(
            status_code=result.status_code, body=event_obj, result_text=result.text
        )
        return AddEventMutation(response=response)

    def _create_p_event(self, organisation, p_event_data) -> PalvelutarjotinEvent:
        p_event_data["linked_event_id"] = self.id
        p_event_data["organisation_id"] = organisation.id
        translations = p_event_data.pop("translations", None)
        p_event, _ = PalvelutarjotinEvent.objects.get_or_create(**p_event_data)
        if translations:
            p_event.create_or_update_translations(translations)
        return p_event


class UpdateEventMutation(Mutation):
    class Arguments:
        event = UpdateEventMutationInput()

    response = Field(EventMutationResponse)

    @event_staff_member_required
    @transaction.atomic
    @map_enums_to_values_in_kwargs
    def mutate(self, info, **kwargs):
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
            # Compare to the current p_event.auto_acceptance if p_event update data
            # doesn't include auto_acceptance
            if p_event_data["needed_occurrences"] > 1 and not p_event_data.get(
                "auto_acceptance", p_event.auto_acceptance
            ):
                raise DataValidationError(
                    "Cannot create manual approval for multi-occurrences enrolment "
                    "event"
                )
        except PalvelutarjotinEvent.DoesNotExist:
            raise PermissionDenied(
                f"User does not have permission to edit this "
                f"{PalvelutarjotinEvent.__name__}"
            )

        if not organisation.publisher_id or not str(organisation.publisher_id).strip():
            raise MissingMantatoryInformationError("Missing/invalid publisher_id")
        kwargs["event"]["publisher"] = organisation.publisher_id

        if kwargs["event"].get("draft", False):
            kwargs["event"]["publication_status"] = (
                PalvelutarjotinEvent.PUBLICATION_STATUS_DRAFT
            )

        body = format_request(kwargs["event"])
        # TODO: proper validation if necessary
        result = api_client.update("event", event_id, body)
        if result.status_code == 200 and p_event_data:
            update_object_with_translations(p_event, p_event_data)
        response = EventMutationResponse(
            status_code=result.status_code,
            body=json2obj(format_response(result)),
            result_text=result.text,
        )
        return UpdateEventMutation(response=response)


class PublishEventMutation(UpdateEventMutation):
    class Arguments:
        event = PublishEventMutationInput()

    response = Field(EventMutationResponse)

    @event_staff_member_required
    @transaction.atomic
    @map_enums_to_values_in_kwargs
    def mutate(self, info, **kwargs):
        event_id = kwargs["event"].get("id")
        try:
            p_event: PalvelutarjotinEvent = PalvelutarjotinEvent.objects.get(
                linked_event_id=event_id
            )
            kwargs["event"].update(prepare_published_event_data(p_event))
        except PalvelutarjotinEvent.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        # Publish event is actually update event, reuse UpdateEventMutation
        response = UpdateEventMutation.mutate(self, info, **kwargs).response
        return PublishEventMutation(response=response)


class UnpublishEventMutation(UpdateEventMutation):
    class Arguments:
        event = PublishEventMutationInput()

    response = Field(EventMutationResponse)

    @event_staff_member_required
    @transaction.atomic
    @map_enums_to_values_in_kwargs
    def mutate(self, info, **kwargs):
        try:
            kwargs["event"].update(
                {"publication_status": PalvelutarjotinEvent.PUBLICATION_STATUS_DRAFT}
            )
        except PalvelutarjotinEvent.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        # Unpublish event is actually update event, reuse UpdateEventMutation
        response = UpdateEventMutation.mutate(self, info, **kwargs).response
        return UnpublishEventMutation(response=response)


class DeleteEventMutation(Mutation):
    class Arguments:
        event_id = String(required=True)

    response = Field(EventMutationResponse)

    @event_staff_member_required
    @map_enums_to_values_in_kwargs
    def mutate(self, info, **kwargs):
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
        "https://github.com/jaydenseric/graphql-multipart"
        "-request-spec"
    )


class UpdateImageMutationInput(UploadImageMutationInput):
    id = String(required=True)


class ImageMutationResponse(ObjectType):
    status_code = Int(required=True)
    body = Field(Image)
    result_text = String()


def _validate_image_upload(image):
    if image.size > settings.MAX_UPLOAD_SIZE:
        raise UploadImageSizeExceededError(
            f"Upload file size cannot be greater than {settings.MAX_UPLOAD_SIZE} bytes"
        )


class UploadImageMutation(Mutation):
    class Arguments:
        image = UploadImageMutationInput()

    response = Field(ImageMutationResponse)

    @event_staff_member_required
    @map_enums_to_values_in_kwargs
    def mutate(self, info, **kwargs):
        image = kwargs["image"].pop("image")
        _validate_image_upload(image)
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

    @event_staff_member_required
    @map_enums_to_values_in_kwargs
    def mutate(self, info, **kwargs):
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

    @event_staff_member_required
    @map_enums_to_values_in_kwargs
    def mutate(self, info, **kwargs):
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
