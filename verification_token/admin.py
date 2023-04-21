from django.contrib import admin

from .models import VerificationToken


def verification_token_person_name(obj):
    if obj.person is not None:
        return obj.person.name
    return "-"


verification_token_person_name.short_description = "Name"


@admin.register(VerificationToken)
class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "verification_type",
        "content_type",
        "object_id",
        verification_token_person_name,
        "email",
        "created_at",
        "expiry_date",
        "is_active",
    )
    list_display_links = ("key",)
    list_filter = (
        "created_at",
        "is_active",
        "verification_type",
    )
    search_fields = (
        "key__exact",
        "content_type__model__exact",
        "object_id__exact",
        "person__name__exact",
        "email__exact",
    )
    ordering = (
        "created_at",
        "expiry_date",
    )
