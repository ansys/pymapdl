# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class Analysis2DTo3D:

    def map2dto3d(self, action: str = "", value1: str = "", value2: str = "", **kwargs):
        r"""Initiates a 2D to 3D analysis and maps variables.

        Mechanical APDL Command: `MAP2DTO3D <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MAP2DTO3D.html>`_

        Parameters
        ----------
        action : str
            The 2D to 3D analysis action to perform:

            * ``START`` - Start the analysis process by rebuilding the 2D analysis database ( :file:`.db` ) based on the
              specified load step and substep information, and update nodes to their deformed positions in the 2D
              mesh.

              * ``VALUE1`` - The load step number at which 2D to 3D analysis should occur. The default value is
                the highest load step number found in the :file:`Jobname.Rnnn` files (for the current jobname and in
                the current directory).

              * ``VALUE2`` - The substep number of the specified load step ( ``VALUE1`` ) at which the 2D to 3D
                analysis should occur. The default value is the highest substep number found in the specified load
                step in the :file:`Jobname.Rnnn` files (for the current jobname and in the current directory).

            * ``FINISH`` - Maps boundary conditions and loads from the 2D mesh to the extruded 3D mesh. ( VALUE1
              and VALUE2 are not used.)

            * ``SOLVE`` - Map nodal and element solutions from 2D to 3D and rebalance the results.

              * ``VALUE1`` - The maximum number of substeps allowed during rebalancing. Default = 500.

        value1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MAP2DTO3D.html>`_ for
            further information.

        value2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MAP2DTO3D.html>`_ for
            further information.

        Notes
        -----
        The :ref:`map2dto3d` command initiates the 2D to 3D analysis process, sets analysis options,
        rebuilds the database, and maps the solution variables from the 2D mesh to the 3D mesh.

        Before issuing this command, clear the database ( :ref:`clear` ).

        For more information, see `2D to 3D Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_ADV2DTO3DREST.html>`_
        """
        command = f"MAP2DTO3D,{action},{value1},{value2}"
        return self.run(command, **kwargs)
