MAPDL as a gRPC Service
-----------------------

.. todo::

   - Launch MAPDL as a persistent remote service.
   - Run MAPDL on the cloud as a genuine service through a single isolated port.
   - Run MAPDL within a docker container.  See <pyansys docker html link>


Downloading Remote MAPDL Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Remote files can be listed and downloaded using ``pyansys``.  For example, to list the remote files and download one of them:

.. code:: python

    remote_files = mapdl.list_files()

    # ensure the result file is one of the remote files
    assert 'file.rst' in remote_files

    # download the remote result file
    mapdl.download('file.rst')


Uploading a Local MAPDL File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can upload a local file to the remote mapdl instance with:

.. code:: python

    # upload a local file
    mapdl.upload('sample.db')

    # ensure the uploaded file is one of the remote files
    remote_files = mapdl.list_files()
    assert 'sample.db' in remote_files
