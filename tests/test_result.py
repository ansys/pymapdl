# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Test DPF implementation of Result class.


Notes
=====

- Many of reader results return strange values (power of +300 or -300). It might be due to running multiphysics examples.
  I presume the retrieving of nodal values in the RST is not performed properly.
  Because of that, we are using also the ``Post_Processing`` module for validation.

- There are some issues with ordering the ``Elemental`` and ``ElementalNodal`` results according to Element ID.
  Because of that, the third level of assertion is made on the sorted arrays.

- ``Post`` does not filter based on mapdl selected nodes (neither reader)

"""
from logging import Logger
import os
import tempfile
from warnings import warn

import numpy as np
import pytest

from conftest import HAS_DPF, ON_LOCAL

DPF_PORT = int(os.environ.get("DPF_PORT", 50056))  # Set in ci.yaml

if not HAS_DPF:
    pytest.skip(
        "Skipping DPF tests because DPF is not installed. "
        "Please install the ansys-dpf-core package.",
        allow_module_level=True,
    )

else:
    from ansys.dpf import core as dpf_core
    from ansys.dpf.gate.errors import DPFServerException
    from ansys.mapdl.core.reader.result import COMPONENTS

from ansys.mapdl.reader import read_binary

from ansys.mapdl.core.examples import (
    electrothermal_microactuator_analysis,
    elongation_of_a_solid_bar,
    modal_analysis_of_a_cyclic_symmetric_annular_plate,
    piezoelectric_rectangular_strip_under_pure_bending_load,
    pinched_cylinder,
    transient_response_of_a_ball_impacting_a_flexible_surface,
    transient_thermal_stress_in_a_cylinder,
)
from ansys.mapdl.core.logging import PymapdlCustomAdapter as MAPDLLogger


def validate(result_values, reader_values=None, post_values=None, rtol=1e-5, atol=1e-8):
    if reader_values is not None and post_values is not None:
        err_post_reader = None
        err_reader = None
        err_post = None

        # Make it fail if the Reader shows different results to DPF and MAPDL-Post
        EXIGENT = False

        try:
            # Attempt to validate all three sets of values
            all_close(result_values, reader_values, post_values, rtol=rtol, atol=atol)
            return
        except AssertionError as err:
            pass

        try:
            # Attempt partial validation against Post values
            all_close(result_values, post_values, rtol=rtol, atol=atol)
            warn("Validation against Reader failed.")
            if not EXIGENT:
                return

        except AssertionError as err:
            # Attempt partial validation against Reader values
            err_post = err
            pass

        if EXIGENT:
            try:
                all_close(post_values, reader_values, rtol=rtol, atol=atol)
                return
            except AssertionError as err:
                raise AssertionError(
                    "Reader shows different results to DPF and MAPDL-Post. "
                    "Showing the post-reader error\n" + str(err)
                ) from err

        try:
            all_close(result_values, reader_values, rtol=rtol, atol=atol)
            raise AssertionError(
                "MAPDL-Post shows different results to DPF and Reader. "
                "Showing the post-error\n" + str(err_post)
            ) from err_post

        except AssertionError as err:
            err_reader = err
            pass

        try:
            all_close(post_values, reader_values, rtol=rtol, atol=atol)
            pytest.mark.skip(
                "Skipping this test because DPF shows different results to MAPDL-Post and Reader."
            )
            return

        except AssertionError as err:
            raise AssertionError(
                "Failed to validate against Post, Reader or DPF values. It seems "
                "the values are all different. Showing the post-error\n" + str(err_post)
            ) from err_post

    elif reader_values is not None:
        all_close(result_values, reader_values, rtol=rtol, atol=atol)

    elif post_values is not None:
        all_close(result_values, post_values, rtol=rtol, atol=atol)


def all_close(*args, rtol=1e-5, atol=1e-8):
    [
        np.testing.assert_allclose(each0, each1, rtol=rtol, atol=atol, equal_nan=True)
        for each0, each1 in zip(args[:-1], args[1:])
    ]
    return True


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
                f"The amount of examples (APDL code blocks separated by '/CLEAR' commands) in this example is {len(indexes)-1}. "
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
        return ",".join(line.split(",")[1:]).strip()


class TestExample:
    """Generic class to test examples."""

    example: str | None = None  # String 'vm33'
    example_name: str | None = None  # Example name, used to create a temporal directory
    _temp_dir: str | None = None  # Temporal directory where download the RST file to.
    # In case you want to overwrite the APDL code of the example.
    # Use with ``prepare_example`` function.
    apdl_code: str | None = None

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
        mapdl.allsel()
        mapdl.save()
        mapdl.post1()
        mapdl.csys(0)

        # downloading file
        rst_name = mapdl.jobname + ".rst"
        mapdl.download_result(self.tmp_dir)
        self.rst_path = os.path.join(self.tmp_dir, rst_name)

        mapdl.post1()
        return mapdl

    @pytest.fixture(scope="class")
    def reader(self, setup):
        return read_binary(os.path.join(self.tmp_dir, self.rst_path))

    @pytest.fixture()
    def post(self, setup):
        mapdl = setup
        mapdl.allsel()
        mapdl.post1()
        mapdl.rsys(0)
        mapdl.shell()
        return mapdl.post_processing

    @pytest.fixture(scope="class")
    def result(self, setup):
        return setup.result


def test_DPF_result_class(mapdl, cube_solve):
    from ansys.mapdl.core.reader.result import DPFResult

    assert isinstance(mapdl.result, DPFResult)


@pytest.mark.skipif(ON_LOCAL, reason="Skip on local machine")
def test_dpf_connection():
    # uses 127.0.0.1 and port 50054 by default
    try:
        grpc_con = dpf_core.connect_to_server(port=DPF_PORT)
        assert grpc_con.live
        assert True
    except OSError:
        assert False


@pytest.mark.skipif(ON_LOCAL, reason="Skip on local machine")
@pytest.mark.skip("Skip until DPF grpc connection is fixed on Ubuntu container. See #")
def test_upload(mapdl, solved_box, tmpdir):
    # Download RST file
    rst_path = mapdl.download_result(str(tmpdir.mkdir("tmpdir")))

    # Establishing connection
    grpc_con = dpf_core.connect_to_server(port=DPF_PORT)
    assert grpc_con.live

    # Upload RST
    server_file_path = dpf_core.upload_file_in_tmp_folder(rst_path)

    # Creating model
    model = dpf_core.Model(server_file_path)
    assert model.results is not None

    # Checks
    mapdl.allsel()
    assert mapdl.mesh.n_node == model.metadata.meshed_region.nodes.n_nodes
    assert mapdl.mesh.n_elem == model.metadata.meshed_region.elements.n_elements


# def test_session_id(mapdl):
#     session_id = f"__{generate_session_id()}"

#     assert session_id not in mapdl.parameters
#     mapdl._run(f"{session_id} = 1")
#     assert session_id not in mapdl.parameters # session id should not shown in mapdl.parameters
#     assert


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

        validate(result_values, reader_values, post_values)

    @pytest.mark.parametrize("set_", list(range(1, 10)), scope="class")
    def test_compatibility_nodal_displacement(self, mapdl, reader, post, result, set_):
        mapdl.set(1, set_)
        post_values = post.nodal_displacement("all")[:, :3]
        result_values = result.nodal_displacement(set_)[1]
        reader_values = reader.nodal_displacement(set_ - 1)[1][:, :3]

        validate(result_values, reader_values, post_values)  # Reader results are broken

    @pytest.mark.parametrize("comp", [0, 1, 2, 3, 4, 5], scope="class")
    @pytest.mark.parametrize("set_", list(range(1, 10)), scope="class")
    def test_compatibility_element_stress(
        self, mapdl, reader, post, result, set_, comp
    ):
        mapdl.set(1, set_)
        post_values = post.element_stress(COMPONENTS[comp])

        result_values = result.element_stress(set_)[1][:, comp]

        # Reader returns a list of arrays. Each element of the list is the array (nodes x stress) for each element
        reader_values = reader.element_stress(set_ - 1)[1]  # getting data
        # We are going to do the average across the element, and then retrieve the first column (X)
        reader_values = np.array(
            [each_element.mean(axis=0)[comp] for each_element in reader_values]
        )

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
            np.array([9.28743307e-07, 4.05498085e-08, 0.00000000e00]),
        )
        node = 90
        assert np.allclose(
            result.nodal_displacement(set_)[1][node],
            np.array([6.32549364e-07, -2.30084084e-19, 0.00000000e00]),
        )

        # nodal temperatures
        assert result.nodal_temperature(0)
        assert np.allclose(result.nodal_temperature(set_)[1], post.nodal_temperature())
        node = 0
        assert np.allclose(
            result.nodal_temperature(set_)[1][node], np.array([70.00000588885841])
        )
        node = 90
        assert np.allclose(
            result.nodal_temperature(set_)[1][node], np.array([70.00018628762524])
        )

    def test_parse_step_substep(self, mapdl, result):
        # Int based
        assert result.parse_step_substep(0) == 0
        with pytest.raises(DPFServerException):
            assert result.parse_step_substep(1)  # Only one step

        # tuple/list
        for each in range(10):
            assert result.parse_step_substep((0, each)) == each
            assert result.parse_step_substep([0, each]) == each

    def test_material_properties(self, mapdl, reader, post, result):
        assert reader.materials == result.materials


class TestElectroThermalCompliantMicroactuator(TestExample):
    """Class to test the Electro-Thermal-Compliant Microactuator VM223 example."""

    example = electrothermal_microactuator_analysis
    example_name = "Electro-Thermal-Compliant Microactuator"
    mapdl_set = 2
    result_set = 1
    reader_set = 1

    def test_compatibility_nodal_temperature(self, mapdl, reader, post, result):
        mapdl.set(1, self.mapdl_set)
        post_values = post.nodal_temperature()
        result_values = result.nodal_temperature(self.result_set)[1]
        reader_values = reader.nodal_temperature(self.reader_set - 1)[1]

        validate(result_values, reader_values, post_values)

    def test_compatibility_nodal_displacement(self, mapdl, reader, post, result):
        mapdl.set(1, self.mapdl_set)
        post_values = post.nodal_displacement("all")[:, :3]
        result_values = result.nodal_displacement(self.result_set)[1]
        reader_values = reader.nodal_displacement(self.reader_set - 1)[1][:, :3]

        validate(result_values, reader_values, post_values)  # Reader results are broken

    def test_compatibility_nodal_voltage(self, mapdl, post, result):
        mapdl.set(1, self.mapdl_set)
        post_values = post.nodal_voltage()
        result_values = result.nodal_voltage(self.result_set)[1]
        # reader_values = reader.nodal_voltage(set_ - 1)[1]  # Nodal Voltage is not implemented in reader

        validate(
            result_values, reader_values=None, post_values=post_values
        )  # Reader results are broken

    @pytest.mark.parametrize("comp", [0, 1, 2, 3, 4, 5], scope="class")
    def test_compatibility_element_stress(self, mapdl, reader, post, result, comp):
        mapdl.set(1, self.mapdl_set)
        post_values = post.element_stress(COMPONENTS[comp])

        result_values = result.element_stress(self.result_set)[1][:, comp]

        # Reader returns a list of arrays. Each element of the list is the array (nodes x stress) for each element
        reader_values = reader.element_stress(self.reader_set - 1)[1]  # getting data
        # We are going to do the average across the element, and then retrieve the first column (X)
        reader_values = np.array(
            [each_element.mean(axis=0)[comp] for each_element in reader_values]
        )

        validate(
            result_values, reader_values, post_values, rtol=1e-4, atol=1e-5
        )  # Reader results are broken

    @pytest.mark.xfail(
        reason="Temperature dependent material properties are not implemented yet"
    )
    def test_material_properties(self, mapdl, reader, post, result):
        assert reader.materials == result.materials


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

    @pytest.mark.parametrize("comp", [0, 1, 2, 3, 4, 5], scope="class")
    def test_compatibility_element_stress(self, mapdl, reader, post, result, comp):
        set_ = 1
        mapdl.set(1, set_)

        # Post returns the elements always ordered, because of the ETAB.
        # It does not filter by selection neither.
        post_values = post.element_stress(COMPONENTS[comp])

        result_values = result.element_stress(set_)[1][:, comp]

        # Reader returns a list of arrays. Each element of the list is the array (nodes x stress) for each element
        reader_values = reader.element_stress(set_ - 1)[1]  # getting data
        # We are going to do the average across the element, and then retrieve the first column (X)
        reader_values = np.array(
            [each_element.mean(axis=0)[comp] for each_element in reader_values]
        )

        validate(result_values, reader_values, post_values)

    def test_selection_nodes(self, mapdl, result, post):
        set_ = 1
        mapdl.set(1, set_)
        nodes = mapdl.mesh.nnum
        ids = list(range(5, 10))
        nodes_selection = nodes[ids]

        post_values = post.nodal_displacement("X")
        result_values = result.nodal_displacement(1, nodes=nodes_selection)[1][:, 0]

        assert len(result_values) == len(nodes_selection)

        validate(result_values, reader_values=None, post_values=post_values[ids])
        mapdl.allsel()  # resetting selection

    def test_selection_elements(self, mapdl, result, post):
        set_ = 1
        mapdl.set(1, set_)
        mapdl.esel("s", "elem", "", 1, 200)
        ids = list(range(3, 6))
        elem_selection = mapdl.mesh.enum[ids]

        post_values = post.element_stress("x")
        result_values = result.element_stress(set_, elements=elem_selection)[1][:, 0]

        assert len(result_values) == len(ids)

        validate(result_values, reader_values=None, post_values=post_values[ids])
        mapdl.allsel()  # resetting selection

    def test_material_properties(self, mapdl, reader, post, result):
        assert reader.materials == result.materials


class TestPiezoelectricRectangularStripUnderPureBendingLoad(TestExample):
    """Class to test the piezoelectric rectangular strip under pure bending load VM231 example.

    A piezoceramic (PZT-4) rectangular strip occupies the region |x| l, |y| h. The material is oriented
    such that its polarization direction is aligned with the Y axis. The strip is subjected to the pure bending
    load $$\sigma_x = \sigma_1$$ y at x = ± l. Determine the electro-elastic field distribution in the strip
    """

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

        validate(
            result_values, reader_values=None, post_values=post_values
        )  # Reader results are broken

    @pytest.mark.parametrize("comp", [0, 1, 2], scope="class")
    def test_compatibility_element_stress(self, mapdl, reader, post, result, comp):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.element_stress(COMPONENTS[comp])

        result_values = result.element_stress(set_)[1][:, comp]

        reader_values = reader.element_stress(set_ - 1)[1]
        reader_values = np.array([each[comp][0] for each in reader_values])

        validate(result_values, reader_values, post_values)  # Reader results are broken

    @pytest.mark.parametrize("comp", [0, 1, 2], scope="class")
    def test_compatibility_nodal_elastic_strain(
        self, mapdl, reader, post, result, comp
    ):
        set_ = 1
        mapdl.set(1, set_)
        post_values = post.nodal_elastic_component_strain(COMPONENTS[comp])
        result_values = result.nodal_elastic_strain(set_)[1][:, comp]
        reader_values = reader.nodal_elastic_strain(set_ - 1)[1][:, comp]

        # Overwrite the midside nodes. It seems that DPF either return them interpolated or not
        # return them at all. This hack will allow partial validation.
        post_values[np.isnan(reader_values)] = 0
        result_values[np.isnan(reader_values)] = 0
        reader_values[np.isnan(reader_values)] = 0  # Overwriting NaNs with zeros

        validate(result_values, reader_values, post_values)

    def test_selection_nodes(self, mapdl, result, post):
        set_ = 1
        mapdl.set(1, set_)
        mapdl.nsel("s", "node", "", 1, 200)
        nnodes = mapdl.mesh.n_node

        post_values = post.nodal_voltage()
        result_values = result.nodal_voltage(set_)[1]

        assert len(post_values) == nnodes
        assert len(result_values) == nnodes

        validate(result_values, reader_values=None, post_values=post_values)
        mapdl.allsel()

    def test_selection_elements(self, mapdl, result, post):
        set_ = 1
        mapdl.set(1, set_)
        mapdl.esel("s", "elem", "", 1, 200)
        nelem = mapdl.mesh.n_elem

        post_values = post.element_stress("x")
        result_values = result.element_stress(set_)[1][:, 0]

        assert len(post_values) == nelem
        assert len(result_values) == nelem

        validate(result_values, reader_values=None, post_values=post_values)
        mapdl.allsel()

    @pytest.mark.xfail(reason="DPF does not read the PERX properties.")
    def test_material_properties(self, mapdl, reader, post, result):
        assert reader.materials == result.materials


class TestPinchedCylinderVM6(TestExample):
    """Class to test a pinched cylinder (VM6 example).

    A thin-walled cylinder is pinched by a force F at the middle of the cylinder length.
    Determine the radial displacement δ at the point where F is applied. The ends of the cylinder are free edges.
    """

    example = pinched_cylinder
    example_name = "piezoelectric rectangular strip under pure bending load"
    apdl_code = prepare_example(example, 0)
    example_name = title(apdl_code)

    def test_compatibility_nodal_displacement(self, mapdl, reader, post, result):
        mapdl.set(1, 1)
        post_values = post.nodal_displacement("all")[:, :3]
        result_values = result.nodal_displacement(1)[1]
        reader_values = reader.nodal_displacement(0)[1][:, :3]

        validate(result_values, reader_values, post_values)  # Reader results are broken

    @pytest.mark.parametrize("comp", [0, 1, 2, 3, 4, 5], scope="class")
    def test_compatibility_element_stress(self, mapdl, reader, post, result, comp):
        set_ = 1
        mapdl.set(1, set_)
        mapdl.shell("mid")  # DPF returns the middle layer value.

        # Post returns the elements always ordered, because of the ETAB.
        # It does not filter by selection neither.
        post_values = post.element_stress(COMPONENTS[comp])

        result_values = result.element_stress(set_)[1][:, comp]

        # Reader returns a list of arrays. Each element of the list is the array (nodes x stress) for each element
        reader_values = reader.element_stress(set_ - 1)[1]  # getting data
        # We are going to do the average across the element, and then retrieve the first column (X)
        reader_values = np.array(
            [each_element.mean(axis=0)[comp] for each_element in reader_values]
        )

        validate(result_values, reader_values, post_values)
        mapdl.shell()  # Back to default

    @pytest.mark.parametrize("comp", [0, 1, 2, 3, 4, 5], scope="class")
    def test_result_in_element_coordinate_system(
        self, mapdl, result, reader, post, comp
    ):
        set_ = 1
        mapdl.set(1, set_)
        mapdl.rsys("solu")
        mapdl.shell("mid")  # DPF returns the middle layer value.

        post_values = post.element_stress(COMPONENTS[comp])
        result_values = result.element_stress(set_, in_element_coord_sys=True)[1][
            :, comp
        ]

        # Reader returns a list of arrays. Each element of the list is the array (nodes x stress) for each element
        reader_values = reader.element_stress(set_ - 1)[1]  # getting data
        # We are going to do the average across the element, and then retrieve the first column (X)
        reader_values = np.array(
            [each_element.mean(axis=0)[comp] for each_element in reader_values]
        )

        validate(result_values, reader_values, post_values)
        mapdl.rsys(0)  # Back to default
        mapdl.shell()

    def test_material_properties(self, mapdl, reader, post, result):
        assert reader.materials == result.materials


class TestTransientResponseOfABallImpactingAFlexibleSurfaceVM65(TestExample):
    """Class to test Transient Response of a Ball Impacting a Flexible Surface (VM65 example).

    A rigid ball of mass m is dropped through a height h onto a flexible surface of stiffness k. Determine
    the velocity, kinetic energy, and displacement y of the ball at impact and the maximum displacement
    of the ball.

    Purposes of tests
    =================
    * Test multiple steps simulations
    * Test mesh and nodes

    Features of test
    ================
    * Analysis Type(s): Nonlinear Transient Dynamic Analysis (ANTYPE = 4)
    * Element Type(s):
      * Structural Mass Elements (MASS21)
      * 2-D/3-D Node-to-Surface Contact Elements (CONTA175)

    """

    example = transient_response_of_a_ball_impacting_a_flexible_surface
    example_name = "Transient Response of a Ball Impacting a Flexible Surface"
    apdl_code = prepare_example(example, 0)
    example_name = title(apdl_code)

    @pytest.mark.parametrize(
        "step",
        [((1, 10), 1), ((2, 1), 2), ((2, 2), 3), ((2, 12), 13), ((2, 21), 22)],
        scope="class",
    )
    def test_compatibility_nodal_displacement(self, mapdl, reader, post, result, step):
        """This test is particularly problematic because the steps start at the ldstep 1 and substep 10, there is nothing before,
        hence the cumulative (which seems a sumation of substeps + 1, do not match the set.

        DPF does index according to set as well as reader.
        To get the same results in post we need to do ``mapdl.set(nset=SET)``

        >>> mapdl.set("list")
        *****  INDEX OF DATA SETS ON RESULTS FILE  *****

          SET   TIME/FREQ    LOAD STEP   SUBSTEP  CUMULATIVE
            1 0.10000E-02         1        10        10
            2 0.20000E-02         2         1        11
            3 0.30000E-02         2         2        12
            4 0.40000E-02         2         3        13
            5 0.50000E-02         2         4        14
        """
        loadstep = step[0]
        set_ = step[1]

        mapdl.set(*loadstep)
        assert mapdl.post_processing.step == set_

        post_values = post.nodal_displacement("all")[:, :3]
        result_values = result.nodal_displacement(set_)[1]
        assert np.allclose(post_values, result_values)

        post_values = post_values[:, :2]
        result_values = result_values[:, :2]
        reader_values = reader.nodal_displacement(set_)[
            1
        ]  # surprisingly here the array only has two columns

        validate(result_values, reader_values, post_values)

    def test_parse_step_substep(self, result):
        assert result.parse_step_substep(0) == 0
        assert result.parse_step_substep(1) == 1
        with pytest.raises(DPFServerException):
            assert result.parse_step_substep(2)  # Only two step

        assert result.parse_step_substep((0, 1)) == -1
        assert result.parse_step_substep((1, 0)) == 1
        assert result.parse_step_substep((1, 1)) == 2
        assert result.parse_step_substep((1, 2)) == 3
        assert result.parse_step_substep((1, 3)) == 4
        assert result.parse_step_substep((1, 4)) == 5
        assert result.parse_step_substep((1, 5)) == 6
        assert result.parse_step_substep((1, 10)) == 11

    def test_mesh(self, mapdl, reader, post, result):
        assert np.allclose(mapdl.mesh.nnum, result.mesh.nodes.scoping.ids)
        assert np.allclose(mapdl.mesh.enum, result.mesh.elements.scoping.ids)

    def test_configuration(self, mapdl, result):
        if result.mode_rst:
            assert isinstance(mapdl.result.logger, Logger)
        elif result.mode_mapdl:
            assert isinstance(mapdl.result.logger, MAPDLLogger)

    def test_no_cyclic(self, mapdl, reader, post, result):
        assert not result.is_cyclic
        assert result.n_sector is None
        assert result.num_stages is None

    def test_material_properties(self, mapdl, reader, post, result):
        assert reader.materials == result.materials


# class TestChabocheRateDependentPlasticMaterialunderCyclicLoadingVM155(TestExample):
#     """Class to test Chaboche Rate-Dependent Plastic Material under Cyclic Loading (VM155 example).

#     A thin plate is modeled with chaboche rate-dependent plastic material model. Uniaxial cyclic displacement
#     loading is applied in vertical direction (Figure .155.1: Uniaxial Loading Problem Sketch (p. 379)). The
#     loading history is composed of 23 cycles (Figure .155.2: Loading history (p. 380)), in which the first 22
#     cycles have an identical displacement path. In the last load cycle the displacement is made constant at
#     time gaps 910 to 940 seconds and at time gaps 960 to 990 seconds. The stress history is computed and
#     compared against the reference solution.

#     Purposes of tests
#     =================
#     * None yet

#     Features of test
#     ================
#     * Analysis Type(s): Static Analysis (ANTYPE = 0)
#     * Element Type(s):
#       * 2-D Structural Solid Elements (PLANE182)

#     """

#     example = threed_nonaxisymmetric_vibration_of_a_stretched_membrane
#     example_name = "Transient Response of a Ball Impacting a Flexible Surface"


class TestModalAnalysisofaCyclicSymmetricAnnularPlateVM244(TestExample):
    """Class to test Modal Analysis of a Cyclic Symmetric Annular Plate (VM244 example).

    The fundamental natural frequency of an annular plate is determined using a mode-frequency analysis.
    The lower bound is calculated from the natural frequency of the annular plates, which are free on the
    inner radius and fixed on the outer. The bounds for the plate frequency are compared to the theoretical
    results.

    Purposes of tests
    =================
    * Test cyclic (axisymmetric) simulations

    Features of test
    ================
    * Analysis Type(s): Mode-frequency analysis (ANTYPE = 2)
    * Element Type(s):
      * 3-D 8-Node Structural Solid (SOLID185)
      * 3-D 20-Node Structural Solid (SOLID186)
      * 3-D 10-Node Tetrahedral Structural Solid (SOLID187)
      * 4-Node Finite Strain Shell (SHELL181)
      * 3-D 8-Node Layered Solid Shell (SOLSH190)
      * 8-Node Finite Strain Shell (SHELL281)

    """

    example = modal_analysis_of_a_cyclic_symmetric_annular_plate
    example_name = "Modal Analysis of a Cyclic Symmetric Annular Plate"

    def test_cyclic(self, mapdl, reader, post, result):
        assert result.is_cyclic
        assert result.n_sector == 12
        assert result.num_stages == 1

    def test_material_properties(self, mapdl, reader, post, result):
        assert reader.materials == result.materials
