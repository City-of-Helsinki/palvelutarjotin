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
                        "amountOfAdult": 0,
                        "extraNeeds": "Stay every something base may middle good father. Past ready join enjoy.",
                        "groupName": "Staff read rule point leg within. Staff country actually generation five training.",
                        "groupSize": 631,
                        "occurrences": {"edges": []},
                        "person": {"name": "William Brewer"},
                        "studyLevels": {"edges": []},
                        "unit": {
                            "name": {
                                "fi": """Age else myself yourself.
Range north skin watch."""
                            }
                        },
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
            "amountOfAdult": 0,
            "extraNeeds": "Stay every something base may middle good father. Past ready join enjoy.",
            "groupName": "Staff read rule point leg within. Staff country actually generation five training.",
            "groupSize": 631,
            "occurrences": {"edges": []},
            "person": {"name": "William Brewer"},
            "studyLevels": {"edges": []},
            "unit": {
                "name": {
                    "fi": """Age else myself yourself.
Range north skin watch."""
                }
            },
            "unitId": None,
            "unitName": """Age else myself yourself.
Range north skin watch.""",
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
                        "amountOfSeats": 43,
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
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "zVxeo",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 7,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 43,
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
            "amountOfSeats": 43,
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
                "externalEnrolmentUrl": None,
                "linkedEventId": "zVxeo",
                "mandatoryAdditionalInformation": False,
                "neededOccurrences": 7,
            },
            "placeId": "Record card my. Sure sister return.",
            "remainingSeats": 43,
            "seatsApproved": 0,
            "seatsTaken": 0,
            "startTime": "2013-12-12T04:57:19+00:00",
            "studyGroups": {"edges": []},
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
                "unit": {"name": {"fi": "Sample study group name"}},
                "unitId": None,
                "unitName": "Sample study group name",
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
                "person": {
                    "emailAddress": "torreswilliam@hotmail.com",
                    "language": "FI",
                    "name": "Gregory Flores",
                    "phoneNumber": "001-954-620-0377x221",
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
                "unit": {"name": {"fi": "Sample study group name"}},
                "unitId": None,
                "unitName": "Sample study group name",
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
                "unit": {"name": {"fi": "Sample study group name"}},
                "unitId": None,
                "unitName": "Sample study group name",
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
                "unit": {"name": {"fi": "Sample study group name"}},
                "unitId": None,
                "unitName": "Sample study group name",
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
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 15,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    },
                    "status": "PENDING",
                    "studyGroup": {"unitName": "To be created group"},
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
                    "studyGroup": {"unitName": "To be created group"},
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
                        "amountOfSeats": 1,
                        "contactPersons": {"edges": []},
                        "endTime": "2017-06-24T21:41:59+00:00",
                        "maxGroupSize": 757,
                        "minGroupSize": 175,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "lucaskerr@barrett.com",
                            "contactPhoneNumber": "001-577-794-2677x934",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2005-07-20T18:51:38+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "PbCye",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 8,
                        },
                        "placeId": "Base may middle good father boy economy.",
                        "remainingSeats": 1,
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
                        "amountOfSeats": 43,
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
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 43,
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

snapshots["test_occurrences_filter_by_date 2"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 1,
                        "contactPersons": {"edges": []},
                        "endTime": "2017-06-24T21:41:59+00:00",
                        "maxGroupSize": 757,
                        "minGroupSize": 175,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "lucaskerr@barrett.com",
                            "contactPhoneNumber": "001-577-794-2677x934",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2005-07-20T18:51:38+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "PbCye",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 8,
                        },
                        "placeId": "Base may middle good father boy economy.",
                        "remainingSeats": 1,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 44,
                        "contactPersons": {"edges": []},
                        "endTime": "1985-01-26T08:23:20+00:00",
                        "maxGroupSize": 205,
                        "minGroupSize": 798,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "ujackson@smith.com",
                            "contactPhoneNumber": "038.916.2596",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2008-03-18T14:54:10+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "uvmwr",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Respond yard door indicate.",
                        "remainingSeats": 44,
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
                        "amountOfSeats": 20,
                        "contactPersons": {"edges": []},
                        "endTime": "2010-05-06T15:51:56+00:00",
                        "maxGroupSize": 787,
                        "minGroupSize": 126,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "charlesalexander@gmail.com",
                            "contactPhoneNumber": "001-773-844-5501x240",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2004-03-18T10:24:36+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "katVN",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 4,
                        },
                        "placeId": "I task moment want write her.",
                        "remainingSeats": 20,
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
                        "amountOfSeats": 44,
                        "contactPersons": {"edges": []},
                        "endTime": "1985-01-26T08:23:20+00:00",
                        "maxGroupSize": 205,
                        "minGroupSize": 798,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "ujackson@smith.com",
                            "contactPhoneNumber": "038.916.2596",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2008-03-18T14:54:10+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "uvmwr",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Respond yard door indicate.",
                        "remainingSeats": 44,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 1,
                        "contactPersons": {"edges": []},
                        "endTime": "2017-06-24T21:41:59+00:00",
                        "maxGroupSize": 757,
                        "minGroupSize": 175,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "lucaskerr@barrett.com",
                            "contactPhoneNumber": "001-577-794-2677x934",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2005-07-20T18:51:38+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "PbCye",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 8,
                        },
                        "placeId": "Base may middle good father boy economy.",
                        "remainingSeats": 1,
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
                        "amountOfSeats": 44,
                        "contactPersons": {"edges": []},
                        "endTime": "1985-01-26T08:23:20+00:00",
                        "maxGroupSize": 205,
                        "minGroupSize": 798,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "ujackson@smith.com",
                            "contactPhoneNumber": "038.916.2596",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2008-03-18T14:54:10+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "uvmwr",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Respond yard door indicate.",
                        "remainingSeats": 44,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 1,
                        "contactPersons": {"edges": []},
                        "endTime": "2017-06-24T21:41:59+00:00",
                        "maxGroupSize": 757,
                        "minGroupSize": 175,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "lucaskerr@barrett.com",
                            "contactPhoneNumber": "001-577-794-2677x934",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2005-07-20T18:51:38+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "PbCye",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 8,
                        },
                        "placeId": "Base may middle good father boy economy.",
                        "remainingSeats": 1,
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
            "studyGroup": {"unitName": "Respond yard door indicate."},
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
    """no-reply@hel.ninja|['qlee@hotmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: sgDOo
    Study group: Respond yard door indicate.
    Occurrence: 06.01.2020 02.00
    Person: qlee@hotmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZToyMl8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: custom message
"""
]

snapshots["test_approve_enrolment 2"] = [
    """no-reply@hel.ninja|['qlee@hotmail.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: WsAOP
    Study group: Respond yard door indicate.
    Occurrence: 06.01.2020 02.00
    Person: qlee@hotmail.com
    Click this link to cancel the enrolment:
    https://beta.kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZToyMF8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

"""
]

snapshots["test_decline_enrolment 2"] = [
    """no-reply@hel.ninja|['qlee@hotmail.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: WsAOP
    Study group: Respond yard door indicate.
    Occurrence: 06.01.2020 02.00
    Person: qlee@hotmail.com

""",
    """no-reply@hel.ninja|['qlee@hotmail.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: WsAOP
    Study group: Respond yard door indicate.
    Occurrence: 06.01.2020 02.00
    Person: qlee@hotmail.com

""",
]

snapshots["test_decline_enrolment_with_custom_message 1"] = {
    "data": {"declineEnrolment": {"enrolment": {"status": "DECLINED"}}}
}

snapshots["test_decline_enrolment_with_custom_message 2"] = [
    """no-reply@hel.ninja|['qlee@hotmail.com']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: sgDOo
    Study group: Respond yard door indicate.
    Occurrence: 06.01.2020 02.00
    Person: qlee@hotmail.com

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
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 15,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    },
                    "status": "PENDING",
                    "studyGroup": {"unitName": "To be created group"},
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
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 15,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    },
                    "status": "PENDING",
                    "studyGroup": {"unitName": "To be created group"},
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
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 15,
                        "seatsTaken": 15,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    },
                    "status": "APPROVED",
                    "studyGroup": {"unitName": "To be created group"},
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
                "id": "AMQQN",
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
                    "remainingSeats": 6,
                    "seatsApproved": 0,
                    "seatsTaken": 29,
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
                    "unitName": "Updated name",
                },
            }
        }
    }
}

snapshots["test_cancel_enrolment_query 1"] = {
    "data": {
        "cancellingEnrolment": {
            "enrolmentTime": "2020-01-04T00:00:00+00:00",
            "occurrence": {"seatsTaken": 914},
            "status": "PENDING",
            "studyGroup": {
                "groupSize": 914,
                "unitName": "Family around year off. Sense person the probably.",
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
                        "amountOfSeats": 21,
                        "contactPersons": {"edges": []},
                        "endTime": "1972-06-16T09:28:30+00:00",
                        "maxGroupSize": 714,
                        "minGroupSize": 757,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "underwoodtracy@roach-cruz.biz",
                            "contactPhoneNumber": "+1-345-773-5577x76712",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Father boy economy the.",
                        "remainingSeats": 21,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1992-11-14T16:36:36+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 50,
                        "contactPersons": {"edges": []},
                        "endTime": "2014-06-11T09:34:06+00:00",
                        "maxGroupSize": 653,
                        "minGroupSize": 676,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "underwoodtracy@roach-cruz.biz",
                            "contactPhoneNumber": "+1-345-773-5577x76712",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Affect senior number scene today friend maintain.",
                        "remainingSeats": 50,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2001-06-29T11:05:04+00:00",
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
                        "amountOfSeats": 22,
                        "contactPersons": {"edges": []},
                        "endTime": "1991-01-06T20:05:17+00:00",
                        "maxGroupSize": 932,
                        "minGroupSize": 512,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "underwoodtracy@roach-cruz.biz",
                            "contactPhoneNumber": "+1-345-773-5577x76712",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "List pressure stage history. City sing himself yard.",
                        "remainingSeats": 22,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2005-01-18T03:44:33+00:00",
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
                        "amountOfSeats": 40,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-08-29T21:32:18+00:00",
                        "maxGroupSize": 746,
                        "minGroupSize": 146,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "underwoodtracy@roach-cruz.biz",
                            "contactPhoneNumber": "+1-345-773-5577x76712",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Through resource professional debate produce college able.",
                        "remainingSeats": 40,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2007-09-11T17:25:39+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 48,
                        "contactPersons": {"edges": []},
                        "endTime": "1970-02-24T07:17:56+00:00",
                        "maxGroupSize": 354,
                        "minGroupSize": 236,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "underwoodtracy@roach-cruz.biz",
                            "contactPhoneNumber": "+1-345-773-5577x76712",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Traditional after born up always sport.",
                        "remainingSeats": 48,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2015-03-06T08:18:33+00:00",
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
                        "amountOfSeats": 35,
                        "contactPersons": {"edges": []},
                        "endTime": "1970-02-26T13:28:56+00:00",
                        "maxGroupSize": 846,
                        "minGroupSize": 568,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "hannah75@gmail.com",
                            "contactPhoneNumber": "144-948-1188x4524",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1980-10-23T00:23:16+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "fGJRg",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Who Mrs public east site chance.",
                        "remainingSeats": 35,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1989-09-05T13:18:43+00:00",
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
                        "amountOfSeats": 44,
                        "contactPersons": {"edges": []},
                        "endTime": "1985-01-26T08:23:20+00:00",
                        "maxGroupSize": 205,
                        "minGroupSize": 798,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "ujackson@smith.com",
                            "contactPhoneNumber": "038.916.2596",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2008-03-18T14:54:10+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "uvmwr",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Respond yard door indicate.",
                        "remainingSeats": 44,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 43,
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
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 43,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 1,
                        "contactPersons": {"edges": []},
                        "endTime": "2017-06-24T21:41:59+00:00",
                        "maxGroupSize": 757,
                        "minGroupSize": 175,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "lucaskerr@barrett.com",
                            "contactPhoneNumber": "001-577-794-2677x934",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2005-07-20T18:51:38+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "PbCye",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 8,
                        },
                        "placeId": "Base may middle good father boy economy.",
                        "remainingSeats": 1,
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
                        "amountOfSeats": 1,
                        "contactPersons": {"edges": []},
                        "endTime": "2017-06-24T21:41:59+00:00",
                        "maxGroupSize": 757,
                        "minGroupSize": 175,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "lucaskerr@barrett.com",
                            "contactPhoneNumber": "001-577-794-2677x934",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2005-07-20T18:51:38+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "PbCye",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 8,
                        },
                        "placeId": "Base may middle good father boy economy.",
                        "remainingSeats": 1,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-07T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 43,
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
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 43,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 44,
                        "contactPersons": {"edges": []},
                        "endTime": "1985-01-26T08:23:20+00:00",
                        "maxGroupSize": 205,
                        "minGroupSize": 798,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "ujackson@smith.com",
                            "contactPhoneNumber": "038.916.2596",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2008-03-18T14:54:10+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "uvmwr",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Respond yard door indicate.",
                        "remainingSeats": 44,
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
                        "amountOfSeats": 44,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-05T00:00:00+00:00",
                        "maxGroupSize": 205,
                        "minGroupSize": 798,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "ujackson@smith.com",
                            "contactPhoneNumber": "038.916.2596",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2008-03-18T14:54:10+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "uvmwr",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Respond yard door indicate.",
                        "remainingSeats": 44,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1985-01-26T08:23:20+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 43,
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
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 43,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 1,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-07T00:00:00+00:00",
                        "maxGroupSize": 757,
                        "minGroupSize": 175,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "lucaskerr@barrett.com",
                            "contactPhoneNumber": "001-577-794-2677x934",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2005-07-20T18:51:38+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "PbCye",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 8,
                        },
                        "placeId": "Base may middle good father boy economy.",
                        "remainingSeats": 1,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2017-06-24T21:41:59+00:00",
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
                        "amountOfSeats": 1,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-07T00:00:00+00:00",
                        "maxGroupSize": 757,
                        "minGroupSize": 175,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "lucaskerr@barrett.com",
                            "contactPhoneNumber": "001-577-794-2677x934",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2005-07-20T18:51:38+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "PbCye",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 8,
                        },
                        "placeId": "Base may middle good father boy economy.",
                        "remainingSeats": 1,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2017-06-24T21:41:59+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 43,
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
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 43,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 44,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-05T00:00:00+00:00",
                        "maxGroupSize": 205,
                        "minGroupSize": 798,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "ujackson@smith.com",
                            "contactPhoneNumber": "038.916.2596",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2008-03-18T14:54:10+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "uvmwr",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Respond yard door indicate.",
                        "remainingSeats": 44,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1985-01-26T08:23:20+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_upcoming[None-3] 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 18,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-02-09T12:33:37+00:00",
                        "maxGroupSize": 75,
                        "minGroupSize": 879,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "codyramirez@gmail.com",
                            "contactPhoneNumber": "+1-333-457-7355x777",
                            "enrolmentEndDays": None,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Throw wrong party wall agency customer clear.",
                        "remainingSeats": 18,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 18,
                        "contactPersons": {"edges": []},
                        "endTime": "2004-11-01T19:25:53+00:00",
                        "maxGroupSize": 53,
                        "minGroupSize": 312,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "codyramirez@gmail.com",
                            "contactPhoneNumber": "+1-333-457-7355x777",
                            "enrolmentEndDays": None,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Figure foreign go age member.",
                        "remainingSeats": 18,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 37,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-04-01T13:16:53+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "codyramirez@gmail.com",
                            "contactPhoneNumber": "+1-333-457-7355x777",
                            "enrolmentEndDays": None,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Think significant land especially can quite.",
                        "remainingSeats": 37,
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

snapshots["test_occurrences_filter_by_upcoming[0-3] 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 18,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-02-09T12:33:37+00:00",
                        "maxGroupSize": 75,
                        "minGroupSize": 879,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "codyramirez@gmail.com",
                            "contactPhoneNumber": "+1-333-457-7355x777",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Throw wrong party wall agency customer clear.",
                        "remainingSeats": 18,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 18,
                        "contactPersons": {"edges": []},
                        "endTime": "2004-11-01T19:25:53+00:00",
                        "maxGroupSize": 53,
                        "minGroupSize": 312,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "codyramirez@gmail.com",
                            "contactPhoneNumber": "+1-333-457-7355x777",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Figure foreign go age member.",
                        "remainingSeats": 18,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 37,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-04-01T13:16:53+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "codyramirez@gmail.com",
                            "contactPhoneNumber": "+1-333-457-7355x777",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Think significant land especially can quite.",
                        "remainingSeats": 37,
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

snapshots["test_occurrences_filter_by_upcoming[1-2] 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 18,
                        "contactPersons": {"edges": []},
                        "endTime": "2004-11-01T19:25:53+00:00",
                        "maxGroupSize": 53,
                        "minGroupSize": 312,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "codyramirez@gmail.com",
                            "contactPhoneNumber": "+1-333-457-7355x777",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Figure foreign go age member.",
                        "remainingSeats": 18,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 37,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-04-01T13:16:53+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "codyramirez@gmail.com",
                            "contactPhoneNumber": "+1-333-457-7355x777",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Think significant land especially can quite.",
                        "remainingSeats": 37,
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

snapshots["test_delete_unpublished_occurrence 1"] = {
    "data": {"deleteOccurrence": {"__typename": "DeleteOccurrenceMutationPayload"}}
}

snapshots["test_update_unpublished_occurrence 1"] = {
    "data": {
        "updateOccurrence": {
            "occurrence": {
                "contactPersons": {"edges": [{"node": {"name": "Thomas Conway"}}]},
                "endTime": "2020-05-06T00:00:00+00:00",
                "languages": {
                    "edges": [
                        {"node": {"id": "en", "name": "English"}},
                        {"node": {"id": "fi", "name": "Finnish"}},
                        {"node": {"id": "sv", "name": "Swedish"}},
                    ]
                },
                "maxGroupSize": 793,
                "minGroupSize": 10,
                "pEvent": {
                    "contactEmail": "mcdanielmonica@yahoo.com",
                    "contactPhoneNumber": "540.389.1625x965",
                    "enrolmentEndDays": 1,
                    "enrolmentStart": "1999-07-28T05:19:09+00:00",
                    "externalEnrolmentUrl": None,
                    "linkedEventId": "VkleI",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 8,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
            }
        }
    }
}

snapshots["test_update_occurrence_of_published_event_without_enrolments 1"] = {
    "data": {
        "updateOccurrence": {
            "occurrence": {
                "contactPersons": {"edges": [{"node": {"name": "Corey Holland"}}]},
                "endTime": "2020-05-06T00:00:00+00:00",
                "languages": {
                    "edges": [
                        {"node": {"id": "en", "name": "English"}},
                        {"node": {"id": "fi", "name": "Finnish"}},
                        {"node": {"id": "sv", "name": "Swedish"}},
                    ]
                },
                "maxGroupSize": 10,
                "minGroupSize": 10,
                "pEvent": {
                    "contactEmail": "molinamichael@mccoy.com",
                    "contactPhoneNumber": "636-588-2540x3891",
                    "enrolmentEndDays": 0,
                    "enrolmentStart": "2021-07-24T21:32:11+00:00",
                    "externalEnrolmentUrl": None,
                    "linkedEventId": "helsinki:afxp6tv4xa",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 3,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
            }
        }
    }
}

snapshots["test_add_occurrence_to_published_event 1"] = {
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
                    "contactEmail": "alexandra95@gray.biz",
                    "contactPhoneNumber": "(959)911-8326",
                    "enrolmentEndDays": 1,
                    "enrolmentStart": "2020-03-08T01:43:57+00:00",
                    "externalEnrolmentUrl": None,
                    "linkedEventId": "HWJti",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 2,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
            }
        }
    }
}

snapshots["test_add_occurrence_to_unpublished_event 1"] = {
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
                    "contactEmail": "alexandra95@gray.biz",
                    "contactPhoneNumber": "(959)911-8326",
                    "enrolmentEndDays": 1,
                    "enrolmentStart": "2020-03-08T01:43:57+00:00",
                    "externalEnrolmentUrl": None,
                    "linkedEventId": "HWJti",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 2,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
            }
        }
    }
}
