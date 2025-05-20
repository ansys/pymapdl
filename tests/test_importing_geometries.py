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

import os

import pytest

from ansys.mapdl.core.errors import (
    MapdlCommandIgnoredError,
    MapdlRuntimeError,
)
from conftest import ON_CI, ON_LOCAL, ON_UBUNTU, NullContext

PATH = os.path.dirname(os.path.abspath(__file__))

# Files with CADs
CADs_path = os.path.join(PATH, "test_files", "CAD_formats")


####################################################################
# Reading in all the supported formats


def geometry_test_is_correct(mapdl, geometry=None):
    if geometry == "iges":
        entities = [0, 8, 36, 44]
    else:
        entities = [1, 8, 18, 12]

    assert (
        mapdl.geometry.n_keypoint == entities[3]
    ), f"The number of keypoints ({mapdl.geometry.n_keypoint}) is not correct."
    assert (
        mapdl.geometry.n_line == entities[2]
    ), f"The number of lines ({mapdl.geometry.n_line}) is not correct."
    assert (
        mapdl.geometry.n_area == entities[1]
    ), f"The number of areas ({mapdl.geometry.n_area}) is not correct."
    assert (
        mapdl.geometry.n_volu == entities[0]
    ), f"The number of volumes ({mapdl.geometry.n_volu}) is not correct."
    return True


def clear_wkdir_from_cads(mapdl):
    """Cleaning files because we don't want to reuse the ANF files"""
    list_files = [
        each for each in mapdl.list_files() if each.startswith("CubeWithHole")
    ]
    for each_file in list_files:
        try:
            mapdl.slashdelete(each_file)
        except IOError:
            pass


## IGES
#
def test_readin_igs(mapdl, cleared):
    mapdl.igesin(fname=os.path.join(CADs_path, "CubeWithHole"), ext="igs")
    assert geometry_test_is_correct(mapdl, geometry="iges")

    nareas = mapdl.geometry.n_area

    # Generating the volumes
    mapdl.prep7()
    mapdl.nummrg("kp")
    mapdl.va("all")

    assert mapdl.geometry.n_volu == 1
    assert nareas == mapdl.geometry.n_area
    # Rest of the entities are not maintained because of the nummrg.

    clear_wkdir_from_cads(mapdl)


## Connection commands
#
@pytest.mark.xfail(True, reason="Command seems broken. See #2377")
def test_readin_sat(mapdl, cleared):
    if ON_CI and mapdl.version >= 23.2:
        context = pytest.raises(
            MapdlRuntimeError, match="Specified library does not exist."
        )

    elif ON_CI and mapdl.version <= 22.2 and not ON_UBUNTU:
        context = pytest.raises(
            MapdlRuntimeError, match="No shared command/library files were found"
        )

    elif ON_CI and mapdl.version == 22.2 and ON_UBUNTU and not ON_LOCAL:
        context = pytest.raises(MapdlCommandIgnoredError, match="anf does not exist.")

    elif ON_CI and ON_LOCAL:
        context = pytest.raises(MapdlCommandIgnoredError, match="anf does not exist.")
    elif ON_CI:
        context = pytest.raises(AssertionError)
    else:
        context = NullContext()

    with context:
        mapdl.satin(
            "CubeWithHole", extension="sat", path=CADs_path, entity="solid", fmt=0
        )
        assert geometry_test_is_correct(mapdl)
    clear_wkdir_from_cads(mapdl)


@pytest.mark.xfail(True, reason="Command seems broken. See #2377")
def test_readin_x_t(mapdl, cleared):
    if ON_CI and mapdl.version >= 23.2:
        context = pytest.raises(
            MapdlRuntimeError, match="Specified library does not exist."
        )

    elif ON_CI and mapdl.version == 23.1:
        context = pytest.raises(MapdlCommandIgnoredError, match="does not exist")

    elif ON_CI and mapdl.version <= 22.2 and not ON_UBUNTU:
        context = pytest.raises(
            MapdlRuntimeError, match="No shared command/library files were found"
        )

    elif ON_CI and ON_LOCAL:
        context = pytest.raises(AssertionError)

    elif ON_CI:
        context = pytest.raises(MapdlCommandIgnoredError, match="anf does not exist.")

    else:
        context = NullContext()

    with context:
        mapdl.parain(
            name="CubeWithHole", extension="x_t", path=CADs_path, entity="solid", fmt=0
        )
        assert geometry_test_is_correct(mapdl)

    clear_wkdir_from_cads(mapdl)


@pytest.mark.xfail(ON_CI, reason="MAPDL docker image do not have the CAD libraries")
def test_readin_catiav4(mapdl, cleared):
    # Catia v4 is only supported on Linux
    if mapdl.platform == "windows":
        context = pytest.raises(OSError)
    else:
        context = NullContext()

    with context:
        mapdl.catiain(
            name="CubeWithHole",  # this file is catia v5. We need to change it
            extension="CATPart",
            path=CADs_path,
        )
        assert geometry_test_is_correct(mapdl)

    clear_wkdir_from_cads(mapdl)


def test_readin_catiav5(mapdl, cleared):
    # Catia v5 is only supported on Windows
    if ON_CI and mapdl.version <= 22.2 and not ON_UBUNTU:
        context = pytest.raises(
            MapdlRuntimeError, match="No shared command/library files were found"
        )

    elif mapdl.platform == "linux":
        context = pytest.raises(OSError)

    else:
        context = NullContext()

    with context:
        mapdl.cat5in(
            name="CubeWithHole",
            extension="CATPart",
            path=CADs_path,
            entity="solid",
            fmt=0,
        )
        assert geometry_test_is_correct(mapdl)

    clear_wkdir_from_cads(mapdl)
