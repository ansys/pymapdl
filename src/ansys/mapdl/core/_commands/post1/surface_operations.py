# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

from ansys.mapdl.core._commands import CommandsBase


class SurfaceOperations(CommandsBase):

    def sucalc(
        self,
        rsetname: str = "",
        lab1: str = "",
        oper: str = "",
        lab2: str = "",
        fact1: str = "",
        fact2: str = "",
        const: str = "",
        **kwargs,
    ):
        r"""Create new result data by operating on two existing result data sets on a given surface.

        Mechanical APDL Command: `SUCALC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUCALC.html>`_

        Parameters
        ----------
        rsetname : str
            Eight character name for new result data.

        lab1 : str
            First result data upon which to operate.

        oper : str
            Mathematical operation to perform.

            * ``ADD`` - ( ``lab1`` + ``lab2`` + ``const`` )

            * ``SUB`` - ( ``lab1`` - ``lab2`` + ``const`` )

            * ``MULT`` - ( ``lab1`` \* ``lab2`` + ``const`` )

            * ``DIV`` - ( ``lab1`` / ``lab2`` + ``const`` )

            * ``EXP`` - ( ``lab1`` ^ ``fact1`` + ``lab2`` ^ ``fact2`` + ``const`` )

            * ``COS`` - (cos ( ``lab1`` ) + ``const`` )

            * ``SIN`` - (sin ( ``lab1`` ) + ``const`` )

            * ``ACOS`` - (acos ( ``lab1`` ) + ``const`` )

            * ``ASIN`` - (asin ( ``lab1`` ) + ``const`` )

            * ``ATAN`` - (atan ( ``lab1`` ) + ``const`` )

            * ``ATA2`` - (atan2 ( ``lab1`` / ``lab2`` ) + ``const`` )

            * ``LOG`` - (log ( ``lab1`` ) + ``const`` )

            * ``ABS`` - (abs ( ``lab1`` ) + ``const`` )

            * ``ZERO`` - (0 + ``const`` )

        lab2 : str
            Second result data upon which to operate.

        fact1 : str
            First scaling factor (for EXP option only).

        fact2 : str
            Second scaling factor (for EXP option only).

        const : str
            Constant added to the values in the resulting data.
        """
        command = f"SUCALC,{rsetname},{lab1},{oper},{lab2},{fact1},{fact2},{const}"
        return self.run(command, **kwargs)

    def sucr(
        self,
        surfname: str = "",
        surftype: str = "",
        nrefine: str = "",
        radius: str = "",
        tolout: str = "",
        **kwargs,
    ):
        r"""Create a surface.

        Mechanical APDL Command: `SUCR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUCR.html>`_

        Parameters
        ----------
        surfname : str
            Eight character surface name.

        surftype : str
            Surface type.

            * ``CPLANE`` - Surface is defined by the cutting plane in window one (controlled by the working
              plane (/CPLANE,1), NOT the view settings (/CPLANE,0)).

            * ``SPHERE`` - Surface is defined by a spherical surface centered about the working plane origin.

            * ``INFC`` - Surface is defined by a cylindrical surface centered about the working plane origin and
              extending indefinitely in the positive and negative Z directions.

        nrefine : str
            Refinement level.

            * ``For SurfType = CPLANE`` - The refinement level of the surface mesh. This will be an integer
              between 0 and 3 (default = 0). See Notes below.

            * ``For SurfType = SPHERE`` - The number of divisions along a 90° arc (minimum = 9). The default is
              9.

            * ``For SurfType = INFC`` - The number of divisions along a 90° arc (minimum = 9). The default is 9.

        radius : str
            Appropriate radius value (for INFC or SPHERE).

        tolout : str
            Tolerance value for inclusion of element facets within a prescribed volume. (for INFC)

        Notes
        -----

        .. _SUCR_notes:

        This command creates a new surface and stores the following data for that surface:

        * GCX, GCY, GCZ - global Cartesian coordinates at each point on the surface.
        * NORMX, NORMY, NORMZ - components of the unit normal at each point on the surface.
        * DA - the contributory area of each point.

        For ``SurfType`` = CPLANE, ``nRefine`` refers to the number of points that define the surface. An
        ``nRefine`` value of zero is used for points where the element face intersects the cutting plane.

        If ``SurfType`` = CPLANE and ``nRefine`` = 0, the points reside at the section cuts where the
        element intersects the cutting plane. Increasing ``nRefine`` from 0 to 1 will subdivide each surface
        facet into 4 subfacets, and increase the number of points at which results can be interpolated.

        For ``SurfType`` = CPLANE, the setting from the :ref:`efacet` command will affect the creation of
        surface facets and the quality of the fit of the surface in the model. :ref:`sucr` employs geometry
        data from PowerGraphics to aid in determining where the surface intersects the model. If
        :ref:`efacet`,1 is in effect when the :ref:`sucr` command is issued, then the curvature of high
        order elements (that is, elements with midside nodes) will be ignored. If your model contains high
        order elements, you can see a better fit for your surface if /EFACET,2 is in effect when the
        :ref:`sucr` command is issued. Currently, the :ref:`sucr` command interprets :ref:`efacet`,4 to
        mean :ref:`efacet`,2.

        For ``SurfType`` = INFC, a default tolerance of 0.01 will be applied to include the vertices of any
        facets that fall out of the cylinder definition. This tolerance increases the facet size by one
        percent to check for inclusion. Excluding facets under such a small tolerance may yield unacceptable
        (aesthetically) results. Increasing the tolerance by a larger amount (0.1 or 10%) will sometimes
        yield smother edges along the surface you create.
        """
        command = f"SUCR,{surfname},{surftype},{nrefine},{radius},,,{tolout}"
        return self.run(command, **kwargs)

    def sudel(self, surfname: str = "", **kwargs):
        r"""Delete geometry information as well as any mapped results for specified surface.

        Mechanical APDL Command: `SUDEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUDEL.html>`_

        Parameters
        ----------
        surfname : str
            Eight character surface name.

            ``SurfName`` = ALL will delete all surface geometry and result information.
        """
        command = f"SUDEL,{surfname}"
        return self.run(command, **kwargs)

    def sueval(self, parm: str = "", lab1: str = "", oper: str = "", **kwargs):
        r"""Perform operations on a mapped item and store result in a scalar parameter.

        Mechanical APDL Command: `SUEVAL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUEVAL.html>`_

        Parameters
        ----------
        parm : str
            APDL parameter name.

        lab1 : str
            Eight character set name for the first set used in calculation.

        oper : str
            Operation to perform:

            * ``SUM`` - Sum of ``lab1`` result values.

            * ``INTG`` - Integral of ``lab1`` over surface.

            * ``AVG`` - Area-weighted average of a result item [Σ( ``lab1`` \*DA) / Σ(DA)]

        Notes
        -----

        .. _SUEVAL_notes:

        The result of this operation is a scalar APDL parameter value. If multiple surfaces are selected
        when this command is issued, then the operation is carried out on each surface individually and the
        parameter represents the cumulative value of the operation on all selected surfaces.
        """
        command = f"SUEVAL,{parm},{lab1},{oper}"
        return self.run(command, **kwargs)

    def suget(
        self,
        surfname: str = "",
        rsetname: str = "",
        parm: str = "",
        geom: str = "",
        **kwargs,
    ):
        r"""Moves surface geometry and mapped results to an array parameter.

        Mechanical APDL Command: `SUGET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUGET.html>`_

        Parameters
        ----------
        surfname : str
            Eight character surface name.

        rsetname : str
            Eight character result name.

        parm : str
            APDL array parameter name (up to 32 characters).

        geom : str
            Switch controlling how data is written.

            * ``ON (or 1 or YES)`` - Writes geometry data and interpolated results information to the parameter.

            * ``OFF (or 0 or NO)`` - Writes only interpolated results information to the parameter. (Default)

        Notes
        -----

        .. _SUGET_notes:

        For ``Geom`` = OFF (or 0 or NO), only results information is written to this parameter.

        For ``Geom`` = ON (or 1 or YES), both geometry data and results information are written to this
        parameter. Geometry data includes 7 data items: (GCX, GCY, GCZ, NORMX, NORMY, NORMZ,  and DA).
        Results information is then written to the 8th column of the parameter. SetNames of GCX, GCY, GCZ,
        NORMX, NORMY, NORMZ, and DA are predefined and computed when :ref:`sucr` is issued.
        """
        command = f"SUGET,{surfname},{rsetname},{parm},{geom}"
        return self.run(command, **kwargs)

    def sumap(self, rsetname: str = "", item: str = "", comp: str = "", **kwargs):
        r"""Map results onto selected surface(s).

        Mechanical APDL Command: `SUMAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUMAP.html>`_

        Parameters
        ----------
        rsetname : str
            Eight-character name for the result being mapped.

        item : str
            Label identifying the item.

            Valid item labels are defined via :ref:`plnsol`. Some items also require a component label.

            If ``Item`` = CLEAR, the specified result set is deleted from all selected surfaces

        comp : str
            Component label of item (if required).

        Notes
        -----

        .. _SUMAP_notes:

        The :ref:`sumap` command maps results in the current coordinate system ( :ref:`rsys` ) using the
        selected set of elements.

        The command interpolates and stores the results data on to each of the selected surfaces.

        :ref:`sumap`,ALL,CLEAR deletes all results sets from all selected surfaces.
        """
        command = f"SUMAP,{rsetname},{item},{comp}"
        return self.run(command, **kwargs)

    def supl(
        self, surfname: str = "", rsetname: str = "", kwire: int | str = "", **kwargs
    ):
        r"""Plot result data on all selected surfaces or on a specified surface.

        Mechanical APDL Command: `SUPL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUPL.html>`_

        Parameters
        ----------
        surfname : str
            Eight-character surface name. ALL plots all selected surfaces.

        rsetname : str
            Eight-character result name.

        kwire : int or str
            Plot in context of model.

            * ``0`` - Plot results without the outline of selected elements.

            * ``1`` - Plot results with the outline of selected elements.

        Notes
        -----

        .. _SUPL_notes:

        If ``RSetName`` is not specified, the surface geometry is plotted. If the Setname portion of the
        argument is a vector prefix (that is, if result sets of name SetNameX, SetNameY, and SetNameZ
        exist), Mechanical APDL plots the vectors on the surface as arrows. For example,
        :ref:`supl`,ALL,NORM plots
        the surface normals as vectors on all selected surfaces, as NORMX, NORMY, and NORMZ are predefined
        geometry items.
        """
        command = f"SUPL,{surfname},{rsetname},{kwire}"
        return self.run(command, **kwargs)

    def supr(self, surfname: str = "", rsetname: str = "", **kwargs):
        r"""Print global status, geometry information and/or result information.

        Mechanical APDL Command: `SUPR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUPR.html>`_

        Parameters
        ----------
        surfname : str
            Eight character surface name. If ``SurfName`` = ALL, repeat printout for all selected surfaces.

        rsetname : str
            Eight character result set name.

        Notes
        -----

        .. _SUPR_notes:

        When no arguments are specified, :ref:`supr` generates a global status summary of all defined
        surfaces. If only ``SurfName`` is specified, the geometry information for that surface is printed.
        If both ``SurfName`` and ``RSetName`` are specified, the value of the results set at each point, in
        addition to the geometry information, is printed.
        """
        command = f"SUPR,{surfname},{rsetname}"
        return self.run(command, **kwargs)

    def suresu(self, fname: str = "", fext: str = "", fdir: str = "", **kwargs):
        r"""Read a set of surface definitions and result items from a file and make them the current set.

        Mechanical APDL Command: `SURESU <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SURESU.html>`_

        Parameters
        ----------

        fname : str
            Eight character name.

        fext : str
            Extension name.

        fdir : str
            Optional path specification.

        Notes
        -----

        .. _SURESU_notes:

        Reading (and therefore resuming) surface and result definitions from a file overwritea any existing
        surface definitions.

        Reading surfaces back into the postprocessor ( :ref:`post1` ) does not insure that the surfaces (and
        their results) are appropriate for the model currently residing in :ref:`post1`.
        """
        command = f"SURESU,,{fname},{fext},{fdir}"
        return self.run(command, **kwargs)

    def susave(
        self, lab: str = "", fname: str = "", fext: str = "", fdir: str = "", **kwargs
    ):
        r"""Saves surface definitions to a file.

        Mechanical APDL Command: `SUSAVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUSAVE.html>`_

        Parameters
        ----------
        lab : str
            Eight-character surface name.

            If ``Lab`` = ALL (default), then all surfaces are saved to the file.

            If ``Lab`` = S, only currently selected surfaces are saved to the file.

        fname : str
            File name and directory path (248 character maximum, including directory). If you do not specify
            a directory path, the default is your working directory and you can use all 248 characters for
            the file name. The file name defaults to the jobname.

        fext : str
            File name extension (eight-character maximum). The extension defaults to "surf".

        fdir : str
            Optional path specification.

        Notes
        -----

        .. _SUSAVE_notes:

        The :ref:`susave` command saves surface definitions (geometry information)--and any result items
        mapped onto the surfaces--to a file.

        Issuing the :ref:`susave` command has no effect on the database. The database remains unchanged.

        Subsequent executions of the :ref:`susave` command overwrite previous data in the file.

        To read the contents of the file created via the :ref:`susave` command, issue the :ref:`suresu`
        command.
        """
        command = f"SUSAVE,{lab},{fname},{fext},{fdir}"
        return self.run(command, **kwargs)

    def susel(
        self,
        type_: str = "",
        name1: str = "",
        name2: str = "",
        name3: str = "",
        name4: str = "",
        name5: str = "",
        name6: str = "",
        name7: str = "",
        name8: str = "",
        **kwargs,
    ):
        r"""Selects a subset of surfaces

        Mechanical APDL Command: `SUSEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUSEL.html>`_

        Parameters
        ----------
        type_ : str
            Label identifying the type of select:

            * ``S`` - Selects a new set (default).

            * ``R`` - Reselects a set from the current set.

            * ``A`` - Additionally selects a set and extends the current set.

            * ``U`` - Unselects a set from the current set.

            * ``ALL`` - Also selects all surfaces.

            * ``NONE`` - Unselects all surfaces.

        name1 : str
            Eight character surface names

        name2 : str
            Eight character surface names

        name3 : str
            Eight character surface names

        name4 : str
            Eight character surface names

        name5 : str
            Eight character surface names

        name6 : str
            Eight character surface names

        name7 : str
            Eight character surface names

        name8 : str
            Eight character surface names

        Notes
        -----

        .. _SUSEL_notes:

        The selected set of surfaces is used in the following operations: :ref:`sumap`, :ref:`sudel`,
        :ref:`sucalc`, :ref:`sueval`, and :ref:`suvect`.
        """
        command = f"SUSEL,{type_},{name1},{name2},{name3},{name4},{name5},{name6},{name7},{name8}"
        return self.run(command, **kwargs)

    def suvect(
        self,
        rsetname: str = "",
        lab1: str = "",
        oper: str = "",
        lab2: str = "",
        offset: str = "",
        **kwargs,
    ):
        r"""Create new result data by operating on two existing result vectors on a given surface.

        Mechanical APDL Command: `SUVECT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SUVECT.html>`_

        Parameters
        ----------
        rsetname : str
            Eight character name of the result data output. There will be one or three ``RSetName`` values
            depending on the operation specified in ``Oper``.

        lab1 : str
            Eight character name of the mapped data that forms vector 1. Specified sets must exist on all
            selected surfaces for this operation to take place. The names NORM and GC will be reserved for
            normals and for global (x, y, z).

        oper : str
            * ``DOT`` - Computes dot product between ``lab1`` and ``lab2`` vectors. The result is a scalar
              parameter ( ``RSetName`` ) and each value within the set can be modified (incremented) via
              ``Offset``.

            * ``CROSS`` - Computes cross product between ``lab1`` and ``lab2`` vectors. Each X, Y, Z value in
              the result can be modified (incremented) via ``Offset``.

            * ``SMULT`` - Scales (lab1x, lab1y, lab1z) vector by scalar ``lab2``. Each X,Y,Z value in the result
              can be modified (incremented) via ``Offset``.

        lab2 : str
            Eight character name of the mapped data that forms vector 2. Sets with names Lab2X, Lab2Y, and
            Lab2Z must exist on all selected surfaces for operation to take place. For ``Oper`` = SMULT a
            scalar value or another predefined scalar item (for example, DA) can be supplied.

        offset : str
            An offset value to be applied to the resultant ``RSetName``. One value is specified for ``Oper``
            = DOT, and three values are specified for ``Oper`` = SMULT.
        """
        command = f"SUVECT,{rsetname},{lab1},{oper},{lab2},{offset}"
        return self.run(command, **kwargs)
