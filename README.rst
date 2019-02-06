pyansys
=======
.. image:: https://img.shields.io/pypi/v/pyansys.svg
    :target: https://pypi.org/project/pyansys/

.. image:: https://travis-ci.org/akaszynski/pyansys.svg?branch=master
    :target: https://travis-ci.org/akaszynski/pyansys

.. image:: http://readthedocs.org/projects/pyansys/badge/?version=latest
    :target: https://pyansys.readthedocs.io/

This Python module allows you to:
 - Interactively control an instance of ANSYS v14.5 + using Python on Linux, >=17.0 on Windows.
 - Extract data directly from binary ANSYS v14.5+ files and to display or animate them.
 - Rapidly read in binary result ``(.rst)``, binary mass and stiffness ``(.full)``, and ASCII block archive ``(.cdb)`` files.

See the `Documentation <http://pyansys.readthedocs.io>`_ page for more details.


Installation
------------
Installation through pip::

    pip install pyansys

You can also visit `GitHub <https://github.com/akaszynski/pyansys>`_ to download the source.


Quick Examples
--------------
Many of the following examples are built in and can be run from the build-in
examples module.  For a quick demo, run:

.. code:: python

    from pyansys import examples
    examples.run_all()


Controlling ANSYS
~~~~~~~~~~~~~~~~~
Create an instance of ANSYS and interactively send commands to it.  This is a direct interface and does not rely on writing a temporary script file.  You can also generate plots using ``matplotlib``.

.. code:: python

    import os
    import pyansys

    path = os.getcwd()
    ansys = pyansys.ANSYS(run_location=path, interactive_plotting=True)

    # create a square area using keypoints
    ansys.Prep7()
    ansys.K(1, 0, 0, 0)
    ansys.K(2, 1, 0, 0)
    ansys.K(3, 1, 1, 0)
    ansys.K(4, 0, 1, 0)    
    ansys.L(1, 2)
    ansys.L(2, 3)
    ansys.L(3, 4)
    ansys.L(4, 1)
    ansys.Al(1, 2, 3, 4)
    ansys.Aplot()
    ansys.Save()
    ansys.Exit()

.. figure:: https://github.com/akaszynski/pyansys/raw/master/doc/images/aplot.png
    :width: 500pt


Loading and Plotting an ANSYS Archive File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ANSYS archive files containing solid elements (both legacy and current), can be loaded using Archive and then converted to a vtk object.


.. code:: python

    import pyansys
    from pyansys import examples
    
    # Sample *.cdb
    filename = examples.hexarchivefile
    
    # Read ansys archive file
    archive = pyansys.Archive(filename)
    
    # Print raw data from cdb
    for key in archive.raw:
       print("%s : %s" % (key, archive.raw[key]))
    
    # Create a vtk unstructured grid from the raw data and plot it
    grid = archive.parse_vtk()
    grid.plot()
    
    # write this as a vtk xml file 
    grid.Write('hex.vtu')

.. figure:: https://github.com/akaszynski/pyansys/raw/master/doc/images/hexbeam.png
    :width: 500pt

You can then load this vtk file using vtki or another program that uses VTK.
    
.. code:: python

    # Load this from vtk
    import vtki
    grid = vtki.UnstructuredGrid('hex.vtu')
    grid.plot()


Loading the Result File
~~~~~~~~~~~~~~~~~~~~~~~

This example reads in binary results from a modal analysis of a beam from ANSYS.  This section of code does not rely on ``VTK`` and can be used with only numpy installed.

.. code:: python

    # Load the reader from pyansys
    import pyansys
    from pyansys import examples
    
    # Sample result file
    rstfile = examples.rstfile
    
    # Create result object by loading the result file
    result = pyansys.ResultReader(rstfile)
    
    # Beam natural frequencies
    freqs = result.time_values

.. code:: python

    >>> print(freq)
    [ 7366.49503969  7366.49503969 11504.89523664 17285.70459456
      17285.70459457 20137.19299035]
    
    # Get the 1st bending mode shape.  Results are ordered based on the sorted 
    # node numbering.  Note that results are zero indexed
    nnum, disp = result.nodal_solution(0)
    
.. code:: python

    >>> print(disp)
    [[ 2.89623914e+01 -2.82480489e+01 -3.09226692e-01]
     [ 2.89489249e+01 -2.82342416e+01  2.47536161e+01]
     [ 2.89177130e+01 -2.82745126e+01  6.05151053e+00]
     [ 2.88715048e+01 -2.82764960e+01  1.22913304e+01]
     [ 2.89221536e+01 -2.82479511e+01  1.84965333e+01]
     [ 2.89623914e+01 -2.82480489e+01  3.09226692e-01]
     ...


Plotting Nodal Results
~~~~~~~~~~~~~~~~~~~~~~
As the geometry of the model is contained within the result file, you can plot the result without having to load any additional geometry.  Below, displacement for the first mode of the modal analysis beam is plotted using ``VTK``.

.. code:: python
    
    # Plot the displacement of Mode 0 in the x direction
    result.plot_nodal_solution(0, 'x', label='Displacement')


.. figure:: https://github.com/akaszynski/pyansys/raw/master/doc/images/hexbeam_disp.png
    :width: 500pt


Results can be plotted non-interactively and screenshots saved by setting up the camera and saving the result.  This can help with the visualization and post-processing of a batch result.

First, get the camera position from an interactive plot:

.. code:: python

    >>> cpos = result.plot_nodal_solution(0)
    >>> print(cpos)
    [(5.2722879880979345, 4.308737919176047, 10.467694436036483),
     (0.5, 0.5, 2.5),
     (-0.2565529433509593, 0.9227952809887077, -0.28745339908049733)]

Then generate the plot:

.. code:: python

    result.plot_nodal_solution(0, 'x', label='Displacement', cpos=cpos,
                             screenshot='hexbeam_disp.png',
                             window_size=[800, 600], interactive=False)

Stress can be plotted as well using the below code.  The nodal stress is computed in the same manner that ANSYS uses by to determine the stress at each node by averaging the stress evaluated at that node for all attached elements.  For now, only component stresses can be displayed.

.. code:: python
    
    # Display node averaged stress in x direction for result 6
    result.plot_nodal_stress(5, 'Sx')

.. figure:: https://github.com/akaszynski/pyansys/raw/master/doc/images/beam_stress.png
    :width: 500pt


Nodal stress can also be generated non-interactively with:

.. code:: python

    result.plot_nodal_stress(5, 'Sx', cpos=cpos, screenshot=beam_stress.png,
                           window_size=[800, 600], interactive=False)


Animating a Modal Solution
~~~~~~~~~~~~~~~~~~~~~~~~~~
Mode shapes from a modal analsyis can be animated using ``animate_nodal_solution``:

.. code:: python

    result.animate_nodal_solution(0)

If you wish to save the animation to a file, specify the movie_filename and animate it with:

.. code:: python

    result.animate_nodal_solution(0, movie_filename='/tmp/movie.mp4', cpos=cpos)

.. figure:: https://github.com/akaszynski/pyansys/raw/master/doc/images/beam_mode_shape.gif
    :width: 500pt


Reading a Full File
-------------------
This example reads in the mass and stiffness matrices associated with the above example.

.. code:: python

    # Load the reader from pyansys
    import pyansys
    from scipy import sparse
    
    # load the full file
    fobj = pyansys.FullReader('file.full')
    dofref, k, m = fobj.load_km()  # returns upper triangle only

    # make k, m full, symmetric matricies
    k += sparse.triu(k, 1).T
    m += sparse.triu(m, 1).T

If you have ``scipy`` installed, you can solve the eigensystem for its natural frequencies and mode shapes.

.. code:: python

    from scipy.sparse import linalg

    # condition the k matrix
    # to avoid getting the "Factor is exactly singular" error
    k += sparse.diags(np.random.random(k.shape[0])/1E20, shape=k.shape)

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


License and Acknowledgments
---------------------------
``pyansys`` is licensed under the MIT license.

ANSYS documentation and functions build from html provided by `Sharcnet <https://www.sharcnet.ca/Software/Ansys/>`_.  Thanks!

This module, ``pyansys`` makes no commercial claim over ANSYS whatsoever.  This tool extends the functionality of ``ANSYS`` by adding a python interface in both file interface as well as interactive scripting without changing the core behavior or license of the original software.  The use of the interactive APDL control of ``pyansys`` requires a legally licensed local copy of ANSYS.
