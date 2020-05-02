"""Various header keys for the result file"""

geometry_header_keys = ['__unused',  # position not used
                        'maxety',
                        'maxrl',
                        'nnod',
                        'nelm',
                        'maxcsy',
                        'ptrETY',
                        'ptrREL',
                        'ptrLOC',
                        'ptrCSY',
                        'ptrEID',
                        'maxsec',
                        'secsiz',
                        'nummat',
                        'matsiz',
                        'ptrMAS',
                        'csysiz',
                        'elmsiz',
                        'etysiz',
                        'rlsiz',
                        'ptrETYl',
                        'ptrETYh',
                        'ptrRELl',
                        'ptrRELh',
                        'ptrCSYl',
                        'ptrCSYh',
                        'ptrLOCl',
                        'ptrLOCh',
                        'ptrEIDl',
                        'ptrEIDh',
                        'ptrMASl',
                        'ptrMASh',
                        'ptrSECl',
                        'ptrSECh',
                        'ptrMATl',
                        'ptrMATh',
                        'ptrCNTl',
                        'ptrCNTh',
                        'ptrNODl',
                        'ptrNODh',
                        'ptrELMl',
                        'ptrELMh',
                        'Glbnnod',
                        'ptrGNODl',
                        'ptrGNODh',
                        'maxn',
                        'NodesUpd',
                        'lenbac',
                        'maxcomp',
                        'compsiz',
                        'ptrCOMPl',
                        'ptrCOMPh']

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
# rlsiz  - the maximum number of items defining a real constant (0, if no real constants are defined)
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
# lbnnod - global number of nodes actually used in the solution phase (== nnod unless using Distributed Ansys)
# GNODl,h- 64 bit pointer to the global nodal equivalence table (only used with Distributed ANSYS and when the mesh does not change during solution)
# maxn   - maximum node number of the model


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
                             'PrinKey','numvdof', 'numadof', '0', '0',
                             'ptrVSLl','ptrVSLh', 'ptrASLl', 'ptrASLh', '0',
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
