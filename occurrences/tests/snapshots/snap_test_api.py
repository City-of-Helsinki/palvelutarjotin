# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_study_groups_query 1"] = {
    "data": {
        "studyGroups": {
            "edges": [
                {
                    "node": {
                        "groupSize": 860,
                        "name": "Increase thank certainly again thought summer. Beyond than trial western.",
                        "occurrences": {"edges": []},
                        "person": {"name": "William Brewer"},
                        "updatedAt": "2020-01-04T00:00:00+00:00",
                    }
                }
            ]
        }
    }
}

snapshots["test_study_group_query 1"] = {
    "data": {
        "studyGroup": {
            "groupSize": 860,
            "name": "Increase thank certainly again thought summer. Beyond than trial western.",
            "occurrences": {"edges": []},
            "person": {"name": "William Brewer"},
            "updatedAt": "2020-01-04T00:00:00+00:00",
        }
    }
}

snapshots["test_occurrences_query 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "contactPersons": {"edges": []},
                        "endTime": "2000-08-18T23:27:03+00:00",
                        "groups": {"edges": []},
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "organisation": {"name": "Dr. Jesus Davis"},
                        "pEvent": {
                            "enrolmentEnd": "2011-02-05T18:10:51+00:00",
                            "enrolmentStart": "1995-04-12T06:10:43+00:00",
                            "linkedEventId": "Success answer entire increase thank. Least then top sing.",
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "startTime": "2013-12-12T04:57:19+00:00",
                    }
                }
            ]
        }
    }
}

snapshots["test_occurrence_query 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "contactPersons": {"edges": []},
                        "endTime": "2000-08-18T23:27:03+00:00",
                        "groups": {"edges": []},
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "organisation": {"name": "Dr. Jesus Davis"},
                        "pEvent": {
                            "enrolmentEnd": "2011-02-05T18:10:51+00:00",
                            "enrolmentStart": "1995-04-12T06:10:43+00:00",
                            "linkedEventId": "Success answer entire increase thank. Least then top sing.",
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "startTime": "2013-12-12T04:57:19+00:00",
                    }
                }
            ]
        }
    }
}

snapshots["test_add_occurrence 1"] = {
    "data": {
        "addOccurrence": {
            "occurrence": {
                "contactPersons": {
                    "edges": [
                        {"node": {"name": "New name"}},
                        {"node": {"name": "Sara Johnson"}},
                    ]
                },
                "endTime": "2020-05-05T00:00:00+00:00",
                "maxGroupSize": 20,
                "minGroupSize": 10,
                "organisation": {"name": "William Brewer"},
                "pEvent": {
                    "duration": 119,
                    "enrolmentEnd": "2004-06-15T12:51:54+00:00",
                    "enrolmentStart": "1987-12-17T21:42:45+00:00",
                    "linkedEventId": "Glass person along age else.",
                    "neededOccurrences": 2,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
            }
        }
    }
}

snapshots["test_delete_occurrence 1"] = {
    "data": {"deleteOccurrence": {"__typename": "DeleteOccurrenceMutationPayload"}}
}

snapshots["test_update_occurrence 1"] = {
    "data": {
        "updateOccurrence": {
            "occurrence": {
                "contactPersons": {"edges": [{"node": {"name": "Melissa Velasquez"}}]},
                "endTime": "2020-05-05T00:00:00+00:00",
                "maxGroupSize": 20,
                "minGroupSize": 10,
                "organisation": {"name": "William Brewer"},
                "pEvent": {
                    "duration": 190,
                    "enrolmentEnd": "1977-11-16T07:32:26+00:00",
                    "enrolmentStart": "2013-06-24T17:35:24+00:00",
                    "linkedEventId": "Respond draw military dog hospital number.",
                    "neededOccurrences": 9,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
            }
        }
    }
}
