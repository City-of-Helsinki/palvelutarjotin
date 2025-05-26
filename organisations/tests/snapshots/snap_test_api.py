# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_add_organisation 1'] = {
    'data': {
        'addOrganisation': {
            'organisation': {
                'name': 'New organisation',
                'phoneNumber': '012345678',
                'publisherId': 'publisher_id',
                'type': 'PROVIDER'
            }
        }
    }
}

snapshots['test_create_my_profile 1'] = {
    'data': {
        'createMyProfile': {
            'myProfile': {
                'emailAddress': 'newEmail@address.com',
                'isStaff': False,
                'language': 'EN',
                'name': 'New name',
                'organisationproposalSet': {
                    'edges': [
                        {
                            'node': {
                                'name': '3rd party org'
                            }
                        }
                    ]
                },
                'organisations': {
                    'edges': [
                        {
                            'node': {
                                'name': 'Myers, Ellis and Gonzalez'
                            }
                        }
                    ]
                },
                'phoneNumber': '',
                'placeIds': [
                ]
            }
        }
    }
}

snapshots['test_create_my_profile_with_place_ids 1'] = {
    'data': {
        'createMyProfile': {
            'myProfile': {
                'emailAddress': 'newEmail@address.com',
                'isStaff': False,
                'language': 'EN',
                'name': 'New name',
                'organisationproposalSet': {
                    'edges': [
                        {
                            'node': {
                                'name': '3rd party org'
                            }
                        }
                    ]
                },
                'organisations': {
                    'edges': [
                        {
                            'node': {
                                'name': 'Myers, Ellis and Gonzalez'
                            }
                        }
                    ]
                },
                'phoneNumber': '',
                'placeIds': [
                    'xyz:123',
                    'abc321'
                ]
            }
        }
    }
}

snapshots['test_my_profile_query 1'] = {
    'data': {
        'myProfile': {
            'emailAddress': 'hutchinsonrachel@example.org',
            'isStaff': False,
            'language': 'FI',
            'name': 'Amanda Newton',
            'organisations': {
                'edges': [
                    {
                        'node': {
                            'name': 'Smith, Wood and Baker'
                        }
                    }
                ]
            },
            'phoneNumber': '497-963-8034x6697',
            'placeIds': [
                'VXgFfhhcjebLxIzCCeza',
                'knnouKQItjsGbbnCZaIe'
            ]
        }
    }
}

snapshots['test_my_profile_query 2'] = {
    'data': {
        'myProfile': {
            'emailAddress': 'jmoore@example.org',
            'isStaff': True,
            'language': 'FI',
            'name': 'Cheyenne Carson',
            'organisations': {
                'edges': [
                    {
                        'node': {
                            'name': 'Smith, Wood and Baker'
                        }
                    }
                ]
            },
            'phoneNumber': '001-895-799-1183x2639',
            'placeIds': [
                'yOWeWgxNvIdaNadghCet',
                'YgCAuXtmqVxzDraSqNld'
            ]
        }
    }
}

snapshots['test_organisation_query 1'] = {
    'data': {
        'organisation': {
            'name': 'Graves and Sons',
            'persons': {
                'edges': [
                ]
            },
            'phoneNumber': '+1-990-963-3345',
            'publisherId': 'rtOzV',
            'type': 'USER'
        }
    }
}

snapshots['test_organisations_query 1'] = {
    'data': {
        'organisations': {
            'edges': [
                {
                    'node': {
                        'name': 'Graves and Sons',
                        'persons': {
                            'edges': [
                            ]
                        },
                        'phoneNumber': '+1-990-963-3345',
                        'publisherId': 'rtOzV',
                        'type': 'USER'
                    }
                }
            ]
        }
    }
}

snapshots['test_organisations_query_type_filter 1'] = {
    'data': {
        'organisations': {
            'edges': [
                {
                    'node': {
                        'name': 'Bryant-Davis',
                        'persons': {
                            'edges': [
                            ]
                        },
                        'phoneNumber': '206-575-0649x763',
                        'publisherId': 'nvThb',
                        'type': 'PROVIDER'
                    }
                },
                {
                    'node': {
                        'name': 'Garcia Group',
                        'persons': {
                            'edges': [
                            ]
                        },
                        'phoneNumber': '+1-515-291-0232x0281',
                        'publisherId': 'yiWRb',
                        'type': 'PROVIDER'
                    }
                },
                {
                    'node': {
                        'name': 'Graves and Sons',
                        'persons': {
                            'edges': [
                            ]
                        },
                        'phoneNumber': '+1-990-963-3345',
                        'publisherId': 'VrtOz',
                        'type': 'PROVIDER'
                    }
                }
            ]
        }
    }
}

snapshots['test_organisations_query_type_filter 2'] = {
    'data': {
        'organisations': {
            'edges': [
                {
                    'node': {
                        'name': 'Hawkins, Davis and Porter',
                        'persons': {
                            'edges': [
                            ]
                        },
                        'phoneNumber': '8127344744',
                        'publisherId': 'QItjs',
                        'type': 'USER'
                    }
                },
                {
                    'node': {
                        'name': 'Travis, Thomas and Ochoa',
                        'persons': {
                            'edges': [
                            ]
                        },
                        'phoneNumber': '+1-583-401-9054',
                        'publisherId': 'jOnQt',
                        'type': 'USER'
                    }
                }
            ]
        }
    }
}

snapshots['test_person_enrolments 1'] = {
    'data': {
        'person': {
            'enrolmentSet': {
                'edges': [
                    {
                        'node': {
                            'studyGroup': {
                                'groupName': 'Hand human value base pattern democratic focus. Kind various laugh smile behavior.'
                            }
                        }
                    },
                    {
                        'node': {
                            'studyGroup': {
                                'groupName': 'Close term where up notice environment father stay. Hold project month similar support line.'
                            }
                        }
                    },
                    {
                        'node': {
                            'studyGroup': {
                                'groupName': 'Eat design give per kind history ahead. Herself consider fight us claim. Age feeling speech eye.'
                            }
                        }
                    },
                    {
                        'node': {
                            'studyGroup': {
                                'groupName': '''Apply somebody especially far. Color price environmental.
Market him beyond.'''
                            }
                        }
                    },
                    {
                        'node': {
                            'studyGroup': {
                                'groupName': 'Civil find learn follow. Tend practice other poor.'
                            }
                        }
                    }
                ]
            },
            'name': 'Patrick Estrada'
        }
    }
}

snapshots['test_person_query 1'] = {
    'data': {
        'person': None
    }
}

snapshots['test_person_query 2'] = {
    'data': {
        'person': None
    }
}

snapshots['test_person_query 3'] = {
    'data': {
        'person': {
            'emailAddress': 'jacobbrown@example.net',
            'language': 'FI',
            'name': 'Brian Daniels',
            'organisations': {
                'edges': [
                ]
            },
            'phoneNumber': '440.584.7694x703',
            'placeIds': [
                'nddsAMQQNGTIkhlhOSlf',
                'VcHUQIIHoLALPuMgdVNr'
            ]
        }
    }
}

snapshots['test_person_query 4'] = {
    'data': {
        'person': {
            'emailAddress': 'ochoaangela@example.org',
            'language': 'FI',
            'name': 'Carolyn Scott',
            'organisations': {
                'edges': [
                    {
                        'node': {
                            'name': 'Williams-Newton'
                        }
                    }
                ]
            },
            'phoneNumber': '244.468.5816x6245',
            'placeIds': [
                'JDOXAmjOnQtrkEQOlnVO'
            ]
        }
    }
}

snapshots['test_person_queued_enrolments 1'] = {
    'data': {
        'person': {
            'eventqueueenrolmentSet': {
                'edges': [
                    {
                        'node': {
                            'studyGroup': {
                                'groupName': 'Let join might player example environment. Then offer organization model.'
                            }
                        }
                    },
                    {
                        'node': {
                            'studyGroup': {
                                'groupName': 'By rate activity business let art. Admit think edge once election seat.'
                            }
                        }
                    },
                    {
                        'node': {
                            'studyGroup': {
                                'groupName': 'Play make war chance discover throw. Crime imagine wall two economy. Far power animal society Mrs.'
                            }
                        }
                    },
                    {
                        'node': {
                            'studyGroup': {
                                'groupName': 'Reach ask I cut ok. Perhaps teacher involve all my improve our Congress.'
                            }
                        }
                    },
                    {
                        'node': {
                            'studyGroup': {
                                'groupName': 'Second yet pay. First teach democratic.'
                            }
                        }
                    }
                ]
            },
            'name': 'Patrick Estrada'
        }
    }
}

snapshots['test_person_study_groups 1'] = {
    'data': {
        'person': {
            'name': 'Patrick Estrada',
            'studygroupSet': {
                'edges': [
                    {
                        'node': {
                            'groupName': 'Hand human value base pattern democratic focus. Kind various laugh smile behavior.'
                        }
                    },
                    {
                        'node': {
                            'groupName': 'Close term where up notice environment father stay. Hold project month similar support line.'
                        }
                    },
                    {
                        'node': {
                            'groupName': 'Eat design give per kind history ahead. Herself consider fight us claim. Age feeling speech eye.'
                        }
                    },
                    {
                        'node': {
                            'groupName': '''Apply somebody especially far. Color price environmental.
Market him beyond.'''
                        }
                    },
                    {
                        'node': {
                            'groupName': 'Civil find learn follow. Tend practice other poor.'
                        }
                    }
                ]
            }
        }
    }
}

snapshots['test_persons_query 1'] = {
    'data': {
        'persons': {
            'edges': [
            ]
        }
    }
}

snapshots['test_persons_query 2'] = {
    'data': {
        'persons': {
            'edges': [
            ]
        }
    }
}

snapshots['test_persons_query 3'] = {
    'data': {
        'persons': {
            'edges': [
                {
                    'node': {
                        'emailAddress': 'jacobbrown@example.net',
                        'language': 'FI',
                        'name': 'Brian Daniels',
                        'organisations': {
                            'edges': [
                            ]
                        },
                        'phoneNumber': '440.584.7694x703'
                    }
                }
            ]
        }
    }
}

snapshots['test_persons_query 4'] = {
    'data': {
        'persons': {
            'edges': [
                {
                    'node': {
                        'emailAddress': 'michael41@example.net',
                        'language': 'FI',
                        'name': 'Brett Dean',
                        'organisations': {
                            'edges': [
                            ]
                        },
                        'phoneNumber': '+1-362-312-6661x44948'
                    }
                },
                {
                    'node': {
                        'emailAddress': 'jacobbrown@example.net',
                        'language': 'FI',
                        'name': 'Brian Daniels',
                        'organisations': {
                            'edges': [
                            ]
                        },
                        'phoneNumber': '440.584.7694x703'
                    }
                },
                {
                    'node': {
                        'emailAddress': 'ochoaangela@example.org',
                        'language': 'FI',
                        'name': 'Carolyn Scott',
                        'organisations': {
                            'edges': [
                                {
                                    'node': {
                                        'name': 'Williams-Newton'
                                    }
                                }
                            ]
                        },
                        'phoneNumber': '244.468.5816x6245'
                    }
                }
            ]
        }
    }
}

snapshots['test_update_my_profile 1'] = {
    'data': {
        'updateMyProfile': {
            'myProfile': {
                'emailAddress': 'newEmail@address.com',
                'isStaff': False,
                'language': 'SV',
                'name': 'New name',
                'organisations': {
                    'edges': [
                    ]
                },
                'phoneNumber': '497-963-8034x6697',
                'placeIds': [
                    'xyz:123',
                    'xxx:123'
                ]
            }
        }
    }
}

snapshots['test_update_organisation 1'] = {
    'data': {
        'updateOrganisation': {
            'organisation': {
                'name': 'New name',
                'phoneNumber': '497-963-8034x6697',
                'publisherId': 'publisher_id',
                'type': 'USER'
            }
        }
    }
}

snapshots['test_update_person_mutation[firstlast@example.com-True] 1'] = {
    'data': {
        'updatePerson': {
            'person': {
                'emailAddress': 'firstlast@example.com',
                'language': 'SV',
                'name': 'New name',
                'organisations': {
                    'edges': [
                        {
                            'node': {
                                'name': 'Williams-Newton'
                            }
                        }
                    ]
                },
                'phoneNumber': '244.468.5816x6245'
            }
        }
    }
}
