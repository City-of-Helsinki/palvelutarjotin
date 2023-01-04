from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter
from django.http import HttpResponseRedirect
from django.template.defaultfilters import date
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from parler.admin import TranslatableAdmin

from occurrences.models import (
    Enrolment,
    Occurrence,
    PalvelutarjotinEvent,
    StudyGroup,
    StudyLevel,
    VenueCustomData,
)
from organisations.admin import RetentionPeriodExceededListFilter
from organisations.models import EnrolleePersonalData


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
    list_display = (
        "id",
        "unit_id",
        "unit_name",
        "created_at",
        "group_size",
        "get_person",
    )
    exclude = ("id",)
    inlines = (OccurrenceInline,)
    list_filter = ["created_at", HasUnitIdStudyGroupListFilter]
    search_fields = ["unit_id", "unit_name", "person"]
    readonly_fields = ("person_deleted_at",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["unit_id"].required = False
        return form

    def get_person(self, obj):
        if obj.person_deleted_at:
            return mark_safe(
                f'<span style="color: gray">{_("Deleted")} '
                f"{date(obj.person_deleted_at)}</span>"
            )
        else:
            return obj.person

    get_person.short_description = _("person")


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
    readonly_fields = ("enrolment_time", "person_deleted_at")
    list_filter = ["enrolment_time", "status"]
    search_fields = ["occurrence__p_event__linked_event_id", "study_group__unit_name"]

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
        "get_contact_email",
    )
    list_filter = [("enrolment_start", DateFieldListFilter)]
    date_hierarchy = "enrolment_start"
    search_fields = ["linked_event_id", "organisation__name", "contact_email"]
    actions = (
        "export_event_enrolments",
        "export_event_enrolments_csv",
    )
    readonly_fields = ["contact_info_deleted_at"]

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

    def get_contact_email(self, obj):
        if obj.contact_info_deleted_at:
            return mark_safe(
                f'<span style="color: gray">{_("Deleted")} '
                f"{date(obj.contact_info_deleted_at)}</span>"
            )
        else:
            return obj.contact_email

    get_contact_email.short_description = _("contact email")


class EnrolmentInline(admin.TabularInline):
    model = Enrolment
    extra = 0
    exclude = ("person_deleted_at",)


class StudyGroupInline(admin.TabularInline):
    model = StudyGroup
    extra = 0
    exclude = ("person_deleted_at",)


@admin.register(EnrolleePersonalData)
class EnrolleePersonalDataAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "email_address",
        "language",
        "created_at",
        "updated_at",
    )
    fields = ("name", "phone_number", "email_address", "language")
    ordering = ("-created_at",)
    list_filter = [
        "created_at",
        RetentionPeriodExceededListFilter,
    ]
    search_fields = ["name", "email_address"]
    inlines = (EnrolmentInline, StudyGroupInline)
