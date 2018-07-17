from shutil import copyfile

import pytest
import numpy as np
import os
import pyansys

ANSYS_150_BIN = '/usr/ansys_inc/v150/ansys/bin/ansys150'
ANSYS_182_BIN = '/usr/ansys_inc/v182/ansys/bin/ansys182'

path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(path, 'testfiles', 'cyclic_reader')

TMPDIR = '/tmp/ansys/'


@pytest.mark.skipif(not os.path.isfile(ANSYS_182_BIN), reason="Requires ANSYS installed")
class TestCyclicResultReader182(object):

    # avoids errors in collection
    try:
        result_file = os.path.join(data_path, 'cyclic_v182.rst')
        result = pyansys.Result(result_file)
        copyfile(result_file, os.path.join(TMPDIR, 'v182.rst'))

        ansys = pyansys.ANSYS(exec_file=ANSYS_182_BIN, override=True,
                              jobname='v182', loglevel='ERROR', run_location=TMPDIR)

        # setup ansys for output without line breaks
        ansys.Post1()
        ansys.Set(1, 1)
        ansys.Header('OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF')
        ansys.Format('', 'E', 80, 20)
        ansys.Page(1E9, '', -1)
    except:
        pass

    def test_prnsol_u(self):
        # verify cyclic displacements
        self.ansys.Prnsol('u')
        msg = self.ansys.last_message().splitlines()
        array = np.genfromtxt(msg[10:])
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

        self.ansys.Presol('S')
        msg = self.ansys.last_message().splitlines()
        ansys_element_stress = []
        for line in msg:
            if len(line) == 201:
                ansys_element_stress.append(line)
        ansys_element_stress = np.genfromtxt(ansys_element_stress)
        ansys_enode = ansys_element_stress[:, 0].astype(np.int)
        ansys_element_stress = ansys_element_stress[:, 1:]

        assert np.allclose(element_stress, ansys_element_stress)
        assert np.allclose(enode, ansys_enode)

    def test_prnsol_s(self):
        # verify cyclic displacements
        self.ansys.Prnsol('s')
        msg = self.ansys.last_message().splitlines()
        array = np.genfromtxt(msg[10:])
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
        self.ansys.Prnsol('prin')
        msg = self.ansys.last_message().splitlines()
        array = np.genfromtxt(msg[10:])
        ansys_nnum = array[:, 0].astype(np.int)
        ansys_stress = array[:, 1:]

        nnum, stress = self.result.PrincipalNodalStress(0)

        # v150 includes nodes in the geometry that aren't in the result
        mask = np.in1d(nnum, ansys_nnum)
        nnum = nnum[mask]
        stress = stress[mask]

        assert np.allclose(ansys_nnum, nnum)
        assert np.allclose(ansys_stress, stress, atol=1E-2)

    def test_plot(self):
        filename = '/tmp/temp.png'
        self.result.PlotNodalSolution(0, screenshot=filename, interactive=False)
        self.result.PlotNodalStress(0, 'Sx', screenshot=filename, interactive=False)
        self.result.PlotPrincipalNodalStress(0, 'SEQV', screenshot=filename,
                                             interactive=False)

    def test_exit(self):
        self.ansys.Exit()


@pytest.mark.skipif(not os.path.isfile(ANSYS_150_BIN), reason="Requires ANSYS installed")
class TestCyclicResultReader150(TestCyclicResultReader182):
    """ test if cyclic result reader works for v150 """
    # avoids errors in collection
    try:
        result_file = os.path.join(data_path, 'cyclic_v150.rst')
        result = pyansys.Result(result_file)
        copyfile(result_file, os.path.join(TMPDIR, 'v150.rst'))

        ansys = pyansys.ANSYS(exec_file=ANSYS_150_BIN,
                              override=True,
                              jobname='v150',
                              loglevel='ERROR',
                              run_location=TMPDIR)

        # setup ansys for output without line breaks
        ansys.Post1()
        ansys.Set(1, 1)
        ansys.Header('OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF')
        ansys.Format('', 'E', 80, 20)
        ansys.Page(1E9, '', -1)
    except:
        pass
