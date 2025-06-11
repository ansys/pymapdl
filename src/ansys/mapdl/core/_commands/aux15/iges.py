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


class Iges:

    def igesin(self, fname: str = "", ext: str = "", **kwargs):
        r"""Transfers IGES data from a file into Mechanical APDL.

        Mechanical APDL Command: `IGESIN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_IGESIN.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to CAD if ``Fname`` is
            blank.

        Notes
        -----

        .. _IGESIN_notes:

        Reads a file containing IGES data and transfers it into the Mechanical APDL database. The file
        transferred
        is the IGES Version 5.1, ASCII format file. IGES (Initial Graphics Exchange Specification) is a
        neutral format developed by the U.S. Dept. of Commerce, National Institute of Standards and
        Technology. No output transfer file is written because the transferred data is read directly into
        the Mechanical APDL database.

        You can import multiple files into a single database, but you must use the same import option (set
        with the :ref:`ioptn` command) for each file.

        The :ref:`ioptn` command sets the parameters for reading the file. Files read via the SMOOTH method
        (the only available method) use the standard database.
        """
        command = f"IGESIN,{fname},{ext}"
        return self.run(command, **kwargs)

    def ioptn(self, lab: str = "", val1: str = "", **kwargs):
        r"""Controls options relating to importing a model.

        Mechanical APDL Command: `IOPTN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_IOPTN.html>`_

        Parameters
        ----------
        lab : str
            Label identifying the import option. The meaning of ``VAL1`` varies depending on ``Lab``.

            * ``STAT`` - List overall status of import facilities, including current option values. ``VAL1`` is ignored.

            * ``DEFA`` - Set default values for all import options. ``VAL1`` is ignored.

            * ``MERG`` - Entity merge option. ``VAL1`` can be:

              * ``YES`` - Automatic merging is performed (default).

              * ``NO`` - No merging of entities.

            * ``SOLID`` - Solid option. ``VAL1`` can be:

              * ``YES`` - Solid is created automatically (default).

              * ``NO`` - No solid created.

            * ``GTOLER`` - Entity merging tolerance. If IGES = SMOOTH, the GTOLER, ``VAL1`` can be:

              * ``DEFA`` - Use system defaults (default).

              * ``FILE`` - Use tolerance from the imported file.

              * ``n`` - A user-specified tolerance value.

            * ``IGES`` - IGES import option. ``VAL1`` can be:

              * ``STAT`` - List status of IGES related options in the output window.

              * ``SMOOTH (or RV52)`` - Use more robust IGES revision 5.2 import function (default).

            * ``SMALL`` - Small areas option. ``VAL1`` can be:

              * ``YES`` - Small areas are deleted (default).

              * ``NO`` - Small areas are retained.

        val1 : str
            Additional input value as described under each ``Lab`` option.

        Notes
        -----

        .. _IOPTN_notes:

        Controls various options during a model file transfer. A global solid model tolerance (GTOLER) can
        be specified.

        The SMALL,YES option (default) delete small areas and can cause geometrical inconsistencies that
        could cause the import process to abort. Retaining the small areas increases processor time and
        memory usage.

        The data is stored in the standard Mechanical APDL graphics database.

        The IGES,SMOOTH (default) option is capable of reading in any rational B-spline curve entity (type
        126), or rational B-spline surface entity (type 128) with a degree less than or equal to 20.
        Attempts to read in B-spline curve or surface entities of degree higher than 20 may result in error
        messages.

        If you issue the :ref:`clear` command, the :ref:`ioptn` settings return to their defaults.

        For MERG,YES, merging of coincident geometry items is performed automatically when the :ref:`igesin`
        command is issued (that is, an internal :ref:`nummrg`,KP command is issued). The model is merged
        with the consideration tolerance ( ``TOLER`` on :ref:`nummrg` ) set equal to 0.75 * the shortest
        distance between the endpoints of any active line. See the :ref:`nummrg` command for more
        information about the tolerances. In most cases, the default merging is appropriate. Use the
        :ref:`ioptn` command when you want to:

        Disable merging operations.
        Override the default merging and specify a global solid model tolerance value (GTOLER).
        Disable the automatic creation of solids (SOLID).

        The :ref:`ioptn` command should be issued before the :ref:`igesin` command. You cannot change these
        options after your model has been imported or created. If you must change the options: Clear the
        database ( :ref:`clear` ) or exit and restart the program.

        Set the correct options.

        Reimport or recreate the model.

        This command is valid in any processor.
        """
        command = f"IOPTN,{lab},{val1}"
        return self.run(command, **kwargs)

    def aux15(self, **kwargs):
        r"""Enters the IGES file transfer processor.

        Mechanical APDL Command: `/AUX15 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AUX15.html>`_

        Notes
        -----

        .. _s-AUX15_notes:

        Enters the IGES file-transfer processor (auxiliary processor AUX15), used to read an IGES data file
        into the Mechanical APDL program.

        This command is valid only at the Begin Level.
        """
        command = "/AUX15"
        return self.run(command, **kwargs)
