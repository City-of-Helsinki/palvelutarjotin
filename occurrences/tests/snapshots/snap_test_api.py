# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_add_occurrence_to_published_event 1"] = {
    "data": {
        "addOccurrence": {
            "occurrence": {
                "contactPersons": {
                    "edges": [
                        {"node": {"name": "New name"}},
                        {"node": {"name": "Sean Rocha"}},
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
                    "contactEmail": "kariweber@example.org",
                    "contactPhoneNumber": "(171)341-1450",
                    "enrolmentEndDays": 0,
                    "enrolmentStart": "1983-11-13T03:03:17+00:00",
                    "externalEnrolmentUrl": None,
                    "linkedEventId": "QoxZH",
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
                        {"node": {"name": "New name"}},
                        {"node": {"name": "Sean Rocha"}},
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
                    "contactEmail": "kariweber@example.org",
                    "contactPhoneNumber": "(171)341-1450",
                    "enrolmentEndDays": 0,
                    "enrolmentStart": "1983-11-13T03:03:17+00:00",
                    "externalEnrolmentUrl": None,
                    "linkedEventId": "QoxZH",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 2,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
            }
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
                "unit": {
                    "internalId": "https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/",
                    "name": {"fi": "Raija Malka & Kaija Saariaho: Blick"},
                },
                "unitId": "helsinki:afxp6tv4xa",
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
                    "emailAddress": "barrettjason@example.org",
                    "language": "FI",
                    "name": "Charles Anderson",
                    "phoneNumber": "134.114.5089x299",
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
                "unit": {
                    "internalId": "https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/",
                    "name": {"fi": "Raija Malka & Kaija Saariaho: Blick"},
                },
                "unitId": "helsinki:afxp6tv4xa",
                "unitName": "Sample study group name",
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

snapshots["test_approve_enrolment 1"] = {
    "data": {"approveEnrolment": {"enrolment": {"status": "APPROVED"}}}
}

snapshots["test_approve_enrolment 2"] = [
    """no-reply@hel.ninja|['barrettjason@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: FffUP
    Study group: Build natural middle however.
    Occurrence: 06.01.2020 02.00
    Person: barrettjason@example.org
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTozOF8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

"""
]

snapshots["test_approve_enrolment_with_custom_message 1"] = {
    "data": {"approveEnrolment": {"enrolment": {"status": "APPROVED"}}}
}

snapshots["test_approve_enrolment_with_custom_message 2"] = [
    """no-reply@hel.ninja|['barrettjason@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: nmvjB
    Study group: Build natural middle however.
    Occurrence: 06.01.2020 02.00
    Person: barrettjason@example.org
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTo0MF8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: custom message
"""
]

snapshots["test_ask_for_cancelled_confirmation_mutation 1"] = {
    "data": {"cancelEnrolment": {"enrolment": {"status": "PENDING"}}}
}

snapshots[
    "test_auto_accept_message_is_used_as_custom_message_in_auto_approved_enrolments[False] 1"
] = {
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

snapshots[
    "test_auto_accept_message_is_used_as_custom_message_in_auto_approved_enrolments[True] 1"
] = {
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

snapshots[
    "test_auto_accept_message_is_used_as_custom_message_in_auto_approved_enrolments[True] 2"
] = [
    """no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: RUkQL
    Study group: To be created group
    Occurrence: 06.01.2020 02.00
    Person: hutchinsonrachel@example.org

    Custom message: Testing auto acceptance message
"""
]

snapshots["test_cancel_enrolment_mutation 1"] = {
    "data": {"cancelEnrolment": {"enrolment": {"status": "CANCELLED"}}}
}

snapshots["test_cancel_enrolment_query 1"] = {
    "data": {
        "cancellingEnrolment": {
            "enrolmentTime": "2020-01-04T00:00:00+00:00",
            "occurrence": {"seatsTaken": 2},
            "status": "PENDING",
            "studyGroup": {
                "groupSize": 2,
                "unitName": "Tough plant traditional after born up always. Return student light a point charge.",
            },
        }
    }
}

snapshots["test_cancel_occurrence 1"] = {
    "data": {"cancelOccurrence": {"occurrence": {"cancelled": True}}}
}

snapshots["test_decline_enrolment 1"] = {
    "data": {"declineEnrolment": {"enrolment": {"status": "DECLINED"}}}
}

snapshots["test_decline_enrolment 2"] = [
    """no-reply@hel.ninja|['barrettjason@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: FffUP
    Study group: Build natural middle however.
    Occurrence: 06.01.2020 02.00
    Person: barrettjason@example.org

""",
    """no-reply@hel.ninja|['barrettjason@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: FffUP
    Study group: Build natural middle however.
    Occurrence: 06.01.2020 02.00
    Person: barrettjason@example.org

""",
]

snapshots["test_decline_enrolment_with_custom_message 1"] = {
    "data": {"declineEnrolment": {"enrolment": {"status": "DECLINED"}}}
}

snapshots["test_decline_enrolment_with_custom_message 2"] = [
    """no-reply@hel.ninja|['barrettjason@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: nmvjB
    Study group: Build natural middle however.
    Occurrence: 06.01.2020 02.00
    Person: barrettjason@example.org

    Custom message: custom message
"""
]

snapshots["test_delete_cancelled_occurrence 1"] = {
    "data": {"deleteOccurrence": {"__typename": "DeleteOccurrenceMutationPayload"}}
}

snapshots["test_delete_unpublished_occurrence 1"] = {
    "data": {"deleteOccurrence": {"__typename": "DeleteOccurrenceMutationPayload"}}
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

snapshots["test_enrol_event_queue_mutation 1"] = {
    "data": {
        "enrolEventQueue": {
            "eventQueueEnrolment": {
                "notificationType": "EMAIL_SMS",
                "pEvent": {
                    "autoAcceptance": False,
                    "contactEmail": "patriciacervantes@example.net",
                    "contactPhoneNumber": "001-990-132-3213x16804",
                    "enrolmentEndDays": 2,
                    "enrolmentStart": "2020-01-01T02:17:13+00:00",
                    "externalEnrolmentUrl": None,
                    "isQueueingAllowed": True,
                    "linkedEventId": "kSRpd",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 2,
                },
                "status": "HAS_NO_ENROLMENTS",
                "studyGroup": {
                    "preferredTimes": "Only tuesdays",
                    "unitName": "To be created group",
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

snapshots["test_enrolment_query 1"] = {
    "data": {
        "enrolment": {
            "occurrence": {
                "endTime": "2016-03-08T13:11:25+00:00",
                "pEvent": {"linkedEventId": "ZwGmN"},
                "seatsTaken": 374,
                "startTime": "1974-09-11T09:28:35+00:00",
            },
            "status": "PENDING",
            "studyGroup": {"groupName": "Conference thing much like test."},
        }
    }
}

snapshots["test_enrolments_summary 1"] = {
    "data": {
        "enrolmentSummary": {
            "count": 4,
            "edges": [
                {"node": {"status": "APPROVED"}},
                {"node": {"status": "CANCELLED"}},
                {"node": {"status": "DECLINED"}},
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

snapshots["test_event_queue_enrolment_query 1"] = {
    "data": {
        "eventQueueEnrolment": {
            "pEvent": {"isQueueingAllowed": True, "linkedEventId": "twlFn"},
            "status": "HAS_NO_ENROLMENTS",
            "studyGroup": {"groupName": "Six feel real fast.", "preferredTimes": ""},
        }
    }
}

snapshots["test_event_queue_enrolments_query 1"] = {
    "data": {
        "eventQueueEnrolments": {
            "count": 15,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Player bad capital of song add. Democratic imagine yes policy.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Phone someone method threat. You decide the threat organization. Good career party offer.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjI=",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Threat kitchen table along evening need line. Mission once pretty. Nor heavy well brother.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjM=",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "First control education list full hotel. Get future stand watch college speech but.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjQ=",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Then instead set part us happy.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjU=",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Commercial lose add bag.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjY=",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Herself personal office could mouth mean space. Purpose get miss also wind.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjc=",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Simple spend decade born. Day range age.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjg=",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Audience we cultural quality serious stay. Treat owner door everybody check manager huge.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjk=",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Want character would. Dream entire account. If bring cut sign force future or spend.",
                            "preferredTimes": "",
                        },
                    },
                },
            ],
        }
    }
}

snapshots["test_event_queue_enrolments_query 2"] = {
    "data": {
        "eventQueueEnrolments": {
            "count": 15,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjEw",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Edge since certainly visit. Majority opportunity summer laugh interview put key. Much prove eight.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjEx",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Agree order just raise change. Out instead matter owner beyond executive. Defense field east.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjEy",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "High three wear offer. Need positive range including growth by. Series instead task build public.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjEz",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Resource set feeling within Mr total learn.",
                            "preferredTimes": "",
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE0",
                    "node": {
                        "pEvent": {
                            "isQueueingAllowed": True,
                            "linkedEventId": "twlFn",
                            "organisation": {"name": "Graves and Sons"},
                        },
                        "status": "HAS_NO_ENROLMENTS",
                        "studyGroup": {
                            "groupName": "Policy parent toward apply see on send in. Full three especially card animal recognize stock.",
                            "preferredTimes": "",
                        },
                    },
                },
            ],
        }
    }
}

snapshots["test_language_query 1"] = {
    "data": {"language": {"id": "aAVEavNlmo", "name": "Him question stay."}}
}

snapshots["test_languagess_query 1"] = {
    "data": {
        "languages": {
            "edges": [
                {"node": {"id": "ar", "name": "Arabic"}},
                {"node": {"id": "zh_hans", "name": "Chinese"}},
                {"node": {"id": "en", "name": "English"}},
                {"node": {"id": "fi", "name": "Finnish"}},
                {"node": {"id": "aAVEavNlmo", "name": "Him question stay."}},
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

snapshots["test_occurrence_query 1"] = {
    "data": {
        "occurrence": {
            "amountOfSeats": 33,
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
                "contactEmail": "bthomas@example.org",
                "contactPhoneNumber": "(064)976-3803x466",
                "enrolmentEndDays": 1,
                "enrolmentStart": "1971-08-19T21:08:32+00:00",
                "externalEnrolmentUrl": None,
                "linkedEventId": "zVxeo",
                "mandatoryAdditionalInformation": False,
                "neededOccurrences": 7,
            },
            "placeId": "Record card my. Sure sister return.",
            "remainingSeats": 33,
            "seatsApproved": 0,
            "seatsTaken": 0,
            "startTime": "2013-12-12T04:57:19+00:00",
        }
    }
}

snapshots["test_occurrences_filter_by_cancelled 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 22,
                        "contactPersons": {"edges": []},
                        "endTime": "1989-12-24T03:25:16+00:00",
                        "maxGroupSize": 75,
                        "minGroupSize": 879,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "dsellers@example.net",
                            "contactPhoneNumber": "345.773.5577",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Throw wrong party wall agency customer clear.",
                        "remainingSeats": 22,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1975-02-09T12:33:37+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 48,
                        "contactPersons": {"edges": []},
                        "endTime": "1989-06-18T13:55:21+00:00",
                        "maxGroupSize": 53,
                        "minGroupSize": 312,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "dsellers@example.net",
                            "contactPhoneNumber": "345.773.5577",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Actually generation five training thought.",
                        "remainingSeats": 48,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2004-11-01T19:25:53+00:00",
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
                        "amountOfSeats": 12,
                        "contactPersons": {"edges": []},
                        "endTime": "2009-12-31T21:53:37+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "dsellers@example.net",
                            "contactPhoneNumber": "345.773.5577",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Think significant land especially can quite.",
                        "remainingSeats": 12,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2000-04-01T13:16:53+00:00",
                    }
                }
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
                        "amountOfSeats": 14,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-04-01T13:16:53+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "huntveronica@example.net",
                            "contactPhoneNumber": "462-003-7722x18274",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2004-09-22T07:20:17+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "Qjarq",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Today friend maintain marriage ok thank realize.",
                        "remainingSeats": 14,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
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
                        "amountOfSeats": 14,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-04-01T13:16:53+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "huntveronica@example.net",
                            "contactPhoneNumber": "462-003-7722x18274",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2004-09-22T07:20:17+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "Qjarq",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Today friend maintain marriage ok thank realize.",
                        "remainingSeats": 14,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "1973-03-29T15:33:10+00:00",
                        "maxGroupSize": 285,
                        "minGroupSize": 350,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "zsilva@example.org",
                            "contactPhoneNumber": "001-651-263-0084x6547",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1993-11-02T08:53:37+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "jGwiN",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Traditional whether serious sister work.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_enrollable[0-3] 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 40,
                        "contactPersons": {"edges": []},
                        "endTime": "2014-12-28T01:38:36+00:00",
                        "maxGroupSize": 749,
                        "minGroupSize": 958,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Name likely behind mission network who.",
                        "remainingSeats": 40,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 2,
                        "contactPersons": {"edges": []},
                        "endTime": "1992-11-14T16:36:36+00:00",
                        "maxGroupSize": 714,
                        "minGroupSize": 757,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Father boy economy the.",
                        "remainingSeats": 2,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 22,
                        "contactPersons": {"edges": []},
                        "endTime": "1991-01-06T20:05:17+00:00",
                        "maxGroupSize": 527,
                        "minGroupSize": 932,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": 0,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Capital city sing himself yard stuff.",
                        "remainingSeats": 22,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-07T00:00:00+00:00",
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_enrollable[1-2] 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 2,
                        "contactPersons": {"edges": []},
                        "endTime": "1992-11-14T16:36:36+00:00",
                        "maxGroupSize": 714,
                        "minGroupSize": 757,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Father boy economy the.",
                        "remainingSeats": 2,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 22,
                        "contactPersons": {"edges": []},
                        "endTime": "1991-01-06T20:05:17+00:00",
                        "maxGroupSize": 527,
                        "minGroupSize": 932,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Capital city sing himself yard stuff.",
                        "remainingSeats": 22,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-07T00:00:00+00:00",
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_filter_by_enrollable[None-3] 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 40,
                        "contactPersons": {"edges": []},
                        "endTime": "2014-12-28T01:38:36+00:00",
                        "maxGroupSize": 749,
                        "minGroupSize": 958,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": None,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Name likely behind mission network who.",
                        "remainingSeats": 40,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 2,
                        "contactPersons": {"edges": []},
                        "endTime": "1992-11-14T16:36:36+00:00",
                        "maxGroupSize": 714,
                        "minGroupSize": 757,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": None,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Father boy economy the.",
                        "remainingSeats": 2,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 22,
                        "contactPersons": {"edges": []},
                        "endTime": "1991-01-06T20:05:17+00:00",
                        "maxGroupSize": 527,
                        "minGroupSize": 932,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": None,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Capital city sing himself yard stuff.",
                        "remainingSeats": 22,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-07T00:00:00+00:00",
                    }
                },
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
                        "amountOfSeats": 8,
                        "contactPersons": {"edges": []},
                        "endTime": "1986-10-16T20:29:23+00:00",
                        "maxGroupSize": 687,
                        "minGroupSize": 225,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "dsellers@example.net",
                            "contactPhoneNumber": "345.773.5577",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Light a point charge stand store.",
                        "remainingSeats": 8,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1974-10-19T15:53:39+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 27,
                        "contactPersons": {"edges": []},
                        "endTime": "1997-12-26T00:43:56+00:00",
                        "maxGroupSize": 459,
                        "minGroupSize": 568,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "dsellers@example.net",
                            "contactPhoneNumber": "345.773.5577",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1998-07-06T01:19:12+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Chance of performance financial.",
                        "remainingSeats": 27,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1989-07-01T22:41:54+00:00",
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
                        "amountOfSeats": 45,
                        "contactPersons": {"edges": []},
                        "endTime": "1978-10-04T07:23:05+00:00",
                        "maxGroupSize": 464,
                        "minGroupSize": 526,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "jonathan20@example.org",
                            "contactPhoneNumber": "001-779-340-5555x089",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2017-02-20T07:43:47+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "rzzET",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Old affect quite.",
                        "remainingSeats": 45,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1971-10-08T22:49:29+00:00",
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
                        "amountOfSeats": 33,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-12-12T04:57:19+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "eduncan@example.org",
                            "contactPhoneNumber": "(750)649-7638x0346",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1988-11-29T04:01:36+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 33,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T10:00:00+00:00",
                    }
                }
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
                        "amountOfSeats": 24,
                        "contactPersons": {"edges": []},
                        "endTime": "1970-05-06T08:51:57+00:00",
                        "maxGroupSize": 288,
                        "minGroupSize": 67,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "pwilliams@example.org",
                            "contactPhoneNumber": "377.940.2178x77950",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2005-08-24T18:22:59+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "nVTDE",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 3,
                        },
                        "placeId": "Few eye first walk west six feel. Fast authority key crime.",
                        "remainingSeats": 24,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T12:00:00+00:00",
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
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "1973-03-29T15:33:10+00:00",
                        "maxGroupSize": 285,
                        "minGroupSize": 350,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "zsilva@example.org",
                            "contactPhoneNumber": "001-651-263-0084x6547",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1993-11-02T08:53:37+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "jGwiN",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Traditional whether serious sister work.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 14,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-04-01T13:16:53+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "huntveronica@example.net",
                            "contactPhoneNumber": "462-003-7722x18274",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2004-09-22T07:20:17+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "Qjarq",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Today friend maintain marriage ok thank realize.",
                        "remainingSeats": 14,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T11:00:00+00:00",
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
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "1973-03-29T15:33:10+00:00",
                        "maxGroupSize": 285,
                        "minGroupSize": 350,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "zsilva@example.org",
                            "contactPhoneNumber": "001-651-263-0084x6547",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1993-11-02T08:53:37+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "jGwiN",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Traditional whether serious sister work.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 14,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-04-01T13:16:53+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "huntveronica@example.net",
                            "contactPhoneNumber": "462-003-7722x18274",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2004-09-22T07:20:17+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "Qjarq",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Today friend maintain marriage ok thank realize.",
                        "remainingSeats": 14,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T11:00:00+00:00",
                    }
                },
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
                        "amountOfSeats": 32,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-05T00:00:00+00:00",
                        "maxGroupSize": 53,
                        "minGroupSize": 312,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": 10,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Staff country actually generation five training.",
                        "remainingSeats": 32,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-04T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 41,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-06T00:00:00+00:00",
                        "maxGroupSize": 1000,
                        "minGroupSize": 984,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": 10,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Senior number scene today friend maintain marriage.",
                        "remainingSeats": 41,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 1,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-07T00:00:00+00:00",
                        "maxGroupSize": 557,
                        "minGroupSize": 345,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "thompsonjessica@example.com",
                            "contactPhoneNumber": "001-333-457-7355x77767",
                            "enrolmentEndDays": 10,
                            "enrolmentStart": "2020-01-05T00:00:00+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "aAVEa",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 6,
                        },
                        "placeId": "Central situation past ready join enjoy.",
                        "remainingSeats": 1,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
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
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-05T00:00:00+00:00",
                        "maxGroupSize": 285,
                        "minGroupSize": 350,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "zsilva@example.org",
                            "contactPhoneNumber": "001-651-263-0084x6547",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1993-11-02T08:53:37+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "jGwiN",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Traditional whether serious sister work.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1973-03-29T15:33:10+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 33,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-06T00:00:00+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "eduncan@example.org",
                            "contactPhoneNumber": "(750)649-7638x0346",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1988-11-29T04:01:36+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 33,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 14,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-07T00:00:00+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "huntveronica@example.net",
                            "contactPhoneNumber": "462-003-7722x18274",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2004-09-22T07:20:17+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "Qjarq",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Today friend maintain marriage ok thank realize.",
                        "remainingSeats": 14,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2000-04-01T13:16:53+00:00",
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
                        "amountOfSeats": 14,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-07T00:00:00+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "huntveronica@example.net",
                            "contactPhoneNumber": "462-003-7722x18274",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2004-09-22T07:20:17+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "Qjarq",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Today friend maintain marriage ok thank realize.",
                        "remainingSeats": 14,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2000-04-01T13:16:53+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 33,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-06T00:00:00+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "eduncan@example.org",
                            "contactPhoneNumber": "(750)649-7638x0346",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1988-11-29T04:01:36+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 33,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-05T00:00:00+00:00",
                        "maxGroupSize": 285,
                        "minGroupSize": 350,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "zsilva@example.org",
                            "contactPhoneNumber": "001-651-263-0084x6547",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1993-11-02T08:53:37+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "jGwiN",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Traditional whether serious sister work.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1973-03-29T15:33:10+00:00",
                    }
                },
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
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "1973-03-29T15:33:10+00:00",
                        "maxGroupSize": 285,
                        "minGroupSize": 350,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "zsilva@example.org",
                            "contactPhoneNumber": "001-651-263-0084x6547",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1993-11-02T08:53:37+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "jGwiN",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Traditional whether serious sister work.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 33,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-12-12T04:57:19+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "eduncan@example.org",
                            "contactPhoneNumber": "(750)649-7638x0346",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1988-11-29T04:01:36+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 33,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 14,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-04-01T13:16:53+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "huntveronica@example.net",
                            "contactPhoneNumber": "462-003-7722x18274",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2004-09-22T07:20:17+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "Qjarq",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Today friend maintain marriage ok thank realize.",
                        "remainingSeats": 14,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-07T00:00:00+00:00",
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
                        "amountOfSeats": 14,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-04-01T13:16:53+00:00",
                        "maxGroupSize": 808,
                        "minGroupSize": 974,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "huntveronica@example.net",
                            "contactPhoneNumber": "462-003-7722x18274",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2004-09-22T07:20:17+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "Qjarq",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 9,
                        },
                        "placeId": "Today friend maintain marriage ok thank realize.",
                        "remainingSeats": 14,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-07T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 33,
                        "contactPersons": {"edges": []},
                        "endTime": "2013-12-12T04:57:19+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "eduncan@example.org",
                            "contactPhoneNumber": "(750)649-7638x0346",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1988-11-29T04:01:36+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "OzVxe",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 0,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 33,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "1973-03-29T15:33:10+00:00",
                        "maxGroupSize": 285,
                        "minGroupSize": 350,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "zsilva@example.org",
                            "contactPhoneNumber": "001-651-263-0084x6547",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "1993-11-02T08:53:37+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "jGwiN",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Traditional whether serious sister work.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                    }
                },
            ]
        }
    }
}

snapshots["test_occurrences_query 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 33,
                        "contactPersons": {"edges": []},
                        "endTime": "2000-08-18T23:27:03+00:00",
                        "maxGroupSize": 383,
                        "minGroupSize": 341,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "bthomas@example.org",
                            "contactPhoneNumber": "(064)976-3803x466",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1971-08-19T21:08:32+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "zVxeo",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 7,
                        },
                        "placeId": "Record card my. Sure sister return.",
                        "remainingSeats": 33,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                    }
                }
            ]
        }
    }
}

snapshots["test_pick_enrolment_from_queue 1"] = {
    "data": {
        "pickEnrolmentFromQueue": {
            "enrolment": {
                "notificationType": "EMAIL",
                "person": {
                    "emailAddress": "guerrajesse@example.org",
                    "name": "John Smith",
                },
                "status": "PENDING",
                "studyGroup": {"groupName": "Six feel real fast."},
            }
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

snapshots["test_unenrol_event_queue_mutation[False] 1"] = {
    "data": {
        "unenrolEventQueue": {
            "pEvent": {"isQueueingAllowed": False, "linkedEventId": "kytNN"},
            "studyGroup": {
                "unitName": "Tough plant traditional after born up always. Return student light a point charge."
            },
        }
    }
}

snapshots["test_unenrol_event_queue_mutation[True] 1"] = {
    "data": {
        "unenrolEventQueue": {
            "pEvent": {"isQueueingAllowed": True, "linkedEventId": "kytNN"},
            "studyGroup": {
                "unitName": "Tough plant traditional after born up always. Return student light a point charge."
            },
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
            "studyGroup": {"unitName": "Build natural middle however."},
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

snapshots["test_update_occurrence_of_published_event_without_enrolments 1"] = {
    "data": {
        "updateOccurrence": {
            "occurrence": {
                "contactPersons": {"edges": [{"node": {"name": "Jamie Alvarez DDS"}}]},
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
                    "contactEmail": "erogers@example.org",
                    "contactPhoneNumber": "(882)540-3891x625",
                    "enrolmentEndDays": 0,
                    "enrolmentStart": "2014-07-18T09:56:19+00:00",
                    "externalEnrolmentUrl": None,
                    "linkedEventId": "helsinki:afxp6tv4xa",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 6,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
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
                "unit": {
                    "internalId": "https://api.hel.fi/linkedevents/v1/place/tprek:15417/",
                    "name": {"fi": "Sellon kirjasto"},
                },
                "unitId": "helsinki:afxp6tv4xa",
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
                    "emailAddress": "shawndouglas@example.com",
                    "language": "FI",
                    "name": "Sean Rocha",
                    "phoneNumber": "001-159-102-3202x81307",
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
                "unit": {
                    "internalId": "https://api.hel.fi/linkedevents/v1/place/tprek:15417/",
                    "name": {"fi": "Sellon kirjasto"},
                },
                "unitId": "helsinki:afxp6tv4xa",
                "unitName": "Sample study group name",
            }
        }
    }
}

snapshots["test_update_unpublished_occurrence 1"] = {
    "data": {
        "updateOccurrence": {
            "occurrence": {
                "contactPersons": {"edges": [{"node": {"name": "Kathryn Hill"}}]},
                "endTime": "2020-05-06T00:00:00+00:00",
                "languages": {
                    "edges": [
                        {"node": {"id": "en", "name": "English"}},
                        {"node": {"id": "fi", "name": "Finnish"}},
                        {"node": {"id": "sv", "name": "Swedish"}},
                    ]
                },
                "maxGroupSize": 588,
                "minGroupSize": 10,
                "pEvent": {
                    "contactEmail": "oharrell@example.org",
                    "contactPhoneNumber": "+1-916-259-6512",
                    "enrolmentEndDays": 0,
                    "enrolmentStart": "1988-12-31T00:41:31+00:00",
                    "externalEnrolmentUrl": None,
                    "linkedEventId": "mwrDP",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 3,
                },
                "startTime": "2020-05-05T00:00:00+00:00",
            }
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
                "id": "Irtal",
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
            "description": "Answer entire increase thank certainly again thought. Beyond than trial western.",
            "hasAreaForGroupWork": False,
            "hasClothingStorage": False,
            "hasIndoorPlayingArea": False,
            "hasOutdoorPlayingArea": False,
            "hasSnackEatingPlace": True,
            "hasToiletNearby": False,
            "id": "PcMpy",
            "outdoorActivity": False,
            "translations": [
                {
                    "description": "Answer entire increase thank certainly again thought. Beyond than trial western."
                }
            ],
        }
    }
}

snapshots["test_venues_query 1"] = {
    "data": {
        "venues": {
            "edges": [
                {
                    "node": {
                        "description": "Answer entire increase thank certainly again thought. Beyond than trial western.",
                        "hasAreaForGroupWork": False,
                        "hasClothingStorage": False,
                        "hasIndoorPlayingArea": False,
                        "hasOutdoorPlayingArea": False,
                        "hasSnackEatingPlace": True,
                        "hasToiletNearby": False,
                        "id": "PcMpy",
                        "outdoorActivity": False,
                        "translations": [
                            {
                                "description": "Answer entire increase thank certainly again thought. Beyond than trial western."
                            }
                        ],
                    }
                }
            ]
        }
    }
}
