import textwrap

import pytest  # type: ignore [import]

from foursquare_swarm_ical.emoji import Emojis
from foursquare_swarm_ical import main


@pytest.mark.vcr
def test_main():
    with main.database(":memory:") as db:
        main.sync(db=db, access_token="TEST", verbose=0)

        checkins = [list(row) for row in db.execute(
            "SELECT id, createdAt FROM checkins ORDER BY createdAt")]
        assert checkins == [
            ['5e4438da6f33df00072b2e60', 1581529306],
            ['5e452f61ba340a000874006b', 1581592417],
            ['5e45c278162b2c0008794e67', 1581630072],
        ]

        emojis = Emojis()

        assert main.ical(db=db, emojis=emojis) == textwrap.dedent("""\
            BEGIN:VCALENDAR
            VERSION:2.0
            PRODID:foursquare-swarm-ical
            BEGIN:VEVENT
            SUMMARY:🍺 Pivnice Pegas
            DTSTART;VALUE=DATE-TIME:20200212T174146Z
            DTEND;VALUE=DATE-TIME:20200212T174146Z
            UID:5e4438da6f33df00072b2e60@foursquare.com
            GEO:49.203087013053825;16.595776878926344
            LOCATION:Jiráskova 44\\, 602 00 Brno\\, Česká republika
            URL:https://www.swarmapp.com/self/checkin/5e4438da6f33df00072b2e60
            END:VEVENT
            BEGIN:VEVENT
            SUMMARY:🍴 Zahrada Ambrosia
            DTSTART;VALUE=DATE-TIME:20200213T111337Z
            DTEND;VALUE=DATE-TIME:20200213T111337Z
            UID:5e452f61ba340a000874006b@foursquare.com
            GEO:49.1980983508588;16.597204121337384
            LOCATION:Údolní 599/37\\, 602 00 Brno\\, Česká republika
            URL:https://www.swarmapp.com/self/checkin/5e452f61ba340a000874006b
            END:VEVENT
            BEGIN:VEVENT
            SUMMARY:🍺 U Vašinů
            DTSTART;VALUE=DATE-TIME:20200213T214112Z
            DTEND;VALUE=DATE-TIME:20200213T214112Z
            UID:5e45c278162b2c0008794e67@foursquare.com
            GEO:49.207467399173076;16.60221666114012
            LOCATION:Kotlářská 907/41\\, 602 00 Brno\\, Česká republika
            URL:https://www.swarmapp.com/self/checkin/5e45c278162b2c0008794e67
            END:VEVENT
            END:VCALENDAR
        """).replace('\n', '\r\n').encode('utf-8')

        assert main.ical(db=db, emojis=None) == textwrap.dedent("""\
            BEGIN:VCALENDAR
            VERSION:2.0
            PRODID:foursquare-swarm-ical
            BEGIN:VEVENT
            SUMMARY:@ Pivnice Pegas
            DTSTART;VALUE=DATE-TIME:20200212T174146Z
            DTEND;VALUE=DATE-TIME:20200212T174146Z
            UID:5e4438da6f33df00072b2e60@foursquare.com
            GEO:49.203087013053825;16.595776878926344
            LOCATION:Jiráskova 44\\, 602 00 Brno\\, Česká republika
            URL:https://www.swarmapp.com/self/checkin/5e4438da6f33df00072b2e60
            END:VEVENT
            BEGIN:VEVENT
            SUMMARY:@ Zahrada Ambrosia
            DTSTART;VALUE=DATE-TIME:20200213T111337Z
            DTEND;VALUE=DATE-TIME:20200213T111337Z
            UID:5e452f61ba340a000874006b@foursquare.com
            GEO:49.1980983508588;16.597204121337384
            LOCATION:Údolní 599/37\\, 602 00 Brno\\, Česká republika
            URL:https://www.swarmapp.com/self/checkin/5e452f61ba340a000874006b
            END:VEVENT
            BEGIN:VEVENT
            SUMMARY:@ U Vašinů
            DTSTART;VALUE=DATE-TIME:20200213T214112Z
            DTEND;VALUE=DATE-TIME:20200213T214112Z
            UID:5e45c278162b2c0008794e67@foursquare.com
            GEO:49.207467399173076;16.60221666114012
            LOCATION:Kotlářská 907/41\\, 602 00 Brno\\, Česká republika
            URL:https://www.swarmapp.com/self/checkin/5e45c278162b2c0008794e67
            END:VEVENT
            END:VCALENDAR
        """).replace('\n', '\r\n').encode('utf-8')
