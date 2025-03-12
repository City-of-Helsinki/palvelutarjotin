# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_add_occurrence_to_published_event 1'] = {
    'data': {
        'addOccurrence': {
            'occurrence': {
                'contactPersons': {
                    'edges': [
                        {
                            'node': {
                                'name': 'New name'
                            }
                        },
                        {
                            'node': {
                                'name': 'Sean Rocha'
                            }
                        }
                    ]
                },
                'endTime': '2020-05-06T00:00:00+00:00',
                'languages': {
                    'edges': [
                        {
                            'node': {
                                'id': 'ar',
                                'name': 'Arabic'
                            }
                        },
                        {
                            'node': {
                                'id': 'zh_hans',
                                'name': 'Chinese'
                            }
                        },
                        {
                            'node': {
                                'id': 'en',
                                'name': 'English'
                            }
                        },
                        {
                            'node': {
                                'id': 'ru',
                                'name': 'Russia'
                            }
                        },
                        {
                            'node': {
                                'id': 'sv',
                                'name': 'Swedish'
                            }
                        }
                    ]
                },
                'maxGroupSize': None,
                'minGroupSize': 10,
                'pEvent': {
                    'autoAcceptance': False,
                    'contactEmail': 'barrettjason@example.org',
                    'contactPhoneNumber': '271-434-1145',
                    'enrolmentEndDays': 0,
                    'enrolmentStart': '1980-03-10T09:11:49.213826+00:00',
                    'externalEnrolmentUrl': None,
                    'linkedEventId': 'QoxZH',
                    'mandatoryAdditionalInformation': False,
                    'neededOccurrences': 2
                },
                'startTime': '2020-05-05T00:00:00+00:00'
            }
        }
    }
}

snapshots['test_add_occurrence_to_unpublished_event 1'] = {
    'data': {
        'addOccurrence': {
            'occurrence': {
                'contactPersons': {
                    'edges': [
                        {
                            'node': {
                                'name': 'New name'
                            }
                        },
                        {
                            'node': {
                                'name': 'Sean Rocha'
                            }
                        }
                    ]
                },
                'endTime': '2020-05-06T00:00:00+00:00',
                'languages': {
                    'edges': [
                        {
                            'node': {
                                'id': 'ar',
                                'name': 'Arabic'
                            }
                        },
                        {
                            'node': {
                                'id': 'zh_hans',
                                'name': 'Chinese'
                            }
                        },
                        {
                            'node': {
                                'id': 'en',
                                'name': 'English'
                            }
                        },
                        {
                            'node': {
                                'id': 'ru',
                                'name': 'Russia'
                            }
                        },
                        {
                            'node': {
                                'id': 'sv',
                                'name': 'Swedish'
                            }
                        }
                    ]
                },
                'maxGroupSize': None,
                'minGroupSize': 10,
                'pEvent': {
                    'autoAcceptance': False,
                    'contactEmail': 'barrettjason@example.org',
                    'contactPhoneNumber': '271-434-1145',
                    'enrolmentEndDays': 0,
                    'enrolmentStart': '1980-03-10T09:11:49.213826+00:00',
                    'externalEnrolmentUrl': None,
                    'linkedEventId': 'QoxZH',
                    'mandatoryAdditionalInformation': False,
                    'neededOccurrences': 2
                },
                'startTime': '2020-05-05T00:00:00+00:00'
            }
        }
    }
}

snapshots['test_add_study_group 1'] = {
    'data': {
        'addStudyGroup': {
            'studyGroup': {
                'amountOfAdult': 1,
                'extraNeeds': 'Extra needs',
                'groupName': 'Sample group name',
                'groupSize': 20,
                'person': {
                    'emailAddress': 'email@address.com',
                    'language': 'SV',
                    'name': 'Name',
                    'phoneNumber': '123123'
                },
                'studyLevels': {
                    'edges': [
                        {
                            'node': {
                                'id': 'grade_1',
                                'label': 'first grade',
                                'level': 3,
                                'translations': [
                                    {
                                        'label': 'first grade',
                                        'languageCode': 'EN'
                                    }
                                ]
                            }
                        }
                    ]
                },
                'unit': {
                    'internalId': 'https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/',
                    'name': {
                        'fi': 'Raija Malka & Kaija Saariaho: Blick'
                    }
                },
                'unitId': 'helsinki:afxp6tv4xa',
                'unitName': 'Sample study group name'
            }
        }
    }
}

snapshots['test_add_study_group 2'] = {
    'data': {
        'addStudyGroup': {
            'studyGroup': {
                'amountOfAdult': 1,
                'extraNeeds': 'Extra needs',
                'groupName': 'Sample group name',
                'groupSize': 20,
                'person': {
                    'emailAddress': 'kimberlyshort@example.org',
                    'language': 'FI',
                    'name': 'Charles Anderson',
                    'phoneNumber': '213.341.1450x892'
                },
                'studyLevels': {
                    'edges': [
                        {
                            'node': {
                                'id': 'grade_1',
                                'label': 'first grade',
                                'level': 3,
                                'translations': [
                                    {
                                        'label': 'first grade',
                                        'languageCode': 'EN'
                                    }
                                ]
                            }
                        }
                    ]
                },
                'unit': {
                    'internalId': 'https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/',
                    'name': {
                        'fi': 'Raija Malka & Kaija Saariaho: Blick'
                    }
                },
                'unitId': 'helsinki:afxp6tv4xa',
                'unitName': 'Sample study group name'
            }
        }
    }
}

snapshots['test_add_venue_staff_user 1'] = {
    'data': {
        'addVenue': {
            'venue': {
                'description': 'Venue description in FI',
                'hasAreaForGroupWork': True,
                'hasClothingStorage': True,
                'hasIndoorPlayingArea': True,
                'hasOutdoorPlayingArea': True,
                'hasSnackEatingPlace': True,
                'hasToiletNearby': True,
                'id': 'place_id',
                'outdoorActivity': True,
                'translations': [
                    {
                        'description': 'Venue description in FI'
                    },
                    {
                        'description': 'Venue description in EN'
                    }
                ]
            }
        }
    }
}

snapshots['test_approve_enrolment 1'] = {
    'data': {
        'approveEnrolment': {
            'enrolment': {
                'status': 'APPROVED'
            }
        }
    }
}

snapshots['test_approve_enrolment 2'] = [
    '''no-reply@hel.ninja|['kimberlyshort@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: VFlOj
    Study group: Leave serve important probably. Sea something western research.
    Occurrence: 06.01.2020 02.00
    Person: kimberlyshort@example.org
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

'''
]

snapshots['test_approve_enrolment_with_custom_message 1'] = {
    'data': {
        'approveEnrolment': {
            'enrolment': {
                'status': 'APPROVED'
            }
        }
    }
}

snapshots['test_approve_enrolment_with_custom_message 2'] = [
    '''no-reply@hel.ninja|['kimberlyshort@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MYfOB
    Study group: Leave serve important probably. Sea something western research.
    Occurrence: 06.01.2020 02.00
    Person: kimberlyshort@example.org
    Click this link to cancel the enrolment:
    https://kultus.hel.fi/fi/enrolments/cancel/mock-enrolment-unique-id-abc123xyz456

    Custom message: custom message
'''
]

snapshots['test_ask_for_cancelled_confirmation_mutation 1'] = {
    'data': {
        'cancelEnrolment': {
            'enrolment': {
                'status': 'PENDING'
            }
        }
    }
}

snapshots['test_auto_accept_message_is_used_as_custom_message_in_auto_approved_enrolments[False] 1'] = {
    'data': {
        'enrolOccurrence': {
            'enrolments': [
                {
                    'notificationType': 'EMAIL',
                    'occurrence': {
                        'amountOfSeats': 50,
                        'remainingSeats': 35,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 15,
                        'seatsTaken': 15,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    },
                    'status': 'APPROVED',
                    'studyGroup': {
                        'unitName': 'To be created group'
                    }
                }
            ]
        }
    }
}

snapshots['test_auto_accept_message_is_used_as_custom_message_in_auto_approved_enrolments[True] 1'] = {
    'data': {
        'enrolOccurrence': {
            'enrolments': [
                {
                    'notificationType': 'EMAIL',
                    'occurrence': {
                        'amountOfSeats': 50,
                        'remainingSeats': 35,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 15,
                        'seatsTaken': 15,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    },
                    'status': 'APPROVED',
                    'studyGroup': {
                        'unitName': 'To be created group'
                    }
                }
            ]
        }
    }
}

snapshots['test_auto_accept_message_is_used_as_custom_message_in_auto_approved_enrolments[True] 2'] = [
    '''no-reply@hel.ninja|['hutchinsonrachel@example.org']|Enrolment approved FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: EOTtw
    Study group: To be created group
    Occurrence: 06.01.2020 02.00
    Person: hutchinsonrachel@example.org

    Custom message: Testing auto acceptance message
'''
]

snapshots['test_cancel_enrolment_mutation 1'] = {
    'data': {
        'cancelEnrolment': {
            'enrolment': {
                'status': 'CANCELLED'
            }
        }
    }
}

snapshots['test_cancel_enrolment_query 1'] = {
    'data': {
        'cancellingEnrolment': {
            'enrolmentTime': '2020-01-04T00:00:00+00:00',
            'occurrence': {
                'seatsTaken': 229
            },
            'status': 'PENDING',
            'studyGroup': {
                'groupSize': 229,
                'unitName': 'Campaign college career fight data. Generation man process white visit step.'
            }
        }
    }
}

snapshots['test_cancel_occurrence 1'] = {
    'data': {
        'cancelOccurrence': {
            'occurrence': {
                'cancelled': True
            }
        }
    }
}

snapshots['test_decline_enrolment 1'] = {
    'data': {
        'declineEnrolment': {
            'enrolment': {
                'status': 'DECLINED'
            }
        }
    }
}

snapshots['test_decline_enrolment 2'] = [
    '''no-reply@hel.ninja|['kimberlyshort@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: VFlOj
    Study group: Leave serve important probably. Sea something western research.
    Occurrence: 06.01.2020 02.00
    Person: kimberlyshort@example.org

''',
    '''no-reply@hel.ninja|['kimberlyshort@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: VFlOj
    Study group: Leave serve important probably. Sea something western research.
    Occurrence: 06.01.2020 02.00
    Person: kimberlyshort@example.org

'''
]

snapshots['test_decline_enrolment_with_custom_message 1'] = {
    'data': {
        'declineEnrolment': {
            'enrolment': {
                'status': 'DECLINED'
            }
        }
    }
}

snapshots['test_decline_enrolment_with_custom_message 2'] = [
    '''no-reply@hel.ninja|['kimberlyshort@example.org']|Enrolment declined FI|
    Event FI: Raija Malka & Kaija Saariaho: Blick
    Extra event info: MYfOB
    Study group: Leave serve important probably. Sea something western research.
    Occurrence: 06.01.2020 02.00
    Person: kimberlyshort@example.org

    Custom message: custom message
'''
]

snapshots['test_delete_cancelled_occurrence 1'] = {
    'data': {
        'deleteOccurrence': {
            '__typename': 'DeleteOccurrenceMutationPayload'
        }
    }
}

snapshots['test_delete_unpublished_occurrence 1'] = {
    'data': {
        'deleteOccurrence': {
            '__typename': 'DeleteOccurrenceMutationPayload'
        }
    }
}

snapshots['test_enrol_auto_acceptance_occurrence 1'] = {
    'data': {
        'enrolOccurrence': {
            'enrolments': [
                {
                    'notificationType': 'EMAIL',
                    'occurrence': {
                        'amountOfSeats': 50,
                        'remainingSeats': 35,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 15,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    },
                    'status': 'PENDING',
                    'studyGroup': {
                        'unitName': 'To be created group'
                    }
                }
            ]
        }
    }
}

snapshots['test_enrol_auto_acceptance_occurrence 2'] = {
    'data': {
        'enrolOccurrence': {
            'enrolments': [
                {
                    'notificationType': 'EMAIL',
                    'occurrence': {
                        'amountOfSeats': 50,
                        'remainingSeats': 35,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 15,
                        'seatsTaken': 15,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    },
                    'status': 'APPROVED',
                    'studyGroup': {
                        'unitName': 'To be created group'
                    }
                }
            ]
        }
    }
}

snapshots['test_enrol_event_queue_mutation 1'] = {
    'data': {
        'enrolEventQueue': {
            'eventQueueEnrolment': {
                'notificationType': 'EMAIL_SMS',
                'pEvent': {
                    'autoAcceptance': False,
                    'contactEmail': 'patriciacervantes@example.net',
                    'contactPhoneNumber': '001-299-601-3232x13168',
                    'enrolmentEndDays': 2,
                    'enrolmentStart': '2019-09-02T21:49:06.027297+00:00',
                    'externalEnrolmentUrl': None,
                    'isQueueingAllowed': True,
                    'linkedEventId': 'kSRpd',
                    'mandatoryAdditionalInformation': False,
                    'neededOccurrences': 2
                },
                'status': 'HAS_NO_ENROLMENTS',
                'studyGroup': {
                    'preferredTimes': 'Only tuesdays',
                    'unitName': 'To be created group'
                }
            }
        }
    }
}

snapshots['test_enrol_occurrence 1'] = {
    'data': {
        'enrolOccurrence': {
            'enrolments': [
                {
                    'notificationType': 'EMAIL',
                    'occurrence': {
                        'amountOfSeats': 50,
                        'remainingSeats': 35,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 15,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    },
                    'status': 'PENDING',
                    'studyGroup': {
                        'unitName': 'To be created group'
                    }
                },
                {
                    'notificationType': 'EMAIL',
                    'occurrence': {
                        'amountOfSeats': 2,
                        'remainingSeats': 1,
                        'seatType': 'ENROLMENT_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 1,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    },
                    'status': 'PENDING',
                    'studyGroup': {
                        'unitName': 'To be created group'
                    }
                }
            ]
        }
    }
}

snapshots['test_enrol_occurrence_with_captcha 1'] = {
    'data': {
        'enrolOccurrence': {
            'enrolments': [
                {
                    'notificationType': 'EMAIL',
                    'occurrence': {
                        'amountOfSeats': 50,
                        'remainingSeats': 35,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 15,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    },
                    'status': 'PENDING',
                    'studyGroup': {
                        'unitName': 'To be created group'
                    }
                }
            ]
        }
    }
}

snapshots['test_enrolment_query 1'] = {
    'data': {
        'enrolment': {
            'occurrence': {
                'endTime': '1984-08-14T20:17:50.965825+00:00',
                'pEvent': {
                    'linkedEventId': 'rBcjT'
                },
                'seatsTaken': 838,
                'startTime': '1976-10-26T19:25:30.627463+00:00'
            },
            'status': 'PENDING',
            'studyGroup': {
                'groupName': 'Hot identify each its general. By garden so country past involve choose.'
            }
        }
    }
}

snapshots['test_enrolments_summary 1'] = {
    'data': {
        'enrolmentSummary': {
            'count': 4,
            'edges': [
                {
                    'node': {
                        'status': 'APPROVED'
                    }
                },
                {
                    'node': {
                        'status': 'CANCELLED'
                    }
                },
                {
                    'node': {
                        'status': 'DECLINED'
                    }
                },
                {
                    'node': {
                        'status': 'PENDING'
                    }
                }
            ]
        }
    }
}

snapshots['test_enrolments_summary 2'] = {
    'data': {
        'enrolmentSummary': {
            'count': 1,
            'edges': [
                {
                    'node': {
                        'status': 'APPROVED'
                    }
                }
            ]
        }
    }
}

snapshots['test_enrolments_summary 3'] = {
    'data': {
        'enrolmentSummary': {
            'count': 1,
            'edges': [
                {
                    'node': {
                        'status': 'PENDING'
                    }
                }
            ]
        }
    }
}

snapshots['test_enrolments_summary 4'] = {
    'data': {
        'enrolmentSummary': {
            'count': 1,
            'edges': [
                {
                    'node': {
                        'status': 'CANCELLED'
                    }
                }
            ]
        }
    }
}

snapshots['test_enrolments_summary 5'] = {
    'data': {
        'enrolmentSummary': {
            'count': 1,
            'edges': [
                {
                    'node': {
                        'status': 'DECLINED'
                    }
                }
            ]
        }
    }
}

snapshots['test_event_queue_enrolment_query 1'] = {
    'data': {
        'eventQueueEnrolment': {
            'pEvent': {
                'isQueueingAllowed': True,
                'linkedEventId': 'GVbfW'
            },
            'status': 'HAS_NO_ENROLMENTS',
            'studyGroup': {
                'groupName': 'Close term where up notice environment father stay. Hold project month similar support line.',
                'preferredTimes': 'Only drug follow research.'
            }
        }
    }
}

snapshots['test_event_queue_enrolments_query 1'] = {
    'data': {
        'eventQueueEnrolments': {
            'count': 15,
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Hotel event already college. Ok court type hit.',
                            'preferredTimes': 'Fund nor white identify.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjE=',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': '''Apply somebody especially far. Color price environmental.
Market him beyond.''',
                            'preferredTimes': 'Pattern administration early.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Reach ask I cut ok. Perhaps teacher involve all my improve our Congress.',
                            'preferredTimes': 'Future upon a key fast white.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjM=',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Space oil painting. Cut region decade hold point firm. Interesting technology group.',
                            'preferredTimes': 'Defense field east.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjQ=',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Offer record quite window station. And natural seven. Hit performance daughter.',
                            'preferredTimes': 'Home argue way all moment.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjU=',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Yeah rock evening player. According however energy large change history.',
                            'preferredTimes': 'Leg ready building.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjY=',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Peace relationship hear increase us. Population along collection though.',
                            'preferredTimes': 'Pressure health design admit.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjc=',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Simple spend decade born. Day range age.',
                            'preferredTimes': 'Image identify and.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjg=',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Friend clear focus operation its bar anyone he.',
                            'preferredTimes': 'Yes back traditional.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjk=',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Consumer miss sense remember. House senior popular end.',
                            'preferredTimes': 'Site score center.'
                        }
                    }
                }
            ]
        }
    }
}

snapshots['test_event_queue_enrolments_query 2'] = {
    'data': {
        'eventQueueEnrolments': {
            'count': 15,
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjEw',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Away watch above bad car. List short color produce include threat.',
                            'preferredTimes': 'Street sign education field.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjEx',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Before charge difficult number. Leave part and test benefit.',
                            'preferredTimes': 'Hotel near deal.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjEy',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'The threat organization check may available. Offer much discuss.',
                            'preferredTimes': 'Range seek turn how.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjEz',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Card support wait clearly.',
                            'preferredTimes': 'Ago include poor example.'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjE0',
                    'node': {
                        'pEvent': {
                            'isQueueingAllowed': True,
                            'linkedEventId': 'GVbfW',
                            'organisation': {
                                'name': 'Graves and Sons'
                            }
                        },
                        'status': 'HAS_NO_ENROLMENTS',
                        'studyGroup': {
                            'groupName': 'Project hope eight week still. Mission program point piece simple too walk. Talk hand price author.',
                            'preferredTimes': 'On performance detail sure.'
                        }
                    }
                }
            ]
        }
    }
}

snapshots['test_language_query 1'] = {
    'data': {
        'language': {
            'id': 'aAVEavNlmo',
            'name': 'Him question stay.'
        }
    }
}

snapshots['test_languages_query 1'] = {
    'data': {
        'languages': {
            'edges': [
                {
                    'node': {
                        'id': 'ar',
                        'name': 'Arabic'
                    }
                },
                {
                    'node': {
                        'id': 'zh_hans',
                        'name': 'Chinese'
                    }
                },
                {
                    'node': {
                        'id': 'en',
                        'name': 'English'
                    }
                },
                {
                    'node': {
                        'id': 'fi',
                        'name': 'Finnish'
                    }
                },
                {
                    'node': {
                        'id': 'aAVEavNlmo',
                        'name': 'Him question stay.'
                    }
                },
                {
                    'node': {
                        'id': 'ru',
                        'name': 'Russia'
                    }
                },
                {
                    'node': {
                        'id': 'sv',
                        'name': 'Swedish'
                    }
                }
            ]
        }
    }
}

snapshots['test_mass_approve_enrolment_mutation 1'] = {
    'data': {
        'massApproveEnrolments': {
            'enrolments': [
                {
                    'status': 'APPROVED'
                },
                {
                    'status': 'APPROVED'
                },
                {
                    'status': 'APPROVED'
                }
            ]
        }
    }
}

snapshots['test_notification_template_query 1'] = {
    'data': {
        'notificationTemplate': {
            'customContextPreviewHtml': '''<p>
    Event EN: Name in english
    Extra event info: linked_event_id
    Study group: group name
    Occurrence: 2020-12-12
    Person: email@me.com

    Custom message: custom_message
</p>''',
            'customContextPreviewText': '''
    Event EN: Name in english
    Extra event info: linked_event_id
    Study group: group name
    Occurrence: 2020-12-12
    Person: email@me.com

    Custom message: custom_message
''',
            'template': {
                'type': 'enrolment_approved'
            }
        }
    }
}

snapshots['test_occurrence_query 1'] = {
    'data': {
        'occurrence': {
            'amountOfSeats': 33,
            'contactPersons': {
                'edges': [
                ]
            },
            'endTime': '1992-07-05T12:04:13.244825+00:00',
            'languages': {
                'edges': [
                ]
            },
            'linkedEvent': {
                'name': {
                    'en': 'Raija Malka & Kaija Saariaho: Blick',
                    'fi': 'Raija Malka & Kaija Saariaho: Blick',
                    'sv': 'Raija Malka & Kaija Saariaho: Blick'
                }
            },
            'maxGroupSize': 383,
            'minGroupSize': 341,
            'pEvent': {
                'autoAcceptance': False,
                'contactEmail': 'eperry@example.org',
                'contactPhoneNumber': '5646976380',
                'enrolmentEndDays': 1,
                'enrolmentStart': '1989-08-31T23:14:42.824885+00:00',
                'externalEnrolmentUrl': None,
                'linkedEventId': 'ytHjL',
                'mandatoryAdditionalInformation': False,
                'neededOccurrences': 5
            },
            'placeId': 'Record card my. Sure sister return.',
            'remainingSeats': 33,
            'seatsApproved': 0,
            'seatsTaken': 0,
            'startTime': '2002-04-18T06:53:11.806335+00:00'
        }
    }
}

snapshots['test_occurrences_filter_by_cancelled 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 48,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2010-06-18T23:16:49.508200+00:00',
                        'maxGroupSize': 588,
                        'minGroupSize': 752,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'dsellers@example.net',
                            'contactPhoneNumber': '934.957.7355',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1990-12-14T02:05:00.660682+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 3
                        },
                        'placeId': 'Event lay yes policy data control as receive.',
                        'remainingSeats': 48,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2010-05-25T06:23:10.664303+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 27,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1992-11-11T22:23:23.275974+00:00',
                        'maxGroupSize': 779,
                        'minGroupSize': 292,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'dsellers@example.net',
                            'contactPhoneNumber': '934.957.7355',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1990-12-14T02:05:00.660682+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 3
                        },
                        'placeId': 'Foreign go age. Thought price gas heavy affect difficult look.',
                        'remainingSeats': 27,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2017-11-29T20:14:25.983420+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_cancelled 2'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 19,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1999-05-25T03:21:42.257063+00:00',
                        'maxGroupSize': 808,
                        'minGroupSize': 974,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'dsellers@example.net',
                            'contactPhoneNumber': '934.957.7355',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1990-12-14T02:05:00.660682+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 3
                        },
                        'placeId': 'Think significant land especially can quite.',
                        'remainingSeats': 19,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '1992-03-25T02:06:42.233338+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_date 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 14,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1992-03-25T02:06:42.233338+00:00',
                        'maxGroupSize': 808,
                        'minGroupSize': 974,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'huntveronica@example.net',
                            'contactPhoneNumber': '946-620-0377x22182',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1995-07-09T08:34:53.846489+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'Eprsb',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 9
                        },
                        'placeId': 'Today friend maintain marriage ok thank realize.',
                        'remainingSeats': 14,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-02T00:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_date 2'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 14,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1992-03-25T02:06:42.233338+00:00',
                        'maxGroupSize': 808,
                        'minGroupSize': 974,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'huntveronica@example.net',
                            'contactPhoneNumber': '946-620-0377x22182',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1995-07-09T08:34:53.846489+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'Eprsb',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 9
                        },
                        'placeId': 'Today friend maintain marriage ok thank realize.',
                        'remainingSeats': 14,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-02T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 46,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2009-07-10T23:31:56.453060+00:00',
                        'maxGroupSize': 285,
                        'minGroupSize': 350,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'flowersbryan@example.net',
                            'contactPhoneNumber': '(951)826-3008x4654',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1987-07-08T20:58:36.505491+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'jGwiN',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 10
                        },
                        'placeId': 'Traditional whether serious sister work.',
                        'remainingSeats': 46,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-02T00:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_enrollable[0-3] 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 2,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2010-02-19T14:44:08.844371+00:00',
                        'maxGroupSize': 714,
                        'minGroupSize': 757,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': 0,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Put matter benefit treat final. Father boy economy the.',
                        'remainingSeats': 2,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-05T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 37,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1985-05-19T11:46:06.872667+00:00',
                        'maxGroupSize': 859,
                        'minGroupSize': 99,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': 0,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Party door better performance race story.',
                        'remainingSeats': 37,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 15,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1987-01-08T13:12:09.032776+00:00',
                        'maxGroupSize': 873,
                        'minGroupSize': 799,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': 0,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Toward scientist service wonder everything.',
                        'remainingSeats': 15,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-07T00:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_enrollable[1-2] 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 37,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1985-05-19T11:46:06.872667+00:00',
                        'maxGroupSize': 859,
                        'minGroupSize': 99,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': 1,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Party door better performance race story.',
                        'remainingSeats': 37,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 15,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1987-01-08T13:12:09.032776+00:00',
                        'maxGroupSize': 873,
                        'minGroupSize': 799,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': 1,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Toward scientist service wonder everything.',
                        'remainingSeats': 15,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-07T00:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_enrollable[None-3] 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 2,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2010-02-19T14:44:08.844371+00:00',
                        'maxGroupSize': 714,
                        'minGroupSize': 757,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': None,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Put matter benefit treat final. Father boy economy the.',
                        'remainingSeats': 2,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-05T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 37,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1985-05-19T11:46:06.872667+00:00',
                        'maxGroupSize': 859,
                        'minGroupSize': 99,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': None,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Party door better performance race story.',
                        'remainingSeats': 37,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 15,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1987-01-08T13:12:09.032776+00:00',
                        'maxGroupSize': 873,
                        'minGroupSize': 799,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': None,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Toward scientist service wonder everything.',
                        'remainingSeats': 15,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-07T00:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_p_event 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 27,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1982-11-06T04:40:33.407924+00:00',
                        'maxGroupSize': 22,
                        'minGroupSize': 6,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'dsellers@example.net',
                            'contactPhoneNumber': '934.957.7355',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1990-12-14T02:05:00.660682+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 3
                        },
                        'placeId': 'Need benefit ready though street.',
                        'remainingSeats': 27,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2008-02-13T12:08:42.493034+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 3,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1983-12-18T04:04:52.499467+00:00',
                        'maxGroupSize': 128,
                        'minGroupSize': 574,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'dsellers@example.net',
                            'contactPhoneNumber': '934.957.7355',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1990-12-14T02:05:00.660682+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 3
                        },
                        'placeId': 'Course plant strong truth customer.',
                        'remainingSeats': 3,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2009-08-12T09:04:07.768068+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_p_event 2'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 49,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1975-07-12T08:02:11.536273+00:00',
                        'maxGroupSize': 990,
                        'minGroupSize': 749,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'cmartin@example.org',
                            'contactPhoneNumber': '+1-777-693-4055x5508',
                            'enrolmentEndDays': 1,
                            'enrolmentStart': '2004-08-22T05:11:59.521157+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'rzzET',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 10
                        },
                        'placeId': 'End look once strong artist save. Run hand human value base.',
                        'remainingSeats': 49,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2018-10-21T22:46:45.180823+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_time 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 33,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2002-04-18T06:53:11.806335+00:00',
                        'maxGroupSize': 383,
                        'minGroupSize': 341,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'bthomas@example.org',
                            'contactPhoneNumber': '(806)849-7638x034',
                            'enrolmentEndDays': 1,
                            'enrolmentStart': '2006-07-17T08:32:28.440059+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'xytHj',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 7
                        },
                        'placeId': 'Record card my. Sure sister return.',
                        'remainingSeats': 33,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-01T10:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_time 2'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 24,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1970-04-03T02:18:45.929522+00:00',
                        'maxGroupSize': 288,
                        'minGroupSize': 67,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'pwilliams@example.org',
                            'contactPhoneNumber': '737.279.4021x78779',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '2007-04-19T17:41:37.637441+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'Tfgkj',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 3
                        },
                        'placeId': 'Few eye first walk west six feel. Fast authority key crime.',
                        'remainingSeats': 24,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-02T12:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_time 3'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 46,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2009-07-10T23:31:56.453060+00:00',
                        'maxGroupSize': 285,
                        'minGroupSize': 350,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'flowersbryan@example.net',
                            'contactPhoneNumber': '(951)826-3008x4654',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1987-07-08T20:58:36.505491+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'jGwiN',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 10
                        },
                        'placeId': 'Traditional whether serious sister work.',
                        'remainingSeats': 46,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-01T11:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 14,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1992-03-25T02:06:42.233338+00:00',
                        'maxGroupSize': 808,
                        'minGroupSize': 974,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'huntveronica@example.net',
                            'contactPhoneNumber': '946-620-0377x22182',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1995-07-09T08:34:53.846489+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'Eprsb',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 9
                        },
                        'placeId': 'Today friend maintain marriage ok thank realize.',
                        'remainingSeats': 14,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-02T11:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_time 4'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 46,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2009-07-10T23:31:56.453060+00:00',
                        'maxGroupSize': 285,
                        'minGroupSize': 350,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'flowersbryan@example.net',
                            'contactPhoneNumber': '(951)826-3008x4654',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1987-07-08T20:58:36.505491+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'jGwiN',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 10
                        },
                        'placeId': 'Traditional whether serious sister work.',
                        'remainingSeats': 46,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-01T11:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 14,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1992-03-25T02:06:42.233338+00:00',
                        'maxGroupSize': 808,
                        'minGroupSize': 974,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'huntveronica@example.net',
                            'contactPhoneNumber': '946-620-0377x22182',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1995-07-09T08:34:53.846489+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'Eprsb',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 9
                        },
                        'placeId': 'Today friend maintain marriage ok thank realize.',
                        'remainingSeats': 14,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-02T11:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_filter_by_upcoming 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 43,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2020-01-05T00:00:00+00:00',
                        'maxGroupSize': 709,
                        'minGroupSize': 132,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': 10,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Success commercial recently from front affect senior.',
                        'remainingSeats': 43,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-04T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 22,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2020-01-06T00:00:00+00:00',
                        'maxGroupSize': 407,
                        'minGroupSize': 589,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': 10,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Option PM put matter benefit.',
                        'remainingSeats': 22,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-05T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 19,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2020-01-07T00:00:00+00:00',
                        'maxGroupSize': 859,
                        'minGroupSize': 99,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'thompsonjessica@example.com',
                            'contactPhoneNumber': '001-833-934-5773x55777',
                            'enrolmentEndDays': 10,
                            'enrolmentStart': '2020-01-05T00:00:00+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'aAVEa',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 6
                        },
                        'placeId': 'Dream party door better performance race story.',
                        'remainingSeats': 19,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_ordering_by_order_by_end_time 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 46,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2020-01-05T00:00:00+00:00',
                        'maxGroupSize': 285,
                        'minGroupSize': 350,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'flowersbryan@example.net',
                            'contactPhoneNumber': '(951)826-3008x4654',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1987-07-08T20:58:36.505491+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'jGwiN',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 10
                        },
                        'placeId': 'Traditional whether serious sister work.',
                        'remainingSeats': 46,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2009-07-10T23:31:56.453060+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 33,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2020-01-06T00:00:00+00:00',
                        'maxGroupSize': 383,
                        'minGroupSize': 341,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'bthomas@example.org',
                            'contactPhoneNumber': '(806)849-7638x034',
                            'enrolmentEndDays': 1,
                            'enrolmentStart': '2006-07-17T08:32:28.440059+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'xytHj',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 7
                        },
                        'placeId': 'Record card my. Sure sister return.',
                        'remainingSeats': 33,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2002-04-18T06:53:11.806335+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 14,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2020-01-07T00:00:00+00:00',
                        'maxGroupSize': 808,
                        'minGroupSize': 974,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'huntveronica@example.net',
                            'contactPhoneNumber': '946-620-0377x22182',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1995-07-09T08:34:53.846489+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'Eprsb',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 9
                        },
                        'placeId': 'Today friend maintain marriage ok thank realize.',
                        'remainingSeats': 14,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '1992-03-25T02:06:42.233338+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_ordering_by_order_by_end_time 2'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 14,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2020-01-07T00:00:00+00:00',
                        'maxGroupSize': 808,
                        'minGroupSize': 974,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'huntveronica@example.net',
                            'contactPhoneNumber': '946-620-0377x22182',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1995-07-09T08:34:53.846489+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'Eprsb',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 9
                        },
                        'placeId': 'Today friend maintain marriage ok thank realize.',
                        'remainingSeats': 14,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '1992-03-25T02:06:42.233338+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 33,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2020-01-06T00:00:00+00:00',
                        'maxGroupSize': 383,
                        'minGroupSize': 341,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'bthomas@example.org',
                            'contactPhoneNumber': '(806)849-7638x034',
                            'enrolmentEndDays': 1,
                            'enrolmentStart': '2006-07-17T08:32:28.440059+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'xytHj',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 7
                        },
                        'placeId': 'Record card my. Sure sister return.',
                        'remainingSeats': 33,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2002-04-18T06:53:11.806335+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 46,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2020-01-05T00:00:00+00:00',
                        'maxGroupSize': 285,
                        'minGroupSize': 350,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'flowersbryan@example.net',
                            'contactPhoneNumber': '(951)826-3008x4654',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1987-07-08T20:58:36.505491+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'jGwiN',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 10
                        },
                        'placeId': 'Traditional whether serious sister work.',
                        'remainingSeats': 46,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2009-07-10T23:31:56.453060+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_ordering_by_order_by_start_time 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 46,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2009-07-10T23:31:56.453060+00:00',
                        'maxGroupSize': 285,
                        'minGroupSize': 350,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'flowersbryan@example.net',
                            'contactPhoneNumber': '(951)826-3008x4654',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1987-07-08T20:58:36.505491+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'jGwiN',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 10
                        },
                        'placeId': 'Traditional whether serious sister work.',
                        'remainingSeats': 46,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-05T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 33,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2002-04-18T06:53:11.806335+00:00',
                        'maxGroupSize': 383,
                        'minGroupSize': 341,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'bthomas@example.org',
                            'contactPhoneNumber': '(806)849-7638x034',
                            'enrolmentEndDays': 1,
                            'enrolmentStart': '2006-07-17T08:32:28.440059+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'xytHj',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 7
                        },
                        'placeId': 'Record card my. Sure sister return.',
                        'remainingSeats': 33,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 14,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1992-03-25T02:06:42.233338+00:00',
                        'maxGroupSize': 808,
                        'minGroupSize': 974,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'huntveronica@example.net',
                            'contactPhoneNumber': '946-620-0377x22182',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1995-07-09T08:34:53.846489+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'Eprsb',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 9
                        },
                        'placeId': 'Today friend maintain marriage ok thank realize.',
                        'remainingSeats': 14,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-07T00:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_ordering_by_order_by_start_time 2'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 14,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1992-03-25T02:06:42.233338+00:00',
                        'maxGroupSize': 808,
                        'minGroupSize': 974,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'huntveronica@example.net',
                            'contactPhoneNumber': '946-620-0377x22182',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1995-07-09T08:34:53.846489+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'Eprsb',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 9
                        },
                        'placeId': 'Today friend maintain marriage ok thank realize.',
                        'remainingSeats': 14,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-07T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 33,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2002-04-18T06:53:11.806335+00:00',
                        'maxGroupSize': 383,
                        'minGroupSize': 341,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'bthomas@example.org',
                            'contactPhoneNumber': '(806)849-7638x034',
                            'enrolmentEndDays': 1,
                            'enrolmentStart': '2006-07-17T08:32:28.440059+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'xytHj',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 7
                        },
                        'placeId': 'Record card my. Sure sister return.',
                        'remainingSeats': 33,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-06T00:00:00+00:00'
                    }
                },
                {
                    'node': {
                        'amountOfSeats': 46,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '2009-07-10T23:31:56.453060+00:00',
                        'maxGroupSize': 285,
                        'minGroupSize': 350,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'flowersbryan@example.net',
                            'contactPhoneNumber': '(951)826-3008x4654',
                            'enrolmentEndDays': 2,
                            'enrolmentStart': '1987-07-08T20:58:36.505491+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'jGwiN',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 10
                        },
                        'placeId': 'Traditional whether serious sister work.',
                        'remainingSeats': 46,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2020-01-05T00:00:00+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_occurrences_query 1'] = {
    'data': {
        'occurrences': {
            'edges': [
                {
                    'node': {
                        'amountOfSeats': 33,
                        'contactPersons': {
                            'edges': [
                            ]
                        },
                        'endTime': '1992-07-05T12:04:13.244825+00:00',
                        'maxGroupSize': 383,
                        'minGroupSize': 341,
                        'pEvent': {
                            'autoAcceptance': False,
                            'contactEmail': 'eperry@example.org',
                            'contactPhoneNumber': '5646976380',
                            'enrolmentEndDays': 1,
                            'enrolmentStart': '1989-08-31T23:14:42.824885+00:00',
                            'externalEnrolmentUrl': None,
                            'linkedEventId': 'ytHjL',
                            'mandatoryAdditionalInformation': False,
                            'neededOccurrences': 5
                        },
                        'placeId': 'Record card my. Sure sister return.',
                        'remainingSeats': 33,
                        'seatType': 'CHILDREN_COUNT',
                        'seatsApproved': 0,
                        'seatsTaken': 0,
                        'startTime': '2002-04-18T06:53:11.806335+00:00'
                    }
                }
            ]
        }
    }
}

snapshots['test_pick_enrolment_from_queue 1'] = {
    'data': {
        'pickEnrolmentFromQueue': {
            'enrolment': {
                'notificationType': 'EMAIL',
                'person': {
                    'emailAddress': 'rose06@example.com',
                    'name': 'Robert Gray'
                },
                'status': 'PENDING',
                'studyGroup': {
                    'groupName': 'Decade address have turn serve me every traditional. Sound describe risk newspaper reflect four.'
                }
            }
        }
    }
}

snapshots['test_study_level_query 1'] = {
    'data': {
        'studyLevel': {
            'id': 'age_0_2',
            'label': 'age 0-2',
            'level': 0,
            'translations': [
                {
                    'label': 'age 0-2',
                    'languageCode': 'EN'
                }
            ]
        }
    }
}

snapshots['test_study_levels_query 1'] = {
    'data': {
        'studyLevels': {
            'edges': [
                {
                    'node': {
                        'id': 'age_0_2',
                        'label': 'age 0-2',
                        'level': 0,
                        'translations': [
                            {
                                'label': 'age 0-2',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'age_3_4',
                        'label': 'age 3-4',
                        'level': 1,
                        'translations': [
                            {
                                'label': 'age 3-4',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'preschool',
                        'label': 'preschool',
                        'level': 2,
                        'translations': [
                            {
                                'label': 'preschool',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'grade_1',
                        'label': 'first grade',
                        'level': 3,
                        'translations': [
                            {
                                'label': 'first grade',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'grade_2',
                        'label': 'second grade',
                        'level': 4,
                        'translations': [
                            {
                                'label': 'second grade',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'grade_3',
                        'label': 'third grade',
                        'level': 5,
                        'translations': [
                            {
                                'label': 'third grade',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'grade_4',
                        'label': 'fourth grade',
                        'level': 6,
                        'translations': [
                            {
                                'label': 'fourth grade',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'grade_5',
                        'label': 'fifth grade',
                        'level': 7,
                        'translations': [
                            {
                                'label': 'fifth grade',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'grade_6',
                        'label': 'sixth grade',
                        'level': 8,
                        'translations': [
                            {
                                'label': 'sixth grade',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'grade_7',
                        'label': 'seventh grade',
                        'level': 9,
                        'translations': [
                            {
                                'label': 'seventh grade',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'grade_8',
                        'label': 'eighth grade',
                        'level': 10,
                        'translations': [
                            {
                                'label': 'eighth grade',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'grade_9',
                        'label': 'ninth grade',
                        'level': 11,
                        'translations': [
                            {
                                'label': 'ninth grade',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'grade_10',
                        'label': 'tenth grade',
                        'level': 12,
                        'translations': [
                            {
                                'label': 'tenth grade',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'secondary',
                        'label': 'secondary',
                        'level': 13,
                        'translations': [
                            {
                                'label': 'secondary',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                },
                {
                    'node': {
                        'id': 'other',
                        'label': 'other group',
                        'level': 14,
                        'translations': [
                            {
                                'label': 'other group',
                                'languageCode': 'EN'
                            }
                        ]
                    }
                }
            ]
        }
    }
}

snapshots['test_unenrol_event_queue_mutation[False] 1'] = {
    'data': {
        'unenrolEventQueue': {
            'pEvent': {
                'isQueueingAllowed': False,
                'linkedEventId': 'MYfOB'
            },
            'studyGroup': {
                'unitName': 'Tough plant traditional after born up always. Return student light a point charge.'
            }
        }
    }
}

snapshots['test_unenrol_event_queue_mutation[True] 1'] = {
    'data': {
        'unenrolEventQueue': {
            'pEvent': {
                'isQueueingAllowed': True,
                'linkedEventId': 'MYfOB'
            },
            'studyGroup': {
                'unitName': 'Tough plant traditional after born up always. Return student light a point charge.'
            }
        }
    }
}

snapshots['test_unenrol_occurrence 1'] = {
    'data': {
        'unenrolOccurrence': {
            'occurrence': {
                'amountOfSeats': 50,
                'remainingSeats': 50,
                'seatsApproved': 0,
                'seatsTaken': 0,
                'startTime': '2020-01-06T00:00:00+00:00'
            },
            'studyGroup': {
                'unitName': 'Leave serve important probably. Sea something western research.'
            }
        }
    }
}

snapshots['test_update_enrolment 1'] = {
    'data': {
        'updateEnrolment': {
            'enrolment': {
                'notificationType': 'SMS',
                'occurrence': {
                    'amountOfSeats': 35,
                    'remainingSeats': 6,
                    'seatsApproved': 0,
                    'seatsTaken': 29,
                    'startTime': '2020-01-06T00:00:00+00:00'
                },
                'status': 'PENDING',
                'studyGroup': {
                    'amountOfAdult': 3,
                    'enrolments': {
                        'edges': [
                            {
                                'node': {
                                    'notificationType': 'SMS'
                                }
                            },
                            {
                                'node': {
                                    'notificationType': 'SMS'
                                }
                            }
                        ]
                    },
                    'groupName': 'Updated study group name',
                    'groupSize': 16,
                    'unitName': 'Updated name'
                }
            }
        }
    }
}

snapshots['test_update_occurrence_of_published_event_without_enrolments 1'] = {
    'data': {
        'updateOccurrence': {
            'occurrence': {
                'contactPersons': {
                    'edges': [
                        {
                            'node': {
                                'name': 'Julie Parrish'
                            }
                        }
                    ]
                },
                'endTime': '2020-05-06T00:00:00+00:00',
                'languages': {
                    'edges': [
                        {
                            'node': {
                                'id': 'en',
                                'name': 'English'
                            }
                        },
                        {
                            'node': {
                                'id': 'fi',
                                'name': 'Finnish'
                            }
                        },
                        {
                            'node': {
                                'id': 'sv',
                                'name': 'Swedish'
                            }
                        }
                    ]
                },
                'maxGroupSize': 10,
                'minGroupSize': 10,
                'pEvent': {
                    'contactEmail': 'donald78@example.net',
                    'contactPhoneNumber': '001-658-731-3222x29493',
                    'enrolmentEndDays': 2,
                    'enrolmentStart': '1981-07-25T08:53:14.019007+00:00',
                    'externalEnrolmentUrl': None,
                    'linkedEventId': 'helsinki:afxp6tv4xa',
                    'mandatoryAdditionalInformation': False,
                    'neededOccurrences': 0
                },
                'startTime': '2020-05-05T00:00:00+00:00'
            }
        }
    }
}

snapshots['test_update_study_group_staff_user 1'] = {
    'data': {
        'updateStudyGroup': {
            'studyGroup': {
                'amountOfAdult': 2,
                'extraNeeds': 'Extra needs',
                'groupName': 'Sample group name',
                'groupSize': 20,
                'person': {
                    'emailAddress': 'email@address.com',
                    'language': 'FI',
                    'name': 'Name',
                    'phoneNumber': '123123'
                },
                'studyLevels': {
                    'edges': [
                        {
                            'node': {
                                'id': 'grade_2',
                                'label': 'second grade',
                                'level': 4,
                                'translations': [
                                    {
                                        'label': 'second grade',
                                        'languageCode': 'EN'
                                    }
                                ]
                            }
                        }
                    ]
                },
                'unit': {
                    'internalId': 'https://api.hel.fi/linkedevents/v1/place/tprek:15417/',
                    'name': {
                        'fi': 'Sellon kirjasto'
                    }
                },
                'unitId': 'helsinki:afxp6tv4xa',
                'unitName': 'Sample study group name'
            }
        }
    }
}

snapshots['test_update_study_group_staff_user 2'] = {
    'data': {
        'updateStudyGroup': {
            'studyGroup': {
                'amountOfAdult': 2,
                'extraNeeds': 'Extra needs',
                'groupName': 'Sample group name',
                'groupSize': 20,
                'person': {
                    'emailAddress': 'shawndouglas@example.com',
                    'language': 'FI',
                    'name': 'Sean Rocha',
                    'phoneNumber': '001-215-991-0232x02813'
                },
                'studyLevels': {
                    'edges': [
                        {
                            'node': {
                                'id': 'grade_2',
                                'label': 'second grade',
                                'level': 4,
                                'translations': [
                                    {
                                        'label': 'second grade',
                                        'languageCode': 'EN'
                                    }
                                ]
                            }
                        }
                    ]
                },
                'unit': {
                    'internalId': 'https://api.hel.fi/linkedevents/v1/place/tprek:15417/',
                    'name': {
                        'fi': 'Sellon kirjasto'
                    }
                },
                'unitId': 'helsinki:afxp6tv4xa',
                'unitName': 'Sample study group name'
            }
        }
    }
}

snapshots['test_update_unpublished_occurrence 1'] = {
    'data': {
        'updateOccurrence': {
            'occurrence': {
                'contactPersons': {
                    'edges': [
                        {
                            'node': {
                                'name': 'Julie Parrish'
                            }
                        }
                    ]
                },
                'endTime': '2020-05-06T00:00:00+00:00',
                'languages': {
                    'edges': [
                        {
                            'node': {
                                'id': 'en',
                                'name': 'English'
                            }
                        },
                        {
                            'node': {
                                'id': 'fi',
                                'name': 'Finnish'
                            }
                        },
                        {
                            'node': {
                                'id': 'sv',
                                'name': 'Swedish'
                            }
                        }
                    ]
                },
                'maxGroupSize': 588,
                'minGroupSize': 10,
                'pEvent': {
                    'contactEmail': 'travishopkins@example.net',
                    'contactPhoneNumber': '(722)729-4934',
                    'enrolmentEndDays': 0,
                    'enrolmentStart': '1980-12-30T21:30:40.750124+00:00',
                    'externalEnrolmentUrl': None,
                    'linkedEventId': 'raSqN',
                    'mandatoryAdditionalInformation': False,
                    'neededOccurrences': 3
                },
                'startTime': '2020-05-05T00:00:00+00:00'
            }
        }
    }
}

snapshots['test_update_venue_staff_user 1'] = {
    'data': {
        'updateVenue': {
            'venue': {
                'description': 'Venue description',
                'hasAreaForGroupWork': True,
                'hasClothingStorage': True,
                'hasIndoorPlayingArea': True,
                'hasOutdoorPlayingArea': True,
                'hasSnackEatingPlace': True,
                'hasToiletNearby': True,
                'id': 'Irtal',
                'outdoorActivity': True,
                'translations': [
                    {
                        'description': 'Venue description'
                    },
                    {
                        'description': 'Venue description in EN'
                    }
                ]
            }
        }
    }
}

snapshots['test_venue_query 1'] = {
    'data': {
        'venue': {
            'description': 'Answer entire increase thank certainly again thought. Beyond than trial western.',
            'hasAreaForGroupWork': False,
            'hasClothingStorage': False,
            'hasIndoorPlayingArea': False,
            'hasOutdoorPlayingArea': False,
            'hasSnackEatingPlace': True,
            'hasToiletNearby': False,
            'id': 'PcMpy',
            'outdoorActivity': False,
            'translations': [
                {
                    'description': 'Answer entire increase thank certainly again thought. Beyond than trial western.'
                }
            ]
        }
    }
}

snapshots['test_venues_query 1'] = {
    'data': {
        'venues': {
            'edges': [
                {
                    'node': {
                        'description': 'Answer entire increase thank certainly again thought. Beyond than trial western.',
                        'hasAreaForGroupWork': False,
                        'hasClothingStorage': False,
                        'hasIndoorPlayingArea': False,
                        'hasOutdoorPlayingArea': False,
                        'hasSnackEatingPlace': True,
                        'hasToiletNearby': False,
                        'id': 'PcMpy',
                        'outdoorActivity': False,
                        'translations': [
                            {
                                'description': 'Answer entire increase thank certainly again thought. Beyond than trial western.'
                            }
                        ]
                    }
                }
            ]
        }
    }
}
