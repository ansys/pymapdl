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
        kp_x, kp_y, kp_z = mapdl.kdist(kp1, kp2)
        dist_kp = math.sqrt(kp_x ** 2 + kp_y ** 2 + kp_z ** 2)
        mapdl.kplot(show_keypoint_numbering=True,
                    background="black",
                    show_bounds=True,
                    font_size=26)
        return dist_kp

    def create_node_method(self):
        node1 = mapdl.n(x=self.x1, y=self.y1, z=self.z1)
        node2 = mapdl.n(x=self.x2, y=self.y2, z=self.z2)
        dist_xyz_n = mapdl.ndist(node1, node2)
        return dist_xyz_n
        # dist_n = math.sqrt(dist_xyz_n[0] ** 2 + dist_xyz_n[1] ** 2 + dist_xyz_n[2] ** 2)
        # print(dist_n)


kp = Create(1, 2, 3, 10, 20, 30)
kp_dist = kp.create_kp_method()
print(f"Distance between keypoints is: {kp_dist}")
print(f"========================================")
node = Create(1, 2, 3, 10, 20, 30)
print(node.create_node_method())
node_dist = node.create_node_method()
print(node_dist)
# print(f"Distance between nodes is: {node_dist}")








###############################################################################
# CHANGES FOR NDIST

string_out ="""
Distance between node is: 33.67491648096547
========================================
Define Distance
The distance between nodes       1 and       2 in coordinate system     0 is:
 DIST              DX (ND2-ND1)      DY (ND2-ND1)      DZ (ND2-ND1)
  33.67491648       9.000000000       18.00000000       27.00000000
"""
#################################
print(string_out.split())
#################################


#################################
ndsit_x = string_out.split()[-1]
ndsit_y = string_out.split()[-2]
ndsit_z = string_out.split()[-3]
ndsit_DIST = string_out.split()[-4]
print(f"DX: {ndsit_x}\n"
      f"DY: {ndsit_y}\n"
      f"DZ: {ndsit_z}\n"
      f"DIST: {ndsit_DIST}")
#################################
print("\n\n\n")

#################################
dist_str = string_out.split()[-4]
dist = float(string_out.split()[-4])
print(f"type of the splited string: {type(dist_str)},\n"
      f"where the full automatically calculated distance between is: {dist_str},\n"
      f"convertation str to flot: {type(dist)},\n"
      f"where the distance is: {dist}")

#################################



