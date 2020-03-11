import sys
import os

import numpy as np
import pytest
from pyvista.plotting import system_supports_plotting
from pyvista.plotting.renderer import CameraPosition

import pyansys
from pyansys.examples import rstfile

try:
    __file__
except:
    __file__ = '/home/alex/afrl/python/source/pyansys/tests/test_cyclic.py'

HAS_FFMPEG = True
try:
    import imageio_ffmpeg
except:
    HAS_FFMPEG = False


is_python2 = sys.version_info.major == 2

path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(path, 'testfiles')
cyclic_testfiles_path = os.path.join(path, 'cyclic_reader')

# modal result z axis
try:
    result_z = pyansys.download_sector_modal()
    result_z.positive_cyclic_dir = True
except:
    result_z = None


# static result x axis
@pytest.fixture(scope='module')
def result_x():
    filename = os.path.join(testfiles_path, 'cyc12.rst')
    return pyansys.read_binary(filename)


@pytest.fixture(scope='module')
def cyclic_v182_z():
    # static result z axis
    filename = os.path.join(cyclic_testfiles_path, 'cyclic_v182.rst')
    return pyansys.read_binary(filename)


@pytest.fixture(scope='module')
def cyclic_v182_z_with_comp():
    # cyclic modal with component
    filename = os.path.join(cyclic_testfiles_path, 'cyclic_v182_w_comp.rst')
    return pyansys.read_binary(filename)


def test_non_cyclic():
    with pytest.raises(Exception):
        pyansys.CyclicResult(rstfile)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(result_z is None, reason="Requires result file")
def test_plot_z_cyc():
    cpos = result_z.plot(off_screen=True)
    assert isinstance(cpos, CameraPosition)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_plot_x_cyc(result_x):
    cpos = result_x.plot(off_screen=True)
    assert isinstance(cpos, CameraPosition)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
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
    element_stress = np.vstack(element_stress)
    enode = np.hstack(enode)

    # cyclic model will only output the master sector
    from_ansys = np.load(os.path.join(cyclic_testfiles_path, 'v182_presol.npz'))
    assert np.allclose(from_ansys['element_stress'], element_stress)
    assert np.allclose(from_ansys['enode'], enode)


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
    phase = 0
    full_rotor = True
    nnum, disp = result_x.nodal_solution(rnum, phase, full_rotor=True,
                                         as_complex=False,
                                         in_nodal_coord_sys=False)

    mask = np.in1d(nnum, ansys_nnum)
    n = mask.sum()
    tmp = ansys_disp.reshape(disp.shape[0], n, 3)
    assert np.allclose(nnum[mask], ansys_nnum[:n])
    assert np.allclose(disp[:, mask], tmp)


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


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
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


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
@pytest.mark.skipif(not HAS_FFMPEG, reason="requires imageio_ffmpeg")
@pytest.mark.skipif(result_z is None, reason="Requires result file")
def test_animate_nodal_solution(tmpdir):
    temp_movie = str(tmpdir.mkdir("tmpdir").join('tmp.mp4'))
    result_z.animate_nodal_solution(0, nangles=20, movie_filename=temp_movie,
                                    off_screen=True, loop=False)
    assert os.path.isfile(temp_movie)


@pytest.mark.skipif(is_python2, reason="Python 2.7 has a bug when loading displacements")
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


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_plot_nodal_stress(result_x):
    result_x.plot_nodal_stress(0, 'z', off_screen=True)
    result_x.plot_nodal_stress(0, 'z', off_screen=False)


@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_plot_nodal_stress(result_x):
    result_x.plot_nodal_stress(0, 'z', off_screen=True, full_rotor=False)



@pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
def test_plot_principal_nodal_stress(result_x):
    result_x.plot_principal_nodal_stress(0, 'eqv', off_screen=True)


# def test_full_z_nodal_stress():
#     """ need to open gui to output full rotor results """
#     from_ansys = np.load(os.path.join(cyclic_testfiles_path,
#                       'prnsol_s_cyclic_z_full_v182_set_1_1.npz'))
#     ansys_nnum = from_ansys['nnum']
#     ansys_stress = from_ansys['stress']

#     rnum = 0
#     phase = 0

#     unod, count = np.unique(ansys_nnum, return_counts=True)
#     unod = np.setdiff1d(unod[count == result_z.n_sector], 32)
#     mask = np.in1d(ansys_nnum, unod)
#     ansys_nnum = ansys_nnum[mask]
#     ansys_stress = ansys_stress[mask]

#     nnum, stress = result_z.nodal_stress(rnum, phase, full_rotor=True)
#     mask = np.in1d(nnum, ansys_nnum)
#     n = mask.sum()
#     tmp = ansys_stress.reshape(stress.shape[0], n, ansys_stress.shape[1])
#     assert np.allclose(stress[:, mask], tmp, atol=1E-5)


# if __name__ == '__main__':
#     test_element_stress_v182_non_cyclic()
