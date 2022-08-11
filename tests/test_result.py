"""Test DPF implementation of Result class."""
import numpy as np
import pytest

from ansys.mapdl.core.examples import static_coupled_thermal


@pytest.fixture(scope="session")
def static_thermocoupled_example(mapdl):
    mapdl.clear()
    mapdl.input(static_coupled_thermal)
    mapdl.post1()
    yield mapdl  # will reuse the simulation


def test_DPF_result_class(mapdl, static_thermocoupled_example):
    from ansys.mapdl.core.reader.result import DPFResult

    assert isinstance(mapdl.result, DPFResult)


@pytest.mark.parametrize(
    "method",
    [
        "nodal_displacement",
        "nodal_elastic_strain",
        "nodal_plastic_strain",
        "nodal_acceleration",
        "nodal_reaction_forces",
        "nodal_stress",
        "nodal_temperature",
        "nodal_thermal_strain",
        "nodal_velocity",
        "nodal_static_forces",
    ],
)
def test_result_methods(mapdl, static_thermocoupled_example, method):
    try:
        res = getattr(mapdl.result, method)(0)
    except ValueError:
        pass


@pytest.mark.parametrize("set_", list(range(0, 10)))  # lowercase intentional
def test_compatibility_post_processing_nodal_temperature(
    mapdl, static_thermocoupled_example, set_
):
    mapdl.set(1, set_)
    post_values = mapdl.post_processing.nodal_temperature()
    result_values = mapdl.result.nodal_temperature(set_ - 1)[1]
    assert np.allclose(post_values, result_values)


@pytest.mark.parametrize("set_", list(range(0, 10)))  # lowercase intentional
def test_compatibility_post_processing_nodal_displacement(
    mapdl, static_thermocoupled_example, set_
):
    mapdl.set(1, set_)
    post_values = mapdl.post_processing.nodal_displacement("all")
    result_values = mapdl.result.nodal_displacement(set_ - 1)[1][:, :3]
    assert np.allclose(post_values, result_values)


@pytest.mark.parametrize("set_", [0, 1, 2])  # lowercase intentional
def test_thermocoupled_example(mapdl, static_thermocoupled_example, set_):
    """functional tests against vm33.

    Solutions on node 0 and node 90 are tested against hardcode values."""
    # For the post_processing module.
    mapdl.post1()
    mapdl.set(1, 1)

    # nodal displacement
    assert mapdl.result.nodal_displacement(0)
    assert np.allclose(
        mapdl.result.nodal_displacement(0)[1][
            :, :3
        ],  # results retrieve also the TEMP DOF.
        mapdl.post_processing.nodal_displacement("all"),
    )
    node = 0
    assert np.allclose(
        mapdl.result.nodal_displacement(0)[1][node],
        np.array(
            [6.552423219981545e-07, 2.860849760514619e-08, 0.0, 69.99904527958618]
        ),
    )
    node = 90
    assert np.allclose(
        mapdl.result.nodal_displacement(0)[1][node],
        np.array([5.13308913e-07, -2.24115511e-08, 0.00000000e00, 6.99990455e01]),
    )

    # nodal temperatures
    assert mapdl.result.nodal_temperature(0)
    node = 0
    assert np.allclose(
        mapdl.result.nodal_temperature(0)[1][node], np.array([69.9990463256836])
    )
    node = 90
    assert np.allclose(
        mapdl.result.nodal_temperature(0)[1][node], np.array([69.9990463256836])
    )
    assert np.allclose(
        mapdl.result.nodal_temperature(0)[1], mapdl.post_processing.nodal_temperature()
    )
