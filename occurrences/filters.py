from datetime import timedelta

import django_filters
from django.db.models import F
from django.db.models.functions import Coalesce
from django.utils import timezone
from occurrences.models import Occurrence

from common.utils import convert_to_localtime_tz


class OccurrenceFilter(django_filters.FilterSet):
    upcoming = django_filters.BooleanFilter(
        method="filter_by_upcoming", field_name="start_time"
    )
    enrollable = django_filters.BooleanFilter(
        method="filter_by_enrollable", field_name="start_time"
    )
    date = django_filters.DateFilter(lookup_expr="date", field_name="start_time")
    time = django_filters.TimeFilter(method="filter_by_time", field_name="start_time")

    class Meta:
        model = Occurrence
        fields = [
            "upcoming",
            "enrollable",
            "date",
            "time",
            "p_event",
            "cancelled",
        ]

    def filter_by_upcoming(self, qs, name, value):
        if value:
            # Only work with PostgreSQL
            return qs.filter(**{name + "__gt": timezone.now()})
        return qs

    def filter_by_enrollable(self, qs, name, value):
        if value:
            # Only work with PostgreSQL
            return qs.annotate(
                # Nulls should be treated as 0, because null returns nothing
                enrolment_end_days=Coalesce("p_event__enrolment_end_days", 0)
            ).filter(
                **{
                    name
                    + "__gt": timezone.now()
                    + timedelta(days=1) * F("enrolment_end_days")
                }
            )
        return qs

    def filter_by_time(self, qs, name, value):
        value = convert_to_localtime_tz(value)
        return qs.filter(**{name + "__time": value})
