"""
These PREP7 commands are used to define the linear material properties.
"""


class Materials:
    def emunit(self, lab="", value="", **kwargs):
        """APDL Command: EMUNIT

        Specifies the system of units for magnetic field problems.

        Parameters
        ----------
        lab
            Label specifying the type of units:

            MKS - Rationalized MKS system of units (meters, amperes,
                  henries, webers, etc.).  Free-space permeability is
                  set to 4 πe-7 henries/meter. Free- space
                  permittivity is set to 8.85 e-12 F/m.

            MUZRO - User defined system of units. Free-space
                    permeability is set to the value input for
                    VALUE. Other units must correspond to the
                    permeability units. Relative permeability may be
                    altered to absolute values.

            EPZRO - User defined system of units. Free-space
                    permittivity is set to the value input for
                    VALUE. Other units must correspond to the
                    permittivity units.

        value
            User value of free-space permeability (defaults to 1) if Lab =
            MUZRO, or free-space permittivity (defaults to 1) if Lab = EPZRO.

        Notes
        -----
        Specifies the system of units to be used for electric and magnetic
        field problems. The free-space permeability and permittivity values may
        be set as desired. These values are used with the relative property
        values [MP] to establish absolute property values.

        Note:: : If the magnetic source field strength (Hs) has already been
        calculated [BIOT], switching EMUNIT will not change the values.

        For micro-electromechanical systems (MEMS), where dimensions are on the
        order of microns, see the conversion factors in System of Units in the
        Coupled-Field Analysis Guide.

        This command is also valid in SOLUTION.
        """
        command = "EMUNIT,%s,%s" % (str(lab), str(value))
        return self.run(command, **kwargs)

    def mp(self, lab="", mat="", c0="", c1="", c2="", c3="", c4="", **kwargs):
        """APDL Command: MP

        Defines a linear material property as a constant or a function of
        temperature.

        Parameters
        ----------
        lab
            Valid material property label.  Applicable labels are listed under
            "Material Properties" in the input table for each element type in
            the Element Reference.  See Linear Material Properties in the
            Material Reference for more complete property label definitions:

            ALPD
                Mass matrix multiplier for damping.

            ALPX
                Secant coefficients of thermal expansion (also ``ALPY``, ``ALPZ``).

            BETD
                Stiffness matrix multiplier for damping.

                .. note:: If used in an explicit dynamic analysis, the value corresponds to the percentage of damping in the high
                   frequency domain. For example, 0.1 roughly corresponds to 10% damping in the high frequency domain.

            BETX
                Coefficient of diffusion expansion (also ``BETY``, ``BETZ``)

            BVIS
                Bulk viscosity

            C
                Specific heat

            CREF
                Reference concentration (may not be temperature dependent)

            CSAT
                Saturated concentration

            CTEX
                Instantaneous coefficients of thermal expansion (also ``CTEY``, ``CTEZ``)

            CVH
                Heat coefficient at constant volume per unit of mass

            DENS
                Mass density.

            DMPR
                Constant structural damping coefficient in full harmonic analysis or damping ratio in mode-superposition
                analysis.

            DXX
                Diffusivity coefficients (also ``DYY``, ``DZZ``)

            EMIS
                Emissivity.

            ENTH
                Enthalpy.

            EX
                Elastic moduli (also ``EY``, ``EZ``)

            GXY
                Shear moduli (also ``GYZ``, ``GXZ``)

            HF
                Convection or film coefficient

            KXX
                Thermal conductivities (also ``KYY``, ``KZZ``)

            LSST
                Electric loss tangent

            LSSM
                Magnetic loss tangent

            MGXX
                Magnetic coercive forces (also ``MGYY``, ``MGZZ``)

            MURX
                Magnetic relative permeabilities (also ``MURY``, ``MURZ``)

            MU
                Coefficient of friction

            NUXY
                Minor Poisson's ratios (also ``NUYZ``, ``NUXZ``) (``NUXY`` = νyx, as described in Stress-Strain Relationships in the
                Mechanical APDL Theory Reference)

            PERX
                Electric relative permittivities (also ``PERY``, ``PERZ``)

                .. note::  If you enter permittivity values less than 1 for ``SOLID5``, ``PLANE13``, or ``SOLID98``, the program interprets
                   the values as absolute permittivity. Values input for ``PLANE223``, ``SOLID226``, or ``SOLID227`` are always interpreted as
                   relative permittivity.

            PRXY
                Major Poisson's ratios (also ``PRYZ``, ``PRXZ``) (``PRXY`` = νxy, as described in Stress-
                Strain Relationships in the Mechanical APDL Theory
                Reference)

            QRATE
                Heat generation rate for thermal mass element MASS71. Fraction of plastic work
                converted to heat (Taylor-Quinney coefficient) for coupled-
                field elements ``PLANE223``, ``SOLID226``, and ``SOLID227``.

            REFT
                Reference temperature.  Must be defined as a constant; ``C1`` through ``C4`` are
                ignored.

            RH
                Hall Coefficient.

            RSVX
                Electrical resistivities (also ``RSVY``, ``RSVZ``).

            SBKX
                Seebeck coefficients (also ``SBKY``, ``SBKZ``).

            SONC
                Sonic velocity.

            THSX
                Thermal strain (also ``THSY``, ``THSZ``).

            VISC
                Viscosity.

        mat
            Material reference number to be associated with the elements
            (defaults to the current MAT setting [MAT]).

        c0
            Material property value, or if a property-versus-temperature
            polynomial is being defined, the constant term in the polynomial.
            ``C0`` can also be a table name (``%tabname%``); if ``C0`` is a table name, ``C1``
            through ``C4`` are ignored.

        c1, c2, c3, c4
            Coefficients of the linear, quadratic, cubic, and quartic terms,
            respectively, in the property-versus-temperature polynomial.  Leave
            blank (or set to zero) for a constant material property.

        Notes
        -----
        MP defines a linear material property as a constant or in terms of a
        fourth order polynomial as a function of temperature. (See the TB
        command for nonlinear material property input.) Linear material
        properties typically require a single substep for solution, whereas
        nonlinear material properties require multiple substeps;  see Linear
        Material Properties in the Material Reference for details.

        If the constants ``C1`` - ``C4`` are input, the polynomial

        .. math::

           Property = C_0 + C_1(T) + C_2(T)^2 + C_3(T)^3 + C_4(T)^4

        is evaluated at discrete temperature points with linear interpolation
        between points (that is, a piecewise linear representation) and a
        constant-valued extrapolation beyond the extreme points. First-order
        properties use two discrete points (±9999°).
        The :meth:`MPTEMP <ansys.mapdl.core.Mapdl.mptemp>` or
        :meth:`MPTGEN <ansys.mapdl.core.Mapdl.mptgen>`
        commands must be used for second and higher order properties to define
        appropriate temperature steps. To ensure that the number of
        temperatures defined via the :meth:`MPTEMP <ansys.mapdl.core.Mapdl.mptemp>`
        and :meth:`MPTGEN <ansys.mapdl.core.Mapdl.mptgen>` commands is minimally
        sufficient for a reasonable representation of the curve, ANSYS
        generates an error message if the number is less than ``N``, and a warning
        message if the number is less than ``2N``. The value ``N`` represents the
        highest coefficient used; for example, if ``C3`` is nonzero and ``C4`` is zero,
        a cubic curve is being used which is defined using 4 coefficients so
        that ``N`` = 4.
        """
        command = "MP,%s,%s,%s,%s,%s,%s,%s" % (
            str(lab),
            str(mat),
            str(c0),
            str(c1),
            str(c2),
            str(c3),
            str(c4),
        )
        return self.run(command, **kwargs)

    def mpamod(self, mat="", deftemp="", **kwargs):
        """APDL Command: MPAMOD

        Modifies temperature-dependent secant coefficients of thermal
        expansion.

        Parameters
        ----------
        mat
            Material number for which the secant coefficients of thermal
            expansion (SCTE's) are to be modified.  Defaults to 1.

        deftemp
            Definition temperature at which the existing SCTE-versus-
            temperature tables were defined.  Defaults to zero.

        Notes
        -----
        This command converts temperature-dependent SCTE data (properties ALPX,
        ALPY, ALPZ)  from the definition temperature (DEFTEMP) to the reference
        temperature defined by MP,REFT or TREF.  If both the MP,REFT and TREF
        commands have been issued, the reference temperature defined by the
        MP,REFT command will be used.

        This command does not apply to the instantaneous coefficients of
        thermal expansion (properties CTEX, CTEY, CTEZ) or to the thermal
        strains (properties THSX, THSY, THSZ).

        See Linear Material Properties in the Mechanical APDL Material
        Reference and the Mechanical APDL Theory Reference for more details.

        This command is also valid in SOLUTION.
        """
        command = "MPAMOD,%s,%s" % (str(mat), str(deftemp))
        return self.run(command, **kwargs)

    def mpchg(self, mat="", elem="", **kwargs):
        """APDL Command: MPCHG

        Changes the material number attribute of an element.

        Parameters
        ----------
        mat
            Assign this material number to the element.  Material numbers are
            defined with the material property commands [MP].

        elem
            Element for material change.  If ALL, change materials for all
            selected elements [ESEL].

        Notes
        -----
        Changes the material number of the specified element.  Between load
        steps in SOLUTION, material properties cannot be changed from linear to
        nonlinear, or from one nonlinear option to another.

        If you change from one MKIN model to another MKIN model, the different
        MKIN models need to have the same number of data points. This
        requirement also applies if you change from one KINH model to another
        KINH model, or from one CHABOCHE model to another CHABOCHE model.
        """
        command = "MPCHG,%s,%s" % (str(mat), str(elem))
        return self.run(command, **kwargs)

    def mpcopy(self, matf="", matt="", **kwargs):
        """APDL Command: MPCOPY

        Copies linear material model data from one material reference number to
        another.

        Parameters
        ----------
        matf
            Material reference number from where material property data will be
            copied.

        matt
            Material reference number to where material property data will be
            copied.

        Notes
        -----
        The MPCOPY command copies linear material properties only, which are
        all properties defined through the MP command. If you copy a model that
        includes both linear and yield behavior constants (for example, a BKIN
        model), the MPCOPY and TBCOPY, ALL commands are used together to copy
        the entire model.  All input data associated with the model is copied,
        that is, all data defined through the MP and TB commands.

        Also, if you copy a material model using the Material Model Interface
        (Edit> Copy), both the commands MPCOPY and TBCOPY, ALL are issued,
        regardless of whether the model includes linear constants only, or if
        it includes a combination of linear and yield behavior constants.

        This command is also valid in SOLUTION.
        """
        command = "MPCOPY,,%s,%s" % (str(matf), str(matt))
        return self.run(command, **kwargs)

    def mpdata(
        self,
        lab="",
        mat="",
        sloc="",
        c1="",
        c2="",
        c3="",
        c4="",
        c5="",
        c6="",
        **kwargs,
    ):
        """APDL Command: MPDATA

        Defines property data to be associated with the temperature table.

        Parameters
        ----------
        lab
            Valid property label.  Applicable labels are listed under "Material
            Properties" in the input table for each element type in the Element
            Reference.  See Linear Material Properties in the Mechanical APDL
            Material Reference for more complete property label definitions:

            ALPD - Mass matrix multiplier for damping.

            ALPX - Secant coefficients of thermal expansion (also ALPY, ALPZ).  (See also MPAMOD
                   command for adjustment to reference temperature).

            BETD - Stiffness matrix multiplier for damping.

            BETX - Coefficient of diffusion expansion (also BETY, BETZ)

            C - Specific heat.

            CREF - Reference concentration (may not be temperature dependent)

            CSAT - Saturated concentration

            CTEX - Instantaneous coefficients of thermal expansion (also CTEY, CTEZ).

            DENS - Mass density.

            DMPR - Constant material damping coefficient.

            DXX - Diffusivity coefficients (also DYY, DZZ)

            EMIS - Emissivity.

            ENTH - Enthalpy.

            EX - Elastic moduli (also EY, EZ).

            GXY - Shear moduli (also GYZ, GXZ).

            HF - Convection or film coefficient.

            KXX - Thermal conductivities (also KYY, KZZ).

            LSST - Dielectric loss tangent.

            MGXX - Magnetic coercive forces (also MGYY, MGZZ).

            MU - Coefficient of friction.

            MURX - Magnetic relative permeabilities (also MURY, MURZ).

            NUXY - Minor Poisson's ratios (also NUYZ, NUXZ).

            PERX - Electric relative permittivities (also PERY, PERZ).

            PRXY - Major Poisson's ratios (also PRYZ, PRXZ).

            QRATE - Heat generation rate.

            REFT - Reference temperature (may not be temperature dependent).

            RH - Hall Coefficient.

            RSVX - Electrical resistivities (also RSVY, RSVZ).

            SBKX - Seebeck coefficients (also SBKY, SBKZ).

            SONC - Sonic velocity.

            THSX - Thermal strain (also THSY, THSZ).

            VISC - Viscosity.

        mat
            Material reference number to be associated with the elements
            (defaults to 1 if you specify zero or no material number).

        sloc
            Starting location in table for generating data.  For example, if
            SLOC = 1, data input in the C1 field is the first constant in the
            table.  If SLOC = 7, data input in the C1 field is the seventh
            constant in the table, etc.  Defaults to the last location filled +
            1.

        c1, c2, c3, . . . , c6
            Property data values assigned to six locations starting with SLOC.
            If a value is already in this location, it is redefined.  A blank
            (or zero) value for C1 resets the previous value in SLOC to zero.
            A value of zero can only be assigned by C1.  Blank (or zero) values
            for C2 to C6 leave the corresponding previous values unchanged.

        Notes
        -----
        Defines a table of property data to be associated with the temperature
        table.  Repeat MPDATA command for additional values (100 maximum).
        Temperatures must be defined first [MPTEMP].  Also stores assembled
        property function table (temperature and data) in virtual space.

        This command is also valid in SOLUTION.

        Without Emag enabled, the ``MURx`` and ``MGxx`` properties are
        not allowed.  In ANSYS Professional, all structural and
        thermal properties are allowed except ALPD, BETD, and MU.  In
        ANSYS Emag, only the ``RSVx``, ``PERx``, ``MURx``, and ``MGxx``
        properties are allowed. Only products that include ANSYS Emag
        can use the LSST property. The ``SBKx`` property is only available
        in ANSYS Multiphysics and ANSYS PrepPost.
        """
        command = "MPDATA,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(lab),
            str(mat),
            str(sloc),
            str(c1),
            str(c2),
            str(c3),
            str(c4),
            str(c5),
            str(c6),
        )
        return self.run(command, **kwargs)

    def mpdele(self, lab="", mat1="", mat2="", inc="", lchk="", **kwargs):
        """APDL Command: MPDELE

        Deletes linear material properties.

        Parameters
        ----------
        lab
            Material property label (see MP command for valid labels).  If ALL,
            delete properties for all applicable labels.

        mat1, mat2, inc
            Delete materials from MAT1 to MAT2 (defaults to MAT1) in steps of
            INC (defaults to 1).  If MAT1 = ALL, MAT2 and INC are ignored and
            the properties for all materials are deleted.

        lchk
            Specifies the level of element-associativity checking:

            NOCHECK - No element-associativity check occurs. This option is the default.

            WARN - When a section, material, or real constant is associated with an element, ANSYS
                   issues a message warning that the necessary entity has been
                   deleted.

            CHECK - The command terminates, and no section, material, or real constant is deleted
                    if it is associated with an element.

        Notes
        -----
        This command is also valid in SOLUTION.

        The LCHK argument is valid only when Lab = ALL.
        """
        command = "MPDELE,%s,%s,%s,%s,%s" % (
            str(lab),
            str(mat1),
            str(mat2),
            str(inc),
            str(lchk),
        )
        return self.run(command, **kwargs)

    def mpdres(self, labf="", matf="", labt="", matt="", **kwargs):
        """APDL Command: MPDRES

        Reassembles existing material data with the temperature table.

        Parameters
        ----------
        labf
            Material property label associated with MATF.

        matf
            Material reference number of property to restore from virtual
            space.

        labt
            Material property label associated with MATT (defaults to label
            associated with MATF).

        matt
            Material reference number assigned to generated property (defaults
            to MATF).

        Notes
        -----
        Restores into the database (from virtual space) a data table previously
        defined [MP] for a particular property, assembles data with current
        database temperature table, and stores back in virtual space as a new
        property.

        This command is also valid in SOLUTION.
        """
        command = "MPDRES,%s,%s,%s,%s" % (
            str(labf),
            str(matf),
            str(labt),
            str(matt),
        )
        return self.run(command, **kwargs)

    def mplib(self, r_w_opt="", path="", **kwargs):
        """APDL Command: /MPLIB

        Sets the default material library read and write paths.

        Parameters
        ----------
        r-w_opt
            Determines what path is being set.  Possible values are:

            READ - Set the read path.

            WRITE - Set the write path.

            STAT - Report what read and write paths are currently in use.

        path
            The directory path to be used for material library files.

        Notes
        -----
        The /MPLIB command sets two path strings used in conjunction with the
        material library feature and the MPREAD and MPWRITE commands.

        For MPREAD, when you use the LIB option and no directory path is given
        in the file name, the command searches for the file in these locations:
        the current working directory, the user's home directory, the user-
        specified material library directory (as defined by the
        /MPLIB,READ,PATH command), and /ansys_dir/matlib.

        For MPWRITE, when you use the LIB option and the directory portion of
        the specification for the material library file is blank, the command
        writes the material  library file to the directory specified by the
        /MPLIB,WRITE,PATH command (if that path has been set).  If the path has
        not been set, the default is to write the file to the current working
        directory.

        The Material Library files supplied with the distribution disks are
        meant for demonstration purposes only.  These files are not intended
        for use in customer applications.
        """
        command = "/MPLIB,%s,%s" % (str(r_w_opt), str(path))
        return self.run(command, **kwargs)

    def mplist(self, mat1="", mat2="", inc="", lab="", tevl="", **kwargs):
        """APDL Command: MPLIST

        Lists linear material properties.

        Parameters
        ----------
        mat1, mat2, inc
            List materials from MAT1 to MAT2 (defaults to MAT1) in steps of INC
            (defaults to 1).  If MAT1= ALL (default), MAT2 and INC are ignored
            and properties for all material numbers are listed.

        lab
            Material property label (see the MP command for labels).  If ALL
            (or blank), list properties for all labels.  If EVLT, list
            properties for all labels evaluated at TEVL.

        tevl
            Evaluation temperature for Lab = EVLT listing (defaults to BFUNIF).

        Notes
        -----
        For Lab = EVLT, when the property is from tables, the MPPLOT command
        will not be valid because the property could be a function of more than
        temperature.

        This command is valid in any processor.
        """
        command = "MPLIST,%s,%s,%s,%s,%s" % (
            str(mat1),
            str(mat2),
            str(inc),
            str(lab),
            str(tevl),
        )
        return self.run(command, **kwargs)

    def mpplot(self, lab="", mat="", tmin="", tmax="", pmin="", pmax="", **kwargs):
        """APDL Command: MPPLOT

        Plots linear material properties as a function of temperature.

        Parameters
        ----------
        lab
            Linear material property label (EX, EY, etc.) [MP].

        mat
            Material reference number. Defaults to 1.

        tmin
            Minimum abscissa value to be displayed.

        tmax
            Maximum abscissa value.

        pmin
            Minimum property (ordinate) value to be displayed.

        pmax
            Maximum property value.

        Notes
        -----
        When the property is from tables, the MPPLOT command will not be valid
        because the property could be a function of more than temperature.

        This command is valid in any processor.
        """
        command = "MPPLOT,%s,%s,%s,%s,%s,%s" % (
            str(lab),
            str(mat),
            str(tmin),
            str(tmax),
            str(pmin),
            str(pmax),
        )
        return self.run(command, **kwargs)

    def mpread(self, fname="", ext="", lib="", **kwargs):
        """APDL Command: MPREAD

        Reads a file containing material properties.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including directory). If you do not specify the ``LIB``
            option, the default directory is the current working
            directory. If you specify the ``LIB`` option, the default is
            the following search path: the current working directory,
            the user's home directory, ``MPLIB_DIR`` (as specified by the
            ``/MPLIB,READ,PATH`` command) and ``/ansys_dir/matlib`` (as
            defined by installation). If you use the default for your
            directory, you can use all 248 characters for the file
            name.

        ext
            Filename extension (eight-character maximum).

        lib
            Reads material library files previously written with the
            MPWRITE command.  (See the description of the ``LIB`` option
            for the ``MPWRITE`` command.)  The only allowed value for ``LIB``
            is ``LIB``.

        Notes
        -----
        Material properties written to a file without the ``LIB`` option
        do not support nonlinear properties.  Also, properties written
        to a file without the ``LIB`` option are restored in the same
        material number as originally defined.  To avoid errors, use
        ``MPREAD`` with the ``LIB`` option only when reading files written
        using MPWRITE with the ``LIB`` option.

        If you omit the ``LIB`` option for ``MPREAD``, this command supports
        only linear properties.

        Material numbers are hardcoded.  If you write a material file
        without specifying the ``LIB`` option, then read that file in
        using the ``MPREAD`` command with the ``LIB`` option, the ANSYS
        program will not write the file to a new material number.
        Instead, it will write the file to the "old" material number
        (the number specified on the MPWRITE command that created the
        file.)

        This command is also valid in SOLUTION.
        """
        return self.run(f"MPREAD,{fname},{ext},,{lib}", **kwargs)

    def mptemp(self, sloc="", t1="", t2="", t3="", t4="", t5="", t6="", **kwargs):
        """APDL Command: MPTEMP

        Defines a temperature table for material properties.

        Parameters
        ----------
        sloc
            Starting location in table for entering temperatures.  For example,
            if SLOC = 1, data input in the T1 field applies to the first
            constant in the table.  If SLOC = 7, data input in the T1 field
            applies to the seventh constant in the table, etc.  Defaults to the
            last location filled + 1.

        t1, t2, t3, . . . , t6
            Temperatures assigned to six locations starting with SLOC.  If a
            value is already in this location, it will be redefined.  A blank
            (or zero) value for T1 resets the previous value in SLOC to zero.
            A value of zero can only be assigned by T1.  Blank (or zero) values
            for T2 to T6 leave the corresponding previous values unchanged.

        Notes
        -----
        Defines a temperature table to be associated with the property data
        table [MPDATA].  These temperatures are also used for polynomial
        property evaluation, if defined [MP].  Temperatures must be defined in
        non-descending order.  Issue MATER $ STAT to list the current
        temperature table.  Repeat MPTEMP command for additional temperatures
        (100 maximum).  If all arguments are blank, the temperature table is
        erased.

        For clear definition, the temperature range you define with the MPTEMP
        command should include the entire range you'll use in subsequently
        defined materials.  To assist the user in this, the first (and only the
        first) excursion out of the temperature range defined by the MPTEMP
        commands is flagged with a warning message.  Similarly, the reference
        temperature (TREF or MP,reft commands) should also fall in this same
        temperature range.  If not and MP,alpx was used, a note will be output.
        If not, and MP,ctex or MP,thsx was used, an error message will be
        output.

        This command is also valid in SOLUTION.
        """
        command = "MPTEMP,%s,%s,%s,%s,%s,%s,%s" % (
            str(sloc),
            str(t1),
            str(t2),
            str(t3),
            str(t4),
            str(t5),
            str(t6),
        )
        return self.run(command, **kwargs)

    def mptgen(self, stloc="", num="", tstrt="", tinc="", **kwargs):
        """APDL Command: MPTGEN

        Adds temperatures to the temperature table by generation.

        Parameters
        ----------
        stloc
            Starting location in table for generating temperatures.  Defaults
            to last location filled + 1.

        num
            Number of temperatures to be generated (1-100).

        tstrt
            Temperature assigned to STLOC location.

        tinc
            Increment previous temperature by TINC and assign to next location
            until all NUM locations are filled.

        Notes
        -----
        Adds temperatures to the temperature table by generation.  May be used
        in combination (or in place of) the MPTEMP command.

        This command is also valid in SOLUTION.
        """
        command = "MPTGEN,%s,%s,%s,%s" % (
            str(stloc),
            str(num),
            str(tstrt),
            str(tinc),
        )
        return self.run(command, **kwargs)

    def mptres(self, lab="", mat="", **kwargs):
        """APDL Command: MPTRES

        Restores a temperature table previously defined.

        Parameters
        ----------
        lab
            Material property label [MP].

        mat
            Material reference number.

        Notes
        -----
        Restores into the database (from virtual space) a temperature table
        previously defined [MP] for a particular property.  The existing
        temperature table in the database is erased before this operation.

        This command is also valid in SOLUTION.
        """
        command = "MPTRES,%s,%s" % (str(lab), str(mat))
        return self.run(command, **kwargs)

    def mpwrite(self, fname="", ext="", lib="", mat="", **kwargs):
        """APDL Command: MPWRITE

        Writes linear material properties in the database to a file
        (if the LIB option is not specified) or writes both linear and
        nonlinear material properties (if LIB is specified) from the
        database to a file.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including
            directory). If you do not specify the ``LIB`` option, the default
            directory is the current working directory. If you specify ``LIB`` and
            you have specified a material library directory (via the ``/MPLIB``
            command), that directory is the default. Otherwise, the default is
            the current working directory. If you use the default for your
            directory, you can use all 248 characters for the file name.

            The file name defaults to Jobname.

        ext
            Filename extension (eight-character maximum).

            If you omit the ``LIB`` option, the default extension is
            MP. If you specify the ``LIB`` option, the default extension
            is units_MPL, where units is the system of units currently
            in use. (See the description of the ``/UNITS`` command.) For
            example, if ``/UNITS`` is set to BIN, the extension defaults
            to BIN_MPL.

        lib
            The only value allowed for this field is the string ``"LIB"``.

            The ``LIB`` option indicates that you wish to have properties
            associated with the material (``MAT``) written to the
            specified material library file using the material library
            file format. The material library file format is
            ASCII-text-based ANSYS command input. Certain commands
            associated with this format have been modified to
            interpret the string "_MATL" to mean the currently
            selected material. This feature makes the material library
            file independent of the material number in effect when the
            file was written; this enables you to restore the
            properties into the ANSYS database using the material
            number of your choice. The ``LIB`` option also enables you to
            save both linear and nonlinear properties. If you omit the
            ``LIB`` option, you can save linear properties only.

        mat
            Specifies the material to be written to the named material library
            file.  There is no default; you must either specify a material or
            omit the ``MAT`` argument.  Even if you specify a ``MAT`` value, the ANSYS
            program ignores it if the ``LIB`` argument is not specified.

        Notes
        -----
        Writes linear material properties currently in the database to a file.
        The file is rewound before and after writing.

        This command is also valid in SOLUTION.
        """
        return self.run(f"MPWRITE,{fname},{ext},,{lib},{mat}", **kwargs)

    def tbft(
        self,
        oper="",
        id_="",
        option1="",
        option2="",
        option3="",
        option4="",
        option5="",
        option6="",
        option7="",
        **kwargs,
    ):
        """APDL Command: TBFT

        Performs material curve-fitting operations.

        Parameters
        ----------
        oper
            The specific curve-fitting operation:

            Define a constitutive model. - Delete a constitutive model.

            Write data related to a constitutive model to the database (same as TB command). - Initialize coefficients of a constitutive model for nonlinear curve-fitting
                              procedure.

            Deletes coefficients at current reference temperature. Applicable only for temperature dependent coefficients.  - Solve for coefficients.

            Fix (hold constant) the coefficient you specify in Option4. - Add experimental data.

            Delete experimental data. - List all data associated with the material model represented by the material ID
                              number.

        id_
            The material reference number (same as MAT argument used in the TB
            command). Valid entry is any number greater than zero (default = 1)
            but less than 100,000.

        option1
            For curve-fit function operations (Oper = FADD, FDEL, FSET, SET,
            CDEL, SOLVE or FIX) this field specifies the category (HYPER).

        option2
            For curve-fit function operations (Oper = FADD, FDEL, FSET, SET,
            CDEL, SOLVE, or FIX), this field specifies constitutive model type.
            The valid entries are listed in Table 231: Hyperelastic Options
            below.

        option3
            For Oper = FADD, FDEL, FSET, CDEL, SET, SOLVE or FIX, some of the
            cases specified in Option2 will require that the polynomial order
            be specified. The applicable values for the order specification are
            listed in Table 231: Hyperelastic Options.

        option4
            When you are working on a specific coefficient (Oper = FIX), this
            field specifies the index of that coefficient. Valid entries vary
            from 1 to n, where n is the total number of coefficients (default =
            1).

        option5
            When you are working on a specific coefficient (Oper = FIX), this
            field specifies the index of that coefficient. Valid entries vary
            from 1 to N, where N is the total number of coefficients (default =
            1)

        option6
            If Oper = SOLVE, specifies the allowed tolerance in residual change
            to stop an iteration. Valid entry is 0.0 to 1.0 (default = 0.0).

        option7
            If Oper = SOLVE, specifies the allowed tolerance in coefficient
            change to stop an iteration. Valid entry is 0 to 1 (default = 0).
        """
        command = "TBFT,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(oper),
            str(id_),
            str(option1),
            str(option2),
            str(option3),
            str(option4),
            str(option5),
            str(option6),
            str(option7),
        )
        return self.run(command, **kwargs)

    def uimp(
        self,
        mat="",
        lab1="",
        lab2="",
        lab3="",
        val1="",
        val2="",
        val3="",
        **kwargs,
    ):
        """APDL Command: UIMP

        Defines constant material properties (GUI).

        Parameters
        ----------
        mat
            Material number.

        lab1, lab2, lab3
            Material property labels (see the MP command for valid labels).

        val1, val2, val3
            Values corresponding to three labels.

        Notes
        -----
        Defines constant material properties.  This is a command generated by
        the Graphical User Interface (GUI) and will appear in the log file
        (Jobname.LOG) if material properties are specified using the Material
        Properties dialog box. This command is not intended to be typed in
        directly in an ANSYS session (although it can be included in an input
        file for batch input or for use with the /INPUT command).
        """
        command = "UIMP,%s,%s,%s,%s,%s,%s,%s" % (
            str(mat),
            str(lab1),
            str(lab2),
            str(lab3),
            str(val1),
            str(val2),
            str(val3),
        )
        return self.run(command, **kwargs)
