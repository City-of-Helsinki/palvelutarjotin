from unittest import mock

import pytest
from auditlog.models import LogEntry
from parameterized import parameterized
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.test import APIRequestFactory

from common.mixins import LogListAccessMixin
from occurrences.factories import PalvelutarjotinEventFactory
from occurrences.models import PalvelutarjotinEvent
from organisations.factories import UserFactory


class TestLogListAccessMixin:
    class DummyListView(LogListAccessMixin, generics.ListAPIView):
        def __init__(self, request=None):
            self.request = request
            self.queryset = PalvelutarjotinEvent.objects.all()

    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.mark.django_db
    def test_write_audit_access_log_of_paginated_objects(self, factory, user):
        batch_size = 3
        p_events = PalvelutarjotinEventFactory.create_batch(batch_size)
        request = factory.get("/")
        request.user = user
        list_view = self.DummyListView(request)
        with mock.patch("auditlog.signals.accessed.send") as mock_send:
            list_view._write_audit_access_log_of_paginated_objects(p_events)
            assert mock_send.call_count == batch_size
            for p_event in p_events:
                mock_send.assert_any_call(sender=PalvelutarjotinEvent, instance=p_event)

    @pytest.mark.django_db
    def test_paginate_queryset_no_pagination(self, factory, user):
        batch_size = 3
        p_events = PalvelutarjotinEventFactory.create_batch(batch_size)
        request = factory.get("/")
        request.user = user
        list_view = self.DummyListView(request)
        with mock.patch.object(
            list_view, "_write_audit_access_log_of_paginated_objects"
        ) as mock_write_log:
            result = list_view.paginate_queryset(p_events)
            assert result is None
            mock_write_log.assert_called_once_with(p_events)

    @parameterized.expand([(5, 5), (10, 20)])
    @pytest.mark.django_db
    def test_paginate_queryset_with_pagination(self, page_size, batch_size):
        user = UserFactory()
        factory = APIRequestFactory()

        class CustomPaginator(PageNumberPagination):
            def paginate_queryset(self, queryset, request, **kwargs):
                return queryset[:page_size]

        p_events = PalvelutarjotinEventFactory.create_batch(batch_size)
        request = factory.get("/", {"page": 1})
        request.user = user
        list_view = self.DummyListView(request)
        list_view.pagination_class = CustomPaginator

        with mock.patch.object(
            list_view, "_write_audit_access_log_of_paginated_objects"
        ) as mock_write_log:
            result = list_view.paginate_queryset(p_events)
            assert result is not None
            mock_write_log.assert_called_once()
            assert len(mock_write_log.call_args[0][0]) == page_size

    @pytest.mark.django_db
    def test_paginate_queryset_with_empty_queryset(self, factory, user):
        request = factory.get("/")
        request.user = user
        list_view = self.DummyListView(request)
        with mock.patch.object(
            list_view, "_write_audit_access_log_of_paginated_objects"
        ) as mock_write_log:
            result = list_view.paginate_queryset([])
            assert result is None
            mock_write_log.assert_called_once_with([])
        assert LogEntry.objects.filter(action=LogEntry.Action.ACCESS).count() == 0

    @pytest.mark.django_db
    def test_access_log_written_from_every_result(self, factory, user):
        """
        Test that an access log entry is written for each object in the list view
        result.
        """
        batch_size = 3
        p_events = PalvelutarjotinEventFactory.create_batch(batch_size)
        request = factory.get("/")
        request.user = user
        list_view = self.DummyListView(request)
        list_view.paginate_queryset(p_events)
        assert PalvelutarjotinEvent.objects.count() == batch_size
        assert (
            LogEntry.objects.filter(actor=user, action=LogEntry.Action.ACCESS).count()
            == batch_size
        )
