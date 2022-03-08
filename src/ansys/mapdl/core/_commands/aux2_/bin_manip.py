class BinManip:
    def combine(self, filetype="", **kwargs):
        """Combines distributed memory parallel (Distributed ANSYS) files.

        APDL Command: COMBINE

        Parameters
        ----------
        filetype
            Type of solution file to combine. There is no default; if (blank),
            the command is ignored.

            RST - Structural results file (.RST)

            RTH - Thermal results file (.RTH)

            RMG - Magnetics results file (.RMG)

            RSTP - Linear perturbation results file (.RSTP)

            EMAT - Element matrix file (.EMAT).

            ESAV - Element saved data file (.ESAV)

            MODE - Modal results file (.MODE)

            MLV - Modal load vector file (.MLV)

            IST - Initial state file (.IST)

            FULL - Full matrix file (.FULL)

            RFRQ - Reduced complex displacement file (.RFRQ)

            RDSP - Reduced displacement file (.RDSP)

        Notes
        -----
        The COMBINE command is used within the AUX2 auxiliary processor to
        combine local solution files from a distributed memory parallel
        solution into a single, global file. Before using this command, you
        must enter the AUX2 processor by issuing the /AUX2 command.

        In a distributed memory parallel (Distributed ANSYS) solution, you can
        use the DMPOPTION command to bypass the file combination step, causing
        all individual local files to be kept on the local disks in the current
        working directory. Later on, you can start a new distributed memory
        parallel solution and use the COMBINE command to combine local files
        into a global file for a downstream solution or another operation
        (e.g., postprocessing with /POST1). For example, the command
        COMBINE,RST will combine local results files (JobnameN.RST) into a
        global results file (Jobname.RST).

        When the COMBINE command is used in a subsequent Distributed ANSYS
        session, the number of processors must be the same as in the
        distributed memory parallel solution that generated the files.

        When running on a cluster, the local solution files must be available
        in the working directory on each node in the subsequent session. As an
        example, consider the following command line used to generate local
        solution files:

        Different machines can be used in the subsequent session to combine
        these files. However, the total number of cores must remain unchanged
        (seven in the above case), and the local files must be copied to the
        working directory (or directories) on each of the machines used in the
        subsequent session.
        """
        command = f"COMBINE,{filetype}"
        return self.run(command, **kwargs)

    def hbmat(self, fname="", ext="", form="", matrx="", rhs="", mapping="", **kwargs):
        """Writes an assembled global matrix in Harwell-Boeing format.

        APDL Command: HBMAT

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        form
            Specifies format of output matrix file:

            ASCII - Write output matrix file in ASCII form.

            BIN - Write output matrix file in binary form.

        matrx
            Specify which matrix to write to the output matrix file:

            STIFF - Write stiffness matrix to output matrix file.  Valid for all types of analyses
                    that write a .FULL file.

            MASS - Write mass matrix to output matrix file.  Valid for buckling, substructure, and
                   modal analyses.  If .FULL file was generated in a buckling
                   analysis, then this label will write stress stiffening
                   matrix to output matrix file.

            DAMP - Write damping matrix to output matrix file.  Only valid for damped modal
                   analyses.

        rhs
            Specifies whether to write the right-hand side vector to output
            matrix file:

            YES - Write right-hand side vector to output matrix file.

            NO - Do not write right-hand side vector to output matrix file.

        mapping
            Specifies whether to write the mapping file. This file is always
            named Fname.MAPPING.

            YES - Write the mapping file.

            NO - Do not write the mapping file (default).

        Notes
        -----
        This command is used to copy a matrix from the assembled global matrix
        file (.FULL file) or from the superelement matrix file (.SUB file) as
        specified on the FILEAUX2 command and write it in Harwell-Boeing format
        to a new file, named jobname.MATRIX.  The Harwell-Boeing format is
        widely used by other applications that deal with matrices.

        The assembled global matrix file is created during solution depending
        on the analysis type, equation solver, and other solution options.  By
        default, the assembled global matrix file is never deleted at the end
        of solution. For most analysis types, the Sparse direct solver and the
        ICCG solver will write a .FULL file. All mode extraction methods used
        for buckling and modal analyses will write a properly formatted .FULL
        file to be used with the HBMAT command. However, when using Distributed
        ANSYS, a majority of analyses will write a distributed (or local) form
        of the .FULL file which is not currently supported by the HBMAT
        command.

        When dumping the stiffness matrix for transient and harmonic analyses,
        be aware that the element mass matrix values (and possibly element
        damping matrix values) are incorporated into the globally assembled
        stiffness matrix.  Thus, the globally assembled stiffness matrix
        represents more than the stiffness of the model for these analysis
        types.  Please refer to the Mechanical APDL Theory Reference for more
        details.

        When dumping a .FULL file, the rows and columns corresponding to
        specified constraints (e.g., D commands) are eliminated from the system
        of equations and therefore are not written to the .MATRIX file. Also,
        rows and columns corresponding to eliminated (slave) degrees of freedom
        from coupling and/or constraint equations (e.g., CE, CP commands) are
        also eliminated from the system of equations and are not written to the
        .MATRIX file. The DOFs that are eliminated from any coupling and/or
        constraint equations are determined internally by the solution code and
        may not match what you specified via the CE/CP (or similar) commands.

        When dumping a .SUB file, the full nxn matrix will be written to the
        .MATRIX file for either symmetric or unsymmetric matrices, regardless
        of whether any of the matrix coefficients are zero-valued. When dumping
        a .FULL file, only the lower triangular part of the matrix will be
        written to the .MATRIX file if the matrix is symmetric; the full matrix
        is written if the matrix is unsymmetric. Only matrix coefficients that
        are greater than zero will be written.

        The Harwell-Boeing format is column-oriented.  That is, non-zero matrix
        values are stored with their corresponding row indices in a sequence of
        columns.  However, since the ANSYS matrix files are stored by row and
        not column, when the HBMAT command is used with a non-symmetric matrix,
        the transpose of the matrix is, in fact, written.

        The WRFULL command, in conjunction with the SOLVE command, can be used
        to generate the assembled global matrix file and eliminate the equation
        solution process and results output process.

        The mapping file can be used to map the matrix equation numbers found
        in the .MATRIX file directly to the corresponding node numbers and
        degrees of freedom.

        When dumping a CMS .SUB file, the last rows/columns of the matrix are
        non-physical degrees of freedom added internally by the CMS process and
        cannot be mapped directly to a node number or particular degree of
        freedom.
        """
        command = f"HBMAT,{fname},{ext},,{form},{matrx},{rhs},{mapping}"
        return self.run(command, **kwargs)

    def psmat(self, fname="", ext="", matrix="", color="", **kwargs):
        """Writes an assembled global matrix to a postscript format that

        APDL Command: PSMAT
        graphically displays nonzero matrix values.

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        matrix
            Specify which matrix to write to the output postscript file:

            STIFF - Write stiffness matrix to output postscript file. Valid for all types of
                    analyses that write a .FULL file.

            MASS - Write mass matrix to output postscript file. Valid for buckling, substructure,
                   and modal analyses. If the .FULL file was generated in a
                   buckling analysis, then this label will write the stress
                   stiffening matrix to the output postscript file.

            DAMP - Write damping matrix to output postscript file. Only valid for damped modal
                   analyses.

        color
            Specifies whether to display the grid in black and white or in
            color:

            BLACK  - Each nonzero coefficient is symbolized by a black square (default).

            COLOR  - Each nonzero coefficient is symbolized by a colored square. The color depends
                     on the module of the coefficient; the range is from blue
                     for the smallest values to red for the largest values. The
                     color map is:

        Notes
        -----
        This command is used to copy a matrix from the assembled global matrix
        file (.FULL file) as specified on the FILE command and write it in a
        postscript format to a new file named Fname.Ext (defaults to
        Jobname.PS). The matrix is symbolized by a grid in which the black or
        colored squares represent the nonzero coefficients of the matrix. The
        .FULL file must be available for this command to work properly.

        If the matrix is large, it may be difficult to display the postscript
        file. In this case, use Color = BLACK to reduce the postscript file
        size.

        The assembled global matrix file is created during solution depending
        on the analysis type, equation solver, and other solution options. By
        default, the assembled global matrix file is never deleted at the end
        of solution. For most analysis types, the Sparse direct solver and the
        ICCG solver write a .FULL file. All mode extraction methods used for
        buckling and modal analyses write a properly formatted .FULL file to be
        used with the PSMAT command.

        When copying the stiffness matrix for transient and harmonic analyses,
        be aware that the element mass matrix values (and possibly element
        damping matrix values) are incorporated into the globally assembled
        stiffness matrix.  Thus, the globally assembled stiffness matrix
        represents more than the stiffness of the model for these analysis
        types.  Please refer to the Mechanical APDL Theory Reference for more
        details.

        The PSMAT command is not able to display a lumped mass matrix from a
        .FULL file generated by a harmonic analysis.

        When copying a .FULL file, the rows and columns corresponding to
        specified constraints (e.g., D commands) are eliminated from the system
        of equations and therefore are not written to the .PS file. In
        addition, rows and columns corresponding to eliminated (slave) degrees
        of freedom from coupling and/or constraint equations (e.g., CE, CP
        commands) are eliminated from the system of equations and are not
        written to the .PS file. The DOFs that are eliminated from any coupling
        and/or constraint equations are determined internally by the solution
        code and may not match what you specified via the CE/CP (or similar)
        commands.

        When copying a .FULL file, only the upper triangular part of the matrix
        will be written to the .PS  file if the matrix is symmetric; the full
        matrix is written if the matrix is unsymmetric. Only matrix
        coefficients that are greater than zero will be written.

        The WRFULL command, in conjunction with the SOLVE command, can be used
        to generate the assembled global matrix file and eliminate the equation
        solution process and results output process.

        The following command sequence shows typical usage of this command.

        Below is an example of an export of the stiffness matrix to a
        postscript format using the COLOR option.

        :
        """
        command = f"PSMAT,{fname},{ext},{matrix},{color}"
        return self.run(command, **kwargs)
