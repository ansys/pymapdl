import pytest

from ansys.mapdl.core.database import MapdlDb
from ansys.mapdl.core.misc import random_string


@pytest.fixture(scope="session")
def db(mapdl):
    return mapdl.db


@pytest.fixture(scope="session")
def nodes(db):
    return db.nodes


@pytest.fixture(scope="session")
def elems(db):
    return db.elems


def test_database_start_stop(mapdl):

    # verify it can be created twice
    mapdl.prep7()
    for _ in range(2):
        database = MapdlDb(mapdl)
        assert not database.active
        database.start()
        assert database.active
        database.stop()
        assert not database.active
        assert "not active" in str(database)
        assert database._channel is None

    with pytest.warns(UserWarning):
        database.stop()


def test_database_repr(db):
    assert db._channel_str in str(db)


def test_save(db):
    with pytest.raises(ValueError, match="Option must be one of the"):
        db.save("file.db", "not_an_option")

    filename = f"{random_string()}.db"
    db.save(filename)

    assert filename in db._mapdl.list_files()
    output = db.load(filename)
    assert f"RESUME ANSYS" in output


def test_clear(db):
    db._mapdl.prep7()
    db._mapdl.k(1, 1, 1, 1)
    db.clear()
    assert db._mapdl.geometry.n_keypoint == 0


def test_nodes_repr(nodes):
    pass
