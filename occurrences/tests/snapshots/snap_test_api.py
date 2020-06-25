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
                        "amountOfSeats": 9,
                        "autoAcceptance": True,
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
                        "remainingSeats": 9,
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
                        "amountOfSeats": 9,
                        "autoAcceptance": True,
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
                        "remainingSeats": 9,
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
                "contactPersons": {"edges": [{"node": {"name": "Rhonda Fischer"}}]},
                "endTime": "2020-05-05T00:00:00+00:00",
                "languages": [
                    {"id": "fi", "name": "Finnish"},
                    {"id": "en", "name": "English"},
                    {"id": "sv", "name": "Swedish"},
                ],
                "maxGroupSize": 20,
                "minGroupSize": 10,
                "pEvent": {
                    "contactEmail": "mitchellkathleen@orozco.org",
                    "contactPhoneNumber": "462.003.7722x182",
                    "duration": 261,
                    "enrolmentEndDays": 0,
                    "enrolmentStart": "1991-09-02T05:06:30+00:00",
                    "linkedEventId": "Realize staff staff read.",
                    "neededOccurrences": 10,
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
                "groupSize": 20,
                "name": "Sample study group name",
                "person": {
                    "emailAddress": "email@address.com",
                    "name": "Name",
                    "phoneNumber": "123123",
                },
            }
        }
    }
}

snapshots["test_add_study_group 2"] = {
    "data": {
        "addStudyGroup": {
            "studyGroup": {
                "groupSize": 20,
                "name": "Sample study group name",
                "person": {
                    "emailAddress": "marilyn21@gmail.com",
                    "name": "Sherri Bell",
                    "phoneNumber": "810-669-5836x9317",
                },
            }
        }
    }
}

snapshots["test_update_study_group_staff_user 1"] = {
    "data": {
        "updateStudyGroup": {
            "studyGroup": {
                "groupSize": 20,
                "name": "Sample study group name",
                "person": {
                    "emailAddress": "email@address.com",
                    "name": "Name",
                    "phoneNumber": "123123",
                },
            }
        }
    }
}

snapshots["test_update_study_group_staff_user 2"] = {
    "data": {
        "updateStudyGroup": {
            "studyGroup": {
                "groupSize": 20,
                "name": "Sample study group name",
                "person": {
                    "emailAddress": "bdorsey@owens.org",
                    "name": "Jason Berg",
                    "phoneNumber": "011-715-9102",
                },
            }
        }
    }
}

snapshots["test_enrol_occurrence 1"] = {
    "data": {
        "enrolOccurrence": {
            "enrolment": {
                "occurrence": {
                    "amountOfSeats": 50,
                    "remainingSeats": 35,
                    "seatsTaken": 15,
                    "startTime": "2020-01-06T00:00:00+00:00",
                },
                "studyGroup": {
                    "name": "Increase thank certainly again thought summer. Beyond than trial western."
                },
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
                        "amountOfSeats": 32,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1996-02-20T13:49:25+00:00",
                        "maxGroupSize": 84,
                        "minGroupSize": 838,
                        "pEvent": {
                            "contactEmail": "marilyn21@gmail.com",
                            "contactPhoneNumber": "810-669-5836x9317",
                            "duration": 269,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2011-12-27T10:59:58+00:00",
                            "linkedEventId": "From daughter order stay sign discover eight.",
                            "neededOccurrences": 5,
                        },
                        "placeId": "Spring never skill. Able process base sing according.",
                        "remainingSeats": 32,
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
                        "amountOfSeats": 9,
                        "autoAcceptance": True,
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
                        "remainingSeats": 9,
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
                        "amountOfSeats": 14,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1987-12-17T21:42:45+00:00",
                        "maxGroupSize": 968,
                        "minGroupSize": 378,
                        "pEvent": {
                            "contactEmail": "stephanieskinner@gmail.com",
                            "contactPhoneNumber": "777.671.2406x75064",
                            "duration": 170,
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "linkedEventId": "Record card my. Sure sister return.",
                            "neededOccurrences": 5,
                        },
                        "placeId": "Stay public high concern glass person. Century spring never.",
                        "remainingSeats": 14,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 35,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1988-12-20T15:52:53+00:00",
                        "maxGroupSize": 899,
                        "minGroupSize": 271,
                        "pEvent": {
                            "contactEmail": "stephanieskinner@gmail.com",
                            "contactPhoneNumber": "777.671.2406x75064",
                            "duration": 170,
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "linkedEventId": "Record card my. Sure sister return.",
                            "neededOccurrences": 5,
                        },
                        "placeId": "Laugh prevent make never.",
                        "remainingSeats": 35,
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
                        "amountOfSeats": 32,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1996-02-20T13:49:25+00:00",
                        "maxGroupSize": 84,
                        "minGroupSize": 838,
                        "pEvent": {
                            "contactEmail": "marilyn21@gmail.com",
                            "contactPhoneNumber": "810-669-5836x9317",
                            "duration": 269,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2011-12-27T10:59:58+00:00",
                            "linkedEventId": "From daughter order stay sign discover eight.",
                            "neededOccurrences": 5,
                        },
                        "placeId": "Spring never skill. Able process base sing according.",
                        "remainingSeats": 32,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 50,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1978-10-12T13:40:17+00:00",
                        "maxGroupSize": 275,
                        "minGroupSize": 594,
                        "pEvent": {
                            "contactEmail": "ujoseph@austin.com",
                            "contactPhoneNumber": "003-772-2182x7408",
                            "duration": 175,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2014-10-11T15:38:18+00:00",
                            "linkedEventId": "Staff read rule point leg within.",
                            "neededOccurrences": 4,
                        },
                        "placeId": "Science sort already name.",
                        "remainingSeats": 50,
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
                        "amountOfSeats": 34,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "2005-03-18T22:03:03+00:00",
                        "maxGroupSize": 698,
                        "minGroupSize": 744,
                        "pEvent": {
                            "contactEmail": "lfriedman@yahoo.com",
                            "contactPhoneNumber": "339-471-3127x06051",
                            "duration": 194,
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2009-04-10T19:35:34+00:00",
                            "linkedEventId": "Republican somebody hotel same can assume.",
                            "neededOccurrences": 2,
                        },
                        "placeId": "Score think turn argue present.",
                        "remainingSeats": 34,
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
                        "amountOfSeats": 50,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1978-10-12T13:40:17+00:00",
                        "maxGroupSize": 275,
                        "minGroupSize": 594,
                        "pEvent": {
                            "contactEmail": "ujoseph@austin.com",
                            "contactPhoneNumber": "003-772-2182x7408",
                            "duration": 175,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2014-10-11T15:38:18+00:00",
                            "linkedEventId": "Staff read rule point leg within.",
                            "neededOccurrences": 4,
                        },
                        "placeId": "Science sort already name.",
                        "remainingSeats": 50,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 32,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1996-02-20T13:49:25+00:00",
                        "maxGroupSize": 84,
                        "minGroupSize": 838,
                        "pEvent": {
                            "contactEmail": "marilyn21@gmail.com",
                            "contactPhoneNumber": "810-669-5836x9317",
                            "duration": 269,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2011-12-27T10:59:58+00:00",
                            "linkedEventId": "From daughter order stay sign discover eight.",
                            "neededOccurrences": 5,
                        },
                        "placeId": "Spring never skill. Able process base sing according.",
                        "remainingSeats": 32,
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
                        "amountOfSeats": 50,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1978-10-12T13:40:17+00:00",
                        "maxGroupSize": 275,
                        "minGroupSize": 594,
                        "pEvent": {
                            "contactEmail": "ujoseph@austin.com",
                            "contactPhoneNumber": "003-772-2182x7408",
                            "duration": 175,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2014-10-11T15:38:18+00:00",
                            "linkedEventId": "Staff read rule point leg within.",
                            "neededOccurrences": 4,
                        },
                        "placeId": "Science sort already name.",
                        "remainingSeats": 50,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 32,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1996-02-20T13:49:25+00:00",
                        "maxGroupSize": 84,
                        "minGroupSize": 838,
                        "pEvent": {
                            "contactEmail": "marilyn21@gmail.com",
                            "contactPhoneNumber": "810-669-5836x9317",
                            "duration": 269,
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2011-12-27T10:59:58+00:00",
                            "linkedEventId": "From daughter order stay sign discover eight.",
                            "neededOccurrences": 5,
                        },
                        "placeId": "Spring never skill. Able process base sing according.",
                        "remainingSeats": 32,
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
