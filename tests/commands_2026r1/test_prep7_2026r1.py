# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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

"""Tests for Mechanical APDL 2026 R1 PREP7 command wrappers (Ticket 02)."""

import pytest


@pytest.mark.parametrize(
    ("method_name", "args", "kwargs", "expected_cmd", "expected_kwargs"),
    [
        ("cntgen", (), {}, "CNTGEN,,,,,,,", {}),
        (
            "cntgen",
            ("ASYM", "CM_CONT", "CM_TARG", 10, 11, 20, 30),
            {"mute": True},
            "CNTGEN,ASYM,CM_CONT,CM_TARG,10,11,20,30",
            {"mute": True},
        ),
        (
            "cntgen",
            (),
            {"option": "SYMM", "compc": "C1", "compt": "T1"},
            "CNTGEN,SYMM,C1,T1,,,,",
            {},
        ),
        ("eens", (), {}, "EENS,,,,", {}),
        (
            "eens",
            ("ALL", "res_file", 1),
            {"write_to_log": False},
            "EENS,ALL,res_file,,1",
            {"write_to_log": False},
        ),
        ("eens", (), {"elem": "ECOMP", "kout": 0}, "EENS,ECOMP,,,0", {}),
        ("fgrad", (), {}, "FGRAD,,,", {}),
        (
            "fgrad",
            (1, "STTE", 1e-7),
            {"mute": False},
            "FGRAD,1,STTE,1e-07",
            {"mute": False},
        ),
        ("mshoptim", (), {}, "MSHOPTIM,,,", {}),
        (
            "mshoptim",
            (1,),
            {"mute": True},
            "MSHOPTIM,,,1",
            {"mute": True},
        ),
        ("mshoptim", (), {"level": -1}, "MSHOPTIM,,,-1", {}),
        ("nsmass", (), {}, "NSMASS,,,,,", {}),
        (
            "nsmass",
            ("ALL", "ADD", 0, 12.5, 1),
            {"mute": True},
            "NSMASS,ALL,ADD,0,12.5,1",
            {"mute": True},
        ),
        (
            "nsmass",
            (),
            {"elem": "BODY_CM", "action": "LIST"},
            "NSMASS,BODY_CM,LIST,,,",
            {},
        ),
        ("rbgen", (), {}, "RBGEN,,,,,,,,", {}),
        (
            "rbgen",
            (100, "EL_CM", "ND_CM", 5, 6, 1, 1, "RB_OUT"),
            {},
            "RBGEN,100,EL_CM,ND_CM,5,6,1,1,RB_OUT",
            {},
        ),
        ("sfcgen", (), {}, "SFCGEN,,,,,,,,,,", {}),
        (
            "sfcgen",
            ("FORCE", 101, "SURF_CM", 0, 111111, "%WT%", 12, 13, 14, 0.5),
            {"write_to_log": True},
            "SFCGEN,FORCE,101,SURF_CM,0,111111,%WT%,12,13,14,0.5",
            {"write_to_log": True},
        ),
        ("tshape", (), {}, "TSHAPE,", {}),
        ("tshape", ("QUAD",), {"mute": True}, "TSHAPE,QUAD", {"mute": True}),
    ],
)
def test_new_prep7_commands_2026r1(
    fake_mapdl, method_name, args, kwargs, expected_cmd, expected_kwargs
):
    """New 2026 R1 PREP7 wrappers emit exact APDL strings and forward kwargs."""
    method = getattr(fake_mapdl, method_name)
    result = method(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


def test_tshap_archived_command_remains_active_without_deprecation(fake_mapdl):
    """Legacy Archived Command tshap() stays active alongside tshape()."""
    fake_mapdl._version = 26.1
    assert fake_mapdl.version == 26.1
    result = fake_mapdl.tshap("PILO", mute=True)
    assert result == "OUT:TSHAP,PILO"
    assert fake_mapdl.calls == [("TSHAP,PILO", {"mute": True})]


def test_prep7_new_commands_explicit_slots_and_single_mixin_ownership(fake_mapdl):
    """Verify empty-slot positions on eens/mshoptim and single-mixin nsmass ownership."""
    from ansys.mapdl.core._commands.prep7.materials import Materials
    from ansys.mapdl.core._commands.solution.misc_loads import MiscLoads

    assert "nsmass" in Materials.__dict__
    assert "nsmass" not in MiscLoads.__dict__

    eens_fields = fake_mapdl.eens("ALL", "fn", 1).removeprefix("OUT:").split(",")
    assert eens_fields == ["EENS", "ALL", "fn", "", "1"]

    mshoptim_fields = fake_mapdl.mshoptim(1).removeprefix("OUT:").split(",")
    assert mshoptim_fields == ["MSHOPTIM", "", "", "1"]


@pytest.mark.parametrize(
    ("method_name", "args", "kwargs", "expected_cmd", "expected_kwargs"),
    [
        ("cdwrite", (), {}, "CDWRITE,,'',,,,,,,", {}),
        (
            "cdwrite",
            ("DB", "model", "cdb", "model", "iges", "BLOCKED", "DUPL"),
            {"mute": True},
            "CDWRITE,DB,'model',cdb,,model,iges,BLOCKED,,DUPL",
            {"mute": True},
        ),
        ("cdwrite", (), {"key": "DUPL"}, "CDWRITE,,'',,,,,,,DUPL", {}),
        ("cgrow", (), {}, "CGROW,,,,,", {}),
        (
            "cgrow",
            ("SOPT", "DAMN", 0.05, "ABSO", 1),
            {"write_to_log": False},
            "CGROW,SOPT,DAMN,0.05,ABSO,1",
            {"write_to_log": False},
        ),
        ("cgrow", (), {"action": "SOPT", "par4": 1}, "CGROW,SOPT,,,,1", {}),
        ("secdata", (), {}, "SECDATA,,,,,,,,,,,,,,", {}),
        (
            "secdata",
            tuple(range(1, 15)),
            {"mute": True},
            "SECDATA,1,2,3,4,5,6,7,8,9,10,11,12,13,14",
            {"mute": True},
        ),
        (
            "secdata",
            (),
            {"val13": "V13", "val14": "V14"},
            "SECDATA,,,,,,,,,,,,,V13,V14",
            {},
        ),
        ("swgen", (), {}, "SWGEN,,,,,,,,,,,,,", {}),
        (
            "swgen",
            ("SW1", 2.5, "N1", "N2", 10, 20, 10.0, 0, 0, 1, 3, "NTOS", "PENE"),
            {"mute": False},
            "SWGEN,SW1,2.5,N1,N2,10,20,10.0,0,0,1,3,NTOS,PENE",
            {"mute": False},
        ),
        ("swgen", (), {"algo": "AL"}, "SWGEN,,,,,,,,,,,,,AL", {}),
    ],
)
def test_updated_prep7_trailing_commands_2026r1(
    fake_mapdl, method_name, args, kwargs, expected_cmd, expected_kwargs
):
    """Updated 2026 R1 PREP7 wrappers expose trailing args in exact APDL slots."""
    method = getattr(fake_mapdl, method_name)
    result = method(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


def test_updated_prep7_trailing_explicit_slot_positions(fake_mapdl):
    """Verify 1-based APDL comma slot indices for cdwrite, cgrow, secdata, swgen."""
    from ansys.mapdl.core._commands.prep7.data_tables import DataTables
    from ansys.mapdl.core._commands.prep7.special_purpose import SpecialPurpose

    assert "cgrow" in DataTables.__dict__
    assert "cgrow" not in SpecialPurpose.__dict__

    cdwrite_fields = fake_mapdl.cdwrite(key="DUPL").removeprefix("OUT:").split(",")
    assert cdwrite_fields[0] == "CDWRITE"
    assert cdwrite_fields[4] == ""
    assert cdwrite_fields[8] == ""
    assert cdwrite_fields[9] == "DUPL"

    cgrow_fields = (
        fake_mapdl.cgrow("SOPT", "DAMN", 0.05, "ABSO", 1)
        .removeprefix("OUT:")
        .split(",")
    )
    assert cgrow_fields == ["CGROW", "SOPT", "DAMN", "0.05", "ABSO", "1"]

    secdata_fields = (
        fake_mapdl.secdata(val13="A", val14="B").removeprefix("OUT:").split(",")
    )
    assert secdata_fields[13] == "A"
    assert secdata_fields[14] == "B"

    swgen_fields = fake_mapdl.swgen(algo="LAGR").removeprefix("OUT:").split(",")
    assert swgen_fields[13] == "LAGR"


@pytest.mark.parametrize(
    ("args", "kwargs", "expected_cmd", "expected_kwargs"),
    [
        ((), {}, "EMSEL,,,,,,", {}),
        (("S", 1, 10, 1), {"mute": True}, "EMSEL,S,,,1,10,1", {"mute": True}),
        (
            ("S", 1, 7, 2),
            {"item": "LAYER", "comp": "NUM", "write_to_log": False},
            "EMSEL,S,LAYER,NUM,1,7,2",
            {"write_to_log": False},
        ),
        (
            (),
            {"type_": "LIST", "item": "LAYER", "comp": "STO"},
            "EMSEL,LIST,LAYER,STO,,,",
            {},
        ),
        (
            ("S",),
            {"item": "LAYER", "comp": "NAME", "vmin": "PLY1"},
            "EMSEL,S,LAYER,NAME,PLY1,,",
            {},
        ),
    ],
)
def test_emsel_positional_and_keyword_only_2026r1(
    fake_mapdl, args, kwargs, expected_cmd, expected_kwargs
):
    """emsel preserves 4-arg positional calls while routing item/comp to slots 2-3."""
    result = fake_mapdl.emsel(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


def test_emsel_rejects_excess_positional_arguments(fake_mapdl):
    """item and comp on emsel are strictly keyword-only."""
    with pytest.raises(TypeError):
        fake_mapdl.emsel("S", "LAYER", "NUM", 1, 10, 1)


@pytest.mark.parametrize(
    ("args", "kwargs", "expected_cmd", "expected_kwargs"),
    [
        ((), {}, "SECMODIF,,,,,,", {}),
        (
            (1, "NORM", 0.0, 1.0, 0.0, 0),
            {"mute": True},
            "SECMODIF,1,NORM,0.0,1.0,0.0,0",
            {"mute": True},
        ),
        (
            (),
            {
                "secid": "ALL",
                "kywrd": "BEAM",
                "value1": "RECT",
                "value2": "B",
                "value3": 2.5,
                "write_to_log": False,
            },
            "SECMODIF,ALL,BEAM,RECT,B,2.5,",
            {"write_to_log": False},
        ),
    ],
)
def test_secmodif_multi_value_2026r1(
    fake_mapdl, args, kwargs, expected_cmd, expected_kwargs
):
    """secmodif maps value1..value4 to APDL fields 3..6 and forwards kwargs."""
    result = fake_mapdl.secmodif(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


def test_secmodif_legacy_addional_command_arg_emits_deprecation_warning(fake_mapdl):
    """Legacy addional_command_arg emits DeprecationWarning and maps to value1."""
    with pytest.deprecated_call(match="addional_command_arg"):
        result = fake_mapdl.secmodif(1, "NAME", addional_command_arg="PRET1", mute=True)
    assert result == "OUT:SECMODIF,1,NAME,PRET1,,,"
    assert fake_mapdl.calls == [("SECMODIF,1,NAME,PRET1,,,", {"mute": True})]


def test_secmodif_both_value1_and_addional_command_arg_raises_type_error(fake_mapdl):
    """Passing both value1 and addional_command_arg raises TypeError."""
    with pytest.raises(TypeError, match="addional_command_arg"):
        fake_mapdl.secmodif(
            1, "NAME", value1="NEW_NAME", addional_command_arg="OLD_NAME"
        )
    assert fake_mapdl.calls == []

    with pytest.raises(TypeError, match="addional_command_arg"):
        fake_mapdl.secmodif(1, "NAME", "NEW_NAME", addional_command_arg="OLD_NAME")
    assert fake_mapdl.calls == []


@pytest.mark.parametrize(
    "cmd",
    [
        "cntgen",
        "eens",
        "fgrad",
        "mshoptim",
        "nsmass",
        "rbgen",
        "sfcgen",
        "tshape",
        "cdwrite",
        "cgrow",
        "secdata",
        "swgen",
        "emsel",
        "secmodif",
    ],
)
def test_prep7_commands_pass_reflection_runner(fake_mapdl, cmd):
    """All 14 Ticket 02 PREP7 commands pass Test_MAPDL_commands.test_command."""
    import test_commands

    runner = test_commands.Test_MAPDL_commands()
    runner.test_command(fake_mapdl, cmd)
