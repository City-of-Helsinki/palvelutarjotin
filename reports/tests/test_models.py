import dateutil.parser
import math
import pytest
from freezegun import freeze_time

from occurrences.factories import EnrolmentFactory, StudyGroupFactory, StudyLevelFactory
from occurrences.models import Enrolment
from reports.factories import EnrolmentReportFactory
from reports.models import EnrolmentReport


@pytest.mark.django_db
def test_enrolment_report(mock_get_event_data):
    EnrolmentReportFactory()
    EnrolmentReport.objects.count() == 1


@pytest.mark.django_db
def test_enrolment_report_enrolment_hydration(mock_get_event_data, enrolment):
    report = EnrolmentReport(enrolment=enrolment)
    assert report.enrolment is not None
    assert report.study_group is not None
    assert report.occurrence is not None
    assert enrolment.occurrence.p_event.enrolment_start is not None
    assert report.enrolment_start_time is not None
    assert report.linked_event_id != ""


@pytest.mark.django_db
def test_enrolment_report_occurrence_hydration(
    mock_get_event_data_with_locations_and_keywords, occurrence
):
    report = EnrolmentReport(occurrence=occurrence)
    assert report.occurrence is not None
    assert occurrence.p_event.enrolment_start is not None
    assert report.enrolment_start_time is not None
    assert report.linked_event_id != ""


@pytest.mark.django_db
def test_get_publisher_from_occurrence(
    mock_get_event_data_with_locations_and_keywords, occurrence
):
    publisher_id = "test_hydration"
    occurrence.p_event.organisation.publisher_id = publisher_id
    report = EnrolmentReport(occurrence=occurrence)
    report.publisher == publisher_id
    report._get_publisher_id_from_occurrence() == publisher_id


@pytest.mark.django_db
def test_enrolment_report_study_group_hydration(
    mock_get_event_data_with_locations_and_keywords,
):
    study_group = StudyGroupFactory(study_levels=(StudyLevelFactory(),))
    report = EnrolmentReport(study_group=study_group)
    assert report.study_group is not None
    assert report.study_group_amount_of_children == study_group.group_size is not None
    assert report.study_group_amount_of_adult == study_group.amount_of_adult is not None
    assert [(id, label) for id, label in report.study_group_study_levels] == [
        (sl.id, sl.label) for sl in study_group.study_levels.all()
    ]


@pytest.mark.django_db
def test_enrolment_report_enrolment_rehydration_with_enrolment(
    mock_get_event_data, enrolment
):
    report = EnrolmentReport()
    report._enrolment = enrolment
    assert report.study_group is None
    assert report.occurrence is None
    report._rehydrate(hydrate_linkedevents_event=True)
    assert report.enrolment is not None
    assert report.study_group is not None
    assert report.occurrence is not None
    assert enrolment.occurrence.p_event.enrolment_start is not None
    assert report.enrolment_start_time is not None
    assert report.linked_event_id != ""
    assert report.publisher is not None
    assert report.keywords is not None


@pytest.mark.django_db
def test_enrolment_report_enrolment_rehydration_with_occurrence(
    mock_get_event_data, occurrence
):
    report = EnrolmentReport()
    report._occurrence = occurrence
    assert report.enrolment_start_time is None
    assert report.linked_event_id == ""
    assert report.publisher is None
    assert report.keywords is None
    report._rehydrate(hydrate_linkedevents_event=True)
    assert report.occurrence is not None
    assert occurrence.p_event.enrolment_start is not None
    assert report.enrolment_start_time is not None
    assert report.linked_event_id != ""
    assert report.publisher is not None
    assert report.keywords is not None


@pytest.mark.django_db
def test_enrolment_report_enrolment_rehydration(mock_get_event_data, occurrence):
    report = EnrolmentReport()
    report._occurrence = occurrence
    assert report.enrolment_start_time is None
    assert report.linked_event_id == ""
    assert report.publisher is None
    assert report.keywords is None
    report._rehydrate(hydrate_linkedevents_event=True)
    assert report.occurrence is not None
    assert occurrence.p_event.enrolment_start is not None
    assert report.enrolment_start_time is not None
    assert report.linked_event_id != ""
    assert report.publisher is not None
    assert report.keywords is not None


@pytest.mark.django_db
def test_unsynced_queryset(mock_get_event_data):
    latest_sync = "2020-01-01"

    def create_enrolment(updated_at_str):
        with freeze_time(updated_at_str):
            return EnrolmentFactory(
                status=Enrolment.STATUS_APPROVED,
            )

    enrolment1, enrolment2, enrolment3, enrolment4 = [
        create_enrolment(updated_at_str)
        for updated_at_str in [latest_sync, "2020-01-02", "2020-01-03", "2020-01-04"]
    ]

    # In sync - also sets the latest sync time to "2020-01-01"
    with freeze_time(latest_sync):
        in_sync = [
            EnrolmentReportFactory(
                updated_at=dateutil.parser.isoparse("20200101"),
                enrolment=enrolment1,
            )
        ]

    with freeze_time("2019-12-30"):
        # Not in sync, but status unchanged
        no_sync_need = [
            EnrolmentReportFactory(
                enrolment=enrolment2,
            )
        ]

        # Not in sync and status updated
        needs_sync = [
            EnrolmentReportFactory(
                enrolment=enrolment3,
            ),
            EnrolmentReportFactory(
                enrolment=enrolment4,
            ),
        ]
        for report in needs_sync:
            # Update the enrolment status gets overriden
            # by enrolment setter and it's hydration
            report.enrolment_status = Enrolment.STATUS_CANCELLED
            report.save()

    assert Enrolment.objects.filter(updated_at__gte=latest_sync).count() == 4
    assert EnrolmentReport.objects.filter(updated_at__lte=latest_sync).count() == len(
        no_sync_need
    ) + len(needs_sync)
    assert EnrolmentReport.objects.filter(updated_at__gte=latest_sync).count() == len(
        in_sync
    )
    assert EnrolmentReport.objects.unsynced().count() == len(needs_sync)


@pytest.mark.django_db
def test_create_missing(mock_get_event_data):
    enrolments = EnrolmentFactory.create_batch(10)
    with freeze_time("2019-12-30"):
        for enrolment in enrolments[:5]:
            EnrolmentReportFactory(enrolment=enrolment)
    assert EnrolmentReport.objects.all().count() == 5
    EnrolmentReport.objects.create_missing()
    assert (
        EnrolmentReport.objects.filter(
            _enrolment_id__in=[e.id for e in enrolments]
        ).count()
        == 10
    )


@pytest.mark.django_db
def test_update_unsynced(mock_get_event_data):
    enrolments = EnrolmentFactory.create_batch(10, status=Enrolment.STATUS_APPROVED)
    # All reports which are wanted to be updated, needs to be in the past
    with freeze_time("2019-12-30"):
        for enrolment in enrolments[:5]:
            EnrolmentReportFactory(enrolment=enrolment)
        for enrolment in enrolments[5:]:
            report = EnrolmentReportFactory(enrolment=enrolment)
            # enrolment_status needs to be implicitly set
            # because otherwise enrolment setter would override it
            report.enrolment_status = Enrolment.STATUS_PENDING
            report.save()
    assert EnrolmentReport.objects.filter(updated_at__lt="2019-12-31").count() == 10

    with freeze_time("2020-01-04"):
        EnrolmentReport.objects.update_unsynced()
        assert (
            EnrolmentReport.objects.filter(
                updated_at__gte="2020-01-04", enrolment_status=Enrolment.STATUS_APPROVED
            ).count()
            == 5
        )
        assert (
            EnrolmentReport.objects.filter(
                enrolment_status=Enrolment.STATUS_APPROVED
            ).count()
            == 10
        )


@pytest.mark.django_db
def test_pre_save_set_distance_from_unit_to_event_place(
    mock_get_event_data_with_locations_and_keywords,
):
    report = EnrolmentReportFactory(
        occurrence_place_position=(24.9384, 60.1699),
        study_group_unit_position=(22.2666, 60.4518),
    )
    report.refresh_from_db()
    assert report.distance_from_unit_to_event_place is not None
    assert math.isclose(report.distance_from_unit_to_event_place, 150.98)


@pytest.mark.django_db
def test_has_missing(mock_get_event_data):
    EnrolmentFactory()
    assert EnrolmentReport.objects.has_missing()


@pytest.mark.django_db
def test_count_missing(mock_get_event_data):
    EnrolmentFactory()
    assert EnrolmentReport.objects.count_missing() == 1
