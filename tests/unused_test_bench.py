import pytest

import pyansys
from pyansys import cyclic_reader


# @pytest.fixture(scope='module')
# def academic_rotor():
#     filename = '/home/alex/projects/pw/academic_sect/Static/5000RPM/academic_4sect_5000rpm_stc.rst'
#     return pyansys.read_binary(filename)


# def load_rotor():
#     filename = '/home/alex/projects/pw/academic_sect/Static/5000RPM/academic_4sect_5000rpm_stc.rst'
#     return pyansys.read_binary(filename)


# def test_load(benchmark):
#     rst = benchmark(load_rotor)
#     assert isinstance(rst, cyclic_reader.CyclicResult)


# def test_nodal_displacement(benchmark, academic_rotor):
#     benchmark(academic_rotor.nodal_displacement, 0)


# # def test_nodal_displacement(benchmark, academic_rotor):
# #     benchmark(academic_rotor.principal_nodal_stress, 0)


# def test_nodal_stress(benchmark, academic_rotor):
#     benchmark(academic_rotor.nodal_stress, 0)
