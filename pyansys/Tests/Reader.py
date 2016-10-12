# -*- coding: utf-8 -*-
"""
Tests/Examples to load cdb files.
"""
from __future__ import print_function
from os.path import dirname, join, realpath

from pyansys import Reader

def Load():
    """ Load and plot hexahedral beam """
    
    # get location of this file
    pth = dirname(realpath(__file__))
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

#    return disp

def Display():
    """ Load and plot hexahedral beam """
    
    # get location of this file
    pth = dirname(realpath(__file__))
    
    fobj = Reader.ResultReader(join(pth, 'file.rst'))
    fobj.LoadCDB(join(pth, 'HexBeam.cdb'))
    
    print('Displaying ANSYS Mode 1')
    fobj.PlotDisplacement(0)
