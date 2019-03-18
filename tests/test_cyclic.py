import os

import numpy as np
import pytest
from vtki.plotting import running_xserver

import pyansys
from pyansys.examples import sector_result_file, rstfile

try:
    __file__
except:
    __file__ = '/home/alex/afrl/python/source/pyansys/tests/test_cyclic.py'


path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(path, 'testfiles')
cyclic_testfiles_path = os.path.join(path, 'cyclic_reader')

result_z = pyansys.ResultReader(sector_result_file)
cyclic_x_filename = os.path.join(testfiles_path, 'cyc12.rst')
result_x = pyansys.ResultReader(cyclic_x_filename)

cyclic_v182_file = os.path.join(cyclic_testfiles_path, 'cyclic_v182.rst')
cyclic_v182_z = pyansys.ResultReader(cyclic_v182_file)

def test_non_cyclic():
    with pytest.raises(Exception):
        pyansys.CyclicResult(rstfile)


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_plot_z_cyc():
    cpos = result_z.plot(off_screen=True)
    assert isinstance(cpos, list)


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_plot_x_cyc():
    cpos = result_x.plot(off_screen=True)
    assert isinstance(cpos, list)


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_plot_component_rotor():
    result_z.plot_nodal_solution(0, full_rotor=False,
                                 node_components='REFINE', sel_type_all=False,
                                 interactive=False)

    result_z.plot_nodal_solution(0, full_rotor=True,
                                 node_components='REFINE', sel_type_all=False,
                                 interactive=False)

    # result_z.plot_nodal_stress(20, 'Sx', node_components='REFINE',
    #                            sel_type_all=False, interactive=False)

    # result.plot_principal_nodal_stress(20, 'SEQV',
    #                                    node_components='REFINE',
    #                                    sel_type_all=False,
    #                                    interactive=False)


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
    result = pyansys.ResultReader(ansys_result_file)

    element_stress, elemnum, enode = result.element_stress(0)
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
    result = pyansys.Result(ansys_result_file)
    nnum, stress = result.nodal_stress(0)

    from_ansys = np.load(os.path.join(cyclic_testfiles_path, 'v182_prnsol_s.npz'))
    assert np.allclose(from_ansys['nnum'][:nnum.size], nnum)
    assert np.allclose(from_ansys['stress'][:nnum.size], stress)


def test_full_x_nodal_solution():
    """ need to open gui to output full rotor results """
    from_ansys = np.load(os.path.join(cyclic_testfiles_path,
                                      'prnsol_d_cyclic_x_full_v182.npz'))

    ansys_nnum = from_ansys['nnum']
    ansys_disp = from_ansys['disp']


    # self = pyansys.ResultReader(cyclic_x_filename)
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


def test_full_z_nodal_solution():
    """ need to open gui to output full rotor results """
    from_ansys = np.load(os.path.join(cyclic_testfiles_path,
                                      'prnsol_d_cyclic_z_full_v182.npz'))

    ansys_nnum = from_ansys['nnum']
    ansys_disp = from_ansys['disp']

    rnum = 0
    phase = 0
    nnum, disp = cyclic_v182_z.nodal_solution(rnum, phase, full_rotor=True,
                                         as_complex=False,
                                         in_nodal_coord_sys=False)

    mask = np.in1d(nnum, ansys_nnum)
    n = mask.sum()
    tmp = ansys_disp.reshape(disp.shape[0], n, 3)
    assert np.allclose(disp[:, mask], tmp)

@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_full_x_nodal_solution_plot():
    result_x.plot_nodal_solution(0, interactive=False)


def test_full_x_nodal_stress():
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
    assert np.allclose(stress[:, mask], tmp, atol=1E-5)
    assert np.allclose(nnum[mask], ansys_nnum[:n])


# def test_full_z_nodal_stress():
#     """ need to open gui to output full rotor results """
#     from_ansys = np.load(os.path.join(cyclic_testfiles_path,
#                                       'prnsol_s_cyclic_z_full_v182.npz'))
#     ansys_nnum = from_ansys['nnum']
#     ansys_stress = from_ansys['stress']

#     rnum = 0
#     phase = 0
#     nnum, stress = cyclic_v182_z.nodal_stress(rnum, phase, full_rotor=True)

#     mask = np.in1d(nnum, ansys_nnum)
#     n = mask.sum()
#     tmp = ansys_stress.reshape(stress.shape[0], n, 6)

#     assert np.allclose(nnum[mask], ansys_nnum[:n])
#     assert np.allclose(stress[:, mask], tmp, atol=1E-5)


# def test_full_x_principal_nodal_stress():
#     """ need to open gui to output full rotor results """
#     from_ansys = np.load(os.path.join(cyclic_testfiles_path,
#                                       'prnsol_s_cyclic_x_full_v182.npz'))
#     ansys_nnum = from_ansys['nnum']
#     ansys_stress = from_ansys['stress']

#     # self = pyansys.ResultReader(cyclic_x_filename)
#     rnum = 0
#     phase = 0
#     nnum, stress = result_x.nodal_stress(rnum, phase, full_rotor=True)

#     mask = np.in1d(nnum, ansys_nnum)
#     n = mask.sum()
#     tmp = ansys_stress.reshape(stress.shape[0], n, 6)

#     assert np.allclose(stress[:, mask], tmp, atol=1E-5)
#     assert np.allclose(nnum[mask], ansys_nnum[:n])


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_animate_nodal_solution(tmpdir):
    temp_movie = str(tmpdir.mkdir("tmpdir").join('tmp.mp4'))
    result_z.animate_nodal_solution(0, nangles=20, movie_filename=temp_movie,
                                interactive=False)
    assert os.path.isfile(temp_movie)


# def test_nodal_solution_v182():
#     ansys_result_file = os.path.join(cyclic_testfiles_path, 'cyclic_v182.rst')
#     result = pyansys.ResultReader(ansys_result_file)

#     nnum, disp = result.nodal_solution(0, full_rotor=True)

#     # cyclic model should only output the master sector
#     assert nnum.size == 230
#     from_ansys = np.load(os.path.join(cyclic_testfiles_path, 'v182_disp.npz'))

#     # mask = np.in1d(nnum, ansys_nnum)
#     # n = mask.sum()
#     # tmp = ansys_disp.reshape(disp.shape[0], n, 3)
#     # assert np.allclose(disp[:, mask], tmp)
#     breakpoint()

#     assert np.allclose(from_ansys['ansys_nnum'][:nnum.size], nnum)
#     assert np.allclose(from_ansys['ansys_disp'][:nnum.size], disp)
