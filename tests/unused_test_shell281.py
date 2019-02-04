"""
In PyAnsys I type
```
test_result = pyansys.ResultReader('sample.rst')
estress,elem,enode = test_result.element_stress(0)
print(estress[23])
print(enode[23])
```
And get
```
[[nan nan nan nan nan nan]
 [nan nan nan nan nan nan]
 [nan nan nan nan nan nan]
 [nan nan nan nan nan nan]]
[ 1 82 92  8]
```

And in Ansys I get
```
ELEMENT=      24        SHELL281
    NODE     SX           SY           SZ           SXY          SYZ          SXZ     
       1  -50.863     -0.63898E-030 -215.25     -0.18465E-015 0.10251E-013 -47.847     
      82   13.635     -0.74815E-030 -178.71     -0.21958E-015 0.11999E-013  17.232     
      92  -7.1801     -0.84355E-030 -213.77     -0.56253E-015 0.13214E-013  2.0152     
       8  -47.523     -0.96156E-030 -204.12     -0.30574E-014 0.12646E-013  2.4081     
       1   107.75      0.13549E-029  454.30      0.45391E-015-0.21674E-013  100.34     
      82  -28.816      0.15515E-029  372.47      0.38337E-015-0.24955E-013 -35.077     
      92   14.454      0.16547E-029  429.43      0.80716E-015-0.26217E-013  1.2719     
       8   94.254      0.19148E-029  409.31      0.59899E-014-0.25281E-013 -3.5690 
```

It would also be really useful to be able to read the Nodal Forces and Moment from the Elemental Solution using the: 

element_solution_data(0,'ENF',sort=True)
From PyAnsys for element 24:
```
array([ 7.1140683e-01,  2.5775826e-06,  1.8592998e+00,  1.7531972e-03,
       -5.4216904e-12, -6.6381943e-04,  7.8414015e-02,  4.7199319e-06,
       -1.2074181e+00, -9.0049638e-04, -5.2645028e-12, -3.2152122e-05,
        7.3660083e-02,  2.5742002e-05, -1.1951995e+00, -2.7250897e-04,
        1.0039868e-12,  1.5112829e-04, -1.9362889e-01,  4.7199323e-06,
        1.3849777e+00,  6.4305059e-05,  2.9884493e-12, -2.2116321e-04,
        3.0604819e-02, -4.8676171e-05, -1.0389121e-01,  5.7917450e-16,
       -2.7263033e-25,  4.0045388e-17, -8.5023224e-02,  2.9796447e-05,
       -5.3827515e+00, -2.2202423e-03,  3.8493188e-11,  7.6806801e-04,
       -8.5418850e-01,  2.4989351e-06, -3.3126956e-01, -9.2828198e-04,
        6.3002242e-11,  8.8052053e-05,  2.3875487e-01, -2.1378659e-05,
        4.9762526e+00,  2.5969518e-03,  5.0141464e-11, -1.8303801e-04],
      dtype=float32)])
```
And From Ansys:
```
  ELEM=      24  FX         FY         FZ                                      
       1  0.71141      0.25776E-005  1.8593     
      82  0.78414E-001 0.47199E-005 -1.2074     
      92  0.73660E-001 0.25742E-004 -1.1952     
       8 -0.19363      0.47199E-005  1.3850     
      83  0.30605E-001-0.48676E-004-0.10389     
      86 -0.85023E-001 0.29796E-004 -5.3828     
      93 -0.85419      0.24989E-005-0.33127     
       9  0.23875     -0.21379E-004  4.9763  

  ELEM=      24  MX         MY         MZ                                      
       1  0.17532E-002-0.54217E-011-0.66382E-003
      82 -0.90050E-003-0.52645E-011-0.32152E-004
      92 -0.27251E-003 0.10040E-011 0.15113E-003
       8  0.64305E-004 0.29884E-011-0.22116E-003
      83  0.57917E-015-0.27263E-024 0.40045E-016
      86 -0.22202E-002 0.38493E-010 0.76807E-003
      93 -0.92828E-003 0.63002E-010 0.88052E-004
       9  0.25970E-002 0.50141E-010-0.18304E-003
"""

import os
import numpy as np
import pyansys
# from pyansys.examples import hexarchivefile
# from pyansys.examples import rstfile
# from pyansys.examples import fullfile

try:
    __file__
    test_path = os.path.dirname(os.path.abspath(__file__))
    testfiles_path = os.path.join(test_path, 'testfiles')
except:
    testfiles_path = '/home/alex/afrl/python/source/pyansys/tests/testfiles'


ANSYS_ELEM = [[0.17662E-07, 79.410, -11.979, -0.11843E-02, 4.8423, -0.72216E-04],
              [0.20287E-07, 91.212, 27.364, -0.13603E-02, 4.8423, -0.72216E-04],
              [0.20287E-07, 91.212, 27.364, -0.13603E-02, -4.8423, 0.72216E-04],
              [0.17662E-07, 79.410, -11.979, -0.11843E-02, -4.8423, 0.72216E-04]]

ANSYS_NODE = [[0.20287E-07, 91.212, 27.364, -0.13603E-02, 4.8423, -0.72216E-04],
              [0.17662E-07, 79.410, -11.979, -0.11843E-02, 4.8423, -0.72216E-04],
              [0.17662E-07, 79.410, -11.979, -0.11843E-02, -4.8423, 0.72216E-04],
              [0.20287E-07, 91.212, 27.364, -0.13603E-02, -4.8423, 0.72216E-04]]

result_file = os.path.join(testfiles_path, 'shell281.rst')
test_result = pyansys.ResultReader(result_file, valid_element_types=['281'])

# estress, elem, enode = test_result.element_stress(0, in_element_coord_sys=False)
estress, elem, enode = test_result.element_stress(0, in_element_coord_sys=True)
print(estress[23][:4])

# debug
np.any(np.isclose(-50.863, estress[23]))
np.isclose(-50.863, estress[23]).any(1).nonzero()
# np.isclose(-50.863, table).any(1).nonzero()


f.seek(400284 - 8)
table = read_table(f, 'f')
# f.seek(400284)
ncomp = 6
nodstr = 4
nl = 7
# nread = nl*3*nodstr*ncomp
# table = read_table(f, 'f', get_nread=False, nread=nread)
print((np.isclose(-50.863, table).nonzero()[0] - 1)/table.size)

# print(read_table(f, 'i', get_nread=False, nread=1))



# print(table[:10])

# # elem, res = test_result.element_solution_data(0, 'ENF', sort=True)
# # print(res[23].reshape(8, -1))


# # fseek(cfile, (ele_table + PTR_ENS_IDX)*4, SEEK_SET)
# # fread(&ptrENS, sizeof(int32_t), 1, cfile)

# # fseek(cfile, (ele_table + ptrENS)*4, SEEK_SET)
# # fread(&ele_data_arr[c, 0], sizeof(float), nread, cfile)

# # number of items in this record is NL*3*nodstr*ncomp
# ncomp = 6
# nodstr = 4
