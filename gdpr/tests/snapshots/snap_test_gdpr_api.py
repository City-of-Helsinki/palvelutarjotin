# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_delete_profile_data_from_gdpr_api[most_complex] enrolment should exist but not contain any person related sensitive data after deletion'] = {
    'children': [
        {
            'key': 'ENROLMENT_TIME',
            'value': '2020-01-04T00:00:00+00:00'
        },
        {
            'key': 'UPDATED_AT',
            'value': '2020-01-04T00:00:00+00:00'
        },
        {
            'key': 'STATUS',
            'value': 'pending'
        },
        {
            'children': [
                {
                    'key': 'START_TIME',
                    'value': '2010-07-23T16:15:55.542261+00:00'
                },
                {
                    'key': 'END_TIME',
                    'value': '2008-11-04T19:11:30.730104+00:00'
                },
                {
                    'key': 'CREATED_AT',
                    'value': '2020-01-04T00:00:00+00:00'
                },
                {
                    'key': 'UPDATED_AT',
                    'value': '2020-01-04T00:00:00+00:00'
                },
                {
                    'children': [
                        {
                            'key': 'LINKED_EVENT_ID',
                            'value': 'FrTcm'
                        },
                        {
                            'key': 'ORGANISATION',
                            'value': 'Carroll, Adams and Evans'
                        },
                        {
                            'key': 'CONTACT_PERSON',
                            'value': 'Erika Martinez, (569)876-1296, mark29@example.com'
                        }
                    ],
                    'key': 'PALVELUTARJOTINEVENT'
                }
            ],
            'key': 'OCCURRENCE'
        }
    ],
    'key': 'ENROLMENT'
}

snapshots['test_delete_profile_data_from_gdpr_api[most_complex] event queue enrolment should exist but not contain any person related sensitive data after deletion'] = {
    'children': [
        {
            'key': 'ENROLMENT_TIME',
            'value': '2020-01-04T00:00:00+00:00'
        },
        {
            'key': 'UPDATED_AT',
            'value': '2020-01-04T00:00:00+00:00'
        },
        {
            'key': 'NOTIFICATION_TYPE',
            'value': 'email'
        },
        {
            'key': 'STUDY_GROUP',
            'value': '1 Tough plant traditional after born up always. Return student light a point charge.'
        },
        {
            'children': [
                {
                    'key': 'LINKED_EVENT_ID',
                    'value': 'TwsLM'
                },
                {
                    'key': 'ORGANISATION',
                    'value': 'Singleton PLC'
                },
                {
                    'key': 'CONTACT_PERSON',
                    'value': 'Robert Davis, 327.543.4893, lanekayla@example.org'
                }
            ],
            'key': 'PALVELUTARJOTINEVENT'
        }
    ],
    'key': 'EVENTQUEUEENROLMENT'
}

snapshots['test_delete_profile_data_from_gdpr_api[most_complex] study group should exist but not contain any person related sensitive data after deletion'] = {
    'children': [
        {
            'key': 'UNIT_ID',
            'value': None
        },
        {
            'key': 'UNIT_NAME',
            'value': 'Daughter animal single whom involve. Different student moment apply president unit.'
        },
        {
            'key': 'GROUP_SIZE',
            'value': 420
        },
        {
            'key': 'AMOUNT_OF_ADULT',
            'value': 0
        },
        {
            'key': 'GROUP_NAME',
            'value': 'Resource set feeling within Mr total learn.'
        },
        {
            'key': 'EXTRA_NEEDS',
            'value': 'Culture most page reduce green conference front. Decide very data four.'
        },
        {
            'key': 'PREFERRED_TIMES',
            'value': 'Increase player power over.'
        },
        {
            'key': 'STUDY_LEVELS',
            'value': ''
        },
        {
            'children': [
                {
                    'children': [
                        {
                            'key': 'ENROLMENT_TIME',
                            'value': '2020-01-04T00:00:00+00:00'
                        },
                        {
                            'key': 'UPDATED_AT',
                            'value': '2020-01-04T00:00:00+00:00'
                        },
                        {
                            'key': 'STATUS',
                            'value': 'pending'
                        },
                        {
                            'children': [
                                {
                                    'key': 'START_TIME',
                                    'value': '1974-05-07T19:29:45.432928+00:00'
                                },
                                {
                                    'key': 'END_TIME',
                                    'value': '1997-04-17T22:13:24.246198+00:00'
                                },
                                {
                                    'key': 'CREATED_AT',
                                    'value': '2020-01-04T00:00:00+00:00'
                                },
                                {
                                    'key': 'UPDATED_AT',
                                    'value': '2020-01-04T00:00:00+00:00'
                                },
                                {
                                    'children': [
                                        {
                                            'key': 'LINKED_EVENT_ID',
                                            'value': 'mbLjf'
                                        },
                                        {
                                            'key': 'ORGANISATION',
                                            'value': 'Moon-Hernandez'
                                        },
                                        {
                                            'key': 'CONTACT_PERSON',
                                            'value': 'Charles Hansen, 419.442.1317, youngpeggy@example.org'
                                        }
                                    ],
                                    'key': 'PALVELUTARJOTINEVENT'
                                }
                            ],
                            'key': 'OCCURRENCE'
                        }
                    ],
                    'key': 'ENROLMENT'
                }
            ],
            'key': 'ENROLMENTS'
        }
    ],
    'key': 'STUDYGROUP'
}

snapshots['test_get_profile_data_from_gdpr_api[Complex User, Deleted] 1'] = {
    'children': [
        {
            'key': 'UUID',
            'value': '26850000-2e85-11ea-b347-acde48001122'
        },
        {
            'key': 'USERNAME',
            'value': 'u-e2cqaaboqui6vm2hvtpeqaarei'
        },
        {
            'key': 'FIRST_NAME',
            'value': ''
        },
        {
            'key': 'LAST_NAME',
            'value': ''
        },
        {
            'key': 'EMAIL',
            'value': ''
        },
        {
            'key': 'LAST_LOGIN',
            'value': None
        },
        {
            'key': 'DATE_JOINED',
            'value': '2020-01-04T00:00:00+00:00'
        }
    ],
    'key': 'USER'
}

snapshots['test_get_profile_data_from_gdpr_api[Complex User, Undeleted] 1'] = {
    'children': [
        {
            'key': 'UUID',
            'value': '26850000-2e85-11ea-b347-acde48001122'
        },
        {
            'key': 'USERNAME',
            'value': 'jeffersonkimberly_3MmHFh'
        },
        {
            'key': 'FIRST_NAME',
            'value': 'Alexis'
        },
        {
            'key': 'LAST_NAME',
            'value': 'Black'
        },
        {
            'key': 'EMAIL',
            'value': 'joshuajohnson@example.com'
        },
        {
            'key': 'LAST_LOGIN',
            'value': '2020-01-04T00:00:00+00:00'
        },
        {
            'key': 'DATE_JOINED',
            'value': '2020-01-04T00:00:00+00:00'
        },
        {
            'children': [
                {
                    'key': 'NAME',
                    'value': 'Tina Wilson'
                },
                {
                    'key': 'PHONE_NUMBER',
                    'value': '+1-910-423-2028x130'
                },
                {
                    'key': 'EMAIL_ADDRESS',
                    'value': 'fhuynh@example.org'
                },
                {
                    'key': 'LANGUAGE',
                    'value': 'fi'
                },
                {
                    'key': 'PLACE_IDS',
                    'value': 'SedRknnouKQItjsGbbnC, aIeOatnXjyxRexoPZaRK, VOMVMNZoGFTsuALvDSCv'
                },
                {
                    'children': [
                        {
                            'children': [
                                {
                                    'key': 'NAME',
                                    'value': 'Williams-Newton'
                                },
                                {
                                    'key': 'PHONE_NUMBER',
                                    'value': '497-963-8034x6697'
                                },
                                {
                                    'key': 'TYPE',
                                    'value': 'user'
                                },
                                {
                                    'key': 'PUBLISHER_ID',
                                    'value': 'TUOfT'
                                }
                            ],
                            'key': 'ORGANISATION'
                        }
                    ],
                    'key': 'ORGANISATIONS'
                },
                [
                    {
                        'children': [
                            {
                                'key': 'NAME',
                                'value': 'Young, Garcia and Dean'
                            },
                            {
                                'key': 'PHONE_NUMBER',
                                'value': '+1-582-474-0847x69470'
                            },
                            {
                                'key': 'DESCRIPTION',
                                'value': '''Beautiful if his their. Stuff election stay every. Base may middle good father boy economy.
Enjoy office water those notice medical. Already name likely behind mission network. Think significant land especially can quite.'''
                            }
                        ],
                        'key': 'ORGANISATIONPROPOSAL'
                    }
                ],
                [
                    {
                        'children': [
                            {
                                'key': 'UNIT_ID',
                                'value': None
                            },
                            {
                                'key': 'UNIT_NAME',
                                'value': 'Tough plant traditional after born up always. Return student light a point charge.'
                            },
                            {
                                'key': 'GROUP_SIZE',
                                'value': 2
                            },
                            {
                                'key': 'AMOUNT_OF_ADULT',
                                'value': 0
                            },
                            {
                                'key': 'GROUP_NAME',
                                'value': 'Hand human value base pattern democratic focus. Kind various laugh smile behavior.'
                            },
                            {
                                'key': 'EXTRA_NEEDS',
                                'value': 'Hot identify each its general. By garden so country past involve choose.'
                            },
                            {
                                'key': 'PREFERRED_TIMES',
                                'value': 'Difficult special respond.'
                            },
                            {
                                'key': 'STUDY_LEVELS',
                                'value': 'Cultural cell at. (id: Democrat., level: 3), Myself simple paper. (id: Happen., level: 4), Town back though. (id: Decade., level: 9)'
                            },
                            {
                                'children': [
                                    {
                                        'children': [
                                            {
                                                'key': 'ENROLMENT_TIME',
                                                'value': '2020-01-04T00:00:00+00:00'
                                            },
                                            {
                                                'key': 'UPDATED_AT',
                                                'value': '2020-01-04T00:00:00+00:00'
                                            },
                                            {
                                                'key': 'STATUS',
                                                'value': 'pending'
                                            },
                                            {
                                                'children': [
                                                    {
                                                        'key': 'START_TIME',
                                                        'value': '2010-07-23T16:15:55.542261+00:00'
                                                    },
                                                    {
                                                        'key': 'END_TIME',
                                                        'value': '2008-11-04T19:11:30.730104+00:00'
                                                    },
                                                    {
                                                        'key': 'CREATED_AT',
                                                        'value': '2020-01-04T00:00:00+00:00'
                                                    },
                                                    {
                                                        'key': 'UPDATED_AT',
                                                        'value': '2020-01-04T00:00:00+00:00'
                                                    },
                                                    {
                                                        'children': [
                                                            {
                                                                'key': 'LINKED_EVENT_ID',
                                                                'value': 'FrTcm'
                                                            },
                                                            {
                                                                'key': 'ORGANISATION',
                                                                'value': 'Carroll, Adams and Evans'
                                                            },
                                                            {
                                                                'key': 'CONTACT_PERSON',
                                                                'value': 'Erika Martinez, (569)876-1296, mark29@example.com'
                                                            }
                                                        ],
                                                        'key': 'PALVELUTARJOTINEVENT'
                                                    }
                                                ],
                                                'key': 'OCCURRENCE'
                                            }
                                        ],
                                        'key': 'ENROLMENT'
                                    },
                                    {
                                        'children': [
                                            {
                                                'key': 'ENROLMENT_TIME',
                                                'value': '2020-01-04T00:00:00+00:00'
                                            },
                                            {
                                                'key': 'UPDATED_AT',
                                                'value': '2020-01-04T00:00:00+00:00'
                                            },
                                            {
                                                'key': 'STATUS',
                                                'value': 'pending'
                                            },
                                            {
                                                'children': [
                                                    {
                                                        'key': 'START_TIME',
                                                        'value': '2018-02-12T23:26:33.996487+00:00'
                                                    },
                                                    {
                                                        'key': 'END_TIME',
                                                        'value': '2019-10-02T02:55:30.688102+00:00'
                                                    },
                                                    {
                                                        'key': 'CREATED_AT',
                                                        'value': '2020-01-04T00:00:00+00:00'
                                                    },
                                                    {
                                                        'key': 'UPDATED_AT',
                                                        'value': '2020-01-04T00:00:00+00:00'
                                                    },
                                                    {
                                                        'children': [
                                                            {
                                                                'key': 'LINKED_EVENT_ID',
                                                                'value': 'stCwh'
                                                            },
                                                            {
                                                                'key': 'ORGANISATION',
                                                                'value': 'Walters, Taylor and Boyd'
                                                            },
                                                            {
                                                                'key': 'CONTACT_PERSON',
                                                                'value': 'James Johnson, 962-942-2074x4988, bullockcarly@example.org'
                                                            }
                                                        ],
                                                        'key': 'PALVELUTARJOTINEVENT'
                                                    }
                                                ],
                                                'key': 'OCCURRENCE'
                                            }
                                        ],
                                        'key': 'ENROLMENT'
                                    }
                                ],
                                'key': 'ENROLMENTS'
                            }
                        ],
                        'key': 'STUDYGROUP'
                    },
                    {
                        'children': [
                            {
                                'key': 'UNIT_ID',
                                'value': None
                            },
                            {
                                'key': 'UNIT_NAME',
                                'value': 'Bit college question animal long. Sometimes growth check court.'
                            },
                            {
                                'key': 'GROUP_SIZE',
                                'value': 519
                            },
                            {
                                'key': 'AMOUNT_OF_ADULT',
                                'value': 0
                            },
                            {
                                'key': 'GROUP_NAME',
                                'value': 'Decade address have turn serve me every traditional. Sound describe risk newspaper reflect four.'
                            },
                            {
                                'key': 'EXTRA_NEEDS',
                                'value': 'Arm listen money language which risk.'
                            },
                            {
                                'key': 'PREFERRED_TIMES',
                                'value': 'Result let join might player.'
                            },
                            {
                                'key': 'STUDY_LEVELS',
                                'value': 'Cultural cell at. (id: Democrat., level: 3), Myself simple paper. (id: Happen., level: 4), Town back though. (id: Decade., level: 9)'
                            },
                            {
                                'children': [
                                    {
                                        'children': [
                                            {
                                                'key': 'ENROLMENT_TIME',
                                                'value': '2020-01-04T00:00:00+00:00'
                                            },
                                            {
                                                'key': 'UPDATED_AT',
                                                'value': '2020-01-04T00:00:00+00:00'
                                            },
                                            {
                                                'key': 'STATUS',
                                                'value': 'pending'
                                            },
                                            {
                                                'children': [
                                                    {
                                                        'key': 'START_TIME',
                                                        'value': '1974-05-07T19:29:45.432928+00:00'
                                                    },
                                                    {
                                                        'key': 'END_TIME',
                                                        'value': '1997-04-17T22:13:24.246198+00:00'
                                                    },
                                                    {
                                                        'key': 'CREATED_AT',
                                                        'value': '2020-01-04T00:00:00+00:00'
                                                    },
                                                    {
                                                        'key': 'UPDATED_AT',
                                                        'value': '2020-01-04T00:00:00+00:00'
                                                    },
                                                    {
                                                        'children': [
                                                            {
                                                                'key': 'LINKED_EVENT_ID',
                                                                'value': 'mbLjf'
                                                            },
                                                            {
                                                                'key': 'ORGANISATION',
                                                                'value': 'Moon-Hernandez'
                                                            },
                                                            {
                                                                'key': 'CONTACT_PERSON',
                                                                'value': 'Charles Hansen, 419.442.1317, youngpeggy@example.org'
                                                            }
                                                        ],
                                                        'key': 'PALVELUTARJOTINEVENT'
                                                    }
                                                ],
                                                'key': 'OCCURRENCE'
                                            }
                                        ],
                                        'key': 'ENROLMENT'
                                    }
                                ],
                                'key': 'ENROLMENTS'
                            }
                        ],
                        'key': 'STUDYGROUP'
                    }
                ],
                [
                    {
                        'children': [
                            {
                                'key': 'ENROLMENT_TIME',
                                'value': '2020-01-04T00:00:00+00:00'
                            },
                            {
                                'key': 'UPDATED_AT',
                                'value': '2020-01-04T00:00:00+00:00'
                            },
                            {
                                'key': 'NOTIFICATION_TYPE',
                                'value': 'email'
                            },
                            {
                                'key': 'STUDY_GROUP',
                                'value': '1 Tough plant traditional after born up always. Return student light a point charge.'
                            },
                            {
                                'children': [
                                    {
                                        'key': 'LINKED_EVENT_ID',
                                        'value': 'TwsLM'
                                    },
                                    {
                                        'key': 'ORGANISATION',
                                        'value': 'Singleton PLC'
                                    },
                                    {
                                        'key': 'CONTACT_PERSON',
                                        'value': 'Robert Davis, 327.543.4893, lanekayla@example.org'
                                    }
                                ],
                                'key': 'PALVELUTARJOTINEVENT'
                            }
                        ],
                        'key': 'EVENTQUEUEENROLMENT'
                    }
                ],
                [
                    {
                        'children': [
                            {
                                'key': 'ENROLMENT_TIME',
                                'value': '2020-01-04T00:00:00+00:00'
                            },
                            {
                                'key': 'UPDATED_AT',
                                'value': '2020-01-04T00:00:00+00:00'
                            },
                            {
                                'key': 'STATUS',
                                'value': 'pending'
                            },
                            {
                                'children': [
                                    {
                                        'key': 'START_TIME',
                                        'value': '2010-07-23T16:15:55.542261+00:00'
                                    },
                                    {
                                        'key': 'END_TIME',
                                        'value': '2008-11-04T19:11:30.730104+00:00'
                                    },
                                    {
                                        'key': 'CREATED_AT',
                                        'value': '2020-01-04T00:00:00+00:00'
                                    },
                                    {
                                        'key': 'UPDATED_AT',
                                        'value': '2020-01-04T00:00:00+00:00'
                                    },
                                    {
                                        'children': [
                                            {
                                                'key': 'LINKED_EVENT_ID',
                                                'value': 'FrTcm'
                                            },
                                            {
                                                'key': 'ORGANISATION',
                                                'value': 'Carroll, Adams and Evans'
                                            },
                                            {
                                                'key': 'CONTACT_PERSON',
                                                'value': 'Erika Martinez, (569)876-1296, mark29@example.com'
                                            }
                                        ],
                                        'key': 'PALVELUTARJOTINEVENT'
                                    }
                                ],
                                'key': 'OCCURRENCE'
                            }
                        ],
                        'key': 'ENROLMENT'
                    },
                    {
                        'children': [
                            {
                                'key': 'ENROLMENT_TIME',
                                'value': '2020-01-04T00:00:00+00:00'
                            },
                            {
                                'key': 'UPDATED_AT',
                                'value': '2020-01-04T00:00:00+00:00'
                            },
                            {
                                'key': 'STATUS',
                                'value': 'pending'
                            },
                            {
                                'children': [
                                    {
                                        'key': 'START_TIME',
                                        'value': '2018-02-12T23:26:33.996487+00:00'
                                    },
                                    {
                                        'key': 'END_TIME',
                                        'value': '2019-10-02T02:55:30.688102+00:00'
                                    },
                                    {
                                        'key': 'CREATED_AT',
                                        'value': '2020-01-04T00:00:00+00:00'
                                    },
                                    {
                                        'key': 'UPDATED_AT',
                                        'value': '2020-01-04T00:00:00+00:00'
                                    },
                                    {
                                        'children': [
                                            {
                                                'key': 'LINKED_EVENT_ID',
                                                'value': 'stCwh'
                                            },
                                            {
                                                'key': 'ORGANISATION',
                                                'value': 'Walters, Taylor and Boyd'
                                            },
                                            {
                                                'key': 'CONTACT_PERSON',
                                                'value': 'James Johnson, 962-942-2074x4988, bullockcarly@example.org'
                                            }
                                        ],
                                        'key': 'PALVELUTARJOTINEVENT'
                                    }
                                ],
                                'key': 'OCCURRENCE'
                            }
                        ],
                        'key': 'ENROLMENT'
                    },
                    {
                        'children': [
                            {
                                'key': 'ENROLMENT_TIME',
                                'value': '2020-01-04T00:00:00+00:00'
                            },
                            {
                                'key': 'UPDATED_AT',
                                'value': '2020-01-04T00:00:00+00:00'
                            },
                            {
                                'key': 'STATUS',
                                'value': 'pending'
                            },
                            {
                                'children': [
                                    {
                                        'key': 'START_TIME',
                                        'value': '1974-05-07T19:29:45.432928+00:00'
                                    },
                                    {
                                        'key': 'END_TIME',
                                        'value': '1997-04-17T22:13:24.246198+00:00'
                                    },
                                    {
                                        'key': 'CREATED_AT',
                                        'value': '2020-01-04T00:00:00+00:00'
                                    },
                                    {
                                        'key': 'UPDATED_AT',
                                        'value': '2020-01-04T00:00:00+00:00'
                                    },
                                    {
                                        'children': [
                                            {
                                                'key': 'LINKED_EVENT_ID',
                                                'value': 'mbLjf'
                                            },
                                            {
                                                'key': 'ORGANISATION',
                                                'value': 'Moon-Hernandez'
                                            },
                                            {
                                                'key': 'CONTACT_PERSON',
                                                'value': 'Charles Hansen, 419.442.1317, youngpeggy@example.org'
                                            }
                                        ],
                                        'key': 'PALVELUTARJOTINEVENT'
                                    }
                                ],
                                'key': 'OCCURRENCE'
                            }
                        ],
                        'key': 'ENROLMENT'
                    }
                ]
            ],
            'key': 'PERSON'
        }
    ],
    'key': 'USER'
}

snapshots['test_get_profile_data_from_gdpr_api[Simple User, Deleted] 1'] = {
    'children': [
        {
            'key': 'UUID',
            'value': '26850000-2e85-11ea-b347-acde48001122'
        },
        {
            'key': 'USERNAME',
            'value': 'u-e2cqaaboqui6vm2hvtpeqaarei'
        },
        {
            'key': 'FIRST_NAME',
            'value': ''
        },
        {
            'key': 'LAST_NAME',
            'value': ''
        },
        {
            'key': 'EMAIL',
            'value': ''
        },
        {
            'key': 'LAST_LOGIN',
            'value': None
        },
        {
            'key': 'DATE_JOINED',
            'value': '2020-01-04T00:00:00+00:00'
        }
    ],
    'key': 'USER'
}

snapshots['test_get_profile_data_from_gdpr_api[Simple User, Undeleted] 1'] = {
    'children': [
        {
            'key': 'UUID',
            'value': '26850000-2e85-11ea-b347-acde48001122'
        },
        {
            'key': 'USERNAME',
            'value': 'jeffersonkimberly_3MmHFh'
        },
        {
            'key': 'FIRST_NAME',
            'value': 'Alexis'
        },
        {
            'key': 'LAST_NAME',
            'value': 'Black'
        },
        {
            'key': 'EMAIL',
            'value': 'joshuajohnson@example.com'
        },
        {
            'key': 'LAST_LOGIN',
            'value': '2020-01-04T00:00:00+00:00'
        },
        {
            'key': 'DATE_JOINED',
            'value': '2020-01-04T00:00:00+00:00'
        }
    ],
    'key': 'USER'
}
