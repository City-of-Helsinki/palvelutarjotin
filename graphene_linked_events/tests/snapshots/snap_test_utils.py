# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_format_response 1"] = {
    "data": [
        {
            "email": "email1@example.com",
            "emails": ["email2@example.com", "email3@example.com"],
            "internal_id": 123,
        },
        {
            "internal_key": "@@@",
            "internal_keys": [{"internal_key": "value"}, {"key": "@value"}],
        },
    ]
}
