from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from organisations.models import Organisation, Person


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    filter_horizontal = ("persons",)
    list_display = ("name", "type")
    exclude = ("id",)


class OrganisationInline(admin.TabularInline):
    model = Organisation.persons.through


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    fields = ("user", "name", "phone_number")
    inlines = (OrganisationInline,)


class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (("UUID", {"fields": ("uuid",)}),)
    readonly_fields = ("uuid",)


admin.site.register(get_user_model(), UserAdmin)
