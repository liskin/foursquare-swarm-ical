from contextlib import contextmanager
from datetime import datetime
from foursquare import Foursquare  # type: ignore [import]
from sys import stderr, stdout
from typing import Iterator, Any
import argparse
import icalendar  # type: ignore [import]
import json
import os
import pytz
import sqlite3


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


def ical(db: sqlite3.Connection) -> bytes:
    cal = icalendar.Calendar()
    cal.add('prodid', "foursquare-swarm-ical")
    cal.add('version', "2.0")

    for checkin in db.execute("SELECT data FROM checkins ORDER BY createdAt"):
        checkin = json.loads(checkin['data'])

        ev = icalendar.Event()
        ev.add('uid', checkin['id'] + "@foursquare.com")
        ev.add('url', "https://www.swarmapp.com/self/checkin/" + checkin['id'])
        ev.add('summary', "@ " + checkin['venue']['name'])
        ev.add('description', "@ " + checkin['venue']['name'])
        ev.add('location', checkin['venue']['name'])
        ev.add('dtstart', datetime.fromtimestamp(checkin['createdAt'], pytz.utc))
        ev.add('dtend', datetime.fromtimestamp(checkin['createdAt'], pytz.utc))
        cal.add_component(ev)

    return cal.to_ical()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync Foursquare Swarm check-ins to local sqlite DB and generate iCalendar"
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
        '-v', '--verbose', action='count', default=0,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with database(args.database) as db:
        sync(db=db, access_token=args.access_token, verbose=args.verbose)
        stdout.buffer.write(ical(db=db))
