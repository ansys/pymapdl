"""Various header keys for the result file

/usr/ansys_inc/v150/ansys/customize/include/fdresu.inc

"""

geometry_header_keys = ['__unused',  # 1
                        'maxety',    # 2
                        'maxrl',     # 3
                        'nnod',      # 4
                        'nelm',      # 5
                        'maxcsy',    # 6
                        'ptrETY',    # 7
                        'ptrREL',    # 8
                        'ptrLOC',    # 9
                        'ptrCSY',    # 10
                        'ptrEID',    # 11
                        'maxsec',    # 12
                        'secsiz',    # 13
                        'nummat',    # 14
                        'matsiz',    # 15
                        'ptrMAS',    # 16
                        'csysiz',    # 17
                        'elmsiz',    # 18
                        'etysiz',    # 19
                        'rlsiz',     # 20
                        'ptrETYl',   # 21
                        'ptrETYh',   # 22
                        'ptrRELl',   # 23
                        'ptrRELh',   # 24
                        'ptrCSYl',   # 25
                        'ptrCSYh',   # 26
                        'ptrLOCl',   # 27
                        'ptrLOCh',   # 28
                        'ptrEIDl',   # 29
                        'ptrEIDh',   # 30
                        'ptrMASl',   # 31
                        'ptrMASh',   # 32
                        'ptrSECl',   # 33
                        'ptrSECh',   # 34
                        'ptrMATl',   # 35
                        'ptrMATh',   # 36
                        'ptrCNTl',   # 37
                        'ptrCNTh',   # 38
                        'ptrNODl',   # 39
                        'ptrNODh',   # 40
                        'ptrELMl',   # 41
                        'ptrELMh',   # 42
                        'Glblenb',   # 43
                        'ptrGNODl',  # 44
                        'ptrGNODh',  # 45
                        'maxn',      # 46
                        'NodesUpd',  # 47
                        'lenbac',    # 48
                        'maxcomp',   # 49
                        'compsiz',   # 50
                        'ptrCOMPl',  # 51
                        'ptrCOMPh',  # 52
                        'nMatProp',  # 53
                        'nStage',    # 54
                        'maxMSsz',   # 55
                        'ptrMSl',    # 56
                        'ptrMSh',    # 57
                        'nCycP',     # 58
                        'ptrCycPl',  # 59
                        'ptrCycPh',  # 60
                        'numety',    # 61
                        'numrl',     # 62
                        'numcsy',    # 63
                        'numsec',    # 64
                        'mapFlag',   # 65
                        'cysCSID'    # 66
]

# FROM fdresu.inc
# maxety - the maximum element type reference number in the model
# maxrl  - the maximum real constant reference number in the model
# nnod   - the number of defined nodes in the model
# nelm   - the number of defined elements in the model
# maxcsy - the maximum coordinate system reference number in the model
# ptrETY - pointer to the element type index table
# ptrREL - pointer to the real constant index table
# ptrLOC - pointer to the nodal point locations
# ptrCSY - pointer to the local coordinate system index table
# ptrEID - pointer to the element index table
# maxsec - the maximum section reference number in the model
# secsiz - the maximum size that any section record may have
# nummat - the number of materials in the model
# matsiz - the maximum size that any material property or table may have
# ptrMAS - pointer to the diagonal mass matrix
# csysiz - the number of items describing a local coordinate system (usually 24)
# elmsiz - the maximum number of nodes that a defined element may have
# etysiz - the number of items describing an element type(=IELCSZ from echprm.inc)
# rlsiz  - the maximum number of items defining a real constant (0, if
#           no real constants are defined)
# ETYl,h - 64 bit pointer to element type data
# RELl,h - 64 bit pointer to real constant data
# CSYl,h - 64 bit pointer to coordinate system data
# LOCl,h - 64 bit pointer to nodal locations
# EIDl,h - 64 bit pointer to element data
# SECl,h - 64 bit pointer to section data
# MATl,h - 64 bit pointer to material data
# CNTl,h - 64 bit pointer to element centroids
# NODl,h - 64 bit pointer to nodal equivalence table
# ELMl,h - 64 bit pointer to element equivalence table
# lbnnod - global number of nodes actually used in the solution phase
#          (== nnod unless using Distributed Ansys)
# GNODl,h- 64 bit pointer to the global nodal equivalence table (only
#          used with Distributed ANSYS and when the mesh does not change during
#          solution)
# maxn     - maximum node number of the model
# NodesUpd - 1, node coords have been updated
# lenbac   - the actual number of nodes used in the solution phase
# numcomp  - number of components/assemblies stored (only node/elem
#            components/assemblies)
# mxcmpsz  - maximum size (in integer words) that any
#            component/assembly record may have
# ptrCOMPl,h - 64 bit pointer to component/assembly data
# nMatProp - number of properties stored per material
# nStage   - number of stages
# maxMSsz  - maximum size (in integer words) that a
#            stage record can have
# ptrMSl,h - 64 bit pointer to multistage (MS) cyclic
#            analysis data
# nCycP    - number of cyclic edge node pair tables (CYCLIC and MS)
# ptrCycPl,h - pointers to cyclic edge node pair tables
# numety   - the number of defined element types
#            in the model
# numrl    - the number of defined real constants in the model
# numcsy   - the number of defined coordinate
#            systems in the model
# numsec   - the number of defined sections in the model
# mapFlag  - flag to indicate format of mapping index vectors for
#            element types, real constants, coordinate systems, and
#            sections.
#            = 0, old format with 1 vector of maxDef len
#            = 1, new format with 2 vectors each having numDef len
# cycCSID  - coordinate system number (CYCLIC and MS)
#            = 0 is ignored (must be cylindrical)



element_index_table_info = {
    'EMS': 'Misc. data',
    'ENF': 'Nodal forces',
    'ENS': 'Nodal stresses',
    'ENG': 'Volume and energies',
    'EGR': 'Nodal gradients',
    'EEL': 'Elastic strains',
    'EPL': 'Plastic strains',
    'ECR': 'Creep strains',
    'ETH': 'Thermal strains',
    'EUL': 'Euler angles',
    'EFX': 'Nodal fluxes',
    'ELF': 'Local forces',
    'EMN': 'Misc. non-sum values',
    'ECD': 'Element current densities',
    'ENL': 'Nodal nonlinear data',
    'EHC': 'Calculated heat generations',
    'EPT': 'Element temperatures',
    'ESF': 'Element surface stresses',
    'EDI': 'Diffusion strains',
    'ETB': 'Etable items',
    'ECT': 'Contact data',
    'EXY': 'Integration point locations',
    'EBA': 'Back stresses',
    'ESV': 'State variables',
    'MNL': 'Material nonlinear record'
}

solution_data_header_keys = ['pv3num', 'nelm', 'nnod', 'mask', 'itime',
                             'iter', 'ncumit', 'nrf', 'cs_LSC', 'nmast',
                             'ptrNSL', 'ptrESL', 'ptrRF', 'ptrMST',
                             'ptrBC', 'rxtrap', 'mode', 'isym', 'kcmplx',
                             'numdof', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                             'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                             'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                             'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                             'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                             'DOFS', 'DOFS', 'DOFS', 'DOFS', 'DOFS',
                             'DOFS', 'title', 'title', 'title', 'title',
                             'title', 'title', 'title', 'title', 'title',
                             'title', 'title', 'title', 'title', 'title',
                             'title', 'title', 'title', 'title', 'title',
                             'title', 'stitle', 'stitle', 'stitle',
                             'stitle', 'stitle', 'stitle', 'stitle',
                             'stitle', 'stitle', 'stitle', 'stitle',
                             'stitle', 'stitle', 'stitle', 'stitle',
                             'stitle', 'stitle', 'stitle', 'stitle',
                             'stitle', 'dbmtim', 'dbmdat', 'dbfncl',
                             'soltim', 'soldat', 'ptrOND', 'ptrOEL',
                             'nfldof', 'ptrEXA', 'ptrEXT', 'ptrEXAl',
                             'ptrEXAh', 'ptrEXTl', 'ptrEXTh', 'ptrNSLl',
                             'ptrNSLh', 'ptrRFl', 'ptrRFh', 'ptrMSTl',
                             'ptrMSTh', 'ptrBCl', 'ptrBCh', 'ptrTRFl',
                             'ptrTRFh', 'ptrONDl', 'ptrONDh', 'ptrOELl',
                             'ptrOELh', 'ptrESLl', 'ptrESLh', 'ptrOSLl',
                             'ptrOSLh', 'sizeDEAD', 'ptrDEADl', 'ptrDEADh',
                             'PrinKey', 'numvdof', 'numadof', '0', '0',
                             'ptrVSLl', 'ptrVSLh', 'ptrASLl', 'ptrASLh', '0',
                             '0', '0', '0', 'numRotCmp', '0',
                             'ptrRCMl', 'ptrRCMh', 'nNodStr', '0', 'ptrNDSTRl',
                             'ptrNDSTRh', 'AvailData', 'geomID', 'ptrGEOl', 'ptrGEOh']

solution_header_keys_dp = ['timfrq', 'lfacto', 'lfactn', 'cptime',
                           'tref', 'tunif', 'tbulk', 'volbase',
                           'tstep', '__unused', 'accel_x', 'accel_y',
                           'accel_z', 'omega_v_x', 'omega_v_y',
                           'omega_v_z', 'omega_a_x', 'omega_a_y',
                           'omega_a_z', 'omegacg_v_x', 'omegacg_v_y',
                           'omegacg_v_z', 'omegacg_a_x',
                           'omegacg_a_y', 'omegacg_a_z', 'cgcent',
                           'cgcent', 'cgcent', 'fatjack', 'fatjack',
                           'dval1', 'pCnvVal']

result_header_keys = ['fun12', 'maxn', 'nnod', 'resmax', 'numdof',
                      'maxe', 'nelm', 'kan', 'nsets', 'ptrend',
                      'ptrDSIl', 'ptrTIMl', 'ptrLSPl', 'ptrELMl',
                      'ptrNODl', 'ptrGEOl', 'ptrCYCl', 'CMSflg',
                      'csEls', 'units', 'nSector', 'csCord',
                      'ptrEnd8', 'ptrEnd8', 'fsiflag', 'pmeth',
                      'noffst', 'eoffst', 'nTrans', 'ptrTRANl',
                      'PrecKey', 'csNds', 'cpxrst', 'extopt',
                      'nlgeom', 'AvailData', 'mmass', 'kPerturb',
                      'XfemKey', 'rstsprs', 'ptrDSIh', 'ptrTIMh',
                      'ptrLSPh', 'ptrCYCh', 'ptrELMh', 'ptrNODh',
                      'ptrGEOh', 'ptrTRANh', 'Glbnnod', 'ptrGNODl',
                      'ptrGNODh', 'qrDmpKy', 'MSUPkey', 'PSDkey',
                      'cycMSUPkey', 'XfemCrkPropTech']

boundary_condition_index_table = [
    'numdis',  # number of nodal constraints
    'ptrDIX',  # pointer to the table of nodes having nodal constraints
    'ptrDIS',  # pointer to nodal constraint values
    'numfor',  # number of nodal input force loadings
    'ptrFIX',  # pointer to the table of nodes having nodal forces
    'ptrFOR',  # pointer to nodal force values
    'format'  # key (0 or 1) denoting which format is used for DIX/FIX data (see below)
]
# if format == 0 --> Nodal constraint DOF.
# This index is calculated as N*32+DOF, where N is the node number and
# DOF is the DOF reference number.  Values are in the same order as
# the DOF number reference table.
# if format == 1 --> Nodal constraint node
# numbers.

# Degrees of freedom per node DOF reference numbers are
DOF_REF = {
    1: 'UX',
    2: 'UY',
    3: 'UZ',
    4: 'ROTX',
    5: 'ROTY',
    6: 'ROTZ',
    7: 'AX',
    8: 'AY',
    9: 'AZ',
    10: 'VX',
    11: 'VY',
    12: 'VZ',
    16: 'WARP',
    17: 'CONC',
    18: 'HDSP',
    19: 'PRES',
    20: 'TEMP',
    21: 'VOLT',
    22: 'MAG',
    23: 'ENKE',
    24: 'ENDS',
    25: 'EMF',
    26: 'CURR',
    27: 'SP01',
    28: 'SP02',
    29: 'SP03',
    30: 'SP04',
    31: 'SP05',
    32: 'SP06',
    33: 'TBOT',
    34: 'TE2',
    35: 'TE3',
    36: 'TE4',
    37: 'TE5',
    38: 'TE6',
    39: 'TE7',
    40: 'TE8',
    41: 'TE9',
    42: 'TE10',
    43: 'TE11',
    44: 'TE12',
    45: 'TE13',
    46: 'TE14',
    47: 'TE15',
    48: 'TE16',
    49: 'TE17',
    50: 'TE18',
    51: 'TE19',
    52: 'TE20',
    53: 'TE21',
    54: 'TE22',
    55: 'TE23',
    56: 'TE24',
    57: 'TE25',
    58: 'TE26',
    59: 'TE27',
    60: 'TE28',
    61: 'TE29',
    62: 'TE30',
    63: 'TE31',
    64: 'TTOP'
}
