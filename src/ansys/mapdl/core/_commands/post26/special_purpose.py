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


class SpecialPurpose(CommandsBase):

    def cvar(
        self,
        ir: str = "",
        ia: str = "",
        ib: str = "",
        itype: int | str = "",
        datum: int | str = "",
        name: str = "",
        **kwargs,
    ):
        r"""Computes covariance between two quantities.

        Mechanical APDL Command: `CVAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CVAR.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to ``NV`` ( :ref:`numvar` )).
            If this number is the same as for a previous variable, the previous variable will be overwritten
            with this result.

        ia : str
            Reference numbers of the two variables to be operated on. If only one, leave ``IB`` blank.

        ib : str
            Reference numbers of the two variables to be operated on. If only one, leave ``IB`` blank.

        itype : int or str
            Defines the type of response PSD to be calculated:

            * ``0,1`` - Displacement (default).

            * ``2`` - Velocity.

            * ``3`` - Acceleration.

        datum : int or str
            Defines the reference with respect to which covariance is to be calculated:

            * ``1`` - Absolute value.

            * ``2`` - Relative to base (default).

        name : str
            Thirty-two character name for identifying the variable on listings and displays. Embedded blanks
            are compressed upon output.

        Notes
        -----

        .. _CVAR_notes:

        This command computes the covariance value for the variables referenced by the reference numbers
        ``IA`` and ``IB``. If ``DATUM`` = 2, the variable referenced by ``IR`` will contain the individual
        modal contributions (that is, the dynamic or relative values). If ``DATUM`` = 1, the variable
        referenced by ``IR`` will contain the modal contributions followed by the contributions of pseudo-
        static and covariance between dynamic and pseudo-static responses. :file:`File.PSD` must be
        available for the calculations to occur.
        """
        command = f"CVAR,{ir},{ia},{ib},{itype},{datum},{name}"
        return self.run(command, **kwargs)

    def pmgtran(
        self,
        fname: str = "",
        freq: str = "",
        fcnam1: str = "",
        fcnam2: str = "",
        pcnam1: str = "",
        pcnam2: str = "",
        ecnam1: str = "",
        ccnam1: str = "",
        **kwargs,
    ):
        r"""Summarizes electromagnetic results from a transient analysis.

        Mechanical APDL Command: `PMGTRAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PMGTRAN.html>`_

        Parameters
        ----------
        fname : str
            File name (8 characters maximum) to which tabular data and plot files will be written. Must be
            enclosed in single quotes when the command is manually typed in. Defaults to MG_TRNS. The data
            file extension is :file:`.OUT` and the plot file extension is. :file:`PLT`.

        freq : str
            Frequency of solution output. Defaults to 1. Every ``FREQ`` th solution on the results file is
            output.

        fcnam1 : str
            Names of element components for force calculation. Must be enclosed in single quotes when the
            command is manually typed in.

        fcnam2 : str
            Names of element components for force calculation. Must be enclosed in single quotes when the
            command is manually typed in.

        pcnam1 : str
            Names of element components for power loss calculation. Must be enclosed in single quotes when
            the command is manually typed in.

        pcnam2 : str
            Names of element components for power loss calculation. Must be enclosed in single quotes when
            the command is manually typed in.

        ecnam1 : str
            Names of element components for energy and total current calculations, respectively. Must be
            enclosed in single quotes when the command is manually typed in.

        ccnam1 : str
            Names of element components for energy and total current calculations, respectively. Must be
            enclosed in single quotes when the command is manually typed in.

        Notes
        -----

        .. _PMGTRAN_notes:

        :ref:`pmgtran` invokes a Mechanical APDL macro which calculates and summarizes electromagnetic
        results from
        a transient analysis. The results are summarized by element components and listed on the screen as
        well as written to a file ( :file:`Fname.OUT` ).

        You can select two components for the summary of electromagnetic forces, two for power loss, and one
        each for stored energy (see :ref:`senergy` ) and total current (see :ref:`curr2d` ). See the
        referenced commands for other restrictions.

        :ref:`pmgtran` is restricted to MKSA units.
        """
        command = f"PMGTRAN,{fname},{freq},{fcnam1},{fcnam2},{pcnam1},{pcnam2},{ecnam1},{ccnam1}"
        return self.run(command, **kwargs)

    def rcyc(
        self, ir: str = "", ia: str = "", sector: str = "", name: str = "", **kwargs
    ):
        r"""Calculates cyclic results for a mode-superposition harmonic solution.

        Mechanical APDL Command: `RCYC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RCYC.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to ``NV`` ( :ref:`numvar` )).
            If this number is the same as for a previous variable, the previous variable will be overwritten
            with this result.

        ia : str
            Reference number of the variable to be operated on.

        sector : str
            Sector number to calculate the results for.

        name : str
            Thirty-two character name identifying the variable on listings and displays. Embedded blanks are
            compressed for output.

        Notes
        -----

        .. _RCYC_notes:

        This command calculates the harmonic response in the sector specified by ``SECTOR`` for the variable
        referenced by the reference number ``IA``. Only component values for ``IA`` are valid (no principles
        or sums). The variable specified by ``IR`` will contain the harmonic solution. :file:`Jobname.RFRQ`
        from the cyclic mode-superposition harmonic solve and :file:`Jobname.RST` or :file:`Jobname.RSTP`
        from the cyclic modal solve must be available for the calculations to occur. The Jobname must be the
        same for the cyclic modal solve and the cyclic mode-superposition harmonic solve.

        For ``SECTOR`` > 1, the result is in the nodal coordinate system of the base sector, and it is
        rotated to the expanded sector``s location. Refer to `Using the /CYCEXPAND Command
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycpost.html#>`_

        See also `Mode-Superposition Harmonic Cyclic Symmetry Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycsolvharmcycsym.html#cycsym_exampleForcedRespMistuning>`_
        """
        command = f"RCYC,{ir},{ia},{sector},{name}"
        return self.run(command, **kwargs)

    def resp(
        self,
        ir: str = "",
        lftab: str = "",
        ldtab: str = "",
        spectype: int | str = "",
        dampratio: str = "",
        dtime: str = "",
        tmin: str = "",
        tmax: str = "",
        inputtype: int | str = "",
        **kwargs,
    ):
        r"""Generates a response spectrum.

        Mechanical APDL Command: `RESP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RESP.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the response spectrum results (2 to NV ( :ref:`numvar`
            )). If this number is the same as for a previously defined variable, the previously defined
            variable will be overwritten with these results.

        lftab : str
            Reference number of variable containing frequency table (created with :ref:`filldata` or
            :ref:`data` command). The frequency table defines the number and frequency of oscillating
            systems used to determine the response spectrum. The frequency interval need not be constant
            over the entire range. Frequencies must be input in ascending order.

        ldtab : str
            Reference number of variable containing the input time-history.

        spectype : int or str
            Defines the type of response spectrum to be calculated:

            * ``0 or 1`` - Displacement (relative to base excitation)

            * ``2`` - Velocity (relative to base excitation)

            * ``3`` - Acceleration response spectrum (absolute)

            * ``4`` - Pseudo-velocity

            * ``5`` - Pseudo-acceleration

        dampratio : str
            Ratio of viscous damping to critical damping (input as a decimal number).

        dtime : str
            Integration time step. This value should be equal to or greater than the integration time step
            used in the initial transient analysis performed to generate the input time-history ( ``LDTAB``
            ).

            ``DTIME`` defaults to a value of 1/(20\*FMAX), where FMAX is the highest frequency in the
            frequency table ( ``LFTAB`` ) except when the time-history is read from the reduced displacement
            ( :file:`RDSP` ) file following a mode-superposition transient analysis without an expansion
            pass. In this case, ``DTIME`` defaults to the time step value used in the analysis.

        tmin : str
            Specifies a subset of the input time-history ( ``LDTAB`` ) to be used in the response spectrum
            calculation. Defaults to the full time range.

        tmax : str
            Specifies a subset of the input time-history ( ``LDTAB`` ) to be used in the response spectrum
            calculation. Defaults to the full time range.

        inputtype : int or str
            Defines the type of the input time-history:

            * ``0`` - Displacement (default)

            * ``1`` - Acceleration

        Notes
        -----

        .. _RESP_notes:

        This command generates a response spectrum from a displacement or acceleration time-history and
        frequency data. The response spectrum is defined as the maximum response of single degree of freedom
        systems of varying frequency (or period) to a given input support excitation.

        A response spectrum analysis ( :ref:`antype`, SPECTR with :ref:`spopt`, SPRS or MPRS) requires a
        response spectrum input. This input can be determined from the response spectrum printout or display
        of this command.

        If a response spectrum is to be calculated from a given displacement (or acceleration) time-history,
        the displacement time-history may be input to a single one-element reduced linear transient dynamic
        ( :ref:`antype`,TRANS) analysis, so that the calculated output (which should be the same as the
        input) will be properly located on the file.

        The integration time step (argument ``DTIME`` on the :ref:`resp` command) and the damping
        coefficient (argument ``dampRatio`` ) are constant over the frequency range. The number of
        calculations done per response spectrum curve is the product of the number of input solution points
        ( ``TMAX`` - ``TMIN`` )/ ``DTIME`` and the number of frequency points (frequencies located in
        variable ``LFTAB`` ).

        Input solution points requested (using ``DTIME`` and the frequency range) at a time not
        corresponding to an actual displacement solution time on the file are linearly interpolated with
        respect to the existing points.

        For the theory of the response spectrum calculation, see `POST26 - Response Spectrum Generator
        (RESP)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post11.html#postimestep>`_

        For an example of the command usage, see `Generating a Response Spectrum
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BASP26add.html#>`_
        """
        command = f"RESP,{ir},{lftab},{ldtab},{spectype},{dampratio},{dtime},{tmin},{tmax},{inputtype}"
        return self.run(command, **kwargs)

    def rpsd(
        self,
        ir: str = "",
        ia: str = "",
        ib: str = "",
        itype: int | str = "",
        datum: int | str = "",
        name: str = "",
        signif: str = "",
        **kwargs,
    ):
        r"""Calculates response power spectral density (PSD).

        Mechanical APDL Command: `RPSD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RPSD.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to ``NV`` ( :ref:`numvar` )).
            If this number is the same as for a previous variable, the previous variable will be overwritten
            with this result.

        ia : str
            Reference numbers of the two variables to be operated on. If only one, leave ``IB`` blank.

        ib : str
            Reference numbers of the two variables to be operated on. If only one, leave ``IB`` blank.

        itype : int or str
            Defines the type of response PSD to be calculated:

            * ``0,1`` - Displacement (default).

            * ``2`` - Velocity.

            * ``3`` - Acceleration.

        datum : int or str
            Defines the reference with respect to which response PSD is to be calculated:

            * ``1`` - Absolute value.

            * ``2`` - Relative to base (default).

        name : str
            Thirty-two character name identifying variable on listings and displays. Embedded blanks are
            compressed for output.

        signif : str
            Combine only those modes whose significance level exceeds the ``SIGNIF`` threshold. The
            significance level is defined as the modal covariance matrix term divided by the maximum of all
            the modal covariance matrix terms. Any term whose significance level is less than ``SIGNIF`` is
            considered insignificant and does not contribute to the response. All modes are taken into
            account by default ( ``SIGNIF`` = 0.0).

            The significance level definition is identical to the one used for the combination ( ``SIGNIF``
            on the :ref:`psdcom` command); however, the default value is different.

            The significance does not apply to spatial correlation ( :ref:`psdspl` ) and wave propagation (
            :ref:`psdwav` ) response power spectral density.

        Notes
        -----

        .. _RPSD_notes:

        This command calculates response power spectral density (PSD) for the variables referenced by the
        reference numbers ``IA`` and ``IB``. The variable referred by ``IR`` will contain the response PSD.
        You must issue the :ref:`store`,PSD command first; :file:`File.PSD` must be available for the
        calculations to occur.

        See `POST26 - Response Power Spectral Density
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post13.html#eqe670f2a2-bc13-4785-aee1-0d74b8bb8922>`_
        in the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_ for more
        information on these equations.
        """
        command = f"RPSD,{ir},{ia},{ib},{itype},{datum},{name},,{signif}"
        return self.run(command, **kwargs)

    def smooth(
        self,
        vect1: str = "",
        vect2: str = "",
        datap: str = "",
        fitpt: int | str = "",
        vect3: str = "",
        vect4: str = "",
        disp: int | str = "",
        **kwargs,
    ):
        r"""Allows smoothing of noisy data and provides a graphical representation of the data.

        Mechanical APDL Command: `SMOOTH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SMOOTH.html>`_

        Parameters
        ----------
        vect1 : str
            Name of the first vector that contains the noisy data set (that is, independent variable). You
            must create and fill this vector before issuing :ref:`smooth`.

        vect2 : str
            Name of the second vector that contains the dependent set of data. Must be the same length as
            the first vector. You must create and fill this vector before issuing :ref:`smooth`.

        datap : str
            Number of data points to be fitted, starting from the beginning of the vector. If left blank,
            the entire vector will be fitted. The maximum number of data points is 100,000 (or greater,
            depending on the memory of the computer).

        fitpt : int or str
            Order of the fitting curve that will be used as a smooth representation of the data. This number
            should be less than or equal to the number of the data points. Default (blank) is one-half the
            number of data points. Maximum number of smoothed data fitting order is the number of data points up
            to 50. Depending on this number, the smoothed curve will be one of the following:

            * ``1`` - Curve is the absolute average of all of the data points.

            * ``2`` - Curve is the least square average of all of the data points.

            * ``3 or more`` - Curve is a polynomial of the order (n-1), where n is the number of data fitting
              order points.

        vect3 : str
            Name of the vector that contains the smoothed data of the independent variable. This vector
            should have a length equal to or greater than the number of smoothed data points. In batch
            (command) mode, you must create this vector before issuing the :ref:`smooth` command. In
            interactive mode, the GUI automatically creates this vector (if it does not exist). If you do
            not specify a vector name, the GUI will name the vector smth_ind.

        vect4 : str
            Name of the vector that contains the smoothed data of the dependent variable. This vector must
            be the same length as ``Vect3``. In batch (command) mode, you must create this vector before
            issuing the :ref:`smooth` command. In interactive mode, the GUI automatically creates this
            vector (if it does not exist). If you do not specify a vector name, the GUI will name the vector
            smth_dep.

        disp : int or str
            Specifies how you want to display data. No default; you must specify an option.

            * ``1`` - Unsmoothed data only

            * ``2`` - Smoothed data only

            * ``3`` - Both smoothed and unsmoothed data

        Notes
        -----

        .. _SMOOTH_notes:

        This command enables you to control the attributes of the graph using standard Mechanical APDL
        controls (
        :ref:`grid`, :ref:`gthk`, :ref:`color`, etc.).

        If working interactively, the controls appear in this dialog box for convenience, as well as in
        their standard dialog boxes.

        You must always create ``Vect1`` and ``Vect2`` (using :ref:`dim` ) and fill these vectors before
        smoothing the data. If working interactively, the program automatically creates ``Vect3`` and
        ``Vect4``. If working in batch (command) mode, you must create ``Vect3`` and ``Vect4`` (using
        :ref:`dim` ) before issuing :ref:`smooth`. ``Vect3`` and ``Vect4`` are then filled automatically by
        the program.

        The program also creates an additional TABLE type array that contains the smoothed array and the
        unsmoothed data to enable plotting later with :ref:`starvplot`. Column 1 in the table corresponds
        to ``Vect1``, column 2 to ``Vect2``, and column 3 to ``Vect4``. The array is named ``Vect3``
        _SMOOTH, up to a limit of 32 characters. For example, if the array name is X1, the table name is
        X1_SMOOTH.

        This command is also valid in PREP7 and SOLUTION.
        """
        command = f"SMOOTH,{vect1},{vect2},{datap},{fitpt},{vect3},{vect4},{disp}"
        return self.run(command, **kwargs)

    def vget(
        self,
        par: str = "",
        ir: str = "",
        tstrt: str = "",
        kcplx: int | str = "",
        **kwargs,
    ):
        r"""Moves a variable into an array parameter vector.

        Mechanical APDL Command: `VGET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VGET.html>`_

        Parameters
        ----------
        par : str
            Array parameter vector in the operation.

        ir : str
            Reference number of the variable (1 to NV ( :ref:`numvar` )).

        tstrt : str
            Time (or frequency) corresponding to start of ``IR`` data. If between values, the nearer value
            is used.

        kcplx : int or str
            Complex number key:

            * ``0`` - Use the real part of the ``IR`` data.

            * ``1`` - Use the imaginary part of the ``IR`` data.

        Notes
        -----

        .. _VGET_notes:

        Moves a variable into an array parameter vector. The starting array element number must be defined.
        For example, :ref:`vget`,A(1),2 moves variable 2 (starting at time 0.0) to array parameter A.
        Looping continues from array element A(1) with the index number incremented by one until the
        variable is filled. The number of loops may be controlled with the `\*VLEN
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_VLEN.html#>`_  :ref:`vlen`
        command (except that loop skipping ( ``NINC`` ) is not allowed). For multi-dimensioned array
        parameters, only the first (row) subscript is incremented.
        """
        command = f"VGET,{par},{ir},{tstrt},{kcplx}"
        return self.run(command, **kwargs)

    def vput(
        self,
        par: str = "",
        ir: str = "",
        tstrt: str = "",
        kcplx: int | str = "",
        name: str = "",
        **kwargs,
    ):
        r"""Moves an array parameter vector into a variable.

        Mechanical APDL Command: `VPUT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VPUT.html>`_

        Parameters
        ----------
        par : str
            Array parameter vector in the operation.

        ir : str
            Arbitrary reference number assigned to this variable (1 to ``NV``   ( :ref:`numvar` )).
            Overwrites any existing results for this variable.

        tstrt : str
            Time (or frequency) corresponding to start of ``IR`` data. If between values, the nearer value
            is used.

        kcplx : int or str
            Complex number key:

            * ``0`` - Use the real part of the ``IR`` data.

            * ``1`` - Use the imaginary part of the ``IR`` data.

        name : str
            Thirty-two character name identifying the item on printouts and displays. Defaults to the label
            formed by concatenating VPUT with the reference number ``IR``.

        Notes
        -----

        .. _VPUT_notes:

        At least one variable should be defined ( :ref:`nsol`, :ref:`esol`, :ref:`rforce`, etc.) before
        using this command. The starting array element number must be defined. For example,
        :ref:`vput`,A(1),2 moves array parameter A to variable 2 starting at time 0.0. Looping continues
        from array element A(1) with the index number incremented by one until the variable is filled.
        Unfilled variable locations are assigned a zero value. The number of loops may be controlled with
        the :ref:`vlen` command (except that loop skipping (NINC) is not allowed). For multi-dimensioned
        array parameters, only the first (row) subscript is incremented.
        """
        command = f"VPUT,{par},{ir},{tstrt},{kcplx},{name}"
        return self.run(command, **kwargs)
