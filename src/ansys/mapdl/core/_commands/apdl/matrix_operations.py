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


class MatrixOperations:

    def axpy(
        self,
        vr: str = "",
        vi: str = "",
        m1: str = "",
        wr: str = "",
        wi: str = "",
        m2: str = "",
        **kwargs,
    ):
        r"""Performs the matrix operation M2= v\2M1 + w\2M2.

        Mechanical APDL Command: `\*AXPY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AXPY.html>`_

        Parameters
        ----------
        vr : str
            The real and imaginary parts of the scalar ``v``. Default value is 0.

        vi : str
            The real and imaginary parts of the scalar ``v``. Default value is 0.

        m1 : str
            Name of matrix ``M1``. If not specified, the operation M2 = w\*M2 will be performed.

        wr : str
            The real and imaginary parts of the scalar ``w``. Default value is 0.

        wi : str
            The real and imaginary parts of the scalar ``w``. Default value is 0.

        m2 : str
            Name of matrix ``M2``. Must be specified.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AXPY.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-AXPY_argdescript:

        * ``vr, vi : str`` - The real and imaginary parts of the scalar ``v``. Default value is 0.

        * ``m1 : str`` - Name of matrix ``M1``. If not specified, the operation M2 = w\*M2 will be
          performed.

        * ``wr, wi : str`` - The real and imaginary parts of the scalar ``w``. Default value is 0.

        * ``m2 : str`` - Name of matrix ``M2``. Must be specified.

        .. _a-AXPY_notes:

        The matrices ``M1`` and ``M2`` must have the same dimensions and same type (dense or sparse). If
        ``M2`` is real, ``vi`` and ``wi`` are ignored.
        """
        command = f"*AXPY,{vr},{vi},{m1},{wr},{wi},{m2}"
        return self.run(command, **kwargs)

    def comp(
        self,
        matrix: str = "",
        algorithm: str = "",
        threshold: str = "",
        val1: str = "",
        val2: str = "",
        **kwargs,
    ):
        r"""Compresses a matrix using a specified algorithm.

        Mechanical APDL Command: `\*COMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_COMP.html>`_

        Parameters
        ----------
        matrix : str
            Name of the matrix to compress.

        algorithm : str
            Algorithm or method to use:

            * ``SVD`` - Singular value decomposition algorithm (default).

            * ``MGS`` - Modified Gram-Schmidt algorithm.

            * ``SPARSE`` - Compress a sparse matrix based on the threshold value.

        threshold : str
            Numerical threshold value used to manage the compression. The default value depends on the
            method of compression: 1E-7 for SVD; 1E-14 for MGS; 1E-16 for SPARSE.

        val1 : str
            Name of the vector used to store the :math:`equation not available`  values (see
            :ref:`a-COMP_notes` below). This argument is optional.

        val2 : str
            Name of the dense matrix used to store the :math:`equation not available`  output matrix (see
            :ref:`a-COMP_notes` below). This argument is optional.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_COMP.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-COMP_argdescript:

        * ``matrix : str`` - Name of the matrix to compress.

        * ``algorithm : str`` - Algorithm or method to use:

          * ``SVD`` - Singular value decomposition algorithm (default).

          * ``MGS`` - Modified Gram-Schmidt algorithm.

          * ``SPARSE`` - Compress a sparse matrix based on the threshold value.

        * ``threshold : str`` - Numerical threshold value used to manage the compression. The default value
          depends on the method of compression: 1E-7 for SVD; 1E-14 for MGS; 1E-16 for SPARSE.

        ``Val1`` and ``Val2`` are additional input used only for the SVD algorithm:

        * ``val1 : str`` - Name of the vector used to store the :math:`equation not available`  values (see
          :ref:`a-COMP_notes` below). This argument is optional.

        * ``val2 : str`` - Name of the dense matrix used to store the :math:`equation not available`  output
          matrix (see :ref:`a-COMP_notes` below). This argument is optional.

        .. _a-COMP_notes:

        The SVD and MGS algorithms are only applicable to dense matrices that were created using the
        :ref:`dmat` command. Columns that are linearly dependent on others are removed, leaving the
        independent or basis vectors. The matrix is resized according to the new size determined by the
        algorithm.

        For the SVD algorithm, the singular value decomposition of an input matrix :math:`equation not
        available`  is a factorization of the form:

        .. math::

            equation not available

        Here, the :math:`equation not available`  matrix is replaced by the  :math:`equation not available`
        matrix, according to the specified threshold.

        The SPARSE compression method is only applicable to sparse matrices that were created using the
        :ref:`smat` command. All terms that have an absolute value below the specified threshold, relative
        to the maximum value in the matrix, are removed from the original matrix. For example, given a
        sparse matrix having 100 as the largest term and ``THRESHOLD`` = 0.5, all terms having an absolute
        value below 0.5\*100 = 50 are removed.
        """
        command = f"*COMP,{matrix},{algorithm},{threshold},{val1},{val2}"
        return self.run(command, **kwargs)

    def dmat(
        self,
        matrix: str = "",
        type_: str = "",
        method: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        **kwargs,
    ):
        r"""Creates a dense matrix.

        Mechanical APDL Command: `\*DMAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DMAT.html>`_

        Parameters
        ----------
        matrix : str
            Name used to identify the matrix. Must be specified.

        type_ : str
            Matrix type:

            * ``D`` - Double precision real values (default).

            * ``Z`` - Complex double precision values.

            * ``I`` - Integer values.

        method : str
            Method used to create the matrix:

            * ``ALLOC`` - Allocate space for a matrix (default).

            * ``RESIZE`` - Resize an existing matrix to new row and column dimensions. Values are kept from the
              original matrix. If the dimensions specified by ``Val1`` (rows) and ``Val2`` (columns) are greater
              than the original matrix size, the additional entries are assigned a value of zero.

            * ``COPY`` - Copy an existing matrix.

            * ``LINK`` - Link to an existing matrix. The memory will be shared between the original matrix and
              the new matrix. This is useful for manipulating a submatrix of a larger matrix. The ``Val1`` through
              ``Val5`` arguments will be used to specify the lower and upper bounds of row and column numbers from
              the original matrix.

            * ``IMPORT`` - Import the matrix from a file.

        val1 : str
            Name of the original matrix.

        val2 : str
            First column number (defaults to 1).

        val3 : str
            Last column number (defaults to the maximum column number of the original matrix).

        val4 : str
            First row number (defaults to 1).

        val5 : str
            Last row number (defaults to the maximum row number of the original matrix).

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DMAT.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-DMAT_argdescript:

        * ``matrix : str`` - Name used to identify the matrix. Must be specified.

        * ``type_ : str`` - Matrix type:

          * ``D`` - Double precision real values (default).

          * ``Z`` - Complex double precision values.

          * ``I`` - Integer values.

        * ``method : str`` - Method used to create the matrix:

          * ``ALLOC`` - Allocate space for a matrix (default).

          * ``RESIZE`` - Resize an existing matrix to new row and column dimensions. Values are kept from the
            original matrix. If the dimensions specified by ``Val1`` (rows) and ``Val2`` (columns) are greater
            than the original matrix size, the additional entries are assigned a value of zero.

          * ``COPY`` - Copy an existing matrix.

          * ``LINK`` - Link to an existing matrix. The memory will be shared between the original matrix and
            the new matrix. This is useful for manipulating a submatrix of a larger matrix. The ``Val1`` through
            ``Val5`` arguments will be used to specify the lower and upper bounds of row and column numbers from
            the original matrix.

          * ``IMPORT`` - Import the matrix from a file.

        * ``val1, val2, val3, val4, val5 : str`` - Additional input. The meaning of ``Val1`` through
          ``Val5`` will vary depending on the specified ``Method``. See details below.

        **The following** ``Valx`` fields are used with ``Method`` = ALLOC or ``Method`` = RESIZE:

        * ``val1 : str`` - Number of rows in the matrix.

        * ``val2 : str`` - Number of columns in the matrix.

        * ``val3 : str`` - Memory allocation type (used only with ``Method`` = ALLOC):

          * ``INCORE`` - In-core memory allocation (default).

          * ``OUTOFCORE`` - Out-of-core memory allocation.

        **The following** ``Valx`` fields are used with ``Method`` = COPY:

        * ``val1 : str`` - Name of the matrix to copy.

        * ``val2 : str`` - Method used for copying the matrix:

          * ``TRANS`` - Transpose the original matrix. ``Val3`` and ``Val4`` are ignored.

          * ``REAL`` - Copy the real part to the output matrix. This option only applies when copying a
            complex value matrix to a real value matrix. ``Val3`` and ``Val4`` are ignored.

          * ``IMAG`` - Copy the imaginary part to the output matrix. This option only applies when copying a
            complex value matrix to a real value matrix. ``Val3`` and ``Val4`` are ignored.

          * ``EXTRACT`` - Extract a submatrix based on row and column numbers specified by ``Val3`` and
            ``Val4``.

        * ``val3 : str`` - Name of integer vector ( :ref:`vec` ) containing row numbers. If no vector is
          specified, defaults to all rows.

        * ``val4 : str`` - Name of integer vector ( :ref:`vec` ) containing column numbers. If no vector is
          specified, defaults to all columns.

        **The following** ``Valx`` fields are used with ``Method`` = LINK:

        * ``val1 : str`` - Name of the original matrix.

        * ``val2 : str`` - First column number (defaults to 1).

        * ``val3 : str`` - Last column number (defaults to the maximum column number of the original
          matrix).

        * ``val4 : str`` - First row number (defaults to 1).

        * ``val5 : str`` - Last row number (defaults to the maximum row number of the original matrix).

        **The following table describes the** ``Valx`` fields used with ``Method`` = IMPORT:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _a-DMAT_notes:

        This command allows you to create a dense matrix. To create a sparse matrix, use the :ref:`smat`
        command. :ref:`smat` is recommended for large matrices obtained from the :file:`.FULL` or
        :file:`.HBMAT` file. Refer to the :ref:`hbmat` command documentation for more information about
        :file:`.FULL` file contents.

        Use the :ref:`vec` command to create a vector.

        For very large matrices, use the OUTOFCORE option ( ``Method`` = ALLOC or COPY) to keep some of the
        matrix on disk if there is insufficient memory.

        When importing a dense matrix from a **DMIG** file, you can define the formatting of the file using
        the ``Val3`` and ``Val4`` fields. Here are a few different example of formats:

        * A LARGE field format file (using ``Val3`` = ``LARGE``):

        .. code:: apdl

           ...    DMIG*   KAAX                          21               2    *                     21
          1-2.261491337E+08...

        * A FREE field format file with blank separators (using ``Val4`` = ``S``):

        .. code:: apdl

           ...    DMIG stiff 1 2 1 2 29988.    1 6 149940. 2 2 -29988.    2 6 149940....

        * A FREE field format file with a comma separator (using ``Val4`` = ``,``):

        .. code:: apdl

           ...    DMIG,KF,22321,3,,22321,2,-5.00E+6    DMIG,KF,22320,3,,22320,2,-5.00E+6...

        **Requirement when importing matrices from a Nastran DMIG file:** To ensure that the :file:`.sub`
        file is properly generated from matrices imported from Nastran **DMIG** file, the generalized
        coordinates for a CMS superelement (SPOINTS in Nastran) must appear last (have
        highest ID number).

        **Example Usage**
        `APDL Math Examples
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdlmathex.html#apdlmath_partfact>`_
        """
        command = f"*DMAT,{matrix},{type_},{method},{val1},{val2},{val3},{val4},{val5}"
        return self.run(command, **kwargs)

    def dot(
        self,
        vector1: str = "",
        vector2: str = "",
        par_real: str = "",
        par_imag: str = "",
        conj: str = "",
        **kwargs,
    ):
        r"""Computes the dot (or inner) product of two vectors.

        Mechanical APDL Command: `\*DOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DOT.html>`_

        Parameters
        ----------
        vector1 : str
            Name of first vector; must have been previously specified by a :ref:`vec` command.

        vector2 : str
            Name of second vector; must have been previously specified by a :ref:`vec` command.

        par_real : str
            Parameter name that contains the result.

        par_imag : str
            Parameter name that contains the imaginary part of the result (used only for complex vectors).

        conj : str
            Key to specify use of the conjugate of ``Vector1`` when the vectors are complex:

            * ``TRUE`` - Use the conjugate of ``Vector1`` (default).

            * ``FALSE`` - Do not use the conjugate of ``Vector1``.

        Notes
        -----

        .. _a-DOT_notes:

        If ``Vector1`` and ``Vector2`` are complex, the complex conjugate of ``Vector1`` is used to compute
        the result ( ``Par_Real``, ``Par_Imag`` ). Therefore, **\*DOT** applied to complex vectors performs
        the operation:

        .. math::

            equation not available

        Set ``Conj`` = FALSE if you do not want to use the conjugate of ``Vector1``. In this case, the
        operation is:

        .. math::

            equation not available
        """
        command = f"*DOT,{vector1},{vector2},{par_real},{par_imag},{conj}"
        return self.run(command, **kwargs)

    def eigen(
        self,
        kmatrix: str = "",
        mmatrix: str = "",
        cmatrix: str = "",
        evals: str = "",
        evects: str = "",
        **kwargs,
    ):
        r"""Performs a modal solution with unsymmetric or damping matrices.

        Mechanical APDL Command: `\*EIGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EIGEN.html>`_

        Parameters
        ----------
        kmatrix : str
            Name of the stiffness matrix. May be a real or complex-valued matrix.

        mmatrix : str
            Name of the mass matrix.

        cmatrix : str
            Name of the damping matrix (used only for :ref:`modopt`,DAMP).

        evals : str
            Name of the output eigenvalues vector. It will be an ``m`` -long :ref:`vec` vector of complex
            values, where ``m`` is the number of eigenvalues requested ( :ref:`modopt` ).

        evects : str
            Name of the output eigenvector matrix. It will be a ``n`` x ``m``  :ref:`dmat` (dense) matrix of
            complex values, where ``n`` is the size of the matrix and ``m`` is the number of eigenvalues
            requested ( :ref:`modopt` ).

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EIGEN.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-EIGEN_argdescript:

        * ``kmatrix : str`` - Name of the stiffness matrix. May be a real or complex-valued matrix.

        * ``mmatrix : str`` - Name of the mass matrix.

        * ``cmatrix : str`` - Name of the damping matrix (used only for :ref:`modopt`,DAMP).

        * ``evals : str`` - Name of the output eigenvalues vector. It will be an ``m`` -long :ref:`vec`
          vector of complex values, where ``m`` is the number of eigenvalues requested ( :ref:`modopt` ).

        * ``evects : str`` - Name of the output eigenvector matrix. It will be a ``n`` x ``m``  :ref:`dmat`
          (dense) matrix of complex values, where ``n`` is the size of the matrix and ``m`` is the number of
          eigenvalues requested ( :ref:`modopt` ).

        .. _a-EIGEN_notes:

        Use the command :ref:`antype`,MODAL and the :ref:`modopt` command to specify the modal solution
        options. Only :ref:`modopt` ,DAMP, :ref:`modopt`,UNSYM, :ref:`modopt`,LANB, and
        :ref:`modopt`,SUBSP are supported.

        :ref:`eigen` with Block Lanczos (LANB) only supports sparse matrices. Distributed-Memory Parallel
        (DMP) Restriction This command is not supported in a DMP solution.
        """
        command = f"*EIGEN,{kmatrix},{mmatrix},{cmatrix},{evals},{evects}"
        return self.run(command, **kwargs)

    def export(
        self,
        matrix: str = "",
        format_: str = "",
        fname: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        **kwargs,
    ):
        r"""Exports a matrix to a file in the specified format.

        Mechanical APDL Command: `\*EXPORT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXPORT.html>`_

        Parameters
        ----------
        matrix : str
            Name of the matrix to export (must be a matrix previously created with :ref:`dmat` or
            :ref:`smat`, or a vector previously created with :ref:`vec` ).

        format_ : str
            Format of the output file:

            * ``MMF`` - Export the matrix in the Matrix Market Format.

            * ``SUB`` - Export the matrix in the :file:`SUB` file format.

            * ``HBMAT`` - Export the matrix in the Harwell-Boeing file format.

            * ``MAT`` - Export the matrix in a native format, to be re-imported using the :ref:`dmat` or
              :ref:`smat` command.

            * ``EMAT`` - Export the matrix to an existing :file:`EMAT` file.

            * ``APDL`` - Export the matrix to an APDL array parameter.

            * ``PS`` - Export the matrix profile to a Postscript file.

            * ``DMIG`` - Export the matrix in the :file:`DMIG` file format.

            * ``CSV`` - Export the matrix to an ASCII CSV (comma-separated values) file.

        fname : str
            Name of the file (case-sensitive, 32-character maximum), or name of the array parameter if
            ``Format`` = APDL (no default).

        val1 : str
            Additional input. The meaning of ``Val1`` through ``Val3`` will vary depending on the specified
            ``Format``. See table below for details.

        val2 : str
            Additional input. The meaning of ``Val1`` through ``Val3`` will vary depending on the specified
            ``Format``. See table below for details.

        val3 : str
            Additional input. The meaning of ``Val1`` through ``Val3`` will vary depending on the specified
            ``Format``. See table below for details.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXPORT.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-EXPORT_argdescript:

        * ``matrix : str`` - Name of the matrix to export (must be a matrix previously created with
          :ref:`dmat` or :ref:`smat`, or a vector previously created with :ref:`vec` ).

        * ``format : str`` - Format of the output file:

          * ``MMF`` - Export the matrix in the Matrix Market Format.

          * ``SUB`` - Export the matrix in the :file:`SUB` file format.

          * ``HBMAT`` - Export the matrix in the Harwell-Boeing file format.

          * ``MAT`` - Export the matrix in a native format, to be re-imported using the :ref:`dmat` or
            :ref:`smat` command.

          * ``EMAT`` - Export the matrix to an existing :file:`EMAT` file.

          * ``APDL`` - Export the matrix to an APDL array parameter.

          * ``PS`` - Export the matrix profile to a Postscript file.

          * ``DMIG`` - Export the matrix in the :file:`DMIG` file format.

          * ``CSV`` - Export the matrix to an ASCII CSV (comma-separated values) file.

        * ``fname : str`` - Name of the file (case-sensitive, 32-character maximum), or name of the array
          parameter if ``Format`` = APDL (no default).

        * ``val1, val2, val3 : str`` - Additional input. The meaning of ``Val1`` through ``Val3`` will vary
          depending on the specified ``Format``. See table below for details.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _a-EXPORT_notes:

        Only sparse matrices can be exported to Postscript files. This option plots the matrix profile as a
        series of dots.

        If you want to create a :file:`.SUB` file from several matrices, you need to set ``Val3`` = WAIT for
        all matrices but the last, and ``Val3`` = DONE for the last one. The export will be effective at the
        last :ref:`export` command.

        To create a :file:`.SUB` file or :file:`.DMIG` file from scratch, you must supply the row
        information array. (Specify this array in the ``Val2`` field for :file:`.SUB` or in the ``Val1``
        field for :file:`.DMIG`.) This must be an ``m`` x 2 array, where ``m`` is the size of the matrix.
        The first column is the node number and the second column is the DOF number corresponding to each
        row of the matrix.

        When exporting an HBMAT file in ASCII format, you can include the matrix type in the header of the
        file by specifying the matrix type in the ``Val2`` field. The matrix type is not included in the
        header if ``Val2`` is empty. If ``Val1`` = BINARY, ``Val2`` is not used.

        The :ref:`export` command is not applicable to sparse matrices initialized from :file:`.FULL` files
        by means of the NOD2SOLV option on the :ref:`smat` command (that is,
        :ref:`smat`,,,IMPORT,FULL,,NOD2SOLV).

        The :file:`.CSV` file format does not support sparse matrices.
        """
        command = f"*EXPORT,{matrix},{format_},{fname},{val1},{val2},{val3}"
        return self.run(command, **kwargs)

    def fft(
        self,
        type_: str = "",
        inputdata: str = "",
        outputdata: str = "",
        dim1: str = "",
        dim2: str = "",
        resultformat: str = "",
        **kwargs,
    ):
        r"""Computes the fast Fourier transformation of a specified matrix or vector.

        Mechanical APDL Command: `\*FFT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FFT.html>`_

        Parameters
        ----------
        type_ : str
            Type of FFT transformation:

            * ``FORW`` - Forward FFT computation (default).

            * ``BACK`` - Backward FFT computation.

        inputdata : str
            Name of matrix or vector for which the FFT will be computed. This can be a dense matrix (created
            by the :ref:`dmat` command) or a vector (created by the :ref:`vec` command). Data can be real or
            complex values. There is no default value for this argument.

        outputdata : str
            Name of matrix or vector where the FFT results will be stored. The type of this argument must be
            consistent with ``InputData`` (see table below). There is no default value for this argument.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        dim1 : str
            The number of terms to consider for a vector, or the number of rows for a matrix. Defaults to
            the whole input vector or all the rows of the matrix.

        dim2 : str
            The number of columns to consider for a matrix. Defaults to all the columns of the matrix.
            (Valid only for matrices.)

        resultformat : str
            Specifies the result format:

            * ``FULL`` - Returns the full result. That is, the result matches the dimension specified on this
              command ( ``DIM1``, ``DIM2`` ).

            * ``PART`` - Returns partial results. For real input data, there is a symmetry in the results of the
              Fourier transform as some coefficients are conjugated. The partial format uses this symmetry to
              optimize the storage of the results. (Valid only for real data.)

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FFT.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-FFT_argdescript:

        * ``type_ : str`` - Type of FFT transformation:

          * ``FORW`` - Forward FFT computation (default).

          * ``BACK`` - Backward FFT computation.

        * ``inputdata : str`` - Name of matrix or vector for which the FFT will be computed. This can be a
          dense matrix (created by the :ref:`dmat` command) or a vector (created by the :ref:`vec` command).
          Data can be real or complex values. There is no default value for this argument.

        * ``outputdata : str`` - Name of matrix or vector where the FFT results will be stored. The type of
          this argument must be consistent with ``InputData`` (see table below). There is no default value for
          this argument.

          This command contains some tables and extra information which can be inspected in the original
          documentation pointed above.
        * ``dim1 : str`` - The number of terms to consider for a vector, or the number of rows for a matrix.
          Defaults to the whole input vector or all the rows of the matrix.

        * ``dim2 : str`` - The number of columns to consider for a matrix. Defaults to all the columns of
          the matrix. (Valid only for matrices.)

        * ``resultformat : str`` - Specifies the result format:

          * ``FULL`` - Returns the full result. That is, the result matches the dimension specified on this
            command ( ``DIM1``, ``DIM2`` ).

          * ``PART`` - Returns partial results. For real input data, there is a symmetry in the results of the
            Fourier transform as some coefficients are conjugated. The partial format uses this symmetry to
            optimize the storage of the results. (Valid only for real data.)

        .. _a-FFT_notes:

        In the example that follows, the fast Fourier transformation is used to filter frequencies from a
        noisy input signal.

        **Example Usage**

        .. _a-FFT_example:

        The fast Fourier transformation can be used to create a filter to remove noise from a noisy input
        signal.

        .. figure::../../../images/_commands/gFFT1.PNG

           Input Signal

        The input signal is decomposed in the Fourier space using the :ref:`fft`, ``FORW`` command so that
        the frequencies that compose the signal can be observed.

        .. figure::../../../images/_commands/gFFT2.PNG

           Amplitude Spectrum of the FFT

        The filter applies a threshold on the Fourier coefficients. Fourier coefficients of small amplitude
        are the result of the noise in the input signal. Only coefficients of a large amplitude are
        significant. The inversion of the :ref:`fft` command ( :ref:`fft`, ``BACK`` command) rebuilds the
        signal from the remaining coefficients.

        .. figure::../../../images/_commands/gFFT3.PNG

           Signal Obtained with the Filter

        Example input demonstrating :ref:`fft` usage is provided below:

        .. code:: apdl

           /com,*************************************************
           /com,*  Usage example of the *FFT APDLMath command.  *
           /com,*  Use FFT to filter a noisy sinusoidal signal. *
           /com,*************************************************
           /verify
           /nopr

           /post26

           /gopr
           /com, *** Definition of the parameters for the signal

           pi             = acos(-1)
           periode1       = 2\2pi/40.0
           phase1         = 4.0
           amplitude1     = 2.5
           periode2       = 2\2pi/150.0
           phase2         = 0.0
           amplitude2     = 2.0
           periode3       = 2\2pi/140.0
           phase3         = 0.0
           amplitude3     = 1.5
           amplitudenoise = 6.0
           n              = 400       !number of points in the sampling input signal
           tbegin         = 0.0       !start time for the signal
           dt             = 0.001     !time step
           tend           = tbegin + (n-1)\2dt

           /com, *** Definition of the parameters

           threshold = 150.0
           FFTmethod = 1 !0 = FFT giving partial results, 1 = FFT giving full results

           /com, *** Create a signal from two sinus and add noise

           *dim,signal,array,n
           *dim,t,array,n
           *dim,noise,array,n
           *vfill,noise,rand

           omega1 = (2.0\2pi) / periode1
           omega2 = (2.0\2pi) / periode2
           omega3 = (2.0\2pi) / periode3

           *do,ii,1,n
             noisec     =  amplitudenoise * noise(ii)
             tc         =  tbegin + (ii-1)\2dt
             t(ii)      =  tc

        signal(ii) = amplitude1\2sin(omega1*tc+phase1) + amplitude2\2sin(omega2*tc+phase2) +
        amplitude3\2sin(omega3*tc+phase3) + noisec *enddo /com, *** Display the input signal
        *dim,signaldisp,table,n *dim,tdisp,table,n *do,ii,1,n
        tdisp(ii)=t(ii) signaldisp(ii)=signal(ii) *enddo /show,png /AXLAB,X,TIME /AXLAB,Y,SIGNAL
        /color,curve,BLUE /color,grbak,WHIT /color,wbak,WHIT /color,axes,BLAC /color,axlab,BLAC
        /color,axnum,blac /GROPT,FILL,OFF *vplot,tdisp,signaldisp /com, *** Copy signal in an APDLMath
        vector *vec,sigvec,d,alloc,n,1 *do,ii,1,n sigvec(ii) = signal(ii) *enddo /com, *** Perform a Fast
        Fourier Transform *vec,VFFT,Z,ALLOC,n,1 *if,FFTmethod,eq,0,then \*FFT,FORW,sigvec,VFFT,,,PART
        !partial FFT (use symmetry properties) *else \*FFT,FORW,sigvec,VFFT,,,FULL !full FFT *endif /com, ***
        Determine the real part and the imaginary part of the Fourier's coefficients *vec,VFFTI,Z,COPY,VFFT
        \*AXPY,,,,0.,-1.,VFFTI *vec,VI,D,COPY,VFFTI *vec,VR,D,COPY,VFFT /com, *** Compute the modulus of the
        Fourier's coeff \*EXPORT,VR,APDL,fftr \*EXPORT,VI,APDL,ffti sizeVR = VR_rowDim *if,FFTmethod,eq,0,then
        sizeVR = sizeVR/2 *endif *dim,ind,table,sizeVR *dim,modfft,array,sizeVR *do,ii,1,sizeVR ind(ii) = ii
        modfft(ii)= sqrt( fftr(ii)\2fftr(ii) + ffti(ii)\2ffti(ii) ) *enddo /com,*** Display the Amplitude
        spectrum of the FFT *dim,modfftdisp,table,sizeVR *do,ii,1,sizeVR modfftdisp(ii) = modfft(ii) *enddo
        /show,png /AXLAB,X,Amplitude spectrum of the FFT /AXLAB,Y, *vplot,ind,modfftdisp fini /com, ***
        Threshold on Fourier coefficients *print,VR *do,ii,1,sizeVR module = modfft(ii)
        *if,module,lt,threshold,then VR(ii) = 0.0 VI(ii) = 0.0 *endif *enddo /com, *** Invert Fourier
        Transform *vec,VIFT,Z,COPY,VR \*AXPY,0.0,1.0,VI,1.0,0.0,VIFT *vec,VFILTER,D,ALLOC,VR_DIM
        \*FFT,BACK,VIFT,VFILTER /com, *** Display the filtered signal \*EXPORT,VFILTER,APDL,filterSignal
        *dim,fsignal,table,sizeVR *do,ii,1,sizeVR fsignal(ii) = filterSignal(ii) *enddo /show,png
        /AXLAB,X,TIME /AXLAB,Y,SIGNAL *vplot,tdisp,fsignal fini /com, *** Free the APDLMath objects
        *free,all
        """
        command = f"*FFT,{type_},{inputdata},{outputdata},{dim1},{dim2},{resultformat}"
        return self.run(command, **kwargs)

    def free(self, name: str = "", val1: str = "", **kwargs):
        r"""Deletes a matrix or a solver object and frees its memory allocation.

        Mechanical APDL Command: `\*FREE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FREE.html>`_

        Parameters
        ----------
        name : str
            Name of the matrix or solver object to delete. Use ``Name`` = ALL to delete all APDL Math
            matrices and solver objects. Use ``Name`` = WRK to delete all APDL Math matrices and solver
            objects that belong to a given workspace.

        val1 : str
            If ``Name`` = WRK, ``Val1`` is the memory workspace number.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FREE.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-FREE_argdescript:

        * ``name : str`` - Name of the matrix or solver object to delete. Use ``Name`` = ALL to delete all
          APDL Math matrices and solver objects. Use ``Name`` = WRK to delete all APDL Math matrices and
          solver objects that belong to a given workspace.

        * ``val1 : str`` - If ``Name`` = WRK, ``Val1`` is the memory workspace number.

        .. _a-FREE_notes:

        A :ref:`clear` command will automatically delete all the current APDL Math objects.
        """
        command = f"*FREE,{name},{val1}"
        return self.run(command, **kwargs)

    def hprod(self, a: str = "", b: str = "", c: str = "", **kwargs):
        r"""Performs a Hadamard vector product (C = A∘B).

        Mechanical APDL Command: `\*HPROD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HPROD.html>`_

        Parameters
        ----------
        a : str
            Name of vector A. Must have been previously created by a :ref:`vec` command.

        b : str
            Name of vector B. Must have been previously created by a :ref:`vec` command.

        c : str
            Name of vector C. Must be specified (no default).

        Notes
        -----

        .. _a-HPROD_notes:

        For two vectors ``A`` and ``B`` of the same dimension ``n``, the Hadamard product (A∘B) is a vector
        of the same dimension as the operands, with elements given by:

        .. math::

            equation not available

        This command is limited to vector operands.
        """
        command = f"*HPROD,{a},{b},{c}"
        return self.run(command, **kwargs)

    def init(
        self,
        name: str = "",
        method: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        **kwargs,
    ):
        r"""Initializes a vector or matrix.

        Mechanical APDL Command: `\*INIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_INIT.html>`_

        Parameters
        ----------
        name : str
            Vector or matrix which will be initialized. This can be a vector (created by the :ref:`vec`
            command), a dense matrix (created by the :ref:`dmat` command), or a sparse matrix (created by
            the :ref:`smat` command).

        method : str
            Initialization method to use:

            * ``ZERO`` - Fill the vector/matrix with zeros (default).

            * ``CONST`` - Fill the vector/matrix with a constant value.

            * ``RAND`` - Fill the vector/matrix with random values.

            * ``DIAG`` - Fill the ``n`` th diagonal of the matrix with a constant value. Other values are not
              overwritten. For this option, ``Name`` must be a dense matrix.

            * ``ADIAG`` - Fill the ``n`` th anti-diagonal of the matrix with a constant value. Other values are
              not overwritten. For this option, ``Name`` must be a dense matrix.

            * ``CONJ`` - Take the complex conjugate of the values in the vector/matrix (no change for non-
              complex values).

            * ``FILTER`` - Initialize a subset of values of a vector using a filtering vector. For this option,
              ``Name`` must be a vector.

        val1 : str
            The name of an existing integer vector (created by :ref:`vec` ) to be used as the filter vector.
            The values in this vector indicate the locations in the ``Name`` vector that are to be
            initialized to ``Val2`` (real value) and ``Val3`` (imaginary value, if applicable). Location
            values higher than the dimension of the original vector are ignored.

        val2 : str
            The real part of the value used for initialization (default = 0).

        val3 : str
            The imaginary part of the value used for initialization (default = 0); applicable only if the
            ``Name`` vector contains complex values.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_INIT.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-INIT_argdescript:

        * ``name : str`` - Vector or matrix which will be initialized. This can be a vector (created by the
          :ref:`vec` command), a dense matrix (created by the :ref:`dmat` command), or a sparse matrix
          (created by the :ref:`smat` command).

        * ``method : str`` - Initialization method to use:

          * ``ZERO`` - Fill the vector/matrix with zeros (default).

          * ``CONST`` - Fill the vector/matrix with a constant value.

          * ``RAND`` - Fill the vector/matrix with random values.

          * ``DIAG`` - Fill the ``n`` th diagonal of the matrix with a constant value. Other values are not
            overwritten. For this option, ``Name`` must be a dense matrix.

          * ``ADIAG`` - Fill the ``n`` th anti-diagonal of the matrix with a constant value. Other values are
            not overwritten. For this option, ``Name`` must be a dense matrix.

          * ``CONJ`` - Take the complex conjugate of the values in the vector/matrix (no change for non-
            complex values).

          * ``FILTER`` - Initialize a subset of values of a vector using a filtering vector. For this option,
            ``Name`` must be a vector.

        * ``val1, val2, val3 : str`` - Additional input. The meaning of ``Val1`` through ``Val3`` will vary
          depending on the specified ``Method``. See details below.

        **The following** ``Valx`` fields are used with ``Method`` = CONST:

        * ``val1 : str`` - The real part of the constant value to use (default = 0).

        * ``val2 : str`` - The imaginary part of the constant value to use (default = 0). Required only for
          a complex vector/matrix.

        **The following** ``Valx`` fields are used with ``Method`` = DIAG or ``Method`` = ADIAG:

        * ``val1 : str`` - The number of the diagonal to fill. A zero value (which is the default) indicates
          the main diagonal (or main anti-diagonal). A positive value indicates an upper diagonal; a negative
          value indicates a lower diagonal.

        * ``val2 : str`` - The real part of the constant value to use (default = 1).

        * ``val3 : str`` - The imaginary part of the constant value to use (default = 0). Required only for
          a complex matrix.

        The following example demonstrates ``Method`` = DIAG:

        .. figure::../../../images/_commands/gINIT1.svg

        **The following** ``Valx`` fields are used with ``Method`` = FILTER:

        * ``val1 : str`` - The name of an existing integer vector (created by :ref:`vec` ) to be used as the
          filter vector. The values in this vector indicate the locations in the ``Name`` vector that are to
          be initialized to ``Val2`` (real value) and ``Val3`` (imaginary value, if applicable). Location
          values higher than the dimension of the original vector are ignored.

        * ``val2 : str`` - The real part of the value used for initialization (default = 0).

        * ``val3 : str`` - The imaginary part of the value used for initialization (default = 0); applicable
          only if the ``Name`` vector contains complex values.

        .. _a-INIT_notes:

        This command initializes a previously defined vector ( :ref:`vec` ), dense matrix ( :ref:`dmat` ),
        or sparse matrix ( :ref:`smat` ).
        """
        command = f"*INIT,{name},{method},{val1},{val2},{val3}"
        return self.run(command, **kwargs)

    def itengine(
        self,
        type_: str = "",
        enginename: str = "",
        precondname: str = "",
        matrix: str = "",
        rhsvector: str = "",
        solvector: str = "",
        maxiter: str = "",
        toler: str = "",
        **kwargs,
    ):
        r"""Performs a solution using an iterative solver.

        Mechanical APDL Command: `\*ITENGINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ITENGINE.html>`_

        Parameters
        ----------
        type_ : str
            Specifies the algorithm to be used:

            * ``PCG`` - Preconditioned conjugate gradient (default).

        enginename : str
            Name used to identify this iterative solver engine. Must be specified.

        precondname : str
            Linear solver engine name ( :ref:`lsengine` ) identifying the factored matrix to be used as the
            preconditioner.

        matrix : str
            Name of the matrix to solve.

        rhsvector : str
            Matrix (load vector) name.

        solvector : str
            Solution vector name. If non-zero, it will be taken as the initial vector for the iterative
            process.

        maxiter : str
            Maximum number of iterations allowed. Default is 2 times the number of rows in the matrix.

        toler : str
            Convergence tolerance. Default is 1.0E-8.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ITENGINE.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-ITENGINE_argdescript:

        * ``type_ : str`` - Specifies the algorithm to be used:

          * ``PCG`` - Preconditioned conjugate gradient (default).

        * ``enginename : str`` - Name used to identify this iterative solver engine. Must be specified.

        * ``precondname : str`` - Linear solver engine name ( :ref:`lsengine` ) identifying the factored
          matrix to be used as the preconditioner.

        * ``matrix : str`` - Name of the matrix to solve.

        * ``rhsvector : str`` - Matrix (load vector) name.

        * ``solvector : str`` - Solution vector name. If non-zero, it will be taken as the initial vector
          for the iterative process.

        * ``maxiter : str`` - Maximum number of iterations allowed. Default is 2 times the number of rows in
          the matrix.

        * ``toler : str`` - Convergence tolerance. Default is 1.0E-8.

        .. _a-ITENGINE_notes:

        This command solves Ax = b using a preconditioned conjugate gradient algorithm. It uses an existing
        factored system as the preconditioner. This solution method is useful if an existing matrix has been
        solved and minor changes have been made to the matrix.
        """
        command = f"*ITENGINE,{type_},{enginename},{precondname},{matrix},{rhsvector},{solvector},{maxiter},{toler}"
        return self.run(command, **kwargs)

    def lsbac(
        self,
        enginename: str = "",
        rhsvector: str = "",
        solvector: str = "",
        transkey: str = "",
        **kwargs,
    ):
        r"""Performs the solve (forward/backward substitution) of a factorized linear system.

        Mechanical APDL Command: `\*LSBAC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSBAC.html>`_

        Parameters
        ----------
        enginename : str
            Name used to identify this engine. Must have been previously created using :ref:`lsengine` and
            factorized using :ref:`lsfactor`.

        rhsvector : str
            Name of vector containing the right-hand side (load) vectors as input. Must have been previously
            defined as a :ref:`vec` vector or a :ref:`dmat` matrix.

        solvector : str
            Name of vector that will contain the solution vectors upon completion. Must be predefined as a
            :ref:`vec` vector or :ref:`dmat` matrix.

        transkey : str
            Transpose key. Set ``TransKey`` = TRANS to solve the transposed linear system. If blank,
            transpose will not be used.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSBAC.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-LSBAC_argdescript:

        * ``enginename : str`` - Name used to identify this engine. Must have been previously created using
          :ref:`lsengine` and factorized using :ref:`lsfactor`.

        * ``rhsvector : str`` - Name of vector containing the right-hand side (load) vectors as input. Must
          have been previously defined as a :ref:`vec` vector or a :ref:`dmat` matrix.

        * ``solvector : str`` - Name of vector that will contain the solution vectors upon completion. Must
          be predefined as a :ref:`vec` vector or :ref:`dmat` matrix.

        * ``transkey : str`` - Transpose key. Set ``TransKey`` = TRANS to solve the transposed linear
          system. If blank, transpose will not be used.

        .. _a-LSBAC_notes:

        This command performs forward and back substitution to obtain the solution to the linear matrix
        equation Ax = b (or A :sup:`T` x = b if ``TransKey`` = TRANS). The matrix engine must have been
        previously defined using :ref:`lsengine`, and the matrix factored using :ref:`lsfactor`.

        You can use the :ref:`dmat`,,,COPY (or :ref:`vec`,,,COPY) command to copy the load vector to the
        solution vector in order to predefine it with the appropriate size.
        """
        command = f"*LSBAC,{enginename},{rhsvector},{solvector},{transkey}"
        return self.run(command, **kwargs)

    def lsdump(self, enginename: str = "", filename: str = "", **kwargs):
        r"""Dumps a linear solver engine to a binary File.

        Mechanical APDL Command: `\*LSDUMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSDUMP.html>`_

        Parameters
        ----------
        enginename : str
            Name used to identify this engine. Must have been previously created using :ref:`lsengine` and
            factorized using :ref:`lsfactor`.

        filename : str
            Name of the file to create.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSDUMP.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-LSDUMP_argdescript:

        * ``enginename : str`` - Name used to identify this engine. Must have been previously created using
          :ref:`lsengine` and factorized using :ref:`lsfactor`.

        * ``filename : str`` - Name of the file to create.

        .. _a-LSDUMP_notes:

        Dumps a previously factorized linear solver system to a binary file. Only LAPACK and BCS linear
        solvers can be used with this feature. The Linear Solver can later be restored with the
        :ref:`lsrestore` command.

        A BCS Sparse Solver can be dumped only if uses the ``INCORE`` memory option (see :ref:`bcsoption` ).


        """
        command = f"*LSDUMP,{enginename},{filename}"
        return self.run(command, **kwargs)

    def lsengine(
        self,
        type_: str = "",
        enginename: str = "",
        matrix: str = "",
        option: str = "",
        **kwargs,
    ):
        r"""Creates a linear solver engine.

        Mechanical APDL Command: `\*LSENGINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSENGINE.html>`_

        Parameters
        ----------
        type_ : str
            Specifies the algorithm to be used:

            * ``DSS`` - MKL sparse linear solver.

            * ``LAPACK`` - LAPACK dense matrix linear solver (default if applied to dense matrices).

            * ``DSP`` - Distributed sparse solver (default for sparse matrices).

        enginename : str
            Name used to identify this engine. Must be specified.

        matrix : str
            Name of the matrix to solve.

        option : str
            Option to control the memory mode of the DSS solver (used only if ``Type`` = DSS):

            * ``INCORE`` - In-core memory mode.

            * ``OUTOFCORE`` - Out-of-core memory mode.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSENGINE.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-LSENGINE_argdescript:

        * ``type_ : str`` - Specifies the algorithm to be used:

          * ``DSS`` - MKL sparse linear solver.

          * ``LAPACK`` - LAPACK dense matrix linear solver (default if applied to dense matrices).

          * ``DSP`` - Distributed sparse solver (default for sparse matrices).

        * ``enginename : str`` - Name used to identify this engine. Must be specified.

        * ``matrix : str`` - Name of the matrix to solve.

        * ``option : str`` - Option to control the memory mode of the DSS solver (used only if ``Type`` =
        DSS):

          * ``INCORE`` - In-core memory mode.

          * ``OUTOFCORE`` - Out-of-core memory mode.

        .. _a-LSENGINE_notes:

        This command creates a linear solver engine.

        The DSS and DSP solvers can only be used with sparse matrices. For dense matrices, use the LAPACK
        solver.
        """
        command = f"*LSENGINE,{type_},{enginename},{matrix},{option}"
        return self.run(command, **kwargs)

    def lsfactor(self, enginename: str = "", option: str = "", **kwargs):
        r"""Performs the numerical factorization of a linear solver system.

        Mechanical APDL Command: `\*LSFACTOR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSFACTOR.html>`_

        Parameters
        ----------
        enginename : str
            Name used to identify this engine. Must have been previously created using :ref:`lsengine`.

        option : str
            Option to invert the matrix, used only with an LAPACK engine ( :ref:`lsengine`,LAPACK):

            * ``INVERT`` - Invert the matrix.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSFACTOR.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-LSFACTOR_argdescript:

        * ``enginename : str`` - Name used to identify this engine. Must have been previously created using
          :ref:`lsengine`.

        * ``option : str`` - Option to invert the matrix, used only with an LAPACK engine (
        :ref:`lsengine`,LAPACK):

          * ``INVERT`` - Invert the matrix.

        .. _a-LSFACTOR_notes:

        Performs the computationally intensive, memory intensive factorization of a matrix specified by
        :ref:`lsengine`, using the solver engine also specified by :ref:`lsengine`.
        """
        command = f"*LSFACTOR,{enginename},{option}"
        return self.run(command, **kwargs)

    def lsrestore(self, enginename: str = "", filename: str = "", **kwargs):
        r"""Restores a linear solver engine from a binary file.

        Mechanical APDL Command: `\*LSRESTORE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSRESTORE.html>`_

        Parameters
        ----------
        enginename : str
            Name used to identify this engine.

        filename : str
            Name of the file to read from.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSRESTORE.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-LSRESTORE_argdescript:

        * ``enginename : str`` - Name used to identify this engine.

        * ``filename : str`` - Name of the file to read from.

        .. _a-LSRESTORE_notes:

        Restores a previously dumped Linear Solver (see the :ref:`lsdump` command). This Linear Solver can
        be used to solve a linear system using the :ref:`lsbac` command.


        """
        command = f"*LSRESTORE,{enginename},{filename}"
        return self.run(command, **kwargs)

    def merge(
        self, name1: str = "", name2: str = "", val1: str = "", val2: str = "", **kwargs
    ):
        r"""Merges two dense matrices or vectors into one.

        Mechanical APDL Command: `\*MERGE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MERGE.html>`_

        Parameters
        ----------
        name1 : str
            Name of the matrix or vector to extend.

        name2 : str
            Name of the matrix or vector to be merged into ``Name1``.

        val1 : str
            Row number indicating where the new values are to be inserted into the ``Name1`` vector.

        val2 : str
            Specifies how the ``Name2`` matrix or vector is copied into the ``Name1`` matrix.

            * ``COL`` - Insert the new values at the column location specified by ``Val1`` (default).

            * ``ROW`` - Insert the new values at the row location specified by ``Val1``.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MERGE.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-MERGE_argdescript:

        * ``name1 : str`` - Name of the matrix or vector to extend.

        * ``name2 : str`` - Name of the matrix or vector to be merged into ``Name1``.

        * ``val1, val2 : str`` - Additional input. The meaning of ``Val1`` and ``Val2`` varies depending on
          the entity type (matrix or vector). See details below.

        **The following** ``Val1`` and ``Val2`` fields are used if ``Name1`` refers to a dense matrix
        created by the :ref:`dmat` command:

        * ``val1 : str`` - Column or row number indicating where the new values are to be inserted into the
          ``Name1`` matrix.

        * ``val2 : str`` - Specifies how the ``Name2`` matrix or vector is copied into the ``Name1`` matrix.

          * ``COL`` - Insert the new values at the column location specified by ``Val1`` (default).

          * ``ROW`` - Insert the new values at the row location specified by ``Val1``.

        **The following** ``Val1`` field is used if ``Name1`` refers to a vector created by the :ref:`vec`
        command:

        * ``val1 : str`` - Row number indicating where the new values are to be inserted into the ``Name1``
          vector.

        .. _a-MERGE_notes:

        :ref:`merge` can be used to add new columns or rows to a dense matrix that was created by the
        :ref:`dmat` command. In this case, ``Name1`` must be the name of the dense matrix and ``Name2`` must
        refer to a vector or another dense matrix.

        The following two examples demonstrate merging columns into a dense matrix.

        .. figure::../../../images/_commands/gMERGE1.png

        The following example demonstrates merging rows into a dense matrix.

        .. figure::../../../images/_commands/gMERGE3.png

        :ref:`merge` can also be used to add new rows to a vector that was created by the :ref:`vec`
        command. In this case, ``Name1`` and ``Name2`` must both refer to vectors, as demonstrated in the
        example below.

        .. figure::../../../images/_commands/gMERGE2.png

        In all cases, the values of the original matrix or vector are retained, and the matrix or vector is
        resized to accommodate the additional rows or columns.
        """
        command = f"*MERGE,{name1},{name2},{val1},{val2}"
        return self.run(command, **kwargs)

    def mult(
        self,
        m1: str = "",
        t1: str = "",
        m2: str = "",
        t2: str = "",
        m3: str = "",
        **kwargs,
    ):
        r"""Performs the matrix multiplication M3 = M1 :sup:`(T1)` *M2 :sup:`(T2)`.

        Mechanical APDL Command: `\*MULT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MULT.html>`_

        Parameters
        ----------
        m1 : str
            Name of matrix ``M1``. Must have been previously specified by a :ref:`dmat` or :ref:`smat`
            command.

        t1 : str
            Transpose key. Set ``T1`` = TRANS to use the non-conjugate transpose of ``M1``. Set ``T1`` =
            CTRANS to use the conjugate transpose of ``M1``. CTRANS is only applicable when the ``M1``
            matrix is complex. If blank, transpose will not be used.

        m2 : str
            Name of matrix ``M2``. Must have been previously specified by a :ref:`dmat` command.

        t2 : str
            Transpose key. Set ``T2`` = TRANS to use the non-conjugate transpose of ``M2``. Set ``T2`` =
            CTRANS to use the conjugate transpose of ``M2``. CTRANS is only applicable when the ``M2``
            matrix is complex. If blank, transpose will not be used.

        m3 : str
            Name of resulting matrix, ``M3``. Must be specified.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MULT.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-MULT_argdescript:

        * ``m1 : str`` - Name of matrix ``M1``. Must have been previously specified by a :ref:`dmat` or
          :ref:`smat` command.

        * ``t1 : str`` - Transpose key. Set ``T1`` = TRANS to use the non-conjugate transpose of ``M1``. Set
          ``T1`` = CTRANS to use the conjugate transpose of ``M1``. CTRANS is only applicable when the ``M1``
          matrix is complex. If blank, transpose will not be used.

        * ``m2 : str`` - Name of matrix ``M2``. Must have been previously specified by a :ref:`dmat`
          command.

        * ``t2 : str`` - Transpose key. Set ``T2`` = TRANS to use the non-conjugate transpose of ``M2``. Set
          ``T2`` = CTRANS to use the conjugate transpose of ``M2``. CTRANS is only applicable when the ``M2``
          matrix is complex. If blank, transpose will not be used.

        * ``m3 : str`` - Name of resulting matrix, ``M3``. Must be specified.

        .. _a-MULT_notes:

        The matrices must be dimensionally consistent such that the number of columns of ``M1`` (or the
        transposed matrix, if requested) is equal to the number of rows of ``M2`` (or the transposed matrix,
        if requested).

        You cannot multiply two sparse matrices with this command (that is, ``M1`` and ``M2`` cannot both be
        sparse). The resulting matrix, ``M3``, will always be a dense matrix, no matter what combination of
        input matrices is used (dense\*sparse, sparse\*dense, or dense\*dense).
        """
        command = f"*MULT,{m1},{t1},{m2},{t2},{m3}"
        return self.run(command, **kwargs)

    def nrm(
        self,
        name: str = "",
        normtype: str = "",
        parr: str = "",
        normalize: str = "",
        **kwargs,
    ):
        r"""Computes the norm of the specified matrix or vector.

        Mechanical APDL Command: `\*NRM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NRM.html>`_

        Parameters
        ----------
        name : str
            Matrix or vector for which the norm will be computed. This can be a dense matrix (created by the
            :ref:`dmat` command), a sparse matrix (created by the :ref:`smat` command) or a vector (created
            by the :ref:`vec` command)

        normtype : str
            Mathematical norm to use:

            * ``NRM2`` - L2 (Euclidian or SRSS) norm (default).

            * ``NRM1`` - L1 (absolute sum) norm (vectors and dense matrices only).

            * ``NRMINF`` - Maximum norm.

        parr : str
            Parameter name that contains the result.

        normalize : str
            Normalization key; to be used only for vectors created by :ref:`vec` :

            * ``YES`` - Normalize the vector such that the norm is 1.0.

            * ``NO`` - Do not normalize the vector (default).

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NRM.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-NRM_argdescript:

        * ``name : str`` - Matrix or vector for which the norm will be computed. This can be a dense matrix
          (created by the :ref:`dmat` command), a sparse matrix (created by the :ref:`smat` command) or a
          vector (created by the :ref:`vec` command)

        * ``normtype : str`` - Mathematical norm to use:

          * ``NRM2`` - L2 (Euclidian or SRSS) norm (default).

          * ``NRM1`` - L1 (absolute sum) norm (vectors and dense matrices only).

          * ``NRMINF`` - Maximum norm.

        * ``parr : str`` - Parameter name that contains the result.

        * ``normalize : str`` - Normalization key; to be used only for vectors created by :ref:`vec` :

          * ``YES`` - Normalize the vector such that the norm is 1.0.

          * ``NO`` - Do not normalize the vector (default).

        .. _a-NRM_notes:

        The NRM2 option corresponds to the Euclidian or L2 norm and is applicable to either vectors or
        matrices:

        :math:`equation not available`,  :math:`equation not available`

        :math:`equation not available`,  :math:`equation not available`  where  :math:`equation not
        available`  is the complex conjugate of  :math:`equation not available`

        :math:`equation not available`,  :math:`equation not available`  = largest eigenvalue of
        :math:`equation not available`

        The NRM1 option corresponds to the L1 norm and is applicable to vectors and dense matrices:

        :math:`equation not available`  or  :math:`equation not available`,  :math:`equation not available`

        :math:`equation not available`  or  :math:`equation not available`,  :math:`equation not available`

        The NRMINF option is the maximum norm and is applicable to either vectors or matrices:

        :math:`equation not available`  or  :math:`equation not available`,  :math:`equation not available`

        :math:`equation not available`  or  :math:`equation not available`,  :math:`equation not available`
        """
        command = f"*NRM,{name},{normtype},{parr},{normalize}"
        return self.run(command, **kwargs)

    def remove(
        self, name: str = "", val1: str = "", val2: str = "", val3: str = "", **kwargs
    ):
        r"""Suppresses rows or columns of a dense matrix or a vector.

        Mechanical APDL Command: `\*REMOVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_REMOVE.html>`_

        Parameters
        ----------
        name : str
            Name of the matrix or vector to be revised.

        val1 : str
            First value index to suppress.

        val2 : str
            Last value index to suppress.

        val3 : str
            Specifies what to remove:

            * ``COL`` - Remove columns of the matrix (default).

            * ``ROW`` - Remove rows of the matrix.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_REMOVE.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-REMOVE_argdescript:

        * ``name : str`` - Name of the matrix or vector to be revised.

        * ``val1, val2, val3 : str`` - Additional input. The meaning of ``Val1`` to ``Val3`` varies
          depending on the entity type (matrix or vector). See details below.

        **The following** ``Val1`` through ``Val3`` fields are used if ``Name`` refers to a dense matrix
        created by the :ref:`dmat` command:

        * ``val1 : str`` - First row or column number to suppress.

        * ``val2 : str`` - Last row or column number to suppress.

        * ``val3 : str`` - Specifies what to remove:

          * ``COL`` - Remove columns of the matrix (default).

          * ``ROW`` - Remove rows of the matrix.

        **The following** ``Val1`` and ``Val2`` fields are used if ``Name`` refers to a vector created by
        the :ref:`vec` command:

        * ``val1 : str`` - First value index to suppress.

        * ``val2 : str`` - Last value index to suppress.

        .. _a-REMOVE_notes:

        The values of the original matrix or vector specified by ``Name`` are retained. The matrix or vector
        is resized to the new number of rows and columns.
        """
        command = f"*REMOVE,{name},{val1},{val2},{val3}"
        return self.run(command, **kwargs)

    def scal(self, name: str = "", val1: str = "", val2: str = "", **kwargs):
        r"""Scales a vector or matrix by a constant.

        Mechanical APDL Command: `\*SCAL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SCAL.html>`_

        Parameters
        ----------
        name : str
            Name used to identify the vector or matrix to be scaled. Must be specified.

        val1 : str
            The real part of the constant to use (default = 1).

        val2 : str
            The imaginary part of the constant to use (default = 0). This value is used only if the vector
            or matrix specified by ``Name`` is complex.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SCAL.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-SCAL_argdescript:

        * ``name : str`` - Name used to identify the vector or matrix to be scaled. Must be specified.

        * ``val1 : str`` - The real part of the constant to use (default = 1).

        * ``val2 : str`` - The imaginary part of the constant to use (default = 0). This value is used only
          if the vector or matrix specified by ``Name`` is complex.

        .. _a-SCAL_notes:

        This command can be applied to vectors and matrices created by the :ref:`vec`, :ref:`dmat` and
        :ref:`smat` commands.
        """
        command = f"*SCAL,{name},{val1},{val2}"
        return self.run(command, **kwargs)

    def smat(
        self,
        matrix: str = "",
        type_: str = "",
        method: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        **kwargs,
    ):
        r"""Creates a sparse matrix.

        Mechanical APDL Command: `\*SMAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SMAT.html>`_

        Parameters
        ----------
        matrix : str
            Name used to identify the matrix. Must be specified.

        type_ : str
            Matrix type:

            * ``D`` - Double precision real values (default).

            * ``Z`` - Complex double precision values.

        method : str
            Method used to create the matrix:

            * ``ALLOC`` - Allocate a new matrix.

            * ``COPY`` - Copy an existing matrix.

            * ``IMPORT`` - Import the matrix from a file.

        val1 : str
            Name of the matrix to copy (can be either a dense or a sparse matrix).

        val2 : str
            Method used for copying the matrix:

            * ``DIAG`` - Copy only the diagonal of the matrix. ``Val3`` and ``Val4`` are ignored.

            * ``TRANS`` - Transpose the original matrix. ``Val3`` and ``Val4`` are ignored.

            * ``EXTRACT`` - Extract a submatrix based on row and column numbers specified by ``Val3`` and
              ``Val4``.

        val3 : str
            Name of integer vector ( :ref:`vec` ) containing row numbers. If no vector is specified,
            defaults to all rows.

        val4 : str
            Name of integer vector ( :ref:`vec` ) containing column numbers. If no vector is specified,
            defaults to all columns.

        val5 : str
            Additional input. The meaning of ``Val1`` through ``Val5`` will vary depending on the specified
            ``Method``. See details below.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SMAT.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-SMAT_argdescript:

        * ``matrix : str`` - Name used to identify the matrix. Must be specified.

        * ``type_ : str`` - Matrix type:

          * ``D`` - Double precision real values (default).

          * ``Z`` - Complex double precision values.

        * ``method : str`` - Method used to create the matrix:

          * ``ALLOC`` - Allocate a new matrix.

          * ``COPY`` - Copy an existing matrix.

          * ``IMPORT`` - Import the matrix from a file.

        * ``val1, val2, val3, val4, val5 : str`` - Additional input. The meaning of ``Val1`` through
          ``Val5`` will vary depending on the specified ``Method``. See details below.

        **The following** ``Valx`` fields are used with ``Method`` = ALLOC.

        * ``val1 : str`` - Method used to create the matrix:

          * ``DIAG`` - Allocate a diagonal square matrix. ``Val2`` is used; ``Val3``, ``Val4``, and ``Val5`` are ignored.

            * ``Val2`` - Matrix size.

          * ``CSR`` - Create a square sparse matrix based on Compressed Sparse Row (CSR) format description vectors. This
            format requires 3 input vectors specified as ``Val2``, ``Val3`` and ``Val4``.

            * ``Val2, Val3, Val4`` - Names of required row_ptr, col_ind and val vectors. These vectors must
              be created using the :ref:`vec` command.

              row_ptr is a long integer vector (use of L instead of I as the scalar type in the :ref:`vec` call);
              col_ind is an integer vector. Val can be a real of complex values vector, according to the matrix
              type.

            * ``Val5`` - Specifies whether the matrix is symmetric (TRUE) or unsymmetric (FALSE). Default =
              TRUE.

        **The following** ``Valx`` fields are used with ``Method`` = COPY.

        * ``val1 : str`` - Name of the matrix to copy (can be either a dense or a sparse matrix).

        * ``val2 : str`` - Method used for copying the matrix:

          * ``DIAG`` - Copy only the diagonal of the matrix. ``Val3`` and ``Val4`` are ignored.

          * ``TRANS`` - Transpose the original matrix. ``Val3`` and ``Val4`` are ignored.

          * ``EXTRACT`` - Extract a submatrix based on row and column numbers specified by ``Val3`` and
            ``Val4``.

        * ``val3 : str`` - Name of integer vector ( :ref:`vec` ) containing row numbers. If no vector is
          specified, defaults to all rows.

        * ``val4 : str`` - Name of integer vector ( :ref:`vec` ) containing column numbers. If no vector is
          specified, defaults to all columns.

        **The following table describes the** ``Valx`` fields used with ``Method`` = IMPORT.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _a-SMAT_notes:

        Use the :ref:`dmat` command to create a dense matrix.

        For more information on the CSR format, see `Creating a Sparse Matrix Using the CSR Format
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdlCSRformat.html#eqdaaeaade-718e-4f25-b7ce-
        ba5a1903b1bf>`_

        For more information on the NOD2SOLV and USR2SOLV mapping vectors, see.

        For more information about :file:`.FULL` file contents, see the :ref:`hbmat` in the `Command
        Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_Z_TOC.html>`_.
        """
        command = f"*SMAT,{matrix},{type_},{method},{val1},{val2},{val3},{val4},{val5}"
        return self.run(command, **kwargs)

    def starinquire(self, obj: str = "", property_: str = "", var1: str = "", **kwargs):
        r"""Retrieves properties of an existing APDL Math object.

        Mechanical APDL Command: `\*INQUIRE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_INQUIRE_a.html>`_

        Parameters
        ----------
        obj : str
            Name of the vector or matrix of interest.

        property_ : str
            Object property to get:

            * ``DIM1`` - First dimension of a matrix, or size of a vector.

            * ``DIM2`` - Second dimension of a matrix.

        var1 : str
            Name of the resulting parameter that contains the property value.

        Notes
        -----

        .. _a-INQUIRE_notes:

        The following example demonstrates using :ref:`starinquire` to get the number of rows and columns of
        an existing matrix.

        .. code:: apdl

           *SMAT,K,D,IMPORT,FULL,file.full,STIFF  ! Import the stiffness matrix from an existing FULL file
           *INQUIRE,K,DIM1,NROW                   ! Get the first dimension of the stiffness matrix
           *INQUIRE,K,DIM2,NCOL                   ! Get the second dimension of the stiffness matrix
           /COM, K matrix size: %NROW% x %NCOL%
        """
        command = f"*INQUIRE,{obj},{property_},{var1}"
        return self.run(command, **kwargs)

    def starprint(self, matrix: str = "", fname: str = "", **kwargs):
        r"""Prints the matrix values to a file.

        Mechanical APDL Command: `\*PRINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRINT_a.html>`_

        Parameters
        ----------
        matrix : str
            Name of matrix or vector to print. Must be specified.

        fname : str
            File name (case-sensitive, 32-character maximum). If blank, matrix is written to the output
            file.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRINT_a.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-PRINT_argdescript:

        * ``matrix : str`` - Name of matrix or vector to print. Must be specified.

        * ``fname : str`` - File name (case-sensitive, 32-character maximum). If blank, matrix is written to
          the output file.

        .. _a-PRINT_notes:

        The matrix may be a dense matrix ( :ref:`dmat` ), a sparse matrix ( :ref:`smat` ), or a vector (
        :ref:`vec` ). Only the non-zero entries of the matrix are printed.
        """
        command = f"*PRINT,{matrix},{fname}"
        return self.run(command, **kwargs)

    def starrename(self, oldname: str = "", newname: str = "", **kwargs):
        r"""Renames an existing vector or matrix.

        Mechanical APDL Command: `\*RENAME <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RENAME_a.html>`_

        Parameters
        ----------
        oldname : str
            Name of the existing vector or matrix to be renamed.

        newname : str
            New name for the vector or matrix.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RENAME_a.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-RENAME_argdescript:

        * ``oldname : str`` - Name of the existing vector or matrix to be renamed.

        * ``newname : str`` - New name for the vector or matrix.

        .. _a-RENAME_notes:

        The :ref:`starrename` command is used to rename `APDL Math
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdlmathex.html>`_ objects.
        """
        command = f"*RENAME,{oldname},{newname}"
        return self.run(command, **kwargs)

    def starsort(
        self,
        name: str = "",
        sorttype: str = "",
        val1: str = "",
        val2: str = "",
        **kwargs,
    ):
        r"""Sorts the values of the specified vector.

        Mechanical APDL Command: `\*SORT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SORT_st.html>`_

        Parameters
        ----------
        name : str
            Name of the vector to be sorted. This vector can contain real or complex values.

        sorttype : str
            Criteria used to sort the values:

            * ``VALUE`` - Values are sorted based on their real value (default).

            * ``ABS`` - Values are sorted based on their absolute value.

            * ``PERM`` - Values are sorted based on the input permutation vector ( ``Val1`` ).

        val1 : str
            Name of the permutation vector used to sort the values. This must be a vector of integer values
            that was created with the :ref:`vec` command. The size of this permutation vector must be
            identical to the size of the vector to be sorted.

            This permutation vector is required when using ``Method`` = PERM.

        val2 : str
            Order of the sort operation:

            * ``0`` - Increasing order (default).

            * ``1`` - Decreasing order.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SORT_st.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-SORT_argdescript:

        * ``name : str`` - Name of the vector to be sorted. This vector can contain real or complex values.

        * ``sorttype : str`` - Criteria used to sort the values:

          * ``VALUE`` - Values are sorted based on their real value (default).

          * ``ABS`` - Values are sorted based on their absolute value.

          * ``PERM`` - Values are sorted based on the input permutation vector ( ``Val1`` ).

        * ``val1, val2 : str`` - Additional input. The meaning of ``Val1``, ``Val2`` varies depending on the
          specified ``SortType``. See below for details.

        **The following** ``Valx`` fields are used with ``SortType`` = VALUE or ABS:

        * ``val1 : str`` - Name of the vector in which permutation values will be saved (optional). This
          should be an empty vector of type integer that was created with the :ref:`vec` command. The size of
          this permutation vector must be identical to the size of the vector to be sorted. After the sort,
          this vector contains the permutation used to sort the values.

        * ``val2 : str`` - Order of the sort operation:

          * ``0`` - Increasing order (default).

          * ``1`` - Decreasing order.

        **The following** ``Valx`` fields are used with ``Method`` = PERM:

        * ``val1 : str`` - Name of the permutation vector used to sort the values. This must be a vector of
          integer values that was created with the :ref:`vec` command. The size of this permutation vector
          must be identical to the size of the vector to be sorted.

          This permutation vector is required when using ``Method`` = PERM.

        .. _a-SORT_notes:

        The examples below demonstrate using :ref:`starsort` to sort the values of an input vector.

        The following input:

        .. code:: apdl

           *VEC,V,I,ALLOC,5
           V(1)=5,-3,2,0,-1
           *SORT,V,VALUE
           *PRINT,V

        generates this output:

        .. code:: apdl

                  -3        -1         0         2         5

        To reverse the order, this input:

        .. code:: apdl

           *SORT,V,VALUE,,1
           *PRINT,V

        generates this output:

        .. code:: apdl

                   5         2         0        -1        -3
        """
        command = f"*SORT,{name},{sorttype},{val1},{val2}"
        return self.run(command, **kwargs)

    def vec(
        self,
        vector: str = "",
        type_: str = "",
        method: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        **kwargs,
    ):
        r"""Creates a vector.

        Mechanical APDL Command: `\*VEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VEC.html>`_

        Parameters
        ----------
        vector : str
            Name used to identify the vector. Must be specified.

        type_ : str
            Vector type:

            * ``D`` - Double precision real values (default).

            * ``Z`` - Complex double precision values.

            * ``I`` - Integer values.

        method : str
            Method used to create the vector:

            * ``ALLOC`` - Allocate space for a vector (default).

            * ``RESIZE`` - Resize an existing vector to a new length. Values are kept from the original vector.
              If the length specified by ``Val1`` is greater than the original vector length, the additional rows
              are assigned a value of zero.

            * ``COPY`` - Copy an existing vector.

            * ``IMPORT`` - Import the vector from a file.

            * ``LINK`` - Link to a column of an existing dense :ref:`dmat` matrix and use it in subsequent
              vector calculations. Any changes to the vector are also made to the corresponding matrix column
              (memory is shared).

        val1 : str
            Name of the :ref:`dmat` matrix.

        val2 : str
            Column number of the matrix to link to.

        val3 : str
            Additional input. The meaning of ``Val1`` through ``Val5`` will vary depending on the specified
            ``Method``. See details below.

        val4 : str
            Additional input. The meaning of ``Val1`` through ``Val5`` will vary depending on the specified
            ``Method``. See details below.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VEC.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-VEC_argdescript:

        * ``vector : str`` - Name used to identify the vector. Must be specified.

        * ``type_ : str`` - Vector type:

          * ``D`` - Double precision real values (default).

          * ``Z`` - Complex double precision values.

          * ``I`` - Integer values.

        * ``method : str`` - Method used to create the vector:

          * ``ALLOC`` - Allocate space for a vector (default).

          * ``RESIZE`` - Resize an existing vector to a new length. Values are kept from the original vector.
            If the length specified by ``Val1`` is greater than the original vector length, the additional rows
            are assigned a value of zero.

          * ``COPY`` - Copy an existing vector.

          * ``IMPORT`` - Import the vector from a file.

          * ``LINK`` - Link to a column of an existing dense :ref:`dmat` matrix and use it in subsequent
            vector calculations. Any changes to the vector are also made to the corresponding matrix column
            (memory is shared).

        * ``val1, val2, val3, val4, val5 : str`` - Additional input. The meaning of ``Val1`` through
          ``Val5`` will vary depending on the specified ``Method``. See details below.

        **The following** ``Valx`` field is used with ``Method`` = ALLOC or ``Method`` = RESIZE:

        * ``val1 : str`` - Number of rows in the vector.

        **The following** ``Valx`` field is used with ``Method`` = COPY:

        * ``val1 : str`` - Name of the vector to copy.

        * ``val2 : str`` - Optional argument to specify either the real or the imaginary part of the values
        to be copied. This
          option only applies when copying a complex value vector to a real value vector.

          * ``REAL`` - Copy the real part of the vector to the output vector.

          * ``IMAG`` - Copy the imaginary part of the vector to the output vector.

        **The following table describes the** ``Valx`` fields used with ``Method`` = IMPORT.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        **The following** ``Valx`` fields are used with ``Method`` = LINK:

        * ``val1 : str`` - Name of the :ref:`dmat` matrix.

        * ``val2 : str`` - Column number of the matrix to link to.

        .. _a-VEC_notes:

        Use the :ref:`dmat` command to create a matrix.

        For more information on the BACK and FORWARD nodal mapping vectors, see in the `Ansys Parametric
        Design Language Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_apdl/apdlxpl.html>`_.
        """
        command = f"*VEC,{vector},{type_},{method},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def wrk(self, num: str = "", **kwargs):
        r"""Sets the active workspace number.

        Mechanical APDL Command: `\*WRK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_WRK.html>`_

        Parameters
        ----------
        num : str
            Number of the active memory workspace for APDLMath vector and matrices. All the following
            APDLMath vectors and matrices will belong to this memory workspace, until the next call to the
            :ref:`wrk` command. By default, all the APDLMath objects belong to workspace number 1.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_WRK.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _a-WRK_argdescript:

        * ``num : str`` - Number of the active memory workspace for APDLMath vector and matrices. All the
          following APDLMath vectors and matrices will belong to this memory workspace, until the next call to
          the :ref:`wrk` command. By default, all the APDLMath objects belong to workspace number 1.

        .. _a-WRK_notes:

        This feature enables you to associate a set of vector and matrices in a given memory workspace, so
        that you can easily manage the free step:

        .. code:: apdl

           *VEC,V,D,ALLOC,5		! V belongs to the default Workspace 1

           \*WRK,2					! Set the active workspace as the number 2

           \*VEC,W,D,IMPORT,FULL,file.full,RHS	! W belongs to the Workspace 2
           \*SMAT,K,D,IMPORT,FULL,file.full,STIFF	! K belongs to the Workspace 2
           \*DMAT,M,ALLOC,10,10 			! M belongs to the Workspace 2
           ...
           \*FREE,WRK,2			! W, K and M are deleted, but not V

           \*PRINT,V

        This feature can be useful to free all the temporary APDLMath variables inside a MACRO in one call.
        """
        command = f"*WRK,{num}"
        return self.run(command, **kwargs)
