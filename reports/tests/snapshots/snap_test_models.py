# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot

snapshots = Snapshot()

snapshots["test_enrolment_report 1"] = {
    "_enrolment_id": 97,
    "_occurrence_id": 1341,
    "_state": GenericRepr("<django.db.models.base.ModelState object at 0x100000000>"),
    "_study_group_id": 129,
    "created_at": GenericRepr("FakeDatetime(2020, 1, 4, 0, 0, tzinfo=<UTC>)"),
    "distance_from_unit_to_event_place": None,
    "enrolment_externally": False,
    "enrolment_start_time": GenericRepr(
        "datetime.datetime(1970, 5, 15, 14, 25, 3, tzinfo=<DstTzInfo 'Europe/Helsinki' LMT+1:40:00 STD>)"
    ),
    "enrolment_status": "pending",
    "enrolment_time": GenericRepr("FakeDatetime(2020, 1, 4, 0, 0, tzinfo=<UTC>)"),
    "id": 1,
    "keywords": None,
    "linked_event_id": "TVcHU",
    "occurrence_amount_of_seats": 49,
    "occurrence_cancelled": False,
    "occurrence_end_time": GenericRepr(
        "datetime.datetime(1976, 9, 7, 23, 2, 28, tzinfo=<DstTzInfo 'Europe/Helsinki' LMT+1:40:00 STD>)"
    ),
    "occurrence_languages": [],
    "occurrence_place_divisions": None,
    "occurrence_place_position": None,
    "occurrence_start_time": GenericRepr(
        "datetime.datetime(2020, 7, 12, 8, 50, 37, tzinfo=<DstTzInfo 'Europe/Helsinki' LMT+1:40:00 STD>)"
    ),
    "provider": None,
    "publisher": None,
    "study_group_amount_of_adult": 0,
    "study_group_amount_of_children": 631,
    "study_group_study_levels": [],
    "study_group_unit_divisions": None,
    "study_group_unit_id": None,
    "study_group_unit_position": None,
    "updated_at": GenericRepr("FakeDatetime(2020, 1, 4, 0, 0, tzinfo=<UTC>)"),
}
