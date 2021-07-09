from django import forms
from django.contrib import admin, messages
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
    ordering = ("-created_at",)
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
        help_text=_(
            "Select organisations to link them with the user's person relation. "
            + "The organisations selection is disabled "
            + "when the user is not linked to any person instance."
        ),
    )

    class Meta:
        model = User
        fields = "__all__"
        help_texts = {
            "is_staff": _(
                "Gives the user the permissions to be a provider "
                + "and create and edit the events. "
                + "Designates whether the user can log into this admin site."
            ),
            "is_admin": _(
                "Designates whether the user can administrate the providers users. "
                + "Admins also receives some administrative emails."
            ),
        }

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
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_admin",
                    "organisation_proposals",
                    "organisations",
                ),
            },
        ),
        (
            _("Advanced permission settings"),
            {
                "fields": ("is_superuser", "groups", "user_permissions",),
                "classes": ["collapse in"],
            },
        ),
        (
            _("Other information"),
            {
                "fields": ("last_login", "date_joined", "uuid", "ad_groups"),
                "classes": ["collapse in"],
            },
        ),
    )
    list_display = DjangoUserAdmin.list_display + ("date_joined", "has_person",)
    list_filter = ("date_joined", "is_staff", "is_admin", "is_superuser", "is_active")

    readonly_fields = (
        "last_login",  # "last_login" is a nice to know, but shouldn't be editable
        "date_joined",  # "date_joined" is a nice to know, but shouldn't be editable
        "uuid",
        "ad_groups",
        "organisation_proposals",
    )
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"
    form = UserAdminForm

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        Overridden so the request could be combined with the model instance save
        and we could write a message about a mail is being sent.
        """

        original_user = form.instance
        is_notifiable_changes_done = False

        # When user is linked to a person...
        if self.has_person(original_user):
            is_notifiable_changes_done = self._has_organisations_changed(
                original_user.person, form
            ) or self._has_is_staff_changed(form)

        user = super(UserAdmin, self).save_form(request, form, change)

        # And the organisations or is_staff status are changed...
        if is_notifiable_changes_done:
            # And the edited user is accepted as a provider,
            # since he is a staff member...
            if user.is_staff:
                # And he is linked to some organisations...
                if user.person.organisations.count() > 0:
                    # And the user instance is different than the current user..
                    if user.id != request.user.id:
                        self._notify_user_of_account_activation(request, form)

        # Return the return value of the original save_form -method.
        return user

    def get_readonly_fields(self, request, obj=None):
        """
        Staff (not superusers) should not manage perms of Users.
        """
        readonly_fields = super(UserAdmin, self).get_readonly_fields(request, obj)
        if not request.user.has_perm("organisations.can_administrate_user_permissions"):
            readonly_fields += (
                "username",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        return readonly_fields

    def has_person(self, obj):
        try:
            return bool(obj.person)
        except (Person.DoesNotExist):
            return False

    has_person.boolean = True

    def organisation_proposals(self, obj):
        if obj.person:
            organisation_proposals = obj.person.organisationproposal_set.all().order_by(
                "name"
            )
            return ", ".join([org.name for org in organisation_proposals])
        return None

    def _has_organisations_changed(self, person, form):
        return (
            bool(
                sorted(list(person.organisations.all().values_list("id", flat=True)))
                != sorted([org.id for org in form.cleaned_data["organisations"]])
            )
            if person
            else False
        )

    def _has_is_staff_changed(self, form):
        return bool("is_staff" in form.changed_data)

    def _notify_user_of_account_activation(self, request, form):

        user = form.instance

        # Send a mail to the accepted user
        user.person.notify_myprofile_accepted()

        # Info about the sent mail
        messages.add_message(
            request, messages.INFO, "Email is sent to an user about the organisation",
        )
