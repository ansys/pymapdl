class Status:

    def calc(self, **kwargs):
        """Specifies "Calculation settings" as the subsequent status topic.

        APDL Command: CALC

        Notes
        -----
        This is a status [STAT] topic command.  Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.
        """
        command = f"CALC,"
        return self.run(command, **kwargs)

    def datadef(self, **kwargs):
        """Specifies "Directly defined data status" as the subsequent status

        APDL Command: DATADEF
        topic.

        Notes
        -----
        This is a status [STAT] topic command.  Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.
        """
        command = f"DATADEF,"
        return self.run(command, **kwargs)

    def display(self, **kwargs):
        """Specifies "Display settings" as the subsequent status topic.

        APDL Command: DISPLAY

        Notes
        -----
        This is a status [STAT] topic command.  Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.
        """
        command = f"DISPLAY,"
        return self.run(command, **kwargs)

    def lccalc(self, **kwargs):
        """Specifies "Load case settings" as the subsequent status topic.

        APDL Command: LCCALC

        Notes
        -----
        This is a status [STAT] topic command.  Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.

        This command is also valid for rezoning.
        """
        command = f"LCCALC,"
        return self.run(command, **kwargs)

    def point(self, **kwargs):
        """Specifies "Point flow tracing settings" as the subsequent status topic.

        APDL Command: POINT

        Notes
        -----
        This is a status [STAT] topic command.  Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.
        """
        command = f"POINT,"
        return self.run(command, **kwargs)

    def spec(self, **kwargs):
        """Specifies "Miscellaneous specifications" as the subsequent status

        APDL Command: SPEC
        topic.

        Notes
        -----
        This is a status [STAT] topic command.  Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.
        """
        command = f"SPEC,"
        return self.run(command, **kwargs)
