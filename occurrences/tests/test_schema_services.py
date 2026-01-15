from datetime import datetime

import pytest
from django.utils import timezone
from freezegun import freeze_time

from occurrences.factories import (
    OccurrenceFactory,
    PalvelutarjotinEventFactory,
    StudyGroupFactory,
)
from occurrences.schema_services import validate_enrolment
from palvelutarjotin.exceptions import EnrolmentClosedError, EnrolmentNotStartedError

# Module-level tzinfo variable for parametrized tests
tzinfo = timezone.now().tzinfo


@pytest.mark.django_db
@freeze_time("2020-01-04")
def test_validate_enrolment_with_null_enrolment_end_days(mock_get_event_data):
    """
    Test that validate_enrolment does not crash when enrolment_end_days is None.

    This tests the fix for the bug where None values in enrolment_end_days
    caused a TypeError when passed to timedelta().
    """
    study_group = StudyGroupFactory(group_size=10)

    # Create event with enrolment_end_days=None
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=tzinfo),
        enrolment_end_days=None,  # This should not cause TypeError
    )

    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=tzinfo),
        p_event=p_event,
        min_group_size=5,
        max_group_size=15,
        amount_of_seats=100,
    )

    # Should not raise TypeError, enrolment should be allowed
    validate_enrolment(study_group, occurrence)

    # Enrolment passed validation successfully
    assert True


@pytest.mark.django_db
@freeze_time("2020-01-04")
def test_validate_enrolment_with_zero_enrolment_end_days(mock_get_event_data):
    """
    Test that validate_enrolment does not crash when enrolment_end_days is 0.

    Zero is a valid value but falsy, so it should also be handled properly.
    """
    study_group = StudyGroupFactory(group_size=10)

    # Create event with enrolment_end_days=0
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=tzinfo),
        enrolment_end_days=0,  # This should also not cause issues
    )

    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 6, 0, 0, 0, tzinfo=tzinfo),
        p_event=p_event,
        min_group_size=5,
        max_group_size=15,
        amount_of_seats=100,
    )

    # Should not raise TypeError, enrolment should be allowed
    validate_enrolment(study_group, occurrence)

    # Enrolment passed validation successfully
    assert True


@pytest.mark.django_db
@freeze_time("2020-01-04")
def test_validate_enrolment_with_valid_enrolment_end_days(mock_get_event_data):
    """
    Test that validate_enrolment still works correctly with valid enrolment_end_days.

    This ensures the fix doesn't break existing functionality.
    """
    study_group = StudyGroupFactory(group_size=10)

    # Create event with enrolment_end_days=2
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 1, 0, 0, 0, tzinfo=tzinfo),
        enrolment_end_days=2,
    )

    # Occurrence starts on 2020-01-05, enrolment closes 2 days before: 2020-01-03
    # Current time is 2020-01-04, so enrolment should be closed
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 5, 0, 0, 0, tzinfo=tzinfo),
        p_event=p_event,
        min_group_size=5,
        max_group_size=15,
        amount_of_seats=100,
    )

    # Should raise EnrolmentClosedError because we're past the closing date
    with pytest.raises(EnrolmentClosedError):
        validate_enrolment(study_group, occurrence)


@pytest.mark.django_db
@freeze_time("2020-01-04")
def test_validate_enrolment_within_valid_period_with_enrolment_end_days(
    mock_get_event_data,
):
    """
    Test that validate_enrolment allows enrolment when within valid period with enrolment_end_days set.
    """
    study_group = StudyGroupFactory(group_size=10)

    # Create event with enrolment_end_days=2
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 3, 0, 0, 0, tzinfo=tzinfo),
        enrolment_end_days=2,
    )

    # Occurrence starts on 2020-01-08, enrolment closes 2 days before: 2020-01-06
    # Current time is 2020-01-04, so enrolment should still be open
    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 8, 0, 0, 0, tzinfo=tzinfo),
        p_event=p_event,
        min_group_size=5,
        max_group_size=15,
        amount_of_seats=100,
    )

    # Should not raise any error
    validate_enrolment(study_group, occurrence)

    # Enrolment passed validation successfully
    assert True


@pytest.mark.django_db
@freeze_time("2020-01-04")
def test_validate_enrolment_before_start_with_null_enrolment_end_days(
    mock_get_event_data,
):
    """
    Test that validate_enrolment still checks enrolment_start even when enrolment_end_days is None.
    """
    study_group = StudyGroupFactory(group_size=10)

    # Create event with enrolment_start in future and enrolment_end_days=None
    p_event = PalvelutarjotinEventFactory(
        enrolment_start=datetime(2020, 1, 5, 0, 0, 0, tzinfo=tzinfo),
        enrolment_end_days=None,
    )

    occurrence = OccurrenceFactory(
        start_time=datetime(2020, 1, 10, 0, 0, 0, tzinfo=tzinfo),
        p_event=p_event,
        min_group_size=5,
        max_group_size=15,
        amount_of_seats=100,
    )

    # Should raise EnrolmentNotStartedError because enrolment hasn't started yet
    with pytest.raises(EnrolmentNotStartedError):
        validate_enrolment(study_group, occurrence)
