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

"""Tests for Mechanical APDL 2026 R1 SOLUTION command wrappers (Ticket 03)."""

import pytest


@pytest.mark.parametrize(
    ("method_name", "args", "kwargs", "expected_cmd", "expected_kwargs"),
    [
        ("cefilter", (), {}, "CEFILTER,", {}),
        ("cefilter", ("OFF",), {"mute": True}, "CEFILTER,OFF", {"mute": True}),
        ("cefilter", (), {"termkey": "ON"}, "CEFILTER,ON", {}),
        ("fval", (), {}, "FVAL,,,,", {}),
        (
            "fval",
            (10, "FX", "ACC", "%ACC_TAB%"),
            {"mute": True},
            "FVAL,10,FX,ACC,%ACC_TAB%",
            {"mute": True},
        ),
        (
            "fval",
            (),
            {"node": 5, "flab": "MZ", "inplab": "VEL", "value": 12.5},
            "FVAL,5,MZ,VEL,12.5",
            {},
        ),
        ("hbmopt", (), {}, "HBMOPT,,,,,,", {}),
        (
            "hbmopt",
            ("CONTSET", "ARC", 0.5, 0.01, 2.5, ""),
            {"write_to_log": False},
            "HBMOPT,CONTSET,ARC,0.5,0.01,2.5,",
            {"write_to_log": False},
        ),
        (
            "hbmopt",
            (),
            {"option": "AFT", "value1": 4, "value2": 128, "value5": "U5"},
            "HBMOPT,AFT,4,128,,,U5",
            {},
        ),
        ("prea", (), {}, "PREA", {}),
        ("prea", (), {"mute": False}, "PREA", {"mute": False}),
        ("scconnect", (), {}, "SCCONNECT,,,", {}),
        (
            "scconnect",
            ("localhost", 12345, "MAPDL_1"),
            {"mute": True},
            "SCCONNECT,localhost,12345,MAPDL_1",
            {"mute": True},
        ),
        (
            "scconnect",
            (),
            {"hostname": "10.0.0.2", "portnum": 54321, "solutionname": "ParticipantA"},
            "SCCONNECT,10.0.0.2,54321,ParticipantA",
            {},
        ),
        ("wksp", (), {}, "WKSP,", {}),
        (
            "wksp",
            (-100.0,),
            {"write_to_log": True},
            "WKSP,-100.0",
            {"write_to_log": True},
        ),
        ("wksp", (), {"value": 1.5}, "WKSP,1.5", {}),
    ],
)
def test_new_solution_commands_2026r1(
    fake_mapdl, method_name, args, kwargs, expected_cmd, expected_kwargs
):
    """New 2026 R1 SOLUTION wrappers emit exact APDL strings and forward kwargs."""
    method = getattr(fake_mapdl, method_name)
    result = method(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


@pytest.mark.parametrize(
    ("method_name", "args", "kwargs", "expected_cmd", "expected_kwargs"),
    [
        ("alphad", (), {}, "ALPHAD,,,", {}),
        (
            "alphad",
            (1000, "AUTO", 0.02),
            {"mute": True},
            "ALPHAD,1000,AUTO,0.02",
            {"mute": True},
        ),
        (
            "alphad",
            (),
            {"auto_adjust": "AUTO", "energy_ratio": 0.01},
            "ALPHAD,,AUTO,0.01",
            {},
        ),
        ("ambeam", (), {}, "AMBEAM,,,", {}),
        (
            "ambeam",
            (2, 250.0, 0.85),
            {},
            "AMBEAM,2,250.0,0.85",
            {},
        ),
        (
            "ambeam",
            (),
            {"power": 300, "absorptivity": 0.7},
            "AMBEAM,,300,0.7",
            {},
        ),
        ("ambuild", (), {}, "AMBUILD,,,,,,,", {}),
        (
            "ambuild",
            ("TIME", 1.0, 2.0, 0.5, "TAB1", "V5", "V6"),
            {},
            "AMBUILD,TIME,1.0,2.0,0.5,TAB1,V5,V6",
            {},
        ),
        (
            "ambuild",
            (),
            {"option": "SCAN", "val5": 11, "val6": 22},
            "AMBUILD,SCAN,,,,,11,22",
            {},
        ),
        ("amenv", (), {}, "AMENV,,,,,", {}),
        (
            "amenv",
            (25.0, 15.0, 1, 0.8, 5.67e-8),
            {},
            "AMENV,25.0,15.0,1,0.8,5.67e-08",
            {},
        ),
        (
            "amenv",
            (),
            {"radopt": 1, "emis": 0.9, "sbc": 5.67e-8},
            "AMENV,,,1,0.9,5.67e-08",
            {},
        ),
        ("awave", (), {}, "AWAVE,,,,,,,,,,,,,,,,,,", {}),
        (
            "awave",
            (1, "PLAN", "PRES", "EXT", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 11),
            {"mute": False},
            "AWAVE,1,PLAN,PRES,EXT,1,2,3,4,5,6,7,8,9,10,11,12,13,11",
            {"mute": False},
        ),
        ("awave", (), {"kcn": 12}, "AWAVE,,,,,,,,,,,,,,,,,,12", {}),
        ("bfe", (), {}, "BFE,,,,,,,,,", {}),
        (
            "bfe",
            (10, "FORC", 1, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0),
            {},
            "BFE,10,FORC,1,1.0,2.0,3.0,4.0,5.0,6.0",
            {},
        ),
        ("bfe", (), {"val5": "F5", "val6": "F6"}, "BFE,,,,,,,,F5,F6", {}),
        ("ddele", (), {}, "DDELE,,,,,,", {}),
        (
            "ddele",
            ("ALL", "UX", 10, 1, "OFF", 1),
            {},
            "DDELE,ALL,UX,10,1,OFF,1",
            {},
        ),
        ("ddele", (), {"irstrtflag": 1}, "DDELE,,,,,,1", {}),
        ("deltim", (), {}, "DELTIM,,,,,", {}),
        (
            "deltim",
            (0.01, 0.001, 0.1, "ON", 1),
            {"write_to_log": False},
            "DELTIM,0.01,0.001,0.1,ON,1",
            {"write_to_log": False},
        ),
        ("deltim", (), {"forcekey": "ON"}, "DELTIM,,,,,ON", {}),
        ("ic", (), {}, "IC,,,,,,,", {}),
        (
            "ic",
            ("NSNODES", "VELY", 500, "", "", "", "LSIC"),
            {},
            "IC,NSNODES,VELY,500,,,,LSIC",
            {},
        ),
        ("ic", (), {"lsic": "LSIC"}, "IC,,,,,,,LSIC", {}),
        ("kryopt", (), {}, "KRYOPT,,,,,", {}),
        (
            "kryopt",
            (100, 0.01, 1e-9),
            {},
            "KRYOPT,100,,,0.01,1e-09",
            {},
        ),
        ("kryopt", (), {"orthtol": 1e-7}, "KRYOPT,,,,,1e-07", {}),
        ("nladaptive", (), {}, "NLADAPTIVE,,,,,,,,,,,", {}),
        (
            "nladaptive",
            ("ALL", "ADD", "CONTACT", "WEAR", 1, 2, 3, 4, 5, 6, 7),
            {},
            "NLADAPTIVE,ALL,ADD,CONTACT,WEAR,1,2,3,4,5,6,7",
            {},
        ),
        (
            "nladaptive",
            (),
            {"val5": "A5", "val6": "A6", "val7": "A7"},
            "NLADAPTIVE,,,,,,,,,A5,A6,A7",
            {},
        ),
        ("nlhist", (), {}, "NLHIST,,,,,,,,,,,", {}),
        (
            "nlhist",
            ("NSOL", "UX_MAX", "U", "X", 10, "", "", "", 5.0, 1, 1e-3),
            {},
            "NLHIST,NSOL,UX_MAX,U,X,10,,,,5.0,1,0.001",
            {},
        ),
        ("nlhist", (), {"stop_tol": 0.05}, "NLHIST,,,,,,,,,,,0.05", {}),
        ("nlmesh", (), {}, "NLMESH,,,,", {}),
        ("nlmesh", ("NLAY", 3, 1, 2), {}, "NLMESH,NLAY,3,1,2", {}),
        ("nlmesh", (), {"val3": 4}, "NLMESH,,,,4", {}),
        ("seopt", (), {}, "SEOPT,,,,,,,,,", {}),
        (
            "seopt",
            ("SUB1", 2, 1, 0, "FULL", " BASIC", "ON", "YES"),
            {},
            "SEOPT,SUB1,2,1,0,FULL, BASIC,,ON,YES",
            {},
        ),
        ("seopt", (), {"seedgekey": 1}, "SEOPT,,,,,,,,,1", {}),
        ("spopt", (), {}, "SPOPT,,,,,", {}),
        (
            "spopt",
            ("SPRS", 20, "YES", "NO", "YES"),
            {},
            "SPOPT,SPRS,20,YES,NO,YES",
            {},
        ),
        ("spopt", (), {"speccum": "YES"}, "SPOPT,,,,,YES", {}),
    ],
)
def test_updated_solution_trailing_commands_2026r1(
    fake_mapdl, method_name, args, kwargs, expected_cmd, expected_kwargs
):
    """Updated 2026 R1 SOLUTION wrappers expose trailing args in exact APDL slots."""
    method = getattr(fake_mapdl, method_name)
    result = method(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


def test_tintp_keyword_only_oslm2_and_positional_compat(fake_mapdl):
    """tintp preserves 9-arg positional callers while routing oslm2= to slot 7."""
    # Default invocation: 11 APDL slots (slot 7 oslm2 blank, slot 8 unused blank)
    assert fake_mapdl.tintp() == "OUT:TINTP,,,,,,,,,,,"

    # Legacy 9-argument positional invocation hits exact same slots (1..6 and 9..11)
    pos_out = fake_mapdl.tintp(
        0.005, 0.25, 0.5, 1.0, 0.5, 0.01, 1, 0.005, 0.0, mute=True
    )
    assert pos_out == "OUT:TINTP,0.005,0.25,0.5,1.0,0.5,0.01,,,1,0.005,0.0"
    pos_fields = pos_out.removeprefix("OUT:").split(",")
    assert pos_fields == [
        "TINTP",
        "0.005",
        "0.25",
        "0.5",
        "1.0",
        "0.5",
        "0.01",
        "",
        "",
        "1",
        "0.005",
        "0.0",
    ]

    # Passing a 10th positional argument must raise TypeError (oslm2 is keyword-only)
    with pytest.raises(TypeError):
        fake_mapdl.tintp(0.005, 0.25, 0.5, 1.0, 0.5, 0.01, 1, 0.005, 0.0, 20)

    # Keyword-only oslm2 lands in slot 7 while slot 8 remains blank
    kw_out = fake_mapdl.tintp(0.005, 0.25, 0.5, 1.0, 0.5, 0.01, 1, 0.005, 0.0, oslm2=20)
    kw_fields = kw_out.removeprefix("OUT:").split(",")
    assert kw_fields[7] == "20"
    assert kw_fields[8] == ""
    assert kw_fields[9:] == ["1", "0.005", "0.0"]


def test_pcgopt_slot7_comma_alignment(fake_mapdl):
    """pcgopt places lm_key in APDL slot 7 leaving unused slot 6 blank."""
    default_fields = fake_mapdl.pcgopt().removeprefix("OUT:").split(",")
    assert default_fields == ["PCGOPT", "", "", "", "", "", "", ""]

    populated_out = fake_mapdl.pcgopt(
        "AUTO", "ON", "YES", "OFF", "ON", "ON", write_to_log=False
    )
    assert populated_out == "OUT:PCGOPT,AUTO,ON,YES,OFF,ON,,ON"
    fields = populated_out.removeprefix("OUT:").split(",")
    assert fields[5] == "ON"  # wrtfull in slot 5
    assert fields[6] == ""  # unused slot 6
    assert fields[7] == "ON"  # lm_key in slot 7

    kw_fields = fake_mapdl.pcgopt(lm_key="OFF").removeprefix("OUT:").split(",")
    assert kw_fields[6] == ""
    assert kw_fields[7] == "OFF"


def test_solution_explicit_slot_positions_and_single_mixin_ownership(fake_mapdl):
    """Verify 1-based APDL comma slots and single-mixin ownership for hbmopt."""
    from ansys.mapdl.core._commands.solution.dynamic_options import DynamicOptions
    from ansys.mapdl.core._commands.solution.nonlinear_options import NonlinearOptions

    assert "hbmopt" in NonlinearOptions.__dict__
    assert "hbmopt" not in DynamicOptions.__dict__

    awave_fields = fake_mapdl.awave(kcn="K18").removeprefix("OUT:").split(",")
    assert len(awave_fields) == 19
    assert awave_fields[18] == "K18"

    ddele_fields = fake_mapdl.ddele(irstrtflag="R6").removeprefix("OUT:").split(",")
    assert ddele_fields == ["DDELE", "", "", "", "", "", "R6"]

    ic_fields = fake_mapdl.ic(lsic="LSIC").removeprefix("OUT:").split(",")
    assert ic_fields == ["IC", "", "", "", "", "", "", "LSIC"]

    kryopt_fields = fake_mapdl.kryopt(orthtol="O5").removeprefix("OUT:").split(",")
    assert kryopt_fields == ["KRYOPT", "", "", "", "", "O5"]

    seopt_fields = fake_mapdl.seopt(seedgekey="E9").removeprefix("OUT:").split(",")
    assert seopt_fields == ["SEOPT", "", "", "", "", "", "", "", "", "E9"]


@pytest.mark.parametrize(
    "cmd",
    [
        "cefilter",
        "fval",
        "hbmopt",
        "prea",
        "scconnect",
        "wksp",
        "alphad",
        "ambeam",
        "ambuild",
        "amenv",
        "awave",
        "bfe",
        "ddele",
        "deltim",
        "ic",
        "kryopt",
        "nladaptive",
        "nlhist",
        "nlmesh",
        "seopt",
        "spopt",
        "tintp",
        "pcgopt",
    ],
)
def test_reflection_runner_on_ticket03_commands(fake_mapdl, cmd):
    """Test_MAPDL_commands.test_command passes offline across all 23 Ticket 03 wrappers."""
    import test_commands

    runner = test_commands.Test_MAPDL_commands()
    runner.test_command(fake_mapdl, cmd)
