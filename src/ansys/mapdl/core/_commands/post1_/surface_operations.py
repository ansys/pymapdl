class SurfaceOperations:
    def sucalc(
        self,
        rsetname="",
        lab1="",
        oper="",
        lab2="",
        fact1="",
        fact2="",
        const="",
        **kwargs,
    ):
        """Create new result data by operating on two existing result data sets on

        APDL Command: SUCALC
        a given surface.

        Parameters
        ----------
        rsetname
            Eight character name for new result data.

        lab1
            First  result data upon which to operate.

        oper
            Mathematical operation to perform.

            ADD - (lab1 + lab2 + const)

            SUB - (lab1 - lab2 + const)

            MULT - (lab1 * lab2 + const)

            DIV - (lab1 / lab2 + const)

            EXP - (lab1 ^ fact1 + lab2 ^ fact2 + const)

            COS - (cos (lab1) + const)

            SIN - (sin (lab1) + const)

            ACOS - (acos (lab1) + const)

            ASIN - (asin (lab1) + const)

            ATAN - (atan (lab1) + const)

            ATA2 - (atan2 (lab1 / lab2) + const)

            LOG - (log (lab1) + const)

            ABS - (abs (lab1) + const)

            ZERO - (0 + const)

        lab2
            Second result data upon which to operate.

        fact1
            First scaling factor (for EXP option only).

        fact2
            Second scaling factor (for EXP option only).

        const
            Constant added to the values in the resulting data.
        """
        command = f"SUCALC,{rsetname},{lab1},{oper},{lab2},{fact1},{fact2},{const}"
        return self.run(command, **kwargs)

    def sucr(
        self,
        surfname="",
        surftype="",
        nrefine="",
        radius="",
        tolout="",
        **kwargs,
    ):
        """Create a surface.

        APDL Command: SUCR

        Parameters
        ----------
        surfname
            Eight character surface name.

        surftype
            Surface type.

            CPLANE - Surface is defined by the cutting plane in window one (controlled by the
                     working plane (/CPLANE,1), NOT the view settings
                     (/CPLANE,0)).

            SPHERE - Surface is defined by a spherical surface centered about the working plane
                     origin.

            INFC - Surface is defined by a cylindrical surface centered about the working plane
                   origin and extending indefinitely in the positive and
                   negative Z directions.

        nrefine
            Refinement level.

            For SurfType = CPLANE -  The refinement level of the surface "mesh". This will be an integer between 0
                              and 3 (default = 0). See Notes below.

            For SurfType = SPHERE - The number of divisions along a 90° arc (minimum = 9). The default is 9.

            For SurfType = INFC - The number of divisions along a 90° arc (minimum = 9). The default is 9.

        radius
            Appropriate radius value (for INFC or SPHERE).

        tolout
            Tolerance value for inclusion of element facets within a prescribed
            volume. (for INFC)

        Notes
        -----
        This command creates a new surface and stores the following data for
        that surface:

        For SurfType = CPLANE, nRefine refers to the number of points that
        define the surface. An nRefine value of zero is used for points where
        the element face intersects the cutting plane.

        If SurfType = CPLANE and nRefine = 0, the points reside at the section
        cuts where the element intersects the cutting plane. Increasing nRefine
        from 0 to 1 will subdivide each surface facet into 4 subfacets, and
        increase the number of points at which results can be interpolated.

        For SurfType = CPLANE , the setting from the /EFACET command will
        affect the creation of surface facets and the quality of the fit of the
        surface in the model.  SUCR employs geometry data from PowerGraphics to
        aid in determining where the surface intersects the model.  If
        /EFACET,1 is in effect when the SUCR command is issued, then the
        curvature of high order elements (that is, elements with midside nodes)
        will be ignored.  If your model contains high order elements, you can
        see a better fit for your surface if /EFACET,2 is in effect when the
        SUCR command is issued.  Currently, the SUCR command interprets
        /EFACET,4 to mean /EFACET,2.

        For SurfType = INFC, a default tolerance of 0.01 will be applied to
        include the vertices of any facets that fall out of the cylinder
        definition. This tolerance increases the facet size by one percent to
        check for inclusion. Excluding facets under such a small tolerance may
        yield unacceptable (aesthetically) results. Increasing the tolerance by
        a larger amount (0.1 or 10%) will sometimes yield smother edges along
        the surface you create.
        """
        command = f"SUCR,{surfname},{surftype},{nrefine},{radius},{tolout}"
        return self.run(command, **kwargs)

    def sudel(self, surfname="", **kwargs):
        """Delete geometry information as well as any mapped results for specified

        APDL Command: SUDEL
        surface.

        Parameters
        ----------
        surfname
            Eight character surface name.
        """
        command = f"SUDEL,{surfname}"
        return self.run(command, **kwargs)

    def sueval(self, parm="", lab1="", oper="", **kwargs):
        """Perform operations on a mapped item and store result in a scalar

        APDL Command: SUEVAL
        parameter.

        Parameters
        ----------
        parm
            APDL parameter name.

        lab1
            Eight character set name for the first set used in calculation.

        oper
            Operation to perform:

            SUM - Sum of lab1 result values.

            INTG - Integral of lab1 over surface.

            AVG - Area-weighted average of a result item ``[Σ(lab1*DA) / Σ(DA)]``

        Notes
        -----
        The result of this operation is a scalar APDL parameter value. If
        multiple surfaces are selected when this command is issued, then the
        operation is carried out on each surface individually and the parameter
        represents the cumulative value of the operation on all selected
        surfaces.
        """
        command = f"SUEVAL,{parm},{lab1},{oper}"
        return self.run(command, **kwargs)

    def suget(self, surfname="", rsetname="", parm="", geom="", **kwargs):
        """Moves surface geometry and mapped results to an array parameter.

        APDL Command: SUGET

        Parameters
        ----------
        surfname
            Eight character surface name.

        rsetname
            Eight character result name.

        parm
            APDL array parameter name (up to 32 characters).

        geom
            Switch controlling how data is written.

            ON (or 1 or YES) - Writes geometry data and interpolated
            results information to the parameter.

            OFF (or 0 or NO) - Writes only interpolated results
            information to the parameter. (Default)

        Notes
        -----
        For Geom = OFF (or 0 or NO), only results information is written to
        this parameter.

        For Geom = ON (or 1 or YES), both geometry data and results information
        are written to this parameter.  Geometry data includes 7 data items:
        (GCX, GCY, GCZ, NORMX, NORMY, NORMZ, and DA). Results information is
        then written to the 8th column of the parameter. SetNames of GCX, GCY,
        GCZ, NORMX, NORMY, NORMZ, and DA are predefined and computed when SUCR
        is issued.
        """
        command = f"SUGET,{surfname},{rsetname},{parm},{geom}"
        return self.run(command, **kwargs)

    def sumap(self, rsetname="", item="", comp="", **kwargs):
        """Map results onto selected surface(s).

        APDL Command: SUMAP

        Parameters
        ----------
        rsetname
            Eight-character name for the result being mapped.

        item
            Label identifying the item.

        comp
            Component label of item (if required).

        Notes
        -----
        The SUMAP command maps results in the current coordinate system (RSYS)
        using the selected set of elements.

        The command interpolates and stores the results data on to each of the
        selected surfaces.

        SUMAP,ALL,CLEAR deletes all results sets from all selected surfaces.
        """
        command = f"SUMAP,{rsetname},{item},{comp}"
        return self.run(command, **kwargs)

    def supl(self, surfname="", rsetname="", kwire="", **kwargs):
        """Plot result data on all selected surfaces or on a specified surface.

        APDL Command: SUPL

        Parameters
        ----------
        surfname
            Eight character surface name. ALL will plot all selected surfaces.

        rsetname
            Eight character result name.

        kwire
            Plot in context of model.

            0 - Plot results without the outline of selected elements.

            1 - Plot results with the outline of selected elements.

        Notes
        -----
        If RSetName is left blank, then the surface geometry will be plotted.
        If the Setname portion of the argument is a vector prefix (i.e. if
        result sets of name SetNameX, SetNameY and SetNameZ exist), ANSYS will
        plot these vectors on the surface as arrows. For example, SUPL, ALL,
        NORM will plot the surface normals as vectors on all selected surfaces,
        since NORMX NORMY and NORMZ are pre-defined geometry items.
        """
        command = f"SUPL,{surfname},{rsetname},{kwire}"
        return self.run(command, **kwargs)

    def supr(self, surfname="", rsetname="", **kwargs):
        """Print global status, geometry information and/or result information.

        APDL Command: SUPR

        Parameters
        ----------
        surfname
            Eight character surface name. If SurfName = ALL, repeat printout
            for all selected surfaces.

        rsetname
            Eight character result set name.

        Notes
        -----
        When no arguments are specified, SUPR generates a global status summary
        of all defined surfaces. If only SurfName is specified, the geometry
        information for that surface is printed. If both SurfName and RSetName
        are specified, the value of the results set at each point, in addition
        to the geometry information, is printed.
        """
        command = f"SUPR,{surfname},{rsetname}"
        return self.run(command, **kwargs)

    def suresu(self, fname="", fext="", fdir="", **kwargs):
        """Read a set of surface definitions and result items from a file

        APDL Command: SURESU
        and make them the current set.

        Parameters
        ----------
        fname
            Eight character name.

        fext
            Extension name.

        fdir
            Optional path specification.

        Notes
        -----
        Reading (and therefore resuming) surface and result
        definitions from a file overwritea any existing surface
        definitions.

        Reading surfaces back into the postprocessor (/POST1) does not
        insure that the surfaces (and their results) are appropriate
        for the model currently residing in /POST1.
        """
        return self.run(f"SURESU,,{fname},{fext},{fdir}", **kwargs)

    def susave(self, lab="", fname="", fext="", fdir="", **kwargs):
        """Saves surface definitions to a file.

        APDL Command: SUSAVE

        Parameters
        ----------
        lab
            Eight-character surface name.

        fname
            File name and directory path (248 character maximum, including
            directory). If you do not specify a directory path, the default is
            your working directory and you can use all 248 characters for the
            file name. The file name defaults to the jobname.

        fext
            File name extension (eight-character maximum). The extension
            defaults to "surf".

        fdir
            Optional path specification.

        Notes
        -----
        The SUSAVE command saves surface definitions (geometry
        information)--and any result items mapped onto the surfaces--to a file.

        Issuing the SUSAVE command has no effect on the database. The database
        remains unchanged.

        Subsequent executions of the SUSAVE command overwrite previous data in
        the file.

        To read the contents of the file created via the SUSAVE command, issue
        the SURESU command.
        """
        command = f"SUSAVE,{lab},{fname},{fext},{fdir}"
        return self.run(command, **kwargs)

    def susel(
        self,
        type_="",
        name1="",
        name2="",
        name3="",
        name4="",
        name5="",
        name6="",
        name7="",
        name8="",
        **kwargs,
    ):
        """Selects a subset of surfaces

        APDL Command: SUSEL

        Parameters
        ----------
        type\_
            Label identifying the type of select:

            S - Selects a new set (default).

            R - Reselects a set from the current set.

            A - Additionally selects a set and extends the current set.

            U - Unselects a set from the current set.

            ALL - Also selects all surfaces.

            NONE - Unselects all surfaces.

        name1, name2, name3, . . . , name8
            Eight character surface names

        Notes
        -----
        The selected set of surfaces is used in the following operations:
        SUMAP, SUDEL, SUCALC, SUEVAL, and SUVECT.
        """
        command = f"SUSEL,{type_},{name1},{name2},{name3},{name4},{name5},{name6},{name7},{name8}"
        return self.run(command, **kwargs)

    def suvect(self, rsetname="", lab1="", oper="", lab2="", offset="", **kwargs):
        """Create new result data by operating on two existing result vectors on a

        APDL Command: SUVECT
        given surface.

        Parameters
        ----------
        rsetname
            Eight character name of the result data output. There will be one
            or three RSetName values depending on the operation specified in
            Oper.

        lab1
            Eight character name of the mapped data that forms vector 1.
            Specified sets must exist on all selected surfaces for this
            operation to take place. The names NORM and GC will be reserved for
            normals and for global (x, y, z).

        oper
            DOT

            DOT - Computes dot product between lab1 and lab2 vectors. The result is a scalar
                  parameter (RSetName) and each value within the set can be
                  modified (incremented) via Offset.

            CROSS - Computes cross product between lab1 and lab2 vectors. Each X, Y, Z value in the
                    result can be modified (incremented) via Offset.

            SMULT - Scales (lab1x, lab1y, lab1z) vector by scalar lab2. Each X,Y,Z value in the
                    result can be modified (incremented) via Offset.

        lab2
            Eight character name of the mapped data that forms vector 2. Sets
            with names Lab2X, Lab2Y, and Lab2Z must exist on all selected
            surfaces for operation to take place.  For Oper = SMULT a scalar
            value or another predefined scalar item (e.g., DA) can be supplied.

        offset
            An offset value to be applied to the resultant RSetName. One value
            is specified for Oper = DOT, and three values are specified for
            Oper = SMULT.
        """
        command = f"SUVECT,{rsetname},{lab1},{oper},{lab2},{offset}"
        return self.run(command, **kwargs)
