"""
These PREP7 commands create and modify the material data tables (that
is, to specify and define material models).
"""


class MaterialDataTables:
    def tb(
        self,
        lab="",
        mat="",
        ntemp="",
        npts="",
        tbopt="",
        eosopt="",
        funcname="",
        **kwargs,
    ):
        """APDL Command: TB

        Activates a data table for material properties or special element
        input.

        Parameters
        ----------
        lab
            Material model data table type:

            AFDM
                Acoustic frequency-dependent material.

            AHYPER
                Anisotropic hyperelasticity.

            ANEL
                Anisotropic elasticity.

            ANISO
                Anisotropic plasticity.

            BB
                Bergstrom-Boyce.

            BH
                Magnetic field data.

            BISO
                Bilinear isotropic hardening using von Mises or Hill plasticity.

            BKIN
                Bilinear kinematic hardening using von Mises or Hill plasticity.

            CAST
                Cast iron.

            CDM
                Mullins effect (for isotropic hyperelasticity models).

            CGCR
                Fracture criterion for crack-growth simulation (``CGROW``).

            CHABOCHE
                Chaboche nonlinear kinematic hardening using von Mises or Hill plasticity.

            COMP
                Composite damage (explicit dynamic analysis).

            CONCR
                Concrete element data.

            CREEP
                Creep. Pure creep, creep with isotropic hardening plasticity, or creep with
                kinematic hardening plasticity using both von Mises or Hill
                potentials.

            CTE
                Secant coefficient of thermal expansion.

            CZM
                Cohesive zone.

            DISCRETE
                Explicit spring-damper (discrete).

            DMGE
                Damage evolution law.

            DMGI
                Damage initiation criteria.

            DP
                Classic Drucker-Prager plasticity.

            DPER
                Anisotropic electric permittivity.

            EDP
                Extended Drucker-Prager (for granular materials such as rock, concrete, soil,
                ceramics and other pressure-dependent materials).

            ELASTIC
                Elasticity. For full harmonic analyses, properties can be defined as frequency-
                or temperature-dependent (:meth:`TBFIELD <ansys.mapdl.core.Mapdl.tbfield>`).

            EOS
                Equation of state (explicit dynamic analysis).

            EVISC
                Viscoelastic element data (explicit dynamic analysis).

            EXPE
                Experimental data.

            FCON
                Fluid conductance data (explicit dynamic analysis).

            FCLI
                Material strength limits for calculating failure criteria.

            FLUID
                Fluid.

            FOAM
                Foam (explicit dynamic analysis).

            FRIC
                Coefficient of friction based on Coulomb's Law or user-defined friction.

            GASKET
                Gasket.

            GCAP
                Geological cap (explicit dynamic analysis).

            GURSON
                Gurson pressure-dependent plasticity for porous metals.

            HFLM
                Film coefficient data.

            HILL
                Hill anisotropy. When combined with other material options, simulates
                plasticity, viscoplasticity, and creep -- all with the Hill
                potential.

            HONEY
                Honeycomb (explicit dynamic analysis).

            HYPER
                Hyperelasticity material models (Arruda-Boyce, Blatz-Ko, Extended Tube, Gent,
                Mooney-Rivlin [default], Neo-Hookean, Ogden, Ogden Foam,
                Polynomial Form, Response Function, Yeoh, and user-
                defined).

            INTER
                Contact interaction.

            JOIN
                Joint (linear and nonlinear elastic stiffness, linear and nonlinear damping, and frictional behavior).

            JROCK
                Jointed rock.

            MC
                Mohr-Coulomb.

            MELAS
                Multilinear elasticity .

            MIGR
                Migration.

            MPLANE
                Microplane.

            NLISO
                Voce isotropic hardening law (or power law) for modeling nonlinear isotropic
                hardening using von Mises or Hill plasticity.

            PELAS
                Porous elasticity.

            PERF
                Perforated material for acoustics; equivalent fluid model of perforated media,
                poroelastic material model, and transfer admittance matrix.

            PIEZ
                Piezoelectric matrix.

            PLASTIC
                Nonlinear plasticity.

            PM
                Porous media. Coupled pore-fluid diffusion and structural model of porous media.

            PRONY
                Prony series constants for viscoelastic materials.

            PZRS
                Piezoresistivity.

            RATE
                Rate-dependent plasticity (viscoplasticity) when combined with the ``BISO``, ``NLISO`` or
                ``PLASTIC`` material options, or rate-dependent anisotropic plasticity (anisotropic viscoplasticity)
                when combined with the HILL and ``BISO``, ``NLISO`` or ``PLASTIC`` material options.

                The exponential visco-hardening option includes an explicit function for directly defining
                static yield stresses of materials.
                The Anand unified plasticity option requires no combination with other material models.

            SDAMP
                Material damping coefficients.

            SHIFT
                Shift function for viscoelastic materials.

            SMA
                Shape memory alloy for simulating hysteresis superelastic behavior with no performance degradation.
                Plane stress is not supported.

            SOIL
                Soil models.

            STATE
                User-defined state variables. Valid with ``TB,USER`` and used with either the UserMat
                or UserMatTh subroutine. Also valid with ``TB,CREEP`` (when ``TBOPT`` = 100) and used with
                the UserCreep subroutine.

            SWELL
                Swelling strain function.

            TNM
                Three-network model for viscoplastic materials.

            THERM
                Thermal properties.

            USER
                User-defined material model (general-purpose except for incompressible material
                models) or thermal material model.

            WEAR
                Contact surface wear.

            XTAL
                Crystal plasticity for elasto-viscoplastic crystalline materials.

        MATID
            Material reference identification number. Valid value is any number ``n``, where 0 < ``n`` < 100,000. Default
            = 1.

        NTEMP
            The number of temperatures for which data will be provided (if applicable). Specify temperatures
            via the :meth:`TBTEMP <ansys.mapdl.core.Mapdl.tbtemp>` command.

        NPTS
            For most labels where ``NPTS`` is defined, the number of data points to be specified for a given
            temperature. Define data points via the :meth:`TBDATA <ansys.mapdl.core.Mapdl.tbdata>` or :meth:`TBPT <ansys.mapdl.core.Mapdl.tbpt>`
            commands.

        FuncName
            The name of the function to be used (entered as %tabname%, where tabname is the name of
            the table created by the Function Tool). Valid only when Lab = ``JOIN`` (joint element material) and
            nonlinear stiffness or damping are specified on the ``TBOPT`` field (see "JOIN -- Joint Element Specifications").
            The function must be predefined via the Function Tool. To learn more about how
            to create a function, see Using the Function Tool in the Basic Analysis Guide

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.
        """
        command = "TB,%s,%s,%s,%s,%s,%s,%s" % (
            str(lab),
            str(mat),
            str(ntemp),
            str(npts),
            str(tbopt),
            str(eosopt),
            str(funcname),
        )
        return self.run(command, **kwargs)

    def tbcopy(self, lab="", matf="", matt="", **kwargs):
        """APDL Command: TBCOPY

        Copies a data table from one material to another.

        Parameters
        ----------
        lab
            Data table label. See the :meth:`TB <ansys.mapdl.core.Mapdl.tb>` command for valid labels, and see
            "Notes" for Lab = ALL.

        matf
            Material reference number where data table is to be copied from.

        matt
            Material reference number where data table is to be copied to.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        The TBCOPY command, with Lab = ALL, copies all of the nonlinear data
        defined by the :meth:`TB <ansys.mapdl.core.Mapdl.tb>` command. If you copy a model that includes both yield
        behavior constants and linear constants (for example, a BKIN model),
        TBCOPY,ALL and MPCOPY are used together to copy the entire model. All
        input data associated with the model is copied, that is, all data
        defined through the :meth:`TB <ansys.mapdl.core.Mapdl.tb>` and MP commands.

        Also, if you copy a material model using the Material Model Interface
        (Edit> Copy), both the commands TBCOPY,ALL and MPCOPY are issued,
        regardless of whether the model includes linear constants only, or if
        it includes a combination of linear and yield behavior constants.

        This command is also valid in SOLUTION.
        """
        command = "TBCOPY,%s,%s,%s" % (str(lab), str(matf), str(matt))
        return self.run(command, **kwargs)

    def tbdata(self, stloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
        """APDL Command: TBDATA

        Defines data for the material data table.

        Parameters
        ----------
        stloc
            Starting location in table for entering data.  For example, if
            ``STLOC`` = 1, data input in the C1 field applies to the first table
            constant, C2 applies to the second table constant, etc.  If ``STLOC`` = 5,
            data input in the C1 field applies to the fifth table
            constant, etc.  Defaults to the last location filled + 1.  The last
            location is reset to 1 with each :meth:`TB <ansys.mapdl.core.Mapdl.tb>` or
            :meth:`TBTEMP <ansys.mapdl.core.Mapdl.tbtemp>` command.

        c1, c2, c3, . . . , c6
            Data values assigned to six locations starting with ``STLOC``.  If a
            value is already in this location, it is redefined.  A blank value
            leaves the existing value unchanged.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        Defines data for the table specified on the last :meth:`TB <ansys.mapdl.core.Mapdl.tb>` command at the
        temperature specified on the last :meth:`TBTEMP <ansys.mapdl.core.Mapdl.tbtemp>`
        command (if applicable). The type of data table specified in the last :meth:`TB <ansys.mapdl.core.Mapdl.tb>` command determines the
        number of data values needed in ``TBDATA``. Data values are linearly
        interpolated for temperatures that fall between user defined :meth:`TBTEMP <ansys.mapdl.core.Mapdl.tbtemp>`
        values. See Material Models in the Material Reference for the number of
        data values required for different material behavior options.

        This command is also valid in SOLUTION.
        """
        command = "TBDATA,%s,%s,%s,%s,%s,%s,%s" % (
            str(stloc),
            str(c1),
            str(c2),
            str(c3),
            str(c4),
            str(c5),
            str(c6),
        )
        return self.run(command, **kwargs)

    def tbdele(self, lab="", mat1="", mat2="", inc="", **kwargs):
        """APDL Command: TBDELE

        Deletes previously defined material data tables.

        Parameters
        ----------
        lab
            Data table label. (See the :meth:`TB <ansys.mapdl.core.Mapdl.tb>` command for valid labels.)  If ALL,
            delete all data tables.

        mat1, mat2, inc
            Delete tables for materials MAT1 to (MAT2 defaults to MAT1) in
            steps of INC (defaults to 1).  If MAT1= ALL, ignore MAT2 and INC
            and delete data tables for all materials.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        This command is also valid in SOLUTION.
        """
        command = "TBDELE,%s,%s,%s,%s" % (
            str(lab),
            str(mat1),
            str(mat2),
            str(inc),
        )
        return self.run(command, **kwargs)

    def tbeo(self, par="", value="", **kwargs):
        """APDL Command: TBEO

        Sets special options or parameters for material data tables.

        Parameters
        ----------
        par
            Parameter name:

            CAPCREEPREG - Available for the viscoplasticity/creep model (TB,CREEP), allows two creep
                          models to be specified via the same material ID when
                          used with the Extended Drucker-Prager model (TB,EDP).

        value
            Parameter value:

            SHEA -  Use the shear stress-state creep model with the Extended Drucker-Prager model.
                   Valid only when Par = CAPCREEPREG.

            COMP - Use the compaction stress-state creep model with the Extended Drucker-Prager
                   model. Valid only when Par = CAPCREEPREG.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        Issue the TBEO command after activating the data table (TB) but before
        defining data for the table (TBDATA) or a point on a nonlinear data
        curve (TBPT).
        """
        command = "TBEO,%s,%s" % (str(par), str(value))
        return self.run(command, **kwargs)

    def tbfield(self, type_="", value="", **kwargs):
        """APDL Command: TBFIELD

        Defines values of field variables for material data tables.

        Parameters
        ----------
        type_
            Type of field variable:

            FREQ - A frequency is to be specified in Value

            TEMP - A temperature is to be specified in Value

            TIME - A time is to be specified in Value

            NPRES - A normal pressure is to be specified in Value

            SLDA - A total sliding distance (algebraic) is to be specified in Value

            SLDI - A total sliding distance (absolute) is to be specified in Value

            SLRV - A sliding velocity is to be specified in Value

            CYCLE - A healing cycle number is to be specified in Value

            UFXX - User-defined field variable (UF01,UF02, ..., UF09)

        value
            The field value to be referenced (use this command multiple times
            to enter values of different field variables).

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        Define your data tables as field-variable-dependent (via the
        appropriate :meth:`TB <ansys.mapdl.core.Mapdl.tb>` command shown below), then issue the TBFIELD command to
        define the field values.

        Define data values in ascending order for all field quantities. If a
        field value is to be held constant, define it only once; subsequent
        definitions are ignored.

        There is no limit on the number of values you can specify. The
        specified field value remains active until the next TBFIELD command is
        input.

        After you have defined the field value(s), define your data for the
        data tables (TBDATA).

        See Understanding Field Variables in the Material Reference for more
        information about the interpolation scheme used for field-dependent
        material properties.

        See Full Harmonic Analysis in the Structural Analysis Guide for more
        information about using TBFIELD with TB,ELASTIC or TB,SDAMP.

        The TBFIELD command supports the following material models (TB,Lab
        commands):

        The TEMP value specified on this command corresponds to the average
        temperature on the contact surface for contact elements CONTA171,
        CONTA172, CONTA173, CONTA174, CONTA175, CONTA176, and CONTA177. For
        contact element CONTA178, the TEMP value corresponds to the average
        temperature of the nodes.

        The TIME value specified on this command corresponds to the analysis
        time specified on the TIME command.

        The algebraic sliding distance (SLDA) specified on this command is the
        total sliding distance (the algebraic sum) as reported in the element
        output definitions table for the contact elements (for example, TASS
        and TASR output items for CONTA174).

        The absolute sliding distance (SLDI) specified on this command is the
        total accumulated sliding distance (the absolute sum) as reported in
        the element output definitions table for the contact elements (for
        example, AASS and AASR output items for CONTA174).

        When used with TB,FRIC, field variables defined by TBFIELD are only
        available for isotropic friction (TBOPT = ISO) and orthotropic friction
        (TBOPT = ORTHO); they are not available for user-defined friction
        (TBOPT = USER).

        See Contact Friction in the Material Reference for more information
        about using TBFIELD with TB,FRIC.
        """
        command = "TBFIELD,%s,%s" % (str(type_), str(value))
        return self.run(command, **kwargs)

    def tbin(self, oper="", par1="", par2="", par3="", par4="", **kwargs):
        """APDL Command: TBIN

        Sets parameters used for interpolation of the material data tables.

        Parameters
        ----------
        oper
            Operation to perform:

            Operation to perform: - SCALE

        par1
            Independent variable, which can be any field variable specified via
            the TBFIELD command.

        par2
            Index of any material parameter specified via the TBDATA command.

        par3
            Scale to be used for the independent variable. Valid options are
            LINEAR (linear) or LOG (logarithmic).

        par4
            Scale to be used for the dependent variable (the material parameter
            specified via Par2). Valid options are LINEAR (linear) or LOG
            (logarithmic).

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        For a list of the supported material data tables (TB), see Logarithmic
        Interpolation and Scaling in the Material Reference.
        """
        command = "TBIN,%s,%s,%s,%s,%s" % (
            str(oper),
            str(par1),
            str(par2),
            str(par3),
            str(par4),
        )
        return self.run(command, **kwargs)

    def tblist(self, lab="", mat="", **kwargs):
        """APDL Command: TBLIST

        Lists the material data tables.

        Parameters
        ----------
        lab
            Data table label. (See the :meth:`TB <ansys.mapdl.core.Mapdl.tb>` command for valid labels.)  Defaults
            to the active table.  If ALL, list data for all labels.

        mat
            Material number to be listed (defaults to the active material).  If
            ALL, list data tables for all materials.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        This command is a utility command, valid anywhere.
        """
        command = "TBLIST,%s,%s" % (str(lab), str(mat))
        return self.run(command, **kwargs)

    def tbmodif(self, row="", col="", value="", **kwargs):
        """APDL Command: TBMODIF

        Modifies data for the material data table (GUI).

        Parameters
        ----------
        row, col
            The row and column numbers of the table entry to be modified.

        value
            The new value to be used in the ROW, COL location.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        The TBMODIF command modifies data for the table specified on the last
        :meth:`TB <ansys.mapdl.core.Mapdl.tb>` command.

        For temperature-dependent data, the temperature specified on the last
        TBTEMP command is used.

        TBMODIF is a command generated by the Graphical User Interface (GUI).
        It appears in the log file (Jobname.LOG) if a :meth:`TB <ansys.mapdl.core.Mapdl.tb>` material data table is
        graphically edited in spreadsheet fashion.

        The TBMODIF command is not intended to be typed in directly during an
        analysis session (although it can be included in an input file for
        batch input or for use with the /INPUT command).

        This command is also valid in SOLUTION.
        """
        command = "TBMODIF,%s,%s,%s" % (str(row), str(col), str(value))
        return self.run(command, **kwargs)

    def tbplot(self, lab="", mat="", tbopt="", temp="", segn="", **kwargs):
        """APDL Command: TBPLOT

        Displays the material data table.

        Parameters
        ----------
        lab
            Data table label.  Valid labels are:  MKIN, KINH, MELAS, MISO,
            BKIN, BISO, BH, GASKET, and JOIN.  Defaults to the active table
            label.  For B-H data, also valid are: NB to display NU-B2, MH to
            display MU vs. H, and SBH, SNB, SMH to display the slopes of the
            corresponding data.

        mat
            Material number to be displayed (defaults to the active material).

        tbopt
            Gasket material or joint element material option to be plotted.

            ALL - Plots all gasket data.

            COMP - Plots gasket compression data only.

            LUNL - Plots gasket linear unloading data with compression curve.

            NUNL - Plots gasket nonlinear unloading data only.

        temp
            Specific temperature at which gasket data or joint element material
            data will be plotted (used only when Lab = GASKET or JOIN). Use
            TEMP = ALL to plot gasket data or joint element material data at
            all temperatures.

        segn
            Segment number of plotted curve (valid only when Lab = GASKET):

            NO - Segment number is not added to plotted curve (default).

            YES - Segment number is added to plotted curve. This option is ignored if the number
                  of data points in a curve exceeds 20.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        Only data for stress-strain, B-H, gasket curves, or joint element
        nonlinear material model curves can be displayed.

        The TBOPT and TEMP values are valid only when Lab = GASKET or JOIN.

        The SEGN value is valid only when Lab = GASKET.

        This command is valid in any processor.
        """
        command = "TBPLOT,%s,%s,%s,%s,%s" % (
            str(lab),
            str(mat),
            str(tbopt),
            str(temp),
            str(segn),
        )
        return self.run(command, **kwargs)

    def tbpt(self, oper="", x1="", x2="", x3="", xn="", **kwargs):
        """APDL Command: TBPT

        Defines a point on a nonlinear data curve.

        Parameters
        ----------
        oper
            Operation to perform:

            DEFI - Defines a new data point (default).  The point is inserted into the table in
                   ascending order of X1.  If a point already exists with the
                   same X1 value, it is replaced.

            DELE - Deletes an existing point.  The X1 value must match the X1 value of the point
                   to be deleted (XN is ignored).

        x1, x2, ..., xn
            The N components of the point. N depends on the type of data table.
            Except for TB,EXPE all other :meth:`TB <ansys.mapdl.core.Mapdl.tb>` Tables support only 2 components.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        TBPT defines a point on a nonlinear data curve (such as a stress-strain
        curve, B-H curve, etc.) at the temperature specified on the last TBTEMP
        command. The meaning of the values depends on the type of data table
        specified on the last :meth:`TB <ansys.mapdl.core.Mapdl.tb>` command (MISO, BH, etc.).

        This command is also valid in SOLUTION.
        """
        command = "TBPT,%s,%s,%s,%s,%s" % (
            str(oper),
            str(x1),
            str(x2),
            str(x3),
            str(xn),
        )
        return self.run(command, **kwargs)

    def tbtemp(self, temp="", kmod="", **kwargs):
        """APDL Command: TBTEMP

        Defines a temperature for a material data table.

        Parameters
        ----------
        temp
            Temperature value (defaults to 0.0 if KMOD is blank).

        kmod
            If blank, TEMP defines a new temperature. (Issue TBLIST to list
            temperatures and data.)

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Notes
        -----
        The TBTEMP command defines a temperature to be associated with the data
        on subsequent TBPT or TBDATA commands.

        The defined temperature remains active until the next TBTEMP command is
        issued.

        Data values must be defined with the temperatures in ascending order.

        This command is also valid in SOLUTION.
        """
        command = "TBTEMP,%s,%s" % (str(temp), str(kmod))
        return self.run(command, **kwargs)
