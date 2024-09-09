# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_get_profile_data_from_gdpr_api 1"] = {
    "children": [
        {"key": "UUID", "value": "26850000-2e85-11ea-b347-acde48001122"},
        {"key": "USERNAME", "value": "jeffersonkimberly_3MmHFh"},
        {"key": "FIRST_NAME", "value": "Alexis"},
        {"key": "LAST_NAME", "value": "Black"},
        {"key": "EMAIL", "value": "joshuajohnson@example.com"},
        {"key": "LAST_LOGIN", "value": "2020-01-04T00:00:00+00:00"},
        {"key": "DATE_JOINED", "value": "2020-01-04T00:00:00+00:00"},
    ],
    "key": "USER",
}
