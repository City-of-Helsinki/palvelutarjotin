# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_approve_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['parkerbrittany@yahoo.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.
    Occurrence: 12.12.2013 06.37
    Person: parkerbrittany@yahoo.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['parkerbrittany@yahoo.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.
    Occurrence: 12.12.2013 06.37
    Person: parkerbrittany@yahoo.com

    Custom message: custom message
"""
]

snapshots["test_cancel_occurrence_notification 1"] = [
    """no-reply@hel.ninja|['phorton@gmail.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Add story arm listen money language which. Get fight concern toward race five least evening.
    Occurrence: 12.12.2013 06.37
    Person: phorton@gmail.com

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['ronaldperez@yahoo.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.37
    Person: ronaldperez@yahoo.com

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['parkerbrittany@yahoo.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.
    Occurrence: 12.12.2013 06.37
    Person: parkerbrittany@yahoo.com

    Custom message: Occurrence cancel reason
""",
]

snapshots["test_local_time_notification[tz0] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Staff country actually generation five training.
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com"""
]

snapshots["test_local_time_notification[tz1] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Staff country actually generation five training.
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com"""
]

snapshots["test_local_time_notification[tz2] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Staff country actually generation five training.
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 04.01.2020 00.00
    Person: stephanieskinner@gmail.com"""
]

snapshots["test_only_send_approved_notification[False] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Country actually generation five training thought price gas.
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 11.06.2014 11.14
    Person: stephanieskinner@gmail.com""",
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Country actually generation five training thought price gas.
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 11.06.2014 11.14
    Person: stephanieskinner@gmail.com

""",
]

snapshots["test_only_send_approved_notification[True] 1"] = [
    """no-reply@hel.ninja|['stephanieskinner@gmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Country actually generation five training thought price gas.
    Study group: Increase thank certainly again thought summer. Beyond than trial western.
    Occurrence: 11.06.2014 11.14
    Person: stephanieskinner@gmail.com

"""
]

snapshots["test_occurrence_enrolment_notifications_email_only 1"] = [
    """no-reply@hel.ninja|['parkerbrittany@yahoo.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.
    Occurrence: 12.12.2013 06.37
    Person: parkerbrittany@yahoo.com""",
    """no-reply@hel.ninja|['parkerbrittany@yahoo.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.
    Occurrence: 12.12.2013 06.57
    Person: parkerbrittany@yahoo.com""",
    """no-reply@hel.ninja|['ronaldperez@yahoo.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.37
    Person: ronaldperez@yahoo.com""",
    """no-reply@hel.ninja|['ronaldperez@yahoo.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Tough plant traditional after born up always. Return student light a point charge.
    Occurrence: 12.12.2013 06.57
    Person: ronaldperez@yahoo.com""",
]

snapshots["test_occurrence_enrolment_notifications_to_contact_person 1"] = [
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.
    Occurrence: 12.12.2013 06.37
    Person: parkerbrittany@yahoo.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Benefit treat final central. Past ready join enjoy. Huge get this success commercial recently from.
    Occurrence: 12.12.2013 06.57
    Person: parkerbrittany@yahoo.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Up always sport return. Light a point charge stand store.
    Occurrence: 12.12.2013 06.37
    Person: do_not_email_me@domain.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Up always sport return. Light a point charge stand store.
    Occurrence: 12.12.2013 06.57
    Person: do_not_email_me@domain.com""",
]
