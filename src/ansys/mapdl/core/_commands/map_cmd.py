class MapCommand:
    def ftype(self, filetype="", prestype="", **kwargs):
        """Specifies the file type and pressure type for the subsequent import of

        APDL Command: FTYPE
        source points and pressures.

        Parameters
        ----------
        filetype
            Type of file from which the pressure data will be retrieved (no
            default):

            CFXTBR - File from a CFX Transient Blade Row (TBR) analysis export.

            CFDPOST - File from a CFD-Post BC Profile export.

            FORMATTED - Formatted file.

            CSV - Comma-Separated Values file.

        prestype
            Type of pressure data contained in the file:

            0 - Only real-valued pressures are on the file.

            1 - Real-valued and imaginary-valued pressures are on the file (default).

        Notes
        -----
        CFX Transient Blade Row files (FileType = CFXTBR) are obtained from the
        Export Results Tab in CFX-Pre, with [Export Surface Name]: Option set
        to Harmonic Forced Response.

        CFD-Post files (FileType = CFDPOST) are obtained from the Export action
        in CFD-Post with Type set to BC Profile.

        Formatted files (FileType = FORMATTED) contain the coordinates and
        pressure data in fixed-format columns in the order  x, y, z, pressure.
        You may have other columns of data in the file which can be skipped
        over in the Format specifier on the READ command, but the data must be
        in that order.

        Comma-separated values files (FileType = CSV) contain the coordinates
        and pressure data in comma-separated fields. The data can be in any
        order, and other fields of data may also be present.
        """
        command = f"FTYPE,{filetype},{prestype}"
        return self.run(command, **kwargs)

    def map(self, kdim="", kout="", limit="", **kwargs):
        """Maps pressures from source points to target surface elements.

        APDL Command: MAP

        kdim
            Interpolation key:

            * ``"0 or 2"`` : Interpolation is done on a surface (default).

            * ``"3"`` : Interpolation is done within a volume. This option
              is useful if the supplied source data is volumetric field
              data rather than surface data.

        kout
            Key to control how pressure is applied when a target node is
            outside of the source region:

            * ``"0"`` : Use the pressure(s) of the nearest source point
              for target nodes outside of the region (default).

            * ``"1"`` : Set pressures outside of the region to zero.

        limit
            Number of nearby points considered for interpolation. The minimum
            is 5; the default is 20. Lower values reduce processing
            time. However, some distorted or irregular meshes will require a
            higher ``LIMIT`` value to find the points encompassing the target node
            in order to define the region for interpolation.

        Notes
        -----
        Maps pressures from source points to target surface elements.
        """
        return self.run(f"MAP,,{kdim},,{kout},{limit}", **kwargs)

    def plgeom(self, item="", nodekey="", **kwargs):
        """Plots target and source geometries.

        APDL Command: PLGEOM

        Parameters
        ----------
        item
            Items to plot:

            BOTH - Plot both target and source geometries (default).

            TARGET - Plot only the target geometry.

            SOURCE - Plot only the source geometry.

        nodekey
            If the source data contains faces (that is, surface elements were
            created upon the READ command), set NODEkey = 1 to plot only the
            source nodes rather than both the nodes and the elements.

        Notes
        -----
        Target faces are displayed in gray and source points in yellow. If the
        source data contains faces (that is, surface elements were created upon
        the READ command), the source faces are also displayed in blue (unless
        NODEkey = 1), and both surfaces are made translucent.
        """
        command = f"PLGEOM,{item},{nodekey}"
        return self.run(command, **kwargs)

    def plmap(self, item="", nodekey="", imagkey="", **kwargs):
        """Plots target and source pressures.

        APDL Command: PLMAP

        Parameters
        ----------
        item
            Items to plot:

            BOTH - Plot both target and source pressures (default).

            TARGET - Plot only the target pressures.

            SOURCE - Plot only the source pressures.

        nodekey
            If the source data contains faces (that is, surface
            elements were created upon the READ command), set NODEkey
            = 1 to plot only the source nodes rather than both the
            nodes and the elements.

        imagkey
            1 - Plot the real pressures (default).

            0 - Plot the imaginary pressures.

        Notes
        -----
        Pressures on the target faces are displayed as a color contour
        plot using the command /PSF,PRES,,3. If the source data
        contains faces (that is, surface elements were created upon
        the READ command), the source faces are also displayed using a
        color contour plot by default. If NODEkey = 1 or no source
        faces are available, the source pressures are displayed as
        colored node symbols (/PSYMB,DOT,1 command).
        """
        return self.run(f"PLMAP,{item},,{nodekey},{imagkey}", **kwargs)

    def read(
        self,
        fname="",
        nskip="",
        format_="",
        xfield="",
        yfield="",
        zfield="",
        prfield="",
        pifield="",
        **kwargs,
    ):
        """Reads coordinate and pressure data from a file.

        APDL Command: READ

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        nskip
            Number of lines at the beginning of the file that will be skipped
            while it is read. Default = 0. NSKIP is ignored for FileType =
            CFXTBR or CFDPOST on the FTYPE command.

        format\_
            For FileType = FORMATTED on the FTYPE command, Format is the read
            format in the FORTRAN FORMAT convention enclosed in parentheses;
            for example: (3e10.0,10x,e10.0,70x,e10.0)

        xfield, yfield, zfield, prfield, pifield
            For FileType = CSV on the FTYPE command, these are field numbers
            locating the coordinates and real and imaginary (if present)
            pressures. The field value may not exceed 20.

        Notes
        -----
        Reads coordinate and pressure data from the specified file. The file
        type must have been previously specified on the FTYPE command.

        Upon reading the file, nodes are created for the source points. For
        FileType = CFXTBR or CFDPOST on the FTYPE command, if face data is
        available, SURF154 elements are also created. A nodal component named
        SOURCENODES and an element component named SOURCEELEMS are created
        automatically.
        """
        command = f"READ,{fname},{nskip},{format_},{xfield},{yfield},{zfield},{prfield},{pifield}"
        return self.run(command, **kwargs)

    def slashmap(self, **kwargs):
        """Enters the mapping processor.

        APDL Command: /MAP

        Notes
        -----
        Enters the mapping processor. This processor is used to read in source
        data from an external file and map it to the existing geometry.

        The current database is saved (to BeforeMapping.DB) upon entering the
        processor, and it is resumed upon exiting (FINISH command). Any nodes
        or elements not on the target surface are deleted for easier viewing of
        the mapping quantities. A database of this mapping geometry
        (Mapping.DB) is also saved at the FINISH command.

        This command is valid only at the Begin Level.
        """
        command = f"/MAP,"
        return self.run(command, **kwargs)

    def target(self, nlist="", **kwargs):
        """Specifies the target nodes for mapping pressures onto surface effect

        APDL Command: TARGET
        elements.

        Parameters
        ----------
        nlist
            Nodes defining the surface upon which the pressures will be mapped.
            Use the label ALL or specify a nodal component name. If ALL, all
            selected nodes [NSEL] are used (default). Individual nodes may not
            be entered.

        Notes
        -----
        The node list specified by Nlist must contain a sufficient number of
        nodes to define an element surface. The surface must be meshed (ESURF
        command) with SURF154 elements prior to issuing this command.
        """
        command = f"TARGET,{nlist}"
        return self.run(command, **kwargs)

    def writemap(self, fname="", **kwargs):
        """Writes interpolated pressure data to a file.

        APDL Command: WRITEMAP

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        Notes
        -----
        Writes the interpolated pressure data to the specified
        file. The data is written as SFE commands applied to the
        SURF154 elements that are on the target surface. You may read
        this data for inclusion in an analysis by using /INPUT,Fname.
        """
        return self.run(f"WRITEMAP,{fname}", **kwargs)
