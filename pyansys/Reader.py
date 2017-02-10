import numpy as np
import warnings

from pyansys import _parsefull

# Try to load optional items
try:
    from ANSYScdb import CDB_Reader
except:
    warnings.warn('CDB_Reader uninstalled')

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
        
        
    def LoadCDB(self, filename):
        """
        SUMMARY
        Loads CDB corresponding to result file
        
        
        INPUTS
        filename (string)
            Filename of cdb file
        
        """
        if not vtkloaded:        
            raise ImportError('VTK not installed.  Cannot continue')

        # Import cdb
        cdb = CDB_Reader.Read(filename)
        self.uGrid = cdb.ParseVTK()
        
        # Extract surface mesh
        sfilter = vtk.vtkDataSetSurfaceFilter()
        sfilter.SetInputData(self.uGrid)
        sfilter.PassThroughPointIdsOn()
        sfilter.PassThroughCellIdsOn()
        sfilter.Update()
        self.exsurf = sfilter.GetOutput()
        
#        # Triangle filter
#        trianglefilter = vtk.vtkTriangleFilter()
#        trianglefilter.SetInputData(self.exsurf)
#        trianglefilter.PassVertsOff()
#        trianglefilter.PassLinesOff()
#        trianglefilter.Update()
#        self.trisurf = trianglefilter.GetOutput()
        
        # Relate nodal equivalence indexing to plot indexing
        nnum = VN.vtk_to_numpy(self.exsurf.GetPointData().GetArray('ANSYSnodenum'))
        
        # Get sorted and reverse sorted indices
        pidx = np.argsort(nnum)
        pidx_r = np.argsort(pidx)
        
        # Get locations in sorted node number results array
        mask = np.in1d(self.nnum, nnum, assume_unique=True)
        if mask.sum() != len(nnum):
            raise Exception('Not all nodes from CDB are in the results file')
        
        # Store results index
        self.ridx = self.sidx[mask][pidx_r]
        
        
    def PlotDisplacement(self, rnum, comp='norm', autoclose=True,
                         as_abs=False):
        """
        SUMMARY
        Plots a result.  Must have a cdb must be loaded
        
        INPUTS
        rnum (interger)
            Result set requested.  Zero based indexing
            
        comp (string, optional) default = 'norm'
            Display component to display.  Options are 'x', 'y', 'z', and
            'comp'.
            
        """
        
        if not hasattr(self, 'exsurf'):
            raise Exception('Load CDB before displaying')
        
        # Load result from file
        result = self.GetResult(rnum, True)

        if comp == 'x':
            d = result[self.ridx, 0]
            stitle = 'X Displacement'
            
        elif comp == 'y':
            d = result[self.ridx, 1]
            stitle = 'Y Displacement'
            
        elif comp == 'z':
            d = result[self.ridx, 2]
            stitle = 'Z Displacement'
            
        else:
            # Normalize displacement
            d = result[self.ridx, :3]
            d = (d*d).sum(1)**0.5
            
            stitle = 'Normalized\nDisplacement'
            
        if as_abs:
            d = np.abs(d)

        # Add frequency at bottom of plot
        textActor = vtk.vtkTextActor()
        textActor.SetInput('Mode {:d} at {:f} Hz'.format(rnum + 1, self.tvalues[rnum]))
        textActor.SetPosition2 (80, 80)
        textActor.GetTextProperty().SetFontSize(24)
        textActor.GetTextProperty().SetColor (1.0, 1.0, 1.0)

        plobj = PlotClass()
        plobj.AddMesh(self.exsurf, scalars=d, stitle=stitle, flipscalars=True)
        plobj.ren.AddActor2D(textActor)
        plobj.Plot()
        cpos = plobj.GetCameraPosition()
        del plobj
        
        return cpos
#        if autoclose:
#            del plobj
#        else:
#            return plobj


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
    
#==============================================================================
# Plotting (ideally in its own module)
#==============================================================================
class PlotClass(object):
    """ Simple interface to VTK's underlying ploting """
    
    def __init__(self):

        # Add FEM Actor to renderer window
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0.3, 0.3, 0.3)
        
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(self.ren)
        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renWin)
        
        # Allow user to interact
        istyle = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(istyle)


    def AddMesh(self, mesh, color=[1, 1, 1], style='', scalars=[], name='',
                rng=[], stitle='', showedges=True, psize=5, opacity=1,
                linethick=[], flipscalars=False):
        """ Adds an actor to the renderwindow """
                
        # Create mapper
        mapper = vtk.vtkDataSetMapper()
        isscalars = False
                
        # Add scalars if they exist
        nscalars = len(scalars)
        if nscalars == mesh.GetNumberOfPoints():
            AddPointScalars(mesh, scalars, name)
            isscalars = True
            mapper.SetScalarModeToUsePointData()
#            mapper.GetLookupTable().SetTableRange(-1, 0)

#        elif nscalars == meshin.GetNumberOfCells():
#            VTK_Utilities.AddCellScalars(mesh, scalars, name)
#            isscalars = True
#            mapper.SetScalarModeToUseCellData()
                    
        # Set scalar range
        if isscalars:
            if not rng:
                rng = [np.min(scalars), np.max(scalars)]
                    
            if np.any(rng):
                mapper.SetScalarRange(rng[0], rng[1])
        
            # Flip if requested
            if flipscalars:
                mapper.GetLookupTable().SetHueRange(0.66667, 0.0)       
        
        # Set Scalar
        mapper.SetInputData(mesh)
        
        # Create Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        if style == 'wireframe':
            actor.GetProperty().SetRepresentationToWireframe()
        elif style == 'points':
            actor.GetProperty().SetRepresentationToPoints()
            actor.GetProperty().SetPointSize(psize)
        else:
            actor.GetProperty().SetRepresentationToSurface()
            
        if showedges:
            actor.GetProperty().EdgeVisibilityOn()
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOpacity(opacity)
        actor.GetProperty().LightingOff()
        
        if style == 'wireframe' and linethick:
            actor.GetProperty().SetLineWidth(linethick) 

        # Add to renderer
        self.ren.AddActor(actor)
        
        # Add scalar bar
        if stitle:
            scalarBar = vtk.vtkScalarBarActor()
            scalarBar.SetLookupTable(mapper.GetLookupTable())
            scalarBar.SetTitle(stitle)
            scalarBar.SetNumberOfLabels(5)    
            self.ren.AddActor(scalarBar)

        
    def GetCameraPosition(self):
        """ Returns camera position of active render window """
        camera = self.ren.GetActiveCamera()
        pos = camera.GetPosition()
        fpt = camera.GetFocalPoint()
        vup = camera.GetViewUp()
        return [pos, fpt, vup]
        

    def SetCameraPosition(self, cameraloc):
        """ Set camera position of active render window """
        camera = self.ren.GetActiveCamera()
        camera.SetPosition(cameraloc[0])
        camera.SetFocalPoint(cameraloc[1]) 
        camera.SetViewUp(cameraloc[2])        
        

    def SetBackground(self, bcolor):
        """ Sets background color """
        self.ren.SetBackground(bcolor)
        
        
    def AddLegend(self, entries, bcolor=[0.5, 0.5, 0.5], border=False):
        """
        Adds a legend to render window.  Entries must be a list containing
        one string and color entry for each item
        """
        
        legend = vtk.vtkLegendBoxActor()
        legend.SetNumberOfEntries(len(entries))
        
        c = 0
        nulldata = vtk.vtkPolyData()
        for entry in entries:
            legend.SetEntry(c, nulldata, entry[0], entry[1])
            c += 1
        
        legend.UseBackgroundOn()
        legend.SetBackgroundColor(bcolor)
        if border:
            legend.BorderOn()
        else:
            legend.BorderOff()
        
        # Add to renderer
        self.ren.AddActor(legend)
        
        
    def Plot(self, title=''):
        """ Renders """
        if title:
            self.renWin.SetWindowName(title)
            
        # Render
        self.iren.Initialize()
        self.renWin.Render()
        self.iren.Start()
        
        
    def AddActor(self, actor):
        """ Adds actor to render window """
        self.ren.AddActor(actor)
        
        
    def AddAxes(self):
        """ Add axes widget """
        axes = vtk.vtkAxesActor()
        widget = vtk.vtkOrientationMarkerWidget()
        widget.SetOrientationMarker(axes)
        widget.SetInteractor(self.iren)
        widget.SetViewport(0.0, 0.0, 0.4, 0.4)
        widget.SetEnabled(1)
        widget.InteractiveOn()
        

def AddPointScalars(mesh, scalars, name, setactive=True):
    """
    Adds point scalars to a VTK object or structured/unstructured grid """
    vtkarr = VN.numpy_to_vtk(np.ascontiguousarray(scalars), deep=True)
    vtkarr.SetName(name)
    mesh.GetPointData().AddArray(vtkarr)
    if setactive:
        mesh.GetPointData().SetActiveScalars(name)
        
    

