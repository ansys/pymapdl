"""Miscellaneous commands requiring additional handling by mapdl"""


class _MapdlMiscCommands():
    """Miscellaneous commands requiring additional handling by mapdl"""

    def lssolve(self, lsmin="", lsmax="", lsinc="", **kwargs):
        """APDL Command: LSSOLVE

        Reads and solves multiple load steps.

        Parameters
        ----------
        lsmin, lsmax, lsinc
            Range of load step files to be read and solved, from
            ``lsmin`` to ``lsmax`` in steps of ``lsinc``.  ``lsmax``
            defaults to ``lsmin``, and ``lsinc`` defaults to 1. If
            ``lsmin`` is blank, a brief command description is
            displayed.  The load step files are assumed to be named
            Jobname.Sn, where n is a number assigned by the
            ``lswrite`` command (01--09, 10, 11, etc.).  On systems
            with a 3-character limit on the extension, the "S" is
            dropped for numbers > 99.

        Examples
        --------
        Write the load and load step option data to a file and solve
        it.  In this case, write the second load step.

        >>> mapdl.lswrite(2)
        >>> mapdl.lssolve(1, 2)

        Notes
        -----
        ``lssolve`` invokes an ANSYS macro to read and solve multiple
        load steps.  The macro loops through a series of load step
        files written by the LSWRITE command.  The macro file called
        by ``lssolve`` is called LSSOLVE.MAC.

        ``lssolve`` cannot be used with the birth-death option.

        ``lssolve`` is not supported for cyclic symmetry analyses.

        ``lssolve`` does not support restarts.
        """
        with self.non_interactive:
            self.run(f"LSSOLVE,{lsmin},{lsmax},{lsinc}", **kwargs)
        return self.last_response
