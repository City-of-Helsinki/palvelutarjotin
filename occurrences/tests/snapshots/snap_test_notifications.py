# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_approve_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['longrebecca@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: eHMMT
    Study group: Care any concern bed agree. Laugh prevent make never.
    Occurrence: 08.02.1985 14.27
    Person: longrebecca@example.com
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: custom message
"""
]

snapshots["test_cancel_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['lucas89@example.com']|Enrolment cancellation confirmation FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Turn argue present throw spend prevent. Point exist road military Republican somebody.
    Occurrence: 12.12.2013 06.37
    Person: lucas89@example.com

    Custom message: custom message
"""
]

snapshots["test_cancel_occurrence_notification 1"] = [
    """no-reply@hel.ninja|['lucas89@example.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Turn argue present throw spend prevent. Point exist road military Republican somebody.
    Occurrence: 12.12.2013 06.37
    Person: lucas89@example.com

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['jacksonphillip@example.org']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Join pay discuss several performance part prevent. Time player right talk several.
    Occurrence: 12.12.2013 06.37
    Person: jacksonphillip@example.org

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['donald83@example.org']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Coach program recently outside. Matter this same happy standard.
    Occurrence: 12.12.2013 06.37
    Person: donald83@example.org

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['elizabeth19@example.net']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Book oil democratic have most discussion responsibility away.
    Occurrence: 12.12.2013 06.37
    Person: elizabeth19@example.net

    Custom message: Occurrence cancel reason
""",
]

snapshots["test_cancelled_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['email_me@dommain.com']|Enrolment cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Data out natural each. Conference thing much like test.
    Occurrence: 12.12.2013 06.37
    Person: email_me@dommain.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['lucas89@example.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Turn argue present throw spend prevent. Point exist road military Republican somebody.
    Occurrence: 12.12.2013 06.37
    Person: lucas89@example.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email_to_multiple_contact_person 1"] = [
    """no-reply@hel.ninja|['lucas89@example.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Turn argue present throw spend prevent. Point exist road military Republican somebody.
    Occurrence: 12.12.2013 06.37
    Person: lucas89@example.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email_to_multiple_contact_person 2"] = [
    """no-reply@hel.ninja|['lucas89@example.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Turn argue present throw spend prevent. Point exist road military Republican somebody.
    Occurrence: 12.12.2013 06.37
    Person: lucas89@example.com

    Custom message: custom message
""",
    """no-reply@hel.ninja|['sarah58@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: atpeB
    Study group: Join pay discuss several performance part prevent. Time player right talk several.
    Occurrence: 01.01.2016 15.17
    Person: sarah58@example.org

    Custom message: custom message
""",
    """no-reply@hel.ninja|['jacksonphillip@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: atpeB
    Study group: Join pay discuss several performance part prevent. Time player right talk several.
    Occurrence: 01.01.2016 15.17
    Person: jacksonphillip@example.org

    Custom message: custom message
""",
]

snapshots["test_local_time_notification[tz0] 1"] = [
    """no-reply@hel.ninja|['longrebecca@example.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: PbCye
    Study group: Care any concern bed agree. Laugh prevent make never.
    Occurrence: 04.01.2020 00.00
    Person: longrebecca@example.com
"""
]

snapshots["test_local_time_notification[tz1] 1"] = [
    """no-reply@hel.ninja|['longrebecca@example.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: PbCye
    Study group: Care any concern bed agree. Laugh prevent make never.
    Occurrence: 04.01.2020 00.00
    Person: longrebecca@example.com
"""
]

snapshots["test_local_time_notification[tz2] 1"] = [
    """no-reply@hel.ninja|['longrebecca@example.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: PbCye
    Study group: Care any concern bed agree. Laugh prevent make never.
    Occurrence: 04.01.2020 00.00
    Person: longrebecca@example.com
"""
]

snapshots["test_mass_approve_enrolment_mutation[False] 1"] = [
    """no-reply@hel.ninja|['higginscody@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Let join might player example environment. Then offer organization model.
    Occurrence: 02.08.1988 10.00
    Person: higginscody@example.org
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['oliviabass@example.net']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Let join might player example environment. Then offer organization model.
    Occurrence: 02.08.1988 10.00
    Person: oliviabass@example.net
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['tonyrussell@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Better majority behavior along pressure yes others. Trouble change world indeed always.
    Occurrence: 02.08.1988 10.00
    Person: tonyrussell@example.com
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['cwall@example.net']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Better majority behavior along pressure yes others. Trouble change world indeed always.
    Occurrence: 02.08.1988 10.00
    Person: cwall@example.net
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['hlee@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Kitchen because trade pressure. Office power create. Within Mr total learn.
    Occurrence: 02.08.1988 10.00
    Person: hlee@example.com
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['melinda81@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: bkihg
    Study group: Kitchen because trade pressure. Office power create. Within Mr total learn.
    Occurrence: 02.08.1988 10.00
    Person: melinda81@example.com
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
""",
]

snapshots["test_occurrence_enrolment_notifications_email_only 1"] = [
    """no-reply@hel.ninja|['lucas89@example.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Turn argue present throw spend prevent. Point exist road military Republican somebody.
    Occurrence: 12.12.2013 06.37
    Person: lucas89@example.com
""",
    """no-reply@hel.ninja|['lucas89@example.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Turn argue present throw spend prevent. Point exist road military Republican somebody.
    Occurrence: 12.12.2013 06.57
    Person: lucas89@example.com
""",
    """no-reply@hel.ninja|['lucas89@example.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Join pay discuss several performance part prevent. Time player right talk several.
    Occurrence: 12.12.2013 06.37
    Person: jacksonphillip@example.org""",
    """no-reply@hel.ninja|['lucas89@example.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Join pay discuss several performance part prevent. Time player right talk several.
    Occurrence: 12.12.2013 06.57
    Person: jacksonphillip@example.org""",
]

snapshots["test_occurrence_enrolment_notifications_to_contact_person 1"] = [
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Turn argue present throw spend prevent. Point exist road military Republican somebody.
    Occurrence: 12.12.2013 06.37
    Person: email_me@dommain.com
""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Turn argue present throw spend prevent. Point exist road military Republican somebody.
    Occurrence: 12.12.2013 06.57
    Person: email_me@dommain.com
""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Decade address have turn serve me every traditional. Sound describe risk newspaper reflect four.
    Occurrence: 12.12.2013 06.37
    Person: do_not_email_me@domain.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Decade address have turn serve me every traditional. Sound describe risk newspaper reflect four.
    Occurrence: 12.12.2013 06.57
    Person: do_not_email_me@domain.com""",
]

snapshots["test_only_send_approved_notification[False] 1"] = [
    """no-reply@hel.ninja|['longrebecca@example.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: eHMMT
    Study group: Care any concern bed agree. Laugh prevent make never.
    Occurrence: 08.02.1985 14.27
    Person: longrebecca@example.com
""",
    """no-reply@hel.ninja|['longrebecca@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: eHMMT
    Study group: Care any concern bed agree. Laugh prevent make never.
    Occurrence: 08.02.1985 14.27
    Person: longrebecca@example.com

""",
]

snapshots["test_only_send_approved_notification[True] 1"] = [
    """no-reply@hel.ninja|['longrebecca@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: eHMMT
    Study group: Care any concern bed agree. Laugh prevent make never.
    Occurrence: 08.02.1985 14.27
    Person: longrebecca@example.com

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
    """no-reply@hel.ninja|['ysmith@example.org']|Enrolment approved FI|
        Total pending enrolments: 3
        Total new accepted enrolments: 1
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/ScBdY
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/ScBdY/occurrences/T2NjdXJyZW5jZU5vZGU6MjE=
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/ScBdY/occurrences/T2NjdXJyZW5jZU5vZGU6MjI=
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/xxmXE
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/xxmXE/occurrences/T2NjdXJyZW5jZU5vZGU6MzE=
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/rlJUL
                    Occurrence: #2020-01-13 22:00:00+00:00 (1 new enrolments)
                    Link to occurrence: https://provider.kultus.fi/fi/events/rlJUL/occurrences/T2NjdXJyZW5jZU5vZGU6NDE=
        """,
]
