from datetime import datetime
import json
import sqlite3
from typing import Optional

import icalendar  # type: ignore [import]
import pytz

from .emoji import Emojis


def ical(db: sqlite3.Connection, emojis: Optional[Emojis]) -> bytes:
    cal = icalendar.Calendar()
    cal.add('prodid', "foursquare-swarm-ical")
    cal.add('version', "2.0")

    for checkin in db.execute("SELECT data FROM checkins ORDER BY createdAt"):
        checkin = json.loads(checkin['data'])

        prefix = emojis.get_emoji_for_venue(checkin['venue']) if emojis else "@"

        location = checkin['venue']['location']
        address = ', '.join(location.get('formattedAddress', []))
        if not address:
            address = str(location['lat']) + "," + str(location['lng'])

        ev = icalendar.Event()
        ev.add('uid', checkin['id'] + "@foursquare.com")
        ev.add('url', "https://www.swarmapp.com/self/checkin/" + checkin['id'])
        ev.add('summary', prefix + " " + checkin['venue']['name'])
        ev.add('location', address)
        ev.add('dtstart', datetime.fromtimestamp(checkin['createdAt'], pytz.utc))
        ev.add('dtend', datetime.fromtimestamp(checkin['createdAt'], pytz.utc))
        ev.add('geo', (location['lat'], location['lng']))
        cal.add_component(ev)

    return cal.to_ical()
