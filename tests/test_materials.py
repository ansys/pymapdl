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
from unittest.mock import Mock, patch

import numpy as np
import pytest

from ansys.mapdl.core._materials import (
    MaterialsSnapshot,
    _parse_cdwrite_mat,
    _read_materials,
)
from ansys.mapdl.core.errors import MapdlRuntimeError
from conftest import requires

TEST_FILES = Path(__file__).parent / "test_files"
MP_ONLY_CDB = TEST_FILES / "materials_mp_only.cdb"
LEGACY_TABLES_CDB = TEST_FILES / "materials_legacy_tables.cdb"
BISO2_CDB = TEST_FILES / "materials_biso2.cdb"
NEWER_TABLES_CDB = TEST_FILES / "materials_newer_tables.cdb"
TBFIELD_CDB = TEST_FILES / "materials_tbfield.cdb"


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


@pytest.fixture(scope="module")
def legacy():
    return _parse_cdwrite_mat(LEGACY_TABLES_CDB.read_text())


def test_biso_at_two_temperatures():
    material = _parse_cdwrite_mat(BISO2_CDB.read_text())[1]
    (biso,) = material.tables
    assert (biso.label, biso.tbopt) == ("BISO", "")
    np.testing.assert_array_equal(biso.temperatures, [20.0, 200.0])
    np.testing.assert_array_equal(biso.constants[0], [250e6, 2e9])
    np.testing.assert_array_equal(biso.constants[1], [200e6, 1.5e9])
    assert biso.points == []
    assert biso.fields == {}
    np.testing.assert_array_equal(material.properties["EX"].values, [2.1e11, 1.9e11])


def test_miso_points_per_temperature(legacy):
    (miso,) = legacy[1].tables
    assert (miso.label, miso.tbopt, miso.constants) == ("MISO", "", [])
    np.testing.assert_array_equal(miso.temperatures, [20.0, 200.0])
    np.testing.assert_array_equal(
        miso.points[0], [[1.25e-3, 250e6], [1e-2, 300e6], [5e-2, 350e6]]
    )
    np.testing.assert_array_equal(
        miso.points[1], [[1e-3, 200e6], [1e-2, 240e6], [5e-2, 280e6]]
    )
    assert sorted(legacy[1].properties) == ["DENS", "EX", "PRXY"]


def test_anel_21_constants_in_order(legacy):
    (anel,) = legacy[3].tables
    assert (anel.label, anel.tbopt, anel.points) == ("ANEL", "0", [])
    np.testing.assert_array_equal(anel.temperatures, [20.0])
    np.testing.assert_array_equal(
        anel.constants[0],
        [1e11, 2e10, 3e10, 4e10, 5e10, 6e10, 1.1e11, 2.1e10, 3.1e10, 4.1e10, 5.1e10]
        + [1.2e11, 2.2e10, 3.2e10, 4.2e10, 1.3e11, 2.3e10, 3.3e10, 1.4e11, 2.4e10]
        + [1.5e11],
    )


def test_constants_land_by_start_index_across_gaps():
    text = LEGACY_TABLES_CDB.read_text()
    gap = "TBDAT,      4, 4.000000000E+10, 5.000000000E+10, 6.000000000E+10\n"
    anel = _parse_cdwrite_mat(text.replace(gap, ""))[3].tables[0]
    assert len(anel.constants[0]) == 21
    np.testing.assert_array_equal(
        anel.constants[0][:7], [1e11, 2e10, 3e10, 0, 0, 0, 1.1e11]
    )


def test_material_with_only_a_data_table(legacy):
    biso = legacy[4].tables[0]
    np.testing.assert_array_equal(biso.temperatures, [0.0])
    np.testing.assert_array_equal(biso.constants[0], [250e6, 2e9])
    assert list(legacy[4].properties) == ["EX"]
    assert legacy[2].tables == []


def test_two_data_tables_on_one_material():
    text = LEGACY_TABLES_CDB.read_text().replace("TB,BISO,       4", "TB,BISO,       1")
    tables = _parse_cdwrite_mat(text)[1].tables
    assert [table.label for table in tables] == ["MISO", "BISO"]
    np.testing.assert_array_equal(tables[1].constants[0], [250e6, 2e9])


def test_data_table_without_tbtemp_is_at_zero():
    text = BISO2_CDB.read_text().replace(
        "TB,BISO,       1,   2", "TB,BISO,       1,   1"
    )
    text = text.split("TBTEM,  200.000000")[0].replace(
        "TBTEM,  20.0000000    ,   1\n", ""
    )
    (biso,) = _parse_cdwrite_mat(text + "/GO\n")[1].tables
    np.testing.assert_array_equal(biso.temperatures, [0.0])
    np.testing.assert_array_equal(biso.constants[0], [250e6, 2e9])


def test_temperature_count_mismatch_raises():
    text = BISO2_CDB.read_text().replace(
        "TB,BISO,       1,   2", "TB,BISO,       1,   3"
    )
    with pytest.raises(ValueError, match=r"BISO.*Material 1.*3 temperatures.*has 2"):
        _parse_cdwrite_mat(text)


def test_data_table_is_immutable(legacy):
    miso = legacy[1].tables[0]
    with pytest.raises(dataclasses.FrozenInstanceError):
        miso.label = "BISO"
    with pytest.raises(ValueError, match="read-only"):
        miso.points[0][0, 0] = 0.0
    with pytest.raises(ValueError, match="read-only"):
        miso.temperatures[0] = 0.0
    with pytest.raises(ValueError, match="read-only"):
        legacy[3].tables[0].constants[0][0] = 0.0


@pytest.fixture(scope="module")
def newer():
    return _parse_cdwrite_mat(NEWER_TABLES_CDB.read_text())


def test_newer_elas_constants_per_temperature(newer):
    (elas,) = newer[5].tables
    assert (elas.label, elas.tbopt, elas.points, elas.fields) == (
        "ELAS",
        "ISOT",
        [],
        {},
    )
    np.testing.assert_array_equal(elas.temperatures, [20.0, 200.0])
    np.testing.assert_array_equal(elas.constants[0], [2.1e11, 0.3])
    np.testing.assert_array_equal(elas.constants[1], [1.9e11, 0.3])


def test_newer_plas_points_and_raw_tbin_options(newer):
    (plas,) = newer[2].tables
    assert (plas.label, plas.tbopt, plas.constants, plas.fields) == (
        "PLAS",
        "MISO",
        [],
        {},
    )
    np.testing.assert_array_equal(plas.temperatures, [20.0])
    np.testing.assert_array_equal(
        plas.points[0], [[0.0, 1e8], [2e-2, 1.5e8], [1e-1, 1.8e8]]
    )
    assert plas.options == {
        "NORM": ("1",),
        "CACH": ("0",),  # codespell-ignore
        "QUAN": ("0",),
        "DEFA": ("temp", "0.00000e+00"),
        "XRES": ("temp", "1"),
    }


def test_newer_creep_label_and_tbopt_as_written(newer):
    biso, cree = newer[4].tables
    assert (biso.label, biso.options) == ("BISO", {})
    assert (cree.label, cree.tbopt) == ("CREE", "10")
    np.testing.assert_array_equal(cree.temperatures, [0.0])
    np.testing.assert_array_equal(cree.constants[0], [1e-20, 5.0, 0.0])


def test_legacy_tables_unchanged_in_newer_fixture(newer, legacy):
    for mat_id in (1, 3):
        (old,) = legacy[mat_id].tables
        (new,) = newer[mat_id].tables
        assert (new.label, new.tbopt, new.fields, new.options) == (
            old.label,
            old.tbopt,
            {},
            {},
        )
        np.testing.assert_array_equal(new.temperatures, old.temperatures)


@pytest.fixture(scope="module")
def tbfield():
    return _parse_cdwrite_mat(TBFIELD_CDB.read_text())


@pytest.mark.parametrize(
    "mat_id, name, values, tbopt",
    [(1, "freq", [10.0, 100.0], "ISOT"), (2, "UF01", [0.0, 1.0], "ISOT")],
)
def test_non_temperature_field_points_at_zero_temperature(
    tbfield, mat_id, name, values, tbopt
):
    (elas,) = tbfield[mat_id].tables
    assert (elas.label, elas.tbopt, list(elas.fields)) == ("ELAS", tbopt, [name])
    np.testing.assert_array_equal(elas.fields[name], values)
    np.testing.assert_array_equal(elas.temperatures, [0.0, 0.0])
    assert len(elas.constants) == 2
    assert elas.options["DEFA"] == (name.lower(), "0.00000e+00")


def test_temperature_and_time_field_tuples(tbfield):
    (elas,) = tbfield[3].tables
    np.testing.assert_array_equal(elas.temperatures, [20.0, 20.0, 200.0, 200.0])
    assert list(elas.fields) == ["time"]
    np.testing.assert_array_equal(elas.fields["time"], [0.0, 10.0, 0.0, 10.0])
    np.testing.assert_array_equal(
        elas.constants,
        [[2.1e11, 0.3], [2.05e11, 0.3], [1.9e11, 0.3], [1.85e11, 0.3]],
    )
    assert elas.options["DEFA"] == ("temp", "0.00000e+00", "time", "0.00000e+00")
    assert elas.options["XRES"] == ("temp", "1", "time", "1")


def test_plastic_strain_rate_field_with_points(tbfield):
    (plas,) = tbfield[4].tables
    assert (plas.label, plas.tbopt) == ("PLAS", "MISO")
    np.testing.assert_array_equal(plas.fields["plsr"], [0.001, 1.0])
    np.testing.assert_array_equal(plas.temperatures, [0.0, 0.0])
    np.testing.assert_array_equal(plas.points[0], [[0.0, 2.5e8], [5e-2, 3e8]])
    np.testing.assert_array_equal(plas.points[1], [[0.0, 2.8e8], [5e-2, 3.4e8]])


def test_field_point_count_mismatch_raises():
    text = TBFIELD_CDB.read_text().replace(
        "TB,ELAS,       3,   4", "TB,ELAS,       3,   2"
    )
    with pytest.raises(ValueError, match=r"ELAS.*Material 3.*2 field points.*has 4"):
        _parse_cdwrite_mat(text)


def test_fields_are_read_only(tbfield):
    with pytest.raises(ValueError, match="read-only"):
        tbfield[1].tables[0].fields["freq"][0] = 0.0


@pytest.mark.parametrize("line", ["/SOLU", "TBFT,FADD,1,HYPER,MOONEY,3"])
def test_unknown_line_raises_quoting_it(line):
    text = LEGACY_TABLES_CDB.read_text().replace("/GO", f"{line}\n/GO")
    with pytest.raises(ValueError, match=re.escape(line)):
        _parse_cdwrite_mat(text)


@pytest.mark.parametrize(
    "line",
    [
        "TBTEM,  0.00000000    ,   1",
        "TBDAT,      1,  250000000.    , 2.000000000E+09,",
        "TBPT,, 1.000000000E-03,  200000000.",
        "TBFIELD,Temps,20.000000",
        "TBIN,NORM,1",
    ],
)
def test_data_table_line_without_tb_header_raises(line):
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


@requires("grpc")
def test_materials_legacy_data_tables_round_trip(mapdl, cleared):
    mapdl.tb("BISO", 1, 2)
    mapdl.tbtemp(20)
    mapdl.tbdata(1, 250e6, 2e9)
    mapdl.tbtemp(200)
    mapdl.tbdata(1, 200e6, 1.5e9)
    mapdl.tb("MISO", 2, 2, 3)
    mapdl.tbtemp(20)
    mapdl.tbpt("DEFI", 0.00125, 250e6)
    mapdl.tbpt("DEFI", 0.01, 300e6)
    mapdl.tbpt("DEFI", 0.05, 350e6)
    mapdl.tbtemp(200)
    mapdl.tbpt("DEFI", 0.001, 200e6)
    mapdl.tbpt("DEFI", 0.01, 240e6)
    mapdl.tbpt("DEFI", 0.05, 280e6)

    materials = mapdl.materials
    (biso,) = materials[1].tables
    assert biso.label == "BISO"
    np.testing.assert_array_equal(biso.temperatures, [20.0, 200.0])
    np.testing.assert_array_equal(biso.constants[0], [250e6, 2e9])
    np.testing.assert_array_equal(biso.constants[1], [200e6, 1.5e9])
    (miso,) = materials[2].tables
    assert miso.label == "MISO"
    np.testing.assert_array_equal(miso.temperatures, [20.0, 200.0])
    np.testing.assert_array_equal(
        miso.points[0], [[0.00125, 250e6], [0.01, 300e6], [0.05, 350e6]]
    )
    np.testing.assert_array_equal(
        miso.points[1], [[0.001, 200e6], [0.01, 240e6], [0.05, 280e6]]
    )


@requires("grpc")
def test_materials_newer_data_tables_round_trip(mapdl, cleared):
    mapdl.tb("PLAS", 1, "", "", "MISO")
    mapdl.tbtemp(20)
    mapdl.tbpt("DEFI", 0.0, 1e8)
    mapdl.tbpt("DEFI", 0.02, 1.5e8)
    mapdl.tb("ELAS", 2, 2, "", "ISOT")
    mapdl.tbtemp(20)
    mapdl.tbdata(1, 2.1e11, 0.3)
    mapdl.tbtemp(200)
    mapdl.tbdata(1, 1.9e11, 0.3)

    materials = mapdl.materials
    (plas,) = materials[1].tables
    assert (plas.label, plas.tbopt, plas.fields) == ("PLAS", "MISO", {})
    np.testing.assert_array_equal(plas.temperatures, [20.0])
    np.testing.assert_array_equal(plas.points[0], [[0.0, 1e8], [0.02, 1.5e8]])
    assert plas.options["NORM"] == ("1",)
    (elas,) = materials[2].tables
    assert (elas.label, elas.tbopt) == ("ELAS", "ISOT")
    np.testing.assert_array_equal(elas.temperatures, [20.0, 200.0])
    np.testing.assert_array_equal(elas.constants, [[2.1e11, 0.3], [1.9e11, 0.3]])


def test_read_in_non_interactive_raises_before_sending_commands():
    mapdl = Mock(_store_commands=True)
    with pytest.raises(MapdlRuntimeError, match="non_interactive"):
        _read_materials(mapdl)
    mapdl.cdwrite.assert_not_called()


def test_read_mutes_every_command_it_sends():
    mapdl = Mock(_store_commands=False)
    mapdl._download_as_raw.return_value = MP_ONLY_CDB.read_bytes()
    assert list(_read_materials(mapdl)) == [1, 2, 4, 10]
    sent = [c for c in mapdl.method_calls if c[0] != "_download_as_raw"]
    assert [name for name, _, _ in sent] == ["cdwrite", "slashdelete"]
    assert all(kwargs.get("mute") is True for _, _, kwargs in sent)


@requires("grpc")
@pytest.mark.parametrize(
    "enter, routine",
    [
        ("finish", "Begin level"),
        ("prep7", "PREP7"),
        ("slashsolu", "SOLUTION"),
        ("post1", "POST1"),
    ],
)
def test_materials_read_from_any_processor_keeps_it(mapdl, steel, enter, routine):
    expected = mapdl.materials
    mapdl.finish()
    getattr(mapdl, enter)()
    assert mapdl.parameters.routine == routine
    materials = mapdl.materials
    assert mapdl.parameters.routine == routine
    assert list(materials) == list(expected) == [1, 4]
    for mat_id in expected:
        assert sorted(materials[mat_id].properties) == sorted(
            expected[mat_id].properties
        )
        for label, table in expected[mat_id].properties.items():
            np.testing.assert_array_equal(
                materials[mat_id].properties[label].values, table.values
            )
    mapdl.finish()
    mapdl.prep7()


@requires("grpc")
def test_materials_read_prints_nothing(mapdl, steel, capsys):
    capsys.readouterr()
    mapdl.materials
    assert capsys.readouterr() == ("", "")


@requires("grpc")
def test_materials_in_non_interactive_raises(mapdl, steel):
    with pytest.raises(MapdlRuntimeError, match="non_interactive"):
        with mapdl.non_interactive:
            mapdl.materials
    assert list(mapdl.materials) == [1, 4]
