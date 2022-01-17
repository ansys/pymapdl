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

# import numpy as np
# import pandas as pd

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

###############################################################################
# Distance between keypoints.


kp = Create(1, 2, 3, 10, 20, 30)
kp_dist, keypoint_list = kp.create_kp_method()
print(f"Distance between keypoint is: {kp_dist},\n"
      f"{keypoint_list}")


###############################################################################
# Distance between nodes.

nodes = Create(1, 200, 3, 10, 20, 300)
node_dist, node_list = nodes.create_node_method()
print(f"Distance between nodes is: {node_dist},\n"
      f"{node_list}")


# ###############################################################################
# # Check Results
# # ~~~~~~~~~~~~~
# # Finally we have the results of the loads for the simplified axisymmetric model,
# # which can be compared with expected target values for models with ``PIPE288``,
# # ``SOLID185``, and ``SHELL181`` elements. Loads expected for each load step are:
# #
# # - 1st Load Step with deflection :math:`\delta = 0.032 (in)` has :math:`load_1 = 1024400\,(lb)`.
# # - 2nd Load Step with deflection :math:`\delta = 0.05 (in)` has :math:`load_2 = 1262000\,(lb)`.
# # - 3rd Load Step with deflection :math:`\delta = 0.1 (in)` has :math:`load_3 = 1262000\,(lb)`.
#
# target_res = np.asarray([1024400, 1262000, 1262000,
#                          1024400, 1262000, 1262000,
#                          1024400, 1262000, 1262000])
#
# simulation_res = np.asarray([pipe288_ls1, pipe288_ls2, pipe288_ls2,
#                              solid185_ls1, solid185_ls2, solid185_ls3,
#                              shell181_ls1, shell181_ls2, shell181_ls3])
#
# main_columns = {
#     "Target": target_res,
#     "Mechanical APDL": simulation_res,
#     "Ratio": list(np.divide(simulation_res, target_res))
# }
#
# row_tuple = [("PIPE288", "Load, lb for Deflection = 0.032 in"),
#              ("PIPE288", "Load, lb for Deflection = 0.05 in"),
#              ("PIPE288", "Load, lb for Deflection = 0.1 in"),
#
#              ("SOLID185", "Load, lb for Deflection = 0.032 in"),
#              ("SOLID185", "Load, lb for Deflection = 0.05 in"),
#              ("SOLID185", "Load, lb for Deflection = 0.1 in"),
#
#              ("SHELL181", "Load, lb for Deflection = 0.032 in"),
#              ("SHELL181", "Load, lb for Deflection = 0.05 in"),
#              ("SHELL181", "Load, lb for Deflection = 0.1 in")]
#
# index_names = ["Element Type", "Load Step"]
# row_indexing = pd.MultiIndex.from_tuples(row_tuple)
# df = pd.DataFrame(main_columns, index=row_indexing)
#
# df.style.set_caption('Results Comparison',
#                      ).set_table_styles([
#                         {
#                             "selector": "th.col_heading",
#                             "props": [("background-color", "#FFEFD5"),
#                                       ("color", "black"),
#                                       ("border", "0.5px solid black"),
#                                       ("font-style", "italic"),
#                                       ("text-align", "center")]
#                         },
#                         {
#                             "selector": "th.row_heading",
#                             "props": [("background-color", "#FFEFD5"),
#                                       ("color", "black"),
#                                       ("border", "0.5px solid black"),
#                                       ("font-style", "italic"),
#                                       ("text-align", "center")]
#                         },
#                         {
#                             "selector": "td:hover",
#                             "props": [("background-color", "#FFF8DC")]
#                         },
#                         {
#                             "selector": "th",
#                             "props": [("max-width", '120px')]
#                         },
#                         {
#                             "selector": "",
#                             "props": [('border', '0.5px solid black')]
#                         },
#                         {
#                             'selector': 'caption',
#                             'props': [('color', 'black'),
#                                       ("font-style", "italic"),
#                                       ('font-size', '24px'),
#                                       ("text-align", "center")]
#                         }],
# ).set_properties(**{
#     "background-color": "#FFFAFA",
#     "color": "black",
#     "border-color": "black",
#     "border-width": "0.5px",
#     "border-style": "solid",
#     "text-align": "center"}).format("{:.3f}")
