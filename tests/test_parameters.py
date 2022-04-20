import re

import numpy as np
import pytest


@pytest.mark.parametrize(
    "number",
    [
        1e11,
        1e21,
        1e31,
        1e41,
        1e51,
        pytest.param(1e61, marks=pytest.mark.xfail),
    ],
)
def test__get_parameter_array(mapdl, number):
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
    with pytest.raises(RuntimeError):
        shape = (100, 100)
        array = np.ones(shape) * number
        mapdl.load_array(name=name, array=array)
        mapdl.parameters._get_parameter_array(name, shape)


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
        pytest.param(
            "_a12345",
            marks=pytest.mark.xfail,
            id="Starting by underscore, but not ending",
        ),
        pytest.param(
            "_asdf(1)_",
            marks=pytest.mark.xfail,
            id="Indexing before underscore",
        ),
        pytest.param(
            "_a12345",
            marks=pytest.mark.xfail,
            id="Starting by underscore, but not ending",
        ),
        pytest.param(
            "_array2d(1,1)",
            marks=pytest.mark.xfail,
            id="Starting by underscore, but not ending",
        ),
        pytest.param("1asdf", marks=pytest.mark.xfail, id="Starting by number"),
        pytest.param(
            "123asdf", marks=pytest.mark.xfail, id="Starting by several numbers"
        ),
        pytest.param(
            "asa12df+", marks=pytest.mark.xfail, id="Invalid symbol in parameter name."
        ),
        # function args
        pytest.param(
            "AR0",
            marks=pytest.mark.xfail,
            id="Using `AR0` with is reserved for functions/macros",
        ),
        pytest.param(
            "AR1",
            marks=pytest.mark.xfail,
            id="Using `AR1` with is reserved for functions/macros",
        ),
        pytest.param(
            "AR10",
            marks=pytest.mark.xfail,
            id="Using `AR10` with is reserved for functions/macros",
        ),
        pytest.param(
            "AR99",
            marks=pytest.mark.xfail,
            id="Using `AR99` with is reserved for functions/macros",
        ),
        pytest.param(
            "AR111",
            marks=pytest.mark.xfail,
            id="Using `AR111` with is reserved for functions/macros",
        ),
        pytest.param(
            "AR999",
            marks=pytest.mark.xfail,
            id="Using `AR999` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG0",
            marks=pytest.mark.xfail,
            id="Using `ARG0` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG1",
            marks=pytest.mark.xfail,
            id="Using `ARG1` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG10",
            marks=pytest.mark.xfail,
            id="Using `ARG10` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG99",
            marks=pytest.mark.xfail,
            id="Using `ARG99` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG111",
            marks=pytest.mark.xfail,
            id="Using `ARG111` with is reserved for functions/macros",
        ),
        pytest.param(
            "ARG999",
            marks=pytest.mark.xfail,
            id="Using `ARG999` with is reserved for functions/macros",
        ),
        # length
        pytest.param(
            "a23456789012345678901234567890123",
            marks=pytest.mark.xfail,
            id="Name too long",
        ),
        pytest.param(
            "aasdf234asdf5678901-2345",
            marks=pytest.mark.xfail,
            id="Not valid sign -",
        ),
        pytest.param(
            "aasdf234asdf5678901+2345",
            marks=pytest.mark.xfail,
            id="Not valid sign +",
        ),
        pytest.param(
            "aasdf234a?sdf5678901?2345",
            marks=pytest.mark.xfail,
            id="Not valid sign ?",
        ),
    ],
)
def test_parameters_name(mapdl, func, par_name):
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

    if not re.search(r"[\(|\)]", par_name):
        assert mapdl.parameters[par_name]
        assert isinstance(mapdl.parameters[par_name], float)
