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


class SolidBodyLoads(CommandsBase):

    def bfa(
        self,
        area: str = "",
        lab: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        **kwargs,
    ):
        r"""Defines a body-force load on an area.

        Mechanical APDL Command: `BFA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFA.html>`_

        Parameters
        ----------
        area : str
            Area to which body load applies. If ALL, apply to all selected areas ( :ref:`asel` ). A
            component name may also be substituted for ``Area``.

        lab : str
            Valid body load label. Load labels are listed under "Body Loads" in the input table for each
            element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        val1 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, CHRGD. For ``Lab`` = JS in magnetics, use
            ``VAL1``, ``VAL2``, and ``VAL3`` for the X, Y, and Z components. For ``Lab`` = IMPD in
            acoustics, ``VAL1`` is the resistance and ``VAL2`` is the reactance in ohms/square. When
            specifying a table name, you must enclose the table name in percent signs (%), e.g., :ref:`bfa`,
            ``Area``, ``Lab``,``tabname``. Use the :ref:`dim` command to define a table.

        val2 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, CHRGD. For ``Lab`` = JS in magnetics, use
            ``VAL1``, ``VAL2``, and ``VAL3`` for the X, Y, and Z components. For ``Lab`` = IMPD in
            acoustics, ``VAL1`` is the resistance and ``VAL2`` is the reactance in ohms/square. When
            specifying a table name, you must enclose the table name in percent signs (%), e.g., :ref:`bfa`,
            ``Area``, ``Lab``,``tabname``. Use the :ref:`dim` command to define a table.

        val3 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, CHRGD. For ``Lab`` = JS in magnetics, use
            ``VAL1``, ``VAL2``, and ``VAL3`` for the X, Y, and Z components. For ``Lab`` = IMPD in
            acoustics, ``VAL1`` is the resistance and ``VAL2`` is the reactance in ohms/square. When
            specifying a table name, you must enclose the table name in percent signs (%), e.g., :ref:`bfa`,
            ``Area``, ``Lab``,``tabname``. Use the :ref:`dim` command to define a table.

        val4 : str
            If ``Lab`` = JS, ``VAL4`` is the phase angle in degrees.

        Notes
        -----

        .. _BFA_notes:

        Defines a body-force load (such as temperature in a structural analysis, heat generation rate in a
        thermal analysis, etc.) on an area. Body loads may be transferred from areas to area elements (or to
        nodes if area elements do not exist) with the :ref:`bftran` or :ref:`sbctran` commands. Body loads
        default to the value specified on the :ref:`bfunif` command, if it was previously specified.

        You can specify a table name only when using temperature (TEMP) and heat generation rate (HGEN) body
        load labels.

        Body loads specified by the :ref:`bfa` command can conflict with other specified body loads. See
        Resolution of Conflicting Body Load Specifications in the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for details.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"BFA,{area},{lab},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def bfadele(self, area: str = "", lab: str = "", **kwargs):
        r"""Deletes body-force loads on an area.

        Mechanical APDL Command: `BFADELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFADELE.html>`_

        Parameters
        ----------
        area : str
            Area at which body load is to be deleted. If ALL, delete for all selected areas ( :ref:`asel` ).
            A component name may also be substituted for ``AREA``.

        lab : str
            Valid body load label. If ALL, use all appropriate labels. Load labels are listed under "Body
            Loads" in the input table for each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. See the
            :ref:`bfa` command for labels.

        Notes
        -----

        .. _BFADELE_notes:

        Deletes body-force loads (and all corresponding finite element loads) for a specified area and
        label. Body loads may be defined on an area with the :ref:`bfa` command.

        This command is also valid in PREP7.
        """
        command = f"BFADELE,{area},{lab}"
        return self.run(command, **kwargs)

    def bfalist(self, area: str = "", lab: str = "", **kwargs):
        r"""Lists the body-force loads on an area.

        Mechanical APDL Command: `BFALIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFALIST.html>`_

        Parameters
        ----------
        area : str
            Area at which body load is to be listed. If ALL (or blank), list for all selected areas (
            :ref:`asel` ). If ``AREA`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``AREA``.

        lab : str
            Valid body load label. If ALL, use all appropriate labels. Load labels are listed under "Body
            Loads" in the input table for each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. See the
            :ref:`bfa` command for labels.

        Notes
        -----

        .. _BFALIST_notes:

        Lists the body-force loads for the specified area and label. Body loads may be defined on an area
        with the :ref:`bfa` command.

        This command is valid in any processor.
        """
        command = f"BFALIST,{area},{lab}"
        return self.run(command, **kwargs)

    def bfk(
        self,
        kpoi: str = "",
        lab: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        phase: str = "",
        **kwargs,
    ):
        r"""Defines a body-force load at a keypoint.

        Mechanical APDL Command: `BFK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFK.html>`_

        Parameters
        ----------
        kpoi : str
            Keypoint to which body load applies. If ALL, apply to all selected keypoints ( :ref:`ksel` ). A
            component name may also be substituted for ``Kpoi``.

        lab : str
            Valid body load label. Load labels are listed under "Body Loads" in the input table for each
            element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

            All keypoints on a given area (or volume) must have the same :ref:`bfk` table name for the
            tables to be transferred to interior nodes.

        val1 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, MVDI and CHRGD. For magnetics, use ``VAL1``,
            ``VAL2``, and ``VAL3`` for the X, Y, and Z components of JS. For acoustics, if ``Lab`` = JS, use
            ``VAL1`` for mass source in a harmonic analysis or mass source rate in a transient analysis, and
            ignore ``VAL2`` and ``VAL3``. When specifying a table name, you must enclose the table name in
            percent signs (%), e.g., :ref:`bfk`, ``Kpoi``, ``Lab``,``tabname``. Use the :ref:`dim` command
            to define a table.

        val2 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, MVDI and CHRGD. For magnetics, use ``VAL1``,
            ``VAL2``, and ``VAL3`` for the X, Y, and Z components of JS. For acoustics, if ``Lab`` = JS, use
            ``VAL1`` for mass source in a harmonic analysis or mass source rate in a transient analysis, and
            ignore ``VAL2`` and ``VAL3``. When specifying a table name, you must enclose the table name in
            percent signs (%), e.g., :ref:`bfk`, ``Kpoi``, ``Lab``,``tabname``. Use the :ref:`dim` command
            to define a table.

        val3 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, MVDI and CHRGD. For magnetics, use ``VAL1``,
            ``VAL2``, and ``VAL3`` for the X, Y, and Z components of JS. For acoustics, if ``Lab`` = JS, use
            ``VAL1`` for mass source in a harmonic analysis or mass source rate in a transient analysis, and
            ignore ``VAL2`` and ``VAL3``. When specifying a table name, you must enclose the table name in
            percent signs (%), e.g., :ref:`bfk`, ``Kpoi``, ``Lab``,``tabname``. Use the :ref:`dim` command
            to define a table.

        phase : str
            Phase angle in degrees associated with the JS label.

        Notes
        -----

        .. _BFK_notes:

        Defines a body-force load (such as temperature in a structural analysis, heat generation rate in a
        thermal analysis, etc.) at a keypoint. Body loads may be transferred from keypoints to nodes with
        the :ref:`bftran` or :ref:`sbctran` commands. Interpolation will be used to apply loads to the nodes
        on the lines between keypoints. All keypoints on a given area (or volume) must have the same
        :ref:`bfk` specification, with the same values, for the loads to be transferred to interior nodes in
        the area (or volume). If only one keypoint on a line has a :ref:`bfk` specification, the other
        keypoint defaults to the value specified on the :ref:`bfunif` command.

        You can specify a table name only when using temperature (TEMP) and heat generation rate (HGEN) body
        load labels.

        Body loads specified by the :ref:`bfk` command can conflict with other specified body loads. See
        Resolution of Conflicting Body Load Specifications in the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for details.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"BFK,{kpoi},{lab},{val1},{val2},{val3},{phase}"
        return self.run(command, **kwargs)

    def bfkdele(self, kpoi: str = "", lab: str = "", **kwargs):
        r"""Deletes body-force loads at a keypoint.

        Mechanical APDL Command: `BFKDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFKDELE.html>`_

        Parameters
        ----------
        kpoi : str
            Keypoint at which body load is to be deleted. If ALL, delete for all selected keypoints (
            :ref:`ksel` ). A component name may also be substituted for ``KPOI``.

        lab : str
            Valid body load label. If ALL, use all appropriate labels. Load labels are listed under "Body
            Loads" in the input table for each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. See the
            :ref:`bfk` command for labels.

        Notes
        -----

        .. _BFKDELE_notes:

        Deletes body-force loads (and all corresponding finite element loads) for a specified keypoint and
        label. Body loads may be defined at a keypoint with the :ref:`bfk` command.

        This command is also valid in PREP7.
        """
        command = f"BFKDELE,{kpoi},{lab}"
        return self.run(command, **kwargs)

    def bfklist(self, kpoi: str = "", lab: str = "", **kwargs):
        r"""Lists the body-force loads at keypoints.

        Mechanical APDL Command: `BFKLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFKLIST.html>`_

        Parameters
        ----------
        kpoi : str
            Keypoint at which body load is to be listed. If ALL (or blank), list for all selected keypoints
            ( :ref:`ksel` ). If ``KPOI`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``KPOI``

        lab : str
            Valid body load label. If ALL, use all appropriate labels. Load labels are listed under "Body
            Loads" in the input table for each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. See the
            :ref:`bfk` command for labels.

        Notes
        -----

        .. _BFKLIST_notes:

        Lists the body-force loads for the specified keypoint and label. Keypoint body loads may be defined
        with the :ref:`bfk` command.

        This command is valid in any processor.
        """
        command = f"BFKLIST,{kpoi},{lab}"
        return self.run(command, **kwargs)

    def bfl(
        self,
        line: str = "",
        lab: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        **kwargs,
    ):
        r"""Defines a body-force load on a line.

        Mechanical APDL Command: `BFL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFL.html>`_

        Parameters
        ----------
        line : str
            Line to which body load applies. If ALL, apply to all selected lines ( :ref:`lsel` ). A
            component name may also be substituted for ``Line``.

        lab : str
            Valid body load label. Load labels are listed under "Body loads" in the input table for each
            element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        val1 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, and CHRGD. For acoustics, if ``Lab`` = JS,
            use ``VAL1`` for mass source in a harmonic analysis or mass source rate in a transient analysis,
            and ignore ``VAL2`` and ``VAL3``. When specifying a table name, you must enclose the table name
            in percent signs (%), for example, :ref:`bfl`, ``Line``, ``Lab``,``tabname``. Use the :ref:`dim`
            command to define a table.

        val2 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, and CHRGD. For acoustics, if ``Lab`` = JS,
            use ``VAL1`` for mass source in a harmonic analysis or mass source rate in a transient analysis,
            and ignore ``VAL2`` and ``VAL3``. When specifying a table name, you must enclose the table name
            in percent signs (%), for example, :ref:`bfl`, ``Line``, ``Lab``,``tabname``. Use the :ref:`dim`
            command to define a table.

        val3 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, and CHRGD. For acoustics, if ``Lab`` = JS,
            use ``VAL1`` for mass source in a harmonic analysis or mass source rate in a transient analysis,
            and ignore ``VAL2`` and ``VAL3``. When specifying a table name, you must enclose the table name
            in percent signs (%), for example, :ref:`bfl`, ``Line``, ``Lab``,``tabname``. Use the :ref:`dim`
            command to define a table.

        val4 : str
            If ``Lab`` = JS, ``VAL4`` is the phase angle in degrees.

        Notes
        -----

        .. _BFL_notes:

        Defines a body-force load (such as temperature in a structural analysis, heat generation rate in a
        thermal analysis, etc.) on a line. Body loads may be transferred from lines to line elements (or to
        nodes if line elements do not exist) with the :ref:`bftran` or :ref:`sbctran` commands.

        You can specify a table name only when using temperature (TEMP) and heat generation rate (HGEN) body
        load labels.

        Body loads specified by the :ref:`bfl` command can conflict with other specified body loads. See
        Resolution of Conflicting Body Load Specifications in the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for details.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"BFL,{line},{lab},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def bfldele(self, line: str = "", lab: str = "", **kwargs):
        r"""Deletes body-force loads on a line.

        Mechanical APDL Command: `BFLDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFLDELE.html>`_

        Parameters
        ----------
        line : str
            Line at which body load is to be deleted. If ALL, delete for all selected lines ( :ref:`lsel` ).
            A component name may also be substituted for ``LINE``.

        lab : str
            Valid body load label. If ALL, use all appropriate labels. Load labels are listed under "Body
            Loads" in the input table for each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. See the
            :ref:`bfl` command for labels.

        Notes
        -----

        .. _BFLDELE_notes:

        Deletes body-force loads (and all corresponding finite element loads) for a specified line and
        label. Body loads may be defined on a line with the :ref:`bfl` command.

        This command is also valid in PREP7.
        """
        command = f"BFLDELE,{line},{lab}"
        return self.run(command, **kwargs)

    def bfllist(self, line: str = "", lab: str = "", **kwargs):
        r"""Lists the body-force loads on a line.

        Mechanical APDL Command: `BFLLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFLLIST.html>`_

        Parameters
        ----------
        line : str
            Line at which body load is to be listed. If ALL (or blank), list for all selected lines (
            :ref:`lsel` ). If ``LINE`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``LINE``.

        lab : str
            Valid body load label. If ALL, use all appropriate labels. Load labels are listed under "Body
            Loads" in the input table for each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. See the
            :ref:`bfl` command for labels.

        Notes
        -----

        .. _BFLLIST_notes:

        Lists the body-force loads for the specified line and label. Body loads may be defined on a line
        with the :ref:`bfl` command.

        This command is valid in any processor.
        """
        command = f"BFLLIST,{line},{lab}"
        return self.run(command, **kwargs)

    def bftran(self, **kwargs):
        r"""Transfers solid model body-force loads to the finite element model.

        Mechanical APDL Command: `BFTRAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFTRAN.html>`_

        Notes
        -----

        .. _BFTRAN_notes:

        Body loads are transferred from selected keypoints and lines to selected nodes and from selected
        areas and volumes to selected elements. The :ref:`bftran` operation is also done if the
        :ref:`sbctran` command is either explicitly issued or automatically issued upon initiation of the
        solution calculations ( :ref:`solve` ).

        This command is also valid in PREP7.
        """
        command = "BFTRAN"
        return self.run(command, **kwargs)

    def bfv(
        self,
        volu: str = "",
        lab: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        phase: str = "",
        **kwargs,
    ):
        r"""Defines a body-force load on a volume.

        Mechanical APDL Command: `BFV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFV.html>`_

        Parameters
        ----------
        volu : str
            Volume to which body load applies. If ALL, apply to all selected volumes ( :ref:`vsel` ). A
            component name may also be substituted for ``Volu``.

        lab : str
            Valid body load label. Load labels are listed under "Body Loads" in the input table for each
            element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        val1 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, and CHRGD. Use ``VAL1``, ``VAL2``, and
            ``VAL3`` for the X, Y, and Z components of JS. For ``Lab`` = JS in magnetics, use ``VAL1``,
            ``VAL2``, and ``VAL3`` for the X, Y, and Z components. For acoustics, if ``Lab`` = JS, use
            ``VAL1`` for mass source in a harmonic analysis or mass source rate in a transient analysis, and
            ignore ``VAL2`` and ``VAL3``. When specifying a table name, you must enclose the table name in
            percent signs (%), e.g., :ref:`bfv`, ``Volu``, ``Lab``,``tabname``. Use the :ref:`dim` command
            to define a table.

        val2 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, and CHRGD. Use ``VAL1``, ``VAL2``, and
            ``VAL3`` for the X, Y, and Z components of JS. For ``Lab`` = JS in magnetics, use ``VAL1``,
            ``VAL2``, and ``VAL3`` for the X, Y, and Z components. For acoustics, if ``Lab`` = JS, use
            ``VAL1`` for mass source in a harmonic analysis or mass source rate in a transient analysis, and
            ignore ``VAL2`` and ``VAL3``. When specifying a table name, you must enclose the table name in
            percent signs (%), e.g., :ref:`bfv`, ``Volu``, ``Lab``,``tabname``. Use the :ref:`dim` command
            to define a table.

        val3 : str
            Value associated with the ``Lab`` item or a table name for specifying tabular boundary
            conditions. Use only ``VAL1`` for TEMP, FLUE, HGEN, and CHRGD. Use ``VAL1``, ``VAL2``, and
            ``VAL3`` for the X, Y, and Z components of JS. For ``Lab`` = JS in magnetics, use ``VAL1``,
            ``VAL2``, and ``VAL3`` for the X, Y, and Z components. For acoustics, if ``Lab`` = JS, use
            ``VAL1`` for mass source in a harmonic analysis or mass source rate in a transient analysis, and
            ignore ``VAL2`` and ``VAL3``. When specifying a table name, you must enclose the table name in
            percent signs (%), e.g., :ref:`bfv`, ``Volu``, ``Lab``,``tabname``. Use the :ref:`dim` command
            to define a table.

        phase : str
            Phase angle in degrees associated with the JS label.

        Notes
        -----

        .. _BFV_notes:

        Defines a body-force load (such as temperature in a structural analysis, heat generation rate in a
        thermal analysis, etc.) on a volume. Body loads may be transferred from volumes to volume elements
        (or to nodes if volume elements do not exist) with the :ref:`bftran` or :ref:`sbctran` commands.
        Body loads default to the value specified on the :ref:`bfunif` command, if it was previously
        specified.

        You can specify a table name only when using temperature (TEMP) and heat generation rate (HGEN) body
        load labels.

        Body loads specified by the :ref:`bfv` command can conflict with other specified body loads. See
        Resolution of Conflicting Body Load Specifications in the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for details.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"BFV,{volu},{lab},{val1},{val2},{val3},{phase}"
        return self.run(command, **kwargs)

    def bfvdele(self, volu: str = "", lab: str = "", **kwargs):
        r"""Deletes body-force loads on a volume.

        Mechanical APDL Command: `BFVDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFVDELE.html>`_

        Parameters
        ----------
        volu : str
            Volume at which body load is to be deleted. If ALL, delete for all selected volumes (
            :ref:`vsel` ). A component name may also be substituted for ``VOLU``.

        lab : str
            Valid body load label. If ALL, use all appropriate labels. Load labels are listed under "Body
            Loads" in the input table for each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. See the
            :ref:`bfv` command for labels.

        Notes
        -----

        .. _BFVDELE_notes:

        Deletes body-force loads (and all corresponding finite element loads) for a specified volume and
        label. Body loads may be defined on a volume with the :ref:`bfv` command.

        This command is also valid in PREP7.
        """
        command = f"BFVDELE,{volu},{lab}"
        return self.run(command, **kwargs)

    def bfvlist(self, volu: str = "", lab: str = "", **kwargs):
        r"""Lists the body-force loads on a volume.

        Mechanical APDL Command: `BFVLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFVLIST.html>`_

        Parameters
        ----------
        volu : str
            Volume at which body load is to be listed. If ALL (or blank), list for all selected volumes (
            :ref:`vsel` ). If ``VOLU`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``VOLU``.

        lab : str
            Valid body load label. If ALL, use all appropriate labels. Load labels are listed under "Body
            Loads" in the input table for each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. See the
            :ref:`bfv` command for labels.

        Notes
        -----

        .. _BFVLIST_notes:

        Lists the body-force loads for the specified volume and label. Body loads may be defined on a volume
        with the :ref:`bfv` command.

        This command is valid in any processor.
        """
        command = f"BFVLIST,{volu},{lab}"
        return self.run(command, **kwargs)
