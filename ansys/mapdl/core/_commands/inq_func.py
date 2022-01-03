"""Inquire undocumented functions"""

class inq_function:

    def ndinqr(self, node, key, pname='__tmpvar__', **kwargs):
        """Get information about a node.

        **Secondary Functions:**
        Set current node pointer to this node.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        node  :  (int,  sc,  in)
            node number.
            It should be 0 for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and
            ``DB_MAXRECLENG``.

        key  :  (int,  sc,  in)
            key as to information needed about the node.

            * = DB_SELECTED    - return select status:

              * =  0 - node is undefined.
              * = -1 - node is unselected.
              * =  1 - node is selected.

            * = ``DB_NUMDEFINED``  - return number of defined nodes
            * = ``DB_NUMSELECTED`` - return number of selected nodes
            * = ``DB_MAXDEFINED``  - return highest node number defined
            * = ``DB_MAXRECLENG``  - return maximum record length (dp words)
            * =   2, return length (dp words)
            * =   3,
            * =   4, pointer to first data word
            * =  11, return void percent (integer)
            * =  17, pointer to start of index
            * = 117, return the maximum number of DP contact data stored for any node
            * =  -1,
            * =  -2, superelement flag
            * =  -3, master dof bit pattern
            * =  -4, active dof bit pattern
            * =  -5, solid model attachment
            * =  -6, pack nodal line parametric value
            * =  -7, constraint bit pattern
            * =  -8, force bit pattern
            * =  -9, body force bit pattern
            * = -10, internal node flag
            * = -11, orientation node flag =1 is =0 is not
            * = -11, contact node flag <0
            * = -12, constraint bit pattern (for ``DSYM``)
            * = -13, if dof constraint written to file.k (for ``LSDYNA`` only)
            * = -14, nodal coordinate system number (set by ``NROTATE``)
            * =-101, pointer to node data record
            * =-102, pointer to angle record
            * =-103,
            * =-104, pointer to attached couplings
            * =-105, pointer to attacted constraint equations
            * =-106, pointer to nodal stresses
            * =-107, pointer to specified disp'S
            * =-108, pointer to specified forces
            * =-109, pointer to x/y/z record
            * =-110,
            * =-111,
            * =-112, pointer to nodal temperatures
            * =-113, pointer to nodal heat generations
            * =-114,
            * =-115, pointer to calculated displacements
            * =-116

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        ndinqr  (int,  func,  out)
            The returned value of ``ndinqr`` is based on setting of key.
        """
        return self.run(f"{pname} = ndinqr({node}, {key})", **kwargs)

    def elmiqr(self, ielem, key, pname='__tmpvar__', **kwargs):
        """Get information about an element.

        **Secondary Functions:**
        Set current element pointer to this element.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        ielem  :  (int,  sc,  in)
            Element number.
            It should be zero for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, ``DB_MAXRECLENG``,
            or 199

        key  :  (int,  sc,  in)
            information flag.

            * = DB_SELECTED    - return select status:                (1)

              * = 0 - element is undefined.
              * =-1 - element is unselected.
              * = 1 - element is selected.

            * = ``DB_NUMDEFINED``  - return number of defined elements    (12)
            * = ``DB_NUMSELECTED`` - return number of selected elements   (13)
            * = ``DB_MAXDEFINED``  - return maximum element number used   (14)
            * = ``DB_MAXRECLENG``  - return maximum record length         (15)
            * = 2 - return length (int words)
            * = 3 - return layer number (for cross reference files return number of entities)
            * = 4 - return address of first data word
            * = 5 - return length (in record type units)
            * = 6 - return compressed record number.
            * = 11 - return void percent (integer)
            * = 16 - return location of next record (this increments the next record count)
            * = 17 - pointer to start of index
            * = 18 - return type of file.

              * = 0 - integer
              * = 1 - double precision
              * = 2 - real
              * = 3 - complex
              * = 4 - character\*8
              * = 7 - index

            * = 19 - return virtual type of file.

              * = 0 - fixed length (4.4 form)
              * = 1 - indexed variable length (layer data)
              * = 2 - xref data tables
              * = 3 - bitmap data (for 32 data item packed records)
              * = 4 - data tables (three dimensional arrays)

            * = 111 - return the maximum number of nodes stored for any element
            * = 123 - return the maximum number of DP contact data stored for any element
            * = -1 - material number           ( = -EL_MAT)
            * = -2 - element type              ( = -EL_TYPE)
            * = -3 - real constant number      ( = -EL_REAL)
            * = -4 - element section ID number ( = -EL_SECT)
            * = -5 - coordinate system number  ( = -EL_CSYS)
            * =-101 - pointer to element integers etc.

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        elmiqr  (int,  sc,  out)
            The returned value of ``elmiqr`` is based on setting of key.
        """
        return self.run(f"{pname} = elmiqr({ielem}, {key})", **kwargs)

    def kpinqr(self, knmi, key, pname='__tmpvar__', **kwargs):
        """Get information about a keypoints.

        **Secondary Functions:**
        Set current keypoints pointer to this keypoints.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        knmi  :  (int,  sc,  in)
            Keypoints for inquire. may be 0 for key=11 thru 15.

        key  :  (int,  sc,  in)
            Information flag.

            * = 1 - return select

              * = -1 - unselected
              * =  0 - undefined
              * =  1 - selected

            * = 2 - return length (data units)
            * = 3 - return layer number
              (for cross reference files return
              number of entities)
            * = 4 - return address of first data word
            * = 5 - return length (in record type units)
            * = 6 - return compressed record number.
            * = 11 - return void percent (integer)
            * = 12 - return number of defined
            * = 13 - return number of selected
            * = 14 - return highest number defined
            * = 15 - return maximum record length
              (data units)
            * = 16 - return location of next record
              (this increments the next
              record count)
            * = 18 - return type of file.

              * = 0 - integer
              * = 1 - double precision
              * = 2 - real
              * = 3 - complex
              * = 4 - character\*8
              * = 7 - index

            * = 19 - return virtual type of file.

              * = 0 - fixed length (4.4 form)
              * = 1 - indexed variable length
                (layer data)
              * = 2 - xref data tables
              * = 3 - bitmap data (for 32 data
                item packed records)
              * = 4 - data tables (three
                dimensional arrays)

            * = -1, material number
            * = -2, type
            * = -3, real number
            * = -4, node number, if meshed
            * = -5, pointer to attached point
            * = -6, esys number
            * = -7, element number, if meshed
            * = -8, Hardpoint stuff
            * = -9, area number associated with hardpoint
            * = -10, line number associated with hardpoint
            * = -11, Orientation kp flag
            * = -12, local integer workspace
            * = -101, pointer to keypoint data
            * = -102, pointer to keypoint fluences
            * = -103, pointer to keypoint moisture content
            * = -104, pointer to keypoint voltage
            * = -105, pointer to keypoint current density
            * = -106, pointer to keypoint heat generations
            * = -107, pointer to keypoint virtual displacements
            * = -108, pointer to parameter data
            * = -109, pointer to keypoint temperatures
            * = -110, pointer to keypoint displacements
            * = -111, pointer to keypoint forces
            * = -112, pointer to line list

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        kpinqr  (int, sc, out)
            For key=1

            * 0 = ``knmi`` is undefined.
            * -1 = ``knmi`` is unselected.
            * 1 = ``knmi`` is selected.

            For key not equal to 1 returned data is based
            on setting of key.
        """
        return self.run(f"{pname} = kpinqr({knmi}, {key})", **kwargs)

    def lsinqr(self, line, key, pname='__tmpvar__', **kwargs):
        """Get information about a line segment.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        lnmi  :  (int, sc, in)
            Line segment for inquire. It should be 0 for key=11 thru 15.

        key  :  (dp, sc, in)
            key as to information needed about the ``lnmi``.

            * =  1, return select
            * =  2, return length (data units)
            * =  3,
            * = 11, return void percent (integer)
            * = 12  return number of defined
            * = 13, return number of selected
            * = 14, return highest number defined
            * = 15, return maximum record length
              (data units)
            * = 16, return location of next record
              (this increments the next
              record count)
            * = 17, return next record from offset
            * = -1, material number
            * = -2, type
            * = -3, real number
            * = -4, number of nodes
            * = -5, esys number
            * = -6, number of elements
            * = -7, pointer to line in foreign db
            * = -8, # of elem divs in existing mesh
            * = -9, keypoint 1
            * = -10, keypoint 2
            * = -11, color,translucency packed
            * = -12, local integer workspace
              (used in delete with sweeps)
            * = -13, orientation kpa
            * = -14, orientation kpb
            * = -15, section id
            * = -16, # of elem divs for next mesh
            * = -17, 0=hard / 1=soft NDIV
            * = -18, 0=hard / 1=soft SPACE
            * =-101, pointer to line segment data
            * =-102,
            * =-103,
            * =-104,
            * =-105, pointer to node list
            * =-106,
            * =-107, pointer to element list
            * =-108, pointer to parameter data
            * =-109,
            * =-110, pointer to line convections
            * =-111, pointer to line constraints
            * =-112,
            * =-113,
            * =-114, pointer to area list
            * =-115, pointer to sub-line list
            * =-116, pointer to line pressures

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        lsinqr  (int, sc, out)
            For key=1

            * 0 = ``lnmi`` is undefined.
            * -1 = ``lnmi`` is unselected.
            * 1 = ``lnmi`` is selected.

            For key not equal to 1 returned data is based
            on setting of key.

        """
        return self.run(f"{pname} = lsinqr({line}, {key})", **kwargs)

    def arinqr(self, anmi, key, pname='__tmpvar__', **kwargs):
        """Get information about a area.

        **Secondary Functions:**
        Set current area pointer to this area.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        anmi  :  (int, sc, in)
            Area for inquire. may be 0 for key=11 thru 15.

        key  :  (dp, sc, in)
            Key as to information needed about the ``anmi``.

            * =  1, return select
            * =  2, return length (data units)
            * =  3,
            * = 11, return void percent (integer)
            * = 12  return number of defined
            * = 13, return number of selected
            * = 14, return highest number defined
            * = 15, return maximum record length
              (data units)
            * = 16, return next record
              (this increments the next record count)
            * = -1, material
            * = -2, type.
            * = -3, real.
            * = -4, number of nodes.
            * = -5,
            * = -6, number of elements.
            * = -7, pointer to area in foreign db
            * = -8, element shape.
            * = -9, mid-node element key.
            * = -10, element coordinate system.
            * = -11, area constraint information.
            * = 0 - no constraint on this area.
            * = 1 - symmetry constraint.
            * = 2 - anti-symmetry
            * = 3 - both symmetry and anti-symmetry
            * = -12, local integer workspace
            * = -13,
            * = -14,
            * = -15, section
            * = -16, color and translucency packed.
            * = -101, pointer to area data
            * = -102,
            * = -103,
            * = -104,
            * = -105, pointer to node list.
            * = -106, pointer to parameter data
            * = -107, pointer to element list.
            * = -108,
            * = -109,
            * = -110,
            * = -111,
            * = -112, pointer to line loop list
            * = -113, pointer to volume xref
            * = -114, pointer to sub-area list
            * = -115, pointer to area presaraes
            * = -116, pointer to area convections

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        arinqr  (int, sc, out)
            For key=1

            * 0 = ``anmi`` is undefined.
            * -1 = ``anmi`` is unselected.
            * 1 = ``anmi`` is selected.

            For key ne 1 returned data is based
            on setting of key.
        """
        return self.run(f"{pname} = arinqr({anmi}, {key})", **kwargs)

    def vlinqr(self, vnmi, key, pname='__tmpvar__', **kwargs):
        """Get information about a volume.

        **Secondary Functions:**
        Set current volume pointer to this volume.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        vnmi  :  (int, sc, in)
            Volume for inquire. may be 0 for key=11 thru 15.

        key  :  (dp, sc, in)
            Key as to information needed about the ``vnmi``.

            * =  1, return select
            * =  2, return length (data units)
            * =  3,
            * = 11, return void percent (integer)
            * = 12  return number of defined
            * = 13, return number of selected
            * = 14, return highest number defined
            * = 15, return maximum record length (data units)
            * = 16, return next record
            * = -1, material
            * = -2, type.
            * = -3, real.
            * = -4, number of nodes.
            * = -5, KZ1 - 1st kpt for elem Z
            * = -6, number of elements.
            * = -7, pointer to volume in foreign db
            * = -8, element shape.
            * = -9, (section id)\*10 + 2
            * = -10, element coordinate system.
            * = -11, KZ2 - 2nd kpt for elem Z
            * = -12, color and translucancy packed
            * = -101, pointer volume data file.
            * = -102,
            * = -103,
            * = -104,
            * = -105, pointer to node list.
            * = -106, pointer to volume pvolmeter dat
            * = -107, pointer to element list.
            * = -108,
            * = -109,
            * = -110, pointer to sub-volume list
            * = -111,
            * = -112, pointer to area shell list

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        vlinqr  (int, sc, out)
            For key=1

            * 0 = ``vnmi`` is undefined.
            * -1 = ``vnmi`` is unselected.
            * 1 = ``vnmi`` is selected.

            For key ne 1 returned data is based
            on setting of key.
        """
        return self.run(f"{pname} = vlinqr({vnmi}, {key})", **kwargs)

    def rlinqr(self, nreal, key, pname='__tmpvar__', **kwargs):
        """Get information about a real constant set.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        variable  :  (typ, siz, intent)
            description

        nreal  :  (int, sc, in)
            Real constant table number
            should be 0 for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and
            ``DB_MAXRECLENG``.

        key  :  (int, sc, in)
            Information flag.

            * = 5 - return number of values stored for nreal.
              Return the REAL set width (number of fields)
            * = ``DB_SELECTED``    - return select status

              * = 0 - real constant table is undefined.
              * =-1 - real constant table is unselected.
              * = 1 - real constant table is selected

            * = ``DB_NUMDEFINED``  - return number of defined real constant tables
            * = ``DB_NUMSELECTED`` - return number of selected real constant tables
            * = ``DB_MAXDEFINED``  - return highest real constant table defined
            * = ``DB_MAXRECLENG``  - return maximum record length (dp words)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        rlinqr  (int, func, out)
            The returned value of ``rlinqr`` is based on setting of key.

        """
        return self.run(f"{pname} = rlinqr({nreal}, {key})", **kwargs)

    def gapiqr(self, ngap, key, pname='__tmpvar__', **kwargs):
        """Get information about a dynamic gap set.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        ngap  :  (int, sc, in)
            gap number for inquire (must be zero for now).

        key  :  (int, sc, in)
            key as to the information needed

            * =  1, return select
            * =  2, return length (data units)
            * =  3,
            * = 11, return void percent (integer)
            * = 12  return number of defined
            * = 13, return number of selected
            * = 14, return highest number defined
            * = 15, return maximum record length (data units)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        gapiqr  (int, sc, out)
            Returned data is based on setting of key.
        """
        return self.run(f"{pname} = gapiqr({ngap}, {key})", **kwargs)

    def masiqr(self, node, key, pname='__tmpvar__', **kwargs):
        """Get information about masters.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        variable  :  (typ, siz, intent)
            Description

        node  :  (int, sc, in)
            Node number for inquire (must be zero for now).

        key  :  (int, sc, in)
            Key as to the information needed

            * =  1, return select
            * =  2, return length (data units)
            * =  3,
            * = 11, return void percent (integer)
            * = 12  return number of defined
            * = 13, return number of selected
            * = 14, return highest number defined
            * = 15, return maximum record length (data units)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        variable  (typ, siz, intent)
            Description

        masiqr  (int, sc, out)
            Returned data is based on setting of key.
        """
        return self.run(f"{pname} = masiqr({node}, {key})", **kwargs)

    def ceinqr(self, nce, key, pname='__tmpvar__', **kwargs):
        """Get information about a constraint equation set

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        nce  :  (int, sc, in)
            Constraint equation number
        key  :  (int, sc, in)
            Inquiry key.
            It should be zero for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and
            ``DB_MAXRECLENG``

            * = DB_SELECTED    - return select status

              * = 1 - equation is selected
              * = 0 - equation is undefined
              * =-1 - equation is unselected

            * = ``DB_NUMDEFINED``  - return number of defined contraint equations
            * = ``DB_NUMSELECTED`` - return number of selected contraint equations
            * = ``DB_MAXDEFINED``  - return number of highest numbered constraint
              equation defined
            * = ``DB_MAXRECLENG``  - return length of longest contraint equation set
              (max record length)
            * =  2             - return length (data units)
            * =  3             - return layer number
            * =  4             - address of first data word
            * =  5             - return number of values stored for nce
            * = 11             - return void percent (integer)
            * = 16             - return location of next record
            * = ``CE_NONLINEAR``   - return 1 if CE is nonlinear
            * = ``CE_ELEMNUMBER``  - return associated element number

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        ceinqr  (int, func, out)
            The returned value of ``ceinqr`` is based on setting of key
        """
        return self.run(f"{pname} = ceinqr({nce}, {key})", **kwargs)

    def cpinqr(self, ncp, key, pname='__tmpvar__', **kwargs):
        """Get information about a coupled set.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        variable  :  (typ, siz, intent)
            Description

        ncp  :  (int, sc, in)
            Coupled set number

        key  :  (int, sc, in)
            Inquiry key. It should be zero for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and ``DB_MAXRECLENG``

            * = DB_SELECTED    - return select status

              * = 1 - coupled set is selected
              * = 0 - coupled set in undefined
              * =-1 - coupled set in unselected

            * = ``DB_NUMDEFINED``  - return number of defined coupled sets
            * = ``DB_NUMSELECTED`` - return number of selected coupled sets
            * = ``DB_MAXDEFINED``  - return the number of the highest numbered
              coupled set
            * = ``DB_MAXRECLENG``  - return length of largest coupled set record
              (max record length)
            * =  2  - return length (data units)
            * =  3  - return layer number
            * =  4  - return address of first data word
            * =  5  - return number of values stored for ncp
            * = 11  - return void percent (integer)
            * = 16  - return location of next record
            * = -1  - return master node for this eqn (this is
              currently only used by solution DB object)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        cpinqr  (int, func, out)
            The returned value of ``cpinqr`` is based on setting of key.

        """
        return self.run(f"{pname} = cpinqr({ncp}, {key})", **kwargs)

    def csyiqr(self, ncsy, key, pname='__tmpvar__', **kwargs):
        """Get information about a coordinate system

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        ncsy  :  (int, sc, in)
            Coordinate system reference number
            should be zero for key= ``DB_NUMDEFINED``
            or ``DB_MAXDEFINED``

        key  :  (int, sc, in)
            Information flag.

            * = ``DB_SELECTED``    - return status:

              * = 0 - coordinate system is not defined
              * = -1 - coordinate system is not selected
              * = 1 - coordinate system is selected

            * = ``DB_NUMDEFINED``  - number of defined coordinate systems
            * = ``DB_MAXDEFINED``  - maximum coordinate system reference
              number used.

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        csyiqr  (int, func, out)
            The returned value of ``csyiqr`` is based on setting of key.
        """
        return self.run(f"{pname} = csyiqr({ncsy}, {key})", **kwargs)

    def etyiqr(self, itype, key, pname='__tmpvar__', **kwargs):
        """Get information about an element type.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        itype  :  (int, sc, in)
            Element type number.
            It should be 0 for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and
            ``DB_MAXRECLENG``

        key  :  (int, sc, in)
            Information flag.

            * = DB_SELECTED    - return select status:

              * = 0 - element type is undefined.
              * =-1 - element type is unselected.
              * = 1 - element type is selected.

            * = ``DB_NUMDEFINED``  - return number of defined element types
            * = ``DB_NUMSELECTED`` - return number of selected element types
            * = ``DB_MAXDEFINED``  - return highest element type number defined
            * = ``DB_MAXRECLENG``  - return maximum record length (int words)
            * = -n, return element characteristic n from ``etycom`` for element
              type itype.
              ``n`` is correlated to the parameter names in ``echprm``.
              see ``elccmt`` for definitions of element characteristics.

              .. note:: This will not overwrite the current setting of ``etycom``.

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        etyiqr  (int, func, out)
            The returned value of ``etyiqr`` is based on setting of key.
        """
        return self.run(f"{pname} = etyiqr({itype}, {key})", **kwargs)

    def foriqr(self, node, key, pname='__tmpvar__', **kwargs):
        """Get information about nodal loads.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        node  :  (int, sc, in)
            Number of node being inquired about.
            should be 0 for key=``DB_MAXDEFINED`` or
            ``DB_NUMDEFINED``.

        key  :  (dp, sc, in)
            Key as to information needed

            * = 1              - return force mask for node
            * = ``DB_MAXDEFINED``, - return number of nodal loadings in model.
            * = ``DB_NUMDEFINED``.  - return number of nodal loadings in model.

            .. note:: Both ``DB_MAXDEFINED`` and ``DB_NUMDEFINED``, produce the same functionality.

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        foriqr  (int, func, out)
            The returned value of ``foriqr`` is based on setting of key.
        """
        return self.run(f"{pname} = foriqr({node}, {key})", **kwargs)

    def sectinqr(self, nsect, key, pname='__tmpvar__', **kwargs):
        """Get information about a section property.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        nsect
            Section id table number, it should be 0 for key = 12, 13, 14.

        key - information flag
            * = 1, select status
            * = 12, return number of defined section id tables
            * = 13, return number of selected section id tables
            * = 14, return highest section id table defined

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        sectinqr
            for key = 1
            * = 0, section id table is undefined.
            * = -1, section id table is unselected.
            * = 1, section id table is selected
        """
        return self.run(f"{pname} = sectinqr({nsect}, {key})", **kwargs)

    def mpinqr(self, mat,  iprop,  key, pname='__tmpvar__', **kwargs):
        """Get information about a material property.

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        mat  :  (int, sc, in)
            Material number
            should be 0 for key=11, ``DB_NUMDEFINED(12)``,
            ``DB_MAXDEFINED(14)``, and ``DB_MAXRECLENG(15)``.

        iprop  :  (int, sc, in)
            Property reference number (See notes).

            If iprop = 0, test for existence of any material property with this
            material number (with key = DB_SELECTED(1)).

            .. seealso:: **MP command labels**

                EX  = 1, EY  = 2, EZ  = 3, NUXY= 4, NUYZ= 5, NUXZ= 6, GXY = 7, GYZ = 8

                GXZ = 9, ALPX=10, ALPY=11, ALPZ=12, DENS=13, MU  =14, DAMP=15, KXX =16

                KYY =17, KZZ =18, RSVX=19, RSVY=20, RSVZ=21,     =22, HF  =23, VISC=24

                EMIS=25, ENTH=26, LSST=27, PRXY=28, PRYZ=29, PRXZ=30, MURX=31, MURY=32

                MURZ=33, PERX=34, PERY=35, PERZ=36, MGXX=37, MGYY=38, MGZZ=39, EGXX=40

                EGYY=41, EGZZ=42, SBKX=43, SBKY=44, SBKZ=45, SONC=46, DMPS=47, ELIM=48

                USR1=49, USR2=50, USR3=51, USR4=51, FLUI=53, ORTH=54, CABL=55, RIGI=56

                HGLS=57, BVIS=58, QRAT=59, REFT=60, CTEX=61, CTEY=62, CTEZ=63, THSX=64,

                THSY=65, THSZ=66, DMPR=67, LSSM=68, BETD=69, ALPD=70, RH  =71, DXX =72,

                DYY =73, DZZ =74, BETX=75, BETY=76, BETZ=77, CSAT=78, CREF=79, CVH =80,

                UMID=81, UVID=82


                (see ``TB`` command for more information)

        key  :  (int, sc, in)
            Key as to the information needed about material property.

            * = ``DB_SELECTED(1)``- return select status:

              * = 0 - material prop is undefined.
              * = 1 - material prop is selected.

            * = ``DB_NUMDEFINED(12)`` - number of defined material properties
            * = ``DB_MAXDEFINED(14)`` - highest material property number defined
            * = ``DB_MAXRECLENG(15)`` - maximum record length (dp words)
            * =  2 - return length (dp words)
            * =  3 - return number of temp. values
            * = 11 - return void percent (integer)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        mpinqr   (int, func, out)
            Returned value of ``mpinqr`` is based on setting of key.

        """
        return self.run(f"{pname} = mpinqr({mat,  iprop}, { key})", **kwargs)

    def dget(self, node,  idf,  kcmplx, pname='__tmpvar__', **kwargs):
        """Get a constraint from the data bsae

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        node  :  (int, sc, in)
            Node number

        idf  :  (int, sc, in)
            Pointer to the dof (1-32)

            * 1 = ux,
            * 2 = uy
            * 3 = uz
            * 4 = rotx
            * 5 = roty
            * 6 = rotz
            * 7 = ax
            * 8 = ay
            * 9 = az
            * 10 = vx
            * 11 = vy
            * 12 = vz
            * 13-18 = spares
            * 19 = pres
            * 20 = temp
            * 21 = volt
            * 22 = mag
            * 23 = enke
            * 24 = ends
            * 25 = emf
            * 26 = curr
            * 27-32 = SP01-SP06

        kcmplx  :  (int, sc, in)

            * 0 = real
            * 1 = imaginary

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        dget   (dp, sc, out)
            Constraint value (High number if undefined)
        """
        return self.run(f"{pname} = dget({node}, {idf}, {kcmplx})", **kwargs)

    def fget(self, node,  idf,  kcmplx, pname='__tmpvar__', **kwargs):
        """Get a force from the data bsae

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        node  :  (int, sc, in)
            Node number

        idf  :  (int, sc, in)
            Pointer to the dof (1-32)

            * 1 = ux
            * 2 = uy
            * 3 = uz
            * 4 = rotx
            * 5 = roty
            * 6 = rotz
            * 7 = ax
            * 8 = ay
            * 9 = az
            * 10 = vx
            * 11 = vy
            * 12 = vz
            * 13-18 = spares
            * 19 = pres
            * 20 = temp
            * 21 = volt
            * 22 = mag
            * 23 = enke
            * 24 = ends
            * 25 = emf
            * 26 = curr
            * 27-32 = spares

        kcmplx  :  (int, sc, in)

            * 0 = real
            * 1 = imaginary

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        fget  (dp, sc, out)
            Force value (High number if undefined)
        """
        return self.run(f"{pname} = fget({node},  {idf}, {kcmplx})", **kwargs)

    def erinqr(self, key, pname='__tmpvar__', **kwargs):
        """Obtain information from errors common

        .. warning:: **DISCLAIMER**: This function is un-documented in the official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encoraged.

                   **Please use it with caution.**

        Parameters
        ----------
        key  :  (int, sc, in)
            Item to be returned.

            * 1 = keyerr (ER_ERRORFLAG)
              Master error flag.
            * 2 = errfil (ER_ERRORFILE)
              Errors file unit number.
            * 3 = numnot (ER_NUMNOTE)
              Total number of notes displayed.
            * 4 = numwrn (ER_NUMWARNING)
              Total number of warnings displayed.
            * 5 = numerr (ER_NUMERROR)
              Total number of errors displayed.
            * 6 = numfat (ER_NUMFATAL)
              Total number of fatals displayed.
            * 7 = maxmsg (ER_MAXMESSAGE)
              Max allowed number of displayed messages before abort.
            * 8 = lvlerr (ER_ERRORLEVEL)
              Used basicly in solution (from ``cnvr`` command.)

              * -1 = do not set keyerr for notes/errors/warnings.
              * -2 = same as -1 but do not display message either.

            * 9 = mxpcmd (ER_MAXCOMMAND)
              Maximum number of messages allowed per command.
            * 10 = nercmd (ER_NUMCOMMAND)
              Number of messages displayed for any one command.
            * 11 = nertim (ER_UICLEAR)
              Key as to how message cleared from u/i pop-up (only for "info" calls)

              * -1 = message is timed before removal
              * 0 = message needs pick or keyboard before removal
              * 1 = message stays up untill replaced by another message

            * 12 = nomore  (ER_NOMOREMSG)
              Display no more messages

              * 0 = display messages
              * 1 = display discontinue message and stop displaying

            * 13 = eropen   (ER_FILEOPEN)

              * 0 = errors file is closed
              * 1 = errors file is opened

            * 14 = ikserr (ER_INTERERROR)

              * 0 = if interactive do not set keyerr.
              * -1 = if interactive set keyerr (used by mesher and tessalation)

            * 15 = kystat (ER_KEYOPTTEST)
              Flag to bypass keyopt tests in the elcxx routines associated with status/panel info inquiries.

              * 0 = do not bypass keyopt tests
              * 1 = perform all keyopt tests also flag to bypass setting of _STATUS upon resume

            * 16 = mxr4r5   (ER_MIXEDREV)
              mixed rev4-rev5 input logic (\*do,\*if, \*go, \*if-go)

              * 1 = rev5 found (\*do,\*fi-then-\*endif)
              * 2 = rev4 found (\*go,:xxx,\*if, ...., :xxx)
              * 3 = warning printed. do not issue any more.

            * 17 = mshkey    (ER_MESHING)
              CPU intensive meshing etc.
              This will cause "nertim (11)" to be set to -1 for "notes", 1 for "warnings",and 0 for "errors".
              Checking of this key is done in "anserr".

              * 0 = not meshing or cpu intensive
              * 1 = yes, meshing or cpu intensive

            * 18 = syerro            (18)
              systop error code. read by anserr if set.
            * 19 = opterr (ER_OPTLOOPING)

              * 0 = no error in main ansys during opt looping
              * 1 = an error has happened in main ansys during opt looping

            * 20 = flowrn            (20)
              Flag used by "floqa" as to list ``floqa.ans``.

              * 0 = list ``floqa.ans``
              * 1 = ``floqa.ans`` has been listed. do not list again.

            * 22 = noreport (22)
              Used in GUI for turning off errors due to strsub calls.

              * 0 = process errors as usual
              * 1 = do NOT report errors

            * 23 = pdserr (ER_PDSLOOPING)

              * 0 = no error in main ansys during pds looping
              * 1 = an error has happened in main ansys during pds looping

            * 24 = mxpcmdw (24)
              Number of messages written to file.err for any command

              * 0 = write all errors to file.err
              * 1 = only write displayed errors to file.err

            * 25 = kystop
              No information is provided.

            * 26 = icloads (26)
              K key to forbid the ``iclist`` command from listing solution data instead of the input data.

              * 0 = ``iclist`` is OK
              * 1 = do not permit ``iclist``

            * 27 = ifkey   error     (27)
              key on whether or not to abort during ``/input`` on error.

              * 0 = do not abort
              * 1 = abort

            * 28 = intrupt  (ER_INTERRUPT)
              Interrupt button, so executable returns no error.

            * spare - spare integer variables

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to ``Mapdl.run``.

        Returns
        -------
        erinqr  (int, sc, out)
            Value corresponding to key.

        """
        return self.run(f"{pname} = erinqr({key})", **kwargs)
