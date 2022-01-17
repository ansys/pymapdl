###############################################################################
# Import and start MAPDL. Import math library.
# import math
import math

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()
mapdl.finish()
mapdl.run("/CLEAR,all")
mapdl.prep7()


###############################################################################


class Create:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        # Attributes
        print("Define Distance")
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

    def create_kp_method(self):
        kp1 = mapdl.k(x=self.x1, y=self.y1, z=self.z1)
        kp2 = mapdl.k(x=self.x2, y=self.y2, z=self.z2)
        dist_kp = mapdl.kdist(kp1, kp2)
        mapdl.kplot(show_keypoint_numbering=True,
                    background="black",
                    show_bounds=True,
                    font_size=26)
        return dist_kp


kp = Create(1, 2, 3, 10, 20, 30)
kp_dist = kp.create_kp_method()
print(kp_dist)



