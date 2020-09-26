import pytest
import numpy as np

import pyansys

@pytest.fixture(scope='module')
def transient_thermal(mapdl):
    mapdl.clear()
    mapdl.prep7()

    # Material properties-- 1020 steel in imperial
    mapdl.units('BIN')  # U.S. Customary system using inches (in, lbf*s2/in, s, °F).
    mapdl.mp('EX', 1, 30023280.0)
    mapdl.mp('NUXY', 1, 0.290000000)
    mapdl.mp('ALPX', 1, 8.388888889E-06)
    mapdl.mp('DENS', 1, 7.346344000E-04)
    mapdl.mp('KXX', 1, 6.252196000E-04)
    mapdl.mp('C', 1, 38.6334760)

    # use a thermal element type
    mapdl.et(1, 'SOLID70')

    # Geometry and Mesh
    mapdl.block(0, 5, 0, 1, 0, 1)
    mapdl.lesize('ALL', 1, layer1=1)
    mapdl.mshape(0, '3D')
    mapdl.mshkey(1)
    mapdl.vmesh(1)
    mapdl.run('/SOLU')
    mapdl.antype(4)            # transient analysis
    mapdl.trnopt('FULL')       # full transient analysis
    mapdl.kbc(0)               # ramp loads up and down

    # Time stepping
    end_time = 500
    mapdl.time(end_time)       # end time for load step
    mapdl.autots('ON')         # use automatic time stepping
    mapdl.deltim(10, 5, 100)    # substep size (seconds)

    # Create a table of convection times and coefficients and trasfer it to MAPDL
    my_conv = np.array([[0, 0.001],      # start time
                        [120, 0.001],    # end of first "flat" zone
                        [130, 0.005],    # ramps up in 10 seconds
                        [300, 0.005],    # end of second "flat zone
                        [400, 0.002],    # ramps down in 10 seconds
                        [end_time, 0.002]])  # end of third "flat" zone
    mapdl.load_table('my_conv', my_conv, 'TIME')


    # Create a table of bulk temperatures for a given time and transfer to MAPDL
    my_bulk = np.array([[0, 100],      # start time
                        [120, 100],    # end of first "flat" zone
                        [200, 300],    # ramps up in 380 seconds
                        [300, 300],    # hold temperature for 200 seconds
                        [400, 75],     # temperature ramps down for 200 seconds
                        [end_time, 75]])   # end of second "flat" zone
    mapdl.load_table('my_bulk', my_bulk, 'TIME')

    # Force transient solve to include the times within the conv and bulk arrays
    # my_tres = np.unique(np.vstack((my_bulk[:, 0], my_conv[:, 0])))[0]  # same as
    mapdl.parameters['my_tsres'] = [120, 130, 300, 400, end_time]
    mapdl.tsres('%my_tsres%')

    mapdl.outres('ERASE')
    mapdl.outres('ALL', 'ALL')

    mapdl.eqslv('SPARSE')  # use sparse solver
    mapdl.tunif(75)        # force uniform starting temperature (otherwise zero)

    # apply the convective load (convection coefficient plus bulk temperature)
    # use "%" around table array names
    mapdl.sfa(6, 1, 'CONV', '%my_conv%', ' %my_bulk%')

    # solve
    mapdl.solve()
    mapdl.post1()
    mapdl.set(1, 1)


def test_nodal_time_history(mapdl, transient_thermal):
    rst = mapdl.result
    nnum, data = rst.nodal_time_history()

    assert np.allclose(nnum, mapdl.mesh.nnum)
    for i in range(mapdl.post_processing.nsets):
        mapdl.set(1, i + 1)
        assert np.allclose(data[i].ravel(), mapdl.post_processing.nodal_temperature)
