# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_list_helsinki_schools_and_kindergartens 1"] = {
    "data": {
        "schoolsAndKindergartensList": {
            "data": [
                {
                    "id": "tprek:3",
                    "name": {
                        "en": "Daycare Kannel",
                        "fi": "Päiväkoti Kannel",
                        "sv": "Päiväkoti Kannel",
                    },
                },
                {
                    "id": "tprek:2266",
                    "name": {
                        "en": "Family day care Itä-Kannelmäki - Hakuninmaa - Maununneva",
                        "fi": "Perhepäivähoito Kaarela",
                        "sv": "Perhepäivähoito Kaarela",
                    },
                },
                {
                    "id": "tprek:73213",
                    "name": {
                        "en": "Daycare Kannelmäki, preschool groups",
                        "fi": "Päiväkoti Kannelmäki, esiopetusryhmät",
                        "sv": "Päiväkoti Kannelmäki, förskolegrupper",
                    },
                },
            ],
            "meta": {"count": 3},
        }
    }
}
