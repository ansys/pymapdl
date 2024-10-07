
.. _ref_hpc_troubleshooting:


Troubleshooting
===============

Debugging jobs
--------------
- Use ``--output`` and ``--error`` directives in batch scripts to captures
  standard output and error messages to specific files.

  .. code-block:: bash

      #!/bin/bash
      #SBATCH --job-name=ansys_job            # Job name
      #SBATCH --partition=qsmall              # Specify the queue/partition name
      #SBATCH --output=ansys_job.out          # Standard output file
      #SBATCH --error=ansys_job.err           # Standard error file

      source /home/user/pymapdl/.venv/bin/activate
      python /home/user/pymapdl.py

- Check SLURM logs for error messages and debugging information.


.. _ref_python_venv_not_accesible:

Python virtual environment is not accessible
--------------------------------------------
If there is an error while testing the Python installation, it might mean 
that the Python environment is not accessible to the compute nodes.
For example, given the following *bash* script `test.sh`:

.. code-block:: bash

   source /home/user/.venv/bin/activate
   python -c "from ansys.mapdl import core as pymapdl; pymapdl.report()"

The following output is shown after running in the terminal:

.. code-block:: console

    user@machine:~$ srun test.sh

    Testing Python!
    Traceback (most recent call last):
    File "<string>", line 1, in <module>
    ImportError: No module named ansys.mapdl

As the output shows, PyMAPDL could not be found, meaning that either:
* The virtual environment does not have PyMAPDL installed.
  See :ref:`ref_install_pymapdl_on_hpc`.
* Or the script did not activate properly the virtual environment
  (``/home/user/.venv``).

For the second reason, there could be a number of reasons.
One of them is that the system Python distribution used to create
the virtual environment is not accessible from the compute nodes
due to one of these reasons:

- The virtual environment has been created in a
  directory that is not accessible from the nodes.
  In this case, your terminal might also show that the
  ``activate`` file could not be found.

  .. code-block:: console

     user@machine:~$ srun test.sh
     Testing Python!
     bash: .venv/bin/activate: No such file or directory

  Depending on your terminal configuration, the above error might be sufficient
  to exit the terminal process, or not. 
  If not, the execution will continue, and the subsequent ``python`` call will
  be executed using the default python executable.
  It is very likely that the default ``python`` executable does not have
  PyMAPDL installed, hence the ``ImportError`` error showed above might appear
  too.

- The virtual environment has been created from a Python executable that is
  not available to the compute nodes. Hence, the virtual environment is not
  activated.
  For example, you might be creating the virtual environment Using
  Python 3.10, but only Python 3.8 is available from the compute nodes.
  You can test which Python executable the cluster is using by starting an
  interactive session in a compute node with this code to list all commands
  which starts with ``python``:

.. code-block:: console

    user@machine:~$ srun --pty /bin/bash
    user@compute_node_01:~$ compgen -c | grep python

.. the approach to solve this comes from:
   https://stackoverflow.com/questions/64188693/problem-with-python-environment-and-slurm-srun-sbatch

It should be noticed the above approach assumes that all the nodes have similar
configuration, hence all of them should have the same Python installations
available.

It is also convenient to be aware that environment variable modules can be
used to activate Python installations.
For more information, see :ref:`ref_envvar_modules_on_hpc`.


.. _ref_envvar_modules_on_hpc:

Using modules to load Python
----------------------------

Many HPC infrastructures use environment managers to load and unload
software packages using modules and environment variables.
Hence, you might want to make sure that the correct module is loaded in your
script.

For information on two of the most common environment managers, see the
`Modules documentation <modules_docs_>`_ and `Lmod documentation <lmod_docs_>`_.
Check your cluster documentation to know which environment
manager is being using and how to load Python with it.
If you find any issue, you should contact your cluster administrator.

If there is not a suitable Python version accessible from the
compute nodes, you might have to request your HPC cluster
administrator to have a suitable Python version installed on all
compute nodes.
If this is not an option, see :ref:`ref_ansys_provided_python`.

.. _ref_ansys_provided_python:

Using the Ansys-provided Python installation
--------------------------------------------

**For development purposes only**

In certain HPC environments the possibility of installing a different Python
version is limited for security reasons.
In such cases, the Python distribution available in the Ansys installation
can be used.
This Python distribution is a customized Python (CPython) version for Ansys
products use only.
Its use is **discouraged** except for very advanced users and special use
cases.

This Python distribution is in the following directory, where
``%MAPDL_VERSION%`` is the three-digit Ansys version:

.. code-block:: text

    /ansys_inc/v%MAPDL_VERSION%/commonfiles/CPython/3_10/linx64/Release/python

For example, here is the directory for Ansys 2024 R2:

.. code-block:: text

    /ansys_inc/v242/commonfiles/CPython/3_10/linx64/Release/python


In Ansys 2024 R1 and later, the unified installer includes CPython 3.10.
Earlier versions include CPython 3.7
(``/commonfiles/CPython/3_7/linx64/Release/python``).

Because the Ansys installation must be available to all
the compute nodes to run simulations using them, this
Python distribution is normally also available to the
compute nodes. Hence, you can use it to create your
own virtual environment.

Due to the particularities of this Python distribution, you must
follow these steps to create a virtual environment accessible to
the compute nodes:

#. Set the Python path environment variable:

   .. code-block:: console

      user@machine:~$ export PY_PATH=/ansys_inc/v241/commonfiles/CPython/3_10/linx64/Release/Python

#. For only Ansys 2024 R1 and earlier, patch the ``PATH`` and ``LD_LIBRARY_PATH``
   environment variables:

   .. code-block:: console

      user@machine:~$ PATH=$PY_PATH/bin:$PATH  # Patching path
      user@machine:~$ LD_LIBRARY_PATH=$PY_PATH/lib:$LD_LIBRARY_PATH  # Patching LD_LIBRARY_PATH

#. On the same terminal, create your own virtual
   environment and activate it:

   .. code-block:: console

      user@machine:~$ $PY_PATH -m venv /home/user/.venv
      user@machine:~$ source /home/user/.venv

4. Install PyMAPDL:

   .. code-block:: console 

      (.venv) user@machine:~$ python -m pip install ansys-mapdl-core

5. Use it to launch simulations, using ``srun``:

   .. code-block:: console

      (.venv) user@machine:~$ srun pymapdl_script.py

   or ``sbatch``:

   .. code-block:: console

      (.venv) user@machine:~$ sbatch job.sh
      Submitted batch job 1
