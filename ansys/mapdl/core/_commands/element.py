"""These PREP7 commands are used to create, modify, list, etc., elements.

Examples
--------
Create a single SURF154 element.

>>> mapdl.prep7()
>>> mapdl.et(1, 'SURF154')
>>> mapdl.n(1, 0, 0, 0)
>>> mapdl.n(2, 1, 0, 0)
>>> mapdl.n(3, 1, 1, 0)
>>> mapdl.n(4, 0, 1, 0)
>>> mapdl.e(1, 2, 3, 4)
1

Create a single hexahedral SOLID185 element

>>> mapdl.et(2, 'SOLID185')
>>> mapdl.type(2)
>>> mapdl.n(5, 0, 0, 0)
>>> mapdl.n(6, 1, 0, 0)
>>> mapdl.n(7, 1, 1, 0)
>>> mapdl.n(8, 0, 1, 0)
>>> mapdl.n(9, 0, 0, 1)
>>> mapdl.n(10, 1, 0, 1)
>>> mapdl.n(11, 1, 1, 1)
>>> mapdl.n(12, 0, 1, 1)
>>> mapdl.e(5, 6, 7, 8, 9, 10, 11, 12)
2

Print the volume of individual elements

>>> mapdl.clear()
>>> output = mapdl.input(examples.vmfiles['vm6'])
>>> mapdl.post1()
>>> label = 'MYVOLU'
>>> mapdl.etable(label, 'VOLU')
>>> print(mapdl.pretab(label))
PRINT ELEMENT TABLE ITEMS PER ELEMENT
   *****ANSYS VERIFICATION RUN ONLY*****
     DO NOT USE RESULTS FOR PRODUCTION
  ***** POST1 ELEMENT TABLE LISTING *****
    STAT     CURRENT
    ELEM     XDISP
       1  0.59135E-001
       2  0.59135E-001
       3  0.59135E-001
...

See the individual commands for more details.


"""
import warnings
import re
from typing import Optional, Union

from ..mapdl_types import MapdlInt, MapdlFloat
