# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_persons_query 1"] = {"data": {"persons": {"edges": []}}}

snapshots["test_persons_query 2"] = {"data": {"persons": {"edges": []}}}

snapshots["test_persons_query 3"] = {
    "data": {
        "persons": {
            "edges": [
                {
                    "node": {
                        "emailAddress": "garciakimberly@hotmail.com",
                        "language": "FI",
                        "name": "Arthur Dominguez",
                        "organisations": {"edges": []},
                        "phoneNumber": "(114)508-9299",
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
                        "emailAddress": "garciakimberly@hotmail.com",
                        "language": "FI",
                        "name": "Arthur Dominguez",
                        "organisations": {"edges": []},
                        "phoneNumber": "(114)508-9299",
                    }
                },
                {
                    "node": {
                        "emailAddress": "travis89@davis-porter.com",
                        "language": "FI",
                        "name": "Jacqueline Salas",
                        "organisations": {
                            "edges": [{"node": {"name": "Terrell Group"}}]
                        },
                        "phoneNumber": "3202813072",
                    }
                },
                {
                    "node": {
                        "emailAddress": "ncombs@hill.com",
                        "language": "FI",
                        "name": "Jeffery Norman",
                        "organisations": {"edges": []},
                        "phoneNumber": "369-317-9621x266",
                    }
                },
            ]
        }
    }
}

snapshots["test_person_query 1"] = {"data": {"person": None}}

snapshots["test_person_query 2"] = {"data": {"person": None}}

snapshots["test_person_query 3"] = {
    "data": {
        "person": {
            "emailAddress": "garciakimberly@hotmail.com",
            "language": "FI",
            "name": "Arthur Dominguez",
            "organisations": {"edges": []},
            "phoneNumber": "(114)508-9299",
            "placeIds": ["HMMTVcHUQIIHoLALPuMg", "VNrNeAhkMBVEOTtwlFnU"],
        }
    }
}

snapshots["test_person_query 4"] = {
    "data": {
        "person": {
            "emailAddress": "travis89@davis-porter.com",
            "language": "FI",
            "name": "Jacqueline Salas",
            "organisations": {"edges": [{"node": {"name": "Terrell Group"}}]},
            "phoneNumber": "3202813072",
            "placeIds": ["nnouKQItjsGbbnCZaIeO", "tnXjyxRexoPZaRKcMIon"],
        }
    }
}

snapshots["test_organisations_query 1"] = {
    "data": {
        "organisations": {
            "edges": [
                {
                    "node": {
                        "name": "Black Ltd",
                        "persons": {"edges": []},
                        "phoneNumber": "063.334.5773x557",
                        "publisherId": "Vxeob",
                        "type": "USER",
                    }
                }
            ]
        }
    }
}

snapshots["test_organisation_query 1"] = {
    "data": {
        "organisation": {
            "name": "Black Ltd",
            "persons": {"edges": []},
            "phoneNumber": "063.334.5773x557",
            "publisherId": "Vxeob",
            "type": "USER",
        }
    }
}

snapshots["test_my_profile_query 1"] = {
    "data": {
        "myProfile": {
            "emailAddress": "stephanieskinner@gmail.com",
            "isStaff": False,
            "language": "FI",
            "name": "William Brewer",
            "organisations": {
                "edges": [{"node": {"name": "Thomas, Ochoa and Peters"}}]
            },
            "phoneNumber": "(767)124-0675x064",
            "placeIds": ["DyxTUOfTVXgFfhhcjebL", "IzCCezaIinzTPCrDgtoN"],
        }
    }
}

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

snapshots["test_update_organisation 1"] = {
    "data": {
        "updateOrganisation": {
            "organisation": {
                "name": "New name",
                "phoneNumber": "(767)124-0675x064",
                "publisherId": "publisher_id",
                "type": "PROVIDER",
            }
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
                "phoneNumber": "(767)124-0675x064",
                "placeIds": ["xyz:123", "xxx:123"],
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
                "organisations": {"edges": [{"node": {"name": "Terrell Group"}}]},
                "phoneNumber": "3202813072",
            }
        }
    }
}

snapshots["test_my_profile_query 2"] = {
    "data": {
        "myProfile": {
            "emailAddress": "brenda99@gmail.com",
            "isStaff": True,
            "language": "FI",
            "name": "Natalie Keith",
            "organisations": {
                "edges": [{"node": {"name": "Thomas, Ochoa and Peters"}}]
            },
            "phoneNumber": "001-042-405-4852x6231",
            "placeIds": [
                "vJGuUZtSihlLyOWeWgxN",
                "IdaNadghCetJYgCAuXtm",
                "VxzDraSqNldgihpkthKx",
            ],
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
                "organisations": {"edges": [{"node": {"name": "Hayes and Sons"}}]},
                "phoneNumber": "",
                "placeIds": [],
            }
        }
    }
}

snapshots["test_organisations_query_type_filter 1"] = {
    "data": {
        "organisations": {
            "edges": [
                {
                    "node": {
                        "name": "Black Ltd",
                        "persons": {"edges": []},
                        "phoneNumber": "063.334.5773x557",
                        "publisherId": "zVxeo",
                        "type": "PROVIDER",
                    }
                },
                {
                    "node": {
                        "name": "Underwood LLC",
                        "persons": {"edges": []},
                        "phoneNumber": "649-763-8034x669",
                        "publisherId": "ThbUS",
                        "type": "PROVIDER",
                    }
                },
                {
                    "node": {
                        "name": "Sherman LLC",
                        "persons": {"edges": []},
                        "phoneNumber": "159.102.3202x8130",
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
                        "name": "Walls-Roy",
                        "persons": {"edges": []},
                        "phoneNumber": "123-447-4468",
                        "publisherId": "KQItj",
                        "type": "USER",
                    }
                },
                {
                    "node": {
                        "name": "Weber-Johnson",
                        "persons": {"edges": []},
                        "phoneNumber": "4883019054",
                        "publisherId": "AmjOn",
                        "type": "USER",
                    }
                },
            ]
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
                "organisations": {"edges": [{"node": {"name": "Hayes and Sons"}}]},
                "phoneNumber": "",
                "placeIds": ["xyz:123", "abc321"],
            }
        }
    }
}
