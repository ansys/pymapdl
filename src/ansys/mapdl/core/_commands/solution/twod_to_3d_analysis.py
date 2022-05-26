class TwoDTo3DAnalysis:
    def map2dto3d(self, action="", ldstep="", sbstep="", option="", **kwargs):
        """Initiates a 2-D to 3-D analysis and maps variables.

        APDL Command: MAP2DTO3D

        Parameters
        ----------
        action
            The 2-D to 3-D action to perform:

            START - Start the analysis process by rebuilding the 2-D analysis database (.db) based
                    on the specified load step and substep information, and
                    update nodes to their deformed positions in the 2-D mesh.

            FINISH - Maps solution variables from the 2-D mesh to the extruded 3-D mesh.

        ldstep
            The load step number at which 2-D to 3-D analysis should occur. The
            default value is the highest load step number found in the
            Jobname.Rnnn files (for the current jobname and in the current
            directory).

        sbstep
            The substep number of the specified load step (LDSTEP) at which the
            2-D to 3-D analysis should occur. The default value is the highest
            substep number found in the specified load step in the Jobname.Rnnn
            files (for the current jobname and in the current directory).

        option
            Mapping option:

            (Blank) - Transfer and map all applied boundary conditions, nodal temperatures, loads,
                      and surface pressures from the 2-D mesh to the extruded
                      3-D mesh. This behavior is the default.

            NOBC - No applied boundary conditions or loads are transferred from the 2-D mesh to
                   the extruded 3-D mesh. Nodal temperatures (defined via the
                   BF,TEMP command) are transferred.

        Notes
        -----
        The MAP2DTO3D command initiates the 2-D to 3-D analysis process, sets
        analysis options, rebuilds the database, and maps the solution
        variables from the 2-D mesh to the 3-D mesh.

        Before issuing this command, clear the database (/CLEAR).

        The LDSTEP and SBSTEP values apply only when Action = START.

        For more information, see 2-D to 3-D Analysis in the Advanced Analysis
        Guide.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"MAP2DTO3D,{action},{ldstep},{sbstep},{option}"
        return self.run(command, **kwargs)
