# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_add_organisation 1"] = {
    "data": {
        "addOrganisation": {
            "organisation": {
                "name": "New organisation",
                "phoneNumber": "012345678",
                "publisherId": "publisher_id",
                "type": "PROVIDER",
            }
        }
    }
}

snapshots["test_create_my_profile 1"] = {
    "data": {
        "createMyProfile": {
            "myProfile": {
                "emailAddress": "newEmail@address.com",
                "isStaff": False,
                "language": "EN",
                "name": "New name",
                "organisationproposalSet": {
                    "edges": [{"node": {"name": "3rd party org"}}]
                },
                "organisations": {
                    "edges": [{"node": {"name": "Myers, Ellis and Gonzalez"}}]
                },
                "phoneNumber": "",
                "placeIds": [],
            }
        }
    }
}

snapshots["test_create_my_profile_with_place_ids 1"] = {
    "data": {
        "createMyProfile": {
            "myProfile": {
                "emailAddress": "newEmail@address.com",
                "isStaff": False,
                "language": "EN",
                "name": "New name",
                "organisationproposalSet": {
                    "edges": [{"node": {"name": "3rd party org"}}]
                },
                "organisations": {
                    "edges": [{"node": {"name": "Myers, Ellis and Gonzalez"}}]
                },
                "phoneNumber": "",
                "placeIds": ["xyz:123", "abc321"],
            }
        }
    }
}

snapshots["test_my_profile_query 1"] = {
    "data": {
        "myProfile": {
            "emailAddress": "hutchinsonrachel@example.org",
            "isStaff": False,
            "language": "FI",
            "name": "Amanda Newton",
            "organisations": {"edges": [{"node": {"name": "Smith, Wood and Baker"}}]},
            "phoneNumber": "976-380-3466x9727",
            "placeIds": ["VXgFfhhcjebLxIzCCeza", "knnouKQItjsGbbnCZaIe"],
        }
    }
}

snapshots["test_my_profile_query 2"] = {
    "data": {
        "myProfile": {
            "emailAddress": "natalie62@example.com",
            "isStaff": True,
            "language": "FI",
            "name": "Cheyenne Carson",
            "organisations": {"edges": [{"node": {"name": "Smith, Wood and Baker"}}]},
            "phoneNumber": "001-959-911-8326x3986",
            "placeIds": ["lLyOWeWgxNvIdaNadghC", "GVbfWcQLRyaHhQRmINWY"],
        }
    }
}

snapshots["test_organisation_query 1"] = {
    "data": {
        "organisation": {
            "name": "Graves and Sons",
            "persons": {"edges": []},
            "phoneNumber": "+1-906-333-4577",
            "publisherId": "rtOzV",
            "type": "USER",
        }
    }
}

snapshots["test_organisations_query 1"] = {
    "data": {
        "organisations": {
            "edges": [
                {
                    "node": {
                        "name": "Graves and Sons",
                        "persons": {"edges": []},
                        "phoneNumber": "+1-906-333-4577",
                        "publisherId": "rtOzV",
                        "type": "USER",
                    }
                }
            ]
        }
    }
}

snapshots["test_organisations_query_type_filter 1"] = {
    "data": {
        "organisations": {
            "edges": [
                {
                    "node": {
                        "name": "Graves and Sons",
                        "persons": {"edges": []},
                        "phoneNumber": "+1-906-333-4577",
                        "publisherId": "VrtOz",
                        "type": "PROVIDER",
                    }
                },
                {
                    "node": {
                        "name": "Bryant-Davis",
                        "persons": {"edges": []},
                        "phoneNumber": "067-506-4976x380",
                        "publisherId": "muDyx",
                        "type": "PROVIDER",
                    }
                },
                {
                    "node": {
                        "name": "Garcia Group",
                        "persons": {"edges": []},
                        "phoneNumber": "+1-159-102-3202x8130",
                        "publisherId": "yiWRb",
                        "type": "PROVIDER",
                    }
                },
            ]
        }
    }
}

snapshots["test_organisations_query_type_filter 2"] = {
    "data": {
        "organisations": {
            "edges": [
                {
                    "node": {
                        "name": "Hawkins, Davis and Porter",
                        "persons": {"edges": []},
                        "phoneNumber": "1234474468",
                        "publisherId": "KQItj",
                        "type": "USER",
                    }
                },
                {
                    "node": {
                        "name": "Mack-Travis",
                        "persons": {"edges": []},
                        "phoneNumber": "(048)830-1905",
                        "publisherId": "XAmjO",
                        "type": "USER",
                    }
                },
            ]
        }
    }
}

snapshots["test_person_enrolments 1"] = {
    "data": {
        "person": {
            "enrolmentSet": {
                "edges": [
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Work early property your stage receive. Determine sort under car."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Ask alone them yeah none young area. Guy Democrat throw score watch method political."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Eat design give per kind history ahead. Herself consider fight us claim. Age feeling speech eye."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": """Apply somebody especially far. Color price environmental.
Market him beyond."""
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Tend practice other poor. Carry owner sense other can loss get girl."
                            }
                        }
                    },
                ]
            },
            "name": "Patrick Estrada",
        }
    }
}

snapshots["test_person_query 1"] = {"data": {"person": None}}

snapshots["test_person_query 2"] = {"data": {"person": None}}

snapshots["test_person_query 3"] = {
    "data": {
        "person": {
            "emailAddress": "imonroe@example.org",
            "language": "FI",
            "name": "Natalie Keith",
            "organisations": {"edges": []},
            "phoneNumber": "+1-042-405-4852",
            "placeIds": ["FDdlvJGuUZtSihlLyOWe", "iaGbqMPXLzvLVGVbfWcQ"],
        }
    }
}

snapshots["test_person_query 4"] = {
    "data": {
        "person": {
            "emailAddress": "andrewgreen@example.net",
            "language": "FI",
            "name": "Carolyn Scott",
            "organisations": {"edges": [{"node": {"name": "Williams-Newton"}}]},
            "phoneNumber": "446.858.1662x4590",
            "placeIds": ["RVJDOXAmjOnQtrkEQOln", "VMNZoGFTsuALvDSCvIVy"],
        }
    }
}

snapshots["test_person_queued_enrolments 1"] = {
    "data": {
        "person": {
            "eventqueueenrolmentSet": {
                "edges": [
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Second yet pay. First teach democratic."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Reach ask I cut ok. Perhaps teacher involve all my improve our Congress."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Play make war chance discover throw. Crime imagine wall two economy. Far power animal society Mrs."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "By rate activity business let art. Admit think edge once election seat."
                            }
                        }
                    },
                    {"node": {"studyGroup": {"groupName": "Six feel real fast."}}},
                ]
            },
            "name": "Patrick Estrada",
        }
    }
}

snapshots["test_person_study_groups 1"] = {
    "data": {
        "person": {
            "name": "Patrick Estrada",
            "studygroupSet": {
                "edges": [
                    {
                        "node": {
                            "groupName": "Work early property your stage receive. Determine sort under car."
                        }
                    },
                    {
                        "node": {
                            "groupName": "Ask alone them yeah none young area. Guy Democrat throw score watch method political."
                        }
                    },
                    {
                        "node": {
                            "groupName": "Eat design give per kind history ahead. Herself consider fight us claim. Age feeling speech eye."
                        }
                    },
                    {
                        "node": {
                            "groupName": """Apply somebody especially far. Color price environmental.
Market him beyond."""
                        }
                    },
                    {
                        "node": {
                            "groupName": "Tend practice other poor. Carry owner sense other can loss get girl."
                        }
                    },
                ]
            },
        }
    }
}

snapshots["test_persons_query 1"] = {"data": {"persons": {"edges": []}}}

snapshots["test_persons_query 2"] = {"data": {"persons": {"edges": []}}}

snapshots["test_persons_query 3"] = {
    "data": {
        "persons": {
            "edges": [
                {
                    "node": {
                        "emailAddress": "imonroe@example.org",
                        "language": "FI",
                        "name": "Natalie Keith",
                        "organisations": {"edges": []},
                        "phoneNumber": "+1-042-405-4852",
                    }
                }
            ]
        }
    }
}

snapshots["test_persons_query 4"] = {
    "data": {
        "persons": {
            "edges": [
                {
                    "node": {
                        "emailAddress": "andrewgreen@example.net",
                        "language": "FI",
                        "name": "Carolyn Scott",
                        "organisations": {
                            "edges": [{"node": {"name": "Williams-Newton"}}]
                        },
                        "phoneNumber": "446.858.1662x4590",
                    }
                },
                {
                    "node": {
                        "emailAddress": "kwebster@example.net",
                        "language": "FI",
                        "name": "Jessica Baker",
                        "organisations": {"edges": []},
                        "phoneNumber": "001-659-825-0580",
                    }
                },
                {
                    "node": {
                        "emailAddress": "imonroe@example.org",
                        "language": "FI",
                        "name": "Natalie Keith",
                        "organisations": {"edges": []},
                        "phoneNumber": "+1-042-405-4852",
                    }
                },
            ]
        }
    }
}

snapshots["test_update_my_profile 1"] = {
    "data": {
        "updateMyProfile": {
            "myProfile": {
                "emailAddress": "newEmail@address.com",
                "isStaff": False,
                "language": "SV",
                "name": "New name",
                "organisations": {"edges": []},
                "phoneNumber": "976-380-3466x9727",
                "placeIds": ["xyz:123", "xxx:123"],
            }
        }
    }
}

snapshots["test_update_organisation 1"] = {
    "data": {
        "updateOrganisation": {
            "organisation": {
                "name": "New name",
                "phoneNumber": "976-380-3466x9727",
                "publisherId": "publisher_id",
                "type": "USER",
            }
        }
    }
}

snapshots["test_update_person_mutation[firstlast@example.com-True] 1"] = {
    "data": {
        "updatePerson": {
            "person": {
                "emailAddress": "firstlast@example.com",
                "language": "SV",
                "name": "New name",
                "organisations": {"edges": [{"node": {"name": "Williams-Newton"}}]},
                "phoneNumber": "446.858.1662x4590",
            }
        }
    }
}
