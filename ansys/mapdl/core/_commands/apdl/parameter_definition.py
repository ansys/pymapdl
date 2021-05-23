import os


def afun(self, lab="", **kwargs):
    """Specifies units for angular functions in parameter expressions.

    APDL Command: *AFUN

    Parameters
    ----------
    lab
        Specifies the units to be used:

        Use radians for input and output of parameter angular functions (default). - Use degrees for input and output of parameter angular functions.

    Notes
    -----
    Only the SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2, ANGLEK, and ANGLEN
    functions [*SET, *VFUN] are affected by this command.
    """
    command = f"*AFUN,{lab}"
    return self.run(command, **kwargs)


def dim(self, par="", type_="", imax="", jmax="", kmax="", var1="", var2="",
        var3="", csysid="", **kwargs):
    """Defines an array parameter and its dimensions.

    APDL Command: *DIM

    Parameters
    ----------
    par
        Name of parameter to be dimensioned.  See *SET for name
        restrictions.

    type\_
        Array type:

        Arrays are similar to standard FORTRAN arrays (indices are integers) (default).  Index numbers for the rows, columns, and planes are sequential values beginning with one. Used for 1-, 2-, or 3-D arrays. - Same as ARRAY, but used to specify 4-D arrays.

        Same as ARRAY, but used to specify 5-D arrays. - Array entries are character strings (up to 8 characters each).  Index numbers
                          for rows, columns, and planes are sequential
                          values beginning with one.

        Array indices are real (non-integer) numbers which must be defined when filling the table.  Index numbers for the rows and columns are stored in the zero column and row "array elements" and are initially assigned a near-zero value.  Index numbers must be in ascending order and are used only for retrieving an array element.  When retrieving an array element with a real index that does not match a specified index, linear interpolation is done among the nearest indices and the corresponding array element values [*SET]. Used for 1-, 2-, or 3-D tables. - Same as TABLE, but used to specify 4-D tables.

        Same as TABLE, but used to specify 5-D tables. - Array entries are character strings (up to IMAX each). Index numbers for
                          columns and planes are sequential values
                          beginning with 1. Row index is character position
                          in string.

    imax
        Extent of first dimension (row). (For Type = STRING, IMAX is
        rounded up to the next multiple of eight and has a limit of 248).
        Defaults to 1.

    jmax
        Extent of second dimension (column).  Defaults to 1.

    kmax
        Extent of third dimension (plane).  Defaults to 1.

    var1
        Variable name corresponding to the first dimension (row) for Type =
        TABLE.  Defaults to Row.

    var2
        Variable name corresponding to the second dimension (column) for
        Type = TABLE.  Defaults to Column.

    var3
        Variable name corresponding to the third dimension (plane) for Type
        = TABLE.  Defaults to Plane.

    csysid
        An integer corresponding to the coordinate system ID Number.

    Notes
    -----
    Up to three dimensions (row, column, and plane) may be defined using
    ARRAY and TABLE.  Use ARR4, ARR5, TAB4, and TAB5 to define up to five
    dimensions (row, column, plane, book, and shelf). An index number is
    associated with each row, column, and plane.  For array and table type
    parameters, element values are initialized to zero.  For character and
    string parameters, element values are initialized to (blank).  A
    defined parameter must be deleted [*SET] before its dimensions can be
    changed.  Scalar (single valued) parameters should not be dimensioned.
    *DIM,A,,3 defines a vector array with elements A(1), A(2), and A(3).
    *DIM,B,,2,3 defines a 2x3 array with elements B(1,1), B(2,1), B(1,2),
    B(2,2), B(1,3), and B(2,3).  Use *STATUS,Par to display elements of
    array Par. You can write formatted data files (tabular formatting) from
    data held in arrays through the *VWRITE command.

    If you use table parameters to define boundary conditions, then Var1,
    Var2, and/or Var3 can either specify a primary variable (listed in
    Table: 130:: *DIM - Primary Variables) or can be an independent
    parameter.  If specifying an independent parameter, then you must
    define an additional table for the independent parameter.  The
    additional table must have the same name as the independent parameter
    and may be a function of one or more primary variables or another
    independent parameter.  All independent parameters must relate to a
    primary variable.

    Tabular load arrays can be defined in both global Cartesian (default)
    or local (see below) coordinate systems by specifying CSYSID, as
    defined in LOCAL. For batch operations, you must specify your
    coordinate system first.

    The following constraints apply when you specify a local coordinate
    system for your tabular loads:

    If you are specifying a 4- or 5-D array or table, four additional
    fields (LMAX, MMAX, Var4, and Var5) are available. Thus, for a 4-D
    table, the command syntax would be:

    For a 5-D table, the command syntax would be:

    You cannot create or edit 4- or 5-D arrays or tables using the GUI.

    See Array Parameters for a detailed discussion on and examples for
    using array parameters.

    Table: 130:: : *DIM - Primary Variables

    Specify PRESSURE as the independent variable (not PRES).

    The X, Y, and Z coordinate locations listed above are valid in global
    Cartesian, or local (Cartesian, cylindrical and spherical) coordinate
    systems. The VELOCITY label is applicable only to the calculated fluid
    velocity in element FLUID116.

    When using PRESSURE as a primary variable, the underlying element must
    have the pressure DOF associated with it, or it must be a supported
    contact element.

    The gap/penetration label (GAP) is only used for defining certain
    contact element real constants.

    The frequency label (FREQ) is valid for harmonic analyses only.

    The OMEGS, ECCENT, and THETA primary variables only apply to the
    COMBI214 element. The amplitude of the rotational velocity (OMEGS) is
    an absolute value, so only positive values of OMEGS are valid. The
    eccentricity (ECCENT) and phase shift (THETA) labels are only valid for
    nonlinear analyses.

    If you use table parameters to define boundary conditions, the table
    names (Par) must not exceed 32 characters.

    In thermal analyses, if you apply tabular loads as a function of
    temperature but the rest of the model is linear (e.g., includes no
    temperature-dependent material properties or radiation ), you should
    turn on Newton-Raphson iterations (NROPT,FULL) to evaluate the
    temperature-dependent tabular boundary conditions correctly.

    This command is valid in any processor.
    """
    command = f"*DIM,{par},{type_},{imax},{jmax},{kmax},{var1},{var2},{var3},{csysid}"
    return self.run(command, **kwargs)


def get(self, par="", entity="", entnum="", item1="", it1num="", item2="",
        it2num="", **kwargs):
    """Retrieves a value and stores it as a scalar parameter or part of an

    APDL Command: *GET
    array parameter.

    Parameters
    ----------
    par
        The name of the resulting parameter. See *SET for name
        restrictions.

    entity
        Entity keyword. Valid keywords are NODE, ELEM, KP, LINE, AREA,
        VOLU, PDS, etc., as shown for Entity = in the tables below.

    entnum
        The number or label for the entity (as shown for ENTNUM = in the
        tables below). In some cases, a zero (or blank) ENTNUM represents
        all entities of the set.

    item1
        The name of a particular item for the given entity. Valid items are
        as shown in the Item1 columns of the tables below.

    it1num
        The number (or label) for the specified Item1 (if any). Valid
        IT1NUM values are as shown in the IT1NUM columns of the tables
        below. Some Item1 labels do not require an IT1NUM value.

    item2, it2num
        A second set of item labels and numbers to further qualify the item
        for which data are to be retrieved. Most items do not require this
        level of information.

    Notes
    -----
    *GET retrieves a value for a specified item and stores the value as a
    scalar parameter, or as a value in a user-named array parameter. An
    item is identified by various keyword, label, and number combinations.
    Usage is similar to the *SET command except that the parameter values
    are retrieved from previously input or calculated results. For example,
    *GET,A,ELEM,5,CENT,X returns the centroid x-location of element 5 and
    stores the result as parameter A. *GET command operations, along with
    the associated Get functions return values in the active coordinate
    system unless stated otherwise. A Get function is an alternative in-
    line function that can be used to retrieve a value instead of the *GET
    command (see Using In-line Get Functions for more information).

    Both *GET and *VGET retrieve information from the active data stored in
    memory. The database is often the source, and sometimes the information
    is retrieved from common memory blocks that the program uses to
    manipulate information. Although POST1 and POST26 operations use a
    *.rst file, *GET data is accessed from the database or from the common
    blocks. Get operations do not access the *.rst file directly. For
    repeated gets of sequential items, such as from a series of elements,
    see the *VGET command.

    Most items are stored in the database after they are calculated and are
    available anytime thereafter. Items are grouped according to where they
    are usually first defined or calculated. Preprocessing data will often
    not reflect the calculated values generated from section data. Do not
    use *GET to obtain data from elements that use calculated section data,
    such as beams or shells. Most of the general items listed below are
    available from all modules. Each of the sections for accessing *GET
    parameters are shown in the following order:

    *GET General Entity Items

    *GET Preprocessing Entity Items

    *GET Solution Entity Items

    *GET Postprocessing Entity Items

    *GET Probabilistic Design Entity Items

    The *GET command is valid in any processor.
    """
    command = f"*GET,{par},{entity},{entnum},{item1},{it1num},{item2},{it2num}"
    return self.run(command, **kwargs)


def inquire(self, func):
    """Returns system information.

    Parameters
    ----------
    func : str
       Specifies the type of system information returned.  See the
       notes section for more information.

    Returns
    -------
    value : str
        Value of the inquired item.

    Notes
    -----
    Allowable func entries
    LOGIN - Returns the pathname of the login directory on Linux
    systems or the pathname of the default directory (including
    drive letter) on Windows systems.

    - ``DOCU`` - Pathname of the ANSYS docu directory.
    - ``APDL`` - Pathname of the ANSYS APDL directory.
    - ``PROG`` - Pathname of the ANSYS executable directory.
    - ``AUTH`` - Pathname of the directory in which the license file resides.
    - ``USER`` - Name of the user currently logged-in.
    - ``DIRECTORY`` - Pathname of the current directory.
    - ``JOBNAME`` - Current Jobname.
    - ``RSTDIR`` - Result file directory
    - ``RSTFILE`` - Result file name
    - ``RSTEXT`` - Result file extension
    - ``OUTPUT`` - Current output file name

    Examples
    --------
    Return the job name

    >>> mapdl.inquire('JOBNAME')
    file

    Return the result file name

    >>> mapdl.inquire('RSTFILE')
    'file.rst'
    """
    response = self.run(f'/INQUIRE,,{func}', mute=False)
    if '=' in response:
        return response.split('=')[1].strip()
    return ''


def parres(self, lab="", fname="", ext="", **kwargs):
    """Reads parameters from a file.

    APDL Command: PARRES

    Parameters
    ----------
    lab
        Read operation.

        NEW - Replace current parameter set with these parameters (default).

        CHANGE - Extend current parameter set with these
        parameters, replacing any that already exist.

    fname
        File name and directory path (248 characters maximum,
        including the characters needed for the directory path).
        An unspecified directory path defaults to the working
        directory; in this case, you can use all 248 characters
        for the file name.

        The file name defaults to Jobname.

    ext
        Filename extension (eight-character maximum).  The
        extension defaults to PARM if Fname is blank.

    Examples
    --------
    Read a local parameter file.

    >>> mapdl.parres('parm.PARM')

    Notes
    -----
    Reads parameters from a coded file.  The parameter file may
    have been written with the PARSAV command.  The parameters
    read may replace or change the current parameter set.

    This command is valid in any processor.
    """
    if ext:
        fname = fname + '.' + ext
    elif not fname:
        fname = '.' + 'PARM'

    if 'Grpc' in self.__class__.__name__:  # grpc mode
        if self._local:
            if not os.path.isfile(fname):
                raise FileNotFoundError(
                    'Unable to locate filename "%s"' % fname)

            if not os.path.dirname(fname):
                filename = os.path.join(os.getcwd(), fname)
            else:
                filename = fname
        else:
            if not os.path.dirname(fname):
                # might be trying to run a local file.  Check if the
                # file exists remotely.
                if fname not in self.list_files():
                    self.upload(fname, progress_bar=False)
            else:
                self.upload(fname, progress_bar=False)
            filename = os.path.basename(fname)
    else:
        filename = fname

    return self.input(filename)


def parsav(self, lab="", fname="", ext="", **kwargs):
    """Writes parameters to a file.

    APDL Command: PARSAV

    Parameters
    ----------
    lab
        Write operation:

        - ``'SCALAR'`` : Write only scalar parameters (default). 
        - ``'ALL'`` : Write scalar and array parameters.
          Parameters may be numeric or alphanumeric.

    fname
        File name and directory path (248 characters maximum,
        including the characters needed for the directory path).
        An unspecified directory path defaults to the working
        directory; in this case, you can use all 248 characters
        for the file name.

    ext
        Filename extension (eight-character maximum).

    Notes
    -----
    Writes the current parameters to a coded file.  Previous
    parameters on this file, if any, will be overwritten.  The
    parameter file may be read with the PARRES command.

    PARSAV/PARRES operations truncate some long decimal strings,
    and can cause differing values in your solution data when
    other operations are performed. A good practice is to limit
    the number of decimal places you will use before and after
    these operations.

    This command is valid in any processor.
    """
    command = f"PARSAV,{lab},{fname},{ext}"
    return self.run(command, **kwargs)


def set(self, lstep="", sbstep="", fact="", kimg="", time="", angle="",
        nset="", order="", **kwargs):
    """Defines the data set to be read from the results file.

    APDL Command: SET

    Parameters
    ----------
    lstep
        Load step number of the data set to be read (defaults to 1):

        N - Read load step N.

        FIRST - Read the first data set (Sbstep and TIME are ignored).

        LAST - Read the last data set (Sbstep and TIME are ignored).

        NEXT - Read the next data set (Sbstep and TIME are ignored).  If at the last data set,
               the first data set will be read as the next.

        PREVIOUS - Read the previous data set (Sbstep and TIME are ignored).  If at the first data
                   set, the last data set will be read as the previous.

        NEAR - Read the data set nearest to TIME (Sbstep is ignored).  If TIME is blank, read
               the first data set.

        LIST - Scan the results file and list a summary of each load step.  (KIMG, TIME,
               ANGLE, and NSET are ignored.)

    sbstep
        Substep number (within Lstep). Defaults to the last substep of the
        load step (except in a buckling or modal analysis). For a buckling
        (ANTYPE,BUCKLE) or modal (ANTYPE,MODAL) analysis, Sbstep
        corresponds to the mode number. Specify Sbstep = LAST to store the
        last substep for the specified load step (that is, issue a
        SET,Lstep,LAST command).

    fact
        Scale factor applied to data read from the file. If zero (or
        blank), a value of 1.0 is used. This scale factor is only applied
        to displacement and stress results. A nonzero factor excludes non-
        summable items.

    kimg
        Used only with complex results (harmonic and complex modal
        analyses).

        0 or REAL - Store the real part of complex solution (default).

        1, 2 or IMAG - Store the imaginary part of a complex solution.

        3 or AMPL - Store the amplitude

        4 or PHAS - Store the phase angle. The angle value, expressed in degrees, will be between
                    -180°  and +180°.

    time
        Time-point identifying the data set to be read.  For a harmonic
        analyses, time corresponds to the frequency.

    angle
        Circumferential location (0.0 to 360°).  Defines the
        circumferential location for the harmonic calculations used when
        reading from the results file.

    nset
        Data set number of the data set to be read.  If a positive value
        for NSET is entered, Lstep, Sbstep, KIMG, and TIME are ignored.
        Available set numbers can be determined by SET,LIST.

    order
        Key to sort the harmonic index results. This option applies to
        cyclic symmetry buckling and modal analyses only, and is valid only
        when Lstep = FIRST, LAST, NEXT, PREVIOUS, NEAR or LIST.

        ORDER  - Sort the harmonic index results in ascending order of eigenfrequencies or
                 buckling load multipliers.

        (blank)  - No sorting takes place.

    Notes
    -----
    Defines the data set to be read from the results file into the
    database.  Various operations may also be performed during the read
    operation.  The database must have the model geometry available (or use
    the RESUME command before the SET command to restore the geometry from
    Jobname.DB).  Values for applied constraints [D] and loads [F] in the
    database will be replaced by their corresponding values on the results
    file, if available. (See the description of the OUTRES command.)  In a
    single load step analysis, these values are usually the same, except
    for results from harmonic elements. (See the description of the ANGLE
    value above.)

    In an interactive run, the sorted list (ORDER option) is also available
    for results-set reading via a GUI pick option.

    You can postprocess results without issuing a SET command if the
    solution results were saved to the database file (Jobname.DB).
    Distributed ANSYS, however, can only postprocess using the results file
    (for example, Jobname.RST) and cannot use the Jobname.DB file since no
    solution results are written to the database. Therefore, you must issue
    a SET command or a RESCOMBINE command before postprocessing in
    Distributed ANSYS.
    """
    command = f"SET,{lstep},{sbstep},{fact},{kimg},{time},{angle},{nset},{order}"
    return self.run(command, **kwargs)


def taxis(self, parmloc="", naxis="", val1="", val2="", val3="", val4="",
          val5="", val6="", val7="", val8="", val9="", val10="", **kwargs):
    """Defines table index numbers.

    APDL Command: *TAXIS

    Parameters
    ----------
    parmloc
        Name and starting location in the table array parameter for
        indexing. Indexing occurs along the axis defined with nAxis.

    naxis
        Axis along which indexing occurs.  Valid labels are:

        Corresponds to Row. Default. - Corresponds to Column.

        Corresponds to Plane. - Corresponds to Book.

        Corresponds to Shelf. - Lists all index numbers. Valid only if Val1 = LIST.

    val1, val2, val3, . . . , val10
        Values of the index numbers for the axis nAxis, starting from the
        table array parameter location ParmLoc. You can define up to ten
        values.

    Notes
    -----
    *TAXIS is a convenient method to define table index values. These
    values reside in the zero column, row, etc. Instead of filling values
    in these zero location spots, use the *TAXIS command. For example,

     would fill index values 1.0, 2.2, 3.5, 4.7, and 5.9 in nAxis 2 (column
    location), starting at location 4.

    To list index numbers, issue *TAXIS,ParmLoc, nAxis, LIST, where nAxis =
    1 through 5 or ALL.
    """
    command = f"*TAXIS,{parmloc},{naxis},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10}"
    return self.run(command, **kwargs)


def tread(self, par="", fname="", ext="", nskip="", **kwargs):
    """Reads data from an external file into a table array parameter.

    APDL Command: *TREAD

    Parameters
    ----------
    par
        Table array parameter name as defined by the *DIM command.

    fname
        File name and directory path (248 characters maximum, including the
        characters needed for the directory path).  An unspecified
        directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name.

    ext
        Filename extension (eight-character maximum).

    nskip
        Number of comment lines at the beginning of the file being read
        that will be skipped during the reading.  Default = 0.

    Notes
    -----
    Use this command to read in a table of data from an external file into
    an ANSYS table array parameter.  The external file may be created using
    a text editor or by an external application or program.  The external
    file must be in tab-delimited, blank-delimited, or comma-delimited
    format to be used by *TREAD. The ANSYS TABLE type array parameter must
    be defined before you can read in an external file.  See *DIM  for more
    information.

    This command is not applicable to 4- or 5-D tables.
    """
    command = f"*TREAD,{par},{fname},{ext},,{nskip}"
    return self.run(command, **kwargs)


def vfill(self, parr="", func="", con1="", con2="", con3="", con4="",
          con5="", con6="", con7="", con8="", con9="", con10="", **kwargs):
    """Fills an array parameter.

    APDL Command: *VFILL

    Parameters
    ----------
    parr
        The name of the resulting numeric array parameter vector.  See *SET
        for name restrictions.

    func
        Fill function:

        DATA - Assign specified values CON1, CON2, etc. to successive
        array elements.  Up to 10 assignments may be made at a
        time.  Any CON values after a blank CON value are
        ignored. - Assign ramp function values: CON1+((n-1)*CON2)
        , where n is the loop number [*VLEN].  To specify a
        constant function (no ramp), set CON2 to zero.

        RAMP - Assign random number values based on a uniform
        distribution RAND(CON1,CON2), where: - Assign random
        sample of Gaussian distributions GDIS(CON1,CON2).

        RAND - Assign random number values based on a uniform
        distribution RAND(CON1,CON2), where CON1 is the lower
        bound (defaults to 0.0) and CON2 is the upper bound
        (defaults to 1.0)

        GDIS - Assign random sample of Gaussian distributions
        GDIS(CON1,CON2) where CON1 is the mean (defaults to 0.0),
        and CON2 is the standard deviation (defaults to 1.0)

        TRIA - Assigns random number values based on a triangular
        distribution TRIA(CON1,CON2,CON3) where CON1 is the lower
        bound (defaults to 0.0), CON2 is the location of the peak
        value (CON1 ≤ CON2 ≤CON3; CON2 defaults to 0 if CON1 ≤ 0 ≤
        CON3, CON1 if 0 ≤ CON1, or CON3 if CON3 ≤ 0), and CON3 is
        the upper bound (defaults to 1.0 + CON1 if CON1 ≥ 0 or 0.0
        if CON1 ≤ 0)

        BETA - Assigns random number values based on a beta
        distribution BETA(CON1,CON2,CON3,CON4) where: CON1 is the
        lower bound (defaults to 0.0), CON2 is the upper bound
        (defaults to 1.0 + CON1 if CON1 ≥ 0 or 0.0 if CON1 ≤ 0), and CON3
        and CON4 are the alpha and beta parameters, respectively,
        of the beta function. Alpha and beta must both be
        positive; they default to 1.0.

        GAMM - Assigns random number values based on a gamma
        distribution: GAMM(CON1,CON2,CON3) where: CON1 is the
        lower bound (defaults to 0.0), CON2 and CON3 are the alpha
        and beta parameters, respectively, of the gamma
        function. Alpha and beta must both be positive; they
        default to 1.0.

        RIGID - Generates the rigid body modes with respect to the
        reference point coordinates (CON1, CON2, CON3). The
        dimensions of the array parameter ParR are (dim1,dim2)
        where dim1 is the maximum node number (including internal
        nodes but excluding orientation nodes) multiplied by the
        number of degrees of freedom, and dim2 is the number of
        rigid body modes (which corresponds to the number of
        structural degrees of freedom).

        CLUSTER - Generates excitation frequencies with clustering
        option CLUSTER(CON1,CON2,CON3,CON4,%CON5%) where:

        - CON1 is the lower end of the frequency range in Hz (0 < CON1)
        - CON2 is the upper end of the frequency range in Hz (CON1 < CON2)
        - CON3 is the number of points on each side of the natural
          frequency (4 ≤ CON3 ≤ 20, defaults to 4)
        - CON4 is the constant damping ratio value or an array
          parameter (size NFR) specifying the damping ratios (if
          zero or blank, defaults to constant damping ratio of
          0.005)
        - CON5 is an array parameter (size NFR) specifying the
          natural frequencies in Hz

        The dimension of the resulting array parameter ParR is
        less than 2+NFR*(2*CON3+1) where NFR is the number of
        natural frequencies defined in CON5.

    con1, con2, con3, . . . , con10
        Constants used with above functions.

    Notes
    -----
    Operates on input data and produces one output array parameter vector
    according to:

    ParR = f(CON1, CON2, : ...)

    where the functions (f) are described above. Operations use successive
    array elements [*VLEN, *VMASK] with the default being all successive
    elements.  For example, *VFILL,A,RAMP,1,10 assigns A(1) = 1.0, A(2) =
    11.0, A(3) = 21.0, etc.  *VFILL,B(5,1),DATA,1.5,3.0 assigns B(5,1) =
    1.5 and B(6,1) = 3.0.  Absolute values and scale factors may be applied
    to the result parameter [*VABS, *VFACT].  Results may be cumulative
    [*VCUM].  See the *VOPER command for details.

    This command is valid in any processor.
    """
    command = f"*VFILL,{parr},{func},{con1},{con2},{con3},{con4},{con5},{con6},{con7},{con8},{con9},{con10}"
    return self.run(command, **kwargs)


def vget(self, par="", ir="", tstrt="", kcplx="", **kwargs):
    """Moves a variable into an array parameter vector.

    APDL Command: VGET

    Parameters
    ----------
    par
        Array parameter vector in the operation.

    ir
        Reference number of the variable (1 to NV [NUMVAR]).

    tstrt
        Time (or frequency) corresponding to start of IR data.  If between
        values, the nearer value is used.

    kcplx
        Complex number key:

        0 - Use the real part of the IR data.

        1 - Use the imaginary part of the IR data.

    Notes
    -----
    Moves a variable into an array parameter vector.  The starting array
    element number must be defined.  For example, VGET,A(1),2 moves
    variable 2 (starting at time 0.0) to array parameter A.  Looping
    continues from array element A(1) with the index number incremented by
    one until the variable is filled.  The number of loops may be
    controlled with the *VLEN command (except that loop skipping (NINC) is
    not allowed).  For multi-dimensioned array parameters, only the first
    (row) subscript is incremented.
    """
    command = f"VGET,{par},{ir},{tstrt},{kcplx}"
    return self.run(command, **kwargs)


def vread(self, parr="", fname="", ext="", label="", n1="", n2="", n3="",
          nskip="", **kwargs):
    """Reads data and produces an array parameter vector or matrix.

    APDL Command: *VREAD

    Parameters
    ----------
    parr
        The name of the resulting array parameter vector.  See *SET for
        name restrictions.  The parameter must exist as a dimensioned array
        [*DIM]. String arrays are limited to a maximum of 8 characters.

    fname
        File name and directory path (248 characters maximum, including the
        characters needed for the directory path).  An unspecified
        directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name.

    ext
        Filename extension (eight-character maximum).

    label
        Can take a value of IJK, IKJ, JIK, JKI, KIJ, KJI, or blank (IJK).

    n1, n2, n3
        Read as (((ParR (i,j,k), k = 1,n1), i = 1, n2), j = 1, n3) for
        Label = KIJ. n2 and n3 default to 1.

    nskip
        Number of lines at the beginning of the file being read that will
        be skipped during the reading.  Default = 0.

    Notes
    -----
    Reads data from a file and fills in an array parameter vector or
    matrix.  Data are read from a formatted file or, if the menu is off
    [/MENU,OFF] and Fname is blank, from the next input lines.  The format
    of the data to be read must be input immediately following the *VREAD
    command.  The format specifies the number of fields to be read per
    record, the field width, and the placement of the decimal point (if
    none specified in the value).  The read operation follows the available
    FORTRAN FORMAT conventions of the system (see your system FORTRAN
    manual).  Any standard FORTRAN real format (such as (4F6.0),
    (E10.3,2X,D8.2), etc.) or alphanumeric format (A) may be used.
    Alphanumeric strings are limited to a maximum of 8 characters for any
    field (A8). For storage of string arrays greater than 8 characters, the
    *SREAD command can be used. Integer (I) and list-directed (*)
    descriptors may not be used.  The parentheses must be included in the
    format and the format must not exceed 80 characters (including
    parentheses).  The input line length is limited to 128 characters.

    A starting array element number must be defined for the result array
    parameter vector (numeric or character).  For example, entering these
    two lines:

    will read two values from each line of file ARRAYVAL and assign the
    values to A(1), A(2), A(3), etc.  Reading continues until successive
    row elements [*VLEN, *VMASK, *DIM] are filled.

    For an array parameter matrix, a starting array element row and column
    number must be defined.  For example, entering these two lines:

    will read two values from each line of file ARRAYVAL and assign the
    values to A(1,1), A(2,1), A(3,1), etc.  Reading continues until n1 (10)
    successive row elements are filled.  Once the maximum row number is
    reached, subsequent data will be read into the next column (e.g.,
    A(1,2), A(2,2), A(3,2), etc.)

    For numerical parameters, absolute values and scale factors may be
    applied to the result parameter [*VABS, *VFACT].  Results may be
    cumulative [*VCUM].  See the *VOPER command for details.  If you are in
    the GUI the *VREAD command must be contained in an externally prepared
    file read into the ANSYS program (i.e., *USE, /INPUT, etc.).

    This command is not applicable to 4- or 5-D arrays.

    This command is valid in any processor.
    """
    command = f"*VREAD,{parr},{fname},{ext},,{label},{n1},{n2},{n3},{nskip}"
    return self.run(command, **kwargs)
