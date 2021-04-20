from contextlib import contextmanager
from datetime import datetime
import json
import os
import sqlite3
from sys import stderr
from typing import Any
from typing import Iterator
from typing import Optional

import appdirs  # type: ignore [import]
import click
import click_config_file  # type: ignore [import]
from foursquare import Foursquare  # type: ignore [import]
import icalendar  # type: ignore [import]
import pytz
import yaml

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


def yaml_config_option():
    path = os.path.join(appdirs.user_config_dir(appname=__package__), 'config.yaml')

    def provider(file_path, _cmd_name):
        if os.path.isfile(file_path):
            with open(file_path) as f:
                return yaml.safe_load(f)
        else:
            return {}

    return click_config_file.configuration_option(implicit=False, default=path, show_default=True, provider=provider)


@click.command(context_settings={'max_content_width': 120})
@click.option(
    '-v', '--verbose', count=True,
    help="Be more verbose")
@click.option(
    '--sync/--no-sync', 'do_sync', default=True, show_default=True,
    help="Sync again or just use local database?")
@click.option(
    '--access-token', type=str, envvar='FOURSQUARE_TOKEN',
    help="Foursquare oauth2 access token")
@click.option(
    '--database', 'db_path', type=click.Path(writable=True), default='checkins.sqlite', show_default=True,
    help="SQLite database file")
@click.option(
    '-e', '--emoji/--no-emoji', default=False, show_default=True,
    help="Prefix summary with venue category as emoji")
@click.option(
    '-o', '--output', type=click.File('wb'), default='-',
    help="Output file")
@yaml_config_option()
def main(verbose: bool, do_sync: bool, access_token: str, db_path: str, emoji: bool, output) -> None:
    """Sync Foursquare Swarm check-ins to local sqlite DB and generate iCalendar"""
    with database(db_path) as db:
        if do_sync:
            if not access_token:
                raise RuntimeError("--access-token or FOURSQUARE_TOKEN required")

            sync(db=db, access_token=access_token, verbose=verbose)

        output.write(ical(db=db, emojis=(Emojis() if emoji else None)))
