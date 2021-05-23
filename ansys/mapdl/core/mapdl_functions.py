"""Pythonic MAPDL Commands"""

def ddaspec(self, keyref="", shptyp="", mountloc="", deftyp="", amin="",
            **kwargs):
    """APDL Command: DDASPEC

    Specifies the shock spectrum computation constants for DDAM analysis.

    Parameters
    ----------
    keyref
        Key for reference catalog:

        1 - The spectrum computation constants are based on NRL-1396 (default). For more
            information, see Dynamic Design Analysis Method in the
            Mechanical APDL Theory Reference

    shptyp
        Select the ship type:

        SUBM - Submarine

        SURF - Surface ship

    mountloc
        Select the mounting location:

        HULL - Hull mounting location. These structures are mounted directly to basic hull
               structures like frames, structural bulkheads below the water
               line, and shell plating above the water line.

        DECK - Deck mounting location. These structures are mounted directly to decks, non-
               structural bulkheads, or to structural bulkheads above the
               water line.

        SHEL - Shell plating mounting location. These structures are mounted directly to shell
               plating below the water line without intervening
               foundations.

    deftyp
        Select the deformation type:

        ELAS - Elastic deformation (default)

        PLAS - Elastic-plastic deformation

    amin
        Minimum acceleration value in inch/sec2. It defaults to 2316
        inch/sec2 which equals 6g, where g is the acceleration due to
        gravity (g = 386 in/sec2).

    Notes
    -----
    The excitation direction is required to calculate the spectrum
    coefficients. Issue the SED command before issuing DDASPEC.

    ADDAM and VDDAM may alternatively be used to calculate spectrum
    coefficients.

    This command is also valid in PREP7.
    """
    command = "DDASPEC,%s,%s,%s,%s,%s" % (str(keyref), str(shptyp), str(mountloc), str(deftyp), str(amin))
    return self.run(command, **kwargs)


def starvput(self, parr="", entity="", entnum="", item1="", it1num="",
             item2="", it2num="", kloop="", **kwargs):
    """APDL Command: *VPUT

    Restores array parameter values into the ANSYS database.

    Parameters
    ----------
    parr
        The name of the input vector array parameter.  See *SET for name
        restrictions.  The parameter must exist as a dimensioned array
        [*DIM] with data input.

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
    The *VPUT command is not supported for PowerGraphics displays.
    Inconsistent results may be obtained if this command is not used in
    /GRAPHICS, FULL.

    Plot and print operations entered via the GUI (Utility Menu> Pltcrtls,
    Utility Menu> Plot) incorporate the AVPRIN command. This means that the
    principal and equivalent values are recalculated. If you use *VPUT to
    put data back into the database, issue the plot commands from the
    command line to preserve your data.

    This operation is basically the inverse of the *VGET operation.  Vector
    items are put directly (without any coordinate system transformation)
    into the ANSYS database.  Items can only replace existing items of the
    database and not create new items.  Degree of freedom results that are
    replaced in the database are available for all subsequent
    postprocessing operations.  Other results are changed temporarily and
    are available mainly for the immediately following print and display
    operations.  The vector specification *VCUM does not apply to this
    command.  The valid labels for the location fields (Entity, ENTNUM,
    Item1, and IT1NUM) are listed below.  Item2 and IT2NUM are not
    currently used.  Not all items from the *VGET list are allowed on *VPUT
    since putting values into some locations could cause the database to be
    inconsistent.

    This command is valid in any processor.

    Table: 250:: : *VPUT - POST1 Items

    X, Y, or Z fluid velocity. X, Y, or Z nodal velocity in a transient
    structural analysis (LS-DYNA analysis or analysis with ANTYPE,TRANS).

    X, Y, or Z magnetic vector potential. X, Y, or Z nodal acceleration in
    a transient structural analysis (LS-DYNA analysis or analysis with
    ANTYPE,TRANS).
    """
    command = "*VPUT,%s,%s,%s,%s,%s,%s,%s,%s" % (str(parr), str(entity), str(entnum), str(item1), str(it1num), str(item2), str(it2num), str(kloop))
    return self.run(command, **kwargs)


def fctyp(self, oper="", lab="", **kwargs):
    """APDL Command: FCTYP

    Activates or removes failure-criteria types for postprocessing.

    Parameters
    ----------
    oper
        Operation key:

        ADD - Activate failure-criteria types. This option is the default behavior.

        DELE - Remove failure-criteria types.

    lab
        Valid failure-criteria labels. If ALL, select all available
        (including user-defined) failure criteria.

        EMAX - Maximum strain criterion (default)

        SMAX - Maximum stress criterion (default)

        TWSI  - Tsai-Wu strength index (default)

        TWSR  - Inverse of Tsai-Wu strength ratio index (default)

        HFIB  - Hashin fiber failure criterion

        HMAT  - Hashin matrix failure criterion

        PFIB  - Puck fiber failure criterion

        PMAT  - Puck inter-fiber (matrix) failure criterion

        L3FB - LaRc03 fiber failure criterion

        L3MT - LaRc03 matrix failure criterion

        L4FB - LaRc04 fiber failure criterion

        L4MT - LaRc04 matrix failure criterion

        USR1 through USR9  - User-defined failure criteria

    Notes
    -----
    The FCTYP command modifies the list of active failure criteria.

    By default, active failure criteria include EMAX, SMAX, TWSI, and TWSR.

    The command affects any subsequent postprocessing listing and plotting
    commands (such as PRESOL, PRNSOL, PLESOL, PLNSOL, and ETABLE).

    A single FCTYP command allows up to six failure-criteria labels. If
    needed, reissue the command to activate or remove additional failure-
    criteria types.
    """
    command = "FCTYP,%s,%s" % (str(oper), str(lab))
    return self.run(command, **kwargs)


def seltol(self, toler="", **kwargs):
    """APDL Command: SELTOL

    Sets the tolerance for subsequent select operations.

    Parameters
    ----------
    toler
        Tolerance value. If blank, restores the default tolerance logic.

    Notes
    -----
    For selects based on non-integer numbers (e.g. coordinates, results,
    etc.), items within the range VMIN - Toler and VMAX + Toler are
    selected, where VMIN and VMAX are the range values input on the xSEL
    commands (ASEL, ESEL, KSEL, LSEL, NSEL, and VSEL).

    The default tolerance logic is based on the relative values of VMIN and
    VMAX as follows:

    If VMIN = VMAX, Toler = 0.005 x VMIN.

    If VMIN = VMAX = 0.0, Toler = 1.0E-6.

    If VMAX ≠ VMIN, Toler = 1.0E-8 x (VMAX-VMIN).

    This command is typically used when VMAX-VMIN is very large so that the
    computed default tolerance is therefore large and the xSEL commands
    selects more than what is desired.

    Toler remains active until respecified by a subsequent SELTOL command.
    A SELTOL < blank > resets back to the default Toler logic.
    """
    command = "SELTOL,%s" % (str(toler))
    return self.run(command, **kwargs)


def starlist(self, fname="", ext="", **kwargs):
    """APDL Command: *LIST

    Displays the contents of an external, coded file.

    Parameters
    ----------
    fname
        File name and directory path (248 characters maximum, including the
        characters needed for the directory path).  An unspecified
        directory path defaults to the working directory; in this case, you
        can use all 248 characters for the file name.

    ext
        Filename extension (eight-character maximum).

    Notes
    -----
    Displays the contents of an external, coded file.  The file to be
    listed cannot be in use (open) at the time (except for the error file,
    File.ERR, which may be displayed with *LIST,ERR).

    Use caution when you are listing active ANSYS files via the List>
    Files> Other and File> List> Other menu paths.  File I/O buffer and
    system configurations can result in incomplete listings unless the
    files are closed.

    This command is valid in any processor.
    """
    command = "*LIST,%s,%s" % (str(fname), str(ext))
    return self.run(command, **kwargs)


def lsrestore(self, enginename="", filename="", **kwargs):
    """APDL Command: *LSRESTORE

    Restores a linear solver engine from a binary file.

    Parameters
    ----------
    enginename
        Name used to identify this engine.

    filename
        Name of the file to read from.

    Notes
    -----
    Restores a previously dumped Linear Solver (see the *LSDUMP command).
    This Linear Solver can be used to solve a linear system using the
    *LSBAC command.
    """
    command = "*LSRESTORE,%s,%s" % (str(enginename), str(filename))
    return self.run(command, **kwargs)


def starvplot(self, parx="", pary="", y2="", y3="", y4="", y5="", y6="",
              y7="", y8="", **kwargs):
    """APDL Command: *VPLOT

    Graphs columns (vectors) of array parameters.

    Parameters
    ----------
    parx
        Name of the array parameter whose column vector values will be the
        abscissa of the graph.  If blank, row subscript numbers are used
        instead.  ParX is not sorted by the program.

    pary
        Name of the array parameter whose column vector values will be
        graphed against the ParX values.

    y2, y3, y4, . . . , y8
        Additional column subscript of the ParY array parameter whose
        values are to be graphed against the ParX values.

    Notes
    -----
    The column to be graphed and the starting row for each array parameter
    must be specified as subscripts.  Additional columns of the ParY array
    parameter may be graphed by specifying column numbers for Y2,  Y3,
    ...,Y8.  For example, *VPLOT,TIME (4,6), DISP (8,1),2,3 specifies that
    the 1st, 2nd, and 3rd columns of array parameter DISP (all starting at
    row 8) are to be graphed against the 6th column of array parameter TIME
    (starting at row 4).  The columns are graphed from the starting row to
    their maximum extent.  See the *VLEN and  *VMASK commands to limit or
    skip data to be graphed.  The array parameters specified on the *VPLOT
    command must be of the same type (type ARRAY or TABLE; [*DIM].   Arrays
    of type TABLE are graphed as continuous curves.  Arrays of type ARRAY
    is displayed in bar chart fashion.

    The normal curve labeling scheme for *VPLOT is to label curve 1 "COL
    1", curve 2 "COL 2" and so on. You can use the /GCOLUMN command to
    apply user-specified labels (8 characters maximum) to your curves. See
    Modifying Curve Labels in the ANSYS Parametric Design Language Guide
    for more information on using /GCOLUMN.

    When a graph plot reaches minimum or maximum y-axis limits, the program
    indicates the condition by clipping the graph. The clip appears as a
    horizontal magenta line. Mechanical APDL calculates y-axis limits
    automatically; however, you can modify the (YMIN and YMAX) limits via
    the /YRANGE command.

    This command is valid in any processor.
    """
    command = "*VPLOT,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(parx), str(pary), str(y2), str(y3), str(y4), str(y5), str(y6), str(y7), str(y8))
    return self.run(command, **kwargs)


def wrk(self, num="", **kwargs):
    """APDL Command: *WRK

    Sets the active workspace number.

    Parameters
    ----------
    num
        Number of the active memory workspace for APDLMath vector and
        matrices. All the following APDLMath vectors and matrices will
        belong to this memory workspace, until the next call to the *WRK
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


def slashdelete(self, fname="", ext="", distkey="", **kwargs):
    """APDL Command: /DELETE

    Deletes a file.

    Parameters
    ----------
    fname
        File name and directory path (248 characters maximum,
        including the characters needed for the directory path).
        An unspecified directory path defaults to the working
        directory; in this case, you can use all 248 characters
        for the file name.

    ext
        Filename extension (eight-character maximum).

    distkey
        Key that specifies whether the file deletion is performed
        on all processes in distributed parallel mode (Distributed
        ANSYS):

        1 (ON or YES) - The program performs the file deletion
        locally on each process.

        0 (OFF or NO) - The program performs the file deletion
        only on the master process (default).

    Notes
    -----
    In distributed parallel mode (Distributed ANSYS), only the
    master process will delete Fname.Ext by default. However, when
    DistKey is set to 1 (or ON or YES), the command is executed by
    all processes. In this case, Fname will automatically have the
    process rank appended to it.  This means FnameN.Ext will be
    deleted by all processes, where N is the Distributed ANSYS
    process rank. For more information see Differences in General
    Behavior in the Parallel Processing Guide.
    """
    return self.run(f"/DELETE,{fname},{ext},,{distkey}", **kwargs)


def secfunction(self, table="", kcn="", **kwargs):
    """APDL Command: SECFUNCTION

    Specifies shell section thickness as a tabular function.

    Parameters
    ----------
    table
        Table name or array parameter reference for specifying thickness.

    kcn
        Local coordinate system reference number or array interpretation
        pattern for this tabular function evaluation.

    Notes
    -----
     The SECFUNCTION command is associated with the section most recently
    defined via the SECTYPE command.

    A table (TABLE) can define tabular thickness as a function of
    coordinates. Alternatively, you can use an array parameter (indexed by
    node number) that expresses the function to be mapped. (For example,
    func (17) should be the desired shell thickness at node 17.)  To
    specify a table, enclose the table or array name in percent signs (%)
    (SECFUNCTION,%tablename%). Use the *DIM command to define a table.

    The table or array defines the total shell thickness at any point in
    space. In multilayered sections, the total thickness and each layer
    thickness are scaled accordingly.

    The Function Tool is a convenient way to define your thickness tables.
    For more information, see Using the Function Tool in the Basic Analysis
    Guide.

    If you do not specify a local coordinate system (KCN), the program
    interprets TABLE in global XYZ coordinates. (For information about
    local coordinate systems, see the LOCAL command documentation.)

    When KCN = NODE, the program interprets TABLE as an array parameter
    (indexed by node number) that expresses the function to be mapped.

    When KCN = NOD2, the program interprets TABLE as a 2-D array parameter
    (where columns contain node numbers and rows contain the corresponding
    thicknesses) that expresses the function to be mapped.
    """
    command = "SECFUNCTION,%s,%s" % (str(table), str(kcn))
    return self.run(command, **kwargs)


def starvget(self, parr="", entity="", entnum="", item1="", it1num="",
             item2="", it2num="", kloop="", **kwargs):
    """APDL Command: *VGET

    Retrieves values and stores them into an array parameter.

    Parameters
    ----------
    parr
        The name of the resulting vector array parameter.  See *SET for
        name restrictions.

    entity
        Entity keyword.  Valid keywords are NODE, ELEM, KP, LINE, AREA,
        VOLU, etc. as shown for Entity = in the tables below.

    entnum
        The number of the entity (as shown for ENTNUM = in the tables
        below).

    item1
        The name of a particular item for the given entity.  Valid items
        are as shown in the Item1 columns of the tables below.

    it1num
        The number (or label) for the specified Item1 (if any).  Valid
        IT1NUM values are as shown in the IT1NUM columns of the tables
        below.  Some Item1 labels do not require an IT1NUM value.

    item2, it2num
        A second set of item labels and numbers to further qualify the item
        for which data is to be retrieved.  Most items do not require this
        level of information.

    kloop
        Field to be looped on:

        Loop on the ENTNUM  field (default). - Loop on the Item1 field.

        Loop on the IT1NUM field.  Successive items are as shown with IT1NUM. - Loop on the Item2 field.

    Notes
    -----
    Retrieves values for specified items and stores the values in an output
    vector of a user-named array parameter according to:

    ParR = f(Entity, ENTNUM, Item1, IT1NUM, Item2, IT2NUM)

    where (f) is the *GET function; Entity, Item1, and Item2 are keywords;
    and ENTNUM, IT1NUM, and IT2NUM are numbers or labels corresponding to
    the keywords. Looping continues over successive entity numbers (ENTNUM)
    for the KLOOP default.  For example, *VGET,A(1),ELEM,5,CENT,X returns
    the centroid x-location of element 5 and stores the result in the first
    location of A.  Retrieving continues with element 6, 7, 8, etc.,
    regardless of whether the element exists or is selected, until
    successive array locations are filled.  Use *VLEN or *VMASK to skip
    locations. Absolute values and scale factors may be applied to the
    result parameter [*VABS, *VFACT].  Results may be cumulative [*VCUM].
    See the *VOPER command for general details.  Results can be put back
    into an analysis by writing a file of the desired input commands with
    the *VWRITE command.  See also the *VPUT command.

    Both *GET and *VGET retrieve information from the active data stored in
    memory. The database is often the source, and sometimes the information
    is retrieved from common memory blocks that ANSYS uses to manipulate
    information. Although POST1 and POST26 operations use a *.rst file, GET
    data is accessed from the database or from the common blocks. Get
    operations do not access the *.rst file directly.

    The *VGET command retrieves both the unprocessed real and the imaginary
    parts (original and duplicate sector nodes and elements) of a cyclic
    symmetry solution.

    Each of the sections for accessing *VGET parameters are shown in the
    following order:

    *VGET PREP7 Items

    *VGET POST1 Items

    This command is valid in any processor.
    """
    command = "*VGET,%s,%s,%s,%s,%s,%s,%s,%s" % (str(parr), str(entity), str(entnum), str(item1), str(it1num), str(item2), str(it2num), str(kloop))
    return self.run(command, **kwargs)


def secmodif(self, secid="", kywrd="", **kwargs):
    """APDL Command: SECMODIF

    Modifies a pretension section

    Parameters
    ----------
    secid
        Unique section number. This number must already be assigned to a
        section.

    norm
        Keyword specifying that the command will modify the pretension
        section normal direction.

    nx, ny, nz
        Specifies the individual normal components to modify.

    kcn
        Coordinate system number. This can be either 0 (Global Cartesian),
        1 (Global Cylindrical) 2 (Global Spherical), 4 (Working Plane), 5
        (Global Y Axis Cylindrical) or an arbitrary reference number
        assigned to a coordinate system.

    Notes
    -----
    The SECMODIF command either modifies the normal for a specified
    pretension section, or changes the name of the specified pretension
    surface.
    """
    command = "SECMODIF,%s,%s" % (str(secid), str(kywrd))
    return self.run(command, **kwargs)
