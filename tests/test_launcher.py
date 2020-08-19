"""Test launching the corba interface"""
import re
import os
import pytest
import pyansys

def get_ansys_bin(rver):
    if os.name == 'nt':
        ans_root = 'c:/Program Files/ANSYS Inc/'
        mapdlbin = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin', 'winx64',
                                'ANSYS%s.exe' % rver)
    else:
        ans_root = '/usr/ansys_inc'
        mapdlbin = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin',
                                'ansys%s' % rver)

    return mapdlbin


versions = ['182',
            '190',  # 19.0
            '191',  # 19.1
            '192',  # 19.2
            '193',  # 2019R1
            '194',  # 2019R2
            '195',  # 2019R3
            '201',  # 2020R1
            '202']  # 2020R2
valid_versions = []
for version in versions:
    exec_file = get_ansys_bin(version)
    if os.path.isfile(get_ansys_bin(version)):
        valid_versions.append(version)



def test_invalid_mode():
    with pytest.raises(ValueError):
        exec_file = get_ansys_bin('182')
        pyansys.launch_mapdl(exec_file, override=True, mode='notamode')


def test_old_version():
    exec_file = get_ansys_bin('150')
    with pytest.raises(ValueError):
        pyansys.launch_mapdl(exec_file, override=True, mode='corba')



@pytest.mark.parametrize('version', valid_versions)
@pytest.mark.skipif(os.name != 'posix', reason="Only supported on Linux")
def test_launch_pexpect(version):
    exec_file = get_ansys_bin(version)
    mapdl = pyansys.launch_mapdl(exec_file, override=True, mode='console')
    assert mapdl.version == int(version)/10


@pytest.mark.parametrize('version', valid_versions)
def test_launch_corba(version):
    exec_file = get_ansys_bin(version)
    mapdl = pyansys.launch_mapdl(exec_file, override=True, mode='corba')
    assert mapdl.version == int(version)/10
