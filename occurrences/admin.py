from django.contrib import admin
from occurrences.models import (
    Enrolment,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
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


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = (
        "p_event",
        "start_time",
        "end_time",
        "amount_of_seats",
        "seats_taken",
        "cancelled",
        "updated_at",
    )
    exclude = ("id",)

    def linked_event_id(self, obj):
        return obj.p_event.linked_event_id


@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    list_display = ("id", "study_group", "linked_event_id", "status")
    list_display_links = ("id", "study_group")
    readonly_fields = ("enrolment_time",)

    def linked_event_id(self, obj):
        return obj.occurrence.p_event.linked_event_id


@admin.register(VenueCustomData)
class VenueCustomDataAdmin(TranslatableAdmin):
    list_display = (
        "place_id",
        "has_clothing_storage",
        "has_snack_eating_place",
        "outdoor_activity",
    )


@admin.register(PalvelutarjotinEvent)
class PalvelutarjotinEventAdmin(admin.ModelAdmin):
    list_display = (
        "linked_event_id",
        "organisation",
        "occurrences_count",
        "enrolment_start",
        "duration",
        "enrolment_end_days",
        "needed_occurrences",
        "contact_email",
    )

    def occurrences_count(self, obj):
        return obj.occurrences.count()
