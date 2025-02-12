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


class BinaryFileDump:

    def dump(self, nstrt: str = "", nstop: str = "", **kwargs):
        r"""Dumps the contents of a binary file.

        Mechanical APDL Command: `DUMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DUMP.html>`_

        Parameters
        ----------
        nstrt : str
            Dump file from record ``NSTRT`` (defaults to 1) to ``NSTOP`` (defaults to ``NSTRT`` ). If
            ``NSTRT`` = HEAD, dump only record 1 of the file ( ``NSTOP`` and the format specification are
            ignored). If ``NSTRT`` = ALL, dump the entire file.

        nstop : str
            Dump file from record ``NSTRT`` (defaults to 1) to ``NSTOP`` (defaults to ``NSTRT`` ). If
            ``NSTRT`` = HEAD, dump only record 1 of the file ( ``NSTOP`` and the format specification are
            ignored). If ``NSTRT`` = ALL, dump the entire file.

        Notes
        -----
        Dumps the file named on the AUX2 :ref:`fileaux2` command according the format specified on the
        :ref:`form` command.
        """
        command = f"DUMP,{nstrt},{nstop}"
        return self.run(command, **kwargs)

    def aux2(self, **kwargs):
        r"""Enters the binary file dumping processor.

        Mechanical APDL Command: `/AUX2 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AUX2.html>`_

        Notes
        -----
        Enters the binary file-dumping processor (auxiliary processor AUX2), used for dumping the contents
        of certain Mechanical APDL binary files for visual examination.

        This command is valid only at the Begin Level.
        """
        command = "/AUX2"
        return self.run(command, **kwargs)

    def form(self, lab: str = "", **kwargs):
        r"""Specifies the format of the file dump.

        Mechanical APDL Command: `FORM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FORM.html>`_

        Parameters
        ----------
        lab : str
            Format:

            * ``RECO`` - Basic record description only (minimum output) (default).

            * ``TEN`` - Same as RECO plus the first ten words of each record.

            * ``LONG`` - Same as RECO plus all words of each record.

        Notes
        -----
        Specifies the format of the file dump (from the :ref:`dump` command).
        """
        command = f"FORM,{lab}"
        return self.run(command, **kwargs)

    def fileaux2(self, fname: str = "", ident: str = "", **kwargs):
        r"""Specifies the binary file to be dumped.

        Mechanical APDL Command: `FILEAUX2 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FILEAUX2.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to the current
            :file:`Jobname` if ``Ident`` is specified.

        ident : str
            File name identifier. See the `Basic Analysis Guide
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for file
            descriptions and identifiers. If not an identifier, the program uses ``Ident`` as the file name
            extension.

        Notes
        -----
        Specifies the binary file to be dumped with the :ref:`dump` command.
        """
        command = f"FILEAUX2,{fname},{ident}"
        return self.run(command, **kwargs)

    def ptr(
        self, loc: str = "", base: str = "", loch: str = "", baseh: str = "", **kwargs
    ):
        r"""Dumps the record of a binary file.

        Mechanical APDL Command: `PTR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PTR.html>`_

        Parameters
        ----------
        loc : str
            Dump the file record starting at pointer ``LOC``. ``BASE`` is the base pointer, and would be
            used if ``LOC`` is a relative pointer.

        base : str
            Dump the file record starting at pointer ``LOC``. ``BASE`` is the base pointer, and would be
            used if ``LOC`` is a relative pointer.

        loch : str
            Second 32-bit integer (if required) for defining the 64-bit pointer.

        baseh : str
            Second 32-bit integer (if required) for defining the 64-bit pointer.

        Notes
        -----
        Dumps the record of the file named on the AUX2 :ref:`fileaux2` command according the format
        specified on the :ref:`form` command.
        """
        command = f"PTR,{loc},{base},{loch},{baseh}"
        return self.run(command, **kwargs)
