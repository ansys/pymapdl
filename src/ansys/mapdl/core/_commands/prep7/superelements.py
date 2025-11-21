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

class Superelements:

    def se(self, file: str = "", toler: str = "", nstartvn: str = "", **kwargs):
        r"""Defines a superelement.

        Mechanical APDL Command: `SE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SE.html>`_

        Parameters
        ----------
        file : str
            The name (case sensitive) of the file containing the original superelement matrix created by the
            generation pass ( :file:`Sename.SUB` ). The default is the current Jobname.

        toler : str
            Tolerance used to determine if use pass nodes are noncoincident with master nodes having the
            same node numbers. Defaults to 0.0001. Use pass nodes will always be replaced by master nodes of
            the same node number. However, if a use pass node is more than ``TOLER`` away from the
            corresponding master node, a warning is generated.

        nstartvn : str
            Node number to be assigned to the first virtual node created to store the generalized
            coordinates in a component mode synthesis analysis. See :ref:`SE_notes` for more information.

        Notes
        -----

        .. _SE_notes:

        Defines a superelement by reading in the superelement matrices and master nodes from the
        superelement matrix file. The matrix file ( :file:`File.SUB` ) must be available from the
        substructure generation pass. The proper element type ( ``MATRIX50`` ) must be active ( :ref:`type`
        ) for this command. A scratch file called :file:`File.SORD` showing the superelement names and their
        corresponding element numbers is also written.

        ``nStartVN`` should be chosen so as to offset the virtual node numbers from the other node numbers
        used in the model. Otherwise, ``nStartVN`` is internally set by the program to fulfill that
        condition. The node number defined through ``nStartVN`` is considered only if applied on the first
        issued :ref:`se` command. ``nStartVN`` can also be defined during the generation pass using the
        :ref:`cmsopt` command. If ``nStartVN`` is defined on both :ref:`cmsopt` and :ref:`se` commands, the
        larger number prevails.
        """
        command = f"SE,{file},,,{toler},{nstartvn}"
        return self.run(command, **kwargs)



    def sedlist(self, sename: str = "", kopt: int | str = "", **kwargs):
        r"""Lists the DOF solution of a superelement after the use pass.

        Mechanical APDL Command: `SEDLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SEDLIST.html>`_

        Parameters
        ----------
        sename : str
            Name of the superelement in :file:`Jobname.DSUB` to be listed. If a number, it is the element
            number of the superelement as used in the use pass. If ALL, list results for all superelements.

        kopt : int or str
            List key:

            * ``0`` - List summary data only.

            * ``1`` - List full contents. Be aware that the listing may be extensive.

        Notes
        -----

        .. _SEDLIST_notes:

        Lists the degree of freedom solution of a superelement after the substructure use pass. Results may
        be listed for any superelement on :file:`FileDSUB`.

        This command is valid in any processor.
        """
        command = f"SEDLIST,{sename},{kopt}"
        return self.run(command, **kwargs)



    def selist(self, sename: str = "", kopt: int | str = "", kint: str = "", **kwargs):
        r"""Lists the contents of a superelement matrix file.

        Mechanical APDL Command: `SELIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SELIST.html>`_

        Parameters
        ----------
        sename : str
            The name (case-sensitive) of the superelement matrix file created by the substructure generation
            pass ( :file:`Sename.SUB` ). Defaults to the current :file:`Jobname`. If a number, it is the
            element number of the superelement as used in the use pass.

        kopt : int or str
            List key:

            * ``0`` - List summary data only.

            * ``1`` - List contents, except load vectors and matrices.

            * ``2`` - List contents, except matrices.

            * ``3`` - List full contents. Be aware that the listing may be extensive.

        kint : str
            Integer printout format key:

            * ``OFF`` - Default.

            * ``ON`` - Long format for large integers.

        Notes
        -----

        .. _SELIST_notes:

        This command is valid in any processor.
        """
        command = f"SELIST,{sename},{kopt},{kint}"
        return self.run(command, **kwargs)



    def sesymm(self, sename: str = "", ncomp: str = "", inc: str = "", file: str = "", ext: str = "", **kwargs):
        r"""Performs a symmetry operation on a superelement within the use pass.

        Mechanical APDL Command: `SESYMM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SESYMM.html>`_

        Parameters
        ----------
        sename : str
            The name (case-sensitive) of the superelement matrix file created by the substructure generation
            pass ( :file:`Sename.SUB` ). Defaults to the current :file:`Jobname`. If a number, it is the
            element number of a previously defined superelement in the current use pass.

        ncomp : str
            Symmetry key:

            * ``X`` - X symmetry (default).

            * ``Y`` - Y symmetry.

            * ``Z`` - Z symmetry.

        inc : str
            Increment all nodes in the superelement by ``INC``.

        file : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. This field must be input.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to SUB.

        Notes
        -----

        .. _SESYMM_notes:

        Performs a symmetry operation on a superelement within the substructure use pass by reversing the
        sign of component ``Ncomp`` in the global Cartesian coordinate system. The node numbers are
        incremented by ``INC``. The new superelement is written to :file:`File.SUB` in the current directory
        (by default). All master node nodal coordinate systems must be global Cartesian (no rotated nodes
        allowed).

        The maximum number of transformations for a given superelement is five (including :ref:`setran`,
        :ref:`sesymm`, and the large rotation transformation if :ref:`nlgeom` is ON in the use pass).

        This command is not supported if the original superelement matrix was created in a component mode
        synthesis analysis generation pass with the element results calculation activated ( ``Elcalc`` = YES
        on :ref:`cmsopt` ).
        """
        command = f"SESYMM,{sename},{ncomp},{inc},{file},{ext}"
        return self.run(command, **kwargs)



    def setran(self, sename: str = "", kcnto: str = "", inc: str = "", file: str = "", ext: str = "", dx: str = "", dy: str = "", dz: str = "", norot: int | str = "", **kwargs):
        r"""Creates a superelement from an existing superelement.

        Mechanical APDL Command: `SETRAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SETRAN.html>`_

        Parameters
        ----------
        sename : str
            The name (case-sensitive) of the file containing the original superelement matrix created by the
            generation pass ( :file:`Sename.SUB` ). The default is the current :file:`Jobname`. If
            ``Sename`` is a number, it is the element number of a previously defined superelement in the
            current use pass.

        kcnto : str
            The reference number of the coordinate system to where the superelement is to be transferred.
            The default is the global Cartesian system. Transfer occurs from the active coordinate system.

        inc : str
            The node offset. The default is zero. All new element node numbers are offset from those on the
            original by ``INC``.

        file : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. This field requires input.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to SUB.

        dx : str
            Node location increments in the global Cartesian coordinate system. Defaults to zero.

        dy : str
            Node location increments in the global Cartesian coordinate system. Defaults to zero.

        dz : str
            Node location increments in the global Cartesian coordinate system. Defaults to zero.

        norot : int or str
            Node rotation :ref:`key: <NOROTnotes>`

            * ``0`` - The nodal coordinate systems of the transferred superelement rotate into the ``KCNTO``
              system. (That is, the nodal coordinate systems rotate with the superelement.) The superelement
              matrices remain unchanged. This value is the default.

            * ``1`` - The nodal coordinate systems do not rotate. (That is, they remain fixed in their original
              global orientation.) The superelement matrices and load vectors are modified if any rotations occur.

        Notes
        -----

        .. _SETRAN_notes:

        The :ref:`setran` command creates a superelement from an existing superelement and writes the new
        element to a file. You can then issue an :ref:`se` command to read the new element (during the `use
        pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/an9Auq1d6ldm.html#advobsl5jla062999>`_
        ).

        You can create a superelement from an original by:

        * Transferring the original's geometry from the active coordinate system into another coordinate
          system ( ``KCNTO`` )

        * Offsetting its geometry in the global Cartesian coordinate system ( ``DX``, ``DY``, and ``DZ`` )

        * Offsetting its node numbers ( ``INC`` ).

        A combination of methods is valid. If you specify both the geometry transfer and the geometry
        offset, the transfer occurs first.

        If you specify rotation of the transferred superelement's nodal coordinate systems into the
        ``KCNTO`` system ( ``NOROT`` = 0), the rotated nodes cannot be coupled via the :ref:`cp` command; in
        this case, issue the :ref:`ce` command instead. If you specify no rotation of the nodal coordinate
        systems ( ``NOROT`` = 1) for models with displacement degrees of freedom, and ``KCNTO`` is not the
        active system, the superelement ``Sename`` must have six MDOF at each node that has MDOF; therefore,
        only elements with all six structural DOFs are valid in such cases.

        There is no limit to the number of copies that can be made of a superelement, provided the copies
        are all generated from the same original superelement. However, nested copies are limited to five.
        In other words, the total number of different ``Sename`` usages on the :ref:`setran` and
        :ref:`sesymm` commands is limited to five.

        This command is not supported if the original superelement matrix was created in a component mode
        synthesis analysis generation pass with the element results calculation activated ( ``Elcalc`` = YES
        on :ref:`cmsopt` ).
        """
        command = f"SETRAN,{sename},{kcnto},{inc},{file},{ext},,{dx},{dy},{dz},{norot}"
        return self.run(command, **kwargs)


