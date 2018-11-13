*comdeck,fdresu                                                         jas

c *** Copyright ANSYS.  All Rights Reserved.
c *** ansys, inc

c     **********  description of results file  **********
c     --- used for the following files:
c       .rfl
c       .rmg
c       .rst
c       .rth
c       .lnn(lxx)

      character*8  RSTNM
      parameter   (RSTNM='rst     ')

      LONGINT         resufpL, adrZipL, resuRfpL
      integer         resubk, resuut, resuRbk, resuRut
      common /fdresu/ resufpL, adrZipL, resubk, resuut, 
     x                 resuRfpL, resuRbk, resuRut

c   ********** common variable descriptions ***********
co  resufpL      file position on file resu
co  resubk       block number for file resu  (usually 6)
co  resuut       file unit for file resu     (0 if not open)  FUN12
c0  resuRxx      variables for remote modal RST file
c   See fddesc for documentation of how binary files are stored

c     **********  file format  **********

c        recid tells the identifier for this record.  Not all records will have
c             identifiers -- they are only indicated for those records whose
c             record pointers are stored in a header.

c        type tells what kind of information is stored in this record:
c             i - integer
c             dp - double precision
c             cmp - complex

c        nrec tells how many records of this description are found here

c        lrec tells how long the records are (how many items are stored)

c recid    type    nrec    lrec     contents

c  ---      i       1      100      standard ANSYS file header (see binhed for
c                                   details of header contents)

c  ---      i       1       80      .RST FILE HEADER

c                                    fun12,    maxn,     nnod,   resmax,   numdof,
c                                     maxe,    nelm,      kan,    nsets,   ptrend,  (10)
c                                  ptrDSIl, ptrTIMl,  ptrLSPl,  ptrELMl,  ptrNODl,
c                                   ptrGEO, ptrCYCl,   CMSflg,    csEls,    units,  (20)
c                                  nSector,  csCord,  ptrEnd8,  ptrEnd8,  fsiflag,
c                                    pmeth,  noffst,   eoffst,   nTrans, ptrTRANl,  (30)
c                                  PrecKey,   csNds,   cpxrst,   extopt,   nlgeom,
c                                AvailData,   mmass, kPerturb,  XfemKey,  rstsprs,  (40)
c                                  ptrDSIh, ptrTIMh,  ptrLSPh,  ptrCYCh,  ptrELMh,
c                                  ptrNODh, ptrGEOh, ptrTRANh,  Glbnnod, ptrGNODl,  (50)
c                                 ptrGNODh, qrDmpKy,  MSUPkey,   PSDkey,cycMSUPkey,
c                          XfemCrkPropTech,cycNoDup,decompMth,        0,        0,  (60)
c                                        0,       0,        0,        0,        0,
c                                        0,       0,        0,        0,        0,  (70)
c                                        0,       0,        0,        0,        0,
c                                        0,       0,        0,        0,        0   (80)

c                                  each item in header is described below:

c                                   fun12  - unit number (resu file is 12)
c                                   maxn   - maximum node number of the model
c                                   nnod   - the actual number of nodes used in
c                                            the solution phase
c                                   resmax - the maximum number of data sets
c                                            allowed on the file (defaults to
c                                            10000; minimum allowed is 10)
c                                   numdof - number of DOFs per node
c                                   maxe   - maximum element number of the
c                                            finite element model
c                                   nelm   - number of finite elements
c                                   kan    - analysis type
c                                   nsets  - number of data sets on the file
c                                   ptrend - pointer to the end of the file
c                                             (see ptrEnd8 in 23,24)
c                                ptrDSIl,h - 64 bit pointer to the data steps
c                                            index table
c                                ptrTIMl,h - 64 bit pointer to the table of time
c                                            values for a load step
c                                ptrLSPl,h - 64 bit pointer to the table of load
c                                            step, substep, and cumulative
c                                            iteration numbers
c                                ptrELMl,h - 64 bit pointer to the element equivalence
c                                            table (used when the mesh does not
c                                            change during solution)
c                                ptrNODl,h - 64 bit pointer to the nodal equivalence
c                                            table (used when the mesh does not
c                                            change during solution)
c                                ptrGEOl,h - 64 bit pointer to the beginning of
c                                            geometry information (used when the
c                                            mesh does not change during solution)
c                                ptrCYCl,h - 64 bit pointer to the table of cyc sym
c                                            nodal-diameters at each load step
c                                   CMSflg - CMS results flag: 0-non cms, >0-cms
c                                   csEls  - Cyclic sym # eles in master sector
c                                   units  - unit system used
c                                            = 0 - user defined units
c                                            = 1 - SI
c                                            = 2 - CSG
c                                            = 3 - U.S. Customary, using feet
c                                            = 4 - U.S. Customary, using inches
c                                            = 5 - MKS
c                                            = 6 - MPA
c                                            = 7 - uMKS
c                                  nSector - number of sectors for cyclic sym
c                                  csCord  - Cyclic symmetry coordinate system
c                                  ptrEnd8 - 64 bit file pointer to the end of
c                                            the file (i.e., length of file)
c                                  fsiflag - FSI analyis flag
c                                  pmeth   - p-method analyis flag
c                                  noffst  - node offset used in writing file
c                                  eoffst  - elem offset used in writing file
c                                  nTrans  - number of SE transformation vects
c                               ptrTRANl,h - 64 bit pointer to SE transformation vects
c                                  PrecKey - 0, double precision
c                                            1, single for element results only
c                                            2, single for all data
c                                  csNds   - Cyclic sym # nds in master sector
c                                  cpxrst  - complex results flag (0-no, 1-yes)
c                                  extopt  - mode extraction option
c                                  nlgeom  - NLGEOM key
c                               AvailData  - bits indicating available data any
c                                            where on the file; see resucm.inc
c                                  mmass   - number of missing mass resp. present
c                                 kPerturb - key for Linear Perturbation results
c                                  XfemKey - XFEM flag (set equal to Active_XfenId)
c                                                      (0=Inactive, 1=Active)
c                                  rstsprs - bitmask for suppressed items
c                                  Glbnnod - global number of nodes actually used
c                                            in the solution phase (== nnod unless
c                                            using Distributed Ansys)
c                               ptrGNODl,h - 64 bit pointer to the global nodal
c                                            equivalence table (only used with
c                                            Distributed ANSYS and when the mesh
c                                            does not change during solution)
c                                  qrDmpKy - QR damped calculations key
c                                  MSUPkey - MSUP results expanded with MSUPCombineModes
c                                  PSDkey  - PSD key
c                               cycMSUPkey - rst file format is for subsequent cyclic MSUP
c                                            (only base results on file)
c                          XfemCrkPropTech - XFEM crack propagation technology
c	                                     (0=phantom node-based, 1=singularity-based)
c                                 cycNoDup - no duplicate sector created
c                                decompMth - domain decomposition method employed with DMP
c                                            (> 0 = MESH; -1 = FREQ, -2 = CYCHI)
c
c                                   Note: ptrXXX are relative to beginning of file

c   ---      i       1     numdof   Degrees of freedom per node
c                                   DOF reference numbers are:
c         UX  = 1, UY  = 2, UZ  = 3, ROTX= 4, ROTY= 5, ROTZ= 6, AX  = 7, AY  = 8
c         AZ  = 9, VX  =10, VY  =11, VZ  =12  *** 13-15 are spares *** , WARP=16
c         CONC=17, HDSP=18, PRES=19, TEMP=20, VOLT=21, MAG =22, ENKE=23, ENDS=24
c         EMF =25, CURR=26, SP01=27, SP02=28, SP03=29, SP04=30, SP05=31, SP06=32
c         TBOT=33, TE2 =34, TE3 =35, TE4 =36, TE5 =37, TE6 =38, TE7 =39, TE8 =40
c         TE9 =41, TE10=42, TE11=43, TE12=44, TE13=45, TE14=46, TE15=47, TE16=48
c         TE17=49, TE18=50, TE19=51, TE20=52, TE21=53, TE22=54, TE23=55, TE24=56
c         TE25=57, TE26=58, TE27=59, TE28=60, TE29=61, TE30=62, TE31=63, TTOP=64
c          *** 65-128 are spares ***
c                                    (curdof(i),i=1,numdof)

c   NOD      i       1     nnod     Nodal equivalence table. This table equates
c                                   the number used for storage to the actual
c                                   node number
c                                    (Back(i),i=1,nnod)

c   ELM      i       1     nelm     Element equivalence table. The ANSYS program
c                                   stores all element data in the numerical
c                                   order that the SOLUTION processor solves the
c                                   elements.  This table equates the order
c                                   number used to the actual element number

c   GNOD     i       1    Glbnnod   Global nodal equivalence table. This table
c                                   equates the number used for storage to the
c                                   actual node number. Only written by the
c                                   master process in Distributed Ansys
c                                    (GlbBack(i),i=1,Glbnnod)

c   DSI      i       1    2*resmax  Data sets index table. This record contains
c                                   the record pointers for the beginning of
c                                   each data set. The first resmax records are
c                                   the first 32 bits of the index, the second
c                                   resmax records are the second 32 bits. To
c                                   create the 64 bit pointer, use:
c                                     LONGPTR = largeIntGet (first,second)
c                                   Read the solution data header as follows:
c                                     call bioBasePut (nblk,LONGPTR)
c                                     loc = bioiqr (nblk,12)
c                                     call biord (nblk,loc,...
c                                   The rest of the file reading continues to use
c                                   the ptrXXX's that are in the headers.

c   TIM     dp       1     resmax   Time/freq table. This record contains the
c                                   time (or frequency) values for each data
c                                   set.

c   LSP      i       1    3*resmax  Data set identifiers. This record contains
c                                   the load step, substep, and cumulative
c                                   iteration numbers for each data set.

c   CYC      i       1     resmax   Cyclic symmetry harmonic index

c   TRAN     dp    nTran     25     Substructure transformation vectors

c   GEO      i       1       80     Geometry data header(was 20 in 32 bit vers)

c                                        0,  maxety,   maxrl,    nnod,    nelm,
c                                   maxcsy,  ptrETY,  ptrREL,  ptrLOC,  ptrCSY,  (10)
c                                   ptrEID,  maxsec,  secsiz,  maxmat,  matsiz,
c                                   ptrMAS,  csysiz,  elmsiz,  etysiz,   rlsiz,  (20)
c                                  ptrETYl, ptrETYh, ptrRELl, ptrRELh, ptrCSYl,
c                                  ptrCSYh, ptrLOCl, ptrLOCh, ptrEIDl, ptrEIDh,  (30)
c                                  ptrMASl, ptrMASh, ptrSECl, ptrSECh, ptrMATl,
c                                  ptrMATh, ptrCNTl, ptrCNTh, ptrNODl, ptrNODh,  (40)
c                                  ptrELMl, ptrELMh, Glblenb,ptrGNODl,ptrGNODh,
c                                     maxn,NodesUpd,  lenbac, maxcomp, compsiz,  (50)
c                                 ptrCOMPl,ptrCOMPh,       0,       0,       0,
c                                        0,       0,       0,       0,       0,  (60)
c                                        0,       0,       0,       0,       0,
c                                        0,       0,       0,       0,       0,  (70)
c                                        0,       0,       0,       0,       0,
c                                        0,       0,       0,       0,       0   (80)

c                                  each item in header is described below:

c                                   0      - position not used
c                                   maxety - the maximum element type reference
c                                            number in the model
c                                   maxrl  - the maximum real constant reference
c                                            number in the model
c                                   nnod   - the number of defined nodes in the
c                                            model
c                                   nelm   - the number of defined elements in
c                                            the model
c                                   maxcsy - the maximum coordinate system
c                                            reference number in the model
c                                   ptrETY - pointer to the element type index
c                                            table
c                                   ptrREL - pointer to the real constant
c                                            index table
c                                   ptrLOC - pointer to the nodal point
c                                            locations
c                                   ptrCSY - pointer to the local coordinate
c                                            system index table
c                                   ptrEID - pointer to the element index
c                                            table
c                                   maxsec - the maximum section
c                                            reference number in the model
c                                   secsiz - the maximum size that any
c                                            section record may have
c                                   nummat - the number of materials
c                                            in the model
c                                   matsiz - the maximum size that any material
c                                            property or table may have
c                                   ptrMAS - pointer to the diagonal mass matrix
c                                   csysiz - the number of items describing a
c                                            local coordinate system (usually
c                                            24)
c                                   elmsiz - the maximum number of nodes that a
c                                            defined element may have
c                                   etysiz - the number of items describing an
c                                            element type(=IELCSZ from echprm.inc)
c                                   rlsiz  - the maximum number of items
c                                            defining a real constant (0, if no
c                                            real constants are defined)
c                                ptrETYl,h - 64 bit pointer to element type data
c                                ptrRELl,h - 64 bit pointer to real constant data
c                                ptrCSYl,h - 64 bit pointer to coordinate system data
c                                ptrLOCl,h - 64 bit pointer to nodal locations
c                                ptrEIDl,h - 64 bit pointer to element data
c                                ptrSECl,h - 64 bit pointer to section data
c                                ptrMATl,h - 64 bit pointer to material data
c                                ptrCNTl,h - 64 bit pointer to element centroids
c                                ptrNODl,h - 64 bit pointer to nodal equivalence table
c                                ptrELMl,h - 64 bit pointer to element equivalence table
c                                  Glblenb - global number of nodes actually used
c                                            in the solution phase (== lenbac unless
c                                            using Distributed Ansys)
c                                ptrGNODl,h- 64 bit pointer to the global nodal
c                                            equivalence table (only used with
c                                            Distributed ANSYS and when the mesh
c                                            does not change during solution)
c                                   maxn   - maximum node number of the model
c                                 NodesUpd - 1, node coords have been updated
c                                   lenbac - the actual number of nodes used in
c                                            the solution phase
c                                  maxcomp - the maximum component
c                                            reference number in the model 
c                                  compsiz - the maximum size that any
c                                            component record may have
c                               ptrCOMPl,h - 64 bit pointer to packed component data  
c
c                                   Note: ptrXXX are relative to beginning of file

c   ETY      i       1     maxety   The element types index table. This record
c                                   contains record pointers for each element
c                                   type description. (Relative to ptrETYPL
c                                   for 64 bit version)

c   ---      i     numety  etysiz   Element type description. Each of these
c                                   records is pointed to by a record pointer
c                                   given in the record labeled ETY. See
c                                   routines echprm and elccmt for a complete
c                                   description of the items stored here.

c                                   These items are typically stored into the
c                                   IELC array, and are used to determine the
c                                   element type characteristics at runtime.
c                                   The following items are typically of
c                                   interest:
c                                   * Item 1     - element type reference number
c                                   * Item 2     - element routine number
c                                   * Items 3-14 - element type option keys
c                                                  (keyopts)
c                                   * Item 34    - DOF/node for this element
c                                                  type.  This is a bit mapping
c                                                  of the DOF/node.
c                                   * Item 61    - number of nodes for this
c                                                  element type (nodelm)
c                                   * Item 63    - number of nodes per element
c                                                  having nodal forces, etc.
c                                                  (nodfor)
c                                   * Item 94    - number of nodes per element
c                                                  having nodal stresses, etc.
c                                                  (nodstr).  This number is the
c                                                  number of corner nodes for
c                                                  higher-ordered elements.

c   REL      i       1     maxrl    Real constants index table.  The record
c                                   contains record pointers for each real
c                                   constant set. (Relative to ptrRELL for
c                                   64 bit version)

c   ---     dp     numrl   varies   Element real constant data.  These records
c                                   contain real constant data used for the
c                                   elements.  (See the ANSYS Elements Reference
c                                   manual for values for a specific element.)
c                                   Each of these records is pointed to by a
c                                   record pointer given in the record labeled
c                                   REL. The length of these records varies for
c                                   each element type (actual length is returned
c                                   from routine BINRD8).

c   CSY      i       1     maxcsy   Coordinate systems index table.  This record
c                                   contains the record pointers for each
c                                   coordinate system set. The ANSYS program
c                                   writes coordinate systems only if local
c                                   coordinate systems were defined.  If a local
c                                   system was defined, the predefined global
c                                   systems 1 to 2 also will be written.  The
c                                   global Cartesian system 0 will never be
c                                   written. (Relative to ptrCSYSL for 64
c                                   bit version)

c   ---     dp     numcsy  csysiz   Coordinate system description.  These
c                                   records contain coordinate system data for
c                                   each coordinate system defined.  Each of
c                                   these records is pointed to by a record
c                                   pointer given in the record labeled SYS.

c                                   The items stored in each record:

c                                   * Items 1-9  are the transformation matrix.
c                                   * Items 10-12 are the coordinate system
c                                     origin (XC,YC,ZC).
c                                   * Items 13-14 are the coordinate system
c                                     parameters (PAR1, PAR2).
c                                   * Items 16-18 are the angles used to define
c                                     the coordinate system.
c                                   * Items 19-20 are theta and phi singularity
c                                     keys.
c                                   * Item 21 is the coordinate system type
c                                     (0, 1, 2, or 3).
c                                   * Item 22 is the coordinate system reference
c                                     number.

c   LOC     dp       1     7*nnod   This group contains the node number and
c                                   coordinates (in the order
c                                     Node,X,Y,Z,THXY,THYZ,THZX) for each node.
c                                   (32 bit version)

c   LOC     dp     nnod      7      (64 bit version)
c                                   Node,X,Y,Z,THXY,THYZ,THZX for each node
c                                   Nodes are in node number order

c   EID      i       1     nelm     Element descriptions index table. This
c                                   record contains the record pointers for each
c                                   element description. (LONGINT (2*nelm) for
c                                   64 bit version, relative to ptrEIDL).
c                                   The order of the elements is the same as
c                                   the order in the element equivalence table.

c   ---      i     nelm  10+nodelm  Element descriptions. Each of these records
c                                   is pointed to by a record pointer given in
c                                   the record labeled EID. The length of these
c                                   records varies for each element (actual
c                                   length is returned from routine BINRD8).
c                                   nodelm shown here is the number of nodes for
c                                   this element. Its value is defined in the
c                                   element type description record.

c                                   The items stored in each record:
c                                      mat,  type,  real, secnum, esys,
c                                    death,solidm, shape, elnum,  baseeid,
c                                    nodes

c                                  each item is described below:

c                                    mat    - material reference number
c                                    type   - element type number
c                                    real   - real constant reference number
c                                    secnum - section number
c                                    esys   - element coordinate system
c                                    death  - death flag
c                                             = 0 - alive
c                                             = 1 - dead
c                                    solidm - solid model reference
c                                    shape  - coded shape key
c                                    elnum  - element number
c                                    baseeid- base element number
c				              (applicable to reinforcing elements only)
c                                    nodes  - node numbers defining the element
c                                             (See the ANSYS Elements Reference
c                                             for nodal order of an element)

c   CENT    dp     nelm      6      Centroid record for each element

c   MAS     dp       1  nnod*numdof Diagonal mass matrix

c   SEC      i       1     maxsec   Section index table.  The record
c                                   contains record pointers for each
c                                   section set.

c   ---     dp     numsec  varies   Element section data.  These records
c                                   contain section data used for the
c                                   elements.
c                                   Each of these records is pointed to by a
c                                   record pointer given in the record labeled
c                                   SEC. The length of these records varies for
c                                   each section type (actual length is returned
c                                   from routine BINRD8).

c   MAT      i     1  3+nummat*(158+1)+2
c                                   Total Sz = Header Data + (158+1)*Number of Materials + Tail
c                                   The 1st 3 integers contain the header information
c                                   1) Version number (-101 for differentiation from prev rst data)
c                                   2) Header size which is 3
c                                   3) Size of the index array
c
c                                   Ith material ID is stored at Data(3+((I-1)*(158+1))+1)
c                                     I varies from 1 to nummat
c
c                                   Material record pointers for the material ID at Ith position
c                                     is stored from location
c                                     3+(I-1)*(158+1)+2 to 3+(I-1)*(158+1)+1+158
c                                   The record includes MP pointers followed by TB pointers for a
c                                     single Material ID
c                                   Last 2 data contains the active table number and material ID

c   ---     dp     nummat  varies   Material property data.  These records
c                                   contain material property data used for the
c                                   elements.
c                                   Each of these records is pointed to by a
c                                   record pointer given in the record labeled
c                                   MAT. The length of these records varies for
c                                   each material property type (actual length
c                                   is returned from routine BINRD8).

c   NOD      i       1    lenbac    Nodal equivalence table. This table equates
c                                   the number used for storage to the actual
c                                   node number
c                                    (Back(i),i=1,lenbac)

c   ELM      i       1     nelm     Element equivalence table. The ANSYS program
c                                   stores all element data in the numerical
c                                   order that the SOLUTION processor solves the
c                                   elements.  This table equates the order
c                                   number used to the actual element number

c   GNOD     i       1    Glblenb   Global nodal equivalence table. This table
c                                   equates the number used for storage to the
c                                   actual node number. Only written by the
c                                   master process in Distributed Ansys
c                                    (GlbBack(i),i=1,Glblenb)


c        The solution information is stored starting at this point in the file.
c        The remaining records on the file are repeated as a group nsets times
c        (once for each data set).  Item nsets is defined in the file header.

c        Each set of data is pointed to by a record pointer given in the record
c        labeled DSI.

c   ---      i       1       200     Solution data header. (was 100 in 32 bit)

c                                  pv3num,    nelm,    nnod,    mask,   itime,
c                                    iter,  ncumit,     nrf,  cs_LSC,   nmast,  (10)
c                                  ptrNSL,  ptrESL,   ptrRF,  ptrMST,   ptrBC,
c                                  rxtrap,    mode,    isym,  kcmplx,  numdof,  (20)
c                                    DOFS,    DOFS,    DOFS,    DOFS,    DOFS,
c                                    DOFS,    DOFS,    DOFS,    DOFS,    DOFS,  (30)
c                                    DOFS,    DOFS,    DOFS,    DOFS,    DOFS,
c                                    DOFS,    DOFS,    DOFS,    DOFS,    DOFS,  (40)
c                                    DOFS,    DOFS,    DOFS,    DOFS,    DOFS,
c                                    DOFS,    DOFS,    DOFS,    DOFS,    DOFS,  (50)
c                                   title,   title,   title,   title,   title,
c                                   title,   title,   title,   title,   title,  (60)
c                                   title,   title,   title,   title,   title,
c                                   title,   title,   title,   title,   title,  (70)
c                                  stitle,  stitle,  stitle,  stitle,  stitle,
c                                  stitle,  stitle,  stitle,  stitle,  stitle,  (80)
c                                  stitle,  stitle,  stitle,  stitle,  stitle,
c                                  stitle,  stitle,  stitle,  stitle,  stitle,  (90)
c                                  dbmtim,  dbmdat,  dbfncl,  soltim,  soldat,
c                                  ptrOND,  ptrOEL,  nfldof,  ptrEXA,  ptrEXT,  (100)
c                                 ptrEXAl, ptrEXAh, ptrEXTl, ptrEXTh, ptrNSLl,
c                                 ptrNSLh,  ptrRFl,  ptrRFh, ptrMSTl, ptrMSTh,  (110)
c                                  ptrBCl,  ptrBCh, ptrTRFl, ptrTRFh, ptrONDl,
c                                 ptrONDh, ptrOELl, ptrOELh, ptrESLl, ptrESLh,  (120)
c                                 ptrOSLl, ptrOSLh,sizeDEAD,ptrDEADl,ptrDEADh,
c                                 PrinKey, numvdof, numadof,       0,       0,  (130)
c                                 ptrVSLl, ptrVSLh, ptrASLl, ptrASLh,       0,
c                                       0,       0,       0,numRotCmp,      0,  (140)
c                                 ptrRCMl, ptrRCMh, nNodStr,       0,ptrNDSTRl,
c                               ptrNDSTRh,AvailData, geomID, ptrGEOl, ptrGEOh,  (150)
c                                       0,       0,       0,       0,       0,
c                                       0,       0,       0,       0,       0,  (160)
c                                       0,       0,       0,       0,       0,
c                                       0,       0,       0,       0,       0,  (170)
c                                       0,       0,       0,       0,       0,
c                                       0,       0,       0,       0,       0,  (180)
c                                       0,       0,       0,       0,       0,
c                                       0,       0,       0,       0,       0,  (190)
c                                       0,       0,       0,       0,       0,
c                                       0,       0,       0,       0,       0   (200)

c                                  each item in header is described below:

c                                   pv3num - current solu set number
c                                   nelm   - number of elements
c                                   nnod   - number of nodes
c                                   mask   - bitmask for the existence of
c                                            several records.  If a bit is set
c                                            here, it indicates that the
c                                            corresponding record exists on the
c                                            file.
c                                            The items in the bitmask that
c                                            correspond to each record are shown
c                                            in the record descriptions below.
c                                   itime  - loadstep
c                                   iter   - iteration number
c                                   ncumit - cumulative iteration number
c                                   nrf    - number of reaction forces
c                                   cs_LSC - cyclic symmetry count of the
c                                            load step for this SOLVE
c                                   nmast  - number of masters
c                                   ptrNSL - 32-bit pointer to nodal solution
c                                   ptrESL - 32-bit pointer to element solution
c                                   ptrRF  - 32-bit pointer to reaction forces
c                                   ptrMST - 32-bit pointer to the masters
c                                   ptrBC  - 32-bit pointer to the boundary conditions
c                                   rxtrap - key to extrapolate integration
c                                            point results to nodes
c                                            = 0 - move
c                                            = 1 - extrapolate unless active
c                                                  non-linear
c                                            = 2 - extrapolate always
c                                   mode   - mode number of harmonic loading
c                                            (for cyclic symmetry: this is cs_LSF
c                                            = first load step for this SOLVE)
c                                   isym   - symmetry for harmonic loading
c                                            (for cyclic symmetry: this is cs_LSL
c                                            = last load step for this SOLVE)
c                                   kcmplx - complex key
c                                            = 0 - real
c                                            = 1 - imaginary
c                                   numdof - number of DOFs/nodes for this data
c                                            set
c                                   DOFS   - DOF/node reference numbers (numdof
c                                            values)
c                                   title  - main title (in integer form)
c                                  stitle1 - 1st subtitle (in integer form)
c                                   dbmtim - time (in compact form) when the
c                                            database was last modified
c                                   dbmdat - date (in compact form) when the
c                                            database was last modified
c                                   dbfncl - number of times that the database
c                                            was modified
c                                   soltim - time (in compact form) when the
c                                            solution for this data set was done
c                                   soldat - date (in compact form) when the
c                                            solution for this data set was done
c                                   ptrOND - 32-bit pointer to the ordered node
c                                            list (load case files only)
c                                   ptrOEL - 32-bit pointer to the ordered element
c                                            list (load case files only)
c                                   nfldof - number of extra Flotran DOFs/nodes
c                                            for this data set
c                                   ptrEXA - 32-bit pointer to header extension
c                                            for FLOTRAN DOF/extra DOF list
c                                   ptrEXT - 32-bit pointer to header extension
c                                ptrEXAl,h - 64-bit pointer to header extension
c                                            for FLOTRAN DOF/extra DOF list
c                                ptrEXTl,h - 64-bit pointer to header extension
c                                ptrNSLl,h - 64-bit pointer to nodal solution
c                                ptrRFl,h  - 64-bit pointer to reaction forces
c                                ptrMSTl,h - 64-bit pointer to the masters
c                                ptrBCl,h  - 64-bit pointer to the boundary conditions
c                                ptrTRFl,h - 64-bit pointer to the FLOTRAN
c                                            transient solution vector
c                                ptrONDl,h - 64-bit pointer to the ordered node
c                                            list (load case files only)
c                                ptrOELl,h - 64-bit pointer to the ordered element
c                                            list (load case files only)
c                                ptrESLl,h - 64-bit pointer to element solution
c                                ptrOSLl,h - 64-bit pointer to extra solution vector
c                                            (to be used later for rezoning project)
c                                sizeDEAD  - size of dead element list
c                                ptrDEADl,h- 64-bit pointer to dead element list
c                                  PrinKey - principal stress key:
c                                            0, use rstsprs (if bit 26 set, no prin)
c                                            1, principals are written for this set
c                                           -1, no principals are written for this set
c                                  numvdof - number of velocity dofs
c                                  numadof - number of acceleration dofs
c                                ptrVSLl,h - 64-bit pointer to transient velocity
c                                            solution
c                                ptrASLl,h - 64-bit pointer to transient acceleration
c                                            solution
c                                numRotCmp - number of rotating components
c                                ptrRCMl,h - 64-bit pointer to RCM
c                                  nNodStr - 0, no nodal component stresses
c                                            1, one set (TOP for shells)
c                                            2, two sets (TOP,BOT for shells)
c                                            3, three sets (TOP,BOT,MID)
c                              ptrNDSTRl,h - 64 bit pointer to nodal component str
c                                AvailData - bits indicating available data
c                                            in this data set; see resucm.inc
c                                   geomID - number identifying which geometry (mesh)
c                                            is used for this set of data (when mesh
c                                            does not change during solution this should
c                                            always be equal to 1)
c                                ptrGEOl,h - 64 bit pointer to geometry data (when mesh
c                                            does not change during solution this points
c                                            to first GEO record near start of file)
c                                        0 - position not used
c
c                                   Note: ptrXXX are relative to ptrDSI, except ptrGEO
c                                         which is relative to the beginning of the file

c   ---     dp       1        100   Solution header - double precision data

c                                    timfrq,  lfacto,  lfactn,  cptime,    tref,
c                                     tunif,   tbulk, volbase,   tstep, dsfpinc,  (10)
c                                     accel,   accel,   accel,   omega,   omega,
c                                     omega,   omega,   omega,   omega, omegacg,  (20)
c                                   omegacg, omegacg, omegacg, omegacg, omegacg,
c                                    cgcent,  cgcent,  cgcent, fatjack, fatjack,  (30)
c                                     dval1,   dval2,   dval3, pCnvVal, pCnvVal,
c                                   pCnvVal, pCnvVal, pCnvVal, pCnvVal, pCnvVal,  (40)
c                                   pCnvVal, pCnvVal, pCnvVal, pCnvVal, pCnvVal,
c                                   pCnvVal, pCnvVal, pCnvVal, pCnvVal, pCnvVal,  (50)
c                                    timdat,  timdat,  timdat,  timdat,  timdat,
c                                    timdat,  timdat,  timdat,  timdat,  timdat,  (60)
c                                    timdat,  timdat,  timdat,  timdat,  timdat,
c                                    timdat,  timdat,  timdat,  timdat,  timdat,  (70)
c                                    timdat,  timdat,  timdat,  timdat,  timdat,
c                                    timdat,  timdat,  timdat,  timdat,  timdat,  (80)
c                                    timdat,  timdat,  timdat,  timdat,  timdat,
c                                    timdat,  timdat,  timdat,  timdat,  timdat,  (90)
c                                    timdat,  timdat,  timdat,  timdat,  timdat,
c                                    timdat,  timdat,  timdat,  timdat,  timdat   (100)

c                                  each item is described below:

c                                    timfrq  - time value (or frequency value,
c                                              for a modal or harmonic analysis)
c                                    lfacto  - the "old" load factor (used in
c                                              ramping a load between old and new
c                                              values)
c                                    lfactn  - the "new" load factor
c                                    cptime  - elapsed cpu time (in seconds)
c                                    tref    - the reference temperature
c                                    tunif   - the uniform temperature
c                                    tbulk   - Bulk temp for FLOTRAN film coefs
c                                    VolBase - Initial total volume for VOF
c                                    tstep   - Time Step size for FLOTRAN analysis
c                                    dsfpinc - incident power of diffuse sound field
c                                    accel   - linear acceleration terms
c                                    omega   - angular velocity (first 3 terms) and
c                                              angular acceleration (second 3 terms)
c                                    omegacg - angular velocity (first 3 terms) and
c                                              angular acceleration (second 3 terms)
c                                              these velocity/acceleration terms are
c                                              computed about the center of gravity
c                                    cgcent  - (x,y,z) location of center of gravity
c                                    fatjack - FATJACK ocean wave data (wave height
c                                              and period)
c                                      dval1 - if pmeth=0: FATJACK ocean wave direction
c                                              if pmeth=1: p-method convergence values
c                                      dval2 - if pmeth=0: machine rpm 
c                                              if pmeth=1: p-method convergence values
c                                      dval3 - if pmeth=0: central frequency of tune band
c                                              if pmeth=1: p-method convergence values
c                                    pCnvVal - p-method convergence values
c                                     timdat - if pmeth=0: load data (slot 53 is
c                                              substep convergence key)
c                                              if pmeth=1: p-method convergence values

c   EXA      i       1         64    Header extension (if ptrEXA=ptrEXT, then
c                                                      ptrEXA is unused.)
c                                    positions   1-32  - current extra Flotran
c                                                        DOFs for this set
c                                    positions  33-64  - current extra Flotran
c                                                        DOF labels for this set

c                                    Extra Flotran DOF reference numbers are:
c         DENS= 1, VISC= 2, EVIS= 3, COND= 4, ECON= 5, LMD1= 6, LMD2= 7, LMD3= 8
c         LMD4= 9, LMD5=10, LMD6=11, EMD1=12, EMD2=13, EMD3=14, EMD4=15, EMD5=16
c         EMD6=17, PTOT=18, TTOT=19, PCOE=20, MACH=21, STRM=22, HFLU=23, HFLM=24
c         YPLU=25, TAUW=26, SPHT=27, CMUV=28
c         *************************** 29-32 are spares *************************

c   EXT      i       1        200    Header extension
c                                    positions   1-32  - current DOF for this
c                                                        result set
c                                    positions  33-64  - current DOF labels for
c                                                        this result set
c                                    positions  65-84  - The third title, in
c                                                        integer form
c                                    positions  85-104 - The fourth title, in
c                                                        integer form
c                                    positions 105-124 - The fifth title, in
c                                                        integer form
c                                    position 125 - ptrTRF- pointer to FLOTRAN
c                                                   previous time step DOF vals
c                                    position 126 - trnvar- #dof in FLOTRAN
c                                                   prev time st DOF vals
c                                                   (Note 2 old steps saved,
c                                                   thus #DP is 2*trnvar*nNode)
c                                    position 127 - numvdof, number of velocity
c                                                   items per node (ANSYS
c                                                   transient)
c                                    position 128 - numadof, number of
c                                                   acceleration items per
c                                                   node (ANSYS transient)
c                                    position 131-133 - position of velocity
c                                                       in DOF record
c                                                       (ANSYS transient)
c                                    position 134-136 - position of acceleration
c                                                       in DOF record
c                                                       (ANSYS transient)
c                                    position 137-142 - velocity and
c                                                       acceleration labels
c                                                       (ANSYS transient)
c                                    position 143 - number of stress items
c                                                   (6 or 11); a -11 indicates
c                                                   to use principals directly
c                                                   and not recompute (for PSD)
c                                    position 144-146 - position of rotational
c                                                       velocity in DOF record
c                                                       (ANSYS transient)
c                                    position 147-149 - position of rotational
c                                                       accel. in DOF record
c                                                       (ANSYS transient)
c                                    position 150-155 - rotational velocity and
c                                                       acceleration labels
c                                                       (ANSYS transient)
c                                    position 160 - pointer to CINT results
c                                    position 161 - size of CINT record
c                                    position 162 - Pointer to  XFEM/SMART-crack surface information
c                                    position 163 - size of crk surface records
c                                    if pmeth=1:
c                                       positions 164-200 - p convergence specs

c   GEO     ---      1     varies    Entire geometry record for this set of
c                                    results data.  Note, when the mesh does not
c                                    change during solution, this pointer will
c                                    simply point to the original GEO record
c                                    stored at the start of the file.  When the
c                                    mesh changes the new geoemtry data will be
c                                    stored here.  The geomID can be used to
c                                    determine when the mesh changes.

c * NSL     dp       1  nnod*Sumdof  The DOF solution for each node in the nodal
c                                    coordinate system.  The DOF order is the
c                                    same as shown above in the DOF number
c                                    reference table.  The nodal order is the
c                                    same order given above in the nodal
c                                    equivalence table.  If a DOF for a node
c                                    isn't valid, a value of 2.0**100 is used.
c                                    Note 1: Sumdof = numdof + nfldof.
c                                    Note 2: If, upon reading of this record,
c                                    there is less than nnod*Sumdof items in the
c                                    record, then only a selected set of nodes
c                                    were output. Another record follows
c                                    (integer, less than nnod long) which
c                                    contains the list of nodes for which DOF
c                                    solutions are available.
c                                      (bit 10 (PDBN) in mask)

c   VSL      dp      1 nnod*numvdof  The velocity solution for each node in the
c                                    nodal coordinate system. The description
c                                    for the DOF solution above also applies
c                                    here.
c                                    ANSYS transient. (bit 27 (PDVEL) in mask)

c   ASL      dp      1 nnod*numadof  The acceleration solution for each node in
c                                    the nodal coordinate system. The
c                                    description for the DOF solution above
c                                    also applies here.
c                                    ANSYS transient. (bit 28 (PDACC) in mask)

c   OSL      dp      1  nnod*Sumdof  extra solution vector for element team
c                                    rezoning project.  To be used later.

c   RF     LONG      1       nrf     Reaction force DOFs.  This index is
c                                    calculated as (N-1)*numdof+DOF, where N is
c                                    the position number of the node in the
c                                    nodal equivalence table, and DOF is the DOF
c                                    reference number.
c                                      (bit 11 (PDBR) in mask)

c * ---     dp       1       nrf     Reaction forces.  The force values are
c                                    ordered according to the DOF order shown
c                                    above in the DOF number reference table.
c                                      (bit 11 (PDBR) in mask)

c   MST    LONG      1       nmast   Master DOF list.  This index is calculated
c                                    as (N-1)*numdof+DOF, where N is the
c                                    position number of the node in the nodal
c                                    equivalence table, and DOF is the DOF
c                                    reference number.
c                                      (bit 4 in mask)

c   BC       i       1        40     Boundary condition index table.
c                                      (bit 23 (PDBBC) in mask)
c                                    numdis,ptrDIX,ptrDIS,numfor,ptrFIX,
c                                    ptrFOR,format,     0,     0,     0,
c                                         0,     0,     0,     0,     0,
c                                         0,     0,     0,     0,     0,
c                                         0,     0,     0,     0,     0,
c                                         0,     0,     0,     0,     0,
c                                         0,     0,     0,     0,     0,
c                                         0,     0,     0,     0,     0

c                                  each item is described below:

c                                    numdis - number of nodal constraints
c                                    ptrDIX - pointer to the table of nodes
c                                             having nodal constraints
c                                    ptrDIS - pointer to nodal constraint values
c                                    numfor - number of nodal input force
c                                             loadings
c                                    ptrFIX - pointer to the table of nodes
c                                             having nodal forces
c                                    ptrFOR - pointer to nodal force values
c                                    format - key (0 or 1) denoting which format
c                                             is used for DIX/FIX data (see below)

c                                    positions 7-40 are unused

c   DIX      i       1      numdis   if format == 0 --> Nodal constraint DOF.
c                                    This index is calculated as N*32+DOF,
c                                    where N is the node number and DOF is
c                                    the DOF reference number.  Values are in
c                                    the same order as the DOF number reference
c                                    table.
c
c                                    if format == 1 --> Nodal constraint node
c                                    numbers.

c   ---      i       1      numdis   if format == 0 --> does not exist.
c
c                                    if format == 1 --> Nodal constraint DOF.
c                                    Values are in the same order as the DOF
c                                    number reference table.

c   DIS     dp       1    4*numdis   Nodal constraints.  This record contains
c                                    present and previous values (real and
c                                    imaginary) of the nodal constraints at each
c                                    DOF.

c   FIX      i       1      numfor   if format == 0 --> Nodal input force DOFs.
c                                    This index is calculated as N*32+DOF,
c                                    where N is the node number and DOF is
c                                    the DOF reference number.  Values are in
c                                    the same order as the DOF number reference
c                                    table.
c
c                                    if format == 1 --> Nodal input force node
c                                    numbers.

c   ---      i       1      numfor   if format == 0 --> does not exist.
c
c                                    if format == 1 --> Nodal input force DOF.
c                                    Values are in the same order as the DOF
c                                    number reference table.

c   FOR     dp       1    4*numfor   Nodal forces.  This record contains present
c                                    and previous values (real and imaginary) of
c                                    the nodal input force loadings at each DOF.

c   TRF     dp       1    28*nnod    Two displacement result sets for transient
c                                    solution in FLOTRAN
c                                      (bit 24 (PDTRFL) in mask)

c   OND      i       1       nnod    Ordered node list.  This record exists for
c                                    a load case file only.

c   OEL      i       1       nelm    Ordered element list.  This record exists
c                                    for a load case file only.

c   DED      i       1   sizeDead    List of dead elements (EKILL). Uses the
c                                    compressed CMBLOCK format

c   ESL      i       1     2*nelm    Element solutions index table.  This record
c                                    contains pointers to each element solution.
c                                    The order of the elements is the same as
c                                    the order in the element equivalence table.
c                                      (bit 12 (PDBE) in mask)
c                                    (was nelm long in 32 bit version)

c   RCM     dp       1  6*numRotCmp  Angular velocities (3) and angular
c                                    accelerations (3) of components.

c   DMI     dp       1  3+nContours  Crack ID, Contour ID, TipNode, J Integral
c                                    values

c        The solution information for each individual element is stored starting
c        at this point in the file.  The next 25 records on the file are
c        repeated as a group nelm times (once for each element).  Item nelm is
c        defined in the file header.

c   ---      i       1       25      Individual element index table.

c                                    ptrEMS,ptrENF,ptrENS,ptrENG,ptrEGR,
c                                    ptrEEL,ptrEPL,ptrECR,ptrETH,ptrEUL,
c                                    ptrEFX,ptrELF,ptrEMN,ptrECD,ptrENL,
c                                    ptrEHC,ptrEPT,ptrESF,ptrEDI,ptrETB,
c                                    ptrECT,ptrEXY,ptrEBA,ptrESV,ptrMNL
c                                   (Relative to ptrESL for 64 bit version)

c                                  each item is described below:

c                                    ptrEMS - pointer to misc. data
c                                    ptrENF - pointer to nodal forces
c                                    ptrENS - pointer to nodal stresses
c                                    ptrENG - pointer to volume and energies
c                                    ptrEGR - pointer to nodal gradients
c                                    ptrEEL - pointer to elastic strains
c                                    ptrEPL - pointer to plastic strains
c                                    ptrECR - pointer to creep strains
c                                    ptrETH - pointer to thermal strains
c                                    ptrEUL - pointer to euler angles
c                                    ptrEFX - pointer to nodal fluxes
c                                    ptrELF - pointer to local forces
c                                    ptrEMN - pointer to misc. non-sum values
c                                    ptrECD - pointer to element current
c                                             densities
c                                    ptrENL - pointer to nodal nonlinear data
c                                    ptrEHC - pointer to calculated heat
c                                             generations
c                                    ptrEPT - pointer to element temperatures
c                                    ptrESF - pointer to element surface
c                                             stresses
c                                    ptrEDI - pointer to diffusion strains
c                                    ptrETB - pointer to ETABLE items(post1 only
c                                    ptrECT - pointer to contact data
c                                    ptrEXY - pointer to integration point
c                                             locations
c                                    ptrEBA - pointer to back stresses
c                                    ptrESV - pointer to state variables
c                                    ptrMNL - pointer to material nonlinear record

c                                    Note! If ptrXXX is negative, then all
c                                    |ptrXXX| items are zero and are not on
c                                    the file.

c   EMS     dp       1    varies     Element summable miscellaneous data.  The
c                                    contents and number of data items is
c                                    element-dependent.  For a list of what's
c                                    available, see the SMISC item in the
c                                    description of the ETABLE command in the
c                                    ANSYS Commands Reference.

c   ENF     dp       1    varies     Element nodal forces.  This record contains
c                                    the forces at each node, in the same DOF
c                                    order as the DOF number reference table.
c                                    For static, damping, and inertia forces, a
c                                    set of forces will be repeated (as
c                                    appropriate).  Number of data items stored
c                                    in this record can be calculated as
c                                    follows: nodfor*NDOF*M, where NDOF is the
c                                    number of DOFs/node for this element,
c                                    nodfor is the number of nodes per element
c                                    having nodal forces (defined in element
c                                    type description record), and M may be 1,
c                                    2, or 3.  For a static analysis, M=1 only.
c                                    For a transient analysis, M can be 1, 2,
c                                    or 3.

c   ENS     dp       1    varies     Element nodal component stresses.  This
c                                    record contains the stresses at each corner
c                                    node, in the order SX,SY,SZ,SXY,SYZ,SXZ.
c                                    Nodal order corresponds to the connectivity
c                                    defined in the element description.
c                                    Stresses can be nodal values extrapolated
c                                    from the integration points or values at
c                                    the integration points moved to the nodes.
c                                    If an element is nonlinear, integration
c                                    point values always will be written.  (See
c                                    item rxtrap in the solution header for the
c                                    setting.)  An element is considered
c                                    nonlinear when either plastic, creep, or
c                                    swelling strains are present.
c
c                                    Definition of common terms referred here
c                                    and in subsequent EEL, EPL, ECR, ETH,
c                                    ENL, EUL EPT, and EDI sections:
c
c                                    nodstr - number of nodes per element
c                                             having stresses, strains, etc.
c                                             For higher-order elements, nodstr
c                                             equals to the number of corner
c                                             nodes (e.g., for 20-noded SOLID186,
c                                             nodstr = 8).
c                                    nodfor - number of nodes per element
c                                             having nodal forces, etc.
c                                    ncomp  - number of solution items per node
c                                             ncomp =   6 for ENS record
c                                                       7 for EEL record
c                                                       7 for EPL record
c                                                       7 for ECR record
c                                                       8 for ETH record
c                                                      10 for ENL record
c                                                       7 for EDI record
c                                    NL     - number of layers in layered
c                                             elements
c
c                                    Note: For result sets with NoPrin=0,
c                                    the ENS record will have ncomp=11 and include
c                                    the principal stresses S1,S2,S3,SI,SIGE.
c
c                                    * For solid elements or layered solid elements
c                                      with KEYOPT(8)=0, the record contains
c                                      stresses at each corner node, and
c                                      the number of items in this record is
c                                      nodstr*ncomp.
c                                    * For shell elements or layered shell elements
c                                      with KEYOPT(8)=0, the record contains
c                                      stresses at each corner node (first
c                                      at the bottom shell surface, then the top
c                                      surface), and the number of items in this
c                                      record is 2*nodstr*ncomp.
c                                    * For layered elements SHELL91, SHELL99,
c                                      SOLID46, and SOLID191 with KEYOPT(8) = 0,
c                                      if failure criteria were used, the record
c                                      contains additional stresses at each corner
c                                      nodes (first the bottom surface, then the
c                                      top surface) of the layer with the largest
c                                      failure criteria. Therefore, the total number
c                                      of items is 4*nodstr*ncomp for SHELL91 and
c                                      SHELL99, and 2*nodstr*ncomp for SOLID46 and
c                                      SOLID191.
c                                    * For layered elements (with KEYOPT(8)=1),
c                                      stresses for each layer are at each
c                                      corner node (first at the bottom surface, then
c                                      at the top surface), and the number of
c                                      items in this record is NL*2*nodstr*ncomp for
c                                      layered shells and NL*nodstr*ncomp for
c                                      layered solid elements.
c                                    * For layered shell elements with KEYOPT(8)=2,
c                                      the record contains stresses for each layer
c                                      at each corner node  (first at the bottom
c                                      surface, then the top, and finally the middle
c                                      surface). Therefore, the number of items
c                                      in this record is NL*3*nodstr*ncomp.
c                                    * For layered membrane elements (SHELL181,
c                                      SHELL281, SHELL208, and SHELL209 with
c                                      KEYOPT(1)=1 and KEYOPT(8)=1), the record
c                                      contains stresses for each layer at each
c                                      corner node, and the number of items in
c                                      this record  is NL*nodstr*ncomp.
c                                    * For beam elements, the contents and number
c                                      of data items is element-dependent.  See
c                                      the Output Data section for the particular
c                                      element in the ANSYS Elements Reference.
c
c   ENG     dp       1      11       Element volume and energies.

c                                    volume,senergy,aenergy,kenergy,coenergy,
c                                    incenergy,0.0,0.0,thenergy,0.0,0.0

c                                  each item is described below:

c                                    volume   - element volume
c                                    senergy  - element energy associated with
c                                               the stiffness matrix
c                                    aenergy  - artificial hourglass energy
c                                    kenergy  - kinetic energy
c                                    coenergy - co-energy (magnetics)
c                                    incenergy- incremental energy (magnetics)
c                                    0.0      - position not used
c                                    0.0      - position not used
c                                    thenergy - thermal dissipation energy
c                                              (see ThermMat, shell131/132 only)
c                                    0.0      - position not used
c                                    0.0      - position not used

c   EGR     dp       1    varies     Element nodal field gradients.  This record
c                                    contains the gradients at each corner node
c                                    in the order X,Y,Z.  Nodal order
c                                    corresponds to the connectivity defined in
c                                    the element description.  If this is a
c                                    coupled-field analysis, the data is stored
c                                    in the following order (as available):
c                                    fluid, thermal (TEMP), electric (VOLT),
c                                    magnetic (AZ), and diffusion (CONC).
c                                    Gradients can be nodal values extrapolated
c                                    from the integration points or values at the
c                                    integration points moved to the nodes.  See
c                                    item rxtrap in the solution header for the
c                                    setting.  The number of items in this record
c                                    is nodstr*3*N, where N can be 1, 2, 3, or 4
c                                    (depending on the coupled-field
c                                    conditions).

c                                    NOTE: nodstr is defined in the element type
c                                    description record.

c   EEL     dp       1    varies     Element nodal component elastic strains.
c                                    This record contains strains in the order
c                                    X,Y,Z,XY,YZ,XZ,EQV. Elastic strains can be
c                                    can be nodal values extrapolated from the
c                                    integration points or values at the
c                                    integration points moved to the nodes.  If
c                                    an element is nonlinear, integration point
c                                    values always will be written.  See item
c                                    rxtrap in the solution header for the
c                                    setting.  An element is considered
c                                    nonlinear when either plastic, creep, or
c                                    swelling strains are present.  For beam
c                                    elements, see item LEPEL in the description
c                                    in the Output Data section for the
c                                    particular element in the ANSYS Elements
c                                    Reference.
c
c                                    NOTE: See ENS record section for more details
c                                    on record content and length.
c

c   EPL     dp       1    varies     Element nodal component plastic strains.
c                                    This record contains strains in the order
c                                    X,Y,Z,XY,YZ,XZ,EQV.
c                                    Plastic strains are always values at the
c                                    integration points moved to the nodes.  For
c                                    beam elements, see item LEPPL in the
c                                    Output Data section for the particular
c                                    element in the ANSYS Elements Reference.
c
c                                    NOTE: See ENS record section for more details
c                                    on record content and length.
c

c   ECR     dp       1    varies     Element nodal component creep strains.
c                                    This record contains strains in the order
c                                    X,Y,Z,XY,YZ,XZ,EQV.
c                                    Creep strains are always values at the
c                                    integration points moved to the nodes.  For
c                                    beam elements, see item LEPCR in the
c                                    Output Data section for the particular
c                                    element in the ANSYS Elements Reference.
c
c                                    NOTE: See ENS record section for more details
c                                    on record content and length.
c

c   ETH     dp       1    varies     Element nodal component thermal strains.
c                                    This record contains strains in the order
c                                    X,Y,Z,XY,YZ,XZ,EQV plus the element
c                                    swelling strain. Thermal
c                                    strains can be nodal values extrapolated
c                                    from the integration points or values at
c                                    the integration points moved to the nodes.
c                                    If the element in nonlinear, integration
c                                    point data always will be written. (An
c                                    element is considered nonlinear when either
c                                    plastic, creep, or swelling strains are
c                                    present.) See item rxtrap in the solution
c                                    header for the setting.  For beam elements,
c                                    see item LEPTH in the description of the
c                                    Output Data section for the particular
c                                    element in the ANSYS Elements Reference.
c
c                                    NOTE: See ENS record section for more details
c                                    on record content and length.
c

c   EUL     dp       1    varies     Element Euler angles.  This record contains
c                                    the Euler angles (THXY,THYZ,THZX). (No
c                                    attempt is made to make this information
c                                    complete for all cases of all element
c                                    types.  Programmers need to verify their
c                                    situations.)
c
c                                    ** FOR OLDER ELEMENTS **
c                                    --For lower-order elements
c                                      (e.g. PLANE42 and SOLID45), angles are
c                                      at the centroid and the number of items
c                                      in this record is 3.
c                                    --For higher-order elements (e.g.
c                                      PLANE82, SOLID92, and SOLID95), angles
c                                      are at each corner node and the number of
c                                      items in this record is nodstr*3.
c                                      The above two categories are output if
c                                      ESYS is used, a material KEYOPT is used
c                                      (e.g. KEYOPT(1) for PLANE42), or if it is
c                                      from a large deflection superelement
c                                      stress pass
c
c                                    ** FOR NEW GENERATION SHELL ELEMENTS **
c                                    --For SHELL181/SHELL281:
c                                       For real constant input: the number of
c                                         items in this record is 12.
c                                       For section input:
c                                        IF KEYOPT(8) > 0:
c                                         the number of items in this record is
c                                                         12 + number of layers
c                                        IF KEYOPT(8) = 0:
c                                          IF regular shell  (KEYOPT(1) = 0)
c                                             the number of items in this record
c                                              is 14
c                                          IF membrane shell (KEYOPT(1) = 1):
c                                            IF number of layers = 1, the number
c                                              of items in this record is 13
c                                            IF number of layers > 1, the number
c                                              of items in this record is 14
c
c                                    ** FOR THE NEW GENERATION SOLID ELEMENTS **
c                                    --For uniform reduced integration lower-order 
c                                      elements (e.g. PLANE182, KEYOPT(1)=1 and
c                                      SOLID185 KEYOPT(2)=1):
c                                      the angles are at the centroid and the number
c                                      of items is 3.
c                                    --For other formulations of lower-order 
c                                      elements (e.g. PLANE182 and SOLID185) and
c                                      the higher-order elements
c                                      (e.g. PLANE183, SOLID186, and SOLID187):
c                                      The number of items in this record is
c                                      (nodstr*3).
c                                    --For layered solid elements, add NL values,
c                                      so that the number of items in this record 
c                                      is (nodstr*3)+NL.
c
c                                    NOTE: See ENS record section for definition of
c                                          terms NL and nodstr.

c   EFX     dp       1    varies     Element nodal field fluxes.  This record
c                                    contains the fluxes at each corner node in
c                                    the order X,Y,Z. If this is a
c                                    coupled-field analysis, the flux data is
c                                    stored in the following order:  thermal,
c                                    electric, magnetic.  Nodal order
c                                    corresponds to the connectivity defined in
c                                    the element description.  Fluxes can be
c                                    nodal values extrapolated from the
c                                    integration points or values at the
c                                    integration points moved to the nodes.
c                                    See item rxtrap in the solution header for
c                                    the setting.  The number of items in this
c                                    record is nodstr*3*N, where N can be 1, 2,
c                                    or 3 depending on the coupled-field
c                                    conditions.

c                                    NOTE: nodstr is defined in the element type
c                                    description record.

c * ELF     dp       1    varies     Element nodal coupled-field forces.  This
c                                    record lists the forces at each node in the
c                                    order X,Y,Z.  For most elements, the number
c                                    of items in this record is nodfor*3.
c                                    However, for the PLANE53 element, the
c                                    number of items in this record is either
c                                    nodfor*3 or nodstr*3.  (See the description
c                                    of KEYOPT(7) for PLANE53 in the ANSYS
c                                    Elements Reference.)  NOTE: nodfor and
c                                    nodstr are defined in the element type
c                                    description record.

c                                    NOTE: nodstr is defined in the element type
c                                    description record.

c   EMN     dp       1    varies     Element nonsummable miscellaneous data.
c                                    The contents and number data items for this
c                                    record is element-dependent.   See the
c                                    description for item NMISC of the ETABLE
c                                    command in the ANSYS Commands Reference.

c * ECD     dp       1       3       Element current densities.  This record
c                                    contains the calculated current densities
c                                    in the order X,Y,Z.

c   ENL     dp       1    varies     Element nodal nonlinear data.  This record
c                                    stores nonlinear data at each corner node
c                                    in the order SEPL, SRAT, HPRES, EPEQ,
c                                    PSV or CREQ, PLWK, CRWK, and ELENG
c                                    followed by 2 spares.

c                                  each item is described below:
c                                    SEPL  - equivalent stress parameter
c                                    SRAT  - stress ratio
c                                    HPRES - hydrostatic pressure
c                                    EPEQ  - accumulated equivalent plastic
c                                            strain
c                                    PSV   - plastic state variable
c                                    CREQ  - accumulated equivalent creep
c                                            strain.  Applies to current
c                                            technology element types
c                                            180,181,182,183,185,186,
c                                            187,188,189,208,209,265,
c                                            281,288,289,290
c                                    PLWK  - plastic strain energy density(work)
c                                    CRWK  - creep strain energy density (work)
c                                    ELENG - elestic strain energy density

c                                    * See ENS record section for details on
c                                      solid and shell elements.
c                                    * For beam elements, the contents and
c                                      number of data items in this record is
c                                      element-dependent.  See the description
c                                      of item NLIN in the Output Data section
c                                      for the particular element in the ANSYS
c                                      Elements Reference.

c * EHC     dp       1       1       Element heat generation.  This record
c                                    stores the calculated heat generation.

c   EPT     dp       1    varies     Element structural nodal temperatures.

c                                    * For solid elements and SHELL41, the
c                                      record contains nodal temperatures at
c                                      each node and the number of items in this
c                                      record is nodfor.
c                                    * For shell elements, except SHELL41 and
c                                      SHELL91, the record contains nodal
c                                      temperatures at each corner node for the
c                                      top surface and the bottom surface.  The
c                                      number of items in this record is
c                                      nodstr*2.
c                                    * For SHELL91 and SOLID191, the record
c                                      contains nodal temperatures at each
c                                      corner node for the bottom of the bottom
c                                      layer, and each succeeding interlayer
c                                      surface up to the top of the top layer.
c                                      The number of items in this record is
c                                      (NL+1)*nodstr.
c                                    * For layered shell elements SHELL181,
c                                      SHELL281, SHELL208, SHELL209, and layered
c                                      solid elements SOLID185, SOLID186,
c                                      and SOLSH190, the record contains
c                                      temperatures for each layer at each
c                                      corner node (first at the bottom layer
c                                      surface, then the top). Therefore, the number
c                                      of items in this record is NL*2*nodstr for
c                                      layered shells and NL*nodstr for layered
c                                      solid elements.
c                                    * For layered membrane elements (SHELL181,
c                                      SHELL281, SHELL208, and SHELL209 with
c                                      KEYOPT(1)=1), the record contains
c                                      temperatures for each layer at each
c                                      corner node. Therefore, the number of items
c                                      in this record is NL*nodstr.
c                                    * For beam elements, the contents and
c                                      number of data items in this record is
c                                      element-dependent.  See the description
c                                      of item LBFE in the Output Data section
c                                      for the particular element in the ANSYS
c                                      Elements Reference.

c                                    NOTE: See ENS record section for definition
c                                          of terms NL, nodstr, and nodfor.

c   ECT     dp       1    varies     Contact element results.  This record
c                                    stores contact results at each corner node
c                                    in the order STAT, PENE, PRES, SFRIC, STOT,
c                                    SLIDE, GAP, FLUX, CNOS, FPRS
c                                  each item is described below:
c                                    STAT  - Contact status
c                                    PENE  - Contact penetration
c                                    PRES  - Contact pressure
c                                    SFRIC - Contact friction stress
c                                    STOT  - Contact total stress (pressure plus friction)
c                                    SLIDE - Contact sliding distance
c                                    GAP   - Contact gap distance
c                                    FLUX  - Total heat flux at contact surface
c                                    CNOS  - Total number of contact status changes during substep
c                                    FPRS  - Actual applied fluid penetration pressure

c   ESF     dp       1    nsurf*19   Element surface stresses.  The
c                                    length of this record is nsurf*19 where
c                                    nsurf is the number of surfaces that have
c                                    surface stress information.  The stress
c                                    information is simply repeated in the
c                                    format shown below for each surface.

c                                    * For 2d elements:

c                                    facenm,  area,  temp, press, eppar,
c                                     epper,   epz, 0.0d0,  spar,  sper,
c                                        sz, 0.0d0, 0.0d0, 0.0d0,    s1,
c                                        s2,    s3,  sint,  seqv

c                                    * For 3d elements:

c                                    facenm,  area,  temp, press,   epx,
c                                       epy,   epz,  epxy,    sx,    sy,
c                                        sz,   sxy, 0.0d0, 0.0d0,    s1,
c                                        s2,    s3,  sint,  seqv

c                                    * For axisymmetric elements:

c                                    facenm,  area,  temp, press, eppar,
c                                     epper,   epz,  epsh,  spar,  sper,
c                                        sz, 0.0d0, 0.0d0,   ssh,    s1,
c                                        s2,    s3,  sint,  seqv

c                                  each item is described below:

c                                    facenm - face number
c                                    area   - face area
c                                    temp   - face temperature
c                                    press  - face pressure
c                                    epx    - strain parallel to face
c                                    epy    - strain parallel to face
c                                    epz    - strain perpendicular to face
c                                    epxy   - shear strain
c                                    eppar  - strain parallel to face
c                                    epper  - strain perpendicular to face
c                                    epsh   - torsion shear strain
c                                    sx     - stress parallel to face
c                                    sy     - stress parallel to face
c                                    sz     - stress perpendicular to face
c                                    sxy    - shear stress
c                                    spar   - stress parallel to face
c                                    sper   - stress perpendicular to face
c                                    ssh    - torsion shear stress
c                                    s1     - S(1)
c                                    s2     - S(2)
c                                    s3     - S(3)
c                                    sint   - S(INT)
c                                    seqv   - S(EQV)
c                                    0.0d0  - position not used

c   EDI     dp       1    varies     Element nodal component diffusion strains.
c                                    This record contains strains in the order
c                                    X,Y,Z,XY,YZ,XZ,EQV. Diffusion
c                                    strains can be nodal values extrapolated
c                                    from the integration points or values at
c                                    the integration points moved to the nodes.
c                                    See item rxtrap in the solution header for
c                                    the setting.
c
c                                    NOTE: See ENS record section for more details
c                                    on record content and length.
c

c   EXY     dp       1    varies     Element integration point coordinates
c                                    The length of the record is numint*3, where
c                                    numint is the number of integration points.
c                                    Even two-dimensional elements use the 3.
c                                    They are output only if requested with the
c                                    OUTRES,loci command.
c                                    Applicable only to legacy element types
c                                    2,42,45,82,92,95, and current technology
c                                    element types 180,181,182,183,185,186,187,
c                                    188,189,208,209,265,281,288,289,290

c   EBA     dp       1    varies     Element structural nodal back stresses
c                                    Record has the same form as the plastic
c                                    strains.  They are output if the form of
c                                    plasticity is kinematic hardening and the
c                                    plastic strains are requested.
c                                    Applicable only to legacy element types
c                                    2,42,45,82,92,95, and current technology
c                                    element types 180,181,182,183,185,186,187,
c                                    188,189,208,209,265,281,288,289,290

c   ESV     dp       1    varies     Element state variable record.  Exists only
c                                    if written by user in usermat or usercreep.

c   MNL     dp       1    varies     Material nonlinear record.

c   records marked with * to the left of the record id can be read and stored
c   into database with "ldread" command.


c *** Nodal Component Stresses (unused)

c  NDSTR    dp       1    6*nnod     Nodal component stresses (TOP for shells)
c                                     (nNodStr > 0)
c           dp       1    6*nnod     BOT nodal component stresses for shells
c                                     (nNodStr > 1)
c           dp       1    6*nnod     MID nodal component stresses for shells
c                                     (nNodStr > 2)
