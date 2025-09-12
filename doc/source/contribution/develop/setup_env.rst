.. _ref_setup_development_environment:

Setup development environment
=============================

To set up your development environment, follow these steps:

#. :ref:`ref_clone_pymapdl_repository`
#. :ref:`ref_create_virtual_environment`
#. :ref:`ref_install_pymapdl_in_dev_mode`
#. :ref:`ref_install_precommit`


.. _ref_clone_pymapdl_repository:

Clone the PyMAPDL repository
----------------------------

Before cloning the PyMAPDL repository, you must install a version control system such as Git.
You can this run this code to clone the latest development version of PyMAPDL:

.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            PS C:\Users\mapdl> git clone https://github.com/ansys/pymapdl
            PS C:\Users\mapdl> cd pymapdl

    .. tab-item:: Linux/MacOS
        :sync: key1

        .. code:: console

            mapdl@machine:~$ git clone https://github.com/ansys/pymapdl
            mapdl@machine:~$ cd pymapdl


.. _ref_create_virtual_environment:

Create a Python virtual environment
-----------------------------------

To avoid dependency conflicts and more easily manage upgrades, you should install PyMAPDL in its own virtual environment. For detailed information on how to install Python and create a virtual environment, see
`Setting up your development environment <dev_guide_setup_your_environment_>`_.


.. _ref_install_pymapdl_in_dev_mode:

Install PyMAPDL in development mode
-----------------------------------

Install the latest version of PyMAPDL in development mode with these commands:

.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            PS C:\Users\mapdl> cd pymapdl
            PS C:\Users\mapdl\pymapdl> .venv/Scripts/Activate.ps1
            (.venv) PS C:\Users\mapdl\pymapdl> pip install pip -U
            (.venv) PS C:\Users\mapdl\pymapdl> pip install -e .

    .. tab-item:: Linux/MacOS
        :sync: key1

        .. code:: console

            mapdl@machine:~$ cd pymapdl
            mapdl@machine:~/pymapdl$ source .venv/bin/activate
            (.venv) mapdl@machine:~/pymapdl$ pip install pip -U
            (.venv) mapdl@machine:~/pymapdl$ pip install -e .


To do testing (required if you are planning to contribute),
you must install the testing dependencies with this command:


.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\mapdl\pymapdl> pip install -e '.[tests]'

    .. tab-item:: Linux/MacOS
        :sync: key1

        .. code:: console

            (.venv) mapdl@machine:~/pymapdl$ pip install -e '.[tests]'


.. _ref_install_precommit:

Install pre-commit
------------------

It is highly recommended to install `pre-commit <precommit_>`_ to ensure that your code
follows the PyMAPDL code style. To install it, run this command:

.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\mapdl\pymapdl> pip install pre-commit

    .. tab-item:: Linux/MacOS
        :sync: key1

        .. code:: console

            (.venv) mapdl@machine:~/pymapdl$ pip install pre-commit


To run pre-commit on all the repository files run this command:

.. tab-set::
    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\mapdl\pymapdl> pre-commit run --all-files

    .. tab-item:: Linux/MacOS
        :sync: key1

        .. code:: console

            (.venv) mapdl@machine:~/pymapdl$ pre-commit run --all-files

If you want to run on certain files only you can run the following command:

.. tab-set::
    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\mapdl\pymapdl> pre-commit run --files ./path/to/my/file0 ./path/to/my/file1

    .. tab-item:: Linux/MacOS
        :sync: key1

        .. code:: console

            (.venv) mapdl@machine:~/pymapdl$ pre-commit run --files ./path/to/my/file0 ./path/to/my/file1


If you want to automatically run pre-commit checks before each commit, you can install the Git hook by running:

.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            (.venv) PS C:\Users\mapdl\pymapdl> pre-commit install

    .. tab-item:: Linux/MacOS
        :sync: key1

        .. code:: console

            (.venv) mapdl@machine:~/pymapdl$ pre-commit install


Now you are ready to start developing, go to :ref:`developing_pymapdl`.
