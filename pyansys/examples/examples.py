"""
pyansys examples

"""
from __future__ import print_function
import os
import inspect
import sys

import numpy as np

import pyansys
import vtkInterface


# get location of this folder and the example files
dir_path = os.path.dirname(os.path.realpath(__file__))
rstfile = os.path.join(dir_path, 'file.rst')
hexarchivefile = os.path.join(dir_path, 'HexBeam.cdb')
tetarchivefile = os.path.join(dir_path, 'TetBeam.cdb')
fullfile = os.path.join(dir_path, 'file.full')
sector_archive_file = os.path.join(dir_path, 'sector.cdb')


def RunAll(run_ansys=False):
    """
    Runs all the functions within this module except for the ansys
    tests.

    """
    testfunctions = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isfunction(obj) and name != 'RunAll':
            if 'ANSYS' in name and not run_ansys:
                continue
            testfunctions.append(obj)

    # run all the functions
    any(f() for f in testfunctions)


def DisplayHexBeam(as_test=False):
    """ Displays a hex beam mesh """
    # Load an archive file
    archive = pyansys.ReadArchive(hexarchivefile)
    grid = archive.ParseVTK()
    grid.Plot(interactive=False)


def LoadResult():
    """
    Loads a result file and prints out the displacement of all the nodes from
    a modal analysis.

    """

    # Load result file
    result = pyansys.ResultReader(rstfile)
    print('Loaded result file with {:d} result sets'.format(result.nsets))
    print('Contains {:d} nodes'.format(len(result.nnum)))

    # display result
    nnum, disp = result.NodalSolution(0)

    print('Nodal displacement for nodes 30 to 40 is:')

    for i in range(29, 40):
        node = result.nnum[i]
        x = disp[i, 0]
        y = disp[i, 1]
        z = disp[i, 2]
        print('{:2d}  {:10.6f}   {:10.6f}   {:10.6f}'.format(node, x, y, z))


def DisplayDisplacement():
    """ Load and plot 1st bend of a hexahedral beam """

    # get location of this file
    fobj = pyansys.ResultReader(rstfile)

    print('Displaying ANSYS Mode 1')
    fobj.PlotNodalSolution(0, label='Displacement')


def DisplayStress():
    """ Load and plot 1st bend of a hexahedral beam """

    # get location of this file
    result = pyansys.ResultReader(rstfile)

    print('Displaying node averaged stress in x direction for Mode 6')
    result.PlotNodalStress(5, 'Sx')


def LoadKM():
    """ Loads m and k matrices from a full file """

    # Create file reader object
    fobj = pyansys.FullReader(fullfile)
    dofref, k, m = fobj.LoadKM()

    # print results
    ndim = k.shape[0]
    print('Loaded {:d} x {:d} mass and stiffness matrices'.format(ndim, ndim))
    print('\t k has {:d} entries'.format(k.indices.size))
    print('\t m has {:d} entries'.format(m.indices.size))

    # compute natural frequencies if installed
    try:
        from scipy.sparse import linalg
        from scipy import sparse
    except ImportError:
        return

    k += sparse.triu(k, 1).T
    m += sparse.triu(m, 1).T
    k += sparse.diags(np.random.random(k.shape[0])/1E20, shape=k.shape)

    # Solve
    w, v = linalg.eigsh(k, k=20, M=m, sigma=10000)

    # System natural frequencies
    f = np.real(w)**0.5 / (2 * np.pi)

    print('First four natural frequencies:')
    for i in range(4):
        print('{:.3f} Hz'.format(f[i]))


def SolveKM():
    """
    Loads and solves a mass and stiffness matrix from an ansys full file
    """
    try:
        from scipy.sparse import linalg
        from scipy import sparse
    except ImportError:
        print('scipy not installed, aborting')
        return

    # load the mass and stiffness matrices
    full = pyansys.FullReader(pyansys.examples.fullfile)
    dofref, k, m = full.LoadKM(sort=True)

    # make symmetric
    k += sparse.triu(k, 1).T
    m += sparse.triu(m, 1).T
    k += sparse.diags(np.random.random(k.shape[0])/1E20, shape=k.shape)

    # Solve
    w, v = linalg.eigsh(k, k=20, M=m, sigma=1000)

    # System natural frequencies
    f = (np.real(w))**0.5 / (2 * np.pi)

    # %% Plot result

    # Get the 4th mode shape
    full_mode_shape = v[:, 3]  # x, y, z displacement for each node
    
    # reshape and compute the normalized displacement
    disp = full_mode_shape.reshape((-1, 3))
    n = (disp * disp).sum(1)**0.5
    n /= n.max()  # normalize

    # load an archive file and create a vtk unstructured grid
    archive = pyansys.ReadArchive(pyansys.examples.hexarchivefile)
    grid = archive.ParseVTK()

    # Fancy plot the displacement
    plobj = vtkInterface.PlotClass()

    # add two meshes to the plotting class
    plobj.AddMesh(grid.Copy(), style='wireframe')
    plobj.AddMesh(grid, scalars=n, stitle='Normalized\nDisplacement',
                  flipscalars=True)
    # Update the coordinates by adding the mode shape to the grid
    plobj.UpdateCoordinates(grid.GetNumpyPoints() + disp / 80, render=False)
    plobj.AddText('Cantliver Beam 4th Mode Shape at {:.4f}'.format(f[3]),
                  fontsize=30)
    plobj.Plot()


def DisplayCellQual(meshtype='tet'):
    """
    Displays minimum scaled jacobian of a sample mesh

    For an ANSYS analysis to run properly, the minimum scaled jacobian of each
    cell must be greater than 0.

    Parameters
    ----------
    meshtype string, optional
        Set to 'hex' to display cell quality of a hexahedral meshed beam.

    """

    # load archive file and parse for subsequent FEM queries
    if meshtype == 'hex':
        archive = pyansys.ReadArchive(hexarchivefile)
    else:
        archive = pyansys.ReadArchive(tetarchivefile)

    # create vtk object
    grid = archive.ParseVTK()

    # get cell quality
    qual = pyansys.CellQuality(grid)

    # plot cell quality
    grid.Plot(scalars=qual, stitle='Cell Minimum Scaled\nJacobian',
              rng=[0, 1])


def CylinderANSYS(exec_file=None, plot_vtk=True, plot_ansys=True, as_test=False):
    """
    Cylinder demo for ansys
    """
    # cylinder parameters
    # torque = 100
    radius = 2
    h_tip = 2
    height = 20
    elemsize = 0.5
    force = 100/radius
    pressure = force/(h_tip*2*np.pi*radius)

    # start ANSYS
    if as_test:
        loglevel = 'ERROR'
    else:
        loglevel = 'INFO'
    ansys = pyansys.ANSYS(exec_file=exec_file, override=True, loglevel=loglevel)

    # Define higher-order SOLID186
    # Define surface effect elements SURF154 to apply torque
    # as a tangential pressure
    ansys.Prep7()
    ansys.Et(1, 186)
    ansys.Et(2, 154)
    ansys.R(1)
    ansys.R(2)

    # Aluminum properties (or something)
    ansys.Mp('ex', 1, 10e6)
    ansys.Mp('nuxy', 1, 0.3)
    ansys.Mp('dens', 1, 0.1/386.1)
    ansys.Mp('dens', 2, 0)

    # Simple cylinder
    for i in range(4):
        ansys.Cylind(radius, '', '', height, 90*(i-1), 90*i)

    ansys.Nummrg('kp')

    # non-interactive volume plot
    if plot_ansys and not as_test:
        ansys.View(1, 1, 1, 1)
        ansys.Vplot()

    # mesh cylinder
    ansys.Lsel('s', 'loc', 'x', 0)
    ansys.Lsel('r', 'loc', 'y', 0)
    ansys.Lsel('r', 'loc', 'z', 0, height - h_tip)
    ansys.Lesize('all', elemsize*2)
    ansys.Mshape(0)
    ansys.Mshkey(1)
    ansys.Esize(elemsize)
    ansys.Allsel('all')
    ansys.Vsweep('ALL')
    ansys.Csys(1)
    ansys.Asel('s', 'loc', 'z', '', height - h_tip + 0.0001)
    ansys.Asel('r', 'loc', 'x', radius)
    ansys.Local(11, 1)
    ansys.Csys(0)
    ansys.Aatt(2, 2, 2, 11)
    ansys.Amesh('all')
    ansys.Finish()

    if plot_ansys and not as_test:
        ansys.Eplot()

    # new solution
    ansys.Slashsolu()
    ansys.Antype('static', 'new')
    ansys.Eqslv('pcg', 1e-8)

    # Apply tangential pressure
    ansys.Esel('s', 'type', '', 2)
    ansys.Sfe('all', 2, 'pres', '', pressure)

    # Constrain bottom of cylinder/rod
    ansys.Asel('s', 'loc', 'z', 0)
    ansys.Nsla('s', 1)

    ansys.D('all', 'all')
    ansys.Allsel()
    ansys.Psf('pres', '', 2)
    ansys.Pbc('u', 1)
    ansys.Solve()
    ansys.Finish()
    ansys.Exit()

    # open the result file
    result = ansys.result
    element_stress, elemnum, enode = result.ElementStress(0)
    if as_test:
        assert len(element_stress)
    else:
        print(element_stress[:10])
    nodenum, stress = result.NodalStress(0)
    if as_test:
        assert np.any(stress)
    else:
        print(stress[:10])

    if plot_vtk:
        if as_test:
            # plot and save non-interactively
            cpos = [(20.992831318277517, 9.78629316586435, 31.905115108541928),
                    (0.35955395443745797, -1.4198191001571547, 10.346158032932495),
                    (-0.10547549888485548, 0.9200673323892437, -0.377294345312956)]

            img = result.PlotNodalSolution(0, interactive=False, cpos=cpos, screenshot=True)
            assert np.any(img)

            img = result.PlotNodalStress(0, 'Sx', colormap='bwr', interactive=False, cpos=cpos,
                                         screenshot=True)
            assert np.any(img)

            result.PlotPrincipalNodalStress(0, 'SEQV', colormap='bwr', interactive=False,
                                            cpos=cpos, screenshot=True)
            assert np.any(img)
        else:
            # plot interactively
            result.PlotNodalSolution(0, colormap='bwr')
            result.PlotNodalStress(0, 'Sx', colormap='bwr')
            result.PlotPrincipalNodalStress(0, 'SEQV', colormap='bwr')

    return True
