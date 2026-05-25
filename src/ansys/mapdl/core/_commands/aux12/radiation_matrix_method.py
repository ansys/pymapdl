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

from ansys.mapdl.core._commands import CommandsBase


class RadiationMatrixMethod(CommandsBase):

    def emis(self, mat: str = "", evalu: str = "", **kwargs):
        r"""Specifies emissivity as a material property for the Radiation Matrix method.

        Mechanical APDL Command: `EMIS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMIS.html>`_

        **Command default:**

        .. _EMIS_default:

        Since there is no :ref:`command default value for emissivity, you must issue <ans_cmd_cmdDef>`
        :ref:`emis` to specify it. Otherwise, an error message appears. If you issue :ref:`emis` without
        defining a numerical value, emissivity defaults to 0.

        Parameters
        ----------
        mat : str
            Material number associated with this emissivity (500 maximum). Defaults to 1.

        evalu : str
            Emissivity for this material (0.0 < ``EVALU``  :math:`equation not available`  1.0).  Enter a
            very small number for zero.

        Notes
        -----

        .. _EMIS_notes:

        Specifies emissivity as a material property for the Radiation Matrix method. This material property
        can then be associated with each element.
        """
        command = f"EMIS,{mat},{evalu}"
        return self.run(command, **kwargs)

    def geom(self, k2d: int | str = "", ndiv: str = "", **kwargs):
        r"""Defines the geometry specifications for the radiation matrix calculation.

        Mechanical APDL Command: `GEOM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GEOM.html>`_

        Parameters
        ----------
        k2d : int or str
            Dimensionality key:

            * ``0`` - 3D geometry (default)

            * ``1`` - 2D geometry (plane or axisymmetric)

        ndiv : str
            Number of divisions in an axisymmetric model. Used only with ``K2D`` = 1. Defaults to 0 (2D
            plane). The 2D model is internally expanded to a 3D model based on the number of divisions
            specified (6 :math:`equation not available`   ``NDIV``  :math:`equation not available`  90).
            For example, ``NDIV`` of 6 is internally represented by six 60° sections.
        """
        command = f"GEOM,{k2d},{ndiv}"
        return self.run(command, **kwargs)

    def mprint(self, key: int | str = "", **kwargs):
        r"""Specifies that radiation matrices are to be printed.

        Mechanical APDL Command: `MPRINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MPRINT.html>`_

        Parameters
        ----------
        key : int or str
            Print key:

            * ``0`` - Do not print matrices.

            * ``1`` - Print matrices.

        Notes
        -----

        .. _MPRINT_notes:

        Specifies that the element and node radiation matrices are to be printed when the :ref:`write`
        command is issued. If ``KEY`` = 1, form factor information for each element will also be printed.
        """
        command = f"MPRINT,{key}"
        return self.run(command, **kwargs)

    def space(self, node: str = "", **kwargs):
        r"""Defines a space node for radiation using the Radiation Matrix method.

        Mechanical APDL Command: `SPACE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPACE.html>`_

        Parameters
        ----------
        node : str
            Node defined to be the space node.

        Notes
        -----

        .. _SPACE_notes:

        A space node is required in an open system to account for radiation losses.
        """
        command = f"SPACE,{node}"
        return self.run(command, **kwargs)

    def vtype(self, nohid: int | str = "", nzone: str = "", **kwargs):
        r"""Specifies the viewing procedure used to determine the form factors for the Radiation Matrix method.

        Mechanical APDL Command: `VTYPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VTYPE.html>`_

        Parameters
        ----------
        nohid : int or str
            Type of viewing procedure:

            * ``0`` - Hidden procedure.

            * ``1`` - Non-hidden (faster, but less general) procedure.

        nzone : str
            Number of sampling zones for the hidden procedure (100 maximum for 3D, 1000 maximum for 2D).
            Defaults to 20 for 3D, 200 for 2D. Number of points is 2* ``NZONE`` for 2D and 2\* ``NZONE`` \*( ``NZONE`` +1) for 3D.
        """
        command = f"VTYPE,{nohid},{nzone}"
        return self.run(command, **kwargs)

    def write(self, fname: str = "", **kwargs):
        r"""Writes the radiation matrix file.

        Mechanical APDL Command: `WRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_WRITE.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name Defaults to :file:`Jobname`.

        Notes
        -----

        .. _WRITE_notes:

        Writes radiation matrix file ( :file:`File.SUB` ) for input to the substructure thermal "use" pass.
        Subsequent :ref:`write` operations to the same file overwrite the file.
        """
        command = f"WRITE,{fname}"
        return self.run(command, **kwargs)
