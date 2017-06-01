# -*- coding: utf-8 -*-
"""
Tests/Examples to load cdb files.
"""
from __future__ import print_function
import os
#from os.path import dirname, join, realpath

import pyansys


# get location of this folder and the example files
dir_path = os.path.dirname(os.path.realpath(__file__))
rstfile = os.path.join(dir_path, 'file.rst')
hexarchivefile = os.path.join(dir_path, 'HexBeam.cdb')
tetarchivefile = os.path.join(dir_path, 'TetBeam.cdb')
hexbeamfile = os.path.join(dir_path, 'hexbeam.vtk')
fullfile = os.path.join(dir_path, 'file.full')


def DisplayHexBeam():
    """ Displays a hex beam mesh """
    # Load an archive file
    archive = pyansys.ReadArchive(hexarchivefile)
    archive.ParseFEM()
    archive.uGrid.Plot()
    

def LoadResult():
    """ Load and plot hexahedral beam """
    
    # Load result file
    result = pyansys.ResultReader(rstfile)
    print('Loaded result file with {:d} result sets'.format(result.nsets))
    print('Contains {:d} nodes'.format(len(result.nnum)))

    # display result
    disp = result.GetResult(0)

    print('Displacements of first 10 nodes are:')
   
    for i in range(10):
        node = result.nnum[i]
        x = disp[i, 0]
        y = disp[i, 1]
        z = disp[i, 2]
        print('{:2d}  {:10.6f}   {:10.6f}   {:10.6f}'.format(node, x, y, z))


def DisplayDisplacement():
    """ Load and plot 1st bend of a hexahedral beam """
    
    # get location of this file
    fobj = pyansys.ResultReader(rstfile)
    fobj.LoadArchive(hexarchivefile)
    
    print('Displaying ANSYS Mode 1')
    fobj.PlotNodalResult(0)


def LoadKM():
    """ Loads m and k matrices from a full file """
    
    # Create file reader object
    fobj = pyansys.FullReader(fullfile)
    fobj.LoadFullKM()

    ndim = fobj.nref.size

    # print results
    print('Loaded {:d} x {:d} mass and stiffness matrices'.format(ndim, ndim))
    print('\t k has {:d} entries'.format(fobj.krows.size))
    print('\t m has {:d} entries'.format(fobj.mrows.size))


def DisplayCellQual(meshtype='tet'):
    """ 
    Displays minimum scaled jacobian of a sample mesh
    
    For an ANSYS analysis to run properly, the minimum scaled jacobian of each
    cell must be greater than 0.
    
    Parameters
    ----------
    meshtype string, optional 
        Set to 'hex' to display cell quality of a hexahedral meshed beam.
        
    Returns
    -------
    None
    
    """
    
    # load archive file and parse for subsequent FEM queries
    if meshtype == 'hex':
        archive = pyansys.ReadArchive(hexarchivefile)
    else:
        archive = pyansys.ReadArchive(tetarchivefile)
            
    # create vtk object
    archive.ParseFEM()

    # get cell quality
    qual = pyansys.CellQuality(archive.uGrid)
    
    # plot cell quality
    archive.uGrid.Plot(scalars=qual, stitle='Cell Minimum Scaled\nJacobian',
                       rng=[0, 1])
    
    
    
    