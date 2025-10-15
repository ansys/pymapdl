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

class HardPoints:

    def hptcreate(self, type_: str = "", entity: str = "", nhp: str = "", label: str = "", val1: str = "", val2: str = "", val3: str = "", **kwargs):
        r"""Defines a hard point.

        Mechanical APDL Command: `HPTCREATE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HPTCREATE.html>`_

        Parameters
        ----------
        type_ : str
            Type of entity on which the hard point will be created.

            * ``LINE`` - Hard point will be created on a line.

            * ``AREA`` - Hard point will be created within an area (not on the boundaries).

        entity : str
            Number of the line or area on which the hard point will be created.

        nhp : str
            Number assigned to the hard point. Defaults to the lowest available hard point number.

        label : str
            If ``LABEL`` = COORD, ``VAL1``, ``VAL2``, and ``VAL3`` are the respective global X, Y, and Z
            coordinates. If ``LABEL`` = RATIO, ``VAL`` 1 is the parameter value (this is available only for
            lines). Valid parameter values are between 0 and 1. ``VAL2`` and ``VAL3`` are ignored.

        val1 : str
            If ``LABEL`` = RATIO, ratio value for line. If ``LABEL`` = COORD, global X coordinate value.

        val2 : str
            If ``LABEL`` = COORD, global Y coordinate value.

        val3 : str
            If ``LABEL`` = COORD, global Z coordinate value.

        Notes
        -----

        .. _HPTCREATE_notes:

        The ability to enter a parameter value provides a simple way of positioning hard points on lines.
        For example, to place a hard point halfway along a line, one can simply specify a ``VAL1`` value of
        0.5.

        For models imported through the DEFAULT IGES filter, you can place hard points on models only by
        specifying coordinates (you can't place a hard point using interactive picking).

        If you issue any commands that update the geometry of an entity, such as Boolean or simplification
        commands, any hard points associated with that entity are deleted. Therefore, you should add any
        hard points after completing the solid model. If you delete an entity that has associated hard
        points, those hard points are either

        * Deleted along with the entity (if the hard point is not associated with any other entities).

        * Detached from the deleted entity (if the hard point is associated with additional entities).

        When archiving your model ( :ref:`cdwrite` ), hardpoint information cannot be written to the IGES
        file. The :file:`Jobname.cdb` file can be written with the :ref:`cdwrite`,DB option.

        Hard points are only applicable for area and volume meshing, not for beams.
        """
        command = f"HPTCREATE,{type_},{entity},{nhp},{label},{val1},{val2},{val3}"
        return self.run(command, **kwargs)



    def hptdelete(self, np1: str = "", np2: str = "", ninc: str = "", **kwargs):
        r"""Deletes selected hardpoints.

        Mechanical APDL Command: `HPTDELETE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HPTDELETE.html>`_

        Parameters
        ----------
        np1 : str
            Delete the pattern of hard points beginning with ``NP1`` to ``NP2`` in steps of ``NINC``
            (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and the pattern is all
            selected hard points ( :ref:`ksel` ). If ``NP1`` = P, graphical picking is enabled and all
            remaining command fields are ignored.

        np2 : str
            Delete the pattern of hard points beginning with ``NP1`` to ``NP2`` in steps of ``NINC``
            (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and the pattern is all
            selected hard points ( :ref:`ksel` ). If ``NP1`` = P, graphical picking is enabled and all
            remaining command fields are ignored.

        ninc : str
            Delete the pattern of hard points beginning with ``NP1`` to ``NP2`` in steps of ``NINC``
            (defaults to 1). If ``NP1`` = ALL, ``NP2`` and ``NINC`` are ignored and the pattern is all
            selected hard points ( :ref:`ksel` ). If ``NP1`` = P, graphical picking is enabled and all
            remaining command fields are ignored.

        Notes
        -----

        .. _HPTDELETE_notes:

        Deletes all attributes attached to the designated hard points as well as the hard points themselves.
        If any entity is attached to a designated hard point, the command detaches the hard point from that
        entity (the program will alert you that this will occur).
        """
        command = f"HPTDELETE,{np1},{np2},{ninc}"
        return self.run(command, **kwargs)


