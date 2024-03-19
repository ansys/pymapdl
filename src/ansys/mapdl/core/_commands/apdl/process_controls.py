class ProcessControls:
    def wait(self, dtime="", **kwargs):
        """APDL Command: /WAIT

        Causes a delay before the reading of the next command.

        Parameters
        ----------
        dtime
            Time delay (in seconds). Maximum time delay is 59 seconds.

        Notes
        -----
        You should consider using ``time.sleep(dtime)``

        The command following the /WAIT will not be processed until the
        specified wait time increment has elapsed.  Useful when reading from a
        prepared input file to cause a pause, for example, after a display
        command so that the display can be reviewed for a period of time.
        Another "wait" feature is available via the ``*ASK`` command.

        This command is valid in any processor.
        """
        command = f"/WAIT,{dtime}"
        return self.run(command, **kwargs)
