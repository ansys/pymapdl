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

"""Tests for Mechanical APDL 2026 R1 radiosity command wrappers (Ticket 01)."""

import pytest

from conftest import requires


def test_reflection_runner_handles_keyword_only_parameters(fake_mapdl):
    """Test_MAPDL_commands.test_command passes keyword-only args by keyword."""
    import test_commands

    def sample(self, a: str = "", b: str = "", *, mid: str = "", **kwargs):
        return self.run(f"SAMPLE,{a},{mid},{b}", **kwargs)

    fake_mapdl.sample = sample.__get__(fake_mapdl, type(fake_mapdl))
    runner = test_commands.Test_MAPDL_commands()
    runner.test_command(fake_mapdl, "sample")
    assert fake_mapdl.sent_commands == ["SAMPLE,arg0,arg2,arg1"]


@pytest.mark.parametrize(
    ("method_name", "args", "kwargs", "expected_cmd", "expected_kwargs"),
    [
        ("vfup", (), {}, "VFUP,,,,,", {}),
        (
            "vfup",
            ("DEFINE", "KNIM", 0.1, 0, 0.05),
            {"mute": True},
            "VFUP,DEFINE,KNIM,0.1,0,0.05",
            {"mute": True},
        ),
        (
            "vfup",
            (),
            {"action": "DEFINE", "opt": "FRQU", "opt2": 3, "opt3": 0},
            "VFUP,DEFINE,FRQU,3,0,",
            {},
        ),
        ("vfdi", (), {}, "VFDI,,,,,", {}),
        (
            "vfdi",
            (3, 1, 1, -0.01, 1.1),
            {"write_to_log": False},
            "VFDI,3,1,1,-0.01,1.1",
            {"write_to_log": False},
        ),
        (
            "vfdi",
            (),
            {"opt": "STAT", "enclosure": 2},
            "VFDI,STAT,2,,,",
            {},
        ),
    ],
)
def test_new_radiosity_commands_2026r1(
    fake_mapdl, method_name, args, kwargs, expected_cmd, expected_kwargs
):
    """New 2026 R1 radiosity wrappers emit exact APDL strings and forward kwargs."""
    method = getattr(fake_mapdl, method_name)
    result = method(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


@pytest.mark.parametrize(
    ("method_name", "args", "kwargs", "expected_cmd", "expected_kwargs"),
    [
        ("rsurf", (), {}, "RSURF,,,,", {}),
        (
            "rsurf",
            ("DEFINE", "", 2, 1),
            {"mute": True},
            "RSURF,DEFINE,,2,1",
            {"mute": True},
        ),
        ("rsurf", (), {"dkey": 1}, "RSURF,,,,1", {}),
        ("radopt", (), {}, "RADOPT,,,,,,,,,,,,,", {}),
        (
            "radopt",
            (1e-4, 2, 500, 0.05, 0.1, 10, 1, "ON"),
            {},
            "RADOPT,,0.0001,2,500,0.05,0.1,,,,,10,1,ON",
            {},
        ),
        (
            "radopt",
            (),
            {"stabilization": "AUTO", "write_to_log": False},
            "RADOPT,,,,,,,,,,,,,AUTO",
            {"write_to_log": False},
        ),
        ("rsymm", (), {}, "RSYMM,,,,,,,,", {}),
        (
            "rsymm",
            ("DEFINE", 0, "ZEXT", 4, "OFF", 0.0, 10.0, 1e-5),
            {},
            "RSYMM,DEFINE,0,ZEXT,4,OFF,0.0,10.0,1e-05",
            {},
        ),
        ("rsymm", (), {"toler": 1e-6}, "RSYMM,,,,,,,,1e-06", {}),
        ("vfquery", (), {}, "VFQUERY,,,,", {}),
        (
            "vfquery",
            ("SRC_CM", "TAR_CM", "WRIT"),
            {"mute": False},
            "VFQUERY,SRC_CM,TAR_CM,,WRIT",
            {"mute": False},
        ),
        ("vfquery", (), {"wropt": 1}, "VFQUERY,,,,1", {}),
    ],
)
def test_updated_radiosity_commands_2026r1(
    fake_mapdl, method_name, args, kwargs, expected_cmd, expected_kwargs
):
    """Updated 2026 R1 radiosity wrappers expose trailing args in exact APDL slots."""
    method = getattr(fake_mapdl, method_name)
    result = method(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


def test_radiosity_explicit_slot_positions_and_single_mixin_ownership(fake_mapdl):
    """Verify 1-based APDL comma slots and single-mixin ownership for vfup/vfdi."""
    from ansys.mapdl.core._commands.aux12.radiosity_solver import RadiositySolver
    from ansys.mapdl.core._commands.solution.radiosity import Radiosity

    assert "vfup" in Radiosity.__dict__
    assert "vfdi" in Radiosity.__dict__
    assert "vfup" not in RadiositySolver.__dict__
    assert "vfdi" not in RadiositySolver.__dict__

    radopt_fields = (
        fake_mapdl.radopt(stabilization="S13").removeprefix("OUT:").split(",")
    )
    assert radopt_fields[0] == "RADOPT"
    assert radopt_fields[13] == "S13"

    vfquery_fields = (
        fake_mapdl.vfquery("SRC", "TAR", "W4").removeprefix("OUT:").split(",")
    )
    assert vfquery_fields == ["VFQUERY", "SRC", "TAR", "", "W4"]


@requires("local")
def test_live_radiosity_commands_recognized_2026r1(mapdl, cleared):
    """Verify live Mechanical APDL 26.1+ recognizes vfup and vfdi in /SOLU."""
    if mapdl.version < 26.1:
        pytest.skip("Requires Mechanical APDL 26.1 or newer.")
    mapdl.slashsolu()
    for out in (mapdl.vfup("STAT"), mapdl.vfdi("STAT")):
        assert "is not a recognized" not in str(out)
