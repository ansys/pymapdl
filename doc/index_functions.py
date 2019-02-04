#==============================================================================
# load a beam and write it
#==============================================================================
import pyansys
from pyansys import examples

# Sample *.cdb
filename = examples.hexarchivefile

# Read ansys archive file
archive = pyansys.Archive(filename)

# Print raw data from cdb
for key in archive.raw:
   print "%s : %s" % (key, archive.raw[key])

# Create a vtk unstructured grid from the raw data and plot it
archive.ParseFEM()
archive.uGrid.Plot()

# write this as a vtk xml file 
archive.save_as_vtk('hex.vtu')


# Load this from vtk
import vtki
grid = vtki.LoadGrid('hex.vtk')
grid.Plot()


#==============================================================================
# load beam results
#==============================================================================
# Load the reader from pyansys
import pyansys
from pyansys import examples

# Sample result file and associated archive file
rstfile = examples.rstfile
hexarchivefile = examples.hexarchivefile


# Create result reader object by loading the result file
result = pyansys.ResultReader(rstfile)

# Get beam natural frequencies
freqs = result.GetTimeValues()

# Get the node numbers in this result file
nnum = result.nnum

# Get the 1st bending mode shape.  Nodes are ordered according to nnum.
disp = result.GetResult(0, True) # uses 0 based indexing 

# Load CDB (necessary for display)
result.LoadArchive(hexarchivefile)

# Plot the displacement of Mode 0 in the x direction
result.PlotNodalResult(0, 'x', label='Displacement')


#==============================================================================
# Load KM
#==============================================================================

# Load the reader from pyansys
import pyansys
from pyansys import examples


filename = examples.fullfile

# Create result reader object and read in full file
fobj = pyansys.FullReader(filename)
fobj.LoadFullKM()
    
import numpy as np
from scipy.sparse import csc_matrix, linalg
ndim = fobj.nref.size
k = csc_matrix((fobj.kdata, (fobj.krows, fobj.kcols)), shape=(ndim, ndim))
m = csc_matrix((fobj.mdata, (fobj.mrows, fobj.mcols)), shape=(ndim, ndim))

# Solve
w, v = linalg.eigsh(k, k=20, M=m, sigma=10000)
# System natural frequencies
f = (np.real(w))**0.5/(2*np.pi)

print('First four natural frequencies')
for i in range(4):
    print '{:.3f} Hz'.format(f[i])
