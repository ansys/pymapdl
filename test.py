
from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.selector import Interval

mapdl = launch_mapdl()

try:
    mapdl.prep7()
    mapdl.et(1, "SOLID185")
    mapdl.block(0, 10, 0, 10, 0, 10)
    mapdl.esize(2)
    mapdl.vmesh("ALL")

    selected_nodes = mapdl.selector.select(
        x=0,
        y=[0, 10],
        z=Interval(0, 10),
    )

    print(selected_nodes)
finally:
    mapdl.exit()