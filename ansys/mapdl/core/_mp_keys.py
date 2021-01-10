"""Contains material property indices

Obtained from:
/usr/ansys_inc/v202/ansys/customize/include/mpcom.inc


These indices are used when reading in results using ptrMAT from a
binary result file.
"""

# order is critical here
mp_keys = ['EX', 'EY', 'EZ', 'NUXY', 'NUYZ', 'NUXZ', 'GXY', 'GYZ',
           'GXZ', 'ALPX', 'ALPY', 'ALPZ', 'DENS', 'MU', 'DAMP', 'KXX',
           'KYY', 'KZZ', 'RSVX', 'RSVY', 'RSVZ', 'C', 'HF', 'VISC',
           'EMIS', 'ENTH', 'LSST', 'PRXY', 'PRYZ', 'PRXZ', 'MURX',
           'MURY', 'MURZ', 'PERX', 'PERY', 'PERZ', 'MGXX', 'MGYY',
           'MGZZ', 'EGXX', 'EGYY', 'EGZZ', 'SBKX', 'SBKY', 'SBKZ',
           'SONC', 'SLIM', 'ELIM', 'USR1', 'USR2', 'USR3', 'USR4',
           'FLUI', 'ORTH', 'CABL', 'RIGI', 'HGLS', 'BVIS', 'QRAT',
           'REFT', 'CTEX', 'CTEY', 'CTEZ', 'THSX', 'THSY', 'THSZ',
           'DMPR', 'LSSM', 'BETD', 'ALPD', 'RH', 'DXX', 'DYY', 'DZZ',
           'BETX', 'BETY', 'BETZ', 'CSAT', 'CREF', 'CVH']
