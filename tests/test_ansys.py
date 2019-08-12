import socket
import glob
import os
from shutil import copyfile

import pytest
import numpy as np
import pyansys
from pyvista.plotting import system_supports_plotting

from pyansys.rst import ResultFile

path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(path, 'testfiles', 'cyclic_reader')

is_azure = socket.gethostname() != 'enterprise'
AZURE_LINUX = is_azure and os.name == 'posix'

# rver = 'v150'
rver = 'v182'

MAPDL150BIN = '/usr/ansys_inc/v150/ansys/bin/ansys150'
MAPDL182BIN = '/usr/ansys_inc/v182/ansys/bin/ansys182'
MAPDL194BIN = '/usr/ansys_inc/v194/ansys/bin/ansys194'


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
class TestCyclicResultReader(object):

    # avoids errors in collection
    result_file = os.path.join(data_path, 'cyclic_%s.rst' % rver)
    try:
        # test if raw results are being read properly by using the normal result reader
        result = ResultFile(result_file, ignore_cyclic=True)

        if rver == 'v182':
            ansys = pyansys.Mapdl(MAPDL182BIN,
                                  override=True, jobname=rver,
                                  loglevel='DEBUG',
                                  interactive_plotting=False,
                                  prefer_pexpect=True)
        else:
            ansys = pyansys.Mapdl(MAPDL150BIN,
                                  override=True, jobname=rver,
                                  loglevel='DEBUG',
                                  interactive_plotting=False,
                                  prefer_pexpect=True)


        # copy result file to ansys's temporary path
        copyfile(result_file, os.path.join(ansys.path, '%s.rst' % rver))

        # setup ansys for output without line breaks
        ansys.post1()
        ansys.set(1, 1)
        ansys.header('OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF')
        nsigfig = 10
        ansys.format('', 'E', nsigfig + 9, nsigfig)  
        ansys.page(1E9, '', -1, 240)

    except:  # for travis and appveyor
        pass

    def test_prnsol_u(self):
        # verify cyclic displacements
        table = self.ansys.prnsol('u').splitlines()
        if self.ansys.using_corba:
            array = np.genfromtxt(table[7:])
        else:
            array = np.genfromtxt(table[9:])
        ansys_nnum = array[:, 0].astype(np.int)
        ansys_disp = array[:, 1:-1]

        nnum, disp = self.result.nodal_solution(0)

        # cyclic model will only output the master sector
        ansys_nnum = ansys_nnum[:nnum.size]
        ansys_disp = ansys_disp[:nnum.size]

        assert np.allclose(ansys_nnum, nnum)
        assert np.allclose(ansys_disp, disp)

    def test_presol_s(self):
        # verify element stress
        element_stress, _, enode = self.result.element_stress(0)
        element_stress = np.vstack(element_stress)
        enode = np.hstack(enode)

        # parse ansys result
        table = self.ansys.presol('S').splitlines()
        ansys_element_stress = []
        line_length = len(table[15])
        for line in table:
            if len(line) == line_length:
                ansys_element_stress.append(line)

        ansys_element_stress = np.genfromtxt(ansys_element_stress)
        ansys_enode = ansys_element_stress[:, 0].astype(np.int)
        ansys_element_stress = ansys_element_stress[:, 1:]

        assert np.allclose(element_stress, ansys_element_stress)
        assert np.allclose(enode, ansys_enode)

    def test_prnsol_s(self):
        # verify cyclic displacements
        table = self.ansys.prnsol('s').splitlines()
        if self.ansys.using_corba:
            array = np.genfromtxt(table[7:])
        else:
            array = np.genfromtxt(table[10:])
        ansys_nnum = array[:, 0].astype(np.int)
        ansys_stress = array[:, 1:]

        nnum, stress = self.result.nodal_stress(0)

        # v150 includes nodes in the geometry that aren't in the result
        mask = np.in1d(nnum, ansys_nnum)
        nnum = nnum[mask]
        stress = stress[mask]

        assert np.allclose(ansys_nnum, nnum)
        assert np.allclose(ansys_stress, stress)

    def test_prnsol_prin(self):
        # verify principal stress
        table = self.ansys.prnsol('prin').splitlines()
        if self.ansys.using_corba:
            array = np.genfromtxt(table[7:])
        else:
            array = np.genfromtxt(table[10:])
        ansys_nnum = array[:, 0].astype(np.int)
        ansys_stress = array[:, 1:]

        nnum, stress = self.result.principal_nodal_stress(0)

        # v150 includes nodes in the geometry that aren't in the result
        mask = np.in1d(nnum, ansys_nnum)
        nnum = nnum[mask]
        stress = stress[mask]

        assert np.allclose(ansys_nnum, nnum)
        assert np.allclose(ansys_stress, stress, atol=1E-2)

    @pytest.mark.skipif(not system_supports_plotting(), reason="Requires active X Server")
    def test_plot(self):
        filename = '/tmp/temp.png'
        self.result.plot_nodal_solution(0, screenshot=filename,
                                      off_screen=True)

        # self.result.plot_nodal_stress(0, 'Sx', screenshot=filename,
        #                             off_screen=True)

        self.result.plot_principal_nodal_stress(0, 'EQV', screenshot=filename,
                                                off_screen=True)

    def test_exit(self):
        self.ansys.exit()


# @pytest.mark.skipif(AZURE_LINUX, reason="Fails on Azure Linux")
def test_read_para():
    para_path = os.path.join(path, 'testfiles', 'para')
    para_files = glob.glob(os.path.join(para_path, '*.txt'))
    from pyansys.mapdl import load_parameters
    for para_file in para_files:
        arr, parm = load_parameters(para_file)


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_v150():
    mapdl = pyansys.Mapdl(MAPDL150BIN, override=True)
    mapdl.prep7()


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_v182():
    mapdl = pyansys.Mapdl(MAPDL182BIN, override=True)
    mapdl.prep7()


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_v194():
    mapdl = pyansys.Mapdl(MAPDL194BIN, override=True)
    mapdl.prep7()
