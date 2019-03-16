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


def test_is_cyclic():
    assert result.n_sector > 1


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_animate_nodal_solution(tmpdir):
    temp_movie = str(tmpdir.mkdir("tmpdir").join('tmp.mp4'))
    result_z.animate_nodal_solution(0, nangles=20, movie_filename=temp_movie,
                                interactive=False)
    assert os.path.isfile(temp_movie)


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_plot_z_cyc(self):
    cpos = result_z.plot()
    assert isinstance(cpos, list)


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_plot_x_cyc(self):
    cpos = result_x.plot()
    assert isinstance(cpos, list)


@pytest.mark.skipif(not running_xserver(), reason="Requires active X Server")
def test_plot_component_rotor():
    # result = pyansys.ResultReader(examples.sector_result_file)
    result_z.plot_nodal_solution(0, full_rotor=False)
                                 # node_components='REFINE', sel_type_all=False,
                                 # interactive=False)

    result.plot_nodal_stress(20, 'Sx', node_components='REFINE',
                             sel_type_all=False, interactive=False)

    result.plot_principal_nodal_stress(20, 'SEQV',
                                       node_components='REFINE',
                                       sel_type_all=False,
                                       interactive=False)


def test_nodal_solution_v182():
    ansys_result_file = os.path.join(cyclic_testfiles_path, 'cyclic_v182.rst')
    result = pyansys.ResultReader(ansys_result_file)
    nnum, disp = result.nodal_solution(0)

    # cyclic model will only output the master sector
    assert nnum.size == 230
    from_ansys = np.load(os.path.join(cyclic_testfiles_path, 'v182_disp.npz'))
    assert np.allclose(from_ansys['ansys_nnum'][:nnum.size], nnum)
    assert np.allclose(from_ansys['ansys_disp'][:nnum.size], disp)


def test_element_stress_v182():
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


def test_nodal_stress_v182():
    """
    Generated with:
    msg = ansys.Prnsol('s').splitlines()
    array = np.genfromtxt(msg[9:])
    ansys_nnum = array[:, 0].astype(np.int)
    ansys_stress = array[:, 1:]
    """
    ansys_result_file = os.path.join(cyclic_testfiles_path, 'cyclic_v182.rst')
    result = pyansys.ResultReader(ansys_result_file)
    nnum, stress = result.nodal_stress(0)

    from_ansys = np.load(os.path.join(cyclic_testfiles_path, 'v182_prnsol_s.npz'))
    assert np.allclose(from_ansys['nnum'][:nnum.size], nnum)
    assert np.allclose(from_ansys['stress'][:nnum.size], stress)


def test_principal_nodal_stress():
    """
    Generated with:
    msg = ansys.Prnsol('prin').splitlines()
    array = np.genfromtxt(msg[9:])
    ansys_nnum = array[:, 0].astype(np.int)
    ansys_stress = array[:, 1:]
    """
    ansys_result_file = os.path.join(cyclic_testfiles_path, 'cyclic_v182.rst')
    result = pyansys.ResultReader(ansys_result_file)
    nnum, stress = result.principal_nodal_stress(0)

    from_ansys = np.load(os.path.join(cyclic_testfiles_path, 'v182_prnsol_prin.npz'))
    assert np.allclose(from_ansys['nnum'], nnum)
    assert np.allclose(from_ansys['stress'], stress)


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

    # self = pyansys.ResultReader(cyclic_x_filename)
    rnum = 0
    phase = 0
    nnum, stress = result_x.nodal_stress(rnum, phase, full_rotor=True)

    mask = np.in1d(nnum, ansys_nnum)
    n = mask.sum()
    tmp = ansys_stress.reshape(stress.shape[0], n, 6)

    assert np.allclose(stress[:, mask], tmp)
    assert np.allclose(nnum[mask], ansys_nnum[:n])

    res = pyansys.Result(cyclic_x_filename)
    nnum_nocyc, stress_ncyc = res.nodal_stress(rnum)

    # stress_ncyc
    # mask = np.in1d(nnum_nocyc, ansys_nnum)
    assert np.allclose(stress_ncyc[mask], ansys_stress[:n])

# s_mask = np.isclose(stress_ncyc[mask], ansys_stress[:n]).all(1)
s_mask = np.isclose(stress[0, mask, :], tmp[0]).all(1)
points = result_x.mas_grid.points[mask]

import vtki
vtki.plot(points, scalars=s_mask, stitle='mask')


# stress[0, mask] - tmp[0]

rnum = 0
phase = 0
# nnum, stress_full = result_x.nodal_stress(rnum, phase, False, full_rotor=True)

# cres = pyansys.CyclicResult(cyclic_x_filename)
# result_x.plot_nodal_solution(0)
result_x.plot_nodal_stress(0, 'Sz')

nnum, stress_full = result_x.nodal_stress(rnum, phase, False, full_rotor=False)

res = pyansys.Result(cyclic_x_filename)
nnum, stress = res.nodal_stress(rnum)

np.allclose(stress_full[0], stress[:401], equal_nan=True)

# result_x.plot_nodal_stress(0, 'Sx')
# result_x.mas_grid.plot(scalars=stress[:401, 2])
result_x.mas_grid.plot(scalars=stress_full[0, :, 2])

pass

arr = np.loadtxt('/tmp/ansys/text.txt', skiprows=2)
np.savez(os.path.join(cyclic_testfiles_path, 'prnsol_s_cyclic_z_full_v182.npz'),
         nnum=arr[:, 0].astype(np.int32), stress=arr[:, 1:])

from_ansys = np.load(os.path.join(cyclic_testfiles_path, 'prnsol_s_cyclic_z_full_v182.npz'))
# from_ansys[
# result_z.plot_nodal_stress(0, 'Sz')

# result = pyansys.Result(sector_result_file)
# cyclic_v182_z.plot_nodal_stress(0, 'Sz')

###############################################################################
from_ansys = np.load(os.path.join(cyclic_testfiles_path,
                                  'prnsol_s_cyclic_z_full_v182.npz'))
ansys_nnum = from_ansys['nnum']
ansys_stress = from_ansys['stress']

# self = pyansys.ResultReader(cyclic_x_filename)
rnum = 0
phase = 0
nnum, stress = cyclic_v182_z.nodal_stress(rnum, phase, full_rotor=True)

mask = np.in1d(nnum, ansys_nnum)
n = mask.sum()
tmp = ansys_stress.reshape(stress.shape[0], n, 6)

s_mask = np.isclose(stress[0, mask, :], tmp[0]).all(1)
points = cyclic_v182_z.mas_grid.points[mask]

import vtki
plotter = vtki.Plotter()
plotter.add_mesh(points, scalars=s_mask, stitle='mask', point_size=10)
plotter.add_mesh(cyclic_v182_z.grid, style='wireframe', color='w')
plotter.show()
