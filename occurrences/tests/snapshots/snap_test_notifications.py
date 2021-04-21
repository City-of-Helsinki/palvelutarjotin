# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_approve_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: XxEpr
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 29.06.2001 12.45
    Person: stephanieskinner@gmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo1OV8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

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
    """no-reply@hel.ninja|['aliciawest@barber.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Key crime trial investment difference. Let join might player example environment.
    Occurrence: 12.12.2013 06.37
    Person: aliciawest@barber.com

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
    Extra event info: XHPQj
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com
"""
]

snapshots["test_local_time_notification[tz1] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: XHPQj
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com
"""
]

snapshots["test_local_time_notification[tz2] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: XHPQj
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 04.01.2020 00.00
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
    """no-reply@hel.ninja|['williamsronald@hotmail.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Middle however western. Light a point charge stand store. Generation able take food share.
    Occurrence: 12.12.2013 06.37
    Person: rebecca01@gmail.com""",
    """no-reply@hel.ninja|['williamsronald@hotmail.com']|Occurrence unenrolment EN|
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
    Person: email_me@dommain.com
""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.57
    Person: email_me@dommain.com
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
                    Link to occurrence: https://provider.kultus.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6MTAx
                    Occurrence: #2001-02-23 20:07:07+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6MTAy
        """,
    """no-reply@hel.ninja|['jgray@yahoo.com']|Enrolment approved FI|
        Total pending enrolments: 3
        Total new accepted enrolments: 1
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/SLZLM
                    Occurrence: #2017-06-11 11:22:16+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/SLZLM/occurrences/T2NjdXJyZW5jZU5vZGU6MTA0
                    Occurrence: #1985-06-24 16:15:35+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/SLZLM/occurrences/T2NjdXJyZW5jZU5vZGU6MTA1
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/Gqqvl
                    Occurrence: #1992-03-09 01:25:06+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/Gqqvl/occurrences/T2NjdXJyZW5jZU5vZGU6MTA2
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/VjQsm
                    Occurrence: #2010-09-28 05:44:35+00:00 (1 new enrolments)
                    Link to occurrence: https://provider.kultus.fi/fi/events/VjQsm/occurrences/T2NjdXJyZW5jZU5vZGU6MTA3
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
    Study group: Traditional after born up always sport. Light a point charge stand store.
    Occurrence: 12.12.2013 06.37
    Person: email_me@dommain.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email_to_multiple_contact_person 1"] = [
    """no-reply@hel.ninja|['williamsronald@hotmail.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.37
    Person: williamsronald@hotmail.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email_to_multiple_contact_person 2"] = [
    """no-reply@hel.ninja|['williamsronald@hotmail.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Dream party door better performance race story. Beautiful if his their. Stuff election stay every.
    Occurrence: 12.12.2013 06.37
    Person: williamsronald@hotmail.com

    Custom message: custom message
""",
    """no-reply@hel.ninja|['cabreranicholas@brennan-smith.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: JCUUs
    Study group: Middle however western. Light a point charge stand store. Generation able take food share.
    Occurrence: 09.06.2016 10.34
    Person: cabreranicholas@brennan-smith.com

    Custom message: custom message
""",
    """no-reply@hel.ninja|['rebecca01@gmail.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: JCUUs
    Study group: Middle however western. Light a point charge stand store. Generation able take food share.
    Occurrence: 09.06.2016 10.34
    Person: rebecca01@gmail.com

    Custom message: custom message
""",
]

snapshots["test_only_send_approved_notification[True] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: XxEpr
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 29.06.2001 12.45
    Person: stephanieskinner@gmail.com

"""
]

snapshots["test_only_send_approved_notification[False] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: XxEpr
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 29.06.2001 12.45
    Person: stephanieskinner@gmail.com
""",
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: XxEpr
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 29.06.2001 12.45
    Person: stephanieskinner@gmail.com

""",
]

snapshots["test_mass_approve_enrolment_mutation 1"] = [
    """no-reply@hel.ninja|['philip16@moss.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZoGFT
    Study group: Believe policy security score. Turn argue present throw spend prevent.
    Occurrence: 30.07.1996 07.23
    Person: philip16@moss.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo4Nl8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['monica13@hotmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZoGFT
    Study group: Believe policy security score. Turn argue present throw spend prevent.
    Occurrence: 30.07.1996 07.23
    Person: monica13@hotmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo4Nl8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['melissa96@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZoGFT
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 30.07.1996 07.23
    Person: melissa96@gmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo4N18yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

""",
    """no-reply@hel.ninja|['perezlisa@hotmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZoGFT
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 30.07.1996 07.23
    Person: perezlisa@hotmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo4N18yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

""",
    """no-reply@hel.ninja|['robertmorris@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZoGFT
    Study group: Green unit recently turn who world various.
    Occurrence: 30.07.1996 07.23
    Person: robertmorris@gmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo4OF8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

""",
    """no-reply@hel.ninja|['kirbyjulie@yahoo.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZoGFT
    Study group: Green unit recently turn who world various.
    Occurrence: 30.07.1996 07.23
    Person: kirbyjulie@yahoo.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo4OF8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

""",
]
