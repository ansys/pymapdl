"""Test post-processing module for ansys.mapdl.core"""
import numpy as np
import pytest

from pyvista.plotting.renderer import CameraPosition

from ansys.mapdl.core import examples
from ansys.mapdl.core.post import (
    COMPONENT_STRESS_TYPE, PRINCIPAL_TYPE, STRESS_TYPES
)


@pytest.fixture(scope="module")
def static_solve(mapdl):
    mapdl.mute = True
    mapdl.finish()
    mapdl.clear()

    # cylinder and mesh parameters
    # torque = 100
    radius = 2
    h_tip = 2
    height = 20
    elemsize = 0.5
    # pi = np.arccos(-1)
    force = 100 / radius
    pressure = force / (h_tip * 2 * np.pi * radius)

    mapdl.prep7()
    mapdl.et(1, 186)
    mapdl.et(2, 154)
    mapdl.r(1)
    mapdl.r(2)

    # Aluminum properties (or something)
    mapdl.mp("ex", 1, 10e6)
    mapdl.mp("nuxy", 1, 0.3)
    mapdl.mp("dens", 1, 0.1 / 386.1)
    mapdl.mp("dens", 2, 0)

    # Simple cylinder
    for i in range(4):
        mapdl.cylind(radius, "", "", height, 90 * (i - 1), 90 * i)

    mapdl.nummrg("kp")

    # mesh cylinder
    mapdl.lsel("s", "loc", "x", 0)
    mapdl.lsel("r", "loc", "y", 0)
    mapdl.lsel("r", "loc", "z", 0, height - h_tip)
    mapdl.lesize("all", elemsize * 2)
    mapdl.mshape(0)
    mapdl.mshkey(1)

    mapdl.esize(elemsize)
    mapdl.allsel("all")
    mapdl.vsweep("ALL")
    mapdl.csys(1)
    mapdl.asel("s", "loc", "z", "", height - h_tip + 0.0001)
    mapdl.asel("r", "loc", "x", radius)
    mapdl.local(11, 1)

    mapdl.csys(0)

    # mesh the surface with SURF154
    mapdl.aatt(2, 2, 2, 11)
    mapdl.amesh("all")
    mapdl.prep7()

    # plot elements
    # mapdl.eplot()

    # Apply tangential pressure
    mapdl.esel("S", "TYPE", "", 2)
    mapdl.sfe("all", 2, "pres", "", pressure)

    # Constrain bottom of cylinder/rod
    mapdl.asel("s", "loc", "z", 0)
    mapdl.nsla("s", 1)
    mapdl.d("all", "all")
    mapdl.allsel()

    # new solution
    mapdl.run("/SOLU")
    mapdl.antype("static", "new")
    # mapdl.eqslv('pcg', 1e-8)
    mapdl.solve()

    # necessary for any prnsol printouts
    mapdl.header("off", "off", "off", "off", "off", "off")
    nsigfig = 10
    mapdl.format("", "E", nsigfig + 9, nsigfig)
    # mapdl.post1(mute=True)
    # mapdl.set(1, 1)
    mapdl.mute = False


@pytest.fixture(scope="module")
def plastic_solve(mapdl):
    mapdl.mute = True
    mapdl.finish()
    mapdl.clear()
    mapdl.input(examples.verif_files.vmfiles["vm273"])

    mapdl.post1()
    mapdl.set(1, 2)
    mapdl.mute = False


@pytest.fixture(scope="module")
def contact_solve(mapdl):
    mapdl.mute = True
    mapdl.finish()
    mapdl.clear()
    mapdl.input(examples.verif_files.vmfiles["vm266"])

    mapdl.post1()
    mapdl.set('last')
    mapdl.mute = False


# must be run first before loading a result
# since MAPDL may be on a remote windows machine, cannot test
# @pytest.mark.skipif(os.name == 'nt', reason="Causes MAPDL to die on windows")
# def test_nodal_eqv_stress_fail(mapdl, static_solve):
#     with pytest.raises(MapdlRuntimeError):
#         mapdl.post_processing.nodal_eqv_stress


@pytest.mark.parametrize("comp", ["X", "Y", "z"])  # lowercase intentional
def test_disp(mapdl, static_solve, comp):

    disp_from_grpc = mapdl.post_processing.nodal_displacement(comp)

    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    nnum, disp_from_prns = np.genfromtxt(mapdl.prnsol("U", comp).splitlines()[1:]).T

    assert np.allclose(mapdl.mesh.nnum, nnum)
    assert np.allclose(disp_from_grpc, disp_from_prns)


def test_disp_norm_all(mapdl, static_solve):

    # test norm
    disp_norm = mapdl.post_processing.nodal_displacement("NORM")

    x = mapdl.post_processing.nodal_displacement("X")
    y = mapdl.post_processing.nodal_displacement("Y")
    z = mapdl.post_processing.nodal_displacement("Z")
    disp = np.vstack((x, y, z))
    manual_norm = np.linalg.norm(disp, axis=0)
    assert np.allclose(disp_norm, manual_norm)

    # test all
    assert np.allclose(disp.T, mapdl.post_processing.nodal_displacement("ALL"))


@pytest.mark.parametrize("comp", ["X", "Y", "z", "norm"])  # lowercase intentional
def test_disp_plot(mapdl, static_solve, comp):
    cpos = mapdl.post_processing.plot_nodal_displacement(comp, smooth_shading=True)
    assert isinstance(cpos, CameraPosition)


def test_disp_plot_subselection(mapdl, static_solve):
    mapdl.nsel("S", "NODE", vmin=500, vmax=2000, mute=True)
    mapdl.esel("S", "ELEM", vmin=500, vmax=2000, mute=True)
    cpos = mapdl.post_processing.plot_nodal_displacement(
        "X", smooth_shading=True, show_node_numbering=True
    )
    assert isinstance(cpos, CameraPosition)
    mapdl.allsel()


def test_nodal_eqv_stress(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("S", "PRIN")  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    seqv_ans = data[:, -1]
    seqv = mapdl.post_processing.nodal_eqv_stress

    seqv_aligned = seqv[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(seqv_ans, seqv_aligned)


def test_plot_nodal_eqv_stress(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_eqv_stress(smooth_shading=True)
    assert isinstance(cpos, CameraPosition)


def test_node_selection(mapdl, static_solve):
    mapdl.nsel("S", "NODE", vmin=1, vmax=2000, mute=True)
    assert mapdl.post_processing.selected_nodes.sum() == 2000

    mapdl.nsel("all", mute=True)
    assert mapdl.post_processing.selected_nodes.sum() == mapdl.mesh.n_node


def test_element_selection(mapdl, static_solve):
    mx_val = 1000
    mapdl.esel("S", "ELEM", vmin=1, vmax=mx_val, mute=True)
    assert mapdl.post_processing.selected_elements.sum() == mx_val

    mapdl.esel("all", mute=True)
    assert mapdl.post_processing.selected_elements.sum() == mapdl.mesh.n_elem


# TODO: add valid result
@pytest.mark.parametrize("comp", ["X", "Y", "z"])  # lowercase intentional
def test_rot(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_rotation(comp)

    # need a result with ROTX DOF
    # mapdl.post1(mute=True)
    # mapdl.set(1, 1, mute=True)
    # nnum, from_prns = np.genfromtxt(mapdl.prnsol('ROT', comp).splitlines()[1:]).T

    # assert np.allclose(mapdl.mesh.nnum, nnum)
    # assert np.allclose(from_grpc, from_prns)
    assert np.allclose(from_grpc, 0)


@pytest.mark.parametrize("comp", ["X", "Y", "z"])  # lowercase intentional
def test_plot_rot(mapdl, static_solve, comp):
    cpos = mapdl.post_processing.plot_nodal_rotation(comp)
    assert isinstance(cpos, CameraPosition)


# TODO: add valid result
def test_temperature(mapdl, static_solve):
    from_grpc = mapdl.post_processing.nodal_temperature
    assert np.allclose(from_grpc, 0)


# TODO: add valid result
def test_element_temperature(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    values = mapdl.post_processing.element_temperature()
    assert np.allclose(values, 0)


def test_plot_element_temperature(mapdl, static_solve):
    mapdl.set(1, 1, mute=True)
    cpos = mapdl.post_processing.plot_element_temperature()
    assert isinstance(cpos, CameraPosition)


def test_plot_temperature(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_temperature()
    assert isinstance(cpos, CameraPosition)


# TODO: add valid result
def test_pressure(mapdl, static_solve):
    from_grpc = mapdl.post_processing.nodal_pressure
    assert np.allclose(from_grpc, 0)


def test_plot_pressure(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_pressure()
    assert isinstance(cpos, CameraPosition)


# TODO: add valid result
def test_voltage(mapdl, static_solve):
    from_grpc = mapdl.post_processing.nodal_voltage
    assert np.allclose(from_grpc, 0)


def test_plot_voltage(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_voltage()
    assert isinstance(cpos, CameraPosition)


@pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
def test_nodal_component_stress(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_component_stress(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = COMPONENT_STRESS_TYPE.index(comp)
    mapdl.prnsol("S", "COMP")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("S", "COMP").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


def test_plot_nodal_component_stress(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_component_stress("X")
    assert isinstance(cpos, CameraPosition)


@pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
def test_nodal_principal_stress(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_principal_stress(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = PRINCIPAL_TYPE.index(comp)
    mapdl.prnsol("S", "PRIN")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


def test_plot_nodal_principal_stress(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_principal_stress(1)
    assert isinstance(cpos, CameraPosition)


def test_nodal_stress_intensity(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("S", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    sint_ans = data[:, -2]
    sint = mapdl.post_processing.nodal_stress_intensity

    sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(sint_ans, sint_aligned)


def test_plot_nodal_stress_intensity(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_stress_intensity()
    assert isinstance(cpos, CameraPosition)


@pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
def test_nodal_total_component_strain(mapdl, static_solve, comp):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    index = COMPONENT_STRESS_TYPE.index(comp)
    mapdl.prnsol("EPTO", "COMP", mute=True)  # run twice to clear out warning

    data = np.genfromtxt(mapdl.prnsol("EPTO", "COMP").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    data_ans = data[:, index + 1]
    data = mapdl.post_processing.nodal_total_component_strain(comp)
    data = data[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(data_ans, data)


def test_plot_nodal_total_component_strain(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_total_component_strain("x")
    assert isinstance(cpos, CameraPosition)


@pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
def test_nodal_principal_total_strain(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_total_principal_strain(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = PRINCIPAL_TYPE.index(comp)
    mapdl.prnsol("EPTO", "PRIN")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("EPTO", "PRIN").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


def test_plot_nodal_principal_total_strain(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_total_principal_strain(1)
    assert isinstance(cpos, CameraPosition)


def test_nodal_total_strain_intensity(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("EPTO", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPTO", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    sint_ans = data[:, -2]
    sint = mapdl.post_processing.nodal_total_strain_intensity

    sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(sint_ans, sint_aligned)


def test_plot_nodal_total_strain_intensity(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_total_strain_intensity()
    assert isinstance(cpos, CameraPosition)


def test_nodal_total_eqv_strain(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("EPTO", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPTO", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    seqv_ans = data[:, -1]
    seqv = mapdl.post_processing.nodal_total_eqv_strain

    seqv_aligned = seqv[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(seqv_ans, seqv_aligned)


def test_plot_nodal_total_eqv_strain(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_total_eqv_strain(smooth_shading=True)
    assert isinstance(cpos, CameraPosition)


###############################################################################
@pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
def test_nodal_component_stress(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_component_stress(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = COMPONENT_STRESS_TYPE.index(comp)
    mapdl.prnsol("S", "COMP")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("S", "COMP").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


def test_plot_nodal_component_stress(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_component_stress("X")
    assert isinstance(cpos, CameraPosition)


@pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
def test_nodal_principal_stress(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_principal_stress(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = PRINCIPAL_TYPE.index(comp)
    mapdl.prnsol("S", "PRIN")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(from_grpc, from_prns, atol=1e-5)


def test_plot_nodal_principal_stress(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_principal_stress(1)
    assert isinstance(cpos, CameraPosition)


def test_nodal_stress_intensity(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("S", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    sint_ans = data[:, -2]
    sint = mapdl.post_processing.nodal_stress_intensity

    sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(sint_ans, sint_aligned)


def test_plot_nodal_stress_intensity(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_stress_intensity()
    assert isinstance(cpos, CameraPosition)


@pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
def test_nodal_elastic_component_strain(mapdl, static_solve, comp):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    index = COMPONENT_STRESS_TYPE.index(comp)
    mapdl.prnsol("EPEL", "COMP", mute=True)  # run twice to clear out warning

    data = np.genfromtxt(mapdl.prnsol("EPEL", "COMP").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    data_ans = data[:, index + 1]
    data = mapdl.post_processing.nodal_elastic_component_strain(comp)
    data = data[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(data_ans, data)


def test_plot_nodal_elastic_component_strain(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_elastic_component_strain("x")
    assert isinstance(cpos, CameraPosition)


@pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
def test_nodal_elastic_principal_strain(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_elastic_principal_strain(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = PRINCIPAL_TYPE.index(comp)
    mapdl.prnsol("EPEL", "PRIN")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("EPEL", "PRIN").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


def test_plot_nodal_elastic_principal_strain(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_elastic_principal_strain(1)
    assert isinstance(cpos, CameraPosition)


def test_nodal_elastic_strain_intensity(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("EPEL", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPEL", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    sint_ans = data[:, -2]
    sint = mapdl.post_processing.nodal_elastic_strain_intensity

    sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(sint_ans, sint_aligned)


def test_plot_nodal_elastic_strain_intensity(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_elastic_strain_intensity()
    assert isinstance(cpos, CameraPosition)


def test_nodal_elastic_eqv_strain(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("EPEL", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPEL", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    seqv_ans = data[:, -1]
    seqv = mapdl.post_processing.nodal_elastic_eqv_strain

    seqv_aligned = seqv[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(seqv_ans, seqv_aligned)


def test_plot_nodal_elastic_eqv_strain(mapdl, static_solve):
    cpos = mapdl.post_processing.plot_nodal_elastic_eqv_strain(smooth_shading=True)
    assert isinstance(cpos, CameraPosition)


@pytest.mark.parametrize("comp", ["X", "Y", "z"])  # lowercase intentional
def test_elem_disp(mapdl, static_solve, comp):

    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    mapdl.allsel()

    disp_from_grpc = mapdl.post_processing.element_displacement(comp)

    # use pretab to get the data
    table_name = "values"
    mapdl.etable(table_name, "U", comp, mute=True)
    arr = np.genfromtxt(mapdl.pretab(table_name).splitlines()[1:])[:, 1]
    assert np.allclose(arr, disp_from_grpc)


@pytest.mark.parametrize("option", ["min", "max", "avg"])
def test_elem_disp_all(mapdl, static_solve, option):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    disp_from_grpc = mapdl.post_processing.element_displacement("ALL", option)

    # use pretab to get the data
    arrays = []
    for comp in ['x', 'y', 'z']:
        table_name = "values" + comp
        mapdl.etable(table_name, "U", comp, option=option, mute=True)
        arrays.append(
            np.genfromtxt(mapdl.pretab(table_name).splitlines()[1:])[:, 1]
        )
    array = np.vstack(arrays).T
    assert np.allclose(array, disp_from_grpc)


def test_elem_disp_norm(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    disp = mapdl.post_processing.element_displacement("ALL")
    norm_disp = np.linalg.norm(disp, axis=1)
    disp_from_grpc = mapdl.post_processing.element_displacement("NORM")
    assert np.allclose(norm_disp, disp_from_grpc)


@pytest.mark.parametrize("comp", ["X", "Y", "Z", "NORM"])
def test_elem_disp_plot(mapdl, static_solve, comp):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    cpos = mapdl.post_processing.plot_element_displacement(comp)
    assert isinstance(cpos, CameraPosition)


@pytest.mark.parametrize("component", STRESS_TYPES[::3])
@pytest.mark.parametrize("option", ["min", "max", "avg"])
def test_element_stress(mapdl, static_solve, component, option):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    stress = mapdl.post_processing.element_stress(component, option)

    # use pretab to get the data
    table_name = "values" + component
    mapdl.etable(table_name, "S", component, option=option, mute=True)
    from_pretab = np.genfromtxt(
        mapdl.pretab(table_name).splitlines()[1:]
    )[:, 1]
    assert np.allclose(stress, from_pretab)


@pytest.mark.parametrize("comp", ["X", "1", "INT", "EQV"])
def test_plot_element_stress(mapdl, static_solve, comp):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    cpos = mapdl.post_processing.plot_element_stress(comp)
    assert isinstance(cpos, CameraPosition)


def test_plot_element_values(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    cpos = mapdl.post_processing.plot_element_values("S", "X")
    assert isinstance(cpos, CameraPosition)


###############################################################################


@pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
def test_nodal_plastic_component_strain(mapdl, plastic_solve, comp):

    index = COMPONENT_STRESS_TYPE.index(comp)
    mapdl.prnsol("EPPL", "COMP", mute=True)  # run twice to clear out warning

    data = np.genfromtxt(mapdl.prnsol("EPPL", "COMP").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    data_ans = data[:, index + 1]
    data = mapdl.post_processing.nodal_plastic_component_strain(comp)
    data = data[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(data_ans, data)


def test_plot_nodal_plastic_component_strain(mapdl, plastic_solve):
    cpos = mapdl.post_processing.plot_nodal_plastic_component_strain("x")
    assert isinstance(cpos, CameraPosition)


@pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
def test_nodal_plastic_principal_strain(mapdl, plastic_solve, comp):
    from_grpc = mapdl.post_processing.nodal_plastic_principal_strain(comp)

    index = PRINCIPAL_TYPE.index(comp)
    mapdl.prnsol("EPPL", "PRIN")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("EPPL", "PRIN").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


def test_plot_nodal_plastic_principal_strain(mapdl, plastic_solve):
    cpos = mapdl.post_processing.plot_nodal_plastic_principal_strain(1)
    assert isinstance(cpos, CameraPosition)


def test_nodal_plastic_strain_intensity(mapdl, plastic_solve):
    mapdl.prnsol("EPPL", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPPL", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    sint_ans = data[:, -2]
    sint = mapdl.post_processing.nodal_plastic_strain_intensity

    sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(sint_ans, sint_aligned)


def test_plot_nodal_plastic_strain_intensity(mapdl, plastic_solve):
    cpos = mapdl.post_processing.plot_nodal_plastic_strain_intensity()
    assert isinstance(cpos, CameraPosition)


def test_nodal_plastic_eqv_strain(mapdl, plastic_solve):
    mapdl.prnsol("EPPL", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPPL", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    seqv_ans = data[:, -1]
    seqv = mapdl.post_processing.nodal_plastic_eqv_strain

    seqv_aligned = seqv[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(seqv_ans, seqv_aligned)


def test_plot_nodal_plastic_eqv_strain(mapdl, plastic_solve):
    cpos = mapdl.post_processing.plot_nodal_plastic_eqv_strain(smooth_shading=True)
    assert isinstance(cpos, CameraPosition)


def test_nodal_contact_friction_stress(mapdl, contact_solve):
    return True

def test_plot_nodal_contact_friction_stress(mapdl, contact_solve):
    cpos = mapdl.post_processing.plot_nodal_contact_friction_stress(smooth_shading=True)
    assert isinstance(cpos, CameraPosition)

###############################################################################
# @pytest.mark.parametrize('comp', COMPONENT_STRESS_TYPE)
# def test_nodal_thermal_component_strain(mapdl, thermal_solve, comp):

#     index = COMPONENT_STRESS_TYPE.index(comp)
#     mapdl.prnsol('EPPL', 'COMP', mute=True)  # run twice to clear out warning

#     data = np.genfromtxt(mapdl.prnsol('EPPL', 'COMP').splitlines()[1:])
#     nnum_ans = data[:, 0].astype(np.int32)
#     data_ans = data[:, index + 1]
#     data = mapdl.post_processing.nodal_thermal_component_strain(comp)
#     data = data[np.in1d(mapdl.mesh.nnum, nnum_ans)]

#     assert np.allclose(data_ans, data)


# def test_plot_nodal_thermal_component_strain(mapdl, thermal_solve):
#     cpos = mapdl.post_processing.plot_nodal_thermal_component_strain('x')
#     assert isinstance(cpos, CameraPosition)


# @pytest.mark.parametrize('comp', PRINCIPAL_TYPE)
# def test_nodal_thermal_principal_strain(mapdl, thermal_solve, comp):
#     from_grpc = mapdl.post_processing.nodal_thermal_principal_strain(comp)

#     index = PRINCIPAL_TYPE.index(comp)
#     mapdl.prnsol('EPPL', 'PRIN')  # flush to ignore warning
#     arr = np.genfromtxt(mapdl.prnsol('EPPL', 'PRIN').splitlines()[1:])
#     nnum_ans = arr[:, 0]
#     from_prns = arr[:, index + 1]

#     # grpc includes all nodes.  ignore the ones not included in prnsol
#     from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

#     assert np.allclose(from_grpc, from_prns)


# def test_plot_nodal_thermal_principal_strain(mapdl, thermal_solve):
#     cpos = mapdl.post_processing.plot_nodal_thermal_principal_strain(1)
#     assert isinstance(cpos, CameraPosition)


# def test_nodal_thermal_strain_intensity(mapdl, thermal_solve):
#     mapdl.prnsol('EPPL', 'PRIN', mute=True)  # run twice to clear out warning
#     data = np.genfromtxt(mapdl.prnsol('EPPL', 'PRIN').splitlines()[1:])
#     nnum_ans = data[:, 0].astype(np.int32)
#     sint_ans = data[:, -2]
#     sint = mapdl.post_processing.nodal_thermal_strain_intensity

#     sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
#     assert np.allclose(sint_ans, sint_aligned)


# def test_plot_nodal_thermal_strain_intensity(mapdl, thermal_solve):
#     cpos = mapdl.post_processing.plot_nodal_thermal_strain_intensity()
#     assert isinstance(cpos, CameraPosition)


# def test_nodal_thermal_eqv_strain(mapdl, thermal_solve):
#     mapdl.prnsol('EPPL', 'PRIN', mute=True)  # run twice to clear out warning
#     data = np.genfromtxt(mapdl.prnsol('EPPL', 'PRIN').splitlines()[1:])
#     nnum_ans = data[:, 0].astype(np.int32)
#     seqv_ans = data[:, -1]
#     seqv = mapdl.post_processing.nodal_thermal_eqv_strain

#     seqv_aligned = seqv[np.in1d(mapdl.mesh.nnum, nnum_ans)]
#     assert np.allclose(seqv_ans, seqv_aligned)


# def test_plot_nodal_thermal_eqv_strain(mapdl, thermal_solve):
#     cpos = mapdl.post_processing.plot_nodal_thermal_eqv_strain(smooth_shading=True)
#     assert isinstance(cpos, CameraPosition)

###############################################################################
