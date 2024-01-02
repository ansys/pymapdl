# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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


class Preparation:
    def rmndisp(self, loadt="", loc="", **kwargs):
        """Extracts neutral plane displacements from a test load or element load

        APDL Command: RMNDISP
        solution for the ROM method.

        Parameters
        ----------
        loadt
            Load type. Load type must be an alphanumeric string enclosed in
            single quotes. Valid load types are 'TLOAD' for the test load and
            'ELOAD' for the element load.

        loc
            Determines whether file will be overwritten or appended. Valid
            labels are 'WRITE' or 'APPEND'. Defaults to 'WRITE' for test load.

        Notes
        -----
        This command extracts the displacements at a neutral plane of a model.
        If  LoadT = 'TLOAD', extract displacements for a test load on a
        structure that represents the expected deflection state.  A test load
        is used to assist in the automatic mode selection for the ROM mode
        characterization. If LoadT = 'ELOAD', extract the neutral plane
        displacements for an element load that will be used in the use pass of
        a ROM analysis.  Typical element loads are gravity, and pressure
        loading. The element loads may be scaled [RMLVSCALE] during the use
        pass.

        The command requires a node component named "NEUN" to be defined. These
        nodes represent the nodes at the neutral plane of a structure (in the
        case of a stress-stiffened structure), or at any plane in the structure
        (non stress-stiffened case).

        For LoadT = 'TLOAD', node displacements are written to the file
        jobname.tld.  For LoadT = 'ELOAD', node displacements are written to
        the file jobname.eld. Up to 5 element load cases may be written to the
        file jobname.eld.

        This command is only valid in POST1.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMNDISP,{loadt},{loc}"
        return self.run(command, **kwargs)

    def rmnevec(self, **kwargs):
        """Extracts neutral plane eigenvectors from a modal analysis for the ROM

        APDL Command: RMNEVEC
        method.

        Notes
        -----
        This command extracts the eigenvectors at a neutral plane of a model
        from a modal analysis.  The modal analysis must have expanded modes
        [MXPAND] in order to process the data. Only the first 9 modes are
        considered.  The command requires a node component named "NEUN" to be
        defined. These nodes represent the nodes at the neutral plane of a
        structure (in the case of a stress-stiffened structure), or at any
        plane in the structure (non stress-stiffened case).

        This command is only valid in POST1.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.

        jobname.evx, jobname.evy, jobname.evz, jobname.evn, jobname.evl
        """
        command = f"RMNEVEC,"
        return self.run(command, **kwargs)
