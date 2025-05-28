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


class LoadStepOperations:

    def lswrite(self, lsnum: str = "", **kwargs):
        r"""Writes load and load step option data to a file.

        Mechanical APDL Command: `LSWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSWRITE.html>`_

        .. warning::

            This command must be run using :func:`non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`.
            Please visit `Unsupported Interactive Commands <https://mapdl.docs.pyansys.com/version/stable/user_guide/mapdl.html#unsupported-interactive-commands>`_
            for further information.

        Parameters
        ----------
        lsnum : str
            Number to be assigned to the load step file name for identification purposes. Defaults to 1 +
            highest ``LSNUM`` used in the current session. Issue :ref:`lswrite`,STAT to list the current
            value of ``LSNUM``. Issue :ref:`lswrite`,INIT to reset to 1. The load step file will be named
            :file:`Jobname.Sn`, where ``n`` is the specified ``LSNUM`` value (preceded by "0" for values
            1-9). On systems with a 3-character limit on the file name extension, the "S" is dropped for
            ``LSNUM`` > 99.

        Notes
        -----

        .. _LSWRITE_notes:

        Writes all load and load step option data for the selected model to a load step file for later use.
        :ref:`lswrite` does not capture changes made to real constants ( :ref:`r` ), material properties (
        :ref:`mp` ), couplings ( :ref:`cp` ), or constraint equations ( :ref:`ce` ).

        Solid model loads will not be saved if the model is not meshed. Solid model loads, if any, are
        transferred to the finite element model. Issue :ref:`lsclear`,FE to delete finite element loads.

        One file is written for each load step. Use the :ref:`lsread` command to read a single load step
        file, and the :ref:`lsdele` command to delete load step files. Use the :ref:`lssolve` command to
        read and solve the load steps sequentially.

        Solution control commands are typically not written to the file unless you specifically change a
        default solution setting.

        :ref:`lswrite` does not support the following commands: :ref:`dj`, :ref:`fj`, :ref:`gsbdata`,
        :ref:`gsgdata`, :ref:`estif`, :ref:`ekill`, :ref:`ealive`, :ref:`mpchg`, and :ref:`outres`. These
        commands will not be written to the load step file.

        :ref:`lswrite` cannot be used with the birth-death option.

        This command is also valid in PREP7.
        """
        command = f"LSWRITE,{lsnum}"
        return self.run(command, **kwargs)

    def lsdele(self, lsmin: str = "", lsmax: str = "", lsinc: str = "", **kwargs):
        r"""Deletes load step files.

        Mechanical APDL Command: `LSDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSDELE.html>`_

        Parameters
        ----------
        lsmin : str
            Range of load step files to be deleted, from ``LSMIN`` to ``LSMAX`` in steps of ``LSINC``.
            ``LSMAX`` defaults to ``LSMIN``, and ``LSINC`` defaults to 1. If ``LSMIN`` = ALL, all load step
            files are deleted (and ``LSMAX`` and ``LSINC`` are ignored). The load step files are assumed to
            be named :file:`Jobname.Sn`, where ``n`` is a number assigned by the :ref:`lswrite` command (01
            --09,10,11, etc.). On systems with a 3-character limit on the extension, the S is dropped for
            numbers > 99.

        lsmax : str
            Range of load step files to be deleted, from ``LSMIN`` to ``LSMAX`` in steps of ``LSINC``.
            ``LSMAX`` defaults to ``LSMIN``, and ``LSINC`` defaults to 1. If ``LSMIN`` = ALL, all load step
            files are deleted (and ``LSMAX`` and ``LSINC`` are ignored). The load step files are assumed to
            be named :file:`Jobname.Sn`, where ``n`` is a number assigned by the :ref:`lswrite` command (01
            --09,10,11, etc.). On systems with a 3-character limit on the extension, the S is dropped for
            numbers > 99.

        lsinc : str
            Range of load step files to be deleted, from ``LSMIN`` to ``LSMAX`` in steps of ``LSINC``.
            ``LSMAX`` defaults to ``LSMIN``, and ``LSINC`` defaults to 1. If ``LSMIN`` = ALL, all load step
            files are deleted (and ``LSMAX`` and ``LSINC`` are ignored). The load step files are assumed to
            be named :file:`Jobname.Sn`, where ``n`` is a number assigned by the :ref:`lswrite` command (01
            --09,10,11, etc.). On systems with a 3-character limit on the extension, the S is dropped for
            numbers > 99.

        Notes
        -----

        .. _LSDELE_notes:

        Deletes load step files in the current directory (written by the :ref:`lswrite` command).

        This command is also valid in PREP7.
        """
        command = f"LSDELE,{lsmin},{lsmax},{lsinc}"
        return self.run(command, **kwargs)

    def lsread(self, lsnum: str = "", **kwargs):
        r"""Reads load and load step option data into the database.

        Mechanical APDL Command: `LSREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSREAD.html>`_

        .. warning::

            This command must be run using :func:`non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`.
            Please visit `Unsupported Interactive Commands <https://mapdl.docs.pyansys.com/version/stable/user_guide/mapdl.html#unsupported-interactive-commands>`_
            for further information.

        Parameters
        ----------
        lsnum : str
            Identification number of the load step file to be read. Defaults to 1 + highest number read in
            the current session. Issue :ref:`lsread`,STAT to list the current value of ``LSNUM``. Issue
            :ref:`lsread`,INIT to reset ``LSNUM`` to 1. The load step files are assumed to be named
            :file:`Jobname.Sn`, where ``n`` is a number assigned by the :ref:`lswrite` command (01--
            09,10,11, etc.). On systems with a 3-character limit on the extension, the S is dropped for
            ``LSNUM`` > 99.

        Notes
        -----

        .. _LSREAD_notes:

        Reads load and load step option data from the load step file into the database. :ref:`lsread`  will
        not clear the database of all current loads. However, if a load is respecified with :ref:`lsread`,
        then it will overwrite the existing load. See the :ref:`lswrite` command to write load step files,
        and the :ref:`lsdele` command to delete load step files. :ref:`lsread` removes any existing
        :ref:`sfgrad` specification.

        This command is also valid in PREP7.
        """
        command = f"LSREAD,{lsnum}"
        return self.run(command, **kwargs)

    def lsclear(self, lab: str = "", **kwargs):
        r"""Clears loads and load step options from the database.

        Mechanical APDL Command: `LSCLEAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSCLEAR.html>`_

        Parameters
        ----------
        lab : str
            Label identifying the data to be cleared:

            * ``SOLID`` - Delete only solid model loads.

            * ``FE`` - Delete only finite element loads.

            * ``INER`` - Delete only inertia loads ( :ref:`acel`, etc.).

            * ``LFACT`` - Initialize only load factors (on :ref:`dcum`, :ref:`fcum`, :ref:`sfcum`, etc.).

            * ``LSOPT`` - Initialize only load step options.

            * ``ALL`` - Delete all loads and initialize all load step options and load factors.

        Notes
        -----

        .. _LSCLEAR_notes:

        Loads are deleted, and load step options are initialized to their default values.

        This command is also valid in PREP7.
        """
        command = f"LSCLEAR,{lab}"
        return self.run(command, **kwargs)

    def lssolve(self, lsmin: str = "", lsmax: str = "", lsinc: str = "", **kwargs):
        r"""Reads and solves multiple load steps.

        Mechanical APDL Command: `LSSOLVE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSSOLVE.html>`_

        Parameters
        ----------
        lsmin : str
            Range of load step files to be read and solved, from ``LSMIN`` to ``LSMAX`` in steps of
            ``LSINC``. ``LSMAX`` defaults to ``LSMIN``, and ``LSINC`` defaults to 1. If ``LSMIN`` is blank,
            a brief command description is displayed. The load step files are assumed to be named
            :file:`Jobname.Sn`, where ``n`` is a number assigned by the :ref:`lswrite` command (01--
            09,10,11, etc.). On systems with a 3-character limit on the extension, the S is dropped for
            numbers > 99.

        lsmax : str
            Range of load step files to be read and solved, from ``LSMIN`` to ``LSMAX`` in steps of
            ``LSINC``. ``LSMAX`` defaults to ``LSMIN``, and ``LSINC`` defaults to 1. If ``LSMIN`` is blank,
            a brief command description is displayed. The load step files are assumed to be named
            :file:`Jobname.Sn`, where ``n`` is a number assigned by the :ref:`lswrite` command (01--
            09,10,11, etc.). On systems with a 3-character limit on the extension, the S is dropped for
            numbers > 99.

        lsinc : str
            Range of load step files to be read and solved, from ``LSMIN`` to ``LSMAX`` in steps of
            ``LSINC``. ``LSMAX`` defaults to ``LSMIN``, and ``LSINC`` defaults to 1. If ``LSMIN`` is blank,
            a brief command description is displayed. The load step files are assumed to be named
            :file:`Jobname.Sn`, where ``n`` is a number assigned by the :ref:`lswrite` command (01--
            09,10,11, etc.). On systems with a 3-character limit on the extension, the S is dropped for
            numbers > 99.

        Notes
        -----

        .. _LSSOLVE_notes:

        This command invokes a Mechanical APDL macro ( :file:`LSSOLVE.MAC` ) to read and solve multiple load
        steps.

        The macro loops through a series of load step files written by the :ref:`lswrite` command.

        This command cannot be used with the birth-death option, does not support cyclic symmetry analysis,
        and does not support restarts.
        """
        command = f"LSSOLVE,{lsmin},{lsmax},{lsinc}"
        return self.run(command, **kwargs)
