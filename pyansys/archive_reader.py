"""
Module to read ANSYS ASCII block formatted CDB files

USAGE

# load module
from ANSYScdb import CDB

# load ANSYS cdb file
cdb = CDB.Reader('example.cdb')

# Parse the raw data into a VTK unstructured grid
cdb.ParseVTK()

# Plot the result
cdb.Plot()

"""
import warnings
import numpy as np

# Attempt to load VTK dependent modules
try:
    from vtkInterface import utilities
    vtk_loaded = True
except:
    warnings.warn('Unable to load vtk dependent modules')
    vtk_loaded = False

# Cython modules
try:
    from pyansys import _reader
    from pyansys import _relaxmidside
    from pyansys import CDBparser
    cython_loaded = True
except:
    warnings.warn('Unable to load Cython modules')
    cython_loaded = False
    
from pyansys import PythonReader
from pyansys import PythonParser


class ReadArchive(object):
    """ FEM object """
    
    def __init__(self, filename='', use_cython=True, raw=None):
        """
        Initialize cdb object by reading raw cdb from file
        
        INPUTS:
        filename (string):
            filename of block formatted cdb file
            
        use_cython (bool optional):
            boolean flag to use cython reader defaults to True

        raw (dictonary optional):
            dictionary of raw data
    
        """
        
        if raw and not filename:
            # Load raw data exterinally
            self.raw = raw
            return
        
        # Defaults to cython reader if user selects it
        if use_cython and cython_loaded:
            self.raw = _reader.Read(filename)

        # Python reader for debug purposes
        else:
            self.raw = PythonReader.Read(filename)


    def ParseVTK(self, use_cython=True, force_linear=False):
        """
        DESCRPTION
        Parses raw data from cdb file to VTK format.  Creates unstructured grid
        as self.uGrid
        
        INPUTS
        use_cython (bool, default True)
            Uses cython parser.  Disable for debugging.
            
        force_linear (bool, default False)
            This parser creates quadradic elements if available.  Set this to
            true to always create linear elements
        
        """
        if not vtk_loaded:
            raise Exception('Unable to load VTK module.  Cannot parse raw cdb data')
            return
            
           
        if self.CheckRaw():
            raise Exception('Missing key data.  Cannot parse into unstructured grid')            
           
        # Convert to vtk style arrays
        if use_cython and cython_loaded:
            cells, offset, cell_type, numref = CDBparser.Parse(self.raw,
                                                               force_linear)
            
        else:
            cells, offset, cell_type, numref = PythonParser.Parse(self.raw, 
                                                                  force_linear)

        # Check for missing midside nodes
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
            nnum = np.hstack((self.raw['nnum'], np.ones(nextra, np.int32)*-1))
            
            if cython_loaded:
                # Set new midside nodes directly between their edge nodes
                temp_nodes = nodes.copy()
                _relaxmidside.ResetMidside(cells, temp_nodes)
                nodes[nnodes:] = temp_nodes[nnodes:]
                
            
        # Create unstructured grid
        uGrid = utilities.MakeuGrid(offset, cells, cell_type, nodes)

        # Store original ANSYS cell and node numbering
        uGrid.AddPointScalars(nnum, 'ANSYSnodenum')

        # Add node components to unstructured grid
        ibool = np.empty(uGrid.GetNumberOfPoints(), dtype=np.int8)
        for comp in self.raw['node_comps']:
            ibool[:] = 0 # reset component array

            # Convert to new node numbering
            nodenum = numref[self.raw['node_comps'][comp]]
            
            ibool[nodenum] = 1
            uGrid.AddPointScalars(ibool, comp.strip())
            
        # Add tracker for original node numbering
        npoints = uGrid.GetNumberOfPoints()
        uGrid.AddPointScalars(np.arange(npoints), 'VTKorigID')
        self.vtkuGrid = uGrid
        
        return uGrid
        
        
    def ParseFEM(self, use_cython=True, raw=None):
        """ Parses raw data from cdb file to VTK format """
        if not vtk_loaded:
            raise Exception('Unable to load VTK module.  Cannot parse raw cdb data')
            return
            
        if self.CheckRaw():
            raise Exception('Missing key data.  Cannot parse into unstructured grid.')            
            
        # Convert to vtk style arrays
        if use_cython and cython_loaded:
            self.data = CDBparser.ParseForFEM(self.raw)
        else:
            self.data = PythonParser.ParseForFEM(self.raw)
            
        # Create unstructured grid
        self.uGrid = utilities.MakeuGrid(self.data['offset'], self.data['cells'], 
                                         self.data['cell_type'],
                                         self.data['nodes'][:, :3])

        # Store original ANSYS cell and node numbering
        self.uGrid.AddPointScalars(self.data['orignode'], 'ANSYSnodenum')

        # Extract ANSYS element numbering and store
        ansyselem = self.raw['enum'].compress(self.data['elemused'])
        self.uGrid.AddCellScalars(ansyselem, 'ANSYSelemnum')

        # Add node components to unstructured grid
        ibool = np.empty(self.uGrid.GetNumberOfPoints(), dtype=np.int8)
        for comp in self.data['node_comps']:
            ibool[:] = 0 # reset component array
            ibool[self.data['node_comps'][comp]] = 1
            self.uGrid.AddPointScalars(ibool, comp.strip())
            
        # Add tracker for original node numbering
        npoints = self.uGrid.GetNumberOfPoints()
        self.uGrid.AddPointScalars(np.arange(npoints), 'VTKorigID')
                                  
        return self.data, self.uGrid, self.data['cellarr'], self.data['ncellpts']
        
        
    def AddThickness(self):
        """
        Adds 'thickness' point scalars to uGrid
        
        Assumes that thickness is stored as SURF154 elements
        
        """
        nnum = self.uGrid.GetPointScalars('ANSYSnodenum')        
        t = ExtractThickness(self.raw)[nnum]
        
        self.uGrid.AddPointScalars(t, 'thickness', False)
        self.hasthickness = True
        

    def Plot(self):
        """ Plot unstructured grid """
        if not vtk_loaded:
            raise Exception('VTK not loaded')

        if hasattr(self, 'vtkuGrid'):
            grid = self.vtkuGrid

        elif hasattr(self, 'uGrid'):
            grid = self.uGrid
        
        else:
            raise Exception('Unstructred grid not generated.  Run ParseVTK or ParseFEM first.')

        if not grid.GetNumberOfCells():
            raise Exception('Unstructured grid contains no cells')
        grid.Plot()


    def CheckRaw(self):
        """ Check if raw data can be converted into an unstructured grid """
        try:
            self.raw['elem'][0, 0]
            self.raw['enum'][0]
        except:
            return 1

        return 0
    
    
    def SaveAsVTK(self, filename, binary=True):
        """
        Writes the ANSYS FEM as a vtk file.
        
        The file extension will select the type of writer to use.  *.vtk will
        use the legacy writer, while *.vtu will select the VTK XML writer.
        
        Run ParseFEM or ParseVTK before running this to generate the vtk object
        
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
        
        # Check if the unstructured grid exists
        if not hasattr(self, 'uGrid'):
            raise Exception('Run ParseFEM or ParseVTK first.')
            
        # Write the grid
        self.uGrid.WriteGrid(filename, binary)
            
            
def ExtractThickness(raw):
    """
    Extract thickness from raw element data:

    Assumes that thickness is stored as a real constant for SURF154 elements

    The "thickness" of nodes belonging to multiple SURF154 elements will is 
    averaged   
    
    """
    
    ekey = raw['ekey']
    etype = raw['etype']
    nnum = raw['nnum']
    e_rcon = raw['e_rcon'] # real constants
    rdat = raw['rdat']
    rnum = raw['rnum']
    
    # Assemble node thickness array (nodes belonging to SURF154)
    ety = np.in1d(ekey[:, 1], 154)
    maskC = np.in1d(etype, ekey[ety, 0])
    
    # Create thickness array
    maxnode = nnum.max() + 1
    t = np.zeros(maxnode)
    a = np.zeros(maxnode, np.int32) # number of entries in thickness array
    
    if np.any(maskC):

        # Reduce element matrix to maskC elements and first four nodes
        elem = raw['elem'][maskC, :8] 
        e_rcon = e_rcon[maskC]

        # Get the nodes of the elements matching each real constant
        for i in range(len(rnum)):
            # Get all surf154 elements matching the real constant
            idx = elem[e_rcon == rnum[i]] # get node indices
            
            idx = idx[idx != -1]
                      
            # Add thickness            
            t[idx] += rdat[i][6]
            a[idx] += 1
        
        # normalize thickness by number of entires
        a[a == 0] = 1 # avoid divide by zero
        t /= a
    
    return t
