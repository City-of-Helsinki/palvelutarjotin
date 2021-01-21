from django.contrib import admin

from .models import VerificationToken


def verification_token_username(obj):
    return obj.user.username


verification_token_username.short_description = "Username"


@admin.register(VerificationToken)
class VerificationTokenAdmin(admin.ModelAdmin):

    list_display = (
        "key",
        "verification_type",
        "content_type",
        "object_id",
        verification_token_username,
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
        "user__username__exact",
        "email__exact",
    )
    ordering = (
        "created_at",
        "expiry_date",
    )
