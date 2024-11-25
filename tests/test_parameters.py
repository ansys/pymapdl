# Copyright (C) 2016 - 2024 ANSYS, Inc. and/or its affiliates.
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

import numpy as np
import pytest

from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.parameters import interp_star_status

parm_status = """PARAMETER STATUS- PORT  (     12 PARAMETERS DEFINED)
                  (INCLUDING        3 INTERNAL PARAMETERS)

 NAME                              VALUE                        TYPE  DIMENSIONS
 PORT                              50054.0000                  SCALAR"""

arr_status = """PARAMETER STATUS- ASDF  (      5 PARAMETERS DEFINED)
                  (INCLUDING        3 INTERNAL PARAMETERS)

      LOCATION                VALUE
        1       1       1    1.00000000
        2       1       1    2.00000000
        3       1       1    3.00000000
        4       1       1    4.00000000"""

arr3d_status = """
PARAMETER STATUS- MYARR  (      6 PARAMETERS DEFINED)
                  (INCLUDING        3 INTERNAL PARAMETERS)

      LOCATION                VALUE
        1       1       1    1.00000000
        2       1       1    1.00000000
        3       1       1    2.00000000
        1       2       1    0.00000000
        2       2       1    0.00000000
        3       2       1    0.00000000
        1       3       1    0.00000000
        2       3       1    0.00000000
        3       3       1    0.00000000
        1       1       2    1.00000000
        2       1       2    2.00000000
        3       1       2    3.00000000
        1       2       2    0.00000000
        2       2       2    0.00000000
        3       2       2    0.00000000
        1       3       2    0.00000000
        2       3       2    0.00000000
        3       3       2    0.00000000
        1       1       3    1.00000000
        2       1       3    2.00000000
        3       1       3    3.00000000
        1       2       3    1.00000000
        2       2       3    2.00000000
        3       2       3    3.00000000
        1       3       3    0.00000000
        2       3       3    0.00000000
        3       3       3    0.00000000"""

strarr_status = """PARAMETER STATUS- MYSTR3  (     12 PARAMETERS DEFINED)
                  (INCLUDING        3 INTERNAL PARAMETERS)
       96       1       1  aqzzzxcv zx zxcv   zxcv

       96       2       1  qwer wer qwer

       96       3       1  zxcv"""

gen_status = """ABBREVIATION STATUS-

  ABBREV    STRING
  SAVE_DB   SAVE
  RESUM_DB  RESUME
  QUIT      Fnc_/EXIT
  POWRGRPH  Fnc_/GRAPHICS

 PARAMETER STATUS-           (     12 PARAMETERS DEFINED)
                  (INCLUDING        3 INTERNAL PARAMETERS)

 NAME                              VALUE                        TYPE  DIMENSIONS
 ASDF                                       STRING ARRAY       8       1       1
 MYARR                                             ARRAY       1       1       1
 MYSTR                                      STRING ARRAY      96       3       1
 MYSTR3                                     STRING ARRAY      96       3       1
 PGFZJK_COLDIM                     1.00000000                  SCALAR
 PGFZJK_DIM                        20.0000000                  SCALAR
 PGFZJK_ROWDIM                     20.0000000                  SCALAR
 PORT                              50054.0000                  SCALAR
 STRARRAY                                   STRING ARRAY      96       1       1"""


@pytest.mark.parametrize(
    "number",
    [
        1e11,
        1e21,
        1e31,
        1e41,
        1e51,
        1e61,
    ],
)
def test__get_parameter_array(mapdl, cleared, number):
    name = "param_array"

    # Testing 1D arrays
    shape = (100,)
    array = np.ones(shape) * number
    mapdl.load_array(name=name, array=array)
    assert np.allclose(array, mapdl.parameters._get_parameter_array(name, shape))

    # Testing 2D arrays
    shape = (100, 5)
    array = np.ones(shape) * number
    mapdl.load_array(name=name, array=array)
    assert np.allclose(array, mapdl.parameters._get_parameter_array(name, shape))

    # High number
    with pytest.raises(MapdlRuntimeError):
        shape = (100, 100)
        array = np.ones(shape) * number
        mapdl.load_array(name=name, array=array)
        mapdl.parameters._get_parameter_array(name, shape)


def parameters_name(mapdl, func, par_name):
    if "_array2d_" in par_name:
        mapdl.dim("_array2d_", "array", 2, 2)

    if "array3d_" in par_name:
        mapdl.dim("array3d_", "array", 2, 2, 2)

    if func == "run":
        mapdl.run(f"{par_name} = 17.0")

    elif func == "get":
        mapdl.prep7()
        mapdl.get(par_name, "active", 0, "rout")  # it should return 17

    elif func == "_check_parameter_name":
        mapdl._check_parameter_name(par_name)
        return True

    elif func == "parameters":
        mapdl.parameters[par_name] = 17.0

    if not re.search(r"[\(|\)]", par_name) and not re.search(r"_.*_", par_name):
        # Avoiding check if indexing or starting and ending with _.
        assert mapdl.parameters[par_name]
        assert isinstance(mapdl.parameters[par_name], float)


# We use also 'run' and 'get' to be more confident.
@pytest.mark.parametrize("func", ["run", "get", "_check_parameter_name", "parameters"])
@pytest.mark.parametrize(
    "par_name",
    [
        "asdf124",
        "asd",
        "a12345",
        "a12345_",
        "_a12345_",
        "_array2d_(1,1)",
        "array3d_(1,1,1)",
    ],
)
def test_parameters_name(mapdl, cleared, func, par_name):
    parameters_name(mapdl, func, par_name)


# We use also 'run' and 'get' to be more confident.
@pytest.mark.parametrize("func", ["run", "get", "_check_parameter_name", "parameters"])
@pytest.mark.parametrize(
    "par_name",
    [
        pytest.param(
            "_a12345",
            id="Starting by underscore, but not ending",
        ),
        pytest.param(
            "_asdf(1)_",
            id="Indexing before underscore",
        ),
        pytest.param(
            "_a12345",
            id="Starting by underscore, but not ending",
        ),
        pytest.param(
            "_array2d(1,1)",
            id="Starting by underscore, but not ending",
        ),
        pytest.param("1asdf", id="Starting by number"),
        pytest.param("123asdf", id="Starting by several numbers"),
        pytest.param(
            "asa12df+",
            id="Invalid symbol in parameter name.",
        ),
        # function args
        pytest.param(
            "AR0",
            id="Using `AR0` with is reserved for functions/macros",
        ),
        pytest.param(
            "AR1",
            id="Using `AR1` with is reserved for functions/macros",
        ),
        pytest.param(
            "AR10",
            id="Using `AR10` with is reserved for functions/macros",
        ),
        pytest.param(
            "AR99",
            id="Using `AR99` with is reserved for functions/macros",
        ),
        pytest.param(
            "AR111",
            id="Using `AR111` with is reserved for functions/macros",
        ),
        pytest.param(
            "AR999",
            id="Using `AR999` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG0",
            id="Using `ARG0` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG1",
            id="Using `ARG1` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG10",
            id="Using `ARG10` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG99",
            id="Using `ARG99` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG111",
            id="Using `ARG111` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG999",
            id="Using `ARG999` with is reserved for functions/macros",
        ),
        # length
        pytest.param(
            "a23456789012345678901234567890123",
            id="Name too long",
        ),
        pytest.param(
            "aasdf234asdf5678901-2345",
            id="Not valid sign -",
        ),
        pytest.param(
            "aasdf234asdf5678901+2345",
            id="Not valid sign +",
        ),
        pytest.param(
            "aasdf234a?sdf5678901?2345",
            id="Not valid sign ?",
        ),
    ],
)
def test_parameters_name_error(mapdl, cleared, func, par_name):
    with pytest.raises(ValueError):
        parameters_name(mapdl, func, par_name)


def test_contain_iter(mapdl, cleared):
    mapdl.finish()  # to check that #1107 is solved
    mapdl.parameters["TWO"] = 2.0
    assert 2.0 == mapdl.parameters["TWO"]
    assert "TWO" in mapdl.parameters

    # iter
    mapdl.parameters["THREE"] = 3.0
    assert hasattr(mapdl.parameters, "__iter__")
    assert sorted(["TWO", "THREE"]) == [each for each in mapdl.parameters]


@pytest.mark.parametrize("number", [1 / 3, 1 / 7, 0.0181681816816816168168168])
def test_double_parameter_get(mapdl, number, cleared):
    # Running grpc method
    mapdl.parameters["value"] = number

    precision_single = 9
    precision_double = 12
    assert np.around(mapdl.parameters["value"], precision_single) == np.around(
        number, precision_single
    )
    assert np.around(mapdl.parameters["value"], precision_double) == np.around(
        number, precision_double
    )

    # to use the alternative method (single precision)
    mapdl_name = mapdl._name
    mapdl._name = "dummy"
    assert np.around(mapdl.parameters["value"], precision_single) == np.around(
        number, precision_single
    )
    assert np.around(mapdl.parameters["value"], precision_double) != np.around(
        number, precision_double
    )
    mapdl._name = mapdl_name


def test_parameter_delete_raise(mapdl, cleared):
    with pytest.raises(KeyError, match="does not exist"):
        del mapdl.parameters["not-a-parm"]


@pytest.mark.parametrize(
    "status,check",
    [
        (parm_status, 50054),
        (arr_status, np.array([1, 2, 3, 4])),
        (
            arr3d_status,
            np.array(
                [
                    [[1.0, 1.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]],
                    [[1.0, 2.0, 2.0], [0.0, 0.0, 2.0], [0.0, 0.0, 0.0]],
                    [[2.0, 3.0, 3.0], [0.0, 0.0, 3.0], [0.0, 0.0, 0.0]],
                ]
            ),
        ),
        (strarr_status, ["aqzzzxcv zx zxcv   zxcv", "qwer wer qwer", "zxcv"]),
        (gen_status, None),
    ],
)
def test_interp_star_status(status, check):
    output = interp_star_status(status)
    if len(output) == 1:
        name = list(output.keys())[0]
        if name == "MYARR" or name == "ASDF":
            assert np.all(output[name]["value"] == check)
        else:
            assert output[name]["value"] == check
    else:
        assert "MYARR" in output
        assert "PGFZJK_COLDIM" in output
        assert output["PGFZJK_COLDIM"]["value"] == 1.0
        assert "PGFZJK_DIM" in output
        assert output["PGFZJK_DIM"]["value"] == 20.0
        assert "PGFZJK_ROWDIM" in output
        assert output["PGFZJK_ROWDIM"]["value"] == 20.0
        assert "PORT" in output
        assert output["PORT"]["value"] == 50054.0


def test_str_arrays(mapdl, cleared):
    mapdl.run("*dim, mystrarr, string, 80")
    mapdl.run("mystrarr(1) = 'hello there!'")

    assert mapdl.parameters["mystrarr"] == "hello there!"

    mapdl.run("*dim, mystrarr, string, 80, 2")
    mapdl.run("mystrarr(1,1) = 'hello there!'")
    mapdl.run("mystrarr(1,2) = 'General Kenobi, you are a bold one!'")

    assert mapdl.parameters["mystrarr"] == [
        "hello there!",
        "General Kenobi, you are a bold one!",
    ]


def test_3d_array(mapdl, cleared):
    mapdl.dim("myarr", "array", 2, 2, 2)
    mapdl.run("myarr(1,1,1)= 100")
    mapdl.run("myarr(1,1,2)= 200")
    mapdl.run("myarr(1,2,2)= 300")
    mapdl.run("myarr(2,1,2)= 400")

    assert np.allclose(
        mapdl.parameters["myarr"],
        np.array([[[100.0, 200.0], [0.0, 300.0]], [[0.0, 400.0], [0.0, 0.0]]]),
    )


def test_parameter_with_spaces(mapdl, cleared):
    string_ = "DEV:F10X, front weights     "
    mapdl.run(f"*SET,SIMULATION,'{string_}'")
    mapdl.parsav()
    mapdl.clear()
    mapdl.parres("NEW", fname="file", ext="parm")
    assert mapdl.starstatus()
    assert mapdl.parameters
    assert "SIMULATION" in mapdl.parameters
    assert string_.strip() == mapdl.parameters["SIMULATION"]


def test_parameters_keys(mapdl, cleared):
    mapdl.parameters["MYPAR"] = 1234

    assert "MYPAR" in list(mapdl.parameters.keys())
    assert mapdl.parameters.keys() is not None
    assert mapdl.parameters["MYPAR"] == 1234


def test_parameters_values(mapdl, cleared):
    mapdl.parameters["MYPAR"] = 9876

    assert 9876 == list(mapdl.parameters.values())[0]["value"]
    assert mapdl.parameters["MYPAR"] == 9876


def test_parameters_copy(mapdl, cleared):
    mapdl.parameters["MYPAR"] = 9876

    copy = mapdl.parameters.copy()
    assert isinstance(copy, dict)
    assert copy["MYPAR"]["value"] == 9876


def test_parameters_items(mapdl, cleared):
    mapdl.parameters["MYPAR"] = 9876

    for each_key, each_item in mapdl.parameters.items():
        assert each_key == "MYPAR"
        assert each_item["value"] == 9876


def test_parameter_contains(mapdl, cleared):
    mapdl.parameters["mypar"] = 9876

    assert "mypar" in mapdl.parameters


def test_non_existing_parameter(mapdl, cleared):
    with pytest.raises(KeyError):
        mapdl.parameters["A"]


def test_non_interactive(mapdl, cleared):
    mapdl.parameters["asdf"] = 2
    with pytest.raises(MapdlRuntimeError):
        with mapdl.non_interactive:
            par = mapdl.parameters["asdf"]

    with mapdl.non_interactive:
        mapdl.parameters["qwer"] = 3

    assert mapdl.parameters["qwer"] == 3
