class Conn:
    def cat5in(
        self,
        name="",
        extension="",
        path="",
        entity="",
        fmt="",
        nocl="",
        noan="",
        **kwargs,
    ):
        """Transfers a .CATPart file into the ANSYS program.

        APDL Command: ~CAT5IN

        Parameters
        ----------
        name
            The name of a valid .CATPart file, created with CATIA Version 5.0.
            The first character of the file name must be an alphanumeric.

        extension
            The extension for the file. The default extension is .CATPart.

        path
            The path name of the directory in which the file resides enclosed
            in single quotes. The default path name is the current working
            directory.

        entity
            Entity to be imported.

            SOLIDS - Solids only, imported as ANSYS volumes (default).

            SURFACES - Surfaces only, imported as ANSYS areas.

            ALL - All entities. Use this option when the file contains different types of
                  entities.

        fmt
            The format in which ANSYS will store the model.

            0 - Neutral format (default). Defeaturing after import is restricted.

            1 - Solid format; this allows defeaturing after import.

        nocl
            Remove tiny objects.

            0 - Remove tiny objects without checking model validity (default).

            1 - Do not remove tiny objects.

        noan
            Perform an analysis of the model.

            0 - Analyze the model (default).

            1 - Do not analyze the model.

        Notes
        -----
        If defeaturing is specified (FMT = 1), this command must be the last
        line of any file, script, or other interactive input.

        More information on importing CATIA Version 5 parts is available in
        CATIA V5 in the Connection User's Guide.
        """
        command = f"~CAT5IN,{name},{extension},{path},{entity},{fmt},{nocl},{noan}"
        return self.run(command, **kwargs)

    def catiain(self, name="", extension="", path="", blank="", **kwargs):
        """Transfers a CATIA model into the ANSYS program.

        APDL Command: ~CATIAIN

        Parameters
        ----------
        name
            The name of a valid CATIA model, created with CATIA 4.x or
            lower.  The first character of the file name must be an
            alphanumeric.  Special characters such as & - and * and
            spaces are not permitted in the part name.

        extension
            The extension for the file. The default extension is .model.

        path
            The path name of the directory in which the file resides, enclosed
            in single quotes. The default path name is the current working
            directory.

        blank
            Sets whether to import "blanked" entities.

            0 - Does not import "blanked" (suppressed) CATIA entities (default).

            1 - Imports "blanked" entities. The portions of CATIA data
            that were suppressed will be included in the import.

        Notes
        -----
        More information on importing CATIA parts is available in CATIA V4 in
        the Connection User's Guide.
        """
        return self.run(f"~CATIAIN,{name},{extension},{path},,,{blank}", **kwargs)

    def parain(
        self,
        name="",
        extension="",
        path="",
        entity="",
        fmt="",
        scale="",
        **kwargs,
    ):
        """Transfers a Parasolid file into the ANSYS program.

        APDL Command: ~PARAIN

        Parameters
        ----------
        name
            The name of a valid Parasolid file. The first character of the file
            name must be an alphanumeric.

        extension
            The extension for the file. The default extension is .x_t on a PC
            or .xmt_txt on a Linux system. Parasolid files are compatible
            across systems, and do not need to be renamed to be used on another
            platform.

        path
            The path name of the directory in which the file resides, enclosed
            in single quotes. The default path name is the current working
            directory.

        entity
            Entity to be imported:

            SOLIDS - Solids only, imported as ANSYS volumes (default)

            SURFACES - Surfaces only, imported as ANSYS areas.

            WIREFRAME - Wireframe only, imported as ANSYS lines.

            ALL - All entities. Use this option when the file contains
                  more than one type of entity.

        fmt
            Sets the format in which ANSYS will store the model

            0 - Neutral format (default). Defeaturing after import is
                restricted. Use this option if you need to scale a model
                to a specific unit of measure (other than meters).

            1 - Solid format; this allows defeaturing after import.

        scale
            Allows scaling for the model

            0 - Do not rescale the model; retain the default Parasolid
                setting of meters (default).

            1 - Scale the model if warranted by the model size.

        Notes
        -----
        More information on importing Parasolid parts is available in Parasolid
        in the Connection User's Guide.
        """
        command = f"~PARAIN,{name},{extension},{path},{entity},{fmt},{scale}"
        return self.run(command, **kwargs)

    def proein(self, name="", extension="", path="", proecomm="", **kwargs):
        """APDL Command: ~PROEIN

        Transfers a Creo Parametric part into the ANSYS program.

        Parameters
        ----------
        name
            The name of the Creo Parametric part to be imported, which cannot
            exceed 64 characters in length and must begin with an alphanumeric
            character. Special characters such as & - and * and spaces are not
            permitted in the part name.

        extension
            The general Creo Parametric extension format is prt for parts and
            asm for assemblies.

        path
            Full path name to the directory containing the part. The default is
            the current working directory.

        proecomm
            The start command for the version of Creo Parametric you are using.
            proe1 is the default command. Note that the full path name to the
            Creo Parametric command need not be used here if the path had been
            included in the PATH variable. The Creo Parametric command name is
            set by the PROE_START_CMD162 environment variable.

        Notes
        -----
        More information on importing Creo Parametric parts is available in
        Creo Parametric (formerly Pro/ENGINEER) in the Connection User's Guide.
        """
        command = f"~PROEIN,{name},{extension},{path},{proecomm}"
        return self.run(command, **kwargs)

    def satin(
        self,
        name="",
        extension="",
        path="",
        entity="",
        fmt="",
        nocl="",
        noan="",
        **kwargs,
    ):
        """Transfers a .SAT file into the ANSYS program.

        APDL Command: ~SATIN

        Parameters
        ----------
        name
            The name of a valid .SAT file, created with a supported version of
            ACIS. The first character of the file name must be an alphanumeric.
            Special characters such as & - and * and spaces are not permitted
            in the part name. See File Names in the Command Reference for more
            information about ANSYS file naming conventions.

        extension
            The extension for the file. The default extension is .sat.

        path
            The path name of the directory in which the file resides enclosed
            in single quotes. The default path name is the current working
            directory.

        entity
            Entity to be imported.

            SOLIDS - Solids only, imported as ANSYS volumes (Not implemented, imports All).

            SURFACES - Surfaces only, imported as ANSYS areas (Not implemented, imports All).

            WIREFRAME - Wireframe only, imported as ANSYS lines (Not implemented, imports All).

            ALL - All entities. Use this option when the file contains different types of
                  entities.

        fmt
            The format in which ANSYS will store the model.

            0 - Neutral format (default). Defeaturing after import is restricted.

            1 - Solid format; this allows defeaturing after import.

        nocl
            Remove tiny objects.

            0 - Remove tiny objects without checking model validity (default).

            1 - Do not remove tiny objects.

        noan
            Perform an ACIS analysis of the model.

            0 - Analyze the model (default).

            1 - Do not analyze the model.

        Notes
        -----
        More information on importing ACIS parts is available in ACIS in the
        Connection User's Guide.
        """
        command = f"~SATIN,{name},{extension},{path},{entity},{fmt},{nocl},{noan}"
        return self.run(command, **kwargs)

    def ugin(
        self,
        name="",
        extension="",
        path="",
        entity="",
        layer="",
        fmt="",
        **kwargs,
    ):
        """Transfers an NX part into the ANSYS program.

        APDL Command: ~UGIN

        Parameters
        ----------
        name
            The file name of the NX part to be imported, which cannot exceed 64
            characters in length. The path name must begin with an alphanumeric
            character. Special characters such as &, -,  and * are not
            permitted in the part name.

        extension
            The NX part file extension. The default is .prt.

        path
            The full path name to the directory containing the part, enclosed
            in single quotes; for example, '/ug_parts'. The default is the
            current working directory.

        entity
            Entity to be imported.

            0 or Solid - Solids only, imported as ANSYS volumes (the
            default).

            1 or Surface - Surfaces only, imported as ANSYS areas.

            2 or Wireframe - Wireframe only, imported as ANSYS lines.

            3 or All - All entities. Use this option when the part
                       contains entities that may not be attached to each
                       other, such as a solid in one location and a
                       surface in another.

        layer
            The number(s) assigned to the layer(s) to be imported. You can
            import one layer or a range of layers (designated by hyphens).
            Defaults to 1-256 (all layers).

        fmt
            The format in which ANSYS will store the model.

            0 - Neutral format (default). Defeaturing after import is restricted.

            1 - Solid format; this allows defeaturing after import.

        Notes
        -----
        More information on importing NX parts is available in UG/NX in the
        Connection User's Guide.
        """
        command = f"~UGIN,{name},{extension},{path},{entity},{layer},{fmt}"
        return self.run(command, **kwargs)
