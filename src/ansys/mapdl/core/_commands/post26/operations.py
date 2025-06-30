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


class Operations:

    def abs(
        self, ir: str = "", ia: str = "", name: str = "", facta: str = "", **kwargs
    ):
        r"""Forms the absolute value of a variable.

        Mechanical APDL Command: `ABS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ABS.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to NV ( :ref:`numvar` )). If
            this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference number of the variable to be operated on.

        name : str
            Thirty-two character name for identifying the variable on the printout and displays. Embedded
            blanks are compressed upon output.

        facta : str
            Scaling factor (positive or negative) applied to variable ``IA`` (defaults to 1.0).

        Notes
        -----

        .. _ABS_notes:

        The new variable is calculated as:

        IR = \| FACTA x IA \|

        For a complex number (a + i b), the absolute value is the magnitude, where the ``IA`` values are
        obtained from:

        .. math::

            equation not available

        See `POST26 - Data Operations
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post10.html#eqbe42048a-448b-4de9-91a9-1c8007937622>`_
         in the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_ for details.
        """
        command = f"ABS,{ir},{ia},,,{name},,,{facta}"
        return self.run(command, **kwargs)

    def add(
        self,
        ir: str = "",
        ia: str = "",
        ib: str = "",
        ic: str = "",
        name: str = "",
        facta: str = "",
        factb: str = "",
        factc: str = "",
        **kwargs,
    ):
        r"""Adds (sums) variables.

        Mechanical APDL Command: `ADD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ADD.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to NV ( :ref:`numvar` )). If
            this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference numbers of the three variables to be operated on. If only two variables, leave ``IC``
            blank. If only one, leave ``IB`` and ``IC`` blank.

        ib : str
            Reference numbers of the three variables to be operated on. If only two variables, leave ``IC``
            blank. If only one, leave ``IB`` and ``IC`` blank.

        ic : str
            Reference numbers of the three variables to be operated on. If only two variables, leave ``IC``
            blank. If only one, leave ``IB`` and ``IC`` blank.

        name : str
            Thirty-two character name for identifying the variable on the printout and displays. Embedded
            blanks are compressed upon output.

        facta : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        factb : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        factc : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        Notes
        -----

        .. _ADD_notes:

        Adds variables (up to three at once) according to the operation:

        ``IR`` = ( ``FACTA`` x ``IA`` ) + ( ``FACTB`` x ``IB`` ) + ( ``FACTC`` x ``IC`` )

        """
        command = f"ADD,{ir},{ia},{ib},{ic},{name},,,{facta},{factb},{factc}"
        return self.run(command, **kwargs)

    def atan(
        self, ir: str = "", ia: str = "", name: str = "", facta: str = "", **kwargs
    ):
        r"""Forms the arctangent of a complex variable.

        Mechanical APDL Command: `ATAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ATAN.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to ``NV`` ( :ref:`numvar` )).
            If this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference number of the complex variable to be operated on.

        name : str
            Thirty-two character name for identifying the variable on the printout and displays. Embedded
            blanks are compressed upon output.

        facta : str
            Scaling factor (positive or negative) applied to variable ``IA`` (defaults to 1.0). Usually
            ``FACTA`` should be set to 1. ``FACTA`` may affect the position of the angle by a multiple of π,
            resulting in a quadrant change.

        Notes
        -----

        .. _ATAN_notes:

        Forms the arctangent of a complex variable according to the operation:

        ``IR`` = ATAN( ``FACTA`` X b / a )

        where a and b are the real and imaginary parts, respectively, of the complex variable ``IA`` (which
        is of the form a + i  b ). The arctangent represents the phase angle (in radians), and is valid only
        for a harmonic analysis ( :ref:`antype`,HARMIC).

        Since the scaling factor is applied uniformly to b / a, applying any positive or negative scaling
        factor will not affect the size of the phase angle, with the exception that a negative scaling
        factor will change the results quadrant by π. The magnitude of a complex number is still obtained
        through the :ref:`abs` command. See `POST26 - Data Operations
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post10.html#eqbe42048a-448b-4de9-91a9-1c8007937622>`_
         in the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_ for details.
        """
        command = f"ATAN,{ir},{ia},,,{name},,,{facta}"
        return self.run(command, **kwargs)

    def clog(
        self,
        ir: str = "",
        ia: str = "",
        name: str = "",
        facta: str = "",
        factb: str = "",
        **kwargs,
    ):
        r"""Forms the common log of a variable

        Mechanical APDL Command: `CLOG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CLOG.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to NV ( :ref:`numvar` )). If
            this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference number of the variable to be operated on.

        name : str
            Thirty-two character name for identifying the variable on printouts and displays. Embedded
            blanks are compressed for output.

        facta : str
            Scaling factor applied to variable ``IA`` (defaults to 1.0).

        factb : str
            Scaling factor (positive or negative) applied to the operation (defaults to 1.0).

        Notes
        -----

        .. _CLOG_notes:

        Forms the common log of a variable according to the operation:

        ``IR`` = ``FACTB`` \*LOG( ``FACTA`` x ``IA`` )
        """
        command = f"CLOG,{ir},{ia},,,{name},,,{facta},{factb}"
        return self.run(command, **kwargs)

    def conjug(
        self, ir: str = "", ia: str = "", name: str = "", facta: str = "", **kwargs
    ):
        r"""Forms the complex conjugate of a variable.

        Mechanical APDL Command: `CONJUG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CONJUG.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to NV ( :ref:`numvar` )). If
            this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference number of the variable to be operated on.

        name : str
            Thirty-two character name for identifying the variable on printouts and displays. Embedded
            blanks are compressed for output.

        facta : str
            Scaling factor (positive or negative) applied to variable (default to 1.0).

        Notes
        -----

        .. _CONJUG_notes:

        Used only with harmonic analyses ( :ref:`antype`,HARMIC).
        """
        command = f"CONJUG,{ir},{ia},,,{name},,,{facta}"
        return self.run(command, **kwargs)

    def deriv(
        self,
        ir: str = "",
        iy: str = "",
        ix: str = "",
        name: str = "",
        facta: str = "",
        **kwargs,
    ):
        r"""Differentiates a variable.

        Mechanical APDL Command: `DERIV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DERIV.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to NV ( :ref:`numvar` )). If
            this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        iy : str
            Reference numbers of variables to be operated on. ``IY`` is differentiated with respect to
            ``IX``.

        ix : str
            Reference numbers of variables to be operated on. ``IY`` is differentiated with respect to
            ``IX``.

        name : str
            Thirty-two character name for identifying the variable on printouts and displays. Embedded
            blanks are compressed for output.

        facta : str
            Scaling factor (positive or negative) applied as shown below (defaults to 1.0).

        Notes
        -----

        .. _DERIV_notes:

        Differentiates variables according to the operation:

        ``IR`` = ``FACTA`` x d( ``IY`` )/d( ``IX`` )

        Variable ``IX`` must be in ascending order.
        """
        command = f"DERIV,{ir},{iy},{ix},,{name},,,{facta}"
        return self.run(command, **kwargs)

    def exp(
        self,
        ir: str = "",
        ia: str = "",
        name: str = "",
        facta: str = "",
        factb: str = "",
        **kwargs,
    ):
        r"""Forms the exponential of a variable.

        Mechanical APDL Command: `EXP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXP.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to NV ( :ref:`numvar` )). If
            this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference number of the variable to be operated on.

        name : str
            Thirty-two character name for identifying the variable on the printout and displays. Embedded
            blanks are compressed upon output.

        facta : str
            Scaling factor applied to variable ``IA`` (defaults to 1.0).

        factb : str
            Scaling factor (positive or negative) applied to the operation (defaults to 1.0).

        Notes
        -----

        .. _EXP_notes:

        Forms the exponential of a variable according to the operation:

        ``IR`` = ``FACTB`` \*EXP( ``FACTA`` x ``IA`` )

        """
        command = f"EXP,{ir},{ia},,,{name},,,{facta},{factb}"
        return self.run(command, **kwargs)

    def filldata(
        self,
        ir: str = "",
        lstrt: str = "",
        lstop: str = "",
        linc: str = "",
        value: str = "",
        dval: str = "",
        **kwargs,
    ):
        r"""Fills a variable by a ramp function.

        Mechanical APDL Command: `FILLDATA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FILLDATA.html>`_

        Parameters
        ----------
        ir : str
            Define data table as variable ``IR`` (2 to ``NV`` ( :ref:`numvar` )).

        lstrt : str
            Start at location ``LSTRT`` (defaults to 1).

        lstop : str
            Stop at location ``LSTOP`` (defaults to maximum location as determined from data previously
            stored.

        linc : str
            Fill every ``LINC`` location between ``LSTRT`` and ``LSTOP`` (defaults to 1).

        value : str
            Value assigned to location ``LSTRT``.

        dval : str
            Increment value of previous filled location by ``DVAL`` and assign sum to next location to be
            filled (may be positive or negative.)

        Notes
        -----

        .. _FILLDATA_notes:

        Locations may be filled continuously or at regular intervals ( ``LINC`` ). Previously defined data
        at a location will be overwritten.
        """
        command = f"FILLDATA,{ir},{lstrt},{lstop},{linc},{value},{dval}"
        return self.run(command, **kwargs)

    def imagin(
        self, ir: str = "", ia: str = "", name: str = "", facta: str = "", **kwargs
    ):
        r"""Forms an imaginary variable from a complex variable.

        Mechanical APDL Command: `IMAGIN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_IMAGIN.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to ``NV`` ( :ref:`numvar` )).
            If this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference number of the variable to be operated on.

        name : str
            Thirty-two character name for identifying the variable on the printout and displays. Embedded
            blanks are compressed upon output.

        facta : str
            Scaling factor (positive or negative) applied to variable ``IA`` (defaults to 1.0).

        Notes
        -----

        .. _IMAGIN_notes:

        This command forms a new variable from a complex variable by storing the imaginary part as the real
        part. The imaginary part can then be used in other operations. Used only with harmonic analyses (
        :ref:`antype`,HARMIC).

        Complex variables are stored in two-column arrays with the real component stored in the first column
        and the imaginary component stored in the second column. This command extracts the value stored in
        the second column (that is, imaginary component). However, with harmonic analyses, all variables are
        stored in two-column arrays as complex variables. If the variable is not complex, then the same
        value is stored in both columns. This command will extract the variable in the second column of the
        array, even if this variable is not the imaginary component of a complex variable.
        """
        command = f"IMAGIN,{ir},{ia},,,{name},,,{facta}"
        return self.run(command, **kwargs)

    def int1(
        self,
        ir: str = "",
        iy: str = "",
        ix: str = "",
        name: str = "",
        facta: str = "",
        factb: str = "",
        const: str = "",
        **kwargs,
    ):
        r"""Integrates a variable.

        Mechanical APDL Command: `INT1 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_INT1.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to ``NV`` ( :ref:`numvar` )).
            If this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result. Table values represent integrated sum of ``IY`` to current
            table position of ``IX``.

        iy : str
            Integrate variable ``IY`` with respect to ``IX``.

        ix : str
            Integrate variable ``IY`` with respect to ``IX``.

        name : str
            Thirty-two character name for identifying the variable on the printout and displays. Embedded
            blanks are compressed upon output.

        facta : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        factb : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        const : str
            Initial value.

        Notes
        -----

        .. _INT1_notes:

        Integrates variables according to the operation:

        ``IR`` = ∫ ( ``FACTA`` x ``IY`` ) d( ``FACTB`` x ``IX`` ) + ``CONST``

        """
        command = f"INT1,{ir},{iy},{ix},,{name},,,{facta},{factb},{const}"
        return self.run(command, **kwargs)

    def large(
        self,
        ir: str = "",
        ia: str = "",
        ib: str = "",
        ic: str = "",
        name: str = "",
        facta: str = "",
        factb: str = "",
        factc: str = "",
        **kwargs,
    ):
        r"""Finds the largest (the envelope) of three variables.

        Mechanical APDL Command: `LARGE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LARGE.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to ``NV`` ( :ref:`numvar` )).
            If this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference numbers of the three variables to be operated on. If only two, leave ``IC`` blank. If
            only one, leave ``IB`` blank also.

        ib : str
            Reference numbers of the three variables to be operated on. If only two, leave ``IC`` blank. If
            only one, leave ``IB`` blank also.

        ic : str
            Reference numbers of the three variables to be operated on. If only two, leave ``IC`` blank. If
            only one, leave ``IB`` blank also.

        name : str
            Thirty-two character name for identifying the variable on the printout and displays. Embedded
            blanks are compressed upon output.

        facta : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        factb : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        factc : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        Notes
        -----

        .. _LARGE_notes:

        Creates a new variable by finding the largest of up to three variables according to the operation:

        ``IR`` = Largest of ( ``FACTA`` x ``IA``, ``FACTB`` x ``IB``, ``FACTC`` x ``IC`` )

        The comparison is done at each time location, so that the new variable is the "envelope" of the
        three existing variables.
        """
        command = f"LARGE,{ir},{ia},{ib},{ic},{name},,,{facta},{factb},{factc}"
        return self.run(command, **kwargs)

    def nlog(
        self,
        ir: str = "",
        ia: str = "",
        name: str = "",
        facta: str = "",
        factb: str = "",
        **kwargs,
    ):
        r"""Forms the natural log of a variable.

        Mechanical APDL Command: `NLOG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NLOG.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to NV ( :ref:`numvar` )). If
            this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference number of the variable to be operated on.

        name : str
            Thirty-two character name identifying the variable on printouts and displays. Embedded blanks
            are compressed for output.

        facta : str
            Scaling factor applied to variable ``IA`` (defaults to 1.0).

        factb : str
            Scaling factor (positive or negative) applied to the operation (defaults to 1.0).

        Notes
        -----

        .. _NLOG_notes:

        Forms the natural log of a variable according to the operation:

        ``IR`` = ``FACTB`` \*LN( ``FACTA`` x ``IA`` )

        """
        command = f"NLOG,{ir},{ia},,,{name},,,{facta},{factb}"
        return self.run(command, **kwargs)

    def prod(
        self,
        ir: str = "",
        ia: str = "",
        ib: str = "",
        ic: str = "",
        name: str = "",
        facta: str = "",
        factb: str = "",
        factc: str = "",
        **kwargs,
    ):
        r"""Multiplies variables.

        Mechanical APDL Command: `PROD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PROD.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to NV ( :ref:`numvar` )). If
            this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference numbers of the three variables to be operated on. If only two leave ``IC`` blank. If
            only one, leave ``IB`` blank also.

        ib : str
            Reference numbers of the three variables to be operated on. If only two leave ``IC`` blank. If
            only one, leave ``IB`` blank also.

        ic : str
            Reference numbers of the three variables to be operated on. If only two leave ``IC`` blank. If
            only one, leave ``IB`` blank also.

        name : str
            Thirty-two character name identifying the variable on printouts and displays. Embedded blanks
            are compressed for output.

        facta : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        factb : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        factc : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        Notes
        -----

        .. _PROD_notes:

        Multiplies variables (up to three at once) according to the operation:

        ``IR`` = ( ``FACTA`` x ``IA`` ) x ( ``FACTB`` x ``IB`` ) x ( ``FACTC`` x ``IC`` )

        """
        command = f"PROD,{ir},{ia},{ib},{ic},{name},,,{facta},{factb},{factc}"
        return self.run(command, **kwargs)

    def quot(
        self,
        ir: str = "",
        ia: str = "",
        ib: str = "",
        name: str = "",
        facta: str = "",
        factb: str = "",
        **kwargs,
    ):
        r"""Divides two variables.

        Mechanical APDL Command: `QUOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_QUOT.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to ``NV`` ( :ref:`numvar` )).
            If this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference numbers of the two variables to be operated on.

        ib : str
            Reference numbers of the two variables to be operated on.

        name : str
            Thirty-two character name identifying the variable on printouts and displays. Embedded blanks
            are compressed for output.

        facta : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        factb : str
            Scaling factors (positive or negative) applied to the corresponding variables (default to 1.0).

        Notes
        -----

        .. _QUOT_notes:

        Divides two variables according to the operation:

        ``IR`` = ( ``FACTA`` x ``IA`` )/( ``FACTB`` x ``IB`` )

        """
        command = f"QUOT,{ir},{ia},{ib},,{name},,,{facta},{factb}"
        return self.run(command, **kwargs)

    def realvar(
        self, ir: str = "", ia: str = "", name: str = "", facta: str = "", **kwargs
    ):
        r"""Forms a variable using only the real part of a complex variable.

        Mechanical APDL Command: `REALVAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_REALVAR.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to NV ( :ref:`numvar` )). If
            this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference number of the variable to be operated on.

        name : str
            Thirty-two character name identifying the variable on printouts and displays. Embedded blanks
            are compressed for output.

        facta : str
            Scaling factor (positive or negative) applied to variable ``IA`` (defaults to 1.0).

        Notes
        -----

        .. _REALVAR_notes:

        Forms a variable using only the real part of a variable. Used only with harmonic analyses (
        :ref:`antype`,HARMIC).

        Complex variables are stored in two-column arrays with the real component stored in the first column
        and the imaginary component stored in the second column. This command extracts the value stored in
        the first column (that is, real component). However with harmonic analyses, all variables are stored
        in two-column arrays as complex variables. If the variable is not complex, then the same value is
        stored in both columns. This command will extract the variable in the first column of the array,
        even if this variable is not the real component of a complex variable.
        """
        command = f"REALVAR,{ir},{ia},,,{name},,,{facta}"
        return self.run(command, **kwargs)

    def small(
        self,
        ir: str = "",
        ia: str = "",
        ib: str = "",
        ic: str = "",
        name: str = "",
        facta: str = "",
        factb: str = "",
        factc: str = "",
        **kwargs,
    ):
        r"""Finds the smallest of three variables.

        Mechanical APDL Command: `SMALL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SMALL.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to ``NV`` ( :ref:`numvar` )).
            If this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference numbers of the three variables to be operated on. If only two, leave ``IC`` blank. If
            only one, leave ``IB`` blank also.

        ib : str
            Reference numbers of the three variables to be operated on. If only two, leave ``IC`` blank. If
            only one, leave ``IB`` blank also.

        ic : str
            Reference numbers of the three variables to be operated on. If only two, leave ``IC`` blank. If
            only one, leave ``IB`` blank also.

        name : str
            Thirty-two character name identifying the variable on printouts and displays. Embedded blanks
            are compressed for output.

        facta : str
            Scaling factors (positive or negative) applied to the corresponding variables (defaults to 1.0).

        factb : str
            Scaling factors (positive or negative) applied to the corresponding variables (defaults to 1.0).

        factc : str
            Scaling factors (positive or negative) applied to the corresponding variables (defaults to 1.0).

        Notes
        -----

        .. _SMALL_notes:

        Finds the smallest of three variables according to the operation:

        ``IR`` = smallest of ( ``FACTA`` x ``IA``, ``FACTB`` x ``IB``, ``FACTC`` x ``IC`` )

        """
        command = f"SMALL,{ir},{ia},{ib},{ic},{name},,,{facta},{factb},{factc}"
        return self.run(command, **kwargs)

    def sqrt(
        self, ir: str = "", ia: str = "", name: str = "", facta: str = "", **kwargs
    ):
        r"""Forms the square root of a variable.

        Mechanical APDL Command: `SQRT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SQRT.html>`_

        Parameters
        ----------
        ir : str
            Arbitrary reference number assigned to the resulting variable (2 to ``NV`` ( :ref:`numvar` )).
            If this number is the same as for a previously defined variable, the previously defined variable
            will be overwritten with this result.

        ia : str
            Reference number of the variable to be operated on.

        name : str
            Thirty-two character name identifying the variable on printouts and displays. Embedded blanks
            are compressed for output.

        facta : str
            Scaling factor (positive or negative) applied to variable ``IA`` (defaults to 1.0).

        Notes
        -----

        .. _SQRT_notes:

        Forms the square root of a variable according to the operation:

        .. math::

            equation not available
        """
        command = f"SQRT,{ir},{ia},,,{name},,,{facta}"
        return self.run(command, **kwargs)
