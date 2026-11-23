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

"""Tests for Mechanical APDL 2026 R1 APDL and POST1 command wrappers (Ticket 04)."""

import pytest

from conftest import requires


@pytest.mark.parametrize(
    ("method_name", "args", "kwargs", "expected_cmd", "expected_kwargs"),
    [
        ("kron", (), {}, "*KRON,,,", {}),
        (
            "kron",
            ("MAT_A", "MAT_B", "MAT_C"),
            {"mute": True},
            "*KRON,MAT_A,MAT_B,MAT_C",
            {"mute": True},
        ),
        (
            "kron",
            (),
            {"m1": "V1", "m2": "V2", "m3": "VOUT"},
            "*KRON,V1,V2,VOUT",
            {},
        ),
        ("starxpl", (), {}, "*XPL,,,", {}),
        (
            "starxpl",
            ("OPEN", "file.full", ""),
            {"write_to_log": False},
            "*XPL,OPEN,file.full,",
            {"write_to_log": False},
        ),
        (
            "starxpl",
            (),
            {"action": "READ", "val1": "MASS", "val2": "MVEC"},
            "*XPL,READ,MASS,MVEC",
            {},
        ),
        ("maxcycmode", (), {}, "MAXCYCMODE,,,,,,,,", {}),
        (
            "maxcycmode",
            (1, 2, "Real", 1, 3, "Real", "USUM", 12),
            {"mute": False},
            "MAXCYCMODE,1,2,Real,1,3,Real,USUM,12",
            {"mute": False},
        ),
        (
            "maxcycmode",
            (),
            {
                "lstep1": 1,
                "sbstep1": 1,
                "cmp1x1": "Real",
                "lstep2": 1,
                "sbstep2": 1,
                "cmp1x2": "Imag",
                "comp": "SX",
            },
            "MAXCYCMODE,1,1,Real,1,1,Imag,SX,",
            {},
        ),
    ],
)
def test_new_apdl_post1_commands_2026r1(
    fake_mapdl, method_name, args, kwargs, expected_cmd, expected_kwargs
):
    """New 2026 R1 APDL and POST1 wrappers emit exact APDL strings and forward kwargs."""
    method = getattr(fake_mapdl, method_name)
    result = method(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


@pytest.mark.parametrize(
    ("method_name", "args", "kwargs", "expected_cmd", "expected_kwargs"),
    [
        ("vec", (), {}, "*VEC,,,,,,,,", {}),
        (
            "vec",
            ("MYVEC", "D", "IMPORT", "RST", "file.rst", 1, "", "NSL"),
            {"mute": True},
            "*VEC,MYVEC,D,IMPORT,RST,file.rst,1,,NSL",
            {"mute": True},
        ),
        ("vec", (), {"val5": "RF"}, "*VEC,,,,,,,,RF", {}),
        ("bfint", (), {}, "BFINT,,,,,,,,,,,,", {}),
        (
            "bfint",
            ("f1", "node", "f2", "bfin", 0, "BF1", 0, 0.5, 1e-4, "UNBLOCKED"),
            {"write_to_log": False},
            "BFINT,f1,node,,f2,bfin,,0,BF1,0,0.5,0.0001,UNBLOCKED",
            {"write_to_log": False},
        ),
        ("bfint", (), {"fmat": "BLOCKED"}, "BFINT,,,,,,,,,,,,BLOCKED", {}),
        ("reswrite", (), {}, "RESWRITE,,,,,,", {}),
        (
            "reswrite",
            ("combined", 1, 1),
            {"mute": False},
            "RESWRITE,combined,,,,1,1",
            {"mute": False},
        ),
        ("reswrite", (), {"gflag": 1}, "RESWRITE,,,,,,1", {}),
    ],
)
def test_updated_apdl_post1_commands_2026r1(
    fake_mapdl, method_name, args, kwargs, expected_cmd, expected_kwargs
):
    """Updated 2026 R1 APDL and POST1 wrappers expose trailing args in exact slots."""
    method = getattr(fake_mapdl, method_name)
    result = method(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


def test_apdl_post1_explicit_slots_and_xpl_property_non_collision(fake_mapdl):
    """Verify 1-based APDL comma slots and that starxpl does not shadow MapdlGrpc.xpl."""
    import inspect

    from ansys.mapdl.core._commands.apdl.matrix_operations import MatrixOperations
    from ansys.mapdl.core._commands.post1.special_purpose import SpecialPurpose
    from ansys.mapdl.core.mapdl_extended import _MapdlExtended
    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

    assert "kron" in MatrixOperations.__dict__
    assert "starxpl" in MatrixOperations.__dict__
    assert "maxcycmode" in SpecialPurpose.__dict__

    # MapdlGrpc.xpl must remain an unshadowed property descriptor while starxpl is callable
    assert isinstance(inspect.getattr_static(MapdlGrpc, "xpl"), property)
    assert callable(getattr(_MapdlExtended, "starxpl", None))
    assert callable(getattr(MapdlGrpc, "starxpl", None))
    assert callable(fake_mapdl.starxpl)

    vec_fields = fake_mapdl.vec(val5="V8").removeprefix("OUT:").split(",")
    assert vec_fields[0] == "*VEC"
    assert len(vec_fields) == 9
    assert vec_fields[8] == "V8"

    bfint_fields = fake_mapdl.bfint(fmat="F12").removeprefix("OUT:").split(",")
    assert bfint_fields[0] == "BFINT"
    assert len(bfint_fields) == 13
    assert bfint_fields[3] == ""
    assert bfint_fields[6] == ""
    assert bfint_fields[12] == "F12"

    reswrite_fields = fake_mapdl.reswrite("fn", 0, "G6").removeprefix("OUT:").split(",")
    assert reswrite_fields == ["RESWRITE", "fn", "", "", "", "0", "G6"]


@pytest.mark.parametrize(
    "cmd", ["kron", "starxpl", "maxcycmode", "vec", "bfint", "reswrite"]
)
def test_mapdl_commands_reflection_runner_ticket04(fake_mapdl, cmd):
    """Verify Test_MAPDL_commands.test_command passes offline for Ticket 04 wrappers."""
    import test_commands

    runner = test_commands.Test_MAPDL_commands()
    runner.test_command(fake_mapdl, cmd)


# All 19 new Mechanical APDL 2026 R1 Command Wrappers with valid processor and probe args.
_NEW_2026R1_LIVE_CASES: tuple[tuple[str, str, tuple], ...] = (
    # Ticket 01 (Radiosity)
    ("vfdi", "slashsolu", ("STAT",)),
    ("vfup", "slashsolu", ("STAT",)),
    # Ticket 02 (PREP7)
    ("cntgen", "prep7", ()),
    ("eens", "prep7", ()),
    ("fgrad", "prep7", ()),
    ("mshoptim", "prep7", ()),
    ("nsmass", "prep7", ()),
    ("rbgen", "prep7", ()),
    ("sfcgen", "prep7", ()),
    ("tshape", "prep7", ()),
    # Ticket 03 (SOLUTION)
    ("cefilter", "slashsolu", ()),
    ("fval", "slashsolu", ()),
    ("hbmopt", "slashsolu", ()),
    ("prea", "slashsolu", ()),
    ("scconnect", "slashsolu", ()),
    ("wksp", "slashsolu", ()),
    # Ticket 04 (APDL & POST1)
    ("kron", "prep7", ("M1", "M2", "M3")),
    ("starxpl", "prep7", ("WHERE",)),
    ("maxcycmode", "post1", ()),
)


@requires("local")
def test_live_2026r1_commands_recognized(mapdl, cleared):
    """Verify live Mechanical APDL 26.1+ recognizes new 2026 R1 command wrappers."""
    from ansys.mapdl.core.errors import MapdlRuntimeError

    if mapdl.version < 26.1:
        pytest.skip("Requires Mechanical APDL 26.1 or newer.")

    # Ensure Ticket 04's 3 new commands are always present and exercised.
    for required_cmd in ("kron", "starxpl", "maxcycmode"):
        assert hasattr(mapdl, required_cmd), f"Missing {required_cmd} on Mapdl"

    current_proc = None
    exercised: list[str] = []
    for method_name, proc_method, call_args in _NEW_2026R1_LIVE_CASES:
        if not hasattr(mapdl, method_name):
            continue
        if proc_method != current_proc:
            mapdl.finish(mute=True)
            getattr(mapdl, proc_method)(mute=True)
            current_proc = proc_method

        try:
            out = str(getattr(mapdl, method_name)(*call_args, ignore_errors=True))
        except MapdlRuntimeError as exc:
            out = str(exc)

        assert (
            "is not a recognized" not in out.lower()
        ), f"{method_name} was not recognized by Mechanical APDL 26.1+: {out}"
        exercised.append(method_name)

    assert {"kron", "starxpl", "maxcycmode"}.issubset(exercised)
