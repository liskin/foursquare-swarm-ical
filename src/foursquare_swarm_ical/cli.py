from pathlib import Path
import re
from typing import BinaryIO
from typing import Optional

import click
import platformdirs

from . import config_file
from . import db
from . import ical
from .emoji import Emojis


class SizeType(click.ParamType):
    _regex = re.compile(r"(\d+)\s*([KM]?)")
    _suffixes = {'': 1, 'K': 1_000, 'M': 1_000_000}

    name = "size"

    def convert(self, value, param, ctx):
        if isinstance(value, int):
            return value
        elif m := self._regex.fullmatch(value):
            return int(m[1]) * self._suffixes[m[2]]
        else:
            self.fail(f"{value!r} is not a valid size", param, ctx)


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
    '--database', type=click.Path(path_type=Path, writable=True),  # type: ignore [type-var] # debian typeshed compat
    default=platformdirs.user_data_path(appname=__package__) / 'checkins.sqlite',
    show_default=True,
    help="SQLite database file")
@click.option(
    '--emoji/--no-emoji', '-e', default=True, show_default=True,
    help="Prefix summary with venue category as emoji")
@click.option(
    '-o', '--output', type=click.File('wb'), default='-',
    help="Output file")
@click.option(
    '-m', '--max-size', type=SizeType(),
    help="Maximum size of the output file in bytes (accepts K and M suffixes as well)")
@config_file.yaml_config_option()
@config_file.yaml_config_sample_option()
def cli(
    verbose: bool,
    sync: bool,
    access_token: str,
    database: Path,
    emoji: bool,
    output: BinaryIO,
    max_size: Optional[int]
) -> None:
    """Sync Foursquare Swarm check-ins to local sqlite DB and generate iCalendar"""
    with db.database(database) as db_conn:
        if sync:
            if not access_token:
                raise RuntimeError("--access-token or FOURSQUARE_TOKEN required")

            db.sync(db=db_conn, access_token=access_token, verbose=verbose)

        output.write(ical.ical(
            checkins=db.checkins(db=db_conn),
            emojis=(Emojis() if emoji else None),
            max_size=max_size
        ))
