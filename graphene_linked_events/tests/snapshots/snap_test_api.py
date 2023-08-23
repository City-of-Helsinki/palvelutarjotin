# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_create_event 1"] = {
    "data": {
        "addEventMutation": {
            "response": {
                "body": {
                    "description": {"en": "desc en", "fi": "desc", "sv": "desc sv"},
                    "id": "qq:afy6aghr2y",
                    "infoUrl": None,
                    "keywords": [{"id": None}],
                    "location": {"id": None},
                    "offers": [{"isFree": False}],
                    "pEvent": {
                        "autoAcceptance": True,
                        "autoAcceptanceMessage": "Automaattisen hyväksynnän viesti",
                        "contactEmail": "contact@email.me",
                        "contactPerson": {"name": "Sean Rocha"},
                        "contactPhoneNumber": "123123",
                        "enrolmentEndDays": 2,
                        "enrolmentStart": "2020-06-06T16:40:48+00:00",
                        "externalEnrolmentUrl": None,
                        "linkedEventId": "qq:afy6aghr2y",
                        "mandatoryAdditionalInformation": True,
                        "neededOccurrences": 1,
                        "organisation": {"name": "Chapman, Scott and Martin"},
                        "translations": [
                            {
                                "autoAcceptanceMessage": "Automaattisen hyväksynnän viesti",
                                "languageCode": "FI",
                            },
                            {
                                "autoAcceptanceMessage": "Custom message of auto approvance",
                                "languageCode": "EN",
                            },
                        ],
                    },
                    "shortDescription": {
                        "en": "short desc en",
                        "fi": "short desc",
                        "sv": "short desc sv",
                    },
                    "startTime": "2020-05-05",
                },
                "statusCode": 201,
            }
        }
    }
}

snapshots["test_create_event_with_external_enrolment 1"] = {
    "data": {
        "addEventMutation": {
            "response": {
                "body": {
                    "description": {"en": "desc en", "fi": "desc", "sv": "desc sv"},
                    "id": "qq:afy6aghr2y",
                    "infoUrl": None,
                    "keywords": [{"id": None}],
                    "location": {"id": None},
                    "offers": [{"isFree": False}],
                    "pEvent": {
                        "autoAcceptance": False,
                        "autoAcceptanceMessage": "Automaattisen hyväksynnän viesti",
                        "contactEmail": "contact@email.me",
                        "contactPerson": {"name": "Sean Rocha"},
                        "contactPhoneNumber": "123123",
                        "enrolmentEndDays": None,
                        "enrolmentStart": None,
                        "externalEnrolmentUrl": "http://test.org",
                        "linkedEventId": "qq:afy6aghr2y",
                        "mandatoryAdditionalInformation": True,
                        "neededOccurrences": 0,
                        "organisation": {"name": "Chapman, Scott and Martin"},
                        "translations": [
                            {
                                "autoAcceptanceMessage": "Automaattisen hyväksynnän viesti",
                                "languageCode": "FI",
                            },
                            {
                                "autoAcceptanceMessage": "Custom message of auto approvance",
                                "languageCode": "EN",
                            },
                        ],
                    },
                    "shortDescription": {
                        "en": "short desc en",
                        "fi": "short desc",
                        "sv": "short desc sv",
                    },
                    "startTime": "2020-05-05",
                },
                "statusCode": 201,
            }
        }
    }
}

snapshots["test_create_event_without_enrolment 1"] = {
    "data": {
        "addEventMutation": {
            "response": {
                "body": {
                    "description": {"en": "desc en", "fi": "desc", "sv": "desc sv"},
                    "id": "qq:afy6aghr2y",
                    "infoUrl": None,
                    "keywords": [{"id": None}],
                    "location": {"id": None},
                    "offers": [{"isFree": False}],
                    "pEvent": {
                        "autoAcceptance": False,
                        "autoAcceptanceMessage": "Automaattisen hyväksynnän viesti",
                        "contactEmail": "contact@email.me",
                        "contactPerson": {"name": "Sean Rocha"},
                        "contactPhoneNumber": "123123",
                        "enrolmentEndDays": None,
                        "enrolmentStart": None,
                        "externalEnrolmentUrl": None,
                        "linkedEventId": "qq:afy6aghr2y",
                        "mandatoryAdditionalInformation": True,
                        "neededOccurrences": 0,
                        "organisation": {"name": "Chapman, Scott and Martin"},
                        "translations": [
                            {
                                "autoAcceptanceMessage": "Automaattisen hyväksynnän viesti",
                                "languageCode": "FI",
                            },
                            {
                                "autoAcceptanceMessage": "Custom message of auto approvance",
                                "languageCode": "EN",
                            },
                        ],
                    },
                    "shortDescription": {
                        "en": "short desc en",
                        "fi": "short desc",
                        "sv": "short desc sv",
                    },
                    "startTime": "2020-05-05",
                },
                "statusCode": 201,
            }
        }
    }
}

snapshots["test_create_event_without_p_event_translations 1"] = {
    "data": {
        "addEventMutation": {
            "response": {
                "body": {
                    "description": {"en": "desc en", "fi": "desc", "sv": "desc sv"},
                    "id": "qq:afy6aghr2y",
                    "infoUrl": None,
                    "keywords": [{"id": None}],
                    "location": {"id": None},
                    "offers": [{"isFree": False}],
                    "pEvent": {
                        "autoAcceptance": True,
                        "autoAcceptanceMessage": None,
                        "contactEmail": "contact@email.me",
                        "contactPerson": {"name": "Sean Rocha"},
                        "contactPhoneNumber": "123123",
                        "enrolmentEndDays": 2,
                        "enrolmentStart": "2020-06-06T16:40:48+00:00",
                        "externalEnrolmentUrl": None,
                        "linkedEventId": "qq:afy6aghr2y",
                        "mandatoryAdditionalInformation": True,
                        "neededOccurrences": 1,
                        "organisation": {"name": "Chapman, Scott and Martin"},
                        "translations": [],
                    },
                    "shortDescription": {
                        "en": "short desc en",
                        "fi": "short desc",
                        "sv": "short desc sv",
                    },
                    "startTime": "2020-05-05",
                },
                "statusCode": 201,
            }
        }
    }
}

snapshots["test_delete_event 1"] = {
    "data": {"deleteEventMutation": {"response": {"body": None, "statusCode": 204}}}
}

snapshots["test_delete_image 1"] = {
    "data": {"deleteImageMutation": {"response": {"statusCode": 204}}}
}

snapshots["test_get_event 1"] = {
    "data": {
        "event": {
            "activities": [{"id": "helfi:12"}],
            "additionalCriteria": [{"id": "helfi:12"}],
            "audience": [],
            "audienceMaxAge": None,
            "audienceMinAge": None,
            "categories": [{"id": "helfi:12"}],
            "createdTime": "2019-12-13T12:49:40.545273Z",
            "customData": None,
            "dataSource": "helsinki",
            "datePublished": None,
            "description": {
                "en": "<p>Visual artist Raija Malka and composer Kaija Saariaho will take over Amos Rex’s exhibition space in a new and experiential way next summer. The work is painterly, spatial and musical all at once, offering visitors an opportunity to shape the space with their own creativity.</p><p>The exhibition title, Blick (Gaze), is a reference to visual artist Wassily Kandinsky’s poem from 1912 that is included in the soundscape by Kaija Saariaho. The gazes of the two artists are brought together in a three-dimensional space.</p><p>The exhibition is a multisensory experience that invites people to stay. In a world made up of the colours and sounds of Malka and Saariaho, visitors can build their own arrangements.</p><p>Amos Rex<br>10.6.-30.8. </p><p>Mon, Fri 11.00-18.00<br>Wed, Thu 11.00-20.00<br>Sat, Sun 11.00-17.00</p><p>Admission fee 5-15€, under 18 yrs free entry</p>",
                "fi": "<p>Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho täyttävät ensi kesänä Amos Rexin näyttelytilan uudella kokemuksellisella tavalla. Teos on yhtä aikaa maalauksellinen, tilallinen ja musiikillinen. </p><p>Näyttelyn nimi Blick (Katse) viittaa kuvataiteilija Wassily Kandinskyn 1912 julkaistuun runoon, joka sisältyy Kaija Saariahon näyttelyssä kuultavaan äänimaisemaan. Kahden taiteilijan katseet yhdistyvät näyttelyn kolmiulotteisessa tilassa.</p><p>Näyttely on moniaistinen kokonaisuus, joka houkuttelee viipymään. Kävijä voi rakentaa omia asetelmiaan Malkan ja Saariahon väri- ja äänimaailmaan.</p><p>Amos Rex<br>10.6.-30.8. </p><p>ma, pe klo 11-18<br>ke, to klo 11-20<br>la, su klo 11-17</p><p>Sisäänpääsy 5-15€, alle 18-vuotiaille vapaa pääsy</p>",
                "sv": "<p>Bildkonstnären Raija Malka och kompositören Kaija Saariaho fyller Amos Rex utställningsutrymme på ett nytt och experimentellt sätt nästa sommaren. Deras verk är på en och samma gång måleriskt, rumsligt och musikaliskt. </p><p>Utställningstiteln, Blick, syftar på bildkonstnären Wassily Kandinskys dikt från 1912. Texten ingår i Kaija Saariahos ljuder i utställningen. De två konstnärernas blickar möts i det tredimensionella utställningsutrymmet.</p><p>Utställningen utgör en sinnlig helhet som lockar besökare att dröja kvar. De kan bidra till Malkas och Saariahos färg- och ljudvärld med sina egna byggstenar.</p><p>Amos Rex<br>10.6.-30.8. </p><p>må, fre kl 11-18<br>ons, to kl 11-20<br>lö, sö kl 11-17</p><p>Inträde 5-15€, under 18 år fritt inträde</p>",
            },
            "endTime": None,
            "enrolmentEndTime": None,
            "enrolmentStartTime": None,
            "eventStatus": "EventPostponed",
            "externalLinks": [],
            "id": "helsinki:afxp6tv4xa",
            "images": [
                {"internalId": "https://api.hel.fi/linkedevents/v1/image/61106/"}
            ],
            "inLanguage": [],
            "infoUrl": {
                "en": "http://www.amosrex.fi",
                "fi": "http://www.amosrex.fi",
                "sv": "http://www.amosrex.fi",
            },
            "internalContext": "http://schema.org",
            "internalId": "https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/",
            "internalType": "Event/LinkedEvent",
            "keywords": [
                {"internalId": "https://api.hel.fi/linkedevents/v1/keyword/helfi:12/"},
                {"internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p5121/"},
                {"internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p6889/"},
                {"internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p1808/"},
            ],
            "lastModifiedTime": "2020-05-05T09:24:58.569334Z",
            "localizationExtraInfo": None,
            "location": {
                "internalId": "https://api.hel.fi/linkedevents-test/v1/place/tprek:15321/"
            },
            "maximumAttendeeCapacity": None,
            "minimumAttendeeCapacity": None,
            "name": {
                "en": "Raija Malka & Kaija Saariaho: Blick",
                "fi": "Raija Malka & Kaija Saariaho: Blick",
                "sv": "Raija Malka & Kaija Saariaho: Blick",
            },
            "offers": [{"isFree": False}],
            "provider": {"en": "Amos Rex", "fi": "Amos Rex", "sv": "Amos Rex"},
            "providerContactInfo": None,
            "publicationStatus": "public",
            "publisher": "ytj:0586977-6",
            "remainingAttendeeCapacity": None,
            "shortDescription": {
                "en": "Visual artist Raija Malka and composer Kaija Saariaho will take over Amos Rex’s exhibition space in a new and experiential way next summer. ",
                "fi": "Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho täyttävät ensi kesänä Amos Rexin näyttelytilan uudella kokemuksellisella tavalla. ",
                "sv": "Bildkonstnären Raija Malka och kompositören Kaija Saariaho fyller Amos Rex utställningsutrymme på ett nytt och experimentellt sätt nästa sommaren.",
            },
            "startTime": None,
            "subEvents": [],
            "superEvent": None,
            "superEventType": None,
        }
    }
}

snapshots["test_get_event_not_found 1"] = {
    "data": {"event": None},
    "errors": [
        {
            "extensions": {"code": "GENERAL_ERROR"},
            "locations": [{"column": 3, "line": 3}],
            "message": "A mocked generic HTTP error",
            "path": ["event"],
        }
    ],
}

snapshots["test_get_event_without_location 1"] = {
    "data": {
        "event": {
            "activities": [{"id": "helfi:12"}],
            "additionalCriteria": [{"id": "helfi:12"}],
            "audience": [],
            "audienceMaxAge": None,
            "audienceMinAge": None,
            "categories": [{"id": "helfi:12"}],
            "createdTime": "2019-12-13T12:49:40.545273Z",
            "customData": None,
            "dataSource": "helsinki",
            "datePublished": None,
            "description": {
                "en": "<p>Visual artist Raija Malka and composer Kaija Saariaho will take over Amos Rex’s exhibition space in a new and experiential way next summer. The work is painterly, spatial and musical all at once, offering visitors an opportunity to shape the space with their own creativity.</p><p>The exhibition title, Blick (Gaze), is a reference to visual artist Wassily Kandinsky’s poem from 1912 that is included in the soundscape by Kaija Saariaho. The gazes of the two artists are brought together in a three-dimensional space.</p><p>The exhibition is a multisensory experience that invites people to stay. In a world made up of the colours and sounds of Malka and Saariaho, visitors can build their own arrangements.</p><p>Amos Rex<br>10.6.-30.8. </p><p>Mon, Fri 11.00-18.00<br>Wed, Thu 11.00-20.00<br>Sat, Sun 11.00-17.00</p><p>Admission fee 5-15€, under 18 yrs free entry</p>",
                "fi": "<p>Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho täyttävät ensi kesänä Amos Rexin näyttelytilan uudella kokemuksellisella tavalla. Teos on yhtä aikaa maalauksellinen, tilallinen ja musiikillinen. </p><p>Näyttelyn nimi Blick (Katse) viittaa kuvataiteilija Wassily Kandinskyn 1912 julkaistuun runoon, joka sisältyy Kaija Saariahon näyttelyssä kuultavaan äänimaisemaan. Kahden taiteilijan katseet yhdistyvät näyttelyn kolmiulotteisessa tilassa.</p><p>Näyttely on moniaistinen kokonaisuus, joka houkuttelee viipymään. Kävijä voi rakentaa omia asetelmiaan Malkan ja Saariahon väri- ja äänimaailmaan.</p><p>Amos Rex<br>10.6.-30.8. </p><p>ma, pe klo 11-18<br>ke, to klo 11-20<br>la, su klo 11-17</p><p>Sisäänpääsy 5-15€, alle 18-vuotiaille vapaa pääsy</p>",
                "sv": "<p>Bildkonstnären Raija Malka och kompositören Kaija Saariaho fyller Amos Rex utställningsutrymme på ett nytt och experimentellt sätt nästa sommaren. Deras verk är på en och samma gång måleriskt, rumsligt och musikaliskt. </p><p>Utställningstiteln, Blick, syftar på bildkonstnären Wassily Kandinskys dikt från 1912. Texten ingår i Kaija Saariahos ljuder i utställningen. De två konstnärernas blickar möts i det tredimensionella utställningsutrymmet.</p><p>Utställningen utgör en sinnlig helhet som lockar besökare att dröja kvar. De kan bidra till Malkas och Saariahos färg- och ljudvärld med sina egna byggstenar.</p><p>Amos Rex<br>10.6.-30.8. </p><p>må, fre kl 11-18<br>ons, to kl 11-20<br>lö, sö kl 11-17</p><p>Inträde 5-15€, under 18 år fritt inträde</p>",
            },
            "endTime": None,
            "enrolmentEndTime": None,
            "enrolmentStartTime": None,
            "eventStatus": "EventPostponed",
            "externalLinks": [],
            "id": "helsinki:afxp6tv4xa",
            "images": [
                {"internalId": "https://api.hel.fi/linkedevents/v1/image/61106/"}
            ],
            "inLanguage": [],
            "infoUrl": {
                "en": "http://www.amosrex.fi",
                "fi": "http://www.amosrex.fi",
                "sv": "http://www.amosrex.fi",
            },
            "internalContext": "http://schema.org",
            "internalId": "https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/",
            "internalType": "Event/LinkedEvent",
            "keywords": [
                {"internalId": "https://api.hel.fi/linkedevents/v1/keyword/helfi:12/"},
                {"internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p5121/"},
                {"internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p6889/"},
                {"internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p1808/"},
            ],
            "lastModifiedTime": "2020-05-05T09:24:58.569334Z",
            "localizationExtraInfo": None,
            "location": {
                "internalId": "https://api.hel.fi/linkedevents-test/v1/place/tprek:15321/"
            },
            "maximumAttendeeCapacity": None,
            "minimumAttendeeCapacity": None,
            "name": {
                "en": "Raija Malka & Kaija Saariaho: Blick",
                "fi": "Raija Malka & Kaija Saariaho: Blick",
                "sv": "Raija Malka & Kaija Saariaho: Blick",
            },
            "offers": [{"isFree": False}],
            "provider": {"en": "Amos Rex", "fi": "Amos Rex", "sv": "Amos Rex"},
            "providerContactInfo": None,
            "publicationStatus": "public",
            "publisher": "ytj:0586977-6",
            "remainingAttendeeCapacity": None,
            "shortDescription": {
                "en": "Visual artist Raija Malka and composer Kaija Saariaho will take over Amos Rex’s exhibition space in a new and experiential way next summer. ",
                "fi": "Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho täyttävät ensi kesänä Amos Rexin näyttelytilan uudella kokemuksellisella tavalla. ",
                "sv": "Bildkonstnären Raija Malka och kompositören Kaija Saariaho fyller Amos Rex utställningsutrymme på ett nytt och experimentellt sätt nästa sommaren.",
            },
            "startTime": None,
            "subEvents": [],
            "superEvent": None,
            "superEventType": None,
        }
    }
}

snapshots["test_get_events 1"] = {
    "data": {
        "events": {
            "data": [
                {
                    "audience": [],
                    "audienceMaxAge": None,
                    "audienceMinAge": None,
                    "createdTime": "2020-05-05T09:27:45.644890Z",
                    "customData": None,
                    "dataSource": "helsinki",
                    "datePublished": None,
                    "description": {
                        "en": None,
                        "fi": "<p>Tule kuulolle ja kysymään muun muassa Viikin, Pukinmäen, Puistolan, Suutarilan, Pihlajamäen, Tapanilan ja Malmin ajankohtaisista suunnitteluasioista. Koilliseen suunnitellaan uusia asuntoja ja liiketiloja, kadut ja viheralueet kohenevat.<br>Malmin lentokentän alueelle suunnitellaan asuntoja noin 25 000 ihmiselle ja Viikin-Malmin pikaraitiotiestä kaavaillaan koillisen uutta raideyhteyttä. Asemanseuduilla eli Tapulikaupunki – Puistola -alueella ja Pukinmäessä hahmotellaan kehittämisperiaatteita. Raide-Jokerin rakentaminen edistyy.<br>Osallistu kotisohvaltasi kaavoituksen sekä liikenteen ja puistojen suunnittelun tilaisuuteen maanantaina 1.6. klo 17−19. Kirjaudu sisään jo klo 16.45. Lisätietoa, ohjeet, liittymislinkki ja vinkit ennakko-osallistumisesta: hel.fi/suunnitelmat.</p><p>Esittelyssä mukana olevat hankkeet:<br>Asemakaavoitus ja muu maankäytön suunnittelu / Ota kantaa juuri nyt<br>· Malmin uimahallin laajennus<br>· Malmin energiakortteli Tattarisuon teollisuusalueen eteläpuolelle</p><p>Kadut, puistot ja viheralueet / Ota kantaa juuri nyt<br>· Katariina Saksilaisen kadun eteläosan katusuunnitelma ja Pornaistenniemen puistosuunnitelma, jotka sisältävät pyöräliikenteen baanayhteyden<br>· Kivikon puistosilta, joka ylittää Lahdenväylän ja johtaa lentokenttäalueelta Kivikon ulkoilupuistoon<br>· Maatullinkujan katusuunnitelma välillä Henrik Forsiuksen tie - Kämnerintie<br>· Suutarilan alueen katusuunnitelmia: Jupiterintie, Marsintie, Merkuriuksentie, Pikkaraistie, Riimukuja, Saturnuksentie ja Uranuksentie</p><p>Ajankohtaiskatsaus – missä mennään muiden koillisen hankkeiden kanssa <br>· Lentoasemankorttelit<br>· Lentokenttäalueen puistokilpailu ja väliaikaiskäytön ajankohtaiset suunnitelmat<br>· Malmin keskustan suunnittelutilanne<br>· Pukinmäki, Säterinportti 3, Säterintie 7-9, Madetojankuja 1 <br>· Pukinmäki, Rälssintien ja Isonkaivontien alueet <br>· Malmi, (Pihlajamäki), Rapakivenkuja 2 Pihlajamäen ostoskeskus <br>· Tapanilan asemanseudun eteläosa <br>· Töyrynummi, Puutarhakortteli <br>· Tapulikaupunki, Kämnerintie <br>· Viikki, Maakaarenkuja 2 ja Aleksanteri Nevskin katu <br>· Mellunkylä, Kivikon pelastusasematontti (helikopterikenttä) <br>· Tapulikaupunki ja Puistolan asemanseutu <br>· Pukinmäen täydennysrakentaminen<br>· Viikin-Malmin pikaraitiotie<br>· Raide-Jokerin rakentamistilanne<br>· Vanhan Porvoontien suunnittelu välillä Suurmetsäntie-Heikinlaaksontie, sisältää melusuojauksen suunnittelun</p>",
                        "sv": None,
                    },
                    "endTime": "2020-06-01T16:00:00Z",
                    "enrolmentEndTime": None,
                    "enrolmentStartTime": None,
                    "eventStatus": "EventScheduled",
                    "externalLinks": [],
                    "id": "helsinki:afy6ikna3u",
                    "images": [
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/image/64235/"
                        }
                    ],
                    "inLanguage": [
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/language/fi/"
                        }
                    ],
                    "infoUrl": {
                        "en": None,
                        "fi": "https://www.hel.fi/Helsinki/fi/asuminen-ja-ymparisto/kaavoitus/ajankohtaiset-suunnitelmat/",
                        "sv": None,
                    },
                    "internalContext": "http://schema.org",
                    "internalId": "https://api.hel.fi/linkedevents/v1/event/helsinki:afy6ikna3u/",
                    "internalType": "Event/LinkedEvent",
                    "keywords": [
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p15875/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p13980/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p14004/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p8270/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p15882/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p26626/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p8268/"
                        },
                    ],
                    "lastModifiedTime": "2020-05-05T09:27:45.644920Z",
                    "localizationExtraInfo": None,
                    "location": {
                        "internalId": "https://api.hel.fi/linkedevents/v1/place/helsinki:internet/"
                    },
                    "maximumAttendeeCapacity": None,
                    "minimumAttendeeCapacity": None,
                    "name": {
                        "en": None,
                        "fi": "Uutta Koillis-Helsinkiä verkkotilaisuus",
                        "sv": None,
                    },
                    "offers": [{"isFree": True}],
                    "provider": None,
                    "providerContactInfo": None,
                    "publicationStatus": None,
                    "publisher": "ahjo:u541000",
                    "remainingAttendeeCapacity": None,
                    "shortDescription": {
                        "en": None,
                        "fi": "Tule kuulemaan ja keskustelemaan verkkoon uudistuvasta Koillis-Helsingistä omalta kotisohvaltasi. Juuri nyt voit vaikuttaa useisiin suunnittelukohteisiin!",
                        "sv": None,
                    },
                    "startTime": "2020-06-01T13:45:00Z",
                    "subEvents": [],
                    "superEvent": None,
                    "superEventType": None,
                }
            ],
            "meta": {
                "count": 151775,
                "next": "https://api.hel.fi/linkedevents/v1/event/?page=2",
                "previous": None,
            },
        }
    }
}

snapshots["test_get_events_with_occurrences 1"] = {
    "data": {
        "events": {
            "data": [
                {
                    "id": "helsinki:afy6ikna3u",
                    "internalId": "https://api.hel.fi/linkedevents/v1/event/helsinki:afy6ikna3u/",
                    "pEvent": {
                        "lastOccurrenceDatetime": "2020-01-06T00:00:00+00:00",
                        "nextOccurrenceDatetime": "2020-01-05T00:00:00+00:00",
                    },
                },
                {
                    "id": "helsinki:afxp6tv4xa",
                    "internalId": "https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/",
                    "pEvent": {
                        "lastOccurrenceDatetime": "2020-01-06T00:00:00+00:00",
                        "nextOccurrenceDatetime": "2020-01-05T00:00:00+00:00",
                    },
                },
            ],
            "meta": {
                "count": 151775,
                "next": "https://api.hel.fi/linkedevents/v1/event/?page=2",
                "previous": None,
            },
        }
    }
}

snapshots["test_get_keyword 1"] = {
    "data": {
        "keyword": {
            "aggregate": False,
            "altLabels": ["spädbarn", "lapset", "imeväisikäiset", "barn"],
            "createdTime": "2014-06-23T11:37:27.705000Z",
            "dataSource": "yso",
            "deprecated": False,
            "id": "yso:p4354",
            "image": None,
            "internalContext": "http://schema.org",
            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p4354/",
            "internalType": "Keyword",
            "lastModifiedTime": "2017-09-06T05:20:47.061426Z",
            "nEvents": 54082,
            "name": {
                "en": "children (age groups)",
                "fi": "lapset (ikäryhmät)",
                "sv": "barn (åldersgrupper)",
            },
            "publisher": "hy:kansalliskirjasto",
        }
    }
}

snapshots["test_get_keyword_set 1"] = {
    "data": {
        "keywordSet": {
            "id": "kultus:categories",
            "internalId": "http://localhost:8080/v1/keyword_set/qq:kultus:categories/",
            "keywords": [
                {
                    "id": "helfi:12",
                    "internalId": "http://localhost:8080/v1/keyword/yso:p27033/",
                    "name": {
                        "en": "Valentine's Day",
                        "fi": "ystävänpäivä",
                        "sv": "alla hjärtans dag",
                    },
                }
            ],
        }
    }
}

snapshots["test_get_keyword_set 2"] = {
    "data": {
        "keywordSet": {
            "id": "kultus:categories",
            "internalId": "http://localhost:8080/v1/keyword_set/qq:kultus:categories/",
            "keywords": [
                {
                    "id": "helfi:12",
                    "internalId": "http://localhost:8080/v1/keyword/yso:p27033/",
                    "name": {
                        "en": "Valentine's Day",
                        "fi": "ystävänpäivä",
                        "sv": "alla hjärtans dag",
                    },
                }
            ],
        }
    }
}

snapshots["test_get_keyword_set 3"] = {
    "data": {
        "keywordSet": {
            "id": "kultus:categories",
            "internalId": "http://localhost:8080/v1/keyword_set/qq:kultus:categories/",
            "keywords": [
                {
                    "id": "helfi:12",
                    "internalId": "http://localhost:8080/v1/keyword/yso:p27033/",
                    "name": {
                        "en": "Valentine's Day",
                        "fi": "ystävänpäivä",
                        "sv": "alla hjärtans dag",
                    },
                }
            ],
        }
    }
}

snapshots["test_get_keyword_set 4"] = {
    "data": {
        "keywordSet": {
            "id": "kultus:categories",
            "internalId": "http://localhost:8080/v1/keyword_set/qq:kultus:categories/",
            "keywords": [
                {
                    "id": "helfi:12",
                    "internalId": "http://localhost:8080/v1/keyword/yso:p27033/",
                    "name": {
                        "en": "Valentine's Day",
                        "fi": "ystävänpäivä",
                        "sv": "alla hjärtans dag",
                    },
                }
            ],
        }
    }
}

snapshots["test_get_keywords 1"] = {
    "data": {
        "keywords": {
            "data": [
                {
                    "aggregate": False,
                    "altLabels": ["spädbarn", "lapset", "imeväisikäiset", "barn"],
                    "createdTime": "2014-06-23T11:37:27.705000Z",
                    "dataSource": "yso",
                    "deprecated": False,
                    "id": "yso:p4354",
                    "image": None,
                    "internalContext": "http://schema.org",
                    "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p4354/",
                    "internalType": "Keyword",
                    "lastModifiedTime": "2017-09-06T05:20:47.061426Z",
                    "nEvents": 54082,
                    "name": {
                        "en": "children (age groups)",
                        "fi": "lapset (ikäryhmät)",
                        "sv": "barn (åldersgrupper)",
                    },
                    "publisher": "hy:kansalliskirjasto",
                },
                {
                    "aggregate": False,
                    "altLabels": [
                        "ydinperheet",
                        "perhe",
                        "familjer (grupper)",
                        "kärnfamiljer",
                        "familj",
                    ],
                    "createdTime": "2014-06-23T11:37:28.246000Z",
                    "dataSource": "yso",
                    "deprecated": False,
                    "id": "yso:p4363",
                    "image": None,
                    "internalContext": "http://schema.org",
                    "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p4363/",
                    "internalType": "Keyword",
                    "lastModifiedTime": "2019-05-11T04:20:04.577893Z",
                    "nEvents": 29262,
                    "name": {"en": "families", "fi": "perheet", "sv": "familjer"},
                    "publisher": "hy:kansalliskirjasto",
                },
            ],
            "meta": {
                "count": 1992,
                "next": "https://api.hel.fi/linkedevents/v1/keyword/?page=2&page_size=2",
                "previous": None,
            },
        }
    }
}

snapshots["test_get_place 1"] = {
    "data": {
        "place": {
            "addressCountry": None,
            "addressLocality": {"en": "Espoo", "fi": "Espoo", "sv": "Esbo"},
            "addressRegion": None,
            "contactType": None,
            "createdTime": None,
            "customData": None,
            "dataSource": "tprek",
            "deleted": False,
            "description": None,
            "divisions": [{"municipality": None, "ocdId": None}],
            "email": "sellonkirjasto@espoo.fi",
            "id": "tprek:15417",
            "image": 54259,
            "infoUrl": {
                "en": "http://www.helmet.fi/sellolibrary",
                "fi": "http://www.helmet.fi/sello",
                "sv": "http://www.helmet.fi/sellobiblioteket",
            },
            "internalContext": "http://schema.org",
            "internalId": "https://api.hel.fi/linkedevents/v1/place/tprek:15417/",
            "internalType": "Place",
            "lastModifiedTime": "2020-04-25T05:09:10.712132Z",
            "nEvents": 27264,
            "name": {
                "en": "Sello Library",
                "fi": "Sellon kirjasto",
                "sv": "Sellobiblioteket",
            },
            "parent": None,
            "position": {"coordinates": [24.80992, 60.21748], "type": "Point"},
            "postOfficeBoxNum": None,
            "postalCode": "02600",
            "publisher": "ahjo:u021600",
            "replacedBy": None,
            "streetAddress": {
                "en": "Leppävaarankatu 9",
                "fi": "Leppävaarankatu 9",
                "sv": "Albergagatan 9",
            },
            "telephone": {"en": None, "fi": "+358 9 8165 7603", "sv": None},
        }
    }
}

snapshots["test_get_places 1"] = {
    "data": {
        "places": {
            "data": [
                {
                    "addressCountry": None,
                    "addressLocality": {"en": "Espoo", "fi": "Espoo", "sv": "Esbo"},
                    "addressRegion": None,
                    "contactType": None,
                    "createdTime": None,
                    "customData": None,
                    "dataSource": "tprek",
                    "deleted": False,
                    "description": None,
                    "divisions": [{"municipality": None, "ocdId": None}],
                    "email": "sellonkirjasto@espoo.fi",
                    "id": "tprek:15417",
                    "image": 54259,
                    "infoUrl": {
                        "en": "http://www.helmet.fi/sellolibrary",
                        "fi": "http://www.helmet.fi/sello",
                        "sv": "http://www.helmet.fi/sellobiblioteket",
                    },
                    "internalContext": "http://schema.org",
                    "internalId": "https://api.hel.fi/linkedevents/v1/place/tprek:15417/",
                    "internalType": "Place",
                    "lastModifiedTime": "2020-04-25T05:09:10.712132Z",
                    "nEvents": 27264,
                    "name": {
                        "en": "Sello Library",
                        "fi": "Sellon kirjasto",
                        "sv": "Sellobiblioteket",
                    },
                    "parent": None,
                    "position": {"coordinates": [24.80992, 60.21748], "type": "Point"},
                    "postOfficeBoxNum": None,
                    "postalCode": "02600",
                    "publisher": "ahjo:u021600",
                    "replacedBy": None,
                    "streetAddress": {
                        "en": "Leppävaarankatu 9",
                        "fi": "Leppävaarankatu 9",
                        "sv": "Albergagatan 9",
                    },
                    "telephone": {"en": None, "fi": "+358 9 8165 7603", "sv": None},
                },
                {
                    "addressCountry": None,
                    "addressLocality": {"en": "Espoo", "fi": "Espoo", "sv": "Esbo"},
                    "addressRegion": None,
                    "contactType": None,
                    "createdTime": None,
                    "customData": None,
                    "dataSource": "tprek",
                    "deleted": False,
                    "description": None,
                    "divisions": [{"municipality": None, "ocdId": None}],
                    "email": "kirjasto.entresse@espoo.fi",
                    "id": "tprek:15321",
                    "image": 54251,
                    "infoUrl": {
                        "en": "http://www.helmet.fi/entressebibliotek",
                        "fi": "http://www.helmet.fi/entressenkirjasto",
                        "sv": "http://www.helmet.fi/entressebibliotek",
                    },
                    "internalContext": "http://schema.org",
                    "internalId": "https://api.hel.fi/linkedevents/v1/place/tprek:15321/",
                    "internalType": "Place",
                    "lastModifiedTime": "2019-09-19T14:10:59.747979Z",
                    "nEvents": 7745,
                    "name": {
                        "en": "Entresse Library",
                        "fi": "Entressen kirjasto",
                        "sv": "Entressebiblioteket",
                    },
                    "parent": None,
                    "position": {
                        "coordinates": [24.657864, 60.203636],
                        "type": "Point",
                    },
                    "postOfficeBoxNum": None,
                    "postalCode": "02770",
                    "publisher": "ahjo:u021600",
                    "replacedBy": None,
                    "streetAddress": {
                        "en": "Siltakatu 11",
                        "fi": "Siltakatu 11",
                        "sv": "Brogatan 11",
                    },
                    "telephone": {"en": None, "fi": "+358 9 8165 3776", "sv": None},
                },
            ],
            "meta": {
                "count": 1346,
                "next": "https://api.hel.fi/linkedevents/v1/place/?page=2&page_size=2&show_all_places=",
                "previous": None,
            },
        }
    }
}

snapshots["test_get_popular_kultus_keywords[None-None-1] 1"] = {
    "data": {
        "popularKultusKeywords": {
            "data": [
                {
                    "dataSource": "yso",
                    "id": "yso:p84",
                    "internalId": "http://localhost:8080/v1/keyword/yso:p84/",
                    "nEvents": 200,
                    "name": {
                        "en": "education and training",
                        "fi": "koulutus",
                        "sv": "utbildning",
                    },
                }
            ],
            "meta": {"count": 1},
        }
    }
}

snapshots["test_get_popular_kultus_keywords[True-1-1] 1"] = {
    "data": {
        "popularKultusKeywords": {
            "data": [
                {
                    "dataSource": "yso",
                    "id": "yso:p84",
                    "internalId": "http://localhost:8080/v1/keyword/yso:p84/",
                    "nEvents": 200,
                    "name": {
                        "en": "education and training",
                        "fi": "koulutus",
                        "sv": "utbildning",
                    },
                }
            ],
            "meta": {"count": 1},
        }
    }
}

snapshots["test_get_popular_kultus_keywords[True-None-2] 1"] = {
    "data": {
        "popularKultusKeywords": {
            "data": [
                {
                    "dataSource": "yso",
                    "id": "yso:p84",
                    "internalId": "http://localhost:8080/v1/keyword/yso:p84/",
                    "nEvents": 200,
                    "name": {
                        "en": "education and training",
                        "fi": "koulutus",
                        "sv": "utbildning",
                    },
                },
                {
                    "dataSource": "yso",
                    "id": "helfi:12",
                    "internalId": "http://localhost:8080/v1/keyword/yso:p27033/",
                    "nEvents": 0,
                    "name": {
                        "en": "Valentine's Day",
                        "fi": "ystävänpäivä",
                        "sv": "alla hjärtans dag",
                    },
                },
            ],
            "meta": {"count": 2},
        }
    }
}

snapshots["test_get_upcoming_events[False-False-False] 1"] = {
    "data": {
        "upcomingEvents": {
            "data": [],
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False,
                "page": 0,
                "pageSize": 10,
                "pages": 0,
                "totalCount": 0,
            },
        }
    }
}

snapshots["test_get_upcoming_events[False-False-True] 1"] = {
    "data": {
        "upcomingEvents": {
            "data": [],
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False,
                "page": 0,
                "pageSize": 10,
                "pages": 0,
                "totalCount": 0,
            },
        }
    }
}

snapshots["test_get_upcoming_events[False-True-False] 1"] = {
    "data": {
        "upcomingEvents": {
            "data": [],
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False,
                "page": 0,
                "pageSize": 10,
                "pages": 0,
                "totalCount": 0,
            },
        }
    }
}

snapshots["test_get_upcoming_events[False-True-True] 1"] = {
    "data": {
        "upcomingEvents": {
            "data": [],
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False,
                "page": 0,
                "pageSize": 10,
                "pages": 0,
                "totalCount": 0,
            },
        }
    }
}

snapshots["test_get_upcoming_events[True-False-False] 1"] = {
    "data": {
        "upcomingEvents": {
            "data": [
                {"id": "kultus:3", "pEvent": {"linkedEventId": "kultus:3"}},
                {"id": "kultus:2", "pEvent": {"linkedEventId": "kultus:2"}},
                {"id": "kultus:1", "pEvent": {"linkedEventId": "kultus:1"}},
            ],
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False,
                "page": 1,
                "pageSize": 10,
                "pages": 1,
                "totalCount": 3,
            },
        }
    }
}

snapshots["test_get_upcoming_events[True-False-True] 1"] = {
    "data": {
        "upcomingEvents": {
            "data": [
                {"id": "kultus:3", "pEvent": {"linkedEventId": "kultus:3"}},
                {"id": "kultus:2", "pEvent": {"linkedEventId": "kultus:2"}},
                {"id": "kultus:1", "pEvent": {"linkedEventId": "kultus:1"}},
            ],
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False,
                "page": 1,
                "pageSize": 10,
                "pages": 1,
                "totalCount": 3,
            },
        }
    }
}

snapshots["test_get_upcoming_events[True-True-False] 1"] = {
    "data": {
        "upcomingEvents": {
            "data": [
                {"id": "kultus:3", "pEvent": {"linkedEventId": "kultus:3"}},
                {"id": "kultus:2", "pEvent": {"linkedEventId": "kultus:2"}},
                {"id": "kultus:1", "pEvent": {"linkedEventId": "kultus:1"}},
            ],
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False,
                "page": 1,
                "pageSize": 10,
                "pages": 1,
                "totalCount": 3,
            },
        }
    }
}

snapshots["test_get_upcoming_events[True-True-True] 1"] = {
    "data": {
        "upcomingEvents": {
            "data": [
                {"id": "kultus:3", "pEvent": {"linkedEventId": "kultus:3"}},
                {"id": "kultus:2", "pEvent": {"linkedEventId": "kultus:2"}},
                {"id": "kultus:1", "pEvent": {"linkedEventId": "kultus:1"}},
            ],
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False,
                "page": 1,
                "pageSize": 10,
                "pages": 1,
                "totalCount": 3,
            },
        }
    }
}

snapshots["test_image_query 1"] = {
    "data": {
        "image": {
            "altText": "Kaksi naista istuu tien laidassa",
            "cropping": "0,478,1920,2399",
            "dataSource": "helsinki",
            "id": "64390",
            "name": "Tuohtumus",
            "photographerName": "Suomen Kansallisteatteri (c) Katri Naukkarinen",
            "url": "https://api.hel.fi/linkedevents/media/images/49776780903_bf54fd7b90_o.jpg",
        }
    }
}

snapshots["test_images_query 1"] = {
    "data": {
        "images": {
            "data": [
                {
                    "altText": "Kaksi naista istuu tien laidassa",
                    "cropping": "0,478,1920,2399",
                    "dataSource": "helsinki",
                    "id": "64390",
                    "name": "Tuohtumus",
                    "photographerName": "Suomen Kansallisteatteri (c) Katri Naukkarinen",
                    "url": "https://api.hel.fi/linkedevents/media/images/49776780903_bf54fd7b90_o.jpg",
                },
                {
                    "altText": None,
                    "cropping": "",
                    "dataSource": "kulke",
                    "id": "64389",
                    "name": "",
                    "photographerName": None,
                    "url": "http://www.vuotalo.fi/instancedata/prime_product_resurssivaraus/kulke/embeds/EventPic_671268.jpg",
                },
            ],
            "meta": {
                "count": 64258,
                "next": "https://api.hel.fi/linkedevents/v1/image/?page=2",
                "previous": None,
            },
        }
    }
}

snapshots["test_nearby_events 1"] = {
    "data": {
        "events": {
            "data": [
                {
                    "id": "helsinki:afy6ikna3u",
                    "internalId": "https://api.hel.fi/linkedevents/v1/event/helsinki:afy6ikna3u/",
                    "name": {
                        "en": None,
                        "fi": "Uutta Koillis-Helsinkiä verkkotilaisuus",
                        "sv": None,
                    },
                }
            ],
            "meta": {
                "count": 151775,
                "next": "https://api.hel.fi/linkedevents/v1/event/?page=2",
                "previous": None,
            },
        }
    }
}

snapshots["test_publish_event[None] 1"] = {
    "data": {
        "publishEventMutation": {
            "response": {
                "body": {
                    "endTime": None,
                    "id": "qq:afy6aghr2y",
                    "publicationStatus": "public",
                    "startTime": "2020-05-07",
                },
                "statusCode": 200,
            }
        }
    }
}

snapshots["test_publish_event[p_event_enrolment_start1] 1"] = {
    "data": {
        "publishEventMutation": {
            "response": {
                "body": {
                    "endTime": None,
                    "id": "qq:afy6aghr2y",
                    "publicationStatus": "public",
                    "startTime": "2020-05-07",
                },
                "statusCode": 200,
            }
        }
    }
}

snapshots["test_publish_event_with_external_enrolments 1"] = {
    "data": {
        "publishEventMutation": {
            "response": {
                "body": {
                    "endTime": None,
                    "id": "qq:afy6aghr2y",
                    "publicationStatus": "public",
                    "startTime": "2020-05-07",
                },
                "statusCode": 200,
            }
        }
    }
}

snapshots["test_publish_event_without_enrolments 1"] = {
    "data": {
        "publishEventMutation": {
            "response": {
                "body": {
                    "endTime": None,
                    "id": "qq:afy6aghr2y",
                    "publicationStatus": "public",
                    "startTime": "2020-05-07",
                },
                "statusCode": 200,
            }
        }
    }
}

snapshots["test_search_events 1"] = {
    "data": {
        "eventsSearch": {
            "data": [
                {
                    "audience": [],
                    "audienceMaxAge": None,
                    "audienceMinAge": None,
                    "createdTime": "2020-05-05T09:27:45.644890Z",
                    "customData": None,
                    "dataSource": "helsinki",
                    "datePublished": None,
                    "description": {
                        "en": None,
                        "fi": "<p>Tule kuulolle ja kysymään muun muassa Viikin, Pukinmäen, Puistolan, Suutarilan, Pihlajamäen, Tapanilan ja Malmin ajankohtaisista suunnitteluasioista. Koilliseen suunnitellaan uusia asuntoja ja liiketiloja, kadut ja viheralueet kohenevat.<br>Malmin lentokentän alueelle suunnitellaan asuntoja noin 25 000 ihmiselle ja Viikin-Malmin pikaraitiotiestä kaavaillaan koillisen uutta raideyhteyttä. Asemanseuduilla eli Tapulikaupunki – Puistola -alueella ja Pukinmäessä hahmotellaan kehittämisperiaatteita. Raide-Jokerin rakentaminen edistyy.<br>Osallistu kotisohvaltasi kaavoituksen sekä liikenteen ja puistojen suunnittelun tilaisuuteen maanantaina 1.6. klo 17−19. Kirjaudu sisään jo klo 16.45. Lisätietoa, ohjeet, liittymislinkki ja vinkit ennakko-osallistumisesta: hel.fi/suunnitelmat.</p><p>Esittelyssä mukana olevat hankkeet:<br>Asemakaavoitus ja muu maankäytön suunnittelu / Ota kantaa juuri nyt<br>· Malmin uimahallin laajennus<br>· Malmin energiakortteli Tattarisuon teollisuusalueen eteläpuolelle</p><p>Kadut, puistot ja viheralueet / Ota kantaa juuri nyt<br>· Katariina Saksilaisen kadun eteläosan katusuunnitelma ja Pornaistenniemen puistosuunnitelma, jotka sisältävät pyöräliikenteen baanayhteyden<br>· Kivikon puistosilta, joka ylittää Lahdenväylän ja johtaa lentokenttäalueelta Kivikon ulkoilupuistoon<br>· Maatullinkujan katusuunnitelma välillä Henrik Forsiuksen tie - Kämnerintie<br>· Suutarilan alueen katusuunnitelmia: Jupiterintie, Marsintie, Merkuriuksentie, Pikkaraistie, Riimukuja, Saturnuksentie ja Uranuksentie</p><p>Ajankohtaiskatsaus – missä mennään muiden koillisen hankkeiden kanssa <br>· Lentoasemankorttelit<br>· Lentokenttäalueen puistokilpailu ja väliaikaiskäytön ajankohtaiset suunnitelmat<br>· Malmin keskustan suunnittelutilanne<br>· Pukinmäki, Säterinportti 3, Säterintie 7-9, Madetojankuja 1 <br>· Pukinmäki, Rälssintien ja Isonkaivontien alueet <br>· Malmi, (Pihlajamäki), Rapakivenkuja 2 Pihlajamäen ostoskeskus <br>· Tapanilan asemanseudun eteläosa <br>· Töyrynummi, Puutarhakortteli <br>· Tapulikaupunki, Kämnerintie <br>· Viikki, Maakaarenkuja 2 ja Aleksanteri Nevskin katu <br>· Mellunkylä, Kivikon pelastusasematontti (helikopterikenttä) <br>· Tapulikaupunki ja Puistolan asemanseutu <br>· Pukinmäen täydennysrakentaminen<br>· Viikin-Malmin pikaraitiotie<br>· Raide-Jokerin rakentamistilanne<br>· Vanhan Porvoontien suunnittelu välillä Suurmetsäntie-Heikinlaaksontie, sisältää melusuojauksen suunnittelun</p>",
                        "sv": None,
                    },
                    "endTime": "2020-06-01T16:00:00Z",
                    "enrolmentEndTime": None,
                    "enrolmentStartTime": None,
                    "eventStatus": "EventScheduled",
                    "externalLinks": [],
                    "id": "helsinki:afy6ikna3u",
                    "images": [
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/image/64235/"
                        }
                    ],
                    "inLanguage": [
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/language/fi/"
                        }
                    ],
                    "infoUrl": {
                        "en": None,
                        "fi": "https://www.hel.fi/Helsinki/fi/asuminen-ja-ymparisto/kaavoitus/ajankohtaiset-suunnitelmat/",
                        "sv": None,
                    },
                    "internalContext": "http://schema.org",
                    "internalId": "https://api.hel.fi/linkedevents/v1/event/helsinki:afy6ikna3u/",
                    "internalType": "Event/LinkedEvent",
                    "keywords": [
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p15875/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p13980/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p14004/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p8270/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p15882/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p26626/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p8268/"
                        },
                    ],
                    "lastModifiedTime": "2020-05-05T09:27:45.644920Z",
                    "localizationExtraInfo": None,
                    "location": {
                        "internalId": "https://api.hel.fi/linkedevents/v1/place/helsinki:internet/"
                    },
                    "maximumAttendeeCapacity": None,
                    "minimumAttendeeCapacity": None,
                    "name": {
                        "en": None,
                        "fi": "Uutta Koillis-Helsinkiä verkkotilaisuus",
                        "sv": None,
                    },
                    "offers": [{"isFree": True}],
                    "provider": None,
                    "providerContactInfo": None,
                    "publicationStatus": None,
                    "publisher": "ahjo:u541000",
                    "remainingAttendeeCapacity": None,
                    "shortDescription": {
                        "en": None,
                        "fi": "Tule kuulemaan ja keskustelemaan verkkoon uudistuvasta Koillis-Helsingistä omalta kotisohvaltasi. Juuri nyt voit vaikuttaa useisiin suunnittelukohteisiin!",
                        "sv": None,
                    },
                    "startTime": "2020-06-01T13:45:00Z",
                    "subEvents": [],
                    "superEvent": None,
                    "superEventType": None,
                },
                {
                    "audience": [],
                    "audienceMaxAge": None,
                    "audienceMinAge": None,
                    "createdTime": "2019-12-13T12:49:40.545273Z",
                    "customData": None,
                    "dataSource": "helsinki",
                    "datePublished": None,
                    "description": {
                        "en": "<p>Visual artist Raija Malka and composer Kaija Saariaho will take over Amos Rex’s exhibition space in a new and experiential way next summer. The work is painterly, spatial and musical all at once, offering visitors an opportunity to shape the space with their own creativity.</p><p>The exhibition title, Blick (Gaze), is a reference to visual artist Wassily Kandinsky’s poem from 1912 that is included in the soundscape by Kaija Saariaho. The gazes of the two artists are brought together in a three-dimensional space.</p><p>The exhibition is a multisensory experience that invites people to stay. In a world made up of the colours and sounds of Malka and Saariaho, visitors can build their own arrangements.</p><p>Amos Rex<br>10.6.-30.8. </p><p>Mon, Fri 11.00-18.00<br>Wed, Thu 11.00-20.00<br>Sat, Sun 11.00-17.00</p><p>Admission fee 5-15€, under 18 yrs free entry</p>",
                        "fi": "<p>Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho täyttävät ensi kesänä Amos Rexin näyttelytilan uudella kokemuksellisella tavalla. Teos on yhtä aikaa maalauksellinen, tilallinen ja musiikillinen. </p><p>Näyttelyn nimi Blick (Katse) viittaa kuvataiteilija Wassily Kandinskyn 1912 julkaistuun runoon, joka sisältyy Kaija Saariahon näyttelyssä kuultavaan äänimaisemaan. Kahden taiteilijan katseet yhdistyvät näyttelyn kolmiulotteisessa tilassa.</p><p>Näyttely on moniaistinen kokonaisuus, joka houkuttelee viipymään. Kävijä voi rakentaa omia asetelmiaan Malkan ja Saariahon väri- ja äänimaailmaan.</p><p>Amos Rex<br>10.6.-30.8. </p><p>ma, pe klo 11-18<br>ke, to klo 11-20<br>la, su klo 11-17</p><p>Sisäänpääsy 5-15€, alle 18-vuotiaille vapaa pääsy</p>",
                        "sv": "<p>Bildkonstnären Raija Malka och kompositören Kaija Saariaho fyller Amos Rex utställningsutrymme på ett nytt och experimentellt sätt nästa sommaren. Deras verk är på en och samma gång måleriskt, rumsligt och musikaliskt. </p><p>Utställningstiteln, Blick, syftar på bildkonstnären Wassily Kandinskys dikt från 1912. Texten ingår i Kaija Saariahos ljuder i utställningen. De två konstnärernas blickar möts i det tredimensionella utställningsutrymmet.</p><p>Utställningen utgör en sinnlig helhet som lockar besökare att dröja kvar. De kan bidra till Malkas och Saariahos färg- och ljudvärld med sina egna byggstenar.</p><p>Amos Rex<br>10.6.-30.8. </p><p>må, fre kl 11-18<br>ons, to kl 11-20<br>lö, sö kl 11-17</p><p>Inträde 5-15€, under 18 år fritt inträde</p>",
                    },
                    "endTime": None,
                    "enrolmentEndTime": None,
                    "enrolmentStartTime": None,
                    "eventStatus": "EventPostponed",
                    "externalLinks": [],
                    "id": "helsinki:afxp6tv4xa",
                    "images": [
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/image/61106/"
                        }
                    ],
                    "inLanguage": [],
                    "infoUrl": {
                        "en": "http://www.amosrex.fi",
                        "fi": "http://www.amosrex.fi",
                        "sv": "http://www.amosrex.fi",
                    },
                    "internalContext": "http://schema.org",
                    "internalId": "https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/",
                    "internalType": "Event/LinkedEvent",
                    "keywords": [
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/helfi:12/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p5121/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p6889/"
                        },
                        {
                            "internalId": "https://api.hel.fi/linkedevents/v1/keyword/yso:p1808/"
                        },
                    ],
                    "lastModifiedTime": "2020-05-05T09:24:58.569334Z",
                    "localizationExtraInfo": None,
                    "location": {
                        "internalId": "https://api.hel.fi/linkedevents/v1/place/tprek:55959/"
                    },
                    "maximumAttendeeCapacity": None,
                    "minimumAttendeeCapacity": None,
                    "name": {
                        "en": "Raija Malka & Kaija Saariaho: Blick",
                        "fi": "Raija Malka & Kaija Saariaho: Blick",
                        "sv": "Raija Malka & Kaija Saariaho: Blick",
                    },
                    "offers": [{"isFree": False}],
                    "provider": {"en": "Amos Rex", "fi": "Amos Rex", "sv": "Amos Rex"},
                    "providerContactInfo": None,
                    "publicationStatus": None,
                    "publisher": "ytj:0586977-6",
                    "remainingAttendeeCapacity": None,
                    "shortDescription": {
                        "en": "Visual artist Raija Malka and composer Kaija Saariaho will take over Amos Rex’s exhibition space in a new and experiential way next summer. ",
                        "fi": "Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho täyttävät ensi kesänä Amos Rexin näyttelytilan uudella kokemuksellisella tavalla. ",
                        "sv": "Bildkonstnären Raija Malka och kompositören Kaija Saariaho fyller Amos Rex utställningsutrymme på ett nytt och experimentellt sätt nästa sommaren.",
                    },
                    "startTime": None,
                    "subEvents": [],
                    "superEvent": None,
                    "superEventType": None,
                },
            ],
            "meta": {
                "count": 151775,
                "next": "https://api.hel.fi/linkedevents/v1/event/?page=2",
                "previous": None,
            },
        }
    }
}

snapshots["test_search_places 1"] = {
    "data": {
        "placesSearch": {
            "data": [
                {
                    "addressCountry": None,
                    "addressLocality": {"en": "Espoo", "fi": "Espoo", "sv": "Esbo"},
                    "addressRegion": None,
                    "contactType": None,
                    "createdTime": None,
                    "customData": None,
                    "dataSource": "tprek",
                    "deleted": False,
                    "description": None,
                    "divisions": [{"municipality": None, "ocdId": None}],
                    "email": "sellonkirjasto@espoo.fi",
                    "id": "tprek:15417",
                    "image": 54259,
                    "infoUrl": {
                        "en": "http://www.helmet.fi/sellolibrary",
                        "fi": "http://www.helmet.fi/sello",
                        "sv": "http://www.helmet.fi/sellobiblioteket",
                    },
                    "internalContext": "http://schema.org",
                    "internalId": "https://api.hel.fi/linkedevents/v1/place/tprek:15417/",
                    "internalType": "Place",
                    "lastModifiedTime": "2020-04-25T05:09:10.712132Z",
                    "nEvents": 27264,
                    "name": {
                        "en": "Sello Library",
                        "fi": "Sellon kirjasto",
                        "sv": "Sellobiblioteket",
                    },
                    "parent": None,
                    "position": {"coordinates": [24.80992, 60.21748], "type": "Point"},
                    "postOfficeBoxNum": None,
                    "postalCode": "02600",
                    "publisher": "ahjo:u021600",
                    "replacedBy": None,
                    "streetAddress": {
                        "en": "Leppävaarankatu 9",
                        "fi": "Leppävaarankatu 9",
                        "sv": "Albergagatan 9",
                    },
                    "telephone": {"en": None, "fi": "+358 9 8165 7603", "sv": None},
                },
                {
                    "addressCountry": None,
                    "addressLocality": {"en": "Espoo", "fi": "Espoo", "sv": "Esbo"},
                    "addressRegion": None,
                    "contactType": None,
                    "createdTime": None,
                    "customData": None,
                    "dataSource": "tprek",
                    "deleted": False,
                    "description": None,
                    "divisions": [{"municipality": None, "ocdId": None}],
                    "email": "kirjasto.entresse@espoo.fi",
                    "id": "tprek:15321",
                    "image": 54251,
                    "infoUrl": {
                        "en": "http://www.helmet.fi/entressebibliotek",
                        "fi": "http://www.helmet.fi/entressenkirjasto",
                        "sv": "http://www.helmet.fi/entressebibliotek",
                    },
                    "internalContext": "http://schema.org",
                    "internalId": "https://api.hel.fi/linkedevents/v1/place/tprek:15321/",
                    "internalType": "Place",
                    "lastModifiedTime": "2019-09-19T14:10:59.747979Z",
                    "nEvents": 7745,
                    "name": {
                        "en": "Entresse Library",
                        "fi": "Entressen kirjasto",
                        "sv": "Entressebiblioteket",
                    },
                    "parent": None,
                    "position": {
                        "coordinates": [24.657864, 60.203636],
                        "type": "Point",
                    },
                    "postOfficeBoxNum": None,
                    "postalCode": "02770",
                    "publisher": "ahjo:u021600",
                    "replacedBy": None,
                    "streetAddress": {
                        "en": "Siltakatu 11",
                        "fi": "Siltakatu 11",
                        "sv": "Brogatan 11",
                    },
                    "telephone": {"en": None, "fi": "+358 9 8165 3776", "sv": None},
                },
            ],
            "meta": {
                "count": 1346,
                "next": "https://api.hel.fi/linkedevents/v1/place/?page=2&page_size=2&show_all_places=",
                "previous": None,
            },
        }
    }
}

snapshots["test_unpublish_event 1"] = {
    "data": {
        "unpublishEventMutation": {
            "response": {
                "body": {
                    "endTime": None,
                    "id": "qq:afy6aghr2y",
                    "publicationStatus": "draft",
                    "startTime": "2020-05-07",
                },
                "statusCode": 200,
            }
        }
    }
}

snapshots["test_update_event 1"] = {
    "data": {
        "updateEventMutation": {
            "response": {
                "body": {
                    "description": {"en": "desc en", "fi": "desc", "sv": "desc sv"},
                    "id": "qq:afy6aghr2y",
                    "infoUrl": None,
                    "keywords": [{"id": None}],
                    "location": {"id": None},
                    "offers": [{"isFree": False}],
                    "pEvent": {
                        "autoAcceptance": True,
                        "autoAcceptanceMessage": "Päivitetty viesti",
                        "contactEmail": "contact@email.me",
                        "contactPerson": {"name": "Sean Rocha"},
                        "contactPhoneNumber": "123123",
                        "enrolmentEndDays": 2,
                        "enrolmentStart": "2020-06-06T16:40:48+00:00",
                        "externalEnrolmentUrl": None,
                        "linkedEventId": "qq:afy6aghr2y",
                        "mandatoryAdditionalInformation": True,
                        "neededOccurrences": 1,
                        "organisation": {"name": "Chapman, Scott and Martin"},
                        "translations": [
                            {
                                "autoAcceptanceMessage": "Päivitetty viesti",
                                "languageCode": "FI",
                            },
                            {
                                "autoAcceptanceMessage": "Updated custom message",
                                "languageCode": "EN",
                            },
                        ],
                    },
                    "shortDescription": {
                        "en": "short desc en",
                        "fi": "short desc",
                        "sv": "short desc sv",
                    },
                    "startTime": "2020-05-07",
                },
                "statusCode": 200,
            }
        }
    }
}

snapshots["test_update_image 1"] = {
    "data": {
        "updateImageMutation": {
            "response": {
                "body": {
                    "altText": "Kaksi naista istuu tien laidassa",
                    "cropping": "0,478,1920,2399",
                    "dataSource": "helsinki",
                    "id": "64390",
                    "name": "Tuohtumus",
                    "photographerName": "Suomen Kansallisteatteri (c) Katri Naukkarinen",
                    "url": "https://api.hel.fi/linkedevents/media/images/49776780903_bf54fd7b90_o.jpg",
                },
                "statusCode": 200,
            }
        }
    }
}
