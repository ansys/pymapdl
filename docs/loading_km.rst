Working with a ANSYS Full File (full)
======================================
The ANSYS full file is a FORTRAN formatted binary file containing the mass and stiffness from an ANSYS analysis.  Using pyansys it can be loaded into memory as either a sparse or full matrix.


Reading a Full File
-------------------
This example reads in the mass and stiffness matrices associated with the above example.  ``load_km`` sorts degrees of freedom such that the nodes are ordered from minimum to maximum, and each degree of freedom (i.e. X, Y, Z), are sorted within each node.  The matrices ``k`` and ``m`` are sparse by default, but if ``scipy`` is not installed, or if the optional parameter ``as_sparse=False`` then they will be full numpy arrays.

By default ``load_km`` outputs the upper triangle of both matrices.  The constrained nodes of the analysis can be identified by accessing ``fobj.const`` where the constrained degrees of freedom are True and all others are False.  This corresponds to the degrees of reference in ``dof_ref``.

By default dof_ref is unsorted.  To sort these values, set ``sort==True``.  It is enabled for this example to allow for plotting of the values later on.

.. code:: python

    # Load pyansys
    import pyansys
    from pyansys import examples
    
    # Create result reader object and read in full file
    full = pyansys.FullReader(examples.fullfile)
    dof_ref, k, m = full.load_km(sort=True)


ANSYS only stores the upper triangular matrix in the full file.  To make the full matrix:

.. code:: python

    k += sparse.triu(k, 1).T
    m += sparse.triu(m, 1).T

If you have ``scipy`` installed, you can solve solve for the natural frequencies and mode shapes of a system.  

.. code:: python

    import numpy as np
    from scipy.sparse import linalg

    # condition the k matrix
    # to avoid getting the "Factor is exactly singular" error
    k += sparse.diags(np.random.random(k.shape[0])/1E20, shape=k.shape)

    # Solve
    w, v = linalg.eigsh(k, k=20, M=m, sigma=10000)

    # System natural frequencies
    f = (np.real(w))**0.5/(2*np.pi)    
    
.. code:: 

    print('First four natural frequencies')
    for i in range(4):
        print('{:.3f} Hz'.format(f[i]))

    First four natural frequencies
    1283.200 Hz
    1283.200 Hz

    5781.975 Hz
    6919.399 Hz


Plotting a Mode Shape
---------------------
You can also plot the mode shape of this finite element model.  Since the constrained degrees of freedom have been removed from the solution, you have to account for these when displaying the displacement.

.. code:: python
    
    import vtki

    # Get the 4th mode shape
    full_mode_shape = v[:, 3] # x, y, z displacement for each node
    
    # reshape and compute the normalized displacement
    disp = full_mode_shape.reshape((-1, 3))
    n = (disp*disp).sum(1)**0.5
    n /= n.max() # normalize
    
    # load an archive file and create a vtk unstructured grid
    archive = pyansys.Archive(pyansys.examples.hexarchivefile)
    grid = archive.parse_vtk()
    
    # plot the normalized displacement
    # grid.plot(scalars=n)
    
    # Fancy plot the displacement
    plobj = vtki.Plotter()
    
    # add the nominal mesh
    plobj.add_mesh(grid, style='wireframe')
	  
    # copy the mesh and displace it
    new_grid = grid.copy()
    new_grid.points += disp/80
    plobj.add_mesh(new_grid, scalars=n, stitle='Normalized\nDisplacement',
                  flipscalars=True)
    
    plobj.add_text('Cantliver Beam 4th Mode Shape at {:.4f}'.format(f[3]),
                   fontsize=30)
    plobj.plot()
    
.. image:: ./images/solved_km.png


This example is built into ``pyansys`` and can be run from  ``examples.SolveKM()``.


FullReader Object Methods
-------------------------
.. autoclass:: pyansys.FullReader
    :members:
