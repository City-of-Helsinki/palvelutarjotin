from datetime import timedelta

import django_filters
from django.db.models import F
from django.utils import timezone
from occurrences.models import Occurrence

from common.utils import convert_to_localtime_tz


class OccurrenceFilter(django_filters.FilterSet):
    upcoming = django_filters.BooleanFilter(
        method="filter_by_upcoming", field_name="start_time"
    )
    date = django_filters.DateFilter(lookup_expr="date", field_name="start_time")
    time = django_filters.TimeFilter(method="filter_by_time", field_name="start_time")

    class Meta:
        model = Occurrence
        fields = ["upcoming", "date", "time", "p_event", "cancelled"]

    order_by = django_filters.OrderingFilter(
        fields=(("start_time", "start_time"), ("end_time", "end_time"),)
    )

    def filter_by_upcoming(self, qs, name, value):
        if value:
            # Only work with PostgreSQL
            return qs.filter(
                **{
                    name
                    + "__gt": timezone.now()
                    + timedelta(days=1) * F("p_event__enrolment_end_days")
                }
            )
        return qs

    def filter_by_time(self, qs, name, value):
        value = convert_to_localtime_tz(value)
        return qs.filter(**{name + "__time": value})
