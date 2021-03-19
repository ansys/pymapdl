"""Wraps commands for MAPDL meshing

Includes
N
CDWRITE


"""
import re

class _MapdlMeshingCommands():

    def n(self, node="", x="", y="", z="", thxy="", thyz="", thzx="",
          **kwargs) -> int:
        """Define a node.

        APDL Command: N

        Parameters
        ----------
        node
            Node number to be assigned.  A previously defined node of
            the same number will be redefined.  Defaults to the
            maximum node number used +1.

        x, y, z
            Node location in the active coordinate system (R, θ, Z for
            cylindrical, R, θ, Φ for spherical or toroidal).

        thxy
            First rotation about nodal Z (positive X toward Y).

        thyz
            Second rotation about nodal X (positive Y toward Z).

        thzx
            Third rotation about nodal Y (positive Z toward X).

        Returns
        -------
        int
            Node number of the generated node.

        Examples
        --------
        Create a node at ``(0, 1, 1)``

        >>> nnum = mapdl.n("", 0, 1, 1)
        >>> nnum
        1

        Create a node at ``(4, 5, 1)`` with a node ID of 10

        >>> nnum = mapdl.n(10, 4, 5, 1)
        >>> nnum
        10

        Notes
        -----
        Defines a node in the active coordinate system [CSYS].  The
        nodal coordinate system is parallel to the global Cartesian
        system unless rotated.  Rotation angles are in degrees and
        redefine any previous rotation angles.  See the NMODIF, NANG,
        NROTAT, and NORA commands for other rotation options.
        """
        command = f"N,{node},{x},{y},{z},{thxy},{thyz},{thzx}"
        msg = self.run(command, **kwargs)
        if msg:
            res = re.search(r"(NODE\s*)([0-9]+)", msg)
            if res is not None:
                return int(res.group(2))

    def cdwrite(self, option="", fname="", ext="", fnamei="", exti="",
                fmat="", **kwargs):
        """Writes geometry and load database items to a file.

        APDL Command: CDWRITE

        Parameters
        ----------
        option
            Selects which data to write:

            ALL - Write all appropriate geometry, material property,
                  load, and component data (default). Two files will
                  be produced. Fname.Ext will contain all data items
                  mentioned in "Notes", except the solid model
                  data. Fnamei.Exti will contain the solid model
                  geometry and solid model loads data in the form of
                  IGES commands. This option is not valid when
                  CDOPT,ANF is active.

            COMB - Write all data mentioned, but to a single file,
                   Fname.Ext. Solid model geometry data will be
                   written in either IGES or ANF format as specified
                   in the CDOPT command, followed by the remainder of
                   the data in the form of ANSYS commands. More
                   information on these (IGES/ANF) file formats is
                   provided in "Notes".

            DB - Write all database information except the solid model
                 and solid model loads to Fname.Ext in the form of
                 ANSYS commands. This option is not valid when
                 CDOPT,ANF is active.

            SOLID - Write only the solid model geometry and solid
                    model load data. This output will be in IGES or
                    ANF format, as specified in the CDOPT
                    command. More information on these (IGES/ANF) file
                    formats is provided in "Notes".

            GEOM - Write only element and nodal geometry data. Neither
                   solid model geometry nor element attribute data
                   will be written. One file, Fname.Ext, will be
                   produced. Use CDREAD,DB to read in a file written
                   with this option. Element types [ET] compatible
                   with the connectivity of the elements on the file
                   must first be defined before reading the file in
                   with CDREAD,DB.

            CM - Write only node and element component and geometry
            data to Fname.Ext.

            MAT - Write only material property data (both linear and
            nonlinear) to Fname.Ext.

            LOAD - Write only loads for current load step to
            Fname.Ext.

            SECT - Write only section data to Fname.Ext. Pretension
            sections are not included.

        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        fnamei
            Name of the IGES file and its directory path (248
            characters maximum, including directory). If you do not
            specify a directory path, it will default to your working
            directory and you can use all 248 characters for the file
            name.

        exti
            Filename extension (eight-character maximum).

        fmat
            Format of the output file (defaults to BLOCKED).

            BLOCKED - Blocked format. This format allows faster
                      reading of the output file. The time savings is
                      most significant when BLOCKED is used to read
                      .cdb files associated with very large models.

            UNBLOCKED - Unblocked format.

        Returns
        -------
        str
            Mapdl command output.

        Examples
        --------
        Create a basic block and save it to disk.

        >>> mapdl.prep7()
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.et(1, 186)
        >>> mapdl.esize(0.25)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.cdwrite('DB', '/tmp/mesh.cdb')
         TITLE =
         NUMBER OF ELEMENT TYPES =      1
                64 ELEMENTS CURRENTLY SELECTED.  MAX ELEMENT NUMBER =   64
               425 NODES CURRENTLY SELECTED.     MAX NODE NUMBER =     425
                 8 KEYPOINTS CURRENTLY SELECTED. MAX KEYPOINT NUMBER =   8
                12 LINES CURRENTLY SELECTED.     MAX LINE NUMBER =      12
                 6 AREAS CURRENTLY SELECTED.     MAX AREA NUMBER =       6
                 1 VOLUMES CURRENTLY SELECTED.   MAX VOL. NUMBER =       1
         WRITE ANSYS DATABASE AS AN ANSYS INPUT FILE: /tmp/mesh.cdb

        Optionally load the mesh into Python using the archive reader.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> mesh = pymapdl_reader.Archive('/tmp/mesh.cdb')
        >>> mesh
        ANSYS Archive File mesh.cdb
         Number of Nodes:              425
         Number of Elements:           64
         Number of Element Types:      1
         Number of Node Components:    0
         Number of Element Components: 0

        Notes
        -----
        Load data includes the current load step only. Loads applied
        to the solid model (if any) are automatically transferred to
        the finite element model when this command is issued. CDWRITE
        writes out solid model loads for meshed models only. If the
        model is not meshed, the solid model loads cannot be
        saved. Component data include component definitions, but not
        assembly definitions. Appropriate NUMOFF commands are included
        at the beginning of the file; this is to avoid overlap of an
        existing database when the file is read in.

        Element order information (resulting from a WAVES command) is
        not written. The data in the database remain untouched.

        Solution control commands are typically not written to the
        file unless you specifically change a default solution
        setting.

        CDWRITE does not support the GSBDATA and GSGDATA commands, and
        these commands are not written to the file.

        The data may be reread (on a different machine, for example)
        with the CDREAD command. Caution: When the file is read in,
        the NUMOFF,MAT command may cause a mismatch between material
        definitions and material numbers referenced by certain loads
        and element real constants. See NUMOFF for details. Also, be
        aware that the files created by the CDWRITE command explicitly
        set the active coordinate system to Cartesian (CSYS,0).

        You should generally use the blocked format (Fmat = BLOCKED)
        when writing out model data with CDWRITE. This is a compressed
        data format that greatly reduces the time required to read
        large models through the CDREAD command. The blocked and
        unblocked formats are described in Chapter 3 of the Guide to
        Interfacing with ANSYS.

        If you use CDWRITE in any of the derived products (ANSYS Emag,
        ANSYS Professional), then before reading the file, you must
        edit the Jobname.cdb file to remove commands that are not
        available in the respective component product.

        The CDWRITE command writes PART information for any ANSYS
        LS-DYNA input file to the Jobname.cdb file via the EDPREAD
        command. (EDPREAD is not a documented command; it is written
        only when the CDWRITE command is issued.) The PART information
        can be automatically read in via the CDREAD command; however,
        if more than one Jobname.cdb file is read, the PART list from
        the last Jobname.cdb file overwrites the existing PART list of
        the total model. This behavior affects all PART-related
        commands contained in the Jobname.cdb file. You can join
        models, but not PART-related inputs, which you must modify
        using the newly-created PART numbers. In limited cases, an
        update of the PART list (EDWRITE,PUPDATE) is possible; doing
        so requires that no used combination of MAT/TYPE/REAL appears
        more than once in the list.

        The CDWRITE command does not support (for beam meshing) any
        line operation that relies on solid model associativity. For
        example, meshing the areas adjacent to the meshed line,
        plotting the line that contains the orientation nodes, or
        clearing the mesh from the line that contains orientation
        nodes may not work as expected. For more information about
        beam meshing, see Meshing Your Solid Model in the Modeling and
        Meshing Guide.

        IGES and ANF File Formats for Solid Model Geometry Information

        The format used for solid model geometry information is
        determined by the current CDOPT command setting. The default
        format is IGES.

        IGES option (default) to write solid model information (CDOPT,
        IGS):

        Before writing solid model entities, select all corresponding
        lower level entities (ALLSEL,BELOW,ALL).
        """
        command = f"CDWRITE,{option},'{fname}',{ext},,{fnamei},{exti},{fmat}"
        return self.run(command, **kwargs)
