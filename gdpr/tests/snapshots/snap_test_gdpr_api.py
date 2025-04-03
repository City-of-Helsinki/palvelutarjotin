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
                    'value': '2010-07-23T14:55:55.542261+00:00'
                },
                {
                    'key': 'END_TIME',
                    'value': '2008-11-04T18:51:30.730104+00:00'
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
                            'value': ''
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
                    'value': 'NoYfT'
                },
                {
                    'key': 'ORGANISATION',
                    'value': 'Rosario and Sons'
                },
                {
                    'key': 'CONTACT_PERSON',
                    'value': 'Justin Smith, 001-605-453-1010, santiagoalicia@example.net'
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
            'value': 'National since collection goal natural. Subject take stop debate.'
        },
        {
            'key': 'GROUP_SIZE',
            'value': 857
        },
        {
            'key': 'AMOUNT_OF_ADULT',
            'value': 0
        },
        {
            'key': 'GROUP_NAME',
            'value': 'Box bring always million eat several. Seven section partner. During their at once exactly.'
        },
        {
            'key': 'EXTRA_NEEDS',
            'value': 'Whose our politics contain blood interview. Cup must tough edge part. Respond pressure people.'
        },
        {
            'key': 'PREFERRED_TIMES',
            'value': 'Sport page if.'
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
                                    'value': '1975-04-25T05:34:32.227218+00:00'
                                },
                                {
                                    'key': 'END_TIME',
                                    'value': '2007-03-16T16:41:40.163531+00:00'
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
                                            'value': 'ulLnD'
                                        },
                                        {
                                            'key': 'ORGANISATION',
                                            'value': 'Guerrero-Powell'
                                        },
                                        {
                                            'key': 'CONTACT_PERSON',
                                            'value': ''
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
                                'value': 'Conference thing much like test.'
                            },
                            {
                                'key': 'GROUP_SIZE',
                                'value': 261
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
                                'value': 'Somebody determine sort under car medical. Particular page step radio.'
                            },
                            {
                                'key': 'PREFERRED_TIMES',
                                'value': 'Result let join might player.'
                            },
                            {
                                'key': 'STUDY_LEVELS',
                                'value': 'age 0-2 (id: age_0_2, level: 0), age 3-4 (id: age_3_4, level: 1), preschool (id: preschool, level: 2)'
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
                                                        'value': '1975-04-25T05:34:32.227218+00:00'
                                                    },
                                                    {
                                                        'key': 'END_TIME',
                                                        'value': '2007-03-16T16:41:40.163531+00:00'
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
                                                                'value': 'ulLnD'
                                                            },
                                                            {
                                                                'key': 'ORGANISATION',
                                                                'value': 'Guerrero-Powell'
                                                            },
                                                            {
                                                                'key': 'CONTACT_PERSON',
                                                                'value': 'Tina Wilson, +1-910-423-2028x130, fhuynh@example.org'
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
                                'value': 'Control as receive cup. Subject family around year.'
                            },
                            {
                                'key': 'GROUP_SIZE',
                                'value': 914
                            },
                            {
                                'key': 'AMOUNT_OF_ADULT',
                                'value': 0
                            },
                            {
                                'key': 'GROUP_NAME',
                                'value': 'Tough plant traditional after born up always. Return student light a point charge.'
                            },
                            {
                                'key': 'EXTRA_NEEDS',
                                'value': 'Prevent pressure point. Voice radio happen color scene.'
                            },
                            {
                                'key': 'PREFERRED_TIMES',
                                'value': 'New expert interview.'
                            },
                            {
                                'key': 'STUDY_LEVELS',
                                'value': 'age 0-2 (id: age_0_2, level: 0), age 3-4 (id: age_3_4, level: 1), preschool (id: preschool, level: 2)'
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
                                                        'value': '2010-07-23T14:55:55.542261+00:00'
                                                    },
                                                    {
                                                        'key': 'END_TIME',
                                                        'value': '2008-11-04T18:51:30.730104+00:00'
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
                                                                'value': 'Tina Wilson, +1-910-423-2028x130, fhuynh@example.org'
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
                                                        'value': '2004-12-30T07:48:32.863351+00:00'
                                                    },
                                                    {
                                                        'key': 'END_TIME',
                                                        'value': '1983-05-12T23:37:18.020950+00:00'
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
                                                                'value': 'IWSGq'
                                                            },
                                                            {
                                                                'key': 'ORGANISATION',
                                                                'value': 'Moore, Ryan and Morris'
                                                            },
                                                            {
                                                                'key': 'CONTACT_PERSON',
                                                                'value': 'Tina Wilson, +1-910-423-2028x130, fhuynh@example.org'
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
                                'value': '1 Control as receive cup. Subject family around year.'
                            },
                            {
                                'children': [
                                    {
                                        'key': 'LINKED_EVENT_ID',
                                        'value': 'NoYfT'
                                    },
                                    {
                                        'key': 'ORGANISATION',
                                        'value': 'Rosario and Sons'
                                    },
                                    {
                                        'key': 'CONTACT_PERSON',
                                        'value': 'Justin Smith, 001-605-453-1010, santiagoalicia@example.net'
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
                                        'value': '2010-07-23T14:55:55.542261+00:00'
                                    },
                                    {
                                        'key': 'END_TIME',
                                        'value': '2008-11-04T18:51:30.730104+00:00'
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
                                                'value': 'Tina Wilson, +1-910-423-2028x130, fhuynh@example.org'
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
                                        'value': '2004-12-30T07:48:32.863351+00:00'
                                    },
                                    {
                                        'key': 'END_TIME',
                                        'value': '1983-05-12T23:37:18.020950+00:00'
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
                                                'value': 'IWSGq'
                                            },
                                            {
                                                'key': 'ORGANISATION',
                                                'value': 'Moore, Ryan and Morris'
                                            },
                                            {
                                                'key': 'CONTACT_PERSON',
                                                'value': 'Tina Wilson, +1-910-423-2028x130, fhuynh@example.org'
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
                                        'value': '1975-04-25T05:34:32.227218+00:00'
                                    },
                                    {
                                        'key': 'END_TIME',
                                        'value': '2007-03-16T16:41:40.163531+00:00'
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
                                                'value': 'ulLnD'
                                            },
                                            {
                                                'key': 'ORGANISATION',
                                                'value': 'Guerrero-Powell'
                                            },
                                            {
                                                'key': 'CONTACT_PERSON',
                                                'value': 'Tina Wilson, +1-910-423-2028x130, fhuynh@example.org'
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
