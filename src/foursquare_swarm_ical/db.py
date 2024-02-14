from contextlib import contextmanager
import json
import logging
from os import PathLike
import sqlite3
from typing import Any
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import Union

from foursquare import Foursquare  # type: ignore [import]


@contextmanager
def database(filename: Union[str, PathLike]) -> Iterator[sqlite3.Connection]:
    db = sqlite3.connect(filename, isolation_level=None)
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


def upsert_row(db: sqlite3.Connection, row: Mapping[str, Any]) -> None:
    keys = ', '.join(row.keys())
    placeholders = ', '.join('?' for k in row.keys())
    db.execute(
        f"INSERT OR REPLACE INTO checkins ({keys}) VALUES ({placeholders})",
        tuple(row.values())
    )


def upsert(db: sqlite3.Connection, rows: Iterable[Any], incremental: Union[bool, int] = False):
    if not isinstance(incremental, int):
        incremental = 10 if incremental else 0

    with db:  # transaction
        db.execute("BEGIN")

        old_ids = set(r['id'] for r in db.execute("SELECT id FROM checkins"))
        seen = 0
        new = 0
        deleted = 0

        for row in rows:
            logging.debug(f"checkins: {row['id']} {'seen' if row['id'] in old_ids else 'new'}")

            if row['id'] in old_ids:
                old_ids.discard(row['id'])

                seen += 1
                if incremental and seen > incremental:
                    break
            else:
                new += 1

            upsert_row(db, row)

        if not incremental:
            delete = ((i,) for i in old_ids)
            db.executemany("DELETE FROM checkins WHERE id = ?", delete)
            deleted += len(old_ids)

        logging.info(f"checkins upsert stats: {new} new, {seen} seen, {deleted} deleted")


def sync(db: sqlite3.Connection, access_token: str, incremental: bool = False) -> None:
    rows = (
        {'id': checkin['id'], 'createdAt': int(checkin['createdAt']), 'data': json.dumps(checkin)}
        for checkin in fetch_checkins(access_token=access_token)
    )
    upsert(db, rows, incremental=incremental)


def fetch_checkins(access_token: str) -> Iterator[Any]:
    client = Foursquare(access_token=access_token)
    return client.users.all_checkins()


def checkins(db: sqlite3.Connection) -> Iterator[Any]:
    for checkin in db.execute("SELECT data FROM checkins ORDER BY createdAt DESC"):
        yield json.loads(checkin['data'])
