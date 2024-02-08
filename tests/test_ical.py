import re
import textwrap

from foursquare_swarm_ical.emoji import Emojis
from foursquare_swarm_ical.ical import ical

checkins = [
    {
        "id": "5e4438da6f33df00072b2e60",
        "createdAt": 1581529306,
        "type": "checkin",
        "timeZoneOffset": 60,
        "venue": {
            "id": "4b969619f964a520a7d634e3",
            "name": "Pivnice Pegas",
            "contact": {},
            "location": {
                "address": "Jiráskova 44",
                "lat": 49.203087013053825,
                "lng": 16.595776878926344,
                "labeledLatLngs": [
                    {
                        "label": "display",
                        "lat": 49.203087013053825,
                        "lng": 16.595776878926344,
                    }
                ],
                "postalCode": "602 00",
                "cc": "CZ",
                "city": "Brno",
                "state": "South Moravian Region",
                "country": "Czech Republic",
                "formattedAddress": [
                    "Jiráskova 44",
                    "602 00 Brno",
                    "Česká republika",
                ],
            },
            "categories": [
                {
                    "id": "4bf58dd8d48988d11b941735",
                    "name": "Pub",
                    "pluralName": "Pubs",
                    "shortName": "Pub",
                    "icon": {
                        "prefix": "https://ss3.4sqi.net/img/categories_v2/nightlife/pub_",
                        "suffix": ".png",
                    },
                    "primary": True,
                }
            ],
            "verified": False,
            "stats": {"tipCount": 22, "usersCount": 519, "checkinsCount": 1023},
            "allowMenuUrlEdit": True,
            "beenHere": {"lastCheckinExpiredAt": 0},
        },
    },
    {
        "id": "5e452f61ba340a000874006b",
        "createdAt": 1581592417,
        "type": "checkin",
        "timeZoneOffset": 60,
        "venue": {
            "id": "4d85e88b8de9721e70d44f51",
            "name": "Zahrada Ambrosia",
            "contact": {
                "phone": "734176934",
                "formattedPhone": "734 176 934",
                "facebook": "151905601526246",
                "facebookName": "Záhrada café therapy",
            },
            "location": {
                "address": "Údolní 599/37",
                "lat": 49.1980983508588,
                "lng": 16.597204121337384,
                "labeledLatLngs": [
                    {
                        "label": "display",
                        "lat": 49.1980983508588,
                        "lng": 16.597204121337384,
                    }
                ],
                "postalCode": "602 00",
                "cc": "CZ",
                "city": "Brno",
                "state": "South Moravian Region",
                "country": "Czech Republic",
                "formattedAddress": [
                    "Údolní 599/37",
                    "602 00 Brno",
                    "Česká republika",
                ],
            },
            "categories": [
                {
                    "id": "4bf58dd8d48988d1d3941735",
                    "name": "Vegetarian / Vegan Restaurant",
                    "pluralName": "Vegetarian / Vegan Restaurants",
                    "shortName": "Vegetarian / Vegan",
                    "icon": {
                        "prefix": "https://ss3.4sqi.net/img/categories_v2/food/vegetarian_",
                        "suffix": ".png",
                    },
                    "primary": True,
                }
            ],
            "verified": False,
            "stats": {"tipCount": 39, "usersCount": 787, "checkinsCount": 3183},
            "allowMenuUrlEdit": True,
            "beenHere": {"lastCheckinExpiredAt": 0},
        },
    },
    {
        "id": "5e45c278162b2c0008794e67",
        "createdAt": 1581630072,
        "type": "checkin",
        "timeZoneOffset": 60,
        "venue": {
            "id": "5ca22fa1f4b525002cc391b4",
            "name": "U Vašinů",
            "contact": {
                "phone": "774215243",
                "formattedPhone": "774 215 243",
                "facebook": "1431852240457668",
                "facebookUsername": "uvasinu",
                "facebookName": "U Vašinů - craft beer & food",
            },
            "location": {
                "address": "Kotlářská 907/41",
                "lat": 49.207467399173076,
                "lng": 16.60221666114012,
                "labeledLatLngs": [
                    {
                        "label": "display",
                        "lat": 49.207467399173076,
                        "lng": 16.60221666114012,
                    }
                ],
                "postalCode": "602 00",
                "cc": "CZ",
                "neighborhood": "Veveří",
                "city": "Brno",
                "state": "South Moravian Region",
                "country": "Czech Republic",
                "formattedAddress": [
                    "Kotlářská 907/41",
                    "602 00 Brno",
                    "Česká republika",
                ],
            },
            "categories": [
                {
                    "id": "56aa371ce4b08b9a8d57356c",
                    "name": "Beer Bar",
                    "pluralName": "Beer Bars",
                    "shortName": "Beer Bar",
                    "icon": {
                        "prefix": "https://ss3.4sqi.net/img/categories_v2/nightlife/pub_",
                        "suffix": ".png",
                    },
                    "primary": True,
                }
            ],
            "verified": False,
            "stats": {"tipCount": 0, "usersCount": 42, "checkinsCount": 91},
            "allowMenuUrlEdit": True,
            "beenHere": {"lastCheckinExpiredAt": 0},
        },
    },
]


def test_ical():
    expected = textwrap.dedent(
        """\
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:foursquare-swarm-ical
        BEGIN:VEVENT
        SUMMARY:🍺 Pivnice Pegas
        DTSTART:20200212T174146Z
        DTEND:20200212T174146Z
        UID:5e4438da6f33df00072b2e60@foursquare.com
        GEO:49.203087013053825;16.595776878926344
        LOCATION:Jiráskova 44\\, 602 00 Brno\\, Česká republika
        URL:https://www.swarmapp.com/self/checkin/5e4438da6f33df00072b2e60
        END:VEVENT
        BEGIN:VEVENT
        SUMMARY:🍴 Zahrada Ambrosia
        DTSTART:20200213T111337Z
        DTEND:20200213T111337Z
        UID:5e452f61ba340a000874006b@foursquare.com
        GEO:49.1980983508588;16.597204121337384
        LOCATION:Údolní 599/37\\, 602 00 Brno\\, Česká republika
        URL:https://www.swarmapp.com/self/checkin/5e452f61ba340a000874006b
        END:VEVENT
        BEGIN:VEVENT
        SUMMARY:🍺 U Vašinů
        DTSTART:20200213T214112Z
        DTEND:20200213T214112Z
        UID:5e45c278162b2c0008794e67@foursquare.com
        GEO:49.207467399173076;16.60221666114012
        LOCATION:Kotlářská 907/41\\, 602 00 Brno\\, Česká republika
        URL:https://www.swarmapp.com/self/checkin/5e45c278162b2c0008794e67
        END:VEVENT
        END:VCALENDAR
    """).replace("\n", "\r\n")
    expected_noemoji = re.sub(r"(?<=SUMMARY:)\S ", "@ ", expected)

    assert ical(checkins=checkins, emojis=Emojis()) == expected.encode("utf-8")
    assert ical(checkins=checkins, emojis=None) == expected_noemoji.encode("utf-8")


def test_ical_max_size():
    empty_size = len(ical([]))
    full_size = len(ical(checkins))
    assert empty_size < full_size
    assert len(ical(checkins, max_size=full_size)) == full_size
    assert empty_size < len(ical(checkins, max_size=full_size - 1)) < full_size
