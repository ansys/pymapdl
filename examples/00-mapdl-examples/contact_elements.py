"""
Basic example creating contact elements.

"""
from ansys.mapdl import core as pymapdl


mapdl = pymapdl.Mapdl()
mapdl.clear()

mapdl.prep7()
mapdl.esize(0.1)

mapdl.et(1, 187)
vnum0 = mapdl.block(0, 1, 0, 1, 0, 0.5)
mapdl.vmesh(vnum0)

# second block slightly higher
mapdl.esize(0.09)
mapdl.et(2, 186)
mapdl.type(2)
vnum1 = mapdl.block(0, 1, 0, 1, 0.50001, 1)
mapdl.vmesh(vnum1)

mapdl.nsel('s', 'loc', 'z', 0.5, 0.50001)
mapdl.esln('s')
mapdl.gcgen('NEW', splitkey='SPLIT', selopt='SELECT')
mapdl.allsel()
mapdl.cdwrite('db', 'contact_cube.cdb')
