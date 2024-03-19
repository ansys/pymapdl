class Rezoning:
    def rezone(self, option="", ldstep="", sbstep="", **kwargs):
        """Initiates the rezoning process, sets rezoning options, and rebuilds the

        APDL Command: REZONE
        database.

        Parameters
        ----------
        option
            The rezoning method to employ:

            MANUAL - Manual rezoning. You decide when to use rezoning, what region(s) to rezone, and
                     what remeshing method to use on the selected region(s).
                     This method is currently the default and only option.

        ldstep
            The load step number at which rezoning should occur. The default
            value is the highest load step number found in the Jobname.Rnnn
            files (for the current jobname and in the current directory).

        sbstep
            The substep number of the specified load step (LDSTEP) at which
            rezoning should occur. The default value is the highest substep
            number found in the specified load step in the Jobname.Rnnn files
            (for the current jobname and in the current directory).

        Notes
        -----
        The REZONE command rebuilds the database (.db file) based on the
        specified load step and substep information, and updates nodes to their
        deformed position for remeshing.

        Before issuing this command, clear the database via the /CLEAR command.

        For more information, see Rezoning in the Advanced Analysis Guide.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"REZONE,{option},{ldstep},{sbstep}"
        return self.run(command, **kwargs)

    def mapsolve(self, maxsbstep="", **kwargs):
        """Maps solved node and element solutions from an original mesh to a new

        APDL Command: MAPSOLVE
        mesh.

        Parameters
        ----------
        maxsbstep
            The maximum number of substeps for rebalancing the residuals. The
            default value is 5.

        Notes
        -----
        Used during the rezoning process, the MAPSOLVE command maps solved node
        and element solutions from the original mesh to the new mesh and
        achieves equilibrium based on the new mesh.

        Additional substeps are necessary to reduce the residuals to zero.

        During the rebalancing stage, the external loads and time remain
        unchanged.

        The MAPSOLVE command is valid only for rezoning (REZONE).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MAPSOLVE,{maxsbstep}"
        return self.run(command, **kwargs)

    def mapvar(
        self,
        option="",
        matid="",
        istrtstress="",
        ntenstress="",
        istrtstrain="",
        ntenstrain="",
        istrtvect="",
        nvect="",
        **kwargs,
    ):
        """Defines tensors and vectors in user-defined state variables for

        APDL Command: MAPVAR
        rezoning and in 2-D to 3-D analyses.

        Parameters
        ----------
        option
            DEFINE

            DEFINE - Define variables for the specified MatId material ID (default).

            LIST - List the defined variables for the specified MatId material ID.

        matid
            The material ID for the state variables which you are defining
            (Option = DEFINE) or listing (Option = LIST).

        istrtstress
            The start position of stress-like tensors in the state variables.
            This value must be either a positive integer or 0 (meaning no
            stress-like tensors).

        ntenstress
            The number of stress-like tensors in the state variables. This
            value must be either a positive integer (or 0), and all stress-like
            tensors must be contiguous.

        istrtstrain
            The start position of strain-like tensors in the state variables.
            This value must be either a positive integer or 0 (meaning no
            strain-like tensors).

        ntenstrain
            The number of strain-like tensors in the state variables. This
            value must be either a positive integer (or 0), and all strain-like
            tensors must be contiguous.

        istrtvect
            The start position of vectors in the state variables. This value
            must be either a positive integer or 0 (meaning no vectors).

        nvect
            The number of vectors in the state variables. This value must be
            either a positive integer (or 0), and all vectors must be
            contiguous.

        Notes
        -----
        The MAPVAR command identifies the tensors and vectors in user-defined
        state variables (TB,STATE) for user-defined materials (TB,USER and
        UserMat or UserMatTh) or user-defined creep laws (TB,CREEP,,,,100 and
        UserCreep).

        The command ensures that user-defined state variables are mapped
        correctly during rezoning and in 2-D to 3-D analyses.

        In a rezoning operation, MAPVAR must be issued after remeshing
        (REMESH,FINISH) but before mapping (MAPSOLVE).
        """
        command = f"MAPVAR,{option},{matid},{istrtstress},{ntenstress},{istrtstrain},{ntenstrain},{istrtvect},{nvect}"
        return self.run(command, **kwargs)

    def remesh(self, action="", filename="", ext="", opt1="", opt2="", **kwargs):
        """Specifies the starting and ending remeshing points, and other options,

        APDL Command: REMESH
        for rezoning.

        Parameters
        ----------
        action
            START

            START - Starts the remeshing operation.

            FINISH - Ends the remeshing operation.

            READ - Reads in a generic (.cdb format) new mesh file generated by a third-party
                   application. This remeshing option applies to both 2-D and
                   3-D rezoning.

            SPLIT - Splits selected elements of an existing 2-D or 3-D mesh such that a
                    quadrilateral element is split into four quadrilaterals, a
                    degenerate quadrilateral is split into three
                    quadrilaterals, and a quadratic triangular element is split
                    into four quadratic triangles.  A tetrahedral element is
                    split into eight tetrahedra.

        filename
            Name of a .cdb generic mesh file. The default value is jobname.
            Valid only when Action = READ.

        ext
            File name extension. The only valid (and the default) extension is
            CDB. Valid only when Action = READ.

        opt1
            Specifies options for the new mesh when using a generic imported
            mesh file or the mesh-splitting remeshing method. Valid only when
            Action = READ or Action = SPLIT.

            REGE - Regenerates all node and element numbers on the new
                    mesh using an offset of the highest existing node
                    and element numbers. This is the default behavior
                    when Action = READ; otherwise, this value is
                    ignored.

            KEEP - Keeps the similarly numbered nodes and elements in
                    the new and the old meshes unchanged. Valid only
                    when Action = READ.

            TRAN - Generates transition elements to ensure nodal
                    compatibility between split and unsplit parts of
                    the mesh. Valid only when Action = SPLIT for 2-D
                    analyses.

        opt2
            Specifies transition options for the mesh when elements are split.
            These options are valid only when Action = SPLIT for 2-D analyses.

            QUAD  - Minimizes the number of degenerate elements in the transition mesh and tries to
                    maximize the number of quadrilateral transition elements
                    across several layers of elements from the split regions.
                    This is the default behavior.

            DEGE  - Creates transition zones between the split and unsplit parts of the mesh using
                    mostly degenerate elements with a single element layer.

        Notes
        -----
        The REMESH command is valid only during the rezoning (REZONE) process.

        In rezoning, a REMESH,START command temporarily exits the /SOLU
        solution processor and enters a special mode of the /PREP7
        preprocessor, after which a limited number of preprocessing commands
        are available for mesh control, but no solution commands are valid.

        A REMESH,FINISH command exits the remeshing process and reenters the
        solution processor, at which point no preprocessing commands are
        available. If the new mesh exists, the command creates contact elements
        if needed, and transfers all boundary conditions (BCs) and loads from
        the original mesh to the new mesh. You can issue any list or plot
        command to verify the created contact elements, transferred BCs, and
        loads. A REMESH,FINISH command is valid only after a previously issued
        REMESH,START command, and is the only way to safely end the remeshing
        operation (and exit the special mode of the /PREP7 preprocessor).

        A REMESH,READ command is valid only when you want to perform a rezoning
        operation using a generic new mesh generated by a third-party
        application (rather than a new mesh generated internally by the ANSYS
        program). The command is valid between REMESH,START and REMESH,FINISH
        commands. In this case, the only valid file extension is .cdb (Ext =
        CDB). When Option = KEEP, ANSYS assumes that the common node and
        element numbers between the old and the new mesh are topologically
        similar (that is, these commonly numbered areas have the same element
        connectivity and nodal coordinates).

        A REMESH,SPLIT command is valid only when you wish to perform a
        rezoning operation by splitting the existing mesh. The command is valid
        between REMESH,START and REMESH,FINISH commands.

        You can use REMESH,READ and REMESH,SPLIT commands for horizontal
        multiple rezoning provided that the meshes used in REMESH,READ do not
        intersect. (ANSYS recommends against issuing an AREMESH command after
        issuing either of these commands.)

        For more detailed about the remeshing options available to you during a
        rezoning operation, see Rezoning in the Advanced Analysis Guide.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        return self.run(f"REMESH,{action},{filename},{ext},,{opt1},{opt2}", **kwargs)

    def aremesh(self, lcomb="", angle="", **kwargs):
        """Generates an area in which to create a new mesh for rezoning.

        APDL Command: AREMESH

        Parameters
        ----------
        lcomb
            Specifies how to combine adjacent line segments:

             0 - Line segments combined by connecting ends to ends. This value is the default.

            -1 - No line segments combined.

        angle
            The maximum angle (in degrees) allowed for connecting two line
            segments together. The default value is 30. This value is valid
            only when LCOMB = 0.

        Notes
        -----
        Issue the AREMESH command after issuing a REMESH,START command and
        before issuing a REMESH,FINISH command.

        The AREMESH command cannot account for an open area (or "hole") inside
        a completely enclosed region. Instead, try meshing around an open area
        by selecting two adjoining regions; for more information, see Hints for
        Remeshing Multiple Regions .
        """
        command = f"AREMESH,{lcomb},{angle}"
        return self.run(command, **kwargs)
