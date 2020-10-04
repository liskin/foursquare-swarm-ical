import argparse
from contextlib import contextmanager
from datetime import datetime
import json
import os
import sqlite3
from sys import stderr
from sys import stdout
from typing import Any
from typing import Iterator
from typing import Optional

from foursquare import Foursquare  # type: ignore [import]
import icalendar  # type: ignore [import]
import pytz

from .emoji import Emojis


@contextmanager
def database(filename: str) -> Iterator[sqlite3.Connection]:
    db = sqlite3.connect(filename)
    db.row_factory = sqlite3.Row
    try:
        db.execute((
            "CREATE TABLE IF NOT EXISTS checkins"
            "( id TEXT PRIMARY KEY"
            ", createdAt NUMERIC"
            ", data TEXT"
            ")"
        ))
        yield db
    finally:
        db.close()


def checkins(access_token: str) -> Iterator[Any]:
    client = Foursquare(access_token=access_token)
    return client.users.all_checkins()


def sync(db: sqlite3.Connection, access_token: str, verbose: int) -> None:
    with db:  # transaction
        for checkin in checkins(access_token=access_token):
            tup = (checkin['id'], int(checkin['createdAt']), json.dumps(checkin))
            try:
                db.execute(("INSERT INTO checkins (id, createdAt, data) VALUES (?, ?, ?)"), tup)
            except sqlite3.IntegrityError:
                break

            if verbose > 0:
                print(datetime.fromtimestamp(checkin['createdAt']), file=stderr)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync Foursquare Swarm check-ins to local sqlite DB and generate iCalendar"
    )
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
    )
    parser.add_argument(
        '--no-sync', dest='sync', action='store_false',
        help="skip online sync, print ical from database only",
    )
    parser.add_argument(
        '--access-token', metavar="XXX", default=os.getenv('FOURSQUARE_TOKEN'),
        help="foursquare oauth2 access token (default: getenv('FOURSQUARE_TOKEN'))",
    )
    parser.add_argument(
        '--database', metavar="FILE", default="checkins.sqlite",
        help="sqlite database file (default: checkins.sqlite)",
    )
    parser.add_argument(
        '--emoji', action='store_true',
        help="prefix summary with venue category as emoji",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    emojis = Emojis() if args.emoji else None

    with database(args.database) as db:
        if args.sync:
            if not args.access_token:
                raise RuntimeError("--access-token or FOURSQUARE_TOKEN required")
            sync(db=db, access_token=args.access_token, verbose=args.verbose)

        stdout.buffer.write(ical(db=db, emojis=emojis))
