from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
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


class HasUnitIdStudyGroupListFilter(admin.SimpleListFilter):
    """
    Does the instance have a user profile or not?
    List filter options: All,True (for have user profile), False (for doesn't have)
    """

    title = _("has unit id")
    parameter_name = "studygroup-has-unitid"

    def lookups(self, request, model_admin):
        return (
            (True, _("True")),
            (False, _("False")),
        )

    def queryset(self, request, queryset):

        if self.value() == "True":
            return queryset.filter(unit_id__isnull=False)
        if self.value() == "False":
            return queryset.filter(unit_id__isnull=True)


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "unit_id", "unit_name", "created_at", "group_size", "person")
    exclude = ("id",)
    inlines = (OccurrenceInline,)
    list_filter = ["created_at", HasUnitIdStudyGroupListFilter]
    search_fields = ["unit_id", "unit_name", "person"]


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
    list_display = ("id", "linked_event_id", "enrolment_time", "study_group", "status")
    readonly_fields = ("enrolment_time",)
    list_filter = ["enrolment_time", "status"]
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
    change_list_template = "admin/palvelutarjotinevent_changelist.html"
    list_display = (
        "linked_event_id",
        "organisation",
        "occurrences_count",
        "enrolment_start",
        "enrolment_end_days",
        "needed_occurrences",
        "contact_email",
    )
    list_filter = [("enrolment_start", DateFieldListFilter)]
    date_hierarchy = "enrolment_start"
    search_fields = ["linked_event_id", "organisation__name", "contact_email"]
    actions = (
        "export_event_enrolments",
        "export_event_enrolments_csv",
    )

    def occurrences_count(self, obj):
        return obj.occurrences.count()

    def export_event_enrolments(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        return HttpResponseRedirect(
            "%s?ids=%s"
            % (
                reverse("report_event_enrolments", current_app="reports"),
                ",".join(str(pk) for pk in selected),
            )
        )

    def export_event_enrolments_csv(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        return HttpResponseRedirect(
            "%s?ids=%s"
            % (
                reverse("report_event_enrolments_csv", current_app="reports"),
                ",".join(str(pk) for pk in selected),
            )
        )

    export_event_enrolments_csv.short_description = _(
        "Export organisation persons (csv)"
    )
