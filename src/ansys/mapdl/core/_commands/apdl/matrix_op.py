class MatrixOP:
    def axpy(self, vr="", vi="", m1="", wr="", wi="", m2="", **kwargs):
        """Performs the matrix operation ``M2= v*M1 + w*M2``.

        APDL Command: ``*AXPY``

        Parameters
        ----------
        vr, vi
            The real and imaginary parts of the scalar v. Default value is 0.

        m1
            Name of matrix M1. If not specified, the operation ``M2 = w*M2`` will
            be performed.

        wr, wi
            The real and imaginary parts of the scalar w. Default value is 0.

        m2
            Name of matrix M2. Must be specified.

        Notes
        -----
        The matrices M1 and M2 must have the same dimensions and same type
        (dense or sparse). If M2 is real, vi and wi are ignored.
        """
        command = f"*AXPY,{vr},{vi},{m1},{wr},{wi},{m2}"
        return self.run(command, **kwargs)

    def comp(self, matrix="", algorithm="", threshold="", **kwargs):
        """Compresses the columns of a matrix using a specified algorithm.

        APDL Command: ``*COMP``

        Parameters
        ----------
        matrix
            Name of the matrix to compress.

        algorithm
            Algorithm to use:

            Singular value decomposition algorithm (default). - Modified Gram-Schmidt algorithm.

        threshold
            Numerical threshold value used to manage the compression. Default
            value for SVD is 1E-7; default value for MGS is 1E-14.

        Notes
        -----
        The algorithms available through this command are only applicable to
        dense matrices that were created using the ``*DMAT`` command.

        Columns which are linearly dependent on others are removed, leaving the
        independent or basis vectors. The matrix is resized according to the
        new size determined by the algorithm.
        """
        command = f"*COMP,{matrix},{algorithm},{threshold}"
        return self.run(command, **kwargs)

    def dmat(
        self,
        matrix="",
        type_="",
        method="",
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        **kwargs,
    ):
        """Creates a dense matrix.

        APDL Command: ``*DMAT``

        Parameters
        ----------
        matrix
            Name used to identify the matrix. Must be specified.

        type\_
            Matrix type:

            Double precision real values (default). - Complex double precision values.

        method
            Method used to create the matrix:

            Allocate space for a matrix (default). - Resize an
            existing matrix to new row and column dimensions. Values
            are kept from the original matrix. If the dimensions
            specified by Val1 (rows) and Val2 (columns) are greater
            than the original matrix size, the additional entries are
            assigned a value of zero.

            Copy an existing matrix. - Link to an existing matrix. The
            memory will be shared between the original matrix and the
            new matrix. This is useful for manipulating a submatrix of
            a larger matrix. The Val1 through Val5 arguments will be
            used to specify the lower and upper bounds of row and
            column numbers from the original matrix.

        val1, val2, val3, val4, val5
            Additional input. The meaning of Val1 through Val5 will vary
            depending on the specified Method. See details below.

        Notes
        -----
        This command allows you to create a dense matrix. To create a sparse
        matrix, use the ``*SMAT`` command. ``*SMAT`` is recommended for large matrices
        obtained from the .FULL or .HBMAT file. Refer to the HBMAT command
        documentation for more information about .FULL file contents.

        Use the ``*VEC`` command to create a vector.

        For very large matrices, use the OUTOFCORE option (Method = ALLOC or
        COPY) to keep some of the matrix on disk if there is insufficient
        memory.

        When importing a dense matrix from a DMIG file, you can define the
        formatting of the file using the Val3 and Val4 fields.

        """
        command = f"*DMAT,{matrix},{type_},{method},{val1},{val2},{val3},{val4},{val5}"
        return self.run(command, **kwargs)

    def dot(self, vector1="", vector2="", par_real="", par_imag="", **kwargs):
        """Computes the dot (or inner) product of two vectors.

        APDL Command: ``*DOT``

        Parameters
        ----------
        vector1
            Name of first vector; must have been previously specified by a ``*VEC``
            command.

        vector2
            Name of second vector; must have been previously specified by a
            ``*VEC`` command.

        par_real
            Parameter name that contains the result.

        par_imag
            Parameter name that contains the imaginary part of the result (used
            only for complex vectors).

        Notes
        -----
        If Vector1 and Vector2 are complex, the complex conjugate of Vector1 is
        used to compute the result (Par_Real, Par_Imag).
        """
        command = f"*DOT,{vector1},{vector2},{par_real},{par_imag}"
        return self.run(command, **kwargs)

    def eigen(self, kmatrix="", mmatrix="", cmatrix="", evals="", evects="", **kwargs):
        """Performs a modal solution with unsymmetric or damping matrices.

        APDL Command: ``*EIGEN``

        Parameters
        ----------
        kmatrix
            Name of the stiffness matrix. May be a real or complex-valued
            matrix.

        mmatrix
            Name of the mass matrix.

        cmatrix
            Name of the damping matrix (used only for MODOPT,DAMP).

        evals
            Name of the output eigenvalues vector. It will be an m-long ``*VEC``
            vector of complex values, where m is the number of eigenvalues
            requested (MODOPT).

        evects
            Name of the output eigenvector matrix. It will be a n x m ``*DMAT``
            (dense) matrix of complex values, where n is the size of the matrix
            and m is the number of eigenvalues requested (MODOPT).

        Notes
        -----
        Use the command ANTYPE,MODAL and the MODOPT command to specify the
        modal solution options. Only MODOPT,DAMP, MODOPT,UNSYM, MODOPT,LANB,
        and MODOPT,SUBSP are supported.

        ``*EIGEN`` with Block Lanczos (LANB) only supports sparse matrices.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"*EIGEN,{kmatrix},{mmatrix},{cmatrix},{evals},{evects}"
        return self.run(command, **kwargs)

    def export(
        self,
        matrix="",
        format_="",
        fname="",
        val1="",
        val2="",
        val3="",
        **kwargs,
    ):
        """Exports a matrix to a file in the specified format.

        APDL Command: ``*EXPORT``

        Parameters
        ----------
        matrix
            Name of the matrix to export (must be a matrix previously created
            with ``*DMAT`` or ``*SMAT``, or a vector previously created with ``*VEC``).

        format\_
            Format of the output file:

            Export the matrix in the Matrix Market Format. - Export
            the matrix in the SUB file format.

            Export the matrix in the Harwell-Boeing file format. -
            Export the matrix in a native format, to be re-imported
            using the ``*DMAT`` or ``*SMAT`` command.

            Export the matrix to an existing EMAT file. - Export the
            matrix to an APDL array parameter.

            Export the matrix profile to a Postscript file. - Export
            the matrix in the DMIG file format.

        fname
            Name of the file, or name of the array parameter if Format = APDL.

        val1, val2, val3
            Additional input. The meaning of Val1 through Val3 will vary
            depending on the specified Format. See table below for details.

        Notes
        -----
        Only sparse matrices can be exported to Postscript files. This option
        plots the matrix profile as a series of dots.

        If you want to create a .SUB file from several matrices, you need to
        set Val3 = WAIT for all matrices but the last, and Val3 = DONE for the
        last one. The export will be effective at the last ``*EXPORT`` command.

        To create a .SUB file or .DMIG file from scratch, you must supply the
        row information array. (Specify this array in the Val2 field for .SUB
        or in the Val1 field for .DMIG.) This must be an m x 2 array, where m
        is the size of the matrix. The first column is the node number and the
        second column is the DOF number corresponding to each row of the
        matrix.

        The ``*EXPORT`` command is not applicable to sparse matrices initialized
        from .FULL files by means of the NOD2BCS option on the ``*SMAT`` command
        (i.e., ``*SMAT,,,IMPORT,FULL,,NOD2BCS``).
        """
        command = f"*EXPORT,{matrix},{format_},{fname},{val1},{val2},{val3}"
        return self.run(command, **kwargs)

    def fft(
        self,
        type_="",
        inputdata="",
        outputdata="",
        dim1="",
        dim2="",
        resultformat="",
        **kwargs,
    ):
        """Computes the fast Fourier transformation of a specified matrix or

        APDL Command: ``*FFT``
        vector.

        Parameters
        ----------
        type\_
            Type of FFT transformation:

            Forward FFT computation (default). - Backward FFT computation.

        inputdata
            Name of matrix or vector for which the FFT will be computed. This
            can be a dense matrix (created by the ``*DMAT`` command) or a vector
            (created by the ``*VEC`` command). Data can be real or complex values.
            There is no default value for this argument.

        outputdata
            Name of matrix or vector where the FFT results will be stored. The
            type of this argument must be consistent with InputData (see table
            below). There is no default value for this argument.

        dim1
            The number of terms to consider for a vector, or the number of rows
            for a matrix. Defaults to the whole input vector or all the rows of
            the matrix.

        dim2
            The number of columns to consider for a matrix. Defaults to all the
            columns of the matrix. (Valid only for matrices.)

        resultformat
            Specifies the result format:

            Returns the full result. That is, the result matches the
            dimension specified on this command (DIM1, DIM2). -
            Returns partial results. For real input data, there is a
            symmetry in the results of the Fourier transform as some
            coefficients are conjugated. The partial format uses this
            symmetry to optimize the storage of the results. (Valid
            only for real data.)

        Notes
        -----
        In the example that follows, the fast Fourier transformation is used to
        filter frequencies from a noisy input signal.
        """
        command = f"*FFT,{type_},{inputdata},{outputdata},{dim1},{dim2},{resultformat}"
        return self.run(command, **kwargs)

    def free(self, name="", **kwargs):
        """Deletes a matrix or a solver object and frees its memory allocation.

        APDL Command: ``*FREE``

        Parameters
        ----------
        name
            Name of the matrix or solver object to delete. Use Name = ALL to
            delete all APDL Math matrices and solver objects.  Use Name = WRK
            to delete all APDL Math matrices and solver objects that belong to
            a given workspace.

        val1
            If Name = WRK, Val1 is to set the memory workspace number.

        Notes
        -----
        A /CLEAR command will automatically delete all the current APDL Math
        objects.
        """
        command = f"*FREE,{name}"
        return self.run(command, **kwargs)

    def init(self, name="", method="", val1="", val2="", val3="", **kwargs):
        """Initializes a vector or dense matrix.

        APDL Command: ``*INIT``

        Parameters
        ----------
        name
            Vector or matrix which will be initialized. This can be a vector
            (created by the ``*VEC`` command) or a dense matrix (created by the
            ``*DMAT`` command).

        method
            Initialization method to use:

            Fill the vector/matrix with zeros (default). - Fill the vector/matrix with a constant value.

            Fill the vector/matrix with random values. - Fill the nth diagonal of the matrix with a constant value. Other values are not
                              overwritten.

        val1, val2, val3
            Additional input. The meaning of Val1 through Val3 will vary
            depending on the specified Method. See details below.

        Notes
        -----
        This command initializes a previously defined vector (``*VEC``) or dense
        matrix (``*DMAT``).
        """
        command = f"*INIT,{name},{method},{val1},{val2},{val3}"
        return self.run(command, **kwargs)

    def itengine(
        self,
        type_="",
        enginename="",
        precondname="",
        matrix="",
        rhsvector="",
        solvector="",
        maxiter="",
        toler="",
        **kwargs,
    ):
        """Performs a solution using an iterative solver.

        APDL Command: ``*ITENGINE``

        Parameters
        ----------
        type\_
            Specifies the algorithm to be used:

        enginename
            Name used to identify this iterative solver engine. Must be
            specified.

        precondname
            Linear solver engine name (``*LSENGINE``) identifying the factored
            matrix to be used as the preconditioner.

        matrix
            Name of the matrix to solve.

        rhsvector
            Matrix (load vector) name.

        solvector
            Solution vector name. If non-zero, it will be taken as the initial
            vector for the iterative process.

        maxiter
            Maximum number of iterations allowed. Default is 2 times the number
            of rows in the matrix.

        toler
            Convergence tolerance. Default is 1.0E-8.

        Notes
        -----
        This command solves Ax = b using a preconditioned conjugate gradient
        algorithm. It uses an existing factored system as the preconditioner.
        This solution method is useful if an existing matrix has been solved
        and minor changes have been made to the matrix.
        """
        command = f"*ITENGINE,{type_},{enginename},{precondname},{matrix},{rhsvector},{solvector},{maxiter},{toler}"
        return self.run(command, **kwargs)

    def lsbac(self, enginename="", rhsvector="", solvector="", **kwargs):
        """Performs the solve (forward/backward substitution) of a
        factorized linear system.

        APDL Command: ``*LSBAC``

        Parameters
        ----------
        enginename
            Name used to identify this engine. Must have been previously
            created using ``*LSENGINE`` and factorized using ``*LSFACTOR``.

        rhsvector
            Name of vector containing the right-hand side (load) vectors as
            input. Must have been previously defined as a ``*VEC`` vector or a
            ``*DMAT`` matrix.

        solvector
            Name of vector that will contain the solution vectors upon
            completion. Must be predefined as a ``*VEC`` vector or ``*DMAT`` matrix.

        Notes
        -----
        This command performs forward and back substitution to obtain the
        solution to the linear matrix equation Ax = b. The matrix engine must
        have been previously defined using ``*LSENGINE``, and the matrix factored
        using ``*LSFACTOR``.

        You can use the ``*DMAT,,,COPY`` (or ``*VEC,,,COPY``) command to copy the load
        vector to the solution vector in order to predefine it with the
        appropriate size.
        """
        command = f"*LSBAC,{enginename},{rhsvector},{solvector}"
        return self.run(command, **kwargs)

    def lsdump(self, enginename="", filename="", **kwargs):
        """Dumps a linear solver engine to a binary File.

        APDL Command: ``*LSDUMP``

        Parameters
        ----------
        enginename
            Name used to identify this engine. Must have been previously
            created using ``*LSENGINE`` and factorized using ``*LSFACTOR``.

        filename
            Name of the file to create.

        Notes
        -----
        Dumps a previously factorized linear solver system to a binary file.
        Only LAPACK and BCS linear solvers can be used with this feature. The
        Linear Solver can later be restored with the ``*LSRESTORE`` command.

        A BCS Sparse Solver can be dumped only if uses the INCORE memory option
        (see BCSOPTION).
        """
        command = f"*LSDUMP,{enginename},{filename}"
        return self.run(command, **kwargs)

    def lsengine(self, type_="", enginename="", matrix="", option="", **kwargs):
        """Creates a linear solver engine.

        APDL Command: ``*LSENGINE``

        Parameters
        ----------
        type_
            Specifies the algorithm to be used:

            * ``"BCS"`` - Boeing sparse solver (default if applied to
                        sparse matrices).

            * ``"DSS"`` : MKL sparse linear solver (Intel Windows and
                        Linux systems only).

            * ``"LAPACK"`` : LAPACK dense matrix linear solver (default if
                           applied to dense matrices).

            * ``"DSP"`` : Distributed sparse solver.

        enginename
            Name used to identify this engine. Must be specified.

        matrix
            Name of the matrix to solve.

        option
            Option to control the memory mode of the DSS solver (used only
            if ``type='dss'``):

            * ``"INCORE"`` : In-core memory mode

            * ``"OUTOFCORE"`` : Out-of-core memory mode

        Notes
        -----
        This command creates a linear solver engine.

        The BCS, DSS, and DSP solvers can only be used with sparse matrices.
        For dense matrices, use the LAPACK solver.
        """
        command = f"*LSENGINE,{type_},{enginename},{matrix},{option}"
        return self.run(command, **kwargs)

    def lsfactor(self, enginename="", option="", **kwargs):
        """Performs the numerical factorization of a linear solver system.

        APDL Command: ``*LSFACTOR``

        Parameters
        ----------
        enginename
            Name used to identify this engine. Must have been previously
            created using ``*LSENGINE``.

        option
            Option to invert the matrix, used only with an LAPACK engine
            (``*LSENGINE,LAPACK``):

        Notes
        -----
        Performs the computationally intensive, memory intensive factorization
        of a matrix specified by ``*LSENGINE``, using the solver engine also
        specified by ``*LSENGINE``.
        """
        command = f"*LSFACTOR,{enginename},{option}"
        return self.run(command, **kwargs)

    def lsrestore(self, enginename="", filename="", **kwargs):
        """Restores a linear solver engine from a binary file.

        APDL Command: ``*LSRESTORE``

        Parameters
        ----------
        enginename
            Name used to identify this engine.

        filename
            Name of the file to read from.

        Notes
        -----
        Restores a previously dumped Linear Solver (see the ``*LSDUMP`` command).
        This Linear Solver can be used to solve a linear system using the
        ``*LSBAC`` command.
        """
        command = "*LSRESTORE,%s,%s" % (str(enginename), str(filename))
        return self.run(command, **kwargs)

    def merge(self, name1="", name2="", val1="", val2="", **kwargs):
        """Merges two dense matrices or vectors into one.

        APDL Command: ``*MERGE``

        Parameters
        ----------
        name1
            Name of the matrix or vector to extend.

        name2
            Name of the matrix or vector to be merged into ``name1``.

        val1
            If ``name1`` refers to a dense matrix created by the ``*DMAT``
            command then the column or row number indicating where the new values
            are to be inserted into the Name1 matrix.

            If ``name` refers to a vector created by ``*VEC`` then this is the
            row number indicating where the new values are to be inserted
            into the ``name1`` vector.

        val2
            Specifies how the ``name2`` matrix or vector is copied into
            the ``name1`` matrix.

            * ``"COL"`` : Insert the new values at the column location
              specified by ``val1`` (default).
            * ``"row"`` : Insert the new values at the row location
              specified by ``val1``.

        Notes
        -----
        ``merge`` can be used to add new columns or rows to a dense matrix
        that was created by the ``*DMAT`` command. In this case, ``name1`` must
        be the name of the dense matrix and ``name2`` must refer to a vector
        or another dense matrix.

        ``*MERGE`` can also be used to add new rows to a vector that was
         created by the ``*VEC`` command. In this case, ``name1`` and
         ``name2`` must both refer to vectors.

        In all cases, the values of the original matrix or vector are
        retained, and the matrix or vector is resized to accommodate the
        additional rows or columns.
        """
        return self.run(f"MERGE,{name1},{name2},{val1},{val2}", **kwargs)

    def mult(self, m1="", t1="", m2="", t2="", m3="", **kwargs):
        """Performs the matrix multiplication ``M3 = M1(T1)*M2(T2)``.

        APDL Command: ``*MULT``

        Parameters
        ----------
        m1
            Name of matrix M1. Must have been previously specified by a ``*DMAT``
            or ``*SMAT`` command.

        t1
            Transpose key. Set T1 = TRANS to use the transpose of M1. If blank,
            transpose will not be used.

        m2
            Name of matrix M2. Must have been previously specified by a ``*DMAT``
            command.

        t2
            Transpose key. Set T2 = TRANS to use the transpose of M2. If blank,
            transpose will not be used.

        m3
            Name of resulting matrix, M3. Must be specified.

        Notes
        -----
        The matrices must be dimensionally consistent such that the number of
        columns of M1 (or the transposed matrix, if requested) is equal to the
        number of rows of M2 (or the transposed matrix, if requested).

        You cannot multiply two sparse matrices with this command (that is, M1
        and M2 cannot both be sparse). The resulting matrix, M3, will always be
        a dense matrix, no matter what combination of input matrices is used
        (dense*sparse, sparse*dense, or dense*dense).
        """
        command = f"*MULT,{m1},{t1},{m2},{t2},{m3}"
        return self.run(command, **kwargs)

    def nrm(self, name="", normtype="", parr="", normalize="", **kwargs):
        """Computes the norm of the specified matrix or vector.

        APDL Command: ``*NRM``

        Parameters
        ----------
        name
            Matrix or vector for which the norm will be computed. This
            can be a dense matrix (created by the ``*DMAT`` command),
            a sparse matrix (created by the ``*SMAT`` command) or a
            vector (created by the ``*VEC`` command)

        normtype
            Mathematical norm to use:

            - L2 (Euclidean or SRSS) norm (default).
            - L1 (absolute sum) norm (vectors only).

        parr
            Parameter name that contains the result.

        normalize
            Normalization key; to be used only for vectors created by ``*VEC``:

            Normalize the vector such that the norm is 1.0. - Do not
            normalize the vector (default).

        Notes
        -----
        The NRM2 option corresponds to the Euclidean or L2 norm and is
        applicable to either vectors or matrices. The NRM1 option corresponds
        to the L1 norm and is applicable to vectors only. The NRMINF option is
        the maximum norm and is applicable to either vectors or matrices.
        """
        if not parr:
            parr = "__temp_par__"
        command = f"*NRM,{name},{normtype},{parr},{normalize}"
        self.run(command, **kwargs)
        return self.parameters[parr]

    def remove(self, name="", val1="", val2="", val3="", **kwargs):
        """Suppresses rows or columns of a dense matrix or a vector.

        APDL Command: ``*REMOVE``

        Parameters
        ----------
        name
            Name of the matrix or vector to be revised.

        val1
            First row or column number to suppress if ``name`` is a dense
            matrix.  First value index to suppress if ``name`` is a
            vector.

        Val2
            Last row or column number to suppress if ``name`` is a dense
            matrix.  Last value index to suppress if ``name`` is a
            vector.

        Val3
            Specifies what to remove if ``name`` is a dense matrix.

            * ``"COL"`` : Remove columns of the matrix (default).

            * ``"ROW"`` : Remove rows of the matrix.

        Notes
        -----
        The values of the original matrix or vector specified by Name are
        retained. The matrix or vector is resized to the new number of
        rows and columns.
        """
        return self.run(f"REMOVE,{name},{val1},{val2},{val3}", **kwargs)

    def scal(self, name="", val1="", val2="", **kwargs):
        """Scales a vector or matrix by a constant or a vector.

        APDL Command: ``*SCAL``

        Parameters
        ----------
        name
            Name used to identify the vector or matrix to be scaled. Must
            be specified.

        val1
            When scaling a matrix or a vector by a scalar value, Val1 is
            the real part of the constant to use (default = 1).

            When scaling a matrix or a vector by a vector, Val1 is the
            name of the vector used for the scaling operation.

        val2
            The imaginary part of the constant to use (default = 0).
            This value is used only if the vector or matrix specified by
            Name is complex.

            val2 is only valid for scaling by a constant. It is not
            used when scaling by a vector.

        Notes
        -----
        This command can be applied to vectors and matrices created by the
        ``*VEC``, ``*DMAT`` and ``*SMAT`` commands.

        Data types must be consistent between the vectors and matrices
        being scaled and the scaling vector (or constant value).

        When scaling a matrix with a vector, the matrix must be square
        and the scaling vector must be the same size.

        Scaling a matrix with a vector, is available only on
        MAPDL V23.2 and greater.

        """
        return self.run(f"*SCAL,{name},{val1},{val2}", **kwargs)

    def smat(
        self,
        matrix="",
        type_="",
        method="",
        val1="",
        val2="",
        val3="",
        val4="",
        **kwargs,
    ):
        """Creates a sparse matrix.

        APDL Command: ``*SMAT``

        Parameters
        ----------
        matrix
            Name used to identify the matrix. Must be specified.

        type\_
            Matrix type:

            Double precision real values (default). - Complex double precision values.

        method
            Method used to create the matrix:

            Copy an existing matrix. - Import the matrix from a file.

        val1, val2, val3, val4
            Additional input. The meaning of Val1 through Val3 will
            vary depending on the specified Method. See in your ansys
            documentation.

        Notes
        -----
        Use the ``*DMAT`` command to create a dense matrix.

        Unlike the ``*DMAT`` command, the ``*SMAT`` command cannot be used to allocate
        a sparse matrix.

        For more information on the NOD2BCS and USR2BCS mapping vectors, see
        Degree of Freedom Ordering in the ANSYS Parametric Design Language
        Guide.

        For more information about .FULL file contents, see the HBMAT in the
        Command Reference.
        """
        command = f"*SMAT,{matrix},{type_},{method},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def starprint(self, matrix="", fname="", **kwargs):
        """Prints the matrix values to a file.

        APDL Command: ``*PRINT``

        Parameters
        ----------
        matrix
            Name of matrix or vector to print. Must be specified.

        fname
            File name. If blank, matrix is written to the output file.

        Notes
        -----
        The matrix may be a dense matrix (``*DMAT``), a sparse matrix
        (``*SMAT``), or a vector (``*VEC``). Only the non-zero entries
        of the matrix are printed.
        """
        command = f"*PRINT,{matrix},{fname}"
        return self.run(command, **kwargs)

    def sort(self, **kwargs):
        """Specifies "Sort settings" as the subsequent status topic.

        APDL Command: SORT

        Notes
        -----
        This is a status [STAT] topic command.  Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.
        """
        command = f"SORT,"
        return self.run(command, **kwargs)

    def vec(
        self,
        vector="",
        type_="",
        method="",
        val1="",
        val2="",
        val3="",
        val4="",
        **kwargs,
    ):
        """Creates a vector.

        APDL Command: ``*VEC``

        Parameters
        ----------
        vector
            Name used to identify the vector. Must be specified.

        type_
            Vector type:

            * ``"D"`` : Double precision real values (default).

            * ``"Z"`` : Complex double precision values.

            * ``"I"`` : Integer values.

        method
            Method used to create the vector:

            * ``"ALLOC"`` : Allocate space for a vector (default).

            * ``"RESIZE"`` : Resize an existing vector to a new
              length. Values are kept from the original vector. If the
              length specified by Val1 is greater than the original vector
              length, the additional rows are assigned a value of zero.

            * ``"COPY"`` : Copy an existing vector.

            * ``"IMPORT"`` : Import the vector from a file.

            * ``"LINK"`` : Link to a column of an existing dense ``*DMAT``
              matrix and use it in subsequent vector calculations. Any
              changes to the vector are also made to the corresponding
              matrix column (memory is shared).

            Copy an existing vector. - Import the vector from a file.

        val1, val2, val3, val4, val5
            Additional input. The meaning of ``val1`` through ``val5`` will vary
            depending on the specified Method.  See:
            https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_VEC.html

        Notes
        -----
        Use the ``*DMAT`` command to create a matrix.

        For more information on the BACK and FORWARD nodal mapping vectors, see
        Degree of Freedom Ordering in the ANSYS Parametric Design Language
        Guide.
        """
        command = f"*VEC,{vector},{type_},{method},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def wrk(self, num="", **kwargs):
        """Sets the active workspace number.

        APDL Command: ``*WRK``

        Parameters
        ----------
        num
            Number of the active memory workspace for APDLMath vector and
            matrices. All the following APDLMath vectors and matrices will
            belong to this memory workspace, until the next call to the ``*WRK``
            command. By default, all the APDLMath objects belong to workspace
            number 1.

        Notes
        -----
        This feature enables you to associate a set of vector and matrices in a
        given memory workspace, so that you can easily manage the free step:

        This feature can be useful to free all the temporary APDLMath variables
        inside a MACRO in one call.
        """
        command = "*WRK,%s" % (str(num))
        return self.run(command, **kwargs)
