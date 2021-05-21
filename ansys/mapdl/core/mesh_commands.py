"""Wraps commands for MAPDL meshing

Includes
N
CDWRITE


"""
import re

class _MapdlMeshingCommands():

    def n(self, node="", x="", y="", z="", thxy="", thyz="", thzx="",
          **kwargs) -> int:
        """Define a node.

        APDL Command: N

        Parameters
        ----------
        node
            Node number to be assigned.  A previously defined node of
            the same number will be redefined.  Defaults to the
            maximum node number used +1.

        x, y, z
            Node location in the active coordinate system (R, θ, Z for
            cylindrical, R, θ, Φ for spherical or toroidal).

        thxy
            First rotation about nodal Z (positive X toward Y).

        thyz
            Second rotation about nodal X (positive Y toward Z).

        thzx
            Third rotation about nodal Y (positive Z toward X).

        Returns
        -------
        int
            Node number of the generated node.

        Examples
        --------
        Create a node at ``(0, 1, 1)``

        >>> nnum = mapdl.n("", 0, 1, 1)
        >>> nnum
        1

        Create a node at ``(4, 5, 1)`` with a node ID of 10

        >>> nnum = mapdl.n(10, 4, 5, 1)
        >>> nnum
        10

        Notes
        -----
        Defines a node in the active coordinate system [CSYS].  The
        nodal coordinate system is parallel to the global Cartesian
        system unless rotated.  Rotation angles are in degrees and
        redefine any previous rotation angles.  See the NMODIF, NANG,
        NROTAT, and NORA commands for other rotation options.
        """
        command = f"N,{node},{x},{y},{z},{thxy},{thyz},{thzx}"
        msg = self.run(command, **kwargs)
        if msg:
            res = re.search(r"(NODE\s*)([0-9]+)", msg)
            if res is not None:
                return int(res.group(2))
