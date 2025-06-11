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


class ResultsFiles:

    def delete(self, set_: str = "", nstart: str = "", nend: str = "", **kwargs):
        r"""Specifies sets in the results file to be deleted before postprocessing.

        Mechanical APDL Command: `DELETE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DELETE.html>`_

        Parameters
        ----------
        set_ : str
            Specifies that sets in the results file are to be deleted.

        nstart : str
            The first set in a results file to be deleted.

        nend : str
            The final set in a results file to be deleted. This field is used only if deleting more than one
            sequential sets.

        Notes
        -----
        :ref:`delete` is a specification command that flags sets in the results file for deletion. It should
        be followed by a :ref:`compress` command, the corresponding action command that deletes the
        specified sets.

        The :ref:`delete` command is valid only in the results file editing processor (auxiliary processor
        AUX3).
        """
        command = f"DELETE,{set_},{nstart},{nend}"
        return self.run(command, **kwargs)

    def list(self, **kwargs):
        r"""Lists out the sets in the results file.

        Mechanical APDL Command: `LIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LIST.html>`_

        Notes
        -----
        This command lists the results set number, the load step, substep, and time step for each set. It
        also shows all sets marked for deletion.

        The :ref:`list` command is valid only in the results file editing processor (auxiliary processor
        AUX3).
        """
        command = "LIST"
        return self.run(command, **kwargs)

    def aux3(self, **kwargs):
        r"""Enters the results file editing processor.

        Mechanical APDL Command: `/AUX3 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AUX3_sl.html>`_

        Notes
        -----
        Enters the results-file editing processor (auxiliary processor AUX3), used for editing Mechanical
        APDL
        results files.

        A pending :ref:`delete` is processed when :ref:`finish` or ``/EOF`` is issued. To cancel a pending
        :ref:`delete`, issue :ref:`undelete`.

        This command is valid only at the Begin Level.
        """
        command = "/AUX3"
        return self.run(command, **kwargs)

    def fileaux3(self, fname: str = "", ext: str = "", **kwargs):
        r"""Specifies the results file to be edited.

        Mechanical APDL Command: `FILEAUX3 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FILEAUX3.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to the current
            :file:`Jobname` if ``Ext`` is specified.

        ext : str
            Filename extension (eight-character maximum).

        Notes
        -----
        Specifies the results file to be edited.
        """
        command = f"FILEAUX3,{fname},{ext}"
        return self.run(command, **kwargs)

    def undelete(self, option: str = "", nstart: str = "", nend: str = "", **kwargs):
        r"""Removes results sets from the group of sets selected for editing.

        Mechanical APDL Command: `UNDELETE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_UNDELETE.html>`_

        Parameters
        ----------
        option : str
            Specifies which sets are to be removed from the selected sets.

            * ``SET`` - Specifies one or more particular sets in the results file that are to be removed from the group of
              sets selected for deletion.

            * ``ALL`` - Removes all selected sets that are currently selected for deletion.

        nstart : str
            The first set to be removed from the set selected for deletion.

        nend : str
            The final set to be removed from the set selected for deletion. This field is used only if
            operating on more than one sequential set.

        Notes
        -----
        Use this command if you have previously marked a set for deletion (with the :ref:`delete` command)
        and now wish to keep that set instead of deleting it.

        The :ref:`undelete` command is valid only in the results file editing processor (auxiliary processor
        AUX3), and, like the other AUX3 commands, it only affects the data steps index (DSI), time (TIM),
        loadstep, substep and cumulative step iteration (LSP) records in the results file.
        """
        command = f"UNDELETE,{option},{nstart},{nend}"
        return self.run(command, **kwargs)

    def compress(self, **kwargs):
        r"""Deletes all specified sets.

        Mechanical APDL Command: `COMPRESS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_COMPRESS.html>`_

        Notes
        -----
        Issue this command to delete all sets specified with the :ref:`delete` command.

        The :ref:`compress` command is valid only in the results file editing processor (auxiliary processor
        AUX3), and, like the other AUX3 commands, it only affects the data steps index (DSI), time (TIM),
        loadstep, substep and cumulative step iteration (LSP) records in the results file.
        """
        command = "COMPRESS"
        return self.run(command, **kwargs)

    def modify(
        self,
        set_: str = "",
        lstep: str = "",
        iter_: str = "",
        cumit: str = "",
        time: str = "",
        ktitle: int | str = "",
        **kwargs,
    ):
        r"""Changes the listed values of the data in a set.

        Mechanical APDL Command: `MODIFY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MODIFY.html>`_

        Parameters
        ----------
        set_ : str
            Set of data in results file to be modified.

        lstep : str
            The new load step number.

        iter_ : str
            The new load substep number.

        cumit : str
            The new cumulative iteration.

        time : str
            The new time/frequency value.

        ktitle : int or str
            Indicates if the set title should be modified.

            * ``0`` - Keep the original title.

            * ``1`` - Change the title to the title specified with the most current :ref:`title` command.

        Notes
        -----
        Use this command to change the listed values in a data set in a results file. Using this command
        does not change any actual model data; it affects only the values listed in the results file.

        The :ref:`modify` command is valid only in the results file editing processor (auxiliary processor
        AUX3), and, like the other AUX3 commands, it only affects the data steps index (DSI), time (TIM),
        loadstep, substep and cumulative step iteration (LSP) records in the results file.
        """
        command = f"MODIFY,{set_},{lstep},{iter_},{cumit},{time},{ktitle}"
        return self.run(command, **kwargs)
