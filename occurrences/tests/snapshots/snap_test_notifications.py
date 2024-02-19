# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_approve_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ihlLy
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 09.05.1995 16.24
    Person: hutchinsonrachel@example.org
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: custom message
"""
]

snapshots["test_cancel_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['gtorres@example.com']|Enrolment cancellation confirmation FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.37
    Person: gtorres@example.com

    Custom message: custom message
"""
]

snapshots["test_cancelled_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['email_me@dommain.com']|Enrolment cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Let join might player example environment. Then offer organization model.
    Occurrence: 12.12.2013 06.37
    Person: email_me@dommain.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['gtorres@example.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.37
    Person: gtorres@example.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email_to_multiple_contact_person 1"] = [
    """no-reply@hel.ninja|['gtorres@example.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.37
    Person: gtorres@example.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email_to_multiple_contact_person 2"] = [
    """no-reply@hel.ninja|['gtorres@example.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.37
    Person: gtorres@example.com

    Custom message: custom message
""",
    """no-reply@hel.ninja|['oadams@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: WREov
    Study group: Real fast authority. Security American future quality result let.
    Occurrence: 14.05.1994 23.52
    Person: oadams@example.org

    Custom message: custom message
""",
    """no-reply@hel.ninja|['amandamurphy@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: WREov
    Study group: Real fast authority. Security American future quality result let.
    Occurrence: 14.05.1994 23.52
    Person: amandamurphy@example.org

    Custom message: custom message
""",
]

snapshots["test_local_time_notification[tz0] 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: eAhkM
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 04.01.2020 00.00
    Person: hutchinsonrachel@example.org
"""
]

snapshots["test_local_time_notification[tz1] 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: eAhkM
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 04.01.2020 00.00
    Person: hutchinsonrachel@example.org
"""
]

snapshots["test_local_time_notification[tz2] 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: eAhkM
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 04.01.2020 00.00
    Person: hutchinsonrachel@example.org
"""
]

snapshots["test_mass_approve_enrolment_mutation[False] 1"] = [
    """no-reply@hel.ninja|['brendasanchez@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 02.08.1988 10.00
    Person: brendasanchez@example.com
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['operry@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 02.08.1988 10.00
    Person: operry@example.com
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['michael98@example.net']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Body hard community somebody quality better majority. Artist alone lawyer might.
    Occurrence: 02.08.1988 10.00
    Person: michael98@example.net
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['acontreras@example.net']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Body hard community somebody quality better majority. Artist alone lawyer might.
    Occurrence: 02.08.1988 10.00
    Person: acontreras@example.net
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['nhuffman@example.net']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Opportunity care ready chair summer structure professional. Short food tree kid meet art space.
    Occurrence: 02.08.1988 10.00
    Person: nhuffman@example.net
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['andrewfox@example.net']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Opportunity care ready chair summer structure professional. Short food tree kid meet art space.
    Occurrence: 02.08.1988 10.00
    Person: andrewfox@example.net
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
]

snapshots["test_occurrence_enrolment_notifications_email_only 1"] = [
    """no-reply@hel.ninja|['gtorres@example.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.37
    Person: gtorres@example.com
""",
    """no-reply@hel.ninja|['gtorres@example.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.57
    Person: gtorres@example.com
""",
    """no-reply@hel.ninja|['gtorres@example.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Real fast authority. Security American future quality result let.
    Occurrence: 12.12.2013 06.37
    Person: amandamurphy@example.org""",
    """no-reply@hel.ninja|['gtorres@example.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Real fast authority. Security American future quality result let.
    Occurrence: 12.12.2013 06.57
    Person: amandamurphy@example.org""",
]

snapshots["test_occurrence_enrolment_notifications_to_contact_person 1"] = [
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.37
    Person: email_me@dommain.com
""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.57
    Person: email_me@dommain.com
""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Stay huge break. Far ten bar ask alone them yeah.
    Occurrence: 12.12.2013 06.37
    Person: do_not_email_me@domain.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Stay huge break. Far ten bar ask alone them yeah.
    Occurrence: 12.12.2013 06.57
    Person: do_not_email_me@domain.com""",
]

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

snapshots["test_send_enrolment_summary_report 1"] = [
    """no-reply@hel.ninja|['dsellers@example.net']|Enrolment approved FI|
        Total pending enrolments: 4
        Total new accepted enrolments: 0
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/aAVEa
                    Occurrence: #2020-01-13 22:00:00+00:00 (3 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6MTE=
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6MTI=
        """,
    """no-reply@hel.ninja|['seanyoung@example.net']|Enrolment approved FI|
        Total pending enrolments: 3
        Total new accepted enrolments: 1
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/tMVlt
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 new enrolments)
                    Link to occurrence: https://provider.kultus.fi/fi/events/tMVlt/occurrences/T2NjdXJyZW5jZU5vZGU6NDE=
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/nvAIl
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/nvAIl/occurrences/T2NjdXJyZW5jZU5vZGU6MjE=
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/nvAIl/occurrences/T2NjdXJyZW5jZU5vZGU6MjI=
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/HjoSH
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/HjoSH/occurrences/T2NjdXJyZW5jZU5vZGU6MzE=
        """,
]
