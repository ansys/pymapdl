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

import inspect
import logging
from unittest.mock import MagicMock

import pytest

from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.mapdl_extended import _MapdlExtended
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc
from conftest import requires
import test_commands


class FakeMapdl(_MapdlExtended):
    """Offline ``Mapdl`` double bypassing ``_MapdlCore.__init__``."""

    def __init__(self) -> None:
        self._do_loop_level = 0
        self._store_commands = False
        self._stored_commands: list[str] = []
        self.sent_commands: list[str] = []
        self.calls: list[tuple[str, dict]] = []
        self._log = MagicMock()
        self._log.logger.level = logging.WARNING

    def run(self, command: str, **kwargs):
        if self._store_commands:
            self._stored_commands.append(command)
            return None
        self.sent_commands.append(command)
        self.calls.append((command, kwargs))
        return f"OUT:{command}"


@pytest.fixture
def fake_mapdl() -> FakeMapdl:
    return FakeMapdl()


ALL_2026R1_COMMANDS: tuple[str, ...] = (
    "vfdi",
    "vfup",
    "cntgen",
    "eens",
    "fgrad",
    "mshoptim",
    "nsmass",
    "rbgen",
    "sfcgen",
    "tshape",
    "cefilter",
    "fval",
    "hbmopt",
    "prea",
    "scconnect",
    "wksp",
    "kron",
    "starxpl",
    "maxcycmode",
    "rsurf",
    "radopt",
    "rsymm",
    "vfquery",
    "cdwrite",
    "cgrow",
    "secdata",
    "swgen",
    "emsel",
    "secmodif",
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
    "vec",
    "bfint",
    "reswrite",
)


def test_reflection_runner_handles_keyword_only_parameters(fake_mapdl: FakeMapdl):
    def sample(self, a: str = "", b: str = "", *, mid: str = "", **kwargs):
        return self.run(f"SAMPLE,{a},{mid},{b}", **kwargs)

    fake_mapdl.sample = sample.__get__(fake_mapdl, type(fake_mapdl))  # type: ignore[attr-defined]
    runner = test_commands.Test_MAPDL_commands()
    runner.test_command(fake_mapdl, "sample")
    assert fake_mapdl.sent_commands == ["SAMPLE,arg0,arg2,arg1"]


@pytest.mark.parametrize("cmd", ALL_2026R1_COMMANDS)
def test_commands_2026r1_pass_reflection_runner(fake_mapdl: FakeMapdl, cmd: str):
    runner = test_commands.Test_MAPDL_commands()
    runner.test_command(fake_mapdl, cmd)


NEW_COMMAND_CASES: tuple[tuple[str, tuple, dict, str, dict], ...] = (
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
    ("vfdi", (), {"opt": "STAT", "enclosure": 2}, "VFDI,STAT,2,,,", {}),
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
    ("mshoptim", (1,), {"mute": True}, "MSHOPTIM,,,1", {"mute": True}),
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
    ("wksp", (-100.0,), {"write_to_log": True}, "WKSP,-100.0", {"write_to_log": True}),
    ("wksp", (), {"value": 1.5}, "WKSP,1.5", {}),
    ("kron", (), {}, "*KRON,,,", {}),
    (
        "kron",
        ("MAT_A", "MAT_B", "MAT_C"),
        {"mute": True},
        "*KRON,MAT_A,MAT_B,MAT_C",
        {"mute": True},
    ),
    ("kron", (), {"m1": "V1", "m2": "V2", "m3": "VOUT"}, "*KRON,V1,V2,VOUT", {}),
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
)


@pytest.mark.parametrize(
    ("method_name", "args", "kwargs", "expected_cmd", "expected_kwargs"),
    NEW_COMMAND_CASES,
)
def test_new_commands_2026r1(
    fake_mapdl: FakeMapdl,
    method_name: str,
    args: tuple,
    kwargs: dict,
    expected_cmd: str,
    expected_kwargs: dict,
):
    method = getattr(fake_mapdl, method_name)
    result = method(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


UPDATED_COMMAND_CASES: tuple[tuple[str, tuple, dict, str, dict], ...] = (
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
    ("emsel", (), {}, "EMSEL,,,,,,", {}),
    ("emsel", ("S", 1, 10, 1), {"mute": True}, "EMSEL,S,,,1,10,1", {"mute": True}),
    (
        "emsel",
        ("S", 1, 7, 2),
        {"item": "LAYER", "comp": "NUM", "write_to_log": False},
        "EMSEL,S,LAYER,NUM,1,7,2",
        {"write_to_log": False},
    ),
    (
        "emsel",
        (),
        {"type_": "LIST", "item": "LAYER", "comp": "STO"},
        "EMSEL,LIST,LAYER,STO,,,",
        {},
    ),
    (
        "emsel",
        ("S",),
        {"item": "LAYER", "comp": "NAME", "vmin": "PLY1"},
        "EMSEL,S,LAYER,NAME,PLY1,,",
        {},
    ),
    ("secmodif", (), {}, "SECMODIF,,,,,,", {}),
    (
        "secmodif",
        (1, "NORM", 0.0, 1.0, 0.0, 0),
        {"mute": True},
        "SECMODIF,1,NORM,0.0,1.0,0.0,0",
        {"mute": True},
    ),
    (
        "secmodif",
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
    ("ambeam", (2, 250.0, 0.85), {}, "AMBEAM,2,250.0,0.85", {}),
    ("ambeam", (), {"power": 300, "absorptivity": 0.7}, "AMBEAM,,300,0.7", {}),
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
    ("amenv", (25.0, 15.0, 1, 0.8, 5.67e-8), {}, "AMENV,25.0,15.0,1,0.8,5.67e-08", {}),
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
    ("ddele", ("ALL", "UX", 10, 1, "OFF", 1), {}, "DDELE,ALL,UX,10,1,OFF,1", {}),
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
    ("kryopt", (100, 0.01, 1e-9), {}, "KRYOPT,100,,,0.01,1e-09", {}),
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
    ("spopt", ("SPRS", 20, "YES", "NO", "YES"), {}, "SPOPT,SPRS,20,YES,NO,YES", {}),
    ("spopt", (), {"speccum": "YES"}, "SPOPT,,,,,YES", {}),
    ("tintp", (), {}, "TINTP,,,,,,,,,,,", {}),
    (
        "tintp",
        (0.005, 0.25, 0.5, 1.0, 0.5, 0.01, 1, 0.005, 0.0),
        {"mute": True},
        "TINTP,0.005,0.25,0.5,1.0,0.5,0.01,,,1,0.005,0.0",
        {"mute": True},
    ),
    (
        "tintp",
        (0.005, 0.25, 0.5, 1.0, 0.5, 0.01, 1, 0.005, 0.0),
        {"oslm2": 20},
        "TINTP,0.005,0.25,0.5,1.0,0.5,0.01,20,,1,0.005,0.0",
        {},
    ),
    ("pcgopt", (), {}, "PCGOPT,,,,,,,", {}),
    (
        "pcgopt",
        ("AUTO", "ON", "YES", "OFF", "ON", "ON"),
        {"write_to_log": False},
        "PCGOPT,AUTO,ON,YES,OFF,ON,,ON",
        {"write_to_log": False},
    ),
    ("pcgopt", (), {"lm_key": "OFF"}, "PCGOPT,,,,,,,OFF", {}),
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
)


@pytest.mark.parametrize(
    ("method_name", "args", "kwargs", "expected_cmd", "expected_kwargs"),
    UPDATED_COMMAND_CASES,
)
def test_updated_commands_2026r1(
    fake_mapdl: FakeMapdl,
    method_name: str,
    args: tuple,
    kwargs: dict,
    expected_cmd: str,
    expected_kwargs: dict,
):
    method = getattr(fake_mapdl, method_name)
    result = method(*args, **kwargs)
    assert result == f"OUT:{expected_cmd}"
    assert fake_mapdl.calls == [(expected_cmd, expected_kwargs)]


def test_explicit_1based_apdl_comma_slots(fake_mapdl: FakeMapdl):
    assert fake_mapdl.eens("ALL", "fn", 1).removeprefix("OUT:").split(",") == [
        "EENS",
        "ALL",
        "fn",
        "",
        "1",
    ]
    assert fake_mapdl.mshoptim(1).removeprefix("OUT:").split(",") == [
        "MSHOPTIM",
        "",
        "",
        "1",
    ]

    radopt_fields = (
        fake_mapdl.radopt(stabilization="S13").removeprefix("OUT:").split(",")
    )
    assert radopt_fields[0] == "RADOPT"
    assert radopt_fields[13] == "S13"

    assert fake_mapdl.vfquery("SRC", "TAR", "W4").removeprefix("OUT:").split(",") == [
        "VFQUERY",
        "SRC",
        "TAR",
        "",
        "W4",
    ]

    cdwrite_fields = fake_mapdl.cdwrite(key="DUPL").removeprefix("OUT:").split(",")
    assert cdwrite_fields[0] == "CDWRITE"
    assert cdwrite_fields[4] == ""
    assert cdwrite_fields[8] == ""
    assert cdwrite_fields[9] == "DUPL"

    secdata_fields = (
        fake_mapdl.secdata(val13="A", val14="B").removeprefix("OUT:").split(",")
    )
    assert secdata_fields[13] == "A"
    assert secdata_fields[14] == "B"

    swgen_fields = fake_mapdl.swgen(algo="LAGR").removeprefix("OUT:").split(",")
    assert swgen_fields[13] == "LAGR"

    pcgopt_fields = (
        fake_mapdl.pcgopt("AUTO", "ON", "YES", "OFF", "ON", "ON")
        .removeprefix("OUT:")
        .split(",")
    )
    assert pcgopt_fields == ["PCGOPT", "AUTO", "ON", "YES", "OFF", "ON", "", "ON"]

    awave_fields = fake_mapdl.awave(kcn="K18").removeprefix("OUT:").split(",")
    assert len(awave_fields) == 19
    assert awave_fields[18] == "K18"

    assert fake_mapdl.ddele(irstrtflag="R6").removeprefix("OUT:").split(",") == [
        "DDELE",
        "",
        "",
        "",
        "",
        "",
        "R6",
    ]
    assert fake_mapdl.ic(lsic="LSIC").removeprefix("OUT:").split(",") == [
        "IC",
        "",
        "",
        "",
        "",
        "",
        "",
        "LSIC",
    ]
    assert fake_mapdl.kryopt(orthtol="O5").removeprefix("OUT:").split(",") == [
        "KRYOPT",
        "",
        "",
        "",
        "",
        "O5",
    ]
    assert fake_mapdl.seopt(seedgekey="E9").removeprefix("OUT:").split(",") == [
        "SEOPT",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "E9",
    ]

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

    assert fake_mapdl.reswrite("fn", 0, "G6").removeprefix("OUT:").split(",") == [
        "RESWRITE",
        "fn",
        "",
        "",
        "",
        "0",
        "G6",
    ]


def test_keyword_only_mid_slot_compatibility_emsel_and_tintp(fake_mapdl: FakeMapdl):
    with pytest.raises(TypeError):
        fake_mapdl.emsel("S", "LAYER", "NUM", 1, 10, 1)

    with pytest.raises(TypeError):
        fake_mapdl.tintp(0.005, 0.25, 0.5, 1.0, 0.5, 0.01, 1, 0.005, 0.0, 20)

    tintp_fields = (
        fake_mapdl.tintp(0.005, 0.25, 0.5, 1.0, 0.5, 0.01, 1, 0.005, 0.0, oslm2=20)
        .removeprefix("OUT:")
        .split(",")
    )
    assert tintp_fields[7] == "20"
    assert tintp_fields[8] == ""
    assert tintp_fields[9:] == ["1", "0.005", "0.0"]


def test_secmodif_legacy_addional_command_arg_deprecation_and_conflict(
    fake_mapdl: FakeMapdl,
):
    with pytest.deprecated_call(match=r"0\.77\.0"):
        result = fake_mapdl.secmodif(1, "NAME", addional_command_arg="PRET1", mute=True)
    assert result == "OUT:SECMODIF,1,NAME,PRET1,,,"
    assert fake_mapdl.calls == [("SECMODIF,1,NAME,PRET1,,,", {"mute": True})]

    fake_mapdl.calls.clear()
    with pytest.raises(TypeError, match="addional_command_arg"):
        fake_mapdl.secmodif(
            1, "NAME", value1="NEW_NAME", addional_command_arg="OLD_NAME"
        )
    assert fake_mapdl.calls == []

    with pytest.raises(TypeError, match="addional_command_arg"):
        fake_mapdl.secmodif(1, "NAME", "NEW_NAME", addional_command_arg="OLD_NAME")
    assert fake_mapdl.calls == []


def test_tshap_archived_command_remains_active_without_deprecation(
    fake_mapdl: FakeMapdl,
):
    fake_mapdl._version = 26.1
    assert fake_mapdl.version == 26.1
    result = fake_mapdl.tshap("PILO", mute=True)
    assert result == "OUT:TSHAP,PILO"
    assert fake_mapdl.calls == [("TSHAP,PILO", {"mute": True})]


def test_starxpl_does_not_shadow_mapdl_grpc_xpl_property(fake_mapdl: FakeMapdl):
    assert isinstance(inspect.getattr_static(MapdlGrpc, "xpl"), property)
    assert callable(getattr(_MapdlExtended, "starxpl", None))
    assert callable(getattr(MapdlGrpc, "starxpl", None))
    assert callable(fake_mapdl.starxpl)


_NEW_2026R1_LIVE_CASES: tuple[tuple[str, str, tuple], ...] = (
    ("vfdi", "slashsolu", ("STAT",)),
    ("vfup", "slashsolu", ("STAT",)),
    ("cntgen", "prep7", ()),
    ("eens", "prep7", ()),
    ("fgrad", "prep7", ()),
    ("mshoptim", "prep7", ()),
    ("nsmass", "prep7", ()),
    ("rbgen", "prep7", ()),
    ("sfcgen", "prep7", ()),
    ("tshape", "prep7", ()),
    ("cefilter", "slashsolu", ()),
    ("fval", "slashsolu", ()),
    ("hbmopt", "slashsolu", ()),
    ("prea", "slashsolu", ()),
    ("scconnect", "slashsolu", ()),
    ("wksp", "slashsolu", ()),
    ("kron", "prep7", ("M1", "M2", "M3")),
    ("starxpl", "prep7", ("WHERE",)),
    ("maxcycmode", "post1", ()),
)


@requires("local")
def test_live_2026r1_commands_recognized(mapdl, cleared):
    assert len(_NEW_2026R1_LIVE_CASES) == 19
    for method_name, _, _ in _NEW_2026R1_LIVE_CASES:
        assert hasattr(mapdl, method_name), f"Missing {method_name} on Mapdl"

    if mapdl.version < 26.1:
        return

    current_proc = None
    exercised: list[str] = []
    for method_name, proc_method, call_args in _NEW_2026R1_LIVE_CASES:
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

    assert len(exercised) == 19
