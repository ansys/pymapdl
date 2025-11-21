# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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


class DataTables:

    def cbtmp(self, temp: str = "", **kwargs):
        r"""Specifies a temperature for composite-beam input.

        Mechanical APDL Command: `CBTMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CBTMP.html>`_

        Parameters
        ----------
        temp : str
            Temperature value.

        Notes
        -----
        The :ref:`cbtmp` command, one of several `composite beam-section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_,
        specifies a temperature to be associated with the data input via subsequent :ref:`cbmx`
        (preintegrated cross-section stiffness), :ref:`cbmd` (preintegrated section mass), or :ref:`cbte`
        (thermal-expansion) commands.

        The specified temperature remains active unt il the next :ref:`cbtmp` command is issued.

        An unspecified temperature value defaults to zero.

        For complete information, see `Using Preintegrated Composite Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_
        """
        command = f"CBTMP,{temp}"
        return self.run(command, **kwargs)

    def cgrow(
        self, action: str = "", par1: str = "", par2: str = "", par3: str = "", **kwargs
    ):
        r"""Specifies crack-growth options in a fracture analysis.

        Mechanical APDL Command: `CGROW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CGROW.html>`_

        Parameters
        ----------
        action : str
            Specifies the action for defining or manipulating crack-growth data:

            * `Command Specification for Action= NEW
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ NEW - Initiate
              a new set of crack-growth simulation data (default).

            * `Command Specification for Action= CID
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ CID - Specify
              the crack-calculation ( :ref:`cint` ) ID for energy-release rates to be used in the fracture
              criterion calculation.

            * `Command Specification for Action= FCOPTION
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ FCOPTION -
              Specify the fracture criterion for crack-growth/delamination.

            * `Command Specification for Action= CSFL
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ CSFL - Specify
              a crack-surface load for crack-growth.

            * `Command Specification for Action= CPATH
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ CPATH - Specify
              the element component for crack-growth.

            * `Command Specification for Action= DTIME
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ DTIME - Specify
              the initial time step for crack-growth.

            * `Command Specification for Action= DTMIN
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ DTMIN - Specify
              the minimum time step for crack-growth.

            * `Command Specification for Action= DTMAX
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ DTMAX - Specify
              the maximum time step for crack-growth.

            * `Command Specification for Action= FCRAT
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ FCRAT -
              Fracture criterion ratio ( `fc
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#vcctuserdeffractcrit>`_
              c ).

            * `Command Specification for Action= STOP
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ STOP - Stops
              the analysis when the specified criterion ( ``Par1`` ) is reached.

            * `Command Specification for Action= METHOD
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ METHOD - Define
              the method of crack propagation.

            * `Command Specification for Action= FCG
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ FCG - Specifies
              `fatigue crack-growth
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracfcgxfem.html#fracfcgxfemexample>`_.

            * `Command Specification for Action= SOPT
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ SOPT -
              Specifies the crack-growth solution option in a multicrack analysis.

            * `Command Specification for Action= RMCONT
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ RMCONT -
              Specifies remeshing control options for mesh coarsening.

            * `Command Specification for Action= NPLOAD
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CGROW.html#>`_ NPLOAD -
              Specifies `nonproportional loading
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#>`_ control options
              for fatigue crack-growth.

        par1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CGROW.html>`_ for further
            information.

        par2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CGROW.html>`_ for further
            information.

        par3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CGROW.html>`_ for further
            information.

        Other Parameters
        ----------------
        **Command Specification for Action= NEW**

        .. _CGROW_NEW:

        * ``Par1`` - Crack-growth data set ID (integer value).

        **Command Specification for Action= CID**

        .. _CGROW_CID:

        * ``Par1`` - Contour-integral calculation ( :ref:`cint` ) ID for energy-release rates to be used in
          fracture criterion calculation.

        **Command Specification for Action= FCOPTION**

        .. _CGROW_FCOPTION:

        * ``Par1`` - **MTAB** - Crack-growth fracture criterion used with the material data table (
        :ref:`tb`, `CGCR -- Crack-Growth Fracture Criterion
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_TB.html#eq4d382484-99d1-41ac-82dc-5a82d9911274>`_
        CGCR).

          **GTC** - Defines the critical energy-release rate, a simple fracture criterion used for the `VCCT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#vcctsimassum>`_ method.

          **KIC** - Defines the `critical stress-intensity factor <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eqa7ac21d8-c5cc-41bd-aced-f664166c2ea0>`_. Valid for the `SMART <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_ method only.

          **JIC** - Defines the `critical J-integral <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eqb5e4514c-a107-4016-847f-af649a691f2f>`_. Valid for the `SMART <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_ method only.

        * ``Par2`` - For ``Par1`` = MTAB: Material ID for the material data table.

          For I ``Par1`` = GTC: Critical energy-release rate value.

          For ``Par1`` = KIC: Critical stress-intensity factor value.

          For ``Par1`` = JIC: Critical J-integral value.

        * ``Par3`` - For ``Par1`` = MTAB, KIC, or JIC: Specifies the fracture-parameter contour to use for
          `SMART
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
          crack-growth evaluation. Default = 2.

        **Command Specification for Action= CSFL**

        .. _CGROW_CSFL:

        * ``Par1`` - Crack-surface load options:

          * PRES - New crack-surface pressure load.
          * CZM - Entire crack-surface enhanced by ``INTER204`` 3D 16-node cohesive elements (generated
            automatically during the first remeshing around the associated crack). See :ref:`CGROW_notes`.

        * ``Par2`` - When ``Par1`` = PRES: (blank)

          When ``Par1`` = CZM: A valid material ID (defined via :ref:`tb`,CZM,,,,BILI, :ref:`tb`,CZM,,,,CEXP,
          or :ref:`tb`,CZM,,,,CLIN [default]). If zero or an invalid value is specified, the program uses
          :ref:`tb`,CZM,,,,CLIN as the default cohesive model type and sets reasonable CZM parameters based on
          the solid elements around the crack fronts/surfaces. For more information, see `Enhancing Crack
          Surfaces with Cohesive Zone Elements
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#eq26e3f167-5353-40f6-b6f1-8c455fe0bc00>`_

        * ``Par3`` - New crack-surface load value, or the name of a table for specifying tabular load values
          for crack- growth.

          The new crack-surface load is always assumed to be constant. If ``Par1`` = PRES, ``Par3`` specifies
          a constant pressure load.

          To specify a table ( :ref:`dim` ), enclose the table name within "%" characters (

          .. code:: apdl

             % tablename% ). Only one table can be specified for a crack-growth set, and time is the only
          primary variable supported.

          .. code:: apdl

             % tablename% ). Only one table can be specified for a crack-growth set, and time is the only
          primary variable supported.

        **Command Specification for Action= CPATH**

        .. _CGROW_CPATH:

        * ``Par1`` - Interface element component for crack path ( `VCCT
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#vcctsimassum>`_
          method only). (Component name must be 32 characters or less.)

        **Command Specification for Action= DTIME**

        .. _CGROW_DTIME:

        * ``Par1`` - Initial time step when crack-growth is detected.

        **Command Specification for Action= DTMIN**

        .. _CGROW_DTMIN:

        * ``Par1`` - Minimum time step allowed when crack-growth is detected.

        **Command Specification for Action= DTMAX**

        .. _CGROW_DTMAX:

        * ``Par1`` - Maximum time step allowed when crack-growth is detected.

        **Command Specification for Action= FCRAT**

        .. _CGROW_FCRAT:

        * ``Par1`` - `Fracture criterion ratio
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#vcctuserdeffractcrit>`_
          (f:sub:`c`, where f:sub:`c` is generally around 1). The recommended ratio is 0.95 to 1.05. The
          default is 1.00.

        **Command Specification for Action= STOP**

        .. _CGROW_STOP:

        * ``Par1`` - **CEMX** - Stops the analysis when the crack extension for any crack-front node reaches
        the maximum value
          (specified via ``Par2`` ).

          **FBOU** - Stops the analysis when the crack extension reaches the free boundary. Valid only for `SMART <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_ crack-growth analysis.

          **KMAX** - Stops the analysis when the maximum equivalent stress-intensity factor exceeds the specified limit
          ( ``Par2`` ). Valid only for SMART crack-growth analysis.

        * ``Par2`` - When ``Par1`` = CEMX, the value of maximum crack extension allowed.

          When ``Par1`` = KMAX, the value of the maximum equivalent stress-intensity factor allowed.

        **Command Specification for Action= METHOD**

        .. _CGROW_METHOD:

        * ``Par1, Par2`` - **VCCT** - Use `VCCT
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#vcctsimassum>`_
        to grow the crack (default).

          **XFEM** - Use `XFEM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_ to grow the crack.

          **SMART** - Use `SMART <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_ to grow the crack.

        * ``Par2`` - REME - Remeshing-based `SMART
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
          crack-growth method (the default and only option). Valid only when ``Par1`` = SMART.

        **Command Specification for Action= FCG**

        .. _CGROW_FCG:

        * ``Par1`` - **METH** - Fatigue crack-growth method.

          **DAMX** - Maximum crack-growth increment.

          **DAMN** - Minimum crack-growth increment.

          **SRAT** - `Stress ratio <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eq4f61610d-5010-4a2d-83de-3c60fba4be9f>`_.

          **DKTH** - Threshold value of equivalent stress-intensity-factor range (SIFS).

          **DN** - Incremental number of cycles.

        * ``Par2`` - ``Method`` - `LC or CBC method
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eq0a4098c5-8c81-4f2f-b279-a2fb84dff9ad>`_
          CBCmethod. Valid only when ``Par1`` = METH.

          ``VALUE`` - Value for the specified ``Par1``. Valid only when ``Par1`` = DAMX, DAMN, SRAT, DKTH, or DN.

          * For ``Par1`` = SRAT or DKTH, ``Par2`` can be a constant or table. To specify a table ( :ref:`dim`
            ), enclose the table name within "%" characters (``tablename``). Only one table can be
            specified for a crack-growth set, and time is the only primary variable supported.

        * ``Par3`` - Valid only for `SMART
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
          crack-growth analysis when ``Par1`` = DKTH.

          MIN or MAX or AVER or blank (default) - The minimum, maximum, or average stress-intensity-factor
          range (ΔK), respectively. The program calculates the range over the entire crack front, then uses
          the result to evaluate the threshold criterion. The entire crack is arrested if the specified
          minimum, maximum, or average ΔK is below the threshold ( ``Par2`` ). Partial crack-growth does not
          occur.

          If ``Par3`` is unspecified (default), the program evaluates threshold criterion at each crack-front
          node individually and ensures that the crack is arrested locally at any node where ΔK is below the
          threshold ( ``Par2`` ). If some nodes have ΔK less than the threshold and others have ΔK greater
          than the threshold, partial crack-growth occurs at the crack front.

            **Example: Using

            .. code:: apdl

               CGROW,FCG,DKTH, Par2, Par3

            **

            If ``Par3`` = MIN, the program selects the minimum ΔK from the ΔK values calculated at all crack-
            front nodes for the corresponding crack ID. If the minimum ΔK does not exceed the threshold (
            ``Par2`` ), there is no crack extension at the entire crack front.

        **Command Specification for Action= SOPT**

        .. _CGROW_SOPT:

        * ``Par1`` - SCN - Use a single number of cycles for all cracks in a multicrack analysis (even if
          each crack has separate loading) (default).

          MCN - Allow a separate cycle count for each crack in a multicrack analysis (available only if each
          crack has separate loading).

        **Command Specification for Action= RMCONT**

        .. _CGROW_RMCONT:

        Valid in a `SMART
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
        crack-growth analysis only.

        * ``Par1`` - COARSE - Controls `mesh-coarsening
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#>`_.

          ESIZE - Controls element sizing and crack-increment size.

          CMULT - Controls the crack-growth increment multiplier.

        * ``Par2`` - For ``Par1`` = COARSE:

          * CONS - Remeshing occurs with conservative mesh-coarsening (default).
          * MODE - Remeshing occurs with moderate mesh-coarsening.
          * AGGR - Remeshing occurs with aggressive mesh-coarsening.

          For ``Par1`` = ESIZE:

          * Crack-front reference element-size value, or the table name for specifying tabular element size
            values as a function of solution time.

          For ``Par1`` = CMULT:

          * Crack-front `element-size multiplier function
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#eq7e7daaf3-47a8-4bfe-8dd8-5cc5e3628ff0>`_
            :
          * TIME - Controls the crack-growth increment multiplier via the beginning and end of the solution
            time.
          * CEMX - Controls the crack-growth increment multiplier via the beginning and end of the accumulated
            maximum crack extension.
          * RMNU - Controls the crack-growth increment multiplier via the beginning and end of the number of
            remeshing steps.
          * TABLE - The name of the table for controlling the crack-growth increment multiplier.

        * ``Par3 - Par5`` - For ``Par1`` = ESIZE and ``Par2`` = ``VALUE`` or ``tablename`` and ``Par3`` =
        COMP:

          * ``Par4`` = Name of the node or element component (≤ 32 characters).

          For ``Par1`` = ESIZE and ``Par2`` = ``VALUE`` or ``tablename`` and ``Par3`` = NODE:

          * ``Par4`` = Node ID.

          For ``Par1`` = ESIZE and ``Par2`` = ``VALUE`` or ``tablename`` and ``Par3`` = ELEM:

          * ``Par4`` = Element ID.

          For ``Par1`` = CMULT and ``Par2`` = TIME:

          * ``Par3`` = ``VALUE`` - Maximum value of the crack-growth multiplier value.
          * ``Par4`` = ``VALUE`` - Time at the beginning of the crack-increment control function.
          * ``Par5`` = ``VALUE`` - Time at the end of the crack-increment control function.

          For ``Par1`` = CMULT and ``Par2`` = CEMX:

          * ``Par3`` = ``VALUE`` - Maximum value of the crack-growth multiplier value.
          * ``Par4`` = ``VALUE`` - Accumulated maximum crack extension at the beginning of the crack-increment
            control function.
          * ``Par5`` = ``VALUE`` - Accumulated maximum crack extension at the end of the crack-increment
            control function.

          For ``Par1`` = CMULT and ``Par2`` = RMNU:

          * ``Par3`` = ``VALUE`` - Maximum value of the crack-growth multiplier value.
          * ``Par4`` = ``VALUE`` - Remeshing number at the beginning of the crack-increment control function.
          * ``Par5`` = ``VALUE`` - Remeshing number at the end of the crack-increment control function.

          For ``Par1`` = CMULT and ``Par2`` = TABLE:

          * ``Par3`` = ``tablename`` - Controls the crack-growth increment multiplier via the tabular data
            in the specified table.
          * To specify a table ( :ref:`dim` ), enclose the table name ``tablename`` within % characters. You
            can specify one table per crack-growth set, and time is the only valid variable.

        **Command Specification for Action= NPLOAD**

        .. _CGROW_NPLOAD:

        Valid in a `SMART
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
        fatigue crack-growth analysis using `nonproportional loading
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#>`_.

        * ``Par1`` - METHOD - Specifies the nonproportional `solution method
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#notenostressratio>`_.

          DIRECTION - Specifies the nonproportional `crack-growth-direction method
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#eq16b7dac1-430d-4d50-9eaa-763f6660ab4e>`_.

        * ``Par2`` - For ``Par1`` = METHOD:

          * DKEF - Specifies the effective stress-intensity-factor range method.
          * DKMO - Specifies the stress-intensity-factor range method based on mode separation.
          * TKEF - Specifies the total effective stress-intensity-factor method.
          * TKMO - Specifies the total stress-intensity-factor method based on mode separation.

          For ``Par1`` = DIRECTION:

          * KMAX - Specifies the maximum-load method for the crack-growth direction.
          * KMIN - Specifies the minimum-load method for the crack-growth direction.
          * KLOC - Specifies the local kink-tip stress-intensity-factor method.

        * ``Par3`` - For ``Par2`` = KLOC:

          * ``w`` - Parameter-fitting value between 0 and 1. Default = 0.5.

        Notes
        -----

        .. _CGROW_notes:

        When ``Action`` = NEW, the :ref:`cgrow` command initializes a crack-growth simulation set.
        Subsequent :ref:`cgrow` commands define the parameters necessary for the simulation.

        For multiple cracks, issue multiple :ref:`cgrow`,NEW commands (and any subsequent :ref:`cgrow`
        commands necessary to define the parameters) for each crack.

        If the analysis is restarted ( :ref:`antype`,,RESTART), the :ref:`cgrow` command must be re-issued.

        If the :ref:`save` command is issued after any :ref:`cgrow` commands are issued, the :ref:`cgrow`
        commands are not saved to the database. Reissue the :ref:`cgrow` command(s) when the database is
        resumed.

        **For** `SMART
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
        -based crack-growth:

        * ``Action`` = CPATH has no effect.

        * ``Action`` = STOP affects both SMART-based `static
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#frackbasedsifs>`_
          and `fatigue
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#fracfcgreferences>`_
          crack-growth analyses.

        * When ``Action`` = CSFL with ``Option`` = CZM, the remeshing for cracks associated with this option
          is enforced at the end of the first load step and the first substep whether or not the crack grows
          at this moment. On original crack surfaces (defined via :ref:`cint`,SURF), ``INTER204`` elements
          are initialized fully damaged, as they are used for crack-closure only and do not contribute
          bonding tractions on crack surfaces. The cohesive tractions on the new open crack surface are
          defined via the cohesive zone material model type ( :ref:`tb`,CZM) and :ref:`cgrow`,CSFL,CZM. This
          option can be combined with :ref:`adpci` to initialize a crack with cohesive effect.

        **For** `VCCT
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#vcctsimassum>`_
        -based crack-growth:

        * Crack-growth element components must use the crack tip nodes as the starting nodes of the crack
          path.

        * Fracture criteria ( ``Action`` = FCOPTION) use energy-release rates calculated via VCCT technology
          ( :ref:`cint`,TYPE,VCCT). For information about the fracture criteria available, see `Fracture
          Criteria
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#vcctuserdeffractcrit>`_
          :ref:`tb`, `CGCR -- Crack-Growth Fracture Criterion
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_TB.html#eq4d382484-99d1-41ac-82dc-5a82d9911274>`_
          CGCR.

        **For** `XFEM
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_
        -based crack-growth:

        * The crack specification originates via the :ref:`xfenrich`, :ref:`xfdata`, or :ref:`xfcrkmesh`
          command.

        * ``Action`` = CPATH, DTMIN, or DTMAX has no effect.

        * ``Action`` = STOP affects `fatigue
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracfcgxfem.html#fracfcgxfemexample>`_
          crack-growth analysis only.
        """
        command = f"CGROW,{action},{par1},{par2},{par3}"
        return self.run(command, **kwargs)

    def inistate(
        self,
        action: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        val9: str = "",
        **kwargs,
    ):
        r"""Defines initial-state data and parameters.

        Mechanical APDL Command: `INISTATE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_INISTATE.html>`_

        Parameters
        ----------
        action : str
            Specifies action for defining or manipulating `initial-state
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_INSTWRITVAL.html>`_ data:

            * ``SET`` - Use ``Action`` = SET to designate initial-state coordinate system, data type, and
              material type parameters. See :ref:`inistate_set`.

            * ``DEFINE`` - Use ``Action`` = DEFINE to specify the actual state values, and the corresponding
              element, integration point, or layer information. See :ref:`inistate_define`.

              Use ``Action`` = DEFINE for `function-based
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_INSTAPPL.html#>`_ initial
              state. See :ref:`inistate_deffuncbased`.

            * ``WRITE`` - Use ``Action`` = WRITE to write the initial-state values to a file when the
              :ref:`solve` command is issued. See :ref:`inistate_write`.

            * ``READ`` - Use ``Action`` = READ to read the initial-state values from a file. See
              :ref:`inistate_read`.

            * ``LIST`` - Use ``Action`` = LIST to read out the initial-state data. See :ref:`inistate_list`.

            * ``DELETE`` - Use ``Action`` = DELE to delete initial-state data from a selected set of elements.
              See :ref:`inistate_delete`

        val1 : str
            Input values based on the ``Action`` type.

        val2 : str
            Input values based on the ``Action`` type.

        val3 : str
            Input values based on the ``Action`` type.

        val4 : str
            Input values based on the ``Action`` type.

        val5 : str
            Input values based on the ``Action`` type.

        val6 : str
            Input values based on the ``Action`` type.

        val7 : str
            Input values based on the ``Action`` type.

        val8 : str
            Input values based on the ``Action`` type.

        val9 : str
            Input values based on the ``Action`` type.

        Other Parameters
        ----------------
        **Command Specification for Action= SET**

        .. _inistate_set:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        ``Action`` = SET specifies and modifies the environment into which you will define the initial-state
        data (via a subsequent :ref:`inistate`,DEFINE command). Otherwise, subsequent
        :ref:`inistate`,DEFINE data is input as initial stress data in the global Cartesian coordinate
        system.

        **Command Specifications for Action= DEFINE**

        .. _inistate_define:

        * ``ELID`` - Element ID number when using element-based initial state. Defaults to current element
          selection.

          Node number when using node-based initial state. Defaults to current node selection.

        * ``EINT`` - Gauss integration point. Default = ALL or -1.

          For node-based initial state ( ``Val2`` = NODE), element ID number (if specified). The
          :ref:`inistate` command is applied only to the specified element (unlike the default behavior, where
          the command is applied to all selected elements containing the specified node).

          Not valid for material-based initial-state data ( ``Val1`` = MAT) or node-based initial state (
          ``Val2`` = NODE).

        * ``KLAYER`` - Layer number (for layered solid/shell elements) or cell number for beam/pipe
          elements. Blank for other supported element types and material-based initial-state data. Default =
          ALL or -1.

        * ``ParmInt`` - Section integration point within a layer, or cell-integration point for beams
          (typically four integration points). Default = ALL or -1. Not valid for material-based initial-state
          data ( ``Val1`` = MAT) or node-based initial state ( ``Val2`` = NODE).

          Not valid for material-based initial-state data ( ``Val1`` = MAT).

          Not used for node-based initial state with elements that do not have a beam/pipe/shell section
          defined.

          For node-based initial state with beams/pipes, values 1 through 4 can be used to specify the values
          at corner nodes within a cell.

          For node-based initial state with layered sections, values can be specified at TOP, BOT, and MID, or
          left blank (ALL or -1).

        * ``Cxx, Cyy, Czz, Cxy, Cyz, Cxz`` - Stress (S), strain (EPEL), or plastic strain (EPPL) values.

        You can issue the :ref:`inistate` command repeatedly to define multiple sets of initial-state
        values. initial-state data can be specified according to elements, layers or integration points.

        When the initial-state parameters are being defined based on the material, (
        :ref:`inistate`,SET,MAT, ``MATID`` ), ``ELID`` designates the element ID number and all subsequent
        values are ignored.

        For coupled-field elements, the stresses to input must be Biot``s effective stresses.

        **Command Specifications for Action= DEFINE (Function-Based Option)**

        .. _inistate_deffuncbased:

        * ``ELID`` - Element ID number when using element-based initial state. Defaults to current element
          selection.

          Node number when using node-based initial state. Defaults to current node selection.

        * ``EINT`` - Gauss integration point (defaults to ALL). Not valid for material-based initial-state
          data ( ``Val1`` = MAT) or node-based initial state ( ``Val2`` = NODE).

        * ``(Blank)`` - Reserved for future use.

        * ``(Blank)`` - Reserved for future use.

        * ``FuncName`` - LINX \| LINY \| LINZ. Apply initial-state data as a linear function of location based
          on the X axis (LINX), Y axis (LINY), or Z axis (LINZ) in the coordinate system specified via the
          :ref:`inistate`,SET,CSYS command. Default coordinate system: CSYS,0 (global Cartesian).

        * ``C1, C2,..., C12`` - For ``FuncName`` with tensors, each component uses two values. SXX = ``C1``
        + X\* ``C2``, SYY = ``C3`` + X\* ``C4``, and so on. Specify 12 values (for the six tensor
        components).

          For ``FuncName`` with scalars, only two values ``C1`` and ``C2`` ( ``VALUE`` = ``C1`` + X\* ``C2`` ) are necessary to apply the initial state.

        You can issue :ref:`inistate` repeatedly with the function-based option to define multiple sets of
        initial-state values. Initial-state data can be specified according to elements or integration
        points.

        For coupled-field elements, the stresses to input must be Biot's effective stresses.

        **Command Specifications for Action= WRITE**

        .. _inistate_write:

        * ``FLAG`` - Set this value to 1 to generate the initial-state file, or 0 to disable initial-state
          file generation.

        * ``CSID`` - Determines the `coordinate system
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_INSTCSYS.html#eq4c704b69-e237-458d-8c30-b7c4107fed8c>`_
          for the initial state:

          * ``0 (default)`` - Write in global Cartesian coordinate system for solid elements.

          * ``-1 (or MAT)`` - Write in material coordinate system

          * ``-2 (or ELEM)`` - Write in element coordinate system for link, beam, and layered elements.

          * ``Dtype`` - Sets the data type to be written in the :file:`.IST` file:

            * ``S`` - Output stresses.

            * ``EPEL`` - Output elastic strain.

            * ``EPPL`` - Output plastic strain.

            * ``PLEQ`` - Output equivalent plastic strain.

            * ``PLWK`` - Output plastic strain energy density.

            * ``EPCR`` - Output creep strain.

            * ``PPRE`` - Initial pore pressure.

            * ``VOID`` - Initial void ratio.

            * ``SVAR`` - State variables.

        Default is 0 for solid elements and -2 for link, beam, and shell elements.

        State variables are always written to the :file:`.ist` file in the material coordinate system.

        Only the three in-plane stresses for the top and bottom surfaces are written.

        For coupled-field elements, the stresses written out are Biot``s effective stress values.

        Initial pore pressure and void ratio are available for the coupled pore-pressure elements (CPT
        ``nnn`` ) only: ``CPT212``, ``CPT213``, ``CPT215``, ``CPT216``, and ``CPT217``.

        **Command Specifications for Action= READ**

        .. _inistate_read:

        Reads initial-state data from a standalone `initial-state (.ist) file
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_INSTFORMAT.html#meshindepIST>`_
        of the specified name ( ``Fname`` ) and filename extension ( ``Ext`` ), located in the specified
        path ( ``Path`` ). The initial-state file must be in a comma-delimited ASCII file format, consisting
        of individual rows for each stress/strain item, with each row consisting of columns separated by
        commas.

        Use ``Action`` = READ to apply complex sets of initial-state data to various elements, cells,
        layers, sections, and integration points. This option is available for element-integration-point-
        based initial-state data and node-based initial-state data.

        Mapping to nodes may offer better performance when many substeps are involved; however, only
        location support is available. Mapping to element-integration points supports additional field
        variables TIME, FREQ and TEMP and generally uses less memory.

        For other non-user-defined field variables (such as initial stress or strain), initial state is
        evaluated only at the first substep in the first load step.

        * ``MeshIndMethod`` - Mesh-Independent method :file:`.ist` read options:

          * 0 or DEFA -- `Standard
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_INSTFORMAT.html#sect2_zrk_jlr_dw>`_
            (mesh-dependent) initial state :file:`.ist` file (default).
          * MAPN -- Map to nodes internally when applying the initial state.
          * MAPI -- Map to element-integration points.
          * DOBJ -- Do not use :file:`.ist` data in the finite element solution. (Use this option if
            `converting initial-stress data to a traction load
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_CINT.html#>`_.)

        **Command Specifications for Action= LIST**

        .. _inistate_list:

        If using the `standard method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_INSTAPPL.html#initfuncbased>`_
        for applying initial-state data,specify ``ELID`` = element ID number to list initial-state data for
        elements. If ``ELID`` is unspecified, all initial-state data for all selected elements are listed.

        If using the mesh-independent method, specify ``ELID`` = MIND to list initial-state data.

        **Command Specifications for Action= DELETE**

        .. _inistate_delete:

        If using the `standard method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_INSTAPPL.html#initfuncbased>`_,
        specify ``ELID`` = element ID number to delete initial-state data for elements. If ``ELID`` is
        unspecified, all initial-state data for all selected elements are deleted.

        If using the mesh-independent method, specify ``ELID`` = MIND to delete initial-state data.

        Notes
        -----
        :ref:`inistate` is available for `current-technology elements
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/EL2oldnewtable.html#EL2curtechelembenefits>`_.

        The command can also be used with ``MESH200`` (via the `mesh-independent method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#strinistmesh200>`_
        for defining `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_ ) to
        apply an initial state to all generated reinforcing elements automatically. For more information,
        see `Applying an Initial State to Reinforcing Elements
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#strinistmesh200>`_

        Initial-state support for a given element is indicated in the documentation for the element under
        **Special Features**.

        Initial-strain input ( :ref:`inistate`,SET,DTYPE,EPEL) enables the nonlinear solver option
        automatically even if no nonlinear materials are involved.

        The command does not support kinematic hardening material properties (such as :ref:`tb`
        ,PLAS,,,,BKIN) or the shape memory alloy material model ( :ref:`tb`,SMA).

        :ref:`inistate` with elastic strain alone is not supported for gasket materials ( :ref:`tb`,GASK)
        and hyperelastic materials ( :ref:`tb` ,HYPER, :ref:`tb` ,BB, :ref:`tb`,AHYPER, :ref:`tb`,CDM,
        :ref:`tb`,EXPE).

        :ref:`inistate` with initial stress alone is not supported for gasket materials ( :ref:`tb`,GASK).

        :ref:`inistate` with plastic strain (which must include initial strain or stress, plastic strain,
        and accumulated plastic strain) does not support gasket materials ( :ref:`tb`,GASK), rate-dependent
        plasticity ( :ref:`tb`,RATE), and viscoelasticity ( :ref:`tb`,PRONY, :ref:`tb`,SHIFT).

        For more information about using the initial-state capability, see `Initial State
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_INSTWRITVAL.html>`_
        """
        command = f"INISTATE,{action},{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9}"
        return self.run(command, **kwargs)

    def tb(
        self,
        lab: str = "",
        matid: str = "",
        ntemp: str = "",
        npts: str = "",
        tbopt: str = "",
        funcname: str = "",
        **kwargs,
    ):
        r"""Activates a data table for material properties or special element input.

        Mechanical APDL Command: `TB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TB.html>`_

        Parameters
        ----------
        lab : str
            Material model data table type:

            * ``AFDM`` - :ref:`Acoustic frequency-dependent material. <TBafdm_spec>`

            * ``AHYPER`` - :ref:`Anisotropic hyperelasticity. <TBahyperspec>`

            * ``ANEL`` - :ref:`Anisotropic elasticity. <TBDTSpANELjwf070600>`

            * ``ANISO`` - :ref:`Generalized Hill anisotropy. <TBANISOspec>`

            * ``AVIS`` - :ref:`Anisotropic viscosity. <AVIS_spec>`

            * ``BB`` - :ref:`Bergstrom-Boyce. <TBBBspecs>`

            * ``BH`` - :ref:`Magnetic field. <TBDTSpBHjwf070600>`

            * ``CAST`` - :ref:`Cast iron. <tbcastspecjmb>`

            * ``CDM`` - :ref:`Damage. <TBCDMspecs>`

            * ``CFOAM`` - :ref:`Crushable foam. <TBCFOAMspecs>`

            * ``CGCR`` - `CGCR -- Crack-Growth Fracture Criterion
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_TB.html#eq4d382484-99d1-41ac-82dc-5a82d9911274>`_
              Crack-growth fracture criterion ( :ref:`cgrow` ).

            * ``CHABOCHE`` - :ref:`Chaboche nonlinear kinematic hardening using von Mises or Hill plasticity.
              <TBDTSpCHABjwf070600>`

            * ``CONCR`` - :ref:`Concrete element or material data. <TBDTSpCONCjwf070600>`

            * ``CREEP`` - :ref:`Creep. Pure creep, creep with isotropic hardening plasticity, or creep with
              kinematic hardening plasticity using both von Mises or Hill potentials. <TBDTSpCREEjwf070600>`

            * ``CRKI`` - - Material criterion for :ref:`adaptive-crack initiation ( <TBspecCRKI>` :ref:`adpci` )

            * ``CTE`` - :ref:`Coefficient of thermal expansion. <TBctespec>`

            * ``CZM`` - :ref:`Cohesive zone. <TBczmspec>`

            * ``DENS`` - :ref:`Mass Density. <TBdensspec>`

            * ``DLST`` - :ref:`Anisotropic dielectric loss tangent. <DLST_spec>`

            * ``DMGE`` - :ref:`Damage evolution law. <TBdmge>`

            * ``DMGI`` - :ref:`Damage initiation criteria. <TBdmgi>`

            * ``DPER`` - :ref:`Anisotropic electric permittivity. <tbdperspec>`

            * ``EDP`` - :ref:`Extended Drucker-Prager (for granular materials such as rock, concrete, soil,
              ceramics and other pressure-dependent materials). <TBedpspec>`

            * ``ELASTIC`` - :ref:`Elasticity. <tbelasticpec>`

            * ``ELST`` - :ref:`Anisotropic elastic loss tangent. <ELST_spec>`

            * ``EXPE`` - :ref:`Experimental data. <TBexperimental>`

            * ``FCON`` - :ref:`Fluid conductance data. <TBDTSpFCONjwf070600>`

            * ``FCLI`` - :ref:`Material strength limits for calculating failure criteria. <TBfclispecs>`

            * ``FLUID`` - :ref:`Fluid. <tbfluidspec>`

            * ``FRIC`` - :ref:`Coefficient of friction based on Coulomb's Law or user-defined friction.
              <tbfricspec>`

            * ``GASKET`` - :ref:`Gasket. <TBDTSgas111501>`

            * ``GURSON`` - :ref:`Gurson pressure-dependent plasticity for porous metals. <TBgurspec>`

            * ``HFLM`` - :ref:`Film coefficient data. <TBDTSpHFLMjwf070600>`

            * ``HILL`` - :ref:`Hill anisotropy. When combined with other material options, simulates plasticity,
              viscoplasticity, and creep -- all with the Hill potential. <TBDTSpHILLjwf070600>`

            * ``HYPER`` - :ref:`Hyperelasticity material models (Arruda-Boyce, Blatz-Ko, Extended Tube, Gent,
              Mooney-Rivlin [default], Neo-Hookean, Ogden, Ogden Foam, Polynomial Form, Response Function, Yeoh,
              and user- defined). <TBDTSpHYPEjwf070600>`

            * ``INTER`` - :ref:`Contact interaction. <tbinterspec>`

            * ``JOIN`` - :ref:`Joint (linear and nonlinear elastic stiffness, linear and nonlinear damping, and
              frictional behavior). <tbjoinspec>`

            * ``JROCK`` - :ref:`Jointed rock. <tbjointedrockspec>`

            * ``MC`` - :ref:`Mohr-Coulomb. <tbmohrcoulombspec>`

            * ``MELAS`` - :ref:`Multilinear elasticity. <tbmelasspec>`

            * ``MIGR`` - :ref:`Migration. <tbmigrspec>`

            * ``MPLANE`` - :ref:`Microplane. <TBmplanespec>`

            * ``NLISO`` - :ref:`Voce isotropic hardening law (or power law) for modeling nonlinear isotropic
              hardening using von Mises or Hill plasticity. <TBDTSpNLISjwf070600>`

            * ``PELAS`` - :ref:`Porous elasticity. <tbporelasspec>`

            * ``PERF`` - :ref:`Perforated material for acoustics; equivalent fluid model of perforated media,
              poroelastic material model, and transfer admittance matrix. <TBperf_model_spec>`

            * ``PIEZ`` - :ref:`Piezoelectric matrix. <TBDTSpPIEZjwf070600>`

            * ``PLASTIC`` - :ref:`Nonlinear plasticity. <tbplasticspec>`

            * ``PM`` - :ref:`Porous media. Coupled pore-fluid diffusion and structural model of porous media.
              <TBpmspec>`

            * ``PRONY`` - :ref:`Prony series constants for viscoelastic materials. <tbpronyspecjmb>`

            * ``PZRS`` - :ref:`Piezoresistivity. <tbpzrsspec>`

            * ``RATE`` - :ref:`Rate-dependent plasticity (viscoplasticity) when combined with the BISO, NLISO or
              PLASTIC material options, or rate-dependent anisotropic plasticity (anisotropic viscoplasticity)
              when combined with the HILL and BISO, NLISO or PLASTIC material options. <TBDTSpRATEjwf070600>`

              The exponential visco-hardening option includes an explicit function for directly defining static
              yield stresses of materials.

              The Anand unified plasticity option requires no combination with other material models.

            * ``SDAMP`` - :ref:`Material damping coefficients. <tbsdampspec>`

            * ``SHIFT`` - :ref:`Shift function for viscoelastic materials. <tbshiftspecjmb>`

            * ``SINT`` - :ref:`Sintering. Available with the Additive Suite license. <tbsintspec>`

            * ``SMA`` - :ref:`Shape memory alloy for simulating <TBDTSpSMA>` `superelasticity
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#>`_, `shape memory effect
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#>`_, or shape memory
              effect with `plasticity
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#matparmsmaplastic>`_.

            * ``SOIL`` - :ref:`Soil models. <tbsoilspec>`

            * ``STATE`` - :ref:`User-defined state variables. Valid with <TBDTSpSTATjwf070600>` :ref:`tb`,USER
              and used with either the `UserMat
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ or `UserMatTh
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ subroutine.
              Also valid with :ref:`tb`,CREEP (when ``TBOPT`` = 100) and used with the UserCreep subroutine.

            * ``SWELL`` - :ref:`Swelling strain function. <TBDTSpSWELjwf070600>`

            * ``TNM`` - :ref:`Three-network model for viscoplastic materials. <tbtnmspec>`

            * ``THERM`` - :ref:`Thermal properties. <tbthermspec>`

            * ``USER`` - :ref:`User-defined material or thermal material model (general-purpose except for
              incompressible material models) or thermal material model. <TBDTSpUSERjwf070600>`

            * ``WEAR`` - :ref:`Contact surface wear. <tbwearspec>`

            * ``XTAL`` - :ref:`Crystal plasticity for elasto-viscoplastic crystalline materials. <xtalspec>`

        matid : str
            Material reference identification number. Valid value is any number ``n``, where 0 < ``n`` <
            100,000. Default = 1.

        ntemp : str
            The number of temperatures for which data will be provided (if applicable). Specify temperatures
            via the :ref:`tbtemp` command.

        npts : str
            For most labels where ``NPTS`` is defined, the number of data points to be specified for a given
            temperature. Define data points via the :ref:`tbdata` or :ref:`tbpt` commands.

        tbopt : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TB.html>`_
            for further information.

        funcname : str
            The name of the function to be used (entered as ``tabname``, where ``tabname`` is the name of
            the table created by the Function Tool). Valid only when ``Lab`` = JOIN (joint element material)
            and nonlinear stiffness or damping are specified on the ``TBOPT`` field (see :ref:`tbjoinspec`
            ). The function must be predefined via the Function Tool. To learn more about how to create a
            function, see `Using the Function Tool
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BASFUNCGRAPH.html>`_

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TB.html>`_
           for further explanations.

        **Data Table Specifications**

        .. _TB_datatabspec:

        Following are input requirements ( ``NTEMP``, ``NPTS``, and ``TBOPT`` values) and links to detailed
        documentation for each data table type ( :ref:`tb`, ``Lab`` value):

        .. _TBafdm_spec:

        * ``NTEMP:`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT:`` - Acoustic material options:

          * ``MAT`` - Material properties

          * ``THIN`` - Thin layer

          * ``RECT`` - Rectangular cross-section

          * ``CIRC`` - Circular cross-section

          * ``ROOM`` - Diffusion properties for room acoustics

        * ``References:`` - `Defining Acoustic Material Properties
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_acous/acous_mat_room.html>`_

          See :ref:`tbfield` for more information about defining temperature- and/or frequency-dependent
          properties.

        .. _TBahyperspec:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. Maximum = 40.

        * ``NPTS :`` - Number of data points to be specified for a given temperature.

        * ``TBOPT :`` - Anisotropic hyperelastic material options.

          * ``POLY`` - Polynomial strain energy potential.

          * ``EXPO`` - Exponential strain energy potential.

          * ``AVEC`` - Define the A vector.

          * ``BVEC`` - Define the B vector.

          * ``PVOL`` - Volumetric potential.

          * ``USER`` - `User-defined
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ potential
            invariant set type.

          * ``UNUM`` - `User-defined
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ invariant set
            number.

          * ``AU01`` - `User-defined
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ material
            parameters.

          * ``FB01`` - `User-defined
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ fiber
            directions.

        * ``References:`` - `Anisotropic Hyperelasticity ( TB,AHYPER)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eq1bb00e38-67c5-4f00-8adb-96bebf98d1f9>`_

          `Anisotropic Hyperelasticity Model
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR8_3.html#>`_

          `Subroutine UserHyperAniso (Writing Your Own Anisotropic Hyperelasticity Laws)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_

          `Anisotropic Hyperelasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_mat5.html#eqbb7fd6a6-e661-44f4-be06-afb4a29e1bf9>`_

        .. _TBDTSpANELjwf070600:

        This material model is not supported for use with the :ref:`coefficient of thermal expansion (
        <TBctespec>` :ref:`tb`,CTE). The maximum number of ANEL tables is 1,000,000.

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 6. Maximum = 6.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - Anisotropic elastic matrix options.

          * ``0`` - Elasticity matrix used as supplied (input in stiffness form).

          * ``1`` - Elasticity matrix inverted before use (input in flexibility form).

        * ``References:`` - `Anisotropic Elasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/anel.html#eq2863f1de-4565-4ce0-a650-8c6d689c13cc>`_

        .. _TBANISOspec:

        * ``NTEMP:`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT:`` - Not used.

        * ``References:`` - `Generalized Hill Anisotropy
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_

        .. _AVIS_spec:

        * ``NTEMP:`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT:`` - Anisotropic viscosity matrix options:

          * ``0`` - Viscosity matrix (used as specified).

          * ``1`` - Fluency matrix (converted to viscosity matrix before use).

        * ``References:`` - `Anisotropic Viscosity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_electricmagnet.html#>`_

        .. _TBBBspecs:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. The maximum
          must be a value such that ( ``NTEMP`` x ``NPTS`` ) <= 1000.

        * ``NPTS :`` - Number of material constants.

        * ``TBOPT :`` - Isochoric or volumetric strain-energy function:

          * ``ISO`` - Define material constants for isochoric strain energy.

          * ``PVOL`` - Define material constants for volumetric strain energy.

        * ``References:`` - `Bergstrom-Boyce
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_bb.html#eqa1cf87c1-283a-4b62-856b-b656928b3269>`_

          `Bergstrom-Boyce Material ( TB,BB)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eq562bbfb4-459d-41bf-89a7-6f815d15f1ca>`_

          `Bergstrom-Boyce Hyperviscoelasticity Model
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR8_3.html#>`_

        .. _TBDTSpBHjwf070600:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Number of data points to be specified. Default = 20. Maximum = 500.

        * ``TBOPT :`` - BH curve options.

          * ``BH or (blank)`` - BH curve data (default).

          * ``TCF`` - Thermal coefficient data for BH curve modification. This option is valid for the
            following elements: ``PLANE223``, ``SOLID226``, ``SOLID227``, ``PLANE233``, ``SOLID236``, and
            ``SOLID237``.

        * ``References:`` -

          `Additional Guidelines for Defining Regional Material Properties and Real Constants
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_lof/Hlp_G_ELE2_3.html#a3nSIn2b4ctg>`_

        .. _tbcastspecjmb:

        * ``NTEMP:`` - Number of temperatures for which data will be provided. Default = 1. Maximum = 10.

        * ``NPTS:`` - Not used.

        * ``TBOPT:`` - Cast iron options:

          * ``ISOTROPIC`` - Specifies cast iron plasticity with isotropic hardening.

          * ``TENSION`` - Defines stress-strain relation in tension.

          * ``COMPRESSION`` - Defines stress-strain relation in compression.

          * ``ROUNDING`` - Defines tension yield surface rounding factor.

        * ``References:`` - `Cast Iron
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_

        .. _TBCDMspecs:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. The maximum
          must be a value such that ( ``NTEMP`` x ``NPTS`` ) <= 1000.

        * ``NPTS :`` - Number of data points to be specified for a given temperature.

        * ``TBOPT :`` - Damage option:

          * ``PSE2`` - Mullins effect for hyperelasticity models: Pseudo-elastic model with a modified Ogden-
            Roxburgh damage function. Requires ``NPTS`` = 3.

          * ``MUSER`` - Mullins effect for hyperelasticity models: Pseudo-elastic model with a user-defined
            damage function.

          * ``GDMG`` - Generalized damage model parameters.

          * ``FIB1`` - Damage parameters in fiber direction 1.

          * ``FIB2`` - Damage parameters in fiber direction 2.

          * ``FIB3`` - Damage parameters in fiber direction 3.

        * ``References:`` - `Mullins Effect
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_mullinseffect.html#thymullinspseudoelas>`_

          `Mullins Effect ( TB,CDM)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eq131b2f6e-5292-4143-80f8-e779d52f1a70>`_

          `Mullins Effect Model
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR8_3.html#>`_

          `Regularized Anisotropic Damage
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_damageall.html#>`_

        .. _TBCFOAMspecs:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - Crushable foam material option:

          * `YIELD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#>`_ -
            Initial yield stress values.

          * `HTYPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#>`_ -
            Hardening evolution type.

          * `MHARD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#>`_ -
            Multilinear hardening evolution points.

          * `PPR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#>`_ -
            Plastic Poisson``s ratio.

        * ``References:`` - `Crushable Foam
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_

        .. _tbcgcrspec:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS :`` - Number of data points to be specified for a given temperature.

        * ``TBOPT :`` - Fracture-criterion option.

          * `LINEAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#>`_
            -- Linear fracture criterion. Valid when ``NPTS`` = 3.
          * `BILINEAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#>`_
            -- Bilinear fracture criterion. Valid when ``NPTS`` = 4.
          * `BK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#>`_ --
            B-K fracture criterion. Valid when ``NPTS`` = 3.
          * `MBK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#>`_ --
            Modified B-K (Reeder) fracture criterion. Valid when ``NPTS`` = 4.
          * `POWERLAW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#>`_
            -- Wu's Power Law fracture criterion. Valid when ``NPTS`` = 6.
          * `USER
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#eq4724c95a-555f-4385-930f-aefcca09897e>`_
            -- User-defined fracture criterion. Valid when ``NPTS`` = 20.
          * `PSMAX
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#eq4724c95a-555f-4385-930f-aefcca09897e>`_
            -- Circumferential stress criterion based on :math:`equation not available`  when sweeping around
            the crack tip at a given radius. Valid when                     ``NPTS`` = 1. Used in an `XFEM
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracfcgxfem.html#fracfcgxfemexample>`_
            -based crack-growth analysis only.
          * `STTMAX
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_STR_VCCT.html#eq4724c95a-555f-4385-930f-aefcca09897e>`_
            -- Maximum circumferential stress criterion. Valid when ``NPTS`` = 1. Used in an `XFEM
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracfcgxfem.html#fracfcgxfemexample>`_
            -based crack-growth analysis only.
          * `RLIN
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemdecaytab.fn1>`_
            -- Rigid linear evolution law for the decay of stress. Valid when ``NPTS`` = 4. Used in an `XFEM
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracfcgxfem.html#fracfcgxfemexample>`_
            -based crack-growth analysis only.
          * `PARIS
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eq4f61610d-5010-4a2d-83de-3c60fba4be9f>`_
            -- Paris' Law for fatigue crack-growth. Valid when ``NPTS`` = 2. Used in a `SMART
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
            - or  `XFEM
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracfcgxfem.html#fracfcgxfemexample>`_
            -based fatigue crack-growth analysis only.
          * `WALK
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eq4ea244c5-0b72-49dc-a7bf-43149889a1cd>`_
            -- Walker equation for fatigue crack-growth. Valid when ``NPTS`` = 3. Used in a `SMART
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
            -based fatigue crack-growth analysis only.
          * `FORM
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eqd9c4405c-14bc-49a6-9c72-1bbe23d41643>`_
            -- Forman equation for fatigue crack-growth. Valid when ``NPTS`` = 3. Used in a `SMART
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
            -based fatigue crack-growth analysis only.
          * `TFDK
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eq5a0147ef-6ed3-4a7a-9998-213217e78bdf>`_
            -- Tabular fatigue law for fatigue crack-growth. Used in a `SMART
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
            -based fatigue crack-growth analysis only.
          * `NG03 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#>`_
            -- `NASGRO
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#nasgro4>`_
            equation v. 3 for fatigue crack-growth. Valid when ``NPTS`` = 9. Used in a `SMART
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
            -based fatigue crack-growth analysis only.
          * `NG04 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#>`_
            -- `NASGRO
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#nasgro4>`_
            equation v. 4 for fatigue crack-growth. Valid when ``NPTS`` = 10. Used in a `SMART
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
            -based fatigue crack-growth analysis only.
          * KIC -- `Critical stress-intensity factor
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eqa7ac21d8-c5cc-41bd-
            aced-f664166c2ea0>`_ for static crack-growth. Valid when ``NPTS`` = 1. Valid in a `SMART
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
            -based static crack-growth analysis only.
          * JIC -- `Critical J-integral
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eqb5e4514c-a107-4016-847f-af649a691f2f>`_
            for static crack-growth. Valid when ``NPTS`` = 1. Valid in a `SMART
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
            -based static crack-growth analysis only.

          Fatigue `crack-closure <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#polynomclosure>`_ option. Valid in a `SMART <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_ -based fatigue crack-growth analysis only, with crack-growth based on `Paris`` law <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eq4f61610d-5010-4a2d-83de-3c60fba4be9f>`_ or `tabular fatigue <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eq5a0147ef-6ed3-4a7a-9998-213217e78bdf>`_ law.

          * `ELBER
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eqe9cf92f4-6e7c-48c1-b951-5ef12345157a>`_
            - Elber closure function.
          * `SCHIJVE
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eqe1ec4405-f082-413b-822b-aaedef99bac5>`_
            - Schijve closure function.
          * `NEWMAN
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eq3ed68a02-4fc8-46ce-
            aa3e-7fe3f5923ef5>`_ - Newman closure function.
          * `UPOLY
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/franundcgrowmech.html#eqa6f0d4fd-
            ce08-4336-b1cf-b632d01a62c1>`_ - Polynomial closure function.

        * ``References:`` - `Fracture Analysis Guide
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACBENCH.html>`_

          :ref:`cgrow` command

        .. _TBDTSpCHABjwf070600:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. The maximum
          value of ``NTEMP`` is such that ``NTEMP`` x (1 + 2 ``NPTS`` ) = 1000.

        * ``NPTS :`` - Number of kinematic models to be superposed. Default = 1. Maximum = 5.

        * ``TBOPT :`` - * ``(blank)`` - Default option for nonlinear kinematic hardening.

          * ``TRATE`` - Include temperature-rate term in back-stress evolution.

          * ``SHDR`` - Strain-hardening of dynamic recovery properties. To use this option, ``TBOPT`` = TRATE
            is also required.

        * ``References:`` - `Nonlinear Kinematic Hardening
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_

        .. _TBDTSpCONCjwf070600:

        * ``NTEMP :`` - Number of temperatures for which data will be provided (used only if ``TBOPT`` = 0
          or 1). Default = 6. Maximum = 6.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - Concrete material options.

          * ``DP`` - `Drucker-Prager
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#matgeomechdefDPconcmod>`_
            concrete strength parameters.

          * ``RCUT`` - Rankine tension failure parameter.

          * ``DILA`` - Drucker-Prager concrete dilatation.

          * ``HSD2`` - Drucker-Prager concrete `exponential
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#eq02d041b8-8522-4917-93c4-d757c809944b>`_
            `hardening/softening/dilitation (HSD)
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#matDPconcrlinearsoft>`_
            behavior.

          * ``HSD4`` - Drucker-Prager concrete `steel reinforcement
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#eq579f37fd-675c-48f0-941d-890069f7ee1d>`_
            HSD behavior.

          * ``HSD5`` - Drucker-Prager concrete `fracture energy
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#eqdae60069-4439-4532-9997-8223567cabd8>`_
            HSD behavior.

          * ``HSD6`` - Drucker-Prager concrete `linear
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#eq1f9198fc-0858-4d52-b551-f12bfd5b2024>`_
            HSD behavior.

          * ``FPLANE`` - Drucker-Prager concrete joint parameters.

          * ``FTCUT`` - Drucker-Prager concrete joint tension cutoff.

          * ``FORIE`` - Drucker-Prager concrete joint orientation.

          * ``MW`` - Menetrey-Willam constitutive model.

          * ``MSOL`` - `Material solution option
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#>`_.

        * ``References:`` - `Drucker-Prager Concrete
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#matgeomechdefDPconcmod>`_

          `Hardening, Softening and Dilatation (HSD) Behavior
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#matDPconcrlinearsoft>`_

          `Menetrey-Willam
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#>`_

        .. _TBDTSpCREEjwf070600:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS :`` - Number of data points to be specified for a given temperature.

        * ``TBOPT :`` - Creep model options.

          * ``1 through 13`` - Implicit creep option. See for a list of available equations.

          * ``100`` - USER CREEP option. Define the creep law using the :file:`USERCREEP.F` subroutine. See
            the `Guide to User-Programmable Features
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/ansysprog_aero_fullycoupled.html>`_

        * ``References:`` - `Creep
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/rate.html#crei>`_

          `Creep Model
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR8_3.html#strimpcrplcd032400>`_

          See also `Combining Material Models
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/strmamoco050401.html>`_

        .. _TBspecCRKI:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 6. Maximum = 6.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - Adaptive crack-initiation options:

          * ``PSMAX`` - Maximum principal stress (default).

        * ``References:`` - `SMART Method for Crack-Initiation Simulation
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fractSMARTinit.html#SMARTcrackinitexamp>`_

        .. _TBctespec:

        * ``NTEMP:`` - No limit.

        * ``NPTS:`` - Not used.

        * ``TBOPT:`` - * ``(blank)`` - Enter the secant coefficients of thermal expansion (CTEX,CTEY,CTEZ)
        (default).

          * ``USER`` - User-defined thermal strain.

          * ``FLUID`` - `Fluid thermal-expansion coefficient
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/elemdatatblpor.html#heattranseq>`_
            for porous media.

          * ``UFSTRAIN`` - `User-defined free strain
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/elemdatatblpor.html#eq367d867d-cabc-4697-89e0-446fa8b7527d>`_
            in porous media.

        * ``References:`` - `Thermal Expansion
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/ansmattherexp.html#eqd3e72ea4-fb9e-483e-94a3-eaa6081710de>`_

          `Porous Media Mechanics
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/elemdatatblpor.html#heattranseq>`_

          `Free-Strain Rate
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/elemdatatblpor.html#eq367d867d-cabc-4697-89e0-446fa8b7527d>`_

          See also :ref:`tbfield` (for defining frequency-dependent, temperature-dependent, and `user-defined
          field-variable-based
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_fielduserdef.html#>`_
          properties).

        .. _TBczmspec:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS :`` - Number of data points to be specified for a given temperature.

        * ``TBOPT :`` - Cohesive zone material options.

          * ``EXPO`` - Exponential material behavior. Valid for interface elements and contact elements.

          * ``BILI`` - `Bilinear material behavior
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/cozonemats.html#eq882acced-35ea-449a-9f59-1a8f1175f44c>`_.
            Valid for interface elements, contact elements, and in an `XFEM-based crack-growth
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_
            analysis when cohesive behavior on the initial crack is desired.

          * ``CBDD`` - Bilinear material behavior with linear softening characterized by maximum traction and
            maximum separation. Valid for contact elements only.

          * ``CBDE`` - Bilinear material behavior with linear softening characterized by maximum traction and
            critical energy release rate. Valid for contact elements only.

          * ``CEXP`` - Exponential material behavior for preventing surface penetration on the cohesive
            interface. Valid for `SMART
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
            -based crack-growth only.

          * ``CLIN`` - Linear material behavior with a penalty slope for preventing surface penetration on the
            cohesive interface. Valid for `SMART
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#fracsmartexample>`_
            -based crack-growth only.

          * ``VREG`` - Viscous regularization. Valid for interface elements and contact elements. Also valid
            in an XFEM- based crack-growth analysis when cohesive behavior is specified for the initial crack.

          * ``USER`` - User-defined option. Valid for interface elements only.

        * ``References:`` - `Cohesive Zone Material (CZM) Model
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_mat11.html#>`_

          `Cohesive Material Law
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/cozonemats.html#cozonepost>`_

          `Subroutine userCZM (Creating Your Own Cohesive Zone Material)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#matstatevaruserdefczm>`_

          `Crack-Initiation and -Growth Simulation, Interface Delamination, and Fatigue Crack-Growth
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracfcgxfem.html>`_

          `XFEM-Based Crack Analysis and Crack-Growth Simulation
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/Hlp_G_FRACXFEM.html#fracxfemreferences>`_

          `Enhancing Crack Surfaces with Cohesive Zone Elements
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_frac/fracSMART.html#eq26e3f167-5353-40f6-b6f1-8c455fe0bc00>`_

        .. _TBdensspec:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - 1

        * ``TBOPT :`` - Not used.

        * ``References:`` - See :ref:`tbfield` and `User-Defined Field Variables
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_fielduserdef.html#>`_

        .. _DLST_spec:

        * ``NTEMP:`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT:`` - Not used.

        * ``References:`` - `Anisotropic Dielectric Loss Tangent
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_electricmagnet.html#eq2d35a8da-
          dc5d-4cd9-9141-6540016c1258>`_

        .. _TBdmge:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS :`` - Number of data points to be specified for a given temperature. Default = 4 when
          ``TBOPT`` = MPDG

        * ``TBOPT :`` - Damage initiation definition:

          * ``1, or MPDG`` - Progressive damage evolution based on simple instant material stiffness
            reduction.

          * ``2, or CDM`` - Progressive damage evolution based on continuum damage mechanics.

        * ``Reference:`` - `Damage Evolution Law
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_damageall.html#matprogdammodel>`_

        .. _TBdmgi:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS :`` - Number of data points to be specified for a given temperature. Default = 4 when
          ``TBOPT`` = FCRT.

        * ``TBOPT :`` - Damage initiation definition:

          * ``1 or FCRT`` - Define failure criteria as the damage initiation criteria.

        * ``Reference:`` - `Damage Initiation Criteria
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_damageall.html#mat_dmge>`_

        .. _tbdperspec:

        * ``NTEMP:`` - Not used.

        * ``NPTS:`` - Not used.

        * ``TBOPT:`` - Permittivity matrix options for ``PLANE222``, ``PLANE223``, ``SOLID225``,
        ``SOLID226``, and
          ``SOLID227``  :

          * ``0`` - Permittivity matrix at constant strain [ε :sup:`S` ] (used as supplied)

          * ``1`` - Permittivity matrix at constant stress [ε :sup:`T` ] (converted to [ε :sup:`S` ] form
            before use)

        * ``References:`` - `Anisotropic Electric Permittivity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_electricmagnet.html#eq3ef40343-18c4-490c-b76d-2ba7f66361a2>`_

        .. _TBedpspec:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. Maximum = 40.

        * ``NPTS :`` - Number of data points to be specified for a given temperature.

        * ``TBOPT :`` - EDP material options.

          * ``LYFUN`` - Linear yield function.

          * ``PYFUN`` - Power law yield function.

          * ``HYFUN`` - Hyperbolic yield function.

          * ``LFPOT`` - Linear flow potential function.

          * ``PFPOT`` - Power law flow potential function.

          * ``HFPOT`` - Hyperbolic flow potential function.

          * ``CYFUN`` - Cap yield function.

          * ``CFPOT`` - Cap flow potential function.

        * ``References:`` - `Extended Drucker-Prager (EDP)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_

          `Extended Drucker-Prager Cap
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_

        .. _tbelasticpec:

        * ``NTEMP:`` - Number of temperatures for which data will be provided.

        * ``NPTS:`` - Number of properties to be defined for the material option. This value is set
          automatically according to the elasticity option ( ``TBOPT`` ) selected. If ``TBOPT`` is not
          specified, default settings become ``NPTS`` = 2 and ``TBOPT`` = ISOT.

        * ``TBOPT:`` - Elasticity options:

          * ``ISOT`` - Isotropic property (EX, NUXY) (default). Setting ``NPTS`` = 2 also selects this option
            automatically.

          * ``OELN`` - Orthotropic option with minor Poisson's ratio (EX, EY, EZ, GXY, GYZ, GXZ, NUXY, NUYZ,
            NUXZ). ``NPTS`` = 9. Setting ``NPTS`` = 9 selects this option automatically. All nine parameters
            must be set, even for the 2D case.

          * ``OELM`` - Orthotropic option with major Poisson's ratio (EX, EY, EZ, GXY, GYZ, GXZ, PRXY, PRYZ,
            PRXZ). ``NPTS`` = 9. All nine parameters must be set, even for the 2D case.

          * ``AELS`` - Anisotropic option in stiffness form (D11, D21, D31, D41, D51, D61, D22, D32, D42, D52,
            D62, D33, D43,..... D66). ``NPTS`` = 21. Setting ``NPTS`` = 21 selects this option automatically.

          * ``AELF`` - Anisotropic option in compliance form (C11, C21, C31, C41, C51, C61, C22, C32, C42,
            C52, C62, C33, C43,..... C66). ``NPTS`` = 21.

          * ``FIB1`` - Fiber parameters in fiber direction 1.

          * ``FIB2`` - Fiber parameters in fiber direction 2.

          * ``FIB3`` - Fiber parameters in fiber direction 3.

          * ``USER`` - User-defined linear elastic properties. For more information on the user_tbelastic
            subroutine, see the `Guide to User-Programmable Features
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/ansysprog_aero_fullycoupled.html>`_

        * ``References:`` - See :ref:`tbfield` for more information about defining temperature- and/or
          frequency-dependent properties.

          `Regularized Anisotropic Damage
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_damageall.html#>`_

          `Full Harmonic Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR4_5.html#sect2_lfd_wk5_2v>`_

        .. _ELST_spec:

        * ``NTEMP:`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT:`` - Not used.

        * ``References:`` - `Anisotropic Elastic Loss Tangent
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_electricmagnet.html#eqe22b3cb5-2fc6-4cc3-8cc4-00b26991ab45>`_

        .. _TBexperimental:

        * ``NTEMP :`` - Number of temperatures for which data will be provided.

        * ``NPTS :`` - Number of data points to be specified for a given temperature.

        * ``TBOPT :`` - Experimental data type:

          * ``UNITENSION`` - Uniaxial tension experimental data.

          * ``UNICOMPRESSION`` - Uniaxial compression experimental data.

          * ``UNIAXIAL`` - Uniaxial experimental data (combined uniaxial tension and compression).

          * ``BIAXIAL`` - Equibiaxial experimental data.

          * ``SHEAR`` - Pure shear experimental data (also known as planar tension).

          * ``SSHEAR`` - Simple shear experimental data.

          * ``VOLUME`` - Volumetric experimental data.

          * ``GMODULUS`` - Shear modulus experimental data.

          * ``KMODULUS`` - Bulk modulus experimental data.

          * ``EMODULUS`` - Tensile modulus experimental data.

          * ``NUXY`` - Poisson's ratio experimental data.

        * ``References:`` -

          `Experimental Response Functions
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_mat5.html#thy_unidevfirstinv>`_

          `Viscoelasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#mat_harmvisco>`_

          See also :ref:`tbfield` for information about defining field-dependent experimental data.

        .. _TBDTSpFCONjwf070600:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. Maximum = 20.

        * ``NPTS :`` - Number of data points to be specified for a given temperature. Default = 1. Maximum =
          100.

        * ``TBOPT :`` - Not used.

        * ``References:`` - ``FLUID116``

        .. _TBfclispecs:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS :`` - Number of data points to be specified for a given temperature. Default = 20 when
          ``TBOPT`` = 1. Default = 9 when ``TBOPT`` = 2.

        * ``TBOPT :`` - Material strength limit definition:

          * ``1`` - Define stress-strength limits.

          * ``2`` - Define strain-strength limits.

        * ``References:`` -

        .. _tbfluidspec:

        * ``NTEMP:`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS:`` - Number of data points to be specified for a given temperature.

        * ``TBOPT:`` - Fluid material options:

          * ``LIQUID`` - Define material constants for a liquid material.

          * ``GAS`` - Define material constants for a gas material.

          * ``PVDATA`` - Define pressure-volume data for a fluid material.

        * ``References:`` -

          `Fluid Material Models
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thyfluidmatmod.html#>`_

        .. _tbfricspec:

        * ``NTEMP:`` - Number of temperatures for which data will be provided. Default = 1. No maximum
        limit.

          ``NTEMP`` is not used for the following situations:

          * Isotropic or orthotropic friction defined in terms of field data ( :ref:`tbfield` command)

          * User-defined friction ( ``TBOPT`` = USER)

        * ``NPTS:`` - Number of data points to be specified for user-defined friction ( ``TBOPT`` = USER).
          Not used for ``TBOPT`` = ISO or ``TBOPT`` = ORTHO.

        * ``TBOPT:`` - Friction options:

          * ``ISO`` - Isotropic friction (one coefficient of friction, MU) (default). This option is valid for
            all 2D and 3D contact elements.

          * ``ORTHO`` - Orthotropic friction (two coefficients of friction, MU1 and MU2). This option is valid
            for the following 3D contact elements: ``CONTA174``, ``CONTA175``, and ``CONTA177``.

          * ``FORTHO`` - Orthotropic friction (two coefficients of friction, MU1 and Mu2) with a friction
            coordinate system fixed in space. This option is valid for the following 3D contact elements:
            ``CONTA174``, ``CONTA175``, and ``CONTA177``.

          * ``EORTHO`` - Equivalent orthotropic friction (two coefficients of friction, MU1 and MU2). This
            option differs from ``TBOPT`` = ORTHO only in the way the friction coefficients are interpolated
            when they are dependent upon the following field variables: sliding distance and/or sliding
            velocity. In this case, the total magnitude of the field variable is used to do the interpolation.

          * ``USER`` - User defined friction. This option is valid for all 2D and 3D contact elements.

        * ``References:`` - `Contact Friction
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/contfriction.html#userfriction>`_

          See also :ref:`tbfield` for more information about defining a coefficient of friction that is
          dependent on temperature, time, normal pressure, sliding distance, or sliding relative velocity.

        .. _TBDTSgas111501:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. The maximum
        number of
          temperatures specified is such that ``NTEMP`` \* ``NPTS`` < 2000.

        * ``NPTS :`` - Number of data points to be specified for a given temperature. Default = 5 for
          ``TBOPT`` = PARA. Default = 1 for all other values of ``TBOPT``.

        * ``TBOPT :`` - Gasket material options.

          * ``PARA`` - Gasket material general parameters.

          * ``COMP`` - Gasket material compression data.

          * ``LUNL`` - Gasket linear unloading data.

          * ``NUNL`` - Gasket nonlinear unloading data.

          * ``TSS`` - Transverse shear data.

          * ``TSMS`` - Transverse shear and membrane stiffness data. (If selected, this option takes
            precedence over TSS.)

        * ``References:`` - `Gasket
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/gask.html#fnstablestiff>`_

          `Gasket Joints Simulation
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STgaga.html>`_

        .. _TBgurspec:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. Maximum = 40.

        * ``NPTS :`` - Number of data points to be specified for a given temperature.

        * ``TBOPT :`` - GURSON material options.

          * ``BASE`` - Basic model without nucleation or coalescence (default).

          * ``SNNU`` - Strain controlled nucleation.

          * ``SSNU`` - Stress controlled nucleation.

          * ``COAL`` - Coalescence.

        * ``References:`` - `Gurson
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#matgursondefining>`_

          `Gurson's Model
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_mat1.html#gursonchaboche>`_

        .. _TBDTSpHFLMjwf070600:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. Maximum = 20.

        * ``NPTS :`` - Number of data points to be specified for a given temperature. Default = 1. Maximum =
          100.

        * ``TBOPT :`` - Not used.

        * ``References:`` - ``FLUID116``

        .. _TBDTSpHILLjwf070600:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. Maximum = 40.

        * ``NPTS :`` - Not used.

        * ``TBOPT:`` - Hill plasticity option:

          * ``(blank)`` - Use one set of Hill parameters (default).

          * ``PC`` - Enter separate Hill parameters for plasticity and creep. This option is valid for
            material combinations of creep and Chaboche nonlinear kinematic hardening only.

        * ``References:`` - `Hill Anisotropy
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_

          `Hill Yield Criterion
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_

          See also `Combining Material Models
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/strmamoco050401.html>`_

        .. _TBDTSpHYPEjwf070600:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. The maximum
          value of ``NTEMP`` is such that ``NTEMP`` x ``NPTS`` = 1000.

        * ``NPTS :`` - Number of material parameters to be specified for a given temperature. Exceptions are
          for ``TBOPT`` = FOAM, OGDEN, POLY and YEOH, where ``NPTS`` is the number of terms in the material
          model``s energy function.

        * ``TBOPT :`` - Hyperelastic material options.

          * ``BOYCE`` - `Arruda-Boyce model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eqcf34a3a5-b377-4b06-9d92-4a7e8e958452>`_.
            For ``NPTS``, default = 3 and maximum = 3.

          * ``BLATZ`` - `Blatz-Ko model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eq1798ab0a-0024-4cef-9876-f55aa5303ff0>`_.
            For ``NPTS``, default = 1 and maximum = 1.

          * ``ETUBE`` - Extended tube model. Five constants ( ``NPTS`` = 5) are required.

          * ``EXF1`` - `Embedded fiber
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eqeb96a83f-1199-4b6e-9338-edf5bebd5ebd>`_
            directions. Three constants ( ``NPTS`` = 3) define the direction for each fiber. Up to five fibers (
            ``NPTS`` = 15) are allowed.

          * ``EX1`` - `Embedded fiber
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eqeb96a83f-1199-4b6e-9338-edf5bebd5ebd>`_
            strain energy potential. Two constants ( ``NPTS`` = 2) are used for each fiber corresponding to the
            defined fiber directions. Undefined values default to zero.

          * ``EXA1`` - `Embedded fiber
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eqeb96a83f-1199-4b6e-9338-edf5bebd5ebd>`_
            compression strain energy potential. Two constants ( ``NPTS`` = 2) are used for each fiber
            corresponding to the defined fiber directions. If not defined, the values specified via EX1 are used
            for both tension and compression.

          * ``FOAM`` - `Hyperfoam (Ogden) model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eq10fe0596-b96a-403b-93f2-1cd3fd8e5adc>`_.
            For ``NPTS``, default = 1 and maximum is the number of terms in the energy function

          * ``GENT`` - `Gent model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eq1300db31-3ece-4812-97ab-279677eddff4>`_.
            For ``NPTS``, default = 3 and maximum = 3.

          * ``MOONEY`` - `Mooney-Rivlin model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eqb1e391b8-b91d-4fea-
            bd00-7efa10f7041e>`_ (default). You can choose a two-parameter Mooney-Rivlin model with ``NPTS`` = 2
            (default), or a three-, five-, or nine-parameter model by setting ``NPTS`` equal to one of these
            values.

          * ``NEO`` - `Neo-Hookean model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eq9758debe-5160-4a73-82a8-8a94f56d6149>`_.
            For ``NPTS``, default = 2 and maximum = 2.

          * ``OGDEN`` - `Ogden model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eqfac052c9-3204-4464-961f-51beb045c192>`_.
            For ``NPTS``, default = 1 and maximum is the number of terms in the energy function.

          * ``POLY`` - `Polynomial form model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eqeac1ba8c-e46b-4ede-a548-778615d646a5>`_.
            For ``NPTS``, default = 1 and maximum is the number of terms in the energy function.

          * ``RESPONSE`` - `Experimental response function model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eqd5e2d942-b39c-4fe3-a1ba-24e8949a80c1>`_.
            For ``NPTS``, default = 0 and maximum is such that ``NTEMP`` x ``NPTS`` + 2 = 1000.

          * ``YEOH`` - `Yeoh model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#eq7eea257d-c84c-4920-ab85-a27129367c87>`_.
            For ``NPTS``, default = 1 and maximum is the number of terms in the energy function.

          * ``USER`` - User-defined hyperelastic model.

        * ``References:`` - `Hyperelasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#hyperthermdefcon>`_

        .. _tbinterspec:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1. No maximum
          limit. ``NTEMP`` is used only for user-defined contact interaction ( ``TBOPT`` = USER).

        * ``NPTS :`` - Number of data points to be specified. ``NPTS`` is used only for user-defined contact
          interaction ( ``TBOPT`` = USER).

        * ``TBOPT :`` - Contact interaction options.

          The following options are valid only for general contact interactions specified via the :ref:`gcdef`
            command:
          * ``STANDARD`` - Standard unilateral contact (default).

          * ``ROUGH`` - Rough, no sliding.

          * ``NOSEPE`` - No separation (sliding permitted).

          * ``BONDED`` - Bonded contact (no separation, no sliding).

          * ``ANOSEP`` - No separation (always).

          * ``ABOND`` - Bonded (always).

          * ``IBOND`` - Bonded (initial contact).

           The following option is valid for all 2D and 3D contact elements:
          * ``USER`` - User-defined contact interaction.

        * ``References:`` - `Contact Interaction
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/continteraction.html#continteruser>`_

          `Defining Your Own Contact Interaction ( USERINTER)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctecuserinterfacial.html#>`_

        .. _tbjoinspec:

        * ``NTEMP:`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS:`` - Number of data points to be specified for a given temperature. ``NPTS`` is ignored if
          ``TBOPT`` = STIF or DAMP.

          If Coulomb friction is specified, ``NPTS`` is used only for ``TBOPT`` = MUS1, MUS4, and MUS6.

        * ``TBOPT:`` - Joint element material options.

           Linear stiffness behavior:
          * ``STIF`` - Linear stiffness.

           Nonlinear stiffness behavior:
          * ``JNSA`` - Nonlinear stiffness behavior in all available components of relative motion for the
            joint element.

          * ``JNS1`` - Nonlinear stiffness behavior in local UX direction only.

          * ``JNS2`` - Nonlinear stiffness behavior in local UY direction only.

          * ``JNS3`` - Nonlinear stiffness behavior in local UZ direction only.

          * ``JNS4`` - Nonlinear stiffness behavior in local ROTX direction only.

          * ``JNS5`` - Nonlinear stiffness behavior in local ROTY direction only.

          * ``JNS6`` - Nonlinear stiffness behavior in local ROTZ direction only.

           Linear damping behavior:
          * ``DAMP`` - Linear damping.

           Nonlinear damping behavior:
          * ``JNDA`` - Nonlinear damping behavior in all available components of relative motion for the joint
            element.

          * ``JND1`` - Nonlinear damping behavior in local UX direction only.

          * ``JND2`` - Nonlinear damping behavior in local UY direction only.

          * ``JND3`` - Nonlinear damping behavior in local UZ direction only.

          * ``JND4`` - Nonlinear damping behavior in local ROTX direction only.

          * ``JND5`` - Nonlinear damping behavior in local ROTY direction only.

          * ``JND6`` - Nonlinear damping behavior in local ROTZ direction only.

           Friction Behavior:
          * ``Coulomb friction coefficient -`` - The values can be specified using either :ref:`tbdata` (
            ``NPTS`` = 0) or :ref:`tbpt` ( ``NPTS`` is nonzero).

          * ``MUS1`` - Coulomb friction coefficient (stiction) in local UX direction only.

          * ``MUS4`` - Coulomb friction coefficient (stiction) in local ROTX direction only.

          * ``MUS6`` - Coulomb friction coefficient (stiction) in local ROTZ direction only, or

            Coulomb friction coefficient (stiction) for Spherical Joint.

          * ``Coulomb friction coefficient - Exponential Law -`` - Use :ref:`tbdata` to specify μ:sub:`s`,
            μ:sub:`d`, and c for the exponential law.

          * ``EXP1`` - Exponential law for friction in local UX direction only.

          * ``EXP4`` - Exponential law for friction in local ROTX direction only.

          * ``EXP6`` - Exponential law for friction in local ROTZ direction only.

           Elastic slip:
          * ``SL1`` - Elastic slip in local UX direction only.

          * ``SL4`` - Elastic slip in local ROTX direction only.

          * ``SL6`` - Elastic slip in local ROTZ direction only, or

            Elastic slip for Spherical Joint.

          * ``TMX1`` - Critical force in local UX direction only.

          * ``TMX4`` - Critical moment in local ROTX direction only.

          * ``TMX6`` - Critical moment in local ROTZ direction only.

           Stick-stiffness:
          * ``SK1`` - Stick-stiffness in local UX direction only.

          * ``SK4`` - Stick-stiffness in local ROTX direction only.

          * ``SK6`` - Stick-stiffness in local ROTZ direction only, or

            Stick-stiffness for Spherical Joint.

           Interference fit force/moment:
          * ``FI1`` - Interference fit force in local UX direction only.

          * ``FI4`` - Interference fit moment in local ROTX direction only.

          * ``FI6`` - Interference fit moment in local ROTZ direction only.

        * ``References:`` - `MPC184 Joint
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/jointmat.html#mpcfriction>`_

        .. _tbjointedrockspec:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - * ``BASE`` - Base material parameters.

          * ``RCUT`` - Base material tension cutoff.

          * ``RSC`` - Residual strength coupling.

          * ``FPLANE`` - Joint parameters.

          * ``FTCUT`` - Joint tension cutoff.

          * ``FORIE`` - Joint orientation.

          * ``MSOL`` - `Material solution option
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#>`_.

        * ``References:`` - `Jointed Rock
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#>`_

        .. _tbmohrcoulombspec:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - * ``BASE`` - Mohr-Coulomb material parameters.

          * ``RCUT`` - Tension cutoff.

          * ``RSC`` - Residual strength coupling.

          * ``POTN`` - Plastic potential.

          * ``FRICTION`` - Friction angle scaling.

          * ``COHESION`` - Cohesion scaling.

          * ``TENSION`` - Tension strength scaling.

          * ``DILATATION`` - Dilatancy angle scaling.

          * ``MSOL`` - `Material solution option
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#>`_.

        * ``References:`` - `Mohr-Coulomb
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#>`_

        .. _tbmelasspec:

        * ``NTEMP :`` - Number of temperatures for which data will be provided.

        * ``NPTS :`` - Number of data points to be specified for a given temperature.

        * ``TBOPT :`` - Not used.

        * ``References:`` - `Multilinear Elasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_multilinelas.html#eqb58de8d9-86b1-4b61-ba30-bbf72444234a>`_

        .. _tbmigrspec:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - Migration model options.

          * ``0`` - Atomic (or ion) flux (default).

          * ``1`` - Vacancy flux.

        * ``References:`` - `Migration Model
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/migr.html#migr_vacancy>`_

          `Electric-Diffusion Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cou/coupelecdiff.html#>`_

          `Thermal-Diffusion Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cou/couthermdiffanal.html#coudirextda>`_

          `Structural-Diffusion Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cou/coustrdiffana.html#>`_

          `Electric-Diffusion Coupling
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thry_elec_diff_couple.html#eq4df90de8-0708-4ba0-90a1-b9cb38b44dcf>`_

          `Thermal-Diffusion Coupling
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thry_therm_diff_couple.html#eqa72b8051-83ce-4640-b97b-e6bae9fed535>`_

          `Structural-Diffusion Coupling
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thry_str_diff_cou.html#eq00699203-a90a-4e59-a5d5-803bca2f9dad>`_

        .. _TBmplanespec:

        * ``NTEMP :`` - The number of temperatures for which data will be provided. Default = 1. Maximum is
          such that ``NTEMP`` x ``NPTS`` = 1000.

        * ``NPTS :`` - The number of data points to be specified for a given temperature. Default = 6.
          Maximum is such that ``NTEMP`` x ``NPTS`` = 1000.

        * ``TBOPT :`` - Microplane model options:

          * ``ORTH`` - `Elastic microplane material with damage
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/microplane.html#>`_ model (default).

          * ``DPC`` - `Coupled damage-plasticity
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/microplane.html#>`_ microplane
            model.

          * ``NLOCAL`` - `Nonlocal parameters
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/microplane.html#eq1cc4a2af-945c-470d-a125-21c3c06eccea>`_.

        * ``References:`` - `Microplane
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/microplane.html#matmicroplanereadlist>`_

        .. _TBDTSpNLISjwf070600:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS :`` - Number of data points to be specified for a given temperature. Default = 4. Maximum =
          4.

        * ``TBOPT :`` - Isotropic hardening options.

          * ``VOCE`` - Voce hardening law (default).

          * ``POWER`` - Power hardening law.

        * ``References:`` - `Nonlinear Isotropic Hardening
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#matnlisvocelaw>`_

        .. _TBperf_model_spec:

        * ``NTEMP:`` - Not used.

        * ``NPTS:`` - Not used.

        * ``TBOPT:`` - Equivalent fluid model options:

          * ``JCA`` - Johnson-Champoux-Allard model

          * ``DLB`` - Delaney-Bazley model

          * ``MIKI`` - Miki model

          * ``ZPRO`` - Complex impedance and propagating constant model

          * ``CDV`` - Complex density and velocity model

          Poroelastic acoustic material:

          * ``PORO`` - Poroelastic material model

          Transfer admittance matrix options:

          * ``YMAT`` - General transfer admittance matrix model

          * ``SGYM`` - Transfer admittance matrix model of square grid structure

          * ``HGYM`` - Transfer admittance matrix model of hexagonal grid structure

        * ``References:`` - `Perforated Media
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/acousticmat.html#acous_mat_trans_admit>`_

          `Equivalent Fluid of Perforated Materials
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thyacous_proprad.html#>`_

          `Poroelastic Acoustics
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thyacous_poroelastic.html#thyacous_poro_coup>`_

          `Perforated Material
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_acous/acous_mat_equivperf.html#acous_poromat>`_

          `Trim Element with Transfer Admittance Matrix
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_acous/acous_excit_loads.html#>`_

          See :ref:`tbfield` for more information about defining temperature and/or frequency-dependent
          properties.

        .. _TBDTSpPIEZjwf070600:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - Piezoelectric matrix options.

          * ``0`` - Piezoelectric stress matrix [e] (used as supplied)

          * ``1`` - Piezoelectric strain matrix [d] (converted to [e] form before use)

        * ``References:`` - `Piezoelectricity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_electricmagnet.html#eqa42ac64b-bb76-4eab-
          ad28-d8fba52e2755>`_

          `Piezoelectric Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cou/Hlp_G_COU3_piezo.html#>`_

        .. _tbplasticspec:

        * ``NTEMP:`` - Not used.

        * ``NPTS:`` - Not used.

        * ``TBOPT:`` - Plasticity option:

          * ``BISO`` - `Bilinear isotropic hardening plasticity
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_.

          * ``BKIN`` - `Bilinear kinematic hardening plasticity
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_.

          * ``MISO`` - `Multilinear isotropic hardening plasticity
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_.

          * ``KINH`` - `Multilinear kinematic hardening plasticity
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_.

            The number of points ( :ref:`tbpt` commands issued) is limited to 100 for this option.

          * ``KSR2`` - `Kinematic static recovery
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_.

          * ``ISR`` - `Isotropic static recovery
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_.

        * ``References:`` - `Rate-Independent Plasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#sintering>`_

        .. _tbporelasspec:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - * ``POISSON`` - Porous elasticity model..

        * ``References:`` - `Porous Elasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_porous_elasticity.html#matporelasdefining>`_

        .. _TBpmspec:

        * ``NTEMP :`` - The number of temperatures. Default = 1. The maximum must be a value such that (
          ``NTEMP`` x ``NPTS`` ) <= 1000.

        * ``NPTS :`` - The number of material constants. Default = 4. The maximum must be a value such that
          ( ``NTEMP`` x ``NPTS`` ) <= 1000.

        * ``TBOPT :`` - Porous media options:

          * ``PERM`` - Permeability

          * ``BIOT`` - Biot coefficient

          * ``SP`` - Solid property

          * ``FP`` - Fluid property

          * ``DSAT`` - Degree-of-saturation table

          * ``RPER`` - Relative-permeability table

          * ``GRAV`` - Gravity magnitude

        * ``References:`` - `Porous Media Material Properties
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/elemdatatblpor.html#pormedunitsperm>`_

          `Porous Media Flow
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thypormediaflow.html#eqf368dccd-e6d9-4ee1-af36-04edf2a7e0ed>`_

          `Structural-Pore-Fluid-Diffusion-Thermal Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cou/Hlp_G_COU_porefluiddiffstruct.html#coupfdsanalysis>`_

          `Applying Initial Degree of Saturation and Relative Permeability
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/Hlp_G_INSTAPPL.html#>`_

          See also `VM260
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_vm/Hlp_V_VM260.html#vm260.results1>`_.

        .. _tbpronyspecjmb:

        * ``NTEMP:`` - Number of temperatures for which data will be provided. Default = 1.

          Unused for ``TBOPT`` = EXPERIMENTAL.

        * ``NPTS:`` - Defines the number of Prony series pairs for ``TBOPT`` = SHEAR or ``TBOPT`` = BULK.
          Default = 1.

          Unused for ``TBOPT`` = INTEGRATION and ``TBOPT`` = EXPERIMENTAL.

        * ``TBOPT:`` - Defines the behavior for viscoelasticity.

          * ``SHEAR`` - Shear Prony series.

          * ``BULK`` - Bulk Prony series.

          * ``INTEGRATION`` - Stress update algorithm.

          * ``EXPERIMENTAL`` - Complex modulus from experimental data.

        * ``References:`` - `Viscoelasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#mat_harmvisco>`_

        .. _tbpzrsspec:

        * ``NTEMP:`` - Not used.

        * ``NPTS:`` - Not used.

        * ``TBOPT:`` - Piezoresistive matrix options

          * ``0`` - Piezoresistive stress matrix (used as supplied)

          * ``1`` - Piezoresistive strain matrix (used as supplied)

        * ``References:`` - `Piezoresistivity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_electricmagnet.html#eqe0185ba1-ccf6-46fc-99f8-7b3596865855>`_

          `Piezoresistive Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cou/Hlp_G_COU3_piezores.html#>`_

        .. _TBDTSpRATEjwf070600:

        * ``NTEMP :`` - The number of temperatures for which data will be provided. Default is 1. Maximum is
          such that ``NTEMP`` x ``NPTS`` = 1000.

        * ``NPTS :`` - The number of data points to be specified for a given temperature. Default = 2.
          Maximum is such that ``NTEMP`` x ``NPTS`` = 1000.

        * ``TBOPT :`` - Rate-dependent viscoplasticity options.

          * ``PERZYNA`` - Perzyna option (default).

          * ``PEIRCE`` - Peirce option.

          * ``EVH`` - Exponential visco-hardening option.

          * ``ANAND`` - Anand option.

        * ``References:`` - `Rate-Dependent Plasticity (Viscoplasticity)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/rate.html#matdpcreep>`_

          `Viscoplasticity Model
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR8_3.html#avFlpr2dtlm>`_

          `Rate-Dependent Plasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_mat2.html#matanandvisco>`_

          See also `Combining Material Models
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/strmamoco050401.html>`_

        .. _tbsdampspec:

        * ``NTEMP:`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS:`` - Number of properties to be defined for the material option. Default = 1 for each
          material damping option ( ``TBOPT`` ) selected.

        * ``TBOPT:`` - Material damping options:

          * ``STRU or 1`` - Structural damping coefficient (default).

          * ``ALPD or 2`` - Rayleigh mass proportional material damping.

          * ``BETD or 3`` - Rayleigh stiffness proportional material damping.

        * ``References:`` - `Material Damping
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_matdamping.html#>`_

          `Full Harmonic Analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR4_5.html#sect2_lfd_wk5_2v>`_

          `Damping Matrices
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_tool3.html#>`_

        .. _tbshiftspecjmb:

        * ``NTEMP:`` - Allows one temperature for which data will be provided.

        * ``NPTS:`` - Number of material constants to be entered as determined by the `shift function
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#mat_userdefshift>`_
        specified via ``TBOPT``. Not used for ``TBOPT`` = PLIN.

          * ``3`` - for ``TBOPT`` = WLF

          * ``2`` - for ``TBOPT`` = TN

          * ``n, :sub:`f``` - for ``TBOPT`` = FICT, where ``n`` :sub:`f` is the number of partial fictive
            temperatures

        * ``TBOPT:`` - Shift function:

          * ``WLF`` - `Williams-Landel-Ferry
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#eq54042d38-108a-429b-a239-e5796a477097>`_.

          * ``TN`` - `Tool-Narayanaswamy
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#matliquidcoeef>`_.

          * ``FICT`` - `Tool-Narayanaswamy
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#matliquidcoeef>`_ with
            fictive temperature.

          * ``PLIN`` - `Piecewise linear
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#eqba8af3fc-
            fa01-4b6b-992c-094ad649ad1f>`_.

          * ``USER`` - User-defined.

        * ``References:`` - `Viscoelasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/evis.html#mat_harmvisco>`_

        .. _tbsintspec:

        * ``NTEMP:`` - Not used.

        * ``NPTS:`` - Not used.

        * ``TBOPT:`` - Sintering options:

          * ``INIT`` - `Initial conditions
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_ : relative
            density, particle diameter, and grain-size diameter. The initial relative density can alternatively
            be specified as a location-varying initial state ( :ref:`inistate` ).

          * ``PARAM`` - `Sintering activation temperature
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_ and mode
            specification.

          * ``STRESS`` - Sintering stress coefficients.

          * ``VSCOEF`` - `Viscosity coefficients
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_. Mutually
            exclusive with VSTABLE.

          * ``VSTABLE`` - Table of viscosity values. Mutually exclusive with VSCOEF.

          * ``GROWTH`` - `Grain-growth
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_ parameters.

          * ``RIEDEL`` - Selects the Riedel sintering model (default) and defines the viscous moduli
            coefficients.

          * ``SOVS`` - Selects the Skorohold-Olevsky sintering model and defines the viscous moduli
            coefficients.

          * ``ANICONST`` - `Orthotropic factors
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_ to be applied
            to the viscous bulk and shear moduli. The factors remain constant throughout densification.

        * ``References:`` - `Sintering
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_

        .. _TBDTSpSMA:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS :`` - Number of data points to be specified for a given temperature. Default = 7 if
          ``TBOPT`` = SUPE or MEFF, 2 if ``TBOPT`` = METE, 6 if ``TBOPT`` = METL or METH, and 7 if ``TBOPT`` =
          MEPD.

        * ``TBOPT :`` - Shape memory model option:

          SUPE -- `Superelasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#>`_ option (default).

          MEFF -- `Shape memory effect
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#>`_ option.

          METE - Shape memory effect with `plasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#matparmsmaplastic>`_
          option: elastic phase-dependent and thermal expansion.

          METL - Shape memory effect with `plasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#matparmsmaplastic>`_
          option: limits of transformation in strain-stress-temperature space.

          METH - Shape memory effect with `plasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#matparmsmaplastic>`_
          option: transformation hardening.

          MEPD - Shape memory effect with `plasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#matparmsmaplastic>`_
          option: plastic response.

          METC - Shape memory effect with `plasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#matparmsmaplastic>`_
          option: tension-compression asymmetry response and hysteresis response.

        * ``Reference:`` - `Shape Memory Alloy (SMA)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/smas.html#matsmareadlist>`_

        .. _tbsoilspec:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - * ``CAMCLAY`` - Modified Cam-clay material model.

          * ``MSOL`` - `Material solution option
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#>`_.

        * ``References:`` - `Cam-clay
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_geomechanics.html#>`_

        .. _TBDTSpSTATjwf070600:

        When ``Lab`` = STATE, state variable specifications affect user-defined material models. The
        subroutine in use depends on the element type used when ``Lab`` = USER is specified.

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Number of state variables.

        * ``TBOPT :`` - Not used.

        * ``References:`` - `Customizing Material Behavior
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/matcustommatmods.html#matsubroutstatevars>`_

        .. _TBDTSpSWELjwf070600:

        * ``NTEMP :`` - Number of temperatures for which data will be provided. The maximum value of NTEMP
          is such that NTEMP x NPTS = 1000

        * ``NPTS :`` - Number of data points to be specified for a given temperature. The maximum value of
          NPTS is such that NPTS x NTEMP = 1000.

        * ``TBOPT :`` - Swelling model options:

          * ``LINEAR`` - Linear swelling function.

          * ``EXPT`` - Exponential swelling function.

          * ``USER`` - User-defined swelling function. Define the swelling function via subroutine
            userswstrain (described in the `Programmer&#39;s Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Hlp_P_UPFTOC.html>`_). Define temperature-dependent constants via the
            :ref:`tbtemp` and :ref:`tbdata` commands. For solution-dependent variables, define the number of
            variables via the :ref:`tb`,STATE command.

        * ``References:`` - `Swelling
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/swel.html#eqe6a35e77-4361-4a55-8524-4e97a33209aa>`_

          `Swelling Model
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR8_3.html#>`_

        .. _tbthermspec:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - Thermal properties:

          * ``COND`` - Thermal conductivity.

          * ``ENTH`` - Enthalpy. Enthalpy must be a function of temperature only (see :ref:`Considerations for
            Enthalpy). <TB_enthalpy_notes>`

          * ``SPHT`` - Specific heat. For `porous media
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/elemdatatblpor.html#pormedflowdamp>`_,
            solid-skeleton specific heat.

          * ``FLSPHT`` - Fluid-specific heat for `porous media
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/elemdatatblpor.html#pormedflowdamp>`_.

        * ``References:`` - `Thermal Properties
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/thermalmat.html#>`_

          `Porous Media Mechanics
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/elemdatatblpor.html#heattranseq>`_

        .. _tbtnmspec:

        * ``NTEMP :`` - Not used.

        * ``NPTS :`` - Not used.

        * ``TBOPT :`` - Three-network model material options:

          * ``NETA`` - Network A properties.

          * ``NETB`` - Network B properties.

          * ``NETC`` - Network C properties.

          * ``FLOW`` - Network flow properties.

          * ``TDEP`` - Temperature-dependence factors.

          * ``LOCK`` - Chain-locking stretch.

          * ``BULK`` - Bulk modulus.

        * ``References:`` - `Three-Network Model ( TB,TNM)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/aQw8sq22dldm.html#mathypertnmrefs>`_

        .. _TBDTSpUSERjwf070600:

        When ``Lab`` = USER, the :ref:`tb` command activates either the `UserMat
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ (user-defined
        material) or the `UserMatTh
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ (user-defined
        thermal material) subroutine automatically. The subroutine activated depends on the element type
        used.

        * ``NTEMP :`` - Number of temperatures for which data will be provided. Default = 1.

        * ``NPTS :`` - Number of data points to be specified for a given temperature. Default = 48.

        * ``TBOPT:`` - User-defined material model ( `UserMat
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ ) or thermal
        material model ( `UserMatTh
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ ) options:

          * ``NONLINEAR`` - Nonlinear iterations are applied (default).

          * ``LINEAR`` - Nonlinear iterations are not applied. This option is ignored if there is any other
            nonlinearity involved, such as contact, geometric nonlinearity, etc.

          * ``MXUP`` - This option indicates a `UserMat material model
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ to be used
            with `mixed u-P element formulation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_continuumelems.html#EL2omnusjwf091100>`_
            for material exhibiting incompressible or nearly incompressible behavior.

          * ``THERM`` - Thermal material model ( UserMatTh ) for a coupled-field analysis using elements
            ``SOLID225``, ``SOLID226`` and ``SOLID227`` with thermal degrees of freedom. Use this option in a
            coupled structural-thermal analysis to specify a user-defined thermal material model ( `UserMatTh
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ )
            independently of the user-defined structural material model ( `UserMat
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ ).

        * ``References:`` - `Customizing Material Behavior
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/matcustommatmods.html#matsubroutstatevars>`_

          `Subroutine UserMat (Creating Your Own Material Model)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_

          `Subroutine UserMatTh (Creating Your Own Thermal Material Model)
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_

        .. _tbwearspec:

        * ``NTEMP:`` - Number of temperatures for which data will be provided.

        * ``NPTS:`` - Number of data points to be specified for the wear option. This value is set
          automatically based on the selected wear option ( ``TBOPT`` ). If ``TBOPT`` is not specified, the
          default becomes ``NPTS`` = 5 and ``TBOPT`` = ARCD.

        * ``TBOPT:`` - Wear model options:

          * ``ARCD`` - Archard wear model (default).

          * ``USER`` - User-defined wear model.

          * ``AUTS`` - Automatic scaling of wear increment. Must be used in conjunction with one of the wear
            models ( ``TBOPT`` = ARCD or USER).

        * ``References:`` - `Contact Surface Wear
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/contwearmat.html#>`_

          `Contact Surface Wear
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_includwear.html>`_

          See also :ref:`tbfield` for more information about defining temperature and/or time-dependent
          properties.

        .. _xtalspec:

        * ``NTEMP:`` - Unused.

        * ``NPTS:`` - Unused.

        * ``TBOPT:`` - Crystal plasticity material options:

          * ``ORIE`` - Crystal orientation.

          * ``NSLFAM`` - Number of slip families.

          * ``FORM`` - Formulation number.

          * ``XPARAM`` - Crystal characteristic parameters.

          * ``HARD`` - Slip system hardness properties.

          * ``FLFCC`` - Face-centered cubic (FCC) flow parameters.

          * ``FLHCP`` - Hexagonal closed packed (HCP) flow parameters.

          * ``FLBCC`` - Body-centered cubic (BCC) flow parameters.

        * ``Reference:`` - `Crystal Plasticity
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/crystalplast.html#cpmrefs>`_

        .. _TB_notes:

        :ref:`tb` activates a data table for use by subsequent :ref:`tbdata` or :ref:`tbpt` commands. The
        table space is initialized to zero values. Data from this table are used for most nonlinear material
        descriptions as well as for special input for some elements.

        For a list of elements supporting each material model ( ``Lab`` value), see `Material Model Element
        Support
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/Mp8sasdgh.html#fncptnnnedp>`_

        For information about linear material property input, see :ref:`mp`.

        This command is also valid in SOLUTION.

        .. _TB_enthalpy_notes:

        Considerations for Enthalpy ( ``TBOPT`` = ENTH)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        * To ensure correct results, you must define enthalpy over a large enough temperature range to span
          all computed temperatures during the solution. The :ref:`tb` command does not extrapolate enthalpy
          values beyond the specified temp range like the :ref:`mp` command does.

        * If both the :ref:`tb` and :ref:`mp` commands are used to specify enthalpy values, enthalpy values
          defined via the :ref:`tb` command are used and those defined via the :ref:`mp` command are
          ignored.

        .. _TBprodRest:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"TB,{lab},{matid},{ntemp},{npts},{tbopt},,{funcname}"
        return self.run(command, **kwargs)

    def tbcopy(self, lab: str = "", matf: str = "", matt: str = "", **kwargs):
        r"""Copies a data table from one material to another.

        Mechanical APDL Command: `TBCOPY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBCOPY.html>`_

        Parameters
        ----------
        lab : str
            Data table label. See the :ref:`tb` command for valid labels, and see :ref:`TBCOPY_notes` for
            ``Lab`` = ALL.

        matf : str
            Material reference number where data table is to be copied from.

        matt : str
            Material reference number where data table is to be copied to.

        Notes
        -----

        .. _TBCOPY_notes:

        The :ref:`tbcopy` command, with ``Lab`` = ALL, copies all of the nonlinear data defined by the
        :ref:`tb` command. If you copy a model that includes both yield behavior constants and linear
        constants (for example, a BKIN model), :ref:`tbcopy`,ALL and :ref:`mpcopy` are used together to copy
        the entire model. All input data associated with the model is copied, that is, all data defined
        through the :ref:`tb` and :ref:`mp` commands.

        Also, if you copy a material model using the `Material Model Interface
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/BAS1matmodifjwf0413001150.html#BAS1mamoimisjwf0414000942>`_
        ( Edit> Copy ), both the commands :ref:`tbcopy`,ALL and :ref:`mpcopy` are issued, regardless of
        whether the model includes linear constants only, or if it includes a combination of linear and
        yield behavior constants.

        This command is also valid in SOLUTION.
        """
        command = f"TBCOPY,{lab},{matf},{matt}"
        return self.run(command, **kwargs)

    def tbdata(
        self,
        stloc: str = "",
        c1: str = "",
        c2: str = "",
        c3: str = "",
        c4: str = "",
        c5: str = "",
        c6: str = "",
        **kwargs,
    ):
        r"""Defines data for the material data table.

        Mechanical APDL Command: `TBDATA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBDATA.html>`_

        Parameters
        ----------
        stloc : str
            Data values assigned to six locations starting with ``STLOC``. If a value is already in this
            location, it is redefined. A blank value leaves the existing value unchanged.

        c1 : str
            Data values assigned to six locations starting with ``STLOC``. If a value is already in this
            location, it is redefined. A blank value leaves the existing value unchanged.

        c2 : str
            Data values assigned to six locations starting with ``STLOC``. If a value is already in this
            location, it is redefined. A blank value leaves the existing value unchanged.

        c3 : str
            Data values assigned to six locations starting with ``STLOC``. If a value is already in this
            location, it is redefined. A blank value leaves the existing value unchanged.

        c4 : str
            Data values assigned to six locations starting with ``STLOC``. If a value is already in this
            location, it is redefined. A blank value leaves the existing value unchanged.

        c5 : str
            Data values assigned to six locations starting with ``STLOC``. If a value is already in this
            location, it is redefined. A blank value leaves the existing value unchanged.

        c6 : str
            Data values assigned to six locations starting with ``STLOC``. If a value is already in this
            location, it is redefined. A blank value leaves the existing value unchanged.

        Notes
        -----

        .. _TBDATA_notes:

        Defines data for the table specified via the most recent :ref:`tb` command (at the temperature
        specified via the most recent :ref:`tbtemp` or :ref:`tbfield` command, if applicable).

        The type of data table specified determines the number of data values needed in :ref:`tbdata`. Data
        values are interpolated for temperatures or other specified field variables that fall between user-
        defined :ref:`tbtemp` or :ref:`tbfield` values.

        You can specify values for up to six constants per :ref:`tbdata` command. Issue the command multiple
        times if needed.

        Some elements (for example, ``SOLID226`` ) support tabular input for some linear materials. For a
        list of elements supporting tabular material properties and associated primary variables, see
        `Defining Linear Material Properties Using Tabular Input
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/ansmatdeflin.html#fntbdatareqd>`_

        This command is also valid in SOLUTION.
        """
        command = f"TBDATA,{stloc},{c1},{c2},{c3},{c4},{c5},{c6}"
        return self.run(command, **kwargs)

    def tbdele(
        self,
        lab: str = "",
        mat1: str = "",
        mat2: str = "",
        inc: str = "",
        tbopt: str = "",
        **kwargs,
    ):
        r"""Deletes previously defined material data tables.

        Mechanical APDL Command: `TBDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBDELE.html>`_

        Parameters
        ----------
        lab : str
            Material data table label to delete. (See :ref:`tb` for valid ``Lab`` values.)

        mat1 : str
            Deletes data tables for materials ``MAT1`` to ``MAT2`` (default = ``MAT1`` ) in steps of ``INC``
            (default = 1).

        mat2 : str
            Deletes data tables for materials ``MAT1`` to ``MAT2`` (default = ``MAT1`` ) in steps of ``INC``
            (default = 1).

        inc : str
            Deletes data tables for materials ``MAT1`` to ``MAT2`` (default = ``MAT1`` ) in steps of ``INC``
            (default = 1).

        tbopt : str
            Material data table option. (See :ref:`tb` for valid ``TBOPT`` values for the given ``Lab``.)

        Notes
        -----

        .. _TBDELE_notes:

        If ``Lab`` = ALL, delete all material data tables.

        If ``MAT1`` = ALL, ``MAT2`` and ``INC`` are ignored and all material data tables are deleted.

        If ``TBOPT`` is specified, the material data table corresponding to ``Lab`` is deleted if it also
        has the specified table option. If ``TBOPT`` is not specified, all material data tables
        corresponding to ``Lab`` are deleted. ``TBOPT`` is ignored when ``Lab`` = ALL.

        This command is also valid in SOLUTION, but is not intended for changing material behaviors between
        load steps.
        """
        command = f"TBDELE,{lab},{mat1},{mat2},{inc},{tbopt}"
        return self.run(command, **kwargs)

    def tbeo(self, par: str = "", value: str = "", **kwargs):
        r"""Sets special options or parameters for material data tables.

        Mechanical APDL Command: `TBEO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBEO.html>`_

        Parameters
        ----------
        par : str
            Parameter name:

            * ``CAPCREEPREG`` - Available for the viscoplasticity/creep model ( :ref:`tb`, CREEP ), allows two
              creep models to be specified via the same material ID when used with the Extended Drucker-Prager
              model ( :ref:`tb`, EDP ).

            * ``FDCS`` - Coordinate system to use with location (XCOR, YCOR, ZCOR) or displacement (UX, UY, UZ)
              field variables.

            * ``NEGSLOPE`` - Controls whether negative tangent slopes of the stress-strain curve are allowed for
              multilinear `kinematic
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_ or `isotropic
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#>`_ hardening in a
              `rate-independent plasticity
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/amp8sq21dldm.html#sintering>`_
              analysis.

        value : str
            Parameter value:

            When ``Par`` = CAPCREEPREG --

            * ``SHEA`` - Use the shear stress-state creep model with the Extended Drucker-Prager model.

            * ``COMP`` - Use the compaction stress-state creep model with the Extended Drucker-Prager model.

            When ``Par`` = FDCS --

            * Any predefined, user-defined, or custom ( :ref:`local` or :ref:`cs` ) Cartesian coordinate system
              number.

            When ``Par`` = NEGSLOPE --

            * ``0`` - Error-trap negative tangent slopes of the stress-strain curve (default).

            * ``1`` - Allow negative tangent slopes of the stress-strain curve.

        Notes
        -----

        .. _TBEO_notes:

        Issue the :ref:`tbeo` command after activating the material data table ( :ref:`tb` ) but before
        defining data for the table ( :ref:`tbdata` ) or a point on a nonlinear data curve ( :ref:`tbpt` ).

        If the defined material data table has subtables, issue the :ref:`tbeo` command for each desired
        subtable.
        """
        command = f"TBEO,{par},{value}"
        return self.run(command, **kwargs)

    def tbfield(self, type_: str = "", value: str = "", **kwargs):
        r"""Defines values of field variables for material data tables.

        Mechanical APDL Command: `TBFIELD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBFIELD.html>`_

        Parameters
        ----------
        type_ : str
            Field variable type:

            * ``CYCLE`` - A healing cycle number is to be specified in ``Value``.

            * ``FREQ`` - A frequency is to be specified in ``Value``.

            * ``NPRES`` - A normal pressure is to be specified in ``Value``.

            * ``PLSR`` - An equivalent plastic strain rate is to be specified in ``Value``.

            * ``PPRE`` - Pressure degree of freedom is to be specified in ``Value``.

            * ``SLDA`` - A total sliding distance (algebraic) is to be specified in ``Value``.

            * ``SLDI`` - A total sliding distance (absolute) is to be specified in ``Value``.

            * ``SLRV`` - A sliding velocity is to be specified in ``Value``.

            * ``SRAT`` - Stress ratio of fatigue load cycle is to be specified in ``Value``.

            * ``TEMP`` - A temperature is to be specified in ``Value``.

            * ``TIME`` - A time is to be specified in ``Value``.

            * ``UFXX`` - `User-defined
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_fielduserdef.html#>`_ field
              variable (UF01,UF02,..., UF09).

            * ``UX / UY / UZ`` - Displacements in the global/local X, Y, or Z coordinate system, respectively,
              are to be specified in ``Value``.

            * ``XCOR / YCOR / ZCOR`` - X, Y and Z locations, respectively, are to be specified in ``Value``..

        value : str
            The field value to be referenced.

        Notes
        -----
        Define your data tables as field-variable-dependent (via the appropriate :ref:`tb` command), then
        issue :ref:`tbfield` to define the field values.

        Issue this command multiple times to enter values for different field variables.

        Define data values in ascending order for all field quantities. If a field value is to be held
        constant, define it only once; subsequent definitions are ignored.

        No limit exists on the number of values that you can specify. The specified field value remains
        active until the next :ref:`tbfield` command is input.

        After you have defined the field value(s), define your data for the data tables ( :ref:`tbdata` ).

        For more information about the interpolation scheme used for field-dependent material properties,
        see `Understanding Field Variables
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/matexampFVinterp.html>`_

        For more information about using :ref:`tbfield` with :ref:`tb`,ELASTIC or :ref:`tb`,SDAMP, see
        `Full Harmonic Analysis
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR4_5.html#sect2_lfd_wk5_2v>`_

        The TEMP (temperature) predefined field variable is available for all material models defined via
        :ref:`tb`, ``Lab``.

        Several other field variables are available for use with some material models (when used with
        specific element types), such as TIME (time), PPRE (pore-pressure), XCOR / YCOR / ZCOR (location),
        UX / UY / UZ (displacement), and UF01 - UF09 ( `user-defined
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_fielduserdef.html#>`_ ).

        The field variables can be defined in the global coordinate system or in any local or user-defined
        coordinate system.

        For more information, see `Predefined Field Variables
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/matpredeffieldvars.html#>`_
        """
        command = f"TBFIELD,{type_},{value}"
        return self.run(command, **kwargs)

    def tbin(
        self,
        oper: str = "",
        par1: str = "",
        par2: str = "",
        par3: str = "",
        par4: str = "",
        **kwargs,
    ):
        r"""Sets parameters used for `interpolation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_loginterpscal.html#>`_ of the
        material data tables.

        Mechanical APDL Command: `TBIN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBIN.html>`_

        Parameters
        ----------
        oper : str
             Operation to perform:

            * :ref:`ALGO <tbinoperalgo>` - Specifies the interpolation algorithm to use for the subtable (or
              table if the material data table has only one subtable) being defined.

            * :ref:`BNDS <tbinoperbnds>` - Specifies the maximum and minimum bounds for individual field
              variables.

            * :ref:`CACH <tbinopercach>` - Enables or disables caching of interpolated data for better
              performance.

            * :ref:`DEFA <tbinoperdefa>` - Specifies the default value of the user-defined field variable used
              for interpolation (if no value was specified).

            * :ref:`EXTR <tbinoperextr>` - Controls extrapolation options.

            * :ref:`NORM <tbinopernorm>` - Scales the field variables before interpolation.

            * :ref:`SCALE <tbinoperscale>` - Interpolates :ref:`tb` -based material parameters in the linear- or
              natural-log scale.

        par1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBIN.html>`_ for further
            information.

        par2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBIN.html>`_ for further
            information.

        par3 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBIN.html>`_ for further
            information.

        par4 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBIN.html>`_ for further
            information.

        Other Parameters
        ----------------
        **Interpolation Parameters for Oper= ALGO**

        .. _tbinoperalgo:

        * ``Par1`` - Interpolation algorithm:

          * `LINEAR
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/matexampFVinterp.html#ansmatexampl>`_
            - Linear 1D / 2D (default).
          * `LMUL
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/matexampFVinterp.html#exlinmult4>`_
            - Linear-multivariate interpolation (multidimensional).

          ``Par1`` = LINEAR is available for all material models. The remaining options are limited to a
          subset of material models. For more information, see.

        **Interpolation Parameters for Oper= BNDS**

        .. _tbinoperbnds:

        * ``Par1`` - The field variable on which the operation is being applied.

        * ``Par2`` - Lower bound of the field variable.

        * ``Par3`` - Upper bound of the field variable.

        **Interpolation Parameters for Oper= CACH**

        .. _tbinopercach:

        * ``Par1`` - Reserved for future use.

        * ``Par2`` - Enable or disable caching of interpolated material parameters. Enable for better
        performance.

          * OFF - Disable (default).
          * ON - Enable.

        **Interpolation Parameters for Oper= DEFA**

        .. _tbinoperdefa:

        * ``Par1`` - The field variable on which the operation is being applied.

        * ``Par2`` - Default value of the field variable for which an initial value was not specified.

        **Interpolation Parameters for Oper= EXTR**

        .. _tbinoperextr:

        * ``Par1`` - Reserved for future use.

        * ``Par2`` - Set extrapolation/projection options for interpolating material parameters.

          * OFF / BBOX- Projects to the hyper-rectangular bounding box (default). An error occurs if query
            points exist outside the convex hull of points but inside the hyper-rectangular bounding box.
          * PHULL - Projects to the convex hull of points if a point is located outside the convex hull
            surface.

        :ref:`tbin`,EXTR is supported for the `linear multivariate
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/matexampFVinterp.html#exlinmult4>`_
        interpolation algorithm only.

        **Interpolation Parameters for Oper= NORM**

        .. _tbinopernorm:

        * ``Par1`` - Reserved for future use.

        * ``Par2`` - Enable or disables field-variable normalization for interpolation.

          * OFF - Disable.
          * ON - Enable (default).

        **Interpolation Parameters for Oper= SCALE**

        .. _tbinoperscale:

        * ``Par1`` - Independent variable, which can be any field variable specified via the :ref:`tbfield`
          command.

        * ``Par2`` - Index of any material parameter specified via the :ref:`tbdata` command.

        * ``Par3`` - Scale to use for the independent variable. Valid options are LINEAR (linear) or LOG
          (logarithmic).

        * ``Par4`` - Scale to use for the dependent variable (the material parameter specified via ``Par2``
          ). Valid options are LINEAR (linear) or LOG (logarithmic).

        Notes
        -----

        .. _TBIN_notes:

        For a list of the supported material data tables ( :ref:`tb` ), see `Logarithmic Interpolation and
        Scaling <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/mat_loginterpscal.html#>`_

        ``Oper`` = DEFA, BNDS, NORM and CACH are supported for the `linear multivariate
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mat/matexampFVinterp.html#exlinmult4>`_
        ( :ref:`tbin`,ALGO,LMUL) interpolation algorithm only.
        """
        command = f"TBIN,{oper},{par1},{par2},{par3},{par4}"
        return self.run(command, **kwargs)

    def tblist(self, lab: str = "", mat: str = "", **kwargs):
        r"""Lists the material data tables.

        Mechanical APDL Command: `TBLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBLIST.html>`_

        Parameters
        ----------
        lab : str
            Data table label. (See the :ref:`tb` command for valid labels.) Defaults to the active table. If
            ALL, list data for all labels.

        mat : str
            Material number to be listed (defaults to the active material). If ALL, list data tables for all
            materials.

        Notes
        -----

        .. _TBLIST_notes:

        This command is a utility command, valid anywhere.
        """
        command = f"TBLIST,{lab},{mat}"
        return self.run(command, **kwargs)

    def tbmodif(self, row: str = "", col: str = "", value: str = "", **kwargs):
        r"""Modifies data for the material data table (GUI).

        Mechanical APDL Command: `TBMODIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBMODIF.html>`_

        Parameters
        ----------
        row : str
            The row and column numbers of the table entry to be modified.

        col : str
            The row and column numbers of the table entry to be modified.

        value : str
            The new value to be used in the ``ROW``, ``COL`` location.

        Notes
        -----

        .. _TBMODIF_notes:

        The :ref:`tbmodif` command modifies data for the table specified on the last :ref:`tb` command.

        For temperature-dependent data, the command uses the temperature specified via the last
        :ref:`tbtemp` command.

        The command is generated by the program's Graphical User Interface (GUI). It appears in the log file
        ( :file:`Jobname`.LOG) if a :ref:`tb` material data table is graphically edited in spreadsheet
        fashion. The command is not intended to be typed in directly during an analysis session (although it
        can be included in an input file for batch input or for use with :ref:`input` ).

        The command supports the following material data tables ( :ref:`tb`, ``Lab`` values):

        * ANEL - Anisotropic elasticity
        * AVIS - Anisotropic viscosity
        * CFOAM - Crushable foam
        * DLST - Anisotropic dielectric loss tangent
        * DPER - Anisotropic electric permittivity
        * ELST - Anisotropic elastic loss tangent
        * FCON - Fluid conductance data
        * GASKET - Gasket
        * GURSON - Gurson pressure-dependent plasticity
        * HFLM - Film coefficient data
        * HILL - Hill anisotropy
        * JOIN - Joint
        * MIGR - Migration
        * NLISO - Voce isotropic hardening law
        * PIEZ - Piezoelectric matrix
        * PLASTIC ( ``TBOPT`` = BISO) - Bilinear isotropic hardening
        * PLASTIC ( ``TBOPT`` = BKIN) - Bilinear kinematic hardening
        * PRONY - Prony series
        * PZRS - Piezoresistivity
        * SHIFT - Shift function for viscoelastic materials
        * SMA - Shape memory alloy
        * STATE - User-defined state variables

        This command is also valid in SOLUTION.
        """
        command = f"TBMODIF,{row},{col},{value}"
        return self.run(command, **kwargs)

    def tbplot(
        self,
        lab: str = "",
        mat: str = "",
        tbopt: str = "",
        temp: str = "",
        segn: str = "",
        **kwargs,
    ):
        r"""Displays the material data table.

        Mechanical APDL Command: `TBPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBPLOT.html>`_

        Parameters
        ----------
        lab : str
            Data table label. Valid labels are: MELAS, BKIN, BISO, BH, GASKET, and JOIN. Defaults to the
            active table label. For B-H data, also valid are: NB to display NU-B :sup:`2`, MH to display MU
            vs. H, and SBH, SNB, SMH to display the slopes of the corresponding data.

        mat : str
            Material number to be displayed (defaults to the active material).

        tbopt : str
            Gasket material or joint element material option to be plotted.

            The following gasket material options are valid only when ``Lab`` = GASKET:

            * ``ALL`` - Plots all gasket data.

            * ``COMP`` - Plots gasket compression data only.

            * ``LUNL`` - Plots gasket linear unloading data with compression curve.

            * ``NUNL`` - Plots gasket nonlinear unloading data only.

            The following joint element material options are valid only when Lab = JOIN:

            * ``JNSA`` - Plots nonlinear stiffness data that is applicable to all relevant directions.

            * ``JNS, n`` - Plots only the specified nonlinear stiffness data. The n  can be 1, 4, or 6. For
              example, JNS4 plots only the nonlinear stiffness data specified in the local direction 4 (ROTX).

            * ``JNDA`` - Plots nonlinear damping data that is applicable to all relevant directions.

            * ``JND, n`` - Plots only the specified nonlinear damping data. The n  can be 1, 4, or 6. For
              example, JND4 plots only the nonlinear damping data specified in the local direction 4 (ROTX).

            * ``JNFA`` - Plots nonlinear hysteretic friction data that is applicable to all relevant directions.

            * ``JNF, n`` - Plots only the specified nonlinear hysteretic friction data. The n  can be 1, 4, or
              6. For example, JNF4 plots only the nonlinear hysteretic friction data specified in local direction
              4 (ROTX).

        temp : str
            Specific temperature at which gasket data or joint element material data will be plotted (used
            only when ``Lab`` = GASKET or JOIN). Use ``TEMP`` = ALL to plot gasket data or joint element
            material data at all temperatures.

        segn : str
            Segment number of plotted curve (valid only when ``Lab`` = GASKET):

            * ``NO`` - Segment number is not added to plotted curve (default).

            * ``YES`` - Segment number is added to plotted curve. This option is ignored if the number of data
              points in a curve exceeds 20.

        Notes
        -----

        .. _TBPLOT_notes:

        Only data for stress-strain, B-H, gasket curves, or joint element nonlinear material model curves
        can be displayed.

        The ``TBOPT`` and ``TEMP`` values are valid only when Lab = GASKET or JOIN.

        The ``SEGN`` value is valid only when Lab = GASKET.

        This command is valid in any processor.
        """
        command = f"TBPLOT,{lab},{mat},{tbopt},{temp},{segn}"
        return self.run(command, **kwargs)

    def tbpt(
        self,
        oper: str = "",
        x1: str = "",
        x2: str = "",
        x3: str = "",
        xn: str = "",
        **kwargs,
    ):
        r"""Defines a point on a nonlinear data curve.

        Mechanical APDL Command: `TBPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBPT.html>`_

        Parameters
        ----------
        oper : str
            Operation to perform:

            * ``DEFI`` - Defines a new data point (default). The point is inserted into the table in ascending
              order of ``X1``. If a point already exists with the same ``X1`` value, it is replaced.

            * ``DELE`` - Deletes an existing point. The ``X1`` value must match the ``X1`` value of the point to
              be deleted ( ``XN`` is ignored).

        x1 : str
            The N components of the point. N depends on the type of data table. Except for :ref:`tb`,EXPE
            all other :ref:`tb` Tables support only 2 components.

        x2 : str
            The N components of the point. N depends on the type of data table. Except for :ref:`tb`,EXPE
            all other :ref:`tb` Tables support only 2 components.

        x3 : str
            The N components of the point. N depends on the type of data table. Except for :ref:`tb`,EXPE
            all other :ref:`tb` Tables support only 2 components.

        xn : str
            The N components of the point. N depends on the type of data table. Except for :ref:`tb`,EXPE
            all other :ref:`tb` Tables support only 2 components.

        Notes
        -----

        .. _TBPT_notes:

        :ref:`tbpt` defines a point on a nonlinear data curve (such as a stress-strain curve, B-H curve,
        etc.) at the temperature specified on the last :ref:`tbtemp` command. The meaning of the values
        depends on the type of data table specified on the last :ref:`tb` command.

        This command is also valid in SOLUTION.
        """
        command = f"TBPT,{oper},{x1},{x2},{x3},{xn}"
        return self.run(command, **kwargs)

    def tbtemp(self, temp: str = "", kmod: str = "", **kwargs):
        r"""Defines a temperature for a material data table.

        Mechanical APDL Command: `TBTEMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TBTEMP.html>`_

        Parameters
        ----------
        temp : str
            Temperature value (defaults to 0.0 if ``KMOD`` is blank).

        kmod : str
            If blank, ``TEMP`` defines a new temperature. (Issue :ref:`tblist` to list temperatures and
            data.)

        Notes
        -----

        .. _TBTEMP_notes:

        The :ref:`tbtemp` command defines a temperature to be associated with the data on subsequent
        :ref:`tbpt` or :ref:`tbdata` commands.

        The defined temperature remains active until the next :ref:`tbtemp` command is issued.

        Data values must be defined with the temperatures in ascending order.

        This command is also valid in SOLUTION.
        """
        command = f"TBTEMP,{temp},{kmod}"
        return self.run(command, **kwargs)
