### MAPDL Docker Image Build

These files are used to build the gRPC MAPDL docker image.  Effectively, it
simply places the MAPDL binaries and libraries into `/ansys_inc`.


The MAPDL install files are a subset of the normal MAPDL install.
Files were trimmed with `reduce_mapdl.py`.
