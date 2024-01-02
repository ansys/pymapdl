from typing import Optional, Union

from ansys.mapdl.core.mapdl_types import MapdlFloat


class BirthAndDeath:
    def ealive(self, elem: str = "", **kwargs) -> Optional[str]:
        """Reactivates an element (for the birth and death capability).

        APDL Command: EALIVE

        Parameters
        ----------
        elem
            Element to be reactivated:

            ALL  - Reactivates all selected elements (ESEL).

            Comp - Specifies a component name.

        Notes
        -----
        Reactivates the specified element when the birth and death
        capability is being used. An element can be reactivated only
        after it has been deactivated (EKILL).

        Reactivated elements have a zero strain (or thermal heat
        storage, etc.)  state.

        ANSYS, Inc. recommends using the element
        deactivation/reactivation procedure for analyses involving
        linear elastic materials only. Do not use element
        deactivation/reactivation in analyses involving time-
        dependent materials, such as viscoelasticity, viscoplasticity,
        and creep analysis.

        This command is also valid in PREP7.
        """
        command = f"EALIVE,{elem}"
        return self.run(command, **kwargs)

    def ekill(self, elem: Union[str, int] = "", **kwargs) -> Optional[str]:
        """Deactivates an element (for the birth and death capability).

        APDL Command: EKILL

        Parameters
        ----------
        elem
            Element to be deactivated. If ALL, deactivate all
            selected elements [ESEL]. A component name may also be
            substituted for ELEM.

        Notes
        -----
        Deactivates the specified element when the birth and death
        capability is being used. A deactivated element remains in
        the model but contributes a near-zero stiffness (or
        conductivity, etc.) value (ESTIF) to the overall matrix. Any
        solution-dependent state variables (such as stress, plastic
        strain, creep strain, etc.) are set to zero. Deactivated
        elements contribute nothing to the overall mass (or
        capacitance, etc.) matrix.

        The element can be reactivated with the EALIVE command.

        ANSYS, Inc. recommends using element deactivation/reactivation
        (EKILL/EALIVE) for linear elastic materials only. For all other
        materials, validate the results carefully before using them.

        This command is also valid in PREP7.
        """
        command = f"EKILL,{elem}"
        return self.run(command, **kwargs)

    def estif(self, kmult: MapdlFloat = "", **kwargs) -> Optional[str]:
        """Specifies the matrix multiplier for deactivated elements.

        APDL Command: ESTIF

        Specifies the stiffness matrix multiplier for elements deactivated with
        the EKILL command (birth and death).

        This command is also valid in PREP7.

        Parameters
        ----------
        kmult
            Stiffness matrix multiplier for deactivated elements (defaults to
            1.0E-6).

        Examples
        --------
        >>> mapdl.prep7()
        >>> mapdl.estif(1E-8)
        'DEAD ELEMENT STIFFNESS MULTIPLIER= 0.10000E-07'

        """
        command = f"ESTIF,{kmult}"
        return self.run(command, **kwargs)
