from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Iterable
from typing import Optional

import icalendar  # type: ignore [import]

from .emoji import Emojis


def ical(checkins: Iterable[Any], emojis: Optional[Emojis] = None, max_size: Optional[int] = None) -> bytes:
    cal = icalendar.Calendar()
    cal.add('prodid', "foursquare-swarm-ical")
    cal.add('version', "2.0")

    cal_size = len(cal.to_ical())

    for checkin in checkins:
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
        ev.add('dtstart', datetime.fromtimestamp(checkin['createdAt'], timezone.utc))
        ev.add('dtend', datetime.fromtimestamp(checkin['createdAt'], timezone.utc))
        ev.add('geo', (location['lat'], location['lng']))

        ev_size = len(ev.to_ical())
        if max_size is not None and cal_size + ev_size > max_size:
            break

        cal.add_component(ev)
        cal_size += ev_size

    return cal.to_ical()
