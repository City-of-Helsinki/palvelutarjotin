# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_approve_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['williamsronald@hotmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.37
    Person: williamsronald@hotmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo1Ml8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['williamsronald@hotmail.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.37
    Person: williamsronald@hotmail.com

    Custom message: custom message
"""
]

snapshots["test_cancel_occurrence_notification 1"] = [
    """no-reply@hel.ninja|['carolyngarrett@yahoo.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Race five least evening take reason yes. I task moment want write her.
    Occurrence: 12.12.2013 06.37
    Person: carolyngarrett@yahoo.com

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['rebecca01@gmail.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Middle however western. Light a point charge stand store. Generation able take food share.
    Occurrence: 12.12.2013 06.37
    Person: rebecca01@gmail.com

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['williamsronald@hotmail.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.37
    Person: williamsronald@hotmail.com

    Custom message: Occurrence cancel reason
""",
]

snapshots["test_local_time_notification[tz0] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: XxEpr
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com
"""
]

snapshots["test_local_time_notification[tz1] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: XxEpr
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com
"""
]

snapshots["test_local_time_notification[tz2] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: XxEpr
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com
"""
]

snapshots["test_only_send_approved_notification[False] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Qjarq
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 11.06.2014 11.14
    Person: stephanieskinner@gmail.com
""",
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Qjarq
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 11.06.2014 11.14
    Person: stephanieskinner@gmail.com

""",
]

snapshots["test_only_send_approved_notification[True] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Qjarq
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 11.06.2014 11.14
    Person: stephanieskinner@gmail.com

"""
]

snapshots["test_occurrence_enrolment_notifications_email_only 1"] = [
    """no-reply@hel.ninja|['williamsronald@hotmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.37
    Person: williamsronald@hotmail.com
""",
    """no-reply@hel.ninja|['williamsronald@hotmail.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.57
    Person: williamsronald@hotmail.com
""",
    """no-reply@hel.ninja|['rebecca01@gmail.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Middle however western. Light a point charge stand store. Generation able take food share.
    Occurrence: 12.12.2013 06.37
    Person: rebecca01@gmail.com""",
    """no-reply@hel.ninja|['rebecca01@gmail.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Middle however western. Light a point charge stand store. Generation able take food share.
    Occurrence: 12.12.2013 06.57
    Person: rebecca01@gmail.com""",
]

snapshots["test_occurrence_enrolment_notifications_to_contact_person 1"] = [
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.37
    Person: williamsronald@hotmail.com
""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.57
    Person: williamsronald@hotmail.com
""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Chance of performance financial. Cause receive kitchen middle new eye.
    Occurrence: 12.12.2013 06.37
    Person: do_not_email_me@domain.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Chance of performance financial. Cause receive kitchen middle new eye.
    Occurrence: 12.12.2013 06.57
    Person: do_not_email_me@domain.com""",
]

snapshots["test_send_enrolment_summary_report 1"] = [
    """no-reply@hel.ninja|['underwoodtracy@roach-cruz.biz']|Enrolment approved FI|
        Total pending enrolments: 4
        Total new accepted enrolments: 0
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/aAVEa
                    Occurrence: #1996-02-20 13:49:25+00:00 (3 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6OTU=
                    Occurrence: #2001-02-23 20:07:07+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6OTY=
        """,
    """no-reply@hel.ninja|['uromero@hotmail.com']|Enrolment approved FI|
        Total pending enrolments: 3
        Total new accepted enrolments: 1
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/eZjav
                    Occurrence: #1990-02-18 00:22:21+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/eZjav/occurrences/T2NjdXJyZW5jZU5vZGU6OTg=
                    Occurrence: #2019-08-09 04:27:48+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/eZjav/occurrences/T2NjdXJyZW5jZU5vZGU6OTk=
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/ZAHQM
                    Occurrence: #1992-06-11 21:36:20+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/ZAHQM/occurrences/T2NjdXJyZW5jZU5vZGU6MTAw
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/tCbRR
                    Occurrence: #1976-03-14 10:36:26+00:00 (1 new enrolments)
                    Link to occurrence: https://provider.kultus.fi/fi/events/tCbRR/occurrences/T2NjdXJyZW5jZU5vZGU6MTAx
        """,
]

snapshots["test_cancel_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['williamsronald@hotmail.com']|Enrolment cancellation confirmation FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.37
    Person: williamsronald@hotmail.com

    Custom message: custom message
"""
]

snapshots["test_cancelled_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['email_me@dommain.com']|Enrolment cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.37
    Person: williamsronald@hotmail.com

    Custom message: custom message
"""
]
