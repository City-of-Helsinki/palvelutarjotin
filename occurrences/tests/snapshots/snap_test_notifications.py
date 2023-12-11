# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_only_send_approved_notification[False] 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ihlLy
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 09.05.1995 16.24
    Person: hutchinsonrachel@example.org
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZToxXzIwMjAtMDEtMDQgMDA6MDA6MDArMDA6MDA=
""",
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ihlLy
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 09.05.1995 16.24
    Person: hutchinsonrachel@example.org
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZToxXzIwMjAtMDEtMDQgMDA6MDA6MDArMDA6MDA=

""",
]

snapshots["test_only_send_approved_notification[True] 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ihlLy
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 09.05.1995 16.24
    Person: hutchinsonrachel@example.org
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZToxXzIwMjAtMDEtMDQgMDA6MDA6MDArMDA6MDA=

"""
]
