from shutil import copyfile

import pytest
import numpy as np
import os
import pyansys
from vtkInterface.plotting import RunningXServer

try:
    __file__
except:
    __file__ = '/home/alex/Documents/AFRL/Python/pyansys/Source/tests/test_ansys.py'


path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(path, 'testfiles', 'cyclic_reader')


rver = 'v150'  # also have 'v182' but will not work on windows
# rver = 'v182'  # also have 'v182' but will not work on windows

@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
class TestCyclicResultReader(object):

    # avoids errors in collection
    result_file = os.path.join(data_path, 'cyclic_%s.rst' % rver)
    try:
        # test if raw results are being read properly by using the normal result reader
        result = pyansys.Result(result_file)
        ansys = pyansys.ANSYS(override=True, jobname=rver, loglevel='DEBUG',
                              interactive_plotting=False, prefer_pexpect=True)

        # copy result file to ansys's temporary path
        copyfile(result_file, os.path.join(ansys.path, '%s.rst' % rver))

        # setup ansys for output without line breaks
        ansys.Post1()
        ansys.Set(1, 1)
        ansys.Header('OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF')
        nsigfig = 10
        ansys.Format('', 'E', nsigfig + 9, nsigfig)  
        ansys.Page(1E9, '', -1, 240)

    except:  # for travis and appveyor
        pass

    def test_prnsol_u(self):
        # verify cyclic displacements
        table = self.ansys.Prnsol('u').splitlines()
        if self.ansys.using_corba:
            array = np.genfromtxt(table[7:])
        else:
            array = np.genfromtxt(table[9:])
        ansys_nnum = array[:, 0].astype(np.int)
        ansys_disp = array[:, 1:-1]

        nnum, disp = self.result.NodalSolution(0)

        # cyclic model will only output the master sector
        ansys_nnum = ansys_nnum[:nnum.size]
        ansys_disp = ansys_disp[:nnum.size]

        assert np.allclose(ansys_nnum, nnum)
        assert np.allclose(ansys_disp, disp)

    def test_presol_s(self):
        # verify element stress
        element_stress, elemnum, enode = self.result.ElementStress(0)
        element_stress = np.vstack(element_stress)
        enode = np.hstack(enode)

        # parse ansys result
        table = self.ansys.Presol('S').splitlines()
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
        table = self.ansys.Prnsol('s').splitlines()
        if self.ansys.using_corba:
            array = np.genfromtxt(table[7:])
        else:
            array = np.genfromtxt(table[10:])
        ansys_nnum = array[:, 0].astype(np.int)
        ansys_stress = array[:, 1:]

        nnum, stress = self.result.NodalStress(0)

        # v150 includes nodes in the geometry that aren't in the result
        mask = np.in1d(nnum, ansys_nnum)
        nnum = nnum[mask]
        stress = stress[mask]

        assert np.allclose(ansys_nnum, nnum)
        assert np.allclose(ansys_stress, stress)

    def test_prnsol_prin(self):
        # verify principal stress
        table = self.ansys.Prnsol('prin').splitlines()
        if self.ansys.using_corba:
            array = np.genfromtxt(table[7:])
        else:
            array = np.genfromtxt(table[10:])
        ansys_nnum = array[:, 0].astype(np.int)
        ansys_stress = array[:, 1:]

        nnum, stress = self.result.PrincipalNodalStress(0)

        # v150 includes nodes in the geometry that aren't in the result
        mask = np.in1d(nnum, ansys_nnum)
        nnum = nnum[mask]
        stress = stress[mask]

        assert np.allclose(ansys_nnum, nnum)
        assert np.allclose(ansys_stress, stress, atol=1E-2)

    @pytest.mark.skipif(not RunningXServer(), reason="Requires active X Server")
    def test_plot(self):
        filename = '/tmp/temp.png'
        self.result.PlotNodalSolution(0, screenshot=filename,
                                      interactive=False)
        # self.result.PlotNodalStress(0, 'Sx', screenshot=filename,
        #                             interactive=False)
        self.result.PlotPrincipalNodalStress(0, 'SEQV', screenshot=filename,
                                             interactive=False)

    def test_exit(self):
        self.ansys.Exit()

# self = TestCyclicResultReader()
# self.test_prnsol_u()

