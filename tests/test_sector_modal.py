import os

import pytest 
import pyansys
import numpy as np
import FEMORPH

try:
    __file__
except:
    __file__ = '/home/alex/python/pyansys/UnitTesting/binary_reader/sector/test_sector.py'

data_path = '/home/alex/python/pyansys/Data'

archivefile = '/home/alex/Documents/AFRL/Python/FEMORPH/Testing/MeshRepair/Density0.cdb'
has_archive = os.path.isfile(archivefile)

def SectorANSYS(run_analysis=False, ver='182'):
    ansys = pyansys.ANSYS('/usr/ansys_inc/v%s/ansys/bin/ansys%s' % (ver, ver),
                          jobname='sector_modal_v%s' % ver, override=True,
                          # jobname='file', override=True,
                          loglevel='error')

    if run_analysis:
        ansys.Cdread('db', archivefile)
        # ansys.Show()
        # ansys.Menu('on')
        # read in morphed positions

        # make cyclic
        ansys('/PREP7')
        ansys('CYCLIC')

        # bore boundary conditions
        ansys.Csys(1)
        ansys.Nsel('s', 'loc', 'x', 0, 0.63)
        ansys.D('all', 'all')
        ansys.Allsel()
        ansys.Csys(0)

        # Steel
        ansys('MP,    NUXY,   1,  0.3')
        ansys('MP,    DENS,   1,  0.0005')
        ansys('MP,      EX,   1,  17000000')
        ansys('EMODIF,ALL,MAT,1')

        # Static solution
        ansys('/SOLU')
        ansys('ANTYPE, 2, new')
        ansys('MODOPT, LANB, 12, 1')
        ansys.Cycopt('hindex', 'all')
        ansys.Bcsoption('', 'INCORE')
        ansys.Mxpand('', '', '', 'Yes')
        ansys.Solve()
        ansys.Finish()
        ansys.Save()

    # read results
    ansys.Post1()
    ansys.Header('off', 'off', 'off', 'off', 'off', 'off')
    ansys.Format('', 'E', 80, 20)
    ansys.Page(1E9, '', -1)
    ansys.Set(1, 1)
    ansys.Show()
    ansys.Menu('ON')
    
    return ansys


# start ansys with gui
# ansys = SectorANSYS(True, '182')  # warning, overwrites text
# result = ansys.results


def TestModalDisp(ver):
    """ test modal solution accuracy """
    resultfile = os.path.join(data_path, 'sector_modal_v%s.rst' % ver)
    result = pyansys.ResultReader(resultfile)

    rnum = 12
    nnum, disp = result.NodalSolution(rnum, full_rotor=True)
    # disp /= 11**0.5 # scale
    # rnum = result.HarmonicIndexToCumulative(1, 0)
    # result.PlotNodalSolution(result.HarmonicIndexToCumulative(1, 0))
    # result.PlotNodalSolution(rnum)
    # result.PlotNodalStress(rnum, 'Sx', full_rotor=True)
    # result.AnimateNodalSolution(rnum)

    # text result comes from the GUI
    text_result = os.path.join(data_path, 'prnsol_u_cyclic_modal_7_%s.txt' % ver)
    raw = np.genfromtxt(text_result, skip_header=4)
    ansys_nnum = raw[:, 0].astype(np.int)
    ansys_disp = raw[:, 1:-1]

    # gen rotor
    rotor = FEMORPH.Rotor(result.grid)
    rotor.ReplicateCyclically()

    splitind = (np.diff(ansys_nnum) < 0).nonzero()[0] + 1
    rotor_nnum = np.split(ansys_nnum, splitind)
    rotor_disp = np.split(ansys_disp, splitind)
    for i in range(22):
        mask = np.in1d(nnum, rotor_nnum[i])

        # ignoring cyclic interface nodes (can't match ansys)
        err = np.zeros_like(disp[0])
        err[mask] = np.abs(rotor_disp[i] - np.real(disp[i, mask]))
        err[rotor.cycpairidx.ravel()] = 0
        assert err.max() < 1

# @pytest.mark.skipif(True, reason="Require local data files")
@pytest.mark.skipif(not has_archive, reason="Require local data files")
def test_modal_disp():
    TestModalDisp('150')  # not working (yet)
    # TestModalDisp('182')  # not working
