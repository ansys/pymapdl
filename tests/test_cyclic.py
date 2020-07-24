import sys
import os

import numpy as np
import pytest
from pyvista.plotting import system_supports_plotting
from pyvista.plotting.renderer import CameraPosition

import pyansys
from pyansys.examples import rstfile

HAS_FFMPEG = True
try:
    import imageio_ffmpeg
except:
    HAS_FFMPEG = False


path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(path, 'testfiles')
cyclic_testfiles_path = os.path.join(path, 'cyclic_reader')
cys12_path = os.path.join(testfiles_path, 'cyc12')
academic_path = os.path.join(cyclic_testfiles_path, 'academic_rotor')

# modal result z axis
try:
    result_z = pyansys.download_sector_modal()
    result_z.positive_cyclic_dir = True
except:
    result_z = None

skip_with_no_xserver = pytest.mark.skipif(not system_supports_plotting(),
                                          reason="Requires active X Server")


# static result x axis
@pytest.fixture(scope='module')
def result_x():
    filename = os.path.join(testfiles_path, 'cyc12.rst')
    rst = pyansys.read_binary(filename)
    return rst


@pytest.fixture(scope='module')
def cyclic_v182_z():
    # static result z axis
    filename = os.path.join(cyclic_testfiles_path, 'cyclic_v182.rst')
    rst = pyansys.read_binary(filename)
    rst.positive_cyclic_dir = True
    return rst


@pytest.fixture(scope='module')
def cyclic_v182_z_with_comp():
    # cyclic modal with component
    filename = os.path.join(cyclic_testfiles_path, 'cyclic_v182_w_comp.rst')
    return pyansys.read_binary(filename)


def test_non_cyclic():
    with pytest.raises(TypeError):
        pyansys.cyclic_reader.CyclicResult(rstfile)


@skip_with_no_xserver
@pytest.mark.skipif(result_z is None, reason="Requires result file")
def test_plot_sectors(tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.png'))
    cpos = result_z.plot_sectors(off_screen=True, screenshot=filename)
    assert isinstance(cpos, CameraPosition)
    assert os.path.isfile(filename)


@skip_with_no_xserver
def test_plot_sectors_x(result_x):
    cpos = result_x.plot_sectors(off_screen=True)
    assert isinstance(cpos, CameraPosition)



@skip_with_no_xserver
@pytest.mark.skipif(result_z is None, reason="Requires result file")
def test_plot_z_cyc():
    cpos = result_z.plot(off_screen=True)
    assert isinstance(cpos, CameraPosition)


@skip_with_no_xserver
def test_plot_x_cyc(result_x):
    cpos = result_x.plot(off_screen=True)
    assert isinstance(cpos, CameraPosition)


@skip_with_no_xserver
def test_plot_component_rotor(cyclic_v182_z_with_comp):
    cyclic_v182_z_with_comp.plot_nodal_solution(0, full_rotor=False,
                                                node_components='REFINE',
                                                sel_type_all=False,
                                                off_screen=True)

    cyclic_v182_z_with_comp.plot_nodal_solution(0, full_rotor=True,
                                                node_components='REFINE',
                                                sel_type_all=False, off_screen=True)

    # result_z.plot_nodal_stress(20, 'Sx', node_components='REFINE',
    #                            sel_type_all=False, off_screen=True)

    # result.plot_principal_nodal_stress(20, 'SEQV',
    #                                    node_components='REFINE',
    #                                    sel_type_all=False,
    #                                    off_screen=True)


def test_element_stress_v182_non_cyclic():
    """
    Generated ansys results with:
    ansys.Post1()
    ansys.Set(1, 1)
    ansys.Header('OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF')
    ansys.Format('', 'E', 80, 20)
    ansys.Page(1E9, '', -1)

    msg = ansys.Presol('S').splitlines()
    ansys_element_stress = []
    for line in msg:
        if len(line) == 201:
            ansys_element_stress.append(line)
    ansys_element_stress = np.genfromtxt(ansys_element_stress)
    ansys_enode = ansys_element_stress[:, 0].astype(np.int)
    ansys_element_stress = ansys_element_stress[:, 1:]

    """
    ansys_result_file = os.path.join(cyclic_testfiles_path, 'cyclic_v182.rst')
    result = pyansys.read_binary(ansys_result_file)

    element_stress, elemnum, enode = result.element_stress(0, False, False)
    assert np.allclose(np.sort(elemnum), elemnum), 'elemnum must be sorted'

    element_stress = np.vstack(element_stress)
    enode = np.hstack(enode)

    # cyclic model will only output the master sector
    from_ansys = np.load(os.path.join(cyclic_testfiles_path, 'v182_presol.npz'))
    assert np.allclose(from_ansys['enode'], enode)
    assert np.allclose(from_ansys['element_stress'], element_stress)


def test_nodal_stress_v182_non_cyclic():
    """
    Generated with:
    msg = ansys.Prnsol('s').splitlines()
    array = np.genfromtxt(msg[9:])
    ansys_nnum = array[:, 0].astype(np.int)
    ansys_stress = array[:, 1:]
    """
    ansys_result_file = os.path.join(cyclic_testfiles_path, 'cyclic_v182.rst')
    result = pyansys.rst.ResultFile(ansys_result_file, ignore_cyclic=True)
    nnum, stress = result.nodal_stress(0)

    from_ansys = np.load(os.path.join(cyclic_testfiles_path, 'v182_prnsol_s.npz'))
    assert np.allclose(from_ansys['nnum'][:nnum.size], nnum)
    assert np.allclose(from_ansys['stress'][:nnum.size], stress)


def test_full_x_nodal_solution(result_x):
    """ need to open gui to output full rotor results """
    from_ansys = np.load(os.path.join(cyclic_testfiles_path,
                                      'prnsol_d_cyclic_x_full_v182.npz'))

    ansys_nnum = from_ansys['nnum']
    ansys_disp = from_ansys['disp']


    # self = pyansys.read_binary(cyclic_x_filename)
    rnum = 0
    nnum, disp = result_x.nodal_solution(rnum, phase=0, full_rotor=True,
                                         as_complex=False,
                                         in_nodal_coord_sys=False)

    assert np.allclose(np.sort(nnum), nnum), 'nnum must be sorted'

    mask = np.in1d(nnum, ansys_nnum)
    n = mask.sum()
    tmp = ansys_disp.reshape(disp.shape[0], n, 3)
    assert np.allclose(nnum[mask], ansys_nnum[:n])
    assert np.allclose(disp[:, mask], tmp)

    nnum_alt, disp_alt = result_x.nodal_displacement(rnum, phase=0,
                                                     full_rotor=True,
                                                     as_complex=False,
                                                     in_nodal_coord_sys=False)

    assert np.allclose(nnum_alt, nnum)
    assert np.allclose(disp_alt, disp)


def test_full_z_nodal_solution(cyclic_v182_z):
    """ need to open gui to output full rotor results """
    from_ansys = np.load(os.path.join(cyclic_testfiles_path,
                                      'prnsol_d_cyclic_z_full_v182.npz'))

    ansys_nnum = from_ansys['nnum']
    ansys_disp = from_ansys['disp']

    rnum = 0
    phase = 0
    nnum, disp = cyclic_v182_z.nodal_solution(rnum, phase,
                                              full_rotor=True,
                                              as_complex=False,
                                              in_nodal_coord_sys=False)

    mask = np.in1d(nnum, ansys_nnum)
    n = mask.sum()
    tmp = ansys_disp.reshape(disp.shape[0], n, 3)
    assert np.allclose(disp[:, mask], tmp)


def test_full_z_nodal_solution_phase(cyclic_v182_z):
    """ need to open gui to output full rotor results """
    from_ansys = np.load(os.path.join(cyclic_testfiles_path,
                                      'prnsol_d_cyclic_z_full_v182.npz'))

    ansys_nnum = from_ansys['nnum']
    ansys_disp = from_ansys['disp']

    rnum = 0
    phase = 0
    nnum, disp = cyclic_v182_z.nodal_solution(rnum, phase, full_rotor=True,
                                              as_complex=True)

    mask = np.in1d(nnum, ansys_nnum)
    n = mask.sum()
    tmp = ansys_disp.reshape(disp.shape[0], n, 3)
    assert np.allclose(disp[:, mask], tmp)


@skip_with_no_xserver
def test_full_x_nodal_solution_plot(result_x):
    result_x.plot_nodal_solution(0, off_screen=True)


def test_full_x_nodal_stress(result_x):
    """ need to open gui to output full rotor results """
    from_ansys = np.load(os.path.join(cyclic_testfiles_path,
                                      'prnsol_s_cyclic_x_full_v182.npz'))
    ansys_nnum = from_ansys['nnum']
    ansys_stress = from_ansys['stress']

    rnum = 0
    phase = 0
    nnum, stress = result_x.nodal_stress(rnum, phase, full_rotor=True)

    mask = np.in1d(nnum, ansys_nnum)
    n = mask.sum()
    tmp = ansys_stress.reshape(stress.shape[0], n, 6)

    np.abs(stress[:, mask] - tmp)

    assert np.allclose(stress[:, mask], tmp)
    assert np.allclose(nnum[mask], ansys_nnum[:n])


def test_mode_table(cyclic_v182_z, result_x):
    assert isinstance(cyclic_v182_z.mode_table, np.ndarray)
    assert isinstance(result_x.mode_table, np.ndarray)


@pytest.mark.skipif(result_z is None, reason="Requires result file")
def test_mode_table_result_z():
    assert isinstance(result_z.mode_table, np.ndarray)


@pytest.mark.skipif(result_z is None, reason="Requires result file")
def test_harmonic_index_to_cumulative():
    # harmonic_index_to_cumulative
    assert result_z.harmonic_index_to_cumulative(0, 0) == 0
    assert result_z.harmonic_index_to_cumulative(1, 0) == 6
    assert result_z.harmonic_index_to_cumulative(-7, 2) == 47

    with pytest.raises(Exception):
        result_z.harmonic_index_to_cumulative(10, 0)

    with pytest.raises(Exception):
        result_z.harmonic_index_to_cumulative(0, 6)


def test_full_x_principal_nodal_stress(result_x):
    """ need to open gui to output full rotor results """
    from_ansys = np.load(os.path.join(cyclic_testfiles_path,
                                      'prnsol_p_cyclic_x_full_v182.npz'))
    ansys_nnum = from_ansys['nnum']
    ansys_stress = from_ansys['stress']

    rnum = 0
    phase = 0
    nnum, stress = result_x.principal_nodal_stress(rnum, phase, full_rotor=True)

    mask = np.in1d(nnum, ansys_nnum)
    n = mask.sum()
    tmp = ansys_stress.reshape(stress.shape[0], n, 5)

    assert np.allclose(nnum[mask], ansys_nnum[:n])
    assert np.allclose(stress[:, mask], tmp, atol=4E-3)  # too loose


@skip_with_no_xserver
@pytest.mark.skipif(not HAS_FFMPEG, reason="requires imageio_ffmpeg")
@pytest.mark.skipif(result_z is None, reason="Requires result file")
def test_animate_nodal_solution(tmpdir):
    temp_movie = str(tmpdir.mkdir("tmpdir").join('tmp.mp4'))
    result_z.animate_nodal_solution(0, nangles=20, movie_filename=temp_movie,
                                    off_screen=True, loop=False)
    assert os.path.isfile(temp_movie)


@pytest.mark.skipif(result_z is None, reason="Requires result file")
def test_cyclic_z_harmonic_displacement():
    from_ansys = np.load(os.path.join(cyclic_testfiles_path,
                                      'prnsol_u_cyclic_z_full_v182_set_4_2.npz'))
    ansys_nnum = from_ansys['nnum']
    ansys_disp = from_ansys['disp']

    unod, count = np.unique(ansys_nnum, return_counts=True)
    unod = np.setdiff1d(unod[count == result_z.n_sector], 32)
    mask = np.in1d(ansys_nnum, unod)
    ansys_nnum = ansys_nnum[mask]
    ansys_disp = ansys_disp[mask]

    nnum, disp = result_z.nodal_solution((4, 2), full_rotor=True)
    mask = np.in1d(nnum, ansys_nnum)
    tmp = ansys_disp.reshape(disp.shape[0], mask.sum(), 3)
    assert np.allclose(disp[:, mask], tmp, atol=1E-5)


@skip_with_no_xserver
def test_plot_nodal_stress(result_x):
    result_x.plot_nodal_stress(0, 'z', off_screen=False)


@skip_with_no_xserver
def test_plot_nodal_stress(result_x):
    result_x.plot_nodal_stress(0, 'z', off_screen=True)


@skip_with_no_xserver
def test_plot_principal_nodal_stress(result_x):
    result_x.plot_principal_nodal_stress(0, 'seqv', off_screen=True)


def test_nodal_elastic_strain_cyclic(result_x):
    from_mapdl = np.load(os.path.join(cys12_path, 'RSYS0_ROTOR_PRNSOL_EPEL.npz'))
    nnum_ans = from_mapdl['nnum']
    stress_ans = from_mapdl['stress']

    # get EPEL
    nnum, stress = result_x.nodal_elastic_strain(0)

    # include only common values
    mask = np.in1d(nnum, nnum_ans[0])
    stress = stress[:, mask, :6]  # stress includes eqv
    nnum = nnum[mask]
    assert np.allclose(nnum, nnum_ans)
    assert np.allclose(stress, stress_ans)


@skip_with_no_xserver
def test_plot_nodal_elastic_strain(result_x):
    result_x.plot_nodal_elastic_strain(0, 'X', off_screen=True)


def test_nodal_temperature(result_x):
    from_mapdl = np.load(os.path.join(cys12_path, 'RSYS0_ROTOR_PRNSOL_BFE.npz'))
    nnum_ans = from_mapdl['nnum']
    temp_ans = from_mapdl['temp']

    nnum, temp = result_x.nodal_temperature(0)

    # include only common values
    assert np.allclose(nnum, nnum_ans)
    assert np.allclose(temp, temp_ans, equal_nan=True)


@skip_with_no_xserver
def test_plot_nodal_nodal_temperature(result_x):
    result_x.plot_nodal_temperature(0, off_screen=True)


def test_nodal_thermal_strain_cyclic(result_x):
    from_mapdl = np.load(os.path.join(cys12_path, 'RSYS0_ROTOR_PRNSOL_EPTH_COMP.npz'))
    nnum_ans = from_mapdl['nnum']
    strain_ans = from_mapdl['strain']

    nnum, strain = result_x.nodal_thermal_strain(0)

    # include only common values
    mask = np.in1d(nnum, nnum_ans)
    strain = strain[:, mask, :6]  # strain includes eqv
    nnum = nnum[mask]
    assert np.allclose(nnum, nnum_ans)
    assert np.allclose(strain, strain_ans)


# def test_nodal_strain_cyclic_modal(academic):
#     from_mapdl = np.load(os.path.join(academic_path, 'RSYS0_ROTOR_PRNSOL_EPTH_COMP.npz'))
#     nnum_ans = from_mapdl['nnum']
#     strain_ans = from_mapdl['strain']

#     nnum, strain = result_x.nodal_thermal_strain(0)

#     # include only common values
#     mask = np.in1d(nnum, nnum_ans)
#     strain = strain[:, mask, :6]  # strain includes eqv
#     nnum = nnum[mask]
#     assert np.allclose(nnum, nnum_ans)
#     assert np.allclose(strain, strain_ans)


@skip_with_no_xserver
def test_plot_nodal_thermal_strain(result_x):
    result_x.plot_nodal_thermal_strain(0, 'X', off_screen=True)
