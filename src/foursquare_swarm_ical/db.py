from contextlib import contextmanager
from datetime import datetime
import json
import logging
from os import PathLike
import sqlite3
from typing import Any
from typing import Iterator
from typing import Union

from foursquare import Foursquare  # type: ignore [import]


@contextmanager
def database(filename: Union[str, PathLike]) -> Iterator[sqlite3.Connection]:
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


def checkins(db: sqlite3.Connection) -> Iterator[Any]:
    for checkin in db.execute("SELECT data FROM checkins ORDER BY createdAt DESC"):
        yield json.loads(checkin['data'])


def fetch_checkins(access_token: str) -> Iterator[Any]:
    client = Foursquare(access_token=access_token)
    return client.users.all_checkins()


def sync(db: sqlite3.Connection, access_token: str) -> None:
    with db:  # transaction
        for checkin in fetch_checkins(access_token=access_token):
            tup = (checkin['id'], int(checkin['createdAt']), json.dumps(checkin))
            try:
                db.execute(("INSERT INTO checkins (id, createdAt, data) VALUES (?, ?, ?)"), tup)
            except sqlite3.IntegrityError:
                break

            logging.debug(f"checkin {checkin['id']} at {datetime.fromtimestamp(checkin['createdAt'])}")
