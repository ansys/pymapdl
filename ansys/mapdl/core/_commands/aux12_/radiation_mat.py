class RadiationMat:
    def emis(self, mat="", evalu="", **kwargs):
        """Specifies emissivity as a material property for the Radiation Matrix

        APDL Command: EMIS
        method.

        Parameters
        ----------
        mat
            Material number associated with this emissivity (500 maximum).
            Defaults to 1.

        evalu
            Emissivity for this material (0.0 < EVALU   1.0).  Enter a very
            small number for zero.

        Notes
        -----
        Specifies emissivity as a material property for the Radiation Matrix
        method. This material property can then be associated with each
        element.
        """
        command = f"EMIS,{mat},{evalu}"
        return self.run(command, **kwargs)

    def geom(self, k2d="", ndiv="", **kwargs):
        """Defines the geometry specifications for the radiation matrix

        APDL Command: GEOM
        calculation.

        Parameters
        ----------
        k2d
            Dimensionality key:

            0 - 3-D geometry (default)

            1 - 2-D geometry (plane or axisymmetric)

        ndiv
            Number of divisions in an axisymmetric model.  Used only with K2D =
            1.  Defaults to 0 (2-D plane).  The 2-D model is internally
            expanded to a 3-D model based on the number of divisions specified
            (6   NDIV   90).  For example, NDIV of 6 is internally represented
            by six 60° sections.
        """
        command = f"GEOM,{k2d},{ndiv}"
        return self.run(command, **kwargs)

    def mprint(self, key="", **kwargs):
        """Specifies that radiation matrices are to be printed.

        APDL Command: MPRINT

        Parameters
        ----------
        key
            Print key:

            0 - Do not print matrices.

            1 - Print matrices.

        Notes
        -----
        Specifies that the element and node radiation matrices are to be
        printed when the WRITE command is issued.  If KEY = 1, form factor
        information for each element will also be printed.
        """
        command = f"MPRINT,{key}"
        return self.run(command, **kwargs)

    def space(self, node="", **kwargs):
        """Defines a space node for radiation using the Radiation Matrix method.

        APDL Command: SPACE

        Parameters
        ----------
        node
            Node defined to be the space node.

        Notes
        -----
        A space node is required in an open system to account for radiation
        losses.

        If using SPACE with the ANSYS Multi-field solver (MFS),  you must
        capture this command in the command file using MFCMMAND. This step is
        necessary because at the end of each field computation, this command is
        unset.
        """
        command = f"SPACE,{node}"
        return self.run(command, **kwargs)

    def vtype(self, nohid="", nzone="", **kwargs):
        """Specifies the viewing procedure used to determine the form factors for

        APDL Command: VTYPE
        the Radiation Matrix method.

        Parameters
        ----------
        nohid
            Type of viewing procedure:

            0 - Hidden procedure.

            1 - Non-hidden (faster, but less general) procedure.

        nzone
            Number of sampling zones for the hidden procedure (100 maximum for
            3-D, 1000 maximum for 2-D).  Defaults to 20 for 3-D, 200 for 2-D.
            Number of points is ``2*NZONE`` for 2-D and ``2*NZONE*(NZONE+1)`` for 3-D.
        """
        command = f"VTYPE,{nohid},{nzone}"
        return self.run(command, **kwargs)

    def write(self, fname="", **kwargs):
        """Writes the radiation matrix file.

        APDL Command: WRITE

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        Notes
        -----
        Writes radiation matrix file (File.SUB) for input to the substructure
        thermal "use" pass.  Subsequent WRITE operations to the same file
        overwrite the file.
        """
        command = f"WRITE,{fname}"
        return self.run(command, **kwargs)
