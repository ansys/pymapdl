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


class SpecialPurpose:

    def bfint(
        self,
        fname1: str = "",
        ext1: str = "",
        fname2: str = "",
        ext2: str = "",
        kpos: int | str = "",
        clab: str = "",
        kshs: int | str = "",
        tolout: str = "",
        tolhgt: str = "",
        **kwargs,
    ):
        r"""Activates the body force interpolation operation.

        Mechanical APDL Command: `BFINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFINT.html>`_

        Parameters
        ----------
        fname1 : str
            File name and directory path (248 characters maximum, including directory) from which to read
            data for interpolation. If you do not specify a directory path, it will default to your working
            directory and you can use all 248 characters for the file name.

            The file name defaults to :file:`Jobname`.

        ext1 : str
            Filename extension (eight-character maximum). The extension defaults to NODE if ``Fname1`` is
            blank.

        fname2 : str
            File name and directory path (248 characters maximum, including directory) to which **BF** commands are written. If you do not specify a directory path, it will default to your working
            directory and you can use all 248 characters for the file name.

            The file name defaults to :file:`Jobname`.

        ext2 : str
            Filename extension (eight-character maximum). The extension defaults to BFIN if ``Fname2`` is
            blank.

        kpos : int or str
            Position on ``Fname2`` to write block of **BF** commands:

            * ``0`` - Beginning of file (overwrite existing file).

            * ``1`` - End of file (append to existing file).

        clab : str
            Label (8 characters maximum, including the colon) for this block of **BF** commands in ``Fname2``. This label is appended to the colon (:). Defaults to BF ``n``, where ``n`` is the cumulative iteration number for the data set currently in the database.

        kshs : int or str
            Shell-to-solid submodeling key:

            * ``0`` - Solid-to-solid or shell-to-shell submodel.

            * ``1`` - Shell-to-solid submodel.

        tolout : str
            Extrapolation tolerance about elements, based on a fraction of the element dimension. Submodel
            nodes outside the element by more than ``TOLOUT`` are not accepted as candidates for DOF
            extrapolation. Defaults to 0.5 (50%).

        tolhgt : str
            Height tolerance above or below shell elements, in units of length. Used only for shell-to-shell
            submodeling ( ``KSHS`` = 0). Submodel nodes off the element surface by more than ``TOLHGT`` are not
            accepted as candidates for DOF interpolation or extrapolation. Defaults to 0.0001 times the maximum
            element dimension.

            .. warning::

                Relaxing this tolerance to allow submodel nodes to be found may cause poor submodel results.

        Notes
        -----

        .. _BFINT_notes:

        File ``Fname1`` should contain a node list for which body forces are to be interpolated (
        :ref:`nwrite` ). File ``Fname2`` is created, and contains interpolated body forces written as a
        block of nodal :ref:`bf` commands.

        Body forces are interpolated from elements having TEMP as a valid body force or degree of freedom,
        and only the label TEMP is written on the nodal :ref:`bf` commands. Interpolation is performed for
        all nodes on file ``Fname1`` using the results data currently in the database. For layered elements,
        use the :ref:`layer` command to select the locations of the temperatures to be used for
        interpolation. Default locations are the bottom of the bottom layer and the top of the top layer.

        The block of :ref:`bf` commands begins with an identifying colon label command and ends with a
        ``/EOF`` command. The colon label command has the form : ``Clab``. Interpolation from multiple
        results sets can be performed by looping through the results file in a user-defined macro.
        Additional blocks can be appended to ``Fname2`` by using ``KPOS`` and unique colon labels. Issue
        :ref:`input`, with the appropriate colon label, to read the block of commands.

        If the model has coincident (or very close) nodes, :ref:`bfint` must be applied to each part of the
        model separately to ensure that the mapping of the nodes is correct. For example, if nodes belonging
        to two adjacent parts linked by springs are coincident, the operation should be performed on each
        part of the model separately.
        """
        command = f"BFINT,{fname1},{ext1},,{fname2},{ext2},,{kpos},{clab},{kshs},{tolout},{tolhgt}"
        return self.run(command, **kwargs)

    def cbdof(
        self,
        fname1: str = "",
        ext1: str = "",
        fname2: str = "",
        ext2: str = "",
        kpos: int | str = "",
        clab: str = "",
        kshs: int | str = "",
        tolout: str = "",
        tolhgt: str = "",
        tolthk: str = "",
        **kwargs,
    ):
        r"""Activates cut-boundary interpolation (for submodeling).

        Mechanical APDL Command: `CBDOF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CBDOF.html>`_

        Parameters
        ----------
        fname1 : str
            File name and directory path (248 characters maximum, including directory) from which to read
            boundary node data. If no specified directory path exists, the path defaults to your working
            directory and you can use all 248 characters for the file name.

            The file name defaults to :file:`Jobname`.

        ext1 : str
            Filename extension (eight-character maximum). The extension defaults to NODE if ``Fname1`` is
            blank.

        fname2 : str
            File name and directory path (248 characters maximum, including directory) to which cut-boundary **D** commands are written. If no specified directory path exists, the path defaults to your working
            directory and you can use all 248 characters for the file name.

            The file name defaults to :file:`Jobname`.

        ext2 : str
            Filename extension (eight-character maximum). The extension defaults to CBDO if ``Fname2`` is
            blank.

        kpos : int or str
            Position on ``Fname2`` to write block of :ref:`d` commands:

            * ``0`` - Beginning of file (overwrite existing file).

            * ``1`` - End of file (append to existing file).

        clab : str
            Label (eight characters maximum, including the colon) for this block of :ref:`d` commands on
            ``Fname2``. his label is appended to the colon (:). Defaults to CB ``n``, where ``n`` is the
            cumulative iteration number for the data set currently in the database. For imaginary data (see
            KIMG on the :ref:`starset` command), ``Clab`` defaults to CI ``n``.

        kshs : int or str
            Shell-to-solid submodeling key:

            * ``0`` - Solid-to-solid or shell-to-shell submodel.

            * ``1`` - Shell-to-solid submodel.

        tolout : str
            Extrapolation tolerance about elements, based on a fraction of the element dimension. Submodel
            nodes outside the element by more than ``TOLOUT`` are not accepted as candidates for DOF
            extrapolation. Defaults to 0.5 (50 percent).

        tolhgt : str
            Height tolerance above or below shell elements, in units of length. Used only for shell-to-shell
            submodeling ( ``KSHS`` = 0). Submodel nodes off the element surface by more than ``TOLHGT`` are
            not accepted as candidates for degree-of-freedom interpolation or extrapolation. Defaults to
            0.0001 times the maximum element dimension.

        tolthk : str
            Height tolerance above or below shell elements, based on a fraction of the shell element
            thickness. Used only for shell-to-solid submodeling (KSHS = 1). Submodel nodes off the element
            surface by more than ``TOLTHK`` are not accepted as candidates for DOF interpolation or
            extrapolation. Defaults to 0.1 times the average shell thickness.

        Notes
        -----

        .. _CBDOF_notes:

        File ``Fname1`` should contain a node list for which boundary conditions are to be interpolated (
        :ref:`nwrite` ). File ``Fname2`` is created to contain interpolated boundary conditions written as a
        block of :ref:`d` commands.

        Boundary conditions are written for the active degree-of-freedom set for the element from which
        interpolation is performed. Interpolation occurs on the selected set of elements. The block of
        :ref:`d` commands begins with an identifying colon label and ends with a ``/EOF`` command. The colon
        label is of the form : ``Clab`` (described above).

        Interpolation from multiple results sets can be performed by looping through the results file in a
        user-defined macro. Additional blocks can be appended to ``Fname2`` by using ``KPOS`` and unique
        colon labels. To read the block of commands, issue the :ref:`input` command with the appropriate
        colon label.

        If the model has coincident (or very close) nodes, the :ref:`cbdof` must be applied to each part of
        the model separately to ensure that the mapping of the nodes is correct. For example, if nodes
        belonging to two adjacent parts linked by springs are coincident, the operation should be performed
        on each part of the model separately.

        Resume the coarse model database at the beginning of the cut-boundary procedure. The database should
        have been saved after the first coarse model solution, as the number of nodes in the database and
        the results file must match, and internal nodes are sometimes created during the solution.

        This command cannot be used to interpolate the magnetic edge-flux (AZ) degree of freedom.

        .. warning::

            Relaxing the TOLHGTor TOLTHKtolerances to allow submodel nodes to be “found” can produce poor
            submodel results.
        """
        command = f"CBDOF,{fname1},{ext1},,{fname2},{ext2},,{kpos},{clab},{kshs},{tolout},{tolhgt},{tolthk}"
        return self.run(command, **kwargs)

    def cmsfile(
        self,
        option: str = "",
        fname: str = "",
        ext: str = "",
        cmskey: str = "",
        **kwargs,
    ):
        r"""Specifies a list of component mode synthesis (CMS) results files for plotting results on the
        assembly.

        Mechanical APDL Command: `CMSFILE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CMSFILE.html>`_

        **Command default:**

        .. _CMSFILE_default:

        If issued with no arguments, the :ref:`cmsfile` command uses these defaults:

        :ref:`cmsfile`,ADD, ``Jobname``,rst,ON

        The command adds the component results file :file:`Jobnamerst`.

        Parameters
        ----------
        option : str
            Specifies the command operation:

            * ``ADD`` - Add the specified component results file ( ``Fname`` ) to the list of files to plot.
              This option is the default.

            * ``DELETE`` - Remove the specified component results file ( ``Fname`` ) from the list of files to
              plot.

            * ``LIST`` - List all specified component results files.

            * ``CLEAR`` - Clear all previous files added.

            * ``ALL`` - Add all component results ( :file:`.rst` ) files from the working directory to the list
              of files to plot.

        fname : str
            The file name (with full directory path) of the component results file. The default file name is
            the :file:`Jobname` (specified via the :ref:`filname` command).

        ext : str
            The file name ( ``Fname`` ) extension. The default extension is :file:`rst`.

        cmskey : str
            Valid only when adding a results file ( ``Option`` = ADD or ALL), this key specifies whether or not to check the specified :file:`.rst` file to determine if it was created via a CMS expansion pass:

            * ``ON`` - Check (default).

            * ``OFF`` - Do not check.

        Notes
        -----

        .. _CMSFILE_notes:

        The :ref:`cmsfile` command specifies the list of component mode synthesis (CMS) results files to
        include when plotting the mode shape of an assembly.

        During postprocessing ( :ref:`post1` ) of a CMS analysis, issue the :ref:`cmsfile` command to point
        to component results files of interest. (You can issue the command as often as needed to include all
        or some of the component results files.) Issue the :ref:`set` command to acquire the frequencies and
        mode shapes from substeps for all specified results files. Execute a plot ( :ref:`plnsol` ) or print
        ( :ref:`prnsol` ) operation to display the mode shape of the entire assembly.

        When you specify a results file to add to the plot list, the default behavior of the command (
        ``CmsKey`` = ON) is to first verify that the file is from a CMS analysis and that the frequencies of
        the result sets on the file match the frequencies on the first file in the list. If ``CmsKey`` =
        OFF, you can add any :file:`.rst` file to the list of files to plot, even if the file was not
        expanded via a CMS expansion pass.

        If ``CmsKey`` = ON (default), output from the command appears as: ``ADD CMS FILE =`` filename.rst
        ``CmsKey`` = OFF, output from the command appears as: ``ADD FILE =`` filename.rst

        If ``Option`` = DELETE or CLEAR, you must clear the database ( ``/CLEAR`` ), then re-enter the
        postprocessor ( :ref:`post1` ) and issue a :ref:`set` command for the change to take effect on
        subsequent plots.

        Clearing the database does not clear the list of files specified via the :ref:`cmsfile` command.
        Specify ``Option`` = CLEAR to clear the list of files.
        """
        command = f"CMSFILE,{option},{fname},{ext},{cmskey}"
        return self.run(command, **kwargs)

    def cyccalc(
        self, fileprefix: str = "", fileformat: str = "", separator: str = "", **kwargs
    ):
        r"""Calculates results from a cyclic harmonic mode-superposition analysis using the specifications
        defined by :ref:`cycspec`.

        Mechanical APDL Command: `CYCCALC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCCALC.html>`_

        **Command default:**

        .. _CYCCALC_default:

        Write the result tables to the output file.

        Parameters
        ----------
        fileprefix : str
            Each result table (corresponding to each :ref:`cycspec` specification) is written to a file
            beginning with ``FilePrefix``. If blank (default), the result tables are written to the output
            file.

        fileformat : str
            If ``FilePrefix`` is specified, then use ``FileFormat`` to specify the format of the file to be
            written:

            * ``FORM`` - Formatted file (default)

            * ``CSV`` - Comma-separated value file

        separator : str
            If ``FileFormat`` is CSV, use ``Separator`` to specify the field separator:

            * ``COMMA`` - Use a comma () as the field separator (default)

            * ``COLON`` - Use a colon (:) as the field separator

            * ``DOT`` - Use a period (.) as the field separator

        Notes
        -----

        .. _CYCCALC_notes:

        :ref:`cyccalc` loops through the specification given by :ref:`cycspec` and computes the requested
        outputs. The outputs are given in a table format, with the rows corresponding to each frequency
        solution from the harmonic analysis, and the columns corresponding to each sector. The table entries
        are the maximum value of the specified quantity at the specified location in the sector. In
        addition, columns containing the maximum value at the frequency, the sector in which it occurs, and
        the node in the sector at which it occurs are output.

        If ``FilePrefix`` is specified, a file is created for each output table with the name
        :file:`FilePrefix_node_type.ext`, where ``node`` is the node number or component name, ``type`` is
        the item/component requested, and the file extension ``.ext`` is either :file:`.txt` or
        :file:`.csv`, depending on ``FileFormat``.

        A :ref:`set` command must precede the :ref:`cyccalc` command.

        The :ref:`cyccalc` results are based on the currently active :ref:`rsys`, :ref:`shell`,
        :ref:`layer`, and :ref:`avprin` settings.

        The :ref:`cyccalc` command only supports matched nodes. For more details on matching cyclic edge
        node pairs see `Edge Component Pairs
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycedgecomp.html#>`_
        """
        command = f"CYCCALC,{fileprefix},{fileformat},{separator}"
        return self.run(command, **kwargs)

    def cycfiles(
        self,
        fnamerst: str = "",
        extrst: str = "",
        fnamerfrq: str = "",
        extrfrq: str = "",
        **kwargs,
    ):
        r"""Specifies the data files where results are to be found for a cyclic symmetry mode-superposition
        harmonic analysis.

        Mechanical APDL Command: `CYCFILES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCFILES.html>`_

        **Command default:**

        .. _CYCFILES_default:

        No defaults are available for the :ref:`cycfiles` command. You must issue this command to properly
        postprocess the results of a cyclic symmetry mode-superposition harmonic analysis. If issued with no
        arguments, the postprocessing will be done using :file:`Jobname.rst` and :file:`Jobname.rfrq` from
        the current working directory.

        Parameters
        ----------
        fnamerst : str
            The file name and directory path of the results file from the cyclic modal solution. Defaults to
            :file:`Jobname`.

        extrst : str
            File name extension for ``FnameRst``. Defaults to :file:`rst`.

        fnamerfrq : str
            The file name and directory path of the results file from the cyclic mode-superposition harmonic
            solution. Defaults to the value of the ``FnameRst`` argument.

        extrfrq : str
            File name extension for ``FnameRfrq``. Defaults to :file:`rfrq`.
        """
        command = f"CYCFILES,{fnamerst},{extrst},{fnamerfrq},{extrfrq}"
        return self.run(command, **kwargs)

    def cycphase(self, type_: str = "", option: str = "", **kwargs):
        r"""Provides tools for determining minimum and maximum possible result values from frequency couplets
        produced in a modal cyclic symmetry analysis.

        Mechanical APDL Command: `CYCPHASE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCPHASE.html>`_

        **Command default:**

        .. _CYCPHASE_default:

        No defaults are available for the :ref:`cycphase` command. You must specify an argument ( ``TYPE`` )
        when issuing the command. Other values which may be necessary ( ``OPTION`` ) depend upon which
        ``TYPE`` argument you specify.

        Parameters
        ----------
        type_ : str
            The type of operation requested:

            * ``DISP`` - Calculate the maximum and minimum possible displacement at each node in the original
              sector model. Store the values and the phase angle at which they occurred.

            * ``STRESS`` - Calculate the maximum and minimum possible stresses at each node in the original
              sector model. Store the values and the phase angle at which they occurred.

            * ``STRAIN`` - Calculate the maximum and minimum possible strains at each node in the original
              sector model. Store the values and the phase angle at which they occurred.

            * ``ALL`` - Calculate the maximum and minimum possible displacement, stress and strain at each node
              in the original sector model. Store the values and the phase angle at which they occurred.

            * ``GET`` - Places the value of a MAX or MIN item into the _CYCVALUE parameter, the node for that
              value in the _CYCNODE parameter, and the phase angle for the value in the _CYCPHASE parameter.

            * ``PUT`` - Put resulting sweep values for printing (via the :ref:`prnsol` command ) or plotting
              (via the :ref:`plnsol` command).

            * ``LIST`` - List the current minimum/maximum displacement, stress and strain nodal values.

            * ``STAT`` - Summarize the results of the last phase sweep.

            * ``CLEAR`` - Clear phase-sweep information from the database.

        option : str
            If TYPE = DISP, STRAIN, STRESS or ALL, controls the sweep angle increment to use in the search:

            * ``Angle`` - The sweep angle increment in degrees, greater than 0.1 and less than 10. The default
              is 1.

            If TYPE = PUT, controls which values are placed onto the model:

            * ``MAX`` - Put all existing nodal maximum values onto the model. This option is the default.

            * ``MIN`` - Put all existing nodal minimum values onto the model.

            If TYPE = GET, controls the values placed into cyclic parameters:

            * ``Item`` - Specifies the type of values on which to operate:

              * U -- Displacement
              * S -- Stress
              * EPEL -- Strain
            * ``Comp`` - Specifies the specific component of displacement, stress or strain for which to get information:

              * X,Y,Z -- Basic components
              * XY,YZ,XZ -- Shear components
              * 1,2,3 -- Principal values
              * EQV -- Equivalent value
              * SUM -- USUM
            * ``MxMn`` - Specifies whether the requested value information is for the maximum or minimum value:

              * MAX -- Maximum value.
              * MIN -- Minimum value.

        Notes
        -----

        .. _CYCPHASE_notes:

        When you `expand the results of a modal cyclic symmetry analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycpost.html#ans_cycsym_res_coord_sys>`_
        (via the :ref:`cycexpand` or :ref:`expand` command), the program combines the real and imaginary
        results for a given nodal diameter, assuming no phase shift between them; however, the modal
        response can occur at any phase shift.

        :ref:`cycphase` response results are valid only for the first cyclic sector. To obtain the response
        at any part of the expanded model, Ansys, Inc. recommends using `cyclic symmetry results
        expansion
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycpost.html#ans_cycsym_res_coord_sys>`_
        at the phase angle obtained via :ref:`cycphase`.

        The phase angles returned by :ref:`cycphase` contain the minimum and maximum values for USUM, SEQV
        and other scalar principal stress and strain quantities; however, they do not always return the true
        minimum and maximum values for directional quantities like UX or SX unless the values fall in the
        first sector.

        :ref:`cycphase` does not consider midside node values when evaluating maximum and minimum values,
        which may affect display quantities but no others. (Typically, the program ignores midside node
        stresses and strains during postprocessing.)

        Issuing :ref:`cycphase`,PUT clears the result values for midside nodes on high order elements;
        therefore, this option sets element faceting ( :ref:`efacet` ) to 1. The command reports that
        midside nodal values are set to zero and indicates that element faceting is set to 1.

        If the sweep values are available after issuing a :ref:`cycphase`,PUT command, the :ref:`prnsol` or
        :ref:`plnsol` command will print or plot (respectively) the sweep values of structure displacement
        Ux, Uy, Uz, component stress/strain X, Y, Z, XY, YZ, ZX, principal stress/strain 1, 2, 3 and
        equivalent stress/strain EQV. The vector sum of displacement (USUM) and stress/strain intensity
        (SINT) are not valid phase-sweep results.

        You can specify any coordinate system via the :ref:`rsys` command for displaying or printing
        :ref:`cycphase` results. However, after :ref:`cycphase` results have been extracted, you cannot then
        transform them via the :ref:`rsys` command. If you try to do so, the program issues a warning
        message.

        The :ref:`cycphase` command is valid in :ref:`post1` and for cyclically symmetric models only.

        To learn more about analyzing a cyclically symmetric structure, see the `Cyclic Symmetry Analysis
        Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_example.html>`_.
        """
        command = f"CYCPHASE,{type_},{option}"
        return self.run(command, **kwargs)

    def cycspec(
        self, label: str = "", node: str = "", item: str = "", comp: str = "", **kwargs
    ):
        r"""Defines the set of result items for a subsequent :ref:`cyccalc` command in postprocessing a cyclic
        harmonic mode-superposition analysis.

        Mechanical APDL Command: `CYCSPEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CYCSPEC.html>`_

        **Command default:**

        .. _CYCSPEC_default:

        No defaults are available for the :ref:`cycspec` command. You must issue this command to define the
        set of result items for evaluation in a subsequent :ref:`cyccalc` command used in computing results
        of a cyclic harmonic mode-superposition analysis.

        Parameters
        ----------
        label : str
            One of the following labels:

            * ``ADD`` - Adds a new specification to the set (default). The maximum number of specifications that
              can be defined is 50.

            * ``LIST`` - Lists the current set of specifications. ``Node``, ``Item``, ``Comp`` are ignored.

            * ``ERASE`` - Erases the current set of specifications. ``Node``, ``Item``, ``Comp`` are ignored.

            * ``DELETE`` - Deletes an existing specification. ``Item``, ``Comp`` are ignored.

        node : str
            The node at which to evaluate the results. If ``Node`` is a nodal component, then all nodes in
            the component are included. All sectors containing this node (or set of nodes) are evaluated.

            For ``LABEL`` = DELETE, use ``Node`` to indicate which specification in the set to delete.

        item : str
            Specifies the type of values to evaluate:

            * ``U`` - Displacement

            * ``S`` - Stress

            * ``EPEL`` - Elastic strain

        comp : str
            Specifies the specific component of displacement, stress, or strain to evaluate:

            * ``X,Y,Z`` - Direct components

            * ``XY,YZ,XZ`` - Shear components (stress and strain only)

            * ``1,2,3`` - Principal values (stress and strain only)

            * ``EQV`` - Equivalent value (stress and strain only)

            * ``SUM`` - Vector sum (displacement only)

            * ``NORM`` - L2 norm for the set of nodes (displacement only)

        Notes
        -----

        .. _CYCSPEC_notes:

        Up to 50 specifications can be defined for use in a subsequent :ref:`cyccalc` command. If more than
        50 specifications are desired, erase the table after the :ref:`cyccalc` operation and add new
        specifications and repeat the :ref:`cyccalc` command. All the specified nodes, items, and components
        are evaluated for all sectors and the maximum amplitude value output. For combined stresses and
        strains ( ``Comp`` = 1,2,3 or EQV) or displacement vector sum ( ``Comp`` = SUM), a 360 degree phase
        sweep is performed at each location to determine the maximum.

        Additional POST1 controls are used to refine the specification. For component values, components are
        in the :ref:`rsys` direction. For shell elements, the results are at the :ref:`shell` location. For
        EPEL,EQV, the results are based on the ``EFFNU`` value on the :ref:`avprin` command. The controls
        active when the :ref:`cyccalc` command is issued determine the result values. If results at another
        :ref:`shell` location are desired, issue the new :ref:`shell` command and then re-issue the
        :ref:`cyccalc` command.

        If a single node is input, the ``Item`` / ``Comp`` value at that location in each sector is output.
        If a node component is given, then the maximum ``Item`` / ``Comp`` value within the set of nodes of
        each sector is output, one value for each sector (the node of the maximum may vary from sector to
        sector). For stress and strain items, only corner nodes are valid.

        For the displacement norm option ( ``Item`` = U, ``Comp`` = NORM), the L2 norm computed from all the
        nodes in the component is output, one per sector.
        """
        command = f"CYCSPEC,{label},{node},{item},{comp}"
        return self.run(command, **kwargs)

    def exoption(self, ldtype: str = "", option: str = "", value: str = "", **kwargs):
        r"""Specifies the :ref:`exprofile` options for the Mechanical APDL to Ansys CFX profile file transfer.

        Mechanical APDL Command: `EXOPTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXOPTION.html>`_

        Parameters
        ----------
        ldtype : str
            Load type:

            * ``SURF`` - Surface load

            * ``VOLU`` - Volume load

        option : str
            Surface options:

            * ``Precision`` - Number of significant digits for the fractional part of real data

            * ``Connectivity`` - Key to include face connectivity in the exported profile file

            Volume options:

            * ``Precision`` - Number of significant digits after the decimal for real data

        value : str
            Specify the value for either Precision or Connectivity.

            For Precision, specify the number of significant digits. Can be any value between 1 to 20, default
            8. When 0 or an invalid value is specified, the program will use the default value of 8 and issue a
            warning message.

            For Connectivity, specify the key to include the element face connectivity data for surface loads
            (does not support volume loads):

            * ``OFF`` - Do not include the connectivity data in the exported file (default)

            * ``ON`` - Include the connectivity data in the exported file
        """
        command = f"EXOPTION,{ldtype},{option},{value}"
        return self.run(command, **kwargs)

    def expand(
        self,
        nrepeat: str = "",
        modal: str = "",
        hindex: str = "",
        icsys: str = "",
        sctang: str = "",
        phase: str = "",
        **kwargs,
    ):
        r"""Displays the results of a modal cyclic symmetry analysis.

        Mechanical APDL Command: `EXPAND <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXPAND.html>`_

        Parameters
        ----------
        nrepeat : str
            Number of sector repetitions for expansion. The default is 0 (no expansion).

        modal : str
            Specifies that the expansion is for a modal cyclic symmetry analysis.

        hindex : str
            The harmonic index ID for the results to expand.

        icsys : str
            The coordinate system number used in the modal cyclic symmetry solution. The default is the
            global cylindrical coordinate system (specified via the :ref:`csys` command where ``KCN`` = 1).

        sctang : str
            The sector angle in degrees, equal to 360 divided by the number of cyclic sectors.

        phase : str
            The phase angle in degrees to use for the expansion. The default is 0. Typically, the value is
            the peak displacement (or stress/strain) phase angle obtained via the :ref:`cycphase` command.

        Notes
        -----

        .. _EXPAND_notes:

        Issue this command to display the results of a modal cyclic symmetry analysis.

        When you issue the :ref:`expand`, ``Nrepeat`` command, subsequent :ref:`set` commands read data from
        the results file and expand them to ``Nrepeat`` sectors. As long as no entities have been modified,
        this expansion can be negated (that is, reverted to single sector) by issuing :ref:`expand` with no
        arguments. If you modify entities and wish to return to the partial model, use the Session Editor
        (see Restoring Database Contents in the `Operations Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ope/Hlp_G_OPE8.html>`_).

        :ref:`expand` displays the results and allows you to print them, as if for a full model. The
        harmonic index (automatically retrieved from the results file) appears in the legend column.

        When plotting or printing element strain energy (SENE), the :ref:`expand` command works with brick
        or tet models only. Element kinetic energy (KENE) plotting or printing is not supported.

        :ref:`expand` is a specification command valid only in POST1. It is significantly different from the
        :ref:`cycexpand` command in several respects, (although you can use either command to display the
        results of a modal cyclic symmetry analysis):

        * :ref:`expand` has none of the limitations of the :ref:`cycexpand` command.

        * :ref:`expand` changes the database by modifying the geometry, the nodal displacements, and element
          stresses as they are read from the results file, whereas the :ref:`cycexpand` command does not
          change the database.

        .. warning::

            The EXPAND command creates new nodes and elements; therefore, saving (or issuing the /EXIT, ALL
            command) after issuing the EXPAND command can result in large databases.
        """
        command = f"EXPAND,{nrepeat},{modal},{hindex},{icsys},{sctang},,{phase}"
        return self.run(command, **kwargs)

    def exprofile(
        self,
        ldtype: str = "",
        load: str = "",
        value: str = "",
        pname: str = "",
        fname: str = "",
        fext: str = "",
        fdir: str = "",
        **kwargs,
    ):
        r"""Exports Mechanical APDL interface data on selected nodes to an Ansys CFX Profile file.

        Mechanical APDL Command: `EXPROFILE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXPROFILE.html>`_

        Parameters
        ----------
        ldtype : str
            Load type:

            * ``SURF`` - Surface load.

            * ``VOLU`` - Volumetric load.

        load : str
            Surface loads:

            * ``DISP`` - Displacement (in a static analysis) or mode shape and global parameters (in a modal
              analysis).

            * ``MODE`` - Normalized mode shape and global parameters (in a modal analysis only).

            * ``TEMP`` - Temperature.

            * ``HFLU`` - Heat flux.

            Volumetric loads:

            * ``DISP`` - Displacement.

            * ``FORC`` - Force.

            * ``HGEN`` - Heat generation.

        value : str
            If a positive integer, specifies the number of the surface or volume interface. If zero
            (default), the selected nodes or Named Selection are used.

        pname : str
            Field name in CFX Profile file (32-character maximum). Defaults to :file:`jobname_bcploadnumber`
            for a surface load and :file:`jobname_subdloadnumber` for volumetric load.

        fname : str
            The CFX Profile filename (248-character maximum). Defaults to :file:`jobname_bcploadnumber` for
            a surface load and :file:`jobname_subdloadnumber` for a volumetric load.

        fext : str
            The Profile file extension (8-character maximum). Defaults to :file:`csv`.

        fdir : str
            The Profile file directory (248-character maximum). Defaults to current directory.

        Notes
        -----
        By default, the :ref:`exprofile` command assumes the data it writes to the Profile file are in SI
        units. For models not described in SI units, issue the :ref:`exunit` command as needed to write the
        correct unit labels on the Profile file.

        For a modal analysis, if ``Load`` = DISP or MODE, global parameters including mass, frequency, and
        maximum displacement are also written to the Ansys CFX Profile file. You should therefore issue the
        :ref:`exunit` command for DISP, TIME, and MASS.

        Verify that the coordinate system is set to the global Cartesian ( :ref:`rsys`,0) before using this
        command.

        To transfer multiple loads across an interface, specify a unique file name and extension for each
        load.

        Force (FORC) and heat generation (HGEN) are per-unit volume.

        For modal analysis, this command will write global parameters including mass, frequency, and maximum
        displacement to the profile file. If using cyclic symmetry analysis, this command will also write
        harmonic indices to the profile file.

        For modal analysis, this command does not support the following mode-extraction methods (
        :ref:`modopt` ): unsymmetric matrix (UNSYM), the damped system (DAMP), or the QR-damped system
        (QRDAMP).

        To write the normalized (instead of non-normalized) mode shapes from a modal analysis to the file:

        * Use ``Load`` = MODE.

        * Verify that the mode shapes are normalized to the mass matrix ( :ref:`modopt`,,,,,,OFF), the
          default behavior.

        * Verify that the scale factor is set to 1.0 ( :ref:`set`,,,1.0), the default value.

        The nodes and underlying elements must be selected in order to be exported. See for details.

        For loads not specified directly via commands (such as :ref:`sf` and :ref:`bf` ), loads must first
        be read into the database ( :ref:`set` or :ref:`lcase` ).
        """
        command = f"EXPROFILE,{ldtype},{load},{value},{pname},{fname},{fext},{fdir}"
        return self.run(command, **kwargs)

    def exunit(
        self,
        ldtype: str = "",
        load: str = "",
        untype: str = "",
        name: str = "",
        **kwargs,
    ):
        r"""Specifies the interface data unit labels to be written to the profile file from Mechanical APDL to
        Ansys CFX transfer.

        Mechanical APDL Command: `EXUNIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXUNIT.html>`_

        Parameters
        ----------
        ldtype : str
            Load type:

            * ``SURF`` - Surface load.

            * ``VOLU`` - Volumetric load.

        load : str
            Surface loads:

            * ``DISP`` - Displacement in a static analysis. Mode shape in a modal analysis.

            * ``TIME`` - Time. The unit for frequency is the inverse of the unit for time.

            * ``MASS`` - Mass.

            * ``TEMP`` - Temperature.

            * ``HFLU`` - Heat flux.

            Volumetric loads:

            * ``DISP`` - Displacement.

            * ``FORC`` - Force

            * ``HGEN`` - Heat generation

        untype : str
            Unit type:

            * ``COMM`` - Predefined unit

            * ``USER`` - User-specified unit

        name : str
            Commonly used predefined unit name or user-specified unit name.

            * ``SI`` - International System of units (meter-kilogram-second) (default)

            * ``FT`` - English System of units (feet-pound-second)

            In the SI system, surface loads are in units of m for DISP, degrees K for TEMP, and W/m :sup:`2` for
            HFLU; volumetric loads are in units of m for DISP, N/m :sup:`3` for FORC, and W/m :sup:`3` for HGEN.

            In the English system, surface loads are in units of ft for DISP, degrees F for TEMP, and BTU/sec-ft
            :sup:`2` for HFLU; volumetric loads are in units of ft for DISP, pdl/ft :sup:`3` for FORC, and
            BTU/sec-ft :sup:`3` for HGEN. A pdl is a poundal, and 32.174 pdl = 1 lbf.

        Notes
        -----
        This command only specifies which unit labels are to be written to the file when the
        :ref:`exprofile` is issued. It does not perform unit conversions.
        """
        command = f"EXUNIT,{ldtype},{load},{untype},{name}"
        return self.run(command, **kwargs)

    def fssparm(self, port1: str = "", port2: str = "", **kwargs):
        r"""Calculates reflection and transmission properties of a frequency selective surface.

        Mechanical APDL Command: `FSSPARM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FSSPARM.html>`_

        Parameters
        ----------
        port1 : str
            Port number of input port. Defaults to 1.

        port2 : str
            Port number of output port. Defaults to 1.

        Notes
        -----
        :ref:`fssparm` calculates reflection and transmission coefficients, power reflection and
        transmission coefficients, and return and insertion losses of a frequency selective surface.
        """
        command = f"FSSPARM,{port1},{port2}"
        return self.run(command, **kwargs)

    def fsum(self, lab: str = "", item: str = "", **kwargs):
        r"""Sums the nodal force and moment contributions of elements.

        Mechanical APDL Command: `FSUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FSUM.html>`_

        Parameters
        ----------
        lab : str
            Coordinate system in which to perform summation.

            * ``(blank)`` - Sum all nodal forces in global Cartesian coordinate system (default).

            * ``RSYS`` - Sum all nodal forces in the currently active RSYS coordinate system.

        item : str
            Selected set of nodes.

            * ``(blank)`` - Sum all nodal forces for all selected nodes (default), excluding contact elements.

            * ``CONT`` - Sum all nodal forces for contact nodes only.

            * ``BOTH`` - Sum all nodal forces for all selected nodes, including contact elements.

        Notes
        -----

        .. _FSUM_notes:

        Sums and prints, in each component direction for the total selected node set, the nodal force and
        moment contributions of the selected elements attached to the node set. Selecting a subset of nodes
        ( :ref:`nsel` ) and then issuing this command will give the total force acting on that set of nodes
        (default), excluding surface-to-surface, node-to-surface, line-to-line, and line-to-surface contact
        elements ( ``TARGE169``, ``TARGE170``, ``CONTA172``, ``CONTA174``, ``CONTA175``, and ``CONTA177`` ).

        Setting ``ITEM`` = CONT sums the nodal forces and moment contributions of the selected contact
        elements ( ``CONTA172``, ``CONTA174``, ``CONTA175``, and ``CONTA177`` ). Setting ``ITEM`` = BOTH
        sums the nodal forces for all selected nodes, including contact elements.

        Nodal forces associated with surface loads are not included. The effects of nodal coupling and
        constraint equations are ignored. Moment summations are about the global origin unless another point
        is specified with the :ref:`spoint` command. This vector sum is printed in the global Cartesian
        system unless it is transformed ( :ref:`rsys` ) and a point is specified with the :ref:`spoint`
        command. By default, the sum is done in global Cartesian, and the resulting vector is transformed to
        the requested system.

        The ``LAB`` = RSYS option transforms each of the nodal forces into the active coordinate system
        before summing and printing. The :ref:`force` command can be used to specify which component
        (static, damping, inertia, or total) of the nodal load is to be used. This command output is
        included in the :ref:`nforce` command.

        The command should not be used with axisymmetric elements because it might calculate a moment where
        none exists. Consider, for example, the axial load on a pipe modeled with an axisymmetric shell
        element. The reaction force on the end of the pipe is the total force (for the full 360 degrees) at
        that location. The net moment about the centerline of the pipe would be zero, but the program would
        incorrectly calculate a moment at the end of the element as the force multiplied by the radius.

        The command is not valid for elements that operate solely within the nodal coordinate system with 1D
        option activated and rotated nodes ( :ref:`nrotat` ).

        **Using FSUM with the NLGEOM Command**
        If you have activated large deflection ( :ref:`nlgeom`, ON ), the :ref:`fsum` command generates the
        following message:

        Summations based on final geometry and will not agree with solution reactions.

        The message warns that the moment summations may not equal the real moment reactions. When
        calculating moment summations, the :ref:`fsum` command assumes that the summation of rotations
        applies; however, it does not apply for large rotations, which require pseudovector representation
        to sum the rotations.

        In contrast, the results for force reactions will be correct because they depend upon linear
        displacement vectors (which can be added).

        **Using FSUM in a Spectrum or PSD Analysis ( ANTYPE, SPECTR)**
        When using :ref:`fsum` in a spectrum analysis (after the combination file has been input through
        :ref:`input`,,MCOM and when :ref:`spopt` has not been issued with ``Elcalc`` = YES during the
        spectrum analysis), or in a PSD analysis when postprocessing 1-sigma results (loadstep 3, 4, or 5),
        the following message will display in the printout header:

        (Spectrum analysis summation is used)

        This message means that the summation of the element nodal forces is performed prior to the
        combination of those forces. In this case, :ref:`rsys` does not apply. The forces are in the nodal
        coordinate systems, and the vector sum is always printed in the global coordinate system.

        The spectrum analysis summation is available when the element results are written to the mode file,
        :file:`Jobname.mode` ( ``MSUPkey`` = Yes on the :ref:`mxpand` command).

        Because modal displacements cannot be used to calculate contact element nodal forces, ``ITEM`` does
        not apply to spectrum and PSD analyses.
        """
        command = f"FSUM,{lab},{item}"
        return self.run(command, **kwargs)

    def hfang(
        self,
        lab: str = "",
        phi1: str = "",
        phi2: str = "",
        theta1: str = "",
        theta2: str = "",
        **kwargs,
    ):
        r"""Defines or displays spatial angles of a spherical radiation surface for sound radiation parameter
        calculations.

        Mechanical APDL Command: `HFANG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HFANG.html>`_

        Parameters
        ----------
        lab : str
            Spatial angle label.

            * ``ANGLE`` - Define spatial angles (default).

            * ``STATE`` - Display spatial angles. ``PHI1``, ``PHI2``, ``THETA1``, and ``THETA2`` are ignored.

        phi1 : str
            Starting and ending ϕ angles (degrees) in the spherical coordinate system. ``PHI1`` defaults to
            0 and ``PHI2`` defaults to 360.

        phi2 : str
            Starting and ending ϕ angles (degrees) in the spherical coordinate system. ``PHI1`` defaults to
            0 and ``PHI2`` defaults to 360.

        theta1 : str
            Starting and ending θ angles (degrees) in the spherical coordinate system. ``THETA1`` defaults
            to 0 and ``THETA2`` defaults to 180.

        theta2 : str
            Starting and ending θ angles (degrees) in the spherical coordinate system. ``THETA1`` defaults
            to 0 and ``THETA2`` defaults to 180.

        Notes
        -----

        .. _HFANG_notes:

        Defines or displays spatial angles of a spherical radiation surface.

        Use this command only with :ref:`plfar`, ``Lab`` = PRES, or :ref:`prfar`, ``Lab`` = PRES.
        """
        command = f"HFANG,{lab},{phi1},{phi2},{theta1},{theta2}"
        return self.run(command, **kwargs)

    def hfsym(
        self, kcn: str = "", xkey: str = "", ykey: str = "", zkey: str = "", **kwargs
    ):
        r"""Indicates the presence of symmetry planes for the computation of acoustic fields in the near and far
        field domains (beyond the finite element region).

        Mechanical APDL Command: `HFSYM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HFSYM.html>`_

        Parameters
        ----------
        kcn : str
            Coordinate system reference number. ``KCN`` may be 0 (Cartesian), or any previously defined
            local Cartesian coordinate system number (>10). Defaults to 0.

        xkey : str
            Key for acoustic field boundary condition, as prescribed for the solution, corresponding to the x =
            constant plane:

            * ``None`` - No sound soft or sound hard boundary conditions (default).

            * ``SSB`` - Sound soft boundary (pressure = 0).

            * ``SHB`` - Sound hard boundary (normal velocity = 0).

        ykey : str
            Key for acoustic field boundary condition, as prescribed for the solution, corresponding to the y =
            constant plane:

            * ``None`` - No sound soft or sound hard boundary conditions (default).

            * ``SSB`` - Sound soft boundary (pressure = 0).

            * ``SHB`` - Sound hard boundary (normal velocity = 0).

        zkey : str
            Key for acoustic field boundary condition, as prescribed for the solution, corresponding to the z =
            constant plane:

            * ``None`` - No sound soft or sound hard boundary conditions (default).

            * ``SSB`` - Sound soft boundary (pressure = 0).

            * ``SHB`` - Sound hard boundary (normal velocity = 0).

        Notes
        -----

        .. _HFSYM_notes:

        :ref:`hfsym` uses the image principle to indicate symmetry planes (x, y, or z = constant plane) for
        acoustic field computations outside the modeled domain. A sound hard boundary condition must be
        indicated even though it occurs as a natural boundary condition.

        No menu paths are available for acoustic applications.
        """
        command = f"HFSYM,{kcn},{xkey},{ykey},{zkey}"
        return self.run(command, **kwargs)

    def macopt(self, **kwargs):
        r"""Specifies modal assurance criterion (MAC) or frequency response function (FRF) correlation criteria
        calculation options for :ref:`rstmac`.

        Mechanical APDL Command: `MACOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MACOPT.html>`_

        **Command default:**
        If :ref:`macopt` is not issued prior to :ref:`rstmac`, node matching based on location is used by
        default in MAC calculations performed by :ref:`rstmac`. Unless otherwise specified, an absolute
        tolerance (ABSTOLN) value of 0.01 is used for the node matching.

        Notes
        -----

        .. _MACOPT_notes:

        The :ref:`rstmac` command calculates the MAC or FRF criteria values based on the options specified
        via :ref:`macopt`. The :ref:`macopt` command must be issued before the :ref:`rstmac` command. These
        commands enable you to compare nodal solutions from two results files ( :file:`.rst` or
        :file:`.rstp` ) or from one results file and one Universal Format file ( :file:`.unv` ). Multiple
        :ref:`macopt` commands can be issued to specify which results are compared and how.

        As listed in the table above, model solutions can be compared using three different mehtods:
        matching nodes based on location, matching nodes based on node number, or by node mapping and
        solution interpolation.

        When node mapping and solution interpolation is performed ( ``Option`` = NODMAP), the following
        applies:

        * ``File1`` on :ref:`rstmac` must correspond to a model meshed in solid and/or shell elements. Other
          types of elements can be present, but the node mapping is not performed for these elements.

        * You should only compare solutions of models having the same dimension (both models are 2D or both
          models are 3D). Comparing models with different dimensions may lead to incorrect results if the
          solution at mapped/matched nodes is not representative of the global solution.

        * Interpolation is performed on UX, UY, and UZ degrees of freedom.

        Node pair MAC computation ( ``Option`` = NMAC) is only supported when a matching procedure is used
        and a specific substep number is requested for each solution ( ``Sbstep1``, ``Sbstep2`` on
        :ref:`rstmac` command).

        Non-structural degrees of freedom in coupled-field analyses are supported for the matching methods (
        ``Option`` = ABSTOLN or NUMMATCH). Multiple :ref:`macopt`, DOF commands can be issued consecutively
        to combine different degrees of freedom.

         .. _MACOPT_FRF:

        The FRF option is not compatible with any MAC calculation options (DOF, NMAC and KEYMASS) and can
        only be used with node matching procedures.

        **Example Usage**

        .. _MACOPT_example:

        For a detailed discussion on using :ref:`macopt` with examples, see `Comparing Nodal Solutions From
        Two Models or From One Model and Experimental Data (RSTMAC)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#>`_
        """
        command = "MACOPT"
        return self.run(command, **kwargs)

    def nforce(self, item: str = "", **kwargs):
        r"""Sums the nodal forces and moments of elements attached to nodes.

        Mechanical APDL Command: `NFORCE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NFORCE.html>`_

        Parameters
        ----------
        item : str
            Specifies the selected set of nodes for summing forces and moments for contact elements.

            * ``(blank)`` - Sums the nodal forces of elements for all selected nodes and excludes contact
              elements (elements 169-177).

            * ``CONT`` - Sums the nodal forces of elements for contact nodes only.

            * ``BOTH`` - Sums the nodal forces of elements for all selected nodes, including contact elements.

        Notes
        -----

        .. _NFORCE_notes:

        Sums and prints, in each component direction for each selected node, the nodal force and moment
        contributions of the selected elements attached to the node. If all elements are selected, the sums
        are usually zero except where constraints or loads are applied. The nodal forces and moments may be
        displayed ( :ref:`pbc`,FORC and :ref:`pbc`,MOME). Use :ref:`presol` to print nodal forces and
        moments on an element-by-element basis. You can use the :ref:`force` command to specify which
        component (static, damping, inertia, or total) of the nodal load is to be used. Nodal forces
        associated with surface loads are not included.

        This vector sum is printed in the global Cartesian system. Moment summations are about the global
        origin unless another point is specified with the :ref:`spoint` command. The summations for each
        node are printed in the global Cartesian system unless transformed ( :ref:`rsys` ). This command is
        generally not applicable to axisymmetric models because moment information from the NFORCE command
        is not correct for axisymmetric elements.

        Selecting a subset of elements ( :ref:`esel` ) and then issuing this command will give the forces
        and moments required to maintain equilibrium of that set of elements. The effects of nodal coupling
        and constraint equations are ignored. The option ``ITEM`` = CONT provides the forces and moments for
        the contact elements ( ``CONTA172``, ``CONTA174``, ``CONTA175``, and ``CONTA177`` ). Setting
        ``ITEM`` = BOTH provides the forces and moments for all selected nodes, including contact elements.

        This command also includes the :ref:`fsum` command function which vectorially sums and prints, in
        each component direction for the total selected node set, the nodal force and moment contributions
        of the selected elements attached to the selected node set.

        **Using NFORCE in a Spectrum or PSD Analysis ( ANTYPE, SPECTR)**
        When using :ref:`nforce` in a spectrum analysis (after the combination file has been input through
        :ref:`input`,,MCOM and when :ref:`spopt` has not been issued with ``Elcalc`` = YES during the
        spectrum analysis), or in a PSD analysis when postprocessing 1-sigma results (loadstep 3, 4, or 5),
        the following message will display in the printout header:

        (Spectrum analysis summation is used)

        This message means that the summation of the element nodal forces is performed prior to the
        combination of those forces. In this case, :ref:`rsys` does not apply. The forces are in the nodal
        coordinate systems, and the vector sum is always printed in the global coordinate system.

        The spectrum analysis summation is available when the element results are written to the mode file,
        :file:`Jobname.MODE` ( ``MSUPkey`` = Yes on the :ref:`mxpand` command).

        Because modal displacements cannot be used to calculate contact element nodal forces, ``ITEM`` does
        not apply to spectrum and PSD analyses.
        """
        command = f"NFORCE,{item}"
        return self.run(command, **kwargs)

    def nldpost(
        self,
        label: str = "",
        key: str = "",
        fileid: str = "",
        prefix: str = "",
        **kwargs,
    ):
        r"""Gets element component information from nonlinear diagnostic files.

        Mechanical APDL Command: `NLDPOST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLDPOST.html>`_

        Parameters
        ----------
        label : str
            Specifies the type of command operation:

            * ``EFLG`` - Element flag for nonlinear diagnostics.

            * ``NRRE`` - Newton-Raphson residuals.

        key : str
            Specifies the command action:

            * ``STAT`` - List information about the diagnostic files ( :file:`Jobname.ndxxx` or
              :file:`Jobname.nrxxx` ) in the current directory.

              For ``Label`` = EFLG, the listing gives a summary that associates the loadstep, substep, time,
              equilibrium iteration number, cumulative iteration number, and the number of elements that fail each
              criteria with a specific file ID ( :file:`Jobname.ndxxx` ). Use the list to create element
              components (via the CM option) based on the cumulative iteration number.

              For ``Label`` = NRRE, the listing provides a summary that associates the loadstep, substep, time,
              equilibrium iteration number, and cumulative iteration number with a specific file ID (
              :file:`Jobname.nrxxx` ). Use the list to identify the respective file ID for creating Newton-Raphson
              residual contour plots ( :ref:`plnsol`,NRRE,..., ``FileID`` ).

            * ``DEL`` - Delete :file:`Jobname.ndxxx` or :file:`Jobname.nrxxx` files in the working directory, if
              any exist.

            * ``CM`` - Create components for elements that violate criteria. This value is valid only when
              ``Label`` = EFLG.

        fileid : str
            Valid only when ``Label`` = EFLG and ``Key`` = CM, this value specifies file IDs:

            * ``IDnum`` - The file ID number. Creates the element components from the diagnostic files
              corresponding to the specified file ID number in the working directory.

            * ``ALL`` - Creates element components from all available diagnostic files residing in the working
              directory. This value is the default if you do not specify an ``IDnum`` value.

        prefix : str
            Sets the prefix name for components. Specify up to 21 alphanumeric characters.

        Notes
        -----

        .. _NLDPOST_notes:

        Based on the nonlinear diagnostic results (created via the :ref:`nldiag`,EFLG command), the
        :ref:`nldpost` command creates element components with predefined names.

        The following table lists the diagnostic criteria and component names (with specified prefix and
        without). Here ``xxx`` corresponds to the file ID ( ``FileID`` ) of :file:`Jobname.ndxxx` or
        :file:`Jobnamenrxxx`.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        If you have trouble viewing specific element components, see `Viewing Hidden Element Components
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS7_4.html#>`_

        For more information, see Performing Nonlinear Diagnostics.
        """
        command = f"NLDPOST,{label},{key},{fileid},{prefix}"
        return self.run(command, **kwargs)

    def plas(
        self,
        lab: str = "",
        ldstep: str = "",
        substep: str = "",
        freqb: str = "",
        freqe: str = "",
        logopt: str = "",
        plottype: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        **kwargs,
    ):
        r"""Plots a specified acoustic quantity during postprocessing of an acoustic analysis.

        Mechanical APDL Command: `PLAS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLAS.html>`_

        Parameters
        ----------
        lab : str
            The acoustic quantity to calculate:

            * ``SIMP`` - Specific acoustic impedance on the selected surface.

            * ``AIMP`` - Acoustic impedance on the selected surface.

            * ``MIMP`` - Mechanical impedance on the selected surface.

            * ``PRES`` - Average pressure on the selected surface.

            * ``FORC`` - Force on the selected surface.

            * ``POWE`` - Acoustic power on the selected surface.

            * ``ERP`` - Equivalent radiated power on the selected structural surface (valid only for
              ``SHELL181``, ``SOLID185``, ``SOLID186``, ``SOLID187``, ``SOLSH190``, ``SOLID225``, ``SOLID226``,
              ``SOLID227``, and ``SHELL281`` ).

            * ``ERPL`` - Equivalent radiated power level on the selected structural surface (valid only for
              ``SHELL181``, ``SOLID185``, ``SOLID186``, ``SOLID187``, ``SOLSH190``, ``SOLID225``, ``SOLID226``,
              ``SOLID227``, and ``SHELL281`` ).

            * ``BSPL`` - Frequency-band sound pressure level on selected nodes.

            * ``BSPA`` - A-weighted frequency-band sound pressure level on selected nodes.

            * ``MENE`` - Acoustic potential energy on the selected elements.

            * ``KENE`` - Acoustic kinetic energy on the selected elements.

            * ``TENE`` - Acoustic total energy on the selected elements.

            * ``PL2V`` - Average square of the L2 norm of pressure on the selected elements.

            * ``LWIN`` - Input sound power level on defined port.

            * ``LWOUT`` - Output sound power level on defined driven port.

            * ``RL`` - Return loss on defined port.

            * ``ALPHA`` - Absorption coefficient on defined port.

            * ``TL`` - Transmission loss on defined ports.

            * ``DFSTL`` - Transmission loss of random acoustic analysis.

            * ``DFSPW`` - Radiated power in random acoustic analysis.

        ldstep : str
            Specified load step. Defaults to the load step number specified on the :ref:`set` command, or defaults to 1 if :ref:`set` has not been issued. This default applies to all ``Lab`` values except DFSTL and DFSPW.

            * ``n`` - Load step number.

            * ``ALL`` - All load steps.

            * ``AVG or 0`` - Average result of multiple samplings in a random acoustic analysis (see the
              :ref:`msolve` command). This option is used only for ``Lab`` = DFSTL and DFSPW, and it is the
              default for these labels.

        substep : str
            Specified substep. Defaults to the substep number specified on the :ref:`set` command, or defaults to ALL (all substeps at the specified load step) if :ref:`set` has not been issued. For ``Lab`` = BSPL or BSPA, ALL is the only valid value.

            * ``n`` - Substep number.

            * ``ALL`` - All substeps.

        freqb : str
            Frequency value representing one of the following:

            * Beginning frequency of the frequency range ( ``FREQB`` to ``FREQE`` ) for the defined load step(s)
              and substeps ( ``SUBSTEP`` = ALL). If a ``SUBSTEP`` value is specified, ``FREQB`` is invalid.

            * Central frequency of octave bands, used when ``LogOpt`` = OB1, OB2, OB3, OB6, OB12, or OB24 and
              ``FREQE`` is blank.

        freqe : str
            Ending frequency of the frequency range ( ``FREQB`` to ``FREQE`` ) for the defined load step(s)
            and substeps ( ``SUBSTEP`` = ALL). If blank, ``FREQE`` is set to ``FREQB``. If a ``SUBSTEP``
            value is specified, ``FREQE`` is invalid.

        logopt : str
            Octave bands:

            * ``OB0`` - Narrow bands (default).

            * ``OB1`` - Octave bands.

            * ``OB2`` - 1/2 octave bands.

            * ``OB3`` - 1/3 octave bands.

            * ``OB6`` - 1/6 octave bands.

            * ``OB12`` - 1/12 octave bands.

            * ``OB24`` - 1/24 octave bands.

        plottype : str
            Type of plot:

            * ``LINE`` - Line plot (default).

            * ``BAR`` - Bar pattern plot, used only for ``Lab`` = BSPL or BSPA.

            * ``CONT`` - Waterfall diagram, used only for ``Lab`` = ERP or ERPL.

        val1 : str
            Input port number for ``Lab`` = LWIN, LWOUT, RL, ALPHA, or TL.

        val2 : str
            Output port number for ``Lab`` = TL.

        val3 : str
            Reference power for ``Lab`` = LWIN, LWOUT, or EPRL (defaults to 1x10 :sup:`-12` W).

        val4 : str
            Fluid mass density for ``Lab`` = ERP or ERPL (defaults to 1.2041 kg/m :sup:`3` ).

        val5 : str
            Speed of sound in the fluid for ``Lab`` = ERP or ERPL (defaults to 343.25 m/s).

        val6 : str
            Radiation efficiency for ``Lab`` = ERP or ERPL (defaults to 1).

        Notes
        -----
        The :ref:`plas` command plots the specified acoustic quantity on the selected exterior surface, the
        energy on selected elements, or the sound pressure level over frequency bands. The calculation is
        based on the pressure and velocity solution or the frequency-band sound pressure level (SPL).

        The total pressure and velocity are used if the selected surface is the excitation source surface.
        To calculate the incoming and outgoing acoustic power and other sound power parameters on the input
        and output surfaces, issue the :ref:`sf`,,PORT command in the preprocessor to define port numbers.

        The sound pressure level of the octave bands and general frequency band (defined via the
        :ref:`harfrq` command) is calculated at the selected nodes in the model.
        """
        command = f"PLAS,{lab},{ldstep},{substep},{freqb},{freqe},{logopt},{plottype},{val1},{val2},{val3},{val4},{val5},{val6}"
        return self.run(command, **kwargs)

    def plcamp(
        self,
        option: str = "",
        slope: str = "",
        unit: str = "",
        freqb: str = "",
        cname: str = "",
        stabval: int | str = "",
        keyallfreq: str = "",
        keynegfreq: str = "",
        **kwargs,
    ):
        r"""Plots Campbell diagram data for applications involving rotating structure dynamics.

        Mechanical APDL Command: `PLCAMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLCAMP.html>`_

        Parameters
        ----------
        option : str
            Flag to activate or deactivate sorting of forward or backward whirl frequencies:

            * ``0 (OFF, or NO)`` - No sorting.

            * ``1 (ON, or YES)`` - Sort. This value is the default.

        slope : str
            The slope of the line to be printed. This value must be positive.

            * ``SLOPE > 0`` - In the stationary reference frame ( ``RefFrame`` = YES on the :ref:`coriolis`
              command), the line represents the number of excitations per revolution of the rotor. For example,
              ``SLOPE`` = 1 represents one excitation per revolution, usually resulting from unbalance.

              In the rotating reference frame ( ``RefFrame`` = NO on the :ref:`coriolis` command), the line
              represents the number of excitations per revolution of the rotor minus 1.

            * ``SLOPE = 0`` - The line represents the stability threshold for stability values or logarithmic
              decrements printout ( ``STABVAL`` = 1, 2, or 3 )

        unit : str
            Specifies the unit of measurement for rotational angular velocities:

            * ``RDS`` - Rotational angular velocities in radians per second (rad/s). This value is the default.

            * ``RPM`` - Rotational angular velocities in revolutions per minute (RPMs).

        freqb : str
            The beginning, or lower end, of the frequency range of interest. The default is zero.

        cname : str
            The rotating component name.

        stabval : int or str
            Flag to plot the stability values:

            * ``0 (OFF, or NO)`` - Plot the frequencies (the imaginary parts of the eigenvalues in Hz). This
              value is the default.

            * ``1 (ON, or YES)`` - Plot the stability values (the real parts of the eigenvalues in Hz).

            * ``2`` - Plot the inverse of the logarithmic decrements. A negative logarithmic decrement indicates
              stable motion.

            * ``3`` - Plot the logarithmic decrements. A positive logarithmic decrement indicates stable motion
              and is consistent with API (American Petroleum Institute) standards.

            For more information about complex eigenmodes and corresponding logarithmic decrements, see `Complex
            Eigensolutions
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool13.html#eq1c0f3d38-81fe-4aa4-860a-7a20afad6c74>`_
            in the `Mechanical APDL Theory Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_.

        keyallfreq : str
            Key to specify if all frequencies above FREQB are plotted:

            * ``0 (OFF, or NO)`` - A maximum of 10 frequencies are plotted. This value is the default.

            * ``1 (ON, or YES)`` - All frequencies are plotted.

        keynegfreq : str
            Key to specify if the negative frequencies are plotted. It only applies to solutions obtained with
            the damped eigensolver ( ``Method`` = DAMP on the :ref:`modopt` command):

            * ``0 (OFF, or NO)`` - Only positive frequencies are plotted. This value is the default.

            * ``1 (ON, or YES)`` - Negative and positive frequencies are plotted.

        Notes
        -----
        The following items are required when generating a Campbell diagram:

        * Activate the Coriolis effect ( :ref:`coriolis` command) in the solution phase ( :ref:`slashsolu`
          ).

        * Run a modal analysis using the QR damped ( :ref:`modopt`,QRDAMP) or damped ( :ref:`modopt`,DAMP)
          method. Complex eigenmodes are necessary ( :ref:`modopt`,QRDAMP, ``Cpxmod`` = ON), and you must
          specify the number of modes to expand ( :ref:`mxpand` ).

        * Define two or more load step results with an ascending order of rotational velocity ( :ref:`omega`
          or :ref:`cmomega` ).

        In some cases where modes are not in the same order from one load step to the other, sorting the
        frequencies ( ``Option`` = 1) can help to obtain a correct plot. Sorting is based on the comparison
        between complex mode shapes calculated at two successive load steps.

        At each load step, the application compares the mode shape to the loads at other load steps to
        determine whirl direction at the load step. If applicable, a label appears (in the plot legend)
        representing each whirl mode (BW for backward whirl and FW for forward whirl).

        At each load step, the program checks for instability (based on the sign of the real part of the
        eigenvalue). The labels "stable" or "unstable" appear in the plot legend for each frequency curve.

        The rotational velocities of a named component ( ``Cname`` ) are displayed on the X-axis.

        For information on plotting a Campbell diagram for a prestressed structure, see `Solving for a
        Subsequent Campbell Analysis of a Prestressed Structure Using the Linear Perturbation Procedure
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTSOLPRESTRESS.html#rotdynsolu_CampbellPrestr>`_

        For a usage example of the :ref:`plcamp` command, see `Campbell Diagram
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTCAMPDIAGS.html#rotgencamp2a>`_

        Damped modal cyclic symmetry ( :ref:`cyclic` ) analyses do not support the :ref:`plcamp` command.
        """
        command = f"PLCAMP,{option},{slope},{unit},{freqb},{cname},{stabval},{keyallfreq},{keynegfreq}"
        return self.run(command, **kwargs)

    def plcfreq(self, spec: str = "", sectbeg: str = "", sectend: str = "", **kwargs):
        r"""Plots the frequency response for the given :ref:`cycspec` specification.

        Mechanical APDL Command: `PLCFREQ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLCFREQ.html>`_

        Parameters
        ----------
        spec : str
            :ref:`cycspec` specification number (ordered 1 to N in the order input; use :ref:`cycspec`,LIST
            to view the current list order). Defaults to 1.

        sectbeg : str
            Beginning sector number to plot. Defaults to 1.

        sectend : str
            Ending sector number to plot. Defaults to the total number of sectors expanded (
            :ref:`cycexpand` ).

        Notes
        -----

        .. _PLCFREQ_notes:

        Following a cyclic mode-superposition harmonic analysis, this command plots the result item given by
        a :ref:`cycspec` specification versus the harmonic frequency, one curve for each of the specified
        sectors. A :ref:`cyccalc` command must have been issued prior to this command.
        """
        command = f"PLCFREQ,{spec},{sectbeg},{sectend}"
        return self.run(command, **kwargs)

    def plchist(self, spec: str = "", freqpt: str = "", **kwargs):
        r"""Plots a histogram of the frequency response of each sector for the given :ref:`cycspec`
        specification.

        Mechanical APDL Command: `PLCHIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLCHIST.html>`_

        Parameters
        ----------
        spec : str
            :ref:`cycspec` specification number (ordered 1 to N in the order input; use :ref:`cycspec`,LIST
            to view the current list order). Defaults to 1.

        freqpt : str
            Harmonic frequency point to plot (the data set number NSET or CUMULATIVE on :ref:`set`,LIST).
            Defaults to the current :ref:`set` frequency.

        Notes
        -----

        .. _PLCHIST_notes:

        Following a cyclic mode-superposition harmonic analysis, this command creates a histogram plot of
        the result item given by a :ref:`cycspec` specification versus the sector number. A :ref:`cyccalc`
        command must have been issued prior to this command.
        """
        command = f"PLCHIST,{spec},{freqpt}"
        return self.run(command, **kwargs)

    def plfar(
        self,
        lab: str = "",
        option: str = "",
        var1b: str = "",
        var1e: str = "",
        nvar1: str = "",
        var2b: str = "",
        var2e: str = "",
        nvar2: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        ldstep: str = "",
        substep: str = "",
        freqb: str = "",
        freqe: str = "",
        plottype: str = "",
        logopt: str = "",
        **kwargs,
    ):
        r"""Plots pressure far fields and far-field parameters.

        Mechanical APDL Command: `PLFAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLFAR.html>`_

        Parameters
        ----------
        lab : str
            Parameters to plot :

            * ``PRES`` - Acoustic parameters

            * ``PROT`` - Acoustic parameters with the y-axis rotated extrusion (not valid for 2D elements)

            * ``PLAT`` - Acoustic parameters radiated by a vibrating structural panel (not valid for 2D
              elements)

        option : str
            Plot option, based on the specified plot parameter type:

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        var1b : str
            Starting and ending values for the first variable associated with ``PlotType`` as described
            below.

            When ``PlotType`` = blank (default) or SPHR: Starting and ending phi (φ) angles (in degrees) in
            the spherical coordinate system. Defaults to 0.

            When ``PlotType`` = PLXY: Starting and ending x value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PlotType`` = PLYZ: Starting and ending y value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PlotType`` = PLXZ: Starting and ending x value in the Cartesian coordinate system.
            Defaults to 0.

        var1e : str
            Starting and ending values for the first variable associated with ``PlotType`` as described
            below.

            When ``PlotType`` = blank (default) or SPHR: Starting and ending phi (φ) angles (in degrees) in
            the spherical coordinate system. Defaults to 0.

            When ``PlotType`` = PLXY: Starting and ending x value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PlotType`` = PLYZ: Starting and ending y value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PlotType`` = PLXZ: Starting and ending x value in the Cartesian coordinate system.
            Defaults to 0.

        nvar1 : str
            Number of divisions between the starting and ending ``VAR1`` values for data computations.
            Defaults to 0.

        var2b : str
            Starting and ending values for the second variable associated with ``PlotType`` as described
            below.

            When ``PlotType`` = blank (default) or SPHR: Starting and ending theta (θ) angles (in degrees)
            in the spherical coordinate system. Defaults to 0 for a 3D model and 90 for a 2D extrusion
            model.

            When ``PlotType`` = PLXY: Starting and ending y value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PlotType`` = PLYZ: Starting and ending z value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PlotType`` = PLXZ: Starting and ending z value in the Cartesian coordinate system.
            Defaults to 0.

        var2e : str
            Starting and ending values for the second variable associated with ``PlotType`` as described
            below.

            When ``PlotType`` = blank (default) or SPHR: Starting and ending theta (θ) angles (in degrees)
            in the spherical coordinate system. Defaults to 0 for a 3D model and 90 for a 2D extrusion
            model.

            When ``PlotType`` = PLXY: Starting and ending y value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PlotType`` = PLYZ: Starting and ending z value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PlotType`` = PLXZ: Starting and ending z value in the Cartesian coordinate system.
            Defaults to 0.

        nvar2 : str
            Number of divisions between the starting and ending ``VAR2`` values for data computations.
            Defaults to 0.

        val1 : str
            ``VAL1`` is additional input. Its meaning depends on the ``PlotType`` argument as described
            below.

            When ``PlotType`` = blank (default) or SPHR: Radius of the sphere surface.

            When ``PlotType`` = PLXY: Fixed z value for an X-Y plane in the Cartesian coordinate system.
            Defaults to 0.

            When ``PlotType`` = PLYZ: Fixed x value for a Y-Z plane in the Cartesian coordinate system.
            Defaults to 0.

            When ``PlotType`` = PLXZ: Fixed y value for an X-Z plane in the Cartesian coordinate system,
            Defaults to 0.

        val2 : str
            When ``Option`` = SPLC, SPLP, SPAC, or SPAP: Reference rms sound pressure. Defaults to 2x10
            :sup:`-5` Pa.

            When ``Option`` = PWL: Reference sound power. Defaults to 1x10 :sup:`-12` watts.

        val3 : str
            When ``Lab`` = PRES: Thickness of 2D model extrusion in the z direction (no default).

            When ``Lab`` = PROT: Angle of the y-axis rotated extrusion model (no default).

        val4 : str
            When ``Lab`` = PLAT: Mass density of acoustic fluid.

        val5 : str
            When ``Lab`` = PLAT: Sound speed in acoustic fluid.

        ldstep : str
            Specified load step. Defaults to the load step number specified on the :ref:`set` command, or defaults to 1 if :ref:`set` has not been issued.

            * ``n`` - Load step number.

            * ``ALL`` - All load steps.

        substep : str
            Specified substep. Defaults to the substep number specified on the :ref:`set` command, or defaults to ALL (all substeps at the specified load step) if :ref:`set` has not been issued.

            * ``n`` - Substep number.

            * ``ALL`` - All substeps.

        freqb : str
            Frequency value representing one of the following:

            * Beginning frequency of the frequency range ( ``FREQB`` to ``FREQE`` ) for the defined load step(s)
              and substeps ( ``SUBSTEP`` = ALL). If a ``SUBSTEP`` value is specified, ``FREQB`` is invalid.

            * Central frequency of octave bands, used when ``LogOpt`` = OB1, OB2, OB3, OB6, OB12, or OB24 and
              ``FREQE`` is blank.

        freqe : str
            Ending frequency of the frequency range ( ``FREQB`` to ``FREQE`` ) for the defined load step(s)
            and substeps ( ``SUBSTEP`` = ALL). If blank, ``FREQE`` is set to ``FREQB``. If a ``SUBSTEP``
            value is specified, ``FREQE`` is invalid.

        plottype : str
            Type of plot:

            * ``ANGX`` - x-y chart with angle as the x-axis variable (default).

            * ``FRQX`` - x-y chart with frequency as the x-axis variable.

            * ``CONT`` - Waterfall diagram of a field parameter with variables (frequency, angle).

            * ``MRPM`` - Waterfall diagram of a field parameter with variables (frequency, RPM).

            * ``PLXY`` - Contour plot on an X-Y plane.

            * ``PLYZ`` - Contour plot on a Y-Z plane.

            * ``PLXZ`` - Contour plot on an X-Z plane.

            * ``SPHR`` - Contour plot on a sphere surface.

        logopt : str
            Octave bands (used only when Option = SPLC, SPLP, SPAC, SPAP, or PWL) :

            * ``OB0`` - Narrow bands (default).

            * ``OB1`` - Octave bands.

            * ``OB2`` - 1/2 octave bands.

            * ``OB3`` - 1/3 octave bands.

            * ``OB6`` - 1/6 octave bands.

            * ``OB12`` - 1/12 octave bands.

            * ``OB24`` - 1/24 octave bands.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLFAR.html>`_
           for further explanations.

        .. _PLFAR_notes:

        The :ref:`plfar` command plots pressure far fields and far-field parameters as determined by the
        equivalent source principle. Use this command to plot pressure and acoustic parameters. See the
        :ref:`hfsym` command for the model symmetry and the :ref:`hfang` command for spatial radiation
        angles.

        Plotting acoustic parameters radiated by a vibrating structural panel ( ``Lab`` = PLAT) is supported
        by elements ``SOLID185``, ``SOLID186``, ``SOLID187``, ``SHELL181``, ``SHELL281``, and ``SOLSH190``.
        The vibration surface of the panel must be flagged by the :ref:`sf`,,MXWF command.

        A maximum of ten curves can be plotted on a 2D chart.

        The waterfall diagram is plotted only in Cartesian coordinates.
        """
        command = f"PLFAR,{lab},{option},{var1b},{var1e},{nvar1},{var2b},{var2e},{nvar2},{val1},{val2},{val3},{val4},{val5},{ldstep},{substep},{freqb},{freqe},{plottype},{logopt}"
        return self.run(command, **kwargs)

    def plmc(
        self,
        lstep: str = "",
        sbstep: str = "",
        timfrq: str = "",
        kimg: int | str = "",
        hibeg: str = "",
        hiend: str = "",
        **kwargs,
    ):
        r"""Plots the modal coordinates from a mode-superposition solution.

        Mechanical APDL Command: `PLMC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLMC.html>`_

        Parameters
        ----------
        lstep : str
            Plot the solution identified as load step ``LSTEP`` and substep ``SBSTEP``

        sbstep : str
            Plot the solution identified as load step ``LSTEP`` and substep ``SBSTEP``

        timfrq : str
            As an alternative to ``LSTEP`` and ``SBSTEP``, plot the solution at the time value ``TIMFRQ``
            (for :ref:`antype`,TRANS) or frequency value ``TIMFRQ`` (for :ref:`antype`,HARMIC). ``LSTEP``
            and ``SBSTEP`` should be left blank.

        kimg : int or str
            Key for plotting real or imaginary solution. Valid only for :ref:`antype`,HARMIC.

            * ``0 (or blank)`` - Plot the real solution (default).

            * ``1`` - Plot the imaginary solution.

            * ``2`` - Plot the amplitude.

        hibeg : str
            For cyclic symmetry solutions, plot the solutions in the harmonic index solution range ``HIbeg``
            to ``HIend``. Defaults to all harmonic indices (all modes).

        hiend : str
            For cyclic symmetry solutions, plot the solutions in the harmonic index solution range ``HIbeg``
            to ``HIend``. Defaults to all harmonic indices (all modes).

        Notes
        -----

        .. _PLMC_notes:

        :ref:`plmc` plots a histogram of the modal coordinates (the factors which modes may be multiplied by
        to obtain their contribution to the response) at a certain time point (transient analyses) or
        frequency point (harmonic analyses). The absolute values of the modal coordinates are plotted. Use
        :ref:`xrange` to plot only modes in a certain range, if desired.

        For transient analyses, a :file:`.rdsp` None file must be available. For harmonic analyses, a
        :file:`.rfrq` None file must be available. The content of these files depends on the :ref:`outres`
        command settings. Note that the default for mode-superposition transient analysis is to write the
        reduced displacement file every 4th substep. For more information, see Command Default in the
        :ref:`outres` command description.

        For a cyclic harmonic mode-superposition analysis, use the :ref:`cycfiles` command to identify the
        :file:`.rfrq` None and modal :file:`.rst` None file. For other analyses, use the ``FILE`` command to
        specify the :file:`.rdsp` or :file:`.rfrq` file.

        You may limit the plot to display only those modes in a certain harmonic index range. The modes
        having the same harmonic index are each plotted in a unique color. If there are less than 10
        harmonic indices, they are identified in the graphics legend.

        This is a graphical representation of the optional :file:`Jobname.mcf` text file (see the
        :ref:`trnopt` and :ref:`hropt` commands). To print the modal coordinates, use the :ref:`prmc`
        command. For more information on modal coordinates, see `Mode-Superposition Method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool9.html#thy_antools_resresp>`_
        in the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_.

        **Example Usage**

        .. _PLMC_examples:

        `Example Mode-Superposition Harmonic Cyclic Symmetry Analysis with Mistuning
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_ex_msupharm.html#cycsym_ex_msupharm_steps>`_

        Example: Forced Response with Mistuning and Aero Coupling
        """
        command = f"PLMC,{lstep},{sbstep},{timfrq},{kimg},{hibeg},{hiend}"
        return self.run(command, **kwargs)

    def plnear(
        self,
        lab: str = "",
        opt: str = "",
        kcn: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        val9: str = "",
        **kwargs,
    ):
        r"""Plots the pressure in the near zone exterior to the equivalent source surface.

        Mechanical APDL Command: `PLNEAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLNEAR.html>`_

        Parameters
        ----------
        lab : str
            Plot the maximum pressure or sound pressure level:

            * ``SPHERE`` - on the spherical structure

            * ``PATH`` - along the path

        opt : str
            * ``PSUM`` - Maximum complex pressure for acoustics.

            * ``PHAS`` - Phase angle of complex pressure for acoustics.

            * ``SPL`` - Sound pressure level for acoustics.

            * ``SPLA`` - A-weighted sound pressure level for acoustics (dBA).

        kcn : str
            KCN is the coordinate system reference number. It may be 0 (Cartesian) or any previously defined
            local coordinate system number (>10). Defaults to 0.

        val1 : str
            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`plnear` computes the electric field or pressure for the path data
            points for the path currently defined by the :ref:`path` and :ref:`ppath` commands.

        val2 : str
            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`plnear` computes the electric field or pressure for the path data
            points for the path currently defined by the :ref:`path` and :ref:`ppath` commands.

        val3 : str
            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`plnear` computes the electric field or pressure for the path data
            points for the path currently defined by the :ref:`path` and :ref:`ppath` commands.

        val4 : str
            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`plnear` computes the electric field or pressure for the path data
            points for the path currently defined by the :ref:`path` and :ref:`ppath` commands.

        val5 : str
            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`plnear` computes the electric field or pressure for the path data
            points for the path currently defined by the :ref:`path` and :ref:`ppath` commands.

        val6 : str
            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`plnear` computes the electric field or pressure for the path data
            points for the path currently defined by the :ref:`path` and :ref:`ppath` commands.

        val7 : str
            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`plnear` computes the electric field or pressure for the path data
            points for the path currently defined by the :ref:`path` and :ref:`ppath` commands.

        val8 : str
            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`plnear` computes the electric field or pressure for the path data
            points for the path currently defined by the :ref:`path` and :ref:`ppath` commands.

        val9 : str
            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`plnear` computes the electric field or pressure for the path data
            points for the path currently defined by the :ref:`path` and :ref:`ppath` commands.

        Notes
        -----

        .. _PLNEAR_notes:

        :ref:`plnear` uses the equivalent source principle to calculate the pressure in the near zone
        exterior to the equivalent source surface (flagged with the Maxwell surface flag in the
        preprocessor) for one of the following locations:

        * A spherical surface in the KCN coordinate system

        * A path defined by the :ref:`path` and :ref:`ppath` commands

        To plot the pressure results for a path, use the :ref:`plpagm` or :ref:`plpath` commands. See the
        :ref:`hfsym` command for the model symmetry.

        To retrieve saved equivalent source data, issue the :ref:`set`, ``Lstep``, ``Sbstep``,,REAL command.
        """
        command = f"PLNEAR,{lab},{opt},{kcn},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9}"
        return self.run(command, **kwargs)

    def plzz(self, rotvel: str = "", deltarotvel: str = "", **kwargs):
        r"""Plots the interference diagram from a cyclic modal analysis.

        Mechanical APDL Command: `PLZZ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLZZ.html>`_

        Parameters
        ----------
        rotvel : str
            Rotational speed in revolutions per minute (RPM) used to define the speed line. If blank, use
            the rotational speed (from :ref:`omega` ) specified in the prestressing step of the linear
            perturbation analysis. If explicitly input as 0, or if the linear perturbation was not used, no
            speed lines are plotted.

        deltarotvel : str
            Adds speed lines about the ``RotVel`` speed line corresponding to ``RotVel`` ± ``DeltaRotVel``.
            Only plotted if ``RotVel`` is known.

        Notes
        -----

        .. _PLZZ_notes:

        :ref:`plzz` plots the cyclic modal frequencies as points on a frequency vs. harmonic index (nodal
        diameter) graph. If rotational speed ( ``RotVel`` ) is provided, the speed line is also plotted,
        leading to the interference diagram (also known as the SAFE or ZZENF diagram). If ``DeltaRotVel`` is
        also provided, two additional speed lines are plotted, enveloping the safe speed line itself.

        For more information, see `Postprocessing a Modal Cyclic Symmetry Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycmodalans.html#>`_
        """
        command = f"PLZZ,{rotvel},{deltarotvel}"
        return self.run(command, **kwargs)

    def pras(
        self,
        lab: str = "",
        ldstep: str = "",
        substep: str = "",
        freqb: str = "",
        freqe: str = "",
        logopt: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        **kwargs,
    ):
        r"""Prints a specified acoustic quantity during postprocessing of an acoustic analysis.

        Mechanical APDL Command: `PRAS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRAS.html>`_

        Parameters
        ----------
        lab : str
            The acoustic quantity to calculate:

            * ``SIMP`` - Specific acoustic impedance on the selected surface.

            * ``AIMP`` - Acoustic impedance on the selected surface.

            * ``MIMP`` - Mechanical impedance on the selected surface.

            * ``PRES`` - Average pressure on the selected surface.

            * ``FORC`` - Force on the selected surface.

            * ``POWE`` - Acoustic power on the selected surface.

            * ``ERP`` - Equivalent radiated power on the selected structural surface (valid only for
              ``SHELL181``, ``SOLID185``, ``SOLID186``, ``SOLID187``, ``SOLSH190``, ``SOLID225``, ``SOLID226``,
              ``SOLID227``, and ``SHELL281`` ).

            * ``ERPL`` - Equivalent radiated power level on the selected structural surface (valid only for
              ``SHELL181``, ``SOLID185``, ``SOLID186``, ``SOLID187``, ``SOLSH190``, ``SOLID225``, ``SOLID226``,
              ``SOLID227``, and ``SHELL281`` ).

            * ``BSPL`` - Frequency-band sound pressure level on selected nodes.

            * ``BSPA`` - A-weighted frequency-band sound pressure level on selected nodes.

            * ``MENE`` - Acoustic potential energy on the selected elements.

            * ``KENE`` - Acoustic kinetic energy on the selected elements.

            * ``TENE`` - Acoustic total energy on the selected elements.

            * ``PL2V`` - Average square of the L2 norm of pressure on the selected elements.

            * ``LWIN`` - Input sound power level on defined port.

            * ``LWOUT`` - Output sound power level on defined driven port.

            * ``RL`` - Return loss on defined port.

            * ``ALPHA`` - Absorption coefficient on defined port.

            * ``TL`` - Transmission loss on defined ports.

            * ``PALL`` - All port-related parameters (LWIN, LWOUT, RL, ALPHA, TL).

            * ``DFSTL`` - Transmission loss of random acoustic analysis.

            * ``DFSPW`` - Radiated power in random acoustic analysis.

            * ``DALL`` - All random acoustic related parameters (DFSTL, DFSPW).

        ldstep : str
            Specified load step. Defaults to the load step number specified on the :ref:`set` command, or defaults to 1 if :ref:`set` has not been issued. This default applies to all ``Lab`` values except DFSTL, DFSPW, and DALL.

            * ``n`` - Load step number.

            * ``ALL`` - All load steps.

            * ``AVG or 0`` - Average result of multiple samplings in a random acoustic analysis (see the
              :ref:`msolve` command). This option is used only for ``Lab`` = DFSTL, DFSPW, and DALL, and it is the
              default for these labels.

        substep : str
            Specified substep. Defaults to the substep number specified on the :ref:`set` command, or defaults to ALL (all substeps at the specified load step) if :ref:`set` has not been issued. For ``Lab`` = BSPL or BSPA, ALL is the only valid value.

            * ``n`` - Substep number.

            * ``ALL`` - All substeps.

        freqb : str
            Frequency value representing one of the following:

            * Beginning frequency of the frequency range ( ``FREQB`` to ``FREQE`` ) for the defined load step(s)
              and substeps ( ``SUBSTEP`` = ALL). If a ``SUBSTEP`` value is specified, ``FREQB`` is invalid.

            * Central frequency of octave bands, used when ``LogOpt`` = OB1, OB2, OB3, OB6, OB12, or OB24 and
              ``FREQE`` is blank.

        freqe : str
            Ending frequency of the frequency range ( ``FREQB`` to ``FREQE`` ) for the defined load step(s)
            and substeps ( ``SUBSTEP`` = ALL). If blank, ``FREQE`` is set to ``FREQB``. If a ``SUBSTEP``
            value is specified, ``FREQE`` is invalid.

        logopt : str
            Octave bands:

            * ``OB0`` - Narrow bands (default).

            * ``OB1`` - Octave bands.

            * ``OB2`` - 1/2 octave bands.

            * ``OB3`` - 1/3 octave bands.

            * ``OB6`` - 1/6 octave bands.

            * ``OB12`` - 1/12 octave bands.

            * ``OB24`` - 1/24 octave bands.

        val1 : str
            Input port number for ``Lab`` = LWIN, LWOUT, RL, ALPHA, TL, or PALL.

        val2 : str
            Output port number for ``Lab`` = TL or PALL.

        val3 : str
            Reference power for ``Lab`` = LWIN, LWOUT, PALL or EPRL (defaults to 1x10 :sup:`-12` W).

        val4 : str
            Fluid mass density for ``Lab`` = ERP or ERPL (defaults to 1.2041 kg/m :sup:`3` ).

        val5 : str
            Speed of sound in the fluid for ``Lab`` = ERP or ERPL (defaults to 343.25 m/s).

        val6 : str
            Radiation efficiency for ``Lab`` = ERP or ERPL (defaults to 1).

        Notes
        -----
        The :ref:`pras` command lists the specified acoustic quantity on the selected exterior surface, the
        energy on selected elements, or the sound pressure level over frequency bands. The calculation is
        based on the pressure and velocity solution or the frequency-band sound pressure level (SPL).

        The total pressure and velocity are used if the selected surface is the excitation source surface.
        To calculate the incoming and outgoing acoustic power and other sound power parameters on the input
        and output surfaces, issue the :ref:`sf`,,PORT command in the preprocessor to define port numbers.

        The sound pressure level of the octave bands and general frequency band (defined via the
        :ref:`harfrq` command) is calculated at the selected nodes in the model.
        """
        command = f"PRAS,{lab},{ldstep},{substep},{freqb},{freqe},{logopt},,{val1},{val2},{val3},{val4},{val5},{val6}"
        return self.run(command, **kwargs)

    def prcamp(
        self,
        option: str = "",
        slope: str = "",
        unit: str = "",
        freqb: str = "",
        cname: str = "",
        stabval: int | str = "",
        keyallfreq: str = "",
        keynegfreq: str = "",
        keywhirl: str = "",
        **kwargs,
    ):
        r"""Prints Campbell diagram data for applications involving rotating structure dynamics.

        Mechanical APDL Command: `PRCAMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRCAMP.html>`_

        Parameters
        ----------
        option : str
            Flag to activate or deactivate sorting of forward or backward whirl frequencies:

            * ``0 (OFF, or NO)`` - No sorting.

            * ``1 (ON, or YES)`` - Sort. This value is the default.

        slope : str
            The slope of the line to be printed. This value must be positive.

            * ``SLOPE > 0`` - In the stationary reference frame ( ``RefFrame`` = YES on the :ref:`coriolis`
              command), the line represents the number of excitations per revolution of the rotor. For example,
              ``SLOPE`` = 1 represents one excitation per revolution, usually resulting from unbalance.

              In the rotating reference frame ( ``RefFrame`` = NO on the :ref:`coriolis` command), the line
              represents the number of excitations per revolution of the rotor minus 1.

            * ``SLOPE = 0`` - The line represents the stability threshold for stability values or logarithmic
              decrements printout ( ``STABVAL`` = 1, 2, or 3 )

        unit : str
            Specifies the unit of measurement for rotational angular velocities:

            * ``RDS`` - Rotational angular velocities in radians per second (rad/s). This value is the default.

            * ``RPM`` - Rotational angular velocities in revolutions per minute (RPMs).

        freqb : str
            The beginning, or lower end, of the frequency range of interest. The default is zero.

        cname : str
            The rotating component name.

        stabval : int or str
            Flag to print the stability values:

            * ``0 (OFF, or NO)`` - Print the frequencies (the imaginary parts of the eigenvalues in Hz). This
              value is the default.

            * ``1 (ON, or YES)`` - Print the stability values (the real parts of the eigenvalues in Hz).

            * ``2`` - Print the inverse of the logarithmic decrements. A negative logarithmic decrement
              indicates stable motion.

            * ``3`` - Print the logarithmic decrements. A positive logarithmic decrement indicates stable motion
              and is consistent with API (American Petroleum Institute) standards.

            For more information about complex eigenmodes and corresponding logarithmic decrements, see `Complex
            Eigensolutions
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool13.html#eq1c0f3d38-81fe-4aa4-860a-7a20afad6c74>`_
            in the `Mechanical APDL Theory Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_.

        keyallfreq : str
            Key to specify if all frequencies above FREQB are printed out:

            * ``0 (OFF, or NO)`` - A maximum of 10 frequencies are printed out. They correspond to the
              frequencies displayed via the :ref:`plcamp` command. This value is the default.

            * ``1 (ON, or YES)`` - All frequencies are printed out.

        keynegfreq : str
            Key to specify if the negative frequencies are printed out. It only applies to solutions obtained
            with the damped eigensolver ( ``Method`` =DAMP on the :ref:`modopt` command):

            * ``0 (OFF, or NO)`` - Only positive frequencies are printed out. This value is the default.

            * ``1 (ON, or YES)`` - Negative and positive frequencies are printed out.

        keywhirl : str
            Flag to print the whirl and instability keys for each load step:

            * ``0 (OFF, or NO)`` - Print the whirl for the last load step. This value is the default.

            * ``1 (ON, or YES)`` - Print the whirl and instability keys for each load step.

        Notes
        -----
        The following items are required when generating a Campbell diagram:

        * Activate the Coriolis effect ( :ref:`coriolis` command) in the solution phase ( :ref:`slashsolu`
          ).

        * Run a modal analysis using the QR damped ( :ref:`modopt`,QRDAMP) or damped ( :ref:`modopt`,DAMP)
          method. Complex eigenmodes are necessary ( :ref:`modopt`,QRDAMP, ``Cpxmod`` = ON), and you must
          specify the number of modes to expand ( :ref:`mxpand` ).

        * Define two or more load step results with an ascending order of rotational velocity ( :ref:`omega`
          or :ref:`cmomega` ).

        In some cases where modes are not in the same order from one load step to the other, sorting the
        frequencies ( ``Option`` = 1) can help to obtain a correct printout. Sorting is based on the
        comparison between complex mode shapes calculated at two successive load steps.

        At each load step, the application compares the mode shape to the loads to determine the whirl
        direction. If applicable, a label appears (on the rows of output data) representing the whirl mode
        (BW for backward whirl and FW for forward whirl).

        If you specify a non-zero slope ( ``SLOPE`` > 0), the command prints the critical speeds
        corresponding to the intersection points of the frequency curves and the added line. In the case of
        a named component ( ``Cname`` ), critical speeds relate to the rotational velocity of the component.
        Critical speeds are available only if the frequencies are printed ( STABVAL = OFF).

        If you specify a zero slope ( ``SLOPE`` = 0), the command prints the stability threshold
        corresponding to the sign change of the stability values (or logarithmic decrements). In the case of
        a named component ( ``Cname`` ), stability thresholds relate to the rotational velocity of the
        component. Stability thresholds are available only if the stability values or logarithmic decrements
        are printed ( ``STABVAL`` = 1, 2, or 3 ).

        At each load step, the program checks for instability (based on the sign of the real part of the
        eigenvalue). The label "U" appears on the printout for each unstable frequency.

        If specified, the rotational velocities of the named component ( ``Cname`` ) are printed out along
        with the natural frequencies.

        For information on printing a Campbell diagram for a prestressed structure, see `Solving for a
        Subsequent Campbell Analysis of a Prestressed Structure Using the Linear Perturbation Procedure
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTSOLPRESTRESS.html#rotdynsolu_CampbellPrestr>`_

        For a usage example of the companion command :ref:`plcamp` (used for plotting a Campbell diagram),
        see `Example: Campbell Diagram Analysis of a Simply Supported Beam
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ADVRSDSMP1.html#>`_

        For more information on Campbell diagram generation, see `Campbell Diagram
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_rot/Hlp_G_ROTCAMPDIAGS.html#rotgencamp2a>`_

        Damped modal cyclic symmetry ( :ref:`cyclic` ) analyses do not support the :ref:`prcamp` command.
        """
        command = f"PRCAMP,{option},{slope},{unit},{freqb},{cname},{stabval},{keyallfreq},{keynegfreq},{keywhirl}"
        return self.run(command, **kwargs)

    def prfar(
        self,
        lab: str = "",
        option: str = "",
        var1b: str = "",
        var1e: str = "",
        nvar1: str = "",
        var2b: str = "",
        var2e: str = "",
        nvar2: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        ldstep: str = "",
        substep: str = "",
        freqb: str = "",
        freqe: str = "",
        printtype: str = "",
        logopt: str = "",
        **kwargs,
    ):
        r"""Prints acoustic far field parameters.

        Mechanical APDL Command: `PRFAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRFAR.html>`_

        Parameters
        ----------
        lab : str
            Parameters to print:

            * ``PRES`` - Acoustic parameters

            * ``PROT`` - Acoustic parameters with the y-axis rotated extrusion (not valid for 2D elements)

            * ``PLAT`` - Acoustic parameters radiated by a vibrating structural panel (not valid for 2D
              elements)

        option : str
            Print option, based on the specified print parameter type:

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        var1b : str
            Starting and ending values for the first variable associated with ``PrintType`` as described
            below.

            When ``PrintType`` = blank (default) or SPHR: Starting and ending phi (φ) angles (in degrees) in
            the spherical coordinate system. Defaults to 0.

            When ``PrintType`` = PLXY: Starting and ending x value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PrintType`` = PLYZ: Starting and ending y value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PrintType`` = PLXZ: Starting and ending x value in the Cartesian coordinate system.
            Defaults to 0.

        var1e : str
            Starting and ending values for the first variable associated with ``PrintType`` as described
            below.

            When ``PrintType`` = blank (default) or SPHR: Starting and ending phi (φ) angles (in degrees) in
            the spherical coordinate system. Defaults to 0.

            When ``PrintType`` = PLXY: Starting and ending x value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PrintType`` = PLYZ: Starting and ending y value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PrintType`` = PLXZ: Starting and ending x value in the Cartesian coordinate system.
            Defaults to 0.

        nvar1 : str
            Number of divisions between the starting and ending ``VAR1`` values for data computations.
            Defaults to 0.

        var2b : str
            Starting and ending values for the second variable associated with ``PrintType`` as described
            below.

            When ``PrintType`` = blank (default) or SPHR: Starting and ending theta (θ) angles (in degrees)
            in the spherical coordinate system. Defaults to 0 for a 3D model and 90 for a 2D extrusion
            model.

            When ``PrintType`` = PLXY: Starting and ending y value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PrintType`` = PLYZ: Starting and ending z value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PrintType`` = PLXZ: Starting and ending z value in the Cartesian coordinate system.
            Defaults to 0.

        var2e : str
            Starting and ending values for the second variable associated with ``PrintType`` as described
            below.

            When ``PrintType`` = blank (default) or SPHR: Starting and ending theta (θ) angles (in degrees)
            in the spherical coordinate system. Defaults to 0 for a 3D model and 90 for a 2D extrusion
            model.

            When ``PrintType`` = PLXY: Starting and ending y value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PrintType`` = PLYZ: Starting and ending z value in the Cartesian coordinate system.
            Defaults to 0.

            When ``PrintType`` = PLXZ: Starting and ending z value in the Cartesian coordinate system.
            Defaults to 0.

        nvar2 : str
            Number of divisions between the starting and ending ``VAR2`` values for data computations.
            Defaults to 0.

        val1 : str
            ``VAL1`` is additional input. Its meaning depends on the ``PrintType`` argument as described
            below.

            When ``PrintType`` = blank (default) or SPHR: Radius of the sphere surface.

            When ``PrintType`` = PLXY: Fixed z value for an X-Y plane in the Cartesian coordinate system.
            Defaults to 0.

            When ``PrintType`` = PLYZ: Fixed x value for a Y-Z plane in the Cartesian coordinate system.
            Defaults to 0.

            When ``PrintType`` = PLXZ: Fixed y value for an X-Z plane in the Cartesian coordinate system,
            Defaults to 0.

        val2 : str
            When ``Option`` = SPLC or SPAC: Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            When ``Option`` = PWL: Reference sound power. Defaults to 1x10 :sup:`-12` watts.

        val3 : str
            When ``Lab`` = PRES: Thickness of 2D model extrusion in the z direction (no default).

            When ``Lab`` = PROT: Angle of the y-axis rotated extrusion model (no default)

        val4 : str
            When ``Lab`` = PLAT: Mass density of acoustic fluid.

        val5 : str
            When ``Lab`` = PLAT: Sound speed in acoustic fluid.

        ldstep : str
            Specified load step. Defaults to the load step number specified on the :ref:`set` command, or defaults to 1 if :ref:`set` has not been issued.

            * ``n`` - Load step number.

            * ``ALL`` - All load steps.

        substep : str
            Specified substep. Defaults to the substep number specified on the :ref:`set` command, or defaults to ALL (all substeps at the specified load step) if :ref:`set` has not been issued.

            * ``n`` - Substep number.

            * ``ALL`` - All substeps.

        freqb : str
            Frequency value representing one of the following:

            * Beginning frequency of the frequency range ( ``FREQB`` to ``FREQE`` ) for the defined load step(s)
              and substeps ( ``SUBSTEP`` = ALL). If a ``SUBSTEP`` value is specified, ``FREQB`` is invalid.

            * Central frequency of octave bands, used when ``LogOpt`` = OB1, OB2, OB3, OB6, OB12, or OB24 and
              ``FREQE`` is blank.

        freqe : str
            Ending frequency of the frequency range ( ``FREQB`` to ``FREQE`` ) for the defined load step(s)
            and substeps ( ``SUBSTEP`` = ALL). If blank, ``FREQE`` is set to ``FREQB``. If a ``SUBSTEP``
            value is specified, ``FREQE`` is invalid.

        printtype : str
            Print out far-field parameters on a plane or sphere (used when ``Option`` = SUMC, PHSC, SPLC, SPAC, DGCT, PSCT, or TSCT). No default.

            * ``PLXY`` - On an X-Y plane.

            * ``PLYZ`` - On a Y-Z plane.

            * ``PLXZ`` - On an X-Z plane.

            * ``SPHR`` - On a sphere surface.

        logopt : str
            Octave bands (used only when Option = SPLC, SPAC, or PWL) :

            * ``OB0`` - Narrow bands (default).

            * ``OB1`` - Octave bands.

            * ``OB2`` - 1/2 octave bands.

            * ``OB3`` - 1/3 octave bands.

            * ``OB6`` - 1/6 octave bands.

            * ``OB12`` - 1/12 octave bands.

            * ``OB24`` - 1/24 octave bands.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRFAR.html>`_
           for further explanations.

        .. _PRFAR_notes:

        The :ref:`prfar` command prints pressure far fields and far field parameters as determined by the
        equivalent source principle. Use this command to print pressure and acoustic parameters. See the
        :ref:`hfsym` command for the model symmetry and the :ref:`hfang` command for spatial radiation
        angles.

        Printing acoustic parameters radiated by a vibrating structural panel ( ``Lab`` = PLAT) is supported
        by elements ``SOLID185``, ``SOLID186``, ``SOLID187``, ``SHELL181``, ``SHELL281``, and ``SOLSH190``.
        The vibration surface of the panel must be flagged by the :ref:`sf`,MXWF command.
        """
        command = f"PRFAR,{lab},{option},{var1b},{var1e},{nvar1},{var2b},{var2e},{nvar2},{val1},{val2},{val3},{val4},{val5},{ldstep},{substep},{freqb},{freqe},{printtype},{logopt}"
        return self.run(command, **kwargs)

    def prmc(
        self,
        lstep: str = "",
        sbstep: str = "",
        timfrq: str = "",
        kimg: int | str = "",
        hibeg: str = "",
        hiend: str = "",
        matrix: str = "",
        **kwargs,
    ):
        r"""Prints the modal coordinates from a mode-superposition solution.

        Mechanical APDL Command: `PRMC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRMC.html>`_

        Parameters
        ----------
        lstep : str
            Print the solution identified as load step ``LSTEP`` and substep ``SBSTEP``.

        sbstep : str
            Print the solution identified as load step ``LSTEP`` and substep ``SBSTEP``.

        timfrq : str
            As an alternative to ``LSTEP`` and ``SBSTEP``, print the solution at the time value ``TIMFRQ``
            (for :ref:`antype`,TRANS) or frequency value ``TIMFRQ`` (for :ref:`antype`,HARMIC). ``LSTEP``
            and ``SBSTEP`` should be left blank.

        kimg : int or str
            Key for printing real or imaginary solution. Valid only for :ref:`antype`,HARMIC.

            * ``0 (or blank)`` - Print the real solution (default).

            * ``1`` - Print the imaginary solution.

            * ``2`` - Print the amplitude.

        hibeg : str
            For cyclic symmetry solutions, print the solutions in the harmonic index solution range
            ``HIbeg`` to ``HIend``. Defaults to all harmonic indices (all modes).

        hiend : str
            For cyclic symmetry solutions, print the solutions in the harmonic index solution range
            ``HIbeg`` to ``HIend``. Defaults to all harmonic indices (all modes).

        matrix : str
            Create an APDL Math dense matrix with the name entered on this field (up to 32 characters; for
            nomenclature guidelines see `Guidelines for Parameter Names
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/Hlp_P_APDL3_2.html#apdlhidparmtlm8599>`_
            ``Matrix`` = blank), no APDL Math matrix is created.

        Notes
        -----

        .. _PRMC_notes:

        :ref:`prmc` prints the modal coordinates (the factors which modes may be multiplied by to obtain
        their contribution to the response) at a certain time point (transient analyses) or frequency point
        (harmonic analyses).

        The printout contains four columns: the mode number (labelled MODE), the modal frequency (labelled
        FREQ), the modal coordinate or mode multiplier (labelled MULT), and the normalized modal coordinate
        (labelled NORM). The normalized modal coordinate is the ratio of absolute value of the mode
        multiplier divided by the sum of the absolute values of all multipliers listed (at a solution
        time/frequency and harmonic index). It may be useful for identifying the dominant modes. Maximum
        values of each column are also listed at the end of each report.

        By default, the real part of the modal coordinate values are printed even if the modal coordinates
        are complex.

        When ``Matrix`` is specified, an APDL Math dense matrix similar to the one created with the
        :ref:`dmat` command is created. If :ref:`prmc` is issued multiple times with the same name entered
        on ``Matrix`` or if a matrix with the specified name already exists, the matrix is overwritten. This
        matrix contains four to five columns depending on the analysis. The first four columns are the ones
        printed by :ref:`prmc`. The fifth column contains the harmonic index for cyclic analysis only. This
        matrix can then be used in APDL Math data processing and file handling (See `APDL Math
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdlmathex.html>`_  :ref:`export`
        can be issued to export the :ref:`prmc` data to a :file:`.csv` file.

        For transient analyses, a :file:`.rdsp` None file must be available. For harmonic analyses, a
        :file:`.rfrq` None file must be available. The content of these files depends on the :ref:`outres`
        command settings. Note that the default for mode-superposition transient analysis is to write the
        reduced displacement file every 4th substep. For more information, see Command Default in the
        :ref:`outres` command description.

        For a cyclic harmonic mode-superposition analysis, use the :ref:`cycfiles` command to identify the
        :file:`.rfrq` None and modal :file:`.rst` None files. For other analyses, use the ``FILE`` command
        to specify the :file:`.rdsp` or :file:`.rfrq` file.

        This information can also be obtained from the optional :file:`Jobname.mcf` text file (see the
        :ref:`trnopt` and :ref:`hropt` commands), and it can be plotted using the :ref:`plmc` command. For
        more information on modal coordinates, see `Mode-Superposition Method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool9.html#thy_antools_resresp>`_
        in the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_

        **Example Usage**

        .. code:: apdl

           /POST1

        FILE,,rdsp ! Specify Jobname.rdsp file from a previous MSUP transient analysis ! Print modal
        coordinates from the second loadstep and fourth substep PRMC,2,4,,,,,MAT ! also create an APDL Math
        matrix called MAT \*EXPORT,MAT,CSV,PRMCFILE.CSV ! Export MAT to a.csv file
        """
        command = f"PRMC,{lstep},{sbstep},{timfrq},{kimg},{hibeg},{hiend},{matrix}"
        return self.run(command, **kwargs)

    def prnear(
        self,
        lab: str = "",
        opt: str = "",
        kcn: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        val9: str = "",
        **kwargs,
    ):
        r"""Prints the pressure in the near zone exterior to the equivalent source surface.

        Mechanical APDL Command: `PRNEAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRNEAR.html>`_

        Parameters
        ----------
        lab : str
            Print the maximum pressure or sound pressure level:

            * ``POINT`` - at the point (x,y,z)

            * ``SPHERE`` - on the spherical structure

            * ``PATH`` - along the path

        opt : str
            * ``PSUM`` - Maximum complex pressure for acoustics.

            * ``PHAS`` - Phase angle of complex pressure for acoustics.

            * ``SPL`` - Sound pressure level for acoustics.

            * ``SPLA`` - A-weighted sound pressure level for acoustics (dBA).

        kcn : str
            KCN is the coordinate system reference number. It may be 0 (Cartesian) or any previously defined
            local coordinate system number (>10). Defaults to 0.

        val1 : str
            For ``Lab`` = POINT:

            * ``VAL1`` - x coordinate value

            * ``VAL2`` - y coordinate value

            * ``VAL3`` - z coordinate value

            * ``VAL4 -, VAL8`` - not used

            * ``VAL9`` - Thickness of model in z direction (defaults to 0).

            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`prnear` computes the pressure for the path data points for the path
            currently defined by the :ref:`path` and :ref:`ppath` commands.

        val2 : str
            For ``Lab`` = POINT:

            * ``VAL1`` - x coordinate value

            * ``VAL2`` - y coordinate value

            * ``VAL3`` - z coordinate value

            * ``VAL4 -, VAL8`` - not used

            * ``VAL9`` - Thickness of model in z direction (defaults to 0).

            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`prnear` computes the pressure for the path data points for the path
            currently defined by the :ref:`path` and :ref:`ppath` commands.

        val3 : str
            For ``Lab`` = POINT:

            * ``VAL1`` - x coordinate value

            * ``VAL2`` - y coordinate value

            * ``VAL3`` - z coordinate value

            * ``VAL4 -, VAL8`` - not used

            * ``VAL9`` - Thickness of model in z direction (defaults to 0).

            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`prnear` computes the pressure for the path data points for the path
            currently defined by the :ref:`path` and :ref:`ppath` commands.

        val4 : str
            For ``Lab`` = POINT:

            * ``VAL1`` - x coordinate value

            * ``VAL2`` - y coordinate value

            * ``VAL3`` - z coordinate value

            * ``VAL4 -, VAL8`` - not used

            * ``VAL9`` - Thickness of model in z direction (defaults to 0).

            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`prnear` computes the pressure for the path data points for the path
            currently defined by the :ref:`path` and :ref:`ppath` commands.

        val5 : str
            For ``Lab`` = POINT:

            * ``VAL1`` - x coordinate value

            * ``VAL2`` - y coordinate value

            * ``VAL3`` - z coordinate value

            * ``VAL4 -, VAL8`` - not used

            * ``VAL9`` - Thickness of model in z direction (defaults to 0).

            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`prnear` computes the pressure for the path data points for the path
            currently defined by the :ref:`path` and :ref:`ppath` commands.

        val6 : str
            For ``Lab`` = POINT:

            * ``VAL1`` - x coordinate value

            * ``VAL2`` - y coordinate value

            * ``VAL3`` - z coordinate value

            * ``VAL4 -, VAL8`` - not used

            * ``VAL9`` - Thickness of model in z direction (defaults to 0).

            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`prnear` computes the pressure for the path data points for the path
            currently defined by the :ref:`path` and :ref:`ppath` commands.

        val7 : str
            For ``Lab`` = POINT:

            * ``VAL1`` - x coordinate value

            * ``VAL2`` - y coordinate value

            * ``VAL3`` - z coordinate value

            * ``VAL4 -, VAL8`` - not used

            * ``VAL9`` - Thickness of model in z direction (defaults to 0).

            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`prnear` computes the pressure for the path data points for the path
            currently defined by the :ref:`path` and :ref:`ppath` commands.

        val8 : str
            For ``Lab`` = POINT:

            * ``VAL1`` - x coordinate value

            * ``VAL2`` - y coordinate value

            * ``VAL3`` - z coordinate value

            * ``VAL4 -, VAL8`` - not used

            * ``VAL9`` - Thickness of model in z direction (defaults to 0).

            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`prnear` computes the pressure for the path data points for the path
            currently defined by the :ref:`path` and :ref:`ppath` commands.

        val9 : str
            For ``Lab`` = POINT:

            * ``VAL1`` - x coordinate value

            * ``VAL2`` - y coordinate value

            * ``VAL3`` - z coordinate value

            * ``VAL4 -, VAL8`` - not used

            * ``VAL9`` - Thickness of model in z direction (defaults to 0).

            For ``LAB`` = SPHERE:

            * ``VAL1`` - Radius of spherical surface in spherical coordinate system.

            * ``VAL2`` - Starting φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL3`` - Ending φ angle (degree) in the spherical coordinate system. Defaults to 0.

            * ``VAL4`` - Number of divisions between the starting and ending φ angles for data
              computations. Defaults to 0.

            * ``VAL5`` - Starting θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL6`` - Ending θ angle (degrees) in the spherical coordinate system. Defaults to 0 in 3D
              and 90 in 2D extension.

            * ``VAL7`` - Number of divisions between the starting and ending θ angles for data
              computations. Defaults to 0.

            * ``VAL8`` - Reference rms sound pressure. Defaults to 2x10 :sup:`-5` Pa.

            * ``VAL9`` - Thickness of 2D model extension in z direction (defaults to 0).

            For ``Lab`` = :ref:`path`, :ref:`prnear` computes the pressure for the path data points for the path
            currently defined by the :ref:`path` and :ref:`ppath` commands.

        Notes
        -----

        .. _PRNEAR_notes:

        The command uses the equivalent source principle to calculate the pressure in the near zone exterior
        to the equivalent source surface (flagged with the Maxwell surface flag in the preprocessor) for one
        of the following locations:

        * A point X, Y, Z in the KCN coordinate system

        * A spherical surface in the KCN coordinate system

        * A path defined by the :ref:`path` and :ref:`ppath` commands

        To list the pressure results for a path, use the :ref:`prpath` command. See :ref:`hfsym` command for
        the model symmetry.

        To retrieve saved equivalent source data, issue the :ref:`set`, ``Lstep``, ``Sbstep``,,REAL command.
        """
        command = f"PRNEAR,{lab},{opt},{kcn},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9}"
        return self.run(command, **kwargs)

    def reswrite(self, fname: str = "", cflag: int | str = "", **kwargs):
        r"""Appends results data from the database to a results file.

        Mechanical APDL Command: `RESWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RESWRITE.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

            The file name extension varies as follows:

            * :file:`.rst` for structural, fluid, or coupled-field analyses
            * :file:`.rth` for thermal or electrical analyses
            * :file:`.rmg` for magnetic analyses

        cflag : int or str
            * ``0`` - The complex results flag is set to 0 in the results file header. This is the default
              option.

            * ``1`` - The complex results flag is set to 1 in the results file header.

        Notes
        -----

        .. _RESWRITE_notes:

        The :ref:`reswrite` command appends a data set to the specified file by writing the results data
        currently in the database. If the intended results file does not exist, it will be created and will
        include the geometry records. The current load step, substep, and time (or frequency) value are
        maintained. All data (summable and nonsummable) are written.

        When complex results are appended, ``cFlag`` must be set to 1 so that the header is consistent with
        the results written on the file.

        The command is primarily intended for use in a top-down substructuring analysis, where the full
        model is resumed and the results data read from the `use pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/an9Auq1d6ldm.html#advobsl5jla062999>`_
        results file ( :ref:`set` ), and subsequently from all substructure `expansion pass
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/axcAuq367ldm.html#adv5note4jla062999>`_
        results files ( :ref:`append` ). The full set of data in memory can then be written out via the
        :ref:`reswrite` command to create a complete results file (as though you had run a nonsubstructured
        analysis).

        The :ref:`reswrite` command can also be used to write a global results file for a distributed-memory
        parallel ( DMP ) solution. This should only be necessary if the :ref:`rescombine` command was used
        to combine results from local results files into the database. The :ref:`reswrite` command can then
        be used to write the combined results into a new results file. This new results file will
        essentially contain the current set of results data for the entire (that is, global) model.
        """
        command = f"RESWRITE,{fname},,,,{cflag}"
        return self.run(command, **kwargs)

    def rmflvec(self, **kwargs):
        r"""Writes eigenvectors of fluid nodes to a file for use in damping parameter extraction.

        Mechanical APDL Command: `RMFLVEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RMFLVEC.html>`_

        Notes
        -----

        .. _RMFLVEC_notes:

        :ref:`rmflvec` extracts the modal information from the modal results file for all nodes specified in
        a node component called 'FLUN'. This component should include all nodes which are located at the
        fluid-structural interface. Mode shapes, element normal orientation, and a scaling factor are
        computed and stored in a file :file:`Jobname.EFL`. For damping parameter extraction, use the
        :ref:`dmpext` command macro. See   for more information on thin film analyses.

        ``FLUID136`` and ``FLUID138`` are used to model the fluid interface. Both the structural and fluid
        element types must be active. The fluid interface nodes must be grouped into a component 'FLUN'. A
        results file of the last modal analysis must be available.
        """
        command = "RMFLVEC"
        return self.run(command, **kwargs)

    def rsplit(
        self,
        option: str = "",
        label: str = "",
        name1: str = "",
        name2: str = "",
        name3: str = "",
        name4: str = "",
        name5: str = "",
        name6: str = "",
        name7: str = "",
        name8: str = "",
        name9: str = "",
        name10: str = "",
        name11: str = "",
        name12: str = "",
        name13: str = "",
        name14: str = "",
        name15: str = "",
        name16: str = "",
        **kwargs,
    ):
        r"""Creates one or more results file(s) from the current results file based on subsets of elements.

        Mechanical APDL Command: `RSPLIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RSPLIT.html>`_

        **Command default:**
        Write all data available for the element subset.

        Parameters
        ----------
        option : str
            Specify which results to include for the subset of elements.

            * ``ALL`` - Write all nodal and element results based on the subset of elements (default).

            * ``EXT`` - Write only the nodal and element results that are on the exterior surface of the element
              subset. The results data will be averaged as in PowerGraphics (see :ref:`avres` ) when this results
              file is brought into POST1. Only valid for solid elements.

        label : str
            Define where the element subset is coming from.

            * ``ALL`` - Use all selected element components ( :ref:`cmsel` ) (default).

            * ``ESEL`` - Use the currently selected ( :ref:`esel` ) set of elements. ``Name1`` defines the
              results file name.

            * ``LIST`` - Use ``Name1`` to ``Name16`` to list the element component and/or assembly names (that
              contain element components).

        name1 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name2 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name3 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name4 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name5 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name6 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name7 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name8 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name9 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name10 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name11 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name12 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name13 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name14 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name15 : str
            Up to 16 element component and/or assembly names (that contain element components).

        name16 : str
            Up to 16 element component and/or assembly names (that contain element components).

        Notes
        -----
        Results files will be named based on the element component or assembly name, for example,
        :file:`Cname.rst`, except for the ESEL option, for which you must specify the results file name (no
        extension) using the ``Name1`` field. Note that the :file:`.rst` filename will be written in all
        uppercase letters ( :file:`CNAME.rst` ) (unless using the ESEL option); when you read the file, you
        must specify the filename using all uppercase letters (that is, :file:`file`,CNAME). You may repeat
        the :ref:`rsplit` command as often as needed. All results sets on the results file are processed.
        Use :ref:`aux3` to produce a results file with just a subset of the results sets.

        Use :ref:`inres` to limit the results data written to the results files.

        The subset geometry is also written so that no database file is required to postprocess the subset
        results files. You must not resume any database when postprocessing one of these results files. The
        input results file must have geometry written to it (that is, do not use :ref:`config`,NORSTGM,1).

        Applied forces and reaction forces are not apportioned if their nodes are shared by multiple element
        subsets. Their full values are written to each results file.

        Each results file renumbers its nodes and elements starting with 1.

        This feature is useful when working with large models. For more information on the advantages and
        uses of the :ref:`rsplit` command, see `Splitting Large Results Files
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#>`_ in the
        `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_.
        """
        command = f"RSPLIT,{option},{label},{name1},{name2},{name3},{name4},{name5},{name6},{name7},{name8},{name9},{name10},{name11},{name12},{name13},{name14},{name15},{name16}"
        return self.run(command, **kwargs)

    def rstmac(
        self,
        file1: str = "",
        lstep1: str = "",
        sbstep1: str = "",
        file2: str = "",
        lstep2: str = "",
        sbstep2: str = "",
        maclim: str = "",
        cname: str = "",
        keyprint: int | str = "",
        **kwargs,
    ):
        r"""Calculates modal assurance criterion (MAC/FRF) and matches nodal solutions from two results files or
        from one results file and one universal format file.

        Mechanical APDL Command: `RSTMAC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RSTMAC.html>`_

        Parameters
        ----------
        file1 : str
            File name ( 248 characters maximum) corresponding to the first results file ( :file:`.rst` or
            :file:`.rstp` file). If the file name does not contain the extension, it defaults to
            :file:`rst`.

        lstep1 : str
            Load step number of the results to be read in ``File1``.

            * ``N`` - Reads load step ``N``. Defaults to 1.

        sbstep1 : str
            Substep number of the results to be read in ``File1``.

            * ``N`` - Reads substep ``N``. Only valid for MAC.

            * ``All`` - Reads all substeps. This value is the default.

        file2 : str
            File name ( 248 characters maximum) corresponding to the second file ( :file:`.rst`,
            :file:`.rstp`, or :file:`.unv` file). If the file name does not contain the extension, it
            defaults to :file:`rst`.

        lstep2 : str
            Load step number of the results to be read in ``File2``.

            * ``N`` - Reads load step ``N``. Defaults to 1.

        sbstep2 : str
            Substep number of the results to be read in ``File2``.

            * ``N`` - Reads substep ``N``. Only valid for MAC.

            * ``All`` - Reads all substeps. This value is the default.

        maclim : str
            Smallest acceptable criterion value. Must be :math:`equation_not_available`  0 and
            :math:`equation_not_available`  1. The default value is 0.90.

        cname : str
            Name of the component from the first file ( ``File1`` ). The component must be based on nodes.
            If unspecified, all nodes are matched and used for MAC calculations. If a component name is
            specified, only nodes included in the specified component are used. Not applicable to node
            mapping ( ``Option`` = NODMAP on :ref:`macopt`  ).

        keyprint : int or str
            Printout options:

            * ``0`` - Printout matched solutions table. This value is the default.

            * ``1`` - Printout matched solutions table and full MAC table.

            * ``2`` - Printout matched solutions table, full MAC table and matched nodes table.

        Notes
        -----
        The :ref:`rstmac` command allows the comparison of the solutions from either:

        * Two different results files. Valid only for MAC calculations.

        * One result file ( :file:`.rst` ) and one universal format file ( :file:`.unv` ).

        Either the modal assurance criterion (MAC) or the frequency response function (FRF) correlation
        method is used. (For more details see `POST1 - Modal Assurance Criterion (MAC)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post16.html#eqff29ac61-1393-4410-9090-572b02773534>`_
        `POST1 - Frequency response function correlation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thryFRF120.html#eqcaaee52b-1bb5-4b48-a411-6a162a579399>`_

        The meshes read from ``File1`` and ``File2`` may be different. The nodes of ``File1`` are matched
        with the nodes of ``File2`` based on either node location (default) or node number. The solutions
        are compared for the identified pair of matched nodes. The nodes can also be mapped and the
        solutions interpolated from ``File1``. See the :ref:`macopt` command for all options.

        Units and coordinate systems must be the same for both models.

        Results may be real or complex; however, if results in ``File1`` have a different type than results
        in ``File2``, only the real parts of the solutions are taken into account in MAC calculations. The
        analysis type can be arbitrary for MAC while only harmonic analysis is supported for FRF criteria
        calculations.

        Non-structural degrees of freedom can be considered. Degrees of freedom can vary between ``File1``
        and ``File2``, but at least one common degree of freedom must exist.

        The solutions read on the results files are not all written to the database; therefore, subsequent
        plotting or printing of solutions is not possible. A :ref:`set` command must be issued after the
        :ref:`rstmac` command to post-process each solution.

        The corresponding database file ( :file:`.db` ) for :file:`File1` on :ref:`rstmac` must be resumed
        before running the command in the following cases:

        * A component ( ``Cname`` ) is used on :ref:`rstmac`.

        * The nodes are mapped ( :ref:`macopt`,NODMAP,YES).

        * The nodes are matched using a relative tolerance ( :ref:`macopt`,RELTOLN).

        :ref:`rstmac` comparison on cyclic symmetry analysis works only if the number of sectors on
        ``File1`` and ``File2`` are the same, and the database is saved after the solution is finished.
        Also, a comparison cannot be made between cyclic symmetry results and the full 360 degree model
        results ( ``File1`` - cyclic solution, ``File2`` - full 360 degree model solution). Comparing cyclic
        symmetry solutions written on a selected set of nodes ( :ref:`outres` ) is not supported.

        The modal assurance criterion values can be retrieved as parameters using the :ref:`get` command (
        ``Entity`` = :ref:`rstmac` ).

        FRF correlation is only supported for the comparison of an :file:`.rst` and a :file:`.unv` file. All
        substeps are considered for both files to define the frequency domain for criteria calculations. The
        printout options consist of listing the table of the criterion results for each frequency in the
        frequency domain ( ``KeyPrint`` = 0, 1, or 2) and the matched nodes table ( ``KeyPrint`` = 2).

        **Example Usage**

        .. _RSTMAC_example:

        For a detailed discussion on using RSTMAC with examples see `Comparing Nodal Solutions From Two
        Models (RSTMAC)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_4.html#>`_ RSTMAC ) in
        the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_.
        """
        command = f"RSTMAC,{file1},{lstep1},{sbstep1},{file2},{lstep2},{sbstep2},,{maclim},{cname},{keyprint}"
        return self.run(command, **kwargs)

    def slashexpand(
        self,
        nrepeat1: str = "",
        type1: str = "",
        method1: str = "",
        dx1: str = "",
        dy1: str = "",
        dz1: str = "",
        nrepeat2: str = "",
        type2: str = "",
        method2: str = "",
        dx2: str = "",
        dy2: str = "",
        dz2: str = "",
        nrepeat3: str = "",
        type3: str = "",
        method3: str = "",
        dx3: str = "",
        dy3: str = "",
        dz3: str = "",
        **kwargs,
    ):
        r"""Allows the creation of a larger graphic display than represented by the actual finite element
        analysis model.

        Mechanical APDL Command: `/EXPAND <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXPAND_sl.html>`_

        Parameters
        ----------
        nrepeat1 : str
            The number of repetitions required for the element pattern. The default is 0 (no expansion).

        type1 : str
            The type of expansion requested.

            * ``RECT`` - Causes a Cartesian transformation of DX, DY, and DZ for each pattern (default).

            * ``POLAR`` - Causes a polar transformation of DR, D-Theta and DZ for each pattern.

            * ``AXIS`` - Causes 2D axisymmetric expansion (that is, rotates a 2D model created in the X-Y plane
              about the Y axis to create a 3D model).

            * ``LRECT`` - Causes a Cartesian transformation of DX, DY, and DZ for each pattern about the current
              local coordinate system (specified via the :ref:`csys` command).

            * ``LPOLAR`` - Causes a polar transformation of DR, D-Theta, and DZ for each pattern about the local
              coordinate system (specified via the :ref:`csys` command).

        method1 : str
            The method by which the pattern is repeated.

            * ``FULL`` - Causes a normal repeat of the pattern (default).

            * ``HALF`` - Uses a symmetry transformation for alternate repeats (to produce an image of a complete
              circular gear from the image of half a tooth, for example).

        dx1 : str
            The Cartesian or polar increments between the repeated patterns. Also determines the reflection
            plane. Reflection is about the plane defined by the normal vector (DX, DY, DZ). If you want no
            translation, specify a small nonzero value. For a half-image expansion, the increment DX, DY, or
            DZ is doubled so that POLAR,HALF,,45 produces full images on 90° centers, and RECT,HALF,,1
            produces full images on 2-meter centers.

        dy1 : str
            The Cartesian or polar increments between the repeated patterns. Also determines the reflection
            plane. Reflection is about the plane defined by the normal vector (DX, DY, DZ). If you want no
            translation, specify a small nonzero value. For a half-image expansion, the increment DX, DY, or
            DZ is doubled so that POLAR,HALF,,45 produces full images on 90° centers, and RECT,HALF,,1
            produces full images on 2-meter centers.

        dz1 : str
            The Cartesian or polar increments between the repeated patterns. Also determines the reflection
            plane. Reflection is about the plane defined by the normal vector (DX, DY, DZ). If you want no
            translation, specify a small nonzero value. For a half-image expansion, the increment DX, DY, or
            DZ is doubled so that POLAR,HALF,,45 produces full images on 90° centers, and RECT,HALF,,1
            produces full images on 2-meter centers.

        nrepeat2 : str
            The number of repetitions required for the element pattern. The default is 0 (no expansion).

        type2 : str
            The type of expansion requested.

            * ``RECT`` - Causes a Cartesian transformation of DX, DY, and DZ for each pattern (default).

            * ``POLAR`` - Causes a polar transformation of DR, D-Theta and DZ for each pattern.

            * ``AXIS`` - Causes 2D axisymmetric expansion (that is, rotates a 2D model created in the X-Y plane
              about the Y axis to create a 3D model).

            * ``LRECT`` - Causes a Cartesian transformation of DX, DY, and DZ for each pattern about the current
              local coordinate system (specified via the :ref:`csys` command).

            * ``LPOLAR`` - Causes a polar transformation of DR, D-Theta, and DZ for each pattern about the local
              coordinate system (specified via the :ref:`csys` command).

        method2 : str
            The method by which the pattern is repeated.

            * ``FULL`` - Causes a normal repeat of the pattern (default).

            * ``HALF`` - Uses a symmetry transformation for alternate repeats (to produce an image of a complete
              circular gear from the image of half a tooth, for example).

        dx2 : str
            The Cartesian or polar increments between the repeated patterns. Also determines the reflection
            plane. Reflection is about the plane defined by the normal vector (DX, DY, DZ). If you want no
            translation, specify a small nonzero value. For a half-image expansion, the increment DX, DY, or
            DZ is doubled so that POLAR,HALF,,45 produces full images on 90° centers, and RECT,HALF,,1
            produces full images on 2-meter centers.

        dy2 : str
            The Cartesian or polar increments between the repeated patterns. Also determines the reflection
            plane. Reflection is about the plane defined by the normal vector (DX, DY, DZ). If you want no
            translation, specify a small nonzero value. For a half-image expansion, the increment DX, DY, or
            DZ is doubled so that POLAR,HALF,,45 produces full images on 90° centers, and RECT,HALF,,1
            produces full images on 2-meter centers.

        dz2 : str
            The Cartesian or polar increments between the repeated patterns. Also determines the reflection
            plane. Reflection is about the plane defined by the normal vector (DX, DY, DZ). If you want no
            translation, specify a small nonzero value. For a half-image expansion, the increment DX, DY, or
            DZ is doubled so that POLAR,HALF,,45 produces full images on 90° centers, and RECT,HALF,,1
            produces full images on 2-meter centers.

        nrepeat3 : str
            The number of repetitions required for the element pattern. The default is 0 (no expansion).

        type3 : str
            The type of expansion requested.

            * ``RECT`` - Causes a Cartesian transformation of DX, DY, and DZ for each pattern (default).

            * ``POLAR`` - Causes a polar transformation of DR, D-Theta and DZ for each pattern.

            * ``AXIS`` - Causes 2D axisymmetric expansion (that is, rotates a 2D model created in the X-Y plane
              about the Y axis to create a 3D model).

            * ``LRECT`` - Causes a Cartesian transformation of DX, DY, and DZ for each pattern about the current
              local coordinate system (specified via the :ref:`csys` command).

            * ``LPOLAR`` - Causes a polar transformation of DR, D-Theta, and DZ for each pattern about the local
              coordinate system (specified via the :ref:`csys` command).

        method3 : str
            The method by which the pattern is repeated.

            * ``FULL`` - Causes a normal repeat of the pattern (default).

            * ``HALF`` - Uses a symmetry transformation for alternate repeats (to produce an image of a complete
              circular gear from the image of half a tooth, for example).

        dx3 : str
            The Cartesian or polar increments between the repeated patterns. Also determines the reflection
            plane. Reflection is about the plane defined by the normal vector (DX, DY, DZ). If you want no
            translation, specify a small nonzero value. For a half-image expansion, the increment DX, DY, or
            DZ is doubled so that POLAR,HALF,,45 produces full images on 90° centers, and RECT,HALF,,1
            produces full images on 2-meter centers.

        dy3 : str
            The Cartesian or polar increments between the repeated patterns. Also determines the reflection
            plane. Reflection is about the plane defined by the normal vector (DX, DY, DZ). If you want no
            translation, specify a small nonzero value. For a half-image expansion, the increment DX, DY, or
            DZ is doubled so that POLAR,HALF,,45 produces full images on 90° centers, and RECT,HALF,,1
            produces full images on 2-meter centers.

        dz3 : str
            The Cartesian or polar increments between the repeated patterns. Also determines the reflection
            plane. Reflection is about the plane defined by the normal vector (DX, DY, DZ). If you want no
            translation, specify a small nonzero value. For a half-image expansion, the increment DX, DY, or
            DZ is doubled so that POLAR,HALF,,45 produces full images on 90° centers, and RECT,HALF,,1
            produces full images on 2-meter centers.

        Notes
        -----

        .. _s-EXPAND_notes:

        You can use the :ref:`slashexpand` command to perform up to three symmetry expansions at once (that
        is, X, Y, and Z which is equal to going from a 1/8 model to a full model). Polar expansions allow
        you to expand a wheel section into a half wheel, then into the half section, and then into the
        whole.

        The command displays elements/results when you issue the :ref:`eplot` command or postprocessing
        commands.

        The command works on all element and result displays, except as noted below. As the graphic display
        is created, the elements (and results) are repeated as many times as necessary, expanding the
        geometry and, if necessary, the displacements and stresses.

        Derived results are not supported.

        The :ref:`slashexpand` command has the following limitations:

        * It does not support solid model entities.

        * POLAR, FULL or HALF operations are meaningful only in global cylindrical systems and are
          unaffected by the :ref:`rsys` or :ref:`dsys` commands. Cartesian symmetry or unsymmetric
          operations also occur about the global Cartesian system.

        * It does not average nodal results across sector boundaries, even for averaged plots (such as those
          obtained via the :ref:`plnsol` command).

        * Axisymmetric harmonic element results are not supported for ``Type`` = AXIS.

        The :ref:`slashexpand` command differs significantly from the :ref:`expand` command in several
        respects:

        * The uses of :ref:`slashexpand` are of a more general nature, whereas the :ref:`expand` command is
          intended primarily to expand modal cyclic symmetry results.

        * :ref:`slashexpand` does not change the database as does the :ref:`expand` command.

        * You cannot print results displayed via :ref:`slashexpand`.

        """
        command = f"/EXPAND,{nrepeat1},{type1},{method1},{dx1},{dy1},{dz1},{nrepeat2},{type2},{method2},{dx2},{dy2},{dz2},{nrepeat3},{type3},{method3},{dx3},{dy3},{dz3}"
        return self.run(command, **kwargs)

    def spmwrite(
        self,
        method: str = "",
        nmode: str = "",
        inputs: str = "",
        inputlabels: str = "",
        outputs: str = "",
        outputlabels: str = "",
        nic: str = "",
        velacckey: str = "",
        fileformat: int | str = "",
        **kwargs,
    ):
        r"""Calculates the state-space matrices and writes them to the SPM file.

        Mechanical APDL Command: `SPMWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPMWRITE.html>`_

        Parameters
        ----------
        method : str
            Reduction method for the calculation of the state-space matrices.

            * ``MODAL`` - Method based on modal analysis results from LANB, LANPCG, SNODE, or SUBSP eigensolver
              (default).

        nmode : str
            Number of modes to be used. Defaults to all modes.

        inputs : str
            Definition of the inputs. Defaults to all load vectors on the MODE file.

            If an integer is entered, it specifies the number of load vectors from the MODE file used for
            the definition of the inputs. The first ``Inputs`` load vectors are used.

            If ``Inputs`` is an array parameter, the first column is the node number and the second column
            is the structural degree of freedom (1=UX, 2=UY, 3=UZ, 4=ROTX, 5=ROTY, 6=ROTZ) indicating input
            points. The number of rows in the array parameter is equal to the number of inputs.

        inputlabels : str
            Definition of the input labels. Defaults to the load vector numbers or input definition (node
            and degree of freedom array parameter), depending on the ``Inputs`` specification.

            If a character array parameter is entered (Type=CHAR in the :ref:`dim` command), each 8
            character string represents an input label. Only valid when ``Inputs`` is an array parameter

        outputs : str
            Definition of the outputs. Defaults to the inputs.

            If an array parameter is entered, the first column is the node number and the second column is
            the structural degree of freedom (1=UX, 2=UY, 3=UZ, 4=ROTX, 5=ROTY, 6=ROTZ) of the output
            points. The number of rows in the array parameter is equal to the number of outputs.

        outputlabels : str
            Definition of the output labels. Defaults to the output definition (node and degree of freedom)
            if used, else defaults to the ``InputLabels``.

            If a character array parameter is entered (Type=CHAR in the \*DIM command), each 8 character
            string represents an output label.

        nic : str
            Load vector on the ``MODE`` file used for the calculation of the initial conditions. Defaults to
            no initial condition.

        velacckey : str
            Output velocities and accelerations key.

            * ``OFF`` - Output displacements only (default).

            * ``ON`` - Output displacements, velocities and accelerations.

        fileformat : int or str
            The format of the SPM file.

            * ``0`` - Dense format.

            * ``1`` - Matrix Market Exchange format (non-zero terms only).

            * ``2`` - Twin Builder SML format without reference (default).

            * ``3`` - Twin Builder SML format with common reference.

            * ``4`` - Twin Builder SML format with independent references.

        Notes
        -----

        .. _SPMWRITE_notes:

        The SPMWRITE generates the file :file:`Jobname.SPM` containing the state-space matrices and other
        information.

        The following applies to the SML formats (FileFormat = 2, 3, and 4):

        * For conservative systems where the outputs are equal to the inputs ( ``Outputs`` is left blank):

        * The labels for the inputs ( ``InputLabels`` ) are required.

        * The ``Inputs`` must use the array parameter option so that the input degrees of freedom (DOFs) are
          known.

        * For non-conservative systems where the outputs are not equal to the inputs:

        * The labels for the outputs ( ``OutputLabels`` ) are required.

        * The file formats with references ( ``FileFormat`` = 3 and 4) do not apply.

        * Velocity and acceleration results are not included in the state-space matrices calculation
          (VelAccKey = OFF)

        * File format with common reference (FileFormat = 3) does not apply if the inputs are based on DOFs
          of a different nature. All input DOFs must be either all rotational or all translational and not a
          mix of the two.

        * A graphics file ( :file:`Jobname_SPM.PNG` ) is generated. It contains an element plot of the
          model.

        For more details about the reduction method and the generation of the state-space matrices, see
        `Reduced-Order Modeling for State-Space Matrices Export
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thystatespacemat.html#eq02c48d71-fb56-4172-a237-77dcfe5729e7>`_

        For examples of the command usage, see `State-Space Matrices Export
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advstatspacmat.html>`_
        """
        command = f"SPMWRITE,{method},{nmode},{inputs},{inputlabels},{outputs},{outputlabels},{nic},{velacckey},{fileformat}"
        return self.run(command, **kwargs)

    def spoint(
        self,
        node: str = "",
        x: str = "",
        y: str = "",
        z: str = "",
        inertiakey: str = "",
        **kwargs,
    ):
        r"""Defines a point for force/moment summations or inertia calculation

        Mechanical APDL Command: `SPOINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPOINT.html>`_

        Parameters
        ----------
        node : str
            Node number of the desired point. If zero, use ``X``, ``Y``, ``Z`` to describe point.

        x : str
            Global Cartesian coordinates of the desired summation point. Used if ``NODE`` is 0. Defaults to
            (0,0,0).

        y : str
            Global Cartesian coordinates of the desired summation point. Used if ``NODE`` is 0. Defaults to
            (0,0,0).

        z : str
            Global Cartesian coordinates of the desired summation point. Used if ``NODE`` is 0. Defaults to
            (0,0,0).

        inertiakey : str
            Inertia key:

            * ``OFF`` - Point or node is used for the force/moment summations (default).

            * ``ON`` - Point or node is used for the calculation of total inertia.

        Notes
        -----

        .. _SPOINT_notes:

        By default ( ``InertiaKey`` = OFF), defines a point (any point other than the origin) about which
        the tabular moment summations are computed. If force summations are desired in other than the global
        Cartesian directions, a node number must be specified on the ``NODE`` field, and the desired
        coordinate system must be activated with :ref:`rsys`. The command must be issued in the :ref:`post1`
        module.

        When the inertia key is activated ( ``InertiaKey`` = ON), the total inertia printed in the precise
        mass summary is calculated with respect to the point or node in the global Cartesian system. In this
        case, the command must be issued during the first load step in the :ref:`slashsolu` module.
        """
        command = f"SPOINT,{node},{x},{y},{z},{inertiakey}"
        return self.run(command, **kwargs)

    def vtkwrite(self, fname: str = "", item: str = "", **kwargs):
        r"""Writes the current displacement data to a :file:`.VTK` file.

        Mechanical APDL Command: `VTKWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VTKWRITE.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. Default: :file:`Jobname`.

        item : str
            The output item (U, S, EPEL, or EPPL) to write to the file. Default: U.

        Notes
        -----

        .. _VTKWRITE_notes:

        Writes the requested data currently in memory ( :ref:`set` ) to a :file:`.VTK` file that can be read
        by any VTK-compatible viewer (such as ParaView).

        Only data associated with the currently selected element set is written.

        Support is available for the displacements of 8-node brick elements (such as ``SOLID185`` ) only. If
        your model uses multiple element types, select only the 8-node elements before issuing
        :ref:`vtkwrite`.
        """
        command = f"VTKWRITE,{fname},{item}"
        return self.run(command, **kwargs)
