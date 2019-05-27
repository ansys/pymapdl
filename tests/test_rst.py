import numpy as np
import pytest
from pyvista.plotting import system_supports_plotting

import pyansys

try:
    vm33 = pyansys.download_verification_result(33)
except:
    vm33 = None


try:
    pontoon = pyansys.download_pontoon()
except:
    pontoon = None

@pytest.mark.skipif(vm33 is None, reason="Requires example files")
def test_nodal_thermal_strain():
    _, tstrain = vm33.nodal_thermal_strain(0)
    assert np.any(tstrain)
    assert tstrain.shape == (vm33.grid.n_points, 8)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(vm33 is None, reason="Requires example files")
def test_plot_nodal_thermal_strain():
    vm33.plot_nodal_thermal_strain(0, 'X', off_screen=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(vm33 is None, reason="Requires example files")
def test_plot_nodal_thermal_strain():
    vm33._animate_time_solution('ENS', off_screen=True)


@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_nodal_elastic_strain():
    _, estrain = pontoon.nodal_elastic_strain(0)
    assert np.any(estrain)
    assert estrain.shape == (pontoon.grid.n_points, 7)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_plot_nodal_elastic_strain():
    pontoon.plot_nodal_elastic_strain(0, 'X', off_screen=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_plot_pontoon():
    pontoon.plot(off_screen=True)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_plot_pontoon_nodal_displacement():
    pontoon.plot_nodal_solution(0, show_displacement=True, max_disp=10,
                                overlay_wireframe=True, off_screen=True)


@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_print_pontoon_components():
    assert isinstance(pontoon.node_components, dict)


@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_repr():
    assert 'Title' in str(pontoon)


@pytest.mark.skipif(pontoon is None, reason="Requires example files")
def test_available_results():
    assert 'ENS' in pontoon.available_results
