"""Inquire undocumented functions"""

class inq_function:

    def ndinqr(node, key):
        """Get information about a node.

        *secondary functions:* set current node pointer to this node.

        Parameters
        ----------
            node     (int,sc,in)       - node number
                                          Should be 0 for key=11, DB_NUMDEFINED,
                                          DB_NUMSELECTED, DB_MAXDEFINED, and
                                          DB_MAXRECLENG
            key      (int,sc,in)       - key as to information needed about
                                         the node.
                     = DB_SELECTED    - return select status:
                         ndinqr  =  0 - node is undefined.
                                 = -1 - node is unselected.
                                 =  1 - node is selected.
                     = DB_NUMDEFINED  - return number of defined nodes
                     = DB_NUMSELECTED - return number of selected nodes
                     = DB_MAXDEFINED  - return highest node number defined
                     = DB_MAXRECLENG  - return maximum record length (dp words)
                     =   2, return length (dp words)
                     =   3,
                     =   4, pointer to first data word
                     =  11, return void percent (integer)
                     =  17, pointer to start of index
                     = 117, return the maximum number of DP contact data stored for any node
                     =  -1,
                     =  -2, superelement flag
                     =  -3, master dof bit pattern
                     =  -4, active dof bit pattern
                     =  -5, solid model attachment
                     =  -6, pack nodal line parametric value
                     =  -7, constraint bit pattern
                     =  -8, force bit pattern
                     =  -9, body force bit pattern
                     = -10, internal node flag
                     = -11, orientation node flag =1 is =0 isnot
                     = -11, contact node flag <0
                     = -12, constraint bit pattern (for DSYM)
                     = -13, if dof constraint written to file.k (for LSDYNA only)
                     = -14, nodal coordinate system number (set by NROTATE)
                     =-101, pointer to node data record
                     =-102, pointer to angle record
                     =-103, 
                     =-104, pointer to attached couplings
                     =-105, pointer to attacted constraint equations
                     =-106, pointer to nodal stresses
                     =-107, pointer to specified disp'S
                     =-108, pointer to specified forces
                     =-109, pointer to x/y/z record
                     =-110,
                     =-111,
                     =-112, pointer to nodal temperatures
                     =-113, pointer to nodal heat generations
                     =-114,
                     =-115, pointer to calculated displacements
                     =-116,

        Returns
        -------
            ndinqr   (int,func,out)   - the returned value of ndinqr is based on 
                                            setting of key.
        """
        pass

    def elmiqr(ielem, key):
        """Get information about an element.

        *secondary functions:* set current element pointer to this element.
        
        Parameters
        ----------
            ielem    (int,sc,in)       - element number
                                         should be zero for key=11, DB_NUMDEFINED,
                                           DB_NUMSELECTED, DB_MAXDEFINED, DB_MAXRECLENG,
                                           or 199
            key      (int,sc,in)       - information flag.
                     = DB_SELECTED    - return select status:                (1)
                          elmiqr = 0 - element is undefined.
                                  =-1 - element is unselected.
                                  = 1 - element is selected.
                     = DB_NUMDEFINED  - return number of defined elements    (12)
                     = DB_NUMSELECTED - return number of selected elements   (13)
                     = DB_MAXDEFINED  - return maximum element number used   (14)
                     = DB_MAXRECLENG  - return maximum record length         (15)
                                         (int words)
                     = 2 - return length (int words)
                     = 3 - return layer number
                           (for cross reference files return number of entities)
                     = 4 - return address of first data word
                     = 5 - return length (in record type units)
                     = 6 - return compressed record number.
                     = 11 - return void percent (integer)
                     = 16 - return location of next record
                            (this increments the next record count)
                     = 17 - pointer to start of index
                     = 18 - return type of file.
                         elmiqr = 0 - integer
                                 = 1 - double precision
                                 = 2 - real
                                 = 3 - complex
                                 = 4 - character*8
                                 = 7 - index
                     = 19 - return virtual type of file.
                         elmiqr = 0 - fixed length (4.4 form)
                                 = 1 - indexed variable length (layer data)
                                 = 2 - xref data tables
                                 = 3 - bitmap data (for 32 data item packed records)
                                 = 4 - data tables (three dimensional arrays)
                     = 111 - return the maximum number of nodes stored for any element
                     = 123 - return the maximum number of DP contact data stored for any element
                     = -1 - material number           ( = -EL_MAT)
                       -2 - element type              ( = -EL_TYPE)
                       -3 - real constant number      ( = -EL_REAL)
                       -4 - element section ID number ( = -EL_SECT)
                       -5 - coordinate system number  ( = -EL_CSYS)
                             (see elmcmx for rest)
                     =-101 - pointer to element integers etc. 
                                (see elmcmx with elmilg and 1 instead of -101)
                                        

        Returns
        -------
            elmiqr  (int,sc,out)  - the returned value of elmiqr is based on 
                                          setting of key.
        """
        pass

    def kpinqr(knmi, key):
        """Get information about a keypoints.

        *secondary functions:* set current keypoints pointer to this
                              keypoints.
        
        Parameters
        ----------
            knmi     (int,sc,in)       - keypoints for inquire. may be 0 for
                                         key=11 thru 15.
            key      (int,sc,in)       - information flag.
                                       = 1 - return select
                                            = -1 - unselected
                                            =  0 - undefined
                                            =  1 - selected
                                       = 2 - return length (data units)
                                       = 3 - return layer number
                                             (for cross reference files return
                                              number of entities)
                                       = 4 - return address of first data word
                                       = 5 - return length (in record type units)
                                       = 6 - return compressed record number.
                                       = 11 - return void percent (integer)
                                       = 12 - return number of defined
                                       = 13 - return number of selected
                                       = 14 - return highest number defined
                                       = 15 - return maximum record length
                                              (data units)
                                       = 16 - return location of next record
                                              (this increments the next
                                               record count)

                                       = 18 - return type of file.
                                            = 0 - integer
                                            = 1 - double precision
                                            = 2 - real
                                            = 3 - complex
                                            = 4 - character*8
                                            = 7 - index
                                       = 19 - return virtual type of file.
                                            = 0 - fixed length (4.4 form)
                                            = 1 - indexed variable length
                                                  (layer data)
                                            = 2 - xref data tables
                                            = 3 - bitmap data (for 32 data
                                                  item packed records)
                                            = 4 - data tables (three
                                                  dimensional arrays)

                                       = -1, material number
                                       = -2, type
                                       = -3, real number
                                       = -4, node number, if meshed
                                       = -5, pointer to attached point
                                       = -6, esys number
                                       = -7, element number, if meshed
                                       = -8, Hardpoint stuff
                                       = -9, area number associated with hardpoint
                                       = -10, line number associated with hardpoint
                                       = -11, Orientation kp flag
                                       = -12, local integer workspace
                                       = -101, pointer to keypoint data
                                       = -102, pointer to keypoint
                                               fluences
                                       = -103, pointer to keypoint
                                               moisture content
                                       = -104, pointer to keypoint
                                               voltage 
                                       = -105, pointer to keypoint
                                               current density
                                       = -106, pointer to keypoint
                                               heat generations
                                       = -107, pointer to keypoint
                                               virtual displacements
                                       = -108, pointer to parameter
                                               data
                                       = -109, pointer to keypoint
                                               temperatures
                                       = -110, pointer to keypoint
                                               displacements
                                       = -111, pointer to keypoint forces
                                       = -112, pointer to line list

        Returns
        -------
            kpinqr   (int,sc,out)    - for key=1   0=knmi is undefined.
                                                    -1=knmi is unselected.
                                                     1=knmi is selected.
                                          for key ne 1 returned data is based
                                          on setting of key.
        """
        pass

    def lsinqr(line, key):
        """
        *primary function:*    get information about a line segment.
        
        Parameters
        ----------
             lnmi     (int,sc,in)       - line segment for inquire. may be 0 for
                                         key=11 thru 15.
             key      (dp,sc,in)        - key as to information needed about
                                         the lnmi.
                                         key=  1, return select
                                         key=  2, return length (data units)
                                         key=  3,
                                         key= 11, return void percent (integer)
                                         key= 12  return number of defined
                                         key= 13, return number of selected
                                         key= 14, return highest number defined
                                         key= 15, return maximum record length
                                                  (data units)
                                         key= 16, return location of next record
                                                  (this increments the next
                                                   record count)
                                         key= 17, return next record from offset
                                         key= -1, material number
                                         key= -2, type
                                         key= -3, real number
                                         key= -4, number of nodes
                                         key= -5, esys number
                                         key= -6, number of elements
                                         key= -7, pointer to line in foreign db
                                         key= -8, # of elem divs in existing mesh
                                         key= -9, keypoint 1
                                         key= -10, keypoint 2
                                         key= -11, color,translucency packed
                                         key= -12, local integer workspace
                                                   (used in delete with sweeps)
                                         key= -13, orientation kpa
                                         key= -14, orientation kpb
                                         key= -15, section id
                                         key= -16, # of elem divs for next mesh
                                         key= -17, 0=hard / 1=soft NDIV
                                         key= -18, 0=hard / 1=soft SPACE
                                         key=-101, pointer to line segment data
                                         key=-102,
                                         key=-103,
                                         key=-104,
                                         key=-105, pointer to node list
                                         key=-106,
                                         key=-107, pointer to element list
                                         key=-108, pointer to parameter data
                                         key=-109,
                                         key=-110, pointer to line convections
                                         key=-111, pointer to line constraints
                                         key=-112,
                                         key=-113,
                                         key=-114, pointer to area list
                                         key=-115, pointer to sub-line list
                                         key=-116, pointer to line pressures

        Returns
        -------
             lsinqr   (int,sc,out)      - for key=1  0=lnmi is undefined.
                                                    -1=lnmi is unselected.
                                                     1=lnmi is selected.
                                          for key ne 1 returned data is based
                                          on setting of key.

        """
        pass

    def arinqr(anmi, key):
        """Get information about a area.

        *secondary functions:* set current area pointer to this
                                  area.
        
        Parameters
        ----------
             anmi     (int,sc,in)      - area for inquire. may be 0 for
                                         key=11 thru 15.
             key      (dp,sc,in)       - key as to information needed about
                                         the anmi.
                                         key=  1, return select
                                         key=  2, return length (data units)
                                         key=  3,
                                         key= 11, return void percent (integer)
                                         key= 12  return number of defined
                                         key= 13, return number of selected
                                         key= 14, return highest number defined
                                         key= 15, return maximum record length
                                                  (data units)
                                         key= 16, return next record
                                                  (this increments the next 
                                                   record count)
                                         key= -1, material
                                         key= -2, type.
                                         key= -3, real.
                                         key= -4, number of nodes.
                                         key= -5,
                                         key= -6, number of elements.
                                         key= -7, pointer to area in foreign db
                                         key= -8, element shape.
                                         key= -9, mid-node element key.
                                         key= -10, element coordinate system.
                                         key= -11, area constraint information.
                                              = 0 - no constraint on this area.
                                              = 1 - symmetry constraint.
                                              = 2 - anti-symmetry
                                              = 3 - both symmetry and anti-symmetry
                                         key= -12, local integer workspace
                                         key= -13,
                                         key= -14,
                                         key= -15, section
                                         key= -16, color and translucency packed.
                                         key= -101, pointer to area data
                                         key= -102,
                                         key= -103,
                                         key= -104,
                                         key= -105, pointer to node list.
                                         key= -106, pointer to parameter data
                                         key= -107, pointer to element list.
                                         key= -108,
                                         key= -109,
                                         key= -110,
                                         key= -111,
                                         key= -112, pointer to line loop list
                                         key= -113, pointer to volume xref
                                         key= -114, pointer to sub-area list
                                         key= -115, pointer to area presaraes
                                         key= -116, pointer to area convections

        Returns
        -------
             arinqr  (int,sc,out)      - for key=1   0=anmi is undefined.
                                                    -1=anmi is unselected.
                                                     1=anmi is selected.
                                         for key ne 1 returned data is based
                                         on setting of key.
        """
        pass

    def vlinqr(vnmi, key):
        """Get information about a volume.

        *secondary functions:* set current volume pointer to this
                              volume.
        
        Parameters
        ----------
            vnmi     (int,sc,in)      - volume for inquire. may be 0 for
                                         key=11 thru 15.
            key      (dp,sc,in)        - key as to information needed about
                                         the vnmi.
                                         key=  1, return select
                                         key=  2, return length (data units)
                                         key=  3,
                                         key= 11, return void percent (integer)
                                         key= 12  return number of defined
                                         key= 13, return number of selected
                                         key= 14, return highest number defined
                                         key= 15, return maximum record length
                                                  (data units)
                                         key= 16, return next record
                                         key= -1, material
                                         key= -2, type.
                                         key= -3, real.
                                         key= -4, number of nodes.
                                         key= -5, KZ1 - 1st kpt for elem Z
                                         key= -6, number of elements.
                                         key= -7, pointer to volume in foreign db
                                         key= -8, element shape.

                                         key= -9, (section id)*10 + 2
                                                  *** fsk qt-58121 5/2007 Rev11 SP1 ***

                                         key= -10, element coordinate system.
                                         key= -11, KZ2 - 2nd kpt for elem Z
                                         key= -12, color and translucancy packed
                                         key= -101, pointer volume data file.
                                         key= -102,
                                         key= -103,
                                         key= -104,
                                         key= -105, pointer to node list.
                                         key= -106, pointer to volume pvolmeter dat
                                         key= -107, pointer to element list.
                                         key= -108,
                                         key= -109,
                                         key= -110, pointer to sub-volume list
                                         key= -111,
                                         key= -112, pointer to area shell list

        Returns
        -------
            vlinqr   (int,sc,out)      - for key=1   0=vnmi is undefined.
                                                    -1=vnmi is unselected.
                                                     1=vnmi is selected.
                                         for key ne 1 returned data is based
                                         on setting of key.
        """
        pass

    def rlinqr(nreal, key):
        """Get information about a real constant set

        typ=int,dp,log,chr,dcp   siz=sc,ar(n),fun     intent=in,out,inout

        Parameters
        ----------
            variable (typ,siz,intent)    description
            nreal   (int,sc,in)       - real constant table number
                                          should be 0 for key=11, DB_NUMDEFINED,
                                          DB_NUMSELECTED, DB_MAXDEFINED, and
                                          DB_MAXRECLENG
            key      (int,sc,in)       - information flag.
                 = 5              - return number of values stored for nreal.
                                    return the REAL set width (number of fields)
                 = DB_SELECTED    - return select status
                          rlinqr = 0 - real constant table is undefined.
                                 =-1 - real constant table is unselected.
                                 = 1 - real constant table is selected
                 = DB_NUMDEFINED  - return number of defined real constant tables
                 = DB_NUMSELECTED - return number of selected real constant tables
                 = DB_MAXDEFINED  - return highest real constant table defined
                 = DB_MAXRECLENG  - return maximum record length (dp words)

        Returns
        -------
            rlinqr   (int,func,out)    - the returned value of rlinqr is based on 
                                          setting of key.
            mpg magnetic interface usage

        """
        pass

    def gapiqr(ngap, key):
        """Get information about a dynamic gap set.

        Parameters
        ----------
            ngap    (int,sc,in)       - gap number for inquire.
                                          (must be zero for now)
            key      (int,sc,in)       - key as to the information needed
                                         key=  1, return select
                                         key=  2, return length (data units)
                                         key=  3,
                                         key= 11, return void percent (integer)
                                         key= 12  return number of defined
                                         key= 13, return number of selected
                                         key= 14, return highest number defined
                                         key= 15, return maximum record length
                                                  (data units)

        Returns
        -------
            gapiqr   (int,sc,out)      - returned data is based
                                         on setting of key.
        """
        pass

    def masiqr(node, key):
        """Get information about masters.
        
        Parameters
        ----------
            variable (typ,siz,intent)    description
            node    (int,sc,in)       - node number for inquire.
                                          (must be zero for now)
            key      (int,sc,in)       - key as to the information needed
                                         key=  1, return select
                                         key=  2, return length (data units)
                                         key=  3,
                                         key= 11, return void percent (integer)
                                         key= 12  return number of defined
                                         key= 13, return number of selected
                                         key= 14, return highest number defined
                                         key= 15, return maximum record length
                                                  (data units)

        Returns
        -------
            variable (typ,siz,intent)    description
            masiqr   (int,sc,out)      - returned data is based
                                    on setting of key.
        """
        pass

    def ceinqr(nce, key):
        """Get information about a constraint equation set

        Parameters
        ----------
        nce         (int,sc,in)       - constraint equation number
        key         (int,sc,in)       - inquiry key:
                                         should be zero for key=11, DB_NUMDEFINED,
                                          DB_NUMSELECTED, DB_MAXDEFINED, and 
                                          DB_MAXRECLENG
                = DB_SELECTED    - return select status
                                       ceinqr = 1 - equation is selected
                                              = 0 - equation is undefined
                                              =-1 - equation is unselected
                = DB_NUMDEFINED  - return number of defined contraint equations
                = DB_NUMSELECTED - return number of selected contraint equations
                = DB_MAXDEFINED  - return number of highest numbered constraint 
                                    equation defined
                = DB_MAXRECLENG  - return length of longest contraint equation set
                                    (max record length)
                =  2             - return length (data units)
                =  3             - return layer number
                =  4             - address of first data word
                =  5             - return number of values stored for nce
                = 11             - return void percent (integer)
                = 16             - return location of next record
                = CE_NONLINEAR   - return 1 if CE is nonlinear
                = CE_ELEMNUMBER  - return associated element number 

        Returns
        -------
            ceinqr   (int,func,out)    - the returned value of ceinqr is based on 
                                           setting of key
        """
        pass

    def cpinqr(ncp, key):
        """Get information about a coupled set

        typ=int,dp,log,chr,dcp   siz=sc,ar(n),fun     intent=in,out,inout

        Parameters
        ----------
        variable  (typ,siz,intent)    description
        ncp       (int,sc,in)     - coupled set number
        key       (int,sc,in)     - inquiry key:
                                      should be zero for key=11, DB_NUMDEFINED,
                                       DB_NUMSELECTED, DB_MAXDEFINED, and 
                                       DB_MAXRECLENG
                    = DB_SELECTED    - return select status
                                cpinqr = 1 - coupled set is selected
                                       = 0 - coupled set in undefined
                                       =-1 - coupled set in unselected
                    = DB_NUMDEFINED  - return number of defined coupled sets
                    = DB_NUMSELECTED - return number of selected coupled sets
                    = DB_MAXDEFINED  - return the number of the highest numbered 
                                        coupled set
                    = DB_MAXRECLENG  - return length of largest coupled set record
                                        (max record length)
                    =  2             - return length (data units)
                    =  3             - return layer number
                    =  4             - return address of first data word
                    =  5             - return number of values stored for ncp
                    = 11             - return void percent (integer)
                    = 16             - return location of next record
                    = -1             - return master node for this eqn (this is
                                       currently only used by solution DB object)

        Returns
        -------
        cpinqr   (int,func,out)    - the returned value of cpinqr is based on 
                                           setting of key

        """
        pass

    def csyiqr(ncsy, key):
        """Get information about a coordinate system

        Parameters
        ----------
        ncsy     (int,sc,in)       - coordinate system reference number
                                       should be zero for key= DB_NUMDEFINED 
                                       or DB_MAXDEFINED
        key      (int,sc,in)       - information flag.
                  = DB_SELECTED    - return status:
                                csyiqr = 0 - coordinate system is not defined
                                        -1 - coordinate system is not selected
                                         1 - coordinate system is selected
                  = DB_NUMDEFINED  - number of defined coordinate systems
                  = DB_MAXDEFINED  - maximum coordinate system reference 
                                     number used.

        Returns
        -------
        csyiqr   (int,func,out)    - the returned value of csyiqr is based on 
                                       setting of key.
        """
        pass

    def etyiqr(itype, key):
        """Get information about an element type.

        Parameters
        ----------
            itype    (int,sc,in)       - element type number
                                          Should be 0 for key=11, DB_NUMDEFINED, 
                                          DB_NUMSELECTED, DB_MAXDEFINED, and 
                                          DB_MAXRECLENG
            key      (int,sc,in)       - information flag.
                     = DB_SELECTED    - return select status:
                          etyiqr = 0 - element type is undefined.
                                 =-1 - element type is unselected.
                                 = 1 - element type is selected.
                     = DB_NUMDEFINED  - return number of defined element types
                     = DB_NUMSELECTED - return number of selected element types
                     = DB_MAXDEFINED  - return highest element type number defined 
                     = DB_MAXRECLENG  - return maximum record length (int words)
                    = -n, return element characteristic n from etycom for element 
                           type itype.
                          n is correlated to the parameter names in echprm.
                          see elccmt for definitions of element characteristics.
                          note- this will not overwrite the current setting of 
                           etycom.

        Returns
        -------
            etyiqr   (int,func,out)    - the returned value of etyiqr is based on 
                                          setting of key.
        """
        pass

    def foriqr(node, key):
        """Get information about nodal loads.
        
        Parameters
        ----------
            node     (int,sc,in)       - number of node being inquired about.  
                                          should be 0 for key=DB_MAXDEFINED or 
                                          DB_NUMDEFINED
            key      (dp,sc,in)        - key as to information needed
                                 = 1              - return force mask for node
                                 = DB_MAXDEFINED,
                                   DB_NUMDEFINED  - return number of nodal loadings
                                                     in model
                                        NOTE: both DB_MAXDEFINED and DB_NUMDEFINED
                                        produce the same functionality

        Returns
        -------
            foriqr   (int,func,out)    - the returned value of foriqr is based on 
                                         setting of key.
        """
        pass

    def sectinqr(nsect, key):
        """
        nsect - section id table number, should be 0 for key = 12, 13, 14
        key - information flag
            = 1, select status
            = 12, return number of defined section id tables
            = 13, return number of selected section id tables
            = 14, return highest section id table defined
        Returns
        -------
        for key = 1
            = 0, section id table is undefined.
            = -1, section id table is unselected.
            = 1, section id table is selected
        """
        pass

    def mpinqr(mat, iprop, key):
        """Get information about a material property.

        Parameters
        ----------
            mat      (int,sc,in)       - material number
                                          should be 0 for key=11,
                                          DB_NUMDEFINED(12),
                                          DB_MAXDEFINED(14), and 
                                          DB_MAXRECLENG(15)

            iprop    (int,sc,in)       - property reference number:
             if iprop = 0, test for existence of any material property with this
                      material number (with key = DB_SELECTED(1))

            ---- MP command labels --------
            EX  = 1, EY  = 2, EZ  = 3, NUXY= 4, NUYZ= 5, NUXZ= 6, GXY = 7, GYZ = 8
            GXZ = 9, ALPX=10, ALPY=11, ALPZ=12, DENS=13, MU  =14, DAMP=15, KXX =16
            KYY =17, KZZ =18, RSVX=19, RSVY=20, RSVZ=21,     =22, HF  =23, VISC=24
            EMIS=25, ENTH=26, LSST=27, PRXY=28, PRYZ=29, PRXZ=30, MURX=31, MURY=32
            MURZ=33, PERX=34, PERY=35, PERZ=36, MGXX=37, MGYY=38, MGZZ=39, EGXX=40
            EGYY=41, EGZZ=42, SBKX=43, SBKY=44, SBKZ=45, SONC=46, DMPS=47, ELIM=48
            USR1=49, USR2=50, USR3=51, USR4=51, FLUI=53, ORTH=54, CABL=55, RIGI=56
            HGLS=57, BVIS=58, QRAT=59, REFT=60, CTEX=61, CTEY=62, CTEZ=63, THSX=64,
            THSY=65, THSZ=66, DMPR=67, LSSM=68, BETD=69, ALPD=70, RH  =71, DXX =72,
            DYY =73, DZZ =74, BETX=75, BETY=76, BETZ=77, CSAT=78, CREF=79, CVH =80,
            UMID=81, UVID=82

                   (see mpinit for uncommented code and for TB command information)

            key      (int,sc,in)       - key as to the information needed
                                         about material property.
                 = DB_SELECTED(1)- return select status:
                            mpinqr = 0 - material prop is undefined.
                                   = 1 - material prop is selected.
                 = DB_NUMDEFINED(12) - number of defined material properties
                 = DB_MAXDEFINED(14) - highest material property number defined
                 = DB_MAXRECLENG(15) - maximum record length (dp words)
                 =  2 - return length (dp words)
                 =  3 - return number of temp. values
                 = 11 - return void percent (integer) 

        Returns
        -------
            mpinqr   (int,func,out)    - returned value of mpinqr is based on 
                                          setting of key.

        """
        pass

    def dget(node, idf, kcmplx):
        """Get a constraint from the data bsae

        Parameters
        ----------
            node     (int,sc,in)       - node number
            idf      (int,sc,in)       - pointer to the dof (1-32)
                                          (see dofcom)
                                         1 =ux,   2 =uy,   3 =uz
                                         4 =rotx, 5 =roty, 6 =rotz
                                         7 =ax,   8 =ay,   9 =az
                                         10=vx,   11=vy,   12=vz
                                         13-18=spares
                                         19=pres, 20=temp, 21=volt
                                         22=mag, 23=enke, 24=ends,
                                         25=emf, 26=curr, 27-32 SP01-SP06
            kcmplx   (int,sc,in)       - 0,real  1,imaginary  2,3- old values

        Returns
        -------
            dget   (dp,sc,out)         - constraint value
                                          (- HUGE if undefined)
        """
        pass

    def fget(node, idf, kcmplx):
        """Get a force from the data bsae

        Parameters
        ----------
            node     (int,sc,in)       - node number
            idf      (int,sc,in)       - pointer to the dof (1-32)
                                          (see dofcom)
                                         1 =ux,   2 =uy,   3 =uz
                                         4 =rotx, 5 =roty, 6 =rotz
                                         7 =ax,   8 =ay,   9 =az
                                         10=vx,   11=vy,   12=vz
                                         13-18=spares
                                         19=pres, 20=temp, 21=volt
                                         22=mag, 23=enke, 24=ends,
                                         25=emf, 26=curr 27-32 spares
            kcmplx   (int,sc,in)       - 0,real  1,imaginary  2,3- old values

        Returns
        -------
            fget   (dp,sc,out)         - force value
                                          (- HUGE if undefined)
        """
        pass

    def erinqr(key):
        """Obtain information from errors common

        Parameters
        ----------
        key      (int,sc,in)       - item to be returned
                                      1=keyerr, 2=errfil,    3=numnot, 4=numwrn,
                                      5=numerr, 6=numfat,    7=maxmsg, 8=lvlerr,
                                      9=mxpcmd, 10=nercmd,  11=nertim,12=nomore,
                                      13=eropen,14=ikserr,  15=kystat,16=mxr4r5,
                                      17=mshkey,            19=opterr,20=flowrn,
                                                22=noreport,23=pdserr,24=mxpcmdw
                                      25=kystop,26=icloads, 27=ifkey,
                                      28=intrupt

            ---- below definitions copied from errcom 7/92 for user information

                                        *** key number= ..........................
                                (see ansysdef for parameter definitions)          |
                                                                                  \/

            keyerr - master error flag                                    (ER_ERRORFLAG)
            errfil - errors file unit number                              (ER_ERRORFILE)
            numnot - total number of notes displayed                      (ER_NUMNOTE)
            numwrn - total number of warnings displayed                   (ER_NUMWARNING)
            numerr - total number of errors displayed                     (ER_NUMERROR)
            numfat - total number of fatals displayed                     (ER_NUMFATAL)
            maxmsg - max allowed number of displayed messages before abort(ER_MAXMESSAGE)
            lvlerr - used basicly in solution (from cnvr command.)        (ER_ERRORLEVEL)
                       -1=do not set keyerr for notes/errors/warnings.
                       -2=same as -1 but do not display message either.
            mxpcmd - maximum number of messages allowed per command       (ER_MAXCOMMAND)
            nercmd - number of messages displayed for any one command     (ER_NUMCOMMAND)
            nertim - key as to how message cleared from u/i pop-up        (ER_UICLEAR)
                      (as per rsg/pft 5/1/92 - only for "info" calls
                       -1=message is timed before removal
                        0=message needs pick or keyboard before removal
                        1=message stays up untill replaced by another message
            nomore   display any more messages                            (ER_NOMOREMSG)
                       0=display messages
                       1=display discontinue message and stop displaying
            eropen - 0=errors file is closed                              (ER_FILEOPEN)
                      1=errors file is opened
            ikserr - 0=if interactive do not set keyerr                   (ER_INTERERROR)
                     - 1=if interactive set keyerr (used by mesher and tessalation)
            kystat - flag to bypass keyopt tests in the elcxx routines    (ER_KEYOPTTEST)
                       associated with status/panel info  inquiries.
                        0=do not bypass keyopt tests
                        1=perform all keyopt tests
                       also flag to bypass setting of _STATUS upon resume
            mxr4r5 - mixed rev4-rev5 input logic (*do,*if,*go,*if-go)     (ER_MIXEDREV)
                        (used in chkmix called from rdmac)
                        1=rev5 found (*do,*fi-then-*endif)
                        2=rev4 found (*go,:xxx,*if,....,:xxx)
                        3=warning printed. do not issue any more.
            mshkey - cpu intensive meshing etc. this will cause           (ER_MESHING)
                       "nertim (11)" to be set to -1 for "notes", 1 for "warnings",
                       and 0 for "errors". checking of this key is done in "anserr".
                        0=not meshing or cpu intensive
                        1=yes, meshing or cpu intensive
            syerro - systop error code. read by anserr if set.            (18)
            opterr - 0=no error in main ansys during opt looping          (ER_OPTLOOPING)
                       1=an error has happened in main ansys during opt looping
            flowrn - flag used by "floqa" as to list floqa.ans            (20)
                       0=list "floqa.ans"
                       1="floqa.ans" has been listed. do not list again.
            noreport- used in GUI for turning off errors due to strsub calls (22)
                       0=process errors as usual
                       1=do NOT report errors
            pdserr - 0=no error in main ansys during pds looping          (ER_PDSLOOPING)
                       1=an error has happened in main ansys during pds looping
            mxpcmdw- number of messages written to file.err for any one   (24)
                      command
                       0=write all errors to file.err
                       1=only write displayed errors to file.err
            icloads - key to forbid the iclist command from listing solution    (26)
                        data instead of the input data.
                       0=iclist is OK
                       1=do not permit iclist
            ifkey   - key on whether or not to abort during /input on error     (27)
                       0=do not abort
                       1=abort
            intrupt - interrupt button, so executable returns no error    (ER_INTERRUPT)

            espare - spare integer variables

                --- end of information from errcom

        Returns
        -------
        erinqr   (int,sc,out)      - value corresponding to key

        mpg erinqr < el117,el115,el126,el109,el53,el96,el97,edg?: get error stat

        """
        pass
    
