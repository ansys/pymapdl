class Radiosity:
    def rdec(self, option="", reduc="", nplace="", **kwargs):
        """Defines the decimation parameters.

        APDL Command: RDEC

        Parameters
        ----------
        option
            Command options:

            DEFINE  - Defines the decimation parameters (default).

            STAT - Shows the status/listing. Other command options are ignored.

        reduc
            Approximate reduction in the number of surface
            elements. Valid range is from 0.0 (no decimation, the
            default) to 1.0. This number is a factor applied to the
            initial number of element radiosity surfaces.

        nplace
            Node placement algorithm

            OPTI - Optimal placement. An edge is collapsed by moving
                    both nodes (I and J in the figure below) to a new
                    location.

            SUBS - Subset placement. An edge is collapsed by moving
                    one node to another one. In the figure below, node
                    I is moved to node J.

        Notes
        -----
        Decimation is the process of simplifying a fine surface mesh into a
        coarse one. This process is accomplished by a sequence of edge
        collapses.

        The maximum degree of decimation (1.0) is unreachable. The real degree
        of decimation is always less than 1.0 because the decimated mesh must
        always consist of at least one element.
        """
        return self.run(f"RDEC,{option},{reduc},,{nplace}", **kwargs)

    def rsopt(self, opt="", filename="", ext="", dir_="", **kwargs):
        """Creates or loads the radiosity mapping data file for SURF251 or SURF252

        APDL Command: RSOPT
        element types.

        Parameters
        ----------
        opt
            File option:

            SAVE - Write the radiosity mapping data to a file. (Default)

            LOAD - Read in the specified mapping data file.

        fname
            File name for radiosity mapping data file. Defaults to Jobname.

        ext
            Filename extension for radiosity mapping data file (default =
            .rsm).

        dir\_
            Directory path for radiosity mapping data file. If you do not
            specify a directory path, it will default to your working
            directory.

        Notes
        -----
        Use this command to manually create or load a radiosity mapping data
        file. This command is useful if you want to create the mapping data
        file without issuing SAVE or CDWRITE, or if you want to specify that
        the file be located in a directory other than your working directory.
        Also use this command to manually load an existing mapping data file
        during a restart.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RSOPT,{opt},{filename},{ext},{dir_}"
        return self.run(command, **kwargs)

    def rsurf(self, options="", delopts="", etnum="", **kwargs):
        """Generates the radiosity surface elements (SURF251/SURF252) and stores

        APDL Command: RSURF
        them in the database.

        Parameters
        ----------
        options
            Command options:

            CLEAR  - Deletes radiosity surface elements and nodes. The set of elements and nodes to
                     be deleted is defined by Delopts. ETNUM is ignored.

            DEFINE  - Creates the radiosity surface elements and nodes (default).

            STAT - Shows the status/listing. Other command options are ignored.

        delopts
            Deletion options

            ALL  - Deletes all radiosity surface elements and nodes.

            LAST  - Deletes radiosity surface elements and nodes created by the last RSURF command.

        etnum
            Element type number. Leave blank to indicate the next available
            number.

        Notes
        -----
        This command generates the radiosity surface elements based on the
        RSYMM and RDEC parameters and stores them in the database. It works
        only on the faces of selected underlying elements that have RDSF flags
        on them and all corner nodes selected. You can issue multiple RSURF
        commands to build the radiosity model. However, all RSURF commands must
        be issued after issuing the RSYMM, and after the model is complete
        (i.e., after all meshing operations are complete).

        If you do issue multiple RSURF commands for different regions, you must
        first mesh the different regions, and then generate the radiosity
        surface elements on each meshed region individually. Use RSURF,,,ETNUM
        to assign a separate element type number to each region. This procedure
        allow you to identify the individual regions later in the multi-field
        analysis.

        If the underlying solid elements are higher order, the radiosity
        surface elements are always lower order (4- or 3-node in 3-D or 2-node
        in 2-D). Decimation will always occur before any symmetry operations.

        For 2-D axisymmetric YR models, the newly-generated nodes can have only
        positive Y coordinates.

        If you have already issued RSURF for a surface and you issue RSURF
        again, the program creates a new set of radiosity surface elements and
        nodes over the existing set, resulting in an erroneous solution.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.

        This is an action command (that creates or deletes surface meshes) and
        is serial in nature. Even if Distributed ANSYS is running, the RSURF
        command runs serially
        """
        command = f"RSURF,{options},{delopts},{etnum}"
        return self.run(command, **kwargs)

    def rsymm(self, option="", cs="", axis="", nsect="", condvalue="", **kwargs):
        """Defines the plane of symmetry or center of rotation for the radiosity

        APDL Command: RSYMM
        method.

        Parameters
        ----------
        option
            Command options:

            CLEAR  - Deletes all symmetry definitions. Other command options are ignored.

            DEFINE  - Defines the symmetry (default).

            STAT - Shows the status/listing. Other command options are ignored.

            COND - Activates or deactivates condensation in the radiosity solver for all defined
                   radiation symmetries. Condensation is the process where the
                   radiosity equation system is reduced in size. Default is
                   off. (See Figure 7: Usage Example: Option = COND .)

        cs
            Local coordinate system (11) as defined using the LOCAL or CS
            commands or a global coordinate system (0). For planar reflection,
            the coordinate system origin must be on the plane of symmetry (POS)
            and one of its axes must be normal to the POS. For cyclic
            reflection, the coordinate system origin must be coincident with
            the center of rotation (COR). Only Cartesian systems are valid.

        axis
            Axis label of the coordinate system (CS) that is normal to the POS
            for planar reflection. For 2-D model planar reflections, valid
            labels are X or Y. For 3-D model planar reflections, valid labels
            are X, Y, or Z. Must be blank for cyclic reflection. For cyclic
            reflection, it is assumed that the Z axis is aligned with the axis
            of rotation.

        nsect
            Number of cyclic reflections to be done  (1). This field must be
            blank or 0 for planar reflection. Default is blank.

        condvalue
            Condensation key. Valid only when Option = COND.

            ON - Activates condensation in the radiosity solver for all defined radiation
                 symmetries.

            OFF - Deactivates condensation in the radiosity solver for all defined radiation
                  symmetries (default).

        Notes
        -----
        This command is used to define the POS for planar reflection or the COR
        for cyclic reflection. The RSYMM command must be issued before RSURF
        and it may be issued multiple times to have more than one planar/cyclic
        reflection; however, the RSURF command processes them in the order they
        are issued.

        For planar reflection, you must define a local coordinate system  (11)
        with its origin on the POS. One of its axes must be aligned so that it
        is normal to the plane. If possible, use the existing global coordinate
        system (0).

        For cyclic reflection, you must define a local coordinate system  (11)
        with its origin coincident with the COR. Reflections occur about the
        local Z-axis in the counterclockwise direction. You must align the
        Z-axis properly. If possible, use the existing global coordinate system
        (0).

        New surface elements generated inherit the properties of the original
        elements.

        For 2-D axisymmetric models, RSYMM can be used only for symmetrization
        in the YR plane. It cannot be used for the theta direction. Use V2DOPT
        in that case.

        For 2-D axisymmetric YR models, the newly-generated nodes can have only
        positive X coordinates.

        Figure: 7:: : Usage Example: Option = COND

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RSYMM,{option},{cs},{axis},{nsect},{condvalue}"
        return self.run(command, **kwargs)

    def qsopt(self, opt="", **kwargs):
        """Specifies quasi static radiation options.

        APDL Command: QSOPT

        Parameters
        ----------
        opt
            Quasi static option:

            OFF - Do not run transient radiation problem to steady-state (default).

            ON - Run transient radiation problem to steady-state.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"QSOPT,{opt}"
        return self.run(command, **kwargs)
