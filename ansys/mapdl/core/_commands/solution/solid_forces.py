class SolidForces:
    def fk(self, kpoi="", lab="", value="", value2="", **kwargs):
        """Defines force loads at keypoints.

        APDL Command: FK

        Parameters
        ----------
        kpoi
            Keypoint at which force is to be specified.  If ALL, apply to all
            selected keypoints [KSEL].  If KPOI = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for KPOI.

        lab
            Valid force label.  Structural labels:  FX, FY, or FZ (forces); MX,
            MY, or MZ (moments).  Thermal labels:  HEAT, HBOT, HE2, HE3, . . .,
            HTOP (heat flow).  Fluid labels:  FLOW (fluid flow).  Electric
            labels:  AMPS (current flow), CHRG (electric charge).  Magnetic
            labels:  FLUX (magnetic flux);  CSGX, CSGY, or CSGZ (magnetic
            current segments). Diffusion labels: RATE (diffusion flow rate).

        value
            Force value or table name reference for specifying tabular boundary
            conditions.  To specify a table, enclose the table name in percent
            signs (%), e.g., FK, KPOI, HEAT,%tabname%).  Use the ``*DIM`` command
            to define a table.

        value2
            Second force value (if any).  If the analysis type and the force
            allow a complex input, VALUE (above) is the real component and
            VALUE2 is the imaginary component.

        Notes
        -----
        Forces may be transferred from keypoints to nodes with the FTRAN or
        SBCTRAN commands.  See the F command for a description of force loads.

        Tabular boundary conditions (VALUE = %tabname%) are available only for
        the following labels: Fluid (FLOW), Electric (AMPS), Structural force
        (FX, FY, FZ, MX, MY, MZ), and Thermal (HEAT, HBOT, HE2, HE3, . . .,
        HTOP).

        This command is also valid in PREP7.
        """
        command = f"FK,{kpoi},{lab},{value},{value2}"
        return self.run(command, **kwargs)

    def fkdele(self, kpoi="", lab="", **kwargs):
        """Deletes force loads at a keypoint.

        APDL Command: FKDELE

        Parameters
        ----------
        kpoi
            Keypoint at which force is to be deleted.  If ALL, delete forces at
            all selected keypoints [KSEL].  If KPOI = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for KPOI.

        lab
            Valid force label.  If ALL, use all appropriate labels.  See the
            FDELE command for labels.

        Notes
        -----
        Deletes force loads (and all corresponding finite element loads) at a
        keypoint.  See the FDELE command for details.

        This command is also valid in PREP7.
        """
        command = f"FKDELE,{kpoi},{lab}"
        return self.run(command, **kwargs)

    def fklist(self, kpoi="", lab="", **kwargs):
        """Lists the forces at keypoints.

        APDL Command: FKLIST

        Parameters
        ----------
        kpoi
            List forces at this keypoint.  If ALL (default), list for all
            selected keypoints [KSEL].  If KPOI = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in
            the GUI).  A component name may also be substituted for KPOI.

        lab
            Force label to be listed (defaults to ALL).  See the DOFSEL command
            for labels.

        Notes
        -----
        Listing applies to the selected keypoints [KSEL] and the selected force
        labels [DOFSEL].

        This command is valid in any processor.
        """
        command = f"FKLIST,{kpoi},{lab}"
        return self.run(command, **kwargs)

    def ftran(self, **kwargs):
        """Transfers solid model forces to the finite element model.

        APDL Command: FTRAN

        Notes
        -----
        Forces are transferred only from selected keypoints to selected nodes.
        The FTRAN operation is also done if the SBCTRAN command is issued or
        automatically done upon initiation of the solution calculations
        [SOLVE].

        This command is also valid in PREP7.
        """
        command = f"FTRAN,"
        return self.run(command, **kwargs)
