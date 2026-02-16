# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

from ansys.mapdl.core._commands import CommandsBase

class SpectrumOptions:

    def addam(
        self,
        af: str = "",
        aa: str = "",
        ab: str = "",
        ac: str = "",
        ad: str = "",
        amin: str = "",
        **kwargs,
    ):
        r"""Specifies the acceleration spectrum computation constants for the analysis of shock resistance of
        shipboard structures.

        Mechanical APDL Command: `ADDAM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADDAM.html>`_

        Parameters
        ----------
        af : str
            Direction-dependent acceleration coefficient for elastic or elastic-plastic analysis option
            (default = 0).

        aa : str
            Coefficients for the DDAM acceleration spectrum equations. Default for these coefficients is
            zero.

        ab : str
            Coefficients for the DDAM acceleration spectrum equations. Default for these coefficients is
            zero.

        ac : str
            Coefficients for the DDAM acceleration spectrum equations. Default for these coefficients is
            zero.

        ad : str
            Coefficients for the DDAM acceleration spectrum equations. Default for these coefficients is
            zero.

        amin : str
            Minimum acceleration value. It defaults to 6g, where g is the acceleration due to gravity.

        Notes
        -----

        .. _ADDAM_notes:

        This command specifies acceleration coefficients to analyze shock resistance of shipboard equipment.
        These coefficients are used to compute mode coefficients according to the equations given in
        `Dynamic Design Analysis Method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eq1bf15231-590e-4b5a-a30a-aa31e15bf78f>`_
        :ref:`vddam` and :ref:`sed` commands, is used with the spectrum ( :ref:`antype`,SPECTR) analysis as
        a special purpose alternative to the :ref:`sv`, :ref:`freq`, and :ref:`svtyp` commands.

        In order to perform a DDAM spectrum analysis using a units system other than BIN (default), you must
        specify the units system complying with the mass and length units of the model using the
        :ref:`units` command. Issue the :ref:`units` command before defining the shock spectrum computation
        constants ( :ref:`addam` ). The :ref:`addam` command is not supported with the user-defined unite
        system ( ``Label`` = USER on :ref:`units` ).

        :ref:`ddaspec` may alternatively be used to calculate spectrum coefficients.

        This command is also valid in PREP7.
        """
        command = f"ADDAM,{af},{aa},{ab},{ac},{ad},{amin}"
        return self.run(command, **kwargs)

    def coval(
        self,
        tblno1: str = "",
        tblno2: str = "",
        sv1: str = "",
        sv2: str = "",
        sv3: str = "",
        sv4: str = "",
        sv5: str = "",
        sv6: str = "",
        sv7: str = "",
        **kwargs,
    ):
        r"""Defines PSD cospectral values.

        Mechanical APDL Command: `COVAL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_COVAL.html>`_

        Parameters
        ----------
        tblno1 : str
            First input PSD table number associated with this spectrum.

        tblno2 : str
            Second input PSD table number associated with this spectrum.

        sv1 : str
            PSD cospectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv2 : str
            PSD cospectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv3 : str
            PSD cospectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv4 : str
            PSD cospectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv5 : str
            PSD cospectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv6 : str
            PSD cospectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv7 : str
            PSD cospectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        Notes
        -----

        .. _COVAL_notes:

        Defines PSD cospectral values to be associated with the previously defined frequency points.
        Two table references are required since values are off- diagonal terms. Unlike autospectra (
        :ref:`psdval` ), the cospectra can be positive or negative. The cospectral curve segment where there
        is a sign change is interpolated linearly (the rest of the curve segments use log-log
        interpolation). For better accuracy, choose as small a curve segment as possible wherever a sign
        change occurs.

        Repeat :ref:`coval` command using the same table numbers for additional points. This command is
        valid for :ref:`spopt`,PSD only.

        This command is also valid in PREP7.
        """
        command = f"COVAL,{tblno1},{tblno2},{sv1},{sv2},{sv3},{sv4},{sv5},{sv6},{sv7}"
        return self.run(command, **kwargs)

    def cqc(self, signif: str = "", label: str = "", forcetype: str = "", **kwargs):
        r"""Specifies the complete quadratic mode combination method.

        Mechanical APDL Command: `CQC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CQC.html>`_

        Parameters
        ----------
        signif : str
            Combine only those modes whose significance level exceeds the ``SIGNIF`` threshold. For single
            point, multipoint, or DDAM response ( :ref:`spopt`,SPRS, MPRS or DDAM), the significance level
            of a mode is defined as the mode coefficient divided by the maximum mode coefficient of all
            modes. Any mode whose significance level is less than ``SIGNIF`` is considered insignificant and
            is not contributed to the mode combinations. The higher the ``SIGNIF`` threshold, the fewer the
            number of modes combined. ``SIGNIF`` defaults to 0.001. If ``SIGNIF`` is specified as 0.0, it is
            taken as 0.0. (This mode combination method is not valid for :ref:`spopt`,PSD.)

        label : str
            Label identifying the combined mode solution output.

            * ``DISP`` - Displacement solution (default). Displacements, stresses, forces, etc., are available.

            * ``VELO`` - Velocity solution. Velocities, "stress velocities," "force velocities," etc., are
              available.

            * ``ACEL`` - Acceleration solution. Accelerations, "stress accelerations," "force accelerations,"
              etc., are available.

        forcetype : str
            Label identifying the forces to be combined:

            * ``STATIC`` - Combine the modal static forces (default).

            * ``TOTAL`` - Combine the modal static plus inertial forces.

        Notes
        -----

        .. _CQC_notes:

        Damping is required for this mode combination method. The :ref:`cqc` command is also valid for
        PREP7.
        """
        command = f"CQC,{signif},{label},,{forcetype}"
        return self.run(command, **kwargs)

    def ddaspec(
        self,
        keyref: int | str = "",
        shptyp: str = "",
        mountloc: str = "",
        deftyp: str = "",
        amin: str = "",
        **kwargs,
    ):
        r"""Specifies the shock spectrum computation constants for DDAM analysis.

        Mechanical APDL Command: `DDASPEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DDASPEC.html>`_

        Parameters
        ----------
        keyref : int or str
            Key for reference catalog:

            * ``1`` - The spectrum computation constants are based on NRL-1396 (default). For more information,
              see `Dynamic Design Analysis Method
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eq1bf15231-590e-4b5a-a30a-aa31e15bf78f>`_

        shptyp : str
            Select the ship type:

            * ``SUBM`` - Submarine

            * ``SURF`` - Surface ship

        mountloc : str
            Select the mounting location:

            * ``HULL`` - Hull mounting location. These structures are mounted directly to basic hull structures
              like frames, structural bulkheads below the water line, and shell plating above the water line.

            * ``DECK`` - Deck mounting location. These structures are mounted directly to decks, non-structural
              bulkheads, or to structural bulkheads above the water line.

            * ``SHEL`` - Shell plating mounting location. These structures are mounted directly to shell plating
              below the water line without intervening foundations.

        deftyp : str
            Select the deformation type:

            * ``ELAS`` - Elastic deformation (default)

            * ``PLAS`` - Elastic-plastic deformation

        amin : str
            Minimum acceleration value. It defaults to 6g, where g is the acceleration due to gravity.

        Notes
        -----

        .. _DDASPEC_notes:

        The excitation along one of the fore and aft, vertical or athwartship directions is required to
        calculate the spectrum coefficients. Issue the :ref:`sed` command before issuing :ref:`ddaspec`. For
        example, if you want to apply the excitation along the fore and aft direction, you should specify
        ``SEDX`` = 1.0 on :ref:`sed`. Similarly, for excitation along vertical or athwartship direction,
        specify ``SEDY`` = 1.0 or ``SEDZ`` = 1.0, respectively, on :ref:`sed`.

        :ref:`addam` and :ref:`vddam` may alternatively be used to calculate spectrum coefficients.

        In order to perform a DDAM spectrum analysis using a units system other than BIN (default), you must
        specify the units system complying with the mass and length units of the model using the
        :ref:`units` command. Issue the :ref:`units` command before defining the shock spectrum computation
        constants ( :ref:`ddaspec` ). The DDASPEC command is not supported with the user-defined units
        system ( ``Label`` = USER on :ref:`units` ).

        This command is also valid in PREP7.
        """
        command = f"DDASPEC,{keyref},{shptyp},{mountloc},{deftyp},{amin}"
        return self.run(command, **kwargs)

    def dsum(
        self,
        signif: str = "",
        label: str = "",
        td: str = "",
        forcetype: str = "",
        **kwargs,
    ):
        r"""Specifies the double sum mode combination method.

        Mechanical APDL Command: `DSUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DSUM.html>`_

        Parameters
        ----------
        signif : str
            Combine only those modes whose significance level exceeds the ``SIGNIF`` threshold. For single
            point, multipoint, or DDAM response ( :ref:`spopt`, SPRS, MPRS, or DDAM), the significance level
            of a mode is defined as the mode coefficient divided by the maximum mode coefficient of all
            modes. Any mode whose significance level is less than ``SIGNIF`` is considered insignificant and
            is not contributed to the mode combinations. The higher the ``SIGNIF`` threshold, the fewer the
            number of modes combined. ``SIGNIF`` defaults to 0.001. If ``SIGNIF`` is specified as 0.0, it is
            taken as 0.0. (This mode combination method is not valid for :ref:`spopt`, PSD.)

        label : str
            Label identifying the combined mode solution output.

            * ``DISP`` - Displacement solution (default). Displacements, stresses, forces, etc., are available.

            * ``VELO`` - Velocity solution. Velocities, "stress velocities," "force velocities," etc., are
              available.

            * ``ACEL`` - Acceleration solution. Accelerations, "stress accelerations," "force accelerations,"
              etc., are available.

        td : str
            Time duration for earthquake or shock spectrum. ``TD`` defaults to 10.

        forcetype : str
            Label identifying the forces to be combined:

            * ``STATIC`` - Combine the modal static forces (default).

            * ``TOTAL`` - Combine the modal static plus inertial forces.

        Notes
        -----

        .. _DSUM_notes:

        This command is also valid for PREP7.
        """
        command = f"DSUM,{signif},{label},{td},{forcetype}"
        return self.run(command, **kwargs)

    def freq(
        self,
        freq1: str = "",
        freq2: str = "",
        freq3: str = "",
        freq4: str = "",
        freq5: str = "",
        freq6: str = "",
        freq7: str = "",
        freq8: str = "",
        freq9: str = "",
        **kwargs,
    ):
        r"""Defines the frequency points for the :ref:`sv` vs. :ref:`freq` tables.

        Mechanical APDL Command: `FREQ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FREQ.html>`_

        Parameters
        ----------
        freq1 : str
            Frequency points for SV vs. FREQ tables. Values must be in ascending order. ``FREQ1`` should be
            greater than zero. Units are cycles/time.

        freq2 : str
            Frequency points for SV vs. FREQ tables. Values must be in ascending order. ``FREQ1`` should be
            greater than zero. Units are cycles/time.

        freq3 : str
            Frequency points for SV vs. FREQ tables. Values must be in ascending order. ``FREQ1`` should be
            greater than zero. Units are cycles/time.

        freq4 : str
            Frequency points for SV vs. FREQ tables. Values must be in ascending order. ``FREQ1`` should be
            greater than zero. Units are cycles/time.

        freq5 : str
            Frequency points for SV vs. FREQ tables. Values must be in ascending order. ``FREQ1`` should be
            greater than zero. Units are cycles/time.

        freq6 : str
            Frequency points for SV vs. FREQ tables. Values must be in ascending order. ``FREQ1`` should be
            greater than zero. Units are cycles/time.

        freq7 : str
            Frequency points for SV vs. FREQ tables. Values must be in ascending order. ``FREQ1`` should be
            greater than zero. Units are cycles/time.

        freq8 : str
            Frequency points for SV vs. FREQ tables. Values must be in ascending order. ``FREQ1`` should be
            greater than zero. Units are cycles/time.

        freq9 : str
            Frequency points for SV vs. FREQ tables. Values must be in ascending order. ``FREQ1`` should be
            greater than zero. Units are cycles/time.

        Notes
        -----

        .. _FREQ_notes:

        Repeat the :ref:`freq` command for additional frequency points (100 maximum). Values are added after
        the last nonzero frequency. If all fields ( ``FREQ1`` -- ``FREQ9`` ) are blank, erase SV vs. FREQ
        tables.

        Frequencies must be in ascending order.

        Spectral values are input with the :ref:`sv` command and interpreted according to the :ref:`svtyp`
        command. Applies only to the SPRS (single-point) option of the :ref:`spopt` command. See the
        :ref:`spfreq` command for frequency input in MPRS (multi-point) analysis.

        Use the :ref:`stat` command to list current frequency points.

        This command is also valid in PREP7.
        """
        command = f"FREQ,{freq1},{freq2},{freq3},{freq4},{freq5},{freq6},{freq7},{freq8},{freq9}"
        return self.run(command, **kwargs)

    def grp(self, signif: str = "", label: str = "", forcetype: str = "", **kwargs):
        r"""Specifies the grouping mode combination method.

        Mechanical APDL Command: `GRP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GRP.html>`_

        Parameters
        ----------
        signif : str
            Combine only those modes whose significance level exceeds the ``SIGNIF`` threshold. For single
            point, multipoint, or DDAM response ( :ref:`spopt`,SPRS, MPRS or DDAM), the significance level
            of a mode is defined as the mode coefficient divided by the maximum mode coefficient of all
            modes. Any mode whose significance level is less than ``SIGNIF`` is considered insignificant and
            is not contributed to the mode combinations. The higher the ``SIGNIF`` threshold, the fewer the
            number of modes combined. ``SIGNIF`` defaults to 0.001. If ``SIGNIF`` is specified as 0.0, it is
            taken as 0.0. (This mode combination method is not valid for :ref:`spopt`,PSD.)

        label : str
            Label identifying the combined mode solution output.

            * ``DISP`` - Displacement solution (default). Displacements, stresses, forces, etc., are available.

            * ``VELO`` - Velocity solution. Velocities, "stress velocities," "force velocities," etc., are
              available.

            * ``ACEL`` - Acceleration solution. Accelerations, "stress accelerations," "force accelerations,"
              etc., are available.

        forcetype : str
            Label identifying the forces to be combined:

            * ``STATIC`` - Combine the modal static forces (default).

            * ``TOTAL`` - Combine the modal static plus inertial forces.

        Notes
        -----

        .. _GRP_notes:

        The ``SIGNIF`` value set with this command (including the default value of 0.001) overrides the
        ``SIGNIF`` value set with the :ref:`mxpand` command.

        This command is also valid for PREP7.
        """
        command = f"GRP,{signif},{label},,{forcetype}"
        return self.run(command, **kwargs)

    def mmass(self, option: str = "", zpa: str = "", **kwargs):
        r"""Specifies the missing mass response calculation.

        Mechanical APDL Command: `MMASS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MMASS.html>`_

        Parameters
        ----------
        option : str
            Flag to activate or deactivate missing mass response calculation.

            * ``0 (OFF or NO)`` - Deactivate (default).

            * ``1 (ON or YES)`` - Activate.

        zpa : str
            Zero Period Acceleration Value. If a scale factor FACT is defined on the :ref:`svtyp` command,
            it is applied to this value.

        Notes
        -----

        .. _MMASS_notes:

        The missing mass calculation is valid only for single point excitation response spectrum analysis (
        :ref:`spopt`, SPRS) and for multiple point response spectrum analysis ( :ref:`spopt`, MPRS)
        performed with base excitation using acceleration response spectrum loading. Missing mass is
        supported in a spectrum analysis only when the preceding modal analysis is performed with the Block
        Lanczos, PCG Lanczos, Supernode, or Subspace eigensolver (Method =LANB, LANPCG, SNODE, or SUBSP on
        the :ref:`modopt` command).

        The velocity solution is not available ( ``Label`` = VELO on the combination command: :ref:`srss`,
        :ref:`cqc`...) when the missing mass calculation is activated.

        The missing mass calculation is not supported when the spectrum analysis is based on a linear
        perturbation modal analysis performed after a nonlinear base analysis.

        The missing mass is not supported when superelements are present.

        To take into account the contribution of the truncated modes, the residual vector ( :ref:`resvec` )
        can be used in place of the missing mass response. This is of particular interest if the velocity
        solution is requested or if a nonlinear prestress is included in the analysis (linear perturbation),
        or if a superelement is present, since the missing mass cannot be used in these cases.

        In a multiple point response spectrum analysis ( :ref:`spopt`,MPRS), the :ref:`mmass` command must
        precede the participation factor calculation command ( :ref:`pfact` ).

        This command is also valid in PREP7.

        * `Performing a Single-Point Response Spectrum (SPRS) Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR6_4.html#aYACegwrd>`_
        * `Performing a Multi-Point Response Spectrum (MPRS) Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR6_10.html#spectrum_multipoint>`_
        * `Missing-Mass Response
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eq7fe0e910-baf8-4b0e-8a3e-67dc4190f121>`_
        * :ref:`rigresp` command
        """
        command = f"MMASS,{option},{zpa}"
        return self.run(command, **kwargs)

    def nrlsum(
        self,
        signif: str = "",
        label: str = "",
        labelcsm: str = "",
        forcetype: str = "",
        **kwargs,
    ):
        r"""Specifies the Naval Research Laboratory (NRL) sum mode combination method.

        Mechanical APDL Command: `NRLSUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NRLSUM.html>`_

        Parameters
        ----------
        signif : str
            Combine only those modes whose significance level exceeds the ``SIGNIF`` threshold. For single
            point, multipoint, or DDAM response ( :ref:`spopt`,SPRS, MPRS or DDAM), the significance level
            of a mode is defined as the mode coefficient divided by the maximum mode coefficient of all
            modes. Any mode whose significance level is less than ``SIGNIF`` is considered insignificant and
            is not contributed to the mode combinations. The higher the ``SIGNIF`` threshold, the fewer the
            number of modes combined. ``SIGNIF`` defaults to 0.001. If ``SIGNIF`` is specified as 0.0, it is
            taken as 0.0. (This mode combination method is not valid for :ref:`spopt`,PSD.)

        label : str
            Label identifying the combined mode solution output.

            * ``DISP`` - Displacement solution (default). Displacements, stresses, forces, etc., are available.

            * ``VELO`` - Velocity solution. Velocities, "stress velocities," "force velocities," etc., are
              available.

            * ``ACEL`` - Acceleration solution. Accelerations, "stress accelerations," "force accelerations,"
              etc., are available.

        labelcsm : str
            Label identifying the CSM (Closely Spaced Modes) method.

            * ``CSM`` - Use the CSM method.

            * ```` - Do not use the CSM method (default).

        forcetype : str
            Label identifying the forces to be combined:

            * ``STATIC`` - Combine the modal static forces (default).

            * ``TOTAL`` - Combine the modal static plus inertial forces.

        Notes
        -----

        .. _NRLSUM_notes:

        This command is also valid in PREP7. This mode combination method is usually used for
        :ref:`spopt`,DDAM.

        This CSM method is only applicable in a DDAM analysis ( :ref:`spopt`, ``DDAM`` ). Element results
        calculation based on modal element results ( ``Elcalc`` on :ref:`spopt` ) is not supported and is
        automatically reset for this method. The CSM method combines two closely spaced modes into one mode
        when their frequencies are within 10 percent of the common mean frequency and their responses are
        opposite in sign. The contribution of these closely spaced modes is then included in the NRL sum as
        a single effective mode. Refer to `Closely Spaced Modes (CSM) Method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eqe88ee1e2-71f7-4a8d-910a-d28d1d27641b>`_
        """
        command = f"NRLSUM,{signif},{label},{labelcsm},{forcetype}"
        return self.run(command, **kwargs)

    def pfact(self, tblno: str = "", excit: str = "", parcor: str = "", **kwargs):
        r"""Calculates participation factors for the PSD or multi-point response spectrum table.

        Mechanical APDL Command: `PFACT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PFACT.html>`_

        Parameters
        ----------
        tblno : str
            Input PSD (Power Spectral Density) table number for which participation factors are to be
            calculated.

        excit : str
            Label defining the location of excitation:

            * ``BASE`` - Base excitation (default).

            * ``NODE`` - Nodal excitation.

        parcor : str
            Label defining excitation type (applies only to :ref:`spopt`,PSD analysis). Used only when partially correlated excitation is due to wave propagation or spatial correlation. Defaults to partially correlated excitation as defined by :ref:`coval` and :ref:`qdval` commands.

            * ``WAVE`` - Excitation defined by :ref:`psdwav` command.

            * ``SPAT`` - Excitation defined by :ref:`psdspl` command.

        Notes
        -----

        .. _PFACT_notes:

        Calculates the participation factors for a particular PSD or multi-point response spectrum table
        defined with the :ref:`psdval` or :ref:`spval` command. The :file:`Jobname.DB` file must contain
        modal solution data in order for this command to calculate the participation factor. There must be a
        :ref:`pfact` command for each excitation spectrum. You are limited to 300 excitations.

        This command is also valid in PREP7.
        """
        command = f"PFACT,{tblno},{excit},{parcor}"
        return self.run(command, **kwargs)

    def psdcom(self, signif: str = "", comode: str = "", forcetype: str = "", **kwargs):
        r"""Specifies the power spectral density mode combination method.

        Mechanical APDL Command: `PSDCOM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSDCOM.html>`_

        Parameters
        ----------
        signif : str
            Combine only those modes whose significance level exceeds the ``SIGNIF`` threshold. For PSD
            response ( :ref:`spopt`,PSD), the significance level is defined as the modal covariance matrix
            term, divided by the maximum modal covariance matrix term. Any term whose significance level is
            less than ``SIGNIF`` is considered insignificant and is not contributed to the mode
            combinations. The higher the ``SIGNIF`` threshold, the fewer the number of terms used.
            ``SIGNIF`` defaults to 0.0001. If ``SIGNIF`` is specified as 0.0, it is taken as 0.0.

        comode : str
            First ``COMODE`` number of modes to be actually combined. ``COMODE`` must always be less than or
            equal to ``NMODE`` (input quantity ``NMODE`` on the :ref:`spopt` command). ``COMODE`` defaults
            to ``NMODE``. ``COMODE`` performs a second level of control for the first sequential ``COMODE``
            number of modes to be combined. It uses the significance level threshold indicated by ``SIGNIF``
            and operates only on the significant modes.

        forcetype : str
            Label identifying the forces to be combined:

            * ``STATIC`` - Combine the modal static forces (default).

            * ``TOTAL`` - Combine the modal static plus inertial forces.

        Notes
        -----

        .. _PSDCOM_notes:

        This command is also valid for PREP7. This command is valid only for :ref:`spopt`,PSD.
        """
        command = f"PSDCOM,{signif},{comode},,{forcetype}"
        return self.run(command, **kwargs)

    def psdfrq(
        self,
        tblno1: str = "",
        tblno2: str = "",
        freq1: str = "",
        freq2: str = "",
        freq3: str = "",
        freq4: str = "",
        freq5: str = "",
        freq6: str = "",
        freq7: str = "",
        **kwargs,
    ):
        r"""Defines the frequency points for the input spectrum tables PSDVAL vs. PSDFRQ for PSD analysis.

        Mechanical APDL Command: `PSDFRQ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSDFRQ.html>`_

        Parameters
        ----------
        tblno1 : str
            Input table number. When used with the :ref:`coval` or the :ref:`qdval` command, ``TBLNO1``
            represents the row number of this table. Up to 200 tables may be defined.

        tblno2 : str
            Input table number. ``TBLNO2`` is used only for the :ref:`coval` or the :ref:`qdval` commands
            and represents the column number of this table.

        freq1 : str
            Frequency points (cycles/time) for spectrum vs. frequency tables. ``FREQ1`` should be greater
            than zero, and values must be in ascending order. Log-log interpolation will be used between
            frequency points.

        freq2 : str
            Frequency points (cycles/time) for spectrum vs. frequency tables. ``FREQ1`` should be greater
            than zero, and values must be in ascending order. Log-log interpolation will be used between
            frequency points.

        freq3 : str
            Frequency points (cycles/time) for spectrum vs. frequency tables. ``FREQ1`` should be greater
            than zero, and values must be in ascending order. Log-log interpolation will be used between
            frequency points.

        freq4 : str
            Frequency points (cycles/time) for spectrum vs. frequency tables. ``FREQ1`` should be greater
            than zero, and values must be in ascending order. Log-log interpolation will be used between
            frequency points.

        freq5 : str
            Frequency points (cycles/time) for spectrum vs. frequency tables. ``FREQ1`` should be greater
            than zero, and values must be in ascending order. Log-log interpolation will be used between
            frequency points.

        freq6 : str
            Frequency points (cycles/time) for spectrum vs. frequency tables. ``FREQ1`` should be greater
            than zero, and values must be in ascending order. Log-log interpolation will be used between
            frequency points.

        freq7 : str
            Frequency points (cycles/time) for spectrum vs. frequency tables. ``FREQ1`` should be greater
            than zero, and values must be in ascending order. Log-log interpolation will be used between
            frequency points.

        Notes
        -----

        .. _PSDFRQ_notes:

        The spectrum values may be input with the :ref:`psdval`, :ref:`coval`, or :ref:`qdval` commands. A
        separate :ref:`psdfrq` command must be used for each table and cross table defined. Frequencies must
        be in ascending order.

        Repeat :ref:`psdfrq` command for additional frequency points. Values are added after the last
        nonzero frequency. If all fields after :ref:`psdfrq` are blank, all input vs. frequency tables are
        erased. If ``TBLNO1`` is nonblank, all corresponding :ref:`psdval` tables are erased. If both
        ``TBLNO1`` and ``TBLNO2`` are nonblank, all corresponding :ref:`coval` and :ref:`qdval` tables are
        erased.

        This command is also valid in PREP7.
        """
        command = f"PSDFRQ,{tblno1},{tblno2},{freq1},{freq2},{freq3},{freq4},{freq5},{freq6},{freq7}"
        return self.run(command, **kwargs)

    def psdgraph(
        self, tblno1: str = "", tblno2: str = "", displaykey: int | str = "", **kwargs
    ):
        r"""Displays input PSD curves.

        Mechanical APDL Command: `PSDGRAPH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSDGRAPH.html>`_

        Parameters
        ----------
        tblno1 : str
            PSD table number to display.

        tblno2 : str
            Second PSD table number to display. ``TBLNO2`` is used only in conjunction with the :ref:`coval`
            or the :ref:`qdval` commands.

        displaykey : int or str
            Key to display the points markers and numbering:

            * ``0`` - Display points markers and numbering (default).

            * ``1`` - Display points numbering only.

            * ``2`` - Display points markers only.

            * ``3`` - No points markers or numbering.

        Notes
        -----

        .. _PSDGRAPH_notes:

        The input PSD tables are displayed in log-log format as dotted lines. The best-fit curves, used to
        perform the closed-form integration, are displayed as solid lines. If there is a significant
        discrepancy between the two, then you should add one or more intermediate points to the table to
        obtain a better fit.

        If ``TBLNO2`` is zero, blank, or equal to ``TBLNO1``, then the autospectra ( :ref:`psdval` ) are
        displayed for ``TBLNO1``. If ``TBLNO2`` is also specified, then the autospectra for ``TBLNO1`` and
        ``TBLNO2`` are displayed, along with the corresponding cospectra ( :ref:`coval` ) and quadspectra (
        :ref:`qdval` ), if they are defined.

        This command is valid in any processor.
        """
        command = f"PSDGRAPH,{tblno1},{tblno2},{displaykey}"
        return self.run(command, **kwargs)

    def psdres(self, lab: str = "", relkey: str = "", **kwargs):
        r"""Controls solution output written to the results file from a PSD analysis.

        Mechanical APDL Command: `PSDRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSDRES.html>`_

        **Command default:**

        .. _PSDRES_default:

        Relative displacement solution, no velocity or acceleration solution for 1 σ results.

        Parameters
        ----------
        lab : str
            Label identifying the solution output:

            * ``DISP`` - Displacement solution (default). One-sigma displacements, stresses, forces, etc.
              Written as load step 3 on :file:`FileRST`.

            * ``VELO`` - Velocity solution. One-sigma velocities, "stress velocities," "force velocities," etc.
              Written as load step 4 of :file:`FileRST`.

            * ``ACEL`` - Acceleration solution. One-sigma accelerations, "stress accelerations," "force
              accelerations," etc. Written as load step 5 on :file:`FileRST`.

        relkey : str
            Key defining relative or absolute calculations:

            * ``REL`` - Calculations are relative to the base excitation (default).

            * ``ABS`` - Calculations are absolute.

            * ``OFF`` - No calculation of solution output identified by ``Lab``.

        Notes
        -----

        .. _PSDRES_notes:


        Controls the amount and form of solution output written to the results file from a PSD analysis.
        One-sigma values of the relative or absolute displacement solution, relative or absolute velocity
        solution, relative or absolute acceleration solution, or any combination may be included on the
        results file.

        This command is also valid in PREP7.
        """
        command = f"PSDRES,{lab},{relkey}"
        return self.run(command, **kwargs)

    def psdspl(self, tblno: str = "", rmin: str = "", rmax: str = "", **kwargs):
        r"""Defines a partially correlated excitation in a PSD analysis.

        Mechanical APDL Command: `PSDSPL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSDSPL.html>`_

        Parameters
        ----------
        tblno : str
            Input PSD table number defined with :ref:`psdval` command.

        rmin : str
            Minimum distance between excitation points which are partially correlated. Excited nodes closer
            than ``RMIN`` will be fully correlated.

        rmax : str
            Maximum distance between excitation points which are partially correlated. Excited nodes farther
            apart than ``RMAX`` will be uncorrelated.

        Notes
        -----

        .. _PSDSPL_notes:

        Notes
        Defines a partially correlated excitation in terms of a sphere of influence relating excitation
        point geometry (in a PSD analysis). If the distance between any two excitation points is less than
        ``RMIN``, then the excitation is fully correlated. If the distance is greater than ``RMAX``, then
        the excitation is uncorrelated. If the distance lies between ``RMIN`` and ``RMAX``, then the
        excitation is partially correlated with the degree of correlation dependent on the separation
        distance between the points. This command is not available for a pressure PSD analysis.

        This command is also valid in PREP7.
        """
        command = f"PSDSPL,{tblno},{rmin},{rmax}"
        return self.run(command, **kwargs)

    def psdunit(self, tblno: str = "", type_: str = "", gvalue: str = "", **kwargs):
        r"""Defines the type of input PSD.

        Mechanical APDL Command: `PSDUNIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSDUNIT.html>`_

        **Command default:**

        .. _PSDUNIT_default:

        Acceleration (ACEL) spectrum (acceleration :sup:`2` /Hz).

        Parameters
        ----------
        tblno : str
            Input table number.

        type_ : str
            Label identifying the type of spectrum:

            * ``DISP`` - Displacement spectrum (in terms of displacement :sup:`2` /Hz ).

            * ``VELO`` - Velocity spectrum (in terms of velocity :sup:`2` /Hz ).

            * ``ACEL`` - Acceleration spectrum (in terms of acceleration :sup:`2` /Hz ).

            * ``ACCG`` - Acceleration spectrum (in terms of g :sup:`2` /Hz ).

            * ``FORC`` - Force spectrum (in terms of force :sup:`2` /Hz ).

            * ``PRES`` - Pressure spectrum (in terms of pressure :sup:`2` /Hz ).

        gvalue : str
            Value of acceleration due to gravity in any arbitrary units for Type=ACCG. Default is 386.4
            in/sec :sup:`2`.

        Notes
        -----

        .. _PSDUNIT_notes:

        Defines the type of PSD defined by the :ref:`psdval`, :ref:`coval`, and :ref:`qdval` commands.

        Force (FORC) and pressure (PRES) type spectra can be used only as a nodal excitation.

        ``GVALUE`` is valid only when type ACCG is specified. A zero or negative value cannot be used. A
        parameter substitution can also be performed.

        This command is also valid in PREP7.
        """
        command = f"PSDUNIT,{tblno},{type_},{gvalue}"
        return self.run(command, **kwargs)

    def psdval(
        self,
        tblno: str = "",
        sv1: str = "",
        sv2: str = "",
        sv3: str = "",
        sv4: str = "",
        sv5: str = "",
        sv6: str = "",
        sv7: str = "",
        **kwargs,
    ):
        r"""Defines PSD values.

        Mechanical APDL Command: `PSDVAL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSDVAL.html>`_

        Parameters
        ----------
        tblno : str
            Input table number being defined.

        sv1 : str
            Spectral values corresponding to the frequency points ( :ref:`psdfrq` ). Values are interpreted
            as defined with the :ref:`psdunit` command.

        sv2 : str
            Spectral values corresponding to the frequency points ( :ref:`psdfrq` ). Values are interpreted
            as defined with the :ref:`psdunit` command.

        sv3 : str
            Spectral values corresponding to the frequency points ( :ref:`psdfrq` ). Values are interpreted
            as defined with the :ref:`psdunit` command.

        sv4 : str
            Spectral values corresponding to the frequency points ( :ref:`psdfrq` ). Values are interpreted
            as defined with the :ref:`psdunit` command.

        sv5 : str
            Spectral values corresponding to the frequency points ( :ref:`psdfrq` ). Values are interpreted
            as defined with the :ref:`psdunit` command.

        sv6 : str
            Spectral values corresponding to the frequency points ( :ref:`psdfrq` ). Values are interpreted
            as defined with the :ref:`psdunit` command.

        sv7 : str
            Spectral values corresponding to the frequency points ( :ref:`psdfrq` ). Values are interpreted
            as defined with the :ref:`psdunit` command.

        Notes
        -----

        .. _PSDVAL_notes:

        Defines PSD values to be associated with the previously defined frequency points.

        Repeat :ref:`psdval` command for additional values, up to the number of frequency points (
        :ref:`psdfrq` ). Values are added after the last nonzero value.

        This command is also valid in PREP7.
        """
        command = f"PSDVAL,{tblno},{sv1},{sv2},{sv3},{sv4},{sv5},{sv6},{sv7}"
        return self.run(command, **kwargs)

    def psdwav(
        self, tblno: str = "", vx: str = "", vy: str = "", vz: str = "", **kwargs
    ):
        r"""Defines a wave propagation excitation in a PSD analysis.

        Mechanical APDL Command: `PSDWAV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSDWAV.html>`_

        Parameters
        ----------
        tblno : str
            Input PSD table number defined with :ref:`psdval` command.

        vx : str
            Global Cartesian X-velocity of traveling wave.

        vy : str
            Global Cartesian Y-velocity of traveling wave.

        vz : str
            Global Cartesian Z-velocity of traveling wave.

        Notes
        -----

        .. _PSDWAV_notes:

        Defines a traveling wave in a PSD analysis. This command is not available for a pressure PSD
        analysis.

        This command is also valid in PREP7.
        """
        command = f"PSDWAV,{tblno},{vx},{vy},{vz}"
        return self.run(command, **kwargs)

    def qdval(
        self,
        tblno1: str = "",
        tblno2: str = "",
        sv1: str = "",
        sv2: str = "",
        sv3: str = "",
        sv4: str = "",
        sv5: str = "",
        sv6: str = "",
        sv7: str = "",
        **kwargs,
    ):
        r"""Defines PSD quadspectral values.

        Mechanical APDL Command: `QDVAL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_QDVAL.html>`_

        Parameters
        ----------
        tblno1 : str
            First input PSD table number associated with this spectrum.

        tblno2 : str
            Second input PSD table number associated with this spectrum.

        sv1 : str
            PSD quadspectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv2 : str
            PSD quadspectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv3 : str
            PSD quadspectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv4 : str
            PSD quadspectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv5 : str
            PSD quadspectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv6 : str
            PSD quadspectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        sv7 : str
            PSD quadspectral values corresponding to the frequency points ( :ref:`psdfrq` ).

        Notes
        -----

        .. _QDVAL_notes:

        Defines PSD quadspectral values to be associated with the previously defined frequency points.
        Repeat :ref:`qdval` command with the same table number for additional points. Unlike autospectra (
        :ref:`psdval` ), the quadspectra can be positive or negative. The quadspectral curve segment where
        there is a sign change is interpolated linearly (the rest of the curve segments use log-log
        interpolation). For better accuracy, choose as small a curve segment as possible wherever a sign
        change occurs.

        Two table numbers are required since values are off-diagonal terms. This command is valid for
        :ref:`spopt`,PSD only.

        This command is also valid in PREP7.
        """
        command = f"QDVAL,{tblno1},{tblno2},{sv1},{sv2},{sv3},{sv4},{sv5},{sv6},{sv7}"
        return self.run(command, **kwargs)

    def rigresp(
        self,
        option: str = "",
        method: str = "",
        val1: str = "",
        val2: str = "",
        **kwargs,
    ):
        r"""Specifies the rigid response calculation.

        Mechanical APDL Command: `RIGRESP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RIGRESP.html>`_

        Parameters
        ----------
        option : str
            Flag to activate or deactivate the rigid response calculation:

            * ``1 (ON or YES)`` - Activate.

            * ``2 (OFF or NO)`` - Deactivate. This value is the default.

        method : str
            Method used to calculate the rigid response:

            * ``GUPTA`` - Gupta method.

            * ``LINDLEY`` - Lindley-Yow method.

        val1 : str
            If ``Method`` = GUPTA, ``Val1`` represents the frequency F:sub:`1` in Hertz.

            If ``Method`` = LINDLEY, ``Val1`` is the Zero Period Acceleration (ZPA). If a scale factor is
            defined (FACT in the :ref:`svtyp` command), it is used to scale this value

        val2 : str
            If ``Method`` = GUPTA, ``Val2`` represents the frequency F:sub:`2` in Hertz.

        Notes
        -----

        .. _RIGRESP_notes:

        This rigid response calculation is only valid for single point response spectrum analysis (
        :ref:`spopt`, SPRS) and multiple point response spectrum analysis ( :ref:`spopt`, MPRS) with
        combination methods ( :ref:`srss` ), complete quadratic ( :ref:`cqc` ) or Rosenblueth ( :ref:`rose`
        )

        This command is also valid in PREP7.

        * `Performing a Single-Point Response Spectrum (SPRS) Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR6_4.html#aYACegwrd>`_
        * `Performing a Multi-Point Response Spectrum (MPRS) Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR6_10.html#spectrum_multipoint>`_
        * `Rigid Responses
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eqfa88cef4-37ad-4f72-9bc5-082358cc4a12>`_
          in the `Mechanical APDL Theory Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_
        * :ref:`mmass` command
        """
        command = f"RIGRESP,{option},{method},{val1},{val2}"
        return self.run(command, **kwargs)

    def rock(
        self,
        cgx: str = "",
        cgy: str = "",
        cgz: str = "",
        omx: str = "",
        omy: str = "",
        omz: str = "",
        **kwargs,
    ):
        r"""Specifies a rocking response spectrum.

        Mechanical APDL Command: `ROCK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ROCK.html>`_

        Parameters
        ----------
        cgx : str
            Global Cartesian X, Y, and Z location of center of rotation about which rocking occurs.

        cgy : str
            Global Cartesian X, Y, and Z location of center of rotation about which rocking occurs.

        cgz : str
            Global Cartesian X, Y, and Z location of center of rotation about which rocking occurs.

        omx : str
            Global Cartesian angular components of the rocking.

        omy : str
            Global Cartesian angular components of the rocking.

        omz : str
            Global Cartesian angular components of the rocking.

        Notes
        -----

        .. _ROCK_notes:

        Specifies a rocking response spectrum effect in the spectrum ( :ref:`antype`,SPECTR) analysis.

        The excitation direction with rocking included is not normalized to one; rather, it scales the
        spectrum. For example, consider a node at coordinates (1,1,0), subject to an excitation in the X
        direction ( ``SEDX`` = 1.0 on :ref:`sed` ), and a rocking with center ``CGX`` = 1.0, ``CGY`` =
        ``CGZ`` = 0, and angular component about Z ( ``OMZ`` = 0.5). The total excitation direction at this
        node is:

        .. math::

            equation not available

        So that half the spectrum input is applied at this node.

        For more information on the equations, see `Participation Factors and Mode Coefficients
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eqe483f2f2-aaa1-4080-a835-10c0e1e18f57>`_

        This command is also valid in PREP7.
        """
        command = f"ROCK,{cgx},{cgy},{cgz},{omx},{omy},{omz}"
        return self.run(command, **kwargs)

    def rose(
        self,
        signif: str = "",
        label: str = "",
        td: str = "",
        forcetype: str = "",
        **kwargs,
    ):
        r"""Specifies the Rosenblueth mode combination method.

        Mechanical APDL Command: `ROSE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ROSE.html>`_

        Parameters
        ----------
        signif : str
            Combine only those modes whose significance level exceeds the SIGNIF threshold. For single
            point, multipoint, or DDAM response ( :ref:`spopt`, SPRS, MPRS, or DDAM), the significance level
            of a mode is defined as the mode coefficient divided by the maximum mode coefficient of all
            modes. Any mode whose significance level is less than ``SIGNIF`` is considered insignificant and
            does not contribute to the mode combinations. The higher the SIGNIF threshold, the fewer the
            number of modes combined. ``SIGNIF`` defaults to 0.001. If SIGNIF is specified as 0.0, it is
            taken as 0.0. (This mode combination method is not valid for :ref:`spopt`,PSD.)

        label : str
            Label identifying the combined mode solution output.

            * ``DISP`` - Displacement solution (default). Displacements, stresses, forces, etc., are available.

            * ``VELO`` - Velocity solution. Velocities, "stress velocities," "force velocities," etc., are
              available.

            * ``ACEL`` - Acceleration solution. Accelerations, "stress accelerations," "force accelerations,"
              etc. are available.

        td : str
            Time duration for earthquake or shock spectrum. ``TD`` defaults to 10.

        forcetype : str
            Label identifying the forces to be combined:

            * ``STATIC`` - Combine the modal static forces (default).

            * ``TOTAL`` - Combine the modal static plus inertial forces.

        Notes
        -----

        .. _ROSE_notes:

        For more information on spectrum analysis combination methods, see `Combination of Modes
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#rosemeth1f>`_

        This command is also valid in PREP7.
        """
        command = f"ROSE,{signif},{label},{td},{forcetype}"
        return self.run(command, **kwargs)

    def sed(
        self, sedx: str = "", sedy: str = "", sedz: str = "", cname: str = "", **kwargs
    ):
        r"""Defines the excitation direction for response spectrum and PSD analyses.

        Mechanical APDL Command: `SED <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SED.html>`_

        Parameters
        ----------
        sedx : str
            Global Cartesian coordinates of a point that defines a line (through the origin) corresponding
            to the excitation direction. For example: 0.0, 1.0, 0.0 defines global Y as the spectrum
            direction.

        sedy : str
            Global Cartesian coordinates of a point that defines a line (through the origin) corresponding
            to the excitation direction. For example: 0.0, 1.0, 0.0 defines global Y as the spectrum
            direction.

        sedz : str
            Global Cartesian coordinates of a point that defines a line (through the origin) corresponding
            to the excitation direction. For example: 0.0, 1.0, 0.0 defines global Y as the spectrum
            direction.

        cname : str
            The component name corresponding to the group of excited nodes. Only applies to base excitation
            multi-point response spectrum analysis ( :ref:`spopt`, MPRS) and power spectral density analysis
            ( :ref:`spopt`, PSD). Defaults to no component.

        Notes
        -----

        .. _SED_notes:

        In single-point response spectrum analysis ( :ref:`spopt`,SPRS), the excitation direction without
        rocking ( :ref:`rock` ) is normalized to one so that the ``SEDX``, ``SEDY``, and ``SEDZ`` values do
        not scale the spectrum. The excitation direction with rocking is not normalized. The ``SEDX``,
        ``SEDY``, and ``SEDZ`` values must be consistent with the linear components of ``OMX``, ``OMY``, and
        ``OMZ`` values on the :ref:`rock` command. The calculated direction then scales the spectrum. For
        more information, see `Participation Factors and Mode Coefficients
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eqe483f2f2-aaa1-4080-a835-10c0e1e18f57>`_.

        In multi-point response spectrum analysis ( :ref:`spopt`,MPRS) and power spectral density analysis
        ( :ref:`spopt`,PSD), the excitation direction is normalized to one so that the ``SEDX``, ``SEDY``,
        and ``SEDZ`` values do not scale the spectrum. The component name ( ``Cname`` ) is required. The
        constraints corresponding to the excitation direction are applied to the component nodes.

        This command is also valid in PREP7.
        """
        command = f"SED,{sedx},{sedy},{sedz},{cname}"
        return self.run(command, **kwargs)

    def spdamp(self, tblno: str = "", curvno: str = "", dampratio: str = "", **kwargs):
        r"""Defines input spectrum damping in a multi-point response spectrum analysis.

        Mechanical APDL Command: `SPDAMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPDAMP.html>`_

        Parameters
        ----------
        tblno : str
            Input table number. Corresponds to the frequency table number ( ``TBLNO`` on the :ref:`spfreq`
            command).

        curvno : str
            Input curve number. Corresponds to the spectrum values curve number ( ``CURVNO`` on the
            :ref:`spval` command).

        dampratio : str
            Damping ratio for the response spectrum curve. Up to 20 different curves may be defined, each
            with a different damping ratio. Damping values must be input in ascending order.

        Notes
        -----

        .. _SPDAMP_notes:

        Defines multi-point response spectrum damping value to be associated with:

        * Previously defined frequency points ( :ref:`spfreq` ).

        * Subsequently defined spectrum points ( :ref:`spval` ).

        Damping values are used only to identify input spectrum values for the mode coefficients
        calculation.

        The curve number must be input in ascending order starting with 1.

        This command is also valid in PREP7.
        """
        command = f"SPDAMP,{tblno},{curvno},{dampratio}"
        return self.run(command, **kwargs)

    def spfreq(
        self,
        tblno: str = "",
        freq1: str = "",
        freq2: str = "",
        freq3: str = "",
        freq4: str = "",
        freq5: str = "",
        freq6: str = "",
        freq7: str = "",
        **kwargs,
    ):
        r"""Defines the frequency points for the input spectrum tables :ref:`spval` vs. :ref:`spfreq` for multi-
        point spectrum analysis.

        Mechanical APDL Command: `SPFREQ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPFREQ.html>`_

        Parameters
        ----------
        tblno : str
            Input table number. Up to 200 tables may be defined.

        freq1 : str
            Frequency points (Hz) for spectrum vs. frequency tables. ``FREQ1`` should be greater than zero,
            and values must be in ascending order.

        freq2 : str
            Frequency points (Hz) for spectrum vs. frequency tables. ``FREQ1`` should be greater than zero,
            and values must be in ascending order.

        freq3 : str
            Frequency points (Hz) for spectrum vs. frequency tables. ``FREQ1`` should be greater than zero,
            and values must be in ascending order.

        freq4 : str
            Frequency points (Hz) for spectrum vs. frequency tables. ``FREQ1`` should be greater than zero,
            and values must be in ascending order.

        freq5 : str
            Frequency points (Hz) for spectrum vs. frequency tables. ``FREQ1`` should be greater than zero,
            and values must be in ascending order.

        freq6 : str
            Frequency points (Hz) for spectrum vs. frequency tables. ``FREQ1`` should be greater than zero,
            and values must be in ascending order.

        freq7 : str
            Frequency points (Hz) for spectrum vs. frequency tables. ``FREQ1`` should be greater than zero,
            and values must be in ascending order.

        Notes
        -----

        .. _SPFREQ_notes:

        The spectrum values are input with the :ref:`spval` command. A separate :ref:`spfreq` command must
        be used for each table defined. Frequencies must be in ascending order.

        Repeat :ref:`spfreq` command for additional frequency points. Values are added after the last
        nonzero frequency.

        If all fields after :ref:`spfreq` are blank, all input vs. frequency tables are erased. If ``TBLNO``
        is the only non-blank field, all corresponding :ref:`spval` curves are erased.

        Use the :ref:`sptopt` and :ref:`stat` commands to list current frequency points.

        This command is also valid in PREP7.
        """
        command = (
            f"SPFREQ,{tblno},{freq1},{freq2},{freq3},{freq4},{freq5},{freq6},{freq7}"
        )
        return self.run(command, **kwargs)

    def spgraph(self, tblno: str = "", curvno: str = "", curvnobeg: str = "", **kwargs):
        r"""Displays input spectrum curves for MPRS analysis.

        Mechanical APDL Command: `SPGRAPH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPGRAPH.html>`_

        Parameters
        ----------
        tblno : str
            Table number to display. Defaults to 1.

        curvno : str
            Curve number to display. Defaults to none.

        curvnobeg : str
            Beginning of the curve number range to display. Defaults to 1.

        Notes
        -----

        .. _SPGRAPH_notes:

        You can display up to 10 input spectrum curves ( :ref:`spval` and :ref:`spfreq` commands) with log X
        scale.

        If the input spectrum curves are not associated with a damping value ( :ref:`spdamp` command),
        ``CURVNO`` and ``CURVNOBeg`` are not applicable and table ``TBLNO`` is displayed. Otherwise, specif
        y ``CURVNO`` or ``CURVNOBeg`` :

        * if ``CURVNO`` is used, one curve is displayed.

        * if ``CURVNOBeg`` is used, up to 10 curves are displayed. ``CURVNOBeg`` is the beginning of the
          curve number range of interest.
        """
        command = f"SPGRAPH,{tblno},{curvno},{curvnobeg}"
        return self.run(command, **kwargs)

    def spopt(
        self,
        spectype: str = "",
        nmode: str = "",
        elcalc: str = "",
        modereusekey: str = "",
        **kwargs,
    ):
        r"""Selects the spectrum type and other spectrum options.

        Mechanical APDL Command: `SPOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPOPT.html>`_

        Parameters
        ----------
        spectype : str
            Spectrum type:

            * ``SPRS`` - Single point excitation response spectrum (default). See also :ref:`svtyp`.

            * ``MPRS`` - Multiple point excitation response spectrum.

            * ``DDAM`` - Dynamic design analysis method.

            * ``PSD`` - Power spectral density.

        nmode : str
            Use the first ``NMODE`` modes from the modal analysis. Defaults to all extracted modes, as
            specified by the :ref:`modopt` and :ref:`bucopt` commands. ``NMODE`` cannot be larger than
            10000.

        elcalc : str
            Element results calculation key:

            * ``NO`` - Do not calculate element results and reaction forces (default).

            * ``YES`` - Calculate element results and reaction forces, as well as the nodal degree of freedom
              solution.

        modereusekey : str
            Key for existing ``MODE`` file reuse when running multiple spectrum analyses:

            * ``NO`` - No spectrum analysis has been performed yet (default).

            * ``YES`` - This is not the first spectrum analysis. The ``MODE`` file will be reused and the
              necessary files will be cleaned up for the new spectrum analysis.

        Notes
        -----

        .. _SPOPT_notes:

        Valid only for a spectrum analysis ( :ref:`antype`,SPECTR). This operation must be preceded by a
        modal solution ( :ref:`antype`,MODAL) with the appropriate files available. Both the spectrum
        analysis and the preceding modal analysis must be performed under the same Mechanical APDL version
        number.

        If used in SOLUTION, this command is valid only within the first load step.

        Element results are calculated ( ``Elcalc`` = YES) only if the element modal results are available
        (written to the :file:`Jobname.mode` file with ``MSUPkey`` = YES on the :ref:`mxpand` command). For
        ``Sptype`` = SPRS, MPRS, and DDAM, if the element results calculation is activated ( ``Elcalc`` =
        YES) and element modal results are not available, it is deactivated automatically.

        For SPRS, DDAM or MPRS analyses, modal responses can be combined and stored directly in the
        :file:`Jobname.rst` file during spectrum solution according to the mode combination method command
        issued ( :ref:`srss`, :ref:`cqc`, etc.) for ``Elcalc`` = YES. This can save significant time
        compared to the method for ``Elcalc`` = NO, which requires generating the file of POST1 commands (
        :file:`Jobname.mcom` file) to be read in POST1 to do the mode combinations. For details and example
        usage, see `Spectrum Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR6_10.html>`_, and Example:
        Multi-Point Response Spectrum (MPRS) Analysis.

        This command is also valid in PREP7.
        """
        command = f"SPOPT,{spectype},{nmode},{elcalc},{modereusekey}"
        return self.run(command, **kwargs)

    def spunit(
        self,
        tblno: str = "",
        type_: str = "",
        gvalue: str = "",
        keyinterp: str = "",
        **kwargs,
    ):
        r"""Defines the type of multi-point response spectrum.

        Mechanical APDL Command: `SPUNIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPUNIT.html>`_

        Parameters
        ----------
        tblno : str
            Input table number.

        type_ : str
            Label identifying the type of spectrum:

            * ``DISP`` - Displacement spectrum ( :ref:`spval` values interpreted as displacements with units of
              length).

            * ``VELO`` - Velocity spectrum ( :ref:`spval` values interpreted as velocities with units of
              length/time).

            * ``ACEL`` - Acceleration spectrum ( :ref:`spval` values interpreted as accelerations with units of
              length/time :sup:`2` ).

            * ``ACCG`` - Acceleration spectrum ( :ref:`spval` values interpreted as accelerations with units of
              g/time :sup:`2` ).

            * ``FORC`` - Force spectrum.

            * ``PRES`` - Pressure spectrum.

        gvalue : str
            Value of acceleration due to gravity in any arbitrary units for Type=ACCG table. Default is
            386.4 in/sec :sup:`2`.

        keyinterp : str
            Key to activate or deactivate the linear interpolation between input response spectrum points and
            input response spectrum curves:

            * ``0 (OFF or NO)`` - Deactivate linear and use logarithmic interpolation. This value is the
              default.

            * ``1 (ON or YES)`` - Activate linear interpolation.

        Notes
        -----

        .. _SPUNIT_notes:

        Defines the type of multi-point response spectrum defined by the :ref:`spfreq` and :ref:`spval`
        commands.

        Force ( **FORC** ) and pressure ( **PRES** ) type spectra can be used only as a nodal excitation.

        ``GVALUE`` is valid only when ``Type`` = ACCG is specified. A zero or negative value cannot be used.
        A parameter substitution can also be performed.

        This command is also valid in PREP7.
        """
        command = f"SPUNIT,{tblno},{type_},{gvalue},{keyinterp}"
        return self.run(command, **kwargs)

    def spval(
        self,
        tblno: str = "",
        curvno: str = "",
        sv1: str = "",
        sv2: str = "",
        sv3: str = "",
        sv4: str = "",
        sv5: str = "",
        sv6: str = "",
        sv7: str = "",
        **kwargs,
    ):
        r"""Defines multi-point response spectrum values.

        Mechanical APDL Command: `SPVAL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPVAL.html>`_

        Parameters
        ----------
        tblno : str
            Input table number. It corresponds to ``TBLNO`` on the :ref:`spfreq` command.

        curvno : str
            Input curve number. It corresponds to ``CURVNO`` on the :ref:`spdamp` command (optional).

        sv1 : str
            Spectral values corresponding to the frequency points ( :ref:`spfreq` ) and damping ratio (
            :ref:`spdamp` ). Values are interpreted as defined with the :ref:`spunit` command.

        sv2 : str
            Spectral values corresponding to the frequency points ( :ref:`spfreq` ) and damping ratio (
            :ref:`spdamp` ). Values are interpreted as defined with the :ref:`spunit` command.

        sv3 : str
            Spectral values corresponding to the frequency points ( :ref:`spfreq` ) and damping ratio (
            :ref:`spdamp` ). Values are interpreted as defined with the :ref:`spunit` command.

        sv4 : str
            Spectral values corresponding to the frequency points ( :ref:`spfreq` ) and damping ratio (
            :ref:`spdamp` ). Values are interpreted as defined with the :ref:`spunit` command.

        sv5 : str
            Spectral values corresponding to the frequency points ( :ref:`spfreq` ) and damping ratio (
            :ref:`spdamp` ). Values are interpreted as defined with the :ref:`spunit` command.

        sv6 : str
            Spectral values corresponding to the frequency points ( :ref:`spfreq` ) and damping ratio (
            :ref:`spdamp` ). Values are interpreted as defined with the :ref:`spunit` command.

        sv7 : str
            Spectral values corresponding to the frequency points ( :ref:`spfreq` ) and damping ratio (
            :ref:`spdamp` ). Values are interpreted as defined with the :ref:`spunit` command.

        Notes
        -----

        .. _SPVAL_notes:

        Notes
        Defines multi-point response spectrum values to be associated with the previously defined frequency
        points ( :ref:`spfreq` ). It can also be associated with the previously defined damping value (
        :ref:`spdamp` ). If ``CURVNO`` is not specified, the input spectrum is not associated with a damping
        value.

        Repeat :ref:`spval` command for additional values, up to the number of frequency points (
        :ref:`spfreq` ). Values are added after the last nonzero value.

        The interpolation method between response spectrum points and curves is specified using
        ``KeyInterp`` on the :ref:`spunit` command. It is logarithmic by default.

        Use the :ref:`sptopt` and :ref:`stat` commands to list current spectrum curve values.

        This command is also valid in PREP7.
        """
        command = f"SPVAL,{tblno},{curvno},{sv1},{sv2},{sv3},{sv4},{sv5},{sv6},{sv7}"
        return self.run(command, **kwargs)

    def srss(
        self,
        signif: str = "",
        label: str = "",
        abssumkey: str = "",
        forcetype: str = "",
        **kwargs,
    ):
        r"""Specifies the square root of sum of squares mode combination method.

        Mechanical APDL Command: `SRSS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SRSS.html>`_

        Parameters
        ----------
        signif : str
            Combine only those modes whose significance level exceeds the ``SIGNIF`` threshold. For single
            point, multipoint, or DDAM response ( :ref:`spopt`,SPRS, MPRS or DDAM), the significance level
            of a mode is defined as the mode coefficient divided by the maximum mode coefficient of all
            modes. Any mode whose significance level is less than ``SIGNIF`` is considered insignificant and
            is not contributed to the mode combinations. The higher the ``SIGNIF`` threshold, the fewer the
            number of modes combined. ``SIGNIF`` defaults to 0.001. If ``SIGNIF`` is specified as 0.0, it is
            taken as 0.0. (This mode combination method is not valid for :ref:`spopt`,PSD.)

        label : str
            Label identifying the combined mode solution output.

            * ``DISP`` - Displacement solution (default). Displacements, stresses, forces, etc., are available.

            * ``VELO`` - Velocity solution. Velocities, "stress velocities," "force velocities," etc., are
              available.

            * ``ACEL`` - Acceleration solution. Accelerations, "stress accelerations," "force accelerations,"
              etc., are available.

        abssumkey : str
            Absolute Sum combination key (for :ref:`spopt`,MPRS only):

            * ``NO`` - Do not use the Absolute Sum method (default).

            * ``YES`` - Combine the modes per excitation direction using the Absolute Sum method, then combine
              the resulting quantities using the square root of sum of squares method.

              When using Absolute Sum combination, the excitation direction must be specified using the :ref:`sed`
              command.

        forcetype : str
            Label identifying the forces to be combined:

            * ``STATIC`` - Combine the modal static forces (default).

            * ``TOTAL`` - Combine the modal static plus inertial forces.

        Notes
        -----

        .. _SRSS_notes:

        This command is also valid for PREP7.
        """
        command = f"SRSS,{signif},{label},{abssumkey},{forcetype}"
        return self.run(command, **kwargs)

    def sv(
        self,
        damp: str = "",
        sv1: str = "",
        sv2: str = "",
        sv3: str = "",
        sv4: str = "",
        sv5: str = "",
        sv6: str = "",
        sv7: str = "",
        sv8: str = "",
        sv9: str = "",
        **kwargs,
    ):
        r"""Defines spectrum values to be associated with frequency points.

        Mechanical APDL Command: `SV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SV.html>`_

        Parameters
        ----------
        damp : str
            Damping ratio for this response spectrum curve. If the same as a previously defined curve, the
            SV values are added to the previous curve. Up to four different curves may be defined, each with
            a different damping ratio. Damping values must be input in ascending order.

        sv1 : str
            Spectrum values corresponding to the frequency points ( :ref:`freq` ). Values are interpreted as
            defined with the :ref:`svtyp` command. SV values should not be zero. Values required outside the
            frequency range use the extreme input values.

        sv2 : str
            Spectrum values corresponding to the frequency points ( :ref:`freq` ). Values are interpreted as
            defined with the :ref:`svtyp` command. SV values should not be zero. Values required outside the
            frequency range use the extreme input values.

        sv3 : str
            Spectrum values corresponding to the frequency points ( :ref:`freq` ). Values are interpreted as
            defined with the :ref:`svtyp` command. SV values should not be zero. Values required outside the
            frequency range use the extreme input values.

        sv4 : str
            Spectrum values corresponding to the frequency points ( :ref:`freq` ). Values are interpreted as
            defined with the :ref:`svtyp` command. SV values should not be zero. Values required outside the
            frequency range use the extreme input values.

        sv5 : str
            Spectrum values corresponding to the frequency points ( :ref:`freq` ). Values are interpreted as
            defined with the :ref:`svtyp` command. SV values should not be zero. Values required outside the
            frequency range use the extreme input values.

        sv6 : str
            Spectrum values corresponding to the frequency points ( :ref:`freq` ). Values are interpreted as
            defined with the :ref:`svtyp` command. SV values should not be zero. Values required outside the
            frequency range use the extreme input values.

        sv7 : str
            Spectrum values corresponding to the frequency points ( :ref:`freq` ). Values are interpreted as
            defined with the :ref:`svtyp` command. SV values should not be zero. Values required outside the
            frequency range use the extreme input values.

        sv8 : str
            Spectrum values corresponding to the frequency points ( :ref:`freq` ). Values are interpreted as
            defined with the :ref:`svtyp` command. SV values should not be zero. Values required outside the
            frequency range use the extreme input values.

        sv9 : str
            Spectrum values corresponding to the frequency points ( :ref:`freq` ). Values are interpreted as
            defined with the :ref:`svtyp` command. SV values should not be zero. Values required outside the
            frequency range use the extreme input values.

        Notes
        -----

        .. _SV_notes:

        Defines the spectrum values to be associated with the previously defined frequency points (
        :ref:`freq` ). Applies only to the single-point response spectrum. Damping has no effect on the
        frequency solution. Damping values are used only to identify SV curves for the mode combinations
        calculation. Only the curve with the lowest damping value is used in the initial mode coefficient
        calculation. Use :ref:`stat` command to list current spectrum curve values.

        Repeat :ref:`sv` command for additional SV points (100 maximum per ``DAMP`` curve). SV values are
        added to the ``DAMP`` curve after the last nonzero SV value.

        The interpolation method between response spectrum points and curves is specified using
        ``KeyInterp`` in the :ref:`svtyp`  command. It is logarithmic by default.

        This command is also valid in PREP7.
        """
        command = f"SV,{damp},{sv1},{sv2},{sv3},{sv4},{sv5},{sv6},{sv7},{sv8},{sv9}"
        return self.run(command, **kwargs)

    def svplot(
        self,
        optionscale: str = "",
        damp1: str = "",
        damp2: str = "",
        damp3: str = "",
        damp4: str = "",
        **kwargs,
    ):
        r"""Displays input spectrum curves.

        Mechanical APDL Command: `SVPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/None>`_

        Parameters
        ----------
        optionscale : str
            Flag to activate or deactivate input spectrum value scaling:

            * ``OFF`` - Do not scale the input spectrum values with scale factor FACT ( :ref:`svtyp` command).
              This is the default value.

            * ``ON`` - Scale the input spectrum values with scale factor FACT ( :ref:`svtyp` command)

        damp1 : str
            Damping ratio corresponding to DAMP ( :ref:`sv` command) defining the first spectrum curve.

        damp2 : str
            Damping ratio corresponding to DAMP ( :ref:`sv` command) defining the second spectrum curve.

        damp3 : str
            Damping ratio corresponding to DAMP ( :ref:`sv` command) defining the third spectrum curve.

        damp4 : str
            Damping ratio corresponding to DAMP ( :ref:`sv` command) defining the fourth spectrum curve.

        Notes
        -----

        .. _SVPLOT_notes:

        You can display up to four input spectrum tables ( :ref:`sv` and :ref:`freq` commands) with log X
        scale. If no damping ratio is specified, all spectrum tables are displayed.

        This command is valid in any processor.
        """
        command = f"SVPLOT,{optionscale},{damp1},{damp2},{damp3},{damp4}"
        return self.run(command, **kwargs)

    def svtyp(self, ksv: int | str = "", fact: str = "", keyinterp: str = "", **kwargs):
        r"""Defines the type of single-point response spectrum.

        Mechanical APDL Command: `SVTYP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SVTYP.html>`_

        Parameters
        ----------
        ksv : int or str
            Response spectrum type:

            * ``0`` - Seismic velocity response spectrum loading (SV values interpreted as velocities with units
              of length/time).

            * ``1`` - Force response spectrum loading (SV values interpreted as force amplitude multipliers).

            * ``2`` - Seismic acceleration response spectrum loading (SV values interpreted as accelerations
              with units of length/time :sup:`2` ).

            * ``3`` - Seismic displacement response spectrum loading (SV values interpreted as displacements
              with units of length).

        fact : str
            Scale factor applied to spectrum values (defaults to 1.0). Values are scaled when the solution
            is initiated ( :ref:`solve` ). Database values remain the same.

        keyinterp : str
            Key to activate or deactivate the linear interpolation between input response spectrum points and
            input response spectrum curves:

            * ``0 (OFF, or NO)`` - Deactivate linear and use logarithmic interpolation. This value is the
              default.

            * ``1 (ON, or YES)`` - Activate linear interpolation.

        Notes
        -----

        .. _SVTYP_notes:

        Defines the type of single-point response spectrum ( :ref:`spopt` ). The seismic excitation
        direction is defined with the :ref:`sed` command.

        This command is also valid in PREP7.
        """
        command = f"SVTYP,{ksv},{fact},{keyinterp}"
        return self.run(command, **kwargs)

    def vddam(self, vf: str = "", va: str = "", vb: str = "", vc: str = "", **kwargs):
        r"""Specifies the velocity spectrum computation constants for the analysis of shock resistance of
        shipboard structures.

        Mechanical APDL Command: `VDDAM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VDDAM.html>`_

        Parameters
        ----------
        vf : str
            Direction-dependent velocity coefficient for elastic or elastic-plastic analysis option (Default
            = 0).

        va : str
            Coefficients for the DDAM velocity spectrum equations. See `Dynamic Design Analysis Method
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eq1bf15231-590e-4b5a-a30a-aa31e15bf78f>`_

        vb : str
            Coefficients for the DDAM velocity spectrum equations. See `Dynamic Design Analysis Method
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eq1bf15231-590e-4b5a-a30a-aa31e15bf78f>`_

        vc : str
            Coefficients for the DDAM velocity spectrum equations. See `Dynamic Design Analysis Method
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eq1bf15231-590e-4b5a-a30a-aa31e15bf78f>`_

        Notes
        -----

        .. _VDDAM_notes:

        This command specifies velocity coefficients to analyze shock resistance of shipboard equipment.
        These coefficients are used to compute mode coefficients according to the equations given in
        `Dynamic Design Analysis Method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_anproc7.html#eq1bf15231-590e-4b5a-a30a-aa31e15bf78f>`_
        :ref:`addam` and :ref:`sed` commands, is used with the spectrum ( :ref:`antype`,SPECTR) analysis as
        a special purpose alternative to the :ref:`sv`, :ref:`freq`, and :ref:`svtyp` commands.

        In order to perform a DDAM spectrum analysis using a units system other than BIN (default), you must
        specify the units system complying with the mass and length units of the model using the
        :ref:`units` command. Issue the :ref:`units` command before defining the shock spectrum computation
        constants ( :ref:`vddam` ). The :ref:`vddam` command is not supported with the user-defined units
        system ( ``Label`` = USER on the :ref:`units` command).

        :ref:`ddaspec` may alternatively be used to calculate spectrum coefficients.

        This command is also valid in PREP7.
        """
        command = f"VDDAM,{vf},{va},{vb},{vc}"
        return self.run(command, **kwargs)
