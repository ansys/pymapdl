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

from ansys.mapdl.core._commands import CommandsBase


class BinaryFileManipulation(CommandsBase):

    def combine(self, filetype: str = "", num: str = "", **kwargs):
        r"""Combines distributed memory parallel ( DMP ) files.

        Mechanical APDL Command: `COMBINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_COMBINE.html>`_

        Parameters
        ----------
        filetype : str
            Type of solution file to combine. There is no default; if (blank), the command is ignored.

            * ``RST`` - Structural results file ( :file:`.RST` )

            * ``RTH`` - Thermal results file ( :file:`.RTH` )

            * ``RMG`` - Magnetics results file ( :file:`.RMG` )

            * ``RSTP`` - Linear perturbation results file ( :file:`.RSTP` )

            * ``EMAT`` - Element matrix file ( :file:`.EMAT` ).

            * ``ESAV`` - Element saved data file ( :file:`.ESAV` )

            * ``MODE`` - Modal results file ( :file:`.MODE` )

            * ``MLV`` - Modal load vector file ( :file:`.MLV` )

            * ``IST`` - Initial state file ( :file:`.IST` )

            * ``FULL`` - Full matrix file ( :file:`.FULL` )

            * ``RFRQ`` - Reduced complex displacement file ( :file:`.RFRQ` )

            * ``RDSP`` - Reduced displacement file ( :file:`.RDSP` )

            * ``RNNN`` - Multiframe restart files ( :file:`.Rnnn` )

        num : str
            Number of :file:`.Rnnn` files to combine:

            * ``ALL`` - Combine all :file:`.Rnnn` files (default).

            * ``N`` - Combine only :file:`.RN` files, where N is an integer from 1 to 999.

        Notes
        -----

        .. _COMBINE_notes:

        The :ref:`combine` command is used within the AUX2 auxiliary processor to combine local solution
        files from a distributed memory parallel solution into a single, global file. Before using this
        command, you must enter the AUX2 processor by issuing the :ref:`aux2` command.

        In a distributed-memory parallel ( DMP ) solution, you can use the :ref:`dmpoption` command to
        bypass the file combination step, causing all individual local files to be kept on the local disks
        in the current working directory. Later on, you can start a new distributed memory parallel solution
        and use the :ref:`combine` command to combine local files into a global file for a downstream
        solution or another operation (such as postprocessing with :ref:`post1` ). For example, the command
        :ref:`combine`,RST will combine local results files ( :file:`JobnameN.RST` ) into a global results
        file ( :file:`Jobname.RST` ).

        The :ref:`combine` command cannot be used to combine local files generated during a distributed
        memory parallel solution that used the frequency or cyclic harmonic index domain decomposition
        method ( :ref:`ddoption`,FREQ or :ref:`ddoption`,CYCHI).

        If :ref:`combine`,RNNN is specified, all of the multiframe restart files named :file:`Jobname.R001`
        to :file:`Jobname.R999` will automatically be combined. To combine only one set of :file:`.Rnnn`
        restart files, place only that set of restart files in your current working directory, or use the
        ``NUM`` argument to specify which set of :file:`.Rnnn` files to combine.

        When the :ref:`combine` command is used in a subsequent distributed memory parallel (DMP) session,
        the number of processors must be the same as in the DMP solution that generated the files.

        When running on a cluster, the local solution files must be available in the working directory on
        each node in the subsequent session. As an example, consider the following command line used to
        generate local solution files:

        .. code:: apdl

           ansys232 -dis -machines machine1: 4: machine2: 1: machine3: 2-i input -o output

        Different machines can be used in the subsequent session to combine these files. However, the total
        number of cores must remain unchanged (seven in the above case), and the local files must be copied
        to the working directory (or directories) on each of the machines used in the subsequent session.
        """
        command = f"COMBINE,{filetype},{num}"
        return self.run(command, **kwargs)

    def hbmat(
        self,
        fname: str = "",
        ext: str = "",
        form: str = "",
        matrx: str = "",
        rhs: str = "",
        mapping: str = "",
        **kwargs,
    ):
        r"""Writes an assembled global matrix in Harwell-Boeing format.

        Mechanical APDL Command: `HBMAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HBMAT.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. Defaults to the current Jobname if left blank.

        ext : str
            Filename extension (eight-character maximum). Defaults to :file:`.matrix` if left blank.

        form : str
            Specifies format of output matrix file:

            * ``ASCII`` - Write output matrix file in ASCII form.

            * ``BIN`` - Write output matrix file in binary form.

        matrx : str
            Specify which matrix to write to the output matrix file:

            * ``STIFF`` - Write stiffness matrix to output matrix file. Valid for all types of analyses that
              write a :file:`.full` file.

            * ``MASS`` - Write mass matrix to output matrix file. Valid for buckling, substructure, and modal
              analyses. If :file:`.full` file was generated in a buckling analysis, then this label will write
              stress stiffening matrix to output matrix file.

            * ``DAMP`` - Write damping matrix to output matrix file. Only valid for damped modal analyses.

        rhs : str
            Specifies whether to write the right-hand side vector to output matrix file:

            * ``YES`` - Write right-hand side vector to output matrix file.

            * ``NO`` - Do not write right-hand side vector to output matrix file.

        mapping : str
            Specifies whether to write the mapping file. This file is always named :file:`Fnamemapping`.

            * ``YES`` - Write the mapping file.

            * ``NO`` - Do not write the mapping file (default).

        Notes
        -----

        .. _HBMAT_notes:

        This command copies a matrix from the assembled global matrix file ( :file:`.full` file) or from the
        superelement matrix file ( :file:`.sub` file) as specified on the :ref:`fileaux2` command and write
        it in Harwell-Boeing format to a new file named :file:`Jobname.matrix`. The Harwell-Boeing format is
        widely used by other applications that deal with matrices.

        The assembled global matrix file is created during solution depending on the analysis type, equation
        solver, and other solution options. By default, the assembled global matrix file is never deleted at
        the end of solution. For most analysis types, the Sparse direct solver and the ICCG solver will
        write a :file:`.full` file. All mode extraction methods used for buckling and modal analyses will
        write a properly formatted :file:`.full` file to be used with the :ref:`hbmat` command. However,
        when using distributed-memory parallel (DMP) processing, a majority of analyses will write a
        distributed (or local) form of the :file:`.full` file which is not currently supported by the
        :ref:`hbmat` command.

        When dumping the stiffness matrix for transient and harmonic analyses, be aware that the element
        mass matrix values (and possibly element damping matrix values) are incorporated into the globally
        assembled stiffness matrix. Thus, the globally assembled stiffness matrix represents more than the
        stiffness of the model for these analysis types. Please refer to the `Mechanical APDL Theory
        Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_ for
        more details.

        When dumping a :file:`.full` file, the rows and columns corresponding to specified constraints (for
        example, :ref:`d` commands) are eliminated from the system of equations and therefore are not
        written to the :file:`.matrix` file. Also, rows and columns corresponding to eliminated (dependent)
        degrees of freedom from coupling and/or constraint equations (for example, :ref:`ce`, :ref:`cp`
        commands) are also eliminated from the system of equations and are not written to the
        :file:`.matrix` file. The DOFs that are eliminated from any coupling and/or constraint equations are
        determined internally by the solution code and may not match what you specified via the :ref:`ce` /
        :ref:`cp` (or similar) commands.

        When dumping a :file:`.sub` file, the full ``n`` x ``n`` matrix will be written to the
        :file:`.matrix` file for either symmetric or unsymmetric matrices, regardless of whether any of the
        matrix coefficients are zero-valued. When dumping a :file:`.full` file, only the lower triangular
        part of the matrix will be written to the :file:`.matrix` file if the matrix is symmetric; the full
        matrix is written if the matrix is unsymmetric. Only matrix coefficients that are greater than zero
        will be written.

        The Harwell-Boeing format is column-oriented. That is, non-zero matrix values are stored with their
        corresponding row indices in a sequence of columns. However, because the Mechanical APDL matrix
        files are
        stored by row and not column, when the :ref:`hbmat` command is used with a non-symmetric matrix, the
        transpose of the matrix is, in fact, written.

        The :ref:`wrfull` command, used with the :ref:`solve` command, generates the assembled global matrix
        file and eliminate the equation solution process and results output process.

        The mapping file can be used to map the matrix equation numbers found in the :file:`.matrix` file
        directly to the corresponding node numbers and degrees of freedom.

        When dumping a CMS :file:`.sub` file, the last rows/columns of the matrix are non-physical degrees
        of freedom added internally by the `CMS process
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_substr/advcms.html#advcmsunderstand>`_
        and cannot be mapped directly to a node number or particular degree of freedom.
        """
        command = f"HBMAT,{fname},{ext},,{form},{matrx},{rhs},{mapping}"
        return self.run(command, **kwargs)

    def psmat(
        self,
        fname: str = "",
        ext: str = "",
        matrix: str = "",
        color: str = "",
        **kwargs,
    ):
        r"""Writes an assembled global matrix to a postscript format that graphically displays nonzero matrix
        values.

        Mechanical APDL Command: `PSMAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSMAT.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. This file name is used for the postscript file
            name. It defaults to the current Jobname if left blank.

        ext : str
            Filename extension (eight-character maximum). Defaults to :file:`.PS` if left blank.

        matrix : str
            Specify which matrix to write to the output postscript file:

            * ``STIFF`` - Write stiffness matrix to output postscript file. Valid for all types of analyses that
              write a :file:`.FULL` file.

            * ``MASS`` - Write mass matrix to output postscript file. Valid for buckling, substructure, and
              modal analyses. If the :file:`.FULL` file was generated in a buckling analysis, then this label will
              write the stress stiffening matrix to the output postscript file.

            * ``DAMP`` - Write damping matrix to output postscript file. Only valid for damped modal analyses.

        color : str
            Specifies whether to display the grid in black and white or in color:

            * ``BLACK`` - Each nonzero coefficient is symbolized by a black square (default).

            * ``COLOR`` - Each nonzero coefficient is symbolized by a colored square. The color depends on the
              module of the coefficient; the range is from blue for the smallest values to red for the largest
              values. The color map is:

        Notes
        -----

        .. _PSMAT_notes:

        This command is used to copy a matrix from the assembled global matrix file ( :file:`.FULL` file) as
        specified on the :ref:`file` command and write it in a postscript format to a new file named
        ``Fname``. ``Ext`` (defaults to :file:`Jobname.PS` ). The matrix is symbolized by a grid in which
        the black or colored squares represent the nonzero coefficients of the matrix. The :file:`.FULL`
        file must be available for this command to work properly.

        If the matrix is large, it may be difficult to display the postscript file. In this case, use
        ``Color`` = BLACK to reduce the postscript file size.

        The assembled global matrix file is created during solution depending on the analysis type, equation
        solver, and other solution options. By default, the assembled global matrix file is never deleted at
        the end of solution. For most analysis types, the Sparse direct solver and the ICCG solver write a
        :file:`.FULL` file. All mode extraction methods used for buckling and modal analyses write a
        properly formatted :file:`.FULL` file to be used with the :ref:`psmat` command.

        When copying the stiffness matrix for transient and harmonic analyses, be aware that the element
        mass matrix values (and possibly element damping matrix values) are incorporated into the globally
        assembled stiffness matrix. Thus, the globally assembled stiffness matrix represents more than the
        stiffness of the model for these analysis types. Please refer to the `Mechanical APDL Theory
        Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_ for
        more details.

        The :ref:`psmat` command is not able to display a lumped mass matrix from a :file:`.FULL` file
        generated by a harmonic analysis.

        When copying a :file:`.FULL` file, the rows and columns corresponding to specified constraints (for
        example, :ref:`d` commands) are eliminated from the system of equations and therefore are not
        written to the :file:`.PS` file. In addition, rows and columns corresponding to eliminated
        (dependent) degrees of freedom from coupling and/or constraint equations (for example, :ref:`ce`,
        :ref:`cp` commands) are eliminated from the system of equations and are not written to the
        :file:`.PS` file. The DOFs that are eliminated from any coupling and/or constraint equations are
        determined internally by the solution code and may not match what you specified via the :ref:`ce` /
        :ref:`cp` (or similar) commands.

        When copying a :file:`.FULL` file, only the upper triangular part of the matrix will be written to
        the :file:`.PS` file if the matrix is symmetric; the full matrix is written if the matrix is
        unsymmetric. Only matrix coefficients that are greater than zero will be written.

        The :ref:`wrfull` command, in conjunction with the :ref:`solve` command, can be used to generate the
        assembled global matrix file and eliminate the equation solution process and results output process.

        The following command sequence shows typical usage of this command.

        .. code:: apdl

           /BATCH,LIST
           /AUX2			! Enter AUX2 processor
           FILE,job1,full		! FULL file containing stiffness matrix is job1.full
           PSMAT,job1KColor,ps,STIFF,COLOR	! Create file job1KColor.ps in color
           !                                 postscript format for stiffness matrix
           PSMAT,job1MBlack,,STIFF,BLACK	! Create file job1MBalck.ps in black/white
           !                                 postscript format for stiffness matrix
           FINISH

        Below is an example of an export of the stiffness matrix to a postscript format using the COLOR
        option.
        """
        command = f"PSMAT,{fname},{ext},{matrix},{color}"
        return self.run(command, **kwargs)
