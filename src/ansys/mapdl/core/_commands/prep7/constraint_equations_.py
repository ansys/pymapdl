from ansys.mapdl.core._commands import CommandsBase

class ConstraintEquations(CommandsBase):

    def cecyc(self, lowname: str = "", highname: str = "", nsector: str = "", hindex: str = "", tolerance: str = "", kmove: int | str = "", kpairs: int | str = "", **kwargs):
        r"""Generates the constraint equations for a cyclic symmetry analysis

        Mechanical APDL Command: `CECYC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CECYC.html>`_

        Parameters
        ----------
        lowname : str
            Name of a component for the nodes on the low angle edge of the sector. Enclosed in single
            quotes.

        highname : str
            Name of a component for the nodes on the high angle edge of the sector. Enclosed in single
            quotes.

        nsector : str
            Number of sectors in the complete 360 degrees.

        hindex : str
            Harmonic index to be represented by this set of constraint equations. If ``Hindex`` is -1,
            generate constraint equations for static cyclic symmetry. If ``HIndex`` is -2, generate
            constraint equations for static cyclic asymmetry.

        tolerance : str
            A positive tolerance is an absolute tolerance (length units), and a negative tolerance is a
            tolerance relative to the local element size.

        kmove : int or str

            * ``0`` - Nodes are not moved.

            * ``1`` - HIGHNAME component nodes are moved to match LOWNAME component nodes exactly.

        kpairs : int or str

            * ``0`` - Do not print paired nodes

            * ``1`` - Print table of paired nodes

        Notes
        -----

        .. _CECYC_notes:

        The analysis can be either modal cyclic symmetry or static cyclic symmetry.

        The pair of nodes for which constraint equations are written are rotated into :ref:`csys`,1.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"CECYC,{lowname},{highname},{nsector},{hindex},{tolerance},{kmove},{kpairs}"
        return self.run(command, **kwargs)


