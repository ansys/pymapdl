from ansys.mapdl.core import launch_mapdl

# Start mapdl.
mapdl = launch_mapdl()


###############################################################################
# Initiate Pre-Processing
# ~~~~~~~~~~~~~~~~~~~~~~~
# Enter verification example mode and the pre-processing routine.

def start_prep7():
    mapdl.clear()
    mapdl.verify()
    mapdl.prep7()


start_prep7()

mapdl.k(1,0,0,0)
mapdl.k(2,0,0,0)
mapdl.k(3,0,0,0)

print(mapdl.klsit())
