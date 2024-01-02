class Controls:
    def cfact(
        self,
        rfacta="",
        ifacta="",
        rfactb="",
        ifactb="",
        rfactc="",
        ifactc="",
        **kwargs,
    ):
        """Defines complex scaling factors to be used with operations.

        APDL Command: CFACT

        Parameters
        ----------
        rfacta
            Real portion of the complex scale factor used in place of FACTA.

        ifacta
            Imaginary portion of the complex scale factor used in place of
            FACTA.

        rfactb
            Real portion of the complex scale factor used in place of FACTB.

        ifactb
            Imaginary portion of the complex scale factor used in place of
            FACTB.

        rfactc
            Real portion of the complex scale factor used in place of FACTC.

        ifactc
            Imaginary portion of the complex scale factor used in place of
            FACTC.

        Notes
        -----
        Defines complex scale factors to be used with the operations [ADD,
        PROD, etc.].  If this command is supplied, these complex factors
        override any real factors (FACTA, FACTB, FACTC) supplied on the
        operation commands.  Factors are typically involved in scaling a
        specified variable, such as in the term FACTA x IA of the ADD command
        to scale variable IA before the ADD operation.

        When the CFACT command is active, defaults are as follows: 1) if the
        complex factor is not specified, but the variable upon which it acts
        (such as IA) is specified, the factor defaults to 1.0+i0.0;  2) if the
        variable upon which the factor operates is not specified, but the
        factor is specified, the variable defaults to 1.0 so that the term in
        the operation becomes the complex factor itself;  3) if neither the
        factor nor the variable number is supplied, the term is omitted from
        the operation.  Once the operation (such as the ADD command) has been
        processed, the CFACT command becomes inactive and must be specified
        again if it is to be used.
        """
        command = f"CFACT,{rfacta},{ifacta},{rfactb},{ifactb},{rfactc},{ifactc}"
        return self.run(command, **kwargs)

    def force(self, lab="", **kwargs):
        """Selects the element nodal force type for output.

        APDL Command: FORCE

        Parameters
        ----------
        lab
            Type of force to be associated with the force items:

            TOTAL - Total forces (static, damping, and inertia).

            STATIC - Static forces.

            DAMP - Damping forces.

            INERT - Inertia forces.

        Notes
        -----
        FORCE selects the element nodal force type for output with the POST1
        PRESOL, PLESOL, PRRFOR, NFORCE, FSUM, etc. commands, the POST26 ESOL
        command, and reaction force plotting [/PBC].  For example, FORCE,STATIC
        causes item F of the PRESOL command to be the static forces for the
        elements processed. Element member forces (such as those available for
        beams and shells and processed by Item and Sequence number) are not
        affected by this command. The SMISC records extract the static force.

        The PRRSOL command is not valid with FORCE.  Use the PRRFOR command,
        which provides the same functionality as PRRSOL, instead.

        Use the FORCE command prior to any load case operations (LCOPER) to
        insure the correct element nodal force combinations.

        In POST26, the ESOL data stored is based on the active FORCE
        specification at the time the data is stored. To store data at various
        specifications (for example, static and inertia forces), issue a STORE
        command before each new specification.

        The FORCE command cannot be used to extract static, damping, and
        inertial forces for MPC184 joint elements.

        To retrieve the different force types, use the ``*GET`` command with
        Entity=ELEM and Item1=EFOR.

        The FORCE command is not supported in a spectrum analysis. You can
        specify the force type directly on the combination method commands
        (ForceType on the PSDCOM, SRSS, CQC, etc. commands).

        The FORCE command is not supported in a modal analysis.
        """
        command = f"FORCE,{lab}"
        return self.run(command, **kwargs)

    def layerp26(self, num="", **kwargs):
        """Specifies the element layer for which data are to be stored.

        APDL Command: LAYERP26

        Parameters
        ----------
        num
            Layer-processing mode:

            N - The layer number to process. The default value is 1.

        Notes
        -----
        Defines the element layer for which results data are to be stored for
        postprocessing.  Applies to stress and strain data for layered elements
        BEAM161, SHELL163, SHELL181, SOLID185, SOLID186, SOLSH190, SHELL208,
        SHELL209, SHELL281, REINF265, and ELBOW290.

        The SHELL command can be used (for shell elements) to specify a
        location (TOP, MID, BOT) within the layer for selection on the ESOL
        command. Transverse shear stresses for MID are linearly averaged from
        TOP and BOT, and do not reflect a parabolic distribution. Setting
        KEYOPT(8) = 2 for SHELL181, SHELL208, SHELL209, SHELL281, and ELBOW290
        writes the mid-surface values directly to the results file and yields
        more accurate values than linear averaging.

        That this command cannot be used for energy output, as energy is a per-
        element quantity.

        When using the LAYERP26 command with SHELL181, SOLID185, SOLID186,
        SOLSH190, SHELL208, or SHELL209, KEYOPT(8) must be set to 1 (or 2 for
        SHELL181, SHELL208, SHELL209, SHELL281, and ELBOW290) in order to store
        results for all layers.

        For the ANSYS LS-DYNA product, this command works differently than
        described above.  For SHELL163 and BEAM161, you must first use EDINT
        during the solution phase to define the integration points for which
        you want output data.  Be aware that the output location for SHELL163
        data is always at the integration point, so "top" and "bottom" refer to
        the top or bottom integration point, not necessarily the top or bottom
        surface.  For more information, see the ANSYS LS-DYNA User's Guide.

        In POST26, the ESOL data stored is based on the active LAYERP26
        specification at the time the data is stored. To store data at various
        specifications (for example, layers 2 and 5), issue a STORE command
        before each new specification.
        """
        command = f"LAYERP26,{num}"
        return self.run(command, **kwargs)

    def shell(self, loc="", **kwargs):
        """Selects a shell element or shell layer location for results output.

        APDL Command: SHELL

        Parameters
        ----------
        loc
            Location within shell element (or layer) to obtain stress results:

            TOP - Top of shell element (or layer) (default).

            MID - Middle of shell element (or layer). The default method averages the TOP and BOT
                  values to obtain a mid value. Setting KEYOPT(8) = 2 for
                  SHELL181, SHELL208, SHELL209, and ELBOW290 uses MID results
                  obtained directly from the results file.

            BOT - Bottom of shell element (or layer).

        Notes
        -----
        Selects the location within a shell element (or a shell layer) for
        results output (nodal stresses, strains, etc.).  Applies to POST1
        selects, sorts, and output [NSEL, NSORT, PRNSOL, PLNSOL, PRPATH,
        PLPATH, etc.], and is used for storage with the POST26 ESOL command.
        For example, SHELL,TOP causes item S of the POST1 PRNSOL command or the
        POST26 ESOL command to be the stresses at the top of the shell
        elements.  For layered shell elements, use the LAYER (POST1) or
        LAYERP26 (POST26) command to select the layer. The SHELL command does
        not apply to the layered thermal shell elements, SHELL131 and SHELL132.

        For PowerGraphics [/GRAPHICS,POWER], the SHELL,MID command affects both
        the printed output and the displayed results, while the SHELL (TOP or
        BOT) command prints and displays both the top and bottom layers
        simultaneously. Note that /CYCEXPAND,ON automatically turns on
        PowerGraphics; however, for cyclic mode-superposition harmonic
        postprocessing (CYCFILES), the SHELL command prints and displays only
        the requested layer.

        In POST26, the ESOL data stored is based on the active SHELL
        specification at the time the data is stored. To store data at various
        specifications (for example, stresses at the top and bottom locations),
        issue a STORE command before each new specification.
        """
        command = f"SHELL,{loc}"
        return self.run(command, **kwargs)

    def tvar(self, key="", **kwargs):
        """Changes time to the cumulative iteration number.

        APDL Command: TVAR

        Parameters
        ----------
        key
            Time key:

            0 - Time is used for the variable TIME.

            1 - NCUMIT is used for the variable TIME.

        Notes
        -----
        Changes the meaning of the time variable to the cumulative iteration
        number (NCUMIT) variable.  Data can be read from the file, printed, and
        displayed as a function of NCUMIT rather than time.  All POST26
        descriptions applying to TIME then apply to NCUMIT.
        """
        command = f"TVAR,{key}"
        return self.run(command, **kwargs)
