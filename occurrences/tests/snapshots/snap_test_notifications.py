# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_occurrence_enrolment_notifications 1"] = [
    """no-reply@hel.ninja|['jameswatkins@ingram.org']|Occurrence enrolment FI|
        Event FI: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Adult data table TV. Bed agree room laugh prevent make never.
        Study group: Scientist service wonder everything pay. Moment strong hand push book and interesting sit.
        Occurrence: 1989-12-20 21:40:39+01:40
        Person: jameswatkins@ingram.org""",
    """no-reply@hel.ninja|['jameswatkins@ingram.org']|Occurrence unenrolment FI|
        Event FI: Raija Malka & Kaija Saariaho: Blick
        Extra event info: Adult data table TV. Bed agree room laugh prevent make never.
        Study group: Scientist service wonder everything pay. Moment strong hand push book and interesting sit.
        Occurrence: 1989-12-20 20:00:39+00:00
        Person: jameswatkins@ingram.org""",
]
