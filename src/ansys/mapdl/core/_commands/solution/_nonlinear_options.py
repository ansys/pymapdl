class NonlinearOptions:

    def crplim(self, crcr: str = "", option: str = "", **kwargs):
        r"""Specifies the creep criterion for automatic time stepping.

        Mechanical APDL Command: `CRPLIM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CRPLIM.html>`_

        Parameters
        ----------
        crcr : str
            Value of creep criteria for the creep limit ratio control.

        option : str
            Type of creep analysis for which the creep limit ratio is specified :

            * ``1 (or ON)`` - Implicit creep analysis.

            * ``0 (or OFF)`` - Explicit creep analysis.

        Notes
        -----

        .. _CRPLIM_notes:

        The :ref:`cutcontrol` command can also be used to set the creep criterion and is preferred over this
        command for setting automatic time step controls.

        The creep ratio control can be used at the same time for implicit creep and explicit creep analyses.
        For implicit creep ( ``Option`` = 1), the default value of ``CRCR`` is zero (that is, no creep limit
        control), and you can specify any value. For explicit creep ( ``Option`` = 0), the default value of
        ``CRCR`` is 0.1, and the maximum value allowed is 0.25.

        This command is also valid in PREP7.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"CRPLIM,{crcr},{option}"
        return self.run(command, **kwargs)


