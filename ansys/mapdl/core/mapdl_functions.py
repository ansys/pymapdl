"""Pythonic MAPDL Commands"""

def felist(self, nev1="", nev2="", ninc="", **kwargs):
    """APDL Command: FELIST

    Lists the fatigue event parameters.

    Parameters
    ----------
    nev1, nev2, ninc
        List event parameters from NEV1 (defaults to 1) to NEV2 (defaults
        to NEV1) in steps of NINC (defaults to 1).  If NEV1 = ALL, NEV2 and
        NINC are ignored and all events are listed.  Fatigue event
        parameters are defined with the FE command.
    """
    command = "FELIST,%s,%s,%s" % (str(nev1), str(nev2), str(ninc))
    return self.run(command, **kwargs)











def wfront(self, kprnt="", kcalc="", **kwargs):
    """APDL Command: WFRONT

    Estimates wavefront statistics.

    Parameters
    ----------
    kprnt
        Wavefront history print key:

        0 - Print current wavefront statistics.

        1 - Print current wavefront statistics but also print wavefront history (wavefront
            at each element).  Elements are listed in the reordered
            sequence.

    kcalc
        Calculation options:

        0 - Wavefront estimate assumes maximum model DOF set at each node and does not
            include the effects of master degrees of freedom and specified
            displacement constraints.

        1 - Wavefront estimate uses the actual DOF set at each node and does not include
            the effects of master degrees of freedom and specified
            displacement constraints.  More time consuming than estimated
            wavefront.  KPRNT = 1 is not available with this option.

    Notes
    -----
    Estimates wavefront statistics of the model as currently ordered.

    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    command = "WFRONT,%s,%s" % (str(kprnt), str(kcalc))
    return self.run(command, **kwargs)





def slashexpand(self, nrepeat1="", type1="", method1="", dx1="", dy1="",
                dz1="", nrepeat2="", type2="", method2="", dx2="", dy2="",
                dz2="", nrepeat3="", type3="", method3="", dx3="", dy3="",
                dz3="", **kwargs):
    """APDL Command: /EXPAND

    Allows the creation of a larger graphic display than represented by the
    actual finite element analysis model.

    Parameters
    ----------
    nrepeat1, nrepeat2, nrepeat3
        The number of repetitions required for the element pattern. The
        default is 0 (no expansion).

    type1, type2, type3
        The type of expansion requested.

        RECT - Causes a Cartesian transformation of DX, DY, and DZ for each pattern (default).

        POLAR - Causes a polar transformation of DR, D-Theta and DZ for each pattern.

        AXIS - Causes 2-D axisymmetric expansion (that is, rotates a 2-D model created in the
               X-Y plane about the Y axis to create a 3-D model).

        LRECT - Causes a Cartesian transformation of DX, DY, and DZ for each pattern about the
                current local coordinate system (specified via the CSYS
                command).

        LPOLAR - Causes a polar transformation of DR, D-Theta, and DZ for each pattern about the
                 local coordinate system (specified via the CSYS command).

    method1, method2, method3
        The method by which the pattern is repeated.

        FULL - Causes a normal repeat of the pattern (default).

        HALF - Uses a symmetry transformation for alternate repeats (to produce an image of a
               complete circular gear from the image of half a tooth, for
               example).

    dx1, dy1, dz1, dx2, dy2, dz2, dx3, dy3, dz3
        The Cartesian or polar increments between the repeated patterns.
        Also determines the reflection plane. Reflection is about the plane
        defined by the normal vector (DX, DY, DZ). If you want no
        translation, specify a small nonzero value.  For a half-image
        expansion, the increment DX, DY, or DZ is doubled so that
        POLAR,HALF, ,45 produces full images on 90° centers, and RECT,HALF,
        ,1 produces full images on 2-meter centers.

    Notes
    -----
    You can use the /EXPAND command to perform up to three symmetry
    expansions at once (that is, X, Y, and Z which is equal to going from a
    1/8 model to a full model). Polar expansions allow you to expand a
    wheel section into a half wheel, then into the half section, and then
    into the whole.

    The command displays elements/results when you issue the EPLOT command
    or postprocessing commands.

    The command works on all element and result displays, except as noted
    below. As the graphic display is created, the elements (and results)
    are repeated as many times as necessary, expanding the geometry and, if
    necessary, the displacements and stresses.

    Derived results are not supported.

    The /EXPAND command has the following limitations:

    It does not support solid model entities.

    POLAR, FULL or HALF operations are meaningful only in global
    cylindrical systems and are unaffected by the RSYS or DSYS commands.
    Cartesian symmetry or unsymmetric operations also occur about the
    global Cartesian system.

    It does not average nodal results across sector boundaries, even for
    averaged plots (such as those obtained via the PLNSOL command).

    Axisymmetric harmonic element results are not supported for Type =
    AXIS.

    The /EXPAND command differs significantly from the EXPAND command in
    several respects:

    The uses of /EXPAND are of a more general nature, whereas the EXPAND
    command is intended primarily to expand modal cyclic symmetry results.

    /EXPAND does not change the database as does the EXPAND command.

    You cannot print results displayed via /EXPAND.


    """
    command = "/EXPAND,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(nrepeat1), str(type1), str(method1), str(dx1), str(dy1), str(dz1), str(nrepeat2), str(type2), str(method2), str(dx2), str(dy2), str(dz2), str(nrepeat3), str(type3), str(method3), str(dx3), str(dy3), str(dz3))
    return self.run(command, **kwargs)



def repeat(self, ntot="", vinc1="", vinc2="", vinc3="", vinc4="", vinc5="",
           vinc6="", vinc7="", vinc8="", vinc9="", vinc10="", vinc11="",
           **kwargs):
    """APDL Command: *REPEAT

    Repeats the previous command.

    Parameters
    ----------
    ntot
        Number of times the preceding command is executed (including the
        initial execution).  Must be 2 or greater.  NTOT of 2 causes one
        repeat (for a total of 2 executions).

    vinc1, vinc2,  vinc3, . . . , vinc11
        Value increments applied to first through eleventh data fields of
        the preceding command.

    Notes
    -----
    *REPEAT must immediately follow the command that is to be repeated.
    The numeric arguments of the initial command may be incremented in the
    generated commands.  The numeric increment values may be integer or
    real, positive or negative, zero or blank.  Alphanumeric arguments
    cannot be incremented.  For large values of NTOT, consider printout
    suppression (/NOPR command) first.

    Most commands beginning with slash (/), star (*), as well as "unknown
    command" macros, cannot be repeated.  For these commands, or if more
    than one command is to be repeated, include them within a do-loop. File
    switching commands (those reading additional commands) cannot be
    repeated.  If a *REPEAT command  immediately follows another *REPEAT
    command, the repeat action only applies to the last non-*REPEAT
    command.  Also, *REPEAT should not  be used in interactive mode
    immediately after a) a command (or its log file equivalent) that uses
    picking, or b) a command that requires a response from the user.

    This command is valid in any processor.
    """
    command = "*REPEAT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(ntot), str(vinc1), str(vinc2), str(vinc3), str(vinc4), str(vinc5), str(vinc6), str(vinc7), str(vinc8), str(vinc9), str(vinc10), str(vinc11))
    return self.run(command, **kwargs)


def cycexpand(self, wn="", option="", value1="", value2="", **kwargs):
    """APDL Command: /CYCEXPAND

    Graphically expands displacements, stresses and strains of a cyclically
    symmetric model.

    Parameters
    ----------
    wn
        The window number to which the expansion applies. Valid values are
        1 through 5. The default value is 1. The window number applies only
        to the AMOUNT argument.

    option
        One of the following options:

        ON - Activates cyclic expansion using the previous settings (if any). If no previous
             settings exist, this option activates the default settings.

        DEFAULT - Resets cyclic expansion to the default settings.

        OFF - Deactivates cyclic expansion. This option is the default.

        STATUS - Lists the current cyclic expansion settings.

        AMOUNT - The number of repetitions or the total angle.

        Value1 - NREPEAT

        Value2 - The number of repetitions. The default is the total number of sectors in 360
                 degrees.

        or - Value1

        ANGLE - Value2

        The total angle in degrees. The default is 360. - WHAT

        A specified portion or subset of the model to expand: - Value1

        The component name of the elements to expand. The default is all selected components. - EDGE

        Sector edge display key. - -1

        Suppresses display of edges between sectors even if the cyclic count varies between active windows. - Caution:  Plots with fewer than the maximum number of repetitions may have
                          missing element faces at the sector boundaries.

        0 or OFF - Averages stresses or strains across sector boundaries. This value is the
                   default (although the default reverts to 1 or ON if the
                   cyclic count varies between active windows).

        1 or ON - No averaging of stresses or strains occurs and sector boundaries are shown on
                  the plot.

        PHASEANG - The phase angle shift:

        Value1 - The phase angle shift in degrees. The valid range is 0 through 360. The default
                 is 0. For a full harmonic solution, this value is
                 typically the phase angle obtained via the CYCPHASE
                 command. If Value1 = AMPLITUDE (or if Value1 ≥ 360), the
                 amplitude is supplied. The amplitude solution for non-
                 component results (such as equivalent stress) are not
                 valid. For a mode-superposition harmonic solution, if
                 Value1 = SWEEP, the maximum values across a phase angle
                 sweep are supplied.

    Notes
    -----
    In preprocessing, the /CYCEXPAND command verifies a cyclically
    symmetric model by graphically expanding it partially or through the
    full 360 degrees.

    For the postprocessing plot nodal solution (PLNSOL) operation, the
    command graphically expands displacements, stresses and strains of a
    cyclically symmetric model partially or though the full 360 degrees by
    combining the real (original nodes and elements) and imaginary
    (duplicate nodes and elements) parts of the solution.

    For the print nodal solution (PRNSOL) operation, the command expands
    the printed output of displacements or stresses on a sector-by-sector
    basis.

    Use of the /CYCEXPAND command does not change the database. The command
    does not modify the geometry, nodal displacements or element stresses.

    The command affects element and result plots only. It has no effect on
    operations other than plot element solution (PLESOL), plot nodal
    solution (PLNSOL), print nodal solution (PRNSOL), and calculate
    harmonic solution (CYCCALC). Operations other than PLESOL, PLNSOL,
    PRNSOL, or CYCCALC work on the unprocessed real and imaginary parts of
    a cyclic symmetry solution

    If you issue a /CYCEXPAND,,OFF command, you cannot then expand the
    model by simply issuing another  /CYCEXPAND command  (for example, to
    specify an NREPEAT value for the number of repetitions). In such a
    case, you must specify /CYCEXPAND,,ON, which activates expansion using
    the previous settings (if any) or the default settings.

    The command requires PowerGraphics and will turn PowerGraphics on
    (/GRAPHICS,POWER) if not already active. Any setting which bypasses
    PowerGraphics (for example, /PBF) also bypasses cyclic expansion; in
    such cases, the /CYCEXPAND command displays unprocessed real and
    imaginary results.

    The CYCPHASE command uses full model graphics (/GRAPHICS,FULL) to
    compute peak values. Because of this, there may be slight differences
    between max/min values obtained with CYCPHASE, and those obtained via
    /CYCEXPAND, which uses power graphics (/GRAPHICS,POWER).

    For PHASEANG = AMPLITUDE (or 360) with a cyclic full harmonic solution,
    the only appropriate coordinate system is the solution coordinate
    system (RSYS,SOLU)

    To learn more about analyzing a cyclically symmetric structure, see the
    Cyclic Symmetry Analysis Guide.
    """
    command = "/CYCEXPAND,%s,%s,%s,%s" % (str(wn), str(option), str(value1), str(value2))
    return self.run(command, **kwargs)



def slashline(self, x1="", y1="", x2="", y2="", **kwargs):
    """APDL Command: /LINE

    Creates annotation lines (GUI).

    Parameters
    ----------
    x1
        Line X starting location (-1.0 < X < 2.0).

    y1
        Line Y starting location (-1.0 < Y < 1.0).

    x2
        Line X ending location (-1.0 < X < 2.0).

    y2
        Line Y ending location (-1.0 < Y < 1.0).

    Notes
    -----
    Defines annotation lines to be written directly onto the display at a
    specified location.  This is a command generated by the Graphical User
    Interface (GUI) and will appear in the log file (Jobname.LOG) if
    annotation is used.  This command is not intended to be typed in
    directly in an ANSYS session (although it can be included in an input
    file for batch input or for use with the /INPUT command).

    All lines are shown on subsequent displays unless the annotation is
    turned off or deleted.  Use the /LSPEC command to set the attributes of
    the line.

    This command is valid in any processor.
    """
    command = "/LINE,%s,%s,%s,%s" % (str(x1), str(y1), str(x2), str(y2))
    return self.run(command, **kwargs)


def slashreset(self, **kwargs):
    """APDL Command: /RESET

    Resets display specifications to their initial defaults.

    Notes
    -----
    Resets slash display specifications (/WINDOW, /TYPE, /VIEW, etc.) back
    to their initial default settings (for convenience).  Also resets the
    focus location to the geometric center of the object.

    This command is valid in any processor.
    """
    command = "/RESET,"
    return self.run(command, **kwargs)


def lsdump(self, enginename="", filename="", **kwargs):
    """APDL Command: *LSDUMP

    Dumps a linear solver engine to a binary File.

    Parameters
    ----------
    enginename
        Name used to identify this engine. Must have been previously
        created using *LSENGINE and factorized using *LSFACTOR.

    filename
        Name of the file to create.

    Notes
    -----
    Dumps a previously factorized linear solver system to a binary file.
    Only LAPACK and BCS linear solvers can be used with this feature. The
    Linear Solver can later be restored with the *LSRESTORE command.

    A BCS Sparse Solver can be dumped only if uses the INCORE memory option
    (see BCSOPTION).
    """
    command = "*LSDUMP,%s,%s" % (str(enginename), str(filename))
    return self.run(command, **kwargs)




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


def fmagbc(self, cnam1="", cnam2="", cnam3="", cnam4="", cnam5="",
           cnam6="", cnam7="", cnam8="", cnam9="", **kwargs):
    """APDL Command: FMAGBC

    Applies force and torque boundary conditions to an element component.

    Parameters
    ----------
    cnam1, cnam2, cnam3, . . . , cnam9
        Names of existing element components (CM command).  Must be
        enclosed in single quotes (e.g., `Cnam1') when the command is
        manually typed in.

    Notes
    -----
    FMAGBC invokes a predefined ANSYS macro to apply Maxwell and virtual
    work force and torque boundary conditions to an element component.
    These boundary conditions are used for subsequent force and torque
    calculations during solution.  Magnetic virtual displacements (MVDI =
    1) are applied to nodes of elements in the components, and  Maxwell
    surface flags (MXWF) are applied to air elements adjoining the element
    components.  Incorrect force and torque calculations will occur for
    components sharing adjacent air elements.   Companion macros FMAGSUM
    and TORQSUM can be used in POST1 to summarize the force and torque
    calculations, respectively.  Torque calculations are valid for 2-D
    planar analysis only.  For 2-D harmonic analysis, force and torque
    represent time-average values.

     If using elements PLANE121, SOLID122, SOLID123, PLANE233, SOLID236 and
    SOLID237 (static analyses only), use EMFT to summarize electromagnetic
    force and torque. If you do use FMAGSUM, you do not need to first set
    either the Maxwell or the virtual work force flags via FMAGBC.
    """
    command = "FMAGBC,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(cnam1), str(cnam2), str(cnam3), str(cnam4), str(cnam5), str(cnam6), str(cnam7), str(cnam8), str(cnam9))
    return self.run(command, **kwargs)


def torqc2d(self, rad="", numn="", lcsys="", **kwargs):
    """APDL Command: TORQC2D

    Calculates torque on a body in a magnetic field based on a circular
    path.

    Parameters
    ----------
    rad
        Radius of the circular path.  The nodes for the path are created at
        this radius.

    numn
        Number of nodes to be created for the circular path.  The greater
        the number of nodes, the higher the accuracy of the torque
        evaluation.  Defaults to 18.

    lcsys
        (Optional) Local coordinate system number to be used for defining
        the circular arc of nodes and the path.  Defaults to 99.  (If a
        local system numbered 99 already exists, it will be overwritten by
        this default.)

    Notes
    -----
    TORQC2D invokes an ANSYS macro which calculates the mechanical torque
    on a body using a circular path.  It is used for a circular or
    cylindrical body such as a rotor in an electric machine.  The body must
    be centered about the global origin and must be surrounded by air
    elements.  The air elements surrounding the path at radius RAD must be
    selected, and elements with a high-permeability material should be
    unselected prior to using the macro.  The macro is valid for 2-D planar
    analyses only.  For a harmonic analysis, the macro calculates the time-
    average torque.  Radial symmetry models are allowed, i.e., the model
    need not be a full 360° model.

    The calculated torque is stored in the parameter TORQUE.  If the model
    is not a full 360° model, TORQUE should be multiplied by the
    appropriate factor (such as 4.0 for a 90° sector) to obtain the total
    torque.  A node plot showing the path is produced in interactive mode.

    The torque is calculated via a circular path integral of the Maxwell
    stress tensor.  The circular path and the nodes for the path are
    created by the macro at the specified radius RAD.  Path operations are
    used for the calculation, and all path items are cleared upon
    completion.  See the TORQ2D command for torque calculation based on an
    arbitrary, non-circular path.
    """
    command = "TORQC2D,%s,%s,%s" % (str(rad), str(numn), str(lcsys))
    return self.run(command, **kwargs)



def rsprnt(self, rslab="", yname="", xout="", **kwargs):
    """APDL Command: RSPRNT

    Print a response surface.

    Parameters
    ----------
    rslab
        Response Surface set label. Identifies the response surfaces
        generated by the RSFIT command.

    yname
        Parameter name. The parameter must have been previously defined as
        a random output parameter with the PDVAR command. Identifies the
        parameter for which a response surface has been generated by the
        RSFIT command.

    xout
        An option if an extended print-out of more feedback about goodness-
        of-fit and the details of the regression analysis of the response
        surface is requested.

        No - Use the standard print-out (default).

        Yes - Use the extended print-out.

    Notes
    -----
    Prints the results and details of a response surface analysis generated
    by the RSFIT command. For the specified output parameter Yname, the
    fitting details such as the individual terms of the response surface
    model and their corresponding coefficients are listed. The command also
    produces a comparison of the original values of Yname used for the
    fitting process and the approximate values derived from the fitting,
    and some goodness of fit measures.

    If Xout = Yes, then more information about the regression analysis of
    the response surface will be printed. For example, the confidence
    intervals on the regression coefficients and the correlation between
    the regression coefficients among others.
    """
    command = "RSPRNT,%s,%s,%s" % (str(rslab), str(yname), str(xout))
    return self.run(command, **kwargs)




def reorder(self, **kwargs):
    """APDL Command: REORDER

    Specifies "Model reordering" as the subsequent status topic.

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
    command = "REORDER,"
    return self.run(command, **kwargs)




def noorder(self, lab="", **kwargs):
    """APDL Command: NOORDER

    Re-establishes the original element ordering.

    Parameters
    ----------
    lab
        Turns element reordering on or off.

        ON (or blank) - Re-establishes original element ordering (default).

        OFF - Original ordering is not used and program establishes its own ordering at the
              beginning of the solution phase.

    Notes
    -----
    If Lab = ON, the original element ordering is re-established and no
    automatic reordering occurs at the beginning of the solution phase.
    Use Lab = OFF only to remove the effect of a previous NOORDER command.
    This command affects only those elements that were defined up to the
    point that this command is issued. See the WSORT and WAVES commands for
    reordering.

    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    command = "NOORDER,%s" % (str(lab))
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








def c(self, comment="", **kwargs):
    """APDL Command: C***

    Places a comment in the output.

    Parameters
    ----------
    comment
        Comment string, up to 75 characters.

    Notes
    -----
    The output from this command consists of two lines -- a blank line
    followed by a line containing C*** and the comment.  This command is
    similar to /COM except that the comment produced by C*** is more easily
    identified in the output.

    Another way to include a comment is to precede it with a ! character
    (on the same line).  The ! may be placed anywhere on the line, and any
    input following it is ignored as a comment.  No output is produced by
    such a comment, but the comment line is included on the log file.  This
    is a convenient way to annotate the log file.

    This command is valid anywhere.
    """
    command = "C***,%s" % (str(comment))
    return self.run(command, **kwargs)

def fe(self, nev="", cycle="", fact="", title="", **kwargs):
    """APDL Command: FE

    Defines a set of fatigue event parameters.

    Parameters
    ----------
    nev
        Reference number for this event (within MXEV).

    cycle
        Number of required cycles (defaults to 1).  If -1, erase all
        parameters and fatigue stresses for this event.

    fact
        Scale factor to be applied to all loadings in this event (defaults
        to 1.0).

    title
        User defined identification title for this event (up to 20
        characters).

    Notes
    -----
    Repeat FE command to define additional sets of event parameters (MXEV
    limit), to redefine event parameters, or to delete event stress
    conditions.

    The set of fatigue event parameters is associated with all loadings and
    all locations.  See the FTSIZE command for the maximum set of events
    (MXEV) allowed.
    """
    command = "FE,%s,%s,%s,%s" % (str(nev), str(cycle), str(fact), str(title))
    return self.run(command, **kwargs)



def rssims(self, rslab="", nsim="", seed="", **kwargs):
    """APDL Command: RSSIMS

    Performs Monte Carlo simulations on response surface(s).

    Parameters
    ----------
    rslab
        Response Surface set label. Identifies the response surfaces
        generated by the RSFIT command.

    nsim
        Number of simulation loops on the response surfaces that will be
        generated for all random output parameters. If the RSSIMS command
        is issued multiple times using the same response surface set label
        the NSIM Monte Carlo simulations is appended to previous ones. The
        default value for NSIM is 10,000.

    seed
        Seed value label. Random number generators require a seed value
        that is used to calculate the next random number. After each random
        number generation finishes, the seed value is updated and is used
        again to calculate the next random number. By default ANSYS
        initializes the seed value with the system time (one time only)
        when the ANSYS session started.

        CONT - Continues updating using the derived seed value (default).

        TIME - Initializes the seed value with the system time. You can use this if you want
               the seed value set to a specific value for one analysis and
               then you want to continue with a "random" seed in the next
               analysis. It is not recommended to "randomize" the seed
               value with the Seed = TIME option for multiple analyses. If
               the Monte Carlo simulations requested with this command will
               be appended to previously existing simulations, then the
               Seed option is ignored and Seed = CONT is used.

        INIT - Initializes the seed value using 123457. This value is a typical recommendation
               used very often in literature. This option leads to
               identical random numbers for all random input variables when
               the exact analysis will be repeated, making it useful for
               benchmarking and validation purposes (where identical random
               numbers are desired). If the Monte Carlo simulations
               requested with this command will be appended to previously
               existing simulations, then the Seed option is ignored and
               Seed = CONT is used.

        Value - Uses the specified (positive) value for the initialization of the seed value.
                This option has the same effect as Seed = INIT, except you
                can chose an arbitrary (positive) number for the
                initialization. If the Monte Carlo simulations requested
                with this command will be appended to previously existing
                simulations, then the Seed option is ignored and Seed =
                CONT is used.

    Notes
    -----
    Generate the Monte Carlo simulations on the response surfaces that are
    included in a response surface set. Simulations are evaluated only for
    the output parameters that have been fitted in a response surface set
    using the RSFIT command.

    If the RSSIMS command is issued multiple times using the same response
    surface label the probabilistic design system appends the samples
    generated here to the previous ones. This way you can start with a
    moderate NSIM number and add more samples if the probabilistic results
    are not accurate enough.
    """
    command = "RSSIMS,%s,%s,%s" % (str(rslab), str(nsim), str(seed))
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



def lmatrix(self, symfac="", coilname="", curname="", indname="",
            **kwargs):
    """APDL Command: LMATRIX

    Calculates an inductance matrix and the total flux linkage for an
    N-winding coil system.

    Parameters
    ----------
    symfac
        Geometric symmetry factor.  Inductance terms are scaled by this
        factor which represents the fraction of the total device modeled.
        Default is 1.

    coilname
        Alphanumeric prefix identifier for coil label used in defining
        named element coil components. Default is 'coil.'

    curname
        Name of a predefined parameter array containing the nominal coil
        currents of the system.  The array must be defined (see *DIM
        command) prior to calling the LMATRIX macro. Default is 'cur.'

    indname
        Name of the array parameter to be created by LMATRIX containing the
        calculated inductance matrix and the flux linkage in each coil.  A
        text file of the same name with an extension .TXT is created
        containing the matrix data. Default is 'lmatrix.'

    Notes
    -----
    LMATRIX calculates the differential inductance matrix for an N-winding
    system where N is the number of coils in the system, and calculates the
    total flux linkage in each coil. LMATRIX may only be executed after the
    solution of a problem with nominal currents applied to the coils at a
    desired "operating point." The array Indname has N rows and N+1
    columns. The N x N block is the differential inductance matrix; the
    N+1th column contains the total flux linkage, with the ith row
    corresponding to the ith coil. See the Mechanical APDL Theory Reference
    for more details.

    To invoke the LMATRIX macro, for the classical formulations, the
    elements for each coil must be grouped into a component using the CM
    command.  Each set of independent coil elements is assigned a component
    name with the prefix Coilname followed by the coil number. For the
    solenoidal formulations, you must make the exciting node with a F,AMPS
    load a node component using the CM command.  The classical and
    solenoidal formulations cannot be mixed.

    To invoke the LMATRIX macro, the vector array parameter Curname with
    dimension N must be defined and named using the *DIM command.  You must
    set each vector array entry equal to the nominal current per turn in
    the corresponding coil at the operating point.  Zero current values
    must be approximated by a negligibly small applied current.

    Do not apply (or remove) inhomogeneous loads before using the LMATRIX
    command. Inhomogeneous loads are those created by:

    Degree of freedom commands (D, DA, etc.) specifying nonzero degrees of
    freedom values on nodes or solid model entities

    Any CE command with a nonzero constant term

    Do not put any loads (for example, current) on elements not contained
    in the element component.

    Operating solutions must be obtained through static analysis before
    calling LMATRIX. All name-strings must be enclosed in single quotes in
    the LMATRIX command line. The geometric symmetry factor, Symfac,
    represents the fraction of the device modeled, disregarding any current
    source primitives.

    LMATRIX works only with magnetic field elements: PLANE53, SOLID96, and
    SOLID97, and with SOURC36 solenoidal formulations. For electromagnetic
    elements PLANE233, SOLID236 and SOLID237, static linear perturbation
    analysis can be used to calculate the differential inductance using the
    element incremental energy record (IENE).

    For more information, see LMATRIX in the Low-Frequency Electromagnetic
    Analysis Guide.

    See the Mechanical APDL Theory Reference and Electric and Magnetic
    Macros in the Low-Frequency Electromagnetic Analysis Guide for details.

    This command does not support multiframe restarts.

    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    command = "LMATRIX,%s,%s,%s,%s" % (str(symfac), str(coilname), str(curname), str(indname))
    return self.run(command, **kwargs)


def for2d(self, **kwargs):
    """APDL Command: FOR2D

    Calculates magnetic forces on a body.

    Notes
    -----
    FOR2D invokes an ANSYS macro which calculates magnetic forces on a body
    that is completely surrounded by air (symmetry permitted).  The
    calculated forces are stored in the parameters FX and FY.  In
    interactive mode, a node plot is produced with the integration path
    highlighted.  A predefined closed path [PATH], passing through the air
    elements surrounding the body, must be available for this calculation.
    A counterclockwise ordering of nodes on the PPATH command will give the
    correct sign on the forces.  Forces are calculated using a Maxwell
    stress tensor approach.  The macro is valid for 2-D planar or
    axisymmetric analysis.  Path operations are used for the calculations,
    and all path items are cleared upon completion.

    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    command = "FOR2D,"
    return self.run(command, **kwargs)

def rsplot(self, rslab="", yname="", x1name="", x2name="", type_="",
           npts="", plow="", pup="", **kwargs):
    """APDL Command: RSPLOT

    Plot a response surface.

    Parameters
    ----------
    rslab
        Response Surface set label. Identifies the response surfaces
        generated by the RSFIT command.

    yname
        Parameter name. The parameter must have been previously defined as
        a random output parameter with the PDVAR command.

    x1name
        Parameter name. The parameter must have been previously defined as
        a random input variable with the PDVAR command.

    x2name
        Parameter name. The parameter must have been previously defined as
        a random input variable with the PDVAR command. X2Name must be
        different than X1Name.

    type\_
        Type of the response surface visualization.

        2D - 2-D contour plot.

        3D - 3-D surface plot.

    npts
        Number of grid points for both the X1-axis and the X2-axis. The
        grid points are used for the evaluation of the response surface.
        The number must be between 1 and 500. Defaults to 20. If NPTS = 0
        or greater than 500, then a value of 20 is used.

    plow
        Lower probability level used to determine the lower boundary
        (plotting range) of the curve in case the random input variable
        does not have a minimum value (such as Gauss). This probability
        must be between 0.0 and 1.0. Defaults to 0.0025.

    pup
        Upper probability level used to determine the upper boundary of the
        curve. This probability must be between 0.0 and 1.0. Defaults to
        0.9975.

    Notes
    -----
     Plots the response surface of an output parameter YName as a function
    of two input parameters X1Name and X2Name.

    If PLOW is left blank, then a minimum value of the distribution is used
    for plotting, provided it exists (for example, uniform distribution).
    If the distribution type has no minimum value (for example, Gaussian
    distribution), then the default value is used to determine the lower
    plotting range value. The same is true for the maximum value if PUP is
    left blank.

    In addition to the response surface, the sampling points that are
    fitted by the response surface are also plotted by this command.
    However, sampling points falling outside of the plotting range defined
    by the PLOW and PUP fields will not be shown in the plot.
    """
    command = "RSPLOT,%s,%s,%s,%s,%s,%s,%s,%s" % (str(rslab), str(yname), str(x1name), str(x2name), str(type_), str(npts), str(plow), str(pup))
    return self.run(command, **kwargs)




def wsort(self, lab="", kord="", wopt="", oldmax="", oldrms="", **kwargs):
    """APDL Command: WSORT

    Initiates element reordering based upon a geometric sort.

    This command was removed by V18.2

    Parameters
    ----------
    lab
        Coordinate (in the active system) along which element
        centroid locations are sorted.  Valid labels are: X, Y, Z,
        ALL.  If ALL (default), all three directions will be used,
        and the order corresponding to the lowest MAX or RMS
        wavefront value will be retained.

    kord
        Sort order:

        0 - Sort according to ascending coordinate values.

        1 - Sort according to descending coordinate values.

    wopt
        Option for comparison:

        MAX - Use maximum wavefront value for comparison (default).

        RMS - Use RMS wavefront value.

    oldmax, oldrms
        MAX and RMS wavefront values of model to be used in place of the
        old values.  OLDRMS defaults to OLDMAX (and vice versa).  If
        neither is  specified, each defaults to its calculated old value.

    Notes
    -----
    Initiates element reordering based upon a geometric sort of the element
    centroid locations.  Wave lists, if any [WSTART], are ignored.
    Reordering affects only the element order for the solution phase and
    not the element numbers (input referring to element numbers, such as
    element pressures, is unaffected by reordering).

    Note: The new order is retained only if new the new maximum or RMS
    wavefront values are lower than the old values, as described below.
    See the WAVES command for another reordering procedure and for more
    details on reordering.  The resulting element ordering can be shown by
    listing the wavefront history [WFRONT,1] or by displaying elements with
    their element location numbers [/PNUM].

    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    return self.run(f"WSORT,{lab},{kord},,{wopt},{oldmax},{oldrms}", **kwargs)







def slashlarc(self, xcentr="", ycentr="", xlrad="", angle1="", angle2="",
              **kwargs):
    """APDL Command: /LARC

    Creates annotation arcs (GUI).

    Parameters
    ----------
    xcentr
        Arc X center location (-1.0 < X < 1.0).

    ycentr
        Arc Y center location (-1.0 < Y < 1.0).

    xlrad
        Arc radius length.

    angle1
        Starting angle of arc.

    angle2
        Ending angle of arc.  The arc is drawn counterclockwise from the
        starting angle, ANGLE1, to the ending angle, ANGLE2.

    Notes
    -----
    Defines annotation arcs to be written directly onto the display at a
    specified location.  This is a command generated by the Graphical User
    Interface (GUI) and will appear in the log file (Jobname.LOG) if
    annotation is used.  This command is not intended to be typed in
    directly in an ANSYS session (although it can be included in an input
    file for batch input or for use with the /INPUT command).

    All arcs are shown on subsequent displays unless the annotation is
    turned off or deleted.  Use the /LSPEC command to set the attributes of
    the arc.

    This command is valid in any processor.
    """
    command = "/LARC,%s,%s,%s,%s,%s" % (str(xcentr), str(ycentr), str(xlrad), str(angle1), str(angle2))
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



def wstart(self, node1="", node2="", ninc="", itime="", inc="", **kwargs):
    """APDL Command: WSTART

    Defines a starting wave list.

    Parameters
    ----------
    node1, node2, ninc
        Define a set of nodes in the starting wave list from NODE1 to NODE2
        (defaults to NODE1) in steps of NINC (defaults to 1).  If NODE1 =
        ALL, ignore remaining fields and use all selected nodes [NSEL].

    itime, inc
        Add more node sets to the same starting wave list by repeating the
        previous node set with NODE1 and NODE2 incremented by INC (defaults
        to 1) each time after the first.  ITIME is the total number of sets
        (defaults to 1) defined with this command.

    Notes
    -----
    Defines a starting wave list (optional) for reordering with the WAVES
    command.  Repeat WSTART command to define other starting wave lists (20
    maximum).

    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    command = "WSTART,%s,%s,%s,%s,%s" % (str(node1), str(node2), str(ninc), str(itime), str(inc))
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






def stargo(self, base="", **kwargs):
    """APDL Command: *GO

    Causes a specified line on the input file to be read next.

    Parameters
    ----------
    base
        "Go to" action:

        A user-defined label (beginning with a colon (:), 8 characters maximum).  The command reader will skip (and wrap to the beginning of the file, if necessary) to the first line that begins with the matching :label.   - Caution:   This label option may not be mixed with do-loop or if-then-else
                          constructs.

    Notes
    -----
    Causes the next read to be from a specified line on the input file.
    Lines may be skipped or reread.  The *GO command will not be executed
    unless it is part of a macro, user file (processed by *USE),  an
    alternate input file (processed by /INPUT), or unless it is used in a
    batch-mode input stream.  Jumping into, out of, or within a do-loop or
    an if-then-else construct to a :label line is not allowed.

    This command is valid in any processor.
    """
    command = "*GO,%s" % (str(base))
    return self.run(command, **kwargs)


def madapt(self, errtargt="", nadapt="", nmax="", kplt="", ksmooth="",
           klst="", kcd="", device="", **kwargs):
    """APDL Command: MADAPT

    Adaptively meshes and solves an edge-based model.

    Parameters
    ----------
    errtargt
        Target percentage for Zienkiewitz Zhu magnetic flux error (defaults
        to 5).

    nadapt
        Maximum number of adaptive steps (defaults to 5).

    nmax
        Maximum number of elements at which the iterations may continue
        (defaults to 50,000). Limits the number of elements that can be
        chosen for refinement.

    kplt
        Plotting options:

        0 - No plot (default)

        1 - Elements and H

        2 - BERR error estimates

        3 - BDSG, BEPC error estimates

        4 - Adaptive details

    ksmooth
        Smoothing options for refinement

        0 - No postprocessing will be done (default).

        1 - Smoothing will be done.  Node locations may change.

        2 - Smoothing and cleanup will be done.  Existing elements may be deleted, and node
            locations may change.

    klst
        Listing options

        0 - No printing (default)

        1 - Final report

        2 - Report at each iteration step

        3 - Report Zienkiewitz Zhu magnetic errors BERR and BSGD

        4 - Regular details

        5 - Full details

        6 - Refine details

        7 - Track

    kcd
        Allows you to issue a CDWRITE or CDREAD at every iteration.

        0 - Do not issue CDWRITE or CDREAD (default).

        1 - Issue CDWRITE at every iteration (to save every mesh variation). This option
            issues CDWRITE,geom, writing the information to jobnameN.cdb.

        2 - Issue CDREAD at every iteration (to read every mesh variation). Reads from an
            existing jobnameN.cdb.

    device
        Defines the output device for plotting.

        0 - Screen only (default)

        1 - JPEG frames. Each frame is written to a file (jobnameN.jpg by default). See
            /SHOW.

    Notes
    -----
    MADAPT invokes a predefined ANSYS macro for adaptive meshing and
    solution of edge-based magnetic analyses.  The macro causes repeated
    runs of the PREP7, SOLUTION, and POST1 phases of the ANSYS program with
    mesh density refinements based upon the percentage error in energy
    norm.

    The MADAPT command macro requires a second, user-defined macro, which
    must be named madaptld.mac and must reside in the same directory where
    ANSYS is being run. This madaptld macro must contain loads and boundary
    conditions, based on permanent geometry or solid model features (such
    as sides or vertices). Loads specified in the madaptld macro cannot be
    based on node numbers because the node numbers will change throughout
    the refinement process. This secondary macro is required because the
    MADAPT macro process must delete all loads and boundary conditions at
    every refinement step.

    MADAPT refines tetrahedral volume elements based on error. Hexahedra,
    wedges, and pyramids are not refined (see NREFINE).

    This command is also valid at the Begin level.

    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    command = "MADAPT,%s,%s,%s,%s,%s,%s,%s,%s" % (str(errtargt), str(nadapt), str(nmax), str(kplt), str(ksmooth), str(klst), str(kcd), str(device))
    return self.run(command, **kwargs)








def wmid(self, key="", **kwargs):
    """APDL Command: WMID

    Specifies reordering options for the WAVES command.

    Parameters
    ----------
    key
         Determines whether midside nodes are considered when reordering.

        NO - Do not consider midside nodes when reordering (default).

        YES - Consider midside nodes when reordering. This option
              is useful for models where line elements are only
              attached to midside nodes of solid elements.

    Notes
    -----
    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    command = "WMID,%s" % (str(key))
    return self.run(command, **kwargs)





def mstart(self, label="", key="", **kwargs):
    """APDL Command: /MSTART

    Controls the initial GUI components.

    Parameters
    ----------
    label
        Label identifying the GUI component:

        ZOOM - Pan, Zoom, Rotate dialog box, off by default.

        WORK - Offset Working Plane dialog box, off by default.

        WPSET - Working Plane Settings dialog box, off by default.

        ABBR - Edit Toolbar/Abbreviations dialog box, off by default.

        PARM - Scalar Parameters dialog box, off by default.

        SELE - Select Entities dialog box, off by default.

        ANNO - Annotation dialog box, off by default.

        HARD - Hard Copy dialog box, off by default.

        UTIL - Turns on the pre-ANSYS 6.1 (UIDL) GUI, off by default.

    key
        Switch value:

        OFF or 0 - Component does not appear when GUI is initialized.

        ON or 1 - Component appears when GUI is initialized.

    Notes
    -----
    Controls which components appear when the Graphical User Interface
    (GUI) is initially brought up.  This command is valid only before the
    GUI is brought up [/MENU,ON] and is intended to be used in the
    start162.ans file.  It only affects how the GUI is initialized; you can
    always bring up or close any component once you are in the GUI.

    This command is valid only at the Begin Level.
    """
    command = "/MSTART,%s,%s" % (str(label), str(key))
    return self.run(command, **kwargs)


def fs(self, node="", nev="", nlod="", stitm="", c1="", c2="", c3="",
       c4="", c5="", c6="", **kwargs):
    """APDL Command: FS

    Stores fatigue stress components at a node.

    Parameters
    ----------
    node
        Node number corresponding to this location.  Used only to associate
        a node with a new location or to find an existing location.

    nev
        Event number to be associated with these stresses (defaults to 1).

    nlod
        Loading number to be associated with these stresses (defaults to
        1).

    stitm
        Starting item number for entering stresses (defaults to 1).  If 1,
        data input in field C1 of this command is entered as the first item
        in the list; if 7, data input in field C1 of this command is
        entered as the seventh item in the list; etc.  Items are as
        follows:

        1-6 - SX, SY, SZ, SXY, SYZ, SXZ total stress components

        7 - Temperature

        8-13 - SX, SY, SZ, SXY, SYZ, SXZ membrane-plus-bending stress components.

        14 - Time

    c1, c2, c3, . . . , c6
        Stresses assigned to six locations starting with STITM.  If a value
        is already in one of these locations, it will be redefined.  A
        blank retains the previous value (except in the C1 field, which
        resets the STITM item to zero).

    Notes
    -----
    Stores fatigue stress components at a node as input on this command
    instead of from the current data in the database.  Stresses are stored
    according to the event number and loading number specified.  The
    location is associated with that previously defined for this node [FL]
    or else it is automatically defined.  May also be used to modify any
    previously stored stress components.  Stresses input with this command
    should be consistent with the global coordinate system for any FSNODE
    or FSSECT stresses used at the same location.
    """
    command = "FS,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(node), str(nev), str(nlod), str(stitm), str(c1), str(c2), str(c3), str(c4), str(c5), str(c6))
    return self.run(command, **kwargs)



def ftwrite(self, fname="", ext="", **kwargs):
    """APDL Command: FTWRITE

    Writes all currently stored fatigue data on a file.

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
    Data are written in terms of the equivalent POST1 fatigue commands
    [FTSIZE, FL, FS, etc.] which you can then edit and resubmit to POST1
    (with a /INPUT command).

    Once you have created a fatigue data file, each subsequent use of the
    FTWRITE command overwrites the contents of that file.
    """
    command = "FTWRITE,%s,%s" % (str(fname), str(ext))
    return self.run(command, **kwargs)

def fp(self, stitm="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
    """APDL Command: FP

    Defines the fatigue S vs. N and Sm vs. T tables.

    Parameters
    ----------
    stitm
        Starting item number for entering properties (defaults to 1).  If
        1, data input in field C1 of this command is entered as the first
        item in the list; if 7, data input in field C1 of this command is
        entered as the seventh item in the list; etc.  If the item number
        is negative, C1-C6 are ignored and the item is deleted.  If -ALL,
        the table is erased.  Items are as follows (items 41-62 are
        required only if simplified elastic-plastic code calculations are
        to be performed):

        1,2,...20 - N1, N2, ... N20

        21,22,...40 - S1, S2, ... S20

        41,42,...50 - T1, T2, ... T10

        51,52,...60 - Sm1, Sm2, ... Sm10

        61 - M (first elastic-plastic material parameter)

        62 - N (second elastic-plastic material parameter)

    c1, c2, c3, . . . , c6
        Data inserted into six locations starting with STITM.  If a value
        is already in one of these locations, it will be redefined.  A
        blank retains the previous value.

    Notes
    -----
    Defines the fatigue alternating stress (S) vs. cycles (N) table and the
    design stress-intensity value (Sm) vs. temperature (T) table.  May also
    be used to modify any previously stored property tables.  Log-log
    interpolation is used in the S vs. N table and linear interpolation is
    used in the Sm vs. T table.  Cycles and temperatures must be input in
    ascending order; S and Sm values in descending order.  Table values
    must be supplied in pairs, i.e., every N entry must have a
    corresponding S entry, etc.  Not all property pairs per curve need be
    used.  If no S vs. N table is defined, the fatigue evaluation will not
    produce usage factor results.  See the Structural Analysis Guide for
    details.
    """
    command = "FP,%s,%s,%s,%s,%s,%s,%s" % (str(stitm), str(c1), str(c2), str(c3), str(c4), str(c5), str(c6))
    return self.run(command, **kwargs)

def term(self, kywrd="", opt1="", opt2="", opt3="", **kwargs):
    """APDL Command: TERM

    Specifies various terminal driver options.

    Parameters
    ----------
    ncopy
        Activate hard copy device for NCOPY (0,1,2, etc.) copies.

    Notes
    -----
    Used only with terminal driver names on /SHOWDISP command.

    This command is also valid in PREP7.
    """
    command = "TERM,%s,%s,%s,%s" % (str(kywrd), str(opt1), str(opt2), str(opt3))
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







def fslist(self, nloc1="", nloc2="", ninc="", nev="", nlod="", **kwargs):
    """APDL Command: FSLIST

    Lists the stresses stored for fatigue evaluation.

    Parameters
    ----------
    nloc1, nloc2, ninc
        List stresses from NLOC1 (defaults to 1) to NLOC2 (defaults to
        NLOC1) in steps of NINC (defaults to 1).  If NLOC1 = ALL, NLOC2 and
        NINC are ignored and stresses for all locations are listed.

    nev
        Event number for stress listing (defaults to ALL).

    nlod
        Loading number for stress listing (defaults to ALL).

    Notes
    -----
    Stresses may be listed per location, per event, per loading, or per
    stress condition.  Use FELIST and FLLIST if only event and location
    parameters (no stresses) are to be listed.
    """
    command = "FSLIST,%s,%s,%s,%s,%s" % (str(nloc1), str(nloc2), str(ninc), str(nev), str(nlod))
    return self.run(command, **kwargs)

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





def fplist(self, **kwargs):
    """APDL Command: FPLIST

    Lists the property table stored for fatigue evaluation.
    """
    command = "FPLIST,"
    return self.run(command, **kwargs)



def uis(self, label="", value="", **kwargs):
    """APDL Command: /UIS

    Controls the GUI behavior.

    Parameters
    ----------
    label
        Behavior control key:

        BORD - Controls the functionality of the mouse buttons for dynamic viewing mode only.
               When Label = BORD, the three values that follow control the
               functionality of the LEFT, MIDDLE and RIGHT buttons,
               respectively (see below).

        MSGPOP - Controls which messages from the ANSYS error message subroutine are displayed
                 in a message dialog box.

        REPLOT - Controls whether or not an automatic replot occurs after functions affecting
                 the model are executed.

        ABORT - Controls whether or not ANSYS displays dialog boxes to show the status of an
                operation in progress and to cancel that operation.

        DYNA - Controls whether the dynamic mode preview is a bounding box or the edge outline
               of the model.  This label only applies to 2-D display
               devices (i.e., /SHOW,XII or /SHOW,WIN32).  This "model edge
               outline" mode is only supported in PowerGraphics
               [/GRAPHICS,POWER] and is intended for element, line,
               results, area, or volume displays.

        PICK - Controls how graphical entities are highlighted from within the ANSYS Select
               menu.

        POWER - Controls whether or not PowerGraphics is active when the GUI is initiated. The
                ANSYS program default status is PowerGraphics "ON";  this
                command is used (placed in the start.ans file) when full
                graphics is desired on start up.

        DPRO - Controls whether or not the ANSYS input window displays a dynamic prompt. The
               dynamic prompt shows the correct command syntax for the
               command, as you are entering it.

        UNDO - Controls whether or not the session editor includes nonessential commands or
               comments in the file it creates. You can use this option to
               include comments and other materials in the session editor
               file.

        LEGE - Controls whether or not the multi-legend is activated when you start the GUI.
               The multi-legend enables you to specify the location of your
               legend items in each of the five graphics windows. You can
               place this option in your start.ans file and have the GUI
               start with the legend items in a pre-specified location.

        PBAK - Controls whether or not the background shading is activated when you start the
               GUI. You can place this option in your start.ans file.

        ZPIC - Controls the sorting order for entities that are coincident (directly in front
               of or behind each other) to a picked spot on your model.
               When you pick a spot on your model that could indicate two
               or more entities, a message warns you of this condition, and
               a list of the coincident entities can be generated. The
               VALUE term (below) will determine the sort order.

        HPOP - Controls the prioritization of your GUI windows when the contents are ported to
               a plot or print file (/UI,COPY,SAVE). OpenGL (3D) graphics
               devices require that the ANSYS Graphics Screen contents be
               set in front of all overlying windows in order to port them
               to a printer or a file. This operation can sometimes
               conflict with /NOERASE settings. See the VALUE term (below)
               to determine the available control options.

    value
        Values controlling behavior if Label = BORD:

        1 - PAN, controls dynamic translations.

        2 - ZOOM, controls zoom, and dynamic rotation about the view vector.

        3 - ROTATE, controls dynamic rotation about the screen X and Y axes.
    """
    command = "/UIS,%s,%s" % (str(label), str(value))
    return self.run(command, **kwargs)

def spower(self, inletport="", outletport="", **kwargs):
    """APDL Command: SPOWER

    Calculates sound power parameters.

    Parameters
    ----------
    inletport
        Inlet source port number.

    outletport
        Outlet port number.

    Notes
    -----
    The SPOWER command calculates the input sound power level, reflected
    sound power level, return loss, and absorption coefficient for an inlet
    port.

    If a matched outlet port is defined, the command also calculates the
    transmission loss.

    The sound power parameters are output to the file
    jobname%ARG1%%ARG2%.anp (where n = 1 or 2).

    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    command = "SPOWER,%s,%s" % (str(inletport), str(outletport))
    return self.run(command, **kwargs)





def segen(self, mode="", nsuper="", mdof="", stopstage="", **kwargs):
    """APDL Command: SEGEN

    Automatically generate superelements.

    Parameters
    ----------
    mode
        Specify action to take (must be specified as one of the following):

        AUTO - Turn on feature.

        OFF - Turn off feature.

    nsuper
        Number of superelements to create. The minimum number of
        superelements is 2, and the maximum number of superelements is 999.
        Note that the number of requested superelements may not be the same
        as the number of defined superelements (see "Notes" for more
        details).

    mdof
        Specifies whether to use the master DOF defined by the user.

        YES - Use master DOF defined by the user with the M command.

        NO - Use the master DOF defined by the automatic generation process. Be aware that
             this option can generate a large number of master DOFs (see
             "Notes"  for more details).

    stopstage
        Specifies when to stop the automatic superelement generation
        process.

        PREVIEW - Preview the superelements only; stop after creating the domains which will
                  become the superelements, and after creating master DOF
                  on the interfaces between each domain.

        GEN - Create (generate) the superelements.

    Notes
    -----
    This command can be used to quickly generate a set of superelements.
    Each superelement is created in a separate file (jobnameXXX.sub, where
    XXX is a positive number from 1 to 999).

    Due to the heuristics in the automatic domain decomposer, which is used
    to define the domains that will become superelements, the number of
    defined superelements may exceed the number of requested superelements.
    Use the mDof and stopStage options to determine exactly how many
    superelements will be created, the interfaces between each
    superelement, and where master DOF will be defined. With the
    /PNUM,DOMAIN command, you can graphically (visually) preview the
    elements in each superelement.  Then, if required, you can add
    additional master DOF to (or remove from) the boundaries of the
    superelements. Use the SEGEN command again with stopStage = GEN to
    actually create the superelements.

    ANSYS automatically defines master DOF at each of the following: all
    interface DOF between superelements, all DOF attached to contact
    elements (TARGE169 to CONTA177), and all DOF associated with nodes
    having a point load defined.  Note that for regular superelements, all
    interface DOFs must be defined as master DOFs for the correct solution
    to be obtained. However, for CMS superelements, some of the interface
    DOFs can be removed without a significant loss of accuracy.

    For the case when mDof = YES, you should select the preview option
    first (stopStage = PREVIEW) to verify exactly how many superelements
    will be created and where the superelement boundaries are located.  If
    more superelements will be created than were requested, you should
    define master DOF on the interface(s) between all superelements.

    This command is valid only for substructuring analyses (ANTYPE,SUBSTR).
    Use SEOPT to specify any options for all of the superelements (e.g.,
    which matrices to reduce), and possibly CMSOPT for any CMS
    substructuring analysis.  Note that the created superelements will
    follow the current /FILNAME instead of SENAME from SEOPT.  Also, only
    one load vector will be written to each .SUB file.  Multiple load steps
    are not supported with the automatic superelement generation process.

    During the actual creation of the superelements, the output is
    redirected to jobname.autoTemp.

    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    command = "SEGEN,%s,%s,%s,%s" % (str(mode), str(nsuper), str(mdof), str(stopstage))
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



def ftsize(self, mxloc="", mxev="", mxlod="", **kwargs):
    """APDL Command: FTSIZE

    Defines the fatigue data storage array.

    Parameters
    ----------
    mxloc
        Maximum number of fatigue locations (defaults to 5).

    mxev
        Maximum number of fatigue events (defaults to 10).

    mxlod
        Maximum number of loadings in each event (defaults to 3).

    Notes
    -----
    Defines the size and erases the stress conditions for the fatigue data
    storage array.  A stress condition is a loading (stresses) at a
    particular location (node) for a particular event.  Size is defined in
    terms of the maximum number of locations, events, and loadings.  The
    array size cannot be changed once data storage has begun (without
    erasing all previously stored data).  If a size change is necessary,
    see the FTWRITE command.
    """
    command = "FTSIZE,%s,%s,%s" % (str(mxloc), str(mxev), str(mxlod))
    return self.run(command, **kwargs)


def menu(self, key="", **kwargs):
    """APDL Command: /MENU

    Activates the Graphical User Interface (GUI).

    Parameters
    ----------
    key
        Activation key:

        ON - Activates the menu system (device dependent).

        GRPH - Enters non-GUI graphics mode.

    Notes
    -----
    Activates the Graphical User Interface (GUI).

    This command is valid in any processor.
    """
    command = "/MENU,%s" % (str(key))
    return self.run(command, **kwargs)


def slashtype(self, wn="", type_="", **kwargs):
    """APDL Command: /TYPE

    Defines the type of display.

    Parameters
    ----------
    wn
        Window number (or ALL) to which command applies (defaults to 1).

    type\_
        Display type.  Defaults to ZBUF for raster mode displays or BASIC
        for vector mode displays:

        BASIC or 0 - Basic display (no hidden or section operations).

        SECT or 1 - Section display (plane view).  Use the /CPLANE command to define the cutting
                    plane.

        HIDC or 2 - Centroid hidden display (based on item centroid sort).

        HIDD or 3 - Face hidden display (based on face centroid sort).

        HIDP or 4 - Precise hidden display (like HIDD but with more precise checking). Because all
                    facets are sorted, this mode can be extremely slow,
                    especially for large models.

        CAP or 5 - Capped hidden display (same as combined SECT and HIDD with model in front of
                   section plane removed).

        ZBUF or 6 - Z-buffered display (like HIDD but using software Z-buffering).

        ZCAP or 7 - Capped Z-buffered display (same as combined SECT and ZBUF with model in front
                    of section plane removed).

        ZQSL or 8 - QSLICE Z-buffered display (same as SECT but the edge lines of the remaining 3-D
                    model are shown).

        HQSL or 9 - QSLICE precise hidden display (like ZQSL but using precise hidden).

    Notes
    -----
    Defines the type of display, such as section display or hidden-line
    display.  Use the /DEVICE command to specify either raster or vector
    mode.

    The SECT, CAP, ZCAP, ZQSL, and HQSL options produce section displays.
    The section or "cutting" plane is specified on the /CPLANE command as
    either normal to the viewing vector at the focus point (default), or as
    the working plane.

    When you use PowerGraphics, the section display options (Section,
    Slice, and Capped) use different averaging techniques for the interior
    and exterior results. Because of the different averaging schemes,
    anomalies may appear at the transition areas. In many cases, the
    automatically computed MIN and MAX values will differ from the full
    range of interior values. You can lessen the effect of these anomalies
    by issuing AVRES,,FULL (Main Menu> General Post Proc> Options for
    Outp). This command sets your legend's automatic contour interval range
    according to the minimum and maximum results found throughout the
    entire model.

    With PowerGraphics active (/GRAPHICS,POWER), the averaging scheme for
    surface data with interior element data included (AVRES,,FULL) and
    multiple facets per edge (/EFACET,2 or /EFACET,4) will yield differing
    minimum and maximum contour values depending on the  Z-Buffering
    options (/TYPE,,6 or /TYPE,,7).  When the Section data is not included
    in the averaging schemes (/TYPE,,7), the resulting absolute value for
    the midside node is significantly smaller.

    The HIDC, HIDD, HIDP, ZBUF, ZQSL, and HQSL options produce displays
    with "hidden" lines removed.  Hidden lines are lines obscured from view
    by another element, area, etc.  The choice of non-Z-buffered hidden-
    line procedure types is available only for raster mode [/DEVICE]
    displays.  For vector mode displays, all non-Z-buffered "hidden-line"
    options use the same procedure (which is slightly different from the
    raster procedures).  Both geometry and postprocessing displays may be
    of the hidden-line type.  Interior stress contour lines within solid
    elements can also be removed as hidden lines, leaving only the stress
    contour lines and element outlines on the visible surfaces.  Midside
    nodes of elements are ignored on postprocessing displays.  Overlapping
    elements will not be displayed.

    The ZBUF, ZCAP, and ZQSL options use a specific hidden-line technique
    called software Z-buffering.  This technique allows a more accurate
    display of overlapping surfaces (common when using Boolean operations
    or /ESHAPE on element displays), and allows smooth shaded displays on
    all interactive graphics displays.  Z-buffered displays can be
    performed faster than HIDP and CAP type displays for large models.  See
    also the /LIGHT, /SHADE, and /GFILE commands for additional options
    when Z-buffering is used.

    This command is valid in any processor.
    """
    command = "/TYPE,%s,%s" % (str(wn), str(type_))
    return self.run(command, **kwargs)


def fl(self, nloc="", node="", scfx="", scfy="", scfz="", title="",
       **kwargs):
    """APDL Command: FL

    Defines a set of fatigue location parameters.

    Parameters
    ----------
    nloc
        Reference number for this location (within MXLOC).  When defining a
        new location, defaults to lowest unused location.  If the specified
        NODE is already associated with a location, NLOC defaults to that
        existing location.

    node
        Node number corresponding to this location (must be unique).  Used
        only to associate a node with a new location or to find an existing
        location (if NLOC is not input).  If NODE = -1 (or redefined),
        erase all parameters and fatigue stresses for this location.

    scfx, scfy, scfz
        Stress concentration factors applied to the total stresses.
        Factors are applied in the global X, Y, and Z directions unless the
        axisymmetric option of the FSSECT is used (i.e., RHO is nonzero),
        in which case the factors are applied in the section x, y, and z
        (radial, axial, and hoop) directions.

    title
        User-defined title for this location (up to 20 characters).

    Notes
    -----
    Repeat FL command to define additional sets of location parameters
    (MXLOC limit), to redefine location parameters, or to delete location
    stress conditions.

    One location must be defined for each node of interest and only one
    node can be associated with each location.  See the FTSIZE command for
    the maximum locations (MXLOC) allowed.  A location will be
    automatically defined for a node not having a location when the FSSECT,
    FSNODE, or FS command is issued.  Automatically defined locations are
    assigned the lowest available location number, unity stress
    concentration factors, and no title.
    """
    command = "FL,%s,%s,%s,%s,%s,%s" % (str(nloc), str(node), str(scfx), str(scfy), str(scfz), str(title))
    return self.run(command, **kwargs)


def fllist(self, nloc1="", nloc2="", ninc="", **kwargs):
    """APDL Command: FLLIST

    Lists the fatigue location parameters.

    Parameters
    ----------
    nloc1, nloc2, ninc
        List location parameters from NLOC1 (defaults to 1) to NLOC2
        (defaults to NLOC1) in steps of NINC (defaults to 1).  If NLOC1 =
        ALL, NLOC2 and NINC are ignored and all locations are listed.
    """
    command = "FLLIST,%s,%s,%s" % (str(nloc1), str(nloc2), str(ninc))
    return self.run(command, **kwargs)
