# Real sample data copied from Linked Events REST API at
# https://api.hel.fi/linkedevents/v1/
EVENTS_DATA = {
    "meta": {
        "count": 151775,
        "next": "https://api.hel.fi/linkedevents/v1/event/?page=2",
        "previous": None,
    },
    "data": [
        {
            "id": "helsinki:afy6ikna3u",
            "location": {
                "@id": "https://api.hel.fi/linkedevents/v1/place/helsinki:internet/"
            },
            "keywords": [
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p15875/"},
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p13980/"},
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p14004/"},
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p8270/"},
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p15882/"},
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p26626/"},
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p8268/"},
            ],
            "super_event": None,
            "event_status": "EventScheduled",
            "external_links": [],
            "offers": [
                {"is_free": True, "price": None, "description": None, "info_url": None}
            ],
            "data_source": "helsinki",
            "publisher": "ahjo:u541000",
            "sub_events": [],
            "images": [
                {
                    "id": 64235,
                    "license": "event_only",
                    "created_time": "2020-05-05T09:16:50.965146Z",
                    "last_modified_time": "2020-05-05T09:16:50.965171Z",
                    "name": "UKH2020_fb _tapahtuma 1920 x10802.jpg",
                    "url": "https://api.hel.fi/linkedevents/media/images"
                    "/UKH2020_fb__tapahtuma_1920_x10802.jpg",
                    "cropping": "420,0,1500,1080",
                    "photographer_name": "",
                    "alt_text": "Ideakuva tulevaisuuden Malmin keskustan katunäkymästä",
                    "data_source": "helsinki",
                    "publisher": "ahjo:u541000",
                    "@id": "https://api.hel.fi/linkedevents/v1/image/64235/",
                    "@context": "http://schema.org",
                    "@type": "ImageObject",
                }
            ],
            "videos": [],
            "in_language": [{"@id": "https://api.hel.fi/linkedevents/v1/language/fi/"}],
            "audience": [],
            "created_time": "2020-05-05T09:27:45.644890Z",
            "last_modified_time": "2020-05-05T09:27:45.644920Z",
            "date_published": None,
            "start_time": "2020-06-01T13:45:00Z",
            "end_time": "2020-06-01T16:00:00Z",
            "custom_data": None,
            "audience_min_age": None,
            "audience_max_age": None,
            "super_event_type": None,
            "deleted": False,
            "replaced_by": None,
            "short_description": {
                "fi": "Tule kuulemaan ja keskustelemaan verkkoon uudistuvasta "
                "Koillis-Helsingistä omalta kotisohvaltasi. Juuri nyt voit "
                "vaikuttaa useisiin suunnittelukohteisiin!"
            },
            "location_extra_info": {
                "fi": "liittymislinkki julkaistaan sivulla hel.fi/suunnitelmat "
                "lähempänä tilaisuutta"
            },
            "name": {"fi": "Uutta Koillis-Helsinkiä verkkotilaisuus"},
            "info_url": {
                "fi": "https://www.hel.fi/Helsinki/fi/asuminen-ja-ymparisto/kaavoitus"
                "/ajankohtaiset-suunnitelmat/"
            },
            "provider": None,
            "description": {
                "fi": "<p>Tule kuulolle ja kysymään muun muassa Viikin, Pukinmäen, "
                "Puistolan, Suutarilan, Pihlajamäen, Tapanilan ja Malmin "
                "ajankohtaisista suunnitteluasioista. Koilliseen suunnitellaan "
                "uusia asuntoja ja liiketiloja, kadut ja viheralueet "
                "kohenevat.<br>Malmin lentokentän alueelle suunnitellaan "
                "asuntoja noin 25 000 ihmiselle ja Viikin-Malmin "
                "pikaraitiotiestä kaavaillaan koillisen uutta raideyhteyttä. "
                "Asemanseuduilla eli Tapulikaupunki – Puistola -alueella ja "
                "Pukinmäessä hahmotellaan kehittämisperiaatteita. Raide-Jokerin "
                "rakentaminen edistyy.<br>Osallistu kotisohvaltasi kaavoituksen "
                "sekä liikenteen ja puistojen suunnittelun tilaisuuteen "
                "maanantaina 1.6. klo 17−19. Kirjaudu sisään jo klo 16.45. "
                "Lisätietoa, ohjeet, liittymislinkki ja vinkit "
                "ennakko-osallistumisesta: "
                "hel.fi/suunnitelmat.</p><p>Esittelyssä mukana olevat "
                "hankkeet:<br>Asemakaavoitus ja muu maankäytön suunnittelu / "
                "Ota kantaa juuri nyt<br>· Malmin uimahallin laajennus<br>· "
                "Malmin energiakortteli Tattarisuon teollisuusalueen "
                "eteläpuolelle</p><p>Kadut, puistot ja viheralueet / Ota kantaa "
                "juuri nyt<br>· Katariina Saksilaisen kadun eteläosan "
                "katusuunnitelma ja Pornaistenniemen puistosuunnitelma, "
                "jotka sisältävät pyöräliikenteen baanayhteyden<br>· Kivikon "
                "puistosilta, joka ylittää Lahdenväylän ja johtaa "
                "lentokenttäalueelta Kivikon ulkoilupuistoon<br>· "
                "Maatullinkujan katusuunnitelma välillä Henrik Forsiuksen tie - "
                "Kämnerintie<br>· Suutarilan alueen katusuunnitelmia: "
                "Jupiterintie, Marsintie, Merkuriuksentie, Pikkaraistie, "
                "Riimukuja, Saturnuksentie ja "
                "Uranuksentie</p><p>Ajankohtaiskatsaus – missä mennään muiden "
                "koillisen hankkeiden kanssa <br>· Lentoasemankorttelit<br>· "
                "Lentokenttäalueen puistokilpailu ja väliaikaiskäytön "
                "ajankohtaiset suunnitelmat<br>· Malmin keskustan "
                "suunnittelutilanne<br>· Pukinmäki, Säterinportti 3, Säterintie "
                "7-9, Madetojankuja 1 <br>· Pukinmäki, Rälssintien ja "
                "Isonkaivontien alueet <br>· Malmi, (Pihlajamäki), "
                "Rapakivenkuja 2 Pihlajamäen ostoskeskus <br>· Tapanilan "
                "asemanseudun eteläosa <br>· Töyrynummi, Puutarhakortteli <br>· "
                "Tapulikaupunki, Kämnerintie <br>· Viikki, Maakaarenkuja 2 ja "
                "Aleksanteri Nevskin katu <br>· Mellunkylä, Kivikon "
                "pelastusasematontti (helikopterikenttä) <br>· Tapulikaupunki "
                "ja Puistolan asemanseutu <br>· Pukinmäen "
                "täydennysrakentaminen<br>· Viikin-Malmin pikaraitiotie<br>· "
                "Raide-Jokerin rakentamistilanne<br>· Vanhan Porvoontien "
                "suunnittelu välillä Suurmetsäntie-Heikinlaaksontie, sisältää "
                "melusuojauksen suunnittelun</p>"
            },
            "provider_contact_info": None,
            "@id": "https://api.hel.fi/linkedevents/v1/event/helsinki:afy6ikna3u/",
            "@context": "http://schema.org",
            "@type": "Event/LinkedEvent",
        },
        {
            "id": "helsinki:afxp6tv4xa",
            "location": {
                "@id": "https://api.hel.fi/linkedevents/v1/place/tprek:55959/"
            },
            "keywords": [
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/helfi:12/"},
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p5121/"},
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p6889/"},
                {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p1808/"},
            ],
            "super_event": None,
            "event_status": "EventPostponed",
            "external_links": [],
            "offers": [
                {
                    "is_free": False,
                    "price": {"fi": "5-15€", "sv": "5-15€", "en": "5-15€"},
                    "description": {"fi": "", "sv": "", "en": ""},
                    "info_url": {
                        "fi": "http://www.amosrex.fi",
                        "sv": "http://www.amosrex.fi",
                        "en": "http://www.amosrex.fi",
                    },
                }
            ],
            "data_source": "helsinki",
            "publisher": "ytj:0586977-6",
            "sub_events": [],
            "images": [
                {
                    "id": 61106,
                    "license": "event_only",
                    "created_time": "2019-12-13T12:45:32.745630Z",
                    "last_modified_time": "2019-12-13T12:45:32.745657Z",
                    "name": "Raija Malka & Kaija Saariaho: Blick",
                    "url": "https://api.hel.fi/linkedevents/media/images/49a8985e"
                    "-2448-44de-ad31-384.jpg",
                    "cropping": "322,0,1598,1275",
                    "photographer_name": "Amos Rex (c) Sara Magno",
                    "alt_text": None,
                    "data_source": "helsinki",
                    "publisher": "ytj:0586977-6",
                    "@id": "https://api.hel.fi/linkedevents/v1/image/61106/",
                    "@context": "http://schema.org",
                    "@type": "ImageObject",
                }
            ],
            "videos": [],
            "in_language": [],
            "audience": [],
            "created_time": "2019-12-13T12:49:40.545273Z",
            "last_modified_time": "2020-05-05T09:24:58.569334Z",
            "date_published": None,
            "start_time": None,
            "end_time": None,
            "custom_data": None,
            "audience_min_age": None,
            "audience_max_age": None,
            "super_event_type": None,
            "deleted": False,
            "replaced_by": None,
            "short_description": {
                "fi": "Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho "
                "täyttävät ensi kesänä Amos Rexin näyttelytilan uudella "
                "kokemuksellisella tavalla. ",
                "sv": "Bildkonstnären Raija Malka och kompositören Kaija Saariaho "
                "fyller Amos Rex utställningsutrymme på ett nytt och "
                "experimentellt sätt nästa sommaren.",
                "en": "Visual artist Raija Malka and composer Kaija Saariaho will "
                "take over Amos Rex’s exhibition space in a new and "
                "experiential way next summer. ",
            },
            "location_extra_info": None,
            "name": {
                "fi": "Raija Malka & Kaija Saariaho: Blick",
                "sv": "Raija Malka & Kaija Saariaho: Blick",
                "en": "Raija Malka & Kaija Saariaho: Blick",
            },
            "info_url": {
                "fi": "http://www.amosrex.fi",
                "sv": "http://www.amosrex.fi",
                "en": "http://www.amosrex.fi",
            },
            "provider": {"fi": "Amos Rex", "sv": "Amos Rex", "en": "Amos Rex"},
            "description": {
                "fi": "<p>Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho "
                "täyttävät ensi kesänä Amos Rexin näyttelytilan uudella "
                "kokemuksellisella tavalla. Teos on yhtä aikaa maalauksellinen, "
                "tilallinen ja musiikillinen. </p><p>Näyttelyn nimi Blick ("
                "Katse) viittaa kuvataiteilija Wassily Kandinskyn 1912 "
                "julkaistuun runoon, joka sisältyy Kaija Saariahon näyttelyssä "
                "kuultavaan äänimaisemaan. Kahden taiteilijan katseet "
                "yhdistyvät näyttelyn kolmiulotteisessa tilassa.</p><p>Näyttely "
                "on moniaistinen kokonaisuus, joka houkuttelee viipymään. "
                "Kävijä voi rakentaa omia asetelmiaan Malkan ja Saariahon väri- "
                "ja äänimaailmaan.</p><p>Amos Rex<br>10.6.-30.8. </p><p>ma, "
                "pe klo 11-18<br>ke, to klo 11-20<br>la, su klo "
                "11-17</p><p>Sisäänpääsy 5-15€, alle 18-vuotiaille vapaa "
                "pääsy</p>",
                "sv": "<p>Bildkonstnären Raija Malka och kompositören Kaija Saariaho "
                "fyller Amos Rex utställningsutrymme på ett nytt och "
                "experimentellt sätt nästa sommaren. Deras verk är på en och "
                "samma gång måleriskt, rumsligt och musikaliskt. "
                "</p><p>Utställningstiteln, Blick, syftar på bildkonstnären "
                "Wassily Kandinskys dikt från 1912. Texten ingår i Kaija "
                "Saariahos ljuder i utställningen. De två konstnärernas blickar "
                "möts i det tredimensionella "
                "utställningsutrymmet.</p><p>Utställningen utgör en sinnlig "
                "helhet som lockar besökare att dröja kvar. De kan bidra till "
                "Malkas och Saariahos färg- och ljudvärld med sina egna "
                "byggstenar.</p><p>Amos Rex<br>10.6.-30.8. </p><p>må, "
                "fre kl 11-18<br>ons, to kl 11-20<br>lö, "
                "sö kl 11-17</p><p>Inträde 5-15€, under 18 år fritt inträde</p>",
                "en": "<p>Visual artist Raija Malka and composer Kaija Saariaho will "
                "take over Amos Rex’s exhibition space in a new and "
                "experiential way next summer. The work is painterly, spatial "
                "and musical all at once, offering visitors an opportunity to "
                "shape the space with their own creativity.</p><p>The "
                "exhibition title, Blick (Gaze), is a reference to visual "
                "artist Wassily Kandinsky’s poem from 1912 that is included in "
                "the soundscape by Kaija Saariaho. The gazes of the two artists "
                "are brought together in a three-dimensional space.</p><p>The "
                "exhibition is a multisensory experience that invites people to "
                "stay. In a world made up of the colours and sounds of Malka "
                "and Saariaho, visitors can build their own "
                "arrangements.</p><p>Amos Rex<br>10.6.-30.8. </p><p>Mon, "
                "Fri 11.00-18.00<br>Wed, Thu 11.00-20.00<br>Sat, "
                "Sun 11.00-17.00</p><p>Admission fee 5-15€, under 18 yrs free "
                "entry</p>",
            },
            "provider_contact_info": None,
            "@id": "https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/",
            "@context": "http://schema.org",
            "@type": "Event/LinkedEvent",
        },
    ],
}

EVENT_DATA = {
    "id": "helsinki:afxp6tv4xa",
    "location": {
        "id": "tprek:15321",
        "divisions": [
            {
                "type": "muni",
                "ocd_id": "ocd-division/country:fi/kunta:espoo",
                "municipality": None,
                "name": {"fi": "Espoo", "sv": "Esbo"},
            }
        ],
        "created_time": None,
        "last_modified_time": "2019-10-04T12:33:26.019395Z",
        "custom_data": None,
        "email": "kirjasto.entresse@espoo.fi",
        "contact_type": None,
        "address_region": None,
        "postal_code": "02770",
        "post_office_box_num": None,
        "address_country": None,
        "deleted": False,
        "has_upcoming_events": False,
        "n_events": 5438,
        "image": 47931,
        "data_source": "tprek",
        "publisher": "ahjo:u021600",
        "parent": None,
        "replaced_by": None,
        "position": {"type": "Point", "coordinates": [24.657864, 60.203636]},
        "telephone": {"fi": "+358 9 8165 3776"},
        "name": {
            "fi": "Entressen kirjasto",
            "sv": "Entressebiblioteket",
            "en": "Entresse Library",
        },
        "street_address": {
            "fi": "Siltakatu 11",
            "sv": "Brogatan 11",
            "en": "Siltakatu 11",
        },
        "address_locality": {"fi": "Espoo", "sv": "Esbo", "en": "Espoo"},
        "info_url": {
            "fi": "http://www.helmet.fi/entressenkirjasto",
            "sv": "http://www.helmet.fi/entressebibliotek",
            "en": "http://www.helmet.fi/entressebibliotek",
        },
        "description": None,
        "@id": "https://api.hel.fi/linkedevents-test/v1/place/tprek:15321/",
        "@context": "http://schema.org",
        "@type": "Place",
    },
    "keywords": [
        {
            "@id": "https://api.hel.fi/linkedevents/v1/keyword/helfi:12/",
            "id": "helfi:12",
        },
        {
            "@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p5121/",
            "id": "yso:p5121",
        },
        {
            "@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p6889/",
            "id": "yso:p6889",
        },
        {
            "@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p1808/",
            "id": "yso:p1808",
        },
    ],
    "super_event": None,
    "event_status": "EventPostponed",
    "publication_status": "public",
    "external_links": [],
    "offers": [
        {
            "is_free": False,
            "price": {"fi": "5-15€", "sv": "5-15€", "en": "5-15€"},
            "description": {"fi": "", "sv": "", "en": ""},
            "info_url": {
                "fi": "http://www.amosrex.fi",
                "sv": "http://www.amosrex.fi",
                "en": "http://www.amosrex.fi",
            },
        }
    ],
    "data_source": "helsinki",
    "publisher": "ytj:0586977-6",
    "sub_events": [],
    "images": [
        {
            "id": 61106,
            "license": "event_only",
            "created_time": "2019-12-13T12:45:32.745630Z",
            "last_modified_time": "2019-12-13T12:45:32.745657Z",
            "name": "Raija Malka & Kaija Saariaho: Blick",
            "url": "https://api.hel.fi/linkedevents/media/images/49a8985e-2448-44de"
            "-ad31-384.jpg",
            "cropping": "322,0,1598,1275",
            "photographer_name": "Amos Rex (c) Sara Magno",
            "alt_text": None,
            "data_source": "helsinki",
            "publisher": "ytj:0586977-6",
            "@id": "https://api.hel.fi/linkedevents/v1/image/61106/",
            "@context": "http://schema.org",
            "@type": "ImageObject",
        }
    ],
    "videos": [],
    "in_language": [],
    "audience": [],
    "created_time": "2019-12-13T12:49:40.545273Z",
    "last_modified_time": "2020-05-05T09:24:58.569334Z",
    "date_published": None,
    "start_time": None,
    "end_time": None,
    "maximum_attendee_capacity": None,
    "remaining_attendee_capacity": None,
    "minimum_attendee_capacity": None,
    "enrolment_start_time": None,
    "enrolment_end_time": None,
    "custom_data": None,
    "audience_min_age": None,
    "audience_max_age": None,
    "super_event_type": None,
    "deleted": False,
    "replaced_by": None,
    "short_description": {
        "fi": "Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho täyttävät ensi "
        "kesänä Amos Rexin näyttelytilan uudella kokemuksellisella tavalla. ",
        "sv": "Bildkonstnären Raija Malka och kompositören Kaija Saariaho fyller Amos "
        "Rex utställningsutrymme på ett nytt och experimentellt sätt nästa "
        "sommaren.",
        "en": "Visual artist Raija Malka and composer Kaija Saariaho will take over "
        "Amos Rex’s exhibition space in a new and experiential way next summer. ",
    },
    "location_extra_info": None,
    "name": {
        "fi": "Raija Malka & Kaija Saariaho: Blick",
        "sv": "Raija Malka & Kaija Saariaho: Blick",
        "en": "Raija Malka & Kaija Saariaho: Blick",
    },
    "info_url": {
        "fi": "http://www.amosrex.fi",
        "sv": "http://www.amosrex.fi",
        "en": "http://www.amosrex.fi",
    },
    "provider": {"fi": "Amos Rex", "sv": "Amos Rex", "en": "Amos Rex"},
    "description": {
        "fi": "<p>Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho täyttävät "
        "ensi kesänä Amos Rexin näyttelytilan uudella kokemuksellisella "
        "tavalla. Teos on yhtä aikaa maalauksellinen, tilallinen ja "
        "musiikillinen. </p><p>Näyttelyn nimi Blick (Katse) viittaa "
        "kuvataiteilija Wassily Kandinskyn 1912 julkaistuun runoon, "
        "joka sisältyy Kaija Saariahon näyttelyssä kuultavaan äänimaisemaan. "
        "Kahden taiteilijan katseet yhdistyvät näyttelyn kolmiulotteisessa "
        "tilassa.</p><p>Näyttely on moniaistinen kokonaisuus, joka houkuttelee "
        "viipymään. Kävijä voi rakentaa omia asetelmiaan Malkan ja Saariahon "
        "väri- ja äänimaailmaan.</p><p>Amos Rex<br>10.6.-30.8. </p><p>ma, "
        "pe klo 11-18<br>ke, to klo 11-20<br>la, su klo 11-17</p><p>Sisäänpääsy "
        "5-15€, alle 18-vuotiaille vapaa pääsy</p>",
        "sv": "<p>Bildkonstnären Raija Malka och kompositören Kaija Saariaho fyller "
        "Amos Rex utställningsutrymme på ett nytt och experimentellt sätt nästa "
        "sommaren. Deras verk är på en och samma gång måleriskt, rumsligt och "
        "musikaliskt. </p><p>Utställningstiteln, Blick, syftar på "
        "bildkonstnären Wassily Kandinskys dikt från 1912. Texten ingår i Kaija "
        "Saariahos ljuder i utställningen. De två konstnärernas blickar möts i "
        "det tredimensionella utställningsutrymmet.</p><p>Utställningen utgör "
        "en sinnlig helhet som lockar besökare att dröja kvar. De kan bidra "
        "till Malkas och Saariahos färg- och ljudvärld med sina egna "
        "byggstenar.</p><p>Amos Rex<br>10.6.-30.8. </p><p>må, fre kl "
        "11-18<br>ons, to kl 11-20<br>lö, sö kl 11-17</p><p>Inträde 5-15€, "
        "under 18 år fritt inträde</p>",
        "en": "<p>Visual artist Raija Malka and composer Kaija Saariaho will take "
        "over Amos Rex’s exhibition space in a new and experiential way next "
        "summer. The work is painterly, spatial and musical all at once, "
        "offering visitors an opportunity to shape the space with their own "
        "creativity.</p><p>The exhibition title, Blick (Gaze), is a reference "
        "to visual artist Wassily Kandinsky’s poem from 1912 that is included "
        "in the soundscape by Kaija Saariaho. The gazes of the two artists are "
        "brought together in a three-dimensional space.</p><p>The exhibition is "
        "a multisensory experience that invites people to stay. In a world made "
        "up of the colours and sounds of Malka and Saariaho, visitors can build "
        "their own arrangements.</p><p>Amos Rex<br>10.6.-30.8. </p><p>Mon, "
        "Fri 11.00-18.00<br>Wed, Thu 11.00-20.00<br>Sat, "
        "Sun 11.00-17.00</p><p>Admission fee 5-15€, under 18 yrs free entry</p>",
    },
    "provider_contact_info": None,
    "@id": "https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/",
    "@context": "http://schema.org",
    "@type": "Event/LinkedEvent",
}

DRAFT_EVENT_DATA = {
    "id": "helsinki:afxp6tv4xa",
    "location": {"@id": "https://api.hel.fi/linkedevents/v1/place/tprek:55959/"},
    "keywords": [
        {"@id": "https://api.hel.fi/linkedevents/v1/keyword/helfi:12/"},
        {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p5121/"},
        {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p6889/"},
        {"@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p1808/"},
    ],
    "super_event": None,
    "event_status": "EventPostponed",
    "publication_status": "draft",
    "external_links": [],
    "offers": [
        {
            "is_free": False,
            "price": {"fi": "5-15€", "sv": "5-15€", "en": "5-15€"},
            "description": {"fi": "", "sv": "", "en": ""},
            "info_url": {
                "fi": "http://www.amosrex.fi",
                "sv": "http://www.amosrex.fi",
                "en": "http://www.amosrex.fi",
            },
        }
    ],
    "data_source": "helsinki",
    "publisher": "ytj:0586977-6",
    "sub_events": [],
    "images": [
        {
            "id": 61106,
            "license": "event_only",
            "created_time": "2019-12-13T12:45:32.745630Z",
            "last_modified_time": "2019-12-13T12:45:32.745657Z",
            "name": "Raija Malka & Kaija Saariaho: Blick",
            "url": "https://api.hel.fi/linkedevents/media/images/49a8985e-2448-44de"
            "-ad31-384.jpg",
            "cropping": "322,0,1598,1275",
            "photographer_name": "Amos Rex (c) Sara Magno",
            "alt_text": None,
            "data_source": "helsinki",
            "publisher": "ytj:0586977-6",
            "@id": "https://api.hel.fi/linkedevents/v1/image/61106/",
            "@context": "http://schema.org",
            "@type": "ImageObject",
        }
    ],
    "videos": [],
    "in_language": [],
    "audience": [],
    "created_time": "2019-12-13T12:49:40.545273Z",
    "last_modified_time": "2020-05-05T09:24:58.569334Z",
    "date_published": None,
    "start_time": None,
    "end_time": None,
    "maximum_attendee_capacity": None,
    "remaining_attendee_capacity": None,
    "minimum_attendee_capacity": None,
    "enrolment_start_time": None,
    "enrolment_end_time": None,
    "custom_data": None,
    "audience_min_age": None,
    "audience_max_age": None,
    "super_event_type": None,
    "deleted": False,
    "replaced_by": None,
    "short_description": {
        "fi": "Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho täyttävät ensi "
        "kesänä Amos Rexin näyttelytilan uudella kokemuksellisella tavalla. ",
        "sv": "Bildkonstnären Raija Malka och kompositören Kaija Saariaho fyller Amos "
        "Rex utställningsutrymme på ett nytt och experimentellt sätt nästa "
        "sommaren.",
        "en": "Visual artist Raija Malka and composer Kaija Saariaho will take over "
        "Amos Rex’s exhibition space in a new and experiential way next summer. ",
    },
    "location_extra_info": None,
    "name": {
        "fi": "Raija Malka & Kaija Saariaho: Blick",
        "sv": "Raija Malka & Kaija Saariaho: Blick",
        "en": "Raija Malka & Kaija Saariaho: Blick",
    },
    "info_url": {
        "fi": "http://www.amosrex.fi",
        "sv": "http://www.amosrex.fi",
        "en": "http://www.amosrex.fi",
    },
    "provider": {"fi": "Amos Rex", "sv": "Amos Rex", "en": "Amos Rex"},
    "description": {
        "fi": "<p>Kuvataiteilija Raija Malka ja säveltäjä Kaija Saariaho täyttävät "
        "ensi kesänä Amos Rexin näyttelytilan uudella kokemuksellisella "
        "tavalla. Teos on yhtä aikaa maalauksellinen, tilallinen ja "
        "musiikillinen. </p><p>Näyttelyn nimi Blick (Katse) viittaa "
        "kuvataiteilija Wassily Kandinskyn 1912 julkaistuun runoon, "
        "joka sisältyy Kaija Saariahon näyttelyssä kuultavaan äänimaisemaan. "
        "Kahden taiteilijan katseet yhdistyvät näyttelyn kolmiulotteisessa "
        "tilassa.</p><p>Näyttely on moniaistinen kokonaisuus, joka houkuttelee "
        "viipymään. Kävijä voi rakentaa omia asetelmiaan Malkan ja Saariahon "
        "väri- ja äänimaailmaan.</p><p>Amos Rex<br>10.6.-30.8. </p><p>ma, "
        "pe klo 11-18<br>ke, to klo 11-20<br>la, su klo 11-17</p><p>Sisäänpääsy "
        "5-15€, alle 18-vuotiaille vapaa pääsy</p>",
        "sv": "<p>Bildkonstnären Raija Malka och kompositören Kaija Saariaho fyller "
        "Amos Rex utställningsutrymme på ett nytt och experimentellt sätt nästa "
        "sommaren. Deras verk är på en och samma gång måleriskt, rumsligt och "
        "musikaliskt. </p><p>Utställningstiteln, Blick, syftar på "
        "bildkonstnären Wassily Kandinskys dikt från 1912. Texten ingår i Kaija "
        "Saariahos ljuder i utställningen. De två konstnärernas blickar möts i "
        "det tredimensionella utställningsutrymmet.</p><p>Utställningen utgör "
        "en sinnlig helhet som lockar besökare att dröja kvar. De kan bidra "
        "till Malkas och Saariahos färg- och ljudvärld med sina egna "
        "byggstenar.</p><p>Amos Rex<br>10.6.-30.8. </p><p>må, fre kl "
        "11-18<br>ons, to kl 11-20<br>lö, sö kl 11-17</p><p>Inträde 5-15€, "
        "under 18 år fritt inträde</p>",
        "en": "<p>Visual artist Raija Malka and composer Kaija Saariaho will take "
        "over Amos Rex’s exhibition space in a new and experiential way next "
        "summer. The work is painterly, spatial and musical all at once, "
        "offering visitors an opportunity to shape the space with their own "
        "creativity.</p><p>The exhibition title, Blick (Gaze), is a reference "
        "to visual artist Wassily Kandinsky’s poem from 1912 that is included "
        "in the soundscape by Kaija Saariaho. The gazes of the two artists are "
        "brought together in a three-dimensional space.</p><p>The exhibition is "
        "a multisensory experience that invites people to stay. In a world made "
        "up of the colours and sounds of Malka and Saariaho, visitors can build "
        "their own arrangements.</p><p>Amos Rex<br>10.6.-30.8. </p><p>Mon, "
        "Fri 11.00-18.00<br>Wed, Thu 11.00-20.00<br>Sat, "
        "Sun 11.00-17.00</p><p>Admission fee 5-15€, under 18 yrs free entry</p>",
    },
    "provider_contact_info": None,
    "@id": "https://api.hel.fi/linkedevents/v1/event/helsinki:afxp6tv4xa/",
    "@context": "http://schema.org",
    "@type": "Event/LinkedEvent",
}

PLACES_DATA = {
    "meta": {
        "count": 1346,
        "next": "https://api.hel.fi/linkedevents/v1/place/?page=2&page_size=2"
        "&show_all_places=",
        "previous": None,
    },
    "data": [
        {
            "id": "tprek:15417",
            "divisions": [
                {
                    "type": "muni",
                    "ocd_id": "ocd-division/country:fi/kunta:espoo",
                    "municipality": None,
                    "name": {"fi": "Espoo", "sv": "Esbo"},
                }
            ],
            "created_time": None,
            "last_modified_time": "2020-04-25T05:09:10.712132Z",
            "custom_data": None,
            "email": "sellonkirjasto@espoo.fi",
            "contact_type": None,
            "address_region": None,
            "postal_code": "02600",
            "post_office_box_num": None,
            "address_country": None,
            "deleted": False,
            "n_events": 27264,
            "image": 54259,
            "data_source": "tprek",
            "publisher": "ahjo:u021600",
            "parent": None,
            "replaced_by": None,
            "position": {"type": "Point", "coordinates": [24.80992, 60.21748]},
            "telephone": {"fi": "+358 9 8165 7603"},
            "street_address": {
                "fi": "Leppävaarankatu 9",
                "sv": "Albergagatan 9",
                "en": "Leppävaarankatu 9",
            },
            "info_url": {
                "fi": "http://www.helmet.fi/sello",
                "sv": "http://www.helmet.fi/sellobiblioteket",
                "en": "http://www.helmet.fi/sellolibrary",
            },
            "name": {
                "fi": "Sellon kirjasto",
                "sv": "Sellobiblioteket",
                "en": "Sello Library",
            },
            "address_locality": {"fi": "Espoo", "sv": "Esbo", "en": "Espoo"},
            "description": None,
            "@id": "https://api.hel.fi/linkedevents/v1/place/tprek:15417/",
            "@context": "http://schema.org",
            "@type": "Place",
        },
        {
            "id": "tprek:15321",
            "divisions": [
                {
                    "type": "muni",
                    "ocd_id": "ocd-division/country:fi/kunta:espoo",
                    "municipality": None,
                    "name": {"fi": "Espoo", "sv": "Esbo"},
                }
            ],
            "created_time": None,
            "last_modified_time": "2019-09-19T14:10:59.747979Z",
            "custom_data": None,
            "email": "kirjasto.entresse@espoo.fi",
            "contact_type": None,
            "address_region": None,
            "postal_code": "02770",
            "post_office_box_num": None,
            "address_country": None,
            "deleted": False,
            "n_events": 7745,
            "image": 54251,
            "data_source": "tprek",
            "publisher": "ahjo:u021600",
            "parent": None,
            "replaced_by": None,
            "position": {"type": "Point", "coordinates": [24.657864, 60.203636]},
            "telephone": {"fi": "+358 9 8165 3776"},
            "street_address": {
                "fi": "Siltakatu 11",
                "sv": "Brogatan 11",
                "en": "Siltakatu 11",
            },
            "info_url": {
                "fi": "http://www.helmet.fi/entressenkirjasto",
                "sv": "http://www.helmet.fi/entressebibliotek",
                "en": "http://www.helmet.fi/entressebibliotek",
            },
            "name": {
                "fi": "Entressen kirjasto",
                "sv": "Entressebiblioteket",
                "en": "Entresse Library",
            },
            "address_locality": {"fi": "Espoo", "sv": "Esbo", "en": "Espoo"},
            "description": None,
            "@id": "https://api.hel.fi/linkedevents/v1/place/tprek:15321/",
            "@context": "http://schema.org",
            "@type": "Place",
        },
    ],
}

PLACE_DATA = {
    "id": "tprek:15417",
    "divisions": [
        {
            "type": "muni",
            "ocd_id": "ocd-division/country:fi/kunta:espoo",
            "municipality": None,
            "name": {"fi": "Espoo", "sv": "Esbo"},
        }
    ],
    "created_time": None,
    "last_modified_time": "2020-04-25T05:09:10.712132Z",
    "custom_data": None,
    "email": "sellonkirjasto@espoo.fi",
    "contact_type": None,
    "address_region": None,
    "postal_code": "02600",
    "post_office_box_num": None,
    "address_country": None,
    "deleted": False,
    "n_events": 27264,
    "image": 54259,
    "data_source": "tprek",
    "publisher": "ahjo:u021600",
    "parent": None,
    "replaced_by": None,
    "position": {"type": "Point", "coordinates": [24.80992, 60.21748]},
    "telephone": {"fi": "+358 9 8165 7603"},
    "street_address": {
        "fi": "Leppävaarankatu 9",
        "sv": "Albergagatan 9",
        "en": "Leppävaarankatu 9",
    },
    "info_url": {
        "fi": "http://www.helmet.fi/sello",
        "sv": "http://www.helmet.fi/sellobiblioteket",
        "en": "http://www.helmet.fi/sellolibrary",
    },
    "name": {"fi": "Sellon kirjasto", "sv": "Sellobiblioteket", "en": "Sello Library"},
    "address_locality": {"fi": "Espoo", "sv": "Esbo", "en": "Espoo"},
    "description": None,
    "@id": "https://api.hel.fi/linkedevents/v1/place/tprek:15417/",
    "@context": "http://schema.org",
    "@type": "Place",
}

KEYWORDS_DATA = {
    "meta": {
        "count": 1992,
        "next": "https://api.hel.fi/linkedevents/v1/keyword/?page=2&page_size=2",
        "previous": None,
    },
    "data": [
        {
            "id": "yso:p4354",
            "alt_labels": ["spädbarn", "lapset", "imeväisikäiset", "barn"],
            "created_time": "2014-06-23T11:37:27.705000Z",
            "last_modified_time": "2017-09-06T05:20:47.061426Z",
            "aggregate": False,
            "deprecated": False,
            "n_events": 54082,
            "image": None,
            "data_source": "yso",
            "publisher": "hy:kansalliskirjasto",
            "replaced_by": None,
            "name": {
                "fi": "lapset (ikäryhmät)",
                "sv": "barn (åldersgrupper)",
                "en": "children (age groups)",
            },
            "@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p4354/",
            "@context": "http://schema.org",
            "@type": "Keyword",
        },
        {
            "id": "yso:p4363",
            "alt_labels": [
                "ydinperheet",
                "perhe",
                "familjer (grupper)",
                "kärnfamiljer",
                "familj",
            ],
            "created_time": "2014-06-23T11:37:28.246000Z",
            "last_modified_time": "2019-05-11T04:20:04.577893Z",
            "aggregate": False,
            "deprecated": False,
            "n_events": 29262,
            "image": None,
            "data_source": "yso",
            "publisher": "hy:kansalliskirjasto",
            "replaced_by": None,
            "name": {"fi": "perheet", "sv": "familjer", "en": "families"},
            "@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p4363/",
            "@context": "http://schema.org",
            "@type": "Keyword",
        },
    ],
}

KEYWORD_DATA = {
    "id": "yso:p4354",
    "alt_labels": ["spädbarn", "lapset", "imeväisikäiset", "barn"],
    "created_time": "2014-06-23T11:37:27.705000Z",
    "last_modified_time": "2017-09-06T05:20:47.061426Z",
    "aggregate": False,
    "deprecated": False,
    "n_events": 54082,
    "image": None,
    "data_source": "yso",
    "publisher": "hy:kansalliskirjasto",
    "replaced_by": None,
    "name": {
        "fi": "lapset (ikäryhmät)",
        "sv": "barn (åldersgrupper)",
        "en": "children (age groups)",
    },
    "@id": "https://api.hel.fi/linkedevents/v1/keyword/yso:p4354/",
    "@context": "http://schema.org",
    "@type": "Keyword",
}

CREATED_EVENT_DATA = {
    "id": "qq:afy6aghr2y",
    "location": {"@id": "http://localhost:8080/v1/place/tprek:9972/"},
    "keywords": [{"@id": "http://localhost:8080/v1/keyword/yso:p9999/"}],
    "super_event": None,
    "event_status": "EventScheduled",
    "publication_status": "public",
    "external_links": [],
    "offers": [
        {
            "is_free": False,
            "price": {"en": "testing", "fi": "testaus", "sv": "testning"},
            "description": {"en": "testing", "fi": "testaus", "sv": "testning"},
            "info_url": {
                "en": "http://localhost",
                "fi": "http://localhost",
                "sv": "http://localhost",
            },
        }
    ],
    "data_source": "qq",
    "publisher": "ahjo:00001",
    "sub_events": [],
    "images": [],
    "videos": [],
    "in_language": [],
    "audience": [],
    "created_time": "2020-05-04T14:31:03.398784Z",
    "last_modified_time": "2020-05-04T14:31:03.398831Z",
    "date_published": None,
    "start_time": "2020-05-05",
    "end_time": None,
    "maximum_attendee_capacity": None,
    "remaining_attendee_capacity": None,
    "minimum_attendee_capacity": None,
    "enrolment_start_time": None,
    "enrolment_end_time": None,
    "created_by": "API key from data source qq",
    "last_modified_by": "API key from data source qq",
    "custom_data": None,
    "audience_min_age": None,
    "audience_max_age": None,
    "super_event_type": None,
    "deleted": False,
    "replaced_by": None,
    "description": {"en": "desc en", "fi": "desc", "sv": "desc sv"},
    "info_url": None,
    "provider_contact_info": None,
    "name": {"fi": "testaus"},
    "location_extra_info": None,
    "provider": None,
    "short_description": {
        "en": "short desc en",
        "fi": "short desc",
        "sv": "short desc sv",
    },
    "@id": "http://localhost:8080/v1/event/qq:afy6aghr2y/",
    "@context": "http://schema.org",
    "@type": "Event/LinkedEvent",
}

UPDATE_EVENT_DATA = {
    "id": "qq:afy6aghr2y",
    "location": {"@id": "http://localhost:8080/v1/place/tprek:9972/"},
    "keywords": [{"@id": "http://localhost:8080/v1/keyword/yso:p9999/"}],
    "super_event": None,
    "event_status": "EventScheduled",
    "publication_status": "public",
    "external_links": [],
    "offers": [
        {
            "is_free": False,
            "price": {"en": "testing", "fi": "testaus", "sv": "testning"},
            "description": {"en": "testing", "fi": "testaus", "sv": "testning"},
            "info_url": {
                "en": "http://localhost",
                "fi": "http://localhost",
                "sv": "http://localhost",
            },
        }
    ],
    "data_source": "qq",
    "publisher": "ahjo:00001",
    "sub_events": [],
    "images": [],
    "videos": [],
    "in_language": [],
    "audience": [],
    "created_time": "2020-05-04T14:31:03.398784Z",
    "last_modified_time": "2020-05-04T14:31:03.398831Z",
    "date_published": None,
    "start_time": "2020-05-07",
    "end_time": None,
    "created_by": "API key from data source qq",
    "last_modified_by": "API key from data source qq",
    "custom_data": None,
    "audience_min_age": None,
    "audience_max_age": None,
    "super_event_type": None,
    "deleted": False,
    "replaced_by": None,
    "description": {"en": "desc en", "fi": "desc", "sv": "desc sv"},
    "info_url": None,
    "provider_contact_info": None,
    "name": {"fi": "testaus"},
    "location_extra_info": None,
    "provider": None,
    "short_description": {
        "en": "short desc en",
        "fi": "short desc",
        "sv": "short desc sv",
    },
    "@id": "http://localhost:8080/v1/event/qq:afy6aghr2y/",
    "@context": "http://schema.org",
    "@type": "Event/LinkedEvent",
}

UNPUBLISH_EVENT_DATA = {**UPDATE_EVENT_DATA, **{"publication_status": "draft"}}

IMAGES_DATA = {
    "meta": {
        "count": 64258,
        "next": "https://api.hel.fi/linkedevents/v1/image/?page=2",
        "previous": None,
    },
    "data": [
        {
            "id": 64390,
            "license": "event_only",
            "created_time": "2020-05-19T09:18:51.902275Z",
            "last_modified_time": "2020-05-19T09:18:51.902297Z",
            "name": "Tuohtumus",
            "url": "https://api.hel.fi/linkedevents/media/images"
            "/49776780903_bf54fd7b90_o.jpg",
            "cropping": "0,478,1920,2399",
            "photographer_name": "Suomen Kansallisteatteri (c) Katri Naukkarinen",
            "alt_text": "Kaksi naista istuu tien laidassa",
            "data_source": "helsinki",
            "publisher": "ytj:0586977-6",
            "@id": "https://api.hel.fi/linkedevents/v1/image/64390/",
            "@context": "http://schema.org",
            "@type": "ImageObject",
        },
        {
            "id": 64389,
            "license": "event_only",
            "created_time": "2020-05-19T08:13:34.072354Z",
            "last_modified_time": "2020-05-19T08:13:34.072380Z",
            "name": "",
            "url": "http://www.vuotalo.fi/instancedata/prime_product_resurssivaraus"
            "/kulke/embeds/EventPic_671268.jpg",
            "cropping": "",
            "photographer_name": None,
            "alt_text": None,
            "data_source": "kulke",
            "publisher": "ahjo:u4804001050",
            "@id": "https://api.hel.fi/linkedevents/v1/image/64389/",
            "@context": "http://schema.org",
            "@type": "ImageObject",
        },
    ],
}

IMAGE_DATA = {
    "id": 64390,
    "license": "event_only",
    "created_time": "2020-05-19T09:18:51.902275Z",
    "last_modified_time": "2020-05-19T09:18:51.902297Z",
    "name": "Tuohtumus",
    "url": "https://api.hel.fi/linkedevents/media/images"
    "/49776780903_bf54fd7b90_o.jpg",
    "cropping": "0,478,1920,2399",
    "photographer_name": "Suomen Kansallisteatteri (c) Katri Naukkarinen",
    "alt_text": "Kaksi naista istuu tien laidassa",
    "data_source": "helsinki",
    "publisher": "ytj:0586977-6",
    "@id": "https://api.hel.fi/linkedevents/v1/image/64390/",
    "@context": "http://schema.org",
    "@type": "ImageObject",
}

RECAPTCHA_DATA = {
    "success": True,
    "challenge_ts": "2020-09-09",
}

KEYWORD_SET_DATA = {
    "id": "kultus:categories",
    "keywords": [
        {
            "id": "helfi:12",
            "alt_labels": ["vändagen", "Valentindagen"],
            "created_time": "2020-05-04T08:51:38.338194Z",
            "last_modified_time": "2020-05-04T08:51:38.338221Z",
            "aggregate": False,
            "deprecated": False,
            "n_events": 0,
            "image": None,
            "data_source": "yso",
            "publisher": "hy:kansalliskirjasto",
            "replaced_by": None,
            "name": {
                "en": "Valentine's Day",
                "sv": "alla hjärtans dag",
                "fi": "ystävänpäivä",
            },
            "@id": "http://localhost:8080/v1/keyword/yso:p27033/",
            "@context": "http://schema.org",
            "@type": "Keyword",
        }
    ],
    "usage": "any",
    "created_time": "2020-11-02T13:58:41.872984Z",
    "last_modified_time": "2020-11-02T13:58:41.873016Z",
    "image": None,
    "data_source": "qq",
    "organization": None,
    "name": {"en": "Kultus Categories"},
    "@id": "http://localhost:8080/v1/keyword_set/qq:kultus:categories/",
    "@context": "http://schema.org",
    "@type": "KeywordSet",
}

POPULAR_KEYWORD_SET_DATA = {
    "id": "kultus:categories",
    "keywords": [
        {
            "id": "yso:p84",
            "alt_labels": ["skolning"],
            "created_time": "2014-06-23T11:37:29.677000Z",
            "last_modified_time": "2017-09-06T05:20:41.555750Z",
            "aggregate": False,
            "deprecated": False,
            "has_upcoming_events": True,
            "n_events": 200,
            "image": None,
            "data_source": "yso",
            "publisher": "hy:kansalliskirjasto",
            "replaced_by": None,
            "name": {
                "fi": "koulutus",
                "sv": "utbildning",
                "en": "education and training",
            },
            "@id": "http://localhost:8080/v1/keyword/yso:p84/",
            "@context": "http://schema.org",
            "@type": "Keyword",
        },
        {
            "id": "helfi:12",
            "alt_labels": ["vändagen", "Valentindagen"],
            "created_time": "2020-05-04T08:51:38.338194Z",
            "last_modified_time": "2020-05-04T08:51:38.338221Z",
            "aggregate": False,
            "deprecated": False,
            "has_upcoming_events": False,
            "n_events": 0,
            "image": None,
            "data_source": "yso",
            "publisher": "hy:kansalliskirjasto",
            "replaced_by": None,
            "name": {
                "en": "Valentine's Day",
                "sv": "alla hjärtans dag",
                "fi": "ystävänpäivä",
            },
            "@id": "http://localhost:8080/v1/keyword/yso:p27033/",
            "@context": "http://schema.org",
            "@type": "Keyword",
        },
    ],
    "usage": "any",
    "created_time": "2020-11-02T13:58:41.872984Z",
    "last_modified_time": "2020-11-02T13:58:41.873016Z",
    "image": None,
    "data_source": "qq",
    "organization": None,
    "name": {"en": "Kultus Categories"},
    "@id": "http://localhost:8080/v1/keyword_set/qq:kultus:categories/",
    "@context": "http://schema.org",
    "@type": "KeywordSet",
}
