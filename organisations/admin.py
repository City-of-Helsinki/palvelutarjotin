from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm
from organisations.models import Organisation, Person, User


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    filter_horizontal = ("persons",)
    list_display = ("name", "type", "publisher_id")
    exclude = ("id",)


class OrganisationInline(admin.TabularInline):
    model = Organisation.persons.through


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email_address",
        "created_at",
        "updated_at",
    )
    fields = ("user", "name", "phone_number", "email_address")
    inlines = (OrganisationInline,)


class UserAdminForm(UserChangeForm):
    organisations = forms.ModelMultipleChoiceField(
        queryset=Organisation.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name="Organisations", is_stacked=False),
    )

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                self.fields[
                    "organisations"
                ].initial = self.instance.person.organisations.all()
            except Person.DoesNotExist:
                self.fields["organisations"].disabled = True

    def save(self, commit=True):
        user = super(UserAdminForm, self).save(commit=False)
        if commit:
            user.save()

        if user.pk:
            user.person.organisations.set(self.cleaned_data["organisations"])
            self.save_m2m()

        return user


class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("UUID", {"fields": ("uuid",)}),
        ("AD Groups", {"fields": ("ad_groups",)}),
        ("Organisations", {"fields": ("organisations",)}),
    )

    list_display = DjangoUserAdmin.list_display + ("date_joined",)
    list_filter = ("date_joined",) + DjangoUserAdmin.list_filter
    readonly_fields = ("uuid", "ad_groups")
    ordering = ("-date_joined",)
    form = UserAdminForm


admin.site.register(get_user_model(), UserAdmin)
