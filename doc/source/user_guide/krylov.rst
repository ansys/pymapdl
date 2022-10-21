=========================================
Harmonic analysis using the Krylov method
=========================================

Introduction
============
You can use the frequency-sweep Krylov method for a high-performance solution of forced-frequency simulations 
in acoustic or single-field structural analyses.

Similar to the full harmonic analysis, the frequency sweep Krylov method also uses the full system matrices 
to compute the harmonic response. While the full method solves the full system matrices at every frequency point 
in the frequency range, the frequency-sweep Krylov method performs the following steps to approximate the response 
across the frequency range :

* Builds a Krylov subspace set of vectors at the frequency value in the middle of the requested
  frequency range
* Reduces the system matrices and loading on the entire frequency range
* Solves the reduced system
* Expands the results back to compute the harmonic response 

MAPDL provides the following methods to implement a harmonic analysis using the Krylov Method:

#. Via Mechanical APDL commands.
#. Via macros, a feature described in *Frequency-Sweep Harmonic Analysis via the Krylov Method* in the *Structural Analysis Guide*.
#. PyMAPDL implementation of the macros, a feature described here.

Assumptions
-----------
The following assumptions are made in the Krylov solution obtained using this method :

* The stiffness, mass, and damping matrices are assumed to be constant (independent of frequency).

* The external load vector is linearly ramped over frequency. Ramping assumes that the frequency at 
  which the Krylov subspace is built is in the middle of the frequency range. If you want to apply 
  stepped loading, there is an option to specify that in the inputs for the 
  :func:`KrylovSolver.krysolve() <ansys.mapdl.core.krylov.KrylovSolver.krysolve>` method.


Krylov method implementation in PyMADL
======================================
The PyMAPDL implementation of the Kylov method gives you customization and flexibility
because you can access
subspace vectors and reduced solutions using the Python programming language for user-defined routines.

If you do not require customization, you can use the simpler using APDL commands to solve a harmonic analysis 
with the Krylov method.
 
The procedure described here implements an analysis identical to that defined by the macros.
Details on the theory and equations describing the Krylov method can be found in the works of Puri [1]_ and Eser [2]_ .

The exposure in PyMAPDL follows the same theory as the APDL macro and has the following methods:

* :func:`KrylovSolver.krygensub() <ansys.mapdl.core.krylov.KrylovSolver.krygensub>`: Creates the Krylov subspace. 
* :func:`KrylovSolver.krysolve() <ansys.mapdl.core.krylov.KrylovSolver.krysolve>`: Solves the reduced system of equations.
* :func:`KrylovSolver.kryexpand() <ansys.mapdl.core.krylov.KrylovSolver.kryexpand>`: Expands the Krylov subspace.

.. warning:: These methods must be run consecutively.

Usage
=====

Generate the full file (``.full``) for the Krylov method using Mechanical APDL:

.. code:: py

    >>> from ansys.mapdl.core import launch_mapdl
    
    >>> mapdl = launch_mapdl()
    >>> mapdl.prep7()

	# Generate the FEA model (mesh, constraints, loads)
  # ...

    >>> mapdl.run("/SOLU")
    >>> mapdl.antype("HARMIC")  # HARMONIC ANALYSIS
    >>> mapdl.hropt("KRYLOV")
    >>> mapdl.eqslv("SPARSE")
    >>> mapdl.harfrq(0,1000)  # Set beginning and ending frequency
    >>> mapdl.nsubst(100)  # Set the number of frequency increments
    >>> mapdl.wrfull(1)  # GENERATE .FULL FILE AND STOP
    >>> mapdl.solve()
    >>> mapdl.finish()

Create an instance of the Krylov class
--------------------------------------

.. code:: py
    
    >>> mk = mapdl.krylov

Call the :func:`krygensub <ansys.mapdl.core.krylov.KrylovSolver.krygensub>` method, which creates the Krylov subspace:
Build a subspace of Size / Dimension 10 and at a frequency of 500 Hz.

.. code:: py

    >>> Qz = mk.krygensub(10, 500, True, True)

Return the Krylov subspace
--------------------------

Call the :func:`krysolve <ansys.mapdl.core.krylov.KrylovSolver.krysolve>` method, which reduces
the system of equations, and then solve at each frequency. The following code solves from 0 Hz
to 1000 Hz with 100 intervals in between, with stepped loading.

.. code:: py

    >>> Yz = mk.krysolve(0, 1000, 100, 1, True)


Return the reduced solution over the frequency range
----------------------------------------------------
            
Call the :func:`kryexpand <ansys.mapdl.core.krylov.KrylovSolver.kryexpand>` method, which expands the reduced solution back to FE space. Output the expanded solution and calculate the residual.   

.. code:: py

    >>> results = mk.kryexpand(True, 3)

Return Ndarray (if out_key = True) solution vectors mapped to User order.

.. note:: The ``ndarray`` returned by the method ``kryexpand`` contains the node number
   along with the dof solution for each of the calculated frequencies.

Get the dof solution at a specific frequency
--------------------------------------------

.. code:: py

   # Get the nodal solution at freq number 3``````
   >>> node_order = res[2]['node'] # Get the nodal order   
   >>> for node_num in node_order:
   >>> 	   nodal_sol = res[2][node_num]['x'] # Get the nodal solution for each node

Example
=======

Examples of using the Krylov method in PyMAPDL are available in :ref:`krylov_example`.

Requirements
============

To use ``krylov`` feature, you need to meet the following requirements:

* ANSYS MAPDL version should be 2022R2 or newer.

.. warning:: This feature does not support Distributed Ansys. 
    However, you can still run MAPDL Math commands without specifying the ``-smp`` flag when
    launching MAPDL.

Reference
=========
For additional details, for the krylov method refer the `APDL Docummentation Manual 
<https://ansysproducthelpqa.win.ansys.com/account/secured?returnurl=/Views/Secured/corp/v231/en/ans_str/str_Krysweep.html>`_

.. [1] Puri, S. R. (2009). Krylov Subspace Based Direct Projection Techniques for Low Frequency,
   Fully Coupled, Structural Acoustic Analysis and Optimization. PhD Thesis. Oxford Brookes University,
   Mechanical Engineering Department. Oxford, UK.

.. [2] Eser, M. C. (2019) Efficient Evaluation of Sound Radiation of an Electric Motor using Model Order
   Reduction.MSc Thesis. Technical University of Munich, Mechanical Engineering Department. Munich, DE.
