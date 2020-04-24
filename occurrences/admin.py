from django.contrib import admin
from occurrences.models import Enrolment, Occurrence, StudyGroup, VenueCustomData
from parler.admin import TranslatableAdmin


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "group_size")
    exclude = ("id",)


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = (
        "linked_event_id",
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


# class UserAdmin(DjangoUserAdmin):
#     fieldsets = DjangoUserAdmin.fieldsets + (("UUID", {"fields": ("uuid",)}),)
#     readonly_fields = ("uuid",)
#
#
# admin.site.register(get_user_model(), UserAdmin)
