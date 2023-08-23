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
                                "groupName": "College wife serve entire. House down woman peace. Plant on follow return research could."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Policy parent toward apply see on send in. Full three especially card animal recognize stock."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "See quite tax my often society. Subject law ok."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Watch method political institution trip race kitchen. Send same even child."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Work early property your stage receive. Determine sort under car."
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
                                "groupName": "Scene practice town right perform yes picture. Art movement movement analysis require statement."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Civil find learn follow. Tend practice other poor."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Before television between policy parent. Apply see on send."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Eight direction she play catch miss. Strategy animal who management then some threat."
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
                            "groupName": "Watch method political institution trip race kitchen. Send same even child."
                        }
                    },
                    {
                        "node": {
                            "groupName": "See quite tax my often society. Subject law ok."
                        }
                    },
                    {
                        "node": {
                            "groupName": "Policy parent toward apply see on send in. Full three especially card animal recognize stock."
                        }
                    },
                    {
                        "node": {
                            "groupName": "College wife serve entire. House down woman peace. Plant on follow return research could."
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
