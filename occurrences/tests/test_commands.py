import pytest
from dateutil.relativedelta import relativedelta
from django.core.management import call_command
from django.utils import timezone
from io import StringIO

from occurrences.factories import OccurrenceFactory, PalvelutarjotinEventFactory
from occurrences.models import PalvelutarjotinEvent


@pytest.mark.django_db
def test_delete_retention_period_exceeding_contact_info_command():
    too_old_1 = timezone.now() - relativedelta(months=24, days=1, minutes=60)
    too_old_2 = timezone.now() - relativedelta(months=24, days=1)
    still_valid_1 = timezone.now() - relativedelta(months=24, days=-1)
    still_valid_2 = timezone.now() - relativedelta(months=24, days=-1, minutes=60)
    output = StringIO()

    # ### CONTACT INFO SHOULD BE DELETED FROM THESE 2

    event_1 = PalvelutarjotinEventFactory()
    OccurrenceFactory(p_event=event_1, start_time=too_old_1, end_time=too_old_2)

    event_2 = PalvelutarjotinEventFactory()
    PalvelutarjotinEvent.objects.filter(pk=event_2.pk).update(created_at=too_old_1)

    # ### THESE 5 SHOULD NOT BE AFFECTED

    event_3 = PalvelutarjotinEventFactory()
    OccurrenceFactory(p_event=event_3, start_time=still_valid_1, end_time=still_valid_2)

    event_4 = PalvelutarjotinEventFactory()
    OccurrenceFactory(p_event=event_4, start_time=too_old_1, end_time=still_valid_1)

    event_5 = PalvelutarjotinEventFactory()
    PalvelutarjotinEvent.objects.filter(pk=event_5.pk).update(
        contact_info_deleted_at=timezone.now()
    )
    OccurrenceFactory(p_event=event_5, start_time=too_old_1, end_time=too_old_2)

    event_6 = PalvelutarjotinEventFactory()
    OccurrenceFactory(p_event=event_6, start_time=too_old_1, end_time=too_old_2)
    OccurrenceFactory(p_event=event_6, start_time=still_valid_1, end_time=still_valid_2)

    event_7 = PalvelutarjotinEventFactory()
    PalvelutarjotinEvent.objects.filter(pk=event_7.pk).update(created_at=still_valid_1)

    call_command("delete_retention_period_exceeding_contact_info", stdout=output)

    events_with_deleted_contact_info = PalvelutarjotinEvent.objects.filter(
        contact_info_deleted_at__isnull=False
    )
    assert events_with_deleted_contact_info.count() == 3
    assert event_1 in events_with_deleted_contact_info
    assert event_2 in events_with_deleted_contact_info
    # this had already contact_info_deleted_at set
    assert event_5 in events_with_deleted_contact_info

    output.seek(0)
    assert "Deleted contact info from 2 event(s)" in output.read()

    # Run the command again, expect no events to be affected
    call_command("delete_retention_period_exceeding_contact_info", stdout=output)
    output.seek(0)
    assert "No events are exceeding the retention period." in output.read()
