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

class PressureMapping:

    def plgeom(self, item: str = "", nodekey: str = "", **kwargs):
        r"""Plots target and source geometries.

        Mechanical APDL Command: `PLGEOM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLGEOM.html>`_

        Parameters
        ----------
        item : str
            Items to plot:

            * ``BOTH`` - Plot both target and source geometries (default).

            * ``TARGET`` - Plot only the target geometry.

            * ``SOURCE`` - Plot only the source geometry.

        nodekey : str
            If the source data contains faces (that is, surface elements were created upon the :ref:`read`
            command), set ``NODEkey`` = 1 to plot only the source nodes rather than both the nodes and the
            elements.

        Notes
        -----

        .. _PLGEOM_notes:

        Target faces are displayed in gray and source points in yellow. If the source data contains faces
        (that is, surface elements were created upon the :ref:`read` command), the source faces are also
        displayed in blue (unless ``NODEkey`` = 1), and both surfaces are made translucent.
        """
        command = f"PLGEOM,{item},{nodekey}"
        return self.run(command, **kwargs)



    def plmap(self, item: str = "", nodekey: str = "", imagkey: int | str = "", **kwargs):
        r"""Plots target and source pressures.

        Mechanical APDL Command: `PLMAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLMAP.html>`_

        Parameters
        ----------
        item : str
            Items to plot:

            * ``BOTH`` - Plot both target and source pressures (default).

            * ``TARGET`` - Plot only the target pressures.

            * ``SOURCE`` - Plot only the source pressures.

        nodekey : str
            If the source data contains faces (that is, surface elements were created upon the :ref:`read`
            command), set ``NODEkey`` = 1 to plot only the source nodes rather than both the nodes and the
            elements.

        imagkey : int or str
            * ``0`` - Plot the real pressures (default).

            * ``1`` - Plot the imaginary pressures.

        Notes
        -----

        .. _PLMAP_notes:

        Pressures on the target faces are displayed as a color contour plot using the command
        :ref:`psf`,PRES,,3. If the source data contains faces (that is, surface elements were created upon
        the :ref:`read` command), the source faces are also displayed using a color contour plot by default.
        If ``NODEkey`` = 1 or no source faces are available, the source pressures are displayed as colored
        node symbols ( :ref:`psymb`,DOT,1 command).
        """
        command = f"PLMAP,{item},,{nodekey},{imagkey}"
        return self.run(command, **kwargs)



    def map(self, kdim: int | str = "", kout: int | str = "", limit: str = "", **kwargs):
        r"""Maps pressures from source points to target surface elements.

        Mechanical APDL Command: `MAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MAP.html>`_

        Parameters
        ----------

        kdim : int or str
            Interpolation key:

            * ``0 or 2`` - Interpolation is done on a surface (default).

            * ``3`` - Interpolation is done within a volume. This option is useful if the supplied source data
              is volumetric field data rather than surface data.

        kout : int or str
            Key to control how pressure is applied when a target node is outside of the source region:

            * ``0`` - Use the pressure(s) of the nearest source point for target nodes outside of the region
              (default).

            * ``1`` - Set pressures outside of the region to zero.

        limit : str
            Number of nearby points considered for interpolation. The minimum is 5; the default is 20. Lower
            values reduce processing time. However, some distorted or irregular meshes will require a higher
            ``LIMIT`` value to find the points encompassing the target node in order to define the region
            for interpolation.

        Notes
        -----

        .. _MAP_notes:

        Maps pressures from source points to target surface elements.
        """
        command = f"MAP,,{kdim},,{kout},{limit}"
        return self.run(command, **kwargs)



    def slashmap(self, **kwargs):
        r"""Enters the mapping processor.

        Mechanical APDL Command: `/MAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MAP_s.html>`_

        Notes
        -----
        Enters the mapping processor. This processor is used to read in source data from an external file
        and map it to the existing geometry.

        The current database is saved (to :file:`BeforeMapping.DB` ) upon entering the processor, and it is
        resumed upon exiting ( :ref:`finish` command). Any nodes or elements not on the target surface are
        deleted for easier viewing of the mapping quantities. A database of this mapping geometry (
        :file:`Mapping.DB` ) is also saved at the :ref:`finish` command.

        This command is valid only at the Begin Level.
        """
        command = "/MAP"
        return self.run(command, **kwargs)



    def target(self, nlist: str = "", **kwargs):
        r"""Specifies the target nodes for mapping pressures onto surface effect elements.

        Mechanical APDL Command: `TARGET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TARGET.html>`_

        Parameters
        ----------
        nlist : str
            Nodes defining the surface upon which the pressures will be mapped. Use the label ALL or specify
            a nodal component name. If ALL, all selected nodes ( :ref:`nsel` ) are used (default).
            Individual nodes may not be entered.

        Notes
        -----

        .. _TARGET_notes:

        The node list specified by ``Nlist`` must contain a sufficient number of nodes to define an element
        surface. The surface must be meshed ( :ref:`esurf` command) with ``SURF154``elements prior to
        issuing this command.
        """
        command = f"TARGET,{nlist}"
        return self.run(command, **kwargs)



    def read(self, fname: str = "", nskip: str = "", format_: str = "", xfield: str = "", yfield: str = "", zfield: str = "", prfield: str = "", pifield: str = "", **kwargs):
        r"""Reads coordinate and pressure data from a file.

        Mechanical APDL Command: `READ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_READ.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name.

        nskip : str
            Number of lines at the beginning of the file that will be skipped while it is read. Default = 0.
            ``NSKIP`` is ignored for ``FileType`` = CFXTBR or CFDPOST on the :ref:`ftype` command.

        format_ : str
            For ``FileType`` = FORMATTED on the :ref:`ftype` command, ``Format`` is the read format in the
            FORTRAN FORMAT convention enclosed in parentheses; for example: (3e10.0,10x,e10.0,70x,e10.0)

        xfield : str
            For ``FileType`` = CSV on the :ref:`ftype` command, these are field numbers locating the
            coordinates and real and imaginary (if present) pressures. The field value may not exceed 20.

        yfield : str
            For ``FileType`` = CSV on the :ref:`ftype` command, these are field numbers locating the
            coordinates and real and imaginary (if present) pressures. The field value may not exceed 20.

        zfield : str
            For ``FileType`` = CSV on the :ref:`ftype` command, these are field numbers locating the
            coordinates and real and imaginary (if present) pressures. The field value may not exceed 20.

        prfield : str
            For ``FileType`` = CSV on the :ref:`ftype` command, these are field numbers locating the
            coordinates and real and imaginary (if present) pressures. The field value may not exceed 20.

        pifield : str
            For ``FileType`` = CSV on the :ref:`ftype` command, these are field numbers locating the
            coordinates and real and imaginary (if present) pressures. The field value may not exceed 20.

        Notes
        -----

        .. _READ_notes:

        Reads coordinate and pressure data from the specified file. The file type must have been previously
        specified on the :ref:`ftype` command.

        Upon reading the file, nodes are created for the source points. For ``FileType`` = CFXTBR or CFDPOST
        on the :ref:`ftype` command, if face data is available, ``SURF154``elements are also created. A
        nodal component named SOURCENODES and an element component named SOURCEELEMS are created
        automatically.
        """
        command = f"READ,{fname},{nskip},{format_},{xfield},{yfield},{zfield},{prfield},{pifield}"
        return self.run(command, **kwargs)



    def writemap(self, fname: str = "", **kwargs):
        r"""Writes interpolated pressure data to a file.

        Mechanical APDL Command: `WRITEMAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_WRITEMAP.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name.

        Notes
        -----

        .. _WRITEMAP_notes:

        Writes the interpolated pressure data to the specified file. The data is written as :ref:`sfe`
        commands applied to the ``SURF154``elements that are on the target surface. You may read this data
        for inclusion in an analysis by using :ref:`input`, ``Fname``.
        """
        command = f"WRITEMAP,{fname}"
        return self.run(command, **kwargs)



    def ftype(self, filetype: str = "", prestype: int | str = "", **kwargs):
        r"""Specifies the file type and pressure type for the subsequent import of source points and pressures.

        Mechanical APDL Command: `FTYPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FTYPE.html>`_

        Parameters
        ----------
        filetype : str
            Type of file from which the pressure data will be retrieved (no default):

            * ``CFXTBR`` - File from a CFX Transient Blade Row (TBR) analysis export.

            * ``CFDPOST`` - File from a CFD-Post BC Profile export.

            * ``FORMATTED`` - Formatted file.

            * ``CSV`` - Comma-Separated Values file.

        prestype : int or str
            Type of pressure data contained in the file:

            * ``0`` - Only real-valued pressures are on the file.

            * ``1`` - Real-valued and imaginary-valued pressures are on the file (default).

        Notes
        -----

        .. _FTYPE_notes:

        CFX Transient Blade Row files ( ``FileType`` = CFXTBR) are obtained from the **Export Results** Tab
        in CFX-Pre, with **[Export Surface Name]: Option** set to Harmonic Forced Response.

        CFD-Post files ( ``FileType`` = CFDPOST) are obtained from the **Export** action in CFD-Post with
        **Type** set to BC Profile.

        Formatted files ( ``FileType`` = FORMATTED) contain the coordinates and pressure data in fixed-
        format columns in the order x, y, z, pressure. You may have other columns of data in the file which
        can be skipped over in the ``Format`` specifier on the :ref:`read` command, but the data must be in
        that order.

        Comma-separated values files ( ``FileType`` = CSV) contain the coordinates and pressure data in
        comma-separated fields. The data can be in any order, and other fields of data may also be present.
        """
        command = f"FTYPE,{filetype},{prestype}"
        return self.run(command, **kwargs)


