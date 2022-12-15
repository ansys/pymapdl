class Operations:
    def abs(self, ir="", ia="", name="", facta="", **kwargs):
        """Forms the absolute value of a variable.

        APDL Command: ABS

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting
            variable (2 to NV [NUMVAR]).  If this number is the same
            as for a previously defined variable, the previously
            defined variable will be overwritten with this result.

        ia
            Reference number of the variable to be operated on.

        name
            Thirty-two character name for identifying the variable on
            the printout and displays.  Embedded blanks are compressed
            upon output.

        facta
            Scaling factor (positive or negative) applied to variable
            IA (defaults to 1.0).

        Notes
        -----
        The new variable is calculated as:

        IR = | FACTA x IA |

        For a complex number (a + ib), the absolute value is the
        magnitude, where the IA values are obtained from:
        ``sqrt(a**2 + b**2)``

        See POST26 - Data Operations in the Mechanical APDL Theory
        Reference for details.
        """
        return self.run(f"ABS,{ir},{ia},,,{name},,,{facta}", **kwargs)

    def add(
        self,
        ir="",
        ia="",
        ib="",
        ic="",
        name="",
        facta="",
        factb="",
        factc="",
        **kwargs,
    ):
        """Adds (sums) variables.

        APDL Command: ADD

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]).  If this number is the same as for a previously
            defined variable, the previously defined variable will be
            overwritten with this result.

        ia, ib, ic
            Reference numbers of the three variables to be operated on.  If
            only two variables, leave IC blank.  If only one, leave IB and IC
            blank.

        name
            Thirty-two character name for identifying the variable on the
            printout and displays.  Embedded blanks are compressed upon output.

        facta, factb, factc
            Scaling factors (positive or negative) applied to the corresponding
            variables (default to 1.0).

        Notes
        -----
        Adds variables (up to three at once) according to the operation:

        IR = (FACTA x IA) + (FACTB x IB) + (FACTC x IC)
        """
        command = f"ADD,{ir},{ia},{ib},{ic},{name},,,{facta},{factb},{factc}"
        return self.run(command, **kwargs)

    def atan(self, ir="", ia="", name="", facta="", **kwargs):
        """Forms the arctangent of a complex variable.

        APDL Command: ATAN

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]).  If this number is the same as for a previously
            defined variable, the previously defined variable will be
            overwritten with this result.

        ia
            Reference number of the complex variable to be operated on.

        name
            Thirty-two character name for identifying the variable on the
            printout and displays.  Embedded blanks are compressed upon output.

        facta
            Scaling factor (positive or negative) applied to variable
            IA (defaults to 1.0).  Usually FACTA should be set to 1.
            FACTA may affect the position of the angle by a multiple
            of π, resulting in a quadrant change.

        Notes
        -----
        Forms the arctangent of a complex variable according to the
        operation:

        IR = ATAN(FACTA X b/a)

        where a and b are the real and imaginary parts, respectively,
        of the complex variable IA (which is of the form a + ib).  The
        arctangent represents the phase angle (in radians), and is
        valid only for a harmonic analysis (ANTYPE,HARMIC).

        Since the scaling factor is applied uniformly to b/a, applying
        any positive or negative scaling factor will not affect the
        size of the phase angle, with the exception that a negative
        scaling factor will change the results quadrant by : π.  The
        magnitude of a complex number is still obtained through the
        ABS command.  See POST26 - Data Operations in the Mechanical
        APDL Theory Reference for details.
        """
        command = f"ATAN,{ir},{ia},,,{name},,,{facta}"
        return self.run(command, **kwargs)

    def clog(self, ir="", ia="", name="", facta="", factb="", **kwargs):
        """Forms the common log of a variable

        APDL Command: CLOG

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting
            variable (2 to NV [NUMVAR]).  If this number is the same
            as for a previously defined variable, the previously
            defined variable will be overwritten with this result.

        ia
            Reference number of the variable to be operated on.

        name
            Thirty-two character name for identifying the variable on
            printouts and displays.  Embedded blanks are compressed
            for output.

        facta
            Scaling factor applied to variable IA (defaults to 1.0).

        factb
            Scaling factor (positive or negative) applied to the operation
            (defaults to 1.0).

        Notes
        -----
        Forms the common log of a variable according to the operation:

        ``IR = FACTB*LOG(FACTA x IA)``
        """
        return self.run(f"CLOG,{ir},{ia},,,{name},,,{facta},{factb}", **kwargs)

    def conjug(self, ir="", ia="", name="", facta="", **kwargs):
        """Forms the complex conjugate of a variable.

        APDL Command: CONJUG

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]).  If this number is the same as for a previously
            defined variable, the previously defined variable will be
            overwritten with this result.

        ia
            Reference number of the variable to be operated on.

        name
            Thirty-two character name for identifying the variable on printouts
            and displays.  Embedded blanks are compressed for output.

        facta
            Scaling factor (positive or negative) applied to variable (default
            to 1.0).

        Notes
        -----
        Used only with harmonic analyses (ANTYPE,HARMIC).
        """
        return self.run(f"CONJUG,{ir},{ia},,,{name},,,{facta}", **kwargs)

    def deriv(self, ir="", iy="", ix="", name="", facta="", **kwargs):
        """Differentiates a variable.

        APDL Command: DERIV

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting
            variable (2 to NV [NUMVAR]).  If this number is the same
            as for a previously defined variable, the previously
            defined variable will be overwritten with this result.

        iy, ix
            Reference numbers of variables to be operated on.  IY is
            differentiated with respect to IX.

        name
            Thirty-two character name for identifying the variable on
            printouts and displays. Embedded blanks are compressed for
            output.

        facta
            Scaling factor (positive or negative) applied as shown
            below (defaults to 1.0).

        Notes
        -----
        Differentiates variables according to the operation:

        IR = FACTA x d(IY)/d(IX)
        """
        return self.run(f"DERIV,{ir},{iy},{ix},,{name},,,{facta}", **kwargs)

    def exp(self, ir="", ia="", name="", facta="", factb="", **kwargs):
        """Forms the exponential of a variable.

        APDL Command: EXP

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting
            variable (2 to NV [NUMVAR]). If this number is the same as
            for a previously defined variable, the previously defined
            variable will be overwritten with this result.

        ia
            Reference number of the variable to be operated on.

        name
            Thirty-two character name for identifying the variable on
            the printout and displays. Embedded blanks are compressed
            upon output.

        facta
            Scaling factor applied to variable IA (defaults to 1.0).

        factb
            Scaling factor (positive or negative) applied to the operation
            (defaults to 1.0).

        Notes
        -----
        Forms the exponential of a variable according to the operation:

        ``IR = FACTB*EXP(FACTA x IA)``
        """
        return self.run(f"EXP,{ir},{ia},,,{name},,,{facta},{factb}", **kwargs)

    def filldata(self, ir="", lstrt="", lstop="", linc="", value="", dval="", **kwargs):
        """Fills a variable by a ramp function.

        APDL Command: FILLDATA

        Parameters
        ----------
        ir
            Define data table as variable IR (2 to NV [NUMVAR]).

        lstrt
            Start at location LSTRT (defaults to 1).

        lstop
            Stop at location LSTOP (defaults to maximum location as determined
            from data previously stored.

        linc
            Fill every LINC location between LSTRT and LSTOP (defaults to 1).

        value
            Value assigned to location LSTRT.

        dval
            Increment value of previous filled location by DVAL and assign sum
            to next location to be filled (may be positive or negative.)

        Notes
        -----
        Locations may be filled continuously or at regular intervals (LINC).
        Previously defined data at a location will be overwritten.
        """
        command = f"FILLDATA,{ir},{lstrt},{lstop},{linc},{value},{dval}"
        return self.run(command, **kwargs)

    def imagin(self, ir="", ia="", name="", facta="", **kwargs):
        """Forms an imaginary variable from a complex variable.

        APDL Command: IMAGIN

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting
            variable (2 to NV [NUMVAR]).  If this number is the same
            as for a previously defined variable, the previously
            defined variable will be overwritten with this result.

        ia
            Reference number of the variable to be operated on.

        name
            Thirty-two character name for identifying the variable on
            the printout and displays.  Embedded blanks are compressed
            upon output.

        facta
            Scaling factor (positive or negative) applied to variable IA
            (defaults to 1.0).

        Notes
        -----
        This command forms a new variable from a complex variable by
        storing the imaginary part as the real part.  The imaginary
        part can then be used in other operations.  Used only with
        harmonic analyses (ANTYPE,HARMIC).

        Complex variables are stored in two-column arrays with the
        real component stored in the first column and the imaginary
        component stored in the second column.  This command extracts
        the value stored in the second column (i.e., imaginary
        component).  However, with harmonic analyses, all variables
        are stored in two-column arrays as complex variables.  If the
        variable is not complex, then the same value is stored in both
        columns.  This command will extract the variable in the second
        column of the array, even if this variable is not the
        imaginary component of a complex variable.
        """
        return self.run(f"IMAGIN,{ir},{ia},,,{name},,,{facta}", **kwargs)

    def int1(
        self,
        ir="",
        iy="",
        ix="",
        name="",
        facta="",
        factb="",
        const="",
        **kwargs,
    ):
        """Integrates a variable.

        APDL Command: INT1

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting
            variable (2 to NV [NUMVAR]).  If this number is the same
            as for a previously defined variable, the previously
            defined variable will be overwritten with this result.
            Table values represent integrated sum of IY to current
            table position of IX.

        iy, ix
            Integrate variable IY with respect to IX.

        name
            Thirty-two character name for identifying the variable on
            the printout and displays.  Embedded blanks are compressed
            upon output.

        facta, factb
            Scaling factors (positive or negative) applied to the
            corresponding variables (default to 1.0).

        const
            Initial value.

        Notes
        -----
        Integrates variables according to the operation:

        IR = ∫ (FACTA x IY) d(FACTB x IX) + CONST
        """
        command = f"INT1,{ir},{iy},{ix},,{name},,,{facta},{factb},{const}"
        return self.run(command, **kwargs)

    def large(
        self,
        ir="",
        ia="",
        ib="",
        ic="",
        name="",
        facta="",
        factb="",
        factc="",
        **kwargs,
    ):
        """Finds the largest (the envelope) of three variables.

        APDL Command: LARGE

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]).  If this number is the same as for a previously
            defined variable, the previously defined variable will be
            overwritten with this result.

        ia, ib, ic
            Reference numbers of the three variables to be operated on.  If
            only two, leave IC blank.  If only one, leave IB blank also.

        name
            Thirty-two character name for identifying the variable on the
            printout and displays.  Embedded blanks are compressed upon output.

        facta, factb, factc
            Scaling factors (positive or negative) applied to the corresponding
            variables (default to 1.0).

        Notes
        -----
        Creates a new variable by finding the largest of up to three variables
        according to the operation:

        IR = Largest of (FACTA x IA, FACTB x IB, FACTC x IC)

        The comparison is done at each time location, so that the new variable
        is the "envelope" of the three existing variables.
        """
        command = f"LARGE,{ir},{ia},{ib},{ic},{name},,,{facta},{factb},{factc}"
        return self.run(command, **kwargs)

    def nlog(self, ir="", ia="", name="", facta="", factb="", **kwargs):
        """Forms the natural log of a variable.

        APDL Command: NLOG

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting
            variable (2 to NV [NUMVAR]).  If this number is the same
            as for a previously defined variable, the previously
            defined variable will be overwritten with this result.

        ia
            Reference number of the variable to be operated on.

        name
            Thirty-two character name identifying the variable on
            printouts and displays.  Embedded blanks are compressed
            for output.

        facta
            Scaling factor applied to variable IA (defaults to 1.0).

        factb
            Scaling factor (positive or negative) applied to the operation
            (defaults to 1.0).

        Notes
        -----
        Forms the natural log of a variable according to the operation:

        ``IR = FACTB*LN(FACTA x IA)``
        """
        return self.run(f"NLOG,{ir},{ia},,,{name},,,{facta},{factb}", **kwargs)

    def prod(
        self,
        ir="",
        ia="",
        ib="",
        ic="",
        name="",
        facta="",
        factb="",
        factc="",
        **kwargs,
    ):
        """Multiplies variables.

        APDL Command: PROD

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting
            variable (2 to NV [NUMVAR]).  If this number is the same
            as for a previously defined variable, the previously
            defined variable will be overwritten with this result.

        ia, ib, ic
            Reference numbers of the three variables to be operated
            on.  If only two leave IC blank.  If only one, leave IB
            blank also.

        name
            Thirty-two character name identifying the variable on
            printouts and displays.  Embedded blanks are compressed
            for output.

        facta, factb, factc
            Scaling factors (positive or negative) applied to the
            corresponding variables (default to 1.0).

        Notes
        -----
        Multiplies variables (up to three at once) according to the
        operation:

        ``IR = (FACTA x IA) x (FACTB x IB) x (FACTC x IC)``
        """
        return self.run(
            f"PROD,{ir},{ia},{ib},{ic},{name},,,{facta},{factb},{factc}",
            **kwargs,
        )

    def quot(self, ir="", ia="", ib="", name="", facta="", factb="", **kwargs):
        """Divides two variables.

        APDL Command: QUOT

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]).  If this number is the same as for a previously
            defined variable, the previously defined variable will be
            overwritten with this result.

        ia, ib
            Reference numbers of the two variables to be operated on.

        name
            Thirty-two character name identifying the variable on printouts and
            displays.  Embedded blanks are compressed for output.

        facta, factb
            Scaling factors (positive or negative) applied to the corresponding
            variables (default to 1.0).

        Notes
        -----
        Divides two variables according to the operation:

        IR = (FACTA x IA)/(FACTB x IB)
        """
        return self.run(f"QUOT,{ir},{ia},{ib},,{name},,,{facta},{factb}", **kwargs)

    def realvar(self, ir="", ia="", name="", facta="", **kwargs):
        """Forms a variable using only the real part of a complex variable.

        APDL Command: REALVAR

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]).  If this number is the same as for a previously
            defined variable, the previously defined variable will be
            overwritten with this result.

        ia
            Reference number of the variable to be operated on.

        name
            Thirty-two character name identifying the variable on printouts and
            displays.  Embedded blanks are compressed for output.

        facta
            Scaling factor (positive or negative) applied to variable IA
            (defaults to 1.0).

        Notes
        -----
        Forms a variable using only the real part of a variable.  Used only
        with harmonic analyses (ANTYPE,HARMIC).

        Complex variables are stored in two-column arrays with the
        real component stored in the first column and the imaginary
        component stored in the second column.  This command extracts
        the value stored in the first column (i.e., real component).
        However with harmonic analyses, all variables are stored in
        two-column arrays as complex variables.  If the variable is
        not complex, then the same value is stored in both columns.
        This command will extract the variable in the first column of
        the array, even if this variable is not the real component of
        a complex variable.
        """
        command = f"REALVAR,{ir},{ia},,,{name},,,{facta}"
        return self.run(command, **kwargs)

    def small(
        self,
        ir="",
        ia="",
        ib="",
        ic="",
        name="",
        facta="",
        factb="",
        factc="",
        **kwargs,
    ):
        """Finds the smallest of three variables.

        APDL Command: SMALL

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting
            variable (2 to NV [NUMVAR]).  If this number is the same
            as for a previously defined variable, the previously
            defined variable will be overwritten with this result.

        ia, ib, ic
            Reference numbers of the three variables to be operated
            on.  If only two, leave IC blank.  If only one, leave IB
            blank also.

        name
            Thirty-two character name identifying the variable on
            printouts and displays.  Embedded blanks are compressed
            for output.

        facta, factb, factc
            Scaling factors (positive or negative) applied to the
            corresponding variables (defaults to 1.0).

        Notes
        -----
        Finds the smallest of three variables according to the operation:

        ``IR = min(FACTA x IA, FACTB x IB, FACTC x IC)``
        """
        command = f"SMALL,{ir},{ia},{ib},{ic},{name},,,{facta},{factb},{factc}"
        return self.run(command, **kwargs)

    def sqrt(self, ir="", ia="", name="", facta="", **kwargs):
        """Forms the square root of a variable.

        APDL Command: SQRT

        Parameters
        ----------
        ir
            Arbitrary reference number assigned to the resulting variable (2 to
            NV [NUMVAR]).  If this number is the same as for a previously
            defined variable, the previously defined variable will be
            overwritten with this result.

        ia
            Reference number of the variable to be operated on.

        name
            Thirty-two character name identifying the variable on printouts and
            displays.  Embedded blanks are compressed for output.

        facta
            Scaling factor (positive or negative) applied to variable IA
            (defaults to 1.0).

        Notes
        -----
        Forms the square root of a variable according to the operation:
        ``IR=sqrt(FACTA*IA)``
        """
        return self.run(f"SQRT,{ir},{ia},,,{name},,,{facta}", **kwargs)
