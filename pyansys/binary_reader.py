import os
import numpy as np
import warnings
import logging
import ctypes

from pyansys import _parsefull
from pyansys import _rstHelper

from pyansys import CDBparser


# attempt to load vtk
try:
    import vtkInterface
#    import vtk
    vtkloaded = True

except:
    warnings.warn('Cannot load vtk\nWill be unable to display results.')
    vtkloaded = False


#==============================================================================
# Pointer information from ansys interface manual
#==============================================================================
#Individual element index table
e_table = ['ptrEMS', 'ptrENF', 'ptrENS', 'ptrENG', 'ptrEGR', 'ptrEEL', 
           'ptrEPL', 'ptrECR', 'ptrETH', 'ptrEUL', 'ptrEFX', 'ptrELF',
           'ptrEMN', 'ptrECD', 'ptrENL', 'ptrEHC', 'ptrEPT', 'ptrESF',
           'ptrEDI', 'ptrETB', 'ptrECT', 'ptrEXY', 'ptrEBA', 'ptrESV', 
           'ptrMNL']

"""
ptrEMS - pointer to misc. data
ptrENF - pointer to nodal forces
ptrENS - pointer to nodal stresses
ptrENG - pointer to volume and energies
ptrEGR - pointer to nodal gradients
ptrEEL - pointer to elastic strains
ptrEPL - pointer to plastic strains
ptrECR - pointer to creep strains
ptrETH - pointer to thermal strains
ptrEUL - pointer to euler angles
ptrEFX - pointer to nodal fluxes
ptrELF - pointer to local forces
ptrEMN - pointer to misc. non-sum values
ptrECD - pointer to element current densities
ptrENL - pointer to nodal nonlinear data
ptrEHC - pointer to calculated heat generations
ptrEPT - pointer to element temperatures
ptrESF - pointer to element surface stresses
ptrEDI - pointer to diffusion strains
ptrETB - pointer to ETABLE items(post1 only
ptrECT - pointer to contact data
ptrEXY - pointer to integration point locations
ptrEBA - pointer to back stresses
ptrESV - pointer to state variables
ptrMNL - pointer to material nonlinear record


"""


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
        
        # check if file exists
        if not os.path.isfile(filename):
            raise Exception('{:s} not found'.format(filename))
        
        self.filename = filename
        self.header = _parsefull.ReturnHeader(filename)
        
        #// Check if lumped (item 11)
        if self.header[11]:
            raise Exception("Unable to read a lumped mass matrix.  Terminating.")
    
        # Check if arrays are unsymmetric (item 14)
        if self.header[14]:
            raise Exception ("Unable to read an unsymmetric mass/stiffness matrix.")


    def LoadKM(self, as_sparse=True, sort=True):
        """
        Load and construct mass and stiffness matrices from an ANSYS full file.

        Parameters
        ----------
        as_sparse : bool, optional
            Outputs the mass and stiffness matrices as scipy csc sparse arrays
            when True by default.
            
        sort : bool, optional
            By default, this setting sorts the rows and columns such that the 
            nodes are in order.  ANSYS stores the mass and stiffness matrices 
            such that the bandwidth of the arrays is minimized.  Therefore, to
            minimize the bandwidth of the arrays, make this setting False.
            
        
        Returns
        -------
        dof_ref : (n x 2) np.int32 array
            This array contains the node and degree corresponding to each row 
            and column in the mass and stiffness matrices.  When the sort 
            parameter is set to True this array will be sorted by node number
            first and then by the degree of freedom.  In a 3 DOF analysis the 
            intergers will correspond to:
            0 - x
            1 - y
            2 - z
            
        k : (n x n) np.float or scipy.csc array
            Stiffness array
            
        m : (n x n) np.float or scipy.csc array
            Mass array
        
        Notes
        -----
        
        
        """
        data = _parsefull.Load_KM(self.filename, sort)
        
        # nodal and DOF references
        self.nref = data[0]
        self.dref = data[1]

        # stiffness rows, columns, and data
        self.krows = data[2]
        self.kcols = data[3]
        self.kdata = data[4]
        
        # stiffness rows, columns, and data
        self.mrows = data[5]
        self.mcols = data[6]
        self.mdata = data[7]
#        self.sidx  = data[8]
        
        # stack these references
        dof_ref = np.vstack((self.nref, self.dref)).T
        
        # see if 
        if as_sparse:
            try:
                from scipy.sparse import csc_matrix, coo_matrix
            except:
                raise Exception('Unable to load scipy, matricies will be full')
                as_sparse = False
        
        # number of dimentions and degree of freedom reference
        ndim = self.nref.size
#        idx, ridx = Unique_Rows(dof_ref)

        # resort K and M matries to ordered sorted node order
#        if sort:
#
#            # get number of degrees of freedom
#            krow = ridx[self.krows]
#            kcol = ridx[self.kcols]
#            mrow = ridx[self.mrows]
#            mcol = ridx[self.mcols]
#            
#            # sorted references
#            dof_ref = dof_ref[idx]
#            
#        else:
        krow = self.krows
        kcol = self.kcols
        mrow = self.mrows
        mcol = self.mcols
            
        # output as a sparse matrix
#        from scipy import sparse
        if as_sparse:
            
#            k = csr_matrix((self.kdata, (krow, kcol)), shape=(ndim,)*2)

            k = coo_matrix((ndim,)*2)
            k.data = self.kdata
            k.row = krow
            k.col = kcol
#            k = csr_matrix(k)
            k = csc_matrix(k)
            
#            m = csr_matrix((self.mdata, (mrow, mcol)), shape=(ndim,)*2)

            m = coo_matrix((ndim,)*2)
            m.data = self.mdata
            m.row = mrow
            m.col = mcol
#            m = csr_matrix(m)
            m = csc_matrix(m)
            
        else:
            k = np.zeros((ndim,)*2)
            k[krow, kcol] = self.kdata

            m = np.zeros((ndim,)*2)
            m[mrow, mcol] = self.mdata

        return dof_ref, k, m
        

class ResultReader(object):
    """
    Object to control the reading of ANSYS results written to fortran file
    """
    
    def __init__(self, filename, logger=False, load_geometry=True):
        """
        Loads basic result information from result file and initializes result
        object.
    
        Parameters
        ----------
        filename : string
            Filename of the ANSYS binary result file.
            
        logger : bool
            Enables logging if True.  Debug feature.
        
        
        Returns
        -------
        None
        
        """

        # set logging level depending on settings
        if logger:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.CRITICAL)

        # store logger pointer
        self.logger = logging.getLogger(__name__)

        # Store filename result header items
        self.filename = filename
        self.resultheader = GetResultInfo(filename)
        
        # Get the total number of results and log it
        self.nsets = len(self.resultheader['rpointers'])
        string = 'There are {:d} results in this file'.format(self.nsets)
        self.logger.debug(string)
        
        # Get indices to resort nodal and element results
        self.sidx = np.argsort(self.resultheader['neqv'])
        self.sidx_elem = np.argsort(self.resultheader['eeqv'])

        # Store node numbering in ANSYS
        self.nnum = self.resultheader['neqv'][self.sidx]
        self.enum = self.resultheader['eeqv'][self.sidx_elem]
        
        # Store time values for later retrival
        self.GetTimeValues()
        
        # store geometry for later retrival
        if load_geometry:
            self.StoreGeometry()
        
        
    def ResultsProperties(self):
        """
        Logs results available in the result file and returns a dictionary
        of available results
        
        Logging must be enabled for the results of the check to be shown in the
        console.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        result_check : dictionary
            Dictionary indicating the availability of results.
            
        Notes
        -----
        None
        
        """
        
        # check number of results
        self.logger.debug('There are {:d} results in this file'.format(self.nsets))

        return {'Number of Results': self.nsets}


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
        None
        
        """
        if not vtkloaded:
            raise Exception('Cannot plot without VTK')

        # Load result from file
        result = self.GetNodalResult(rnum)

        # Process result
        if comp == 'x':
            d = result[:, 0]
            stitle = 'X {:s}'.format(label)
            
        elif comp == 'y':
            d = result[:, 1]
            stitle = 'Y {:s}'.format(label)
            
        elif comp == 'z':
            d = result[:, 2]
            stitle = 'Z {:s}'.format(label)
            
        else:
            # Normalize displacement
            d = result[:, :3]
            d = (d*d).sum(1)**0.5
            
            stitle = 'Normalized\n{:s}'.format(label)
            
        if as_abs:
            d = np.abs(d)
        
        # Generate plot
        text = 'Result {:d} at {:f}'.format(rnum + 1, self.tvalues[rnum])
        plobj = vtkInterface.PlotClass()
        plobj.AddMesh(self.uGrid, no_copy=True, scalars=d, stitle=stitle, 
                      flipscalars=True, interpolatebeforemap=True)
        plobj.AddText(text)
        cpos = plobj.Plot();  # store camera position
        del plobj

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
        
        endian = self.resultheader['endian']
        ptrTIMl = self.resultheader['ptrTIMl']
        
        # Load values if not already stored
        if not hasattr(self, 'tvalues'):
    
            # Seek to start of time result table
            f = open(self.filename, 'rb')
    
            f.seek(ptrTIMl*4 + 8)
            self.tvalues = np.fromfile(f, endian + 'd', self.nsets)
            
            f.close()
        
        return self.tvalues


    def GetNodalResult(self, rnum, sort=True):
        """
        Returns the nodal result for a result number
        
        Parameters
        ----------
        rnum : interger
            Result set requested.  Zero based indexing.
        sort : bool, optional
            Resorts the results so that the results correspond to the sorted
            node numbering (self.nnum) (default).  If left unsorted, results 
            correspond to the nodal equivalence array self.resultheader['neqv']
        
        Returns
        -------
        result : numpy.float array
            Result is (nnod x numdof), or number of nodes by degrees of freedom
            
        Notes
        -----
        None
            
        """
        # Get info from result header
        endian = self.resultheader['endian']
        numdof = self.resultheader['numdof']
        nnod = self.resultheader['nnod']
        rpointers = self.resultheader['rpointers']
        
        # Check if result is available
        if rnum > self.nsets - 1:
            raise Exception('There are only {:d} results in the result file.'.format(self.nsets))
        
        # Read a result
        f = open(self.filename, 'rb')
        
        # Seek to result table and to get pointer to DOF results of result table
        f.seek((rpointers[rnum] + 12)*4) # item 11
        ptrNSLl = np.fromfile(f, endian + 'i', 1)[0]
        
        # Seek and read DOF results
        f.seek((rpointers[rnum] + ptrNSLl + 2)*4)
        nitems = nnod*numdof
        result = np.fromfile(f, endian + 'd', nitems)
        
        f.close()
        
        # Reshape to number of degrees of freedom
        result = result.reshape((-1, numdof))
        
        # Return results
        if sort:
            # Reorder based on sorted indexing and return
            return result.take(self.sidx, 0)
        else:
            return result
    
    
    def StoreGeometry(self):
        """ Stores the geometry from the result file """
        
        f = open(self.filename, 'rb')
        f.seek((self.resultheader['ptrGEO'] + 2)*4)
        geotable = np.fromfile(f, self.resultheader['endian'] + 'i', 80)
        geotable.tolist()
        
        ptrLOC = geotable[26]
        
        #==============================================================================
        # Node information
        #==============================================================================
        nnod = self.resultheader['nnod']
        nnum = np.empty(nnod, np.int32)
        nloc = np.empty((nnod, 6), np.float)
        _rstHelper.LoadNodes(self.filename, ptrLOC, nnod, nloc, nnum)
        
        #======================================================================
        # Element Information
        #======================================================================
        nelm = geotable[4]
        ptrEID = geotable[28]
        maxety = geotable[1]
        
        # pointer to the element type index table
        ptrETYP = geotable[20]
        f.seek((ptrETYP + 2)*4)
        e_type_table = np.fromfile(f, self.resultheader['endian'] + 'i', maxety)
        
        # store information for each element type
        # make these arrays large so you can reference a value via element type numbering
#        etype_arr = np.empty(10000, np.int32)
        nodelm = np.empty(10000, np.int32) # number of nodes for this element type
        nodfor = np.empty(10000, np.int32) # number of nodes per element having nodal forces
        nodstr = np.empty(10000, np.int32) # number of nodes per element having nodal stresses
        etype_ID = np.empty(maxety, np.int32)
        ekey = []
        for i in range(maxety):
            f.seek((ptrETYP + e_type_table[i] + 2)*4)
            einfo = np.fromfile(f, self.resultheader['endian'] + 'i', 2)
            etype_ref = einfo[0]
            etype_ID[i] = einfo[1]
            ekey.append(einfo)
            
            f.seek((ptrETYP + e_type_table[i] + 2 + 60)*4)
            nodelm[etype_ref] = np.fromfile(f, self.resultheader['endian'] + 'i', 1)
        
            f.seek((ptrETYP + e_type_table[i] + 2 + 62)*4)
            nodfor[etype_ref] = np.fromfile(f, self.resultheader['endian'] + 'i', 1)
        
            f.seek((ptrETYP + e_type_table[i] + 2 + 93)*4)
            nodstr[etype_ref] = np.fromfile(f, self.resultheader['endian'] + 'i', 1)
        
        # store element table data
        self.element_table = {'nodelm': nodelm,
                              'nodfor': nodfor,
                              'nodstr': nodstr}
        
        # get the element description table
        f.seek((ptrEID + 2)*4)
        e_disp_table = np.empty(nelm, np.int32)
        e_disp_table[:] = np.fromfile(f, self.resultheader['endian'] + 'i8', nelm)
        
        # get pointer to start of element table and adjust element pointers
        ptr = ptrEID + e_disp_table[0]
        e_disp_table -= e_disp_table[0]


        f.close()
        
        # The following is stored for each element
        """
        mat     - material reference number
        type    - element type number
        real    - real constant reference number
        secnum  - section number
        esys    - element coordinate system
        death   - death flat (1 live, 0 dead)
        solidm  - solid model reference
        shape   - coded shape key
        elnum   - element number
        baseeid - base element number
        NODES   - node numbers defining the element
        """
        
        
        # allocate memory for this (a maximum of 21 points per element)
        etype = np.empty(nelm, np.int32)

        elem = np.empty((nelm, 20), np.int32)
        elem[:] = -1
        
        # load elements
        _rstHelper.LoadElements(self.filename, ptr, nelm, e_disp_table, elem, 
                                etype)


    #==============================================================================
    # old python
    #==============================================================================
#        for i in range(nelm-1):
#        
#            # Element type
#            f.seek((ptrEID + e_disp_table[i] + 3)*4)
#            etype = np.fromfile(f, self.resultheader['endian'] + 'i', 1)[0]
#            etype_arr[i] = etype
#            
#            nread =  e_disp_table[i + 1] -  e_disp_table[i] - 13
#        
#            # store element numbers
#            f.seek(32, 1)
#            rnodes = np.fromfile(f, self.resultheader['endian'] + 'i', nread)
#            elem[i, :nread] = rnodes
#            
#            
#        i += 1
#        f.seek((ptrEID + e_disp_table[i])*4)
#        nentry = np.fromfile(f, self.resultheader['endian'] + 'i', 1)[0]
#        nread = nentry - 10
#        f.seek(8, 1)
#        
#        etype = np.fromfile(f, self.resultheader['endian'] + 'i', 1)[0]
#        etype_arr[i] = etype
#        
#        # store element numbers
#        f.seek(32, 1)
#        rnodes = np.fromfile(f, self.resultheader['endian'] + 'i', nread)
#        elem[i, :nread] = rnodes

#        import ctypes
#        e_disp_table = e_disp_table.astype(ctypes.c_long)
#        _rstHelper.LoadElements(self.filename, ptrEID, nelm, e_disp_table, 
#                                elem, etype)
        
#        for i in range(nelm):
#            if not np.all(elem_linux[i] == elem[i]):
#                print i
#                break
#        
        
        # store geometry dictionary
        self.geometry = {'nnum': nnum,
                         'nodes': nloc,
                         'etype': etype,
                         'elem': elem,
                         'enum': self.resultheader['eeqv'],
                         'ekey': np.asarray(ekey, ctypes.c_long)}
        
        
        # store the reference array
        cells, offset, cell_type, self.numref = CDBparser.Parse(self.geometry, True)
        
        # Create vtk object if vtk installed
        if vtkloaded:
            nodes = nloc[:, :3]
            self.uGrid = vtkInterface.MakeuGrid(offset, cells, cell_type, nodes)
            
        
        # get edge nodes            
        nedge = nodstr[etype].sum()
        self.edge_idx = np.empty(nedge, np.int32)
        _rstHelper.AssembleEdges(nelm, etype, elem, self.numref.astype(np.int32), 
                                 self.edge_idx, nodstr)
            
        
        # store edge node numbers and indices to the node array
        self.edge_node_num_idx = np.unique(self.edge_idx)
        self.edge_node_num = self.geometry['nnum'][self.edge_node_num_idx]
    
    
    def NodalStress(self, rnum):
        """
        Retrives the component stresses for each node in the solution.
        
        The order of the results corresponds to the sorted node numbering.
        
        This algorthim, like ANSYS, computes the nodal stress by averaging the
        stress for each element at each node.  Due to the discontinunities
        across elements, stresses will vary based on the element they are
        evaluated from.
        
        Parameters
        ----------
        rnum : interger
            Result set to load using zero based indexing.
        
        Returns
        -------
        stress : array
            Stresses at Sx Sy Sz Sxy Syz Sxz averaged at each corner node.  
            For the corresponding node numbers, see "edge_node_num"
            
        Notes
        -----
        None
            
        """
        #%% debug cell
        # Get the header information from the header dictionary
        endian = self.resultheader['endian']
        rpointers = self.resultheader['rpointers']
        nelm = self.resultheader['nelm']
        nodstr = self.element_table['nodstr']
        etype = self.geometry['etype']
        
        # Check if result is available
        if rnum > self.nsets - 1:
            raise Exception('There are only {:d} results in the result file.'.format(self.nsets))
        
        # Read a result
        f = open(self.filename, 'rb')
        
        # Seek to result table and to get pointer to DOF results of result table
        f.seek((rpointers[rnum] + 13)*4) # item 12
        
        # 32-bit pointer to element solution
        ptrESL = np.fromfile(f, endian + 'i', 1)[0]
        
        if not ptrESL:
            f.close()
            raise Exception('No element solution in result set {:d}'.format(rnum + 1))
        
        # Seek to element result header
        element_rst_ptr = rpointers[rnum] + ptrESL + 2
        f.seek(element_rst_ptr*4)
        
        # element index table
        ele_ind_table = np.fromfile(f, endian + 'i8', nelm).astype(np.int32)
        ele_ind_table += element_rst_ptr
        
        # Each element header contains 25 records for the individual results
        table_index = e_table.index('ptrENS')
        
        # check number of records to read (differs with each version)
        f.seek((ele_ind_table[0] + table_index)*4)
        ptrENS = np.fromfile(f, endian + 'i', 1)[0]

        nnode_elem = nodstr[etype[0]]
        f.seek((ele_ind_table[0] + ptrENS - 2)*4)
        nitem = np.fromfile(f, endian + 'i', 1)[0]/nnode_elem


        nstresses = self.edge_idx.size
        stresses = np.empty((nstresses, 6), np.float32)
        
        #%% debug cell 2
        c = 0
        for i in range(len(ele_ind_table)):
            # Element nodal stresses, ptrENS, is the third item in the table
            f.seek((ele_ind_table[i] + table_index)*4)
            ptrENS = np.fromfile(f, endian + 'i', 1)[0]
        
            # read the stresses evaluated at the intergration points or nodes
            nnode_elem = nodstr[etype[i]]
            
            f.seek((ele_ind_table[i] + ptrENS)*4)
            stress = np.fromfile(f, endian + 'f', nnode_elem*nitem).reshape((-1, nitem))#[:, sidx]

            # store stresses
            stresses[c:c + nnode_elem] = stress[:, :6]
            c += nnode_elem
            
        # close file
        f.close()
        
        
        # Average the stresses for each element at each node
#        enode = self.edge_node_num_idx
#        s_node = np.empty((enode.size, 6), np.float32)
#        for i in range(6):
#            s_node[:, i] = np.bincount(self.edge_idx, weights=stresses[:, i])[enode]
#        ntimes = np.bincount(self.edge_idx)[enode]
#        s_node /= ntimes.reshape((-1, 1))



        # grabe element results from binary
        enode = self.edge_node_num_idx
        ntimes = np.bincount(self.edge_idx)[enode]
        
        nnod = self.resultheader['nnod']
        ele_data_arr = np.zeros((nnod, 6), np.float32)
        _rstHelper.LoadStress(self.filename, table_index, 
                              ele_ind_table, nodstr, etype, 
                              nitem, ele_data_arr, self.edge_idx)
        
        s_node = ele_data_arr[enode]
        s_node /= ntimes.reshape((-1, 1))
        
        return s_node
        
    
    def PlotNodalStress(self, rnum, stype):
        """
        Plots the stresses at each node in the solution.
        
        The order of the results corresponds to the sorted node numbering.
        This algorthim, like ANSYS, computes the node stress by averaging the
        stress for each element at each node.  Due to the discontinunities
        across elements, stresses will vary based on the element they are
        evaluated from.
        
        Parameters
        ----------
        rnum : interger
            Result set using zero based indexing.
        stype : string
            Stress type from the following list: [Sx Sy Sz Sxy Syz Sxz]
        
        Returns
        -------
        None
            
        Notes
        -----
        None
            
        """
        
        stress_types = ['Sx', 'Sy', 'Sz', 'Sxy', 'Syz', 'Sxz', 'Seqv']
        if stype not in stress_types:
            raise Exception("Stress type not in \n ['Sx', 'Sy', 'Sz', 'Sxy', 'Syz', 'Sxz']")

        sidx = ['Sx', 'Sy', 'Sz', 'Sxy', 'Syz', 'Sxz'].index(stype)

        # create a zero array for all nodes
        stress = np.zeros(self.resultheader['nnod'])
        
        # Populate with nodal stress at edge nodes
        stress[self.edge_node_num_idx] = self.NodalStress(rnum)[:, sidx]
        stitle = 'Nodal Stress\n{:s}'.format(stype)
        
        # Generate plot
        plobj = vtkInterface.PlotClass()
        plobj.AddMesh(self.uGrid, scalars=stress, stitle=stitle, no_copy=True,
                      flipscalars=True, interpolatebeforemap=True)
        
        text = 'Result {:d} at {:f}'.format(rnum + 1, self.tvalues[rnum])
        plobj.AddText(text)
        
        cpos = plobj.Plot() # store camera position
        del plobj
        
        return cpos


def GetResultInfo(filename):
    """
    Returns pointers used to access results from an ANSYS result file.

    Parameters
    ----------
    filename : string
        Filename of result file.

    Returns
    -------
    resultheader : dictionary
    
    """
    
    f = open(filename, 'rb')

    # initialize result header dictionary
    resultheader = {}

    # Check if big or small endian
    endian = '<'
    if np.fromfile(f, dtype='<i', count=1) != 100:
        
        # Check if big enos
        f.seek(0)
        if np.fromfile(f, dtype='>i', count=1) == 100:
            endian = '>'

        # Otherwise, it's probably not a result file
        else:
            raise Exception('Unable to determine endian type.\n\n' +\
                            'File is possibly not a result file.')

    resultheader['endian'] = endian

    # Read standard header
    f.seek(0);
    
    # Get ansys version
    f.seek(11*4)
    version = f.read(4)[::-1]

    try:
        resultheader['mainver'] = int(version[:2])
        resultheader['subver'] = int(version[-1])
    except:
        warnings.warn('Unable to parse version')
        resultheader['mainver'] = 15
        resultheader['subver'] = 0
        
    
    #======================
    # Read .RST FILE HEADER 
    #======================
    # 100 is size of standard header, plus extras, 3 is location of pointer in table
    f.seek(105*4)
    rheader = np.fromfile(f, endian + 'i', count=55)
    
    # Number of nodes (item 3)
    resultheader['nnod'] = rheader[2]

    # Number of elements (item 6)
    resultheader['nelm'] = rheader[6]
    
    # Number of degrees of freedom (item 5)
    resultheader['numdof'] = rheader[4]
    
    # Number of sets of results
    resultheader['nsets'] = rheader[8]
    
    # Pointer to results table (item 11)
    ptrDSIl = rheader[10]
    
    # Pointer to the table of time values for a load step (item 12)
    resultheader['ptrTIMl'] = rheader[11]
    
    # pointer to element equivalence table (item 14)
    ptrELM = rheader[13]
    
    # pointer to nodal equivalence table (item 15)
    ptrNODl = rheader[14]
    
    # pointer to geometry information (item 15)
    resultheader['ptrGEO'] = rheader[15]
    
    # Read nodal equivalence table
    f.seek((ptrNODl + 2)*4) # Start of pointer, then empty, then data
    resultheader['neqv'] = np.fromfile(f, endian + 'i', count=resultheader['nnod'])
    
    # Read nodal equivalence table
    f.seek((ptrELM + 2)*4) # Start of pointer, then empty, then data
    resultheader['eeqv'] = np.fromfile(f, endian + 'i', count=resultheader['nelm'])
    
    # Read table of pointers to locations of results
    f.seek((ptrDSIl + 2)*4) # Start of pointer, then empty, then data
    rpointers = np.fromfile(f, endian + 'i', count=resultheader['nsets'])
    resultheader['rpointers'] = rpointers
    
    f.close()
    
    return resultheader



def Unique_Rows(a):
    """ Returns unique rows of a and indices of those rows """
    b = np.ascontiguousarray(a).view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
    _, idx, ridx = np.unique(b, return_index=True, return_inverse=True)
    
    return idx, ridx


