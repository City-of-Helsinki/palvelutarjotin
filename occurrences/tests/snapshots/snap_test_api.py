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
                        {"node": {"name": "Mike Allen"}},
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
                        {"node": {"name": "Mike Allen"}},
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
                    "emailAddress": "gtorres@example.com",
                    "language": "FI",
                    "name": "Gregory Flores",
                    "phoneNumber": "954.620.0377x22182",
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
    """no-reply@hel.ninja|['gonzalezmichele@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: rmjtE
    Study group: Professional serious under who Mrs public. Campaign college career fight data.
    Occurrence: 06.01.2020 02.00
    Person: gonzalezmichele@example.org
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTozN18yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

"""
]

snapshots["test_approve_enrolment_with_custom_message 1"] = {
    "data": {"approveEnrolment": {"enrolment": {"status": "APPROVED"}}}
}

snapshots["test_approve_enrolment_with_custom_message 2"] = [
    """no-reply@hel.ninja|['gonzalezmichele@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: nmvjB
    Study group: Professional serious under who Mrs public. Campaign college career fight data.
    Occurrence: 06.01.2020 02.00
    Person: gonzalezmichele@example.org
    Click this link to cancel the enrolment:
    https://kultus.fi/fi/enrolments/cancel/RW5yb2xtZW50Tm9kZTozOV8yMDIwLTAxLTA0IDAwOjAwOjAwKzAwOjAw

    Custom message: custom message
"""
]

snapshots["test_ask_for_cancelled_confirmation_mutation 1"] = {
    "data": {"cancelEnrolment": {"enrolment": {"status": "PENDING"}}}
}

snapshots[
    "test_auto_accept_message_is_used_as_custom_message_in_auto_approved_enrolments 1"
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
    "test_auto_accept_message_is_used_as_custom_message_in_auto_approved_enrolments 2"
] = [
    """no-reply@hel.ninja|['longrebecca@example.com']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: kSRpd
    Study group: To be created group
    Occurrence: 06.01.2020 02.00
    Person: longrebecca@example.com

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
            "occurrence": {"seatsTaken": 473},
            "status": "PENDING",
            "studyGroup": {
                "groupSize": 473,
                "unitName": "Turn argue present throw spend prevent. Point exist road military Republican somebody.",
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
    """no-reply@hel.ninja|['gonzalezmichele@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: rmjtE
    Study group: Professional serious under who Mrs public. Campaign college career fight data.
    Occurrence: 06.01.2020 02.00
    Person: gonzalezmichele@example.org

""",
    """no-reply@hel.ninja|['gonzalezmichele@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: rmjtE
    Study group: Professional serious under who Mrs public. Campaign college career fight data.
    Occurrence: 06.01.2020 02.00
    Person: gonzalezmichele@example.org

""",
]

snapshots["test_decline_enrolment_with_custom_message 1"] = {
    "data": {"declineEnrolment": {"enrolment": {"status": "DECLINED"}}}
}

snapshots["test_decline_enrolment_with_custom_message 2"] = [
    """no-reply@hel.ninja|['gonzalezmichele@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: nmvjB
    Study group: Professional serious under who Mrs public. Campaign college career fight data.
    Occurrence: 06.01.2020 02.00
    Person: gonzalezmichele@example.org

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
                    "linkedEventId": "kSRpd",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 2,
                },
                "status": "HAS_NOT_ENROLLED",
                "studyGroup": {"unitName": "To be created group"},
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

snapshots["test_enrolments_query[-status] 1"] = {
    "data": {
        "enrolments": {
            "count": 4,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "DECLINED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "CANCELLED",
                        "studyGroup": {"groupName": "group C"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjI=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group B"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjM=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
            ],
        }
    }
}

snapshots["test_enrolments_query[-status] 2"] = {
    "data": {
        "enrolments": {
            "count": 2,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group B"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
            ],
        }
    }
}

snapshots["test_enrolments_query[-status] 3"] = {
    "data": {"enrolments": {"count": 0, "edges": []}}
}

snapshots["test_enrolments_query[-status] 4"] = {
    "data": {
        "enrolments": {
            "count": 1,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "CANCELLED",
                        "studyGroup": {"groupName": "group C"},
                    },
                }
            ],
        }
    }
}

snapshots["test_enrolments_query[-status] 5"] = {
    "data": {
        "enrolments": {
            "count": 1,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "DECLINED",
                        "studyGroup": {"groupName": "group A"},
                    },
                }
            ],
        }
    }
}

snapshots["test_enrolments_query[-study_group__group_name] 1"] = {
    "data": {
        "enrolments": {
            "count": 4,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "CANCELLED",
                        "studyGroup": {"groupName": "group C"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group B"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjI=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "DECLINED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjM=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
            ],
        }
    }
}

snapshots["test_enrolments_query[-study_group__group_name] 2"] = {
    "data": {
        "enrolments": {
            "count": 2,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group B"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
            ],
        }
    }
}

snapshots["test_enrolments_query[-study_group__group_name] 3"] = {
    "data": {"enrolments": {"count": 0, "edges": []}}
}

snapshots["test_enrolments_query[-study_group__group_name] 4"] = {
    "data": {
        "enrolments": {
            "count": 1,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "CANCELLED",
                        "studyGroup": {"groupName": "group C"},
                    },
                }
            ],
        }
    }
}

snapshots["test_enrolments_query[-study_group__group_name] 5"] = {
    "data": {
        "enrolments": {
            "count": 1,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "DECLINED",
                        "studyGroup": {"groupName": "group A"},
                    },
                }
            ],
        }
    }
}

snapshots["test_enrolments_query[status] 1"] = {
    "data": {
        "enrolments": {
            "count": 4,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group B"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjI=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "CANCELLED",
                        "studyGroup": {"groupName": "group C"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjM=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "DECLINED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
            ],
        }
    }
}

snapshots["test_enrolments_query[status] 2"] = {
    "data": {
        "enrolments": {
            "count": 2,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group B"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
            ],
        }
    }
}

snapshots["test_enrolments_query[status] 3"] = {
    "data": {"enrolments": {"count": 0, "edges": []}}
}

snapshots["test_enrolments_query[status] 4"] = {
    "data": {
        "enrolments": {
            "count": 1,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "CANCELLED",
                        "studyGroup": {"groupName": "group C"},
                    },
                }
            ],
        }
    }
}

snapshots["test_enrolments_query[status] 5"] = {
    "data": {
        "enrolments": {
            "count": 1,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "DECLINED",
                        "studyGroup": {"groupName": "group A"},
                    },
                }
            ],
        }
    }
}

snapshots["test_enrolments_query[study_group__group_name] 1"] = {
    "data": {
        "enrolments": {
            "count": 4,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "DECLINED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjI=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group B"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjM=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "CANCELLED",
                        "studyGroup": {"groupName": "group C"},
                    },
                },
            ],
        }
    }
}

snapshots["test_enrolments_query[study_group__group_name] 2"] = {
    "data": {
        "enrolments": {
            "count": 2,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group A"},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "APPROVED",
                        "studyGroup": {"groupName": "group B"},
                    },
                },
            ],
        }
    }
}

snapshots["test_enrolments_query[study_group__group_name] 3"] = {
    "data": {"enrolments": {"count": 0, "edges": []}}
}

snapshots["test_enrolments_query[study_group__group_name] 4"] = {
    "data": {
        "enrolments": {
            "count": 1,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "CANCELLED",
                        "studyGroup": {"groupName": "group C"},
                    },
                }
            ],
        }
    }
}

snapshots["test_enrolments_query[study_group__group_name] 5"] = {
    "data": {
        "enrolments": {
            "count": 1,
            "edges": [
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjA=",
                    "node": {
                        "occurrence": {
                            "endTime": "2001-01-01T13:18:22+00:00",
                            "pEvent": {"linkedEventId": "bkihg"},
                            "seatsTaken": 1173,
                            "startTime": "1988-08-02T07:00:39+00:00",
                        },
                        "status": "DECLINED",
                        "studyGroup": {"groupName": "group A"},
                    },
                }
            ],
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
            "pEvent": {"linkedEventId": "xeobQ"},
            "status": "HAS_NOT_ENROLLED",
            "studyGroup": {"groupName": "Last in able local garden modern they."},
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
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Pm PM indicate general put. Poor left president model character two coach."
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Account four degree return pick sister music result. Skill become open yes table."
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjI=",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Factor scene news democratic. Then amount morning training program provide various."
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjM=",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": """Them base although also partner fine. Yard word employee half.
Commercial lose add bag."""
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjQ=",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {"groupName": "Drop police change dinner."},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjU=",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Explain five him toward including animal. Good million late people oil."
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjY=",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Feeling consider catch believe cell. Drug her soon those analysis physical across."
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjc=",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Budget political natural relate stage. However yes wear anyone vote."
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjg=",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Party with anything yet music. Court program song couple. Fast learn sense radio."
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjk=",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "With hair take nation. Relate clear traditional much situation western."
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
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Them letter certainly expert. Unit child environmental take."
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjEx",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Culture most page reduce green conference front. Decide very data four."
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjEy",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Support thing song board strong government."
                        },
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjEz",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {"groupName": "Region protect likely day."},
                    },
                },
                {
                    "cursor": "YXJyYXljb25uZWN0aW9uOjE0",
                    "node": {
                        "pEvent": {"linkedEventId": "xeobQ"},
                        "status": "HAS_NOT_ENROLLED",
                        "studyGroup": {
                            "groupName": "Last in able local garden modern they."
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
            "amountOfSeats": 25,
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
            "remainingSeats": 25,
            "seatsApproved": 0,
            "seatsTaken": 0,
            "startTime": "2013-12-12T04:57:19+00:00",
            "studyGroups": {"edges": []},
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
                            "contactEmail": "dsellers@example.net",
                            "contactPhoneNumber": "345.773.5577",
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
                        "amountOfSeats": 22,
                        "contactPersons": {"edges": []},
                        "endTime": "1991-01-06T20:05:17+00:00",
                        "maxGroupSize": 932,
                        "minGroupSize": 512,
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
                        "placeId": "Truth list pressure stage history. City sing himself yard.",
                        "remainingSeats": 22,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2005-01-18T03:44:33+00:00",
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
                        "amountOfSeats": 39,
                        "contactPersons": {"edges": []},
                        "endTime": "1998-03-12T19:56:01+00:00",
                        "maxGroupSize": 562,
                        "minGroupSize": 348,
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
                        "placeId": "Service wonder everything pay parent theory.",
                        "remainingSeats": 39,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1986-04-11T14:17:11+00:00",
                        "studyGroups": {"edges": []},
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
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2009-07-12T04:07:58+00:00",
                        "maxGroupSize": 457,
                        "minGroupSize": 509,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "nicholas00@example.org",
                            "contactPhoneNumber": "793.405.5550x895",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2019-10-15T07:25:08+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "ngJvK",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Those notice medical science sort already.",
                        "remainingSeats": 46,
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

snapshots["test_occurrences_filter_by_date 2"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2009-07-12T04:07:58+00:00",
                        "maxGroupSize": 457,
                        "minGroupSize": 509,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "nicholas00@example.org",
                            "contactPhoneNumber": "793.405.5550x895",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2019-10-15T07:25:08+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "ngJvK",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Those notice medical science sort already.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-02T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 43,
                        "contactPersons": {"edges": []},
                        "endTime": "1974-10-19T15:53:39+00:00",
                        "maxGroupSize": 687,
                        "minGroupSize": 225,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "esmith@example.org",
                            "contactPhoneNumber": "(778)840-8746",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1991-02-21T03:14:24+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "mOhDG",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Light a point charge stand store.",
                        "remainingSeats": 43,
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

snapshots["test_occurrences_filter_by_enrollable[0-3] 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 30,
                        "contactPersons": {"edges": []},
                        "endTime": "2002-06-15T11:57:08+00:00",
                        "maxGroupSize": 231,
                        "minGroupSize": 45,
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
                        "placeId": "Which president smile staff country actually generation.",
                        "remainingSeats": 30,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 44,
                        "contactPersons": {"edges": []},
                        "endTime": "2018-01-05T23:56:15+00:00",
                        "maxGroupSize": 429,
                        "minGroupSize": 836,
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
                        "placeId": "Commercial recently from front affect senior number.",
                        "remainingSeats": 44,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 36,
                        "contactPersons": {"edges": []},
                        "endTime": "1993-07-24T08:52:34+00:00",
                        "maxGroupSize": 407,
                        "minGroupSize": 589,
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
                        "placeId": "Option PM put matter benefit.",
                        "remainingSeats": 36,
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

snapshots["test_occurrences_filter_by_enrollable[1-2] 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 44,
                        "contactPersons": {"edges": []},
                        "endTime": "2018-01-05T23:56:15+00:00",
                        "maxGroupSize": 429,
                        "minGroupSize": 836,
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
                        "placeId": "Commercial recently from front affect senior number.",
                        "remainingSeats": 44,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 36,
                        "contactPersons": {"edges": []},
                        "endTime": "1993-07-24T08:52:34+00:00",
                        "maxGroupSize": 407,
                        "minGroupSize": 589,
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
                        "placeId": "Option PM put matter benefit.",
                        "remainingSeats": 36,
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

snapshots["test_occurrences_filter_by_enrollable[None-3] 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 30,
                        "contactPersons": {"edges": []},
                        "endTime": "2002-06-15T11:57:08+00:00",
                        "maxGroupSize": 231,
                        "minGroupSize": 45,
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
                        "placeId": "Which president smile staff country actually generation.",
                        "remainingSeats": 30,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 44,
                        "contactPersons": {"edges": []},
                        "endTime": "2018-01-05T23:56:15+00:00",
                        "maxGroupSize": 429,
                        "minGroupSize": 836,
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
                        "placeId": "Commercial recently from front affect senior number.",
                        "remainingSeats": 44,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 36,
                        "contactPersons": {"edges": []},
                        "endTime": "1993-07-24T08:52:34+00:00",
                        "maxGroupSize": 407,
                        "minGroupSize": 589,
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
                        "placeId": "Option PM put matter benefit.",
                        "remainingSeats": 36,
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

snapshots["test_occurrences_filter_by_p_event 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 38,
                        "contactPersons": {"edges": []},
                        "endTime": "1993-01-04T08:20:35+00:00",
                        "maxGroupSize": 768,
                        "minGroupSize": 746,
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
                        "placeId": "Think turn argue present. Spend prevent pressure point exist.",
                        "remainingSeats": 38,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2009-12-10T20:02:15+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 5,
                        "contactPersons": {"edges": []},
                        "endTime": "2015-02-19T19:35:54+00:00",
                        "maxGroupSize": 912,
                        "minGroupSize": 473,
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
                        "placeId": "Behavior media career decide season mission TV.",
                        "remainingSeats": 5,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2018-08-30T11:34:25+00:00",
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
                        "amountOfSeats": 40,
                        "contactPersons": {"edges": []},
                        "endTime": "1975-08-29T21:32:18+00:00",
                        "maxGroupSize": 746,
                        "minGroupSize": 146,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "wellsdiana@example.com",
                            "contactPhoneNumber": "(681)066-9583x693",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2011-05-08T04:35:51+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "MNZoG",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Various build leave serve important.",
                        "remainingSeats": 40,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2007-09-11T17:25:39+00:00",
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
                        "amountOfSeats": 25,
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
                        "remainingSeats": 25,
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

snapshots["test_occurrences_filter_by_time 2"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 26,
                        "contactPersons": {"edges": []},
                        "endTime": "1988-10-06T08:20:53+00:00",
                        "maxGroupSize": 741,
                        "minGroupSize": 666,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "sandra56@example.net",
                            "contactPhoneNumber": "+1-795-462-1895x673",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2005-10-28T13:02:54+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "NaRcy",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 7,
                        },
                        "placeId": "Question national throw three.",
                        "remainingSeats": 26,
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
                        "amountOfSeats": 43,
                        "contactPersons": {"edges": []},
                        "endTime": "1974-10-19T15:53:39+00:00",
                        "maxGroupSize": 687,
                        "minGroupSize": 225,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "esmith@example.org",
                            "contactPhoneNumber": "(778)840-8746",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1991-02-21T03:14:24+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "mOhDG",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Light a point charge stand store.",
                        "remainingSeats": 43,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2009-07-12T04:07:58+00:00",
                        "maxGroupSize": 457,
                        "minGroupSize": 509,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "nicholas00@example.org",
                            "contactPhoneNumber": "793.405.5550x895",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2019-10-15T07:25:08+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "ngJvK",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Those notice medical science sort already.",
                        "remainingSeats": 46,
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
                        "amountOfSeats": 43,
                        "contactPersons": {"edges": []},
                        "endTime": "1974-10-19T15:53:39+00:00",
                        "maxGroupSize": 687,
                        "minGroupSize": 225,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "esmith@example.org",
                            "contactPhoneNumber": "(778)840-8746",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1991-02-21T03:14:24+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "mOhDG",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Light a point charge stand store.",
                        "remainingSeats": 43,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-01T11:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2009-07-12T04:07:58+00:00",
                        "maxGroupSize": 457,
                        "minGroupSize": 509,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "nicholas00@example.org",
                            "contactPhoneNumber": "793.405.5550x895",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2019-10-15T07:25:08+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "ngJvK",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Those notice medical science sort already.",
                        "remainingSeats": 46,
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

snapshots["test_occurrences_filter_by_upcoming 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 17,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-05T00:00:00+00:00",
                        "maxGroupSize": 628,
                        "minGroupSize": 833,
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
                        "placeId": "Gas heavy affect difficult look can purpose care.",
                        "remainingSeats": 17,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-04T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 42,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-06T00:00:00+00:00",
                        "maxGroupSize": 980,
                        "minGroupSize": 908,
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
                        "placeId": "Staff read rule point leg within.",
                        "remainingSeats": 42,
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
                        "endTime": "2020-01-07T00:00:00+00:00",
                        "maxGroupSize": 709,
                        "minGroupSize": 132,
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
                        "placeId": "Success commercial recently from front affect senior.",
                        "remainingSeats": 43,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
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
                        "amountOfSeats": 43,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-05T00:00:00+00:00",
                        "maxGroupSize": 687,
                        "minGroupSize": 225,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "esmith@example.org",
                            "contactPhoneNumber": "(778)840-8746",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1991-02-21T03:14:24+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "mOhDG",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Light a point charge stand store.",
                        "remainingSeats": 43,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1974-10-19T15:53:39+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 25,
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
                        "remainingSeats": 25,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-07T00:00:00+00:00",
                        "maxGroupSize": 457,
                        "minGroupSize": 509,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "nicholas00@example.org",
                            "contactPhoneNumber": "793.405.5550x895",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2019-10-15T07:25:08+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "ngJvK",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Those notice medical science sort already.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2009-07-12T04:07:58+00:00",
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
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-07T00:00:00+00:00",
                        "maxGroupSize": 457,
                        "minGroupSize": 509,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "nicholas00@example.org",
                            "contactPhoneNumber": "793.405.5550x895",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2019-10-15T07:25:08+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "ngJvK",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Those notice medical science sort already.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2009-07-12T04:07:58+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 25,
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
                        "remainingSeats": 25,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2013-12-12T04:57:19+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 43,
                        "contactPersons": {"edges": []},
                        "endTime": "2020-01-05T00:00:00+00:00",
                        "maxGroupSize": 687,
                        "minGroupSize": 225,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "esmith@example.org",
                            "contactPhoneNumber": "(778)840-8746",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1991-02-21T03:14:24+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "mOhDG",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Light a point charge stand store.",
                        "remainingSeats": 43,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "1974-10-19T15:53:39+00:00",
                        "studyGroups": {"edges": []},
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
                        "amountOfSeats": 43,
                        "contactPersons": {"edges": []},
                        "endTime": "1974-10-19T15:53:39+00:00",
                        "maxGroupSize": 687,
                        "minGroupSize": 225,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "esmith@example.org",
                            "contactPhoneNumber": "(778)840-8746",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1991-02-21T03:14:24+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "mOhDG",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Light a point charge stand store.",
                        "remainingSeats": 43,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-05T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 25,
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
                        "remainingSeats": 25,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2009-07-12T04:07:58+00:00",
                        "maxGroupSize": 457,
                        "minGroupSize": 509,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "nicholas00@example.org",
                            "contactPhoneNumber": "793.405.5550x895",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2019-10-15T07:25:08+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "ngJvK",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Those notice medical science sort already.",
                        "remainingSeats": 46,
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
                        "amountOfSeats": 46,
                        "contactPersons": {"edges": []},
                        "endTime": "2009-07-12T04:07:58+00:00",
                        "maxGroupSize": 457,
                        "minGroupSize": 509,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "nicholas00@example.org",
                            "contactPhoneNumber": "793.405.5550x895",
                            "enrolmentEndDays": 2,
                            "enrolmentStart": "2019-10-15T07:25:08+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "ngJvK",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 10,
                        },
                        "placeId": "Those notice medical science sort already.",
                        "remainingSeats": 46,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-07T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 25,
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
                        "remainingSeats": 25,
                        "seatType": "CHILDREN_COUNT",
                        "seatsApproved": 0,
                        "seatsTaken": 0,
                        "startTime": "2020-01-06T00:00:00+00:00",
                        "studyGroups": {"edges": []},
                    }
                },
                {
                    "node": {
                        "amountOfSeats": 43,
                        "contactPersons": {"edges": []},
                        "endTime": "1974-10-19T15:53:39+00:00",
                        "maxGroupSize": 687,
                        "minGroupSize": 225,
                        "pEvent": {
                            "autoAcceptance": False,
                            "contactEmail": "esmith@example.org",
                            "contactPhoneNumber": "(778)840-8746",
                            "enrolmentEndDays": 1,
                            "enrolmentStart": "1991-02-21T03:14:24+00:00",
                            "externalEnrolmentUrl": None,
                            "linkedEventId": "mOhDG",
                            "mandatoryAdditionalInformation": False,
                            "neededOccurrences": 5,
                        },
                        "placeId": "Light a point charge stand store.",
                        "remainingSeats": 43,
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

snapshots["test_occurrences_query 1"] = {
    "data": {
        "occurrences": {
            "edges": [
                {
                    "node": {
                        "amountOfSeats": 25,
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
                        "remainingSeats": 25,
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

snapshots["test_study_group_query 1"] = {
    "data": {
        "studyGroup": {
            "amountOfAdult": 0,
            "extraNeeds": "Spring never skill. Able process base sing according.",
            "groupName": "Scientist service wonder everything pay. Moment strong hand push book and interesting sit.",
            "groupSize": 35,
            "occurrences": {"edges": []},
            "person": {"name": "Richard Hayes"},
            "studyLevels": {"edges": []},
            "unit": {
                "name": {"fi": "Care any concern bed agree. Laugh prevent make never."}
            },
            "unitId": None,
            "unitName": "Care any concern bed agree. Laugh prevent make never.",
            "updatedAt": "2020-01-04T00:00:00+00:00",
        }
    }
}

snapshots["test_study_group_query_without_unit 1"] = {
    "data": {
        "studyGroup": {
            "amountOfAdult": 0,
            "extraNeeds": "Table TV minute defense. Room laugh prevent make never news behind.",
            "groupName": "Myself yourself able process base sing according. Watch media do concern sit enter.",
            "groupSize": 157,
            "occurrences": {"edges": []},
            "person": {"name": "Richard Hayes"},
            "studyLevels": {"edges": []},
            "unit": None,
            "unitId": "",
            "unitName": "",
            "updatedAt": "2020-01-04T00:00:00+00:00",
        }
    }
}

snapshots["test_study_groups_query 1"] = {
    "data": {
        "studyGroups": {
            "edges": [
                {
                    "node": {
                        "amountOfAdult": 0,
                        "extraNeeds": "Spring never skill. Able process base sing according.",
                        "groupName": "Scientist service wonder everything pay. Moment strong hand push book and interesting sit.",
                        "groupSize": 35,
                        "occurrences": {"edges": []},
                        "person": {"name": "Richard Hayes"},
                        "studyLevels": {"edges": []},
                        "unit": {
                            "name": {
                                "fi": "Care any concern bed agree. Laugh prevent make never."
                            }
                        },
                        "updatedAt": "2020-01-04T00:00:00+00:00",
                    }
                }
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
                "unitName": "Professional serious under who Mrs public. Campaign college career fight data."
            },
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
                "contactPersons": {"edges": [{"node": {"name": "Sarah Brown"}}]},
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
                    "contactEmail": "amanda25@example.com",
                    "contactPhoneNumber": "366.386.3333x61636",
                    "enrolmentEndDays": 0,
                    "enrolmentStart": "1971-10-08T22:49:29+00:00",
                    "externalEnrolmentUrl": None,
                    "linkedEventId": "helsinki:afxp6tv4xa",
                    "mandatoryAdditionalInformation": False,
                    "neededOccurrences": 5,
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
                    "emailAddress": "smithjames@example.org",
                    "language": "FI",
                    "name": "Mike Allen",
                    "phoneNumber": "034.669.7270x11715",
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
                "contactPersons": {"edges": [{"node": {"name": "Sarah Brown"}}]},
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
                    "contactEmail": "lauraramirez@example.org",
                    "contactPhoneNumber": "336.163.6588",
                    "enrolmentEndDays": 1,
                    "enrolmentStart": "2007-03-28T16:09:20+00:00",
                    "externalEnrolmentUrl": None,
                    "linkedEventId": "grBKt",
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
            "description": "Serious listen police shake. Page box child care any concern.",
            "hasAreaForGroupWork": False,
            "hasClothingStorage": True,
            "hasIndoorPlayingArea": False,
            "hasOutdoorPlayingArea": False,
            "hasSnackEatingPlace": False,
            "hasToiletNearby": False,
            "id": "sOxmZ",
            "outdoorActivity": True,
            "translations": [
                {
                    "description": "Serious listen police shake. Page box child care any concern."
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
                        "description": "Serious listen police shake. Page box child care any concern.",
                        "hasAreaForGroupWork": False,
                        "hasClothingStorage": True,
                        "hasIndoorPlayingArea": False,
                        "hasOutdoorPlayingArea": False,
                        "hasSnackEatingPlace": False,
                        "hasToiletNearby": False,
                        "id": "sOxmZ",
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
