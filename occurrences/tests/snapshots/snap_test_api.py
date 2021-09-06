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
                        "studyLevels": {"edges": []},
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
            "studyLevels": {"edges": []},
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
                        "amountOfSeats": 5,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-08-18T23:27:03+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "smithpaige@hotmail.com",
                            "contactPhoneNumber": "+1-064-976-3803x4669",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1971-08-19T21:08:32+00:00",
                            "linkedEventId": "zVxeo",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 7,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 5,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
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
        "occurrence": {
            "amountOfSeats": 5,
            "contactPersons": {"edges": []},
            "endTime": "2000-08-18T23:27:03+00:00",
            "languages": {"edges": []},
            "linkedEvent": {
                "name": {
                    "en": "Raija Malka & Kaija Saariaho: Blick",
                    "fi": "Raija Malka & Kaija Saariaho: Blick",
                    "sv": "Raija Malka & Kaija Saariaho: Blick",
                }
            },
            "maxGroupSize": 383,
            "minGroupSize": 341,
            "pEvent": {
                "autoAcceptance": False,
                "contactEmail": "smithpaige@hotmail.com",
                "contactPhoneNumber": "+1-064-976-3803x4669",
                "enrolmentEndDays": 1,
                "enrolmentStart": "1971-08-19T21:08:32+00:00",
                "linkedEventId": "zVxeo",
                "mandatoryAdditionalInformation": False,
                "neededOccurrences": 7,
            },
            "placeId": "Record card my. Sure sister return.",
            "remainingSeats": 5,
            "seatsApproved": 0,
            "seatsTaken": 0,
            "startTime": "2013-12-12T04:57:19+00:00",
            "studyGroups": {"edges": []},
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
                "endTime": "2020-05-06T00:00:00+00:00",
                "languages": {
                    "edges": [
                        {"node": {"id": "ar", "name": "Arabic"}},
                        {"node": {"id": "zh_hans", "name": "Chinese"}},
                        {"node": {"id": "en", "name": "English"}},
                        {"node": {"id": "ru", "name": "Russia"}},
                        {"node": {"id": "sv", "name": "Swedish"}},
                    ]
                },
                "maxGroupSize": None,
                "minGroupSize": 10,
                "pEvent": {
                    "autoAcceptance": False,
                    "contactEmail": "parkerbrittany@yahoo.com",
                    "contactPhoneNumber": "(179)621-2666",
                    "enrolmentEndDays": 2,
                    "enrolmentStart": "1998-03-12T19:56:01+00:00",
                    "linkedEventId": "LvDSC",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 10,
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
                "contactPersons": {"edges": [{"node": {"name": "Aaron Burton"}}]},
                "endTime": "2020-05-06T00:00:00+00:00",
                "languages": {
                    "edges": [
                        {"node": {"id": "en", "name": "English"}},
                        {"node": {"id": "fi", "name": "Finnish"}},
                        {"node": {"id": "sv", "name": "Swedish"}},
                    ]
                },
                "maxGroupSize": 88,
                "minGroupSize": 10,
                "pEvent": {
                    "contactEmail": "jonesmichael@navarro-morton.net",
                    "contactPhoneNumber": "3232221713",
                    "enrolmentEndDays": 1,
                    "enrolmentStart": "2011-10-01T03:22:55+00:00",
                    "linkedEventId": "oNLUZ",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 7,
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
                "hasAreaForGroupWork": True,
                "hasClothingStorage": True,
                "hasIndoorPlayingArea": True,
                "hasOutdoorPlayingArea": True,
                "hasSnackEatingPlace": True,
                "hasToiletNearby": True,
                "id": "place_id",
                "outdoorActivity": True,
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
                        "hasAreaForGroupWork": False,
                        "hasClothingStorage": True,
                        "hasIndoorPlayingArea": False,
                        "hasOutdoorPlayingArea": False,
                        "hasSnackEatingPlace": False,
                        "hasToiletNearby": False,
                        "id": "mZHxy",
                        "outdoorActivity": True,
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

snapshots["test_venue_query 1"] = {
    "data": {
        "venue": {
            "description": "Serious listen police shake. Page box child care any concern.",
            "hasAreaForGroupWork": False,
            "hasClothingStorage": True,
            "hasIndoorPlayingArea": False,
            "hasOutdoorPlayingArea": False,
            "hasSnackEatingPlace": False,
            "hasToiletNearby": False,
            "id": "mZHxy",
            "outdoorActivity": True,
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
                "studyLevels": {
                    "edges": [
                        {
                            "node": {
                                "id": "grade_1",
                                "label": "first grade",
                                "level": 3,
                                "translations": [
                                    {"label": "first grade", "languageCode": "EN"}
                                ],
                            }
                        }
                    ]
                },
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
                    "emailAddress": "hannah75@gmail.com",
                    "language": "FI",
                    "name": "Brandon Sullivan",
                    "phoneNumber": "144-948-1188x4524",
                },
                "studyLevels": {
                    "edges": [
                        {
                            "node": {
                                "id": "grade_1",
                                "label": "first grade",
                                "level": 3,
                                "translations": [
                                    {"label": "first grade", "languageCode": "EN"}
                                ],
                            }
                        }
                    ]
                },
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
                "studyLevels": {
                    "edges": [
                        {
                            "node": {
                                "id": "grade_2",
                                "label": "second grade",
                                "level": 4,
                                "translations": [
                                    {"label": "second grade", "languageCode": "EN"}
                                ],
                            }
                        }
                    ]
                },
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
                "studyLevels": {
                    "edges": [
                        {
                            "node": {
                                "id": "grade_2",
                                "label": "second grade",
                                "level": 4,
                                "translations": [
                                    {"label": "second grade", "languageCode": "EN"}
                                ],
                            }
                        }
                    ]
                },
            }
        }
    }
}

snapshots["test_enrol_occurrence 1"] = {
    "data": {
        "enrolOccurrence": {
            "enrolments": [
                {
                    "notificationType": "EMAIL",
                    "occurrence": {
                        "amountOfSeats": 50,
                        "remainingSeats": 30,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 20,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    },
                    "status": "PENDING",
                    "studyGroup": {"name": "To be created group"},
                },
                {
                    "notificationType": "EMAIL",
                    "occurrence": {
                        "amountOfSeats": 2,
                        "remainingSeats": 1,
                        "seatType": "ENROLMENT_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 1,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    },
                    "status": "PENDING",
                    "studyGroup": {"name": "To be created group"},
                },
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_date 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 45,
                        "contactPersons": {"edges": []},
                        "endTime": "2001-02-23T20:07:07+00:00",
                        "maxGroupSize": 777,
                        "minGroupSize": 399,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "stricklandpatrick@combs.com",
                            "contactPhoneNumber": "106.695.8369x31796",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1993-11-15T08:45:06+00:00",
                            "linkedEventId": "ZoGFT",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Later evening southern would according strong.",
                        "remainingSeats": 45,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
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
                        "amountOfSeats": 5,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-12-12T04:57:19+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "bthomas@charles.com",
                            "contactPhoneNumber": "750-649-7638x0346",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1988-11-29T04:01:36+00:00",
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 5,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
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
                        "amountOfSeats": 33,
                        "contactPersons": {"edges": []},
                        "endTime": "2011-05-08T04:35:51+00:00",
                        "maxGroupSize": 527,
                        "minGroupSize": 631,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "codyramirez@gmail.com",
                            "contactPhoneNumber": "+1-333-457-7355x777",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "From daughter order stay sign discover eight.",
                        "remainingSeats": 33,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 24,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-08-12T12:08:34+00:00",
                        "maxGroupSize": 838,
                        "minGroupSize": 847,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "codyramirez@gmail.com",
                            "contactPhoneNumber": "+1-333-457-7355x777",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Write century spring never skill down subject town.",
                        "remainingSeats": 24,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
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
                        "amountOfSeats": 45,
                        "contactPersons": {"edges": []},
                        "endTime": "2001-02-23T20:07:07+00:00",
                        "maxGroupSize": 777,
                        "minGroupSize": 399,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "stricklandpatrick@combs.com",
                            "contactPhoneNumber": "106.695.8369x31796",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1993-11-15T08:45:06+00:00",
                            "linkedEventId": "ZoGFT",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Later evening southern would according strong.",
                        "remainingSeats": 45,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 35,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-02-09T12:33:37+00:00",
                        "maxGroupSize": 75,
                        "minGroupSize": 879,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "delgadopatricia@hotmail.com",
                            "contactPhoneNumber": "+1-013-232-1316",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1978-07-26T12:24:03+00:00",
                            "linkedEventId": "pdZDV",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Throw wrong party wall agency customer clear.",
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
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
                        "amountOfSeats": 27,
                        "contactPersons": {"edges": []},
                        "endTime": "1974-10-19T15:53:39+00:00",
                        "maxGroupSize": 687,
                        "minGroupSize": 225,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "matthewwarren@walker.com",
                            "contactPhoneNumber": "788-408-7466",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1991-02-21T03:14:24+00:00",
                            "linkedEventId": "mOhDG",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Middle however western. Light a point charge stand store.",
                        "remainingSeats": 27,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
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
                        "amountOfSeats": 35,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-02-09T12:33:37+00:00",
                        "maxGroupSize": 75,
                        "minGroupSize": 879,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "delgadopatricia@hotmail.com",
                            "contactPhoneNumber": "+1-013-232-1316",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1978-07-26T12:24:03+00:00",
                            "linkedEventId": "pdZDV",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Throw wrong party wall agency customer clear.",
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 45,
                        "contactPersons": {"edges": []},
                        "endTime": "2001-02-23T20:07:07+00:00",
                        "maxGroupSize": 777,
                        "minGroupSize": 399,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "stricklandpatrick@combs.com",
                            "contactPhoneNumber": "106.695.8369x31796",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1993-11-15T08:45:06+00:00",
                            "linkedEventId": "ZoGFT",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Later evening southern would according strong.",
                        "remainingSeats": 45,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
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
                        "amountOfSeats": 35,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-02-09T12:33:37+00:00",
                        "maxGroupSize": 75,
                        "minGroupSize": 879,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "delgadopatricia@hotmail.com",
                            "contactPhoneNumber": "+1-013-232-1316",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1978-07-26T12:24:03+00:00",
                            "linkedEventId": "pdZDV",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Throw wrong party wall agency customer clear.",
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 45,
                        "contactPersons": {"edges": []},
                        "endTime": "2001-02-23T20:07:07+00:00",
                        "maxGroupSize": 777,
                        "minGroupSize": 399,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "stricklandpatrick@combs.com",
                            "contactPhoneNumber": "106.695.8369x31796",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1993-11-15T08:45:06+00:00",
                            "linkedEventId": "ZoGFT",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Later evening southern would according strong.",
                        "remainingSeats": 45,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
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
                "seatsApproved": 0,
                "seatsTaken": 0,
                "startTime": "2020-01-06T00:00:00+00:00",
            },
            "studyGroup": {
                "name": "Last appear experience seven. Throw wrong party wall agency customer clear. Control as receive cup."
            },
        }
    }
}

snapshots["test_approve_enrolment 1"] = {
    "data": {"approveEnrolment": {"enrolment": {"status": "APPROVED"}}}
}

snapshots["test_decline_enrolment 1"] = {
    "data": {"declineEnrolment": {"enrolment": {"status": "DECLINED"}}}
}

snapshots["test_approve_enrolment_with_custom_message 1"] = {
    "data": {"approveEnrolment": {"enrolment": {"status": "APPROVED"}}}
}

snapshots["test_approve_enrolment_with_custom_message 2"] = [
    """no-reply@hel.ninja|['barbarafarrell@yahoo.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: LVGVb
    Study group: Last appear experience seven. Throw wrong party wall agency customer clear. Control as receive cup.
    Occurrence: 06.01.2020 02.00
    Person: barbarafarrell@yahoo.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZToxOV8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: custom message
"""
]

snapshots["test_approve_enrolment 2"] = [
    """no-reply@hel.ninja|['barbarafarrell@yahoo.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: NGFIo
    Study group: Last appear experience seven. Throw wrong party wall agency customer clear. Control as receive cup.
    Occurrence: 06.01.2020 02.00
    Person: barbarafarrell@yahoo.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZToxN18yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

"""
]

snapshots["test_decline_enrolment 2"] = [
    """no-reply@hel.ninja|['barbarafarrell@yahoo.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: NGFIo
    Study group: Last appear experience seven. Throw wrong party wall agency customer clear. Control as receive cup.
    Occurrence: 06.01.2020 02.00
    Person: barbarafarrell@yahoo.com

""",
    """no-reply@hel.ninja|['barbarafarrell@yahoo.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: NGFIo
    Study group: Last appear experience seven. Throw wrong party wall agency customer clear. Control as receive cup.
    Occurrence: 06.01.2020 02.00
    Person: barbarafarrell@yahoo.com

""",
]

snapshots["test_decline_enrolment_with_custom_message 1"] = {
    "data": {"declineEnrolment": {"enrolment": {"status": "DECLINED"}}}
}

snapshots["test_decline_enrolment_with_custom_message 2"] = [
    """no-reply@hel.ninja|['barbarafarrell@yahoo.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: LVGVb
    Study group: Last appear experience seven. Throw wrong party wall agency customer clear. Control as receive cup.
    Occurrence: 06.01.2020 02.00
    Person: barbarafarrell@yahoo.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZToyNF8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: custom message
"""
]

snapshots["test_notification_template_query 1"] = {
    "data": {
        "notificationTemplate": {
            "customContextPreviewHtml": """<p>
    Event EN: Name in english
    Extra event info: linked_event_id
    Study group: group name
    Occurrence: 2020-12-12
    Person: email@me.com

    Custom message: custom_message
</p>""",
            "customContextPreviewText": """
    Event EN: Name in english
    Extra event info: linked_event_id
    Study group: group name
    Occurrence: 2020-12-12
    Person: email@me.com

    Custom message: custom_message
""",
            "template": {"type": "enrolment_approved"},
        }
    }
}

snapshots["test_delete_cancelled_occurrence 1"] = {
    "data": {"deleteOccurrence": {"__typename": "DeleteOccurrenceMutationPayload"}}
}

snapshots["test_cancel_occurrence 1"] = {
    "data": {"cancelOccurrence": {"occurrence": {"cancelled": True}}}
}

snapshots["test_enrol_occurrence_with_captcha 1"] = {
    "data": {
        "enrolOccurrence": {
            "enrolments": [
                {
                    "notificationType": "EMAIL",
                    "occurrence": {
                        "amountOfSeats": 50,
                        "remainingSeats": 30,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 20,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    },
                    "status": "PENDING",
                    "studyGroup": {"name": "To be created group"},
                }
            ]
        }
    }
}

snapshots["test_enrolments_summary 1"] = {
    "data": {
        "enrolmentSummary": {
            "count": 4,
            "edges": [
                {"node": {"status": "CANCELLED"}},
                {"node": {"status": "DECLINED"}},
                {"node": {"status": "APPROVED"}},
                {"node": {"status": "PENDING"}},
            ],
        }
    }
}

snapshots["test_enrolments_summary 2"] = {
    "data": {
        "enrolmentSummary": {"count": 1, "edges": [{"node": {"status": "APPROVED"}}]}
    }
}

snapshots["test_enrolments_summary 3"] = {
    "data": {
        "enrolmentSummary": {"count": 1, "edges": [{"node": {"status": "PENDING"}}]}
    }
}

snapshots["test_enrolments_summary 4"] = {
    "data": {
        "enrolmentSummary": {"count": 1, "edges": [{"node": {"status": "CANCELLED"}}]}
    }
}

snapshots["test_enrolments_summary 5"] = {
    "data": {
        "enrolmentSummary": {"count": 1, "edges": [{"node": {"status": "DECLINED"}}]}
    }
}

snapshots["test_enrol_auto_acceptance_occurrence 1"] = {
    "data": {
        "enrolOccurrence": {
            "enrolments": [
                {
                    "notificationType": "EMAIL",
                    "occurrence": {
                        "amountOfSeats": 50,
                        "remainingSeats": 30,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 20,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    },
                    "status": "PENDING",
                    "studyGroup": {"name": "To be created group"},
                }
            ]
        }
    }
}

snapshots["test_enrol_auto_acceptance_occurrence 2"] = {
    "data": {
        "enrolOccurrence": {
            "enrolments": [
                {
                    "notificationType": "EMAIL",
                    "occurrence": {
                        "amountOfSeats": 50,
                        "remainingSeats": 30,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 20,
                        "seatsTaken": 20,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    },
                    "status": "APPROVED",
                    "studyGroup": {"name": "To be created group"},
                }
            ]
        }
    }
}

snapshots["test_study_levels_query 1"] = {
    "data": {
        "studyLevels": {
            "edges": [
                {
                    "node": {
                        "id": "age_0_2",
                        "label": "age 0-2",
                        "level": 0,
                        "translations": [{"label": "age 0-2", "languageCode": "EN"}],
                    }
                },
                {
                    "node": {
                        "id": "age_3_4",
                        "label": "age 3-4",
                        "level": 1,
                        "translations": [{"label": "age 3-4", "languageCode": "EN"}],
                    }
                },
                {
                    "node": {
                        "id": "preschool",
                        "label": "preschool",
                        "level": 2,
                        "translations": [{"label": "preschool", "languageCode": "EN"}],
                    }
                },
                {
                    "node": {
                        "id": "grade_1",
                        "label": "first grade",
                        "level": 3,
                        "translations": [
                            {"label": "first grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_2",
                        "label": "second grade",
                        "level": 4,
                        "translations": [
                            {"label": "second grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_3",
                        "label": "third grade",
                        "level": 5,
                        "translations": [
                            {"label": "third grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_4",
                        "label": "fourth grade",
                        "level": 6,
                        "translations": [
                            {"label": "fourth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_5",
                        "label": "fifth grade",
                        "level": 7,
                        "translations": [
                            {"label": "fifth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_6",
                        "label": "sixth grade",
                        "level": 8,
                        "translations": [
                            {"label": "sixth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_7",
                        "label": "seventh grade",
                        "level": 9,
                        "translations": [
                            {"label": "seventh grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_8",
                        "label": "eighth grade",
                        "level": 10,
                        "translations": [
                            {"label": "eighth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_9",
                        "label": "ninth grade",
                        "level": 11,
                        "translations": [
                            {"label": "ninth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_10",
                        "label": "tenth grade",
                        "level": 12,
                        "translations": [
                            {"label": "tenth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "secondary",
                        "label": "secondary",
                        "level": 13,
                        "translations": [{"label": "secondary", "languageCode": "EN"}],
                    }
                },
                {
                    "node": {
                        "id": "other",
                        "label": "other group",
                        "level": 14,
                        "translations": [
                            {"label": "other group", "languageCode": "EN"}
                        ],
                    }
                },
            ]
        }
    }
}

snapshots["test_study_level_query 1"] = {
    "data": {
        "studyLevel": {
            "id": "age_0_2",
            "label": "age 0-2",
            "level": 0,
            "translations": [{"label": "age 0-2", "languageCode": "EN"}],
        }
    }
}

snapshots["test_language_query 1"] = {
    "data": {"language": {"id": "aAVEavNlmo", "name": "Guy site late eat."}}
}

snapshots["test_languagess_query 1"] = {
    "data": {
        "languages": {
            "edges": [
                {"node": {"id": "ar", "name": "Arabic"}},
                {"node": {"id": "zh_hans", "name": "Chinese"}},
                {"node": {"id": "en", "name": "English"}},
                {"node": {"id": "fi", "name": "Finnish"}},
                {"node": {"id": "aAVEavNlmo", "name": "Guy site late eat."}},
                {"node": {"id": "ru", "name": "Russia"}},
                {"node": {"id": "sv", "name": "Swedish"}},
            ]
        }
    }
}

snapshots["test_update_venue_staff_user 1"] = {
    "data": {
        "updateVenue": {
            "venue": {
                "description": "Venue description",
                "hasAreaForGroupWork": True,
                "hasClothingStorage": True,
                "hasIndoorPlayingArea": True,
                "hasOutdoorPlayingArea": True,
                "hasSnackEatingPlace": True,
                "hasToiletNearby": True,
                "id": "OnQtr",
                "outdoorActivity": True,
                "translations": [
                    {"description": "Venue description in EN"},
                    {"description": "Venue description"},
                ],
            }
        }
    }
}

snapshots["test_update_enrolment 1"] = {
    "data": {
        "updateEnrolment": {
            "enrolment": {
                "notificationType": "SMS",
                "occurrence": {
                    "amountOfSeats": 35,
                    "remainingSeats": 1,
                    "seatsApproved": 0,
                    "seatsTaken": 34,
                    "startTime": "2020-01-06T00:00:00+00:00",
                },
                "status": "PENDING",
                "studyGroup": {
                    "amountOfAdult": 3,
                    "enrolments": {
                        "edges": [
                            {"node": {"notificationType": "SMS"}},
                            {"node": {"notificationType": "SMS"}},
                        ]
                    },
                    "groupName": "Updated study group name",
                    "groupSize": 16,
                    "name": "Updated name",
                },
            }
        }
    }
}

snapshots["test_cancel_enrolment_query 1"] = {
    "data": {
        "cancellingEnrolment": {
            "enrolmentTime": "2020-01-04T00:00:00+00:00",
            "occurrence": {"seatsTaken": 354},
            "status": "PENDING",
            "studyGroup": {
                "groupSize": 345,
                "name": "Dream party door better performance race story. Beautiful if his their. Stuff election stay every.",
            },
        }
    }
}

snapshots["test_ask_for_cancelled_confirmation_mutation 1"] = {
    "data": {"cancelEnrolment": {"enrolment": {"status": "PENDING"}}}
}

snapshots["test_cancel_enrolment_mutation 1"] = {
    "data": {"cancelEnrolment": {"enrolment": {"status": "CANCELLED"}}}
}

snapshots["test_mass_approve_enrolment_mutation 1"] = {
    "data": {
        "massApproveEnrolments": {
            "enrolments": [
                {"status": "APPROVED"},
                {"status": "APPROVED"},
                {"status": "APPROVED"},
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_cancelled 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 5,
                        "contactPersons": {"edges": []},
                        "endTime": "1978-12-17T12:06:21+00:00",
                        "maxGroupSize": 851,
                        "minGroupSize": 837,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "underwoodtracy@roach-cruz.biz",
                            "contactPhoneNumber": "+1-345-773-5577x76712",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Pay parent theory go. Push book and interesting sit future.",
                        "remainingSeats": 5,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1996-04-05T11:49:51+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 17,
                        "contactPersons": {"edges": []},
                        "endTime": "1983-04-29T08:34:00+00:00",
                        "maxGroupSize": 777,
                        "minGroupSize": 399,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "underwoodtracy@roach-cruz.biz",
                            "contactPhoneNumber": "+1-345-773-5577x76712",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Daughter order stay sign discover.",
                        "remainingSeats": 17,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2001-02-23T20:07:07+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_cancelled 2"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 21,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-09-23T10:26:32+00:00",
                        "maxGroupSize": 84,
                        "minGroupSize": 838,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "underwoodtracy@roach-cruz.biz",
                            "contactPhoneNumber": "+1-345-773-5577x76712",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Able process base sing according.",
                        "remainingSeats": 21,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1996-02-20T13:49:25+00:00",
                        "studyGroups": {"edges": []},
                    }
                }
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_p_event 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 9,
                        "contactPersons": {"edges": []},
                        "endTime": "2002-08-15T13:47:04+00:00",
                        "maxGroupSize": 231,
                        "minGroupSize": 45,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "underwoodtracy@roach-cruz.biz",
                            "contactPhoneNumber": "+1-345-773-5577x76712",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Which president smile staff country actually generation.",
                        "remainingSeats": 9,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2002-06-15T11:57:08+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2016-11-01T20:07:19+00:00",
                        "maxGroupSize": 835,
                        "minGroupSize": 429,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "underwoodtracy@roach-cruz.biz",
                            "contactPhoneNumber": "+1-345-773-5577x76712",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Already name likely behind mission network.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2018-01-05T23:56:15+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_p_event 2"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 6,
                        "contactPersons": {"edges": []},
                        "endTime": "2017-05-02T13:53:33+00:00",
                        "maxGroupSize": 64,
                        "minGroupSize": 136,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "manningelizabeth@gmail.com",
                            "contactPhoneNumber": "001-227-741-6754x3903",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1995-02-20T07:52:36+00:00",
                            "linkedEventId": "mRVJD",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 8,
                        },
                        "placeId": "Box myself last appear. Wrong when lead involve sport.",
                        "remainingSeats": 6,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2000-02-02T08:29:39+00:00",
                        "studyGroups": {"edges": []},
                    }
                }
            ]
        }
    }
}

snapshots["test_occurrences_ordering_by_order_by_start_time 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 35,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-02-09T12:33:37+00:00",
                        "maxGroupSize": 75,
                        "minGroupSize": 879,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "delgadopatricia@hotmail.com",
                            "contactPhoneNumber": "+1-013-232-1316",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1978-07-26T12:24:03+00:00",
                            "linkedEventId": "pdZDV",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Throw wrong party wall agency customer clear.",
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 5,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-12-12T04:57:19+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "bthomas@charles.com",
                            "contactPhoneNumber": "750-649-7638x0346",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1988-11-29T04:01:36+00:00",
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 5,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 45,
                        "contactPersons": {"edges": []},
                        "endTime": "2001-02-23T20:07:07+00:00",
                        "maxGroupSize": 777,
                        "minGroupSize": 399,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "stricklandpatrick@combs.com",
                            "contactPhoneNumber": "106.695.8369x31796",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1993-11-15T08:45:06+00:00",
                            "linkedEventId": "ZoGFT",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Later evening southern would according strong.",
                        "remainingSeats": 45,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-07T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_ordering_by_order_by_start_time 2"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 45,
                        "contactPersons": {"edges": []},
                        "endTime": "2001-02-23T20:07:07+00:00",
                        "maxGroupSize": 777,
                        "minGroupSize": 399,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "stricklandpatrick@combs.com",
                            "contactPhoneNumber": "106.695.8369x31796",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1993-11-15T08:45:06+00:00",
                            "linkedEventId": "ZoGFT",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Later evening southern would according strong.",
                        "remainingSeats": 45,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-07T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 5,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-12-12T04:57:19+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "bthomas@charles.com",
                            "contactPhoneNumber": "750-649-7638x0346",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1988-11-29T04:01:36+00:00",
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 5,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 35,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-02-09T12:33:37+00:00",
                        "maxGroupSize": 75,
                        "minGroupSize": 879,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "delgadopatricia@hotmail.com",
                            "contactPhoneNumber": "+1-013-232-1316",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1978-07-26T12:24:03+00:00",
                            "linkedEventId": "pdZDV",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Throw wrong party wall agency customer clear.",
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_ordering_by_order_by_end_time 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 35,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-05T00:00:00+00:00",
                        "maxGroupSize": 75,
                        "minGroupSize": 879,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "delgadopatricia@hotmail.com",
                            "contactPhoneNumber": "+1-013-232-1316",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1978-07-26T12:24:03+00:00",
                            "linkedEventId": "pdZDV",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Throw wrong party wall agency customer clear.",
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1975-02-09T12:33:37+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 5,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-06T00:00:00+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "bthomas@charles.com",
                            "contactPhoneNumber": "750-649-7638x0346",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1988-11-29T04:01:36+00:00",
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 5,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 45,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-07T00:00:00+00:00",
                        "maxGroupSize": 777,
                        "minGroupSize": 399,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "stricklandpatrick@combs.com",
                            "contactPhoneNumber": "106.695.8369x31796",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1993-11-15T08:45:06+00:00",
                            "linkedEventId": "ZoGFT",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Later evening southern would according strong.",
                        "remainingSeats": 45,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2001-02-23T20:07:07+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_ordering_by_order_by_end_time 2"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 45,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-07T00:00:00+00:00",
                        "maxGroupSize": 777,
                        "minGroupSize": 399,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "stricklandpatrick@combs.com",
                            "contactPhoneNumber": "106.695.8369x31796",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1993-11-15T08:45:06+00:00",
                            "linkedEventId": "ZoGFT",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Later evening southern would according strong.",
                        "remainingSeats": 45,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2001-02-23T20:07:07+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 5,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-06T00:00:00+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "bthomas@charles.com",
                            "contactPhoneNumber": "750-649-7638x0346",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1988-11-29T04:01:36+00:00",
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 5,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 35,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-05T00:00:00+00:00",
                        "maxGroupSize": 75,
                        "minGroupSize": 879,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "delgadopatricia@hotmail.com",
                            "contactPhoneNumber": "+1-013-232-1316",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1978-07-26T12:24:03+00:00",
                            "linkedEventId": "pdZDV",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Throw wrong party wall agency customer clear.",
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1975-02-09T12:33:37+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}
