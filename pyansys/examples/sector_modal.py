"""
This script was used to generate the sector modal analysis result file.

Result file is sector.rst
"""
import pyansys
from pyansys import examples

ansys = pyansys.ANSYS()

ansys.Cdread('db', examples.sector_archive_file)

# make cyclic
ansys('/PREP7')
ansys('CYCLIC')

# Steel
ansys('MP,    NUXY,   1,  0.3')
ansys('MP,    DENS,   1,  0.0005')
ansys('MP,      EX,   1,  17000000')
ansys('EMODIF,ALL,MAT,1')

# Static solution
ansys('/SOLU')
ansys('ANTYPE, 2, new')
ansys('MODOPT, LANB, 6, 1')
ansys.Cycopt('hindex', 'all')
ansys.Bcsoption('', 'INCORE')
ansys.Mxpand('', '', '', 'Yes')
ansys.Solve()
ansys.Finish()
ansys.Save()
ansys.Exit()

# ansys.result.animate_nodal_solution(20)
