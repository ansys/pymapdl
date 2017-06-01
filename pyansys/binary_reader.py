import numpy as np
import warnings

from pyansys import archive_reader
from pyansys import _parsefull

try:
    from vtkInterface import plotting
except:
    pass

try:
    import vtk
    from vtk.util import numpy_support as VN
    vtkloaded = True

except:
    warnings.warn('Cannot load vtk\nWill be unable to display results or load CDB.')
    vtkloaded = False


class FullReader(object):
    """
    Object to store the results of an ANSYS full file

    NOTES:
    Currently only supports symmetric and real stiffness matrices as well as
    non-lumped mass matrices.
    
    """
    
    def __init__(self, filename):
        """
        Loads full header on initialization
        
        See ANSYS programmer's reference manual full header section for
        definitions of each header.
        
        """
        
        self.filename = filename
        self.header = _parsefull.ReturnHeader(filename)
        
        #// Check if lumped (item 11)
        if self.header[11]:
            raise Exception("Unable to read a lumped mass matrix.  Terminating.")
    
        # Check if arrays are unsymmetric (item 14)
        if self.header[14]:
            raise Exception ("Unable to read an unsymmetric mass/stiffness matrix.")


    def LoadFullKM(self):
        """
        Load indices for constructing symmetric mass and stiffness
        matricies

        STORES TO SELF:
        
        nref (np.int32 array)
            Ordered reference to original ANSYS node numbers
        
        dref (np.int32 array)
            DOF reference where
            0 - x
            1 - y
            2 - z

        krows (np.int32 array)
            Rows to construct the sparse stiffness matrix

        kcols (np.int32 array)
            Columns to construct the sparse stiffness matrix
        
        kdata (np.int32 array)
            Data for each entry in thesparse stiffness matrix

        mrows (np.int32 array)
            Rows to construct the mass stiffness matrix

        mcols (np.int32 array)
            Columns to construct the mass stiffness matrix

        mdata (np.int32 array)
            Data to construct the mass stiffness matrix
        
        """
        data = _parsefull.ReturnFull_KM(self.filename)
        
        # nodal reference
        self.nref = data[0]
        
        # DOF reference
        self.dref = data[1]

        # stiffness rows, columns, and data
        self.krows = data[2]
        self.kcols = data[3]
        self.kdata = data[4]
        
        # stiffness rows, columns, and data
        self.mrows = data[5]
        self.mcols = data[6]
        self.mdata = data[7]
        
    

class ResultReader(object):
    """
    Object to control the reading of ANSYS results written to fortran file
    """
    
    def __init__(self, filename):
        """
        SUMMARY
        Loads basic result information from result file.

    
        INPUTS
        filename (str)
            Filename of the ANSYS binary result file.
        
        
        OUTPUTS
        None
        
        
        LOADS TO SELF
        nnod (int)
            Number of nodes
            
        numdof (int)
            Number of degress of freedom
            
        neqv (np.int32 array)
            Nodal equivalence array.  Unsorted results correspond to each node
            in this array
            
        rpointers (np.int32 array)
            Location of each result within result file
            
        pointers (dictionary)
            Contains locations of various tables within the result file
            Designed to be expanded
            
        nsets (int)
            Number of results in this file
            
        sidx (np.int array)
            Indices to sort noal equivalence array            
            
        nnum (np.int32 array)
            Sorted node numbering.  Sorted results correspond to these nodes
        
        """

        # Store filename to self
        self.filename = filename
        
        # Store result retrieval items
        self.nnod, self.numdof, self.neqv, self.rpointers, self.pointers, self.endian = GetResultInfo(filename)
        
        # Number of results
        self.nsets = len(self.rpointers)
        
        # Get indices to resort nodal results
        self.sidx = np.argsort(self.neqv)

        # Store node numbering in ANSYS
        self.nnum = self.neqv[self.sidx]
        
        # Store time values for later retrival
        self.GetTimeValues()
        
        
    def LoadArchive(self, filename):
        """
        SUMMARY
        Loads blocked ANSYS archive file corresponding to result file.
        
        
        INPUTS
        filename (string)
            Archive filename (generally *.cdb)
        
        """
        if not vtkloaded:        
            raise ImportError('VTK not installed.  Cannot continue')

        # Import cdb
        cdb = archive_reader.ReadArchive(filename)
        cdb.ParseFEM()
        self.uGrid = cdb.uGrid
        
        # Extract surface mesh
        self.exsurf = self.uGrid.ExtractSurface()
        
        # Relate nodal equivalence indexing to plot indexing
        nnum = VN.vtk_to_numpy(self.exsurf.GetPointData().GetArray('ANSYSnodenum'))
        
        # Get sorted and reverse sorted indices
        pidx = np.argsort(nnum)
        pidx_r = np.argsort(pidx)
        
        # Get locations in sorted node number results array
        mask = np.in1d(self.nnum, nnum, assume_unique=True)
        if mask.sum() != len(nnum):
#            raise Exception('Not all nodes from the archive file are in the results file')
            warnings.warn('Not all nodes from the archive file are in the results file')
        
        # Store results index
        self.ridx = self.sidx[mask][pidx_r]
        
        # For uGrid as well
#        nnum = VN.vtk_to_numpy(self.uGrid.GetPointData().GetArray('ANSYSnodenum'))
        nnum = self.uGrid.GetPointScalars('ANSYSnodenum')

        # Get sorted and reverse sorted indices
        pidx = np.argsort(nnum)
        pidx_r = np.argsort(pidx)
        
        # Get locations in sorted node number results array
        mask = np.in1d(self.nnum, nnum, assume_unique=True)
        if mask.sum() != len(nnum):
            warnings.warn('Not all nodes from the archive file are in the results file')
#            raise Exception('Not all nodes from CDB are in the results file')
            
        self.ridx_full = self.sidx[mask][pidx_r]
            
        
    def PlotNodalResult(self, rnum, comp='norm', as_abs=False, label=''):
        """
        Plots a nodal result.  
        
        Archive file must be loaded and nodal results must exist.
        
        Parameters
        ----------
        rnum : interger
            Result set requested.  Zero based indexing.
        comp : string, optional
            Display component to display.  Options are 'x', 'y', 'z', and
            'norm', corresponding to the x directin, y direction, z direction,
            and the combined direction (x**2 + y**2 + z**2)**0.5
        as_abs : bool, optional
            Displays the absolute value of the result.
        label: string, optional
            Annotation string to add to scalar bar in plot.
        
        Returns
        -------
        cpos : list
            Camera position from vtk render window.
            
        Notes
        -----
        
        """   
        if not hasattr(self, 'exsurf'):
            raise Exception('Load archive file before displaying')
        
        # Load result from file
        result = self.GetResult(rnum, True)

        # Process result
        if comp == 'x':
            d = result[self.ridx, 0]
            stitle = 'X {:s}'.format(label)
            
        elif comp == 'y':
            d = result[self.ridx, 1]
            stitle = 'Y {:s}'.format(label)
            
        elif comp == 'z':
            d = result[self.ridx, 2]
            stitle = 'Z {:s}'.format(label)
            
        else:
            # Normalize displacement
            d = result[self.ridx, :3]
            d = (d*d).sum(1)**0.5
            
            stitle = 'Normalized\n{:s}'.format(label)
            
        if as_abs:
            d = np.abs(d)
        
        # Generate plot
        text = 'Result {:d} at {:f}'.format(rnum + 1, self.tvalues[rnum])
        plobj = plotting.PlotClass()
        plobj.AddMesh(self.exsurf, scalars=d, stitle=stitle, flipscalars=True)
        plobj.AddText(text)
        cpos = plobj.Plot() # store camera position
        
        return cpos


    def GetTimeValues(self):
        """
        SUMMARY
        Returns table of time values for results.  For a modal analysis, this
        corresponds to the frequencies of each mode.
        
        
        INPUTS
        None
            
            
        OUTPUTS
        tvalues (np.float64 array)
        
        """
        # Load values if not already stored
        if not hasattr(self, 'tvalues'):
    
            # Format endian            
            
            # Seek to start of time result table
            f = open(self.filename, 'rb')
    
            f.seek(self.pointers['ptrTIMl']*4 + 8)
            self.tvalues = np.fromfile(f, self.endian + 'd', self.nsets)
            
            f.close()
        
        return self.tvalues


    def GetResult(self, rnum, nosort=False):
        """
        SUMMARY
        Returns DOF results from result file in memory


        INPUTS:
        rnum (interger)
            Result set requested
            
        nosort (bool default False)
            Resorts the results so that the results correspond to the sorted
            node numbering (self.nnum).  If left unsorted, results correspond
            to the nodal equivalence array (self.neqv)
            
            
        OUTPUTS:
        result (np.float array)
            Result is (nnod x numdof), or number of nodes by degrees of freedom
            
        """
        
        # Check if result is available
        if rnum > self.nsets - 1:
            raise Exception('There are only {:d} results in the result file.'.format(self.nsets))
        
        # Read a result
        f = open(self.filename, 'rb')
        
        # Seek to result table and to get pointer to DOF results of result table
        f.seek((self.rpointers[rnum] + 12)*4) # item 12
        ptrNSLl = np.fromfile(f, self.endian + 'i', 1)[0]
        
        # Seek and read DOF results
        f.seek((self.rpointers[rnum] + ptrNSLl + 2)*4)
        nitems = self.nnod*self.numdof
        result = np.fromfile(f, self.endian + 'd', nitems)
        
        f.close()
        
        # Reshape to number of degrees of freedom
        result = result.reshape((-1, self.numdof))
        
        # Return results
        if nosort:
            return result
        else:
            # Reorder based on sorted indexing and return
            return result.take(self.sidx, 0)
    
    
def GetResultInfo(filename):
    """
    Returns information used to access results from the result file

    INPUTS:
    filename (string)
        Result filename

    OUTPUTS:
    nnod (interger)
        Number of nodes
        
    numdof (interger)
        Number of degrees of freedom
        
    neqv (np.int32 array)
        Nodal equivalence array.  Relates nodal results to ANSYS node numbers
        
    rpointers (np.int32 array)
        Array containing the interger locations in the result file of each
        result
    
    """
    
    pointers = {}
    f = open(filename, 'rb')

    # Check if big or small endian
    endian = '<'
    inttype = '<i'
    if np.fromfile(f, dtype='<i', count=1) != 100:
        # Check if big enos
        f.seek(0)
        if np.fromfile(f, dtype='>i', count=1) == 100:
            endian = '>'
            inttype = '>i'
        # Otherwise, it's probably not a result file
        else:
            raise Exception('Unable to determine endian type.\n\n' +\
                            'File is possibly not a result file.')
                            

    # Read standard header
#    f.seek(0);header = np.fromfile(f, dtype='>i', count=100)
    
    #======================
    # Read .RST FILE HEADER 
    #======================
    # 100 is size of standard header, plus extras, 3 is location of pointer in table
    f.seek(105*4)
    rheader = np.fromfile(f, dtype=inttype, count=55)
    
    # Number of nodes (item 3)
    nnod = rheader[2]
    
    # Number of degrees of freedom (item 5)
    numdof = rheader[4]
    
    # Number of sets of results
    nsets = rheader[8]
    
    # Pointer to results table (item 11)
    ptrDSIl = rheader[10]
    
    # Pointer to the table of time values for a load step (item 12)
    pointers['ptrTIMl'] = rheader[11]
    
    # pointer to nodal equivalence table (item 15)
    ptrNODl = rheader[14]
    
    # Read nodal equivalence table
    f.seek((ptrNODl + 2)*4) # Start of pointer says size, then empty, then data
    neqv = np.fromfile(f, dtype=inttype, count=nnod)
    #neqv = np.frombuffer(f, dtype=np.int32, count=nnod)
    
    # Read table of pointers to locations of results
    f.seek((ptrDSIl + 2)*4) # Start of pointer says size, then empty, then data
    rpointers = np.fromfile(f, dtype=inttype, count=nsets)
    
    f.close()
    
    return nnod, numdof, neqv, rpointers, pointers, endian
    
