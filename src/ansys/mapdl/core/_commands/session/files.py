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


class Files:

    def anstoaqwa(
        self,
        fname: str = "",
        vertaxis: str = "",
        gc: str = "",
        rho: str = "",
        hwl: str = "",
        diffkey: int | str = "",
        symxkey: int | str = "",
        symykey: int | str = "",
        **kwargs,
    ):
        r"""Creates an AQWA-LINE input file from the current Mechanical APDL model.

        Mechanical APDL Command: `ANSTOAQWA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANSTOAQWA.html>`_

        Parameters
        ----------
        fname : str
            AQWA file name. Defaults to :file:`Jobname`.

        vertaxis : str
            Axis in the vertical direction:

            * ``Y (or 2)`` - Global Y axis.

            * ``Z (or 3)`` - Global Z axis (default).

        gc : str
            Gravitational acceleration. Defaults to 9.81.

        rho : str
            Density of water. Defaults to 1025.0.

        hwl : str
            Waterline height in model coordinates. Defaults to 0.0.

        diffkey : int or str
            Diffracting model key:

            * ``0`` - Create a non-diffracting AQWA model.

            * ``1`` - Create a diffracting AQWA model (default).

        symxkey : int or str
            Key indicating if model is symmetric about the global XZ plane:

            * ``0`` - No symmetry about XZ plane (default).

            * ``1`` - Use symmetry about XZ plane. Only include (or select) half the model.

        symykey : int or str
            Key indicating if model is symmetric about the global YZ plane:

            * ``0`` - No symmetry about YZ plane (default).

            * ``1`` - Use symmetry about YZ plane. Only include (or select) half the model.

        Notes
        -----

        .. _ANSTOAQWA_notes:

        This command creates the input file ``Fname``.aqwa for the Ansys Aqwa Multi-Body Hydrodynamics
        System
        for diffraction analysis in AQWA-LINE from the model currently in the database, based on the
        currently selected set of elements. The selected set must only include the hull envelope; no
        internal structure should be selected.

        There should be a line of nodes defined at the waterline. Only those elements that are entirely
        below the waterline will be specified as diffracting. If there are no waterline nodes, there will be
        no diffracting elements at the waterline, which will severely reduce the accuracy of the diffraction
        analysis.

        The translator maps PLANE42, SHELL63, and ``SHELL181`` elements to PANELs, and maps PIPE16 and
        PIPE59 elements to TUBEs. It does not recognize any other element types. Any material or geometric
        properties can be used for the shell elements, as AQWA does not need any properties at all and the
        command does not use them. All the shell elements below the water must have their normals pointing
        outward.

        TUBE elements in AQWA have material density, outside diameter, wall thickness, added mass, and drag
        coefficients, so appropriate properties should be used in the Mechanical APDL model. PIPE59 elements
        can
        have added mass and damping coefficients; these will be written to the file. The Mechanical APDL
        program
        uses the inertia coefficient C M, whereas AQWA uses the added mass coefficient C A, where C M = (1 +
        C A ). This correction is made automatically.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        In AQWA the vertical axis is always the Z-axis. The command can convert a model built with either
        the Y or Z-axis vertical, but the X-axis must be horizontal and should preferably be along the
        fore/aft axis of the vessel. If the structure is symmetric and you wish to use the symmetry options,
        you must only select one half or one quarter of the model, as appropriate. If you model a complete
        vessel and specify X symmetry, the AQWA model will contain two sets of coincident elements.

        If you are working from a model created for a structural analysis, it will probably be necessary to
        remesh the model as the structural mesh is most likely finer than needed for a diffraction analysis.

        If you enter this command interactively (with the GUI active) and no data is provided for the
        command options, the application prompts you for their values.

        You must verify the completeness and accuracy of the data written.

        **AQWA-LINE Notes**

        .. _ANSTOAQWA_aqwa:

        The file will specify restart stages 1-2 only. It has no options except REST, so AQWA may fail if
        any of the elements are badly shaped.

        The total mass is obtained by integrating over the wetted surface area and adding the TUBE masses,
        so it should be reasonably accurate. However, the integration used is not as accurate as that in
        AQWA, so there may be a small difference between the weight and buoyancy, particularly if tubes
        represent a large portion of the model.

        The position of the CG is unknown. A point mass is placed at the water-line above the CB, but you
        should change this to the correct position.

        The moments of inertia are estimated based on the overall dimensions of the model and using standard
        formulae for a ship. You should change these to the correct values.

        The maximum frequency is calculated from the maximum side length of the underwater elements. The
        range of frequencies runs from 0.1 rad/s to the calculated maximum, in steps of 0.1 rad/s.

        The directions are in steps of 15° over a range that is determined by the symmetry you have
        specified, in accordance with the requirements of AQWA.
        """
        command = f"ANSTOAQWA,{fname},{vertaxis},{gc},{rho},{hwl},{diffkey},{symxkey},{symykey}"
        return self.run(command, **kwargs)

    def anstoasas(self, fname: str = "", key: int | str = "", **kwargs):
        r"""Creates an ASAS input file from the current Mechanical APDL model.

        Mechanical APDL Command: `ANSTOASAS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANSTOASAS.html>`_

        Parameters
        ----------
        fname : str
            ASAS file name. Defaults to :file:`Jobname`.

        key : int or str
            Key indicating type of file to produce:

            * ``0`` - ASAS file for use by Ansys Aqwa (no loads written). Creates the file ``Fname``.asas.

            * ``1`` - ASAS file (all data written, including loads). Creates the file ``Fname``.asas.

            * ``2`` - ASAS(NL) file. Creates the file ``Fname``.asnl.

        Notes
        -----

        .. _ANSTOASAS_notes:

        This command creates an input file for the Ansys Asas Finite Element Analysis System from the model
        and loads currently in the database, based on the currently selected set of elements. Most common
        structural element types are written, as well as sections (or real constants), materials, boundary
        conditions and loads, and solution and load step options.

        **Data Written**

        The following data is written:

        * :ref:`Solution control options <solconop>`

        * Nodes

        * :ref:`Elements <elemdat>`

        * :ref:`Material data <matdat>`

        * :ref:`Geometry data <geomdat>`

        * :ref:`Section data <sectdat>`

        * Mechanical APDL element components (ASAS sets)

        * :ref:`Boundary conditions <boundcon>`

        * :ref:`Loads <loadsasas>`

        * Added mass (via ``MASS21`` element)

        Details are provided in the following sections.

        Not all data is written. You must verify the completeness and accuracy of the data. Only loading at
        the current step is transferred; hence, no load step history is captured.

        .. _solconop:

        **Solution Control Options**

        The ASAS project name is defined as "Ansys".

        The solution control options are converted as follows:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        For conversion to ASAS(NL), the large displacement option is set based on :ref:`nlgeom`, final load
        solution time is set based on :ref:`time`, and sub-step times are set based on :ref:`deltim` or
        :ref:`nsubst` (assuming constant step size).

        .. _elemdat:

        **Element Data**

        If you intend to use the data only with AQWA-WAVE, only the elements that form the wetted surface
        are required. Selecting these elements before invoking the :ref:`anstoasas` command will improve
        performance. In order for AQWA-WAVE to identify the direction of the wave loading, all elements must
        be defined by nodes in a clockwise direction. For further information, refer to the AQWA-WAVE
        manual.

        The element types are converted as follows:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _anstoasas_fn1:

        Documentation for this archived element type appears in the `Feature Archive
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_arch/archlegacytheory.html>`_.

        .. _matdat:

        **Material Data**

        Linear isotropic material conversion is supported for ASAS and ASAS(NL).

        .. _geomdat:

        **Geometry Data**

        The following ASAS element geometry data is supported:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        For all beam elements, the third node position must be explicitly defined. If the position is not
        defined, the program generates an error code (-1) in the output file.

        .. _sectdat:

        **Section Data**

        No user sections are generated if AQWA-WAVE data is selected.

        The following sections are converted for ASAS and ASAS(NL):

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _boundcon:

        **Boundary Conditions**

        The following boundary conditions are converted for ASAS and ASAS(NL):

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _loadsasas:

        **Loads**

        No user loading is generated if AQWA-WAVE data is selected. However, a load case (number 1000) is
        automatically defined to identify the wetted surface of the elements for use by AQWA-WAVE based on
        the normal surface loads applied to the solid or shell elements.

        Pressure loads from ``SURF154`` elements are converted to equivalent nodal loads for ASAS. For AQWA-
        WAVE, the ``SURF154`` pressures are used to identify the wetted surface of the underlying elements.
        The following loads are converted for ASAS:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"ANSTOASAS,{fname},{key}"
        return self.run(command, **kwargs)

    def assign(
        self, ident: str = "", fname: str = "", ext: str = "", lgkey: str = "", **kwargs
    ):
        r"""Reassigns a file name to a Mechanical APDL file identifier.

        Mechanical APDL Command: `/ASSIGN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASSIGN.html>`_

        Parameters
        ----------
        ident : str
            Mechanical APDL file name identifier. Valid identifiers are: CMS, EMAT, EROT, ESAV, FULL, LN07,
            LN09, LN11, LN20, LN21, LN22, LN25, LN31, LN32, MODE, OSAV, RDSP, RFRQ, RMG, RST, RSTP, RTH,
            SELD, and SSCR. See `File Management and Files
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS18_9.html>`_

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name.

        ext : str
            Filename extension (eight-character maximum).

        lgkey : str
            Key to specify local or global file name control for the specified file identifier in a distributed-
            memory parallel processing run. For more information on local and global files, see File Handling Conventions in the `Parallel Processing Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_dan/HybParallel.html>`_.

            * ``BOTH`` - Reassign the file name for both the local and global files (default).

            * ``LOCAL`` - Reassign the file name for only the local files.

            * ``GLOBAL`` - Reassign the file name for only the global file.

        Notes
        -----

        .. _s-ASSIGN_notes:

        The reassignment of file names is valid only if it is done before the file is used. All file
        reassignments are retained (not cleared) even if the database is cleared ( ``/CLEAR`` ) or the
        Jobname is changed ( :ref:`filname` ). Assigned files may be overwritten. If file name arguments
        (``Fname``, ``Ext``, ``--``) are blank, the default Mechanical APDL assignment is restored. Use
        :ref:`seopt` for SUB files
        and :ref:`seexp` for DSUB files.

        This command is valid only at the Begin level.

        This command also checks to ensure that the path/file is valid and can be written by the user. If it
        is not valid, an error message will be returned. Ensure that the directory exists prior to using
        :ref:`assign` command.
        """
        command = f"/ASSIGN,{ident},{fname},{ext},,{lgkey}"
        return self.run(command, **kwargs)

    def copy(
        self,
        fname1: str = "",
        ext1: str = "",
        fname2: str = "",
        ext2: str = "",
        distkey: str = "",
        **kwargs,
    ):
        r"""Copies a file.

        Mechanical APDL Command: `/COPY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_COPY.html>`_

        Parameters
        ----------
        fname1 : str
            File name to be copied and its directory path (248 characters maximum for both file name and
            directory). If you do not specify a directory path, it will default to your working directory
            and you can use all 248 characters for the file name.

            The file name defaults to the current :file:`Jobname`.

        ext1 : str
            Filename extension (eight-character maximum).

        fname2 : str
            File name to be created and its directory path (248 characters maximum for both file name and
            directory). If you do not specify a directory path, it will default to your working directory
            and you can use all 248 characters for the file name.

            ``Fname2`` defaults to ``Fname1``.

        ext2 : str
            Filename extension (eight-character maximum). ``Ext2`` defaults to ``Ext1``.

        distkey : str
            Key that specifies which copy operation is performed on all processes in distributed-memory parallel
            mode :

            * ``0 (OFF or NO)`` - The program performs the copy operation only on the master process (default).

            * ``1 (ON or YES)`` - The program performs the copy operation locally on each process.

            * ``2 or BOTH`` - The program performs the copy operation for ``Fname``. ``Ext`` on the master
              process and for ``FnameN``. ``Ext`` on all processes.

        Notes
        -----

        .. _s-COPY_notes:

        The original file is untouched. Ex: :ref:`copy`,A,,,B copies file A to B in the same directory.
        :ref:`copy`,A,DAT,,,INP copies the file :file:`A.DAT` to :file:`A.INP`. See the `Operations Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_ for
        details. Mechanical APDL binary and ASCII files can be copied.

        In distributed-memory parallel (DMP) mode, only the master process will copy ``Fname1``. ``Ext1``
        to ``Fname2``. ``Ext2`` by default. However, when ``DistKey`` is set to 1 (or ON, or YES) or 2 (or
        BOTH), the command is executed by all processes. In this case, ``Fname1`` and ``Fname2`` will
        automatically have the process rank appended to them. This means ``Fname1N``. ``Ext1`` will be
        copied to ``Fname2N``. ``Ext2`` by all processes, where ``N`` is the DMP process rank. For more
        information see in the `Parallel Processing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_dan/HybParallel.html>`_.
        """
        command = f"/COPY,{fname1},{ext1},,{fname2},{ext2},,{distkey}"
        return self.run(command, **kwargs)

    def fclean(self, **kwargs):
        r"""Deletes all local files in all processors in a distributed parallel processing run.

        Mechanical APDL Command: `/FCLEAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FCLEAN_sl.html>`_

        Notes
        -----

        .. _s-FCLEAN_notes:

        Issue :ref:`fclean` to delete all local files having the current ``Jobname`` ( :ref:`filname` ) and
        save disk space in a distributed parallel processing run. Like other file deletion commands,
        deletion happens immediately upon issuing this command. Different than other file deletion commands,
        it enables the convenience of deleting all :file:`Jobname.\*` local files without having to issue
        separate commands specifying each file type.

        All :file:`.log` files except the master ( :file:`Jobname0.log` ) are deleted.

        .. warning::

            Because /FCLEAN deletes all local files, it should only be issued if you are sure that none of
            those files are needed in any downstream analyses. Deleting files that are necessary for
            subsequent substeps, load steps, commands, or analyses will prevent continuation of the run. For
            example, since the local files are combined into global files when you issue FINISH in the
            solution processor, issuing /FCLEAN before FINISH in /SOLU will result in a program crash.
        """
        command = "/FCLEAN"
        return self.run(command, **kwargs)

    def fcomp(self, ident: str = "", level: int | str = "", **kwargs):
        r"""Specifies file-compression options.

        Mechanical APDL Command: `/FCOMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FCOMP_sl.html>`_

        Parameters
        ----------
        ident : str
            Mechanical APDL file identifier. There is no default. Valid labels are:

            * ``RST`` - Results file.

            * ``DB`` - Database file.

            * ``RNNN`` - Restart file.

            * ``OSAV`` - File created during a nonlinear analysis that contains a copy of :file:`ESAV` file from
              the last converged substep.

        level : int or str
            Compression level:

            * ``SPARSE`` - Use a sparsification scheme for file compression (default).

            * ``0`` - No file compression occurs.

            * ``n`` - A zlib-based file compression occurs using level number ``n``, which ranges from 1 to 5.

        Notes
        -----

        .. _s-FCOMP_notes:

        Specifies file compression options for results files ( :file:`.rst`, :file:`.rstp`, :file:`.rth`,
        and :file:`.rmg` files), database files ( :file:`.db` and :file:`.rdb` ), certain restart files (
        :file:`.Rnnn` ), and the :file:`.osav` file created during a nonlinear analysis. (See `Program-
        Generated Files
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS18_4.html#aHXtsq2aaldm>`_
        :ref:`set` command or the :ref:`resume` command).

        For results files compressed using the sparsification scheme ( ``LEVEL`` = SPARSE, which is the
        default), use the ``*XPL`` command to uncompress the file. For third party tools that need to read
        the results file, use the method described in `Accessing Mechanical APDL Binary Files
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Hlp_P_INT2_1.html#intlargeintget>`_

        See in the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for more
        details.

        This command is valid only at the Begin Level.
        """
        command = f"/FCOMP,{ident},{level}"
        return self.run(command, **kwargs)

    def lgwrite(self, fname: str = "", ext: str = "", kedit: str = "", **kwargs):
        r"""Writes the database command log to a file.

        Mechanical APDL Command: `LGWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LGWRITE.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to LGW if ``Fname`` and
            ``Ext`` are blank.

        kedit : str
            Flag to suppress nonessential commands:

            * ``NONE`` - Do not suppress any commands (default).

            * ``COMMENT`` - Write nonessential commands as comments (starting with !).

            * ``REMOVE`` - Do not write nonessential commands or comments.

        Notes
        -----

        .. _LGWRITE_notes:

        Writes the database command log to a named file. The database command log contains all commands that
        were used to create the current database. These commands are recorded in the database as they are
        issued, and saved in the database file ( :file:`File.DB` ) whenever the database is saved. The
        :ref:`lgwrite` command extracts these commands from the database and writes them to a file.
        Nonessential commands (for listing, graphics displays, help, etc.) can be excluded from the file by
        using the ``Kedit`` field. The file resulting from :ref:`lgwrite` can be used as command input to
        the program. This command is most useful if the session log file ( :file:`File.LOG` ), which is
        normally saved during an interactive session, has been lost or corrupted.

        This command is valid in any processor.
        """
        command = f"LGWRITE,{fname},{ext},,{kedit}"
        return self.run(command, **kwargs)

    def slashclog(self, fname: str = "", ext: str = "", **kwargs):
        r"""Copies the session log file to a named file.

        Mechanical APDL Command: `/CLOG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CLOG_sl.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path to which the log file is to be copied (248 characters maximum,
            including directory). If you do not specify a directory path, it will default to your working
            directory and you can use all 248 characters for the file name.

        ext : str
            Filename extension (eight-character maximum).

        Notes
        -----

        .. _s-CLOG_notes:

        This command is valid in any processor, but only during an interactive run.
        """
        command = f"/CLOG,{fname},{ext}"
        return self.run(command, **kwargs)

    def slashdelete(self, fname: str = "", ext: str = "", distkey: str = "", **kwargs):
        r"""Deletes a file.

        Mechanical APDL Command: `/DELETE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DELETE_sl.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to the current
            :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum).

        distkey : str
            Key that specifies which file deletion action is performed on all processes in distributed-memory
            parallel mode:

            * ``0 (OFF or NO)`` - The program performs the file deletion only on the master process (default).

            * ``1 (ON or YES)`` - The program performs the file deletion locally on each process.

            * ``2 or BOTH`` - The program performs file deletion for ``Fname``. ``Ext`` on the master process
              and for ``FnameN``. ``Ext`` on all processes.

        Notes
        -----
        In distributed-memory parallel (DMP) mode, only the master process will delete ``Fname``. ``Ext``
        by default. However, when ``DistKey`` is set to 1 (or ON, or YES) or 2 (or BOTH), the command is
        executed by all processes. In this case, ``Fname`` will automatically have the process rank appended
        to it. This means ``FnameN``. ``Ext`` will be deleted by all processes, where ``N`` is the DMP
        process rank. For more information see in the `Parallel Processing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_dan/HybParallel.html>`_.
        """
        command = f"/DELETE,{fname},{ext},,{distkey}"
        return self.run(command, **kwargs)

    def slashfdele(self, ident: str = "", stat: str = "", **kwargs):
        r"""Deletes a binary file after it is used.

        Mechanical APDL Command: `/FDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FDELE_sl.html>`_

        Parameters
        ----------
        ident : str
            Mechanical APDL file name identifier. Valid identifiers are: EMAT, ESAV, FULL, SUB, MODE, DSUB,
            USUB, OSAV, and SELD. See the `Basic Analysis Guide
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for file
            descriptions.

        stat : str
            Keep or delete key:

            * ``KEEP`` - Keep this file.

            * ``DELE`` - Delete (or do not write, if not necessary) this file.

        Notes
        -----

        .. _s-FDELE_notes:

        Deletes as soon as possible (or prevents writing) a binary file created by Mechanical APDL to save
        space.

        .. warning::

            Deleting files that are necessary for the next substep, load step, or analysis will prevent
            continuation of the run.

        This command is valid only at the Begin level.
        """
        command = f"/FDELE,{ident},{stat}"
        return self.run(command, **kwargs)

    def slashrename(
        self,
        fname1: str = "",
        ext1: str = "",
        fname2: str = "",
        ext2: str = "",
        distkey: str = "",
        **kwargs,
    ):
        r"""Renames a file.

        Mechanical APDL Command: `/RENAME <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RENAME.html>`_

        Parameters
        ----------
        fname1 : str
            The file to be renamed. You can also include an optional directory path as part of the specified
            file name; if not, the default file location is the working directory.

            File name defaults to the current :file:`Jobname`.

        ext1 : str
            Filename extension (eight-character maximum).

        fname2 : str
            The new name for the file. You can also include an optional directory path as part of the new
            file name; if not, the default is the working directory. A maximum of 248 characters is allowed
            for the file name (or combined file name and directory path, if both are specified).

            ``Fname2`` defaults to ``Fname1``.

        ext2 : str
            Filename extension (eight-character maximum). ``Ext2`` defaults to ``Ext1``.

        distkey : str
            Key that specifies which rename operation is performed on all processes in distributed-memory
            parallel mode:

            * ``0 (OFF or NO)`` - The program performs the rename operation only on the master process
              (default).

            * ``1 (ON or YES)`` - The program performs the rename operation locally on each process.

            * ``2 or BOTH`` - The program performs the rename operation for ``Fname``. ``Ext`` on the master
              process and for ``FnameN``. ``Ext`` on all processes.

        Notes
        -----

        .. _s-RENAME_notes:

        Renames a file. Ex: :ref:`slashrename`,A,,,B renames file A to B in the same directory.
        :ref:`slashrename`,A,DAT,,,INP renames file A.DAT to A.INP. On all systems, this command will
        overwrite any existing file named B. See the `Operations Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_ for details. Only
        Mechanical APDL binary files should
        be renamed. Use :ref:`sys` and system renaming commands for other files.

        In distributed-memory parallel (DMP) mode, only the master process will rename ``Fname1``. ``Ext1``
        to ``Fname2``. ``Ext2`` by default. However, when ``DistKey`` is set to 1 (or ON, or YES) or 2 (or
        BOTH), the command is executed by all processes. In this case, ``Fname1`` and ``Fname2`` will
        automatically have the process rank appended to them. This means ``Fname1N``. ``Ext1`` will be
        renamed to ``Fname2N``. ``Ext2`` by all processes, where ``N`` is the DMP process rank. For more
        information see in the `Parallel Processing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_dan/HybParallel.html>`_.

        Renaming across system partitions may be internally done by a copy and delete operation on some
        systems.

        This command is valid only at the Begin level.
        """
        command = f"/RENAME,{fname1},{ext1},,{fname2},{ext2},,{distkey}"
        return self.run(command, **kwargs)

    def starlist(self, fname: str = "", ext: str = "", **kwargs):
        r"""Displays the contents of an external, coded file.

        Mechanical APDL Command: `\*LIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LIST_st.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name.

        ext : str
            Filename extension (eight-character maximum).

        Notes
        -----

        .. _a-LIST_notes:

        Displays the contents of an external, coded file. The file to be listed cannot be in use (open) at
        the time (except for the error file, :file:`Jobname.err` None, which may be displayed with
        :ref:`starlist`,ERR).

        Use caution when you are listing active Mechanical APDL files via the List> Files> Other and File>
        List>
        Other menu paths. File I/O buffer and system configurations can result in incomplete listings unless
        the files are closed.

        This command is valid in any processor.
        """
        command = f"*LIST,{fname},{ext}"
        return self.run(command, **kwargs)
