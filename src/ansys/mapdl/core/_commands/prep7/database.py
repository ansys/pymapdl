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


class Database:

    def aflist(self, **kwargs):
        r"""Lists the current data in the database.

        Mechanical APDL Command: `AFLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AFLIST.html>`_

        Notes
        -----

        .. _AFLIST_notes:

        Lists the current data and specifications in the database. If batch, lists all appropriate data. If
        interactive, lists only summaries.
        """
        command = "AFLIST"
        return self.run(command, **kwargs)

    def cdopt(self, option: str = "", **kwargs):
        r"""Specifies format to be used for archiving geometry.

        Mechanical APDL Command: `CDOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CDOPT.html>`_

        Parameters
        ----------
        option : str
            * ``IGES`` - Write solid model geometry information using IGES format (default).

            * ``ANF`` - Write solid model geometry information using Ansys Neutral File (ANF) format.

            * ``STAT`` - Print out the current format setting.

        Notes
        -----

        .. _CDOPT_notes:

        This command controls your solid model geometry format for :ref:`cdwrite` operations. The ANF option
        affects only the COMB and SOLID options of the :ref:`cdwrite` command. All other options remain
        unaffected.

        This option setting is saved in the database.
        """
        command = f"CDOPT,{option}"
        return self.run(command, **kwargs)

    def cdread(
        self,
        option: str = "",
        fname: str = "",
        ext: str = "",
        fnamei: str = "",
        exti: str = "",
        **kwargs,
    ):
        r"""Reads a file of solid model and database information into the database.

        Mechanical APDL Command: `CDREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CDREAD.html>`_

        Parameters
        ----------
        option : str
            Selects which data to read:

            * ``ALL`` - Read all geometry, material property, load, and component data (default). Solid model
              geometry and loads will be read from the file :file:`fnamei.exti`. All other data will be read from
              the file :file:`fname.ext.` None

            * ``DB`` - Read all database information contained in file :file:`Fname.Ext`. This file should
              contain all information mentioned above except the solid model loads. If reading a :file:`.CDB` file
              written with the GEOM option of the :ref:`cdwrite` command, element types ( :ref:`et` ) compatible
              with the connectivity of the elements on the file must be defined prior to reading.

            * ``SOLID`` - Read the solid model geometry and solid model loads from the file :file:`Fnamei.Exti`.
              This file could have been written by the :ref:`cdwrite` or :ref:`igesout` command.

            * ``COMB`` - Read the combined solid model and database information from the file :file:`Fname.Ext.`
              None

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to :file:`.cdb` if
            ``Fname`` is blank.

        fnamei : str
            Name of the IGES file and its directory path (248 characters maximum, including directory). If
            you do not specify a directory path, it will default to your working directory and you can use
            all 248 characters for the file name.

            The file name defaults to ``Fname``. Used only if ``Option`` = ALL or SOLID.

        exti : str
            Filename extension (eight-character maximum). Defaults to IGES if ``Fnamei`` is blank.

        Notes
        -----

        .. _CDREAD_notes:

        This command causes coded files of solid model (in IGES format) and database (in command format)
        information to be read. These files are normally written by the :ref:`cdwrite` or :ref:`igesout`
        command. Note that the active coordinate system in these files has been reset to Cartesian (
        :ref:`csys`,0).

        If a set of data exists prior to the :ref:`cdread` operation, that data set is offset upward to
        allow the new data to fit without overlap. The :ref:`nooffset` command allows this offset to be
        ignored on a set-by-set basis, causing the existing data set to be overwritten with the new data
        set.

        When you write the geometry data using the :ref:`cdwrite`,GEOM option, you use the :ref:`cdread`,DB
        option to read the geometry information.

        Using the :ref:`cdread`,COMB option will not write :ref:`numoff` commands to offset entity ID
        numbers if there is no solid model in the database.

        Multiple :file:`.cdb` file imports cannot have elements with real constants in one file and section
        definitions in another. The section attributes will override the real constant attributes. If you
        use :ref:`cdread` to import multiple CDB files, define all of the elements using only real
        constants, or using only section definitions. Combining real constants and section definitions is
        not recommended.

        If a radiosity mapping data file ( :file:`.rsm` file) was saved by the previous :ref:`cdwrite`
        command, that mapping file must be present in the directory along with the coded geometry file in
        order for radiosity surface elements ( ``SURF251``, ``SURF252`` ) to be correctly mapped onto the
        model when :ref:`cdread` is issued.

        If you issue :ref:`cdwrite` to import a :file:`.cdb` file containing a `user-defined element
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_USER300.html#user300prodrest>`_,
        manually insert :ref:`usrelem` and :ref:`usrdof` commands in the :file:`.cdb` file to provide the
        user-defined element characteristics. Insert the two commands after the :ref:`et` command (defining
        the user-defined element) and before the ``EBLOCK``  command. (If multiple element types are defined
        in the :file:`.cdb` file, insert the :ref:`type` command to select the user-defined element. Place
        it before  :ref:`usrelem` and :ref:`usrdof`.)

        This command is valid in any processor.
        """
        command = f"CDREAD,{option},{fname},{ext},,{fnamei},{exti}"
        return self.run(command, **kwargs)

    def cdwrite(
        self,
        option: str = "",
        fname: str = "",
        ext: str = "",
        fnamei: str = "",
        exti: str = "",
        fmat: str = "",
        **kwargs,
    ):
        r"""Writes geometry and load database items to a file.

        Mechanical APDL Command: `CDWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CDWRITE.html>`_

        Parameters
        ----------
            option
            Selects which data to write:

            ALL
            Write all appropriate geometry, material property,
            load, and component data (default). Two files will
            be produced. ``Fname.Ext`` will contain all data items
            mentioned in "Notes", except the solid model
            data. ``Fnamei.Exti`` will contain the solid model
            geometry and solid model loads data in the form of
            ``IGES`` commands. This option is not valid when
            ``CDOPT,ANF`` is active.

            COMB
            Write all data mentioned, but to a single file,
            ``Fname.Ext``. Solid model geometry data will be
            written in either ``IGES`` or ``ANF`` format as specified
            in the ``CDOPT`` command, followed by the remainder of
            the data in the form of ANSYS commands. More
            information on these (IGES/ANF) file formats is
            provided in "Notes".

            DB
            Write all database information except the solid model
            and solid model loads to ``Fname.Ext`` in the form of
            ANSYS commands. This option is not valid when
            ``CDOPT,ANF`` is active.

            SOLID
            Write only the solid model geometry and solid
            model load data. This output will be in IGES or
            ANF format, as specified in the ``CDOPT``
            command. More information on these (``IGES/ANF``) file
            formats is provided in "Notes".

            GEOM
            Write only element and nodal geometry data. Neither
            solid model geometry nor element attribute data
            will be written. One file, ``Fname.Ext``, will be
            produced. Use ``CDREAD,DB`` to read in a file written
            with this option. Element types [``ET``] compatible
            with the connectivity of the elements on the file
            must first be defined before reading the file in
            with ``CDREAD,DB``.

            CM
            Write only node and element component and geometry
            data to ``Fname.Ext``.

            MAT
            Write only material property data (both linear and
            nonlinear) to ``Fname.Ext``.

            LOAD
            Write only loads for current load step to
            ``Fname.Ext``.

            SECT
            Write only section data to ``Fname.Ext``. Pretension
            sections are not included.

            fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

            ext
            Filename extension (eight-character maximum).

            fnamei
            Name of the IGES file and its directory path (248
            characters maximum, including directory). If you do not
            specify a directory path, it will default to your working
            directory and you can use all 248 characters for the file
            name.

            exti
            Filename extension (eight-character maximum).

            fmat
            Format of the output file (defaults to BLOCKED).

            BLOCKED
            Blocked format. This format allows faster
            reading of the output file. The time savings is
            most significant when BLOCKED is used to read
            .cdb files associated with very large models.

            UNBLOCKED
            Unblocked format.

        Returns
        -------
        str
            Mapdl command output.

        Notes
        -----

        .. _CDWRITE_notes:

        Load data includes the current load step only. Loads applied to the solid model (if any) are
        automatically transferred to the finite element model when this command is issued. :ref:`cdwrite`
        writes out solid model loads for meshed models only. If the model is not meshed, the solid model
        loads cannot be saved. Component data include component definitions, but not assembly definitions.
        Appropriate :ref:`numoff` commands are included at the beginning of the file; this is to avoid
        overlap of an existing database when the file is read in.

        Solution control commands are typically not written to the file unless you specifically change a
        default solution setting.

        :ref:`cdwrite` does not support the :ref:`gsbdata` and :ref:`gsgdata` commands, and these commands
        are not written to the file.

        The data may be reread (on a different machine, for example) with the :ref:`cdread` command.
        Caution: When the file is read in, the :ref:`numoff`,MAT command may cause a mismatch between
        material definitions and material numbers referenced by certain loads and element real constants.
        See :ref:`numoff` for details. Also, be aware that the files created by the :ref:`cdwrite` command
        explicitly set the active coordinate system to Cartesian ( :ref:`csys`,0).

        You should generally use the blocked format ( ``Fmat`` = BLOCKED) when writing out model data with
        :ref:`cdwrite`. This is a compressed data format that greatly reduces the time required to read
        large models through the :ref:`cdread` command. The blocked and unblocked formats are described in
        `The CDWRITE (CDB) File Format
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Hlp_P_INT3_3.html>`_

        If you use :ref:`cdwrite` in any of the derived products (Ansys Mechanical Pro, Ansys Mechanical
        Premium), then before reading the
        file, you must edit the :file:`Jobname.cdb` file to remove commands that are not available in the
        respective component product.

        The :ref:`cdwrite` command does not support (for beam meshing) any line operation that relies on
        solid model associativity. For example, meshing the areas adjacent to the meshed line, plotting the
        line that contains the orientation nodes, or clearing the mesh from the line that contains
        orientation nodes may not work as expected. For more information about beam meshing, see `Meshing
        Your Solid Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_8.html>`_ in the
        `Modeling and Meshing Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD14.html>`_.

        If you issue :ref:`cdwrite` to write a :file:`.cdb` file containing a user-defined element, manually
        insert :ref:`usrelem` and :ref:`usrdof` commands in the :file:`.cdb` file to provide the user-
        defined element characteristics. Insert the two commands after the :ref:`et` command (defining the
        user-defined element) and before the ``EBLOCK``  command. (If multiple element types are defined in
        the :file:`.cdb` file, insert the :ref:`type` command to select the user-defined element. Place it
        before  :ref:`usrelem` and :ref:`usrdof`.)

        If radiosity surface elements ( ``SURF251`` or ``SURF252`` ) are present in the model, a radiosity
        mapping data file, :file:`Fname.RSM,` is also saved when the :ref:`cdwrite` command is issued. For
        more information, see `Advanced Radiosity Options
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THEadvrad.html#themultrsymm>`_

        *\*IGES and ANF File Formats for Solid Model Geometry Information**

        The format used for solid model geometry information is determined by the current :ref:`cdopt`
        command setting. The default format is IGES.

        IGES option (default) to write solid model information ( :ref:`cdopt`, IGS):

        * Before writing solid model entities, select all corresponding lower level entities (
          :ref:`allsel`,BELOW,ALL).

        * Section properties assigned to areas, lines and other solid model entities are not maintained when
          the model is exported.

        * If you issue :ref:`cdwrite` after generating a beam mesh with orientation nodes, the database file
          will contain all of the nodes for every beam element, including the orientation nodes; however,
          the orientation keypoints that were specified for the line ( :ref:`latt` ) are no longer
          associated with the line and won't be written out to the geometry file. All associativity between
          the line and the orientation keypoints is lost.

        * For beam meshing, this option does not support any line operation that relies on solid model
          associativity. For example, meshing the areas adjacent to the meshed line, plotting the line that
          contains the orientation nodes, or clearing the mesh from the line that contains orientation nodes
          may not work as expected.

        * Concatenated lines are not written. The line segments that make up the concatenated lines are
          written; however, if the command encounters an area that contains a concatenated line, the write
          operation halts (that area cannot be recreated during the read operation). If your model has areas
          that contain concatenated lines, you must first list these and then unconcatenate them before
          issuing the :ref:`cdwrite` command. Similarly, hardpoint information cannot be written.

        ANF option to write solid model information ( :ref:`cdopt`, ANF):

        * Writes all model information in the database (regardless of select status) to the archive file;
          however, when you restore the database using this archived file, the select status of entities is
          also restored.

        * Restores all line attributes, including orientation keypoints. It also writes out any components
          (not assemblies) that consist of solid model entities.

        * Halts :ref:`cdwrite` when a concatenated line or an area that contains a concatenated line is
          detected. You must delete the concatenated lines before issuing :ref:`cdwrite`. Similarly,
          hardpoint information cannot be written.

        This command is also valid in SOLUTION.

        Examples
        --------
        Create a basic block and save it to disk.

        >>> mapdl.prep7()
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.et(1, 186)
        >>> mapdl.esize(0.25)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.cdwrite('DB', '/tmp/mesh.cdb')
        TITLE =
        NUMBER OF ELEMENT TYPES =      1
        64 ELEMENTS CURRENTLY SELECTED.  MAX ELEMENT NUMBER =   64
        425 NODES CURRENTLY SELECTED.     MAX NODE NUMBER =     425
        8 KEYPOINTS CURRENTLY SELECTED. MAX KEYPOINT NUMBER =   8
        12 LINES CURRENTLY SELECTED.     MAX LINE NUMBER =      12
        6 AREAS CURRENTLY SELECTED.     MAX AREA NUMBER =       6
        1 VOLUMES CURRENTLY SELECTED.   MAX VOL. NUMBER =       1
        WRITE ANSYS DATABASE AS AN ANSYS INPUT FILE: /tmp/mesh.cdb

        Optionally load the mesh into Python using the archive reader.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> mesh = pymapdl_reader.Archive('/tmp/mesh.cdb')
        >>> mesh
        ANSYS Archive File mesh.cdb
        Number of Nodes:              425
        Number of Elements:           64
        Number of Element Types:      1
        Number of Node Components:    0
        Number of Element Components: 0
        """
        command = f"CDWRITE,{option},'{fname}',{ext},,{fnamei},{exti},{fmat}"
        return self.run(command, **kwargs)

    def cecheck(self, itemlab: str = "", tolerance: str = "", dof: str = "", **kwargs):
        r"""Check constraint equations and couplings for rigid body motions.

        Mechanical APDL Command: `CECHECK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CECHECK.html>`_

        Parameters
        ----------
        itemlab : str
            Item indicating what is to be checked:

            * ``CE`` - Check constraint equations only

            * ``CP`` - Check couplings only

            * ``ALL`` - Check both CE and CP

        tolerance : str
            Allowed amount of out-of-balance for any constraint equation or coupled set. The default value
            of 1.0e-6 is usually good.

        dof : str
            Specifies which DOF is to be checked. Default is RIGID, the usual option. Other choices are
            individual DOF such as UX, ROTZ, etc. or THERM. The THERM option will check the constraint
            equations or coupled sets for free thermal expansions, whereas the individual DOFs check under
            rigid body motions. ALL is RIGID and THERM.

        Notes
        -----

        .. _CECHECK_notes:

        This command imposes a rigid body motion on the nodes attached to the constraint equation or coupled
        set and makes sure that no internal forces are generated for such rigid body motions. Generation of
        internal forces by rigid body motions usually indicates an error in the equation specification
        (possibly due to nodal coordinate rotations). The THERM option does a similar check to see that no
        internal forces are created by the equations if the body does a free thermal expansion (this check
        assumes a single isotropic coefficient of expansion).
        """
        command = f"CECHECK,{itemlab},{tolerance},{dof}"
        return self.run(command, **kwargs)

    def check(self, sele: str = "", levl: str = "", **kwargs):
        r"""Checks current database items for completeness.

        Mechanical APDL Command: `CHECK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CHECK.html>`_

        Parameters
        ----------
        sele : str
            Specifies which elements are to be checked:

            * ``(blank)`` - Check all data.

            * ``ESEL`` - Check only elements in the selected set and unselect any elements not producing
              geometry check messages. The remaining elements (those producing check messages) can then be
              displayed and corrected. A null set results if no elements produce a message. Issue :ref:`esel`,ALL
              to select all elements before proceeding.

        levl : str
            Used only with ``Sele`` = ESEL:

            * ``WARN`` - Select elements producing warning and error messages.

            * ``ERR`` - Select only elements producing error messages (default).

        Notes
        -----

        .. _CHECK_notes:

        This command will not work if :ref:`shpp`,OFF has been set. A similar, automatic check of all data
        is done before the solution begins.

        If the Check Elements option is invoked through the GUI (menu path Main Menu> Preprocessor> Meshing>
        Check Elems ), the :ref:`check`,ESEL logic is used to highlight elements in the following way: good
        elements are blue, elements having warnings are yellow, and bad (error) elements are red. The
        currently selected set of elements is not changed by this GUI function.

        This command is also valid in PREP7.
        """
        command = f"CHECK,{sele},{levl}"
        return self.run(command, **kwargs)

    def cncheck(
        self,
        option: str = "",
        rid1: str = "",
        rid2: str = "",
        rinc: str = "",
        intertype: str = "",
        trlevel: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        **kwargs,
    ):
        r"""Provides and/or adjusts the initial status of contact pairs.

        Mechanical APDL Command: `CNCHECK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CNCHECK.html>`_

        Parameters
        ----------
        option : str
            Option to be performed:

            * ``DETAIL`` - List all contact pair properties (default).

            * ``SUMMARY`` - List only the open/closed status for each contact pair.

            * ``POST`` - Execute a partial solution to write the initial contact configuration to the
              :file:`jobname.rcn` file.

            * ``ADJUST`` - Physically move contact nodes to the target in order to close a gap or reduce
              penetration. The initial adjustment is converted to structural displacement values (UX, UY, UZ) and
              stored in the :file:`jobname.rcn` file.

            * ``MORPH`` - Physically move contact nodes to the target in order to close a gap or reduce
              penetration, and also morph the underlying solid mesh. The initial adjustment of contact nodes and
              repositioning of solid element nodes due to mesh morphing are converted to structural displacement
              values (UX, UY, UZ) and stored in the :file:`jobname.rcn` file.

            * ``TADJUST`` - Physically move target body to the contact surface in order to close a gap or reduce
              penetration. The initial adjustment is converted to structural displacement values (UX, UY, UZ) and
              stored in the :file:`jobname.rcn` file.

            * ``RESET`` - Reset target element and contact element key options and real constants to their
              default values. This option is not valid for general contact.

            * ``AUTO`` - Automatically sets certain real constants and key options to recommended values or
              settings in order to achieve better convergence based on overall contact pair behaviors. This option
              is not valid for general contact.

            * ``TRIM`` - Trim contact pair (remove certain contact and target elements).

            * ``UNSE`` - Unselect certain contact and target elements.

            * ``SPLIT`` - Split base (original) contact pairs into smaller sub-pairs at the preprocessing (
              :ref:`prep7` ) level. The main intent of this option is to achieve better scalability in a
              distributed-memory parallel (DMP) run. The splitting operation may create additional overlapping
              contact elements at the split boundaries. Contact pairs can only be split once; repeated use of this
              option results in no further splitting for those contact pairs already split.

            * ``DMP`` - This option is similar to the SPLIT, but it is more automatic and contact pair splitting
              is done at the solution level ( :ref:`solve` ) of the first load step, not at the preprocessing
              level. This option is activated only in a distributed-memory parallel (DMP) run. For this option,
              ``TRlevel`` and ``InterType`` are valid; all other arguments are ignored.

            * ``MERGE`` - Merge all contact sub-pairs that were previously split (by prior ``Option`` = SPLIT or
              DMP operations) back to their original pairs. Any contact and target elements deleted due to the
              trim logic of the splitting operation cannot be recovered by the MERGE operation. All other
              arguments are ignored.

        rid1 : str
            The meanings of ``RID1``, ``RID2``, and ``RINC`` vary depending on the contact type or the
            ``Option`` specified, as described below. ``RID1`` accepts tabular input for some ``Option`` values.
            ``RID1``, ``RID2``, ``RINC`` are ignored when ``Option`` = DMP.

            Pair-Based Contact For pair-based contact, the range of real constant pair IDs for which ``Option`` will be performed.
            If ``RID2`` is not specified, it defaults to ``RID1``. If no value is specified, all contact pairs
            in the selected set of elements are considered.

            General Contact For general contact ( ``InterType`` = GCN), ``RID1`` and ``RID2`` are section IDs associated with
            general contact surfaces instead of real constant IDs. If ``RINC`` = 0, the ``Option`` is performed
            between the two sections, ``RID1`` and ``RID2``. If ``RINC >`` 0, the ``Option`` is performed among
            all specified sections ( ``RID1`` to ``RID2`` with increment of ``RINC`` ).

            Contact Splitting For contact splitting at the preprocessing level ( ``Option`` = SPLIT only), ``RID1``, ``RID2``, and ``RINC`` are used as follows:

            * If ``RID1``, ``RID2``, and ``RINC`` are non-zero and positive, split the contact pairs from real
              constant pair ID number ``RID1`` to ``RID2`` in increments of ``RINC``. In this case, if
              ``TRlevel`` is non-zero, it will only be applied to these specified pairs.

            * If ``RID1`` is zero or blank, ``TRlevel`` will take affect for all contact pairs in the model from
              largest to smallest.

            * If ``RID1``, ``RID2``, ``RINC``, and ``TRlevel`` are not defined, the program automatically
              determines the number of sub-pairs for splitting each contact pair.

            Tabular Input for ``RID1``  ``RID1`` accepts tabular input in the form of a 2D array when ``Option`` = ADJUST, MORPH or TADJUST.
            In this case, ``RID2``, ``RINC``, ``Val1``, ``Val2``, and ``Val3`` are ignored. For more
            information, see `Physically Moving Contact Nodes Toward the Target Surface
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_realkey.html#ctec_adjlrggap>`_

        rid2 : str
            The meanings of ``RID1``, ``RID2``, and ``RINC`` vary depending on the contact type or the
            ``Option`` specified, as described below. ``RID1`` accepts tabular input for some ``Option`` values.
            ``RID1``, ``RID2``, ``RINC`` are ignored when ``Option`` = DMP.

            Pair-Based Contact For pair-based contact, the range of real constant pair IDs for which ``Option`` will be performed.
            If ``RID2`` is not specified, it defaults to ``RID1``. If no value is specified, all contact pairs
            in the selected set of elements are considered.

            General Contact For general contact ( ``InterType`` = GCN), ``RID1`` and ``RID2`` are section IDs associated with
            general contact surfaces instead of real constant IDs. If ``RINC`` = 0, the ``Option`` is performed
            between the two sections, ``RID1`` and ``RID2``. If ``RINC >`` 0, the ``Option`` is performed among
            all specified sections ( ``RID1`` to ``RID2`` with increment of ``RINC`` ).

            Contact Splitting For contact splitting at the preprocessing level ( ``Option`` = SPLIT only), ``RID1``, ``RID2``, and ``RINC`` are used as follows:

            * If ``RID1``, ``RID2``, and ``RINC`` are non-zero and positive, split the contact pairs from real
              constant pair ID number ``RID1`` to ``RID2`` in increments of ``RINC``. In this case, if
              ``TRlevel`` is non-zero, it will only be applied to these specified pairs.

            * If ``RID1`` is zero or blank, ``TRlevel`` will take affect for all contact pairs in the model from
              largest to smallest.

            * If ``RID1``, ``RID2``, ``RINC``, and ``TRlevel`` are not defined, the program automatically
              determines the number of sub-pairs for splitting each contact pair.

            Tabular Input for ``RID1``  ``RID1`` accepts tabular input in the form of a 2D array when ``Option`` = ADJUST, MORPH or TADJUST.
            In this case, ``RID2``, ``RINC``, ``Val1``, ``Val2``, and ``Val3`` are ignored. For more
            information, see `Physically Moving Contact Nodes Toward the Target Surface
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_realkey.html#ctec_adjlrggap>`_

        rinc : str
            The meanings of ``RID1``, ``RID2``, and ``RINC`` vary depending on the contact type or the
            ``Option`` specified, as described below. ``RID1`` accepts tabular input for some ``Option`` values.
            ``RID1``, ``RID2``, ``RINC`` are ignored when ``Option`` = DMP.

            Pair-Based Contact For pair-based contact, the range of real constant pair IDs for which ``Option`` will be performed.
            If ``RID2`` is not specified, it defaults to ``RID1``. If no value is specified, all contact pairs
            in the selected set of elements are considered.

            General Contact For general contact ( ``InterType`` = GCN), ``RID1`` and ``RID2`` are section IDs associated with
            general contact surfaces instead of real constant IDs. If ``RINC`` = 0, the ``Option`` is performed
            between the two sections, ``RID1`` and ``RID2``. If ``RINC >`` 0, the ``Option`` is performed among
            all specified sections ( ``RID1`` to ``RID2`` with increment of ``RINC`` ).

            Contact Splitting For contact splitting at the preprocessing level ( ``Option`` = SPLIT only), ``RID1``, ``RID2``, and ``RINC`` are used as follows:

            * If ``RID1``, ``RID2``, and ``RINC`` are non-zero and positive, split the contact pairs from real
              constant pair ID number ``RID1`` to ``RID2`` in increments of ``RINC``. In this case, if
              ``TRlevel`` is non-zero, it will only be applied to these specified pairs.

            * If ``RID1`` is zero or blank, ``TRlevel`` will take affect for all contact pairs in the model from
              largest to smallest.

            * If ``RID1``, ``RID2``, ``RINC``, and ``TRlevel`` are not defined, the program automatically
              determines the number of sub-pairs for splitting each contact pair.

            Tabular Input for ``RID1``  ``RID1`` accepts tabular input in the form of a 2D array when ``Option`` = ADJUST, MORPH or TADJUST.
            In this case, ``RID2``, ``RINC``, ``Val1``, ``Val2``, and ``Val3`` are ignored. For more
            information, see `Physically Moving Contact Nodes Toward the Target Surface
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_realkey.html#ctec_adjlrggap>`_

        intertype : str
            The type of contact interface ( `pair-based versus general contact
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_comppairgen.html#gcfeatnotsup>`_
            ) to be considered; or the type of contact pair to be trimmed/unselected/auto-set.

            The following labels specify the type of contact interface:

            * ``(blank)`` - Include all contact definitions (pair-based and general contact).

            * ``GCN`` - Include general contact definitions only (not valid when ``Option`` = RESET or AUTO).

            The following labels specify the type of contact pairs to be trimmed/unselected/auto-set (used only
            when ``Option`` = TRIM, UNSE, or AUTO, and only for pair-based contact definitions):

            * ``ANY`` - All types (default).

            * ``MPC`` - MPC-based contact pairs (KEYOPT(2) = 2).

            * ``BOND`` - Bonded contact pairs (KEYOPT(12) = 3, 5, 6).

            * ``NOSP`` - No separation contact pairs (KEYOPT(12) = 2, 4).

            * ``SMAL`` - Small sliding contact pairs (KEYOPT(18) = 1).

            * ``SELF`` - Self contact pairs (target surface completely overlaps contact surface).

            * ``INAC`` - Inactive contact pairs (symmetric contact pairs for MPC contact or KEYOPT(8) = 2).

            The following labels specify the type of contact pairs to be trimmed only when ``Option`` = SPLIT or DMP, and only for pair-based contact definitions:

            * ``(blank)`` - The program automatically deletes inactive contact pairs defined by auto-asymmetric
              selection (KEYOPT(8) = 2). If ``Option`` = DMP, the program also trims split contact pairs that are
              associated with bonded contact (KEYOPT(12) = 5 or 6) or small sliding contact (KEYOPT(18) = 1).

            * ``TRIM`` - The program automatically deletes inactive contact pairs defined by auto-asymmetric
              selection (KEYOPT(8) = 2), and also trims all split contact pairs.

        trlevel : str
            This argument is either the trimming level for trimming contact pairs or the number of sub-pairs for
            contact splitting.

            Trimming level (used only when ``Option`` = TRIM, UNSE, or MORPH):

            * ``(blank)`` - Normal trimming (default): remove/unselect contact and target elements which are in
              far-field.

            * ``AGGRE`` - Aggressive trimming: remove/unselect contact and target elements which are in far-
              field, and certain elements in near-field.

            Number of sub-pairs used for contact splitting (used only when ``Option`` = SPLIT or DMP):

            * ``(blank)`` - The program automatically chooses the number of sub-pairs for splitting in order to
              achieve better scalability in a DMP run.

            * ``N`` - Input a non-zero positive number to indicate the maximum number of sub-pairs for splitting
              the largest contact pair in the model. All other smaller contact pairs will be split following this
              number proportionally. The number you input may not always be honored; splitting may results in a
              fewer number of sub-pairs basing on many factors

        val1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CNCHECK.html>`_ for
            further information.

        val2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CNCHECK.html>`_ for
            further information.

        val3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CNCHECK.html>`_ for
            further information.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CNCHECK.html>`_
           for further explanations.

        .. _CNCHECK_notes:

        The :ref:`cncheck` command provides information for surface-to-surface, node-to-surface, and line-
        to-line contact pairs (element types ``TARGE169``, ``TARGE170``, ``CONTA172``, ``CONTA174``,
        ``CONTA175``, ``CONTA177`` ). All contact and target elements of interest, along with the solid
        elements and nodes attached to them, must be selected for the command to function properly. For
        performance reasons, the program uses a subset of nodes and elements based on the specified contact
        regions ( ``RID1``, ``RID2``, ``RINC`` ) when executing the :ref:`cncheck` command.

        :ref:`cncheck` is available in both the PREP7 and SOLUTION processors, but only before the first
        solve operation (that is, only before the first load step or the first substep).

        If the contact and target elements were generated through mesh commands ( :ref:`amesh`,
        :ref:`lmesh`, etc.) instead of the :ref:`esurf` command, you must issue :ref:`modmsh`,DETACH before
        :ref:`cncheck`. Otherwise, :ref:`cncheck` will not work correctly.

        The following additional notes are available:

        The command :ref:`cncheck`,POST solves the initial contact configuration in one substep. After
        issuing this command, you can postprocess the contact result items as you would for any other
        converged load step; however, only the contact status, contact penetration or gap, and contact
        pressure will have meaningful values. Other contact quantities (friction stress, sliding distance,
        chattering) will be available but are not useful.

        In order to report the real geometric penetration and gap, the program internally sets KEYOPT(9) = 0
        during the execution of :ref:`cncheck`,POST.

        Because ``Option`` = POST forces a solve operation, the PrepPost (PP) license does not work with
        :ref:`cncheck`,POST.

        If :ref:`cncheck`,POST is issued within the solution processor, the :ref:`solve` command that solves
        the first load step of your analysis should appear in a different step, as shown in the following
        example:

        .. code:: apdl

           /SOLU
           CNCHECK,POST
           FINISH
           ...

           /SOLU
           SOLVE
           FINISH
           ...

        :ref:`cncheck`,POST writes initial contact results to a file named :file:`jobname.rcn`. When
        postprocessing the initial contact state, you need to explicitly read results from this file using
        the :ref:`file` and :ref:`set`,FIRST commands in POST1 to properly read the corresponding contact
        data. Otherwise, the results may be read improperly. The following example shows a valid command
        sequence for plotting the initial contact gap:

        .. code:: apdl

           /SOLU
           CNCHECK,POST
           FINISH
           /POST1
           FILE,Jobname,RCN
           SET,FIRST
           PLNSOL,CONT,GAP,0,1
           FINISH
           ...

        You can issue :ref:`cncheck`,ADJUST to physically move contact nodes to the target surface.
        Alternatively, you can issue :ref:`cncheck`,MORPH to physically move contact nodes to the target
        surface and then morph the underlying mesh to improve the mesh quality. See `Physically Moving
        Contact Nodes Toward the Target Surface
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_realkey.html#ctec_adjlrggap>`_
        :ref:`cncheck`,ADJUST or :ref:`cncheck`,MORPH is issued within the solution processor, the
        :ref:`solve` command that solves the first load step of your analysis should appear in a different
        step:

        .. code:: apdl

           /SOLU
           CNCHECK,ADJUST
           FINISH
           ...

           /SOLU
           SOLVE
           FINISH
           ...

        After issuing the :ref:`cncheck`,ADJUST command, the initial adjustment is converted to structural
        displacement values (UX, UY, UZ) and stored in a file named :file:`jobname.rcn`. Similarly, the
        :ref:`cncheck`,MORPH command converts the initial adjustment of contact nodes as well as the
        morphing adjustment of solid element nodes to structural displacement values (UX, UY, UZ) and stores
        them in the :file:`jobname.rcn` file. You can use this file to plot or list nodal adjustment vectors
        or create a contour plot of the adjustment magnitudes via the displacements. When postprocessing the
        nodal adjustment values, you need to explicitly read results from this file using the :ref:`file`
        and :ref:`set`,FIRST commands in POST1 to properly read the corresponding contact data. Otherwise,
        the results may be read improperly.

        The :file:`jobname.rcn` file contains information generated from the :ref:`cncheck`,POST,
        :ref:`cncheck`,ADJUST, :ref:`cncheck`,MORPH, or :ref:`cncheck`, TADJUST command. If multiple
        commands are issued in the same analysis, the file is overwritten by the last :ref:`cncheck`
        command.

        You can issue :ref:`cncheck`,TADJUST to physically move the target body to the contact surface. This
        command tries to establish initial contact with penetration in a range specified by ``PMAX`` and
        ``PMIN``. Similar to the ADJUST and MORPH options, the initial adjustment is converted to structural
        displacement values (UX, UY, UZ) and stored in the :file:`jobname.rcn` file. This option accepts
        tabular input in the ``RID1`` field.

        You can specify either a positive or negative value for ``PMIN`` and ``PMAX``. The program
        interprets a positive value as a scaling factor and interprets a negative value as the absolute
        value.

        For more information, see `Physically Moving the Target Body Toward the Contact Surface
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_realkey.html#>`_

        The command :ref:`cncheck`,RESET allows you to reset all but a few key options and real constants
        associated with the specified contact pairs ( ``RID1``, ``RID2``, ``RINC`` ) to their default
        values. This option is only valid for pair-based contact definitions.

        The following key options and real constants remain unchanged when this command is issued:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        The command :ref:`cncheck`,AUTO automatically changes certain default or undefined key options and
        real constants to optimized settings or values. The changes are based on overall contact pair
        behaviors. In general, this command improves convergence for nonlinear contact analysis. This option
        is only valid for pair-based contact definitions.

        The tables below list typical KEYOPT and real constant settings implemented by :ref:`cncheck`,AUTO.
        The actual settings implemented for your specific model may vary from what is described here. You
        should always verify the modified settings by issuing :ref:`cncheck`,DETAIL to list current contact
        pair properties.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _AUTO_keyopts_ft_1:

        Set to 0 if KEYOPT(2) > 1 for debonding.

        .. _AUTO_keyopts_ft_2:

        Set to 1 if underlying elements are superelements, or if KEYOPT(9) = 2 was previously specified.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _AUTO_real_ft_1:

        PINB default depends on contact behavior (rigid vs. flexible target), :ref:`nlgeom`,ON or OFF,
        KEYOPT(9) setting, KEYOPT(12) setting, and the value of real constant CNOF (see ).

        :ref:`cncheck`,AUTO also sets :ref:`pred`,OFF for the case of a `force-distributed constraint
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_surfcon.html#strbeamso1703>`_
        defined via `MPC contact
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_restmpc.html>`_.

        You can issue :ref:`cncheck`,TRIM or :ref:`cncheck`,UNSEL to remove or unselect contact and target
        elements which are in far-field (that is, open and not near contact), or even in near-field if
        aggressive trimming logic is used ( ``TRlevel`` = AGGRE).

        The SPLIT, DMP, and MERGE options are intended for use in a distributed-memory parallel (DMP) run.
        Use the command :ref:`cncheck`,SPLIT or :ref:`cncheck`,DMP to split large contact pairs into
        smaller sub-pairs so that the smaller contact pairs can be distributed into different cores, thereby
        improving performance. This functionality is not the same as manually splitting contact pairs during
        the modeling process. The program splitting logic performs the necessary exchange of data on the
        boundaries between the split contact pairs to ensure that the results with and without splitting are
        essentially identical.

        The command :ref:`cncheck`,MERGE can be used to merge the sub-pairs together again, which is useful
        for postprocessing the contact results based on the original contact pair geometry. However, caution
        must be taken when a downstream analysis is performed since the MERGE operation may alter the
        database.

        For more information, see `Solving Large Contact Models in a Distributed-Memory Parallel Environment
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctecsplitting.html#ctecsplitlimit>`_
        """
        command = f"CNCHECK,{option},{rid1},{rid2},{rinc},{intertype},{trlevel},{val1},{val2},{val3}"
        return self.run(command, **kwargs)

    def escheck(self, sele: str = "", levl: str = "", defkey: int | str = "", **kwargs):
        r"""Perform element shape checking for a selected element set.

        Mechanical APDL Command: `ESCHECK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ESCHECK.html>`_

        Parameters
        ----------
        sele : str
            Specifies whether to select elements for checking:

            * ``(blank)`` - List all warnings/errors from element shape checking.

            * ``ESEL`` - Select the elements based on the. ``Levl`` criteria specified below.

        levl : str

            * ``WARN`` - Select elements producing warning and error messages.

            * ``ERR`` - Select only elements producing error messages (default).

        defkey : int or str
            Specifies whether check should be performed on deformed element shapes.

            * ``0`` - Do not update node coordinates before performing shape checks (default).

            * ``1`` - Update node coordinates using the current set of deformations in the database.

        Notes
        -----

        .. _ESCHECK_notes:

        Shape checking will occur according to the current :ref:`shpp` settings. Although :ref:`escheck` is
        valid in all processors, ``Defkey`` uses the current results in the database. If no results are
        available a warning will be issued.

        This command is also valid in PREP7, SOLUTION and POST1.
        """
        command = f"ESCHECK,{sele},{levl},{defkey}"
        return self.run(command, **kwargs)

    def igesout(self, fname: str = "", ext: str = "", att: int | str = "", **kwargs):
        r"""Writes solid model data to a file in IGES Version 5.1 format.

        Mechanical APDL Command: `IGESOUT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_IGESOUT.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to IGES if ``Fname`` is
            blank.

        att : int or str
            Attribute key:

            * ``0`` - Do not write assigned numbers and attributes of the solid model entities to the IGES file
              (default).

            * ``1`` - Write assigned numbers and attributes of solid model entities (keypoints, lines, areas,
              volumes) to the IGES file. Attributes include MAT, TYPE, REAL, and ESYS specifications as well as
              associated solid model loads and meshing (keypoint element size, number of line divisions and
              spacing ratio) specifications.

        Notes
        -----

        .. _IGESOUT_notes:

        Causes the selected solid model data to be written to a coded file in the IGES Version 5.1 format.
        Previous data on this file, if any, are overwritten.

        Keypoints that are not attached to any line are written to the output file as IGES entity 116
        (Point).

        Lines that are not attached to any area are written to the output file as either IGES Entity 100
        (Circular Arc), 110 (Line), or 126 (Rational B-Spline Curve) depending upon whether the Mechanical
        APDL
        entity was defined as an arc, straight line, or spline.

        Areas are written to the output file as IGES Entity 144 (Trimmed Parametric Surface).

        Volumes are written to the output file as IGES entity 186 (Manifold Solid B-Rep Object).

        Solid model entities to be written must have all corresponding lower level entities selected (use
        :ref:`allsel`,BELOW,ALL) before issuing command.

        Concatenated lines and areas are not written to the IGES file; however, the entities that comprise
        the concatenated entities are written.

        .. warning::

            Section properties assigned to areas, lines and other solid model entities are not maintained
            when the model is exported via IGESOUT. Issuing IGESOUT after generating a beam mesh with
            orientation nodes causes the orientation keypoints specified for the line ( LATT ) to no longer
            be associated with the line and are therefore not written out to the IGES file. The line does
            not recognize that orientation keypoints were ever assigned to it. Therefore, IGESOUT does not
            support (for beam meshing) any line operation relying on solid model associativity. (For
            example, meshing the areas adjacent to the meshed line, plotting the line that contains the
            orientation nodes, or clearing the mesh from the line that contains orientation nodes may not
            work as expected.) For more information about beam meshing, see Meshing Your Solid Model.
        """
        command = f"IGESOUT,{fname},{ext},,{att}"
        return self.run(command, **kwargs)

    def nooffset(self, label: str = "", **kwargs):
        r"""Prevents the :ref:`cdread` command from offsetting specified data items

        Mechanical APDL Command: `NOOFFSET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NOOFFSET.html>`_

        Parameters
        ----------
        label : str
            Specifies items not to be offset.

            * ``NODE`` - Node numbers

            * ``ELEM`` - Element numbers

            * ``KP`` - Keypoint numbers

            * ``LINE`` - Line numbers

            * ``AREA`` - Area numbers

            * ``VOLU`` - Volume numbers

            * ``MAT`` - Material numbers

            * ``TYPE`` - Element type numbers

            * ``REAL`` - Real constant numbers

            * ``CSYS`` - Coordinate system numbers

            * ``SECN`` - Section numbers

            * ``CP`` - Coupled set numbers

            * ``CE`` - Constraint equation numbers

            * ``CLEAR`` - All items will be offset

            * ``STATUS`` - Shows which items are specified not to be offset.

        Notes
        -----

        .. _NOOFFSET_notes:

        The :ref:`nooffset` command specifies data items not to be offset by a set of data read from a
        :ref:`cdread` command.
        """
        command = f"NOOFFSET,{label}"
        return self.run(command, **kwargs)

    def numcmp(self, label: str = "", **kwargs):
        r"""Compresses the numbering of defined items.

        Mechanical APDL Command: `NUMCMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NUMCMP.html>`_

        Parameters
        ----------
        label : str
            Items to be compressed:

            * ``NODE`` - Node numbers

            * ``ELEM`` - Element numbers

            * ``KP`` - Keypoint numbers

            * ``LINE`` - Line numbers

            * ``AREA`` - Area numbers

            * ``VOLU`` - Volume numbers

            * ``MAT`` - Material numbers

            * ``TYPE`` - Element type numbers

            * ``REAL`` - Real constant numbers

            * ``CP`` - Coupled set numbers

            * ``SECN`` - Section numbers

            * ``CE`` - Constraint equation numbers

            * ``CSYS`` - Coordinate system numbers

            * ``ALL`` - All item numbers

        Notes
        -----

        .. _NUMCMP_notes:

        The :ref:`numcmp` command effectively compresses out unused item numbers by renumbering all the
        items, beginning with one and continuing throughout the model. The renumbering order follows the
        initial item numbering order (that is, compression lowers the maximum number by "sliding" numbers
        down to take advantage of unused or skipped numbers). All defined items are renumbered, regardless
        of whether or not they are actually used or selected. Applicable related items are also checked for
        renumbering as described for the merge operation ( :ref:`nummrg` ).

        Compressing material numbers ( :ref:`numcmp`,ALL or :ref:`numcmp`,MAT) does not update the material
        number referenced by either of the following:

        * A temperature-dependent convection or surface-to-surface radiation load ( :ref:`sf`, :ref:`sfe`,
          :ref:`sfl`, :ref:`sfa` )

        * Real constants for multi-material elements

        Compression is usually not required unless memory space is limited and there are large gaps in the
        numbering sequence.
        """
        command = f"NUMCMP,{label}"
        return self.run(command, **kwargs)

    def nummrg(
        self,
        label: str = "",
        toler: str = "",
        gtoler: str = "",
        action: str = "",
        switch: str = "",
        **kwargs,
    ):
        r"""Merges coincident or equivalently defined items.

        Mechanical APDL Command: `NUMMRG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NUMMRG.html>`_

        Parameters
        ----------
        label : str
            Items to be merged:

            * ``NODE`` - Nodes

            * ``ELEM`` - Elements

            * ``KP`` - Keypoints (will also merge lines, areas, and volumes)

            * ``MAT`` - Materials

            * ``TYPE`` - Element types

            * ``REAL`` - Real constants

            * ``SECT`` - Section types

            * ``CP`` - Coupled sets

            * ``CE`` - Constraint equations

            * ``ALL`` - All items

        toler : str
            Range of coincidence. For ``Label`` = NODE and KP, defaults to 1.0E-4 (based on maximum
            Cartesian coordinate difference between nodes or keypoints). For ``Label`` = MAT, REAL, SECT,
            and CE, defaults to 1.0E-7 (based on difference of the values normalized by the values). Only
            items within range are merged. (For keypoints attached to lines, further restrictions apply. See
            the ``GTOLER`` field and Merging Solid Model Entities below.)

        gtoler : str
            Global solid model tolerance -- used only when merging keypoints attached to lines. If
            specified, ``GTOLER`` will override the internal relative solid model tolerance. See Merging
            Solid Model Entities below.

        action : str
            Specifies whether to merge or select coincident items.

            * ``SELE`` - Select coincident items but do not merge. ``Action`` = SELE is only valid for ``Label``
              = NODE.

            * ``(Blank)`` - Merge the coincident items (default).

        switch : str
            Specifies whether the lowest or highest numbered coincident item is retained after the merging
            operation. This option does not apply to keypoints; that is, for ``Label`` = KP, the lowest numbered keypoint is retained regardless of the ``Switch`` setting.

            * ``LOW`` - Retain the lowest numbered coincident item after the merging operation (default).

            * ``HIGH`` - Retain the highest numbered coincident item after the merging operation.

        Notes
        -----

        .. _NUMMRG_notes:

        The :ref:`nummrg` command does not change a model's geometry, only the topology.

        After issuing the command, the area and volume sizes ( :ref:`asum` and :ref:`vsum` ) may give
        slightly different results. In order to obtain the same results as before, use :ref:`facet`,
        :ref:`normal`, and :ref:`asum` / :ref:`vsum`.

        The merge operation is useful for tying separate but coincident parts of a model together. If not
        all items are to be checked for merging, use the select commands ( :ref:`nsel`, :ref:`esel`, etc.)
        to select items. Only selected items are included in the merge operation for nodes, keypoints, and
        elements.

        By default, the merge operation retains the lowest numbered coincident item. Higher numbered
        coincident items are deleted. Set ``Switch`` to HIGH to retain the highest numbered coincident item
        after the merging operation. Applicable related items are also checked for deleted item numbers and
        if found, are replaced with the retained item number. For example, if nodes are merged, element
        connectivities (except superelements), mesh item range associativity, coupled degrees of freedom,
        constraint equations, master degrees of freedom, degree of freedom constraints, nodal-force loads,
        nodal surface loads, and nodal body force loads are checked. Merging material numbers (
        :ref:`nummrg`,ALL or :ref:`nummrg`,MAT) does not update the material number referenced:

        * By temperature-dependent film coefficients as part of convection load or a temperature-dependent
          emissivity as part of a surface-to-surface radiation load ( :ref:`sf`, :ref:`sfe`, :ref:`sfl`,
          :ref:`sfa` )

        * By real constants for multi-material elements

        When merging tapered beam or pipe sections, the program first uses the associated end sections for
        merging. If the merge is successful, the program replaces the tapered section database with the end
        section data.

        If a unique load is defined among merged nodes, the value is kept and applied to the retained node.
        If loads are not unique (not recommended), only the value on the lowest node (or highest if
        ``Switch`` = HIGH) is kept (except for "force" loads for which the values are summed if they are not
        defined via tabular boundary conditions).

        The unused nodes (not recommended) in elements, couplings, constraint equations, etc. may become
        active after the merge operation.

         The ``Action`` field provides the option of visualizing the coincident items before the merging
        operation.

        .. warning::

            When merging entities in a model that has already been meshed, the order in which you issue
            multiple NUMMRG commands is significant. To merge two adjacent meshed regions having coincident
            nodes and keypoints, always merge nodes ( NUMMRG,NODE) beforemerging keypoints ( NUMMRG,KP);
            otherwise, some of the nodes may lose their association with the solid model (causing other
            operations to fail). To prevent mesh failure, avoid multiple merging and meshing operations.

        After a :ref:`nummrg`,NODE command executes, some nodes may be attached to more than one solid
        entity. As a result, subsequent attempts to transfer solid model loads to the elements may not be
        successful. Issue :ref:`nummrg`,KP to correct this problem. Do NOT issue :ref:`vclear` before
        issuing :ref:`nummrg`,KP.

        For :ref:`nummrg`,ELEM, elements must be identical in all aspects, including the direction of the
        element coordinate system.

        For certain solid and shell elements, the program interprets coincident faces as internal and
        eliminate them. To prevent this from occurring, shrink the entities by a very small factor to
        delineate coincident items ( :ref:`shrink`, 0.0001) and no internal nodes, lines, areas or elements
        will be eliminated.

        When working with solid models, you may have better success with the gluing operations (
        :ref:`aglue`, :ref:`lglue`, :ref:`vglue` ). Please read the following information when attempting to
        merge solid model entities.

        Gluing Operations vs. Merging Operations

        Adjacent, touching regions can be joined by gluing them ( :ref:`aglue`, :ref:`lglue`, :ref:`vglue` )
        or by merging coincident keypoints ( :ref:`nummrg`,KP, which also causes merging of identical lines,
        areas, and volumes). In many situations, either approach will work just fine. Some factors, however,
        may lead to a preference for one method over the other.

        **Geometric Configuration**

        Gluing is possible regardless of the initial alignment or offset of the input entities. Keypoint
        merging is possible only if each keypoint on one side of the face to be joined is matched by a
        coincident keypoint on the other side. This is commonly the case after a symmetry reflection (
        :ref:`arsym` or :ref:`vsymm` ) or a copy ( :ref:`agen` or :ref:`vgen` ), especially for a model
        built entirely in Mechanical APDL rather than imported from a CAD system. When the geometry is
        extremely
        precise, and the configuration is correct for keypoint merging, :ref:`nummrg` is more efficient and
        robust than :ref:`aglue` or :ref:`vglue`.

        **Model Accuracy**

        As with all boolean operations, gluing requires that the input entities meet the current boolean
        tolerance (BTOL). Otherwise, :ref:`aglue` or :ref:`vglue` may fail. In such cases, relaxing the
        tolerance may allow the glue to complete. An advantage of gluing is that it is unlikely to degrade
        the accuracy of a geometric model. Keypoint merging can operate on almost any combination of
        entities (although you may have to override the default tolerances on :ref:`nummrg` ). However, it
        can also introduce or increase accuracy flaws, making later boolean operations less likely to
        succeed. If the input tolerances are too large, :ref:`nummrg` can collapse out small lines, areas,
        or volumes you intended to keep, possibly rendering the model unusable.

        **Mesh Status**

        As with all boolean operations, gluing requires that the input entities be unmeshed. Keypoint
        merging is effective for meshed models under the right conditions. More information on keypoint
        merging follows.

        Merging Solid Model Entities:

        When merging solid model entities ( ``Label`` = KP or ALL), keypoint locations are used as the basis
        for merging. Once keypoints are merged, any higher order solid model entities (lines, areas, and
        volumes), regardless of their select status or attachment to the merged keypoints, are considered
        for merging.

        Keypoints that are attached to lines will be merged only if:

        * ΔX, ΔY, and ΔZ are each less than ``TOLER``

        where,

        * ΔX is the X component of the distance between keypoints, * ΔY is the Y component of the distance
          between keypoints, and * ΔZ is the Z component of the distance between keypoints;

        and

        * :math:`equation not available`  is less than 1E-5 times the length of the longest line attached to
          those     keypoints (internal relative solid model tolerance), or  :math:`equation not available`
          is less than  ``GTOLER`` (global solid model tolerance) if specified.

        The ``TOLER`` field is a consideration tolerance. If a keypoint is within ``TOLER`` of another
        keypoint, then those two keypoints are candidates to be merged. If, when "moving" the higher
        numbered keypoint, the distance exceeds the internal relative solid model tolerance, or the global
        solid model tolerance ( ``GTOLER`` ) if specified, the keypoints will not be merged. Lines, areas,
        and volumes are considered for merging in a similar manner.

        The internal relative solid model tolerance should be overridden by the global solid model tolerance
        ( ``GTOLER`` ) only when absolutely necessary. ``GTOLER`` is an absolute tolerance; if specified,
        relative lengths of lines in the model will no longer be considered in the merge operation. If
        ``GTOLER`` is too large, you can "merge-out" portions of your model accidently, effectively
        defeaturing the model. If using ``GTOLER``, it is good practice so first save the database before
        issuing :ref:`nummrg` (as undesired merges of solid model entities could occur).
        """
        command = f"NUMMRG,{label},{toler},{gtoler},{action},{switch}"
        return self.run(command, **kwargs)

    def numoff(self, label: str = "", value: str = "", kref: str = "", **kwargs):
        r"""Adds a number offset to defined items.

        Mechanical APDL Command: `NUMOFF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NUMOFF.html>`_

        Parameters
        ----------
        label : str
            Apply offset number to one of the following sets of items:

            * ``NODE`` - Nodes

            * ``ELEM`` - Elements

            * ``KP`` - Keypoints

            * ``LINE`` - Lines

            * ``AREA`` - Areas

            * ``VOLU`` - Volumes

            * ``MAT`` - Materials

            * ``TYPE`` - Element types

            * ``REAL`` - Real constants

            * ``CP`` - Coupled sets

            * ``SECN`` - Section numbers

            * ``CE`` - Constraint equations

            * ``CSYS`` - Coordinate systems

        value : str
            Offset number value (cannot be negative)

        kref : str
            Attribute reference key:

            0 - Add number offset to defined items only (default)

            1 - Add number offset to all attribute references (includes undefined items)

        Notes
        -----

        .. _NUMOFF_notes:

        Useful for offsetting current model data to prevent overlap if another model is read in.
        :ref:`cdwrite` automatically writes the appropriate :ref:`numoff` commands followed by the model
        data to :file:`File.CDB`. When the file is read, therefore, any model already existing in the
        database is offset before the model data on the file is read.

        Offsetting material numbers with this command ( :ref:`numoff`,MAT) does not update the material
        number referenced by either of the following:

        * A temperature-dependent convection or surface-to-surface radiation load ( :ref:`sf`, :ref:`sfe`,
          :ref:`sfl`, :ref:`sfa` )

        * Real constants for multi-material elements

        A mismatch may therefore exist between the material definitions and the material numbers referenced.
        """
        command = f"NUMOFF,{label},{value},{kref}"
        return self.run(command, **kwargs)

    def numstr(self, label: str = "", value: str = "", **kwargs):
        r"""Establishes starting numbers for automatically numbered items.

        Mechanical APDL Command: `NUMSTR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NUMSTR.html>`_

        Parameters
        ----------
        label : str
            Apply starting number to one of the following sets of items:

            * ``NODE`` - Node numbers. ``Value`` defaults (and is continually reset) to 1 + maximum node number
              in model. Cannot be reset lower.

            * ``ELEM`` - Element numbers. ``Value`` defaults (and is continually reset) to 1 + maximum element
              number in model. Cannot be reset lower.

            * ``KP`` - Keypoint numbers. ``Value`` defaults to 1. Only undefined numbers are used. Existing
              keypoints are not overwritten.

            * ``LINE`` - Line numbers. ``Value`` defaults to 1. Only undefined numbers are used. Existing lines
              are not overwritten.

            * ``AREA`` - Area numbers. ``Value`` defaults to 1. Only undefined numbers are used. Existing areas
              are not overwritten.

            * ``VOLU`` - Volume numbers. ``Value`` defaults to 1. Only undefined numbers are used. Existing
              volumes are not overwritten.

            * ``DEFA`` - Default. Returns all starting numbers to their default values.

        value : str
            Starting number value.

        Notes
        -----

        .. _NUMSTR_notes:

        Establishes starting numbers for various items that may have numbers automatically assigned (such as
        element numbers with the :ref:`egen` command, and node and solid model entity numbers with the mesh
        like :ref:`amesh`, :ref:`vmesh`, etc.. Use :ref:`numstr`,STAT to display settings. Use
        :ref:`numstr`,DEFA to reset all specifications back to defaults. Defaults may be lowered by
        deleting and compressing items (that is, :ref:`ndele` and :ref:`numcmp`,NODE for nodes, etc.).

        A mesh clear operation ( :ref:`vclear`, :ref:`aclear`, :ref:`lclear`, and :ref:`kclear` )
        automatically sets starting node and element numbers to the highest unused numbers. If a specific
        starting node or element number is desired, issue :ref:`numstr` after the clear operation.
        """
        command = f"NUMSTR,{label},{value}"
        return self.run(command, **kwargs)
