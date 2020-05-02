import os

import pytest
import pyansys


path = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope='module')
def rst():
    rst_file = os.path.join(path, 'file.rst')
    return pyansys.read_binary(rst_file)


def test_materials(rst):
    materials = rst.materials
    material = materials[1]
    material['EX'] = 40000000000
    material['EY'] = 10000000000
    material['EZ'] = 10000000000
    material['PRXY'] = 0.3
    material['PRYZ'] = 0.3
    material['PRXZ'] = 0.3
    material['GXY'] = 5000000000
    material['GYZ'] = 5000000000
    material['GXZ'] = 5000000000

