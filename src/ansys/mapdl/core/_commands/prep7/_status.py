from ansys.mapdl.core._commands import CommandsBase

class Status(CommandsBase):

    def fatigue(self, **kwargs):
        r"""Specifies "Fatigue data status" as the subsequent status topic.

        Mechanical APDL Command: `FATIGUE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FATIGUE.html>`_

        Notes
        -----

        .. _FATIGUE_notes:

        This is a status ( :ref:`stat` ) topic command that appears in the log file ( :file:`Jobname.LOG` )
        if status is requested for some items. This command is followed immediately by a :ref:`stat`
        command, which reports the status for the specified topic.

        If entered directly into the program, the :ref:`stat` command should immediately follow this
        command.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = "FATIGUE"
        return self.run(command, **kwargs)


