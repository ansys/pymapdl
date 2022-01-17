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
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

    def create_kp_method(self):
        kp1 = mapdl.k(x=self.x1, y=self.y1, z=self.z1)
        kp2 = mapdl.k(x=self.x2, y=self.y2, z=self.z2)
        dist_kp, kx, ky, kz = mapdl.kdist(kp1, kp2)
        mapdl.kplot(show_keypoint_numbering=True,
                    background="grey",
                    show_bounds=True,
                    font_size=26)
        return dist_kp, mapdl.klist()

    def create_node_method(self):
        node1 = mapdl.n(x=self.x1, y=self.y1, z=self.z1)
        node2 = mapdl.n(x=self.x2, y=self.y2, z=self.z2)
        dist_node, node_x, node_y, node_z = mapdl.ndist(node1, node2)
        mapdl.nplot(background="green",
                    show_bounds=True,
                    font_size=26)
        return dist_node, mapdl.nlist()


kp = Create(1, 2, 3, 10, 20, 30)
kp_dist, keypoint_list = kp.create_kp_method()
print(f"Distance between keypoint is: {kp_dist},\n\n\n"
      f"{keypoint_list}")

nodes = Create(1, 200, 3, 10, 20, 300)
node_dist, node_list = nodes.create_node_method()
print(f"Distance between nodes is: {node_dist},\n\n\n"
      f"{node_list}")
