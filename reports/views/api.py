import logging

from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions

from common.mixins import LogListAccessMixin
from common.utils import (
    to_local_datetime_if_naive,
)
from reports.models import EnrolmentReport
from reports.serializers import EnrolmentReportSerializer

logger = logging.getLogger(__name__)


class EnrolmentReportListView(LogListAccessMixin, generics.ListAPIView):
    """
    API endpoint that returns a list of enrolment reports in JSON format.

    There are some query parameters available that can be used as filters to
    narrow the result of the queryset.
    E.g you can use `?updated_at__gte=2021-11-23` to filter the results where
    the updated_at -field value should be greater than or equal to the given
    date in ISO-format (2021-11-23). The `__lte` stands for less than or equal.

    The available filters:
        - `updated_at__gte`, to filter with a report update date
        - `updated_at__gt`,
        - `updated_at__lte`,
        - `updated_at__lt`,
        - `created_at__gte`, to filter with a report creation date
        - `created_at__gt`,
        - `created_at__lte`
        - `created_at__lt`
        - `enrolment_time__gte`, to filter with a report enrolment time
        - `enrolment_time__gt`,
        - `enrolment_time__lte`
        - `enrolment_time__lt`
        - `enrolment_start_time__gte`, to filter with a report enrolment start time
        - `enrolment_start_time__gt`,
        - `enrolment_start_time__lte`
        - `enrolment_start_time__lt`
        - `enrolment_status`, to filter with an enrolment status:
        approved, pending. cancelled. declined

    The result set can also be ordered by with an `order_by` -query parameter.
    E.g `?order_by=updated_at` will order the resultset by updated_at -field.
    The order will be ascending by default but can be set to be descending,
    by adding a "-" (minus) in front of the field name,
    e.g `?order_by=-updated_at`.
    """

    allowed_non_datetime_filter_keys = [
        "enrolment_status",
    ]
    allowed_datetime_filter_keys = [
        "updated_at__gte",
        "updated_at__gt",
        "updated_at__lte",
        "updated_at__lt",
        "created_at__gte",
        "created_at__gt",
        "created_at__lte",
        "created_at__lt",
        "enrolment_start_time__gte",
        "enrolment_start_time__gt",
        "enrolment_start_time__lte",
        "enrolment_start_time__lt",
        "enrolment_time__gte",
        "enrolment_time__gt",
        "enrolment_time__lte",
        "enrolment_time__lt",
    ]

    serializer_class = EnrolmentReportSerializer
    # Must be allowed only with model permissions (for 1 power bi user).
    # Should not be allowed for every staff member,
    # but only the ones with special permission.
    permission_classes = [DjangoModelPermissions]
    # It is wanted from Power bi reports creator,
    # that there should be no pagination
    pagination_class = None

    queryset = EnrolmentReport.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Parse non-datetime filter parameters
        filter_params = {
            k: self.request.query_params.get(k)
            for k in self.allowed_non_datetime_filter_keys
            if self.request.query_params.get(k)
        }
        # Parse datetime filter parameters
        filter_params.update(
            {
                k: to_local_datetime_if_naive(self.request.query_params.get(k))
                for k in self.allowed_datetime_filter_keys
                if self.request.query_params.get(k)
            }
        )
        if filter_params:
            # Filter with allowed params
            queryset = queryset.filter(**filter_params)

        return queryset.order_by(self.request.query_params.get("order_by", "id"))

    @extend_schema(
        operation_id="listEnrolmentReports",
        summary=_("List all enrolment reports"),
        description=_(
            "Returns a list of all enrolment reports. Supports filtering by "
            "updated at, created at, enrolment time, enrolment start time, "
            "and enrolment status. Results can be ordered by any field."
        ),
        responses={
            200: OpenApiResponse(
                response=EnrolmentReportSerializer(many=True),
                description=_("A list of enrolment reports in JSON format."),
            ),
        },
        parameters=[
            OpenApiParameter(
                name=key,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=_(f"Filter by {key}"),
            )
            for key in allowed_datetime_filter_keys + allowed_non_datetime_filter_keys
        ]
        + [
            OpenApiParameter(
                name="order_by",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=_(
                    "Order the results by a specific field "
                    "(e.g., updated_at, -created_at)."
                ),
            ),
        ],
        tags=["Reports"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
