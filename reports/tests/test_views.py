import pytest
from datetime import datetime, timedelta
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import override_settings, TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from django.views.generic import TemplateView
from freezegun import freeze_time
from graphql_relay.node.node import to_global_id
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock

from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from occurrences.models import Enrolment, PalvelutarjotinEvent
from organisations.factories import OrganisationFactory, PersonFactory, UserFactory
from organisations.models import Organisation
from reports.factories import EnrolmentReportFactory
from reports.models import EnrolmentReport
from reports.views import (
    EnrolmentReportListView,
    ExportReportViewMixin,
    OrganisationPersonsAdminView,
    OrganisationPersonsMixin,
    PalvelutarjotinEventEnrolmentsAdminView,
    PalvelutarjotinEventEnrolmentsMixin,
)


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
        today = datetime.now(tz=timezone.utc)
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
        today = datetime.now(tz=timezone.utc)
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
class OrganisationPersonsAdminViewTest(TestCase):
    def setUp(self):
        super().setUp()
        # Setup request and view.
        self.view = OrganisationPersonsAdminView()

    @pytest.mark.django_db
    def test_get_context_data(self):
        self.view.request = RequestFactory().get("/fake-path/")
        org1, org2 = OrganisationFactory.create_batch(2)
        PersonFactory.create_batch(2, organisations=[org1])
        PersonFactory.create_batch(2, organisations=[org2])
        # Prepare initial params
        kwargs = {}
        # Launch Mixin's get_context_data
        context = self.view.get_context_data(object_list=[org1, org2], **kwargs)
        self.assertEqual(len(context["organisations"]), 2)


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
        self.view.request = RequestFactory().get("/fake-path/")
        today = datetime.now(tz=timezone.utc)
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


@pytest.mark.usefixtures("mock_get_event_or_place_data")
class PalvelutarjotinEventEnrolmentsTest(TestCase):
    @pytest.mark.django_db
    def test_export_enrolment_csv_data(self):
        today = datetime.now(tz=timezone.utc)
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
@pytest.mark.usefixtures("mock_get_event_data")
class EnrolmentReportListViewTest(TestCase):
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
        len(response.json()) == 60

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

    def test_filtering_with_enrolment_status(self):
        EnrolmentReportFactory(enrolment_status=Enrolment.STATUS_APPROVED)
        EnrolmentReportFactory(enrolment_status=Enrolment.STATUS_APPROVED)
        EnrolmentReportFactory(enrolment_status=Enrolment.STATUS_PENDING)
        self._authenticate()
        response = self._goto_reports(f"?enrolment_status={Enrolment.STATUS_APPROVED}")
        len(response.json()) == 2
        response = self._goto_reports(f"?enrolment_status={Enrolment.STATUS_PENDING}")
        len(response.json()) == 1

    @parameterized.expand(
        [
            "updated_at__gte",
            "updated_at__lte",
            "created_at__gte",
            "created_at__lte",
            "enrolment_start_time__gte",
            "enrolment_start_time__lte",
        ]
    )
    def test_filtering_with_timestamps(self, param):
        with freeze_time("2020-01-01"):
            EnrolmentReportFactory()
        with freeze_time("2020-01-02"):
            EnrolmentReportFactory()
        with freeze_time("2020-01-03"):
            EnrolmentReportFactory()
        self._authenticate()
        response = self._goto_reports(f"?{param}=2020-01-01")
        len(response.json()) == 3 if param.endswith("gte") else 0
        response = self._goto_reports(f"?{param}=2020-01-02")
        len(response.json()) == 2 if param.endswith("gte") else 1
        response = self._goto_reports(f"?{param}=2020-01-03")
        len(response.json()) == 1 if param.endswith("gte") else 2
        response = self._goto_reports(f"?{param}=2020-01-04")
        len(response.json()) == 0 if param.endswith("gte") else 3

    @parameterized.expand(["enrolment_start_time__gte", "enrolment_start_time__lte"])
    def test_filtering_with_enrolment_start_time(self, param):
        EnrolmentReport(enrolment_start_time=datetime.fromisoformat("2020-01-01"))
        EnrolmentReport(enrolment_start_time=datetime.fromisoformat("2020-01-02"))
        EnrolmentReport(enrolment_start_time=datetime.fromisoformat("2020-01-03"))
        self._authenticate()
        response = self._goto_reports(f"?{param}=2020-01-01")
        len(response.json()) == 3 if param.endswith("gte") else 0
        response = self._goto_reports(f"?{param}=2020-01-02")
        len(response.json()) == 2 if param.endswith("gte") else 1
        response = self._goto_reports(f"?{param}=2020-01-03")
        len(response.json()) == 1 if param.endswith("gte") else 2
        response = self._goto_reports(f"?{param}=2020-01-04")
        len(response.json()) == 0 if param.endswith("gte") else 3

    def test_filtering_with_combination(self):
        with freeze_time("2020-01-01"):
            EnrolmentReportFactory()
        with freeze_time("2020-01-02"):
            EnrolmentReportFactory()
        with freeze_time("2020-01-03"):
            EnrolmentReportFactory()
        with freeze_time("2020-01-04"):
            EnrolmentReportFactory()
        self._authenticate()
        response = self._goto_reports(
            "?created_at__gte=2020-01-02&created_at__lte=2020-01-03"
        )
        len(response.json()) == 2
