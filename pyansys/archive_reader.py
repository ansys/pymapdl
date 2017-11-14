"""
Module to read ANSYS ASCII block formatted CDB files

USAGE

# load module
import pyansys

# load ANSYS cdb file
archive = pyansys.ReadArchive('example.cdb')

# Parse the raw data into a VTK unstructured grid
grid = archive.ParseVTK()

# Plot the result
grid.Plot()

"""
import warnings
import numpy as np

from pyansys import _reader
from pyansys import _relaxmidside
from pyansys import _parser

# Attempt to load VTK dependent modules
try:
    import vtk
    import vtkInterface
    vtk_loaded = True
except BaseException:
    warnings.warn('Unable to load vtk dependent modules')
    vtk_loaded = False


class ReadArchive(object):
    """
    Initialize cdb object by reading raw cdb from file

    Parameters
    ----------
    filename : string
        Filename of block formatted cdb file

    """

    def __init__(self, filename):
        """ Initializes a cdb object """
        self.raw = _reader.Read(filename)

    def ParseVTK(self, force_linear=False, allowable_types=None):
        """
        Parses raw data from cdb file to VTK format.  Creates unstructured grid
        as self.uGrid

        Parameters
        ----------
        force_linear : bool, optional
            This parser creates quadradic elements if available.  Set this to
            True to always create linear elements.  Defaults to False.

        allowable_types : list, optional
            Allowable element types.  Defaults to:
            ['45', '95', '185', '186', '92', '187']

            Can include:
            ['45', '95', '185', '186', '92', '187', '154']

        Returns
        -------
        uGrid : vtk.vtkUnstructuredGrid
            VTK unstructured grid from archive file.

        """

        if not vtk_loaded:
            raise Exception(
                'Unable to load VTK module.  Cannot parse raw cdb data')

        if self.CheckRaw():
            raise Exception(
                'Missing key data.  Cannot parse into unstructured grid')

        # Convert to vtk style arrays
        if allowable_types is None:
            allowable_types = ['45', '95', '185', '186', '92', '187']
        else:
            assert isinstance(allowable_types, list), \
                   'allowable_types must be a list'

        result = _parser.Parse(self.raw, force_linear, allowable_types)
        cells, offset, cell_type, numref, enum, etype, rcon = result

        # catch bug
        cells[cells > numref.max()] = -1

        # Check for missing midside nodes
        possible_merged = False
        if force_linear or np.all(cells != -1):
            nodes = self.raw['nodes'][:, :3].copy()
            nnum = self.raw['nnum']

        else:
            mask = cells == -1

            nextra = mask.sum()
            maxnum = numref.max() + 1
            cells[mask] = np.arange(maxnum, maxnum + nextra)

            nnodes = self.raw['nodes'].shape[0]
            nodes = np.zeros((nnodes + nextra, 3))
            nodes[:nnodes] = self.raw['nodes'][:, :3]

            # Add extra node numbers
            nnum = np.hstack((self.raw['nnum'],
                              np.ones(nextra, np.int32) * -1))

            # Set new midside nodes directly between their edge nodes
            temp_nodes = nodes.copy()
            _relaxmidside.ResetMidside(cells, temp_nodes)
            nodes[nnodes:] = temp_nodes[nnodes:]

            possible_merged = True

        # Create unstructured grid
        uGrid = vtkInterface.MakeuGrid(offset, cells, cell_type, nodes)

        # Store original ANSYS numbering
        uGrid.AddPointScalars(nnum, 'ANSYSnodenum')
        uGrid.AddCellScalars(enum, 'ANSYS_elem_num')
        uGrid.AddCellScalars(etype, 'ANSYS_elem_typenum')
        uGrid.AddCellScalars(rcon, 'ANSYS_real_constant')

        # Add node components to unstructured grid
        ibool = np.empty(uGrid.GetNumberOfPoints(), dtype=np.int8)
        for comp in self.raw['node_comps']:
            ibool[:] = 0  # reset component array

            # Convert to new node numbering
            nodenum = numref[self.raw['node_comps'][comp]]

            ibool[nodenum] = 1
            uGrid.AddPointScalars(ibool, comp.strip())

        # merge duplicate points
        if possible_merged:
            vtkappend = vtk.vtkAppendFilter()
            vtkappend.AddInputData(uGrid)
            vtkappend.MergePointsOn()
            vtkappend.Update()
            uGrid = vtkappend.GetOutput()
            vtkInterface.AddFunctions(uGrid)

        # Add tracker for original node numbering
        npoints = uGrid.GetNumberOfPoints()
        uGrid.AddPointScalars(np.arange(npoints), 'VTKorigID')

        self.vtkuGrid = uGrid

        return uGrid

    def CheckRaw(self):
        """ Check if raw data can be converted into an unstructured grid """
        try:
            self.raw['elem'][0, 0]
            self.raw['enum'][0]
        except BaseException:
            return 1

        return 0

    def SaveAsVTK(self, filename):
        """
        Writes the ANSYS FEM as a vtk file.

        The file extension will select the type of writer to use.  *.vtk will
        use the legacy writer, while *.vtu will select the VTK XML writer.

        Run ParseFEM before running this to generate the vtk object

        Parameters
        ----------
        filename : str
            Filename of grid to be written.  The file extension will select the
            type of writer to use.  *.vtk will use the legacy writer,
            while *.vtu will select the PVTK XML writer

        binary : bool, optional
            Writes as a binary file by default.  Set to False to write ASCII

        Returns
        -------
        None

        Notes
        -----
        Binary files write much faster than ASCII, but binary files written on
        one  system may not be readable on other systems.  Binary can only be
        selected for the legacy writer.

        """
        # place holder
        print('Run grid = archive.ParseVTK() and then\ngrid.WriteGrid(filename, binary)')
