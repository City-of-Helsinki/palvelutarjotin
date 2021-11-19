import logging
from datetime import datetime
from typing import List, Optional, Union

import occurrences.models as occurrences_models
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from occurrences.event_api_services import fetch_event_as_json
from reports.exceptions import EnrolmentReportCouldNotHydrateLinkedEventsData
from reports.utils import haversine

from common.models import TimestampedModel

logger = logging.getLogger(__name__)


class EnrolmentQuerySet(models.QuerySet):
    def unsynced(
        self, sync_from: datetime = None
    ) -> Union[models.QuerySet, List[occurrences_models.Enrolment]]:
        """Get a list of enrolments which are updated after latest report updates."""
        sync_from = sync_from or UnsyncedQuerySet.latest_sync(self)
        if sync_from:
            return occurrences_models.Enrolment.objects.filter(
                updated_at__gte=sync_from
            )
        return occurrences_models.Enrolment.objects.all()

    def missing(
        self, sync_from: datetime = None
    ) -> Union[models.QuerySet, List[occurrences_models.Enrolment]]:
        """Get a list of enrolments which are missing from EnrolmentReport db-table."""
        enrolments = EnrolmentQuerySet.unsynced(self, sync_from=sync_from)
        reports_enrolment_ids = self.filter(
            _enrolment_id__in=[e.id for e in enrolments]
        ).values_list("_enrolment_id", flat=True)
        return enrolments.exclude(id__in=reports_enrolment_ids)


class UnsyncedQuerySet(models.QuerySet):
    def latest_sync(self) -> Optional[datetime]:
        """Returns latest updated_at, which represents the date of the last sync made"""
        return self.aggregate(models.Max("updated_at"))["updated_at__max"]

    def unsynced(self):
        """
        Query unsynced enrolment report instances:
        Enrolment report is not in sync when it's related enrolment instance
        has an updated_at -field value greater than
        report instances updated_at -field value.
        """
        # Even if the enrolment instance has updated,
        # we do not want to update it's related enrolment report instance,
        # until the status of enrolment has changed.
        enrolment_ids_with_statuses = list(
            {"_enrolment_id": id, "enrolment_status": status}
            for id, status in EnrolmentQuerySet.unsynced(self).values_list(
                "id", "status"
            )
        )
        separator = ":"
        return (
            # Filter all reports that are related to enrolments
            self.filter(
                _enrolment_id__in=[
                    entry["_enrolment_id"] for entry in enrolment_ids_with_statuses
                ]
            )
            # Exclude from the queryset all the report instances
            # that are in the enrolment_ids_with_statuses list
            # by using the annotated concat-field
            .annotate(
                # Annotate a new field that concatenates enrolment id and status
                enrolment_id_status=models.functions.Concat(
                    "_enrolment_id",
                    models.Value(separator),
                    "enrolment_status",
                    output_field=models.CharField(),
                ),
            ).exclude(
                enrolment_id_status__in=[
                    "{}{}{}".format(
                        entry["_enrolment_id"], separator, entry["enrolment_status"]
                    )
                    for entry in enrolment_ids_with_statuses
                ]
            )
        )


class EnrolmentReportManager(models.Manager):
    def get_queryset(self):
        return UnsyncedQuerySet(self.model, using=self._db)

    def latest_sync(self):
        """Returns latest updated_at, which represents the date of the last sync made"""
        return self.get_queryset().latest_sync()

    def unsynced(self, sync_from: datetime = None):
        """Query unsynced enrolment report instances"""
        return self.get_queryset().unsynced()

    def create_missing(self, sync_from: datetime = None):
        """Create missing enrolment report instances."""
        enrolments = self.model.enrolment_objects.missing(sync_from=sync_from)
        return self.bulk_create(
            [EnrolmentReport(enrolment=enrolment) for enrolment in enrolments]
        )

    def update_unsynced(
        self, hydrate_linkedevents_event=False, sync_from: datetime = None
    ):
        """Sync existing unsynced enrolment report instances."""
        # TODO: Do we need to update every field,
        # or would it be ok to use bulk_update or queryset.update()?
        reports = self.unsynced(sync_from=sync_from)
        for report in reports:
            report._rehydrate(hydrate_linkedevents_event=hydrate_linkedevents_event)
            report.save()
        return reports


class EnrolmentReport(TimestampedModel):
    """
    Enrolment report model is used to offer some exportable data related to enrolments.
    It stores the information about enrolments and their study groups,
    the coordinates of the group unit position and the coordinates of
    the event position to calculate the distance to event,
    the event data like time frame of the event and te publisher,
    capacity information, event keywords, etc.
    """

    """
    Study group
    - Store the foreign key to fetch all data
    - If the foreign key integrity is gone,
    keep some information so the data is still available for reports:
        1. Group sizes: Kids and adults
        2. Study levels
    - Store the unit position (coordinates) and divisions to normalise the data.
    Place data must be fetched from LinkedEvents API
    (or from other service like the servicemap API)
    """
    _study_group = models.ForeignKey(
        occurrences_models.StudyGroup,
        on_delete=models.SET_NULL,
        null=True,
        db_column="study_group_id",
    )
    study_group_unit_id = models.CharField(
        max_length=255, verbose_name=_("study group's unit id"), null=True
    )
    study_group_amount_of_children = models.PositiveSmallIntegerField(
        verbose_name=_("amount of the children in the study group")
    )
    study_group_amount_of_adult = models.PositiveSmallIntegerField(
        verbose_name=_("amount of the adults in the study group"), default=0
    )
    study_group_study_levels = ArrayField(
        # ArrayField Size 2: Study level id, translated name
        ArrayField(models.CharField(max_length=255), size=2),
        verbose_name=_("study levels of the study group"),
    )
    # The position of the (unit) place from LinkedEvents API
    study_group_unit_position = ArrayField(
        ArrayField(models.DecimalField(max_digits=9, decimal_places=6), size=2),
        null=True,
        verbose_name=_("coordinates of the study group unit"),
    )
    # The divisions of the (unit) place from LinkedEvents API
    study_group_unit_divisions = ArrayField(
        models.CharField(max_length=200),
        verbose_name=_("study group unit divisions"),
        help_text=_("Open Civic Data identifiers"),
        null=True,
    )

    """
    Enrolment
    - Store the foreign key to fetch all data
    - If the foreign key integrity is gone,
    keep some information so the data is still available for reports:
        1. enrolment time
        2. enrolment status
    - Enrolment status is also used to check whether or not
    the db row should be updated.
    """
    _enrolment = models.ForeignKey(
        occurrences_models.Enrolment,
        on_delete=models.SET_NULL,
        null=True,
        db_column="enrolment_id",
    )
    enrolment_time = models.DateTimeField(verbose_name=_("enrolment time"))
    enrolment_status = models.CharField(
        max_length=255, verbose_name=_("enrolment status")
    )

    """
    Occurrence
    - Store the foreign key to fetch all data
    - If the foreign key integrity is gone,
    keep some information so the data is still available for reports:
        1. Amount of the seats
        2. cancelled status
    - Store the occurrence languages
    - Store the event position (coordinates) and divisions to normalise the data.
    Place data must be fetched from LinkedEvents API
    (or from other service like the servicemap API)
    """
    _occurrence = models.ForeignKey(
        occurrences_models.Occurrence,
        on_delete=models.SET_NULL,
        null=True,
        db_column="occurrence_id",
    )
    # The position of the (event) place from LinkedEvents API
    occurrence_place_position = ArrayField(
        ArrayField(models.DecimalField(max_digits=9, decimal_places=6), size=2),
        verbose_name=_("coordinates of the event occurrence place"),
        null=True,
    )
    # The divisions of the (event) place from LinkedEvents API
    occurrence_place_divisions = ArrayField(
        models.CharField(max_length=200),
        verbose_name=_("divisions of the occurrence place"),
        help_text=_("Open Civic Data identifiers"),
        null=True,
    )
    occurrence_languages = ArrayField(
        # ArrayField Size 2: Language id, translated name
        ArrayField(models.CharField(max_length=255), size=2),
        verbose_name=_("languages of the occurrence"),
    )
    occurrence_cancelled = models.BooleanField(
        verbose_name=_("cancelled status of the occurrence")
    )
    occurrence_amount_of_seats = models.PositiveSmallIntegerField(
        verbose_name=_("amount of the seats in the occurrence")
    )

    occurrence_start_time = models.DateTimeField(
        verbose_name=_("occurrence start time")
    )
    occurrence_end_time = models.DateTimeField(verbose_name=_("occurrence end time"))

    """
    PalvelutarjotinEvent
    - If the foreign key integrity is gone,
    keep some information so the data is still available for reports:
        1. Enrolment start time
        2. LinkedEvent id
    - Store the status of the type of the enrolment
    """
    linked_event_id = models.CharField(
        max_length=255, verbose_name=_("linked event id")
    )
    enrolment_start_time = models.DateTimeField(
        verbose_name=_("enrolment start time"), null=True
    )
    # enrolment_externally tells if the
    # PalvelutarjotinEvent.external_enrolment_url is filled
    enrolment_externally = models.BooleanField(
        verbose_name=_("external enrolments"), default=False
    )

    """
    LinkedEvents Event information
    """
    provider = models.CharField(verbose_name=_("provider"), max_length=512, null=True)
    publisher = models.CharField(
        max_length=255,
        help_text=_("a primary name of the publisher, e.g. a legally recognized name"),
        null=True,
    )
    keywords = ArrayField(
        # ArrayField Size 2: id, translated name
        ArrayField(models.CharField(max_length=255), size=2),
        verbose_name=_("keywords"),
        null=True,
    )

    """
    Distance
    """
    distance_from_unit_to_event_place = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name=_("distance from unit to event place"),
        null=True,
    )

    objects = EnrolmentReportManager()
    enrolment_objects = EnrolmentQuerySet.as_manager()

    @property
    def study_group_group_size(self):
        return self.study_group_amount_of_children

    @study_group_group_size.setter
    def study_group_group_size(self, value):
        self.study_group_amount_of_children = value

    def __pre_save_set_distance_from_unit_to_event_place(self):
        """
        Calculate the distance between
        the study group unit and the event occurrence place.
        """
        if self.occurrence_place_position and self.study_group_unit_position:
            self.distance_from_unit_to_event_place = haversine(
                self.occurrence_place_position[0],
                self.occurrence_place_position[1],
                self.study_group_unit_position[0],
                self.study_group_unit_position[1],
            )
        else:
            self.distance_from_unit_to_event_place = None

    def save(self, *args, **kwargs):
        self.__pre_save_set_distance_from_unit_to_event_place()
        super().save(*args, **kwargs)

    def _rehydrate(self, hydrate_linkedevents_event=False):
        try:
            # enrolment setter hydrates everything
            if getattr(self, "enrolment"):
                # Trigger the setter
                self.enrolment = getattr(self, "enrolment")
            # If enrolment instance is not available,
            # hydrate with occurrence setter is the 2nd best thing
            elif getattr(self, "occurrence"):
                # Trigger the setter
                self.occurrence = getattr(self, "occurrence")
            # Hydrate Event data from LinkedEvents API
            if hydrate_linkedevents_event:
                self._hydrate_linkedevents_event()
        except AttributeError:
            pass

    @property
    def study_group(self):
        try:
            return self._study_group
        except occurrences_models.StudyGroup.DoesNotExist:
            return None

    @study_group.setter
    def study_group(self, obj: occurrences_models.StudyGroup):
        self._study_group = obj
        self.study_group_unit_id = obj.unit_id
        # self.study_group_unit_position = TODO
        # self.study_group_unit_divisions = TODO
        self.study_group_amount_of_children = obj.group_size
        self.study_group_amount_of_adult = obj.amount_of_adult
        self.study_group_study_levels = (
            [(lvl.id, lvl.label) for lvl in obj.study_levels.all()]
            if obj.id and obj.study_levels.exists()
            else []
        )

    @property
    def enrolment(self):
        try:
            return self._enrolment
        except occurrences_models.Enrolment.DoesNotExist:
            return None

    @enrolment.setter
    def enrolment(
        self, obj: occurrences_models.Enrolment,
    ):
        self._enrolment = obj
        self.enrolment_time = obj.enrolment_time
        self.enrolment_status = obj.status

        # Set related
        self.occurrence = obj.occurrence
        self.study_group = obj.study_group

    @property
    def occurrence(self):
        try:
            return self._occurrence
        except occurrences_models.Occurrence.DoesNotExist:
            return None

    @occurrence.setter
    def occurrence(self, obj: occurrences_models.Occurrence):
        self._occurrence = obj
        # self.occurrence_place_position = TODO
        # self.occurrence_place_divisions = TODO
        self.occurrence_languages = (
            [(lng.id, lng.name) for lng in obj.languages.all()]
            if obj.id and obj.languages.exists()
            else []
        )
        self.occurrence_cancelled = obj.cancelled
        self.occurrence_amount_of_seats = obj.amount_of_seats
        self.occurrence_start_time = obj.start_time
        self.occurrence_end_time = obj.end_time

        self._set_palvelutarjotin_event(obj.p_event)

    def _set_palvelutarjotin_event(self, obj: occurrences_models.PalvelutarjotinEvent):
        self.linked_event_id = getattr(obj, "linked_event_id", None)
        self.enrolment_start_time = getattr(obj, "enrolment_start", None)
        self.enrolment_externally = bool(getattr(obj, "external_enrolment_url", None))

        # Populate the events data from LinkedEvents API
        # self._hydrate_linkedevents_event()

    def _hydrate_linkedevents_event(self):
        try:
            event = fetch_event_as_json(self.linked_event_id, includes=["keywords"])
            self.provider = event["provider"]
            self.publisher = event["publisher"]
            self.keywords = (
                [
                    (kw["id"], kw.get("name", {"en": ""})["en"])
                    for kw in event["keywords"]
                ]
                if event["keywords"]
                else []
            )
        except Exception:
            raise EnrolmentReportCouldNotHydrateLinkedEventsData(
                "Could not rehydrate Linked Events data!"
            )
