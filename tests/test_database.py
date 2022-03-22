import pytest

from ansys.mapdl.core.database import MapdlDb
from ansys.mapdl.core.misc import random_string


@pytest.fixture(scope="module")
def check_supports_database(mapdl):
    if mapdl._server_version < (0, 4, 1):  # 2021R2
        pytest.skip("Database service not supported")


@pytest.fixture(scope="session")
def db(mapdl):
    return mapdl.db


@pytest.fixture(scope="session")
def gen_block(mapdl):
    """Generate nodes and elements in a simple block."""
    mapdl.clear()
    mapdl.prep7()
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, 186)
    mapdl.esize(0.25)
    mapdl.vmesh("ALL")


@pytest.fixture(scope="session")
def nodes(gen_block, db):
    return db.nodes


@pytest.fixture(scope="session")
def elems(db):
    return db.elems


@pytest.mark.usefixtures("check_supports_database")
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


@pytest.mark.usefixtures("check_supports_database")
def test_database_repr(db):
    assert db._channel_str in str(db)


@pytest.mark.usefixtures("check_supports_database")
def test_save(db):
    with pytest.raises(ValueError, match="Option must be one of the"):
        db.save("file.db", "not_an_option")

    filename = f"{random_string()}.db"
    db.save(filename)

    assert filename in db._mapdl.list_files()
    output = db.load(filename)
    assert f"RESUME ANSYS" in output


@pytest.mark.usefixtures("check_supports_database")
def test_clear(db):
    db._mapdl.prep7()
    db._mapdl.k(1, 1, 1, 1)
    db.clear()
    assert db._mapdl.geometry.n_keypoint == 0


@pytest.mark.usefixtures("check_supports_database")
def test_nodes_repr(nodes):
    breakpoint()
    # nodes
