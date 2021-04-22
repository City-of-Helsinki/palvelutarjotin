from django.contrib import admin
from occurrences.models import (
    Enrolment,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    StudyLevel,
    VenueCustomData,
)
from parler.admin import TranslatableAdmin


class OccurrenceInline(admin.TabularInline):
    model = Occurrence.study_groups.through


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "group_size")
    exclude = ("id",)
    inlines = (OccurrenceInline,)


@admin.register(StudyLevel)
class StudyLevelAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "level")
    ordering = ("level",)


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "p_event",
        "start_time",
        "end_time",
        "amount_of_seats",
        "seats_taken",
        "seat_type",
        "cancelled",
        "updated_at",
    )
    exclude = ("id",)
    list_filter = ["start_time", "end_time", "seat_type", "cancelled"]
    search_fields = ["p_event__linked_event_id"]

    def linked_event_id(self, obj):
        return obj.p_event.linked_event_id


@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    list_display = ("id", "study_group", "linked_event_id", "status")
    list_display_links = ("id", "study_group")
    readonly_fields = ("enrolment_time",)
    list_filter = ["status"]
    search_fields = ["occurrence__p_event__linked_event_id", "study_group__name"]

    def linked_event_id(self, obj):
        return obj.occurrence.p_event.linked_event_id


@admin.register(VenueCustomData)
class VenueCustomDataAdmin(TranslatableAdmin):
    list_display = (
        "place_id",
        "has_clothing_storage",
        "has_snack_eating_place",
        "outdoor_activity",
        "has_toilet_nearby",
        "has_area_for_group_work",
        "has_indoor_playing_area",
        "has_outdoor_playing_area",
    )

    list_filter = [
        "has_clothing_storage",
        "has_snack_eating_place",
        "outdoor_activity",
        "has_toilet_nearby",
        "has_area_for_group_work",
        "has_indoor_playing_area",
        "has_outdoor_playing_area",
    ]

    search_fields = ["place_id"]


@admin.register(PalvelutarjotinEvent)
class PalvelutarjotinEventAdmin(admin.ModelAdmin):
    list_display = (
        "linked_event_id",
        "organisation",
        "occurrences_count",
        "enrolment_start",
        "enrolment_end_days",
        "needed_occurrences",
        "contact_email",
    )

    def occurrences_count(self, obj):
        return obj.occurrences.count()
