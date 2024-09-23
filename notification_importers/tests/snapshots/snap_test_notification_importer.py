# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_update_notifications 1"] = (
    "enrolment_approved|enrolment_approved fi updated subject|enrolment_approved en updated subject|enrolment_approved sv updated subject|enrolment_approved fi updated body_text|enrolment_approved en updated body_text|enrolment_approved sv updated body_text|||"
)

snapshots[
    "test_create_non_existing_and_update_existing_notifications 1"
] = """enrolment_approved|enrolment_approved fi updated subject|enrolment_approved en updated subject|enrolment_approved sv updated subject|enrolment_approved fi updated body_text|enrolment_approved en updated body_text|enrolment_approved sv updated body_text|||
occurrence_enrolment|occurrence_enrolment fi updated subject|occurrence_enrolment en updated subject|occurrence_enrolment sv updated subject|occurrence_enrolment fi updated body_text|occurrence_enrolment en updated body_text|occurrence_enrolment sv updated body_text|||"""

snapshots[
    "test_create_non_existing_notifications 1"
] = """enrolment_approved|enrolment_approved fi original subject|enrolment_approved en original subject|enrolment_approved sv original subject|enrolment_approved fi original body_text|enrolment_approved en original body_text|enrolment_approved sv original body_text|||
occurrence_enrolment|occurrence_enrolment fi updated subject|occurrence_enrolment en updated subject|occurrence_enrolment sv updated subject|occurrence_enrolment fi updated body_text|occurrence_enrolment en updated body_text|occurrence_enrolment sv updated body_text|||"""
