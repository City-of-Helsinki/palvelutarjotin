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
                        "amountOfSeats": 35,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-08-18T23:27:03+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2005-04-01T09:01:02+00:00",
                            "linkedEventId": "Leg him president compare room hotel town.",
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 35,
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
                        "amountOfSeats": 35,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-08-18T23:27:03+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2005-04-01T09:01:02+00:00",
                            "linkedEventId": "Leg him president compare room hotel town.",
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 35,
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

snapshots["test_delete_occurrence 1"] = {
    "data": {"deleteOccurrence": {"__typename": "DeleteOccurrenceMutationPayload"}}
}

snapshots["test_update_occurrence 1"] = {
    "data": {
        "updateOccurrence": {
            "occurrence": {
                "contactPersons": {"edges": [{"node": {"name": "Gregory Flores"}}]},
                "endTime": "2020-05-05T00:00:00+00:00",
                "languages": [
                    {"id": "fi", "name": "Finnish"},
                    {"id": "en", "name": "English"},
                    {"id": "sv", "name": "Swedish"},
                ],
                "maxGroupSize": 20,
                "minGroupSize": 10,
                "pEvent": {
                    "duration": 297,
                    "enrolmentEndDays": 1,
                    "enrolmentStart": "2003-11-12T21:12:26+00:00",
                    "linkedEventId": "Those notice medical science sort already.",
                    "neededOccurrences": 4,
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
                    "emailAddress": "manningelizabeth@gmail.com",
                    "name": "Jacob Baker",
                    "phoneNumber": "001-227-741-6754x3903",
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

snapshots["test_occurrences_filter_by_date 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 23,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1989-05-02T21:40:19+00:00",
                        "maxGroupSize": 181,
                        "minGroupSize": 392,
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1995-02-20T07:52:36+00:00",
                            "linkedEventId": "Shoulder write century spring never skill.",
                        },
                        "placeId": "News behind material address prove color effort loss.",
                        "remainingSeats": 23,
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
                        "amountOfSeats": 35,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-12-12T04:57:19+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2005-04-01T09:01:02+00:00",
                            "linkedEventId": "Machine try lead behind everyone agency start.",
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 35,
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
                        "amountOfSeats": 35,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1988-12-20T15:52:53+00:00",
                        "maxGroupSize": 899,
                        "minGroupSize": 271,
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "linkedEventId": "Record card my. Sure sister return.",
                        },
                        "placeId": "Laugh prevent make never.",
                        "remainingSeats": 35,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 46,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1971-11-04T13:17:08+00:00",
                        "maxGroupSize": 218,
                        "minGroupSize": 92,
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "linkedEventId": "Record card my. Sure sister return.",
                        },
                        "placeId": "Then top sing. Serious listen police shake.",
                        "remainingSeats": 46,
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
                        "amountOfSeats": 23,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1989-05-02T21:40:19+00:00",
                        "maxGroupSize": 181,
                        "minGroupSize": 392,
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1995-02-20T07:52:36+00:00",
                            "linkedEventId": "Shoulder write century spring never skill.",
                        },
                        "placeId": "News behind material address prove color effort loss.",
                        "remainingSeats": 23,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 45,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1996-04-05T11:49:51+00:00",
                        "maxGroupSize": 851,
                        "minGroupSize": 837,
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1999-10-11T19:54:38+00:00",
                            "linkedEventId": "Beautiful if his their. Stuff election stay every.",
                        },
                        "placeId": "Push book and interesting sit future.",
                        "remainingSeats": 45,
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
                        "amountOfSeats": 13,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "2002-06-15T11:57:08+00:00",
                        "maxGroupSize": 231,
                        "minGroupSize": 45,
                        "pEvent": {
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "1979-11-05T04:12:50+00:00",
                            "linkedEventId": "Challenge box myself last appear experience seven.",
                        },
                        "placeId": "Which president smile staff country actually generation.",
                        "remainingSeats": 13,
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
                        "amountOfSeats": 45,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1996-04-05T11:49:51+00:00",
                        "maxGroupSize": 851,
                        "minGroupSize": 837,
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1999-10-11T19:54:38+00:00",
                            "linkedEventId": "Beautiful if his their. Stuff election stay every.",
                        },
                        "placeId": "Push book and interesting sit future.",
                        "remainingSeats": 45,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 23,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1989-05-02T21:40:19+00:00",
                        "maxGroupSize": 181,
                        "minGroupSize": 392,
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1995-02-20T07:52:36+00:00",
                            "linkedEventId": "Shoulder write century spring never skill.",
                        },
                        "placeId": "News behind material address prove color effort loss.",
                        "remainingSeats": 23,
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
                        "amountOfSeats": 45,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1996-04-05T11:49:51+00:00",
                        "maxGroupSize": 851,
                        "minGroupSize": 837,
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1999-10-11T19:54:38+00:00",
                            "linkedEventId": "Beautiful if his their. Stuff election stay every.",
                        },
                        "placeId": "Push book and interesting sit future.",
                        "remainingSeats": 45,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 23,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1989-05-02T21:40:19+00:00",
                        "maxGroupSize": 181,
                        "minGroupSize": 392,
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1995-02-20T07:52:36+00:00",
                            "linkedEventId": "Shoulder write century spring never skill.",
                        },
                        "placeId": "News behind material address prove color effort loss.",
                        "remainingSeats": 23,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}
