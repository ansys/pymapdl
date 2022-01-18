r"""
.. _ref_vm8_example:

Parametric Calculation
----------------------
Problem Description:
 - Write a user file macro to calculate the distance d between either nodes
   or keypoints in ``PREP7``. Define abbreviations for calling the macro and
   verify the parametric expressions by using the macro to calculate
   the distance between nodes :math:`N_1` and :math:`N_2` and
   between keypoints :math:`K_3` and :math:`K_4`.

Reference:
 - None.

Analysis Type(s):
 - Parametric Arithmetic

Element Type:
 - None.

Geometric Properties(Coordinates):
 - :math:`N_{\mathrm{1(x,y,z)}} = 1.5, 2.5, 3.5`
 - :math:`N_{\mathrm{2(x,y,z)}} = -3.7, 4.6, -3`
 - :math:`K_{\mathrm{3(x,y,z)}} = 100, 0, 30`
 - :math:`K_{\mathrm{4(x,y,z)}} = -200,25,80`

.. image:: ../../_static/vm8_setup.png
   :width: 300
   :alt: VM8 Problem Sketch

Analysis Assumptions and Modeling Notes:
 - The user file is created by the *CREATE command within the run.
   In normal use, this file would most likely already exist locally.
   Colons are used in the user file to create non-echoing comments (the colon
   character specifies a branching label in Mechanical APDL).
   The active coordinate system is saved and restored within the macro to ensure
   Cartesian coordinates in the distance calculations and to re-establish
   the active coordinate system after the macro is used. Lowercase input
   is used throughout. Input case is preserved by Mechanical APDL where
   appropriate (system-dependent).


"""
# sphinx_gallery_thumbnail_path = '_static/vm8_setup.png'

###############################################################################
# Start MAPDL
# ~~~~~~~~~~~

import numpy as np
import pandas as pd

from ansys.mapdl.core import launch_mapdl

# Start MAPDL.
mapdl = launch_mapdl()


###############################################################################
# Pre-Processing
# ~~~~~~~~~~~~~~
# Enter verification example mode and the pre-processing routine.

mapdl.clear()
mapdl.verify()
_ = mapdl.prep7()


###############################################################################
# Pre-Processing
# ~~~~~~~~~~~~~~

class Create:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        # Coordinate Attributes.
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

    def create_kp_method(self):

        # Define keypoints by coordinates.
        kp1 = mapdl.k(npt=3, x=self.x1, y=self.y1, z=self.z1)
        kp2 = mapdl.k(npt=4, x=self.x2, y=self.y2, z=self.z2)

        # Get the distance between keypoints.
        dist_kp, kx, ky, kz = mapdl.kdist(kp1, kp2)

        # Plot keypoints.
        mapdl.kplot(show_keypoint_numbering=True,
                    background="grey",
                    show_bounds=True,
                    font_size=26)
        return dist_kp, mapdl.klist()

    def create_node_method(self):

        # Define nodes by coordinates.
        node1 = mapdl.n(node=1, x=self.x1, y=self.y1, z=self.z1)
        node2 = mapdl.n(node=2, x=self.x2, y=self.y2, z=self.z2)

        # Get the distance between nodes.
        dist_node, node_x, node_y, node_z = mapdl.ndist(node1, node2)

        # Plot nodes.
        mapdl.nplot(background="grey",
                    show_bounds=True,
                    font_size=26)
        return dist_node, mapdl.nlist()

###############################################################################
# Distance between keypoints
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#

kp = Create(1.5, 2.5, 3.5, -3.7, 4.6, -3)
kp_dist, keypoint_list = kp.create_kp_method()
print(f"Distance between keypoint is: {kp_dist:.2f}\n\n"
      f"{keypoint_list}")


###############################################################################
# Distance between nodes.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#

nodes = Create(100, 0, 30, -200, 25, 80)
node_dist, node_list = nodes.create_node_method()
print(f"Distance between nodes is: {node_dist:.2f}\n\n"
      f"{node_list}")


###############################################################################
# Check Results
# ~~~~~~~~~~~~~
# Finally we have the results of the distances for both simulations,
# which can be compared with expected target values:
#
# - 1st simulation to get the distance between keypoints :math:`K_3` and :math:`K_4`, where :math:`LEN_1 = 8.58\,(in)`.
# - 2nd simulation to get the distance between nodes :math:`N_1` and :math:`N_2`, where :math:`LEN_2 = 305.16\,(in)`.

# Define the names of the rows.
row_names = ["N1 - N2 distance (LEN2)",
             "K3 - K4 distance (LEN1)"]

# Define the names of the columns.
col_names = ['Target',
             'Mechanical APDL',
             'RATIO']

# Define the values of the target results.
target_res = np.asarray([8.5849, 305.16])

# Create an array with outputs of the simulations.
simulation_res = np.asarray([kp_dist, node_dist])

# Identifying and filling corresponding columns.
main_columns = {
    "Target": target_res,
    "Mechanical APDL": simulation_res,
    "Ratio": list(np.divide(simulation_res, target_res))
}

# Create and fill the output dataframe with pandas.
df2 = pd.DataFrame(main_columns, index=row_names)

# Apply style settings for the dataframe.
df2.style.set_table_styles([
                            {
                              "selector": "th",
                              "props": [('font-size', '16px')]
                            },
                            {
                              "selector": "td",
                              "props": [('font-size', '16px')]
                            },
                            {
                                "selector": "td:hover",
                                "props": [("background-color", "#FFF8DC")]
                            }],
).set_properties(**
                 {
                    "color": "black",
                    "text-align": "center"
                 },
).format("{:.2f}")
