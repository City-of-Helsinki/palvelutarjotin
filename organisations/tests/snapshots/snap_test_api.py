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
                        "emailAddress": "nancy55@yahoo.com",
                        "language": "FI",
                        "name": "Robert Cruz",
                        "organisations": {"edges": []},
                        "phoneNumber": "390-340-4467x342",
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
                        "emailAddress": "jesse27@hotmail.com",
                        "language": "FI",
                        "name": "Gregory Weber",
                        "organisations": {"edges": []},
                        "phoneNumber": "0488301905",
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
                        "emailAddress": "nancy55@yahoo.com",
                        "language": "FI",
                        "name": "Robert Cruz",
                        "organisations": {"edges": []},
                        "phoneNumber": "390-340-4467x342",
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
            "emailAddress": "nancy55@yahoo.com",
            "language": "FI",
            "name": "Robert Cruz",
            "organisations": {"edges": []},
            "phoneNumber": "390-340-4467x342",
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
            "organisations": {"edges": [{"node": {"name": "Perry Ltd"}}]},
            "phoneNumber": "(767)124-0675x064",
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
                "organisations": {"edges": [{"node": {"name": "Perry Ltd"}}]},
                "phoneNumber": "(767)124-0675x064",
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
            "emailAddress": "moniquedavis@vargas.biz",
            "isStaff": True,
            "language": "FI",
            "name": "Andrew Coleman",
            "organisations": {"edges": [{"node": {"name": "Perry Ltd"}}]},
            "phoneNumber": "+1-583-693-1796x212",
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
                "organisations": {"edges": [{"node": {"name": "Davis Inc"}}]},
                "phoneNumber": "",
            }
        }
    }
}
