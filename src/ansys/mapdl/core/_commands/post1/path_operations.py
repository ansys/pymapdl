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


class PathOperations:

    def fssect(
        self,
        rho: str = "",
        nev: str = "",
        nlod: str = "",
        kbr: int | str = "",
        **kwargs,
    ):
        r"""Calculates and stores total linearized stress components.

        Mechanical APDL Command: `FSSECT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FSSECT.html>`_

        Parameters
        ----------
        rho : str
            In-plane (X-Y) average radius of curvature of the inside and outside surfaces of an axisymmetric
            section. If zero (or blank), a plane or 3D structure is assumed. If nonzero, an axisymmetric
            structure is assumed. Use a suitably large number (see the `Mechanical APDL Theory Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_) or use -1
            for an axisymmetric straight section.

        nev : str
            Event number to be associated with these stresses (defaults to 1).

        nlod : str
            Loading number to be associated with these stresses (defaults to 1).

        kbr : int or str
            For an axisymmetric analysis ( ``RHO`` ≠ 0):

            * ``0`` - Include the thickness-direction bending stresses

            * ``1`` - Ignore the thickness-direction bending stresses

            * ``2`` - Include the thickness-direction bending stress using the same formula as the Y (axial
              direction ) bending stress. Also use the same formula for the shear stress.

        Notes
        -----

        .. _FSSECT_notes:

        Calculates and stores the total linearized stress components at the ends of a section path (
        :ref:`path` ) (as defined by the first two nodes with the :ref:`ppath` command). The path must be
        entirely within the selected elements (that is, there must not be any element gaps along the path).
        Stresses are stored according to the fatigue event number and loading number specified. Locations
        (one for each node) are associated with those previously defined for these nodes (FL) or else they
        are automatically defined. Stresses are separated into six total components (SX through SXZ) and six
        membrane-plus-bending (SX through SXZ) components. The temperature at each end point and the current
        time are also stored along with the total stress components. Calculations are made from the stresses
        currently in the database (last :ref:`set` or :ref:`lcase` command). Stresses are stored as section
        coordinate components if axisymmetric or as global Cartesian coordinate components otherwise,
        regardless of the active results coordinate system ( :ref:`rsys` ). The FSLIST command may be used
        to list stresses. The FS command can be used to modify stored stresses. See also the :ref:`prsect`
        and :ref:`plsect` commands for similar calculations.
        """
        command = f"FSSECT,{rho},{nev},{nlod},{kbr}"
        return self.run(command, **kwargs)

    def padele(self, delopt: str = "", **kwargs):
        r"""Deletes a defined path.

        Mechanical APDL Command: `PADELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PADELE.html>`_

        **Command default:**

        .. _PADELE_default:

        Deletes the currently active path.

        Parameters
        ----------
        delopt : str
            Path delete option (one of the following):

            * ``ALL`` - Delete all defined paths.

            * ``NAME`` - Delete a specific path from the list of path definitions. (Substitute the actual path
              name for NAME.)

        Notes
        -----

        .. _PADELE_notes:

        Paths are identified by individual path names. To review the current list of path names, issue the
        command :ref:`path`,STATUS.

        This command is valid in the general postprocessor.
        """
        command = f"PADELE,{delopt}"
        return self.run(command, **kwargs)

    def paget(self, parray: str = "", popt: str = "", **kwargs):
        r"""Writes current path information into an array variable.

        Mechanical APDL Command: `PAGET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PAGET.html>`_

        Parameters
        ----------
        parray : str
            The name of the array parameter that Mechanical APDL creates to store the path information. If
            the array parameter already exists, it will be replaced with the current path information.

        popt : str
            Determines how data will be stored in the parameter specified with ``PARRAY`` :

            * ``POINTS`` - Store the path points, the nodes (if any), and coordinate system. (For information on
              defining paths and path points, see the descriptions of the :ref:`path` and :ref:`ppath` commands.)

            * ``TABLE`` - Store the path data items. (See the :ref:`pdef` command description for path data
              items.)

            * ``LABEL`` - Stores path data labels.

        Notes
        -----

        .. _PAGET_notes:

        Use the :ref:`paget` command with the :ref:`paput` command to store and retrieve path data in array
        variables for archiving purposes.

        When retrieving path information, restore the path points (POINTS option) first, then the path data
        (TABLE option), and then the path labels (LABEL option).
        """
        command = f"PAGET,{parray},{popt}"
        return self.run(command, **kwargs)

    def paput(self, parray: str = "", popt: str = "", **kwargs):
        r"""Retrieves path information from an array variable.

        Mechanical APDL Command: `PAPUT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PAPUT.html>`_

        Parameters
        ----------
        parray : str
            Name of the array variable containing the path information.

        popt : str
            Specifies which path data to retrieve:

            * ``POINTS`` - Retrieve path point information (specified with the :ref:`ppath` command and stored
              with the :ref:`paget`,POINTS command). The path data name will be assigned to the path points.

            * ``TABLE`` - Retrieve path data items (defined via the :ref:`pdef` command and stored with the
              :ref:`paget`,,TABLE command).

            * ``LABEL`` - Retrieve path labels stored with the :ref:`paget`,,LABEL command.

        Notes
        -----

        .. _PAPUT_notes:

        When retrieving path information, restore path points (POINTS option) first, then the path data
        (TABLE option), and then the path labels (LABEL option).
        """
        command = f"PAPUT,{parray},{popt}"
        return self.run(command, **kwargs)

    def paresu(self, lab: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Restores previously saved paths from a file.

        Mechanical APDL Command: `PARESU <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PARESU.html>`_

        Parameters
        ----------
        lab : str
            Read operation:

            * ``ALL`` - Read all paths from the selected file (default).

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to PATH if ``Fname`` is
            blank.

        Notes
        -----

        .. _PARESU_notes:

        This command removes all paths from virtual memory and then reads path data from a file written with
        the :ref:`pasave` command. All paths on the file will be restored. All paths currently in memory
        will be deleted.
        """
        command = f"PARESU,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def pasave(self, lab: str = "", fname: str = "", ext: str = "", **kwargs):
        r"""Saves selected paths to an external file.

        Mechanical APDL Command: `PASAVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PASAVE.html>`_

        Parameters
        ----------
        lab : str
            Write operation:

            * ``S`` - Saves only selected paths.

            * ``ALL`` - Saves all paths (default).

            * ``Pname`` - Saves the named path (from the :ref:`psel` command).

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name.

            The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum).

            The extension defaults to PATH if ``Fname`` is blank.

        Notes
        -----

        .. _PASAVE_notes:

        Saves the paths selected with the :ref:`psel` command to an external file (default
        :file:`Jobname.path` ).

        Previous paths on this file, if any, are overwritten. The path file can be read via :ref:`paresu`.

        This command is valid in POST1.
        """
        command = f"PASAVE,{lab},{fname},{ext}"
        return self.run(command, **kwargs)

    def path(
        self, name: str = "", npts: str = "", nsets: str = "", ndiv: str = "", **kwargs
    ):
        r"""Defines a path name and establishes parameters for the path.

        Mechanical APDL Command: `PATH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PATH.html>`_

        Parameters
        ----------
        name : str
            Name for this path (eight characters maximum. If ``nPts`` is blank, set the current path to the
            path with this name. If ``nPts`` is greater than zero, create a path of this name. If a path
            with this name already exists, replace it with a new path. If the ``NAME`` value is STATUS,
            display the status for path settings.

        npts : str
            The number of points used to define this path. The minimum number is two, and the maximum is
            1000. Default is 2.

        nsets : str
            The number of sets of data which you can map to this path. You must specify at least four: X, Y,
            Z, and S. Default is 30.

        ndiv : str
            The number of divisions between adjacent points. Default is 20. There is no maximum number of
            divisions.

        Notes
        -----

        .. _PATH_notes:

        The :ref:`path` command is used to define parameters for establishing a path. The path geometry is
        created by the :ref:`ppath` command. Multiple paths may be defined and named; however, only one path
        may be active for data interpolation ( :ref:`pdef` ) and data operations ( :ref:`pcalc`, etc.). Path
        geometry points and data are stored in memory while in POST1. If you leave POST1, the path
        information is erased. Path geometry and data may be saved in a file by archiving the data using the
        :ref:`pasave` command. Path information may be restored by retrieving the data using the
        :ref:`paresu` command.

        For overlapping nodes, the lowest numbered node is assigned to the path.

        The number of divisions defined using ``nDiv`` does NOT affect the number of divisions used by
        :ref:`plsect` and :ref:`prsect`.

        For information on displaying paths you have defined, see `Mapping Results onto a Path
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_3.html#basdelepathtlm51799>`_
        """
        command = f"PATH,{name},{npts},{nsets},{ndiv}"
        return self.run(command, **kwargs)

    def pcalc(
        self,
        oper: str = "",
        labr: str = "",
        lab1: str = "",
        lab2: str = "",
        fact1: str = "",
        fact2: str = "",
        const: str = "",
        **kwargs,
    ):
        r"""Forms additional labeled path items by operating on existing path items.

        Mechanical APDL Command: `PCALC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PCALC.html>`_

        Parameters
        ----------
        oper : str
            Type of operation to be performed. See :ref:`PCALC_notes` below for specific descriptions of each operation:

            * ``ADD`` - Adds two existing path items.

            * ``MULT`` - Multiplies two existing path items.

            * ``DIV`` - Divides two existing path items (a divide by zero results in a value of zero).

            * ``EXP`` - Exponentiates and adds existing path items.

            * ``DERI`` - Finds a derivative.

            * ``INTG`` - Finds an integral.

            * ``SIN`` - Sine.

            * ``COS`` - Cosine.

            * ``ASIN`` - Arcsine.

            * ``ACOS`` - Arccosine.

            * ``LOG`` - Natural log.

        labr : str
            Label assigned to the resulting path item.

        lab1 : str
            First labeled path item in operation.

        lab2 : str
            Second labeled path item in operation. ``Lab2`` must not be blank for the MULT, DIV, DERI, and
            INTG operations.

        fact1 : str
            Factor applied to ``Lab1``. A (blank) or '0' entry defaults to 1.0.

        fact2 : str
            Factor applied to ``Lab2``. A (blank) or '0' entry defaults to 1.0.

        const : str
            Constant value (defaults to 0.0).

        Notes
        -----

        .. _PCALC_notes:

        If ``Oper`` = ADD, the command format is:

        :ref:`pcalc`,ADD, ``LabR``, ``Lab1``, ``Lab2``, ``FACT1``, ``FACT2``, ``CONST``

        This operation adds two existing path items according to the operation:

        ``LabR`` = ( ``FACT1`` x ``Lab1`` ) + ( ``FACT2`` x ``Lab2`` ) + ``CONST``

        It may be used to scale the results for a single path item.

        If ``Oper`` = MULT, the command format is:

        :ref:`pcalc`,MULT, ``LabR``, ``Lab1``, ``Lab2``, ``FACT1``

        ``Lab2`` must not be blank. This operation multiplies two existing path items according to the
        operation:

        ``LabR`` = ``Lab1`` x ``Lab2`` x ``FACT1``

        If ``Oper`` = DIV, the command format is:

        :ref:`pcalc`,DIV, ``LabR``, ``Lab1``, ``Lab2``, ``FACT1``

        ``Lab2`` must not be blank. This operation divides two existing path items according to the
        operation:

        ``LabR`` = ( ``Lab1`` / ``Lab2`` ) x ``FACT1``

        If ``Oper`` = EXP, the command format is:

        :ref:`pcalc`,EXP, ``LabR``, ``Lab1``, ``Lab2``, ``FACT1``, ``FACT2``

        This operation exponentiates and adds existing path items according to the operation:

        ``LabR`` = (\| ``Lab1`` \| :sup:`FACT1` ) + (\| ``Lab2`` \| :sup:`FACT2` \|)

        If ``Oper`` = DERI, the command format is:

        :ref:`pcalc`,DERI, ``LabR``, ``Lab1``, ``Lab2``, ``FACT1``

        ``Lab2`` must not be blank. This operation finds a derivative according to the operation:

        ``LabR`` = ``FACT1`` x d( ``Lab1`` )/d( ``Lab2`` )

        If ``Oper`` = INTG, the command format is:

        :ref:`pcalc`,INTG, ``LabR``, ``Lab1``, ``Lab2``, ``FACT1``

        ``Lab2`` must not be blank. This operation finds an integral according to the operation:

        .. math::

            equation not available

        Use S for ``Lab2`` to integrate ``Lab1`` with respect to the path length. S, the distance along the
        path, is automatically calculated by the program when a path item is created with the :ref:`pdef`
        command.

        If ``Oper`` = SIN, COS, ASIN, ACOS, or LOG, the command format is:

        :ref:`pcalc`,Oper, ``LabR``, ``Lab1``, ``FACT1``, ``CONST``

        where the function (SIN, COS, ASIN, ACOS or LOG) is substituted for ``Oper`` and ``Lab2`` is blank.

        The operation finds the resulting path item according to one of the following formulas:

        ``LabR`` = FACT2 x ``sin(FACT1 x Lab1) + CONST``

        ``LabR`` = FACT2 x ``cos(FACT1 x Lab1) + CONST``

        ``LabR`` = FACT2 x ``sin`` -1(FACT1 x Lab1) + CONST

        ``LabR`` = FACT2 x ``cos`` -1(FACT1 x Lab1) + CONST

        ``LabR`` = FACT2 x ``log(FACT1 x Lab1) + CONST``

        """
        command = f"PCALC,{oper},{labr},{lab1},{lab2},{fact1},{fact2},{const}"
        return self.run(command, **kwargs)

    def pcross(
        self,
        labxr: str = "",
        labyr: str = "",
        labzr: str = "",
        labx1: str = "",
        laby1: str = "",
        labz1: str = "",
        labx2: str = "",
        laby2: str = "",
        labz2: str = "",
        **kwargs,
    ):
        r"""Calculates the cross product of two path vectors along the current path.

        Mechanical APDL Command: `PCROSS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PCROSS.html>`_

        Parameters
        ----------
        labxr : str
            Label assigned to X-component of resultant vector.

        labyr : str
            Label assigned to Y-component of resultant vector.

        labzr : str
            Label assigned to Z-component of resultant vector.

        labx1 : str
            X-component of first vector label (labeled path item).

        laby1 : str
            Y-component of first vector label.

        labz1 : str
            Z-component of first vector label.

        labx2 : str
            X-component of second vector label (labeled path item).

        laby2 : str
            Y-component of second vector label.

        labz2 : str
            Z-component of second vector label.
        """
        command = f"PCROSS,{labxr},{labyr},{labzr},{labx1},{laby1},{labz1},{labx2},{laby2},{labz2}"
        return self.run(command, **kwargs)

    def pdef(
        self, lab: str = "", item: str = "", comp: str = "", avglab: str = "", **kwargs
    ):
        r"""Interpolates an item onto a path.

        Mechanical APDL Command: `PDEF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PDEF.html>`_

        Parameters
        ----------
        lab : str
            Label assigned to the resulting path item (8 characters maximum). This item may be used as input
            for other path operations.

        item : str
            Label identifying the item for interpolation. Valid item labels are shown in :ref:`pdef_tab_1`
            below. Some items also require a component label.

        comp : str
            Component of the item (if required). Valid component labels are shown in :ref:`pdef_tab_1`
            below.

        avglab : str
            Option to average across element boundaries:

            * ``AVG`` - Average element results across elements (default).

            * ``NOAV`` - Do not average element results across elements. If the parameter ``DISCON`` = MAT on
              the :ref:`pmap` command, this option is automatically invoked.

        Notes
        -----

        .. _PDEF_notes:

        Defines and interpolates a labeled path item along a predefined path ( :ref:`path` ). Path item
        results are in the global Cartesian coordinate directions unless transformed ( :ref:`rsys` ). A path
        item must be defined before it can be used with other path operations. Additional path items may be
        defined from the :ref:`pvect`, :ref:`pcalc`, :ref:`pdot`, and :ref:`pcross` commands. Path items may
        be listed ( :ref:`prpath` ) or displayed ( :ref:`plpath`, :ref:`plpagm` ). A maximum number of path
        items permitted is established by the ``nSets`` argument specified with the :ref:`path` command.

        When you create the first path item ( :ref:`pdef` or :ref:`pvect` ), the program automatically
        interpolates four path items which are used to describe the geometry of the path. These predefined
        items are the position of the interpolated path points (labels XG, YG, and ZG) in global Cartesian
        coordinates, and the path length (label S). For alternate methods of mapping the path geometry (to
        include, for example, material discontinuity) see the :ref:`pmap` command. These items may also be
        listed or displayed with the :ref:`prpath`, :ref:`plpath`, and :ref:`plpagm` commands.

        If specifying that load case operations act on principal/equivalent stresses ( :ref:`sumtype`,PRIN),
        derived quantities (principal and equivalent stresses/strains) will be zero for path plots. A
        typical use for such a case involves mode combinations in a response spectrum analysis.

        The number of interpolation points on the path is defined by the ``nDiv`` argument on the
        :ref:`path` command. See `Mapping Nodal and Element Data onto the Path
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post3.html#LazAk2efjw>`_
        :ref:`pdef`,STAT to list the path item labels. Use :ref:`pdef`,CLEAR to erase all labeled path
        items, except the path geometry items (XG, YG, ZG, S).

        See also `Mapping Results onto a Path
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_3.html#basdelepathtlm51799>`_

        .. _pdef_tab_1:

        PDEF - Valid Item and Component Labels
        **************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - Valid item and component labels for nodal degree of freedom results are:
           * - U
             - X, Y, Z, SUM
             - X, Y, or Z structural displacement or vector sum.
           * - ROT
             - X, Y, Z, SUM
             - X, Y, or Z structural rotation or vector sum.
           * - TEMP[ :ref:`PDEF_temp` ]
             -
             - Temperature.
           * - PRES
             -
             - Pressure.
           * - VOLT
             -
             - Electric potential.
           * - MAG
             -
             - Magnetic scalar potential.
           * - V
             - X, Y, Z, SUM
             - X, Y, or Z fluid velocity or vector sum.
           * - A
             - X, Y, Z, SUM
             - X, Y, or Z magnetic vector potential or vector sum.
           * - CONC
             -
             - Concentration.
           * - CURR
             -
             - Current.
           * - EMF
             -
             - Electromotive force drop.
           * - Valid item and component labels for element results are:
           * - S
             - X, Y, Z, XY, YZ, XZ
             - Component stress.
           * - "
             - 1, 2, 3
             - Principal stress.
           * - "
             - INT, EQV
             - Stress intensity or Equivalent stress.
           * - EPTO
             - X, Y, Z, XY, YZ, XZ
             - Component total strain (EPEL + EPPL + EPCR).
           * - "
             - 1, 2, 3
             - Principal total strain.
           * - "
             - INT, EQV
             - Total strain intensity or total equivalent strain.
           * - EPEL
             - X, Y, Z, XY, YZ, XZ
             - Component elastic strain.
           * - "
             - 1, 2, 3
             - Principal elastic strain.
           * - "
             - INT, EQV
             - Elastic strain intensity or elastic equivalent strain.
           * - EPPL
             - X, Y, Z, XY, YZ, XZ
             - Component plastic strain.
           * - "
             - 1, 2, 3
             - Principal plastic strain.
           * - "
             - INT, EQV
             - Plastic strain intensity or plastic equivalent strain.
           * - EPCR
             - X, Y, Z, XY, YZ, XZ
             - Component creep strain.
           * - "
             - 1, 2, 3
             - Principal creep strain.
           * - "
             - INT, EQV
             - Creep strain intensity or creep equivalent strain.
           * - EPTH
             - X, Y, Z, XY, YZ, XZ
             - Component thermal strain.
           * - "
             - 1, 2, 3
             - Principal thermal strain.
           * - "
             - INT, EQV
             - Thermal strain intensity or thermal equivalent strain.
           * - EPSW
             -
             - Swelling strain.
           * - NL
             - SEPL
             - Equivalent stress (from stress-strain curve).
           * - "
             - SRAT
             - Stress state ratio.
           * - "
             - HPRES
             - Hydrostatic pressure.
           * - "
             - EPEQ
             - Accumulated equivalent plastic strain.
           * - "
             - PSV
             - Plastic state variable.
           * - "
             - PLWK
             - Plastic work/volume.
           * - For contact results PowerGraphics is applicable for 3D models only.
           * - CONT
             - STAT :ref:`PDEFcontstat`
             - Contact status.
           * - "
             - PENE
             - Contact penetration.
           * - "
             - PRES
             - Contact pressure.
           * - "
             - SFRIC
             - Contact friction stress.
           * - "
             - STOT
             - Contact total stress (pressure plus friction).
           * - "
             - SLIDE
             - Contact sliding distance.
           * - "
             - GAP
             - Contact gap distance.
           * - "
             - FLUX
             - Total heat flux at contact surface.
           * - TG
             - X, Y, Z, SUM
             - Component thermal gradient or vector sum.
           * - TF
             - X, Y, Z, SUM
             - Component thermal flux or vector sum.
           * - PG
             - X, Y, Z, SUM
             - Component pressure gradient or vector sum.
           * - EF
             - X, Y, Z, SUM
             - Component electric field or vector sum.
           * - D
             - X, Y, Z, SUM
             - Component electric flux density or vector sum.
           * - JC
             - X, Y, Z, SUM
             - Component conduction current density or vector sum (for elements that support conduction current calculation)
           * - H
             - X, Y, Z, SUM
             - Component magnetic field intensity or vector sum.
           * - B
             - X, Y, Z, SUM
             - Component magnetic flux density or vector sum.
           * - CG
             - X, Y, Z, SUM
             - Component concentration gradient or vector sum
           * - DF
             - X, Y, Z, SUM
             - Component diffusion flux density or vector sum
           * - FMAG
             - X, Y, Z, SUM
             - Component electromagnetic force or vector sum.
           * - ETAB
             - Lab
             - Any user-defined element table label (see :ref:`etable` command).
           * - BFE
             - TEMP
             - Applied and calculated temperatures along a defined path.
           * - SPL
             -
             - Sound pressure level.
           * - SPLA
             -
             - A-weighted sound pressure level (dBA).

        .. _PDEF_temp:

        For ``SHELL131`` and ``SHELL132`` elements with KEYOPT(3) = 0 or 1, use the labels TBOT, TE2,
        TE3,..., TTOP instead of TEMP.

        .. _PDEFcontstat:

        For more information on the meaning of contact status and its possible values, see `Reviewing
        Results in POST1
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_revresu.html#ctecpostslide>`_
        """
        command = f"PDEF,{lab},{item},{comp},{avglab}"
        return self.run(command, **kwargs)

    def pdot(
        self,
        labr: str = "",
        labx1: str = "",
        laby1: str = "",
        labz1: str = "",
        labx2: str = "",
        laby2: str = "",
        labz2: str = "",
        **kwargs,
    ):
        r"""Calculates the dot product of two path vectors along the current path.

        Mechanical APDL Command: `PDOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PDOT.html>`_

        Parameters
        ----------
        labr : str
            Label assigned to dot product result.

        labx1 : str
            X-component of first vector label (labeled path item).

        laby1 : str
            Y-component of first vector label (labeled path item).

        labz1 : str
            Z-component of first vector label (labeled path item).

        labx2 : str
            X-component of second vector label (labeled path item).

        laby2 : str
            Y-component of second vector label (labeled path item).

        labz2 : str
            Z-component of second vector label (labeled path item).
        """
        command = f"PDOT,{labr},{labx1},{laby1},{labz1},{labx2},{laby2},{labz2}"
        return self.run(command, **kwargs)

    def plpagm(self, item: str = "", gscale: str = "", nopt: str = "", **kwargs):
        r"""Displays path items along the path geometry.

        Mechanical APDL Command: `PLPAGM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLPAGM.html>`_

        Parameters
        ----------
        item : str
            The path data item to be displayed on the currently active path (defined by the :ref:`path`
            command). Valid path items are those defined with the :ref:`pdef` or :ref:`plnear` commands.

        gscale : str
            Scale factor for the offset from the path for the path data item displays. Defaults to 1.0.

        nopt : str
            Determines how data is displayed:

            * ``(blank)`` - Do not display nodes, and scale the display based on the currently selected node set
              (default).

            * ``NODE`` - Display path item data along with the currently selected set of nodes. The display
              geometry is scaled to the selected node set.

        Notes
        -----

        .. _PLPAGM_notes:

        You can use the ``Gscale`` argument to scale the contour display offset from the path for clarity.
        You need to type all six characters to issue this command.

        Fore more information, see `Mapping Results onto a Path
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_3.html#basdelepathtlm51799>`_
        """
        command = f"PLPAGM,{item},{gscale},{nopt}"
        return self.run(command, **kwargs)

    def plpath(
        self,
        lab1: str = "",
        lab2: str = "",
        lab3: str = "",
        lab4: str = "",
        lab5: str = "",
        lab6: str = "",
        **kwargs,
    ):
        r"""Displays path items on a graph.

        Mechanical APDL Command: `PLPATH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLPATH.html>`_

        Parameters
        ----------
        lab1 : str
            Labels identifying the path items to be displayed. Up to six items may be drawn per frame.
            Predefined path geometry items XG, YG, ZG, and S ( :ref:`pdef` ) may also be displayed.

        lab2 : str
            Labels identifying the path items to be displayed. Up to six items may be drawn per frame.
            Predefined path geometry items XG, YG, ZG, and S ( :ref:`pdef` ) may also be displayed.

        lab3 : str
            Labels identifying the path items to be displayed. Up to six items may be drawn per frame.
            Predefined path geometry items XG, YG, ZG, and S ( :ref:`pdef` ) may also be displayed.

        lab4 : str
            Labels identifying the path items to be displayed. Up to six items may be drawn per frame.
            Predefined path geometry items XG, YG, ZG, and S ( :ref:`pdef` ) may also be displayed.

        lab5 : str
            Labels identifying the path items to be displayed. Up to six items may be drawn per frame.
            Predefined path geometry items XG, YG, ZG, and S ( :ref:`pdef` ) may also be displayed.

        lab6 : str
            Labels identifying the path items to be displayed. Up to six items may be drawn per frame.
            Predefined path geometry items XG, YG, ZG, and S ( :ref:`pdef` ) may also be displayed.

        Notes
        -----

        .. _PLPATH_notes:

        The path must have been defined by the :ref:`path` and :ref:`ppath` commands. Path items and their
        labels must have been defined with the :ref:`pdef`, :ref:`pvect`, :ref:`pcalc`, :ref:`pdot`,
        :ref:`pcross`, or :ref:`plnear` commands. Path items may also be printed with the :ref:`prpath`
        command. Graph scaling may be controlled with the :ref:`xrange`, :ref:`yrange`, and :ref:`prange`
        commands. You need to type all six characters to issue this command.

        Fore more information, see `Mapping Results onto a Path
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_3.html#basdelepathtlm51799>`_
        """
        command = f"PLPATH,{lab1},{lab2},{lab3},{lab4},{lab5},{lab6}"
        return self.run(command, **kwargs)

    def plsect(
        self,
        item: str = "",
        comp: str = "",
        rho: str = "",
        kbr: int | str = "",
        kbr3d: int | str = "",
        **kwargs,
    ):
        r"""Displays membrane and membrane-plus-bending linearized stresses.

        Mechanical APDL Command: `PLSECT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLSECT.html>`_

        Parameters
        ----------
        item : str
            Label identifying the item to be processed. Valid item labels are shown in :ref:`plsect_tab_1`
            below. Items also require a component label.

        comp : str
            Component of the item. Valid component labels are shown in :ref:`plsect_tab_1` below.

        rho : str
            In-plane (X-Y) average radius of curvature of the inside and outside surfaces of an axisymmetric
            section. If zero (or blank), a plane or 3D structure is assumed. If nonzero, an axisymmetric
            structure is assumed. Use a very large number (or -1) for an axisymmetric straight section.

        kbr : int or str
            Through-thickness bending stresses key for an axisymmetric analysis ( ``RHO`` ≠ 0):

            * ``0`` - Include the thickness-direction bending stresses.

            * ``1`` - Ignore the thickness-direction bending stresses.

            * ``2`` - Include the thickness-direction bending stress using the same formula as the Y (axial
              direction ) bending stress. Also use the same formula for the shear stress.

        kbr3d : int or str
            Through-thickness bending stresses key for 3D geometry ( ``RHO`` = 0):

            * ``0`` - Include the thickness-direction bending stresses.

            * ``1`` - Ignore the following thickness-direction bending stresses: SX, SXY, SXZ

        Notes
        -----

        .. _PLSECT_notes:

        Calculates and displays the membrane and membrane-plus-bending linearized stresses (as described for
        the :ref:`prsect` command) along a path section ( :ref:`path` ) as a graph. The path section is
        defined by two points specified with the :ref:`ppath` command. For linearized stress calculations,
        the path must be defined with nodes. The path must be entirely within the selected elements (that
        is, there must not be any element gaps along the path). The total stress (equivalent to the
        :ref:`plpath` display) is also displayed. This command always uses 48 divisions along the path,
        regardless of the number of divisions defined by :ref:`path`.

        In analyses of 3D models with ``RHO`` = 0, ignoring the calculated out-of-plane bending stresses is
        recommended in some scenarios when determining the linearized bending stresses. If ``KBR3D`` = 0,
        all calculated stresses are included in the linearized bending-stress calculations. If ``KBR3D`` =
        1, these calculated out-of-plane bending stresses are ignored in the linearized bending-stress
        calculations: SX, SXY, SXZ. (The principal bending-stress calculation for S1, S2, S3, SINT, and SEQV
        is performed with these zeroed components.)

        Portions of this command are not supported by PowerGraphics ( :ref:`graphics`,POWER).

        .. _plsect_tab_1:

        PLSECT - Valid Item and Component Labels
        ****************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - Valid item and component labels for element results are:
           * - S
             - X, Y, Z, XY, YZ, XZ
             - Component stress.
           * - "
             - 1, 2, 3
             - Principal stress.
           * - "
             - INT, EQV
             - Stress intensity or equivalent stress.

        """
        command = f"PLSECT,{item},{comp},{rho},{kbr},{kbr3d}"
        return self.run(command, **kwargs)

    def pmap(self, form: str = "", discon: str = "", **kwargs):
        r"""Creates mapping of the path geometry by defining path interpolation division points.

        Mechanical APDL Command: `PMAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PMAP.html>`_

        Parameters
        ----------
        form : str
            Defines the mapping method:

            * ``UNIFORM`` - Maps uniform divisions (specified on the ``nDiv`` argument of the :ref:`path`
              command) between specified points. This is the default.

            * ``ACCURATE`` - Map geometry using a small division at the beginning and end of each segment. This
              gives you accurate derivatives, integrals, tangents, and normals for curves which do not have
              continuous slopes at the specified points. To create nonuniform divisions, the ``nDiv`` argument of
              the :ref:`path` command must be greater than 2.

        discon : str
            Sets mapping for discontinuities in the field. The divisions are modified to put a point just
            before and just after the discontinuity. The valid label is MAT, for a material discontinuity.
            No discontinuity is the default. Discontinuity mapping involves the NOAV option on the
            :ref:`pdef` command.
        """
        command = f"PMAP,{form},{discon}"
        return self.run(command, **kwargs)

    def ppath(
        self,
        point: str = "",
        node: str = "",
        x: str = "",
        y: str = "",
        z: str = "",
        cs: str = "",
        **kwargs,
    ):
        r"""Defines a path by picking or defining nodes, or locations on the currently active working plane, or
        by entering specific coordinate locations.

        Mechanical APDL Command: `PPATH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PPATH.html>`_

        Parameters
        ----------
        point : str
            The point number. It must be greater than zero and less than or equal to the ``nPts`` value
            specified on the :ref:`path` command if graphical picking is not being used.

        node : str
            The node number defining this point. If blank, use the X, Y, Z coordinates to define the point.
            A valid node number will override ``X``, ``Y``, ``Z`` coordinate arguments.

        x : str
            The location of the point in the global Cartesian coordinate system. Use these arguments only if
            you omit the ``NODE`` argument.

        y : str
            The location of the point in the global Cartesian coordinate system. Use these arguments only if
            you omit the ``NODE`` argument.

        z : str
            The location of the point in the global Cartesian coordinate system. Use these arguments only if
            you omit the ``NODE`` argument.

        cs : str
            The coordinate system for interpolation of the path between the previous point and this point.
            Omit this argument if you wish to use the currently active ( :ref:`csys` ) coordinate system. If
            the coordinate system of two adjacent points is different, the ``CS`` value of the latter point
            will be used.

        Notes
        -----

        .. _PPATH_notes:

        For linearized stress calculations, the path must be defined with nodes.

        This command is designed and works best in interactive (GUI) mode, using the menu paths listed
        below. For command line operations, issue :ref:`ppath`,P to define your path by picking nodes.

        For information on displaying paths you have defined, see `Mapping Results onto a Path
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_3.html#basdelepathtlm51799>`_
        """
        command = f"PPATH,{point},{node},{x},{y},{z},{cs}"
        return self.run(command, **kwargs)

    def prange(
        self, linc: str = "", vmin: str = "", vmax: str = "", xvar: str = "", **kwargs
    ):
        r"""Determines the path range.

        Mechanical APDL Command: `PRANGE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRANGE.html>`_

        **Command default:**

        .. _PRANGE_default:

        Include every interpolation point and entire path distance.

        Parameters
        ----------
        linc : str
            Set the range for listing or displaying the table locations between a minimum value ( ``VMIN`` )
            and a maximum value ( ``VMAX`` ) of the path distance with a location increment of ``LINC``
            (defaults to 1). The first location begins at ``VMIN``.

        vmin : str
            Set the range for listing or displaying the table locations between a minimum value ( ``VMIN`` )
            and a maximum value ( ``VMAX`` ) of the path distance with a location increment of ``LINC``
            (defaults to 1). The first location begins at ``VMIN``.

        vmax : str
            Set the range for listing or displaying the table locations between a minimum value ( ``VMIN`` )
            and a maximum value ( ``VMAX`` ) of the path distance with a location increment of ``LINC``
            (defaults to 1). The first location begins at ``VMIN``.

        xvar : str
            Path variable item to be used as the x-axis plot variable. Any valid path variable may be used (
            :ref:`pdef` command). Default variable is the path distance, S.

        Notes
        -----

        .. _PRANGE_notes:

        Determines the path distance range for use with the :ref:`prpath` and :ref:`plpath` commands.
        """
        command = f"PRANGE,{linc},{vmin},{vmax},{xvar}"
        return self.run(command, **kwargs)

    def prpath(
        self,
        lab1: str = "",
        lab2: str = "",
        lab3: str = "",
        lab4: str = "",
        lab5: str = "",
        lab6: str = "",
        **kwargs,
    ):
        r"""Prints path items along a geometry path.

        Mechanical APDL Command: `PRPATH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRPATH.html>`_

        Parameters
        ----------
        lab1 : str
            Labels identifying the path items to be printed. Up to six items may be printed at a time.
            Predefined path geometry items XG, YZ, ZG, and S ( :ref:`pdef` ) may also be printed.

        lab2 : str
            Labels identifying the path items to be printed. Up to six items may be printed at a time.
            Predefined path geometry items XG, YZ, ZG, and S ( :ref:`pdef` ) may also be printed.

        lab3 : str
            Labels identifying the path items to be printed. Up to six items may be printed at a time.
            Predefined path geometry items XG, YZ, ZG, and S ( :ref:`pdef` ) may also be printed.

        lab4 : str
            Labels identifying the path items to be printed. Up to six items may be printed at a time.
            Predefined path geometry items XG, YZ, ZG, and S ( :ref:`pdef` ) may also be printed.

        lab5 : str
            Labels identifying the path items to be printed. Up to six items may be printed at a time.
            Predefined path geometry items XG, YZ, ZG, and S ( :ref:`pdef` ) may also be printed.

        lab6 : str
            Labels identifying the path items to be printed. Up to six items may be printed at a time.
            Predefined path geometry items XG, YZ, ZG, and S ( :ref:`pdef` ) may also be printed.

        Notes
        -----

        .. _PRPATH_notes:

        Prints path items with respect to a geometry path (as defined by the :ref:`path` and :ref:`ppath`
        commands). Path items and their labels must have been defined with the :ref:`pdef`, :ref:`pvect`,
        :ref:`pcalc`, :ref:`pdot`, :ref:`pcross`, or :ref:`prnear` commands. Path items may also be
        displayed with the :ref:`plpath` and :ref:`plpagm` commands. See the :ref:`prange` command for range
        control of the path.

        Fore more information, see `Mapping Results onto a Path
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_3.html#basdelepathtlm51799>`_
        """
        command = f"PRPATH,{lab1},{lab2},{lab3},{lab4},{lab5},{lab6}"
        return self.run(command, **kwargs)

    def prsect(
        self, rho: str = "", kbr: int | str = "", kbr3d: int | str = "", **kwargs
    ):
        r"""Calculates and prints linearized stresses along a section path.

        Mechanical APDL Command: `PRSECT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRSECT.html>`_

        Parameters
        ----------
        rho : str
            In-plane (X-Y) average radius of curvature of the inside and outside surfaces of an axisymmetric
            section. If zero (or blank), a plane or 3D structure is assumed. If nonzero, an axisymmetric
            structure is assumed. Use any large number (or -1) for an axisymmetric straight section.

        kbr : int or str
            Through-thickness bending stresses key for an axisymmetric analysis ( ``RHO`` ≠ 0):

            * ``0`` - Include the thickness-direction bending stresses.

            * ``1`` - Ignore the thickness-direction bending stresses.

            * ``2`` - Include the thickness-direction bending stress using the same formula as the Y (axial
              direction ) bending stress. Also use the same formula for the shear stress.

        kbr3d : int or str
            Through-thickness bending stresses key for 3D geometry ( ``RHO`` = 0):

            * ``0`` - Include the thickness-direction bending stresses.

            * ``1`` - Ignore the following thickness-direction bending stresses: SX, SXY, SXZ

        Notes
        -----

        .. _PRSECT_notes:

        You may want to linearize the stresses through a section and separate them into categories for
        various code calculations. :ref:`prsect` calculates and reports linearized stresses along a section
        path. The linearized stresses are also separated into membrane, bending, membrane plus bending,
        peak, and total stress categories.

        Define your section path ( :ref:`path` and :ref:`ppath` with the NODE option). Your path must lie
        entirely within the selected set of elements (that is, no element gaps may exist along the path).
        :ref:`path` and :ref:`ppath` only retrieve the two end nodes; the path data is not retained. The
        section path is defined by the two end nodes, and by 47 intermediate points that are automatically
        determined by linear interpolation in the active display coordinate system ( :ref:`dsys` ). The
        number and location of the intermediate points are not affected by the number of divisions set by
        :ref:`path`,, ``nDiv``.

        Your linearized component stress values are obtained by interpolating each element``s average corner
        nodal values along the section path points within each path element. :ref:`prsect` reports the
        linearized component and principal stresses for each stress category at the beginning, mid-length,
        and end of the section path. :ref:`prpath` can be used to report the total stresses at the
        intermediate points.

        Section paths can be through any set of solid (2D plane, 2D axisymmetric or 3D) elements; however,
        section paths are usually defined to be through the thickness of the structure and normal to the
        inner and outer structure surfaces. Section paths (in-plane only) can also be defined for shell
        element structures.

        If the ``RHO`` option is set to indicate the axisymmetric option (non-zero), :ref:`prsect` reports
        the linearized stresses in the section coordinates (SX - along the path, SY - normal to the path,
        and SZ - hoop direction). If the ``RHO`` option is set to indicate the 2D planar or 3D option (zero
        or blank), :ref:`prsect` reports the linearized stresses in the active results coordinate system (
        :ref:`rsys` ]. If the ``RHO`` option is zero or blank and either :ref:`rsys`, SOLU or :ref:`rsys`,
        -1 are active, the linearized stresses are calculated and reported in the global Cartesian
        coordinate system.

        Linearized stress calculations should be performed in a rectangular coordinate system. Principal
        stresses are recalculated from the component stresses and are invariant with the coordinate system
        as long as SX is in the same direction at all points along the defined path. The :ref:`plsect`
        command displays the linearized stresses in the same coordinate system as reported by :ref:`prsect`.

        Stress components through the section are linearized by a line integral method and separated into
        constant membrane stresses, bending stresses varying linearly between end points, and peak stresses
        (defined as the difference between the actual (total) stress and the membrane plus bending
        combination).

        For nonaxisymmetric structures, the bending stresses are calculated such that the neutral axis is at
        the midpoint of the path. Axisymmetric results include the effects of both the radius of revolution
        (automatically determined from the node locations) and the in-plane average radius of curvature of
        the section surfaces (user input).

        For axisymmetric cases, Mechanical APDL calculates the linearized bending stress in the through-
        thickness
        direction as the difference between the total outer fiber stress and the membrane stress if ``KBR``
        = 0. The calculation method may be conservative for locations with a highly nonlinear variation of
        stress in the through-thickness direction. Alternatively, you can specify ``KBR`` = 2 to calculate
        the bending stress using the same method and formula as the Y (axial direction) bending stress. For
        more information, see the discussion of `axisymmetric cases
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post4.html#eqa0e44427-d764-4797-9c99-13f056f2227c>`_
        (specifically ) in the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_.

        In analyses of 3D models with ``RHO`` = 0, ignoring the calculated out-of-plane bending stresses is
        recommended in some scenarios when determining the linearized bending stresses. If ``KBR3D`` = 0,
        all calculated stresses are included in the linearized bending-stress calculations. If ``KBR3D`` =
        1, these calculated out-of-plane bending stresses are ignored in the linearized bending-stress
        calculations: SX, SXY, SXZ. (The principal bending-stress calculation for S1, S2, S3, SINT, and SEQV
        is performed with these zeroed components.)

        Portions of this command are not supported by PowerGraphics ( :ref:`graphics`,POWER].
        """
        command = f"PRSECT,{rho},{kbr},{kbr3d}"
        return self.run(command, **kwargs)

    def psel(
        self,
        type_: str = "",
        pname1: str = "",
        pname2: str = "",
        pname3: str = "",
        pname4: str = "",
        pname5: str = "",
        pname6: str = "",
        pname7: str = "",
        pname8: str = "",
        pname9: str = "",
        pname10: str = "",
        **kwargs,
    ):
        r"""Selects a path or paths.

        Mechanical APDL Command: `PSEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSEL.html>`_

        Parameters
        ----------
        type_ : str
            Label identifying the type of select:

            * ``S`` - Select a new path.

            * ``R`` - Reselect a path from the current set of paths.

            * ``A`` - Additionally select a path and extend the current set of paths.

            * ``U`` - Unselect a path from the current set of paths.

            * ``ALL`` - Restore the full set of paths.

            * ``NONE`` - Unselect the full set of paths.

            * ``INV`` - Invert the current set of paths (selected becomes unselected and vice versa).

        pname1 : str
            Name of existing path(s).

        pname2 : str
            Name of existing path(s).

        pname3 : str
            Name of existing path(s).

        pname4 : str
            Name of existing path(s).

        pname5 : str
            Name of existing path(s).

        pname6 : str
            Name of existing path(s).

        pname7 : str
            Name of existing path(s).

        pname8 : str
            Name of existing path(s).

        pname9 : str
            Name of existing path(s).

        pname10 : str
            Name of existing path(s).

        Notes
        -----

        .. _PSEL_notes:

        Selects a path or multiple paths, up to ten. Data are flagged as selected and unselected; no data
        are actually deleted from the database. There is no default for this command; you must specify a
        type and pathname.
        """
        command = f"PSEL,{type_},{pname1},{pname2},{pname3},{pname4},{pname5},{pname6},{pname7},{pname8},{pname9},{pname10}"
        return self.run(command, **kwargs)

    def pvect(
        self,
        oper: str = "",
        labxr: str = "",
        labyr: str = "",
        labzr: str = "",
        **kwargs,
    ):
        r"""Interpolates a set of items onto a path.

        Mechanical APDL Command: `PVECT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PVECT.html>`_

        Parameters
        ----------
        oper : str
            Valid operations for geometry operations along a path are:

            * ``NORM`` - Defines a unit normal vector at each interpolation point in the direction of the cross
              product of the tangent to the path and the active Z axis. Resulting vector components are in the
              active coordinate system (which must be Cartesian).

            * ``TANG`` - Defines a unit vector tangent to the path at each interpolation point. Vector
              components are in the active coordinate system (which must be Cartesian).

            * ``RADI`` - Defines the position vector of each interpolation point of the path from the center of
              the active coordinate system (which must be Cartesian).

        labxr : str
            Label (8 characters maximum) assigned to X-component of the resulting vector.

        labyr : str
            Label (8 characters maximum) assigned to Y-component of the resulting vector.

        labzr : str
            Label (8 characters maximum) assigned to Z-component of the resulting vector.

        Notes
        -----

        .. _PVECT_notes:

        Defines and interpolates a set of labeled path items along predefined path ( :ref:`path` ) and
        performs various geometric operations on these path items. A path item must be defined before it can
        be used with other path operations. Additional path items may be defined with the :ref:`pdef`,
        :ref:`pcalc`, :ref:`pdot`, and :ref:`pcross` commands. Path items may be listed or displayed with
        the :ref:`plpath`, :ref:`plpagm` and :ref:`prpath` commands. Path geometry items (XG, YG, ZG, S) are
        automatically interpolated (in the active CSYS) if not done so previously with the :ref:`pdef`
        command.
        """
        command = f"PVECT,{oper},{labxr},{labyr},{labzr}"
        return self.run(command, **kwargs)
