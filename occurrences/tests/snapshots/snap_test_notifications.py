# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_occurrence_enrolment_notifications 1"] = [
    """no-reply@hel.ninja|['gramirez@yahoo.com']|Occurrence enrolment FI|
        Event FI: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Leg him president compare room hotel town.
        Study group: Election stay every something base. Treat final central situation past ready join.
        Occurrence: 2013-12-12 06:37:19+01:40
        Person: gramirez@yahoo.com""",
    """no-reply@hel.ninja|['gramirez@yahoo.com']|Occurrence unenrolment FI|
        Event FI: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Leg him president compare room hotel town.
        Study group: Election stay every something base. Treat final central situation past ready join.
        Occurrence: 2013-12-12 04:57:19+00:00
        Person: gramirez@yahoo.com""",
    """no-reply@hel.ninja|['pereztimothy@nunez.com']|Occurrence enrolment EN|
        Event EN: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Leg him president compare room hotel town.
        Study group: Wrong when lead involve sport. Wall agency customer clear certain. As receive cup teacher.
        Occurrence: 2013-12-12 06:37:19+01:40
        Person: pereztimothy@nunez.com""",
    """no-reply@hel.ninja|['pereztimothy@nunez.com']|Occurrence unenrolment EN|
        Event EN: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Leg him president compare room hotel town.
        Study group: Wrong when lead involve sport. Wall agency customer clear certain. As receive cup teacher.
        Occurrence: 2013-12-12 04:57:19+00:00
        Person: pereztimothy@nunez.com""",
]
