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
                        "emailAddress": "mallory34@manning.com",
                        "name": "Melinda Cunningham",
                        "organisations": {"edges": []},
                        "phoneNumber": "+1-483-227-7416x754",
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
                        "emailAddress": "htravis@peters.net",
                        "name": "Jonathan Smith",
                        "organisations": {
                            "edges": [{"node": {"name": "Jennifer Crane"}}]
                        },
                        "phoneNumber": "234.474.4685x81662",
                    }
                },
                {
                    "node": {
                        "emailAddress": "mallory34@manning.com",
                        "name": "Melinda Cunningham",
                        "organisations": {"edges": []},
                        "phoneNumber": "+1-483-227-7416x754",
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
            "emailAddress": "mallory34@manning.com",
            "name": "Melinda Cunningham",
            "organisations": {"edges": []},
            "phoneNumber": "+1-483-227-7416x754",
        }
    }
}

snapshots["test_person_query 4"] = {
    "data": {
        "person": {
            "emailAddress": "htravis@peters.net",
            "name": "Jonathan Smith",
            "organisations": {"edges": [{"node": {"name": "Jennifer Crane"}}]},
            "phoneNumber": "234.474.4685x81662",
        }
    }
}

snapshots["test_organisations_query 1"] = {
    "data": {
        "organisations": {
            "edges": [
                {
                    "node": {
                        "name": "Jose Kerr",
                        "persons": {"edges": []},
                        "phoneNumber": "063.334.5773x557",
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
            "name": "Jose Kerr",
            "persons": {"edges": []},
            "phoneNumber": "063.334.5773x557",
            "type": "USER",
        }
    }
}

snapshots["test_my_profile_query 1"] = {
    "data": {
        "myProfile": {
            "emailAddress": "stephanieskinner@gmail.com",
            "name": "William Brewer",
            "organisations": {"edges": [{"node": {"name": "Jason Berg"}}]},
            "phoneNumber": "(767)124-0675x064",
        }
    }
}

snapshots["test_update_person_mutation 1"] = {
    "data": {
        "updatePerson": {
            "person": {
                "emailAddress": "clifford71@gmail.com",
                "name": "New name",
                "organisations": {"edges": [{"node": {"name": "William Brewer"}}]},
                "phoneNumber": "+1-023-202-8130x72770",
            }
        }
    }
}

snapshots["test_add_organisation 1"] = {
    "data": {
        "addOrganisation": {
            "organisation": {
                "name": "New organisation",
                "phoneNumber": "012345678",
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
                "name": "New name",
                "organisations": {"edges": [{"node": {"name": "Jason Berg"}}]},
                "phoneNumber": "(767)124-0675x064",
            }
        }
    }
}

snapshots["test_create_my_profile 1"] = {
    "data": {
        "createMyProfile": {
            "myProfile": {
                "emailAddress": "newEmail@address.com",
                "name": "New name",
                "organisations": {"edges": [{"node": {"name": "Brandon Johnson"}}]},
                "phoneNumber": "",
            }
        }
    }
}
