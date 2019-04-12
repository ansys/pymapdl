"""
This header is straight out of fdemat.inc
*comdeck,fdemat

c *** Copyright ANSYS.  All Rights Reserved.
c *** ansys, inc.

c     **********  description of element matrix file  **********
c
c *** mpg fdemat.inc < eoelem elostr eofini outelm elfini EmatAssemble sffini
c          eqprep sfform elstrt slvstr: emat file description
c
      character*8  EMATNM 
      parameter  (EMATNM='emat    ')

      LONGINT         ematfpL, ematfp
      integer         ematbk, ematut
      common /fdemat/ ematfpL, ematbk, ematut
      equivalence  (ematfp,ematfpL)

c   ********** common variable descriptions ***********
co  ematfpL      file position on file emat
co  ematbk       block number for file emat
co  ematut       file unit for file emat

c   See fddesc for documentation of how binary files are stored.
c  
c     **********  file format  **********

c        recid tells the identifier for this record.  Not all records will have
c             identifiers -- they are only indicated for those records whose 
c             record pointers are stored in the second file header.

c        type tells what kind of information is stored in this record:
c             i - integer
c             dp - double precision
c             cmp - complex

c        nrec tells how many records of this description are found here

c        lrec tells how long the records are (how many items are stored)

c recid    type    nrec    lrec     contents

c  ---      i       1      100      standard ANSYS file header (see binhed for 
c                                   details of header contents)

c  ---      i       1       40      .EMAT FILE HEADER
c                        
c                                    fun02,    nume,   numdof,    lenu,  lenbac,
c                                     maxn, nlgeEMA,  sstEMAT,  nodref,   lumpm,
c                                    kygst,    kygm,     kycd,   kygss,   kygaf,
c                                    kygrf,       0,Glblenbac, ptrGBkl, ptrGBkh,
c                                  ptrElmh, ptrFSTh,  ptrLSTh, ptrBITh, ptrEHDh,
c                                  ptrIDXh,   numCE,  maxLeng,  ptrCEl,  ptrCEh,
c                                   ptrDOF,  ptrBAC,  ptrELMl, ptrFSTl, ptrLSTl,
c                                  ptrBITl, ptrEHDl,  ptrIDXl, ptrendH, ptrendL

c                                each item in header is described below:

c                                   fun02  - unit number (emat file is 2)
c                                   nume   - number of elements
c                                   numdof - number of dofs per node
c                                   lenu   - total DOFs of model
c                                   lenbac - number of nodes
c                                   maxn   - maximum node number
c                                   nlgeEMA  = 0 - nlgeom is OFF the time this Emat file is created
c                                              1 - nlgeom is ON the time this Emat file is created
c                                   sstEMAT  = 0 - sstif key is OFF the time this Emat file is created
c                                              1 - sstif key is ON the time this Emat file is created
c                                                  this key is for internal use only
c                                   nodref - actual number of nodes referenced
c                                   lumpm  - lumped mass key 
c                                            = 0 - default matrix type
c                                            = 1 - lumped
c                                   kygst  - global stiffness matrix calculate 
c                                            key 
c                                            = 0 - do not calculate
c                                            = 1 - calculate
c                                   kygm   - global mass matrix calculate key 
c                                            = 0 - do not calculate
c                                            = 1 - calculate
c                                   kycd   - global damping matrix calculate key
c                                            = 0 - do not calculate
c                                            = 1 - calculate
c                                   kygss  - global stress stiffening matrix 
c                                            calculate key 
c                                            = 0 - do not calculate
c                                            = 1 - calculate
c                                   kygaf  - global applied force vector 
c                                            calculate key
c                                            = 0 - do not calculate
c                                            = 1 - calculate
c                                   kygrf  - global restoring force vector 
c                                            calculate key (Newton-Raphson only)
c                                            = 0 - do not calculate
c                                            = 1 - calculate
c                                   0      - position not used
c                                   Glblenbac - global global number of nodes (== lenbac unless using
c                                               Distributed Ansys)
c                                   ptrGBkl- low pointer to global nodal equivalence table
c                                   ptrGBkh- high pointer to global nodal equivalence table
c                                   ptrELMh- high pointer to element equivalence table
c                                   ptrFSTh- high pointer to first element at a
c                                            DOF table 
c                                   ptrLSTh- high pointer to last element at a
c                                            DOF table
c                                   ptrBITh- high pointer to dof bits
c                                   ptrEHDh- high pointer to the start of the
c                                            element matrices
c                                   ptrIDXh- high pointer to element matrices
c                                            index table
c                                   numCE  - number of internal CEs
c                                   maxLeng- maximum length of any internal CE
c                                   ptrCEl - low pointer to internal CE list
c                                   ptrCEh - high pointer to internal CE list
c                                   ptrDOF - pointer to degrees of freedom per 
c                                            node used in model
c                                   ptrBAC - pointer to nodal equivalence table

c                                   ptrELMl- Low pointer to element equivalence 
c                                            table
c                                   ptrFSTl- Low pointer to first element at a
c                                            DOF table 
c                                   ptrLSTl- Low pointer to last element at a
c                                            DOF table
c                                   ptrBITl- Low pointer to dof bits
c                                   ptrEHDl- Low pointer to the start of the
c                                            element matrices
c                                   ptrIDXl- Low pointer to element matrices
c                                            index table

c                                   ptrendH- High pointer to end of file
c                                   ptrendL- Low  pointer to end of file

c       Note: the analysis type sets the global calculate keys.

c  ---     dp       1       20      Time information
c                                   
c                                   timval, timinc, frqval, timbeg, timend,
c                                      0.0,    0.0,    0.0,    0.0,    0.0,
c                                      0.0,    0.0,    0.0,    0.0,    0.0,
c                                      0.0,    0.0,    0.0,    0.0,    0.0,

c                                  each item is described below:

c                                   timval - the current time
c                                   timinc - the time increment
c                                   frqval - the current frequency (from a 
c                                            harmonic analysis)
c                                   timbeg - the start time for the analysis
c                                   timend - the end time for the analysis
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used
c                                   0.0    - position not used

c  DOF      i       1    numdof     Degrees of freedom per node 
c                                   DOF reference numbers are:
c         UX  = 1, UY  = 2, UZ  = 3, ROTX= 4, ROTY= 5, ROTZ= 6, AX  = 7, AY  = 8
c         AZ  = 9, VX  =10, VY  =11, VZ  =12  ****** 13-18 are spares **********
c         ****************  PRES=19, TEMP=20, VOLT=21, MAG =22, ENKE=23, ENDS=24
c         EMF =25, CURR=26  ********* 27-32 are spares *************************
c                                    (curdof(i),i=1,numdof)

c  BAC      i       1    lenbac     Nodal equivalence table. This table equates
c                                   the number used for storage to the actual 
c                                   node number 
c                                    (Back(i),i=1,lenbac)

c  ELM      i       1     nume      Element equivalence table. The ANSYS program
c                                   stores all element data in the numerical 
c                                   order that the SOLUTION processor solves the
c                                   elements.  This table equates the order 
c                                   number used to the actual element number
c                                    (Order(i),i=1,nume)

c  GBK      i       1  Glblenbac    Global nodal equivalence table.  This
c                                   table equates the number used for storage
c                                   to the actual node number.  Only written
c                                   by the master process in Distributed Ansys
c                                    (GlbBack(i),i=1,Glblenbac)

c  FST      i       1     lenu      First element at a DOF table. This record 
c                                   signifies the first element encountered at a
c                                   particular DOF.
c                                    (First(i),i=1,lenu)

c  LST      i       1     lenu      Last element at a DOF table. This record 
c                                   signifies the last element encountered at a
c                                   particular DOF.
c                                    (Last(i),i=1,lenu)

c  BIT      i       1     lenu      Bits set at a DOF table. This record 
c                                   has bits for constraints, forces, etc.
c                                    (DofBits(i),i=1,lenu) (added at 10.0)

c  IDX      i       1     2*nume    Element index table. This record specifies 
c                                   the file location for the beginning of the
c                                   data for each element.
c                                    (index(i),i=1,nume) Low part of pointer
c                                    (index(i),i=1,nume) High part of pointer


c  The records at the end of the file store element information and get written
c  as a set for each element(nume sets of these records will appear on the file
c  at this point) ptrEHD indicates the beginning of the element data.

c  If substructure matrices are written to the EMAT file, they are written in a
c  different format than is shown here. This alternate format is not documented
c  at this time, as it is likely to change in the future.


c  EHD      i       1      10       Element matrix header
c                                   
c                                    stkey,   mkey,   dkey,  sskey, akey,
c                                    nrkey,   ikey,      0,      0, nmrow

c                                  each item in header is described below:

c                                   stkey  - stiffness matrix key 
c                                            = 0 - matrix not present
c                                            = 1 - matrix present
c                                   mkey   - mass matrix key 
c                                            = 0 - matirx not present
c                                            = 1 - matrix present
c                                   dkey   - damping matrix key 
c                                            = 0 - matrix not present
c                                            = 1 - matrix present
c                                   sskey  - stress stiffening matrix key 
c                                            = 0 - matrix not present
c                                            = 1 - matrix present
c                                   akey   - applied load vector key 
c                                            = 0 - vector not used
c                                            = 1 - vector used
c                                   nrkey  - newton-raphson(restoring) load 
c                                            vector key (for nonlinear analyses)
c                                            = 0 - vector not used
c                                            = 1 - vector used
c                                   ikey   - imaginary load vector key 
c                                              (for complex analyses)
c                                            = 0 - vector not used
c                                            = 1 - vector used 
c                                   0      - position not used
c                                   0      - position not used
c                                   nmrow  - numbers/columns in matrices. If the
c                                            number is negative, the matrices 
c                                            will be written in lower triangular
c                                            form.

c  ---      i       1    nmrow      DOF index table. This record specifies the 
c                                   DOF locations of this element matrix in 
c                                   relation to the global matrix. The index is
c                                   calculated as (N-1)*NUMDOF+DOF, where N is 
c                                   the position number of the node in the nodal
c                                   equivalence table and DOF is the DOF 
c                                   reference number given above

c  ---     dp    varies  varies     Element matrices. This record is repeated 
c                                   for each stiffness, mass, damping, and 
c                                   stress stiffening matrix. If the matrix is 
c                                   diagonal, the length of the records will be
c                                   nmrow.  If the matrix is unsymmetric, the 
c                                   length of the records will be nmrow*nmrow. 
c                                   If the matrix is symmetric, only the lower 
c                                   triangular terms are written and the length
c                                   of the records will be (nmrow)*(nmrow+1)/2.

c  ---     dp       1    2*nmrow    Element force vectors. This record contains
c                                   both the applied force vector and the 
c                                   (restoring or imaginary) load vector.
c
c 
c      *************** Internal CE information ***********************
c      The following records repeat numCE times... one for each internal
c      CE created during solution... these are stored here for the 
c      usage of a prestressed modal analysis such as the linear perturbation analysis
c
c  CE      i       3     numCE      First part is the CE number, the second part is
c                                   the number of terms in this internal CE, and
c                                   the third part is the external element number
c                                   of the element that created this internal CE
c
c  ---     i     nTerms  numCE      integer info (list of node*32 + dof)
c                                                     
c  ---    dp     nTerms  numCE      dp info (list of coefficients including constant term)
c
c
c   kygst        global stiffness matrix calculate key
c   kygm         global mass matrix calculate key
c   kygd         global damping matrix calculate key
c   kygss        global stress stiffening matrix calculate key
c   kygaf        global applied force matrix calculate key
c   kygrf        global restoring force matrix calculate key

"""
from pyansys.generic_binary import BinaryFile
from pyansys.common import read_table, parse_header

EMAT_HEADER_KEYS = ['fun02', 'nume', 'numdof', 'lenu', 'lenbac',
                    'maxn', 'nlgeEMA', 'sstEMAT', 'nodref', 'lumpm',
                    'kygst', 'kygm', 'kycd', 'kygss', 'kygaf',
                    'kygrf', '0', 'Glblenbac', 'ptrGBkl', 'ptrGBkh',
                    'ptrElmh', 'ptrFSTh', 'ptrLSTh', 'ptrBITh',
                    'ptrEHDh', 'ptrIDXh', 'numCE', 'maxLeng',
                    'ptrCEl', 'ptrCEh', 'ptrDOF', 'ptrBAC', 'ptrElml',
                    'ptrFSTl', 'ptrLSTl', 'ptrBITl', 'ptrEHDl',
                    'ptrIDXl', 'ptrendH', 'ptrendL']


class EmatFile(BinaryFile):

    def __init__(self):
        self.read_header()

    def read_header(self):
        header = {}
        with open(self.filename, 'rb') as f:
            f.seek(103*4)
            self.header = parse_header(read_table(f), EMAT_HEADER_KEYS)

    def read_element_matrix_header(self):
        """Read element matrix header

        Notes
        -----
        stkey - stiffness matrix key 
            0 - matrix not present
            1 - matrix present

        mkey - mass matrix key 
            0 - matirx not present
            1 - matrix present

        dkey - damping matrix key 
            0 - matrix not present
            1 - matrix present

        sskey - stress stiffening matrix key 
            0 - matrix not present
            1 - matrix present

        akey - applied load vector key 
            0 - vector not used
            1 - vector used

        nrkey - newton-raphson(restoring) load 

        vector key (for nonlinear analyses)
            0 - vector not used
            1 - vector used

        ikey - imaginary load vector key (for complex analyses)
            0 - vector not used
            1 - vector used 
        nmrow - numbers/columns in matrices. 
            If the number is negative, the matrices will be written in
            lower triangular form.

        """
        header_keys = ['stkey', 'mkey', 'dkey', 'sskey', 'akey',
                       'nrkey', 'ikey', '_', '_', 'nmrow']

        with open(self.filename, 'rb') as f:
            f.seek(4*self.header['ptrEHD'])
            self.element_matrix_header = parse_header(read_table(f),
                                                      header_keys)
