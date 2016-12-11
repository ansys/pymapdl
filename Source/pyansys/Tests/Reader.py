# -*- coding: utf-8 -*-
"""
Tests/Examples to load cdb files.
"""
from __future__ import print_function
from os.path import dirname, join, realpath

from pyansys import Reader

pth = dirname(realpath(__file__))

def LoadResult():
    """ Load and plot hexahedral beam """
    
    # get location of this file
    filename = join(pth, 'file.rst')
    
    fobj = Reader.ResultReader(filename)
    
    print('Loaded result file with {:d} result sets'.format(fobj.nsets))

    print('Contains {:d} nodes'.format(len(fobj.nnum)))

    disp = fobj.GetResult(0)

    print('Displacements of first 10 nodes are:')
   
    for i in range(10):
        node = fobj.nnum[i]
        x = disp[i, 0]
        y = disp[i, 1]
        z = disp[i, 2]
        print('{:2d}  {:10.6f}   {:10.6f}   {:10.6f}'.format(node, x, y, z))


def DisplayResult():
    """ Load and plot hexahedral beam """
    
    # get location of this file
    fobj = Reader.ResultReader(join(pth, 'file.rst'))
    fobj.LoadCDB(join(pth, 'HexBeam.cdb'))
    
    print('Displaying ANSYS Mode 1')
    fobj.PlotDisplacement(0)


def LoadKM():
    """ Loads m and k matrices from a full file """
    
    # Create file reader object
    fobj = Reader.FullReader(join(pth, 'file.full'))
    fobj.LoadFullKM()

    ndim = fobj.nref.size

    # print results
    print('Loaded {:d} x {:d} mass and stiffness matrices'.format(ndim, ndim))
    print('\t k has {:d} entries'.format(fobj.krows.size))
    print('\t m has {:d} entries'.format(fobj.mrows.size))


