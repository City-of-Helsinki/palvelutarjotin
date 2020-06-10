# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_occurrence_enrolment_notifications 1"] = [
    """no-reply@hel.ninja|['rcruz@watkins.info']|Occurrence enrolment FI|
        Event FI: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Defense level church use.
        Study group: Analysis season project executive entire. Service wonder everything pay parent theory.
        Occurrence: 1989-12-20 21:40:39+01:40
        Person: rcruz@watkins.info""",
    """no-reply@hel.ninja|['rcruz@watkins.info']|Occurrence unenrolment FI|
        Event FI: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Defense level church use.
        Study group: Analysis season project executive entire. Service wonder everything pay parent theory.
        Occurrence: 1989-12-20 20:00:39+00:00
        Person: rcruz@watkins.info""",
]
