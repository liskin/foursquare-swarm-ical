from contextlib import contextmanager
from datetime import datetime
import json
from os import PathLike
import sqlite3
from sys import stderr
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
