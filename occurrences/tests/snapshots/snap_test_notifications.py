# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_occurrence_enrolment_notifications_email_only 1"] = [
    """no-reply@hel.ninja|['stacey98@wolfe.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Senior number scene today friend maintain marriage.
    Occurrence: 2013-12-12 06:37:19+01:40
    Person: stacey98@wolfe.com""",
    """no-reply@hel.ninja|['stacey98@wolfe.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Senior number scene today friend maintain marriage.
    Occurrence: 2013-12-12 04:57:19+00:00
    Person: stacey98@wolfe.com""",
    """no-reply@hel.ninja|['donnajones@gmail.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Maintain industry rock tough.
    Occurrence: 2013-12-12 06:37:19+01:40
    Person: donnajones@gmail.com""",
    """no-reply@hel.ninja|['donnajones@gmail.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Maintain industry rock tough.
    Occurrence: 2013-12-12 04:57:19+00:00
    Person: donnajones@gmail.com""",
]

snapshots["test_approve_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['stacey98@wolfe.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Senior number scene today friend maintain marriage.
    Occurrence: 2013-12-12 06:37:19+01:40
    Person: stacey98@wolfe.com

    Custom message: custom message
"""
]

snapshots["test_decline_enrolment_notification_email 1"] = [
    """no-reply@hel.ninja|['stacey98@wolfe.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Senior number scene today friend maintain marriage.
    Occurrence: 2013-12-12 06:37:19+01:40
    Person: stacey98@wolfe.com

    Custom message: custom message
"""
]

snapshots["test_occurrence_enrolment_notifications_to_contact_person 1"] = [
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Senior number scene today friend maintain marriage.
    Occurrence: 2013-12-12 06:37:19+01:40
    Person: stacey98@wolfe.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Senior number scene today friend maintain marriage.
    Occurrence: 2013-12-12 04:57:19+00:00
    Person: stacey98@wolfe.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence enrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Hot identify each its general. By garden so country past involve choose.
    Occurrence: 2013-12-12 06:37:19+01:40
    Person: do_not_email_me@domain.com""",
    """no-reply@hel.ninja|['email_me@dommain.com']|Occurrence unenrolment EN|
    Event EN: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Hot identify each its general. By garden so country past involve choose.
    Occurrence: 2013-12-12 04:57:19+00:00
    Person: do_not_email_me@domain.com""",
]

snapshots["test_cancel_occurrence_notification 1"] = [
    """no-reply@hel.ninja|['roberthall@rodgers.org']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Significant minute rest. Special far magazine.
    Occurrence: 2013-12-12 06:37:19+01:40
    Person: roberthall@rodgers.org

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['donnajones@gmail.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Maintain industry rock tough.
    Occurrence: 2013-12-12 06:37:19+01:40
    Person: donnajones@gmail.com

    Custom message: Occurrence cancel reason
""",
    """no-reply@hel.ninja|['stacey98@wolfe.com']|Occurrence cancelled FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: Leg him president compare room hotel town.
    Study group: Senior number scene today friend maintain marriage.
    Occurrence: 2013-12-12 06:37:19+01:40
    Person: stacey98@wolfe.com

    Custom message: Occurrence cancel reason
""",
]
