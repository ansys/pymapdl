"""
.. _ref_mapdl_math_mapdl_vs_scipy:

Compute Eigenvalues using MAPDL or SciPy
----------------------------------------

This example shows:

- How to extract the stiffness and mass matrices from a MAPDL model.
- How to use the ``Math`` module of PyMapdl to compute the first
  eigenvalues.
- How to can get these matrices in the SciPy world, to get the same
  solutions using Python resources.
- How MAPDL is really faster than SciPy :)
"""

###############################################################################
# First load python packages we need for this example
import time
import math

import matplotlib.pylab as plt
import numpy as np
import scipy
from scipy.sparse.linalg import eigs, eigsh

from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core import examples

###############################################################################
# Next:
#
# - Load the ansys.mapdl module
# - Get the ``Math`` module of PyMapdl
#
mapdl = launch_mapdl()
print(mapdl)
mm = mapdl.math

###############################################################################
# APDLMath EigenSolve
# First ask MAPDL to load the input file
#
print(mapdl.input(examples.examples.wing_model))

###############################################################################
# Plot and mesh using the ``eplot`` method.
mapdl.eplot()


###############################################################################
# Next, setup a modal Analysis and ask for the $K$ and $M$ matrices to
# be formed. MAPDL store these matrices in a ``.FULL`` file.

print(mapdl.slashsolu())
print(mapdl.antype(antype='MODAL'))
print(mapdl.modopt(method='LANB', nmode='10', freqb='1.'))
print(mapdl.wrfull(ldstep='1'))

# store the output of the solve command
output = mapdl.solve()


###############################################################################
# Read Sparse Matrices using pyMapdl
#
mapdl.finish()
mm.free()
K = mm.stiff(fname='file.full')
M = mm.mass(fname='file.full')


###############################################################################
# PyMapdl solves the Eigenproblem
# 
nev = 10
A = mm.mat( K.nrow, nev)

print( '\nCalling MAPDL to solve the eigenproblem .. \n')
t1 = time.time()
ev = mm.eigs( nev, K, M, phi=A, fmin=1.)
t2 = time.time()
MapdlElapsedTime = t2-t1
print( '\nElapsed time to solve this problem : ', MapdlElapsedTime)

###############################################################################
# Print EigenFrequencies && Accuracy
# 
# Accuracy : $\frac{||(K-\lambda.M).\phi||_2}{||K.\phi||_2}$
# 
MapdlAcc = np.zeros(nev)

for i in range(0, nev):
    F = ev[i]                        # Eigenfrequency (Hz)
    omega = 2*np.pi*F                # omega = 2.pi.Frequency
    lam = omega**2                   # lambda = omega^2
    
    Phi = A[i]                       # i-th eigenshape                      
    KPhi = K.dot(Phi)                     # K.Phi                                
    MPhi = M.dot(Phi)                     # M.Phi                                
    
    KPhinrm = KPhi.norm()             # Normalization scalar value           

    MPhi *= lam                      # (K-\lambda.M).Phi
    KPhi -= MPhi
    
    MapdlAcc[i] = KPhi.norm()/KPhinrm      # We compute the residual
    print( "[",i,"] : Freq = ",F,"\tHz, \t Residual = ",MapdlAcc[i])

    
###############################################################################
# Ask SciPy to solve the same problem
#
# First get MAPDL sparse matrices into SciPy world
# 
pK = K.asarray()
pM = M.asarray()

#get_ipython().run_line_magic('matplotlib', 'inline')

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('K and M Matrix profiles')
ax1.spy( pK, markersize=0.01)
ax1.set_title('K Matrix')
ax2.spy( pM, markersize=0.01)
ax2.set_title('M Matrix')
plt.show(block=True)


###############################################################################
# Need to Unsymetrize the sparse matrices for SciPy
#  ( -> Not good for memory usage)
#
# $K = K + K^T - diag(K)$
#
pKd = scipy.sparse.diags(pK.diagonal())
pK = pK + pK.transpose() - pKd
pMd = scipy.sparse.diags(pM.diagonal())
pM = pM + pM.transpose() - pMd


###############################################################################
# Plot Matrices
#
#get_ipython().run_line_magic('matplotlib', 'inline')

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('K and M Matrix profiles')
ax1.spy( pK, markersize=0.01)
ax1.set_title('K Matrix')
ax2.spy( pM, markersize=0.01)
ax2.set_title('M Matrix')
plt.show(block=True)


###############################################################################
# Run the Eigensolve
# 
print( '\nCalling SCIPY to solve the eigenproblem .. \n')
t3 = time.time()
vals, vecs = eigsh( A=pK, M=pM, k=10, sigma=1, which='LA')
t4 = time.time()
SciPyElapsedTime = t4-t3
print( '\nElapsed time to solve this problem : ', SciPyElapsedTime)


###############################################################################
# We convert Lambda values to Frequency values:
# $freq = \frac{\sqrt(\lambda)}{2.\pi}$
#
Freqs = np.sqrt(vals) / (2*math.pi)


###############################################################################
# We compute residual errors:
# $Err=\frac{||(K-\lambda.M).\phi||_2}{||K.\phi||_2}$
#
SciPyAcc = np.zeros(nev)

for i in range(0, nev):
    lam = vals[i]                      # i-th eigenvalue
    Phi = vecs.T[i]                    # i-th eigenshape
    
    KPhi = pK*Phi.T                    # K.Phi
    MPhi = pM*Phi.T                    # M.Phi
    
    KPhinrm = np.linalg.norm(KPhi,2)             # Normalization scalar value

    MPhi *= lam                      # (K-\lambda.M).Phi
    KPhi -= MPhi
    
    SciPyAcc[i] = np.linalg.norm(KPhi,2)/KPhinrm      # We compute the residual
    print( "[",i,"] : Freq = ", Freqs[i], "\tHz, \t Residual = ", SciPyAcc[i])


###############################################################################
# How MAPDL is more accurate than SciPy
#
fig = plt.figure(figsize=(12,10))
ax = plt.axes()
x = np.linspace(1, 10, 10)
plt.title('Residual Error (%)')
plt.yscale('log')
plt.xlabel('Frequency #')
plt.ylabel('Errors (%)')
ax.bar(x, SciPyAcc, label='SciPy Results')
ax.bar(x, MapdlAcc, label='MAPDL Results')
plt.legend(loc='lower right')


###############################################################################
# How MAPDL is faster than SciPy
# 
Ratio = SciPyElapsedTime/MapdlElapsedTime
print( "Mapdl is ",Ratio," times faster")
