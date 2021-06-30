from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from organisations.models import Organisation, OrganisationProposal, Person, User


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    filter_horizontal = ("persons",)
    list_display = ("name", "type", "publisher_id")
    list_filter = ["type"]
    search_fields = ["name", "publisher_id"]
    exclude = ("id",)
    actions = (
        "export_organisation_persons",
        "export_organisation_persons_csv",
    )

    def export_organisation_persons(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        return HttpResponseRedirect(
            "%s?ids=%s"
            % (
                reverse("report_organisation_persons", current_app="reports"),
                ",".join(str(pk) for pk in selected),
            )
        )

    def export_organisation_persons_csv(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        return HttpResponseRedirect(
            "%s?ids=%s"
            % (
                reverse("report_organisation_persons_csv", current_app="reports"),
                ",".join(str(pk) for pk in selected),
            )
        )

    export_organisation_persons_csv.short_description = _(
        "Export organisation persons (csv)"
    )


class OrganisationInline(admin.TabularInline):
    model = Organisation.persons.through


@admin.register(OrganisationProposal)
class OrganisationProposalAdmin(admin.ModelAdmin):
    list_display = ("name", "applicant")
    search_fields = (
        "name",
        "applicant__name",
        "applicant__user__username",
    )


class UserExistenceListFilter(admin.SimpleListFilter):
    """
    Does the instance have a user profile or not?
    List filter options: All,True (for have user profile), False (for doesn't have)
    """

    title = _("has user profile")
    parameter_name = "person-has-user"

    def lookups(self, request, model_admin):
        return (
            (True, _("True")),
            (False, _("False")),
        )

    def queryset(self, request, queryset):

        if self.value() == "True":
            return queryset.filter(user__isnull=False)
        if self.value() == "False":
            return queryset.filter(user__isnull=True)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "email_address",
        "created_at",
        "updated_at",
    )
    fields = ("user", "name", "phone_number", "email_address")
    inlines = (OrganisationInline,)
    list_filter = [
        "created_at",
        UserExistenceListFilter,
    ]
    search_fields = ["name", "email_address"]


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

        if user.pk and hasattr(user, "person"):
            user.person.organisations.set(self.cleaned_data["organisations"])
            self.save_m2m()

        return user


@admin.register(get_user_model())
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("UUID", {"fields": ("uuid",)}),
        ("AD Groups", {"fields": ("ad_groups",)}),
        ("Organisations", {"fields": ("organisation_proposals", "organisations",)}),
    )
    list_display = DjangoUserAdmin.list_display + ("date_joined", "has_person")
    list_filter = ("date_joined",) + DjangoUserAdmin.list_filter
    readonly_fields = ("uuid", "ad_groups", "organisation_proposals")
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"
    form = UserAdminForm

    def has_person(self, obj):
        try:
            return bool(obj.person)
        except (Person.DoesNotExist):
            return False

    has_person.boolean = True

    def organisation_proposals(self, obj):
        if obj.person:
            organisation_proposals = obj.person.organisationproposal_set.all()
            return ", ".join([org.name for org in organisation_proposals])
        return None
