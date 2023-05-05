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
                "organisations": {"edges": [{"node": {"name": "Peters-Buchanan"}}]},
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
                "organisations": {"edges": [{"node": {"name": "Peters-Buchanan"}}]},
                "phoneNumber": "",
                "placeIds": ["xyz:123", "abc321"],
            }
        }
    }
}

snapshots["test_my_profile_query 1"] = {
    "data": {
        "myProfile": {
            "emailAddress": "longrebecca@example.com",
            "isStaff": False,
            "language": "FI",
            "name": "Richard Hayes",
            "organisations": {"edges": [{"node": {"name": "Harris Inc"}}]},
            "phoneNumber": "557.776.7124",
            "placeIds": ["pyLmAmuDyxTUOfTVXgFf"],
        }
    }
}

snapshots["test_my_profile_query 2"] = {
    "data": {
        "myProfile": {
            "emailAddress": "nicole77@example.net",
            "isStaff": True,
            "language": "FI",
            "name": "James Reed",
            "organisations": {"edges": [{"node": {"name": "Harris Inc"}}]},
            "phoneNumber": "001-825-058-0719",
            "placeIds": ["KQQJMHyYXxEprsbAXEni", "lygJhpAZXxwQoxZHkjdK"],
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
                                "groupName": "Federal minute paper third item future far power. College information training."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Focus few executive. Movie work organization successful. Fear teacher loss sea just soon food."
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
                                "groupName": "Tv news management letter. Animal list adult draw staff her."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Second know say former conference carry factor. Natural each difficult special respond positive."
                            }
                        }
                    },
                ]
            },
            "name": "Nancy Conway",
        }
    }
}

snapshots["test_person_query 1"] = {"data": {"person": None}}

snapshots["test_person_query 2"] = {"data": {"person": None}}

snapshots["test_person_query 3"] = {
    "data": {
        "person": {
            "emailAddress": "gonzalezmichele@example.org",
            "language": "FI",
            "name": "Wanda Rubio",
            "organisations": {"edges": []},
            "phoneNumber": "694.703.2322x217",
            "placeIds": ["dZDVgFLcfOQPeHMMTVcH", "QIIHoLALPuMgdVNrNeAh"],
        }
    }
}

snapshots["test_person_query 4"] = {
    "data": {
        "person": {
            "emailAddress": "anthonycross@example.com",
            "language": "FI",
            "name": "Shawn Santana",
            "organisations": {"edges": [{"node": {"name": "Day-Gibson"}}]},
            "phoneNumber": "001-117-159-1023x20281",
            "placeIds": [
                "CCezaIinzTPCrDgtoNZh",
                "COmRVJDOXAmjOnQtrkEQ",
                "KcMIonuxkiABRtJfcwOr",
            ],
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
                                "groupName": "Anyone conference should feel produce wife. Wonder pressure stage research direction forget list."
                            }
                        }
                    },
                    {
                        "node": {
                            "studyGroup": {
                                "groupName": "Tonight use form simply trade minute production."
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
                                "groupName": "Hotel event already college. Ok court type hit."
                            }
                        }
                    },
                    {"node": {"studyGroup": {"groupName": "Six feel real fast."}}},
                ]
            },
            "name": "Nancy Conway",
        }
    }
}

snapshots["test_person_study_groups 1"] = {
    "data": {
        "person": {
            "name": "Nancy Conway",
            "studygroupSet": {
                "edges": [
                    {
                        "node": {
                            "groupName": "Second know say former conference carry factor. Natural each difficult special respond positive."
                        }
                    },
                    {
                        "node": {
                            "groupName": "Tv news management letter. Animal list adult draw staff her."
                        }
                    },
                    {
                        "node": {
                            "groupName": "Eat design give per kind history ahead. Herself consider fight us claim. Age feeling speech eye."
                        }
                    },
                    {
                        "node": {
                            "groupName": "Focus few executive. Movie work organization successful. Fear teacher loss sea just soon food."
                        }
                    },
                    {
                        "node": {
                            "groupName": "Federal minute paper third item future far power. College information training."
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
                        "emailAddress": "gonzalezmichele@example.org",
                        "language": "FI",
                        "name": "Wanda Rubio",
                        "organisations": {"edges": []},
                        "phoneNumber": "694.703.2322x217",
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
                        "emailAddress": "hannah75@example.com",
                        "language": "FI",
                        "name": "Janet Ritter",
                        "organisations": {"edges": []},
                        "phoneNumber": "494-811-8845x2419",
                    }
                },
                {
                    "node": {
                        "emailAddress": "anthonycross@example.com",
                        "language": "FI",
                        "name": "Shawn Santana",
                        "organisations": {"edges": [{"node": {"name": "Day-Gibson"}}]},
                        "phoneNumber": "001-117-159-1023x20281",
                    }
                },
                {
                    "node": {
                        "emailAddress": "gonzalezmichele@example.org",
                        "language": "FI",
                        "name": "Wanda Rubio",
                        "organisations": {"edges": []},
                        "phoneNumber": "694.703.2322x217",
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
                "phoneNumber": "557.776.7124",
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
                "phoneNumber": "557.776.7124",
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
                "organisations": {"edges": [{"node": {"name": "Day-Gibson"}}]},
                "phoneNumber": "001-117-159-1023x20281",
            }
        }
    }
}
