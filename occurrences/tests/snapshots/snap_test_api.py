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
                    "contactEmail": "colin84@yahoo.com",
                    "contactPhoneNumber": "179.621.2666x14494",
                    "enrolmentEndDays": 1,
                    "enrolmentStart": "1986-04-11T14:17:11+00:00",
                    "linkedEventId": "fcwOr",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 9,
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
                                "label": None,
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
                                "label": None,
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
                                "label": None,
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
                                "label": None,
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
                        "remainingSeats": 50,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    },
                    "status": "PENDING",
                    "studyGroup": {"name": "To be created group"},
                },
                {
                    "notificationType": "EMAIL",
                    "occurrence": {
                        "amountOfSeats": 2,
                        "remainingSeats": 2,
                        "seatType": "ENROLMENT_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
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
                        "amountOfSeats": 32,
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
                        "remainingSeats": 32,
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
                        "amountOfSeats": 47,
                        "contactPersons": {"edges": []},
                        "endTime": "2015-05-17T15:09:08+00:00",
                        "maxGroupSize": 761,
                        "minGroupSize": 932,
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
                        "placeId": "Watch media do concern sit enter. Himself from daughter order.",
                        "remainingSeats": 47,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 0,
                        "contactPersons": {"edges": []},
                        "endTime": "2008-06-07T05:04:58+00:00",
                        "maxGroupSize": 796,
                        "minGroupSize": 700,
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
                        "placeId": "Newspaper force newspaper business himself exist.",
                        "remainingSeats": 0,
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
                        "amountOfSeats": 32,
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
                        "remainingSeats": 32,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 24,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-02-02T08:29:39+00:00",
                        "maxGroupSize": 64,
                        "minGroupSize": 136,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "patricia05@campbell-luna.com",
                            "contactPhoneNumber": "+1-299-013-2321x3168",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1973-12-22T08:50:45+00:00",
                            "linkedEventId": "KkSRp",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Wrong when lead involve sport.",
                        "remainingSeats": 24,
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
                        "endTime": "2015-09-20T23:57:56+00:00",
                        "maxGroupSize": 225,
                        "minGroupSize": 551,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "alicehobbs@cole.com",
                            "contactPhoneNumber": "778-840-8746x609",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1983-10-25T22:51:16+00:00",
                            "linkedEventId": "dgihp",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Dog five traditional late majority of generation.",
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
                        "amountOfSeats": 24,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-02-02T08:29:39+00:00",
                        "maxGroupSize": 64,
                        "minGroupSize": 136,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "patricia05@campbell-luna.com",
                            "contactPhoneNumber": "+1-299-013-2321x3168",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1973-12-22T08:50:45+00:00",
                            "linkedEventId": "KkSRp",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Wrong when lead involve sport.",
                        "remainingSeats": 24,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 32,
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
                        "remainingSeats": 32,
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
                        "amountOfSeats": 24,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-02-02T08:29:39+00:00",
                        "maxGroupSize": 64,
                        "minGroupSize": 136,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "patricia05@campbell-luna.com",
                            "contactPhoneNumber": "+1-299-013-2321x3168",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1973-12-22T08:50:45+00:00",
                            "linkedEventId": "KkSRp",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Wrong when lead involve sport.",
                        "remainingSeats": 24,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 32,
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
                        "remainingSeats": 32,
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

snapshots["test_update_enrolment 1"] = {
    "data": {
        "updateEnrolment": {
            "enrolment": {
                "notificationType": "SMS",
                "occurrence": {
                    "amountOfSeats": 35,
                    "remainingSeats": 35,
                    "seatsApproved": 0,
                    "seatsTaken": 0,
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
                        "remainingSeats": 50,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
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
                        "remainingSeats": 50,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
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

snapshots["test_cancel_enrolment_query 1"] = {
    "data": {
        "cancellingEnrolment": {
            "enrolmentTime": "2020-01-04T00:00:00+00:00",
            "occurrence": {"seatsTaken": 0},
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

snapshots["test_study_levels_query 1"] = {
    "data": {
        "studyLevels": {
            "edges": [
                {
                    "node": {
                        "id": "age_0_2",
                        "label": None,
                        "level": 0,
                        "translations": [{"label": "age 0-2", "languageCode": "EN"}],
                    }
                },
                {
                    "node": {
                        "id": "age_3_4",
                        "label": None,
                        "level": 1,
                        "translations": [{"label": "age 3-4", "languageCode": "EN"}],
                    }
                },
                {
                    "node": {
                        "id": "preschool",
                        "label": None,
                        "level": 2,
                        "translations": [{"label": "preschool", "languageCode": "EN"}],
                    }
                },
                {
                    "node": {
                        "id": "grade_1",
                        "label": None,
                        "level": 3,
                        "translations": [
                            {"label": "first grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_2",
                        "label": None,
                        "level": 4,
                        "translations": [
                            {"label": "second grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_3",
                        "label": None,
                        "level": 5,
                        "translations": [
                            {"label": "third grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_4",
                        "label": None,
                        "level": 6,
                        "translations": [
                            {"label": "fourth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_5",
                        "label": None,
                        "level": 7,
                        "translations": [
                            {"label": "fifth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_6",
                        "label": None,
                        "level": 8,
                        "translations": [
                            {"label": "sixth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_7",
                        "label": None,
                        "level": 9,
                        "translations": [
                            {"label": "seventh grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_8",
                        "label": None,
                        "level": 10,
                        "translations": [
                            {"label": "eighth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_9",
                        "label": None,
                        "level": 11,
                        "translations": [
                            {"label": "ninth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "grade_10",
                        "label": None,
                        "level": 12,
                        "translations": [
                            {"label": "tenth grade", "languageCode": "EN"}
                        ],
                    }
                },
                {
                    "node": {
                        "id": "secondary",
                        "label": None,
                        "level": 13,
                        "translations": [{"label": "secondary", "languageCode": "EN"}],
                    }
                },
                {
                    "node": {
                        "id": "other",
                        "label": None,
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
            "label": None,
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
