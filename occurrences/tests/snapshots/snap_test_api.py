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
                        "amountOfAdult": 5,
                        "extraNeeds": "Recently analysis season project executive.",
                        "groupName": "Dream party door better performance race story. Beautiful if his their. Stuff election stay every.",
                        "groupSize": 860,
                        "name": "Increase thank certainly again thought summer. Beyond than trial western.",
                        "occurrences": {"edges": []},
                        "person": {"name": "William Brewer"},
                        "studyLevel": "GRADE_6",
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
            "amountOfAdult": 5,
            "extraNeeds": "Recently analysis season project executive.",
            "groupName": "Dream party door better performance race story. Beautiful if his their. Stuff election stay every.",
            "groupSize": 860,
            "name": "Increase thank certainly again thought summer. Beyond than trial western.",
            "occurrences": {"edges": []},
            "person": {"name": "William Brewer"},
            "studyLevel": "GRADE_6",
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
                        "amountOfSeats": 49,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-08-18T23:27:03+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "contactEmail": "bdorsey@owens.org",
                            "contactPhoneNumber": "972-701-1715x9102",
                            "duration": 120,
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2005-04-01T09:01:02+00:00",
                            "linkedEventId": "Leg him president compare room hotel town.",
                            "neededOccurrences": 4,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 49,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                        "studyGroups": {"edges": []},
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
                        "amountOfSeats": 49,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-08-18T23:27:03+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "contactEmail": "bdorsey@owens.org",
                            "contactPhoneNumber": "972-701-1715x9102",
                            "duration": 120,
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2005-04-01T09:01:02+00:00",
                            "linkedEventId": "Leg him president compare room hotel town.",
                            "neededOccurrences": 4,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 49,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                        "studyGroups": {"edges": []},
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
                        {"node": {"name": "Jason Berg"}},
                        {"node": {"name": "New name"}},
                    ]
                },
                "endTime": "2020-05-05T00:00:00+00:00",
                "languages": [
                    {"id": "en", "name": "English"},
                    {"id": "sv", "name": "Swedish"},
                ],
                "maxGroupSize": 20,
                "minGroupSize": 10,
                "pEvent": {
                    "contactEmail": "jgilbert@baker-johnston.org",
                    "contactPhoneNumber": "+1-614-494-8118x845",
                    "duration": 81,
                    "enrolmentEndDays": 0,
                    "enrolmentStart": "1978-12-17T12:06:21+00:00",
                    "linkedEventId": "Respond improve office table.",
                    "neededOccurrences": 6,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
            }
        }
    }
}

snapshots["test_update_occurrence 1"] = {
    "data": {
        "updateOccurrence": {
            "occurrence": {
                "contactPersons": {"edges": [{"node": {"name": "Aaron Little"}}]},
                "endTime": "2020-05-05T00:00:00+00:00",
                "languages": [
                    {"id": "fi", "name": "Finnish"},
                    {"id": "en", "name": "English"},
                    {"id": "sv", "name": "Swedish"},
                ],
                "maxGroupSize": 20,
                "minGroupSize": 10,
                "pEvent": {
                    "contactEmail": "mlong@gmail.com",
                    "contactPhoneNumber": "+1-316-804-2405x485",
                    "duration": 77,
                    "enrolmentEndDays": 0,
                    "enrolmentStart": "1979-08-26T09:49:31+00:00",
                    "linkedEventId": "Control as receive cup. Subject family around year.",
                    "neededOccurrences": 1,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
            }
        }
    }
}

snapshots["test_add_venue_staff_user 1"] = {
    "data": {
        "addVenue": {
            "venue": {
                "description": "Venue description in FI",
                "hasClothingStorage": True,
                "hasSnackEatingPlace": True,
                "id": "place_id",
                "translations": [
                    {"description": "Venue description in EN"},
                    {"description": "Venue description in FI"},
                ],
            }
        }
    }
}

snapshots["test_venues_query 1"] = {
    "data": {
        "venues": {
            "edges": [
                {
                    "node": {
                        "description": "Serious listen police shake. Page box child care any concern.",
                        "hasClothingStorage": True,
                        "hasSnackEatingPlace": False,
                        "id": "mZHxy",
                        "translations": [
                            {
                                "description": "Serious listen police shake. Page box child care any concern."
                            }
                        ],
                    }
                }
            ]
        }
    }
}

snapshots["test_update_venue_staff_user 1"] = {
    "data": {
        "updateVenue": {
            "venue": {
                "description": "Venue description",
                "hasClothingStorage": True,
                "hasSnackEatingPlace": True,
                "id": "OnQtr",
                "translations": [
                    {"description": "Venue description in EN"},
                    {"description": "Venue description"},
                ],
            }
        }
    }
}

snapshots["test_venue_query 1"] = {
    "data": {
        "venue": {
            "description": "Serious listen police shake. Page box child care any concern.",
            "hasClothingStorage": True,
            "hasSnackEatingPlace": False,
            "id": "mZHxy",
            "translations": [
                {
                    "description": "Serious listen police shake. Page box child care any concern."
                }
            ],
        }
    }
}

snapshots["test_add_study_group 1"] = {
    "data": {
        "addStudyGroup": {
            "studyGroup": {
                "amountOfAdult": 1,
                "extraNeeds": "Extra needs",
                "groupName": "Sample group name",
                "groupSize": 20,
                "name": "Sample study group name",
                "person": {
                    "emailAddress": "email@address.com",
                    "language": "SV",
                    "name": "Name",
                    "phoneNumber": "123123",
                },
                "studyLevel": "GRADE_1",
            }
        }
    }
}

snapshots["test_add_study_group 2"] = {
    "data": {
        "addStudyGroup": {
            "studyGroup": {
                "amountOfAdult": 1,
                "extraNeeds": "Extra needs",
                "groupName": "Sample group name",
                "groupSize": 20,
                "name": "Sample study group name",
                "person": {
                    "emailAddress": "smithmichael@gmail.com",
                    "language": "FI",
                    "name": "Rebekah Johnson",
                    "phoneNumber": "(719)885-7779x42677",
                },
                "studyLevel": "GRADE_1",
            }
        }
    }
}

snapshots["test_update_study_group_staff_user 1"] = {
    "data": {
        "updateStudyGroup": {
            "studyGroup": {
                "amountOfAdult": 2,
                "extraNeeds": "Extra needs",
                "groupName": "Sample group name",
                "groupSize": 20,
                "name": "Sample study group name",
                "person": {
                    "emailAddress": "email@address.com",
                    "language": "FI",
                    "name": "Name",
                    "phoneNumber": "123123",
                },
                "studyLevel": "GRADE_2",
            }
        }
    }
}

snapshots["test_update_study_group_staff_user 2"] = {
    "data": {
        "updateStudyGroup": {
            "studyGroup": {
                "amountOfAdult": 2,
                "extraNeeds": "Extra needs",
                "groupName": "Sample group name",
                "groupSize": 20,
                "name": "Sample study group name",
                "person": {
                    "emailAddress": "bdorsey@owens.org",
                    "language": "FI",
                    "name": "Jason Berg",
                    "phoneNumber": "011-715-9102",
                },
                "studyLevel": "GRADE_2",
            }
        }
    }
}

snapshots["test_enrol_occurrence 1"] = {
    "data": {
        "enrolOccurrence": {
            "enrolment": {
                "notificationType": "EMAIL",
                "occurrence": {
                    "amountOfSeats": 50,
                    "remainingSeats": 35,
                    "seatsTaken": 15,
                    "startTime": "2020-01-06T00:00:00+00:00",
                },
                "studyGroup": {"name": "To be created group"},
            }
        }
    }
}

snapshots["test_occurrences_filter_by_date 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 50,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-05-12T21:58:38+00:00",
                        "maxGroupSize": 605,
                        "minGroupSize": 263,
                        "pEvent": {
                            "contactEmail": "jvelasquez@hotmail.com",
                            "contactPhoneNumber": "071-988-5777x942",
                            "duration": 172,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2020-04-28T13:05:41+00:00",
                            "linkedEventId": "Put matter benefit treat final. Father boy economy the.",
                            "neededOccurrences": 0,
                        },
                        "placeId": "Near increase process truth list pressure.",
                        "remainingSeats": 50,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                }
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_time 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 49,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-12-12T04:57:19+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "contactEmail": "bdorsey@owens.org",
                            "contactPhoneNumber": "972-701-1715x9102",
                            "duration": 120,
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2005-04-01T09:01:02+00:00",
                            "linkedEventId": "Machine try lead behind everyone agency start.",
                            "neededOccurrences": 4,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 49,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T10:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                }
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_upcoming 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 17,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2001-02-23T20:07:07+00:00",
                        "maxGroupSize": 777,
                        "minGroupSize": 399,
                        "pEvent": {
                            "contactEmail": "stephanieskinner@gmail.com",
                            "contactPhoneNumber": "777.671.2406x75064",
                            "duration": 170,
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "linkedEventId": "Record card my. Sure sister return.",
                            "neededOccurrences": 5,
                        },
                        "placeId": "Daughter order stay sign discover.",
                        "remainingSeats": 17,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 21,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1996-02-20T13:49:25+00:00",
                        "maxGroupSize": 84,
                        "minGroupSize": 838,
                        "pEvent": {
                            "contactEmail": "stephanieskinner@gmail.com",
                            "contactPhoneNumber": "777.671.2406x75064",
                            "duration": 170,
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "linkedEventId": "Record card my. Sure sister return.",
                            "neededOccurrences": 5,
                        },
                        "placeId": "Able process base sing according.",
                        "remainingSeats": 21,
                        "seatsTaken": 0,
                        "startTime": "2020-01-07T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_date 2"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 50,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-05-12T21:58:38+00:00",
                        "maxGroupSize": 605,
                        "minGroupSize": 263,
                        "pEvent": {
                            "contactEmail": "jvelasquez@hotmail.com",
                            "contactPhoneNumber": "071-988-5777x942",
                            "duration": 172,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2020-04-28T13:05:41+00:00",
                            "linkedEventId": "Put matter benefit treat final. Father boy economy the.",
                            "neededOccurrences": 0,
                        },
                        "placeId": "Near increase process truth list pressure.",
                        "remainingSeats": 50,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 32,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-06-04T19:09:17+00:00",
                        "maxGroupSize": 342,
                        "minGroupSize": 669,
                        "pEvent": {
                            "contactEmail": "lfriedman@yahoo.com",
                            "contactPhoneNumber": "339-471-3127x06051",
                            "duration": 194,
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2009-04-10T19:35:34+00:00",
                            "linkedEventId": "Voice radio happen color scene. Create state rock only.",
                            "neededOccurrences": 2,
                        },
                        "placeId": "Believe policy security score.",
                        "remainingSeats": 32,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_time 2"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 33,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-11-21T02:09:38+00:00",
                        "maxGroupSize": 400,
                        "minGroupSize": 226,
                        "pEvent": {
                            "contactEmail": "mbrown@gmail.com",
                            "contactPhoneNumber": "+1-300-846-5476",
                            "duration": 33,
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1997-02-03T22:43:02+00:00",
                            "linkedEventId": "Pressure unit toward movie by garden. Country past involve.",
                            "neededOccurrences": 2,
                        },
                        "placeId": "Yard campaign former model reduce here natural.",
                        "remainingSeats": 33,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T12:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                }
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_time 3"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 32,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-06-04T19:09:17+00:00",
                        "maxGroupSize": 342,
                        "minGroupSize": 669,
                        "pEvent": {
                            "contactEmail": "lfriedman@yahoo.com",
                            "contactPhoneNumber": "339-471-3127x06051",
                            "duration": 194,
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2009-04-10T19:35:34+00:00",
                            "linkedEventId": "Voice radio happen color scene. Create state rock only.",
                            "neededOccurrences": 2,
                        },
                        "placeId": "Believe policy security score.",
                        "remainingSeats": 32,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 50,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-05-12T21:58:38+00:00",
                        "maxGroupSize": 605,
                        "minGroupSize": 263,
                        "pEvent": {
                            "contactEmail": "jvelasquez@hotmail.com",
                            "contactPhoneNumber": "071-988-5777x942",
                            "duration": 172,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2020-04-28T13:05:41+00:00",
                            "linkedEventId": "Put matter benefit treat final. Father boy economy the.",
                            "neededOccurrences": 0,
                        },
                        "placeId": "Near increase process truth list pressure.",
                        "remainingSeats": 50,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_time 4"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 32,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-06-04T19:09:17+00:00",
                        "maxGroupSize": 342,
                        "minGroupSize": 669,
                        "pEvent": {
                            "contactEmail": "lfriedman@yahoo.com",
                            "contactPhoneNumber": "339-471-3127x06051",
                            "duration": 194,
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2009-04-10T19:35:34+00:00",
                            "linkedEventId": "Voice radio happen color scene. Create state rock only.",
                            "neededOccurrences": 2,
                        },
                        "placeId": "Believe policy security score.",
                        "remainingSeats": 32,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 50,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-05-12T21:58:38+00:00",
                        "maxGroupSize": 605,
                        "minGroupSize": 263,
                        "pEvent": {
                            "contactEmail": "jvelasquez@hotmail.com",
                            "contactPhoneNumber": "071-988-5777x942",
                            "duration": 172,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2020-04-28T13:05:41+00:00",
                            "linkedEventId": "Put matter benefit treat final. Father boy economy the.",
                            "neededOccurrences": 0,
                        },
                        "placeId": "Near increase process truth list pressure.",
                        "remainingSeats": 50,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}

snapshots["test_delete_occurrence 1"] = {
    "data": {"deleteOccurrence": {"__typename": "DeleteOccurrenceMutationPayload"}}
}

snapshots["test_unenrol_occurrence 1"] = {
    "data": {
        "unenrolOccurrence": {
            "occurrence": {
                "amountOfSeats": 50,
                "remainingSeats": 50,
                "seatsTaken": 0,
                "startTime": "2020-01-06T00:00:00+00:00",
            },
            "studyGroup": {
                "name": "Last appear experience seven. Throw wrong party wall agency customer clear. Control as receive cup."
            },
        }
    }
}
