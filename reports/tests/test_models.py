import dateutil.parser
import pytest
from freezegun import freeze_time
from occurrences.factories import EnrolmentFactory, StudyGroupFactory, StudyLevelFactory
from occurrences.models import Enrolment
from reports.factories import EnrolmentReportFactory
from reports.models import EnrolmentReport


@pytest.mark.django_db
def test_enrolment_report(snapshot, mock_get_event_data):
    report = EnrolmentReportFactory()
    EnrolmentReport.objects.count() == 1
    snapshot.assert_match(report.__dict__)


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
def test_enrolment_report_occurrence_hydration(mock_get_event_data, occurrence):
    report = EnrolmentReport(occurrence=occurrence)
    assert report.occurrence is not None
    assert occurrence.p_event.enrolment_start is not None
    assert report.enrolment_start_time is not None
    assert report.linked_event_id != ""


@pytest.mark.django_db
def test_enrolment_report_study_group_hydration(mock_get_event_data):
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
            return EnrolmentFactory(status=Enrolment.STATUS_APPROVED,)

    enrolment1, enrolment2, enrolment3, enrolment4 = [
        create_enrolment(updated_at_str)
        for updated_at_str in [latest_sync, "2020-01-02", "2020-01-03", "2020-01-04"]
    ]

    # In sync - also sets the latest sync time to "2020-01-01"
    with freeze_time(latest_sync):
        in_sync = [
            EnrolmentReportFactory(
                updated_at=dateutil.parser.isoparse("20200101"), enrolment=enrolment1,
            )
        ]

    with freeze_time("2019-12-30"):
        # Not in sync, but status unchanged
        no_sync_need = [EnrolmentReportFactory(enrolment=enrolment2,)]

        # Not in sync and status updated
        needs_sync = [
            EnrolmentReportFactory(enrolment=enrolment3,),
            EnrolmentReportFactory(enrolment=enrolment4,),
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
