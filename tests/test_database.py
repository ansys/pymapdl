# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

from ansys.tools.versioning import server_meets_version
import numpy as np
import pytest

## Checking MAPDL versions
from ansys.mapdl.core.database import MINIMUM_MAPDL_VERSION, DBDef, MapdlDb
from ansys.mapdl.core.errors import MapdlRuntimeError, MapdlVersionError
from ansys.mapdl.core.misc import random_string
from conftest import ON_CI, TestClass

SKIP_ON_VERSIONS = ["22.2", "23.1", "23.2", "24.1", "24.2", "25.1", "25.2"]


@pytest.fixture(scope="session")
def db(mapdl):
    from ansys.api.mapdl import __version__ as api_version

    api_version = tuple(int(each) for each in api_version.split("."))
    if api_version < (0, 5, 1):
        pytest.skip("Requires 'ansys.api.mapdl' package to at least v0.5.1.")

    ## Checking MAPDL versions
    mapdl_version = str(mapdl.version)
    if not server_meets_version(mapdl_version, MINIMUM_MAPDL_VERSION):
        pytest.skip(
            f"This MAPDL version ({mapdl_version}) is not compatible with the Database module."
        )

    ## Exceptions
    if mapdl_version in SKIP_ON_VERSIONS and ON_CI:
        pytest.skip(
            f"This MAPDL version ({mapdl_version}) docker image seems to not support DB on CICD."
        )

    if mapdl._server_version < (0, 4, 1):  # 2021R2
        ver_ = ".".join([str(each) for each in mapdl._server_version])
        pytest.skip(
            f"This version of MAPDL gRPC API version ('ansys.api.mapdl' == {ver_}) is not compatible with 'database' module."
        )

    mapdl.clear()
    if mapdl.db.active or mapdl.db._stub is None:
        mapdl.db.stop()

    mapdl.db.start()
    return mapdl.db


def test_failure_on_non_allowed_versions(mapdl, cleared):
    if str(mapdl.version) in ["24.1", "24.2"]:
        with pytest.raises(MapdlVersionError):
            mapdl.db.start()
    else:
        pytest.skip(f"Should run only on MAPDL 24.1 and 24.2")


def test_database_start_stop(mapdl, cleared):
    if mapdl._server_version < (0, 4, 1):  # 2021R2
        pytest.skip("requires 2021R2 or newer")

    mapdl_version = str(mapdl.version)
    if not server_meets_version(mapdl_version, MINIMUM_MAPDL_VERSION):
        pytest.skip(
            f"This MAPDL version ({mapdl_version}) is not compatible with the Database module."
        )

    # Exceptions
    if mapdl_version in SKIP_ON_VERSIONS and ON_CI:
        pytest.skip(
            f"This MAPDL version ({mapdl_version}) docker image seems to not support DB, but local does."
        )

    if MapdlDb(mapdl).active:
        MapdlDb(mapdl)._stop()

    # verify it can be created twice
    mapdl.prep7()
    for _ in range(2):
        database = MapdlDb(mapdl)
        assert not database.active
        database.start()
        assert database.active

        # verify a double start does not lead to an error
        database.start()
        assert database.active

        database.stop()
        assert not database.active
        assert "not active" in str(database)
        assert database._channel is None

    with pytest.warns(UserWarning):
        database.stop()

    # Starting the database for the rest of the test session
    mapdl.db.start()


def test_database_repr(db):
    assert db._channel_str in str(db)


def test_save(db):
    with pytest.raises(ValueError, match="Option must be one of the"):
        db.save("file.db", "not_an_option")

    filename = f"{random_string()}.db"
    db.save(filename)

    assert filename in db._mapdl.list_files()
    output = db.load(filename)
    assert "RESUME ANSYS" in output


def test_clear(db):
    db._mapdl.prep7()
    db._mapdl.k(1, 1, 1, 1)
    db.clear()
    assert db._mapdl.get_value("KP", 0, "count") == 0.0


def test__channel_str(db):
    assert db._channel_str is not None
    assert ":" in db._channel_str
    assert re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", db._channel_str)
    assert re.search(r"\d{4,6}", db._channel_str)


def test_off_db(mapdl, cleared, db):
    """Testing that when there is no active database"""
    if db.active:
        db.stop()
    assert not mapdl.db.active
    assert mapdl.db.nodes is None
    assert mapdl.db.elems is None


def test_wrong_api_version(mapdl, cleared, db):
    mapdl.db.stop()
    mapdl.__server_version = (0, 1, 1)
    mapdl._MapdlGrpc__server_version = (0, 1, 1)

    from ansys.mapdl.core.errors import MapdlVersionError

    with pytest.raises(MapdlVersionError):
        mapdl.db.start()

    mapdl.__sever_version = None
    mapdl._MapdlGrpc__server_version = None

    mapdl._server_version  # resetting
    mapdl.db.start()

    assert "is currently running" in mapdl.db._status()


def test_repr(mapdl, cleared, db):
    elems = mapdl.db.elems
    nodes = mapdl.db.nodes

    assert elems
    assert nodes

    assert isinstance(elems.__repr__(), str)
    assert isinstance(nodes.__repr__(), str)

    assert isinstance(elems.__str__(), str)
    assert isinstance(nodes.__str__(), str)


def gen_block(mapdl):
    """Generate nodes and elements in a simple block."""
    from conftest import clear

    clear(mapdl)

    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, 186)
    mapdl.esize(0.25)
    mapdl.vmesh("ALL")


class Test_Nodes(TestClass):

    @staticmethod
    @pytest.fixture(scope="class")
    def nodes(mapdl, db):
        gen_block(mapdl)
        return db.nodes

    @staticmethod
    def test_nodes_repr(nodes):
        assert "425" in str(nodes)
        assert "Number of nodes" in str(nodes)

    @staticmethod
    def test_nodes_first(nodes):
        assert nodes.first() == 1
        assert nodes.first(inod=10) == 11

    @staticmethod
    def test_nodes_next(nodes):
        nodes._itnod = -1  # resets nodes state

        with pytest.raises(
            MapdlRuntimeError, match="You first have to call the `DbNodes.first` method"
        ):
            nodes.next()

        nodes.first()
        assert nodes.next() == 2

    @staticmethod
    def test_nodes_info(nodes):
        assert nodes.info(1, DBDef.DB_SELECTED) == 1

    @staticmethod
    @pytest.mark.parametrize("selected", [True, False])
    def test_nodes_num(nodes, selected):
        assert nodes.num(selected=selected) == 425

    @staticmethod
    def test_nodes_max_num(nodes):
        assert nodes.max_num == 425

    @staticmethod
    def test_nodes_coord(nodes):
        sel, coord = nodes.coord(22)
        assert sel == 0  # selected
        assert coord == (1.0, 0.5, 0.0, 0.0, 0.0, 0.0)

    @staticmethod
    def test_nodes_asarray(nodes):
        ind, coords, angles = nodes.all_asarray()
        assert np.allclose(ind, np.arange(1, 426))

        assert np.allclose(coords, nodes._db._mapdl.mesh.nodes)
        assert np.allclose(angles, 0)

    @staticmethod
    def test_nodes_push(mapdl, nodes):
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

        # this test changes the database, so let's restore it back
        # as in `nodes` fixture.
        gen_block(mapdl)


class Test_Elems(TestClass):

    @staticmethod
    @pytest.fixture(scope="class")
    def elems(mapdl, db):
        gen_block(mapdl)
        return db.elems

    @staticmethod
    def test_elems_repr(elems):
        assert "64" in str(elems)
        assert "Number of elements" in str(elems)

    @staticmethod
    def test_elems_first(elems):
        assert elems.first() == 1
        assert elems.first(ielm=10) == 11

    @staticmethod
    def test_elems_next(elems):
        elems._itelm = -1  # resets elems state

        with pytest.raises(
            MapdlRuntimeError, match="You first have to call the `DbElems.first` method"
        ):
            elems.next()

        elems.first()
        assert elems.next() == 2

    @staticmethod
    def test_elems_info(elems):
        assert elems.info(1, DBDef.DB_SELECTED) == 1

    @pytest.mark.parametrize("selected", [True, False])
    @staticmethod
    def test_elems_num(elems, selected):
        assert elems.num(selected=selected) == 64

    @staticmethod
    def test_elems_max_num(elems):
        assert elems.max_num == 64

    @staticmethod
    def test_elems_get(elems):
        ielm = 1
        elem_info = elems.get(ielm)

        assert len(elem_info.nodes) == elem_info.nnod
        assert len(elem_info.elmdat) == 10
        assert elem_info.ielem == ielm

    @staticmethod
    def test_elems_push(elems):
        ielm = 1
        elem_info = elems.get(ielm)

        ielm_new = 10000
        elems.push(ielm_new, elem_info.elmdat, elem_info.nodes)

        elem_info_new = elems.get(ielm_new)
        assert elem_info.elmdat == elem_info_new.elmdat
        assert elem_info.nnod == elem_info_new.nnod
        assert elem_info.nodes == elem_info_new.nodes

        with pytest.raises(ValueError, match="`elmdat` must be length 10"):
            elems.push(ielm_new, [1, 2, 3], elem_info.nodes)
