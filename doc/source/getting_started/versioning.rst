***********************
Versions and interfaces
***********************
The PyMAPDL project attempts to maintain compatibility with legacy
versions of MAPDL while allowing for support of faster and better
interfaces with the latest versions of MAPDL.


Ansys 2021 R1 and later
~~~~~~~~~~~~~~~~~~~~~~~
Ansys 2020 R1 and later support the latest gRPC interface, allowing
for remote management of MAPDL with rapid streaming of mesh, results,
and files from the MAPDL service. If you have the applicable
license, you can install and use MAPDL with Docker, enabling you
to run and solve even on officially unsupported platforms like Mac
OS.


AnsysS 17.0 to 2020 R1 - CORBA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Ansys 17.0 supports the legacy CORBA interface, enabled with the
``ansys.mapdl.corba`` module. This interface allows you to send only
text to and from the MAPDL service, relying on file IO for all other
operations. While not as performant as gRPC, this interface still
allows you to control a local instance of MAPDL. These versions of
MAPDL support specific versions of Windows and Linux. For more information
on the supported platforms, see `Ansys Platform Support
<https://www.ansys.com/solutions/solutions-by-role/it-professionals/platform-support>`_.

.. Note::

   The CORBA interface is likely to be phased out from MAPDL at some
   point. The gRPC interface is faster, more stable, and can run in
   both local and remote connection configurations.


Earlier than Ansys 17.0
~~~~~~~~~~~~~~~~~~~~~~~
The ``PyMAPDL`` project supports Ansys versions as early as 13.0 on Linux using a
console interface. Like CORBA, the console interface allows for the exchange of text to
and from the Ansys instance.

.. Warning::

   Because console-specific support is to be depreciated at some point, you should
   shift to a modern version of Ansys to continue to use PyMAPDL.
