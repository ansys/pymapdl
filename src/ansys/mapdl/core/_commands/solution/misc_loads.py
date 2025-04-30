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


class MiscLoads:

    def mrpm(self, val1: str = "", **kwargs):
        r"""Defines the revolutions per minute (RPM) for a machine rotation.

        Mechanical APDL Command: `MRPM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MRPM.html>`_

        Parameters
        ----------
        val1 : str
            The RPM value (no default).

        Notes
        -----

        .. _MRPM_notes:

        A different RPM value can be defined at each load step. The RPM value is used to postprocess the
        equivalent radiated power from the structural surface (the :ref:`pras` and :ref:`plas` commands) or
        the radiated sound power level (the :ref:`prfar` and :ref:`plfar` commands).
        """
        command = f"MRPM,{val1}"
        return self.run(command, **kwargs)

    def rstcontrol(
        self,
        type_: str = "",
        cname: str = "",
        method: str = "",
        methoditem: str = "",
        **kwargs,
    ):
        r"""Controls whether element single value results are written to the results file.

        Mechanical APDL Command: `RSTCONTROL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RSTCONTROL.html>`_

        Parameters
        ----------
        type_ : str
            Solution format for database and file-write control:

            * ``AUTO`` - Write element output quantities (STRS, EPEL, EPPL, EPCR, EPTH) in single value form for
              those element types that support it, and in element nodal form for all other element types
              (default). See `Element Single Value Results
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#>`_

            * ``ELSV`` - Write element output quantities only in single value form. If the single value form is
              not supported by the element types in the model, none of the applicable results (STRS, EPEL, EPPL,
              EPCR, EPTH) will be available.

            * ``ELND`` - Write all element output quantities only in element nodal form.

            * ``ERASE`` - Reset :ref:`rstcontrol` specifications to their default values.

            * ``STAT`` - List the current :ref:`rstcontrol` specifications.

        cname : str
            Name of the component (created via :ref:`cm` ) defining the selected set of elements for which
            this specification is active. If no name is entered, the specification applies to all elements.

        method : str
            For single value results, ``Method`` controls how the integration point values of each element are reduced to one value:

            * ``AVG`` - Use a simple average of values from all integration points (default).

            * ``MAXE`` - Use only the integration point corresponding to the maximum equivalent (EQV) stress or
              strain quantity specified by ``MethodItem``.

            * ``MAXP`` - Use only the integration point corresponding to the maximum 1st principal stress or
              strain quantity specified by ``MethodItem``.

            * ``MAXS`` - Use only the integration point corresponding to the maximum shear stress or strain
              quantity specified by ``MethodItem``.

        methoditem : str
            The quantity used to determine the integration point where single value results are reported. Only
            valid when ``Method`` = MAXE, MAXP, or MAXS.

            * ``STRS`` - Choose the integration point based on stress.

            * ``EPEL`` - Choose the integration point based on elastic strain.

            * ``EPPL`` - Choose the integration point based on plastic strain.

            * ``EPCR`` - Choose the integration point based on creep strain.

            * ``EPTH`` - Choose the integration point based on thermal strain.

        Notes
        -----
        :ref:`rstcontrol` is an optional output control command that specifies whether element nodal results
        or element single value results are written to the results file. This command works in conjunction
        with the :ref:`outres` command. :ref:`outres` specifies when each element quantity will be output,
        while :ref:`rstcontrol` specifies the type of result (element nodal versus single value). Not all
        elements support single value results. For more information, see `Element Single Value Results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#>`_

        The element output quantities affected by this command are:

        * stress (STRS)
        * elastic strain (EPEL)
        * plastic strain (EPPL)
        * creep strain (EPCR)
        * thermal/swelling strains (EPTH)

        You can issue up to 50 :ref:`rstcontrol` commands in an analysis. :ref:`rstcontrol`,ERASE erases the
        existing output specifications and resets the counted number of :ref:`rstcontrol` commands to zero.

        :ref:`rstcontrol` is also valid in PREP7.
        """
        command = f"RSTCONTROL,{type_},{cname},{method},{methoditem}"
        return self.run(command, **kwargs)

    def rescontrol(
        self,
        action: str = "",
        ldstep: str = "",
        frequency: str = "",
        maxfiles: int | str = "",
        maxtotalfiles: str = "",
        filetype: str = "",
        **kwargs,
    ):
        r"""Controls file writing for multiframe restarts.

        Mechanical APDL Command: `RESCONTROL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RESCONTROL.html>`_

        Parameters
        ----------
        action : str
            Command action:

            * ``DEFINE`` - Specifies how often :file:`.xnnn` restart files (default) or :file:`.rdnn` remeshing
              database files (for `nonlinear mesh adaptivity
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_ analysis) are
              written for a load step. The file type controlled by this command is determined by ``Filetype``.

            * ``FILE_SUMMARY`` - Prints the substep and load-step information for all :file:`.xnnn` or
              :file:`.rdnn` files for the current jobname in the current directory. If specified, all other
              arguments are ignored.

            * ``STATUS`` - Issuing the command lists the current status in the tables of restart controls
              specified previously by :ref:`rescontrol`. If this option is specified, all other arguments are
              ignored.

            * ``NORESTART`` - Cleans up some of the restart files after a distributed-memory parallel (DMP)
              solution. (Not valid for `nonlinear mesh adaptivity
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_.)

              The master process will not have the following files in the working directory at the end of the run:
              :file:`.esav`, :file:`.osav`, :file:`.xnnn`, :file:`.rdb`, :file:`.ldhi`. The worker processes will
              not have the following files in the working directory at the end of the run: :file:`.esav`,
              :file:`.osav`, :file:`.xnnn`, :file:`.rst` (or :file:`.rth`, etc.). Some restart files are never
              written, some are removed upon exiting the solution processor (for example, upon :ref:`finish` ),
              and some are removed upon exiting the program.

              This option is useful for cleaning up files written by all distributed processes, especially when
              you know that these restart files will not be needed later. If this option is specified, all other
              arguments are ignored.

              If this option is used in a shared-memory parallel (SMP) environment, most restart files in the
              working directory are removed. It has the same effect as issuing :ref:`rescontrol`,,NONE.

            * ``LINEAR`` - Same as ``Action`` = DEFINE, but for linear static applications only. For a linear
              static analysis, the restart capability is normally not needed; however, it is typically needed when
              a subsequent linear perturbation analysis is desired. By default, none of the restart files are
              written for a linear static analysis.

            * ``DELETE`` - Delete the restart control specification corresponding to the ``Ldstep`` label on a
              previous :ref:`rescontrol`,DEFINE command.

        ldstep : str
            Specifies how the :file:`.xnnn` or :file:`.rdnn` files are written for the specified load steps. This option also affects how often the load history information is written to the :file:`.ldhi` file.

            * ``ALL`` - Write the :file:`.xnnn` or :file:`.rdnn` files at the same substep ``Frequency`` for all
              load steps; write the load history information to the :file:`.ldhi` file for all load steps. For
              :file:`.rdnn` files, this option is the default.

            * ``LAST`` - Write the :file:`.xnnn` or :file:`.rdnn` files for the last load step only; write load-
              history information to the :file:`.ldhi` file for the last load step only. This option is the
              default for nonlinear static and full transient analyses for :file:`.xnnn` files. If specified, all
              remaining arguments are ignored.

            * ``N`` - Number that indicates how often the :file:`.xnnn` or :file:`.rdnn` files are written.

              Input a positive number to write the :file:`.xnnn` or :file:`.rdnn` files at the substep
              ``Frequency`` indicated only for load step ``N``. Other load steps will be written at the default
              substep frequency or at a frequency defined by a previous :ref:`rescontrol` specification. Load-
              history information is written to the :file:`.ldhi` file only for load steps ``N``.

              Specifying a negative number (- ``N`` ) is valid for controlling :file:`.xnnn` files only. The files
              are written for every ``N`` th load step at the specified substep ``Frequency``. The load history
              information is written to the :file:`.ldhi` file every ``N`` th load step. This option is suitable
              for restart applications in which more than a few hundred load steps are required. Compared to the
              ALL and positive ``N`` options, it can save disk space, as the :file:`.ldhi` file is smaller and
              fewer :file:`.xnnn` files are written.

              If ``Ldstep`` = - ``N``, all other ``Ldstep`` options specified by :ref:`rescontrol` are ignored and
              the program follows the - ``N`` option (write load history information every ``N`` th load step). If
              you want to change this pattern, issue :ref:`rescontrol`,DELETE, - ``N``, then issue another
              :ref:`rescontrol` command with the desired ``Ldstep`` option.

            * ``NONE`` - No multiframe restart files ( :file:`.rdb`, :file:`.ldhi`, :file:`.xnnn` ) are created.
              (Not valid for `nonlinear mesh adaptivity
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_ analysis.)

              This option is the default for mode-superposition analyses. The remaining arguments are ignored.

              For nonlinear static, linear static, and full transient analyses, this option enables a restart to
              occur at the last or abort point (using the :file:`.emat`, :file:`.esav` or :file:`.osav`, and
              :file:`.db` files).

              For mode-superposition transient analyses, this option allows a restart from the last point using
              the :file:`.rdsp` and :file:`.db` files.

        frequency : str
            Frequency at which the :file:`.xnnn` files are written at the substep level, or at which the :file:`.rdnn` files are written at the remeshing level:

            * ``NONE`` - Do not write :file:`.xnnn` files for this load step (not available for :file:`.rdnn`
              files).

            * ``LAST`` - Write the :file:`.xnnn` files for the last substep of the load step only (default for
              nonlinear static and full transient analyses), or write the :file:`.rdnn` files for the last remesh
              of the load step only (default for `nonlinear mesh adaptivity
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_ analysis).

            * ``N`` - If ``N`` is positive, write the :file:`.xnnn` files at every ``N`` th substep of a load
              step, or write the :file:`.rdnn` files at every ``N`` th remesh of a load step.

              If ``N`` is negative (not valid for :file:`.rdnn` files), write ``N`` equally spaced :file:`.xnnn`
              files within a load step.

              In nonlinear static and full transient analyses, ``-N`` is valid only when automatic time stepping
              is enabled ( :ref:`autots`,ON).

              In mode-superposition analyses, negative ``N`` is always valid.

        maxfiles : int or str
            Maximum number of :file:`.xnnn` files to save within a load step ( not available for :file:`.rdnn` files):

            * ``-1`` - Overwrite existing :file:`.xnnn` files (default). The total maximum number of
              :file:`.xnnn` files for one run is 999. If this number is reached before the analysis is complete,
              the program will reset the :file:`.xnnn` file numbering back to 1 and continue to write
              :file:`.xnnn` files; the program keeps the newest 999 restart files and overwrites the oldest
              restart files. For this option, the maximum number of files can be changed to a number less than 999
              by setting the MAXTotalFiles argument.

            * ``0`` - Do not overwrite any existing :file:`.xnnn` files. The total maximum number of
              :file:`.xnnn` files for one run is 999. If this number is reached before the analysis is complete,
              the analysis continues but no longer writes any :file:`.xnnn` files.

            * ``N`` - Maximum number of :file:`.xnnn` files to keep for each load step. When ``N``
              :file:`.xnnn` files have been written for a load step, the program overwrites the first
              :file:`.xnnn` file of that load step for subsequent substeps. ``N`` must be <= 999. If a total of
              999 restart files is reached before the analysis is complete, the analysis continues but writes no
              additional :file:`.xnnn` files.

        maxtotalfiles : str
            Total number of restart files to keep. Default = 999 for :file:`.xnnn` files and 99 for
            :file:`.rdnn` files. This option is valid only when ``MAXFILES`` = -1 (default).

            Valid ``MAXTotalFiles`` values are 1 through 999 for :file:`.xnnn` files, and 1 through 99 for
            :file:`.rdnn` files.

            When the total number of restart files written exceeds ``MAXTotalFiles``, the program resets the
            :file:`.xnnn` or :file:`.rdnn` file numbering back to 1 and continues to write :file:`.xnnn` or
            :file:`.rdnn` files. The newest files are retained and the oldest files are overwritten.

            The ``MAXtotalFiles`` value specified applies to all subsequent load steps. To reset it to the
            default, reissue the command with ``MAXTotalFiles`` = 0 or some negative value.

            If ``MAXTotalFiles`` is set to different values at different load steps, and if the value of
            ``MAXTotalFiles`` specified in the prior load step is larger than that of the current load step,
            the program can only overwrite the current number of maximum restart files up to the number
            ``MAXTotalFiles`` currently specified (which is smaller than the previous number).

            The recommended way to control the maximum number of restart files is to specify
            ``MAXTotalFiles`` at the first load step and not vary it in subsequent load steps. Also,
            ``MAXTotalFiles`` is best used when ``Ldstep`` = - ``N`` or ALL.

        filetype : str
            The type of restart file to be controlled by this command. Valid only when ``Action`` = DEFINE:

            * ``XNNN`` - Control :file:`.xnnn` files (default).

            * ``RDNN`` - Control :file:`.rdnn` remeshing database files. Needed only for a `nonlinear mesh
              adaptivity <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_
              analysis.

        Notes
        -----

        .. _RESCONTROL_notes:

        :ref:`rescontrol` sets up the restart parameters for a multiframe restart, enabling you to restart
        an analysis from any load step and substep for which there is an :file:`.xnnn` file. You can perform
        a multiframe restart for static and transient (full or mode-superposition method) analyses only. For
        more information about multiframe restarts and descriptions of the contents of the files used, see
        `Restarting an Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS3_12.html#bassolumodres>`_

        **Syntax**

        * Multiframe restart files are generically indicated here as :file:`.xnnn` files. They correspond to
          :file:`.rnnn` files for nonlinear static and full transient analyses, and :file:`.mnnn` files for
          mode-superposition analyses.
        * Remeshing database files are indicated as :file:`.rdnn` files. This type of restart file is needed
          only after remeshing during a `nonlinear mesh adaptivity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_ analysis.
        * When ``Action`` = DEFINE, the specified ``Filetype`` determines the type of file ( :file:`.xnnn`
          or :file:`.rdnn` ) controlled by this command.

        **Number of Restart Files Allowed**

        * The total number of restart files for any analysis cannot exceed 999 (for example,
          :file:`jobname.r001` to :file:`jobname.r999` ).
        * The total number of remeshing database files cannot exceed 99 (for example, :file:`jobname.rd01`
          to :file:`jobname.rd99` ).

        **Considerations for** `Nonlinear Mesh Adaptivity
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/advmnaexample.html>`_ Analysis

        * To control both  :file:`.xnnn` and :file:`.rdnn` file writing ( ``Filetype`` = XNNN and
          ``Filetype`` = RDNN, respectively), separate :ref:`rescontrol` commands are necessary.
        * ``Action`` = NORESTART and ``Ldstep`` = NONE are not valid and will cause the analysis to fail.
        * ``Ldstep`` = ``-N`` is not valid for controlling :file:`.xnnn` files.

        **Limiting the Number of Files Saved**

        * If you have many substeps for each load step and are writing :file:`.xnnn` files frequently, you
          may want to set ``MAXFILES`` to limit the number of :file:`.xnnn` files saved, as they can fill
          your disk quickly.
        * You can specify ``MAXFILES`` and ``Frequency`` for individual load steps. These arguments take on
          the default value or the value defined by :ref:`rescontrol`,,ALL, ``Frequency``, ``MAXFILES`` if
          they are not explicitly defined for a specific load step.
        * When :file:`.xnnn` files are written over many load steps, you may want to further limit the
          number of :file:`.xnnn` files by setting ``MAXTotalFiles``.

        **Maximum Number of Load Steps**

        * You can specify a maximum of ten load steps; that is, you can issue the :ref:`rescontrol`,,N
          command a maximum of ten times. Specified load steps cannot be changed in a restart.

        **Specifying** ``Ldstep`` = LAST or ``-N``

        * The program accepts only one occurrence of :ref:`rescontrol` with ``Ldstep`` = LAST. If you issue
          :ref:`rescontrol`,,LAST, ``Frequency``, ``MAXFILES`` multiple times, the last specification
          overwrites the previous one.
        * The program accepts only one occurrence of :ref:`rescontrol` with a negative ``Ldstep`` value (
          :ref:`rescontrol`, ``N`` where ``N`` is a negative number). If you issue :ref:`rescontrol`
          multiple times with a negative ``Ldstep`` value, the last specification overwrites the previous
          one.

        **Using** :ref:`rescontrol` in a Restarted Analysis

        * The :ref:`rescontrol` command is not valid in the restarted load step of a restart analysis. It is
          only valid in subsequent load steps.

        **Example Usage**

        * `Multiframe Restart
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS3_12.html#bassolumodres>`_
        * `Linear Perturbation Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strlinpertinputs.html#linpert2genpass>`_
        """
        command = f"RESCONTROL,{action},{ldstep},{frequency},{maxfiles},,{maxtotalfiles},{filetype}"
        return self.run(command, **kwargs)

    def outgeom(self, item: str = "", freq: str = "", **kwargs):
        r"""Controls geometry-related data written to the results file.

        Mechanical APDL Command: `OUTGEOM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OUTGEOM.html>`_

        Parameters
        ----------
        item : str
            Geometry data item for file write control:

            * ``MAT`` - Material Properties.

            * ``ERASE`` - Reset :ref:`outgeom` specifications to their default values.

            * ``STAT`` - List the current :ref:`outgeom` specifications.

        freq : str
            Specifies how often to write the specified geometry data:

            * ``NONE`` - Suppress writing of the specified item for all substeps.

            * ``ALL`` - Write the data of the specified item for every substep.

        Notes
        -----

        .. _OUTGEOM_notes:

        The :ref:`outgeom` command controls writing of the specified geometry ``Item`` to the results file.
        The geometry items correspond to the geometry records that are included in the results file (see the
        GEO records of the results file as described in ).

        The command generates a specification for controlling data storage by either activating storage of
        the specified geometry item ( ``Freq`` = ALL) or by suppressing storage of that item ( ``Freq`` =
        NONE).

        You can issue multiple :ref:`outgeom` commands in an analysis. After the initial command creates the
        storage specification, subsequent :ref:`outgeom` commands modify the specification set. The command
        processes your specifications in the order in which you input them. If you specify a given ``Item``
        twice, output is based upon the last specification.

        In addition to :ref:`outgeom`, :ref:`outpr` and :ref:`outres` also control solution output. You can
        issue up to 50 of these output-control commands (any combination of the three) in an analysis.

        :ref:`outgeom`,ERASE erases the existing output specifications and resets the counted number of
        :ref:`outgeom` commands to zero.

        When material property information is not written to the results file ( :ref:`outgeom`,MAT,NONE),
        clearing the database via ``/CLEAR`` and reading in a set of data in the general postprocessor (
        :ref:`post1` ) via the :ref:`set` command results in no material property data being stored in the
        database. In this case, the lack of material data prevents a successful solve from occurring with
        the modified database, and the results file is only applicable for carrying out post-processing.

        The :ref:`outgeom` command is also valid in :ref:`prep7`.
        """
        command = f"OUTGEOM,{item},{freq}"
        return self.run(command, **kwargs)

    def outres(
        self,
        item: str = "",
        freq: str = "",
        cname: str = "",
        nsvar: str = "",
        dsubres: str = "",
        **kwargs,
    ):
        r"""Controls the solution-result data written to the database.

        Mechanical APDL Command: `OUTRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OUTRES.html>`_

        Parameters
        ----------
        item : str
            Solution item for database and file-write control:

            * ``ALL`` - All solution items except LOCI, SVAR, and NAR (default).

            * ``BASIC`` - Write only NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX records to the results file and
              database.

            * ``ERASE`` - Resets :ref:`outres` specifications to their default values.

            * ``STAT`` - Lists the current :ref:`outres` specifications.

            * ``NSOL`` - Nodal degree-of-freedom solution.

            * ``RSOL`` - Nodal reaction loads.

            * ``V`` - Nodal velocity (applicable to structural transient analysis only ( :ref:`antype`,TRANS)).

            * ``A`` - Nodal acceleration (applicable to structural transient analysis only (
              :ref:`antype`,TRANS)).

            * ``CINT`` - All available results generated by :ref:`cint`.

            * ``SVAR`` - State variables (used with supported `subroutines that customize material behavior
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#b7K4rfblcd>`_ ).

            * ``ESOL`` - Enables or disables all of the following element-solution items. (These items can also be
              individually enabled or disabled.)

              * ``NLOAD`` - Element nodal, input constraint, and force loads (also used with POST1 commands
                :ref:`prrfor`, :ref:`nforce`, and :ref:`fsum` to calculate reaction loads).

              * ``STRS`` - Element nodal stresses.

              * ``EPEL`` - Element elastic strains.

              * ``EPTH`` - Element thermal, initial, and swelling strains.

              * ``EPPL`` - Element plastic strains.

              * ``EPCR`` - Element creep strains.

              * ``EPDI`` - Element diffusion strains.

              * ``FGRAD`` - Element nodal gradients.

              * ``FFLUX`` - Element nodal fluxes.

              * ``LOCI`` - Integration point locations.

              * ``VENG`` - Element energies.

              * ``MISC`` - Element miscellaneous data ( :ref:`etable` SMISC and NMISC items).

              * ``FMAG`` - Electromagnetic nodal forces.

              * ``CURD`` - Element source current density.

              * ``NLDAT`` - Element nonlinear data.

              * ``EHEAT`` - Element heat generation rate.

              * ``ETMP`` - Element temperatures.

              * ``SRFS`` - Element surface stresses.

              * ``CONT`` - Element contact data.

              * ``BKSTR`` - Element backstresses. Enabling this output also requires that you enable EPPL.

              * ``EANGL`` - Element Euler angles.

              * ``AESO`` - Enables or disables all of the following advanced element-solution output items. (These items cannot be individually enabled or disabled.)

                * BKS - Back-stress for kinematic hardening.
                * CDM - Damage variable for Mullins effect.
                * ESIG - BIOT's effective stress.
                * FFLX - Fluid flow flux in poromechanics.
                * FICT - Fictive temperature.
                * FSVAR - Fluence state variables.
                * MPLS - Microplane damage.
                * NS - Nominal strain.
                * PDMG - Progressive damage parameters.
                * PFC - Failure criteria based on the effective stresses in the damaged material.
                * PMSV - Permeability state variables.
                * SEND - Energy record.
                * TF - Thermal flux.
                * TG - Thermal gradient.
                * YSIDX - Yield status for geomechanical materials.

            * ``NAR`` - Enables or disables all of the following nodal-averaged solution items. (These items can also be
              individually enabled or disabled.)

              * ``NDST`` - Nodal-averaged stresses.

              * ``NDEL`` - Nodal-averaged elastic strains.

              * ``NDPL`` - Nodal-averaged plastic strains.

              * ``NDCR`` - Nodal-averaged creep strains.

              * ``NDTH`` - Nodal-averaged thermal and swelling strains.

        freq : str
            Specifies how often (that is, at which substeps) to write the specified solution item. The
            following values are valid:

             This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        cname : str
            The name of the component (created via :ref:`cm` ) defining the selected set of elements or
            nodes for which this specification is active. If not specified, the set is all entities. A
            component name is not allowed with the ALL, BASIC, or RSOL items.

        nsvar : str
            The number of user-defined state variables ( :ref:`tb`,STATE) to be written to the results file.
            Valid only when ``Item`` = SVAR and user-defined state variables exist. The specified value
            cannot exceed the total number of state variables defined; if no value is specified, all user-
            defined state variables are written to the results file. This argument acts on all sets of user-
            defined state variables that exist for the model.

        dsubres : str
            Specifies whether to write additional results in :file:`Jobname.DSUB` during a substructure or CMS
            `use pass
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/an9Auq1d6ldm.html#advobsl5jla062999>`_
            in a transient or harmonic analysis.

            * ```` - Write the nodal degree-of-freedom solution in :file:`Jobname.DSUB` (default).

            * ``ALL`` - In addition to the nodal degree-of-freedom solution, also write necessary data to
              compute quantities using nodal velocity and nodal acceleration (damping force, inertial force,
              kinetic energy, etc.) in the subsequent expansion pass. For more information, see `Step 3: Expansion
              Pass
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/axcAuq367ldm.html#adv5note4jla062999>`_

        Notes
        -----

        .. _OUTRES_notes:

        :ref:`outres` controls following output parameters:

        * The solution item ( ``Item`` ) to write to the database (and to the reduced displacement and
          results files)

        * The frequency ( ``Freq`` ) at which the solution item is written (applicable to static, transient,
          or full harmonic analyses)

        * The set of elements or nodes ( ``Cname`` ) to which your specification applies.

        The command generates a specification for controlling data storage for each substep, activating
        storage of the specified solution item for the specified substeps of the solution and suppressing
        storage of that item for all other substeps.

        You can issue :ref:`outres` multiple times in an analysis. After the initial command creating the
        storage specification, subsequent :ref:`outres` commands modify the specification set for each
        substep. The command processes your specifications at each substep in the order in which you input
        them. If you specify a given solution item twice, output is based upon the last specification.
        Therefore, issue multiple :ref:`outres` commands carefully and in the proper sequence.

        In addition to :ref:`outres`, these commands also control solution output: :ref:`outpr`,
        :ref:`outgeom`, and :ref:`osresult`.

        You can issue up to 50 output-control commands for :ref:`outres`, :ref:`outpr`, :ref:`outgeom` in an
        analysis. There is no limit on the number of :ref:`osresult` commands.

        :ref:`outres`,ERASE erases the existing output specifications and resets the counted number of
        :ref:`outres` commands to zero. The ERASE argument works in a similar manner for :ref:`outpr`,
        :ref:`outgeom`, and :ref:`osresult`.

        A given :ref:`outres` command generally has no effect on solution items not specified. For example,
        an :ref:`outres`,ESOL,LAST command does not affect NSOL data; that is, it neither activates nor
        suppresses NSOL data storage in any substep. An exception to this behavior involves the EANGL
        solution item.

        :ref:`outres` controls element Euler angle (EANGL) data output as follows:

        * When ``Freq`` = NONE, no element Euler angles are output at any substeps.

        * Without Euler angles, element results postprocessing can occur in the element solution coordinate
          system only (that is, :ref:`rsys` has no effect on element results); therefore, nodal averaging of
          element solution items may not be applicable when element solution coordinate systems are not
          uniform.

        * When ``Freq`` = any other value (including the command default), element Euler angles are output
          at substeps specified by ``Freq``, and at any substeps where one or more tensorial element
          solution items (STRS, EPEL, EPTH, EPPL, EPCR, EPDI, FGRAD, FFLUX, and AESO) are output.

        Additional results in the :file:`Jobname.DSUB` file (DSUBres = ALL) can only be requested in the
        first load step.

        In the results-item hierarchy, certain items are subsets of other items. For example, element
        solution (ESOL) data is a subset of all (ALL) solution data. An :ref:`outres`,ALL command can
        therefore affect ESOL data. Likewise, an :ref:`outres` command that controls ESOL data can affect a
        portion of all data.

         The :ref:`example <OUTRES_example>` :ref:`outres` commands illustrate the interrelationships between
        solution items and the necessity of issuing :ref:`outres` thoughtfully.

        To suppress all data at every substep, issue the :ref:`outres`,ALL,NONE command. (
        :ref:`outres`,ERASE does not suppress all data at every substep.)

        The NSOL, RSOL, V, and A solution items are associated with nodes. The CINT solution item is
        associated with fracture. All remaining solution items are associated with elements.

        Enabling nodal-averaged results ( ``Item`` = NAR or any of the associated labels) generally reduces
        the results file size, provided the equivalent element-based results are concurrently disabled. When
        nodal-averaged results are enabled, element values for stress and strain are averaged and stored as
        nodal values. Some limitations apply when using nodal averaged results. For more information and an
        example, see `Nodal-Averaged Results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_

        The boundary conditions (constraints and force loads) are written to the results file only if either
        nodal or reaction loads (NLOAD or RSOL items) are also written.

        When specifying a ``Freq`` value, observe the following:

        * For a modal analysis, only NONE or ALL are valid.

        * If you issue multiple :ref:`outres` commands during an analysis, you cannot specify a :ref:`key
          time array parameter (% <freqkap>` ``array%``) in a given :ref:`outres` command and then specify
          a different ``Freq`` option in a subsequent :ref:`outres` command.

        For additive manufacturing analyses during the build step ( :ref:`amstep`,BUILD), ``Freq`` refers to
        the layer number (for example, output ALL layers, LAST layer, or every ``N``  :sup:`th` layer).

        To specify selected results to output to the database, see :ref:`osresult`.

        :ref:`outres` is also valid in PREP7.

        **Example**

        .. _OUTRES_example:

        When issuing an :ref:`outres` command, think of a matrix in which you set switches on and off. When
        a switch is on, a solution item is stored for the specified substep. When a switch is off, a
        solution item is suppressed for a specified substep.

        Assuming a static ( :ref:`antype`,STATIC) analysis, this example shows how the matrix looks after
        issuing each :ref:`outres` command in this six-substep solution.

        .. code:: apdl

           NSUBST,6
           OUTRES,ERASE
           OUTRES,NSOL,2
           OUTRES,ALL,3
           OUTRES,ESOL,4
           SOLVE

        To simplify the example, only a subset of the available solution items appears in the matrix.

        :ref:`outres`,ERASE -- After issuing this command, the default output specifications are in effect,
        as shown:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        :ref:`outres`,NSOL,2 -- This command modifies the initial specifications so that NSOL is enabled for
        substeps 2, 4 and 6, and disabled for substeps 1, 3 and 5, as shown:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        :ref:`outres`,ALL,3 -- This command further modifies the specifications so that ALL is enabled for
        substeps 3 and 6, and disabled for substeps 1, 2, 4 and 5, as shown:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        :ref:`outres`,ESOL,4 -- This command once again modifies the specifications so that ESOL is enabled
        for the fourth and last substeps, and disabled for substeps 1, 2, 3 and 5, as shown:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        :ref:`solve`

        When obtaining the solution, results data are stored as follows:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"OUTRES,{item},{freq},{cname},,{nsvar},{dsubres}"
        return self.run(command, **kwargs)

    def osresult(
        self, item: str = "", comp: str = "", freq: str = "", cname: str = "", **kwargs
    ):
        r"""Controls the selected result data written to the database.

        Mechanical APDL Command: `OSRESULT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OSRESULT.html>`_

        Parameters
        ----------
        item : str
            Item to output to the database. See :ref:`OSRESULT_tab_1`.

        comp : str
            Component of ``Item`` to output to the database. See :ref:`OSRESULT_tab_1`.

        freq : str
            Frequency to output to the database.

            * ``n`` - Writes every ``n`` th and last substep of each load step.

            * ``-n`` - Writes up to ``n`` equally spaced substeps of each load step.

            * ``ALL`` - Writes every substep.

            * ``LAST`` - Writes the last substep of each load step (default).

        cname : str
            The name of an element component ( :ref:`cm` ) defining the set of elements for which this
            specification is active. If not specified, the set is all elements.

        Notes
        -----

        .. _OSRESULT_notes:

        :ref:`osresult` controls output to the results database for the selected result defined by the item
        and component combination. The command activates output of the selected result for the specified
        substeps and elements. Multiple commands for the same result are cumulative. No selected results are
        written to the database unless specified via an :ref:`osresult` command.

        :ref:`osresult`,ERASE deletes the existing output specifications.

        :ref:`osresult`,STATUS lists the current set of selected result specifications.

        The output of selected results is valid for static ( :ref:`antype`,STATIC) and transient (
        :ref:`antype`,TRANS) analysis types.

        To specify other results to output to the database, see :ref:`outres`.

        Element quantities specified via :ref:`outres` can be redundant to those specified via
        :ref:`osresult`. Avoid specifying redundant quantities, as they are stored and processed separately.

        This command is also valid in PREP7.

        .. _OSRESULT_tab_1:

        OSRESULT - Item and Component Labels
        ************************************

        .. flat-table:: **Component Name Method**
           :header-rows: 1

           * - **Item**
             - **Comp**
             - **Description**
           * - ERASE
             - --
             - Erases all selected result output specifications.
           * - STATUS
             - --
             - Lists the current set of selected result output specifications.
           * - SVAR
             - 1,2,3,..., ``N``
             - State variable number.
           * - FLD
             - UF01, UF02,..., UF09
             - User-defined field variables

        """
        command = f"OSRESULT,{item},{comp},{freq},{cname}"
        return self.run(command, **kwargs)

    def outpr(self, item: str = "", freq: str = "", cname: str = "", **kwargs):
        r"""Controls the solution printout.

        Mechanical APDL Command: `OUTPR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_OUTPR.html>`_

        Parameters
        ----------
        item : str
            Item for print control:

            * ``BASIC`` - Basic quantities (nodal DOF solution, nodal reaction loads, and element solution)
              (default).

            * ``NSOL`` - Nodal DOF solution.

            * ``RSOL`` - Nodal reaction loads.

            * ``ESOL`` - Element solution.

            * ``NLOAD`` - Element nodal loads. When `nonlinear stabilization
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRUNST.html#>`_ is active,
              the stabilization force/moments are also printed.

            * ``SFOR`` - Stabilization force/moment at the applicable nodes (valid only when `nonlinear
              stabilization <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRUNST.html#>`_
              is active).

            * ``VENG`` - Element energies. When `nonlinear stabilization
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRUNST.html#>`_ is active,
              the energy dissipation due to stabilization is also printed.

            * ``RSFO`` - Result section force/moment output (valid only when a `result section
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_resultsec.html#>`_ is defined).
              Result section output is always written to a file named :file:`JobnameSECF`.

            * ``V`` - Nodal velocity (applicable to structural transient analysis only ( :ref:`antype`,TRANS)).

            * ``A`` - Nodal acceleration (applicable to structural transient analysis only (
              :ref:`antype`,TRANS)).

            * ``ALL`` - All of the above solution items.

        freq : str
            Print solution for this item every ``Freq``  :sup:`th` (and the last) substep of each load step.
            If - ``n``, print up to ``n`` equally spaced solutions (only applies to static or full transient
            analyses when automatic time stepping is enabled). If NONE, suppress all printout for this item
            for this load step. If ALL, print solution for this item for every substep. If LAST, print
            solution for this item only for the last substep of each load step. For a modal analysis, use
            NONE or ALL.

        cname : str
            Name of the component, created with the :ref:`cm` command, defining the selected set of nodes or
            elements for which this specification is active. If blank, the set is all entities.

            The component named must be of the same type as the item, i.e. nodal or element. A component
            name is not allowed with the BASIC, RSFO, or ALL labels.

        Notes
        -----

        .. _OUTPR_notes:

        Controls the solution items to be printed, the frequency with which they are printed (in static,
        transient, or full harmonic analyses), and the set of nodes or elements to which this specification
        applies (in static, transient, or full harmonic analyses). An item is associated with either a node
        ( :ref:`nsol`, :ref:`rforce`, V, and A items) or an element (all of the remaining items). The
        specifications are processed in the order that they are input. Use :ref:`outpr`,STAT to list the
        current specifications and use :ref:`outpr`,ERASE to erase all the current specifications.

        In addition to :ref:`outpr`, :ref:`outres` and :ref:`outgeom` also control solution output. You can
        issue up to 50 of these output-control commands (any combination of the three) in an analysis.

        As described above, :ref:`outpr` writes some or all items (depending on analysis type) for all
        elements. To restrict the solution printout, use :ref:`outpr` to selectively suppress ( ``Freq`` =
        NONE) the writing of solution data, or first suppress the writing of all solution data (
        :ref:`outpr`,ALL,NONE) and then selectively turn on the writing of solution data with subsequent
        :ref:`outpr` commands.

        If the generalized plane strain feature is active and :ref:`outpr` is issued, the change of fiber
        length at the ending point during deformation and the rotation of the ending plane about X and Y
        during deformation will be printed if any displacement at the nodes is printed. The reaction forces
        at the ending point will be printed if any reaction force at the nodes is printed.

        Nodal reaction loads ( ``Item`` = RSOL) are processed according to the specifications listed for the
        :ref:`prrsol` command.

        Result printouts for interactive sessions are suppressed for models with more than 10 elements
        except when the printout is redirected to a file using the :ref:`output` command.

        This command is also valid in PREP7.
        """
        command = f"OUTPR,{item},{freq},{cname}"
        return self.run(command, **kwargs)

    def wsprings(self, **kwargs):
        r"""Creates weak springs on corner nodes of a bounding box of the currently selected elements.

        Mechanical APDL Command: `WSPRINGS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_WSPRINGS.html>`_

        Notes
        -----

        .. _WSPRINGS_notes:

        This command invokes a predefined Mechanical APDL macro that is used during the import of loads from
        the
        ADAMS program into Mechanical APDL.

        The command creates weak springs on the corner nodes of the bounding box of the currently selected
        elements. The six nodes of the bounding box are attached to ground using ``COMBIN14``elements. The
        stiffness is chosen as a small number and can be changed by changing the real constants of the
        ``COMBIN14``elements.

        The command works only for models that have a geometric extension in two or three dimensions. One-
        dimensional problems (pure beam in one axis) are not supported.

        For more information about how :ref:`wsprings` is used during the transfer of loads from the ADAMS
        program to Mechanical APDL, see `Import Loads into Mechanical APDL
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advtrans12902.html#advimport>`_.

         Distributed-Memory Parallel (DMP) Restriction This command is not supported in a DMP solution.
        """
        command = "WSPRINGS"
        return self.run(command, **kwargs)

    def ic(
        self,
        node: str = "",
        lab: str = "",
        value: str = "",
        value2: str = "",
        nend: str = "",
        ninc: str = "",
        **kwargs,
    ):
        r"""Specifies initial conditions at nodes.

        Mechanical APDL Command: `IC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_IC.html>`_

        Parameters
        ----------
        node : str
            Node at which initial condition is to be specified. If ALL, apply to all selected nodes (
            :ref:`nsel` ). If ``NODE`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may be substituted for ``NODE``.

        lab : str
            Degree-of-freedom label for which the initial condition is to be specified. If ALL, use all
            appropriate labels.

            * **Structural labels** : UX, UY, or UZ (displacements); ROTX, ROTY, or ROTZ (rotations); HDSP
              (hydrostatic pressure); PRES (pore pressure)
            * For structural static and transient analyses, specify translational and rotational velocities as
              initial conditions using these labels: VELX, VELY, VELZ (translational velocities); OMGX, OMGY,
              OMGZ (rotational velocities).
            * For structural transient analysis, specify translational and rotational accelerations as initial
              conditions using these labels: ACCX, ACCY, ACCZ (translational accelerations); DMGX, DMGY, DMGZ
              (rotational accelerations).
            * The velocity and acceleration initial conditions are not included with ``Lab`` = ALL.
            * **Thermal labels** : TEMP, TBOT, TE2, TE3,..., TTOP (temperature)
            * **Magnetic labels** : MAG (scalar magnetic potential); AZ (vector magnetic potential)
            * **Diffusion label** : CONC (concentration)
            * **Acoustic label** : ENKE (acoustic energy density)

        value : str
            Initial value of the degree of freedom. Defaults to the program default for that degree of
            freedom (0.0 for structural analysis, :ref:`tunif` for thermal analysis, etc.). Values are in
            the nodal coordinate system and in radians for rotational degrees of freedom.

        value2 : str
            Second-order degree of freedom value, mainly used for non-structural DOF where VELX can't be
            used. Defaults to the program default for that degree of freedom (0.0 for structural analysis).
            Values are in the nodal coordinate system and in radians/time for rotational degrees of freedom.

        nend : str
            Specifies the same initial condition values at the range of nodes from ``NODE`` to ``NEND``
            (defaults to ``NODE`` ), in steps of ``NINC`` (defaults to 1).

        ninc : str
            Specifies the same initial condition values at the range of nodes from ``NODE`` to ``NEND``
            (defaults to ``NODE`` ), in steps of ``NINC`` (defaults to 1).

        Notes
        -----

        .. _IC_notes:

        The :ref:`ic` command specifies initial conditions, which are the initial values of the specified
        degrees of freedom. It is valid only for a static analysis and full method transient analysis (
        :ref:`timint`,ON and :ref:`trnopt`,FULL). For the transient, the initial value is specified at the
        beginning of the first load step, that is, at time = 0.0.

        If constraints ( :ref:`d`, :ref:`dsym`, etc.) and initial conditions are applied at the same node,
        the constraint specification overrides. Exercise caution when specifying constraints. The degree-of-
        freedom values start from zero, or the first value given in the table when table name is specified.
        To match the nonzero initial condition value with the initial value for degree-of-freedom
        constraint, use a table for the degree-of-freedom constraint.

        For thermal analyses, any :ref:`tunif` specification should be applied before the :ref:`ic` command;
        otherwise, the :ref:`tunif` specification is ignored. If the :ref:`ic` command is input before any
        :ref:`tunif` specification, use the :ref:`icdele` command and then reissue any :ref:`tunif`
        specification and then follow with the :ref:`ic` command.

        When issuing the :ref:`ic` command for elements ``SOLID278`` `Layered Thermal Solid
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_SOLID278.html#SOLID278L.fig.1>`_
        and ``SOLID279`` `Layered Thermal Solid
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_SOLID279.html#SOLID279L.fig.1>`_
        with through-the-thickness degrees of freedom (KEYOPT(3) = 2), layers are always interpolated
        linearly based on the location of the degrees of freedom.

        Define consistent initial conditions. For example, if you define an initial velocity at a single
        degree of freedom, the initial velocity at every other degree of freedom will be 0.0, potentially
        leading to conflicting initial conditions. In most cases, you should define initial conditions at
        every unconstrained degree of freedom in your model. If you define an initial condition for any
        degree of freedom at the pilot node of a rigid body (see `Modeling Rigid Bodies
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctecrigidbodies.html#strmodrigidbod>`_
        in the `Contact Technology Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_flpressexamp.html>`_ for the
        definition of rigid body), then the same initial condition must also be
        defined for the same degree of freedom on all other nodes of the rigid body.

        After a solution has been performed, the specified initial conditions are overwritten by the actual
        solution and are no longer available. You must respecify them if you want to perform a subsequent
        analysis. You may want to keep a database file saved prior to the first solution for subsequent
        reuse.

        If you use the :ref:`cdwrite` command to archive your model, initial displacements, temperatures,
        etc. specified via the :ref:`ic` command are not written to the archive file; initial velocities and
        accelerations are written.

        This command is also valid in PREP7.
        """
        command = f"IC,{node},{lab},{value},{value2},{nend},{ninc}"
        return self.run(command, **kwargs)

    def icrotate(
        self,
        node: str = "",
        omega: str = "",
        x1: str = "",
        y1: str = "",
        z1: str = "",
        x2: str = "",
        y2: str = "",
        z2: str = "",
        vx: str = "",
        vy: str = "",
        vz: str = "",
        accel: str = "",
        **kwargs,
    ):
        r"""Specifies initial velocity at nodes as a sum of rotation about an axis and translation.

        Mechanical APDL Command: `ICROTATE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ICROTATE.html>`_

        Parameters
        ----------
        node : str
            Node at which the initial velocity is to be specified. If ALL, apply to all selected nodes (
            :ref:`nsel` ). A component name may be input for ``NODE``.

        omega : str
            Scalar rotational velocity about the rotational axis.

        x1 : str
            Coordinates (in the global Cartesian coordinate system) of the beginning point of the rotational
            axis vector.

        y1 : str
            Coordinates (in the global Cartesian coordinate system) of the beginning point of the rotational
            axis vector.

        z1 : str
            Coordinates (in the global Cartesian coordinate system) of the beginning point of the rotational
            axis vector.

        x2 : str
            Coordinates (in the global Cartesian coordinate system) of the end point of the rotational axis
            vector.

        y2 : str
            Coordinates (in the global Cartesian coordinate system) of the end point of the rotational axis
            vector.

        z2 : str
            Coordinates (in the global Cartesian coordinate system) of the end point of the rotational axis
            vector.

        vx : str
            Initial translational velocity in direction x of the nodal coordinate system.

        vy : str
            Initial translational velocity in direction y of the nodal coordinate system.

        vz : str
            Initial translational velocity in direction z of the nodal coordinate system.

        accel : str
            Key to initialize acceleration due to centrifugal effects:

            * ``(blank)`` - Do not initialize acceleration (default).

            * ``CENT`` - Initialize acceleration due to centrifugal effects along with the initial velocity.

        Notes
        -----

        .. _ICROTATE_notes:

        The :ref:`icrotate` command specifies initial velocity for all translational degrees of freedom of
        the specified nodes. The velocity value is a combination of velocity due to rotation about an axis
        and translation. The velocity at the node is calculated as:

        :math:``

        where

        * v :sup:`N` = velocity of node ``N`` in the nodal coordinate system
        * v :sup:`trans` = translational velocity input as [ ``Vx``, ``Vy``, ``Vz`` ]
        * ω = scalar angular velocity input as ``OMEGA``
        * x :sup:`1` and x :sup:`2` denote the coordinates of points prescribing the beginning [ ``X1``,
          ``Y1``, ``Z1`` ] and end [ ``X2``, ``Y2``, ``Z2`` ] of the rotation axis
        * x :sup:`N` denotes the coordinates of node ``N``

        All coordinates are input in the global Cartesian coordinate system, and the velocity due to
        rotation is then converted to the nodal coordinate system and added to the prescribed translation.

        If ``ACCEL`` = CENT is specified, acceleration due to centrifugal effects is initialized as well.
        The acceleration at node a :sup:`N` is initialized as:

        :math:``

        The :ref:`icrotate` command is valid only for static analysis and full method transient analysis (
        :ref:`timint`,ON with :ref:`trnopt`,FULL). The initial value is specified at the beginning of the
        first load step; that is, at time = 0.0.

        The command calculates the nodal velocities and saves them in the database as if the :ref:`ic`
        command had been used to calculate these velocities. Thus, when the :file:`Jobname.CDB` or
        :file:`Jobname.DB` file is written, the velocities prescribed by the :ref:`icrotate` command appear
        as :ref:`ic` commands. All assumptions, recommendations, and restrictions for the :ref:`ic` command
        are also true for the :ref:`icrotate` command.

        This command is also valid in PREP7.
        """
        command = f"ICROTATE,{node},{omega},{x1},{y1},{z1},{x2},{y2},{z2},{vx},{vy},{vz},{accel}"
        return self.run(command, **kwargs)

    def icdele(self, **kwargs):
        r"""Deletes initial conditions at nodes.

        Mechanical APDL Command: `ICDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ICDELE.html>`_

        Notes
        -----

        .. _ICDELE_notes:

        Deletes all initial conditions previously specified with the :ref:`ic` or :ref:`icrotate` command at
        all nodes.

        This command is also valid in PREP7.
        """
        command = "ICDELE"
        return self.run(command, **kwargs)

    def iclist(
        self, node1: str = "", node2: str = "", ninc: str = "", lab: str = "", **kwargs
    ):
        r"""Lists the initial conditions.

        Mechanical APDL Command: `ICLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ICLIST.html>`_

        Parameters
        ----------
        node1 : str
            List initial conditions for nodes ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NODE1`` = ALL (default), ``NODE2`` and ``NINC`` are ignored and
            initial conditions for all selected nodes ( :ref:`nsel` ) are listed. If ``NODE1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        node2 : str
            List initial conditions for nodes ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NODE1`` = ALL (default), ``NODE2`` and ``NINC`` are ignored and
            initial conditions for all selected nodes ( :ref:`nsel` ) are listed. If ``NODE1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        ninc : str
            List initial conditions for nodes ``NODE1`` to ``NODE2`` (defaults to ``NODE1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NODE1`` = ALL (default), ``NODE2`` and ``NINC`` are ignored and
            initial conditions for all selected nodes ( :ref:`nsel` ) are listed. If ``NODE1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may be substituted for ``NODE1`` ( ``NODE2`` and ``NINC`` are ignored).

        lab : str
            Label identifying the initial condition to list out:

            * ``DISP`` - Displacements, temperature, etc. (default).

            * ``VELO`` - Velocities.

            * ``ACC`` - Accelerations.

        Notes
        -----

        .. _ICLIST_notes:

        Lists the initial conditions specified by the :ref:`ic`  or :ref:`icrotate`  command. Listing
        applies to all the selected nodes ( :ref:`nsel` ) and DOF labels. :ref:`iclist` is not the same as
        the :ref:`dlist` command. All the initial conditions including the default conditions are listed for
        the selected nodes.

        This command is valid in any processor.
        """
        command = f"ICLIST,{node1},{node2},{ninc},{lab}"
        return self.run(command, **kwargs)

    def anpres(
        self,
        nfram: str = "",
        delay: str = "",
        ncycl: str = "",
        refframe: int | str = "",
        **kwargs,
    ):
        r"""Produces an animated sequence of the time-harmonic pressure variation of an engine-order excitation
        in a cyclic harmonic analysis.

        Mechanical APDL Command: `ANPRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANPRES.html>`_

        Parameters
        ----------
        nfram : str
            Number of frame captures per cycle. Defaults to 3 times the number of sectors.

        delay : str
            Time delay (seconds) during animation. Defaults to 0.1 seconds.

        ncycl : str
            Number of animation cycles. Defaults to 5.

        refframe : int or str
            Reference frame for the model rotation.

            * ``0`` - Rotating reference frame (default). The model remains fixed in space and the pressure
              revolve around the model.

            * ``1`` - Stationary reference frame. The model rotates and the pressure locations remain fixed in
              space.

        Notes
        -----

        .. _ANPRES_notes:

        :ref:`anpres` invokes a macro which produces an animated sequence of the time-harmonic applied
        pressure in the case of a mode-superposition harmonic analysis ( :ref:`antype`,HARMIC with
        :ref:`cycopt`,MSUP,ON). The engine-order excitation must also have been specified (
        :ref:`cycfreq`,EO). While pressure loads are not accepted as valid loading in a mode-superposition
        analysis (they must be applied in the modal analysis and the modal load vector applied in the mode-
        superposition analysis) you can apply them for the purposes of this animation.

        For ``RefFrame`` = 1 (stationary reference frame), the rotational velocity from the Linear
        Perturbation step, or the current :ref:`omega` or :ref:`cgomga` value, is used to determine the
        rotation direction about the cyclic cylindrical axis, otherwise a positive rotation is assumed.

        You may use :ref:`hbc`,,ON to hide overlapping pressure faces, and use :ref:`gline`,,-1 to suppress
        the element outlines if desired.
        """
        command = f"ANPRES,{nfram},{delay},{ncycl},{refframe}"
        return self.run(command, **kwargs)

    def aport(
        self,
        portnum: str = "",
        label: str = "",
        kcn: str = "",
        pres: str = "",
        phase: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        **kwargs,
    ):
        r"""Specifies input data for plane wave and acoustic duct ports.

        Mechanical APDL Command: `APORT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_aport.html>`_

        Parameters
        ----------
        portnum : str
            Port number. This number is associated with an exterior port or interior port previously
            specified by the :ref:`sf` and :ref:`bf` family of commands, respectively. The number must be
            between 1 and 50.

        label : str
            * ``PLAN`` - Incident plane wave.

            * ``RECT`` - Rectangular duct.

            * ``CIRC`` - Circular duct.

            * ``COAX`` - Coaxial duct.

            * ``LIST`` - List the port settings. If ``PortNum`` = ALL, list the port settings for all defined
              ports.

            * ``DELE`` - Delete defined ports. If ``PortNum`` = ALL, delete all defined ports.

        kcn : str
            A previously-defined local ( ``KCN`` >10) or global ( ``KCN`` = 0) Cartesian coordinate system
            number used to specify the geometric properties of the duct. Defaults to the global Cartesian
            coordinate system (0). The local Z-direction must be the direction of wave propagation. The
            origin of the local coordinate system must be centered about the face of the duct port without
            considering symmetry.

        pres : str
            Zero-to-peak amplitude of the pressure. If blank, the port will appear as a matching impedance.

        phase : str
            Phase angle of the applied pressure in degrees. Defaults to 0.

        val1 : str
            Additional input. The meaning of ``VAL1`` through ``VAL4`` varies depending on the specified
            ``Label``.

            ``Label`` = PLAN:

            * ``VAL1`` - :math:``  angle from positive X-axis to positive Y-axis
              in the local Cartesian coordinates                                        ( ``KCN`` ).

            * ``VAL2`` - :math:``  angle away from positive Z-axis in the local
              Cartesian coordinates ( ``KCN`` ).

            * ``VAL3-VAL4`` - Not used.

            ``Label`` = RECT:

            * ``VAL1`` - Width of the rectangular duct.

            * ``VAL2`` - Height of the rectangular duct.

            * ``VAL3`` - Mode index for pressure variation along the width (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the height (defaults to 0).

            ``Label`` = CIRC:

            * ``VAL1`` - Radius of the circular duct.

            * ``VAL2`` - Not used.

            * ``VAL3`` - Mode index for pressure variation along the azimuth (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the radii (defaults to 0).

            ``Label`` = COAX:

            * ``VAL1`` - Inner radius of the coaxial duct.

            * ``VAL2`` - Outer radius of the coaxial duct.

            * ``VAL3`` - Mode index for pressure variation along the azimuth (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the radii (defaults to 0).

        val2 : str
            Additional input. The meaning of ``VAL1`` through ``VAL4`` varies depending on the specified
            ``Label``.

            ``Label`` = PLAN:

            * ``VAL1`` - :math:``  angle from positive X-axis to positive Y-axis
              in the local Cartesian coordinates                                        ( ``KCN`` ).

            * ``VAL2`` - :math:``  angle away from positive Z-axis in the local
              Cartesian coordinates ( ``KCN`` ).

            * ``VAL3-VAL4`` - Not used.

            ``Label`` = RECT:

            * ``VAL1`` - Width of the rectangular duct.

            * ``VAL2`` - Height of the rectangular duct.

            * ``VAL3`` - Mode index for pressure variation along the width (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the height (defaults to 0).

            ``Label`` = CIRC:

            * ``VAL1`` - Radius of the circular duct.

            * ``VAL2`` - Not used.

            * ``VAL3`` - Mode index for pressure variation along the azimuth (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the radii (defaults to 0).

            ``Label`` = COAX:

            * ``VAL1`` - Inner radius of the coaxial duct.

            * ``VAL2`` - Outer radius of the coaxial duct.

            * ``VAL3`` - Mode index for pressure variation along the azimuth (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the radii (defaults to 0).

        val3 : str
            Additional input. The meaning of ``VAL1`` through ``VAL4`` varies depending on the specified
            ``Label``.

            ``Label`` = PLAN:

            * ``VAL1`` - :math:``  angle from positive X-axis to positive Y-axis
              in the local Cartesian coordinates                                        ( ``KCN`` ).

            * ``VAL2`` - :math:``  angle away from positive Z-axis in the local
              Cartesian coordinates ( ``KCN`` ).

            * ``VAL3-VAL4`` - Not used.

            ``Label`` = RECT:

            * ``VAL1`` - Width of the rectangular duct.

            * ``VAL2`` - Height of the rectangular duct.

            * ``VAL3`` - Mode index for pressure variation along the width (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the height (defaults to 0).

            ``Label`` = CIRC:

            * ``VAL1`` - Radius of the circular duct.

            * ``VAL2`` - Not used.

            * ``VAL3`` - Mode index for pressure variation along the azimuth (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the radii (defaults to 0).

            ``Label`` = COAX:

            * ``VAL1`` - Inner radius of the coaxial duct.

            * ``VAL2`` - Outer radius of the coaxial duct.

            * ``VAL3`` - Mode index for pressure variation along the azimuth (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the radii (defaults to 0).

        val4 : str
            Additional input. The meaning of ``VAL1`` through ``VAL4`` varies depending on the specified
            ``Label``.

            ``Label`` = PLAN:

            * ``VAL1`` - :math:``  angle from positive X-axis to positive Y-axis
              in the local Cartesian coordinates                                        ( ``KCN`` ).

            * ``VAL2`` - :math:``  angle away from positive Z-axis in the local
              Cartesian coordinates ( ``KCN`` ).

            * ``VAL3-VAL4`` - Not used.

            ``Label`` = RECT:

            * ``VAL1`` - Width of the rectangular duct.

            * ``VAL2`` - Height of the rectangular duct.

            * ``VAL3`` - Mode index for pressure variation along the width (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the height (defaults to 0).

            ``Label`` = CIRC:

            * ``VAL1`` - Radius of the circular duct.

            * ``VAL2`` - Not used.

            * ``VAL3`` - Mode index for pressure variation along the azimuth (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the radii (defaults to 0).

            ``Label`` = COAX:

            * ``VAL1`` - Inner radius of the coaxial duct.

            * ``VAL2`` - Outer radius of the coaxial duct.

            * ``VAL3`` - Mode index for pressure variation along the azimuth (defaults to 0).

            * ``VAL4`` - Mode index for pressure variation along the radii (defaults to 0).

        Notes
        -----

        .. _APORT_notes:

        Use the :ref:`aport` command to launch a specified analytic acoustic mode into a guided duct.

        The low-order ``FLUID30``element does not support the higher modes in the coaxial duct ( ``Label`` =
        COAX).

        For more information, see `Specified Mode Excitation in an Acoustic Duct
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_acous/acous_excit_src.html#>`_
        `Analytic Port Modes in a Duct
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thyacous_proprad.html#eq897eb704-ab8d-4c80-aa70-eeda53797cc5>`_
        """
        command = (
            f"APORT,{portnum},{label},{kcn},{pres},{phase},,{val1},{val2},{val3},{val4}"
        )
        return self.run(command, **kwargs)

    def awave(
        self,
        wavenum: str = "",
        wavetype: str = "",
        opt1: str = "",
        opt2: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        val9: str = "",
        val10: str = "",
        val11: str = "",
        val12: str = "",
        val13: str = "",
        **kwargs,
    ):
        r"""Specifies input data for an acoustic incident wave.

        Mechanical APDL Command: `AWAVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AWAVE.html>`_

        Parameters
        ----------
        wavenum : str
            Wave number. You specify the integer number for an acoustic incident wave inside or outside the
            model. The number must be between 1 and 20.

        wavetype : str
            Wave type:

            * ``PLAN`` - Planar incident wave

            * ``MONO`` - Monopole or pulsating sphere incident wave

            * ``DIPO`` - Dipole incident wave

            * ``BACK`` - Back enclosed loudspeaker

            * ``BARE`` - Bare loudspeaker

            * ``STATUS`` - Displays the status of the acoustic wave settings if ``Wavenum`` = a number between 1
              and 20 or ALL.

            * ``DELE`` - Deletes the acoustic wave settings if ``Wavenum`` = a number between 1 and 20 or ALL.

        opt1 : str
            * ``PRES`` - Pressure

            * ``VELO`` - Velocity

        opt2 : str
            * ``EXT`` - Incident wave outside the model.

            * ``INT`` - Incident wave inside the model. This option is only available for pure scattered
              pressure formulation.

            For ``Wavetype`` = PLAN, only ``Opt2`` = EXT is available.

        val1 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val2 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val3 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val4 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val5 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val6 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val7 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val8 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val9 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val10 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val11 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val12 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        val13 : str
            If ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL1`` - Amplitude of pressure or normal velocity to the sphere surface.

            * ``VAL2`` - Phase angle of the applied pressure or velocity (in degrees). Defaults to 0 degrees.

            If ``Wavetype`` = PLAN:

            * ``VAL3`` - Incident ϕ angle from x axis toward y axis.

            * ``VAL4`` - Incident θ angle from z axis toward y axis.

            * ``VAL5`` - Not used.

            If ``Wavetype`` = MONO, DIPO, BACK, or BARE:

            * ``VAL3 - VAL5`` - Global Cartesian coordinate values of source position.

             If
             ``Wavetype`` = PLAN, MONO, DIPO, BACK, or BARE:

            * ``VAL6`` - Mass density of base medium (defaults to 1.2041 kg/m3).

            * ``VAL7`` - Speed of sound in base medium (defaults to 343.24 m/s).

            * ``VAL8`` - Radius of pulsating sphere (not used for ``Wavetype`` = PLAN).

            * ``VAL9`` - Dipole length (only available for ``Wavetype`` = DIPO, BARE).

            * ``VAL10 - VAL12`` - Unit vector of dipole axis from the positive to the negative. Only available
              for ``Wavetype`` = DIPO, BARE.

            * ``VAL13`` - Port number if the incident power is required on the port

        Notes
        -----
        Use the :ref:`asol` command to activate the scattered field algorithm and the :ref:`ascres` command
        for output control with the scattered field algorithm. Refer to `Acoustics
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thyacous_poroelastic.html>`_


        """
        command = f"AWAVE,{wavenum},{wavetype},{opt1},{opt2},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10},{val11},{val12},{val13}"
        return self.run(command, **kwargs)

    def asifile(
        self,
        opt: str = "",
        fname: str = "",
        ext: str = "",
        oper: str = "",
        kdim: str = "",
        kout: str = "",
        limit: str = "",
        resopt: str = "",
        **kwargs,
    ):
        r"""Writes or reads one-way acoustic-structural coupling data.

        Mechanical APDL Command: `ASIFILE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ASIFILE.html>`_

        Parameters
        ----------
        opt : str
            Command behavior option:

            * ``WRITE`` - Write the structural results to the specified file.

            * ``READ`` - Read the structural results from the specified file. This option is invalid during
              :ref:`post1` postprocessing.

        fname : str
            File name and directory path of a one-way acoustic-structural coupling data file (248 characters
            maximum, including the characters needed for the directory path). An unspecified directory path
            defaults to the working directory; in this case, you can use all 248 characters for the file
            name (defaults to :file:`jobname` ).

        ext : str
            File name extension of the one-way acoustic-structural coupling data file (defaults to
            :file:`.asi` ).

        oper : str
            Command operation:

            * ``NOMAP`` - No mapping occurs between the structural and acoustic models when reading the
              structural results from the specified file (default).

            * ``MAP`` - Maps the results from the structural to the acoustic model. (See :ref:`ASIFILE_notes`.)

        kdim : str
            Interpolation criteria. Valid only when ``Oper`` = MAP.

            If ``kDim`` = 2 or 0, two-dimensional interpolation is applied (that is, interpolate occurs on a
            surface).

        kout : str
            Outside region results. Valid only when ``Oper`` = MAP.

            If ``kOut`` = 0, use the value(s) of the nearest region point for points outside of the region.

            If ``kOut`` = 1, set results extrapolated outside of the region to zero.

        limit : str
            Number of nearby nodes considered for interpolation. Valid only when ``Oper`` = MAP.

            Minimum = 5. Default = 20.

            Lower values reduce processing time; however, some distorted or irregular meshes require a
            higher value to encounter three nodes for triangulation.

        resopt : str
            Transient results option:

            * ``ACEL`` - Output or input the particle acceleration in a transient analysis (default).

            * ``VELO`` - Output or input the particle velocity in a transient analysis.

        Notes
        -----

        .. _ASIFILE_notes:

        The :ref:`asifile` command writes to, or reads from, a file containing one-way acoustic-structural
        coupling data.

        Results data on the one-way coupling interface (defined by the :ref:`sf`,,FSIN command) in the
        structural model are written to the one-way coupling result data file during the structural
        solution.

        By default, one-way coupling results data are read into the acoustic model as the velocity
        (harmonic) or acceleration (transient) excitation during the sequential acoustic solution. If the
        transient is to be solved with the velocity potential formulation in acoustics, set ``ResOpt`` =
        VELO to write/read the results data as velocity excitation.

        If ``Oper`` = NOMAP, both structural and acoustic models must share the same node number on the one-
        way coupling interface.

        If ``Oper`` = MAP:

        * The one-way coupling interface must be defined in the acoustic model ( :ref:`sf`,,FSIN) such that
          it corresponds to the field-surface interface number (FSIN) in the structural model.

        * The output points are correct only if they are within the boundaries set via the specified input
          points.

        * Calculations for out-of-bound points require much more processing time than do points that are
          within bounds.

        * For each point in the acoustic destination mesh, the command searches all possible triangles in
          the structural source mesh to find the best triangle containing each point, then performs a linear
          interpolation inside this triangle. For faster and more accurate results, consider your
          interpolation method and search criteria carefully (see ``LIMIT`` ).

        You can also write an :file:`.asi` file during postprocessing of the structural model. In the POST1
        postprocessor ( :ref:`post1` ), issue the command :ref:`asifile`,WRITE, ``Fname``, ``Ext`` to output
        results on selected surface nodes of the structural model. In the subsequent acoustic analysis,
        apply the :ref:`sf`,,FSIN,1 command on the selected nodes of the acoustic model, and issue the
        :ref:`asifile`,READ, ``Fname``, ``Ext`` command to read the :file:`.asi` file.

        One-way coupling excitation can be applied to multiple frequencies or time steps.
        """
        command = f"ASIFILE,{opt},{fname},{ext},{oper},{kdim},{kout},{limit},,{resopt}"
        return self.run(command, **kwargs)

    def dfswave(
        self,
        kcn: str = "",
        radius: str = "",
        psdref: str = "",
        dens: str = "",
        sonic: str = "",
        incang: str = "",
        npara: str = "",
        sampopt: str = "",
        **kwargs,
    ):
        r"""Specifies the incident planar waves with random phases for a diffuse sound field.

        Mechanical APDL Command: `DFSWAVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DFSWAVE.html>`_

        Parameters
        ----------
        kcn : str
            Local coordinate system:

            * ``N`` - Coordinate system number. Default = 0.

            * ``DELETE`` - Delete defined incident diffused planar waves.

        radius : str
            Radius of the reference sphere on which the incident planar waves are distributed with equal
            energy. Defaults to 50 x the half-maximum dimension of the structural panel.

        psdref : str
            Reference power spectral density. Default = 1.

        dens : str
            Mass density of incident planar wave media. Default = 1.2041 kg/m :sup:`3`.

        sonic : str
            Sound speed in incident planar wave media. Default = 343.24 m/s)

        incang : str
            Maximum incident angle (0 :sup:`o` <= ``degree`` <= 180 :sup:`o` ) against the positive z axis
            in the local coordinate system ``KCN``. Default = 89 :sup:`o`.

        npara : str
            Number of divisions on the reference sphere with cutting planes parallel to the x-y coordinate
            plane of the local coordinate system. Default = 20.

        sampopt : str
            Random sampling option:

            * ``ALL`` - Initializes the random generator of incident planar wave phases and samples the phases
              at each solving frequency.

            * ``MULT`` - Initializes the random generator of incident planar wave phases at the first frequency
              and samples the phases at each solving frequency.

            * ``MONO`` - Initializes the random generator of incident planar wave phases and samples the phases
              only once at first solving frequency so that the same phases are used over the whole frequency range
              for each incident planar wave.

        Notes
        -----

        .. _DFSWAVE_notes:

        Issue the :ref:`dfswave` command to activate a diffuse sound field. (The :ref:`awave` command does
        not activate a diffuse sound field.)

        The ``SURF154``surface element must be defined on the surface of the structural solid element for
        the excitation.

        The acoustic elements and the absorbing boundary condition must be defined in the open acoustic
        domain. Do not define the acoustic domain on the excitation side.

        The :ref:`pras` and :ref:`plas` commands calculate the average transmission loss for multiple
        sampling phases at each frequency over the frequency range.

        The symmetry of a panel structure cannot be used to reduce the simulation size, as the incident
        plane waves have varying random phase angles. The z axis of the Cartesian coordinate system (
        ``KCN`` ) must be consistent with the panel``s outward normal unit vector at the center of the
        panel``s sending side.
        """
        command = (
            f"DFSWAVE,{kcn},{radius},{psdref},{dens},{sonic},{incang},{npara},{sampopt}"
        )
        return self.run(command, **kwargs)

    def biot(self, label: str = "", **kwargs):
        r"""Calculates the Biot-Savart source magnetic field intensity.

        Mechanical APDL Command: `BIOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BIOT.html>`_

        **Command default:**

        .. _BIOT_default:

        Calculate the H s field upon encountering the first :ref:`solve` command to produce a source field.

        Parameters
        ----------
        label : str
            Controls the Biot-Savart calculation:

            * ``NEW`` - Calculate the magnetic source field intensity (H s ) from the selected set of source
              elements to the selected set of nodes. Overwrite any existing H s field values.

            * ``SUM`` - Calculate the H s field from the selected set of source elements to the selected set of
              nodes. Accumulate with any existing H s field values.

        Notes
        -----

        .. _BIOT_notes:

        Calculates the Biot-Savart source magnetic field intensity (H s ) at the selected nodes from the
        selected source elements. The calculation is done at the time the :ref:`biot` command is issued.

        Source elements include primitives described by element ``SOURC36``, and coupled-field elements
        ``SOLID5``, ``LINK68``, and ``SOLID98``. Current conduction elements do not have a solved-for
        current distribution from which to calculate a source field until after the first substep. Inclusion
        of a current conduction element H s field will require a subsequent :ref:`biot`,SUM command (with
        ``SOURC36``elements unselected) and a :ref:`solve` command.

        The units of H s are as specified by the current :ref:`emunit` command setting.

        This command is also valid in PREP7.

        Distributed-Memory Parallel (DMP) Restriction When used with ``SOLID5``, ``LINK68``, or ``SOLID98``,
        the :ref:`biot` command is not supported in a
        DMP solution.
        """
        command = f"BIOT,{label}"
        return self.run(command, **kwargs)

    def sbclist(self, **kwargs):
        r"""Lists solid model boundary conditions.

        Mechanical APDL Command: `SBCLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SBCLIST.html>`_

        Notes
        -----

        .. _SBCLIST_notes:

        Lists all solid model boundary conditions for the selected solid model entities. See also
        :ref:`dklist`, :ref:`dllist`, :ref:`dalist`, :ref:`fklist`, :ref:`sfllist`, :ref:`sfalist`,
        :ref:`bfllist`, :ref:`bfalist`, :ref:`bfvlist`, and :ref:`bfklist` to list items separately.

        This command is valid in any processor.
        """
        command = "SBCLIST"
        return self.run(command, **kwargs)

    def sbctran(self, **kwargs):
        r"""Transfers solid model loads and boundary conditions to the FE  model.

        Mechanical APDL Command: `SBCTRAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SBCTRAN.html>`_

        Notes
        -----

        .. _SBCTRAN_notes:

        Causes a manual transfer of solid model loads and boundary conditions to the finite element model.
        Loads and boundary conditions on unselected keypoints, lines, areas, and volumes are not
        transferred. Boundary conditions and loads will not be transferred to unselected nodes or elements.
        The :ref:`sbctran` operation is also automatically done upon initiation of the solution calculations
        ( :ref:`solve` ).

        This command is also valid in PREP7.
        """
        command = "SBCTRAN"
        return self.run(command, **kwargs)

    def fluread(
        self,
        fname: str = "",
        ext: str = "",
        kdim: str = "",
        kout: int | str = "",
        limit: str = "",
        listopt: str = "",
        **kwargs,
    ):
        r"""Reads one-way Fluent-to-Mechanical APDL coupling data via a :file:`.cgns` file with one-side fast Fourier
        transformation complex pressure peak value.

        Mechanical APDL Command: `FLUREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FLUREAD.html>`_

        Parameters
        ----------

        fname : str
            File name and directory path of a one-way Fluent-to-Mechanical APDL coupling data file (248
            characters maximum, including the characters needed for the directory path). An unspecified
            directory path defaults to the working directory; in this case, you can use all 248 characters
            for the file name. Defaults to :file:`jobname`.

        ext : str
            File name extension of the one-way Fluent-to-Mechanical APDL coupling data file. Defaults to
            :file:`.cgns` ).

        kdim : str
            Interpolation data for mapping. A value of 0 (default) or 2 applies 2D interpolation (where
            interpolation occurs on a surface).

        kout : int or str
            Outside region results for mapping:

            * ``0`` - Use the value(s) of the nearest region point for points outside of the region. This
              behavior is the default.

            * ``1`` - Set results extrapolated outside of the region to zero.

        limit : str
            Number of nearby nodes considered for mapping interpolation. Minimum = 5. Default = 20.

            Lower values reduce processing time; however, some distorted or irregular meshes require a
            higher value in cases where three nodes are encountered for triangulation.

        listopt : str
            Type of items picked:

            * ``(blank)`` - No listing (default).

            * ``SOURCE`` - List the node coordinates and complex pressure values on the Fluent source side
              during the solution.

            * ``TARGET`` - List the node coordinates and complex pressure values on the mapped Mechanical APDL target
              side during the solution.

            * ``BOTH`` - List the node coordinates and complex pressure values on both the Fluent source side
              and the mapped Mechanical APDL target side during the solution.

        Notes
        -----

        .. _FLUREAD_notes:

        The :ref:`fluread` command reads one-way Fluent-to-Mechanical APDL coupling data from a
        :file:`.cgns`
        file. The Fluent one-side fast Fourier transformation (FFT) peak complex pressure values are
        mapped to the Mechanical APDL structure model during the acoustic-structural solution at each FFT
        frequency.

        The command can be used only for the model with the acoustic elements.

        To apply complex pressure to the structure model, define the ``SURF154``surface element, then define
        the one-way coupling interface ( :ref:`sf`,,FSIN) on the element.

        You can define the solving frequency range via the ``HARFRQ``command. The solver selects the FFT
        frequencies between the beginning and ending frequencies. The number of substeps is determined by
        the number of FFT frequencies over the frequency range. The number of substeps defined via the
        :ref:`nsubst` command is overwritten.

        For better mapping performance, consider the following:

        * Calculations for out-of-bound points require much more processing time than do points that are
          within bounds.

        * For each point in the structural destination mesh, the command searches all possible triangles in
          the Fluent source mesh to find the best triangle containing each point, then performs a linear
          interpolation inside this triangle. For faster and more accurate results, consider your
          interpolation method and search criteria carefully. (See ``LIMIT``.)

        It is possible to apply one-way coupling excitation to multiple frequencies. The one-side FFT peak
        complex pressure values are necessary to do so.
        """
        command = f"FLUREAD,,{fname},{ext},{kdim},{kout},{limit},{listopt}"
        return self.run(command, **kwargs)
