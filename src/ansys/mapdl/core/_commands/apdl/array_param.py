class ArrayParam:
    def mfouri(self, oper="", coeff="", mode="", isym="", theta="", curve="", **kwargs):
        """Calculates the coefficients for, or evaluates, a Fourier series.

        APDL Command: ``*MFOURI``

        Parameters
        ----------
        oper
            Type of Fourier operation:

            Calculate Fourier coefficients COEFF from MODE, ISYM,
            THETA, and CURVE. - Evaluate the Fourier curve CURVE from
            COEFF, MODE, ISYM and THETA.

        coeff
            Name of the array parameter vector containing the Fourier
            coefficients (calculated if Oper = FIT, required as input if Oper =
            EVAL).  See ``*SET`` for name restrictions.

        mode
            Name of the array parameter vector containing the mode numbers of
            the desired Fourier terms.

        isym
            Name of the array parameter vector containing the symmetry key for
            the corresponding Fourier terms.  The vector should contain keys
            for each term as follows:

            Symmetric (cosine) term - Antisymmetric (sine) term.

        theta, curve
            Names of the array parameter vectors containing the theta vs. curve
            description, respectively.  Theta values should be input in
            degrees.  If Oper = FIT, one curve value should be supplied with
            each theta value.  If Oper = EVAL, one curve value will be
            calculated for each theta value.

        Notes
        -----
        Calculates the coefficients of a Fourier series for a given
        curve, or evaluates the Fourier curve from the given (or
        previously calculated) coefficients.  The lengths of the
        COEFF, MODE, and ISYM vectors must be the same--typically two
        times the number of modes desired, since two terms (sine and
        cosine) are generally required for each mode.  The lengths of
        the CURVE and THETA vectors should be the same or the smaller
        of the two will be used.  There should be a sufficient number
        of points to adequately define the curve--at least two times
        the number of coefficients.  A starting array element number
        (1) must be defined for each array parameter vector.

        The vector specifications ``*VLEN``, ``*VCOL``, ``*VABS``,
        ``*VFACT``, and ``*VCUM`` do not apply to this command.  Array
        elements should not be skipped with the ``*VMASK`` and the
        NINC value of the ``*VLEN`` specifications.  The vector being
        calculated (COEFF if Oper is FIT, or CURVE if Oper is EVAL)
        must exist as a dimensioned array [``*DIM``].

        This command is valid in any processor.
        """
        command = f"*MFOURI,{oper},{coeff},{mode},{isym},{theta},{curve}"
        return self.run(command, **kwargs)

    def mfun(self, parr="", func="", par1="", **kwargs):
        """Copies or transposes an array parameter matrix.

        APDL Command: ``*MFUN``

        Parameters
        ----------
        parr
            The name of the resulting array parameter matrix.  See ``*SET`` for
            name restrictions.

        func
            Copy or transpose function:

            Par1 is copied to ParR - Par1 is transposed to ParR.  Rows
            (m) and columns (n) of Par1 matrix are transposed to
            resulting ParR matrix of shape (n,m).

        par1
            Array parameter matrix input to the operation.

        Notes
        -----
        Operates on one input array parameter matrix and produces one output
        array parameter matrix according to:

        ParR = f(Par1)

        where the function (f) is either a copy or transpose, as described
        above.

        Functions are based on the standard FORTRAN definitions where
        possible.  ParR may be the same as Par1.  Starting array
        element numbers must be defined for each array parameter
        matrix if it does not start at the first location. For
        example, ``*MFUN,A(1,5),COPY,B(2,3)`` copies matrix B
        (starting at element (2,3)) to matrix A (starting at element
        (1,5)).  The diagonal corner elements for each submatrix must
        be defined: the upper left corner by the array starting
        element (on this command), the lower right corner by the
        current values from the ``*VCOL`` and ``*VLEN`` commands.  The
        default values are the (1,1) element and the last element in
        the matrix.  No operations progress across matrix planes (in
        the 3rd dimension).  Absolute values and scale factors may be
        applied to all parameters [``*VABS``, ``*VFACT``].  Results
        may be cumulative [``*VCUM``].

        Array elements should not be skipped with the ``*VMASK`` and the
        NINC value of the ``*VLEN`` specifications.  The number of
        rows [``*VLEN``] applies to the Par1 array.  See the
        ``*VOPER`` command for details.

        This command is valid in any processor.
        """
        command = f"*MFUN,{parr},{func},{par1}"
        return self.run(command, **kwargs)

    def moper(
        self,
        parr="",
        par1="",
        oper="",
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        val6="",
        **kwargs,
    ):
        """Performs matrix operations on array parameter matrices.

        APDL Command: ``*MOPER``

        Parameters
        ----------
        parr
            The name of the resulting array parameter matrix.  See ``*SET`` for
            name restrictions.

        par1
            First array parameter matrix input to the operation. For ``Oper =
            MAP``, this is an ``N`` x 3 array of coordinate locations at which to
            interpolate. ``ParR`` will then be an ``N(out)`` x ``M`` array containing the
            interpolated values.

        oper
            Matrix operations:

            * `INVERT` - ``(*MOPER, ParR, Par1, INVERT)``
              Square matrix invert: Inverts the ``n`` x ``n`` matrix in ``Par1``
              into ``ParR``. The matrix must be well conditioned.

              **Warning**: Non-independent or ill-conditioned equations can
              cause erroneous results. - For large matrices, use the
              APDL Math operation ``*LSFACTOR`` for efficiency (see APDL
              Math).

            * `MULT` - ``(*MOPER, ParR, Par1, MULT, Par2)``
              Matrix multiply: Multiplies ``Par1`` by ``Par2``.  The number of
              rows of ``Par2`` must equal the number of columns of ``Par1`` for
              the operation. If ``Par2`` is input with a number of rows
              greater than the number of columns of ``Par1``, matrices are
              still multiplied. However, the operation only uses a
              number of rows of ``Par2`` equal to the number of columns of
              ``Par1``.

            * `COVAR` - ``(*MOPER, ParR, Par1, COVAR, Par2)``
              Covariance: The measure of association between two columns
              of the input matrix (``Par1``).  ``Par1``, of size m runs (rows)
              by ``n`` data (columns) is first processed to produce a row
              vector containing the mean of each column which is
              transposed to a column vector (``Par2``) of n array elements.
              The ``Par1`` and ``Par2`` operation then produces a resulting ``n`` x
              ``n`` matrix (``ParR``) of covariances (with the variances as the
              diagonal terms).

            * `CORR` - ``(*MOPER, ParR, Par1, CORR, Par2)``
              Correlation: The correlation coefficient between two
              variables.  The input matrix (``Par1``), of size m runs (rows)
              by n data (columns), is first processed to produce a row
              vector containing the mean of each column which is then
              transposed to a column vector (``Par2``) of n array elements.
              The ``Par1`` and ``Par2`` operation then produces a resulting ``n`` x
              ``n`` matrix (``ParR``) of correlation coefficients (with a value
              of 1.0 for the diagonal terms).

            * `SOLV` - ``(*MOPER, ParR, Par1, SOLV, Par2)``
              Solution of simultaneous equations: Solves the set of ``n``
              equations of n terms of the form ``an_1 x_1 + an_2 x_2 + ... +
              an_n x_n = b_n`` where ``Par1`` contains the matrix of
              a-coefficients, ``Par2`` the vector(s) of b-values, and ``ParR``
              the vector(s) of x-results.  ``Par1`` must be a square matrix.
              The equations must be linear, independent, and well
              conditioned.

              **Warning**: Non-independent or ill-conditioned equations can
              cause erroneous results. - For large matrices, use the
              APDL Math operation ``*LSFACTOR`` for efficiency (see APDL
              Math).

            * `SORT` - ``(*MOPER, ParR, Par1, SORT, Par2, n1, n2, n3)``
              Matrix sort: Sorts matrix ``Par1`` according to sort vector
              ``Par2`` and places the result back in ``Par1``. Rows of ``Par1`` are
              moved to the corresponding positions indicated by the
              values of ``Par2``. ``Par2`` may be a column of ``Par1`` (in which
              case it will also be reordered). Alternatively, you may
              specify the column of ``Par1`` to sort using n1 (leaving ``Par2``
              blank). A secondary sort can be specified by column ``n2``,
              and a third sort using ``n3``. ``ParR`` is the vector of initial
              row positions (the permutation vector).  Sorting ``Par1``
              according to ``ParR`` should reproduce the initial ordering.

            * `NNEAR` - ``(*MOPER, ParR, Par1, NNEAR, Toler)``
              Nearest Node: Quickly determine all the nodes within a
              specified tolerance of a given array.  ``ParR`` is a vector of
              the nearest selected nodes, or 0 if no nodes are nearer
              than ``Toler``. ``Par1`` is the ``n`` x 3 array of coordinate
              locations. ``Toler`` defaults to 1 and is limited to the
              maximum model size.

            * `ENEAR` - ``(*MOPER, ``ParR``, ``Par1``, ENEAR, Toler)``
              Nearest Element: Quickly determine the elements with
              centroids that are within a specified tolerance of the
              points in a given array. - ``ParR`` is a vector of the nearest
              selected elements, or 0 if no element centroids are nearer
              than ``Toler``. ``Par1`` is the ``n`` x 3 array of coordinate
              locations.

            * `MAP` - ``(*MOPER, ParR, Par1, MAP, Par2, Par3, kDim, --, kOut, LIMIT)``
              Maps the results from one set of points to another. For
              example, you can map pressures from a CFD analysis onto
              your model for a structural analysis.

              * ``Par1`` is the ``Nout`` x 3 array of points that will be mapped
                to. ``Par2`` is the ``Nin`` x ``M`` array that contains ``M`` values of
                data to be interpolated at each point and corresponds to
                the ``Nin`` x 3 points in ``Par3``. The resulting ``ParR`` is the ``Nout``
                x ``M`` array of mapped data points.

                For each point in the destination mesh, all possible
                triangles in the source mesh are searched to find the best
                triangle containing each point. It then does a linear
                interpolation inside this triangle. You should carefully
                specify your interpolation method and search criteria in
                order to provide faster and more accurate results (see
                ``LIMIT``, below).

              * ``kDim`` is the interpolation criteria. If ``kDim = 2 or 0``, two
                dimensional interpolation is applied (interpolate on a
                surface). If ``kDim = 3``, three dimensional interpolation is
                applied (interpolate on a volume).

              * ``kOut`` specified how points outside of the domain are
                handled. If ``kOut`` = 0, use the value(s) of the nearest
                region point for points outside of the region. If ```kOut``` =
                1, set results outside of the region to zero.

            * `LIMIT` specifies the number of nearby points considered for
              interpolation. The default is 20, and the minimum is
              5. Lower values will reduce processing time; however, some
              distorted or irregular sets of points will require a
              higher ``LIMIT`` value to encounter three nodes for
              triangulation.

              Output points are incorrect if they are not within the
              domain (area or volume) defined by the specified input
              points. Also, calculations for out-of-bound points require
              much more processing time than do points that are within
              bounds. Results mapping is available from the command line
              only.

            * `INTP` - ``(*MOPER, ParR, Par1, INTP, Par2)``
              Finds the elements that contain each point in the array of
              ``n`` x 3 points in ``Par1``. ``Par2`` will contain the set of element
              ID numbers and ``ParR`` will contain their ``n`` x 3 set of
              natural element coordinates (values between -1 and
              1). ``Par1`` must be in global Cartesian coordinates.

            * `SGET` - ``(*MOPER, ParR, Par1, SGET, Par2, Label, Comp)``
              Gets the nodal solution item corresponding to Label and
              Comp (see the PLNSOL command) and interpolates it to the
              given element locations. ``Par1`` contains the ``n`` x 3 array of
              natural element coordinates (values between -1 and 1) of
              the ``n`` element ID numbers in ``Par2``. ``Par1`` and ``Par2`` are
              usually the output of the ``*MOPER,,,INTP`` operation. ``ParR``
              contains the ``n`` interpolated results.

            * ``Val1, Val2, ..., Val6``
              Additional input used in the operation. The meanings of
              ``Val1`` through ``Val6`` vary depending on the specified matrix
              operation. See the description of Oper for details.
        """
        command = (
            f"*MOPER,{parr},{par1},{oper},{val1},{val2},{val3},{val4},{val5},{val6}"
        )
        return self.run(command, **kwargs)

    def mwrite(
        self, parr="", fname="", ext="", label="", n1="", n2="", n3="", **kwargs
    ):
        """Writes a matrix to a file in a formatted sequence.

        APDL Command: ``*MWRITE``

        Parameters
        ----------
        parr
            The name of the array parameter. See ``*SET`` for name restrictions.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        label
            Can use a value of ``IJK``, ``IKJ``, ``JIK``, ``JKI``, ``KIJ``, ``KJI``, or blank (``JIK``).

        n1, n2, n3
            Write as ``(((ParR(i,j,k), k = 1,n1), i = 1, n2), j = 1, n3)`` for
            ``Label = KIJ``. ``n1``, ``n2``, and ``n3`` default to the corresponding dimensions
            of the array parameter ParR.

        Notes
        -----
        Writes a matrix or vector to a specified file in a formatted sequence.
        You can also use the ``*VWRITE`` command to write data to a specified file.
        Both commands contain format descriptors on the line immediately
        following the command. The format descriptors can be in either Fortran
        or C format.

        Fortran format descriptors are enclosed in parentheses. They must
        immediately follow the ``*MWRITE`` command on a separate line of the same
        input file. The word FORMAT should not be included. The format must
        specify the number of fields to be written per line, the field width,
        the placement of the decimal point, etc. There should be one field
        descriptor for each data item written. The write operation uses the
        available system FORTRAN FORMAT conventions (see your system FORTRAN
        manual). Any standard FORTRAN real format (such as (4F6.0),
        (E10.3,2X,D8.2), etc.) and character format (A) may be used.  Integer
        (I) and list-directed (``*``) descriptors may not be used. Text may be
        included in the format as a quoted string. The FORTRAN descriptor must
        be enclosed in parentheses and the format must not exceed 80 characters
        (including parentheses).

        The "C" format descriptors are used if the first character of the
        format descriptor line is not a left parenthesis. "C" format
        descriptors may be up to 80 characters long, consisting of text strings
        and predefined "data descriptors" between the strings where numeric or
        alphanumeric character data are to be inserted. The normal descriptors
        are %I for integer data, %G for double precision data, %C for
        alphanumeric character data, and %/ for a line break. There must be one
        data descriptor for each specified value in the order of the specified
        values. The enhanced formats described in ``*MSG`` may also be used.

        The starting array element number must be defined. Looping continues in
        the directions indicated by the Label argument. The number of loops and
        loop skipping may also be controlled with the ``*VLEN`` and ``*VMASK``
        commands, which work in the n2 direction (by row on the output file),
        and by  the ``*VCOL`` command, which works in the n1 direction (by column
        in the output file).  The vector specifications ``*VABS`` and ``*VFACT`` apply
        to this command, while ``*VCUM`` does not apply to this command. See the
        ``*VOPER`` command for details. If you are in the GUI, the ``*MWRITE`` command
        must be contained in an externally prepared file and read into ANSYS
        (i.e., ``*USE``, ``/INPUT``, etc.).

        This command is valid in any processor.
        """
        command = f"*MWRITE,{parr},{fname},{ext},,{label},{n1},{n2},{n3}"
        return self.run(command, **kwargs)

    def starvput(
        self,
        parr="",
        entity="",
        entnum="",
        item1="",
        it1num="",
        item2="",
        it2num="",
        kloop="",
        **kwargs,
    ):
        """Restores array parameter values into the ANSYS database.

        APDL Command: ``*VPUT``

        Parameters
        ----------
        parr
            The name of the input vector array parameter.  See ``*SET`` for name
            restrictions.  The parameter must exist as a dimensioned array
            [``*DIM``] with data input.

        entity
            Entity keyword.  Valid keywords are shown for Entity = in the table
            below.

        entnum
            The number of the entity (as shown for ENTNUM= in the table below).

        item1
            The name of a particular item for the given entity.  Valid items
            are as shown in the Item1 columns of the table below.

        it1num
            The number (or label) for the specified Item1 (if any).  Valid
            IT1NUM values are as shown in the IT1NUM columns of the table
            below.  Some Item1 labels do not require an IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify the item
            for which data is to be stored.  Most items do not require this
            level of information.

        kloop
            Field to be looped on:

            Loop on the ENTNUM field (default). - Loop on the Item1 field.

            Loop on the IT1NUM field.  Successive items are as shown with IT1NUM. - Loop on the Item2 field.

        Notes
        -----
        The ``*VPUT`` command is not supported for PowerGraphics
        displays.  Inconsistent results may be obtained if this
        command is not used in /GRAPHICS, FULL.

        Plot and print operations entered via the GUI (Utility Menu>
        Pltcrtls, Utility Menu> Plot) incorporate the AVPRIN
        command. This means that the principal and equivalent values
        are recalculated. If you use ``*VPUT`` to put data back into
        the database, issue the plot commands from the command line to
        preserve your data.

        This operation is basically the inverse of the ``*VGET``
        operation.  Vector items are put directly (without any
        coordinate system transformation) into the ANSYS database.
        Items can only replace existing items of the database and not
        create new items.  Degree of freedom results that are replaced
        in the database are available for all subsequent
        postprocessing operations.  Other results are changed
        temporarily and are available mainly for the immediately
        following print and display operations.  The vector
        specification ``*VCUM`` does not apply to this command.  The
        valid labels for the location fields (Entity, ENTNUM, Item1,
        and IT1NUM) are listed below.  Item2 and IT2NUM are not
        currently used.  Not all items from the ``*VGET`` list are
        allowed on ``*VPUT`` since putting values into some locations
        could cause the database to be inconsistent.

        This command is valid in any processor.

        """
        command = (
            f"*VPUT,{parr},{entity},{entnum},{item1},{it1num},{item2},{it2num},{kloop}"
        )
        return self.run(command, **kwargs)

    def sread(
        self,
        strarray="",
        fname="",
        ext="",
        nchar="",
        nskip="",
        nread="",
        **kwargs,
    ):
        """Reads a file into a string array parameter.

        APDL Command: ``*SREAD``

        Parameters
        ----------
        strarray
            Name of the "string array" parameter which will hold the read file.
            String array parameters are similar to character arrays, but each
            array element can be as long as 128 characters. If the string
            parameter does not exist, it will be created. The array will be
            created as: ``*DIM,StrArray,STRING,nChar,nRead```

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        nchar
            Number of characters per line to read (default is length of the
            longest line in the file).

        nskip
            Number of lines to skip at the start of the file (default is 0).

        nread
            Number of lines to read from the file (default is the entire file).

        Notes
        -----
        The ``*SREAD`` command reads from a file into a string array
        parameter. The file must be an ASCII text file.
        """
        command = f"*SREAD,{strarray},{fname},{ext},,{nchar},{nskip},{nread}"
        return self.run(command, **kwargs)

    def toper(
        self,
        parr="",
        par1="",
        oper="",
        par2="",
        fact1="",
        fact2="",
        con1="",
        **kwargs,
    ):
        """Operates on table parameters.

        APDL Command: ``*TOPER``

        Parameters
        ----------
        parr
            Name of the resulting table parameter. The command will create a
            table array parameter with this name.  Any existing parameter with
            this name will be overwritten.

        par1
            Name of the first table parameter.

        oper
            The operation to be performed: ``ADD``.  The operation is:
            ``ParR(i,j,k) = FACT1*Par1(i,j,k) + FACT2 *Par2(i,j,k) +CON1``

        par2
            Name of the second table parameter.

        fact1
            The first table parameter multiplying constant. Defaults to 1.

        fact2
            The second table parameter multiplying constant.  Defaults to 1.

        con1
            The constant increment for offset.  Defaults to 0.

        Notes
        -----
        ``*TOPER`` operates on table parameters according to:
        ``ParR(i,j,k) = FACT1*Par1(i,j,k) + FACT2 *Par2(i,j,k) +CON1``

        Par1 and Par2 must have the same dimensions and the same variable names
        corresponding to those dimensions. Par1 and Par2 must also have
        identical index values for rows, columns, etc.

        If you want a local coordinate system for the resulting array, you must
        dimension it as such using the ``*DIM`` command before issuing ``*TOPER``.

        This command is valid in any processor.
        """
        command = f"*TOPER,{parr},{par1},{oper},{par2},{fact1},{fact2},{con1}"
        return self.run(command, **kwargs)

    def vabs(self, kabsr="", kabs1="", kabs2="", kabs3="", **kwargs):
        """Applies the absolute value function to array parameters.

        APDL Command: ``*VABS``

        Parameters
        ----------
        kabsr
            Absolute value of results parameter:

            Do not take absolute value of results parameter (``ParR``). - Take absolute value.

        kabs1
            Absolute value of first parameter:

            Do not take absolute value of first parameter (``Par1`` or ``ParI``). - Take absolute value.

        kabs2
            Absolute value of second parameter:

            Do not take absolute value of second parameter (``Par2`` or ``ParJ``). - Take absolute value.

        kabs3
            Absolute value of third parameter:

            Do not take absolute value of third parameter (``Par3`` or ``ParK``). - Take absolute value.

        Notes
        -----
        Applies an absolute value to parameters used in certain  ``*VXX`` and ``*MXX``
        operations.  Typical absolute value applications are of the form:

        ``ParR = |f(|Par1|)|``

        or

        ``ParR = |(|Par1| o |Par2|)|``

        The absolute values are applied to each input parameter value before
        the operation and to the result value after the operation.  Absolute
        values are applied before the scale factors so that negative scale
        factors may be used.  The absolute value settings are reset to the
        default (no absolute value) after each ``*VXX`` or ``*MXX`` operation.  Use
        ``*VSTAT`` to list settings.

        This command is valid in any processor.
        """
        command = f"*VABS,{kabsr},{kabs1},{kabs2},{kabs3}"
        return self.run(command, **kwargs)

    def vcol(self, ncol1="", ncol2="", **kwargs):
        """Specifies the number of columns in matrix operations.

        APDL Command: ``*VCOL``

        Parameters
        ----------
        ncol1
            Number of columns to be used for Par1 with ``*MXX`` operations.
            Defaults to whatever is needed to fill the result array.

        ncol2
            Number of columns to be used for Par2 with ``*MXX`` operations.
            Defaults to whatever is needed to fill the result array.

        Notes
        -----
        Specifies the number of columns to be used in array parameter matrix
        operations.  The size of the submatrix used is determined from the
        upper left starting array element (defined on the operation command) to
        the lower right array element (defined by the number of columns on this
        command and the number of rows on the ``*VLEN`` command).

        The default NCOL is calculated from the maximum number of columns of
        the result array (the ``*DIM`` column dimension) minus the starting
        location + 1.  For example, ``*DIM,R,,1,10`` and a starting location of
        R(1,7) gives a default of 4 columns ( starting with R(1,7), R(1,8),
        R(1,9), and R(1,10)).  Repeat operations automatically terminate at the
        last column of the result array.  Existing values in the rows and
        columns of the results matrix remain unchanged where not overwritten by
        the requested input or operation values.

        The column control settings are reset to the defaults after each ``*MXX``
        operation.  Use ``*VSTAT`` to list settings.

        This command is valid in any processor.
        """
        command = f"*VCOL,{ncol1},{ncol2}"
        return self.run(command, **kwargs)

    def vcum(self, key="", **kwargs):
        """Allows array parameter results to add to existing results.

        APDL Command: ``*VCUM``

        Parameters
        ----------
        key
            Accumulation key:

            Overwrite results. - Add results to the current value of the results parameter.

        Notes
        -----
        Allows results from certain ``*VXX`` and ``*MXX`` operations to overwrite or
        add to existing results.  The cumulative operation is of the form:

        ``ParR = ParR + ParR(Previous)``

        The cumulative setting is reset to the default (overwrite) after each
        ``*VXX`` or ``*MXX`` operation.  Use ``*VSTAT`` to list settings.

        This command is valid in any processor.
        """
        command = f"*VCUM,{key}"
        return self.run(command, **kwargs)

    def vfact(self, factr="", fact1="", fact2="", fact3="", **kwargs):
        """Applies a scale factor to array parameters.

        APDL Command: ``*VFACT``

        Parameters
        ----------
        factr
            Scale factor applied to results (``ParR``) parameter.  Defaults to 1.0.

        fact1
            Scale factor applied to first parameter (``Par1`` or ``ParI``).  Defaults
            to 1.0.

        fact2
            Scale factor applied to second parameter (``Par2`` or ``ParJ``).  Defaults
            to 1.0.

        fact3
            Scale factor applied to third parameter (``Par3`` or ``ParK``).  Defaults
            to 1.0.

        Notes
        -----
        Applies a scale factor to parameters used in certain ``*VXX`` and ``*MXX``
        operations.   Typical scale factor applications are of the form:

        ``ParR = FACTR*f(FACT1*Par1)``

        or

        ``ParR = FACTR*((FACT1*Par1) o (FACT2*Par2))``

        The factors are applied to each input parameter value before the
        operation and to the result value after the operation.  The scale
        factor settings are reset to the default (1.0) after each ``*VXX`` or ``*MXX``
        operation.  Use ``*VSTAT`` to list settings.

        This command is valid in any processor.
        """
        command = f"*VFACT,{factr},{fact1},{fact2},{fact3}"
        return self.run(command, **kwargs)

    def vfun(self, parr="", func="", par1="", con1="", con2="", con3="", **kwargs):
        """Performs a function on a single array parameter.

        APDL Command: ``*VFUN``

        Parameters
        ----------
        parr
            The name of the resulting numeric array parameter vector.  See ``*SET``
            for name restrictions.

        func
            Function to be performed:

            * ACOS
              Arccosine: ``ACOS(Par1)``.

            * ``ASIN``
              Arcsine: ``ASIN(Par1)``.

            * ``ASORT``
              ``Par1`` is sorted in ascending order.  ``*VCOL``, ``*VMASK``,
              ``*VCUM``, and ``*VLEN,,NINC`` do not apply.
              ``*VLEN,NROW`` does apply.

            * ``ATAN``
              Arctangent: ``ATAN(Par1)``

            * ``COMP``
              Compress: Selectively compresses data set.  "True"
              (``*VMASK``) values of ``Par1`` (or row positions to be considered
              according to the ``NINC`` value on the ``*VLEN`` command) are
              written in compressed form to ``ParR``, starting at the
              specified position.

            * ``COPY``
              Copy: ``Par1`` copied to ``ParR``.

            * ``COS``
              Cosine: ``COS(Par1)``.

            * ``COSH``
              Hyperbolic cosine: ``COSH(Par1)``.

            * ``DIRCOS``
              Direction cosines of the principal stresses (nX9).  ``Par1``
              contains the nX6 component stresses for the ``n`` locations of
              the calculations.

            * ``DSORT``
              ``Par1`` is sorted in descending order.
              ``*VCOL``, ``*VMASK``, ``*VCUM``, and ``*VLEN,,NINC`` do not apply.
              ``*VLEN,NROW`` does apply.

            * ``EURLER``
              Euler angles of the principal stresses (nX3).  ``Par1``
              contains the nX6 component stresses for the ``n`` locations of
              the calculations.

            * ``EXP``
              Exponential: ``EXP(Par1)``.

            * ``EXPA``
              Expand: Reverse of the COMP function.  All elements of
              ``Par1`` (starting at the position specified) are written in
              expanded form to corresponding "true" (``*VMASK``) positions
              (or row positions to be considered according to the ``NINC``
              value on the ``*VLEN`` command) of ``ParR``.

            * ``LOG``
              Natural logarithm: ``LOG(Par1)``.

            * ``LOG10``
              Common logarithm: ``LOG10(Par1)``.

            * ``NINT``
              Nearest integer: 2.783 becomes 3.0, -1.75 becomes -2.0.

            * ``NOT``
              Logical complement: values 0.0 (false) become 1.0 (true).
              Values > 0.0 (true) become 0.0 (false).

            * ``PRIN``
              Principal stresses (nX5). ``Par1`` contains the ``nX6`` component stresses
              for the ``n`` locations of the calculations.

            * ``PWR``
              Power function: ``Par1**CON1``. Exponentiation of any negative
              number in the vector ``Par1`` to a non-integer power is
              performed by exponentiating the positive number and
              prepending the minus sign. For example, ``-4**2.3`` is
              ``-(4**2.3)``.

            * ``SIN``
              Sine: ``SIN(Par1)``

            * ``SINH``
              Hyperbolic sine: ``SINH(Par1)``.

            * ``SQRT``
              Square root: ``SQRT(Par1)``.

            * ``TAN``
              Tangent: ``TAN(Par1)``.

            * ``TANH``
              Hyperbolic tangent: ``TANH(Par1)``.

            * ``TANG``
              Tangent to a path at a point: the slope at a point is determined by linear interpolation half
              way between the previous and next points. Points are assumed to be in the global Cartesian
              coordinate system. Path points are specified in array ``Par1`` (having 3 consecutive columns
              of data, with the columns containing the ``x``, ``y``, and ``z`` coordinate locations, respectively, of
              the points). Only the starting row index and the column index for the x coordinates are
              specified, such as ``A(1,1)``. The y and z coordinates of the vector are assumed to begin in the
              corresponding next columns, such as ``A(1,2)`` and ``A(1,3)``. The tangent result, ``ParR``, must also
              have 3 consecutive columns of data and will contain the tangent direction vector (normalized
              to 1.0); such as 1,0,0 for an x-direction vector.

            * ``NORM``
              Normal to a path and an input vector at a point: determined from the cross-product of the
              calculated tangent vector (see ``TANG``) and the input direction vector (with the ``i``,
              ``j``, and ``k`` components input as ``CON1``, ``CON2``, and ``CON3``).
              Points are assumed to be in the global Cartesian coordinate system.
              Path points are specified in array ``Par1`` (having 3 consecutive
              columns of data, with the columns containing the ``x``, ``y``, and ``z``
              coordinate locations, respectively, of the points).
              Only the starting row index and the column index for the ``x`` coordinates
              are specified, such as ``A(1,1)``. The ``y`` and ``z`` coordinates of the vector are assumed to begin
              in the corresponding next columns, such as ``A(1,2)`` and ``A(1,3)``. The normal result, ``ParR``,
              must also have 3 consecutive columns of data and will contain the normal direction vector
              (normalized to 1.0); such as ``1,0,0`` for an x-direction vector

            * ``LOCAL``
              Transforms global Cartesian coordinates of a point to the coordinates of a specified system:
              points to be transformed are specified in array ``Par1`` (having 3 consecutive columns of
              data, with the columns containing the ``x``, ``y``, and ``z`` global Cartesian coordinate locations,
              respectively, of the points).
              Only the starting row index and the column index for the ``x``
              coordinates are specified, such as ``A(1,1)``.
              The y and z coordinates of the vector are assumed
              to begin in the corresponding next columns, such as ``A(1,2)`` and ``A(1,3)``.
              Results are transformed to coordinate system ``CON1`` (which may be any valid coordinate system number,
              such as 1,2,11,12, etc.). The transformed result, ``ParR``, must also have 3 consecutive columns
              of data and will contain the corresponding transformed coordinate locations.

            * ``GLOBAL``
              Transforms specified coordinates of a point to global Cartesian coordinates: points to be
              transformed are specified in array ``Par1`` (having 3 consecutive columns of data, with the
              columns containing the local coordinate locations (``x``, ``y``, ``z`` or ``r``, ``θ``, ``z``
              or etc.) of the points).
              Only the starting row index and the column index for the x coordinates are specified, such
              as ``A(1,1)``.
              The y and z coordinates (or ``θ`` and ``z``, or etc.) of the vector are assumed to begin
              in the corresponding next columns, such as ``A(1,2)`` and ``A(1,3)``.
              Local coordinate locations are assumed to be in coordinate system ``CON1``
              (which may be any valid coordinate system number, such as 1,2,11,12, etc.).
              The transformed result, ``ParR``, must also have 3 consecutive
              columns of data, with the columns containing the global Cartesian ``x``, y, and z coordinate
              locations, respectively.

        par1
            Array parameter vector in the operation.

        con1, con2, con3
            Constants (used only with the PWR, NORM, LOCAL, and GLOBAL
            functions).

        Notes
        -----
        Operates on one input array parameter vector and produces one output
        array parameter vector according to:

        ``ParR = f(Par1)``

        """
        command = f"*VFUN,{parr},{func},{par1},{con1},{con2},{con3}"
        return self.run(command, **kwargs)

    def vitrp(self, parr="", part="", pari="", parj="", park="", **kwargs):
        """Forms an array parameter by interpolation of a table.

        APDL Command: ``*VITRP``

        Parameters
        ----------
        parr
            The name of the resulting array parameter.  See ``*SET`` for name
            restrictions.

        part
            The name of the TABLE array parameter.  The parameter must exist as
            a dimensioned array of type TABLE [``*DIM``].

        pari
            Array parameter vector of I (row) index values for interpolation in
            ParT.

        parj
            Array parameter vector of J (column) index values for interpolation
            in ParT (which must be at least 2-D).

        park
            Array parameter vector of K (depth) index values for interpolation
            in ParT (which must be 3-D).

        Notes
        -----
        Forms an array parameter (of type ``ARRAY``) by interpolating values of an
        array parameter (of type ``TABLE``) at specified table index locations
        according to:

        ``ParR = f(ParT, Parl, ParJ, ParK)``

        where ``ParT`` is the type ``TABLE`` array parameter, and ``ParI``, ``ParJ``, ``ParK`` are
        the type ``ARRAY`` array parameter vectors of index values for
        interpolation in ``ParT``.  See the ``*DIM`` command for ``TABLE`` and ``ARRAY``
        declaration types.  Linear interpolation is used.  The starting array
        element number for the ``TABLE`` array (``ParT``) is not used (but a value must
        be input).  Starting array element numbers must be defined for each
        array parameter vector if it does not start at the first location. For
        example, ``*VITRP,R(5),TAB(1,1),X(2),Y(4)`` uses the second element of X
        and the fourth element of Y as index values (row and column) for a 2-D
        interpolation in ``TAB`` and stores the result in the fifth element of R.
        Operations continue on successive array elements ``[*VLEN, *VMASK]`` with
        the default being all successive elements.  Absolute values and scale
        factors may be applied to the result parameter ``[*VABS, *VFACT]``.
        Results may be cumulative ``[*VCUM]``.  See the ``*VOPER`` command for details.

        This command is valid in any processor.
        """
        command = f"*VITRP,{parr},{part},{pari},{parj},{park}"
        return self.run(command, **kwargs)

    def vlen(self, nrow="", ninc="", **kwargs):
        """Specifies the number of rows to be used in array parameter operations.

        APDL Command: ``*VLEN``

        Parameters
        ----------
        nrow
            Number of rows to be used with the ``*VXX`` or ``*MXX`` operations.
            Defaults to the number of rows needed to fill the result array.

        ninc
            Perform the operation on every NINC row (defaults to 1).

        Notes
        -----
        Specifies the number of rows to be used in array parameter operations.
        The size of the submatrix used is determined from the upper left
        starting array element (defined on the operation command) to the lower
        right array element (defined by the number of rows on this command and
        the number of columns on the ``*VCOL`` command).  ``NINC`` allows skipping row
        operations for some operation commands.  Skipped rows are included in
        the row count.  The starting row number must be defined on the
        operation command for each parameter read and for the result written.

        The default ``NROW`` is calculated from the maximum number of rows of the
        result array (the ``*DIM`` row dimension) minus the starting location + 1.
        For example, ``*DIM,R,,10`` and a starting location of ``R(7)`` gives a default
        of 4 loops (filling ``R(7)``, ``R(8)``, ``R(9)``, and ``R(10)``).  Repeat operations
        automatically terminate at the last row of the result array.  Existing
        values in the rows and columns of the results matrix remain unchanged
        where not overwritten by the requested input or operation values.

        The stride (``NINC``) allows operations to be performed at regular
        intervals.  It has no effect on the total number of row operations.
        Skipped operations retain the previous result.  For example, ``*DIM,R,,6,``
        with a starting location of ``R(1)``, ``NROW = 10``, and ``NINC = 2`` calculates
        values for locations ``R(1)``, ``R(3)``, and ``R(5)`` and retains values for
        locations ``R(2)``, ``R(4)``, and ``R(6)``.  A more general skip control may be
        done by masking ``[*VMASK]``.  The row control settings are reset to the
        defaults after each ``*VXX`` or ``*MXX`` operation.  Use ``*VSTAT`` to list
        settings.

        This command is valid in any processor.
        """
        command = f"*VLEN,{nrow},{ninc}"
        return self.run(command, **kwargs)

    def vmask(self, par="", **kwargs):
        """Specifies an array parameter as a masking vector.

        APDL Command: ``*VMASK``

        Parameters
        ----------
        par
            Name of the mask parameter.  The starting subscript must also be
            specified.

        Notes
        -----
        Specifies the name of the parameter whose values are to be checked for
        each resulting row operation.  The mask vector usually contains only 0
        (for false) and 1 (for true) values.  For each row operation the
        corresponding mask vector value is checked.  A true value allows the
        operation to be done.  A false value skips the operation (and retains
        the previous results).  A mask vector can be created from direct input,
        such as ``M(1) = 1,0,0,1,1,0,1``; or from the DATA function of the ``*VFILL``
        command.  The NOT function of the ``*VFUN`` command can be used to reverse
        the logical sense of the mask vector.  The logical compare operations
        (``LT``, ``LE``, ``EQ``, ``NE``, ``GE``, and ``GT``) of
        the ``*VOPER`` command also produce a mask
        vector by operating on two other vectors.  Any numeric vector can be
        used as a mask vector since the actual interpretation assumes values
        less than 0.0 are 0.0 (false) and values greater than 0.0 are 1.0
        (true).  If the mask vector is not specified (or has fewer values than
        the result vector), true (1.0) values are assumed for the unspecified
        values.  Another skip control may be input with ``NINC`` on the ``*VLEN``
        command.  If both are present, operations occur only when both are
        true.  The mask setting is reset to the default (no mask) after each
        ``*VXX`` or ``*MXX`` operation.  Use ``*VSTAT`` to list settings.

        This command is valid in any processor.
        """
        command = f"*VMASK,{par}"
        return self.run(command, **kwargs)

    def voper(self, parr="", par1="", oper="", par2="", con1="", con2="", **kwargs):
        """Operates on two array parameters.

        APDL Command: ``*VOPER``

        Parameters
        ----------
        PARR
            The name of the resulting array parameter vector.  See ``*SET``  for
            name restrictions.

        PAR1
            First array parameter vector in the operation.  May also be a
            scalar parameter or a literal constant.

        OPER
            Operations:

            * ``ADD``
              Addition: ``Par1+Par2``.

            * ``SUB``
              Subtraction: ``Par1-Par2``.

            * ``MULT``
              Multiplication: ``Par1*Par2``.

            * ``DIV``
              Division: ``Par1/Par2``  (a divide by zero results in a value of zero).

            * ``MIN``
              Minimum: minimum of ``Par1`` and ``Par2``.

            * ``MAX``
              Maximum: maximum of ``Par1`` and ``Par2``.

            * ``LT``
              Less than comparison: ``Par1<Par2`` gives 1.0 if true, 0.0 if
              false.

            * ``LE``
              Less than or equal comparison: ``Par1 <= Par2`` gives
              1.0 if true, 0.0 if false.

            * ``EQ``
              Equal comparison: ``Par1 = Par2`` gives 1.0 if true, 0.0 if
              false.

            * ``NE``
              Not equal comparison: ``Par1 ≠ Par2`` gives 1.0 if
              true, 0.0 if false.

            * ``GE``
              Greater than or equal comparison: ``Par1 >= Par2`` gives 1.0 if
              true, 0.0 if false.

            * ``GT``
              Greater than comparison: ``Par1>Par2``
              gives 1.0 if true, 0.0 if false.

            * ``DER``
              First derivative:

              .. math::
                 \dfrac{\mathrm{d}(\mathrm{Par1})}{\mathrm{d}(\mathrm{Par2})}

              The derivative at a point is determined over points
              half way between the previous and next points
              (by linear interpolation).
              ``Par1`` must be a function (a unique ``Par1``
              value for each ``Par2``
              value) and ``Par2`` must be in ascending order.

            * ``DER2``
              Second derivative:

              .. math::
                 \dfrac{\mathrm{d}^2(\mathrm{Par1})}{\mathrm{d}(\mathrm{Par2})^2}

              See also ``DER1``.

            * ``INT1``
              Single integral:

              .. math::

                 \int Par1 \, d(Par2)

              where ``CON1`` is the integration constant.
              The integral at a point is
              determined by using the single integration procedure
              described in the Mechanical APDL Theory Reference.

            * ``INT2``
              Double integral:

              .. math::

                 \iint Par1 \, d(Par2)

              where ``CON1`` is the integration constant of the first
              integral and ``CON2`` is the integration constant
              of the second integral.  If ``Par1``
              contains acceleration data, ``CON1`` is the initial velocity
              and ``CON2`` is the initial displacement.  See also ``INT1``.

            * ``DOT``
              Dot product: ``Par1 . Par2``.
              ``Par1`` and ``Par2`` must each have
              three consecutive columns of data, with the columns
              containing the ``i``, ``j``, and ``k`` vector components,
              respectively.  Only the starting row index and the column
              index for the ``i`` components are specified for ``Par1`` and
              ``Par2``, such as ``A(1,1)``.  The ``j`` and ``k`` components of the
              vector are assumed to begin in the corresponding next
              columns, such as ``A(1,2)`` and ``A(1,3)``.

            * ``CROSS``
              Cross product: ``Par1 x Par2``.
              ``Par1``, ``Par2``, and ``ParR`` must each have 3 components,
              respectively.  Only the starting row index and the column
              index for the i components are specified for ``Par1``, ``Par2``,
              and ``ParR``, such as ``A(1,1)``.  The j and k components of the
              vector are assumed to begin in the corresponding next
              columns, such as ``A(1,2)`` and ``A(1,3)``.

            * ``GATH``
              Gather: For a vector of position numbers, ``Par2``, copy the
              value of ``Par1`` at each position number to ParR.  Example:
              for ``Par1 = 10,20,30,40`` and ``Par2 = 2,4,1``; ``ParR =
              20,40,10``.

            * ``SCAT``
              Scatter: Opposite of ``GATH`` operation.  For a
              vector of position numbers, ``Par2``, copy the value of ``Par1``
              to that position number in ``ParR``.  Example: for ``Par1 =
              10,20,30,40,50`` and ``Par2 = 2,1,0,5,3``; ``ParR = 20,10,50,0,40``.

            * ``ATN2``
              Arctangent: arctangent of ``Par1/Par2`` with the sign of each
              component considered.

            * ``LOCAL``
              Transform the data in ``Par1`` from
              the global Cartesian coordinate system to the local
              coordinate system given in ``CON1``. ``Par1`` must be an ``N`` x 3
              (i.e., vector) or an ``N`` x 6 (i.e., stress or strain tensor)
              array. If the local coordinate system is a cylindrical,
              spherical, or toroidal system, then you must provide the
              global Cartesian coordinates in ``Par2`` as an ``N`` x 3 array.
              Set ``CON2 = 1`` if the data is strain data.

            * ``GLOBAL``
              Transform the data in ``Par1`` from the local coordinate system given in ``CON1`` to the global
              Cartesian coordinate system. ``Par1`` must be an ``N`` x 3 (that is, vector) or an ``N`` x 6 (that is,
              stress or strain tensor) array. If the local coordinate system is a cylindrical, spherical, or
              toroidal system, then you must provide the global Cartesian coordinates in ``Par2`` as an ``N``
              x 3 array. Set ``CON2 = 1`` if the data is strain data.

        PAR2
            Second array parameter vector in the operation.  May also be a
            scalar parameter or a literal constant.

        CON1
            First constant (used only with the ``INT1`` and ``INT2`` operations).

        CON2
            Second constant (used only with the ``INT2`` operation).

        Notes
        -----
        Operates on two input array parameter vectors and produces one output
        array parameter vector according to:

        ``ParR = Par1 o Par2``

        where the operations (o) are described below.  ParR may be the same as
        ``Par1`` or ``Par2``.  Absolute values and scale factors may be applied to all
        parameters [``*VABS``, ``*VFACT``].  Results may be cumulative [``*VCUM``].
        Starting array element numbers must be defined for each array parameter
        vector if it does not start at the first location, such as
        ``*VOPER,A,B(5),ADD,C(3)`` which adds the third element of C to the fifth
        element of B and stores the result in the first element of A.
        Operations continue on successive array elements ``[*VLEN, *VMASK]`` with
        the default being all successive elements.  Skipping array elements via
        ``*VMASK`` or ``*VLEN`` for the ``DER`` and ``INT`` functions skips only the writing
        of the results (skipped array element data are used in all
        calculations).

        Parameter functions and operations are available to operate on a scalar
        parameter or a single element of an array parameter, such as ``SQRT(B)`` or
        ``SQRT(A(4))``.  See the ``*SET`` command for details.  Operations on a
        sequence of array elements can be done by repeating the desired
        function or operation in a do-loop ``[*DO]``.  The vector operations within
        the ANSYS program (``*VXX`` commands) are internally programmed do-loops
        that conveniently perform the indicated operation over a sequence of
        array elements.  If the array is multidimensional, only the first
        subscript is incremented in the do-loop, that is, the operation repeats
        in column vector fashion "down" the array.  For example, for ``A(1,5)``,
        ``A(2,5)``, ``A(3,5)``, etc.  The starting location of the row index must be
        defined for each parameter read and for the result written.

        The default number of loops is from the starting result location to the
        last result location and can be altered with the ``*VLEN`` command.  A
        logical mask vector may be defined to control at which locations the
        operations are to be skipped [``*VMASK``].  The default is to skip no
        locations.  Repeat operations automatically terminate at the last array
        element of the result array column if the number of loops is undefined
        or if it exceeds the last result array element.  Zeroes are used in
        operations for values read beyond the last array element of an input
        array column.  Existing values in the rows and columns of the results
        matrix
        """
        command = f"*VOPER,{parr},{par1},{oper},{par2},{con1},{con2}"
        return self.run(command, **kwargs)

    def vscfun(self, parr="", func="", par1="", **kwargs):
        """Determines properties of an array parameter.

        APDL Command: ``*VSCFUN``

        Parameters
        ----------
        parr
            The name of the resulting scalar parameter.  See ``*SET`` for name
            restrictions.

        func
            Functions:

            * ``MAX``
              Maximum: the maximum ``Par1`` array element value.

            * ``MIN``
              Minimum: the minimum ``Par1`` array element value.

            * ``LMAX``
              Index location of the maximum ``Par1`` array element value.
              Array ``Par1`` is searched starting from its specified
              index.

            * ``LMIN``
              Index location of the minimum ``Par1`` array element
              value.  Array ``Par1`` is searched starting from its specified
              index.

            * ``FIRST``
              Index location of the first nonzero value in array ``Par1``.
              Array ``Par1`` is searched starting from its specified
              index.

            * ``LAST``
              Index location of the last nonzero value in array
              ``Par1``.  Array ``Par1`` is searched starting from its specified
              index.

            * ``SUM``
              Sum: ``Par1`` (the summation of the ``Par1`` array element
              values).

            * ``MEDI``
              Median: value of ``Par1`` at which there are an
              equal number of values above and below.

            * ``MEAN``
              Mean: ``(σ Par1)/NUM``, where ``NUM`` is the number of summed
              values.

            * ``VARI``
              Variance: ``(σ ((Par1-MEAN)**2))/NUM``.

            * ``STDV``
              Standard deviation: square root of ``VARI``.

            * ``RMS``
              Root-mean-square: square root of ``(σ (Par1**2))/NUM``.

            * ``NUM``
              Number: the number of summed values (masked values are not counted).

        par1
            Array parameter vector in the operation.

        Notes
        -----
        Operates on one input array parameter vector and produces one output
        scalar parameter according to:

        ``ParR = f(Par1)``

        where the functions (f) are described below. The starting array element
        number must be defined for the array parameter vector.  For example,
        ``*VSCFUN,MU,MEAN,A(1)`` finds the mean of the ``A`` vector values, starting
        from the first value and stores the result as parameter ``MU``.  Operations
        use successive array elements ``[*VLEN, *VMASK]`` with the default being
        all successive array elements.  Absolute values and scale factors may
        be applied to all parameters ``[*VABS, *VFACT]``.  Results may be
        cumulative ``[*VCUM]``.  See the ``*VOPER`` command for details.

        This command is valid in any processor.
        """
        command = f"*VSCFUN,{parr},{func},{par1}"
        return self.run(command, **kwargs)

    def vstat(self, **kwargs):
        """Lists the current specifications for the array parameters.

        APDL Command: ``*VSTAT``

        Notes
        -----
        Lists the current specifications for the ``*VABS``, ``*VCOL``,
        ``*VCUM``, ``*VFACT``, ``*VLEN``, and ``*VMASK`` commands.

        This command is valid in any processor.
        """
        command = f"*VSTAT,"
        return self.run(command, **kwargs)

    def vwrite(
        self,
        par1="",
        par2="",
        par3="",
        par4="",
        par5="",
        par6="",
        par7="",
        par8="",
        par9="",
        par10="",
        par11="",
        par12="",
        par13="",
        par14="",
        par15="",
        par16="",
        par17="",
        par18="",
        par19="",
        **kwargs,
    ):
        """Writes data to a file in a formatted sequence.

        APDL Command: ``*VWRITE``

        .. warning::
           This command cannot be run interactively.  See
           :func:`non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`.

        Parameters
        ----------
        par1, par2, par3, . . . , par19
            You can write up to 19 parameters (or constants) at a time. Any Par
            values after a blank  Par value are ignored.  If you leave them all
            blank, one line will be written (to write a title or a blank line).
            If you input the keyword SEQU, a sequence of numbers (starting from
            1) will be written for that item.

        Notes
        -----
        You use ``*VWRITE`` to write data to a file in a formatted sequence. Data
        items (Par1, Par2, etc.) may be array parameters, scalar parameters,
        character parameters (scalar or array), or constants.  You must
        evaluate expressions and functions in the data item fields before using
        the ``*VWRITE`` command, since initially they will be evaluated to a
        constant and remain constant throughout the operation.  Unless a file
        is defined with the ``*CFOPEN``  command, data is written to the standard
        output file. Data written to the standard output file may be diverted
        to a different file by first switching the current output file with the
        /OUTPUT command. You can also use the ``*MWRITE`` command to write data to
        a specified file. Both commands contain format descriptors on the line
        immediately following the command. The format descriptors can be in
        either Fortran or C format.

        You must enclose Fortran format descriptors in parentheses. They must
        immediately follow the ``*VWRITE`` command on a separate line of the same
        input file.  Do not include the word FORMAT. The format must specify
        the number of fields to be written per line, the field width, the
        placement of the decimal point, etc.  You should use one field
        descriptor for each data item written.  The write operation uses your
        system's available FORTRAN FORMAT conventions (see your system FORTRAN
        manual).  You can use any standard FORTRAN real format (such as
        (4F6.0), (E10.3,2X,D8.2), etc.) and alphanumeric format (A).
        Alphanumeric strings are limited to a maximum of 8 characters for any
        field (A8) using the Fortran format. Use the "C" format for string
        arrays larger than 8 characters. Integer (I) and list-directed (*)
        descriptors may not be used.  You can include text in the format as a
        quoted string.  The parentheses must be included in the format and the
        format must not exceed 80 characters (including parentheses).  The
        output line length is limited to 128 characters.

        The "C" format descriptors are used if the first character of the
        format descriptor line is not a left parenthesis. "C" format
        descriptors are up to 80 characters long, consisting of text strings
        and predefined "data descriptors" between the strings where numeric or
        alphanumeric character data will be inserted.  The normal descriptors
        are %I for integer data, %G for double precision data, %C for
        alphanumeric character data, and %/ for a line break. There must be one
        data descriptor for each specified value (8 maximum) in the order of
        the specified values. The enhanced formats described in ``*MSG`` may also
        be used.

        For array parameter items, you must define the starting array
        element number. Looping continues (incrementing the vector
        index number of each array parameter by one) each time you
        output a line, until the maximum array vector element is
        written.  For example, ``*VWRITE,A(1)`` followed by (F6.0)
        will write one value per output line, i.e., A(1), A(2), A(3),
        A(4), etc.  You write constants and scalar parameters with the
        same values for each loop.  You can also control the number of
        loops and loop skipping with the ``*VLEN`` and ``*VMASK``
        commands.  The vector specifications ``*VABS``, ``*VFACT``,
        and ``*VCUM`` do not apply to this command.  If looping
        continues beyond the supplied data array's length, zeros will
        be output for numeric array parameters and blanks for
        character array parameters.  For multi-dimensioned array
        parameters, only the first (row) subscript is incremented.
        See the ``*VOPER`` command for details.  If you are in the GUI,
        the ``*VWRITE`` command must be contained in an externally
        prepared file and read into ANSYS (i.e., ``*USE``, /INPUT, etc.).

        This command is valid in any processor.

        """
        # cannot be in interactive mode
        if not self._store_commands:
            raise MapdlRuntimeError(
                "VWRTIE cannot run interactively.  \n\nPlease use "
                "``with mapdl.non_interactive:``"
            )

        command = f"*VWRITE,{par1},{par2},{par3},{par4},{par5},{par6},{par7},{par8},{par9},{par10},{par11},{par12},{par13},{par14},{par15},{par16},{par17},{par18},{par19}"
        return self.run(command, **kwargs)
