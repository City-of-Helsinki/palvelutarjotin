from datetime import datetime, timedelta
from datetime import timezone as datetime_timezone
from unittest import mock

import pytest
from auditlog.context import disable_auditlog
from auditlog.models import LogEntry
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import override_settings, TestCase
from django.test.client import RequestFactory
from django.utils.timezone import get_current_timezone
from django.views.generic import TemplateView
from freezegun import freeze_time
from graphql_relay import to_global_id
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APIClient

from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from occurrences.models import Enrolment, PalvelutarjotinEvent
from organisations.factories import OrganisationFactory, PersonFactory, UserFactory
from organisations.models import Organisation, Person
from reports.factories import EnrolmentReportFactory
from reports.models import EnrolmentReport
from reports.views import (
    EnrolmentReportListView,
    ExportReportViewMixin,
    OrganisationPersonsAdminView,
    OrganisationPersonsMixin,
    PalvelutarjotinEventEnrolmentsAdminView,
    PalvelutarjotinEventEnrolmentsMixin,
    PersonsAdminView,
)

REMOTE_ADDR = "127.0.0.1"


def local_datetime(*args, **kwargs):
    """
    Create a datetime object with the current timezone.
    """
    return datetime(*args, **kwargs, tzinfo=get_current_timezone())


class ExportReportViewMixinTest(TestCase):
    class DummyExportReportView(ExportReportViewMixin, TemplateView):
        model = PalvelutarjotinEvent

    def setUp(self):
        super().setUp()

        # Setup request and view.
        self.view = self.DummyExportReportView()

    @pytest.mark.django_db
    def test_get_queryset(self):
        (
            p_event1,
            p_event2,
            p_event3,
            p_event4,
        ) = PalvelutarjotinEventFactory.create_batch(4)
        self.view.request = RequestFactory().get(
            "/fake-path?ids=%s,%s,%s" % (p_event1.id, p_event2.id, p_event3.id)
        )
        self.assertEqual(
            set(self.view.get_queryset()), set([p_event1, p_event2, p_event3])
        )


class OrganisationPersonsMixinTest(TestCase):
    class DummyOrganisationPersonsMixinView(OrganisationPersonsMixin, TemplateView):
        model = Organisation

    def setUp(self):
        super().setUp()

        # Setup request and view.
        self.view = self.DummyOrganisationPersonsMixinView()

    @pytest.mark.django_db
    def test_get_queryset(self):
        org1, org2 = OrganisationFactory.create_batch(2)
        org3 = OrganisationFactory()
        PersonFactory.create_batch(2, organisations=[org1])
        PersonFactory.create_batch(2, organisations=[org2])
        PersonFactory.create_batch(2, organisations=[org3])
        self.view.request = RequestFactory().get(
            "/fake-path?ids=%s,%s" % (org1.id, org2.id)
        )
        self.assertEqual(set(self.view.get_queryset()), set([org1, org2]))
        persons = [
            person for org in self.view.get_queryset() for person in org.persons.all()
        ]
        self.assertEqual(len(persons), 4)


@pytest.mark.usefixtures("mock_get_event_data")
class PalvelutarjotinEventEnrolmentsMixinTest(TestCase):
    class DummyPalvelutarjotinEventEnrolmentCsvView(
        PalvelutarjotinEventEnrolmentsMixin
    ):
        model = PalvelutarjotinEvent
        max_results = 10

    def setUp(self):
        super().setUp()
        # Setup request and view.
        self.view = self.DummyPalvelutarjotinEventEnrolmentCsvView()

    def test_get_node_id_with_integer(self):
        self.assertEqual(self.view.get_node_id("1"), 1)

    def test_get_node_id_with_global_id(self):
        global_id = to_global_id("PalvelutarjotinEventNode", 1)
        self.assertEqual(self.view.get_node_id(global_id), "1")
        global_id = to_global_id("PalvelutarjotinEventNode", "asdf")
        self.assertEqual(self.view.get_node_id(global_id), "asdf")

    @pytest.mark.django_db
    @mock.patch("django.contrib.messages.add_message")
    def test_message_max_result(self, add_message):
        (
            p_event1,
            p_event2,
            p_event3,
        ) = p_events = PalvelutarjotinEventFactory.create_batch(3)
        for p_event in p_events:
            for occurrence in OccurrenceFactory.create_batch(3, p_event=p_event):
                EnrolmentFactory.create_batch(
                    3, occurrence=occurrence, status=Enrolment.STATUS_APPROVED
                )
        self.view.request = RequestFactory().get(
            "/fake-path?ids=%s,%s,%s" % (p_event1.id, p_event2.id, p_event3.id)
        )
        self.view.message_max_result(self.view.request)
        assert add_message.called

    @pytest.mark.django_db
    def test_get_queryset_without_filter(self):
        today = datetime.now(tz=datetime_timezone.utc)
        for p_event in PalvelutarjotinEventFactory.create_batch(
            3, enrolment_start=today
        ):
            occurrence = OccurrenceFactory(p_event=p_event)
            EnrolmentFactory.create_batch(
                3, occurrence=occurrence, status=Enrolment.STATUS_APPROVED
            )
        self.view.request = RequestFactory().get("/fake-path/")
        self.assertEqual(self.view.get_queryset().count(), 9)

    @pytest.mark.django_db
    def test_get_queryset_with_unapproved_enrolments(self):
        for p_event in PalvelutarjotinEventFactory.create_batch(3):
            occurrence = OccurrenceFactory(p_event=p_event)
            EnrolmentFactory.create_batch(
                3, occurrence=occurrence, status=Enrolment.STATUS_APPROVED
            )
        self.view.request = RequestFactory().get("/fake-path/")
        self.assertEqual(self.view.get_queryset().count(), 0)

    @pytest.mark.django_db
    def test_get_queryset_with_ids(self):
        (
            p_event1,
            p_event2,
            p_event3,
        ) = p_events = PalvelutarjotinEventFactory.create_batch(3)
        for p_event in p_events:
            occurrence = OccurrenceFactory(p_event=p_event)
            EnrolmentFactory.create_batch(
                3, occurrence=occurrence, status=Enrolment.STATUS_APPROVED
            )
        self.view.request = RequestFactory().get(
            "/fake-path?ids=%s,%s" % (p_event1.id, p_event2.id)
        )
        self.assertEqual(self.view.get_queryset().count(), 6)

    @pytest.mark.django_db
    def test_get_queryset_with_start_date_and_end_date(self):
        today = datetime.now(tz=datetime_timezone.utc)
        p_event1 = PalvelutarjotinEventFactory(
            enrolment_start=today - timedelta(days=3)
        )
        p_event2 = PalvelutarjotinEventFactory(
            enrolment_start=today - timedelta(days=2)
        )
        p_event3 = PalvelutarjotinEventFactory(
            enrolment_start=today - timedelta(days=1)
        )
        for p_event in [
            p_event1,
            p_event2,
            p_event3,
        ]:
            occurrence = OccurrenceFactory(p_event=p_event)
            EnrolmentFactory.create_batch(
                3, occurrence=occurrence, status=Enrolment.STATUS_APPROVED
            )
        # filtered with start
        self.view.request = RequestFactory().get(
            "/fake-path/?start=%s" % ((today - timedelta(days=2)).strftime("%Y-%m-%d"))
        )
        self.assertEqual(self.view.get_queryset().count(), 6)
        self.view.request = RequestFactory().get(
            "/fake-path/?start=%s" % ((today + timedelta(days=1)).strftime("%Y-%m-%d"))
        )
        self.assertEqual(self.view.get_queryset().count(), 0)

        # filtered with end
        self.view.request = RequestFactory().get(
            "/fake-path/?end=%s" % ((today - timedelta(days=2)).strftime("%Y-%m-%d"))
        )
        self.assertEqual(self.view.get_queryset().count(), 6)
        self.view.request = RequestFactory().get(
            "/fake-path/?end=%s" % ((today - timedelta(days=3)).strftime("%Y-%m-%d"))
        )
        self.assertEqual(self.view.get_queryset().count(), 3)

        # filtered with start and end
        self.view.request = RequestFactory().get(
            "/fake-path/?start=%s&end=%s"
            % (
                (today - timedelta(days=3)).strftime("%Y-%m-%d"),
                (today - timedelta(days=2)).strftime("%Y-%m-%d"),
            )
        )
        self.assertEqual(self.view.get_queryset().count(), 6)


@pytest.mark.usefixtures("mock_get_event_data")
class PersonsAdminViewTest(TestCase):
    def setUp(self):
        super().setUp()
        # Setup request and view.
        self.view = PersonsAdminView()

    @pytest.mark.django_db
    def test_auditlog_access_logging(self):
        PERSONS_BATCH_COUNT = 5
        user = UserFactory()
        PersonFactory.create_batch(PERSONS_BATCH_COUNT)
        self.view.request = RequestFactory().get(
            "/fake-path/", headers={"X-Forwarded-For": REMOTE_ADDR}
        )
        self.view.request.user = user
        queryset = self.view.get_queryset()
        self.assertEqual(queryset.count(), PERSONS_BATCH_COUNT)
        access_logs = LogEntry.objects.filter(action=LogEntry.Action.ACCESS)
        self.assertEqual(
            access_logs.count(),
            PERSONS_BATCH_COUNT,
        )
        access_log_entry = access_logs.first()
        self.assertEqual(access_log_entry.actor, user)
        self.assertEqual(access_log_entry.remote_addr, REMOTE_ADDR)


@pytest.mark.usefixtures("mock_get_event_data")
class OrganisationPersonsAdminViewTest(TestCase):
    def setUp(self):
        super().setUp()
        # Setup request and view.
        self.view = OrganisationPersonsAdminView()

    @pytest.mark.django_db
    def test_get_context_data(self):
        user = UserFactory()
        self.view.request = RequestFactory().get("/fake-path/")
        self.view.request.user = user
        org1, org2 = OrganisationFactory.create_batch(2)
        PersonFactory.create_batch(2, organisations=[org1])
        PersonFactory.create_batch(2, organisations=[org2])
        # Prepare initial params
        kwargs = {}
        # Launch Mixin's get_context_data
        context = self.view.get_context_data(object_list=[org1, org2], **kwargs)
        self.assertEqual(len(context["organisations"]), 2)

    @pytest.mark.django_db
    def test_auditlog_access_logging(
        self,
    ):
        ORGANISATION_BATCH_COUNT = 2
        user = UserFactory()
        org1, org2 = OrganisationFactory.create_batch(ORGANISATION_BATCH_COUNT)
        PersonFactory.create_batch(2, organisations=[org1])
        PersonFactory.create_batch(2, organisations=[org2])
        self.view.request = RequestFactory().get(
            "/fake-path/", headers={"X-Forwarded-For": REMOTE_ADDR}
        )
        self.view.request.user = user
        queryset = self.view.get_queryset()
        self.assertEqual(queryset.count(), ORGANISATION_BATCH_COUNT)
        access_logs = LogEntry.objects.filter(action=LogEntry.Action.ACCESS)
        self.assertEqual(
            access_logs.count(),
            ORGANISATION_BATCH_COUNT,
        )
        access_log_entry = access_logs.first()
        self.assertEqual(access_log_entry.actor, user)
        self.assertEqual(access_log_entry.remote_addr, REMOTE_ADDR)


@pytest.mark.usefixtures("mock_get_event_data")
class PalvelutarjotinEventEnrolmentsAdminViewTest(TestCase):
    def setUp(self):
        super().setUp()
        # Setup request and view.
        self.view = PalvelutarjotinEventEnrolmentsAdminView()

    @pytest.mark.django_db
    @override_settings(
        LINKED_EVENTS_API_CONFIG={
            "ROOT": "http://test.com",
            "API_KEY": "API_KEY",
            "DATA_SOURCE": "DATA_SOURCE",
        }
    )
    def test_get_context_data(self):
        user = UserFactory()
        self.view.request = RequestFactory().get("/fake-path/")
        self.view.request.user = user
        today = datetime.now(tz=datetime_timezone.utc)
        p_events = PalvelutarjotinEventFactory.create_batch(3, enrolment_start=today)
        for p_event in p_events:
            occurrence = OccurrenceFactory(p_event=p_event, amount_of_seats=100)
            EnrolmentFactory(
                occurrence=occurrence,
                status=Enrolment.STATUS_APPROVED,
                study_group=StudyGroupFactory(group_size=2, amount_of_adult=1),
            )
        # Prepare initial params
        kwargs = {}
        # Launch Mixin's get_context_data
        context = self.view.get_context_data(object_list=p_events, **kwargs)
        # Your checkings here
        self.assertEqual(context["linked_events_root"], "http://test.com")
        self.assertEqual(context["total_children"], 6)
        self.assertEqual(context["total_adults"], 3)
        self.assertIsNotNone(context["opts"])

    @pytest.mark.django_db
    def test_auditlog_access_logging(
        self,
    ):
        EVENT_BATCH_COUNT = 2
        ENROLMENT_BATCH_COUNT = 2
        ENROLMENT_TOTAL_COUNT = EVENT_BATCH_COUNT * ENROLMENT_BATCH_COUNT
        user = UserFactory()
        today = datetime.now(tz=datetime_timezone.utc)

        p_event1, p_event2 = PalvelutarjotinEventFactory.create_batch(
            EVENT_BATCH_COUNT, enrolment_start=today
        )
        EnrolmentFactory.create_batch(
            ENROLMENT_BATCH_COUNT,
            occurrence__p_event=p_event1,
            status=Enrolment.STATUS_APPROVED,
        )
        EnrolmentFactory.create_batch(
            ENROLMENT_BATCH_COUNT,
            occurrence__p_event=p_event2,
            status=Enrolment.STATUS_APPROVED,
        )
        self.view.request = RequestFactory().get(
            "/fake-path/", headers={"X-Forwarded-For": REMOTE_ADDR}
        )
        self.view.request.user = user
        self.assertEqual(PalvelutarjotinEvent.objects.count(), EVENT_BATCH_COUNT)
        self.assertEqual(Enrolment.objects.count(), ENROLMENT_TOTAL_COUNT)
        kwargs = {}
        self.view.get_context_data(object_list=[p_event1, p_event2], **kwargs)
        access_logs = LogEntry.objects.filter(action=LogEntry.Action.ACCESS)
        self.assertEqual(
            access_logs.count(),
            ENROLMENT_TOTAL_COUNT,
        )
        access_log_entry = access_logs.first()
        self.assertEqual(access_log_entry.actor, user)
        self.assertEqual(access_log_entry.remote_addr, REMOTE_ADDR)


@pytest.mark.usefixtures("mock_get_event_data")
class PersonsCsvViewTest(TestCase):
    @pytest.mark.django_db
    def test_export_persons_csv_data(
        self,
    ):
        PERSONS_BATCH_COUNT = 2
        person_1, person_2 = PersonFactory.create_batch(PERSONS_BATCH_COUNT)

        admin_user = UserFactory(is_staff=True)
        user = UserFactory(is_staff=False)

        user_api_client = APIClient()
        user_api_client.force_authenticate(user=user)

        staff_api_client = APIClient()
        staff_api_client.force_authenticate(user=admin_user)

        response = user_api_client.get(
            "/reports/persons/csv/?ids={}".format(person_1.id)
        )
        # Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = staff_api_client.get(
            "/reports/persons/csv/?ids={}".format(person_1.id)
        )
        assert response.status_code == status.HTTP_200_OK

        self.assertContains(response, person_1.name)
        self.assertContains(response, person_1.email_address)

        self.assertNotContains(response, person_2.name)
        self.assertNotContains(response, person_2.email_address)

    @pytest.mark.django_db
    def test_auditlog_access_logging(
        self,
    ):
        PERSON_BATCH_COUNT = 2
        admin_user = UserFactory(is_staff=True)
        PersonFactory.create_batch(
            PERSON_BATCH_COUNT,
        )
        staff_api_client = APIClient()
        staff_api_client.force_authenticate(user=admin_user)
        staff_api_client.get(
            "/reports/persons/csv/",
            headers={"X-Forwarded-For": REMOTE_ADDR},
        )

        self.assertEqual(Person.objects.count(), PERSON_BATCH_COUNT)
        access_logs = LogEntry.objects.filter(
            action=LogEntry.Action.ACCESS, actor=admin_user
        )
        self.assertEqual(
            access_logs.count(),
            PERSON_BATCH_COUNT,
        )
        access_log_entry = access_logs.first()
        self.assertEqual(access_log_entry.actor, admin_user)
        self.assertEqual(access_log_entry.remote_addr, REMOTE_ADDR)


@pytest.mark.usefixtures("mock_get_event_data")
class OrganisationPersonsCsvViewTest(TestCase):
    def test_export_organisation_csv_data(self):
        org1, org2 = OrganisationFactory.create_batch(2)
        person_1 = PersonFactory.create(organisations=[org1])
        person_2 = PersonFactory.create(organisations=[org2])

        admin_user = UserFactory(is_staff=True)
        user = UserFactory(is_staff=False)

        user_api_client = APIClient()
        user_api_client.force_authenticate(user=user)

        staff_api_client = APIClient()
        staff_api_client.force_authenticate(user=admin_user)

        response = user_api_client.get(
            "/reports/organisation/persons/csv/?ids={}".format(org1.id)
        )
        # Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = staff_api_client.get(
            "/reports/organisation/persons/csv/?ids={}".format(org1.id)
        )
        assert response.status_code == status.HTTP_200_OK

        self.assertContains(response, org1.name)
        self.assertContains(response, person_1.name)

        self.assertNotContains(response, org2.name)
        self.assertNotContains(response, person_2.name)

    @pytest.mark.django_db
    def test_auditlog_access_logging(
        self,
    ):
        ORGANISATION_BATCH_COUNT = 2
        PERSON_BATCH_COUNT = 2
        PERSON_TOTAL_COUNT = ORGANISATION_BATCH_COUNT * PERSON_BATCH_COUNT
        admin_user = UserFactory(is_staff=True)
        org1, org2 = OrganisationFactory.create_batch(ORGANISATION_BATCH_COUNT)
        PersonFactory.create_batch(
            PERSON_BATCH_COUNT,
            organisations=[org1],
        )
        PersonFactory.create_batch(
            PERSON_BATCH_COUNT,
            organisations=[org2],
        )
        staff_api_client = APIClient()
        staff_api_client.force_authenticate(user=admin_user)
        staff_api_client.get(
            "/reports/organisation/persons/csv/",
            headers={"X-Forwarded-For": REMOTE_ADDR},
        )

        self.assertEqual(Organisation.objects.count(), ORGANISATION_BATCH_COUNT)
        self.assertEqual(Person.objects.count(), PERSON_TOTAL_COUNT)
        access_logs = LogEntry.objects.filter(
            action=LogEntry.Action.ACCESS, actor=admin_user
        )
        self.assertEqual(
            access_logs.count(),
            PERSON_TOTAL_COUNT,
        )
        access_log_entry = access_logs.first()
        self.assertEqual(access_log_entry.actor, admin_user)
        self.assertEqual(access_log_entry.remote_addr, REMOTE_ADDR)


@pytest.mark.usefixtures("mock_get_event_or_place_data")
class PalvelutarjotinEventEnrolmentsTest(TestCase):
    @pytest.mark.django_db
    def test_export_enrolment_csv_data(self):
        today = datetime.now(tz=datetime_timezone.utc)
        p_events = PalvelutarjotinEventFactory.create_batch(3, enrolment_start=today)
        for p_event in p_events:
            occurrence = OccurrenceFactory(p_event=p_event, amount_of_seats=100)
            EnrolmentFactory(
                occurrence=occurrence,
                status=Enrolment.STATUS_APPROVED,
                study_group=StudyGroupFactory(group_size=2, amount_of_adult=1),
            )

        admin_user = UserFactory(is_staff=True)
        user = UserFactory(is_staff=False)

        user_api_client = APIClient()
        user_api_client.force_authenticate(user=user)

        staff_api_client = APIClient()
        staff_api_client.force_authenticate(user=admin_user)

        response = user_api_client.get(
            "/reports/palvelutarjotinevent/enrolments/csv/?ids={}".format(
                p_events[0].id
            )
        )
        # Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = staff_api_client.get(
            "/reports/palvelutarjotinevent/enrolments/csv/?ids={}".format(
                p_events[0].id
            )
        )
        assert response.status_code == status.HTTP_200_OK

        self.assertContains(response, p_events[0].linked_event_id)
        # comes from LE place data
        self.assertContains(response, "Sellon kirjasto")

        self.assertNotContains(response, p_events[1].linked_event_id)
        self.assertNotContains(response, p_events[2].linked_event_id)

    @pytest.mark.django_db
    def test_auditlog_access_logging(
        self,
    ):
        EVENT_BATCH_COUNT = 2
        ENROLMENT_BATCH_COUNT = 2
        ENROLMENT_TOTAL_COUNT = EVENT_BATCH_COUNT * ENROLMENT_BATCH_COUNT
        today = datetime.now(tz=datetime_timezone.utc)
        admin_user = UserFactory(is_staff=True)
        p_event1, p_event2 = PalvelutarjotinEventFactory.create_batch(
            EVENT_BATCH_COUNT, enrolment_start=today
        )
        EnrolmentFactory.create_batch(
            ENROLMENT_BATCH_COUNT,
            occurrence__p_event=p_event1,
            status=Enrolment.STATUS_APPROVED,
        )
        EnrolmentFactory.create_batch(
            ENROLMENT_BATCH_COUNT,
            occurrence__p_event=p_event2,
            status=Enrolment.STATUS_APPROVED,
        )
        staff_api_client = APIClient()
        staff_api_client.force_authenticate(user=admin_user)
        staff_api_client.get(
            "/reports/palvelutarjotinevent/enrolments/csv/",
            headers={"X-Forwarded-For": REMOTE_ADDR},
        )
        self.assertEqual(PalvelutarjotinEvent.objects.count(), EVENT_BATCH_COUNT)
        self.assertEqual(Enrolment.objects.count(), ENROLMENT_TOTAL_COUNT)
        access_logs = LogEntry.objects.filter(
            action=LogEntry.Action.ACCESS, actor=admin_user
        )
        self.assertEqual(
            access_logs.count(),
            ENROLMENT_TOTAL_COUNT,
        )
        access_log_entry = access_logs.first()
        self.assertEqual(access_log_entry.actor, admin_user)
        self.assertEqual(access_log_entry.remote_addr, REMOTE_ADDR)


@pytest.mark.django_db
@pytest.mark.usefixtures("mock_get_event_data")
class EnrolmentReportListViewTest(TestCase):
    TEST_TIMEZONE_SETTINGS = {
        "USE_TZ": True,
        "TIME_ZONE": "Europe/Helsinki",
    }

    def setUp(self):
        self.user = UserFactory()
        content_type = ContentType.objects.get_for_model(EnrolmentReport)
        self.view_permission = Permission.objects.get(
            codename="view_enrolmentreport", content_type=content_type
        )
        self.user.user_permissions.add(self.view_permission)
        self.view = EnrolmentReportListView
        self.user_api_client = APIClient()
        self.root = "/reports/enrolmentreport/"

    def _authenticate(self):
        self.user_api_client.force_authenticate(user=self.user)

    def _goto_reports(self, query_params: str = ""):
        return self.user_api_client.get(self.root + query_params)

    def test_permissionless_user_cannot_access_enrolment_reports(self):
        response = self._goto_reports()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_all_enrolment_reports_are_in_single_page(self):
        # FIXME: slow
        EnrolmentReportFactory.create_batch(60)
        self._authenticate()
        response = self._goto_reports()
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 60

    # FIXME: make the test work with updated_at and created_at
    # @parameterized.expand(["updated_at", "created_at", "id"])
    @parameterized.expand(["id"])
    def test_order_by_param(self, param):
        reports = EnrolmentReportFactory.create_batch(5)
        self._authenticate()
        # Ascending
        response = self._goto_reports(f"?order_by={param}")
        assert [e["id"] for e in response.json()] == [getattr(r, "id") for r in reports]
        # Descending
        response = self._goto_reports(f"?order_by=-{param}")
        assert [e["id"] for e in response.json()] == list(
            reversed([getattr(r, "id") for r in reports])
        )

    def test_filtering_with_enrolment_status_from_enrolment(self):
        # EnrolmentReport's enrolment_status value is read enrolment.status here
        EnrolmentReportFactory(
            enrolment=EnrolmentFactory(status=Enrolment.STATUS_APPROVED)
        )
        EnrolmentReportFactory(
            enrolment=EnrolmentFactory(status=Enrolment.STATUS_APPROVED)
        )
        EnrolmentReportFactory(
            enrolment=EnrolmentFactory(status=Enrolment.STATUS_PENDING)
        )
        assert EnrolmentReport.objects.count() == 3
        assert (
            EnrolmentReport.objects.filter(
                enrolment_status=Enrolment.STATUS_APPROVED
            ).count()
            == 2
        )
        assert (
            EnrolmentReport.objects.filter(
                enrolment_status=Enrolment.STATUS_PENDING
            ).count()
            == 1
        )
        self._authenticate()
        response = self._goto_reports(f"?enrolment_status={Enrolment.STATUS_APPROVED}")
        assert len(response.json()) == 2
        response = self._goto_reports(f"?enrolment_status={Enrolment.STATUS_PENDING}")
        assert len(response.json()) == 1

    def test_filtering_with_overridden_enrolment_status_from_enrolment(self):
        # EnrolmentReport.enrolment_status value is overridden by enrolment.status here
        # so basically values put into EnrolmentReport.enrolment_status are irrelevant
        # as only the values in enrolment.status are used
        EnrolmentReportFactory(
            enrolment=EnrolmentFactory(status=Enrolment.STATUS_PENDING),
            enrolment_status=Enrolment.STATUS_APPROVED,  # NOT USED!
        )
        EnrolmentReportFactory(
            enrolment=EnrolmentFactory(status=Enrolment.STATUS_PENDING),
            enrolment_status=Enrolment.STATUS_APPROVED,  # NOT USED!
        )
        EnrolmentReportFactory(
            enrolment=EnrolmentFactory(status=Enrolment.STATUS_CANCELLED),
            enrolment_status=Enrolment.STATUS_APPROVED,  # NOT USED!
        )
        assert EnrolmentReport.objects.count() == 3
        assert (
            EnrolmentReport.objects.filter(
                enrolment_status=Enrolment.STATUS_PENDING
            ).count()
            == 2
        )
        assert (
            EnrolmentReport.objects.filter(
                enrolment_status=Enrolment.STATUS_CANCELLED
            ).count()
            == 1
        )
        self._authenticate()
        response = self._goto_reports(f"?enrolment_status={Enrolment.STATUS_PENDING}")
        assert len(response.json()) == 2
        response = self._goto_reports(f"?enrolment_status={Enrolment.STATUS_CANCELLED}")
        assert len(response.json()) == 1

    @parameterized.expand(
        [
            ("enrolment_start_time__gte", [3, 2, 1, 0]),
            ("enrolment_start_time__gt", [2, 1, 0, 0]),
            ("enrolment_start_time__lte", [1, 2, 3, 3]),
            ("enrolment_start_time__lt", [0, 1, 2, 3]),
            ("updated_at__gte", [3, 2, 1, 0]),
            ("updated_at__gt", [2, 1, 0, 0]),
            ("updated_at__lte", [1, 2, 3, 3]),
            ("updated_at__lt", [0, 1, 2, 3]),
            ("created_at__gte", [3, 2, 1, 0]),
            ("created_at__gt", [2, 1, 0, 0]),
            ("created_at__lte", [1, 2, 3, 3]),
            ("created_at__lt", [0, 1, 2, 3]),
        ]
    )
    @override_settings(**TEST_TIMEZONE_SETTINGS)
    def test_filtering_with_timestamps(self, param, expected_response_counts):
        datetimes = [
            local_datetime(2020, 1, 1),
            local_datetime(2020, 1, 2),
            local_datetime(2020, 1, 3),
        ]
        for obj_datetime in datetimes:
            with freeze_time(obj_datetime):
                p_event = PalvelutarjotinEventFactory(enrolment_start=obj_datetime)
                occurrence = OccurrenceFactory(p_event=p_event)
                enrolment = EnrolmentFactory(
                    occurrence=occurrence, status=Enrolment.STATUS_APPROVED
                )
                EnrolmentReportFactory(
                    enrolment=enrolment, enrolment_start_time=obj_datetime
                )
        self._authenticate()
        count1, count2, count3, count4 = expected_response_counts
        response = self._goto_reports(f"?{param}=2020-01-01")
        assert len(response.json()) == count1
        response = self._goto_reports(f"?{param}=2020-01-02")
        assert len(response.json()) == count2
        response = self._goto_reports(f"?{param}=2020-01-03")
        assert len(response.json()) == count3
        response = self._goto_reports(f"?{param}=2020-01-04")
        assert len(response.json()) == count4

    @override_settings(**TEST_TIMEZONE_SETTINGS)
    def test_filtering_with_combination(self):
        with freeze_time(local_datetime(2020, 1, 1)):
            EnrolmentReportFactory()
        with freeze_time(local_datetime(2020, 1, 2)):
            EnrolmentReportFactory()
        with freeze_time(local_datetime(2020, 1, 3)):
            EnrolmentReportFactory()
        with freeze_time(local_datetime(2020, 1, 4)):
            EnrolmentReportFactory()
        self._authenticate()
        response = self._goto_reports(
            "?created_at__gte=2020-01-02&created_at__lte=2020-01-03"
        )
        assert len(response.json()) == 2

    @parameterized.expand(
        [(5, 5), (20, 20)]
    )  # currently there is no paginator, so everything should be included.
    def test_accesslog_written_from_every_result(self, batch_size, page_size):
        """
        Test that an access log entry is written for each object in the list view
        result.

        This test verifies that when a list view is accessed, a corresponding
        LogEntry with action ACCESS is created for each object in the returned
        list. It utilizes parameterized testing to cover different batch sizes,
        ensuring that the access log is correctly generated regardless of the
        number of objects.

        Args:
            batch_size (int): The number of EnrolmentReport objects to create.
            page_size (int): The expected number of objects returned by the list view,
                and therefore the expected number of created access log entries.
        """
        with disable_auditlog():
            EnrolmentReportFactory.create_batch(batch_size)
        self._authenticate()
        response = self._goto_reports("?page_size=%s" % page_size)
        assert EnrolmentReportListView.pagination_class is None
        assert EnrolmentReport.objects.count() == batch_size
        assert len(response.json()) == page_size
        assert (
            LogEntry.objects.filter(
                actor=self.user, action=LogEntry.Action.ACCESS
            ).count()
            == page_size
        )
