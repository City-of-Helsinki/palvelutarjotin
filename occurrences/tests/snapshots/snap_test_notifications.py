# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_occurrence_enrolment_notifications 1"] = [
    """no-reply@hel.ninja|['stacey98@wolfe.com']|Occurrence enrolment FI|
        Event FI: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Leg him president compare room hotel town.
        Study group: Senior number scene today friend maintain marriage.
        Occurrence: 2013-12-12 06:37:19+01:40
        Person: stacey98@wolfe.com""",
    """no-reply@hel.ninja|['stacey98@wolfe.com']|Occurrence unenrolment FI|
        Event FI: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Leg him president compare room hotel town.
        Study group: Senior number scene today friend maintain marriage.
        Occurrence: 2013-12-12 04:57:19+00:00
        Person: stacey98@wolfe.com""",
    """no-reply@hel.ninja|['vandrews@lynch.com']|Occurrence enrolment EN|
        Event EN: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Leg him president compare room hotel town.
        Study group: Simply state social believe policy. Score think turn argue present.
        Occurrence: 2013-12-12 06:37:19+01:40
        Person: vandrews@lynch.com""",
    """no-reply@hel.ninja|['vandrews@lynch.com']|Occurrence unenrolment EN|
        Event EN: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Leg him president compare room hotel town.
        Study group: Simply state social believe policy. Score think turn argue present.
        Occurrence: 2013-12-12 04:57:19+00:00
        Person: vandrews@lynch.com""",
]
