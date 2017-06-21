Working with a ANSYS Full File (full)
======================================

The ANSYS full file is a fortran formatted binary file containing the mass and
stiffness from an ANSYS analysis.  Using pyansys it can be loaded into memory
as either a sparse or full matrix.


Reading a Full File
-------------------
This example reads in the mass and stiffness matrices associated with the above
example.  By default, ``LoadKM`` sorts degrees of freedom such that the nodes are
ordered from minimum to maximum, and each degree of freedom (i.e. X, Y, Z), are
sorted within each node.  This increases the bandwidth of mass and stiffness
matrices and can be disabled by setting ``sort=False``.  The matrices ``k`` and
``m`` are sparse by default, but if ``scipy`` is not installed, or if the
optional parameter ``as_sparse=False`` then they will be full numpy arrays.

.. code:: python

    # Load pyansys
    import pyansys
    
    # Create result reader object and read in full file
    fobj = pyansys.FullReader('file.full')
    dof_ref, k, m = fobj.LoadKM()
    

If you have ``scipy`` installed, you can solve solve for the natural 
frequencies of a system.

.. code:: python

    from scipy.sparse import linalg
    #numpy.linalg.eig

    # Solve
    w, v = linalg.eigsh(k, k=20, M=m, sigma=10000)

    # System natural frequencies
    f = (np.real(w))**0.5/(2*np.pi)
    
    print('First four natural frequencies')
    for i in range(4):
        print '{:.3f} Hz'.format(f[i])
    
.. code:: 

    First four natural frequencies
    1283.200 Hz
    1283.200 Hz
    5781.975 Hz
    6919.399 Hz
    
This exact example can be run from pyansys's examples::

    from pyansys import examples
    examples.LoadKM()
    
    
    
