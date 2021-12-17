import logging

from django import forms
from django.contrib import admin, messages
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import ngettext_lazy
from occurrences.models import Language, StudyLevel
from reports.exceptions import EnrolmentReportCouldNotHydrateLinkedEventsData
from reports.models import EnrolmentReport

logger = logging.getLogger(__name__)


class StudyLevelFilter(admin.SimpleListFilter):
    title = _("study level")
    parameter_name = "study_level"

    def lookups(self, request, model_admin):
        study_levels = StudyLevel.objects.all()
        return [(sl.id, sl.label) for sl in study_levels]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(study_group_study_levels__contains=[self.value()])


class OccurrenceLanguageFilter(admin.SimpleListFilter):
    title = _("occurrence language")
    parameter_name = "occurrence_language"

    def lookups(self, request, model_admin):
        languages = Language.objects.all()
        return [(lng.id, lng.name) for lng in languages]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(occurrence_languages__contains=[self.value()])


class BooleanListFilterBase(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        return (
            (True, _("True")),
            (False, _("False")),
        )


class HasUnitIdStudyGroupListFilter(BooleanListFilterBase):
    title = _("has story group unit id")
    parameter_name = "studygroup-has-unitid"

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(study_group_unit_id__isnull=False)
        if self.value() == "False":
            return queryset.filter(study_group_unit_id__isnull=True)


class HasEnrolmentListFilter(BooleanListFilterBase):
    title = _("has enrolment")
    parameter_name = "has-enrolment"

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(_enrolment_id__isnull=False)
        if self.value() == "False":
            return queryset.filter(_enrolment_id__isnull=True)


class HasOccurrenceListFilter(BooleanListFilterBase):
    title = _("has occurrence")
    parameter_name = "has-occurrence"

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(_occurrence_id__isnull=False)
        if self.value() == "False":
            return queryset.filter(_occurrence_id__isnull=True)


class HasStudyGroupListFilter(BooleanListFilterBase):
    title = _("has study group")
    parameter_name = "has-study_group"

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(_study_group_id__isnull=False)
        if self.value() == "False":
            return queryset.filter(_study_group_id__isnull=True)


class IsOutOfSyncListFilter(BooleanListFilterBase):
    title = _("is out of sync with enrolment")
    parameter_name = "is-out-of-sync"

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.exclude(_enrolment__status=F("enrolment_status"))
        if self.value() == "False":
            return queryset.filter(_enrolment__status=F("enrolment_status"))


class EnrolmentReportAdminForm(forms.ModelForm):
    class Meta:
        model = EnrolmentReport
        fields = "__all__"
        # Exclude foreign keys that has an advanced and aggressive setter
        # Exclude all the array fields that contains array field,
        # because they don't have a working widget!
        exclude = [
            "_enrolment",
            "_occurrence",
            "_study_group",
            "study_group_study_levels",
            "study_group_unit_position",
            "study_group_unit_divisions",
            "occurrence_place_position",
            "occurrence_place_divisions",
            "occurrence_languages",
            "keywords",
        ]


@admin.register(EnrolmentReport)
class EnrolmentReportAdmin(admin.ModelAdmin):
    change_list_template = "reports/admin/enrolmentreport_changelist.html"
    form = EnrolmentReportAdminForm
    list_display = [
        "id",
        "created_at",
        "updated_at",
        "get_sync_status",
        "_enrolment_id",
        "_study_group_id",
        "_occurrence_id",
        "linked_event_id",
        "enrolment_time",
        "enrolment_status",
        "enrolment_start_time",
        "occurrence_start_time",
        "occurrence_end_time",
        "occurrence_place_id",
        "study_group_unit_id",
        "distance_from_unit_to_event_place",
        "study_group_amount_of_children",
        "study_group_amount_of_adult",
        "occurrence_amount_of_seats",
        "occurrence_cancelled",
        "get_study_level_labels",
        "get_occurrence_languages",
        "enrolment_externally",
        "provider",
        "publisher",
        "get_keywords",
    ]

    list_filter = [
        "updated_at",
        "enrolment_start_time",
        "enrolment_status",
        "enrolment_externally",
        IsOutOfSyncListFilter,
        HasUnitIdStudyGroupListFilter,
        StudyLevelFilter,
        OccurrenceLanguageFilter,
        "occurrence_cancelled",
        HasEnrolmentListFilter,
        HasOccurrenceListFilter,
        HasStudyGroupListFilter,
    ]
    search_fields = [
        "linked_event_id",
        "study_group_unit_id",
        "occurrence_place_id",
        "publisher",
        "provider",
        "keywords",
    ]
    date_hierarchy = "updated_at"
    actions = (
        "sync_enrolment_reports",
        "sync_enrolment_reports_with_le",
        "export_event_enrolments_csv",
    )

    def changelist_view(self, request, *args, **kwargs):
        count_missing = EnrolmentReport.objects.count_missing()
        if count_missing:
            message = ngettext_lazy(
                f"""There is {count_missing} enrolment without a report.
                Please sync to create the missing enrolment reports!""",
                f"""There are {count_missing} enrolments without a report.
                Please sync to create the missing enrolment reports!""",
                count_missing,
            )
            self.message_user(request, message, messages.WARNING)
        return super().changelist_view(request, *args, **kwargs)

    def get_sync_status(self, obj):
        if not obj._enrolment:
            return obj.enrolment_status is None
        # TODO: Cache needed? - May be too heavy to load for each
        return obj._enrolment.status == obj.enrolment_status

    get_sync_status.short_description = _("in sync with the enrolment")
    get_sync_status.boolean = True

    def get_study_level_labels(self, obj):
        return ",".join(
            [dict(enumerate(sl)).get(1, "") for sl in obj.study_group_study_levels]
        )

    get_study_level_labels.short_description = _("Study levels")

    def get_occurrence_languages(self, obj):
        return ",".join(
            [
                dict(enumerate(language)).get(1, "")
                for language in obj.occurrence_languages
            ]
        )

    get_occurrence_languages.short_description = _("Occurrence languages")

    def get_keywords(self, obj):
        return ", ".join([dict(enumerate(kw)).get(1, "") for kw in obj.keywords or []])

    get_keywords.short_description = _("Keywords")

    def __sync_enrolment_reports(
        self, request, queryset, hydrate_linkedevents_event=False
    ):
        try:
            for report in queryset:
                report._rehydrate(hydrate_linkedevents_event=hydrate_linkedevents_event)
                report.save()
        except EnrolmentReportCouldNotHydrateLinkedEventsData as e:
            self._send_error_message(request, e)
            return

        num_of_updated = queryset.count()

        if num_of_updated:
            message = ngettext_lazy(
                f"Updated {num_of_updated} enrolment report.",
                f"Updated {num_of_updated} enrolment reports.",
                num_of_updated,
            )
        else:
            message = _("The selected notifications were in sync already.")

        self.message_user(request, message, messages.SUCCESS)

    def sync_enrolment_reports(self, request, queryset):
        self.__sync_enrolment_reports(
            request, queryset, hydrate_linkedevents_event=False
        )

    sync_enrolment_reports.short_description = _(
        "Rehydrate the enrolment report instances without LinkedEvent data."
    )

    def sync_enrolment_reports_with_le(self, request, queryset):
        self.__sync_enrolment_reports(
            request, queryset, hydrate_linkedevents_event=True
        )

    sync_enrolment_reports_with_le.short_description = _(
        "Rehydrate the enrolment report instances with LinkedEvent data."
    )

    def export_event_enrolments_csv(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        return HttpResponseRedirect(
            "%s?ids=%s"
            % (
                reverse("report_enrolment_report_csv", current_app="reports"),
                ",".join(str(pk) for pk in selected),
            )
        )

    export_event_enrolments_csv.short_description = _("Export enrolment reports (csv)")

    def _send_error_message(self, request, message):
        logger.error(message)
        self.message_user(request, message, messages.ERROR)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Make all the nullable fields unrequired.
        for field in form.base_fields:
            form.base_fields[field].required = False
        return form
