# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_approve_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: dlvJG
    Study group: Age else myself yourself.
Range north skin watch.
    Occurrence: 15.07.2008 03.29
    Person: stephanieskinner@gmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo2Ml8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['tonyjimenez@yahoo.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Family around year off. Sense person the probably.
    Occurrence: 12.12.2013 06.37
    Person: tonyjimenez@yahoo.com

    Custom message: custom message
"""
]

snapshots["test_local_time_notification[tz0] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: fvBni
    Study group: Age else myself yourself.
Range north skin watch.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com
"""
]

snapshots["test_local_time_notification[tz1] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: fvBni
    Study group: Age else myself yourself.
Range north skin watch.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com
"""
]

snapshots["test_local_time_notification[tz2] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: fvBni
    Study group: Age else myself yourself.
Range north skin watch.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com
"""
]

snapshots["test_occurrence_enrolment_notifications_email_only 1"] = [
    """no-reply@hel.ninja|['tonyjimenez@yahoo.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Family around year off. Sense person the probably.
    Occurrence: 12.12.2013 06.37
    Person: tonyjimenez@yahoo.com
""",
    """no-reply@hel.ninja|['tonyjimenez@yahoo.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Family around year off. Sense person the probably.
    Occurrence: 12.12.2013 06.57
    Person: tonyjimenez@yahoo.com
""",
    """no-reply@hel.ninja|['tonyjimenez@yahoo.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 12.12.2013 06.37
    Person: richardsanchez@yahoo.com""",
    """no-reply@hel.ninja|['tonyjimenez@yahoo.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 12.12.2013 06.57
    Person: richardsanchez@yahoo.com""",
]

snapshots["test_occurrence_enrolment_notifications_to_contact_person 1"] = [
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Family around year off. Sense person the probably.
    Occurrence: 12.12.2013 06.37
    Person: email_me@dommain.com
""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Family around year off. Sense person the probably.
    Occurrence: 12.12.2013 06.57
    Person: email_me@dommain.com
""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Key crime trial investment difference. Let join might player example environment.
    Occurrence: 12.12.2013 06.37
    Person: do_not_email_me@domain.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Key crime trial investment difference. Let join might player example environment.
    Occurrence: 12.12.2013 06.57
    Person: do_not_email_me@domain.com""",
]

snapshots["test_send_enrolment_summary_report 1"] = [
    """no-reply@hel.ninja|['underwoodtracy@roach-cruz.biz']|Enrolment approved FI|
        Total pending enrolments: 4
        Total new accepted enrolments: 0
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/aAVEa
                    Occurrence: #2005-01-18 03:44:33+00:00 (3 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6MTU1
                    Occurrence: #1992-11-14 16:36:36+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6MTU2
        """,
    """no-reply@hel.ninja|['cooknathan@gmail.com']|Enrolment approved FI|
        Total pending enrolments: 3
        Total new accepted enrolments: 1
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/QiZdS
                    Occurrence: #1982-07-08 17:49:14+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/QiZdS/occurrences/T2NjdXJyZW5jZU5vZGU6MTU4
                    Occurrence: #2006-03-19 04:44:09+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/QiZdS/occurrences/T2NjdXJyZW5jZU5vZGU6MTU5
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/TxNhK
                    Occurrence: #2017-06-15 05:09:54+00:00 (1 pending)
                    Link to occurrence: https://provider.kultus.fi/fi/events/TxNhK/occurrences/T2NjdXJyZW5jZU5vZGU6MTYw
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://provider.kultus.fi/fi/events/tNows
                    Occurrence: #1977-06-01 10:58:40+00:00 (1 new enrolments)
                    Link to occurrence: https://provider.kultus.fi/fi/events/tNows/occurrences/T2NjdXJyZW5jZU5vZGU6MTYx
        """,
]

snapshots["test_cancel_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['tonyjimenez@yahoo.com']|Enrolment cancellation confirmation FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Family around year off. Sense person the probably.
    Occurrence: 12.12.2013 06.37
    Person: tonyjimenez@yahoo.com

    Custom message: custom message
"""
]

snapshots["test_cancelled_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['email_me@dommain.com']|Enrolment cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Challenge school rule wish book significant minute. Special far magazine.
    Occurrence: 12.12.2013 06.37
    Person: email_me@dommain.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email_to_multiple_contact_person 1"] = [
    """no-reply@hel.ninja|['tonyjimenez@yahoo.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Family around year off. Sense person the probably.
    Occurrence: 12.12.2013 06.37
    Person: tonyjimenez@yahoo.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email_to_multiple_contact_person 2"] = [
    """no-reply@hel.ninja|['tonyjimenez@yahoo.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Family around year off. Sense person the probably.
    Occurrence: 12.12.2013 06.37
    Person: tonyjimenez@yahoo.com

    Custom message: custom message
""",
    """no-reply@hel.ninja|['bradshawpaul@gmail.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: TDEBK
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 11.03.1988 18.26
    Person: bradshawpaul@gmail.com

    Custom message: custom message
""",
    """no-reply@hel.ninja|['richardsanchez@yahoo.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: TDEBK
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 11.03.1988 18.26
    Person: richardsanchez@yahoo.com

    Custom message: custom message
""",
]

snapshots["test_only_send_approved_notification[True] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: dlvJG
    Study group: Age else myself yourself.
Range north skin watch.
    Occurrence: 15.07.2008 03.29
    Person: stephanieskinner@gmail.com

"""
]

snapshots["test_only_send_approved_notification[False] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: dlvJG
    Study group: Age else myself yourself.
Range north skin watch.
    Occurrence: 15.07.2008 03.29
    Person: stephanieskinner@gmail.com
""",
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: dlvJG
    Study group: Age else myself yourself.
Range north skin watch.
    Occurrence: 15.07.2008 03.29
    Person: stephanieskinner@gmail.com

""",
]

snapshots["test_mass_approve_enrolment_mutation 1"] = [
    """no-reply@hel.ninja|['barnettdiana@perry.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MTVcH
    Study group: Decade better attorney six. Shoulder decade address have. Serve me every traditional.
    Occurrence: 30.11.2020 14.06
    Person: barnettdiana@perry.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo5NF8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['byrdbrandon@newton-miranda.info']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MTVcH
    Study group: Decade better attorney six. Shoulder decade address have. Serve me every traditional.
    Occurrence: 30.11.2020 14.06
    Person: byrdbrandon@newton-miranda.info
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo5NF8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['scott76@cameron-hansen.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MTVcH
    Study group: Eat design give per kind history ahead. Herself consider fight us claim. Age feeling speech eye.
    Occurrence: 30.11.2020 14.06
    Person: scott76@cameron-hansen.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo5NV8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['jensenjulia@hotmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MTVcH
    Study group: Eat design give per kind history ahead. Herself consider fight us claim. Age feeling speech eye.
    Occurrence: 30.11.2020 14.06
    Person: jensenjulia@hotmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo5NV8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['robert99@hotmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MTVcH
    Study group: Civil find learn follow. Tend practice other poor.
    Occurrence: 30.11.2020 14.06
    Person: robert99@hotmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo5Nl8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: Custom message
""",
    """no-reply@hel.ninja|['newmanmelinda@yahoo.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MTVcH
    Study group: Civil find learn follow. Tend practice other poor.
    Occurrence: 30.11.2020 14.06
    Person: newmanmelinda@yahoo.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo5Nl8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: Custom message
""",
]

snapshots["test_cancel_occurrence_notification 1"] = [
    """no-reply@hel.ninja|['wlopez@dominguez-myers.net']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Pressure yes others.
Form you standard live. Responsibility dinner leg window old lawyer the say.
    Occurrence: 12.12.2013 06.37
    Person: wlopez@dominguez-myers.net

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['troy79@hotmail.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: A into hold project month. Line argue try unit.
    Occurrence: 12.12.2013 06.37
    Person: troy79@hotmail.com

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['richardsanchez@yahoo.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Work early property your stage receive. Determine sort under car.
    Occurrence: 12.12.2013 06.37
    Person: richardsanchez@yahoo.com

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['tonyjimenez@yahoo.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: zVxeo
    Study group: Family around year off. Sense person the probably.
    Occurrence: 12.12.2013 06.37
    Person: tonyjimenez@yahoo.com

    Custom message: Occurrence cancel reason
""",
]
