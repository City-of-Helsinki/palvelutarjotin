import datetime
from unittest import mock

import pytest
from django.test import override_settings, TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from django.views.generic import TemplateView
from graphql_relay.node.node import to_global_id
from occurrences.factories import (
    EnrolmentFactory,
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from occurrences.models import Enrolment, PalvelutarjotinEvent
from organisations.factories import OrganisationFactory, PersonFactory
from organisations.models import Organisation
from reports.views import (
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
        super(ExportReportViewMixinTest, self).setUp()

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
        super(OrganisationPersonsMixinTest, self).setUp()

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


class PalvelutarjotinEventEnrolmentsMixinTest(TestCase):
    class DummyPalvelutarjotinEventEnrolmentCsvView(
        PalvelutarjotinEventEnrolmentsMixin
    ):
        model = PalvelutarjotinEvent
        max_results = 10

    def setUp(self):
        super(PalvelutarjotinEventEnrolmentsMixinTest, self).setUp()
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
        today = datetime.datetime.now(tz=timezone.utc)
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
        today = datetime.datetime.now(tz=timezone.utc)
        p_event1 = PalvelutarjotinEventFactory(
            enrolment_start=today - datetime.timedelta(days=3)
        )
        p_event2 = PalvelutarjotinEventFactory(
            enrolment_start=today - datetime.timedelta(days=2)
        )
        p_event3 = PalvelutarjotinEventFactory(
            enrolment_start=today - datetime.timedelta(days=1)
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
            "/fake-path/?start=%s"
            % ((today - datetime.timedelta(days=2)).strftime("%Y-%m-%d"))
        )
        self.assertEqual(self.view.get_queryset().count(), 6)
        self.view.request = RequestFactory().get(
            "/fake-path/?start=%s"
            % ((today + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
        )
        self.assertEqual(self.view.get_queryset().count(), 0)

        # filtered with end
        self.view.request = RequestFactory().get(
            "/fake-path/?end=%s"
            % ((today - datetime.timedelta(days=2)).strftime("%Y-%m-%d"))
        )
        self.assertEqual(self.view.get_queryset().count(), 3)
        self.view.request = RequestFactory().get(
            "/fake-path/?end=%s"
            % ((today - datetime.timedelta(days=3)).strftime("%Y-%m-%d"))
        )
        self.assertEqual(self.view.get_queryset().count(), 0)

        # filtered with start and end
        self.view.request = RequestFactory().get(
            "/fake-path/?start=%s&end=%s"
            % (
                (today - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
                (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            )
        )
        self.assertEqual(self.view.get_queryset().count(), 3)


class OrganisationPersonsAdminViewTest(TestCase):
    def setUp(self):
        super(OrganisationPersonsAdminViewTest, self).setUp()
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


class PalvelutarjotinEventEnrolmentsAdminViewTest(TestCase):
    def setUp(self):
        super(PalvelutarjotinEventEnrolmentsAdminViewTest, self).setUp()
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
        today = datetime.datetime.now(tz=timezone.utc)
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
