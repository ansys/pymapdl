class MultiFieldSolverInterfaceMapping:
    def mfbucket(self, key="", value="", **kwargs):
        """Turns a bucket search on or off.

        APDL Command: MFBUCKET

        Parameters
        ----------
        key
            Bucket search key:

            ON - Activates a bucket search (default).

            OFF - Deactivates a bucket search. A global search is then activated.

        value
            Scaling factor (%) used to determine the number of buckets for a
            bucket search. Defaults to 50%.

        Notes
        -----
        A bucket search will more efficiently compute the mapping of surface
        and volumetric interpolation data across field interfaces (flagged by
        the FSIN label using SF, SFA, SFE, or SFL or the FVIN label using BFE).

        The number of buckets used to partition a flagged interface is equal to
        the scaling factor (%) times the total number of interface elements.
        For example, for the default scaling factor of 50% and a 10,000 element
        interface, 5,000 buckets are used.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFBUCKET,{key},{value}"
        return self.run(command, **kwargs)

    def mfci(self, val1="", val2="", **kwargs):
        """Sets the control parameters used by the conservative (CPP)

        APDL Command: MFCI
        interpolation scheme.

        Parameters
        ----------
        val1
            Controls the pixel resolution. The higher the resolution, the more
            accurate and more expensive the conservative (CPP) interpolation
            will be. Valid values are 10 to 256; defaults to 100.

        val2
            The separation factor to handle any gap between the two surfaces.
            It is a relative measure of the gap, normalized by the averaged
            element face sizes from both sides of the interface. Defaults to
            0.1.

        Notes
        -----
        In a conservative (CPP) interpolation scheme as specified on the
        MFLCOMM command, each element face is first divided into n number of
        faces, where n is the number of nodes on the face. The three-
        dimensional faces are then converted onto a two-dimensional polygon
        made up of rows and columns of dots called pixels. By default, these
        pixels have a resolution of 100 x 100; use VAL1 to increase the
        resolution and improve the accuracy of the algorithm. See Load
        Interpolation in the Coupled-Field Analysis Guide for more information
        on interpolation schemes and adjusting the pixel resolution for the
        conservative interpolation scheme.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFCI,{val1},{val2}"
        return self.run(command, **kwargs)

    def mfmap(self, lab1="", lab2="", filename="", opt="", **kwargs):
        """Calculates, saves, resumes, or deletes mapping data in an ANSYS Multi-

        APDL Command: MFMAP
        field solver analysis.

        Parameters
        ----------
        lab1
            Operation label:

            CALC  - Calculate mapping data and keep it in memory (default).

            SAVE  - Calculate mapping data, keep it in memory, and save it to a file. (If
                    MFMAP,CALC or MFMAP,RESU have been issued, just save it to
                    a file.)

            RESU  - Resume the mapping from a file and keep it in memory.

            DELE  - Free the mapping memory.

        lab2
            Applicable mapping label:

            ALL  - Surface and volumetric mapping.

            SURF  - Surface mapping only.

            VOLU  - Volumetric mapping only.

        filename
            The file name for a mapping data file (filename.sur for surface
            mapping and filename.vol for volumetric mapping). Defaults to
            Jobname. Applies to the commands MFMAP,SAVE and MFMAP,RESU only.

        opt
            File format:

            BINA  - Binary file (default).

            ASCI  - ASCII file.

        Notes
        -----
        This command calculates, saves, resumes, or deletes mapping data. It
        defaults to calculating the mapping data. If MFMAP has not been
        previously issued, the mapping data will be automatically calculated
        during the solution process. On the other hand, the ANSYS Multi-field
        solver will use previously created mapping data. Resumed mapping files
        must have load transfer specifications that are consistent with those
        of the current MFSURFACE and MFVOLUME commands and the ANSYS database.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFMAP,{lab1},{lab2},{filename},{opt}"
        return self.run(command, **kwargs)

    def mftol(self, key="", value="", toler="", **kwargs):
        """Activates or deactivates normal distance checking for surface mapping

        APDL Command: MFTOL
        in an ANSYS Multi-field solver analysis.

        Parameters
        ----------
        key
            Normal distance key

            ON - Activates normal distance checking.

            OFF - Deactivates normal distance checking (default).

        value
            The normal distance tolerance for surface mapping.  Defaults to
            1.0e-6. If Toler = REL, Value is dimensionless. If Toler = ABS,
            Value has the dimensions of length.

        toler
            Tolerance definition key

            REL - Activates relative gap tolerance, which is independent of units (default).

            ABS - Activates absolute gap tolerance.

        Notes
        -----
        For a dissimilar mesh interface, the nodes of one mesh are mapped to
        the local coordinates of an element in the other mesh. When normal
        distance checking is activated, the mapping tool checks the normal
        distance from the node to the nearest element. The node is considered
        improperly mapped if the normal distance exceeds the tolerance value.
        The mapping tool creates a component to graphically display the
        improperly mapped nodes. See Mapping Diagnostics in the Coupled-Field
        Analysis Guide for more information.

        When using relative gap tolerance (Toler = REL), the normal distance
        tolerance is derived from the product of the relative tolerance Value
        and the largest dimension of the Cartesian bounding box for a specific
        interface. Therefore, each interface will have a different normal
        distance tolerance , even though MFTOL is a global command.

        This command is also valid in PREP7.

        See Multi-field Commands in the Coupled-Field Analysis Guide for a list
        of all ANSYS Multi-field solver commands and their availability for MFS
        and MFX analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MFTOL,{key},{value},{toler}"
        return self.run(command, **kwargs)
