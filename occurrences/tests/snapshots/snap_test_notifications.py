# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_occurrence_enrolment_notifications 1"] = [
    """no-reply@hel.ninja|['cathy55@dixon-moran.com']|Occurrence enrolment FI|
        Event FI: Raija Malka & Kaija Saariaho: Blick
        Extra event info: In weight success answer entire increase thank.
        Study group: Local challenge box myself last.
Experience seven Republican throw wrong party wall.
        Occurrence: 1989-12-20 21:40:39+01:40
        Person: cathy55@dixon-moran.com""",
    """no-reply@hel.ninja|['cathy55@dixon-moran.com']|Occurrence unenrolment FI|
        Event FI: Raija Malka & Kaija Saariaho: Blick
        Extra event info: In weight success answer entire increase thank.
        Study group: Local challenge box myself last.
Experience seven Republican throw wrong party wall.
        Occurrence: 1989-12-20 20:00:39+00:00
        Person: cathy55@dixon-moran.com""",
]
