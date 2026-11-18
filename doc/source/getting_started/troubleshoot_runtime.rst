.. _ref_troubleshooting_runtime:

Connection, licensing, and runtime issues
=========================================

This page covers licensing, MPI, and network issues, as well as problems that
appear while you use PyMAPDL. For other problems, see :ref:`ref_troubleshooting`.

Licensing and network issues
----------------------------

.. _ref_mpi_issues:

Message Passing Interface (MPI) issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using a distributed memory parallel (DMP) version of MAPDL, you might
experience issues with the Message Passing Interface (MPI) communication libraries when running on AMD processors.
By default, MAPDL uses OpenMPI as the MPI implementation when running on AMD processors.
If OpenMPI has not been installed, or if you are trying to use IntelMPI on AMD processors, you might see an error similar to the following:

.. code:: text

    line 430: mpirun: command not found


To make sure you are using OpenMPI, pass the ``-mpi openmpi`` option to the :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>` function.

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(additional_switches="-mpi openmpi")

You can also run MAPDL in shared memory parallel (SMP) mode by passing the ``-smp`` option.

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(additional_switches="-smp")


See also :ref:`vpn_issues_troubleshooting` for incompatibilities between the VPN and the MPI communication.


.. _ref_licensing_issues:

Licensing issues
~~~~~~~~~~~~~~~~

Incorrect license server configuration can prevent MAPDL from being able to get a valid license.
In such cases, if you try to start MAPDL from the command line you might see an output **similar** to:


.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> & 'C:\Program Files\ANSYS Inc\v241\ansys\bin\winx64\ANSYS241.exe'

            ANSYS LICENSE MANAGER ERROR:

            Maximum licensed number of demo users already reached.


            ANSYS LICENSE MANAGER ERROR:

            Request name mech_2 does not exist in the licensing pool.
            No such feature exists.
            Feature:          mech_2
            License path:  C:\Users\user\AppData\Local\Temp\\cb0400ba-6edb-4bb9-a333-41e7318c007d;
            FlexNet Licensing error:-5,357

    .. tab-item:: Linux
        :sync: oskey

        .. code:: console

            (.venv) user@machine:~$ /usr/ansys_inc/v241/ansys/bin/ansys241

            ANSYS LICENSE MANAGER ERROR:

            Maximum licensed number of demo users already reached.


            ANSYS LICENSE MANAGER ERROR:

            Request name mech_2 does not exist in the licensing pool.
            No such feature exists.
            Feature:          mech_2
            FlexNet Licensing error:-5,357


Not enough licenses are available to start MAPDL.
In this case, contact your Ansys license administrator at your organization.

If you are responsible for maintaining Ansys licensing or have a personal installation of Ansys, see the
`Ansys Installation and Licensing documentation <ansys_installation_and_licensing_>`_.
If you cannot find the information you need, open a customer request ticket.

For an example blog post on licensing issues at ANSYS 2020R1, see `Changes to Licensing at ANSYS 2020R1 <padt_licensing_>`_.


Incorrect licensing environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The license server can be also specified using the environment variable :envvar:`ANSYSLMD_LICENSE_FILE`.
The following code examples show how you can see the value of this environment variable on
either Windows or Linux.


.. tab-set::

    .. tab-item:: Windows
        :sync: oskey

        .. code:: pwsh-session

            (.venv) PS C:\Users\user\pymapdl> $env:ANSYSLMD_LICENSE_FILE
            1055@1.1.1.1

    .. tab-item:: Linux
        :sync: oskey

        .. code:: console

            (.venv) user@machine:~$ printenv | grep ANSYSLMD_LICENSE_FILE
            1055@1.1.1.1


.. _vpn_issues_troubleshooting:

Virtual private network (VPN) issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From Ansys 2021 R1 to Ansys 2022 R2, MAPDL has issues launching when VPN software is running.
One issue stems from MPI communication. You can work around it by either:

- Passing the ``-smp`` option to set the execution mode to `Shared Memory Parallel`,
  which disables the default `Distributed Memory Parallel`.
- Using a different MPI library. For example, on Windows, pass ``-mpi msmpi`` to use
  the Microsoft MPI library instead of the default Intel MPI library.

This issue does not affect the Linux version of MAPDL.

.. note:: If you are using Windows in any of the versions from Ansys 2021 R1 to Ansys 2022 R2,
   the default MPI library is Microsoft MPI when the MAPDL instance is launched by PyMAPDL.

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(additional_switches="-smp")

While this approach has the disadvantage of using the potentially slower shared
memory parallel mode, you can still run MAPDL.
For more information on shared versus distributed memory, see
`High-Performance Computing for Mechanical Simulations using ANSYS <ansys_parallel_computing_guide_>`_.


In addition, if your device is connected to a VPN, MAPDL might not be able to correctly
resolve the IP of the license server. Verify that the hostname or IP address of the license server
is correct.

On Windows, you can find the license configuration file that points to the license server in ``C:\Program Files\ANSYS Inc\Shared Files\Licensing\ansyslmd.ini``.


Using a proxy server
~~~~~~~~~~~~~~~~~~~~

In some rare cases, you might have trouble connecting to the MAPDL instance if you are
using a proxy.
When `gRPC <grpc_>`_ is used in a proxy environment and a local address (``127.0.0.1``)
is specified as the connection destination, the gRPC implementation automatically refers to the proxy address.
In this case, the local address cannot be resolved, resulting in a connection error.
As a workaround, set the environment variable ``NO_PROXY`` to your local address ``127.0.0.1``,
and then run :func:`launch_mapdl() <ansys.mapdl.core.launcher.launch_mapdl>`
to connect to the MAPDL instance.


Firewall settings
~~~~~~~~~~~~~~~~~

MAPDL and Python should have the correct firewall settings to allow communication between the two.
If you are using a firewall, you should allow MAPDL to receive inbound connections to the following ports:

* ``50052`` (TCP) for gRPC connection.
* ``50053+`` (TCP) for extra gRPC connection.
* ``50055`` (TCP) for gRPC connection to the MAPDL database.

Allow the Python process to connect to the mentioned ports (outbound connections).

Most firewall rules focus on inbound connections, so you typically do not need to
configure outbound connections. However, if you are experiencing problems, make sure
the firewall is not blocking outbound connections on the following ports:

* ``5005X`` (TCP) for gRPC connections.
* ``50055`` (TCP) for gRPC connection to the MAPDL database.
* ``1055`` (TCP) for licensing connections.
* ``2325`` (TCP) for licensing connections.

For more information on how to **configure your firewall on Windows**, see
`Ansys forum-Licensing 2022 R2 Linux Ubuntu (and also Windows) <af_licensing_windows_ubuntu_>`_.

For more information on how to **configure your firewall on Ubuntu Linux**, see
`Security-Firewall | Ubuntu <ubuntu_firewall_>`_.


PyMAPDL usage issues
--------------------

.. _ref_issues_np_mapdl:

Issues when importing and exporting NumPy arrays in MAPDL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because of the way MAPDL is designed, there is no way to store an
array where one or more dimensions are zero.
This can happen in NumPy arrays, where the first dimension can be
set to zero. For example:

.. code:: pycon

   >>> import numpy
   >>> from ansys.mapdl.core import launch_mapdl
   >>> mapdl = launch_mapdl()
   >>> my_array = np.reshape([1, 2, 3, 4], (4,))
   >>> my_array
   array([1, 2, 3, 4])


These types of array dimensions are always converted to ``1``.

For example:

.. code:: pycon

   >>> mapdl.parameters["mapdlarray"] = my_array
   >>> mapdl.parameters["mapdlarray"]
   array([[1.],
      [2.],
      [3.],
      [4.]])
   >>> mapdl.parameters["mapdlarray"].shape
   (4, 1)

This means that when you pass two arrays—one with the second axis equal
to zero (for example, ``my_array``) and another with the second axis equal
to one—they have the same shape when later retrieved.

.. code:: pycon

   >>> my_other_array = np.reshape([1, 2, 3, 4], (4, 1))
   >>> my_other_array
   array([[1],
      [2],
      [3],
      [4]])
   >>> mapdl.parameters["mapdlarray_b"] = my_other_array
   >>> mapdl.parameters["mapdlarray_b"]
   array([[1.],
      [2.],
      [3.],
      [4.]])
   >>> np.allclose(mapdl.parameters["mapdlarray"], mapdl.parameters["mapdlarray_b"])
   True


.. _ref_pymapdl_stability:

PyMAPDL stability
-----------------

Recommendations
~~~~~~~~~~~~~~~

When connecting to an instance of MAPDL using gRPC (default), there are some cases
where the MAPDL server might exit unexpectedly. There
are several ways to improve MAPDL performance and stability:

Use ``mute`` to improve stability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When possible, pass ``mute=True`` to individual MAPDL commands or
set it globally with the :func:`Mapdl.mute <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.mute>`
method. This disables streaming back the response from MAPDL for each command
and marginally improves performance and stability. Consider having a debug flag in
your program or script so that you can turn on and off logging and
verbosity as needed.


Known Issues
~~~~~~~~~~~~

* MAPDL 2021 R1 has a stability issue with the
  :func:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>`
  method. Avoid using input files if possible. Attempt to use the
  :meth:`Mapdl.upload() <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.upload>` method to upload
  nodes and elements and read them in via the
  :func:`Mapdl.nread() <ansys.mapdl.core.Mapdl.nread>` and
  :func:`Mapdl.eread() <ansys.mapdl.core.Mapdl.eread>` methods.
