# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_approve_enrolment_notification_email 1'] = [
    '''no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MPXLz
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 05.09.1971 13.56
    Person: hutchinsonrachel@example.org
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: custom message
'''
]

snapshots['test_cancel_enrolment_notification_email 1'] = [
    '''no-reply@hel.ninja|['brett47@example.com']|Enrolment cancellation confirmation FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Campaign college career fight data. Generation man process white visit step.
    Occurrence: 18.04.2002 09.53
    Person: brett47@example.com

    Custom message: custom message
'''
]

snapshots['test_cancelled_enrolment_notification_email 1'] = [
    '''no-reply@hel.ninja|['email_me@dommain.com']|Enrolment cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Investment difference heart guess west black.
    Occurrence: 18.04.2002 09.53
    Person: email_me@dommain.com

    Custom message: custom message
'''
]

snapshots['test_decline_enrolment_notification_email 1'] = [
    '''no-reply@hel.ninja|['brett47@example.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Campaign college career fight data. Generation man process white visit step.
    Occurrence: 18.04.2002 09.53
    Person: brett47@example.com

    Custom message: custom message
'''
]

snapshots['test_decline_enrolment_notification_email_to_multiple_contact_person 1'] = [
    '''no-reply@hel.ninja|['brett47@example.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Campaign college career fight data. Generation man process white visit step.
    Occurrence: 18.04.2002 09.53
    Person: brett47@example.com

    Custom message: custom message
'''
]

snapshots['test_decline_enrolment_notification_email_to_multiple_contact_person 2'] = [
    '''no-reply@hel.ninja|['brett47@example.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Campaign college career fight data. Generation man process white visit step.
    Occurrence: 18.04.2002 09.53
    Person: brett47@example.com

    Custom message: custom message
''',
    '''no-reply@hel.ninja|['davidsummers@example.net']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: HHEUh
    Study group: Close term where up notice environment father stay. Hold project month similar support line.
    Occurrence: 01.11.2006 02.06
    Person: davidsummers@example.net

    Custom message: custom message
''',
    '''no-reply@hel.ninja|['sandra56@example.net']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: HHEUh
    Study group: Close term where up notice environment father stay. Hold project month similar support line.
    Occurrence: 01.11.2006 02.06
    Person: sandra56@example.net

    Custom message: custom message
'''
]

snapshots['test_local_time_notification[tz0] 1'] = [
    '''no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: OhDGq
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 04.01.2020 00.00
    Person: hutchinsonrachel@example.org
'''
]

snapshots['test_local_time_notification[tz1] 1'] = [
    '''no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: OhDGq
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 04.01.2020 00.00
    Person: hutchinsonrachel@example.org
'''
]

snapshots['test_local_time_notification[tz2] 1'] = [
    '''no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: OhDGq
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 04.01.2020 00.00
    Person: hutchinsonrachel@example.org
'''
]

snapshots['test_mass_approve_enrolment_mutation[False] 1'] = [
    '''no-reply@hel.ninja|['jamesmcgrath@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZHkjd
    Study group: Question national throw three.
    Occurrence: 29.08.1983 11.35
    Person: jamesmcgrath@example.com
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
''',
    '''no-reply@hel.ninja|['bradleybutler@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZHkjd
    Study group: Question national throw three.
    Occurrence: 29.08.1983 11.35
    Person: bradleybutler@example.com
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
''',
    '''no-reply@hel.ninja|['schwartzkayla@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZHkjd
    Study group: Better majority behavior along pressure yes others. Trouble change world indeed always.
    Occurrence: 29.08.1983 11.35
    Person: schwartzkayla@example.org
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
''',
    '''no-reply@hel.ninja|['cwall@example.net']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZHkjd
    Study group: Better majority behavior along pressure yes others. Trouble change world indeed always.
    Occurrence: 29.08.1983 11.35
    Person: cwall@example.net
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
''',
    '''no-reply@hel.ninja|['elizabethschultz@example.net']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZHkjd
    Study group: Structure professional message road focus turn space. Art space along win.
    Occurrence: 29.08.1983 11.35
    Person: elizabethschultz@example.net
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
''',
    '''no-reply@hel.ninja|['tammyjordan@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ZHkjd
    Study group: Structure professional message road focus turn space. Art space along win.
    Occurrence: 29.08.1983 11.35
    Person: tammyjordan@example.com
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: Custom message
'''
]

snapshots['test_occurrence_enrolment_notifications_email_only 1'] = [
    '''no-reply@hel.ninja|['brett47@example.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Campaign college career fight data. Generation man process white visit step.
    Occurrence: 18.04.2002 09.53
    Person: brett47@example.com
''',
    '''no-reply@hel.ninja|['brett47@example.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Campaign college career fight data. Generation man process white visit step.
    Occurrence: 18.04.2002 09.53
    Person: brett47@example.com
''',
    '''no-reply@hel.ninja|['brett47@example.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Close term where up notice environment father stay. Hold project month similar support line.
    Occurrence: 18.04.2002 09.53
    Person: sandra56@example.net''',
    '''no-reply@hel.ninja|['brett47@example.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Close term where up notice environment father stay. Hold project month similar support line.
    Occurrence: 18.04.2002 09.53
    Person: sandra56@example.net'''
]

snapshots['test_occurrence_enrolment_notifications_to_contact_person 1'] = [
    '''no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Campaign college career fight data. Generation man process white visit step.
    Occurrence: 18.04.2002 09.53
    Person: email_me@dommain.com
''',
    '''no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Campaign college career fight data. Generation man process white visit step.
    Occurrence: 18.04.2002 09.53
    Person: email_me@dommain.com
''',
    '''no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Race kitchen change single now rich. Bill write color politics. Matter this same happy standard.
    Occurrence: 18.04.2002 09.53
    Person: do_not_email_me@domain.com''',
    '''no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: ytHjL
    Study group: Race kitchen change single now rich. Bill write color politics. Matter this same happy standard.
    Occurrence: 18.04.2002 09.53
    Person: do_not_email_me@domain.com'''
]

snapshots['test_only_send_approved_notification[False] 1'] = [
    '''no-reply@hel.ninja|['hutchinsonrachel@example.org']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MPXLz
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 05.09.1971 13.56
    Person: hutchinsonrachel@example.org
''',
    '''no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MPXLz
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 05.09.1971 13.56
    Person: hutchinsonrachel@example.org

'''
]

snapshots['test_only_send_approved_notification[True] 1'] = [
    '''no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MPXLz
    Study group: Skin watch media. Condition like lay still bar. From daughter order stay sign discover eight.
    Occurrence: 05.09.1971 13.56
    Person: hutchinsonrachel@example.org

'''
]

snapshots['test_send_enrolment_summary_report 1'] = [
    '''no-reply@hel.ninja|['john29@example.com']|Enrolment approved FI|
        Total pending enrolments: 3
        Total new accepted enrolments: 1
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://kultus-admin.hel.fi/fi/events/TuZpF
                    Occurrence: #2020-01-14 00:00:00+00:00 (1 new enrolments)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/TuZpF/occurrences/T2NjdXJyZW5jZU5vZGU6NDE=
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://kultus-admin.hel.fi/fi/events/csgfn
                    Occurrence: #2020-01-14 00:00:00+00:00 (1 pending)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/csgfn/occurrences/T2NjdXJyZW5jZU5vZGU6MzE=
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://kultus-admin.hel.fi/fi/events/jfwob
                    Occurrence: #2020-01-14 00:00:00+00:00 (1 pending)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/jfwob/occurrences/T2NjdXJyZW5jZU5vZGU6MjE=
                    Occurrence: #2020-01-14 00:00:00+00:00 (1 pending)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/jfwob/occurrences/T2NjdXJyZW5jZU5vZGU6MjI=
        ''',
    '''no-reply@hel.ninja|['dsellers@example.net']|Enrolment approved FI|
        Total pending enrolments: 4
        Total new accepted enrolments: 0
            Event name: Raija Malka & Kaija Saariaho: Blick
            Event link: https://kultus-admin.hel.fi/fi/events/aAVEa
                    Occurrence: #2020-01-14 00:00:00+00:00 (3 pending)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6MTE=
                    Occurrence: #2020-01-14 00:00:00+00:00 (1 pending)
                    Link to occurrence: https://kultus-admin.hel.fi/fi/events/aAVEa/occurrences/T2NjdXJyZW5jZU5vZGU6MTI=
        '''
]
