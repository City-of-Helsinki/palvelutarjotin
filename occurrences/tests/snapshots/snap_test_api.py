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
                        "amountOfSeats": 1,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-08-18T23:27:03+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "organisation": {"name": "Dr. Jesus Davis"},
                        "pEvent": {
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "1973-05-05T15:42:14+00:00",
                            "linkedEventId": "Certainly again thought summer because serious listen.",
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 1,
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
                        "amountOfSeats": 1,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-08-18T23:27:03+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "organisation": {"name": "Dr. Jesus Davis"},
                        "pEvent": {
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "1973-05-05T15:42:14+00:00",
                            "linkedEventId": "Certainly again thought summer because serious listen.",
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 1,
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
                "organisation": {"name": "Deborah Cardenas"},
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
                "organisation": {"name": "Deborah Cardenas"},
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
                    "emailAddress": "mallory34@manning.com",
                    "name": "Melinda Cunningham",
                    "phoneNumber": "+1-483-227-7416x754",
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
                        "amountOfSeats": 24,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2018-04-11T16:16:16+00:00",
                        "maxGroupSize": 570,
                        "minGroupSize": 394,
                        "organisation": {"name": "Justin Martinez"},
                        "pEvent": {
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2011-12-27T10:59:58+00:00",
                            "linkedEventId": "Still bar later evening southern. Sign discover eight.",
                        },
                        "placeId": "Room laugh prevent make never news behind.",
                        "remainingSeats": 24,
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
                        "amountOfSeats": 1,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-12-12T04:57:19+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "organisation": {"name": "Kari Sellers"},
                        "pEvent": {
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "1973-05-05T15:42:14+00:00",
                            "linkedEventId": "Certainly again thought summer because serious listen.",
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 1,
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
                        "amountOfSeats": 24,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2007-12-19T00:57:52+00:00",
                        "maxGroupSize": 845,
                        "minGroupSize": 334,
                        "organisation": {"name": "Jane Thompson"},
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "linkedEventId": "Record card my. Sure sister return.",
                        },
                        "placeId": "Alone our very television beat at success.",
                        "remainingSeats": 24,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 28,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "1986-01-08T08:26:19+00:00",
                        "maxGroupSize": 49,
                        "minGroupSize": 530,
                        "organisation": {"name": "Jason Berg"},
                        "pEvent": {
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "linkedEventId": "Record card my. Sure sister return.",
                        },
                        "placeId": "Machine try lead behind everyone agency start.",
                        "remainingSeats": 28,
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
                        "amountOfSeats": 24,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2018-04-11T16:16:16+00:00",
                        "maxGroupSize": 570,
                        "minGroupSize": 394,
                        "organisation": {"name": "Justin Martinez"},
                        "pEvent": {
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2011-12-27T10:59:58+00:00",
                            "linkedEventId": "Still bar later evening southern. Sign discover eight.",
                        },
                        "placeId": "Room laugh prevent make never news behind.",
                        "remainingSeats": 24,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 50,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1997-07-23T19:06:26+00:00",
                        "maxGroupSize": 162,
                        "minGroupSize": 88,
                        "organisation": {"name": "Janet Ritter"},
                        "pEvent": {
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1978-10-12T13:40:17+00:00",
                            "linkedEventId": "Success commercial recently from front affect senior.",
                        },
                        "placeId": "Book and interesting sit future dream party.",
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
                        "amountOfSeats": 47,
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "2002-06-15T11:57:08+00:00",
                        "maxGroupSize": 231,
                        "minGroupSize": 45,
                        "organisation": {"name": "Carl Nunez"},
                        "pEvent": {
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "1979-08-26T09:49:31+00:00",
                            "linkedEventId": "End available avoid girl middle.",
                        },
                        "placeId": "Which president smile staff country actually generation.",
                        "remainingSeats": 47,
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
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1997-07-23T19:06:26+00:00",
                        "maxGroupSize": 162,
                        "minGroupSize": 88,
                        "organisation": {"name": "Janet Ritter"},
                        "pEvent": {
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1978-10-12T13:40:17+00:00",
                            "linkedEventId": "Success commercial recently from front affect senior.",
                        },
                        "placeId": "Book and interesting sit future dream party.",
                        "remainingSeats": 50,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 24,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2018-04-11T16:16:16+00:00",
                        "maxGroupSize": 570,
                        "minGroupSize": 394,
                        "organisation": {"name": "Justin Martinez"},
                        "pEvent": {
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2011-12-27T10:59:58+00:00",
                            "linkedEventId": "Still bar later evening southern. Sign discover eight.",
                        },
                        "placeId": "Room laugh prevent make never news behind.",
                        "remainingSeats": 24,
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
                        "autoAcceptance": False,
                        "contactPersons": {"edges": []},
                        "endTime": "1997-07-23T19:06:26+00:00",
                        "maxGroupSize": 162,
                        "minGroupSize": 88,
                        "organisation": {"name": "Janet Ritter"},
                        "pEvent": {
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1978-10-12T13:40:17+00:00",
                            "linkedEventId": "Success commercial recently from front affect senior.",
                        },
                        "placeId": "Book and interesting sit future dream party.",
                        "remainingSeats": 50,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 24,
                        "autoAcceptance": True,
                        "contactPersons": {"edges": []},
                        "endTime": "2018-04-11T16:16:16+00:00",
                        "maxGroupSize": 570,
                        "minGroupSize": 394,
                        "organisation": {"name": "Justin Martinez"},
                        "pEvent": {
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2011-12-27T10:59:58+00:00",
                            "linkedEventId": "Still bar later evening southern. Sign discover eight.",
                        },
                        "placeId": "Room laugh prevent make never news behind.",
                        "remainingSeats": 24,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}
