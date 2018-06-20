import numpy as np
import pyansys
from pyansys.examples import hexarchivefile
from pyansys.examples import rstfile
from pyansys.examples import fullfile


def test_readarchive():
    archive = pyansys.ReadArchive(hexarchivefile)
    grid = archive.ParseVTK()
    assert grid.points.size
    assert grid.cells.size
    assert grid.GetPointScalars('ANSYSnodenum') is not None
    assert np.all(grid.quality > 0)


def test_loadresult():
    result = pyansys.ResultReader(rstfile)

    # check result is loaded
    assert result.nsets
    assert result.nnum.size

    # check geometry is genreated
    grid = result.grid
    assert grid.points.size
    assert grid.cells.size
    assert grid.GetPointScalars('ANSYSnodenum') is not None

    # check results can be loaded
    nnum, disp = result.NodalSolution(0)
    assert nnum.size
    assert disp.size

    nnum, disp = result.NodalSolution(0)
    assert nnum.size
    assert disp.size

    nnum, disp = result.PrincipalNodalStress(0)
    assert nnum.size
    assert disp.size

    nnum, disp = result.NodalStress(0)
    assert nnum.size
    assert disp.size

    element_stress, enum, enode = result.ElementStress(0)
    assert element_stress[0].size
    assert enum.size
    assert enode[0].size

    element_stress, enum, enode = result.ElementStress(0, principal=True)
    assert element_stress[0].size
    assert enum.size
    assert enode[0].size


def test_fullreader():
    fobj = pyansys.FullReader(fullfile)
    dofref, k, m = fobj.LoadKM()
    assert dofref.size
    assert k.size
    assert m.size


if __name__ == '__main__':
    test_readarchive()
    test_loadresult()
    print('PASS')
