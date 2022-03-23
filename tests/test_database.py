import numpy as np
import pytest

from ansys.mapdl.core.database import DBDef, MapdlDb
from ansys.mapdl.core.misc import random_string


@pytest.fixture(scope="session")
def db(mapdl):
    if mapdl._server_version < (0, 4, 1):  # 2021R2
        pytest.skip("requires 2021R2 or newer")
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


def test_database_start_stop(mapdl):
    if mapdl._server_version < (0, 4, 1):  # 2021R2
        pytest.skip("requires 2021R2 or newer")

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


def test_nodes_first(nodes):
    assert nodes.first() == 1
    assert nodes.first(inod=10) == 11


def test_nodes_next(nodes):
    nodes._itnod = -1  # resets nodes state

    with pytest.raises(
        RuntimeError, match="You first have to call the `DbNodes.first` method"
    ):
        nodes.next()

    nodes.first()
    assert nodes.next() == 2


def test_nodes_info(nodes):
    assert nodes.info(1, DBDef.DB_SELECTED) == 1


@pytest.mark.parametrize("selected", [True, False])
def test_nodes_num(nodes, selected):
    assert nodes.num(selected=selected) == 425


def test_nodes_max_num(nodes):
    assert nodes.max_num == 425


def test_nodes_coord(nodes):
    sel, coord = nodes.coord(22)
    assert sel == 0  # selected
    assert coord == (1.0, 0.5, 0.0, 0.0, 0.0, 0.0)


def test_nodes_asarray(nodes):
    ind, coords, angles = nodes.all_asarray()
    assert np.allclose(ind, np.arange(1, 426))

    assert np.allclose(coords, nodes._db._mapdl.mesh.nodes)
    assert np.allclose(angles, 0)


def test_nodes_push(nodes):
    nnum = 100000
    x, y, z, xang, yang, zang = 1, 5, 10, 30, 40, 50
    nodes.push(nnum, x, y, z, xang, yang, zang)

    selected, coord = nodes.coord(nnum)
    assert selected == 0
    assert coord == (x, y, z, xang, yang, zang)

    with pytest.raises(ValueError, match="X angle must be input"):
        nodes.push(nnum, x, y, z, yang=1)

    with pytest.raises(ValueError, match="X and Y angles must be input"):
        nodes.push(nnum, x, y, z, zang=1)
