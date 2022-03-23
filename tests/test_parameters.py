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
