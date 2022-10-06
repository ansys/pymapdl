"""Test DPF implementation of Result class.


Notes
=====

- Many of reader results return strange values (power of +300 or -300). It might be due to running multiphysics examples.
  I presume the retrieving of nodal values in the RST is not performed properly.
  Because of that, we are using also the ``Post_Processing`` module for validation.

- There are some issues with ordering the ``Elemental`` and ``ElementalNodal`` results according to Element ID.
  Because of that, the third level of assertion is made on the sorted arrays.

"""
import os
import tempfile

from ansys.mapdl.reader import read_binary
import numpy as np
import pytest

from ansys.mapdl.core.examples import (
    electrothermal_microactuator_analysis,
    elongation_of_a_solid_bar,
    piezoelectric_rectangular_strip_under_pure_bending_load,
    transient_thermal_stress_in_a_cylinder,
)

COMPONENTS = ["X", "Y", "Z", "XY", "YZ", "XZ"]


def validate(result_values, reader_values, post_values=None):
    try:
        assert all_close(result_values, reader_values, post_values)
    except AssertionError:
        try:
            assert np.allclose(result_values, post_values) or np.allclose(
                result_values, reader_values
            )
        except AssertionError:  # Sometimes sorting fails.
            assert np.allclose(sorted(result_values), sorted(post_values))


def all_close(*args):
    return np.all(
        [np.allclose(each0, each1) for each0, each1 in zip(args[:-1], args[1:])]
    )


def test_DPF_result_class(mapdl, cube_solve):
    from ansys.mapdl.core.reader.result import DPFResult

    assert isinstance(mapdl.result, DPFResult)


def extract_sections(vm_code, index):
    if not isinstance(index, (int, tuple, list)):
        raise TypeError("'index' should be an integer")

    # Splitting code on lines containing /clear
    vm_code_lines = vm_code.splitlines()
    indexes = [
        ind
        for ind, each in enumerate(vm_code_lines)
        if "/CLEAR" in each.upper().strip()
    ]
    indexes.insert(0, 0)  # Adding index 0 at the beginning.
    indexes.append(len(vm_code_lines))

    if isinstance(index, int):
        index = [index]

    code_ = []
    for each_ in index:
        try:
            selection = vm_code_lines[indexes[each_] : indexes[each_ + 1]]
        except IndexError:
            raise IndexError(
                f"The amount of examples (APDL code blocks separated by '/CLEAR' commands) in this example ('{vm}') is {len(indexes)-1}. "
                "Please use an index value inside that range."
            )
        code_.extend(selection)

    return "\n".join(code_) + "\nSAVE"


def prepare_example(example, index=None, solve=True, stop_after_first_solve=False):
    """Extract the different examples inside each VM. You can also choose to solve or not."""

    with open(example, "r") as fid:
        vm_code = fid.read()

    vm_code = vm_code.upper()

    if not solve:
        vm_code = vm_code.replace("SOLVE", "!SOLVE")

    if stop_after_first_solve:
        return vm_code.replace("SOLVE", "SOLVE\n/EOF")

    if index:
        vm_code = extract_sections(vm_code, index)

    return vm_code


def title(apdl_code):
    line = [each for each in apdl_code if each.strip().startswith("/TITLE")]
    if line:
        return ",".join(line.split(",")[1:])


class TestExample:
    """Generic class to test examples."""

    example = None  # String 'vm33'
    example_name = None  # Example name, used to create a temporal directory
    _temp_dir = None  # Temporal directory where download the RST file to.
    apdl_code = None  # In case you want to overwrite the APDL code of the example. Use with ``prepare_example`` function.

    @property
    def tmp_dir(self):
        if self._temp_dir is None:
            self._temp_dir = os.path.join(
                tempfile.gettempdir(), f"{self.example_name}_reader_temp"
            )
            try:
                os.mkdir(self._temp_dir)
            except FileExistsError:
                pass
        return self._temp_dir

    @pytest.fixture(scope="class")
    def setup(self, mapdl):
        mapdl.clear()
        if self.apdl_code:
            mapdl.input_strings(self.apdl_code)
        else:
            mapdl.input(self.example)
        mapdl.save()
        mapdl.post1()
        mapdl.csys(0)
        return mapdl

    @pytest.fixture(scope="class")
    def reader(self, setup):
        rst_name = setup.jobname + ".rst"
        setup.download_result(self.tmp_dir)
        return read_binary(os.path.join(self.tmp_dir, rst_name))

    @pytest.fixture(scope="class")
    def post(self, setup):
        return setup.post_processing

    @pytest.fixture(scope="class")
    def result(self, setup):
        return setup.result


class TestStaticThermocoupledExample(TestExample):
    """Class to test a Static Thermo-coupled example."""

    example = transient_thermal_stress_in_a_cylinder
    example_name = "transient_thermal_stress_in_a_cylinder"

    @pytest.mark.parametrize("set_", list(range(1, 10)), scope="class")
    def test_compatibility_nodal_temperature(self, mapdl, reader, post, result, set_):
        mapdl.set(1, set_)
        post_values = post.nodal_temperature()
        result_values = result.nodal_temperature(set_)[1]
        reader_values = reader.nodal_temperature(set_ - 1)[1]

        validate(post_values, result_values, reader_values)

    @pytest.mark.parametrize("set_", list(range(1, 10)), scope="class")
    def test_compatibility_nodal_displacement(self, mapdl, reader, post, result, set_):
        mapdl.set(1, set_)
        post_values = post.nodal_displacement("all")[:, :3]
        result_values = result.nodal_displacement(set_)[1]
        reader_values = reader.nodal_displacement(set_ - 1)[1][:, :3]

        validate(result_values, reader_values, post_values)  # Reader results are broken

    @pytest.mark.parametrize("set_", list(range(1, 10)), scope="class")
    def test_compatibility_element_stress(self, mapdl, reader, post, result, set_):
        mapdl.set(1, set_)
        post_values = post.element_stress("x")
        result_values = result.element_stress(set_)[1][:, 0]
        reader_values = reader.element_stress(set_ - 1)[1]
        reader_values = np.array([each[0][0] for each in reader_values])

        validate(result_values, reader_values, post_values)  # Reader results are broken

    def test_hardcoded_values(self, mapdl, result, post):
        """functional tests against vm33.

        Solutions on node 0 and node 90 are tested against hardcode values."""
        # For the post_processing module.
        mapdl.post1()
        set_ = 1
        mapdl.set(1, set_)

        # nodal displacement
        assert result.nodal_displacement(0)
        assert np.allclose(
            result.nodal_displacement(set_)[1],
            post.nodal_displacement("all"),
        )
        node = 0
        assert np.allclose(
            result.nodal_displacement(set_)[1][node],
            np.array([6.552423219981545e-07, 2.860849760514619e-08, 0.0]),
        )
        node = 90
        assert np.allclose(
            result.nodal_displacement(set_)[1][node],
            np.array([5.13308913e-07, -2.24115511e-08, 0.00000000e00]),
        )

        # nodal temperatures
        assert result.nodal_temperature(0)
        assert np.allclose(result.nodal_temperature(set_)[1], post.nodal_temperature())
        node = 0
        assert np.allclose(
            result.nodal_temperature(set_)[1][node], np.array([69.9990463256836])
        )
        node = 90
        assert np.allclose(
            result.nodal_temperature(set_)[1][node], np.array([69.9990463256836])
        )


class TestElectroThermalCompliantMicroactuator(TestExample):
    """Class to test the Electro-Thermal-Compliant Microactuator VM223 example."""

    example = electrothermal_microactuator_analysis
    example_name = "Electro-Thermal-Compliant Microactuator"

    def test_compatibility_nodal_temperature(self, mapdl, reader, post, result):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.nodal_temperature()
        result_values = result.nodal_temperature(set_)[1]
        reader_values = reader.nodal_temperature(set_ - 1)[1]

        validate(post_values, result_values, reader_values)

    def test_compatibility_nodal_displacement(self, mapdl, reader, post, result):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.nodal_displacement("all")[:, :3]
        result_values = result.nodal_displacement(set_)[1]
        reader_values = reader.nodal_displacement(set_ - 1)[1][:, :3]

        validate(result_values, reader_values, post_values)  # Reader results are broken

    def test_compatibility_nodal_voltage(self, mapdl, post, result):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.nodal_voltage()
        result_values = result.nodal_voltage(set_)[1]
        # reader_values = reader.nodal_voltage(set_ - 1)[1]  # Nodal Voltage is not implemented in reader

        # validate(result_values, reader_values, post_values)  # Reader results are broken
        assert np.allclose(post_values, result_values)

    def test_compatibility_element_stress(self, mapdl, reader, post, result):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.element_stress("x")
        result_values = result.element_stress(set_)[1][:, 0]
        reader_values = reader.element_stress(set_ - 1)[1]
        reader_values = np.array([each[0][0] for each in reader_values])

        validate(result_values, reader_values, post_values)  # Reader results are broken


class TestSolidStaticPlastic(TestExample):
    """Test on the vm37."""

    example = elongation_of_a_solid_bar
    apdl_code = prepare_example(example, 0)
    example_name = title(apdl_code)

    def test_compatibility_nodal_displacement(self, mapdl, reader, post, result):
        mapdl.set(1, 1)
        post_values = post.nodal_displacement("all")[:, :3]
        result_values = result.nodal_displacement(1)[1]
        reader_values = reader.nodal_displacement(0)[1][:, :3]

        validate(result_values, reader_values, post_values)  # Reader results are broken

    def test_compatibility_element_stress(self, mapdl, reader, post, result):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.element_stress("x")
        result_values = result.element_stress(set_)[1][:, 0]
        reader_values = reader.element_stress(set_ - 1)[1]
        reader_values = np.array([each[0][0] for each in reader_values])

        validate(result_values, reader_values, post_values)  # Reader results are broken


class TestPiezoelectricRectangularStripUnderPureBendingLoad(TestExample):
    """Class to test the piezoelectric rectangular strip under pure bending load VM231 example."""

    example = piezoelectric_rectangular_strip_under_pure_bending_load
    example_name = "piezoelectric rectangular strip under pure bending load"

    def test_compatibility_nodal_displacement(self, mapdl, reader, post, result):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.nodal_displacement("all")[:, :3]
        result_values = result.nodal_displacement(set_)[1]
        reader_values = reader.nodal_displacement(set_ - 1)[1][:, :3]

        validate(result_values, reader_values, post_values)  # Reader results are broken

    def test_compatibility_nodal_voltage(self, mapdl, post, result):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.nodal_voltage()
        result_values = result.nodal_voltage(set_)[1]
        # reader_values = reader.nodal_voltage(set_ - 1)[1]  # Nodal Voltage is not implemented in reader

        # validate(result_values, reader_values, post_values)  # Reader results are broken
        assert np.allclose(post_values, result_values)

    @pytest.mark.parametrize("comp", [0, 1, 2], scope="class")
    def test_compatibility_element_stress(self, mapdl, reader, post, result, comp):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.element_stress(COMPONENTS[comp])
        result_values = result.element_stress(set_)[1][:, comp]
        reader_values = reader.element_stress(set_ - 1)[1]
        reader_values = np.array([each[comp][0] for each in reader_values])

        validate(result_values, reader_values, post_values)  # Reader results are broken

    @pytest.mark.xfail(
        reason="DPF shows different results with respect to Post and Reader. Interpolation between nodes?"
    )
    @pytest.mark.parametrize("comp", [0, 1, 2], scope="class")
    def test_compatibility_nodal_elastic_strain(
        self, mapdl, reader, post, result, comp
    ):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.nodal_elastic_component_strain(COMPONENTS[comp])
        result_values = result.nodal_elastic_strain(set_)[1][:, comp]
        reader_values = reader.nodal_elastic_strain(set_ - 1)[1][:, comp]
        reader_values[np.isnan(reader_values)] = 0  # Overwriting NaNs with zeros

        validate(result_values, reader_values, post_values)  # Reader results are broken

    def test_selection_nodes(self, mapdl, result, post):
        set_ = 1
        mapdl.set(1, set_)
        mapdl.nsel("s", "node", "", 0, 200)
        nnodes = mapdl.mesh.n_node

        post_values = post.nodal_voltage()
        result_values = result.nodal_voltage(set_)[1]

        assert len(post_values) == nnodes
        assert len(result_values) == nnodes

        assert np.allclose(result_values, post_values)
        mapdl.allsel()

    def test_selection_elements(self, mapdl, result, post):
        set_ = 1
        mapdl.set(1, set_)
        mapdl.esel("s", "elem", "", 0, 200)
        nelem = mapdl.mesh.n_elem

        post_values = post.element_stress("x")
        result_values = result.element_stress(set_)[1][:, 0]

        assert len(post_values) == nelem
        assert len(result_values) == nelem

        assert np.allclose(result_values, post_values)
        mapdl.allsel()
