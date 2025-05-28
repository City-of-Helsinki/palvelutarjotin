from typing import Any

from auditlog_extra.mixins import AuditlogAdminViewAccessLogMixin
from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from occurrences.models import StudyGroup
from organisations.models import Organisation, OrganisationProposal, Person, User


@admin.register(Organisation)
class OrganisationAdmin(AuditlogAdminViewAccessLogMixin, admin.ModelAdmin):
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


class OrganisationProposalAdminForm(forms.ModelForm):
    class Meta:
        model = OrganisationProposal
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["applicant"].queryset = Person.objects.all().order_by(
            "name", "-created_at"
        )
        self.fields["applicant"].label_from_instance = (
            lambda instance: f"{instance.__str__()} (id: {instance.id})"
        )


@admin.register(OrganisationProposal)
class OrganisationProposalAdmin(AuditlogAdminViewAccessLogMixin, admin.ModelAdmin):
    list_display = ("name", "applicant")
    search_fields = (
        "name",
        "applicant__name",
        "applicant__user__username",
    )
    form = OrganisationProposalAdminForm


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


class RetentionPeriodExceededListFilter(admin.SimpleListFilter):
    title = _("retention period exceeded")
    parameter_name = "retention-period-exceeded"

    def lookups(self, request, model_admin):
        return ((True, _("True")),)

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.retention_period_exceeded()


class RelatedNameDropdownFilter(RelatedDropdownFilter):
    def field_admin_ordering(self, field, request, model_admin):
        return ["name"]


class StudyGroupInline(admin.TabularInline):
    model = StudyGroup
    extra = 0
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False


class PersonAdminForm(forms.ModelForm):
    language = forms.ChoiceField(choices=settings.LANGUAGES)

    class Meta:
        model = Person
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.fields["user"]
        # Show only users without any links to a person
        user.queryset = User.objects.filter(person__isnull=True)
        if self.instance.user:
            # If an user instance is already set, add it to queryset with an union.
            user.queryset |= User.objects.filter(pk=self.instance.user.pk)
            user.initial = self.instance.user
        user.help_text = _(
            "Only the users that aren't linked to a person yet, can be selected."
        )


@admin.register(Person)
class PersonAdmin(AuditlogAdminViewAccessLogMixin, admin.ModelAdmin):
    enable_list_view_audit_logging = True
    list_display = (
        "id",
        "name",
        "user",
        "email_address",
        "created_at",
        "updated_at",
        "get_organisation_names",
        "get_study_groups",
    )
    fields = ("user", "name", "phone_number", "email_address", "language", "place_ids")
    ordering = ("-created_at",)
    inlines = (OrganisationInline, StudyGroupInline)
    list_filter = [
        "created_at",
        UserExistenceListFilter,
        ("organisations", RelatedNameDropdownFilter),
        RetentionPeriodExceededListFilter,
    ]
    search_fields = ["name", "email_address"]
    form = PersonAdminForm
    actions = (
        "export_persons",
        "export_persons_csv",
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return (
            super()
            .get_queryset(request)
            .prefetch_related("organisations")
            .prefetch_related("studygroup_set")
        )

    def get_organisation_names(self, obj):
        return ", ".join((org.name for org in obj.organisations.all()))

    get_organisation_names.short_description = _("organisations")

    def get_study_groups(self, obj):
        return ", ".join((str(group) for group in obj.studygroup_set.all()))

    get_study_groups.short_description = _("study groups")

    def export_persons(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        return HttpResponseRedirect(
            "%s?ids=%s"
            % (
                reverse("report_persons", current_app="reports"),
                ",".join(str(pk) for pk in selected),
            )
        )

    def export_persons_csv(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        return HttpResponseRedirect(
            "%s?ids=%s"
            % (
                reverse("report_persons_csv", current_app="reports"),
                ",".join(str(pk) for pk in selected),
            )
        )


class UserPersonInLine(admin.StackedInline):
    """
    UserPersonInLine is created to make a support visible and clickable
    view and navigation between user and person from an admin user change form.

    NOTE: If any of the fields are writable, users that shouldn't have
    a person instance linked to them, will get one, because when any of the
    fields in the (person) inline form are included in save submit request,
    a person instance will be created - this should be avoided, since we
    would also like to support users without persons.
    """

    model = Person
    verbose_name = _("Person")
    verbose_name_plural = _(
        "Persons (The Kultus provider model extension for the User model)"
    )
    fields = ["name", "email_address", "language"]
    readonly_fields = fields  # All fields should be readonly fields
    show_change_link = True  # show a link to a person instance
    can_delete = False  # Prevent the deletion of a person instance
    classes = ["collapse"]  # Collapsible inline form


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                self.fields[
                    "organisations"
                ].initial = self.instance.person.organisations.all()
            except Person.DoesNotExist:
                self.fields["organisations"].disabled = True

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        if user.pk and hasattr(user, "person"):
            user.person.organisations.set(self.cleaned_data["organisations"])
            self.save_m2m()

        return user


@admin.register(get_user_model())
class UserAdmin(AuditlogAdminViewAccessLogMixin, DjangoUserAdmin):
    enable_list_view_audit_logging = True
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_event_staff",
                    "organisation_proposals",
                    "organisations",
                ),
            },
        ),
        (
            _("Advanced permission settings"),
            {
                "fields": (
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
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
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_event_staff",
        "is_staff",
        "has_person",
        "uuid",
        "date_joined",
        "last_login",
    )
    list_filter = (
        "date_joined",
        "last_login",
        "is_event_staff",
        "is_staff",
        "is_admin",
        "is_superuser",
        "is_active",
    )
    readonly_fields = (
        "last_login",  # "last_login" is a nice to know, but shouldn't be editable
        "date_joined",  # "date_joined" is a nice to know, but shouldn't be editable
        "uuid",
        "ad_groups",
        "organisation_proposals",
    )
    ordering = ("-date_joined",)
    date_hierarchy = "date_joined"
    # The person link is in huge role all around the system,
    # so it would be good to show the related information InLine.
    # All the fields needs to be read_only,
    # or otherwise a missing person relation is created on (every) save and
    # sometimes it is wanted to have a user without person, e.g a pure admin user
    # or a superuser.
    inlines = (UserPersonInLine,)
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
            ) or self._has_is_event_staff_changed(form)

        user = super().save_form(request, form, change)

        # And the organisations or is_event_staff status are changed...
        if is_notifiable_changes_done:
            # And the edited user is accepted as a provider,
            # since he is an event staff member...
            if getattr(user, "is_event_staff", False):
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
        except Person.DoesNotExist:
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

    def _has_is_event_staff_changed(self, form):
        return bool("is_event_staff" in form.changed_data)

    def _notify_user_of_account_activation(self, request, form):
        user = form.instance

        # Send a mail to the accepted user
        user.person.notify_myprofile_accepted()

        # Info about the sent mail
        messages.add_message(
            request,
            messages.INFO,
            "An email is sent to the user about the organisation changes "
            + "and the profile acceptance!",
        )
