"""These SESSION commands are for file operations, such as deleting, copying, and listing."""

import os


class Files:
    def anstoasas(self, fname="", key="", **kwargs):
        """Creates an ASAS input file from the current ANSYS model.

        APDL Command: ANSTOASAS

        Parameters
        ----------
        fname
            ASAS file name. Defaults to Jobname.

        key
            Key indicating type of file to produce:

            0 - ASAS file for use by ANSYS Aqwa (no loads written). Creates the file
                Fname.asas.

            1 - ASAS file (all data written, including loads). Creates the file Fname.asas.

            2 - ASAS(NL) file. Creates the file Fname.asnl.

        Notes
        -----
        This command creates an input file for the ANSYS Asas Finite Element
        Analysis System from the model and loads currently in the database,
        based on the currently selected set of elements. Most common structural
        element types are written, as well as sections (or real constants),
        materials, boundary conditions and loads, and solution and load step
        options.

        Data Written

        The following data is written:

        Solution control options

        Nodes

        Elements

        Material data

        Geometry data

        Section data

        ANSYS element components (ASAS sets)

        Boundary conditions

        Loads

        Added mass (via MASS21 element)

        Details are provided in the following sections.

        Not all data is written. You must verify the completeness and accuracy
        of the data. Only loading at the current step is transferred; hence, no
        load step history is captured.

        Solution Control Options

        The ASAS project name is defined as "ANSYS".

        The solution control options are converted as follows:

        JOB: STAT SPIT: KGEOM

        JOB: STAT SPIT: KGEOM

        For conversion to ASAS(NL), the large displacement option is set based
        on NLGEOM, final load solution time is set based on TIME, and sub-step
        times are set based on DELTIM or NSUBST (assuming constant step size).

        Element Data

        If you intend to use the data only with AQWA-WAVE, only the elements
        that form the wetted surface are required.  Selecting these elements
        before invoking the ANSTOASAS command will improve performance.  In
        order for AQWA-WAVE to identify the direction of the wave loading, all
        elements must be defined by nodes in a clockwise direction. For further
        information, refer to the AQWA-WAVE manual.

        The element types are converted as follows:

        SPR1:  SPR2: if: rotational: spring:  FLA2: (ASAS(L): only):  if:
        nodes: are: not: coincident:  and: longitudinal: spring:

        QUM4:  TRM3: -: if: Triangular

        BRK8:  TET4: -: if: Tetrahedral:  BRK6: -: if: Prism

        QUS4:  TBC3: -: if: Triangular

        QUM8:  TRM6: -: if: Triangular

        BR20:  TE10: -: if: Tetrahedral: :  BR15: -: if: Prism

        QUS4:  TBC3: -: if: Triangular

        QUM4:  TRM3: -: if: Triangular

        QUM8:  TRM6: -: if: Triangular

        BRK8:  TET4: -: if: Tetrahedral:  BRK6: -: if: Prism

        BR20:  TE10: -: if: Tetrahedral:  BR15: -: if: Prism

        TCBM: -: if: ASAS(L):  STF4: -: if: ASAS(NL)

        Documentation for this legacy element type appears in the Feature
        Archive.

        Material Data

        Linear isotropic material conversion is supported for ASAS and
        ASAS(NL).

        Geometry Data
        """
        command = "ANSTOASAS,%s,%s" % (str(fname), str(key))
        return self.run(command, **kwargs)

    def anstoaqwa(
        self,
        fname="",
        vertaxis="",
        gc="",
        rho="",
        hwl="",
        diffkey="",
        symxkey="",
        symykey="",
        **kwargs,
    ):
        """Creates an AQWA-LINE input file from the current ANSYS model.

        APDL Command: ANSTOAQWA

        Parameters
        ----------
        fname
            AQWA file name. Defaults to Jobname.

        vertaxis
            Axis in the vertical direction:

            Y (or 2)  - Global Y axis.

            Z (or 3)  - Global Z axis (default).

        gc
            Gravitational acceleration. Defaults to 9.81.

        rho
            Density of water. Defaults to 1025.0.

        hwl
            Waterline height in model coordinates. Defaults to 0.0.

        diffkey
            Diffracting model key:

            0 - Create a non-diffracting AQWA model.

            1 - Create a diffracting AQWA model (default).

        symxkey
            Key indicating if model is symmetric about the global XZ plane:

            0 - No symmetry about XZ plane (default).

            1 - Use symmetry about XZ plane. Only include (or select) half the model.

        symykey
            Key indicating if model is symmetric about the global YZ plane:

            0 - No symmetry about YZ plane (default).

            1 - Use symmetry about YZ plane. Only include (or select) half the model.

        Notes
        -----
        This command creates the input file Fname.aqwa for the ANSYS Aqwa
        Multi-Body Hydrodynamics System for diffraction analysis in AQWA-LINE
        from the model currently in the database, based on the currently
        selected set of elements. The selected set must only include the hull
        envelope; no internal structure should be selected.

        There should be a line of nodes defined at the waterline. Only those
        elements that are entirely below the waterline will be specified as
        diffracting. If there are no waterline nodes, there will be no
        diffracting elements at the waterline, which will severely reduce the
        accuracy of the diffraction analysis.

        The translator maps PLANE42, SHELL41, SHELL63, and SHELL181 elements to
        PANELs, and maps PIPE16 and PIPE59 elements to TUBEs. It does not
        recognize any other element types. Any material or geometric properties
        can be used for the shell elements, as AQWA does not need any
        properties at all and the command does not use them. All the shell
        elements below the water must have their normals pointing outward.

        TUBE elements in AQWA have material density, outside diameter, wall
        thickness, added mass, and drag coefficients, so appropriate properties
        should be used in the ANSYS model. PIPE59 elements can have added mass
        and damping coefficients; these will be written to the file. The ANSYS
        program uses the inertia coefficient CM, whereas AQWA uses the added
        mass coefficient CA, where CM = (1 + CA). This correction is made
        automatically.

        In AQWA the vertical axis is always the Z-axis. The command can convert
        a model built with either the Y or Z-axis vertical, but the X-axis must
        be horizontal and should preferably be along the fore/aft axis of the
        vessel.  If the structure is symmetric and you wish to use the symmetry
        options, you must only select one half or one quarter of the model, as
        appropriate. If you model a complete vessel and specify X symmetry, the
        AQWA model will contain two sets of coincident elements.

        If you are working from a model created for a structural analysis, it
        will probably be necessary to remesh the model as the structural mesh
        is most likely finer than needed for a diffraction analysis.

        If you enter this command interactively (with the GUI active) and no
        data is provided for the command options, you will be prompted for
        their values.

        You must verify the completeness and accuracy of the data written.
        """
        command = "ANSTOAQWA,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(fname),
            str(vertaxis),
            str(gc),
            str(rho),
            str(hwl),
            str(diffkey),
            str(symxkey),
            str(symykey),
        )
        return self.run(command, **kwargs)

    def assign(self, ident="", fname="", ext="", lgkey="", **kwargs):
        """Reassigns a file name to an ANSYS file identifier.

        APDL Command: /ASSIGN

        Parameters
        ----------
        ident
            ANSYS file name identifier.  Valid identifiers are: CMS, EMAT,
            EROT,  ESAV, FULL, LN07, LN09, LN11, LN20, LN21, LN22, LN25, LN31,
            LN32, MODE, OSAV, RDSP, RFRQ, RMG, RST, RSTP, RTH, SELD, and SSCR.
            See File Management and Files for file descriptions.  If blank,
            list currently reassigned files.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        lgkey
            Key to specify local or global file name control for the specified
            file identifier in a distributed-memory parallel processing
            (Distributed ANSYS) run. For more information on local and global
            files, see File Handling Conventions in the Parallel Processing
            Guide.

            BOTH - Reassign the file name for both the local and global files (default).

            LOCAL - Reassign the file name for only the local files.

            GLOBAL - Reassign the file name for only the global file.

        Notes
        -----
        The reassignment of file names is valid only if it is done before the
        file is used.  All file reassignments are retained (not cleared) even
        if the database is cleared [/CLEAR] or the Jobname is changed
        [/FILNAME].  Assigned files may be overwritten.  If file name arguments
        (Fname, Ext, --) are blank, the default ANSYS assignment is restored.
        Use SEOPT for SUB files and SEEXP for DSUB files.

        This command is valid only at the Begin Level.

        This command also checks to ensure that the path/file is valid and can
        be written by the user. If it is not valid, an error message will be
        returned. Ensure that the directory exists prior to using /ASSIGN
        command.
        """
        return self.run(f"/ASSIGN,{ident},{fname},{ext},,{lgkey}", **kwargs)

    def slashclog(self, fname="", ext="", **kwargs):
        """APDL Command: /CLOG

        Copies the session log file to a named file.

        Parameters
        ----------
        fname
            File name and directory path to which the log file is to be copied
            (248 characters maximum, including directory). If you do not
            specify a directory path, it will default to your working directory
            and you can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        This command is valid in any processor, but only during an interactive
        run.
        """
        command = "/CLOG,%s,%s" % (str(fname), str(ext))
        return self.run(command, **kwargs)

    def copy(self, fname1="", ext1="", fname2="", ext2="", distkey="", **kwargs):
        """Copies a file.

        APDL Command: /COPY

        Parameters
        ----------
        fname1
            File name to be copied and its directory path (248
            characters maximum for both file name and directory). If
            you do not specify a directory path, it will default to
            your working directory and you can use all 248 characters
            for the file name.

        ext1
            Filename extension (eight-character maximum).

        fname2
            File name to be created and its directory path (248
            characters maximum for both file name and directory). If
            you do not specify a directory path, it will default to
            your working directory and you can use all 248 characters
            for the file name.

        ext2
            Filename extension (eight-character maximum).

        distkey
            Key that specifies whether the copy operation is performed
            on all processes in distributed parallel mode (Distributed
            ANSYS):

            0 (OFF or NO) - The program performs the copy operation
            only on the master process (default).

            1 (ON or YES) - The program performs the copy operation
            locally on each process.

            2 or BOTH - The program performs the copy operation for
            Fname.Ext on the master process and for FnameN.Ext on all
            processes.

        Notes
        -----
        The original file is untouched.  Ex: /COPY,A,,,B copies file A
        to B in the same directory.  /COPY,A,DAT,,,INP copies the file
        A.DAT to A.INP.  See the Operations Guide for details.  ANSYS
        binary and ASCII files can be copied.

        In distributed parallel mode (Distributed ANSYS), only the
        master process will copy Fname1.Ext1 to Fname2.Ext2 by
        default. However, when DistKey is set to 1 (or ON or YES), the
        command is executed by all processes. In this case, Fname1 and
        Fname2 will automatically have the process rank appended to
        them. This means Fname1N.Ext1 will be copied to Fname2N.Ext2
        by all processes, where N is the Distributed ANSYS process
        rank.  For more information see Differences in General
        Behavior in the Parallel Processing Guide.
        """
        command = f"/COPY,{fname1},{ext1},,{fname2},{ext2},,{distkey}"
        return self.run(command, **kwargs)

    def fclean(self, **kwargs):
        """Deletes all local files in all processors in a distributed parallel processing run.

        APDL Command: /FCLEAN

        Deletes all local files (``.rst``, ``.esav``, ``.emat``, ``.mode``, ``.mlv``,
        ``.seld``, ``.dsub``, ``.ist``, ``.full``, ``.rdsp``, ``.rfrq``, ``.rnnn``,
        ``.resf``, ``.stat``, ``.modesym``, ``.osave``, ``.erot``, ``.log``)
        in all processors in a distributed parallel processing run.

        .. warning:: Because ``/FCLEAN`` deletes all local files, it should only be issued if you are sure that
           none of those files are needed in downstream analyses. Deleting files that are necessary for
           the next substep, load step, or analysis will prevent continuation of the run.

        Notes
        -----

        Issue ``/FCLEAN`` to delete all local files having the current Jobname (``/FILNAME``) and save
        disk space in a distributed parallel processing run. Like other file deletion commands, deletion happens
        immediately upon issuing this command. Different than other file deletion commands, it enables the
        convenience of deleting all ``Jobname.*`` local files without having to issue separate commands specifying
        each file type

        This command is valid only at the Begin Level.
        """
        return self.run("/FCLEAN", **kwargs)

    def fcomp(self, ident="", level="", **kwargs):
        """Specifies file compression level.

        Parameters
        ----------
        ident
            ANSYS file name identifier. Input the label RST to compress
            the following results files: .RST, .RSTP, .RTH, and .RMG. See
            File Management and Files for file descriptions.

        level
            Compression level. Valid input values are 0 (no compression -
            default) to 5 (maximum compression).

        Notes
        -----
        Command Default
        File compression is not performed.

        Specifies file compression for results files (.RST, .RSTP, .RTH,
        and .RMG files). Records are compressed as they are written and
        uncompressed as they are read (for example, by the SET command).

        See File Compression in the Basic Analysis Guide for more details.
        """
        return self.run(f"/FCOMP,{ident},{level}", **kwargs)

    def lgwrite(self, fname="", ext="", kedit="", remove_grpc_extra=True, **kwargs):
        """Writes the database command log to a file.

        APDL Command: LGWRITE

        Parameters
        ----------
        fname : str, optional
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

            The file name defaults to Jobname.

        ext : str, optional
            Filename extension (eight-character maximum).

        kedit : str, optional
            Flag to suppress nonessential commands:

            * ``"NONE"`` - Do not suppress any commands (default).
            * ``"COMMENT"`` - Write nonessential commands as comments (starting with !).
            * ``"REMOVE"`` - Do not write nonessential commands or comments.

        remove_grpc_extra : bool, default: True
            Remove gRPC related content (like ``/OUT,anstmp``). This will be
            ignored when MAPDL is not in gRPC mode.

        Notes
        -----
        Writes the database command log to a named file.  The database
        command log contains all commands that were used to create the
        current database.  These commands are recorded in the database
        as they are issued, and saved in the database file (File.DB)
        whenever the database is saved.  The LGWRITE command extracts
        these commands from the database and writes them to a file.
        Nonessential commands (for listing, graphics displays, help,
        etc.) can be excluded from the file by using the Kedit field.
        The file resulting from LGWRITE can be used as command input
        to the program.  This command is most useful if the session
        log file (File.LOG), which is normally saved during an
        interactive session, has been lost or corrupted.

        This command is valid in any processor.

        Examples
        --------
        Output the database command log to the local directory.

        >>> import os
        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 0, 0, mute=True)
        >>> mapdl.k(2, 2, 0, 0)
        >>> filename = os.path.join(os.getcwd(), 'log.txt')
        >>> mapdl.lgwrite(filename, kedit='REMOVE')

        Print the output from the log file.

        >>> with open(filename) as fid:
        ...     lines = fid.readlines()
        >>> print(''.join(lines))
        /BATCH
        /PREP7,
        K,1,0,0,0
        K,2,2,0,0

        """
        # always add extension to fname
        if ext:
            fname = fname + f".{ext}"

        # seamlessly deal with remote instances in gRPC mode
        target_dir = None
        is_grpc = "Grpc" in type(self).__name__
        if is_grpc and fname:
            if not self._local and os.path.basename(fname) != fname:
                target_dir, fname = os.path.dirname(fname), os.path.basename(fname)

        # generate the log and download if necessary
        output = self.run(f"LGWRITE,{fname},,,{kedit}", **kwargs)
        if not fname:
            # defaults to <jobname>.lgw
            fname = self.jobname + ".lgw"
        if target_dir is not None:
            self.download(fname, target_dir=target_dir)

        # remove extra grpc /OUT commands
        if remove_grpc_extra and is_grpc and target_dir:
            filename = os.path.join(target_dir, fname)
            with open(filename, "r") as fid:
                lines = [line for line in fid if not line.startswith("/OUT")]
            with open(filename, "w") as fid:
                fid.writelines(lines)

        return output

    def starlist(self, fname="", ext="", **kwargs):
        """Displays the contents of an external, coded file.

        APDL Command: ``*LIST``

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).  An
            unspecified directory path defaults to the working directory;
            in this case, you can use all 248 characters for the file
            name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Displays the contents of an external, coded file.  The file to be
        listed cannot be in use (open) at the time (except for the error
        file, File.ERR, which may be displayed with ``*LIST,ERR``).

        This command is valid in any processor.
        """
        command = f"*LIST,{fname},{ext}"
        return self.run(command, **kwargs)

    def rename(self, fname1="", ext1="", fname2="", ext2="", distkey="", **kwargs):
        """Renames a file.

        APDL Command: /RENAME

        Parameters
        ----------
        fname1
            The file to be renamed. You can also include an optional
            directory path as part of the specified file name; if not,
            the default file location is the working directory.

        ext1
            Filename extension (eight-character maximum).

        fname2
            The new name for the file. You can also include an
            optional directory path as part of the new file name; if
            not, the default is the working directory. A maximum of
            248 characters is allowed for the file name (or combined
            file name and directory path, if both are specified).

        ext2
            Filename extension (eight-character maximum).

        distkey
            Key that specifies whether the rename operation is
            performed on all processes in distributed parallel mode
            (Distributed ANSYS):

            1 (ON or YES) - The program performs the rename operation
            locally on each process.

            0 (OFF or NO) - The program performs the rename operation
            only on the master process (default).

        Notes
        -----
        Renames a file.  Ex: /RENAME,A,,,B renames file A to B in the
        same directory.  /RENAME,A,DAT,,,INP renames file A.DAT to
        A.INP. On all systems, this command will overwrite any
        existing file named B. See the Operations Guide for
        details. Only ANSYS binary files should be renamed. Use /SYS
        and system renaming commands for other files.

        In distributed parallel mode (Distributed ANSYS), only the
        master process will rename Fname1.Ext1 to Fname2.Ext2 by
        default. However, when DistKey is set to 1 (or ON or YES), the
        command is executed by all processes. In this case, Fname1 and
        Fname2 will automatically have the process rank appended to
        them. This means Fname1N.Ext1 will be renamed to Fname2N.Ext2
        by all processes, where N is the Distributed ANSYS process
        rank. For more information see Differences in General Behavior
        in the Parallel Processing Guide.

        Renaming across system partitions may be internally done by a
        copy and delete operation on some systems.

        This command is valid only at the Begin Level.
        """
        return self.run(
            f"/RENAME,{fname1},{ext1},,{fname2},{ext2},,{distkey}", **kwargs
        )

    def slashfdele(self, ident="", stat="", **kwargs):
        """Deletes a binary file after it is used.

        APDL Command: /FDELE

        Parameters
        ----------
        ident
            ANSYS file name identifier.  Valid identifiers are:  EMAT, ESAV,
            FULL, SUB, MODE, DSUB, USUB, OSAV, and SELD.  See the Basic
            Analysis Guide for file descriptions.

        stat
            Keep or delete key:

            KEEP - Keep this file.

            DELE - Delete (or do not write, if not necessary) this file.

        Notes
        -----
        Deletes as soon as possible (or prevents writing) a binary file created
        by the ANSYS program to save space.

        .. warning::
            Deleting files that are necessary for the next substep,
            load step, or analysis will prevent continuation of the
            run.

        This command is valid only at the Begin Level.
        """
        command = f"/FDELE,{ident},{stat}"
        return self.run(command, **kwargs)

    def slashdelete(self, fname="", ext="", distkey="", **kwargs):
        """Deletes a file.

        APDL Command: /DELETE

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        distkey
            Key that specifies whether the file deletion is performed
            on all processes in distributed parallel mode (Distributed
            ANSYS):

            1 (ON or YES) - The program performs the file deletion
            locally on each process.

            0 (OFF or NO) - The program performs the file deletion
            only on the master process (default).

        Notes
        -----
        In distributed parallel mode (Distributed ANSYS), only the
        master process will delete Fname.Ext by default. However, when
        DistKey is set to 1 (or ON or YES), the command is executed by
        all processes. In this case, Fname will automatically have the
        process rank appended to it.  This means FnameN.Ext will be
        deleted by all processes, where N is the Distributed ANSYS
        process rank. For more information see Differences in General
        Behavior in the Parallel Processing Guide.
        """
        return self.run(f"/DELETE,{fname},{ext},,{distkey}", **kwargs)
