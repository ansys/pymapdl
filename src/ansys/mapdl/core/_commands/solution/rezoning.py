# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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


class Rezoning:

    def aremesh(self, lcomb: int | str = "", angle: str = "", **kwargs):
        r"""Generates an area in which to create a new mesh for rezoning.

        Mechanical APDL Command: `AREMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AREMESH.html>`_

        Parameters
        ----------
        lcomb : int or str
            Specifies how to combine adjacent line segments:

            * ``0`` - Line segments combined by connecting ends to ends. This value is the default.

            * ``-1`` - No line segments combined.

        angle : str
            The maximum angle (in degrees) allowed for connecting two line segments together. The default
            value is 30. This value is valid only when ``LCOMB`` = 0.

        Notes
        -----
        Issue the :ref:`aremesh` command after issuing a :ref:`remesh`,START command and before issuing a
        :ref:`remesh`,FINISH command.

        The :ref:`aremesh` command cannot account for an open area (or "hole") inside a completely enclosed
        region. Instead, try meshing around an open area by selecting two adjoining regions; for more
        information, see.
        """
        command = f"AREMESH,{lcomb},{angle}"
        return self.run(command, **kwargs)

    def mapsolve(self, maxsbstep: str = "", **kwargs):
        r"""Maps solved node and element solutions from an original mesh to a new mesh.

        Mechanical APDL Command: `MAPSOLVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MAPSOLVE.html>`_

        Parameters
        ----------
        maxsbstep : str
            The maximum number of substeps for rebalancing the residuals. The default value is 5.

        Notes
        -----
        Used during the `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_ process, the
        :ref:`mapsolve` command maps solved node and element solutions from the original mesh to the new
        mesh and achieves equilibrium based on the new mesh.

        Additional substeps are necessary to reduce the residuals to zero.

        During the rebalancing stage, the external loads and time remain unchanged.

        The :ref:`mapsolve` command is valid only for rezoning ( :ref:`rezone` ). Distributed-Memory
        Parallel (DMP) Restriction This command is not supported in a DMP solution.
        """
        command = f"MAPSOLVE,{maxsbstep}"
        return self.run(command, **kwargs)

    def mapvar(
        self,
        option: str = "",
        matid: str = "",
        istrtstress: str = "",
        ntenstress: str = "",
        istrtstrain: str = "",
        ntenstrain: str = "",
        istrtvect: str = "",
        nvect: str = "",
        **kwargs,
    ):
        r"""Defines tensors and vectors in user-defined state variables for rezoning and in 2D to 3D analyses.

        Mechanical APDL Command: `MAPVAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MAPVAR.html>`_

        Parameters
        ----------
        option : str
            * ``DEFINE`` - Define variables for the specified ``MatId`` material ID (default).

            * ``LIST`` - List the defined variables for the specified ``MatId`` material ID.

        matid : str
            The material ID for the state variables which you are defining ( ``Option`` = DEFINE) or listing
            ( ``Option`` = LIST).

            When ``Option`` = LIST, the default value for this argument is ALL (which lists all defined
            variables). When ``Option`` = DEFINE, you must explicitly specify a material ID.

        istrtstress : str
            The start position of stress-like tensors in the state variables. This value must be either a
            positive integer or 0 (meaning no stress-like tensors).

        ntenstress : str
            The number of stress-like tensors in the state variables. This value must be either a positive
            integer (or 0), and all stress-like tensors must be contiguous.

        istrtstrain : str
            The start position of strain-like tensors in the state variables. This value must be either a
            positive integer or 0 (meaning no strain-like tensors).

        ntenstrain : str
            The number of strain-like tensors in the state variables. This value must be either a positive
            integer (or 0), and all strain-like tensors must be contiguous.

        istrtvect : str
            The start position of vectors in the state variables. This value must be either a positive
            integer or 0 (meaning no vectors).

        nvect : str
            The number of vectors in the state variables. This value must be either a positive integer (or
            0), and all vectors must be contiguous.

        Notes
        -----

        .. _MAPVAR_notes:

        The :ref:`mapvar` command identifies the tensors and vectors in user-defined state variables (
        :ref:`tb`,STATE) for user-defined materials ( :ref:`tb`,USER and `UserMat
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ or `UserMatTh
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ ) or user-
        defined creep laws ( :ref:`tb`,CREEP,,,,100 and UserCreep ).

        To handle large-rotation effects and to correctly differentiate between tensor- and vector-mapping,
        specify the start position of specific state variables. For stress-like tensors, the shear
        components saved as state variables are the tensor component. For strain-like tensors, the shear
        components saved as state variables are twice the tensor components. Therefore, issue the
        :ref:`mapvar` command to define the stress-like and strain-like tensors individually. The command
        ensures that user-defined state variables are mapped correctly during `rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_ and in `2D
        to 3D analyses
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_ADV2DTO3DREST.html>`_.

        In a rezoning operation, :ref:`mapvar` must be issued after remeshing ( :ref:`remesh`,FINISH) but
        before mapping ( :ref:`mapsolve` ).
        """
        command = f"MAPVAR,{option},{matid},{istrtstress},{ntenstress},{istrtstrain},{ntenstrain},,{istrtvect},{nvect}"
        return self.run(command, **kwargs)

    def remesh(
        self,
        action: str = "",
        filename: str = "",
        ext: str = "",
        opt1: str = "",
        opt2: str = "",
        **kwargs,
    ):
        r"""Specifies the starting and ending remeshing points, and other options, for rezoning.

        Mechanical APDL Command: `REMESH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_REMESH.html>`_

        Parameters
        ----------
        action : str
            * ``START`` - Starts the remeshing operation.

            * ``FINISH`` - Ends the remeshing operation.

            * ``READ`` - Reads in a generic ( :file:`.cdb` format) new mesh file generated by a third-party
              application. This remeshing option applies to both 2D and 3D rezoning.

            * ``SPLIT`` - Splits selected elements of an existing 2D or 3D mesh such that a quadrilateral
              element is split into four quadrilaterals, a degenerate quadrilateral is split into three
              quadrilaterals, and a quadratic triangular element is split into four quadratic triangles. A
              tetrahedral element is split into eight tetrahedra.

        filename : str
            Name of a :file:`.cdb` generic mesh file. The default value is :file:`jobname`. Valid only when
            ``Action`` = READ.

        ext : str
            File name extension. The only valid (and the default) extension is CDB. Valid only when
            ``Action`` = READ.

        opt1 : str
            Specifies options for the new mesh when using a generic imported mesh file or the mesh-splitting
            remeshing method. Valid only when ``Action`` = READ or ``Action`` = SPLIT.

            * ``REGE`` - Regenerates all node and element numbers on the new mesh using an offset of the highest
              existing node and element numbers. This is the default behavior when ``Action`` = READ; otherwise,
              this value is ignored.

            * ``KEEP`` - Keeps the similarly numbered nodes and elements in the new and the old meshes
              unchanged. Valid only when ``Action`` = READ.

            * ``TRAN`` - Generates transition elements to ensure nodal compatibility between split and unsplit
              parts of the mesh. Valid only when ``Action`` = SPLIT for 2D analyses.

        opt2 : str
            Specifies transition options for the mesh when elements are split. These options are valid only when
            ``Action`` = SPLIT for 2D analyses.

            * ``QUAD`` - Minimizes the number of degenerate elements in the transition mesh and tries to
              maximize the number of quadrilateral transition elements across several layers of elements from the
              split regions. This is the default behavior.

            * ``DEGE`` - Creates transition zones between the split and unsplit parts of the mesh using mostly
              degenerate elements with a single element layer.

        Notes
        -----
        This command is valid only during the rezoning ( :ref:`rezone` ) process.

        In rezoning, :ref:`remesh`,START exits the solution processor temporarily and enters a special mode
        of the PREP7 preprocessor, after which a limited number of preprocessing commands are available for
        `mesh control
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZREM.html#advrezcmdtbl>`_,
        but no solution commands are valid.

        :ref:`remesh`,FINISH exits the remeshing process and reenters the solution processor, at which
        point no preprocessing commands are available. If the new mesh exists, the command creates contact
        elements if needed, and transfers all boundary conditions (BCs) and loads from the original mesh to
        the new mesh. You can issue any list or plot command to verify the created contact elements,
        transferred BCs, and loads. :ref:`remesh`,FINISH is valid only after a previously issued
        :ref:`remesh`,START, and is the only way to safely end the remeshing operation (and exit the special
        mode of PREP7).

        :ref:`remesh`,READ is valid only when you want to perform a rezoning operation using a generic new
        mesh generated by a third-party application (rather than a new mesh generated internally by
        Mechanical APDL). The command is valid between :ref:`remesh`,START and :ref:`remesh`,FINISH. In this
        case,
        the only valid file extension is :file:`.cdb` ( ``Ext`` = CDB). When ``Option`` = KEEP, Mechanical
        APDL
        assumes that the common node and element numbers between the old and the new mesh are topologically
        similar (that is, these commonly numbered areas have the same element connectivity and nodal
        coordinates).

        :ref:`remesh`,SPLIT is valid only when performing a rezoning operation via splitting the existing
        mesh. The command is valid between :ref:`remesh`,START and :ref:`remesh`,FINISH.

        You can use :ref:`remesh`,READ and :ref:`remesh`,SPLIT for horizontal multiple rezoning provided
        that the meshes used in :ref:`remesh`,READ do not intersect. (Avoid issuing :ref:`aremesh` after
        issuing either of these commands.)

        For more information about the remeshing options available during rezoning, see `Rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_
        Distributed-Memory Parallel (DMP) Restriction This command is not supported in a DMP solution.
        """
        command = f"REMESH,{action},{filename},{ext},,{opt1},{opt2}"
        return self.run(command, **kwargs)

    def rezone(self, option: str = "", ldstep: str = "", sbstep: str = "", **kwargs):
        r"""Initiates the rezoning process, sets rezoning options, and rebuilds the database.

        Mechanical APDL Command: `REZONE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_REZONE.html>`_

        Parameters
        ----------
        option : str
            The `rezoning
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_ method to
            employ:

            * ``MANUAL`` - Manual rezoning. You decide when to use rezoning, what region(s) to rezone, and what
              remeshing method to use on the selected region(s). This method is currently the default and
              only option.

        ldstep : str
            The load step number at which rezoning should occur. The default value is the highest load step
            number found in the :file:`Jobname.Rnnn` files (for the current jobname and in the current
            directory).

        sbstep : str
            The substep number of the specified load step ( ``LDSTEP`` ) at which rezoning should occur. The
            default value is the highest substep number found in the specified load step in the
            :file:`Jobname.Rnnn` files (for the current jobname and in the current directory).

        Notes
        -----

        .. _REZONE_notes:

        The :ref:`rezone` command rebuilds the database ( :file:`.db` file) based on the specified load step
        and substep information, and updates nodes to their deformed position for remeshing.

        Before issuing this command, clear the database via the :ref:`clear` command.

        For more information, see `Rezoning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVRZSMP.html>`_
        Distributed-Memory Parallel (DMP) Restriction This command is not supported in a DMP solution.
        """
        command = f"REZONE,{option},{ldstep},{sbstep}"
        return self.run(command, **kwargs)
