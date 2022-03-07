class Digitizing:
    def dig(self, node1="", node2="", ninc="", **kwargs):
        """Digitizes nodes to a surface.

        APDL Command: DIG

        Parameters
        ----------
        node1, node2, ninc
            Digitize nodes NODE1 through NODE2 in steps of NINC.  NODE2
            defaults to NODE1 and NINC defaults to 1.

        Notes
        -----
        Digitizes nodes to the surface defined by the DSURF command.  The nodes
        indicated must be digitized from the tablet after this command is
        given.  The program must be in the interactive mode and the graphics
        terminal show option [/SHOW] must be active.  The global Cartesian
        coordinates of the nodes are stored.
        """
        command = f"DIG,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def dmove(self, node1="", node2="", ninc="", **kwargs):
        """Digitizes nodes on surfaces and along intersections.

        APDL Command: DMOVE

        Parameters
        ----------
        node1, node2, ninc
            Digitize nodes NODE1through NODE2 in steps of NINC.  NODE2 defaults
            to NODE1 and NINC defaults to 1.

        Notes
        -----
        Digitizes nodes on undefined surfaces, warped surfaces, and along
        intersection lines.  Two orthogonal views showing the nodes on a plane
        in each view are required.  No surfaces need be specified.  Two
        coordinates are determined from the second view and the other
        coordinate is retained from the first view.  Use the DIG command to
        first define nodes in one view (as determined from the DSET command).
        Then reset the view and use this command to move the nodes to the
        proper location.
        """
        command = f"DMOVE,{node1},{node2},{ninc}"
        return self.run(command, **kwargs)

    def dset(self, node1="", node2="", node3="", ddev="", **kwargs):
        """Sets the scale and drawing plane orientation for a digitizing tablet.

        APDL Command: DSET

        Parameters
        ----------
        node1, node2, node3
            Any three (noncolinear) nodes defining a plane parallel to the
            drawing.  Nodes and actual locations (in any coordinate system)
            must have been previously defined.

        ddev
            Digitizing device type number (device dependent).

        Notes
        -----
        Sets drawing scale size and defines the drawing plane orientation for
        use with a digitizing tablet.  Drawings must be to scale.  Views must
        represent standard orthogonal parallel projections.  The three nodes
        indicated must be digitized [DIG] from the tablet after this command is
        issued.
        """
        command = f"DSET,{node1},{node2},{node3},{ddev}"
        return self.run(command, **kwargs)

    def dsurf(self, kcn="", xsurf="", ysurf="", zsurf="", **kwargs):
        """Defines the surface upon which digitized nodes lie.

        APDL Command: DSURF

        Parameters
        ----------
        kcn
            Surface is located in coordinate system KCN.  KCN may be 0,1,2 or
            any previously defined local coordinate system number.

        xsurf, ysurf, zsurf
            Input one value to define the surface constant.  Input 999 in the
            other two fields.  Interpret fields as R, θ, Z for cylindrical or
            R, θ, Φ for spherical or toroidal coordinate systems.  XSURF and
            YSURF default to 999 if KCN = 0.

        Notes
        -----
        Defines the surface upon which the nodes to be digitized (with the DIG
        command) actually lie.  Surfaces are defined by a coordinate system
        number and a coordinate constant [MOVE].  Two coordinates are
        determined from the drawing and converted to surface coordinates.  The
        third coordinate is defined from the input surface constant.  If nodes
        lie on warped or undefined surfaces, use the DMOVE command.
        """
        command = f"DSURF,{kcn},{xsurf},{ysurf},{zsurf}"
        return self.run(command, **kwargs)
