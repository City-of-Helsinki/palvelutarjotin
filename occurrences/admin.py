from django.contrib import admin
from occurrences.models import (
    Enrolment,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    VenueCustomData,
)
from parler.admin import TranslatableAdmin


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "group_size")
    exclude = ("id",)


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = (
        "place_id",
        "created_at",
        "updated_at",
    )
    exclude = ("id",)


@admin.register(Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    readonly_fields = ("enrolment_time",)


@admin.register(VenueCustomData)
class VenueCustomDataAdmin(TranslatableAdmin):
    list_display = ("place_id",)


@admin.register(PalvelutarjotinEvent)
class PalvelutarjotinEventAdmin(admin.ModelAdmin):
    list_display = ("linked_event_id", "enrolment_start", "enrolment_end_days")
