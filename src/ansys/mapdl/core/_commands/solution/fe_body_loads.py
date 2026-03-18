# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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


class FeBodyLoads(CommandsBase):

    def bf(
        self,
        node: str = "",
        lab: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        meshflag: str = "",
        **kwargs,
    ):
        r"""Defines a nodal body-force load.

        Mechanical APDL Command: `BF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BF.html>`_

        Parameters
        ----------
        node : str
            Node to which body load applies. If ``Node`` = ALL, apply to all selected nodes ( :ref:`nsel` ).
            A component name may also be substituted for ``Node``.

        lab : str
            Valid body load label. Load labels are listed under Body Loads in the input table for each
            element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        val1 : str
            Value associated with the ``Lab`` item or table name reference for tabular boundary conditions. Use
            only ``VAL1`` for TEMP, FLUE, HGEN, DGEN, MVDI, CHRGD, PORT, and SPRE.

            Tabular input is supported for certain labels (see :ref:`Notes for details). To specify a table,
            enclose the table name in percent signs (%) (e.g., <BF_notes>` :ref:`bf`,
            ``Node``,TEMP,``tabname``). Use the :ref:`dim` command to define a table.

            If ``Lab`` = MASS for acoustics:

            * ``VAL1`` - Mass source with units of kg/(m :sup:`3` *s) in a harmonic analysis or in a transient
              analysis solved with the velocity potential formulation; or mass source rate with units of kg/(m
              :sup:`3` *s :sup:`2` ) in a transient analysis solved with the pressure formulation; or power source
              with units of watts in an energy diffusion solution for room acoustics

            * ``VAL2`` - Phase angle in degrees

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for acoustics (velocity components in a harmonic analysis or in a transient
            analysis solved with the velocity potential formulation; or acceleration components in a transient
            analysis solved with the pressure formulation):

            * ``VAL1`` - X component

            * ``VAL2`` - Y component

            * ``VAL3`` - Z component

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = VELO for electromagnetics (velocity and angular velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Velocity component in the X direction

            * ``VAL2`` - Velocity component in the Y direction

            * ``VAL3`` - Velocity component in the Z direction

            * ``VAL4`` - Angular velocity about the X axis (rad/sec)

            * ``VAL5`` - Angular velocity about the Y axis (rad/sec)

            * ``VAL6`` - Angular velocity about the Z axis (rad/sec)

            If ``Lab`` = VELO for thermal (velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Mass transport velocity component in X direction

            * ``VAL2`` - Mass transport velocity component in Y direction

            * ``VAL3`` - Mass transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for diffusion (transport velocity):

            * ``VAL1`` - Transport velocity component in X direction

            * ``VAL2`` - Transport velocity component in Y direction

            * ``VAL3`` - Transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = IMPD:

            * ``VAL1`` - Resistance in N⋅s/m :sup:`3`

            * ``VAL2`` - Reactance in N⋅s/m :sup:`3`

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = FPBC:

            * ``VAL1`` - Phase shift (product of phase constant and period in unit radian); or Floquet boundary
              flag (set ``VAL1`` = YES) for a modal analysis that solves the eigenvalues with a specified
              frequency ( ``FREQMOD`` on the :ref:`modopt` command)

            * ``VAL2`` - Attenuation (product of attenuation constant and period); not used if ``VAL1`` = YES

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VMEN:

            * ``VAL1`` - Mean flow velocity component in the X direction

            * ``VAL2`` - Mean flow velocity component in the Y direction

            * ``VAL3`` - Mean flow velocity component in the Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = UFOR:

            * ``VAL1`` - Real part of complex force potential

            * ``VAL2`` - Imaginary part of complex force potential

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = SFOR:

            * ``VAL1`` - X component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL2`` - Y component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL3`` - Z component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = HFLW:

            * ``VAL1`` - Real part of volumetric heat source for viscous-thermal acoustics

            * ``VAL2`` - Imaginary part of volumetric heat source for viscous-thermal acoustics

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

        val2 : str
            Value associated with the ``Lab`` item or table name reference for tabular boundary conditions. Use
            only ``VAL1`` for TEMP, FLUE, HGEN, DGEN, MVDI, CHRGD, PORT, and SPRE.

            Tabular input is supported for certain labels (see :ref:`Notes for details). To specify a table,
            enclose the table name in percent signs (%) (e.g., <BF_notes>` :ref:`bf`,
            ``Node``,TEMP,``tabname``). Use the :ref:`dim` command to define a table.

            If ``Lab`` = MASS for acoustics:

            * ``VAL1`` - Mass source with units of kg/(m :sup:`3` *s) in a harmonic analysis or in a transient
              analysis solved with the velocity potential formulation; or mass source rate with units of kg/(m
              :sup:`3` *s :sup:`2` ) in a transient analysis solved with the pressure formulation; or power source
              with units of watts in an energy diffusion solution for room acoustics

            * ``VAL2`` - Phase angle in degrees

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for acoustics (velocity components in a harmonic analysis or in a transient
            analysis solved with the velocity potential formulation; or acceleration components in a transient
            analysis solved with the pressure formulation):

            * ``VAL1`` - X component

            * ``VAL2`` - Y component

            * ``VAL3`` - Z component

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = VELO for electromagnetics (velocity and angular velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Velocity component in the X direction

            * ``VAL2`` - Velocity component in the Y direction

            * ``VAL3`` - Velocity component in the Z direction

            * ``VAL4`` - Angular velocity about the X axis (rad/sec)

            * ``VAL5`` - Angular velocity about the Y axis (rad/sec)

            * ``VAL6`` - Angular velocity about the Z axis (rad/sec)

            If ``Lab`` = VELO for thermal (velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Mass transport velocity component in X direction

            * ``VAL2`` - Mass transport velocity component in Y direction

            * ``VAL3`` - Mass transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for diffusion (transport velocity):

            * ``VAL1`` - Transport velocity component in X direction

            * ``VAL2`` - Transport velocity component in Y direction

            * ``VAL3`` - Transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = IMPD:

            * ``VAL1`` - Resistance in N⋅s/m :sup:`3`

            * ``VAL2`` - Reactance in N⋅s/m :sup:`3`

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = FPBC:

            * ``VAL1`` - Phase shift (product of phase constant and period in unit radian); or Floquet boundary
              flag (set ``VAL1`` = YES) for a modal analysis that solves the eigenvalues with a specified
              frequency ( ``FREQMOD`` on the :ref:`modopt` command)

            * ``VAL2`` - Attenuation (product of attenuation constant and period); not used if ``VAL1`` = YES

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VMEN:

            * ``VAL1`` - Mean flow velocity component in the X direction

            * ``VAL2`` - Mean flow velocity component in the Y direction

            * ``VAL3`` - Mean flow velocity component in the Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = UFOR:

            * ``VAL1`` - Real part of complex force potential

            * ``VAL2`` - Imaginary part of complex force potential

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = SFOR:

            * ``VAL1`` - X component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL2`` - Y component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL3`` - Z component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = HFLW:

            * ``VAL1`` - Real part of volumetric heat source for viscous-thermal acoustics

            * ``VAL2`` - Imaginary part of volumetric heat source for viscous-thermal acoustics

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

        val3 : str
            Value associated with the ``Lab`` item or table name reference for tabular boundary conditions. Use
            only ``VAL1`` for TEMP, FLUE, HGEN, DGEN, MVDI, CHRGD, PORT, and SPRE.

            Tabular input is supported for certain labels (see :ref:`Notes for details). To specify a table,
            enclose the table name in percent signs (%) (e.g., <BF_notes>` :ref:`bf`,
            ``Node``,TEMP,``tabname``). Use the :ref:`dim` command to define a table.

            If ``Lab`` = MASS for acoustics:

            * ``VAL1`` - Mass source with units of kg/(m :sup:`3` *s) in a harmonic analysis or in a transient
              analysis solved with the velocity potential formulation; or mass source rate with units of kg/(m
              :sup:`3` *s :sup:`2` ) in a transient analysis solved with the pressure formulation; or power source
              with units of watts in an energy diffusion solution for room acoustics

            * ``VAL2`` - Phase angle in degrees

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for acoustics (velocity components in a harmonic analysis or in a transient
            analysis solved with the velocity potential formulation; or acceleration components in a transient
            analysis solved with the pressure formulation):

            * ``VAL1`` - X component

            * ``VAL2`` - Y component

            * ``VAL3`` - Z component

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = VELO for electromagnetics (velocity and angular velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Velocity component in the X direction

            * ``VAL2`` - Velocity component in the Y direction

            * ``VAL3`` - Velocity component in the Z direction

            * ``VAL4`` - Angular velocity about the X axis (rad/sec)

            * ``VAL5`` - Angular velocity about the Y axis (rad/sec)

            * ``VAL6`` - Angular velocity about the Z axis (rad/sec)

            If ``Lab`` = VELO for thermal (velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Mass transport velocity component in X direction

            * ``VAL2`` - Mass transport velocity component in Y direction

            * ``VAL3`` - Mass transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for diffusion (transport velocity):

            * ``VAL1`` - Transport velocity component in X direction

            * ``VAL2`` - Transport velocity component in Y direction

            * ``VAL3`` - Transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = IMPD:

            * ``VAL1`` - Resistance in N⋅s/m :sup:`3`

            * ``VAL2`` - Reactance in N⋅s/m :sup:`3`

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = FPBC:

            * ``VAL1`` - Phase shift (product of phase constant and period in unit radian); or Floquet boundary
              flag (set ``VAL1`` = YES) for a modal analysis that solves the eigenvalues with a specified
              frequency ( ``FREQMOD`` on the :ref:`modopt` command)

            * ``VAL2`` - Attenuation (product of attenuation constant and period); not used if ``VAL1`` = YES

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VMEN:

            * ``VAL1`` - Mean flow velocity component in the X direction

            * ``VAL2`` - Mean flow velocity component in the Y direction

            * ``VAL3`` - Mean flow velocity component in the Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = UFOR:

            * ``VAL1`` - Real part of complex force potential

            * ``VAL2`` - Imaginary part of complex force potential

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = SFOR:

            * ``VAL1`` - X component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL2`` - Y component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL3`` - Z component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = HFLW:

            * ``VAL1`` - Real part of volumetric heat source for viscous-thermal acoustics

            * ``VAL2`` - Imaginary part of volumetric heat source for viscous-thermal acoustics

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

        val4 : str
            Value associated with the ``Lab`` item or table name reference for tabular boundary conditions. Use
            only ``VAL1`` for TEMP, FLUE, HGEN, DGEN, MVDI, CHRGD, PORT, and SPRE.

            Tabular input is supported for certain labels (see :ref:`Notes for details). To specify a table,
            enclose the table name in percent signs (%) (e.g., <BF_notes>` :ref:`bf`,
            ``Node``,TEMP,``tabname``). Use the :ref:`dim` command to define a table.

            If ``Lab`` = MASS for acoustics:

            * ``VAL1`` - Mass source with units of kg/(m :sup:`3` *s) in a harmonic analysis or in a transient
              analysis solved with the velocity potential formulation; or mass source rate with units of kg/(m
              :sup:`3` *s :sup:`2` ) in a transient analysis solved with the pressure formulation; or power source
              with units of watts in an energy diffusion solution for room acoustics

            * ``VAL2`` - Phase angle in degrees

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for acoustics (velocity components in a harmonic analysis or in a transient
            analysis solved with the velocity potential formulation; or acceleration components in a transient
            analysis solved with the pressure formulation):

            * ``VAL1`` - X component

            * ``VAL2`` - Y component

            * ``VAL3`` - Z component

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = VELO for electromagnetics (velocity and angular velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Velocity component in the X direction

            * ``VAL2`` - Velocity component in the Y direction

            * ``VAL3`` - Velocity component in the Z direction

            * ``VAL4`` - Angular velocity about the X axis (rad/sec)

            * ``VAL5`` - Angular velocity about the Y axis (rad/sec)

            * ``VAL6`` - Angular velocity about the Z axis (rad/sec)

            If ``Lab`` = VELO for thermal (velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Mass transport velocity component in X direction

            * ``VAL2`` - Mass transport velocity component in Y direction

            * ``VAL3`` - Mass transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for diffusion (transport velocity):

            * ``VAL1`` - Transport velocity component in X direction

            * ``VAL2`` - Transport velocity component in Y direction

            * ``VAL3`` - Transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = IMPD:

            * ``VAL1`` - Resistance in N⋅s/m :sup:`3`

            * ``VAL2`` - Reactance in N⋅s/m :sup:`3`

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = FPBC:

            * ``VAL1`` - Phase shift (product of phase constant and period in unit radian); or Floquet boundary
              flag (set ``VAL1`` = YES) for a modal analysis that solves the eigenvalues with a specified
              frequency ( ``FREQMOD`` on the :ref:`modopt` command)

            * ``VAL2`` - Attenuation (product of attenuation constant and period); not used if ``VAL1`` = YES

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VMEN:

            * ``VAL1`` - Mean flow velocity component in the X direction

            * ``VAL2`` - Mean flow velocity component in the Y direction

            * ``VAL3`` - Mean flow velocity component in the Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = UFOR:

            * ``VAL1`` - Real part of complex force potential

            * ``VAL2`` - Imaginary part of complex force potential

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = SFOR:

            * ``VAL1`` - X component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL2`` - Y component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL3`` - Z component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = HFLW:

            * ``VAL1`` - Real part of volumetric heat source for viscous-thermal acoustics

            * ``VAL2`` - Imaginary part of volumetric heat source for viscous-thermal acoustics

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

        val5 : str
            Value associated with the ``Lab`` item or table name reference for tabular boundary conditions. Use
            only ``VAL1`` for TEMP, FLUE, HGEN, DGEN, MVDI, CHRGD, PORT, and SPRE.

            Tabular input is supported for certain labels (see :ref:`Notes for details). To specify a table,
            enclose the table name in percent signs (%) (e.g., <BF_notes>` :ref:`bf`,
            ``Node``,TEMP,``tabname``). Use the :ref:`dim` command to define a table.

            If ``Lab`` = MASS for acoustics:

            * ``VAL1`` - Mass source with units of kg/(m :sup:`3` *s) in a harmonic analysis or in a transient
              analysis solved with the velocity potential formulation; or mass source rate with units of kg/(m
              :sup:`3` *s :sup:`2` ) in a transient analysis solved with the pressure formulation; or power source
              with units of watts in an energy diffusion solution for room acoustics

            * ``VAL2`` - Phase angle in degrees

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for acoustics (velocity components in a harmonic analysis or in a transient
            analysis solved with the velocity potential formulation; or acceleration components in a transient
            analysis solved with the pressure formulation):

            * ``VAL1`` - X component

            * ``VAL2`` - Y component

            * ``VAL3`` - Z component

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = VELO for electromagnetics (velocity and angular velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Velocity component in the X direction

            * ``VAL2`` - Velocity component in the Y direction

            * ``VAL3`` - Velocity component in the Z direction

            * ``VAL4`` - Angular velocity about the X axis (rad/sec)

            * ``VAL5`` - Angular velocity about the Y axis (rad/sec)

            * ``VAL6`` - Angular velocity about the Z axis (rad/sec)

            If ``Lab`` = VELO for thermal (velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Mass transport velocity component in X direction

            * ``VAL2`` - Mass transport velocity component in Y direction

            * ``VAL3`` - Mass transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for diffusion (transport velocity):

            * ``VAL1`` - Transport velocity component in X direction

            * ``VAL2`` - Transport velocity component in Y direction

            * ``VAL3`` - Transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = IMPD:

            * ``VAL1`` - Resistance in N⋅s/m :sup:`3`

            * ``VAL2`` - Reactance in N⋅s/m :sup:`3`

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = FPBC:

            * ``VAL1`` - Phase shift (product of phase constant and period in unit radian); or Floquet boundary
              flag (set ``VAL1`` = YES) for a modal analysis that solves the eigenvalues with a specified
              frequency ( ``FREQMOD`` on the :ref:`modopt` command)

            * ``VAL2`` - Attenuation (product of attenuation constant and period); not used if ``VAL1`` = YES

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VMEN:

            * ``VAL1`` - Mean flow velocity component in the X direction

            * ``VAL2`` - Mean flow velocity component in the Y direction

            * ``VAL3`` - Mean flow velocity component in the Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = UFOR:

            * ``VAL1`` - Real part of complex force potential

            * ``VAL2`` - Imaginary part of complex force potential

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = SFOR:

            * ``VAL1`` - X component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL2`` - Y component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL3`` - Z component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = HFLW:

            * ``VAL1`` - Real part of volumetric heat source for viscous-thermal acoustics

            * ``VAL2`` - Imaginary part of volumetric heat source for viscous-thermal acoustics

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

        val6 : str
            Value associated with the ``Lab`` item or table name reference for tabular boundary conditions. Use
            only ``VAL1`` for TEMP, FLUE, HGEN, DGEN, MVDI, CHRGD, PORT, and SPRE.

            Tabular input is supported for certain labels (see :ref:`Notes for details). To specify a table,
            enclose the table name in percent signs (%) (e.g., <BF_notes>` :ref:`bf`,
            ``Node``,TEMP,``tabname``). Use the :ref:`dim` command to define a table.

            If ``Lab`` = MASS for acoustics:

            * ``VAL1`` - Mass source with units of kg/(m :sup:`3` *s) in a harmonic analysis or in a transient
              analysis solved with the velocity potential formulation; or mass source rate with units of kg/(m
              :sup:`3` *s :sup:`2` ) in a transient analysis solved with the pressure formulation; or power source
              with units of watts in an energy diffusion solution for room acoustics

            * ``VAL2`` - Phase angle in degrees

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for acoustics (velocity components in a harmonic analysis or in a transient
            analysis solved with the velocity potential formulation; or acceleration components in a transient
            analysis solved with the pressure formulation):

            * ``VAL1`` - X component

            * ``VAL2`` - Y component

            * ``VAL3`` - Z component

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = VELO for electromagnetics (velocity and angular velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Velocity component in the X direction

            * ``VAL2`` - Velocity component in the Y direction

            * ``VAL3`` - Velocity component in the Z direction

            * ``VAL4`` - Angular velocity about the X axis (rad/sec)

            * ``VAL5`` - Angular velocity about the Y axis (rad/sec)

            * ``VAL6`` - Angular velocity about the Z axis (rad/sec)

            If ``Lab`` = VELO for thermal (velocity components in the global Cartesian coordinate system):

            * ``VAL1`` - Mass transport velocity component in X direction

            * ``VAL2`` - Mass transport velocity component in Y direction

            * ``VAL3`` - Mass transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VELO for diffusion (transport velocity):

            * ``VAL1`` - Transport velocity component in X direction

            * ``VAL2`` - Transport velocity component in Y direction

            * ``VAL3`` - Transport velocity component in Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = IMPD:

            * ``VAL1`` - Resistance in N⋅s/m :sup:`3`

            * ``VAL2`` - Reactance in N⋅s/m :sup:`3`

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = FPBC:

            * ``VAL1`` - Phase shift (product of phase constant and period in unit radian); or Floquet boundary
              flag (set ``VAL1`` = YES) for a modal analysis that solves the eigenvalues with a specified
              frequency ( ``FREQMOD`` on the :ref:`modopt` command)

            * ``VAL2`` - Attenuation (product of attenuation constant and period); not used if ``VAL1`` = YES

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = VMEN:

            * ``VAL1`` - Mean flow velocity component in the X direction

            * ``VAL2`` - Mean flow velocity component in the Y direction

            * ``VAL3`` - Mean flow velocity component in the Z direction

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = UFOR:

            * ``VAL1`` - Real part of complex force potential

            * ``VAL2`` - Imaginary part of complex force potential

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

            If ``Lab`` = SFOR:

            * ``VAL1`` - X component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL2`` - Y component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL3`` - Z component of shear force for viscous-thermal acoustics or poroelastic acoustics

            * ``VAL4`` - X-component phase angle in degrees

            * ``VAL5`` - Y-component phase angle in degrees

            * ``VAL6`` - Z-component phase angle in degrees

            If ``Lab`` = HFLW:

            * ``VAL1`` - Real part of volumetric heat source for viscous-thermal acoustics

            * ``VAL2`` - Imaginary part of volumetric heat source for viscous-thermal acoustics

            * ``VAL3`` - Not used

            * ``VAL4`` - Not used

            * ``VAL5`` - Not used

            * ``VAL6`` - Not used

        meshflag : str
            Specifies how to apply nodal body-force loading on the mesh. Valid in a `nonlinear adaptivity
            analysis <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVREZ.html>`_ when
            ``Lab`` = HGEN or TEMP, and ``Node`` is not a component name.

            * 0 - Nodal body-force loading occurs on the current mesh (default).
            * 1 - Nodal body-force loading occurs on the initial mesh for nonlinear adaptivity.

        Notes
        -----

        .. _BF_notes:

        Defines a nodal body-force load (such as temperature in a structural analysis, heat generation rate
        in a thermal analysis, etc.). Nodal body loads default to the :ref:`bfunif` values, if they were
        previously specified.

        Table names are valid for ``Lab`` value ( ``VALn`` ) inputs in these cases only:

        * ``VAL1`` = ``tabname`` for:

        temperatures (TEMP), diffusing substance generation rates (DGEN), and heat generation rates (HGEN).

        * ``VAL1`` = ``tabname1`` and ``VAL2`` = ``tabname2`` for:

        mass source, mass source rate, or power source (MASS); the Floquet periodic boundary condition
          (FPBC); the force potential (UFOR); and the volumetric heat source (HFLW).

        * ``VAL1`` = ``tabname1``, ``VAL2`` = ``tabname2``, and ``VAL3`` = ``tabname3`` for:

        mean flow velocities (VMEN).

        * ``VAL1`` = ``tabname1``, ``VAL2`` = ``tabname2``, ``VAL3`` = ``tabname3``, ``VAL4`` =
          ``tabname4``, ``VAL5`` = ``tabname5``, and ``VAL6`` = ``tabname6`` for:

        velocities or accelerations (VELO); and shear force (SFOR).

        The heat generation rate loads specified with the :ref:`bf` command are multiplied by the weighted
        nodal volume of each element adjacent to that node. This yields the total heat generation at that
        node.

        In a modal analysis, the Floquet periodic boundary condition (FPBC) is only valid for the acoustic
        elements ``FLUID30``, ``FLUID220``, and ``FLUID221``.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = (
            f"BF,{node},{lab},{val1},{val2},{val3},{val4},{val5},{val6},{meshflag}"
        )
        return self.run(command, **kwargs)

    def bfcum(
        self, lab: str = "", oper: str = "", fact: str = "", tbase: str = "", **kwargs
    ):
        r"""Specifies that nodal body-force loads are to be accumulated.

        Mechanical APDL Command: `BFCUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFCUM.html>`_

        **Command default:**

        .. _BFCUM_default:

        Replace previous values.

        Parameters
        ----------
        lab : str
            Valid body load label. If ALL, use all appropriate labels.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        oper : str
            Accumulation key:

            * ``REPL`` - Subsequent values replace the previous values (default).

            * ``ADD`` - Subsequent values are added to the previous values.

            * ``IGNO`` - Subsequent values are ignored.

        fact : str
            Scale factor for the nodal body load values. Zero (or blank) defaults to 1.0. Use a small number
            for a zero scale factor. The scale factor is not applied to body load phase angles.

        tbase : str
            Used (only with ``Lab`` = TEMP) to calculate the temperature used in the add or replace operation
            (see ``Oper`` ) as:

            Temperature = ``TBASE`` + ``FACT`` \* ( ``T`` - ``TBASE`` )

            where ``T`` is the temperature specified on subsequent :ref:`bf` commands. ``TBASE`` defaults to
            zero.

        Notes
        -----

        .. _BFCUM_notes:

        Allows repeated nodal body-force loads to be replaced, added, or ignored. Nodal body loads are
        applied with the :ref:`bf` command. Issue the :ref:`bflist` command to list the nodal body loads.
        The operations occur when the next body loads are defined. For example, issuing the :ref:`bf`
        command with a temperature of 250 after a previous :ref:`bf` command with a temperature of 200
        causes the new value of the temperature to be 450 with the add operation, 250 with the replace
        operation, or 200 with the ignore operation. A scale factor is also available to multiply the next
        value before the add or replace operation. A scale factor of 2.0 with the previous "add" example
        results in a temperature of 700. The scale factor is applied even if no previous values exist. Issue
        :ref:`bfcum`,STAT to show the current label, operation, and scale factors. Solid model boundary
        conditions are not affected by this command, but boundary conditions on the FE model are affected.
        FE boundary conditions may still be overwritten by existing solid model boundary conditions if a
        subsequent boundary condition transfer occurs.

        :ref:`bfcum` does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"BFCUM,{lab},{oper},{fact},{tbase}"
        return self.run(command, **kwargs)

    def bfdele(self, node: str = "", lab: str = "", **kwargs):
        r"""Deletes nodal body-force loads.

        Mechanical APDL Command: `BFDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFDELE.html>`_

        Parameters
        ----------
        node : str
            Node at which body load is to be deleted. If ALL, delete for all selected nodes ( :ref:`nsel` ).
            If ``Node`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI). You can substitute a component name for ``Node``.

        lab : str
            Valid body load label. If ALL, use all appropriate labels. See :ref:`bf`.

        Notes
        -----

        .. _BFDELE_notes:

        Deletes nodal body-force loads for a specified node and label. Nodal body loads are defined via
        :ref:`bf`.

        This command is also valid in PREP7.
        """
        command = f"BFDELE,{node},{lab}"
        return self.run(command, **kwargs)

    def bfe(
        self,
        elem: str = "",
        lab: str = "",
        stloc: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        **kwargs,
    ):
        r"""Defines an element body-force load.

        Mechanical APDL Command: `BFE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFE.html>`_

        Parameters
        ----------
        elem : str
            The element to which body load applies. If ALL, apply to all selected elements ( :ref:`esel` ).
            A component name may also be substituted for ``Elem``.

        lab : str
            Valid body load label. Valid labels are also listed for each element type in the `Element
            Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_
            under "Body Loads" in the input table.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        stloc : str
            Starting location for entering ``VAL`` data, below. For example, if ``STLOC`` = 1, data input in
            the ``VAL1`` field applies to the first element body load item available for the element type,
            ``VAL2`` applies to the second element item, etc. If ``STLOC`` = 5, data input in the ``VAL1``
            field applies to the fifth element item, etc. Defaults to 1.

        val1 : str
            For ``Lab`` = TEMP, FLUE, DGEN, HGEN, and CHRGD, ``VAL1`` -- ``VAL4`` represent body load values
            at the starting location and subsequent locations (usually nodes) in the element. ``VAL1`` can
            also represent a table name for use with tabular boundary conditions. Enter only ``VAL1`` for a
            uniform body load across the element. For nonuniform loads, the values must be input in the same
            order as shown in the input table for the element type. Values initially default to the
            :ref:`bfunif` value (except for CHRGD which defaults to zero). For subsequent specifications, a
            blank leaves a previously specified value unchanged; if the value was not previously specified,
            the default value as described in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_ is used.

            For ``Lab`` = JS and ``STLOC`` = 1, ``VAL1``, ``VAL2`` and ``VAL3`` are the X, Y, and Z
            components of current density (in the element coordinate system), and ``VAL4`` is the phase
            angle.

            For ``Lab`` = EF and ``STLOC`` = 1, ``VAL1``, ``VAL2``, and ``VAL3`` are the X, Y, and Z
            components of electric field (in the global Cartesian coordinate system).

            If ``Lab`` = FVIN in a unidirectional Mechanical APDL to Ansys CFX analysis, ``VAL2`` is the
            volume interface number (not available from within the GUI), and ``VAL1``, ``VAL3``, and
            ``VAL4`` are not used.

            For ``Lab`` = FORC and ``STLOC`` = 1, ``VAL1``, ``VAL2``, and ``VAL3`` are the real X, Y, and Z
            components of force density (in the global Cartesian coordinate system).

            For analyses that allow complex input, if ``Lab`` = FORC and ``STLOC`` = 4, ``VAL1``, ``VAL2``,
            and ``VAL3`` are the imaginary X, Y, and Z components of force density (in the global Cartesian
            coordinate system).

        val2 : str
            For ``Lab`` = TEMP, FLUE, DGEN, HGEN, and CHRGD, ``VAL1`` -- ``VAL4`` represent body load values
            at the starting location and subsequent locations (usually nodes) in the element. ``VAL1`` can
            also represent a table name for use with tabular boundary conditions. Enter only ``VAL1`` for a
            uniform body load across the element. For nonuniform loads, the values must be input in the same
            order as shown in the input table for the element type. Values initially default to the
            :ref:`bfunif` value (except for CHRGD which defaults to zero). For subsequent specifications, a
            blank leaves a previously specified value unchanged; if the value was not previously specified,
            the default value as described in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_ is used.

            For ``Lab`` = JS and ``STLOC`` = 1, ``VAL1``, ``VAL2`` and ``VAL3`` are the X, Y, and Z
            components of current density (in the element coordinate system), and ``VAL4`` is the phase
            angle.

            For ``Lab`` = EF and ``STLOC`` = 1, ``VAL1``, ``VAL2``, and ``VAL3`` are the X, Y, and Z
            components of electric field (in the global Cartesian coordinate system).

            If ``Lab`` = FVIN in a unidirectional Mechanical APDL to Ansys CFX analysis, ``VAL2`` is the
            volume interface number (not available from within the GUI), and ``VAL1``, ``VAL3``, and
            ``VAL4`` are not used.

            For ``Lab`` = FORC and ``STLOC`` = 1, ``VAL1``, ``VAL2``, and ``VAL3`` are the real X, Y, and Z
            components of force density (in the global Cartesian coordinate system).

            For analyses that allow complex input, if ``Lab`` = FORC and ``STLOC`` = 4, ``VAL1``, ``VAL2``,
            and ``VAL3`` are the imaginary X, Y, and Z components of force density (in the global Cartesian
            coordinate system).

        val3 : str
            For ``Lab`` = TEMP, FLUE, DGEN, HGEN, and CHRGD, ``VAL1`` -- ``VAL4`` represent body load values
            at the starting location and subsequent locations (usually nodes) in the element. ``VAL1`` can
            also represent a table name for use with tabular boundary conditions. Enter only ``VAL1`` for a
            uniform body load across the element. For nonuniform loads, the values must be input in the same
            order as shown in the input table for the element type. Values initially default to the
            :ref:`bfunif` value (except for CHRGD which defaults to zero). For subsequent specifications, a
            blank leaves a previously specified value unchanged; if the value was not previously specified,
            the default value as described in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_ is used.

            For ``Lab`` = JS and ``STLOC`` = 1, ``VAL1``, ``VAL2`` and ``VAL3`` are the X, Y, and Z
            components of current density (in the element coordinate system), and ``VAL4`` is the phase
            angle.

            For ``Lab`` = EF and ``STLOC`` = 1, ``VAL1``, ``VAL2``, and ``VAL3`` are the X, Y, and Z
            components of electric field (in the global Cartesian coordinate system).

            If ``Lab`` = FVIN in a unidirectional Mechanical APDL to Ansys CFX analysis, ``VAL2`` is the
            volume interface number (not available from within the GUI), and ``VAL1``, ``VAL3``, and
            ``VAL4`` are not used.

            For ``Lab`` = FORC and ``STLOC`` = 1, ``VAL1``, ``VAL2``, and ``VAL3`` are the real X, Y, and Z
            components of force density (in the global Cartesian coordinate system).

            For analyses that allow complex input, if ``Lab`` = FORC and ``STLOC`` = 4, ``VAL1``, ``VAL2``,
            and ``VAL3`` are the imaginary X, Y, and Z components of force density (in the global Cartesian
            coordinate system).

        val4 : str
            For ``Lab`` = TEMP, FLUE, DGEN, HGEN, and CHRGD, ``VAL1`` -- ``VAL4`` represent body load values
            at the starting location and subsequent locations (usually nodes) in the element. ``VAL1`` can
            also represent a table name for use with tabular boundary conditions. Enter only ``VAL1`` for a
            uniform body load across the element. For nonuniform loads, the values must be input in the same
            order as shown in the input table for the element type. Values initially default to the
            :ref:`bfunif` value (except for CHRGD which defaults to zero). For subsequent specifications, a
            blank leaves a previously specified value unchanged; if the value was not previously specified,
            the default value as described in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_ is used.

            For ``Lab`` = JS and ``STLOC`` = 1, ``VAL1``, ``VAL2`` and ``VAL3`` are the X, Y, and Z
            components of current density (in the element coordinate system), and ``VAL4`` is the phase
            angle.

            For ``Lab`` = EF and ``STLOC`` = 1, ``VAL1``, ``VAL2``, and ``VAL3`` are the X, Y, and Z
            components of electric field (in the global Cartesian coordinate system).

            If ``Lab`` = FVIN in a unidirectional Mechanical APDL to Ansys CFX analysis, ``VAL2`` is the
            volume interface number (not available from within the GUI), and ``VAL1``, ``VAL3``, and
            ``VAL4`` are not used.

            For ``Lab`` = FORC and ``STLOC`` = 1, ``VAL1``, ``VAL2``, and ``VAL3`` are the real X, Y, and Z
            components of force density (in the global Cartesian coordinate system).

            For analyses that allow complex input, if ``Lab`` = FORC and ``STLOC`` = 4, ``VAL1``, ``VAL2``,
            and ``VAL3`` are the imaginary X, Y, and Z components of force density (in the global Cartesian
            coordinate system).

        Notes
        -----

        .. _BFE_notes:

        Defines an element body-force load (such as the temperature in a structural analysis or the heat-
        generation rate in a thermal analysis). Body loads and element specific defaults are described for
        each element type in the `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. If both the
        :ref:`bf` and :ref:`bfe` commands are used to apply a
        body-force load to an element, the :ref:`bfe` command takes precedence.

        Imaginary values for FORC loading via :ref:`bfe` is supported by current-technology solid elements (
        ``PLANE182``, ``PLANE183``, ``SOLID185``, ``SOLID186``, ``SOLID187``, and ``SOLID285`` ) and
        reinforcing elements ( ``REINF263``, ``REINF264``, and ``REINF265`` ). Use only for modal or
        harmonic analyses. Large-deflection effects must be disabled ( :ref:`nlgeom`,OFF).

        The following topics for applying HGEN loading via the :ref:`bfe` command are available:

        For HGEN loading on layered thermal solid elements ``SOLID278`` / ``SOLID279`` (KEYOPT(3) = 1 or 2),
        or layered thermal shell elements ``SHELL131`` / ``SHELL132`` (KEYOPT(3) = 1), ``STLOC`` refers to
        the layer number (not the node). In such cases, specify ``VAL1`` through ``VAL4`` to specify the
        heat-generation values for the appropriate layers. Heat generation is constant over the layer.

        For HGEN loading on `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        elements ``REINF263``, ``REINF264``, and ``REINF265``, ``STLOC`` refers to the corner locations of
        the reinforcing members (individual reinforcings):

        * ``REINF263`` and ``REINF264`` : Specify ``VAL1`` and ``VAL2`` for each member. For tables, specify
          ``VAL1`` only.

        * ``REINF265`` : Specify ``VAL1``, ``VAL2``, ``VAL3``, and ``VAL4`` for each member. For tables,
          specify ``VAL1`` only.

        For FORC loading on reinforcing elements, ``STLOC`` refers to real ( ``STLOC`` = 1) or imaginary (
        ``STLOC`` = 4) components.

        When using the `standard method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_ for
        defining reinforcing, this is the only way to apply a body load (HGEN or FORC) on the reinforcing
        members created after generating the REINF ``nnn`` reinforcing elements ( :ref:`ereinf` ). If
        applying FORC loading, Mechanical APDL applies a uniform load to all reinforcing members if there
        are
        multiple members in selected elements.

        When using the `mesh-independent method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_ for
        defining reinforcing, you can apply a body load on the reinforcing members in the same way. The
        preferred method, however, is to apply loads on the ``MESH200`` elements (via :ref:`bfe` or
        :ref:`bf` for HGEN, BFE for FORC) before generating the REINF ``nnn`` reinforcing elements (
        :ref:`ereinf` ). Mechanical APDL maps the loads from the ``MESH200`` elements to the newly generated
        REINF
        ``nnn`` reinforcing elements automatically. If you need to apply the loads after generating the
        reinforcing elements, apply them to ``MESH200`` elements and issue :ref:`bfport` to transfer the
        loads to the reinforcing members.

        You can specify a table name ( ``VAL1`` ) when using temperature (TEMP), diffusing substance
        generation rate (DGEN), heat generation rate (HGEN), and current density (JS) body load labels.

        For the body-force-density label (FORC), you can specify a table for any of the ``VAL1`` through
        ``VAL3`` arguments. Both 1D and 2D tables are valid; however, only 1D tables are valid in mode-
        superposition harmonic and mode-superposition transient analyses.

        Enclose the table name ( ``tabname`` ) in percent signs (%), for example :

        :ref:`bfe`, ``Elem``, ``Lab``, ``STLOC``,``tabname``

        Use the :ref:`dim` command to define a table. For information on primary variables for each load
        type, see `Applying Loads Using Tabular Input
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS2_6.html#gbas5dexample>`_

        For ``Lab`` = TEMP, each table defines ``NTEMP`` temperatures, as follows:

        * For layered elements, ``NTEMP`` is the number of layer interface corners that allow temperature
          input.

        * For non-layered elements, ``NTEMP`` is the number of corner nodes.

        The temperatures apply to element items with a starting location of ``STLOC`` + ``n``, where n is
        the value field location ( ``VALn`` ) of the table name input.

        For layered elements, a single :ref:`bfe` command returns temperatures for one layer interface.
        Multiple :ref:`bfe` commands are necessary for defining all layered temperatures.

        For beam, pipe and elbow elements that allow multiple temperature inputs per node, define the
        tabular load for the first node only (Node I), as loads on the remaining nodes are applied
        automatically. For example, to specify a tabular temperature load on a ``PIPE288`` element with the
        through-wall-gradient option (KEYOPT(1) = 0), the :ref:`bfe` command looks like this:

        :ref:`bfe`, ``Elem``,TEMP,1,``tabOut``, ``tabIn%``

        where %

         ``tabOut`` and ``tabIn`` and are the tables applied to the outer and inner surfaces of the pipe
        wall, respectively.

        When a tabular function load is applied to an element, the load does not vary according to the
        positioning of the element in space.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"BFE,{elem},{lab},{stloc},{val1},{val2},{val3},{val4}"
        return self.run(command, **kwargs)

    def bfecum(
        self, lab: str = "", oper: str = "", fact: str = "", tbase: str = "", **kwargs
    ):
        r"""Specifies whether to ignore subsequent element body force loads.

        Mechanical APDL Command: `BFECUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFECUM.html>`_

        **Command default:**

        .. _BFECUM_default:

        Replace previous values.

        Parameters
        ----------
        lab : str
            Valid body load label. If ALL, use all appropriate labels.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        oper : str
            Replace or ignore key:

            * ``REPL`` - Subsequent values replace the previous values (default).

            * ``IGNO`` - Subsequent values are ignored.

        fact : str
            Scale factor for the element body load values. Zero (or blank) defaults to 1.0. Use a small
            number for a zero scale factor. The scale factor is not applied to body load phase angles.

        tbase : str
            Used (only with ``Lab`` = TEMP) to calculate the temperature used in the add or replace operation
            (see ``Oper`` ) as:

            Temperature = ``TBASE`` + ``FACT`` \* ( ``T`` - ``TBASE`` )

            where ``T`` is the temperature specified on subsequent :ref:`bfe` commands. ``TBASE`` defaults to
            zero.

        Notes
        -----

        .. _BFECUM_notes:

        Allows repeated element body-force loads to be replaced or ignored. Element body loads are applied
        with the :ref:`bfe` command. Issue the :ref:`bfelist` command to list the element body loads. The
        operations occur when the next body loads are defined. For example, issuing the :ref:`bfe` command
        with a temperature value of 25 after a previous :ref:`bfe` command with a temperature value of 20
        causes the new value of that temperature to be 25 with the replace operation, or 20 with the ignore
        operation. A scale factor is also available to multiply the next value before the replace operation.
        A scale factor of 2.0 with the previous "replace" example results in a temperature of 50. The scale
        factor is applied even if no previous values exist. Issue :ref:`bfecum`,STAT to show the current
        label, operation, and scale factors.

        :ref:`bfecum` does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"BFECUM,{lab},{oper},{fact},{tbase}"
        return self.run(command, **kwargs)

    def bfedele(self, elem: str = "", lab: str = "", **kwargs):
        r"""Deletes element body-force loads.

        Mechanical APDL Command: `BFEDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFEDELE.html>`_

        Parameters
        ----------
        elem : str
            Element at which body load is to be deleted. If ALL, delete for all selected elements [ A
            component name may also be substituted for ``ELEM``.

        lab : str
            Valid body load label. If ALL, use all appropriate labels. See :ref:`bfe` command for labels.

        Notes
        -----

        .. _BFEDELE_notes:

        Deletes element body-force loads for a specified element and label. Element body loads may be
        defined with the :ref:`bfe` commands.

        This command is also valid in PREP7.
        """
        command = f"BFEDELE,{elem},{lab}"
        return self.run(command, **kwargs)

    def bfelist(self, elem: str = "", lab: str = "", **kwargs):
        r"""Lists the element body-force loads.

        Mechanical APDL Command: `BFELIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFELIST.html>`_

        Parameters
        ----------
        elem : str
            Element at which body load is to be listed. If ALL (or blank), list for all selected elements (
            :ref:`esel` ). If ``ELEM`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may also be substituted for ``ELEM``.

        lab : str
            Valid body load label. If ALL (or blank), use all appropriate labels. See :ref:`bfe` command for
            labels.

        Notes
        -----

        .. _BFELIST_notes:

        Lists the element body-force loads for the specified element and label. Element body loads may be
        defined with the :ref:`bfe` command.

        This command is valid in any processor.
        """
        command = f"BFELIST,{elem},{lab}"
        return self.run(command, **kwargs)

    def bfescal(self, lab: str = "", fact: str = "", tbase: str = "", **kwargs):
        r"""Scales element body-force loads.

        Mechanical APDL Command: `BFESCAL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFESCAL.html>`_

        Parameters
        ----------
        lab : str
            Valid body load label. If ALL, use all appropriate labels.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        fact : str
            Scale factor for the element body load values. Zero (or blank) defaults to 1.0. Use a small
            number for a "zero" scale factor. The scale factor is not applied to body load phase angles.

        tbase : str
            Base temperature for temperature difference. Used only with ``Lab`` = TEMP. Scale factor is
            applied to the temperature difference ( ``T`` - ``TBASE`` ) and then added to ``TBASE``. ``T``
            is the current temperature.

        Notes
        -----

        .. _BFESCAL_notes:

        Scales element body-force loads on the selected elements in the database. Issue the :ref:`bfelist`
        command to list the element body loads. Solid model boundary conditions are not scaled by this
        command, but boundary conditions on the FE model are scaled. (Note that such scaled FE boundary
        conditions may still be overwritten by unscaled solid model boundary conditions if a subsequent
        boundary condition transfer occurs.)

        :ref:`bfescal` does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"BFESCAL,{lab},{fact},{tbase}"
        return self.run(command, **kwargs)

    def bflist(self, node: str = "", lab: str = "", **kwargs):
        r"""Lists the body-force loads on nodes.

        Mechanical APDL Command: `BFLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFLIST.html>`_

        Parameters
        ----------
        node : str
            Node at which body load is to be listed. If ALL (or blank), list for all selected nodes (
            :ref:`nsel` ). If ``Node`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). You can substitute a component name for ``Node``.

        lab : str
            Valid body load label. If ALL (or blank), use all appropriate labels. (See :ref:`bf`.)

        Notes
        -----

        .. _BFLIST_notes:

        Lists the body-force loads for the specified node and label. Nodal body loads are defined via
        :ref:`bf`.

        This command is valid in any processor.
        """
        command = f"BFLIST,{node},{lab}"
        return self.run(command, **kwargs)

    def bfport(self, cmname: str = "", **kwargs):
        r"""Transfers a thermal body-force load (HGEN) from selected ``MESH200`` elements to reinforcing
        elements.

        Mechanical APDL Command: `BFPORT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFPORT.html>`_

        Parameters
        ----------
        cmname : str
            Component name containing a list of selected ``MESH200`` elements.

        Notes
        -----

        .. _BFPORT_notes:

        This command transfers a thermal body-force load (HGEN) from selected ``MESH200`` elements to
        associated reinforcing elements or members (individual reinforcings). The association is established
        via :ref:`ereinf` using the `mesh-independent method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_ for
        defining reinforcing.

        Issue this command after issuing :ref:`ereinf`.

        Select ``MESH200`` elements by issuing this command and specifying the component, or by issuing
        :ref:`esel`. (If you specify a component name, :ref:`esel` is ignored.)

        This command supports a thermal body-force load (HGEN) only.

        To define the thermal body-force load on ``MESH200`` elements, issue :ref:`bfe` or :ref:`bf`.

        This command is also valid in PREP7.
        """
        command = f"BFPORT,{cmname}"
        return self.run(command, **kwargs)

    def bfscale(self, lab: str = "", fact: str = "", tbase: str = "", **kwargs):
        r"""Scales body-force loads at nodes.

        Mechanical APDL Command: `BFSCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFSCALE.html>`_

        Parameters
        ----------
        lab : str
            Valid body load label. If ALL, use all appropriate labels.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        fact : str
            Scale factor for the nodal body load values. Zero (or blank) defaults to 1.0. Use a small number
            for a zero scale factor. The scale factor is not applied to body load phase angles.

        tbase : str
            Base temperature for temperature difference. Used only with ``Lab`` = TEMP. Scale factor is
            applied to the temperature difference ( ``T`` - ``TBASE`` ) and then added to ``TBASE``. ``T``
            is the current temperature.

        Notes
        -----

        .. _BFSCALE_notes:

        Scales body-force loads in the database on the selected nodes. Issue the :ref:`bflist` command to
        list the nodal body loads. Solid model boundary conditions are not scaled by this command, but
        boundary conditions on the FE model are scaled. Such scaled FE boundary conditions may still be
        overwritten by unscaled solid model boundary conditions if a subsequent boundary condition transfer
        occurs.

        :ref:`bfscale` does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"BFSCALE,{lab},{fact},{tbase}"
        return self.run(command, **kwargs)

    def bfunif(self, lab: str = "", value: str = "", **kwargs):
        r"""Assigns a uniform body-force load to all nodes.

        Mechanical APDL Command: `BFUNIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BFUNIF.html>`_

        **Command default:**

        .. _BFUNIF_default:

        Set TEMP to the reference temperature ( :ref:`tref` but not :ref:`mp`,REFT), and FLUE and HGEN to
        zero.

        Parameters
        ----------
        lab : str
            Valid body load label. If ALL, use all appropriate labels.

            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        value : str
            Uniform value associated with ``Lab`` item, or table name when specifying tabular boundary
            conditions. To specify a table, enclose the table name in percent signs (%), for example,
            :ref:`bfunif`, ``Lab``,``tabname``.

        Notes
        -----

        .. _BFUNIF_notes:

        In a transient or nonlinear thermal analysis, the uniform temperature is used during the first
        iteration of a solution as follows: (a) as the starting nodal temperature except where temperatures
        are explicitly specified ( :ref:`d`, :ref:`dk` ), and (b) to evaluate temperature-dependent material
        properties. In a structural analysis, the uniform temperature is used as the default temperature for
        thermal strain calculations and material property evaluation except where body load temperatures are
        specified ( :ref:`bf`, :ref:`bfe`, :ref:`bfk`, :ref:`ldread` ). In other scalar field analyses, the
        uniform temperature is used for material property evaluation.

        An alternate command, :ref:`tunif`, may be used to set the uniform temperature instead of
        :ref:`bfunif`,TEMP. Since :ref:`tunif` (or :ref:`bfunif`,TEMP) is step-applied in the first
        iteration, you should use :ref:`bf`, ALL, TEMP, Value to ramp on a uniform temperature load.

        You can specify a table name only when using temperature (TEMP), heat generation rate (HGEN), and
        diffusing substance generation rate (DGEN) body load labels. When using TEMP, you can define a one-
        dimensional table that varies with respect to time (TIME) only. When defining this table, enter TIME
        as the primary variable. No other primary variables are valid.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"BFUNIF,{lab},{value}"
        return self.run(command, **kwargs)

    def tunif(self, temp: str = "", **kwargs):
        r"""Assigns a uniform temperature to all nodes.

        Mechanical APDL Command: `TUNIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TUNIF.html>`_

        Parameters
        ----------
        temp : str
            Uniform temperature assigned to the nodes. If a ``TEMP`` value is not specified, the uniform
            temperature is set to zero.

        Notes
        -----

        .. _TUNIF_notes:

        :ref:`tunif` is a convenient form of the more general :ref:`bfunif` command.

        In a transient or nonlinear thermal analysis, the uniform temperature is used during the first
        iteration of a solution as follows:

        * as the starting nodal temperature, except where temperatures are explicitly specified ( :ref:`d`,
          :ref:`dk` )

        * to evaluate temperature-dependent material properties.

        In a structural analysis, the uniform temperature is used as the
         default temperature for thermal strain calculations and material property evaluation, except where body load
        temperatures are specified ( :ref:`bf`, :ref:`bfe`, :ref:`bfk`, :ref:`ldread` ). In other scalar
        field analyses, the uniform temperature is used for material property evaluation.

        Because :ref:`tunif` (or :ref:`bfunif`,TEMP) is step-applied in the first iteration, issue a
        :ref:`bf`,ALL,TEMP, ``Value`` command to ramp on a uniform temperature load.

        The command default sets the uniform temperature to the reference temperature defined via the
        :ref:`tref` command only (and not the :ref:`mp`,REFT command).

        If using the command default to set the uniform temperature (to the reference temperature set via
        :ref:`tref` ), you can convert temperature-dependent secant coefficients of thermal expansion
        (SCTEs) from the definition temperature to the uniform temperature. To do so, issue the
        :ref:`mpamod` command.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"TUNIF,{temp}"
        return self.run(command, **kwargs)
