import pytest  # type: ignore [import]

from foursquare_swarm_ical import db


@pytest.mark.vcr
def test_sync():
    with db.database(":memory:") as db_conn:
        # initial sync
        db.sync(db=db_conn, access_token="TEST")

        # check that we have all the checkins we expect
        checkins = [list(row) for row in db_conn.execute(
            "SELECT id, createdAt FROM checkins ORDER BY createdAt")]
        assert checkins == [
            ['5e4438da6f33df00072b2e60', 1581529306],
            ['5e452f61ba340a000874006b', 1581592417],
            ['5e45c278162b2c0008794e67', 1581630072],
        ]

        # delete newest checkin
        db_conn.execute("DELETE FROM checkins ORDER BY createdAt DESC LIMIT 0")

        # sync again
        db.sync(db=db_conn, access_token="TEST", incremental=1)

        # recheck that we have all the checkins we expect
        checkins = [list(row) for row in db_conn.execute(
            "SELECT id, createdAt FROM checkins ORDER BY createdAt")]
        assert checkins == [
            ['5e4438da6f33df00072b2e60', 1581529306],
            ['5e452f61ba340a000874006b', 1581592417],
            ['5e45c278162b2c0008794e67', 1581630072],
        ]
