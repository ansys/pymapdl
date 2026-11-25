# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

import dataclasses
from pathlib import Path
import re
from unittest.mock import patch

import numpy as np
import pytest

from ansys.mapdl.core._materials import MaterialsSnapshot, _parse_cdwrite_mat
from conftest import requires

MP_ONLY_CDB = Path(__file__).parent / "test_files" / "materials_mp_only.cdb"


@pytest.fixture(scope="module")
def parsed():
    return _parse_cdwrite_mat(MP_ONLY_CDB.read_text())


def test_temperature_dependent_property_longer_than_one_line(parsed):
    ex = parsed[1].properties["EX"]
    np.testing.assert_array_equal(ex.temperatures, [20, 50, 100, 150, 200, 250])
    np.testing.assert_array_equal(
        ex.values, [2.1e11, 2.08e11, 2.05e11, 2.0e11, 1.95e11, 1.9e11]
    )


def test_constant_property_is_one_point_table_at_zero(parsed):
    prxy = parsed[1].properties["PRXY"]
    np.testing.assert_array_equal(prxy.temperatures, [0.0])
    np.testing.assert_array_equal(prxy.values, [0.3])
    np.testing.assert_array_equal(parsed[1].properties["DENS"].values, [7850.0])


def test_material_ids_and_labels_come_back_as_defined(parsed):
    assert list(parsed) == [1, 2, 4, 10]
    assert [parsed[i].id for i in parsed] == [1, 2, 4, 10]
    assert sorted(parsed[1].properties) == ["DENS", "EX", "PRXY"]
    np.testing.assert_array_equal(parsed[10].properties["EX"].values, [1e9])


def test_commands_match_on_four_characters_case_insensitively(parsed):
    text = MP_ONLY_CDB.read_text().lower().replace("mptemp,", "mpte,")
    relaxed = _parse_cdwrite_mat(f"\n{text}\n\n")
    assert list(relaxed) == list(parsed)
    np.testing.assert_array_equal(
        relaxed[1].properties["EX"].temperatures,
        parsed[1].properties["EX"].temperatures,
    )
    assert sorted(relaxed[1].properties) == ["DENS", "EX", "PRXY"]


def test_snapshot_is_immutable(parsed):
    material = parsed[1]
    ex = material.properties["EX"]
    with pytest.raises(dataclasses.FrozenInstanceError):
        material.id = 2
    with pytest.raises(dataclasses.FrozenInstanceError):
        ex.values = np.zeros(6)
    with pytest.raises(ValueError, match="read-only"):
        ex.values[0] = 0.0
    with pytest.raises(ValueError, match="read-only"):
        ex.temperatures[0] = 0.0


@pytest.mark.parametrize(
    "line",
    [
        "TB,BISO,       4,   1",
        "TBTEM,  0.00000000    ,   1",
        "TBDAT,      1,  250000000.    , 2.000000000E+09,",
        "/SOLU",
    ],
)
def test_unknown_line_raises_quoting_it(line):
    text = MP_ONLY_CDB.read_text().replace("/GO", f"{line}\n/GO")
    with pytest.raises(ValueError, match=re.escape(line)):
        _parse_cdwrite_mat(text)


@requires("pandas")
def test_to_dataframe_has_one_row_per_temperature_point(parsed):
    df = MaterialsSnapshot(parsed).to_dataframe()
    assert list(df.columns) == ["material", "label", "temperature", "value"]
    assert df.to_records(index=False).tolist() == [
        (1, "EX", 20.0, 2.1e11),
        (1, "EX", 50.0, 2.08e11),
        (1, "EX", 100.0, 2.05e11),
        (1, "EX", 150.0, 2.0e11),
        (1, "EX", 200.0, 1.95e11),
        (1, "EX", 250.0, 1.9e11),
        (1, "DENS", 0.0, 7850.0),
        (1, "PRXY", 0.0, 0.3),
        (2, "EX", 0.0, 7e10),
        (4, "EX", 0.0, 2e11),
        (10, "EX", 0.0, 1e9),
    ]


def test_to_dataframe_without_pandas_raises_install_error(parsed):
    with (
        patch("ansys.mapdl.core._materials._HAS_PANDAS", False),
        pytest.raises(ModuleNotFoundError, match="pip install pandas"),
    ):
        MaterialsSnapshot(parsed).to_dataframe()


@pytest.fixture
def steel(mapdl, cleared):
    mapdl.mptemp(1, 20, 50, 100, 150, 200, 250)
    mapdl.mpdata("EX", 1, 1, 2.1e11, 2.08e11, 2.05e11, 2.0e11, 1.95e11, 1.9e11)
    mapdl.mptemp()
    mapdl.mp("PRXY", 1, 0.3)
    mapdl.mp("DENS", 1, 7850)
    mapdl.mp("EX", 4, 7e10)


@requires("grpc")
def test_materials_round_trip(mapdl, steel):
    material = mapdl.materials[1]
    assert material.id == 1
    ex = material.properties["EX"]
    np.testing.assert_array_equal(ex.temperatures, [20, 50, 100, 150, 200, 250])
    np.testing.assert_array_equal(
        ex.values, [2.1e11, 2.08e11, 2.05e11, 2.0e11, 1.95e11, 1.9e11]
    )
    np.testing.assert_array_equal(material.properties["PRXY"].temperatures, [0.0])
    np.testing.assert_array_equal(material.properties["PRXY"].values, [0.3])
    np.testing.assert_array_equal(material.properties["DENS"].values, [7850.0])


@requires("grpc")
def test_materials_mapping(mapdl, steel):
    materials = mapdl.materials
    assert len(materials) == 2
    assert list(materials) == [1, 4]
    assert 4 in materials
    assert 2 not in materials
    with pytest.raises(KeyError):
        materials[2]


@requires("grpc")
def test_materials_snapshot_does_not_follow_later_changes(mapdl, steel):
    before = mapdl.materials[1]
    mapdl.mp("PRXY", 1, 0.25)
    np.testing.assert_array_equal(before.properties["PRXY"].values, [0.3])
    np.testing.assert_array_equal(mapdl.materials[1].properties["PRXY"].values, [0.25])


@requires("grpc")
def test_materials_leaves_no_file_behind(mapdl, steel):
    files_before = set(mapdl.list_files())
    mapdl.materials
    mapdl.materials
    assert set(mapdl.list_files()) == files_before


@requires("grpc")
def test_materials_empty_session(mapdl, cleared):
    assert len(mapdl.materials) == 0
