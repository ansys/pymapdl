"""Inquire undocumented functions"""


class inq_function:
    def ndinqr(self, node, key, pname="__tmpvar__", **kwargs):
        """Get information about a node.

        **Secondary Functions:**
        Set current node pointer to this node.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        node : int
            node number.
            It should be 0 for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and
            ``DB_MAXRECLENG``.

        key : int
            key as to information needed about the node.

            * DB_SELECTED - return select status:

              * 0 - node is undefined.
              * -1 - node is unselected.
              * 1 - node is selected.

            * ``DB_NUMDEFINED`` - return number of defined nodes
            * ``DB_NUMSELECTED`` - return number of selected nodes
            * ``DB_MAXDEFINED`` - return highest node number defined
            * ``DB_MAXRECLENG`` - return maximum record length (dp words)
            * 2, return length (dp words)
            * 3,
            * 4, pointer to first data word
            * 11, return void percent (integer)
            * 17, pointer to start of index
            * 117, return the maximum number of DP contact data stored for any node
            * -1,
            * -2, superelement flag
            * -3, master dof bit pattern
            * -4, active dof bit pattern
            * -5, solid model attachment
            * -6, pack nodal line parametric value
            * -7, constraint bit pattern
            * -8, force bit pattern
            * -9, body force bit pattern
            * -10, internal node flag
            * -11, orientation node flag =1 is =0 is not
            * -11, contact node flag <0
            * -12, constraint bit pattern (for ``DSYM``)
            * -13, if dof constraint written to file.k (for ``LSDYNA`` only)
            * -14, nodal coordinate system number (set by ``NROTATE``)
            * -101, pointer to node data record
            * -102, pointer to angle record
            * -103,
            * -104, pointer to attached couplings
            * -105, pointer to attacted constraint equations
            * -106, pointer to nodal stresses
            * -107, pointer to specified disp'S
            * -108, pointer to specified forces
            * -109, pointer to x/y/z record
            * -110,
            * -111,
            * -112, pointer to nodal temperatures
            * -113, pointer to nodal heat generations
            * -114,
            * -115, pointer to calculated displacements
            * -116

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        str, int, or float
            The returned value of ``ndinqr`` is based on setting of key.
        """
        return self.run(f"{pname} = ndinqr({node}, {key})", **kwargs)

    def elmiqr(self, ielem, key, pname="__tmpvar__", **kwargs):
        """Get information about an element.

        **Secondary Functions:**
        Set current element pointer to this element.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        ielem : int
            Element number.
            It should be zero for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, ``DB_MAXRECLENG``,
            or 199

        key : int
            information flag.

            * DB_SELECTED - return select status:  (1)

              * 0 - element is undefined.
              * -1 - element is unselected.
              * 1 - element is selected.

            * ``DB_NUMDEFINED`` - return number of defined elements (12)
            * ``DB_NUMSELECTED`` - return number of selected elements (13)
            * ``DB_MAXDEFINED`` - return maximum element number used (14)
            * ``DB_MAXRECLENG`` - return maximum record length (15)
            * 2 - return length (int words)
            * 3 - return layer number (for cross reference files return number of entities)
            * 4 - return address of first data word
            * 5 - return length (in record type units)
            * 6 - return compressed record number.
            * 11 - return void percent (integer)
            * 16 - return location of next record (this increments the next record count)
            * 17 - pointer to start of index
            * 18 - return type of file.

              * 0 - integer
              * 1 - double precision
              * 2 - real
              * 3 - complex
              * 4 - character\*8
              * 7 - index

            * 19 - return virtual type of file.

              * 0 - fixed length (4.4 form)
              * 1 - indexed variable length (layer data)
              * 2 - xref data tables
              * 3 - bitmap data (for 32 data item packed records)
              * 4 - data tables (three dimensional arrays)

            * 111 - return the maximum number of nodes stored for any element
            * 123 - return the maximum number of DP contact data stored for any element
            * -1 - material number ( ``= -EL_MAT``)
            * -2 - element type ( ``= -EL_TYPE``)
            * -3 - real constant number ( ``= -EL_REAL``)
            * -4 - element section ID number ( ``= -EL_SECT``)
            * -5 - coordinate system number ( ``= -EL_CSYS``)
            * -101 - pointer to element integers etc.

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            The returned value of ``elmiqr`` is based on setting of key.
        """
        return self.run(f"{pname} = elmiqr({ielem}, {key})", **kwargs)

    def kpinqr(self, knmi, key, pname="__tmpvar__", **kwargs):
        """Get information about a keypoints.

        **Secondary Functions:**
        Set current keypoints pointer to this keypoints.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        knmi : int
            Keypoints for inquire. may be 0 for key=11 thru 15.

        key : int
            Information flag.

            * 1 - return select

              * -1 - unselected
              * 0 - undefined
              * 1 - selected

            * 2 - return length (data units)
            * 3 - return layer number
              (for cross reference files return
              number of entities)
            * 4 - return address of first data word
            * 5 - return length (in record type units)
            * 6 - return compressed record number.
            * 11 - return void percent (integer)
            * 12 - return number of defined
            * 13 - return number of selected
            * 14 - return highest number defined
            * 15 - return maximum record length
              (data units)
            * 16 - return location of next record
              (this increments the next
              record count)
            * 18 - return type of file.

              * 0 - integer
              * 1 - double precision
              * 2 - real
              * 3 - complex
              * 4 - character\*8
              * 7 - index

            * 19 - return virtual type of file.

              * 0 - fixed length (4.4 form)
              * 1 - indexed variable length
                (layer data)
              * 2 - xref data tables
              * 3 - bitmap data (for 32 data
                item packed records)
              * 4 - data tables (three
                dimensional arrays)

            * -1, material number
            * -2, type
            * -3, real number
            * -4, node number, if meshed
            * -5, pointer to attached point
            * -6, esys number
            * -7, element number, if meshed
            * -8, Hardpoint stuff
            * -9, area number associated with hardpoint
            * -10, line number associated with hardpoint
            * -11, Orientation kp flag
            * -12, local integer workspace
            * -101, pointer to keypoint data
            * -102, pointer to keypoint fluences
            * -103, pointer to keypoint moisture content
            * -104, pointer to keypoint voltage
            * -105, pointer to keypoint current density
            * -106, pointer to keypoint heat generations
            * -107, pointer to keypoint virtual displacements
            * -108, pointer to parameter data
            * -109, pointer to keypoint temperatures
            * -110, pointer to keypoint displacements
            * -111, pointer to keypoint forces
            * -112, pointer to line list

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            For key=1

            * 0 = ``knmi`` is undefined.
            * -1 = ``knmi`` is unselected.
            * 1 = ``knmi`` is selected.

            For key not equal to 1 returned data is based
            on setting of key.
        """
        return self.run(f"{pname} = kpinqr({knmi}, {key})", **kwargs)

    def lsinqr(self, line, key, pname="__tmpvar__", **kwargs):
        """Get information about a line segment.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        lnmi : int
            Line segment for inquire. It should be 0 for key=11 thru 15.

        key : float
            key as to information needed about the ``lnmi``.

            * 1, return select
            * 2, return length (data units)
            * 3,
            * 11, return void percent (integer)
            * 12, return number of defined
            * 13, return number of selected
            * 14, return highest number defined
            * 15, return maximum record length
              (data units)
            * 16, return location of next record
              (this increments the next
              record count)
            * 17, return next record from offset
            * -1, material number
            * -2, type
            * -3, real number
            * -4, number of nodes
            * -5, esys number
            * -6, number of elements
            * -7, pointer to line in foreign db
            * -8, # of elem divs in existing mesh
            * -9, keypoint 1
            * -10, keypoint 2
            * -11, color,translucency packed
            * -12, local integer workspace
              (used in delete with sweeps)
            * -13, orientation kpa
            * -14, orientation kpb
            * -15, section id
            * -16, # of elem divs for next mesh
            * -17, 0=hard / 1=soft ``NDIV``
            * -18, 0=hard / 1=soft ``SPACE``
            * -101, pointer to line segment data
            * -102,
            * -103,
            * -104,
            * -105, pointer to node list
            * -106,
            * -107, pointer to element list
            * -108, pointer to parameter data
            * -109,
            * -110, pointer to line convections
            * -111, pointer to line constraints
            * -112,
            * -113,
            * -114, pointer to area list
            * -115, pointer to sub-line list
            * -116, pointer to line pressures

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            For key=1

            * 0 = ``lnmi`` is undefined.
            * -1 = ``lnmi`` is unselected.
            * 1 = ``lnmi`` is selected.

            For key not equal to 1 returned data is based
            on setting of key.

        """
        return self.run(f"{pname} = lsinqr({line}, {key})", **kwargs)

    def arinqr(self, anmi, key, pname="__tmpvar__", **kwargs):
        """Get information about a area.

        **Secondary Functions:**
        Set current area pointer to this area.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        anmi : int
            Area for inquire. may be 0 for key=11 thru 15.

        key : float
            Key as to information needed about the ``anmi``.

            * 1, return select
            * 2, return length (data units)
            * 3,
            * 11, return void percent (integer)
            * 12, return number of defined
            * 13, return number of selected
            * 14, return highest number defined
            * 15, return maximum record length
              (data units)
            * 16, return next record
              (this increments the next record count)
            * -1, material
            * -2, type.
            * -3, real.
            * -4, number of nodes.
            * -5,
            * -6, number of elements.
            * -7, pointer to area in foreign db
            * -8, element shape.
            * -9, mid-node element key.
            * -10, element coordinate system.
            * -11, area constraint information.
            * 0 - no constraint on this area.
            * 1 - symmetry constraint.
            * 2 - anti-symmetry
            * 3 - both symmetry and anti-symmetry
            * -12, local integer workspace
            * -13,
            * -14,
            * -15, section
            * -16, color and translucency packed.
            * -101, pointer to area data
            * -102,
            * -103,
            * -104,
            * -105, pointer to node list.
            * -106, pointer to parameter data
            * -107, pointer to element list.
            * -108,
            * -109,
            * -110,
            * -111,
            * -112, pointer to line loop list
            * -113, pointer to volume xref
            * -114, pointer to sub-area list
            * -115, pointer to area presaraes
            * -116, pointer to area convections

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
          For key=1

          * 0 = ``anmi`` is undefined.
          * -1 = ``anmi`` is unselected.
          * 1 = ``anmi`` is selected.

          For key not equal to 1, the returned data is based
          on setting of key.
        """
        return self.run(f"{pname} = arinqr({anmi}, {key})", **kwargs)

    def vlinqr(self, vnmi, key, pname="__tmpvar__", **kwargs):
        """Get information about a volume.

        **Secondary Functions:**
        Set current volume pointer to this volume.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        vnmi : int
            Volume for inquire. may be 0 for key=11 thru 15.

        key : float
            Key as to information needed about the ``vnmi``.

            * 1, return select
            * 2, return length (data units)
            * 3,
            * 11, return void percent (integer)
            * 12, return number of defined
            * 13, return number of selected
            * 14, return highest number defined
            * 15, return maximum record length (data units)
            * 16, return next record
            * -1, material
            * -2, type.
            * -3, real.
            * -4, number of nodes.
            * -5, KZ1 - 1st kpt for elem Z
            * -6, number of elements.
            * -7, pointer to volume in foreign db
            * -8, element shape.
            * -9, (``section id``)\*10 + 2
            * -10, element coordinate system.
            * -11, KZ2 - 2nd kpt for elem Z
            * -12, color and transparency packed
            * -101, pointer volume data file.
            * -102,
            * -103,
            * -104,
            * -105, pointer to node list.
            * -106, pointer to volume pvolmeter dat
            * -107, pointer to element list.
            * -108,
            * -109,
            * -110, pointer to sub-volume list
            * -111,
            * -112, pointer to area shell list

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            For key=1

            * 0 = ``vnmi`` is undefined.
            * -1 = ``vnmi`` is unselected.
            * 1 = ``vnmi`` is selected.

            For key ne 1 returned data is based
            on setting of key.
        """
        return self.run(f"{pname} = vlinqr({vnmi}, {key})", **kwargs)

    def rlinqr(self, nreal, key, pname="__tmpvar__", **kwargs):
        """Get information about a real constant set.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        nreal : int
            Real constant table number
            should be 0 for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and
            ``DB_MAXRECLENG``.

        key : int
            Information flag.

            * 5 - return number of values stored for ``nreal``.
              Return the REAL set width (number of fields)
            * ``DB_SELECTED`` - return select status

              * 0 - real constant table is undefined.
              * -1 - real constant table is unselected.
              * 1 - real constant table is selected

            * ``DB_NUMDEFINED`` - return number of defined real constant tables
            * ``DB_NUMSELECTED`` - return number of selected real constant tables
            * ``DB_MAXDEFINED`` - return highest real constant table defined
            * ``DB_MAXRECLENG`` - return maximum record length (dp words)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            The returned value of ``rlinqr`` is based on setting of key.

        """
        return self.run(f"{pname} = rlinqr({nreal}, {key})", **kwargs)

    def gapiqr(self, ngap, key, pname="__tmpvar__", **kwargs):
        """Get information about a dynamic gap set.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        ngap : int
            gap number for inquire (must be zero for now).

        key : int
            key as to the information needed

            * 1, return select
            * 2, return length (data units)
            * 3,
            * 11, return void percent (integer)
            * 12, return number of defined
            * 13, return number of selected
            * 14, return highest number defined
            * 15, return maximum record length (data units)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            Returned data is based on setting of key.
        """
        return self.run(f"{pname} = gapiqr({ngap}, {key})", **kwargs)

    def masiqr(self, node, key, pname="__tmpvar__", **kwargs):
        """Get information about masters nodes.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        node : int
            Node number for inquire (must be zero for now).

        key : int
            Key as to the information needed

            * 1, return select
            * 2, return length (data units)
            * 3,
            * 11, return void percent (integer)
            * 12, return number of defined
            * 13, return number of selected
            * 14, return highest number defined
            * 15, return maximum record length (data units)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int
            Returned data is based on setting of key.
        """
        return self.run(f"{pname} = masiqr({node}, {key})", **kwargs)

    def ceinqr(self, nce, key, pname="__tmpvar__", **kwargs):
        """Get information about a constraint equation set.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        nce : int
            Constraint equation number

        key : int
            Inquiry key.
            It should be zero for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and
            ``DB_MAXRECLENG``

            * ``DB_SELECTED`` - return select status

              * 1 - equation is selected
              * 0 - equation is undefined
              * -1 - equation is unselected

            * ``DB_NUMDEFINED`` - return number of defined constraint
              equations.
            * ``DB_NUMSELECTED`` - return number of selected constraint
              equations.
            * ``DB_MAXDEFINED`` - return number of highest numbered
              constraint equation defined.
            * ``DB_MAXRECLENG`` - return length of longest constraint
              equation set (max record length)
            * 2 - return length (data units)
            * 3 - return layer number
            * 4 - address of first data word
            * 5 - return number of values stored for nce
            * 11 - return void percent (integer)
            * 16 - return location of next record
            * ``CE_NONLINEAR`` - return 1 if CE is nonlinear
            * ``CE_ELEMNUMBER`` - return associated element number

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            The returned value of ``ceinqr`` is based on setting of key.
        """
        return self.run(f"{pname} = ceinqr({nce}, {key})", **kwargs)

    def cpinqr(self, ncp, key, pname="__tmpvar__", **kwargs):
        """Get information about a coupled set.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        ncp : int
            Coupled set number.

        key : int
            Inquiry key. It should be zero for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and ``DB_MAXRECLENG``

            * ``DB_SELECTED`` - return select status

              * 1 - coupled set is selected
              * 0 - coupled set in undefined
              * -1 - coupled set in unselected

            * ``DB_NUMDEFINED`` - return number of defined coupled sets
            * ``DB_NUMSELECTED`` - return number of selected coupled sets
            * ``DB_MAXDEFINED`` - return the number of the highest numbered
              coupled set
            * ``DB_MAXRECLENG`` - return length of largest coupled set record
              (max record length)
            * 2 - return length (data units)
            * 3 - return layer number
            * 4 - return address of first data word
            * 5 - return number of values stored for ncp
            * 11 - return void percent (integer)
            * 16 - return location of next record
            * \-1 - return master node for this eqn (this is currently only used by solution DB object)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            The returned value of ``cpinqr`` is based on setting of key.

        """
        return self.run(f"{pname} = cpinqr({ncp}, {key})", **kwargs)

    def csyiqr(self, ncsy, key, pname="__tmpvar__", **kwargs):
        """Get information about a coordinate system.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        ncsy : int
            Coordinate system reference number
            should be zero for key= ``DB_NUMDEFINED``
            or ``DB_MAXDEFINED``

        key : int
            Information flag.

            * ``DB_SELECTED`` - return status:

              * 0 - coordinate system is not defined
              * -1 - coordinate system is not selected
              * 1 - coordinate system is selected

            * ``DB_NUMDEFINED`` - number of defined coordinate systems
            * ``DB_MAXDEFINED`` - maximum coordinate system reference
              number used.

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            The returned value of ``csyiqr`` is based on setting of key.
        """
        return self.run(f"{pname} = csyiqr({ncsy}, {key})", **kwargs)

    def etyiqr(self, itype, key, pname="__tmpvar__", **kwargs):
        """Get information about an element type.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        itype : int
            Element type number.
            It should be 0 for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and
            ``DB_MAXRECLENG``

        key : int
            Information flag.

            * ``DB_SELECTED`` - return select status:

              * 0 - element type is undefined.
              * -1 - element type is unselected.
              * 1 - element type is selected.

            * ``DB_NUMDEFINED`` - return number of defined element types
            * ``DB_NUMSELECTED`` - return number of selected element types
            * ``DB_MAXDEFINED`` - return highest element type number defined
            * ``DB_MAXRECLENG`` - return maximum record length (int words)
            * ``-n``- return element characteristic n from ``etycom`` for element
              type itype.
              ``n`` is correlated to the parameter names in ``echprm``.
              see ``elccmt`` for definitions of element characteristics.

              .. note:: This will not overwrite the current setting of
                        ``etycom``.

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            The returned value of ``etyiqr`` is based on setting of key.
        """
        return self.run(f"{pname} = etyiqr({itype}, {key})", **kwargs)

    def foriqr(self, node, key, pname="__tmpvar__", **kwargs):
        """Get information about nodal loads.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        node : int
            Number of node being inquired about.
            should be 0 for key = ``DB_MAXDEFINED`` or
            ``DB_NUMDEFINED``.

        key : float
            Key as to information needed

            * 1 - return force mask for node
            * ``DB_MAXDEFINED`` - return number of nodal loadings in model.
            * ``DB_NUMDEFINED`` - return number of nodal loadings in model.

            .. note:: Both ``DB_MAXDEFINED`` and ``DB_NUMDEFINED``, produce the
                     same functionality.

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            The returned value of ``foriqr`` is based on setting of key.
        """
        return self.run(f"{pname} = foriqr({node}, {key})", **kwargs)

    def sectinqr(self, nsect, key, pname="__tmpvar__", **kwargs):
        """Get information about a section id set.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        nsect : int
            Section id table number
            should be 0 for key=11, ``DB_NUMDEFINED``,
            ``DB_NUMSELECTED``, ``DB_MAXDEFINED``, and
            ``DB_MAXRECLENG``.

        key : int
            Information flag.

            * ``DB_SELECTED`` - return select status

              * 0 - ection id table is undefined.
              * -1 - section id table is unselected.
              * 1 - section id table is selected

            * ``DB_NUMDEFINED`` - return number of defined section id tables
            * ``DB_NUMSELECTED`` - return number of selected section id tables
            * ``DB_MAXDEFINED`` - return highest section id table defined
            * ``DB_MAXRECLENG`` - return maximum record length (dp words)
            * 2 - return length (dp words)
            * 3 - return layer number (for cross reference files return number
              of entities)
            * 4 - return address of first data word
            * 5 - return length (in record type units)
            * 6 - return compressed record number.
            * 11 - return void percent (integer)
            * 16 - return location of next record (this increments the next
              record count)
            * 18 - return type of file.

              * 0 - integer
              * 1 - double precision
              * 2 - real
              * 3 - complex
              * 4 - character*8
              * 7 - index

            * 19 - return virtual type of file.

              * 0 - fixed length (4.4 form)
              * 1 - indexed variable length (layer data)
              * 2 - xref data tables
              * 3 - bitmap data (for 32 data item packed records)
              * 4 - data tables (three dimensional arrays)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            The returned value of sectinqr is based on setting of key.
        """
        return self.run(f"{pname} = sectinqr({nsect}, {key})", **kwargs)

    def mpinqr(self, mat, iprop, key, pname="__tmpvar__", **kwargs):
        """Get information about a material property.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        mat : int
            Material number
            should be 0 for key=11, ``DB_NUMDEFINED(12)``,
            ``DB_MAXDEFINED(14)``, and ``DB_MAXRECLENG(15)``.

        iprop  :  int
            Property reference number (See Table-1_ in the Notes section).

            If iprop = 0, test for existence of any material property with this
            material number (with key = ``DB_SELECTED(1)``).

        key : int
            Key as to the information needed about material property.

            * ``DB_SELECTED(1)`` - return select status:

              * 0 - material prop is undefined.
              * 1 - material prop is selected.

            * ``DB_NUMDEFINED(12)`` - number of defined material properties
            * ``DB_MAXDEFINED(14)`` - highest material property number defined
            * ``DB_MAXRECLENG(15)`` - maximum record length (dp words)
            * 2 - return length (dp words)
            * 3 - return number of temp. values
            * 11 - return void percent (integer)

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            Returned value of ``mpinqr`` is based on setting of key.

        Notes
        -----

        The material properties are obtained from the :meth:`MP <ansys.mapdl.core.Mapdl.mp>` command labels,
        which are detailed below:

        **MP command labels**

        .. _Table-1:

        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | Property | Key | Property | Key | Property | Key | Property | Key | Property | Key | Property | Key |
        +==========+=====+==========+=====+==========+=====+==========+=====+==========+=====+==========+=====+
        | EX       | 1   | DAMP     | 15  | PRYZ     | 29  | SBKX     | 43  | HGLS     | 57  | RH       | 71  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | EY       | 2   | KXX      | 16  | PRXZ     | 30  | SBKY     | 44  | BVIS     | 58  | DXX      | 72  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | EZ       | 3   | KYY      | 17  | MURX     | 31  | SBKZ     | 45  | QRAT     | 59  | DYY      | 73  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | NUXY     | 4   | KZZ      | 18  | MURY     | 32  | SONC     | 46  | REFT     | 60  | DZZ      | 74  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | NUYZ     | 5   | RSVX     | 19  | MURZ     | 33  | DMPS     | 47  | CTEX     | 61  | BETX     | 75  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | NUXZ     | 6   | RSVY     | 20  | PERX     | 34  | ELIM     | 48  | CTEY     | 62  | BETY     | 76  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | GXY      | 7   | RSVZ     | 21  | PERY     | 35  | USR1     | 49  | CTEZ     | 63  | BETZ     | 77  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | GYZ      | 8   |          | 22  | PERZ     | 36  | USR2     | 50  | THSX     | 64  | CSAT     | 78  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | GXZ      | 9   | HF       | 23  | MGXX     | 37  | USR3     | 51  | THSY     | 65  | CREF     | 79  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | ALPX     | 10  | VISC     | 24  | MGYY     | 38  | USR4     | 51  | THSZ     | 66  | CVH      | 80  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | ALPY     | 11  | EMIS     | 25  | MGZZ     | 39  | FLUI     | 53  | DMPR     | 67  | UMID     | 81  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | ALPZ     | 12  | ENTH     | 26  | EGXX     | 40  | ORTH     | 54  | LSSM     | 68  | UVID     | 82  |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | DENS     | 13  | LSST     | 27  | EGYY     | 41  | CABL     | 55  | BETD     | 69  |          |     |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+
        | MU       | 14  | PRXY     | 28  | EGZZ     | 42  | RIGI     | 56  | ALPD     | 70  |          |     |
        +----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+----------+-----+

        see :meth:`TB <ansys.mapdl.core.Mapdl.tb>` command for more information.

        """
        return self.run(f"{pname} = mpinqr({mat}, {iprop}, {key})", **kwargs)

    def dget(self, node, idf, kcmplx, pname="__tmpvar__", **kwargs):
        """Get a constraint from the data base.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        node : int
            Node number

        idf : int
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

        kcmplx : int

            * 0 = real
            * 1 = imaginary

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        float
            Constraint value (High number if undefined)
        """
        return self.run(f"{pname} = dget({node}, {idf}, {kcmplx})", **kwargs)

    def fget(self, node, idf, kcmplx, pname="__tmpvar__", **kwargs):
        """Get a force load from the data base.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        node : int
            Node number

        idf : int
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

        kcmplx : int

            * 0 = real
            * 1 = imaginary

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        float
            Force value (high number if undefined)
        """
        return self.run(f"{pname} = fget({node}, {idf}, {kcmplx})", **kwargs)

    def erinqr(self, key, pname="__tmpvar__", **kwargs):
        """Obtain information from common errors.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        Parameters
        ----------
        key : int
            Item to be returned.

            * 1 = keyerr (``ER_ERRORFLAG``)

              Master error flag.

            * 2 = errfil (``ER_ERRORFILE``)

              Errors file unit number.

            * 3 = numnot (``ER_NUMNOTE``)

              Total number of notes displayed.

            * 4 = numwrn (``ER_NUMWARNING``)

              Total number of warnings displayed.

            * 5 = numerr (``ER_NUMERROR``)

              Total number of errors displayed.

            * 6 = numfat (``ER_NUMFATAL``)

              Total number of fatals displayed.

            * 7 = maxmsg (``ER_MAXMESSAGE``)

              Max allowed number of displayed messages before abort.

            * 8 = lvlerr (``ER_ERRORLEVEL``)

              Used basically in solution (from ``cnvr`` command.)

              * -1 = do not set keyerr for notes/errors/warnings.
              * -2 = same as -1 but do not display message either.

            * 9 = mxpcmd (``ER_MAXCOMMAND``)

              Maximum number of messages allowed per command.

            * 10 = nercmd (``ER_NUMCOMMAND``)

              Number of messages displayed for any one command.

            * 11 = nertim (``ER_UICLEAR``)

              Key as to how message cleared from u/i pop-up (only for "info"
              calls)

              * -1 = message is timed before removal
              * 0 = message needs pick or keyboard before removal
              * 1 = message stays up until replaced by another message

            * 12 = nomore (``ER_NOMOREMSG``)

              Display no more messages

              * 0 = display messages
              * 1 = display discontinue message and stop displaying

            * 13 = eropen (``ER_FILEOPEN``)

              * 0 = errors file is closed
              * 1 = errors file is opened

            * 14 = ikserr (``ER_INTERERROR``)

              * 0 = if interactive do not set keyerr.
              * -1 = if interactive set keyerr (used by mesher and tessalation)

            * 15 = kystat (``ER_KEYOPTTEST``)

              Flag to bypass keyopt tests in the elcxx routines associated with
              status/panel info inquiries.

              * 0 = do not bypass keyopt tests
              * 1 = perform all keyopt tests also flag to bypass setting of
                ``_STATUS`` upon resume

            * 16 = mxr4r5 (``ER_MIXEDREV``)

              Mixed rev4-rev5 input logic (``*do``, ``*if`` , ``*go`` , ``*if-go``)

              * 1 = rev5 found (``*do``, ``*fi-then-*endif``)
              * 2 = rev4 found (``*go``, ``:xxx`` , ``*if``, ...., ``:xxx``)
              * 3 = warning printed. do not issue any more.

            * 17 = mshkey (``ER_MESHING``)

              CPU intensive meshing etc.
              This will cause ``nertim (11)`` to be set to ``-1`` for "notes", ``1`` for
              "warnings",and ``0`` for "errors".
              Checking of this key is done in ``anserr``.

              * 0 = not meshing or cpu intensive
              * 1 = yes, meshing or cpu intensive

            * 18 = syerro (18)

              Systop error code. read by anserr if set.

            * 19 = opterr (``ER_OPTLOOPING``)

              * 0 = no error in main ansys during opt looping
              * 1 = an error has happened in main ansys during opt looping

            * 20 = flowrn (20)

              Flag used by "floqa" as to list ``floqa.ans``.

              * 0 = list ``floqa.ans``
              * 1 = ``floqa.ans`` has been listed. do not list again.

            * 22 = noreport (22)

              Used in GUI for turning off errors due to strsub calls.

              * 0 = process errors as usual
              * 1 = do **NOT** report errors

            * 23 = pdserr (``ER_PDSLOOPING``)

              * 0 = no error in main ansys during pds looping
              * 1 = an error has happened in main ansys during pds looping

            * 24 = mxpcmdw (24)

              Number of messages written to file.err for any command

              * 0 = write all errors to file.err
              * 1 = only write displayed errors to file.err

            * 25 = kystop

              No information is provided.

            * 26 = icloads (26)

              Key to forbid the ``iclist`` command from listing solution data
              instead of the input data.

              * 0 = ``iclist`` is OK
              * 1 = do not permit ``iclist``

            * 27 = ifkey error (27)

              key on whether or not to abort during :meth:`/input <ansys.mapdl.core.Mapdl.input>` on error.

              * 0 = do not abort
              * 1 = abort

            * 28 = intrupt (``ER_INTERRUPT``)

              Interrupt button, so executable returns no error.

            * spare - spare integer variables

        pname : str
            Name of the variable where the queried value is stored.

        **kwargs
            Extra arguments to be passed to :meth:`Mapdl.run <ansys.mapdl.core.Mapdl.run>`.

        Returns
        -------
        int or str
            Value corresponding to key.

        """
        return self.run(f"{pname} = erinqr({key})", **kwargs)

    def wrinqr(self, key, pname="__tmpvar__", **kwargs):
        """Obtain information about output.

        .. warning:: **DISCLAIMER**: This function is un-documented in the
                   official ANSYS Command Reference Guide.
                   Hence its support is limited and it use is not encouraged.
                   **Please use it with caution.**

        .. warning:: Caution: the following variables are "saved/resumed".
                    key=``WR_COLINTER`` thru ``WR_SUPCOLMAX`` in "wrinqr/wrinfo".

        Parameters
        ----------
        key : int
            Key.

            * 1 - kprint (WR_PRINT)
              Print flag.

              * 0 - no output
              * 1 - print

            * 2 - outfil (WR_OUTPUT)
              Current output unit number(iott).
            * 4 - frstot (WR_MASTEROUT)
              Master output file.
            * 5 - intcol (WR_COLINTER)
              Interactive columns per page.
            * 6 - batcol (WR_COLBATCH)
              Batch columns per page.
            * 7 - intlin (WR_LINEINTER)
              Interactive lines per page.
            * 8 - batlin (WR_LINEBATCH)
              Batch lines per page.
            * 9 - CommaSep (WR_COMMASEP)
              1 for comma separated output.
            * 11 - chrper (WR_CHARITEM)
              Characters per output item.
            * 12 - chrdec (WR_CHARDECIMAL)
              Characters past decimal.
            * 13 - chrint (WR_CHARINTEGER)
              Characters in leading integer.
            * 14 - chrtyp (WR_CHARTYPE)

              * 1 - using E format in output.
              * 2 - using F format in output.
              * 3 - using G format in output.

            * 15 - (WR_TEMPLINEBATCH)
              Undocumented (50 default).
            * 16 - keyhed (WR_SUPTITLE)
              Tlabel suppress key.
            * 17 - keytit (WR_SUPSUBTITLE)
              Subtitle suppress key.
            * 18 - keyid (WR_SUPLSITER)
              Ls,iter id suppress key.
            * 19 - keynot (WR_NOTELINE)
              Note line suppress key.
            * 20 - keylab (WR_SUPCOLHEADER)
               column header suppress key.
            * 21 - keysum (WR_SUPCOLMAX)
              Column maximum suppress key.
            * 22 - ListOpt (WR_LISTOPT)
              ListOpt from /output command.

        Returns
        -------
        int or str
            The value corresponding to key.

        """
        return self.run(f"{pname} = wrinqr({key})", **kwargs)
