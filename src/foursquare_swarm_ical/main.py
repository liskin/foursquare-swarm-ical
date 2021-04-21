import os

import appdirs  # type: ignore [import]
import click

from . import config_file
from . import db
from . import ical
from .emoji import Emojis


@click.command(context_settings={'max_content_width': 120})
@click.option(
    '-v', '--verbose', count=True,
    help="Be more verbose")
@click.option(
    '--sync/--no-sync', default=True, show_default=True,
    help="Sync again or just use local database?")
@click.option(
    '--access-token', type=str, envvar='FOURSQUARE_TOKEN', show_envvar=True,
    help="Foursquare oauth2 access token")
@click.option(
    '--database', type=click.Path(writable=True),
    default=os.path.join(appdirs.user_data_dir(appname=__package__), 'checkins.sqlite'), show_default=True,
    help="SQLite database file")
@click.option(
    '-e', '--emoji/--no-emoji', default=False, show_default=True,
    help="Prefix summary with venue category as emoji")
@click.option(
    '-o', '--output', type=click.File('wb'), default='-',
    help="Output file")
@config_file.yaml_config_option()
def main(verbose: bool, sync: bool, access_token: str, database: str, emoji: bool, output) -> None:
    """Sync Foursquare Swarm check-ins to local sqlite DB and generate iCalendar"""
    with db.database(database) as db_conn:
        if sync:
            if not access_token:
                raise RuntimeError("--access-token or FOURSQUARE_TOKEN required")

            db.sync(db=db_conn, access_token=access_token, verbose=verbose)

        output.write(ical.ical(db=db_conn, emojis=(Emojis() if emoji else None)))
