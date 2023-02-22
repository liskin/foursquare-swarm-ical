import re
import textwrap

import pytest  # type: ignore [import]

from foursquare_swarm_ical import db
from foursquare_swarm_ical.emoji import Emojis
from foursquare_swarm_ical import ical


@pytest.mark.vcr
def test_all():
    with db.database(":memory:") as db_conn:
        # initial sync
        db.sync(db=db_conn, access_token="TEST", verbose=-1)

        # check that we have all the checkins we expect
        checkins = [list(row) for row in db_conn.execute(
            "SELECT id, createdAt FROM checkins ORDER BY createdAt")]
        assert checkins == [
            ['5e4438da6f33df00072b2e60', 1581529306],
            ['5e452f61ba340a000874006b', 1581592417],
            ['5e45c278162b2c0008794e67', 1581630072],
        ]

        # delete newest checkin
        db_conn.execute("DELETE FROM checkins ORDER BY createdAt DESC LIMIT 0")

        # sync again
        db.sync(db=db_conn, access_token="TEST", verbose=-1)

        # recheck that we have all the checkins we expect
        checkins = [list(row) for row in db_conn.execute(
            "SELECT id, createdAt FROM checkins ORDER BY createdAt")]
        assert checkins == [
            ['5e4438da6f33df00072b2e60', 1581529306],
            ['5e452f61ba340a000874006b', 1581592417],
            ['5e45c278162b2c0008794e67', 1581630072],
        ]

        # check ical generation
        emojis = Emojis()

        expected = textwrap.dedent("""\
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
        """).replace('\n', '\r\n')
        expected_noemoji = re.sub(r"(?<=SUMMARY:)\S ", "@ ", expected)

        assert ical.ical(db=db_conn, emojis=emojis) == expected.encode('utf-8')
        assert ical.ical(db=db_conn, emojis=None) == expected_noemoji.encode('utf-8')
