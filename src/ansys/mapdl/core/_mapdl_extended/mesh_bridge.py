# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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

"""The mesh bridge MAPDL extended mixin."""

from collections.abc import Mapping, Sequence
from pathlib import Path
import tempfile
from typing import TYPE_CHECKING, Any, Literal, TypeAlias

import numpy as np
from numpy.typing import NDArray

from ansys.mapdl.core.misc import random_string

from . import _ExtendedMixinBase

if TYPE_CHECKING:
    import pyvista as pv

_IntAttribute: TypeAlias = int | Sequence[int] | NDArray[np.integer] | None


class _ExtendedMeshBridgeMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    def load_mesh(
        self,
        mesh: "pv.DataSet | tuple[Any, Any] | str | Path | Any",
        *,
        etype: str | int | Mapping[Any, str | int] | None = None,
        mat: _IntAttribute = None,
        real: _IntAttribute = None,
        secnum: _IntAttribute = None,
        esys: _IntAttribute = None,
        keyopt: Mapping[int, int] | None = None,
        components: Mapping[str, Any] | None = None,
        include_components: bool = True,
        keep_boundary_elements: bool = False,
        sanitize_names: bool = False,
        on_conflict: Literal["error", "replace", "append"] = "error",
        node_ids: Sequence[int] | NDArray[np.integer] | None = None,
        elem_ids: Sequence[int] | NDArray[np.integer] | None = None,
    ) -> Any:
        """Load an external finite-element mesh and its Mesh Components.

        The mesh is converted into a standalone Mesh Archive (``ET``,
        ``KEYOPT``, ``NBLOCK``, ``EBLOCK``, and ``CMBLOCK`` blocks) and read
        with ``CDREAD,DB`` inside ``/PREP7``. Materials, sections, real
        constants, and coordinate systems already defined in the database
        are kept. Linear and quadratic point, line, shell, planar, and solid
        cells are supported, including degenerate shapes (triangles,
        tetrahedra, pyramids, and wedges) written in Mechanical APDL node
        order.

        When the mesh mixes cells of several dimensions, such as a Gmsh
        tetrahedral mesh with tagged boundary triangles, only the cells of the
        highest dimension become elements by default. Boolean cell masks,
        ``meshio`` cell sets, and Gmsh physical groups on the dropped
        lower-dimensional cells become ``NODE`` Mesh Components holding the
        nodes of those cells. All nodes are created.

        Parameters
        ----------
        mesh : pyvista.DataSet, meshio.Mesh, tuple, str, or pathlib.Path
            Mesh to load.

            * :class:`pyvista.DataSet`: an unstructured grid is used as is,
              and other datasets are cast to one. The ``ansys_node_num``,
              ``ansys_elem_num``, ``ansys_etype``, ``ansys_elem_type_num``,
              ``ansys_material_type``, ``ansys_real_constant``,
              ``ansys_secnum``, and ``ansys_esys`` arrays and the
              ``ansys_keyopt`` field array, such as those on
              ``mapdl.mesh.grid``, are reused when valid. Points whose
              ``ansys_node_num`` is ``-1`` are omitted midside nodes: they are
              not created as nodes and are written as ``0`` in element
              connectivity.
            * ``meshio.Mesh``: ``point_sets`` become ``NODE`` Mesh Components,
              and ``cell_sets`` and Gmsh physical groups (``field_data`` names
              with ``gmsh:physical`` cell data) become ``ELEM`` Mesh
              Components. The mesh is not modified.
            * ``(nodes, elements)`` tuple: ``(N, 2)`` or ``(N, 3)`` node
              coordinates, with ``z = 0`` for 2D nodes, and the elements as a
              2D array or a sequence of 1D arrays of 0-based node indices.
              Elements with 3, 4, 6, or 8 nodes are ambiguous (for example
              ``QUAD`` or ``TETRA``) and require ``etype``.
            * File path: ``.cdb`` and ``.inp`` files, including files written
              by ``CDWRITE``, are read with their element types, ``KEYOPT``
              values, attributes, and Mesh Components, and only their mesh is
              loaded. ``.vtk``, ``.vtu``, ``.vtp``, and ``.pvtu`` files are read
              with PyVista. Other formats, such as ``.msh``, ``.xdmf``, or
              ``.med``, are read with the optional ``meshio`` package.

        etype : str, int, or Mapping, optional
            Element type of the new elements.

            * ``None`` (default): reuse ``ansys_etype`` and
              ``ansys_elem_type_num`` when present on ``mesh``. Otherwise,
              assign structural defaults by cell type: ``MASS21`` for
              vertices, ``BEAM188``/``BEAM189`` for lines, ``SHELL181``/
              ``SHELL281`` for triangles and quadrilaterals, ``SOLID185`` for
              linear solids, ``SOLID186`` for quadratic hexahedra, wedges, and
              pyramids, and ``SOLID187`` for quadratic tetrahedra.
            * ``str``: element name or number, such as ``"SOLID187"``,
              ``"PLANE183"``, or ``"187"``, defined as a new ``ET`` entry.
            * ``int``: ID of an element type already defined in the database
              with ``ET``.
            * ``Mapping``: per cell type element types. Keys are
              :class:`pyvista.CellType` members, VTK cell type integers, or
              ``meshio`` cell type names such as ``"tetra10"`` or
              ``"hexahedron20"``. Values follow the ``str`` and ``int`` rules
              above. Unmapped cell types use the structural defaults.

        mat, real, secnum : int or sequence of int, optional
            Material, real constant, and section IDs, either one value for all
            elements or one value per cell. Per cell values may cover every
            input cell or only the cells loaded as elements. When omitted, the
            matching ``ansys_*`` cell array is reused if valid, otherwise ``1``.

        esys : int or sequence of int, optional
            Element coordinate system IDs, either one value for all elements
            or one value per cell, like ``mat``. When omitted, ``ansys_esys``
            is reused if valid, otherwise ``0``.

        keyopt : Mapping[int, int], optional
            ``KEYOPT`` values, keyed by key option number (1 to 18), applied
            to every new element type.

        components : Mapping[str, Any], optional
            Additional Mesh Components. Each value is either a sequence of node
            IDs, a boolean mask over the mesh points, or a ``(type, ids)`` tuple
            where ``type`` is ``"NODE"`` or ``"ELEM"`` and ``ids`` is a sequence
            of IDs or a boolean mask over the points or the loaded elements.
            These components replace embedded components with the same name.

        include_components : bool, default: True
            Whether to create ``NODE`` Mesh Components from boolean (or ``0``/``1``
            ``uint8``) point arrays and ``ELEM`` Mesh Components from boolean cell
            arrays. Internal arrays (``origid``, ``VTKorigID``, and names
            starting with ``vtk`` or ``ansys_``) are ignored.

        keep_boundary_elements : bool, default: False
            Whether to load lower-dimensional cells of a mixed-dimension mesh
            as elements instead of converting their groups to ``NODE`` Mesh
            Components. Lower-dimensional cell types mapped in an ``etype``
            mapping, and meshes carrying ``ansys_etype`` and
            ``ansys_elem_type_num`` arrays, are always loaded as elements.

        sanitize_names : bool, default: False
            Whether to convert invalid component names into valid Mechanical
            APDL names by replacing invalid characters with ``_``, prefixing
            names that do not start with a letter with ``C_``, and truncating
            them to 32 characters. Names are always converted to uppercase.

        on_conflict : str, default: "error"
            Behavior when nodes or elements already exist in the database.

            * ``"error"``: raise a ``ValueError``.
            * ``"replace"``: delete all existing elements, nodes, and ``NODE``
              and ``ELEM`` Mesh Components first.
            * ``"append"``: offset incoming node and element IDs above the
              highest existing IDs.

            New element type IDs always start above the highest element type
            ID already defined.

        node_ids : sequence of int, optional
            Unique positive node IDs, one per point. They replace
            ``ansys_node_num``. By default, nodes are numbered from 1.

        elem_ids : sequence of int, optional
            Unique positive element IDs, one per input cell or per loaded
            element. They replace ``ansys_elem_num``. By default, elements are
            numbered from 1.

        Returns
        -------
        ansys.mapdl.core.mesh_grpc.MeshGrpc or ansys.mapdl.reader.Archive
            The updated :attr:`Mapdl.mesh <ansys.mapdl.core.Mapdl.mesh>`.

        Raises
        ------
        TypeError
            If ``mesh`` is not a supported mesh type.
        FileNotFoundError
            If the ``mesh`` file does not exist.
        ImportError
            If reading the ``mesh`` file requires ``meshio`` and it is not
            installed.
        ValueError
            If a cell type is unsupported or incompatible with its element
            type, raw element node counts are ambiguous without ``etype``, raw
            element node indices are out of range, an ``int`` element type is
            not defined, an attribute or ID array has the wrong length, a
            component name is invalid or duplicated, a group contains both
            elements and dropped lower-dimensional cells, a component
            references IDs that are not in the mesh, or nodes or elements
            already exist and ``on_conflict="error"``.

        Examples
        --------
        Load a tetrahedral mesh as ``SOLID185`` elements with a ``NODE``
        Mesh Component on its bottom face.

        >>> import pyvista as pv
        >>> grid = pv.ImageData(dimensions=(3, 3, 3)).triangulate()
        >>> fixed = grid.points[:, 2] == 0
        >>> mesh = mapdl.load_mesh(grid, components={"FIXED": fixed})
        >>> mesh.n_node
        27

        Load quadratic tetrahedra as ``SOLID187`` elements with material 2.

        >>> tet10 = pv.examples.cells.QuadraticTetra()
        >>> mapdl.load_mesh(tet10, etype="SOLID187", mat=2, on_conflict="replace")

        Append a second mesh that uses an element type already defined.

        >>> mapdl.et(10, "SOLID185")
        >>> mapdl.load_mesh(
        ...     pv.ImageData(dimensions=(3, 3, 3)), etype=10, on_conflict="append"
        ... )

        Load a Gmsh mesh. Physical volumes become ``ELEM`` Mesh Components and
        physical surfaces become ``NODE`` Mesh Components.

        >>> mapdl.load_mesh("part.msh", etype="SOLID187", on_conflict="replace")

        Load two ``PLANE182`` quadrilaterals from NumPy arrays.

        >>> nodes = [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]]
        >>> elements = [[0, 1, 4, 3], [1, 2, 5, 4]]
        >>> mapdl.load_mesh(
        ...     (nodes, elements), etype="PLANE182", on_conflict="replace"
        ... )
        """
        from ansys.mapdl.core.mesh.bridge import (
            _as_grid,
            _existing_etype_ids,
            _mesh_data_from_grid,
            _offset_ids,
            write_mesh_archive,
        )

        if on_conflict not in ("error", "replace", "append"):
            raise ValueError(
                "`on_conflict` must be 'error', 'replace', or 'append', "
                f"not {on_conflict!r}."
            )

        wanted = _existing_etype_ids(etype)
        # ``*GET,,ETYP,<id>,ATTR,ENAM`` warns on undefined IDs, so read ``ekey`` instead.
        defined = {int(i): int(n) for i, n in self.mesh.ekey} if wanted else {}
        if missing := sorted(wanted - defined.keys()):
            raise ValueError(
                f"Element type IDs {missing} are not defined. Define them with "
                "`mapdl.et` or pass an element name such as 'SOLID187'."
            )
        existing_etypes = {et_id: defined[et_id] for et_id in wanted}
        grid = _as_grid(mesh, etype, existing_etypes)

        # ``NUM,MAXD`` is the highest ID defined, independent of the selection.
        node_max = int(self.get_value("NODE", 0, "NUM", "MAXD"))
        elem_max = int(self.get_value("ELEM", 0, "NUM", "MAXD"))
        if on_conflict == "error" and (node_max or elem_max):
            raise ValueError(
                "Nodes or elements already exist in the database. Pass "
                "`on_conflict='replace'` to delete them first or "
                "`on_conflict='append'` to add the new mesh after them."
            )

        data = _mesh_data_from_grid(
            grid,
            etype=etype,
            existing_etypes=existing_etypes,
            et_offset=int(self.get_value("ETYP", 0, "NUM", "MAX")),
            mat=mat,
            real=real,
            secnum=secnum,
            esys=esys,
            keyopt=keyopt,
            components=components,
            include_components=include_components,
            keep_boundary_elements=keep_boundary_elements,
            sanitize_names=sanitize_names,
            node_ids=node_ids,
            elem_ids=elem_ids,
        )
        if on_conflict == "append":
            _offset_ids(data, node_max, elem_max)

        self.prep7(mute=True)
        if on_conflict == "replace" and (node_max or elem_max):
            self.allsel(mute=True)
            self.cmsel("ALL", mute=True)
            for name, kind in list(self.components.items()):
                if kind in ("NODE", "ELEM"):
                    self.cmdele(name, mute=True)
            self.edele("ALL", mute=True)
            self.ndele("ALL", mute=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            cdb_path = Path(tmpdir) / f"_load_mesh_{random_string()}.cdb"
            write_mesh_archive(data, cdb_path)
            self.cdread("DB", str(cdb_path))
        self._reset_cache()
        return self.mesh
