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

"""Test element preprocess commands"""
import numpy as np
import pytest

from ansys.mapdl.core import examples
from ansys.mapdl.core._commands.parse import parse_e, parse_et
from conftest import TestClass, requires


@pytest.fixture
def vm6(mapdl, cleared):
    mapdl.input(examples.vmfiles["vm6"])


def test_e(mapdl, cleared):
    mapdl.et("", 183)
    n0 = mapdl.n("", 0, 0, 0)
    n1 = mapdl.n("", 1, 0, 0)
    n2 = mapdl.n("", 1, 1, 0)
    n3 = mapdl.n("", 0, 1, 1)
    n4 = mapdl.n("", 0, 1, -1)
    e0 = mapdl.e(n0, n1, n2, n3)
    assert e0 == 1
    e1 = mapdl.e(n0, n1, n2, n4)
    assert e1 == 2


def test_et(mapdl, cleared):
    n_plane183 = mapdl.et("", "PLANE183")
    assert n_plane183 == 1
    n_compare = int(mapdl.get_value("ETYP", item1="NUM", it1num="MAX"))
    assert n_plane183 == n_compare
    n_plane183 = mapdl.et(17, "PLANE183")
    assert n_plane183 == 17


@requires("grpc")
def test_ewrite(mapdl, cleared):
    mapdl.et("", 183)
    n0 = mapdl.n("", 0, 0, 0)
    n1 = mapdl.n("", 1, 0, 0)
    n2 = mapdl.n("", 1, 1, 0)
    n3 = mapdl.n("", 0, 1, 1)
    n4 = mapdl.n("", 0, 1, -1)
    e0 = mapdl.e(n0, n1, n2, n3)

    filename = "elem.txt"
    mapdl.ewrite(filename, format_="LONG")
    etable_raw = mapdl._download_as_raw(filename).decode()
    etable = np.array(etable_raw.split(), np.int32)
    assert np.allclose(etable[:4], [n0, n1, n2, n3])


def test_eusort(mapdl, cleared):
    mapdl.post1()
    assert "ELEMENT SORT REMOVED" in mapdl.eusort()


def test_estif(mapdl, cleared):
    stiff = 1e-8
    output = mapdl.estif(stiff)
    statement, flt_out = output.split("=")
    assert "DEAD ELEMENT STIFFNESS MULTIPLIER" in statement
    assert float(flt_out) == stiff


def test_emodif(mapdl, cleared):
    mp_num = 2
    mapdl.mp("EX", mp_num, 210e9)
    mapdl.mp("DENS", mp_num, 7800)
    mapdl.mp("NUXY", mp_num, 0.3)
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, "SOLID186")
    mapdl.vmesh("ALL")
    output = mapdl.emodif("ALL", "MAT", i1=mp_num)
    statement, flt_out = output.split("=")
    assert "MODIFY ALL SELECTED ELEMENTS TO HAVE  MAT" in statement
    assert float(flt_out) == mp_num


def test_esol(mapdl, vm6):
    mapdl.post26()
    nvar = 2
    mapdl.esol(nvar, 1, 1, "S", "X", name="stuff")
    mapdl.dim("ARR", "ARRAY", 1)
    mapdl.vget("ARR", nvar)
    assert mapdl.parameters["ARR"] > 0  # expected 6017.83056641


def test_etype(mapdl, cleared):
    mapdl.et(1, "SOLID186")
    mapdl.etype()
    out = mapdl.stat()
    assert "IS SOLID186" in out
    assert "CURRENT NODAL DOF SET IS  UX    UY    UZ" in out


def test_eshape(mapdl, cleared):
    with pytest.warns(UserWarning):
        mapdl.eshape()


def test_etcontrol(mapdl, cleared):
    output = mapdl.etcontrol(eltech="set", eldegene="OFF")
    assert "SET" in output
    assert "OFF" in output


def test_edele(mapdl, cleared):
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, 186)
    mapdl.esize(0.25)
    mapdl.vmesh("ALL")
    mapdl.modmsh("DETACH")
    output = mapdl.edele(1, 10)
    assert "DELETE SELECTED ELEMENTS" in output


class TestParseElementCommands(TestClass):
    @pytest.mark.parametrize(
        "message",
        [
            ("ELEMENT 8", 8),
            ("ELEMENT 0", 0),
            ("ELEMENT -1", None),
            ("ELEMENT 23", 23),
            (None, None),
        ],
    )
    def test_parse_e_valid(self, message):
        response = parse_e(message[0])
        assert response is message[1]

    @pytest.mark.parametrize(
        "message",
        [
            "Element 8",
            "eLEMENT 0",
            "other thing entirely",
            "ELEMENT  8",
            "ELEMENT TYPE 8",
        ],
    )
    def test_parse_e_invalid(self, message):
        response = parse_e(message[0])
        assert response is None

    @pytest.mark.parametrize(
        "message",
        [
            ("ELEMENT TYPE 8", 8),
            ("ELEMENT TYPE 0", 0),
            ("ELEMENT TYPE -1", None),
            ("ELEMENT TYPE 23", 23),
            (None, None),
        ],
    )
    def test_parse_et_valid(self, message):
        response = parse_et(message[0])
        assert response == message[1]

    @pytest.mark.parametrize(
        "message",
        [
            "Element Type 8",
            "eLEMENT TyPe 0",
            "other thing entirely",
            "ELEMENT TYPE  8",
        ],
    )
    def test_parse_et_invalid(self, message):
        response = parse_e(message[0])
        assert response is None
