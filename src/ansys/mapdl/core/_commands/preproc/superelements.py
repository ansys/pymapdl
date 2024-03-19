class Superelements:
    def se(self, file="", toler="", **kwargs):
        """Defines a superelement.

        APDL Command: SE

        Parameters
        ----------
        file
            The name (case sensitive) of the file containing the
            original superelement matrix created by the generation
            pass (Sename.SUB).  The default is the current Jobname.

        toler
            Tolerance used to determine if use pass nodes are
            noncoincident with master nodes having the same node
            numbers.  Defaults to 0.0001.  Use pass nodes will always
            be replaced by master nodes of the same node number.
            However, if a use pass node is more than TOLER away from
            the corresponding master node, a warning is generated.

        Notes
        -----
        Defines a superelement by reading in the superelement matrices
        and master nodes from the superelement matrix file.  The
        matrix file (File.SUB) must be available from the substructure
        generation pass.  The proper element type (MATRIX50) must be
        active [TYPE] for this command.  A scratch file called
        File.SORD showing the superelement names and their
        corresponding element numbers is also written.
        """
        return self.run(f"SE,{file},,,{toler}", **kwargs)

    def sedlist(self, sename="", kopt="", **kwargs):
        """Lists the DOF solution of a superelement after the use pass.

        APDL Command: SEDLIST

        Parameters
        ----------
        sename
            Name of the superelement in Jobname.DSUB to be listed.  If a
            number, it is the element number of the superelement as used in the
            use pass.  If ALL, list results for all superelements.

        kopt
            List key:

            0 - List summary data only.

            1 - List full contents.  Be aware that the listing may be extensive.

        Notes
        -----
        Lists the degree of freedom solution of a superelement after the
        substructure use pass.  Results may be listed for any superelement on
        File.DSUB.

        This command is valid in any processor.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"SEDLIST,{sename},{kopt}"
        return self.run(command, **kwargs)

    def selist(self, sename="", kopt="", kint="", **kwargs):
        """Lists the contents of a superelement matrix file.

        APDL Command: SELIST

        Parameters
        ----------
        sename
            The name (case-sensitive) of the superelement matrix file created
            by the substructure generation pass (Sename.SUB).   Defaults to the
            current Jobname.  If a number, it is the element number of the
            superelement as used in the use pass.

        kopt
            List key:

            0 - List summary data only.

            1 - List contents, except load vectors and matrices.

            2 - List contents, except matrices.

            3 - List full contents.  Be aware that the listing may be extensive.

        kint
            Integer printout format key:

            OFF - Default.

            ON - Long format for large integers.

        Notes
        -----
        This command is valid in any processor.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"SELIST,{sename},{kopt},{kint}"
        return self.run(command, **kwargs)

    def sesymm(self, sename="", ncomp="", inc="", file="", ext="", **kwargs):
        """Performs a symmetry operation on a superelement within the use pass.

        APDL Command: SESYMM

        Parameters
        ----------
        sename
            The name (case-sensitive) of the superelement matrix file
            created by the substructure generation pass (Sename.SUB).
            Defaults to the current Jobname.  If a number, it is the
            element number of a previously defined superelement in the
            current use pass.

        ncomp
            Symmetry key:

            X - X symmetry (default).

            Y - Y symmetry.

            Z - Z symmetry.

        inc
            Increment all nodes in the superelement by INC.

        file
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Performs a symmetry operation on a superelement within the
        substructure use pass by reversing the sign of component Ncomp
        in the global Cartesian coordinate system.  The node numbers
        are incremented by INC.  The new superelement is written to
        File.SUB in the current directory (by default).  All master
        node nodal coordinate systems must be global Cartesian (no
        rotated nodes allowed).

        The maximum number of transformations for a given superelement
        is five (including SETRAN, SESYMM, and the large rotation
        transformation if NLGEOM is ON in the use pass).

        Distributed ANSYS Restriction: This command is not supported
        in Distributed ANSYS.
        """
        command = f"SESYMM,{sename},{ncomp},{inc},{file},{ext}"
        return self.run(command, **kwargs)

    def setran(
        self,
        sename="",
        kcnto="",
        inc="",
        file="",
        ext="",
        dx="",
        dy="",
        dz="",
        norot="",
        **kwargs,
    ):
        """Creates a superelement from an existing superelement.

        APDL Command: SETRAN

        Parameters
        ----------
        sename
            The name (case-sensitive) of the file containing the original
            superelement matrix created by the generation pass (Sename.SUB).
            The default is the current Jobname.  If Sename is a number, it is
            the element number of a previously defined superelement in the
            current use pass.

        kcnto
            The reference number of the coordinate system to where the
            superelement is to be transferred. The default is the global
            Cartesian system.  Transfer occurs from the active coordinate
            system.

        inc
            The node offset.  The default is zero.  All new element node
            numbers are offset from those on the original by INC.

        file
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        dx, dy, dz
            Node location increments in the global Cartesian coordinate system.
            Defaults to zero.

        norot
            Node rotation key:

            0 - The nodal coordinate systems of the transferred superelement rotate into the
                KCNTO system. (That is, the nodal coordinate systems rotate
                with the superelement.) The superelement matrices remain
                unchanged. This value is the default.

            1 - The nodal coordinate systems do not rotate. (That is, they remain fixed in
                their original global orientation.)  The superelement matrices
                and load vectors are modified if any rotations occur.

        Notes
        -----
        The SETRAN command creates a superelement from an existing superelement
        and writes the new element to a file.  You can then issue an SE command
        to read the new element (during the use pass).

        You can create a superelement from an original by:

        Transferring the original's geometry from the active coordinate system
        into another coordinate system (KCNTO)

        Offsetting its geometry in the global Cartesian coordinate system (DX,
        DY, and DZ )

        Offsetting its node numbers (INC).

        A combination of methods is valid. If you specify both the geometry
        transfer and the geometry offset, the transfer occurs first.

        If you specify rotation of the transferred superelement's nodal
        coordinate systems into the KCNTO system (NOROT = 0), the rotated nodes
        cannot be coupled via the CP command; in this case, issue the CE
        command instead. If you specify no rotation of the nodal coordinate
        systems (NOROT = 1) for models with displacement degrees of freedom,
        and KCNTO is not the active system, the superelement Sename must have
        six MDOF at each node that has MDOF; therefore, only elements with all
        six structural DOFs are valid in such cases.

        There is no limit to the number of copies that can be made of a
        superelement, provided the copies are all generated from the same
        original superelement. However, nested copies are limited to five. In
        other words, the total number of different Sename usages on the SETRAN
        and SESYMM commands is limited to five.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"SETRAN,{sename},{kcnto},{inc},{file},{ext},,{dx},{dy},{dz},{norot}"
        return self.run(command, **kwargs)
