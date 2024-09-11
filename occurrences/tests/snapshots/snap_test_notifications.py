# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_approve_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: qMPXL
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 13.04.1972 14.30
    Person: hutchinsonrachel@example.org
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

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
    Study group: Attorney six throughout shoulder decade. Message now case.
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
    """no-reply@hel.ninja|['davidsummers@example.net']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: HEUhR
    Study group: Woman staff know eight account true tax. Tv news management letter.
    Occurrence: 22.03.2014 02.11
    Person: davidsummers@example.net

    Custom message: custom message
""",
    """no-reply@hel.ninja|['michaelanderson@example.net']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: HEUhR
    Study group: Woman staff know eight account true tax. Tv news management letter.
    Occurrence: 22.03.2014 02.11
    Person: michaelanderson@example.net

    Custom message: custom message
""",
]

snapshots["test_local_time_notification[tz0] 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: gihpk
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 04.01.2020 00.00
    Person: hutchinsonrachel@example.org
"""
]

snapshots["test_local_time_notification[tz1] 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: gihpk
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 04.01.2020 00.00
    Person: hutchinsonrachel@example.org
"""
]

snapshots["test_local_time_notification[tz2] 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: gihpk
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 04.01.2020 00.00
    Person: hutchinsonrachel@example.org
"""
]

snapshots["test_mass_approve_enrolment_mutation[False] 1"] = [
    """no-reply@hel.ninja|['brandonharvey@example.net']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 02.08.1988 10.00
    Person: brandonharvey@example.net
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['operry@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 02.08.1988 10.00
    Person: operry@example.com
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['obrooks@example.net']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Yes others enter program form you standard.
    Occurrence: 02.08.1988 10.00
    Person: obrooks@example.net
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['raymondking@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Yes others enter program form you standard.
    Occurrence: 02.08.1988 10.00
    Person: raymondking@example.org
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['joelsandoval@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Structure professional message road focus turn space. Art space along win.
    Occurrence: 02.08.1988 10.00
    Person: joelsandoval@example.com
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['madeline82@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Structure professional message road focus turn space. Art space along win.
    Occurrence: 02.08.1988 10.00
    Person: madeline82@example.com
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

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
    Study group: Woman staff know eight account true tax. Tv news management letter.
    Occurrence: 12.12.2013 06.37
    Person: michaelanderson@example.net""",
    """no-reply@hel.ninja|['gtorres@example.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Woman staff know eight account true tax. Tv news management letter.
    Occurrence: 12.12.2013 06.57
    Person: michaelanderson@example.net""",
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
    Study group: Watch method political institution trip race kitchen. Send same even child.
    Occurrence: 12.12.2013 06.37
    Person: do_not_email_me@domain.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Watch method political institution trip race kitchen. Send same even child.
    Occurrence: 12.12.2013 06.57
    Person: do_not_email_me@domain.com""",
]

snapshots["test_only_send_approved_notification[False] 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: qMPXL
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 13.04.1972 14.30
    Person: hutchinsonrachel@example.org
""",
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: qMPXL
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 13.04.1972 14.30
    Person: hutchinsonrachel@example.org

""",
]

snapshots["test_only_send_approved_notification[True] 1"] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: qMPXL
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 13.04.1972 14.30
    Person: hutchinsonrachel@example.org

"""
]

snapshots["test_send_enrolment_summary_report 1"] = [
    """no-reply@hel.ninja|['halljames@example.org']|Enrolment approved FI|
        Total pending enrolments: 3
        Total new accepted enrolments: 1
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://kultus-admin.hel.fi/fi/events/XalDf
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/XalDf/occurrences/T2NjdXJyZW5jZU5vZGU6MzE=
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://kultus-admin.hel.fi/fi/events/TuZpF
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 new enrolments)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/TuZpF/occurrences/T2NjdXJyZW5jZU5vZGU6NDE=
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://kultus-admin.hel.fi/fi/events/VnRGu
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/VnRGu/occurrences/T2NjdXJyZW5jZU5vZGU6MjE=
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/VnRGu/occurrences/T2NjdXJyZW5jZU5vZGU6MjI=
        """,
    """no-reply@hel.ninja|['dsellers@example.net']|Enrolment approved FI|
        Total pending enrolments: 4
        Total new accepted enrolments: 0
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://kultus-admin.hel.fi/fi/events/aAVEa
                    Occurrence: #2020-01-13 22:00:00+00:00 (3 pending)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6MTE=
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6MTI=
        """,
]
