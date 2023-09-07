import os

import pytest

from ansys.mapdl.core.errors import MapdlInvalidRoutineError, MapdlRuntimeError
from conftest import ON_CI, ON_LOCAL

PATH = os.path.dirname(os.path.abspath(__file__))

# Files with CADs
CADs_path = os.path.join(PATH, "test_files", "CAD_formats")


####################################################################
# Reading in all the supported formats


def geometry_test_is_correct(mapdl, geometry=None):
    if geometry == "iges":
        entities = [0, 8, 36, 44]
    else:
        entities = [1, 8, 18, 12]

    assert (
        mapdl.geometry.n_keypoint == entities[3]
    ), f"The number of keypoints ({mapdl.geometry.n_keypoint}) is not correct."
    assert (
        mapdl.geometry.n_line == entities[2]
    ), f"The number of lines ({mapdl.geometry.n_line}) is not correct."
    assert (
        mapdl.geometry.n_area == entities[1]
    ), f"The number of areas ({mapdl.geometry.n_area}) is not correct."
    assert (
        mapdl.geometry.n_volu == entities[0]
    ), f"The number of volumes ({mapdl.geometry.n_volu}) is not correct."
    return True


def clear_wkdir_from_cads(mapdl):
    """Cleaning files because we don't want to reuse the ANF files"""
    list_files = [
        each for each in mapdl.list_files() if each.startswith("CubeWithHole")
    ]
    for each_file in list_files:
        try:
            mapdl.slashdelete(each_file)
        except IOError:
            pass


class NullContext:
    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

    def __init__(self):
        pass


## IGES
#
def test_readin_igs(mapdl, cleared):
    mapdl.igesin(fname=os.path.join(CADs_path, "CubeWithHole"), ext="igs")
    assert geometry_test_is_correct(mapdl, geometry="iges")

    nareas = mapdl.geometry.n_area

    # Generating the volumes
    mapdl.prep7()
    mapdl.nummrg("kp")
    mapdl.va("all")

    assert mapdl.geometry.n_volu == 1
    assert nareas == mapdl.geometry.n_area
    # Rest of the entities are not maintained because of the nummrg.

    clear_wkdir_from_cads(mapdl)


## Connection commands
#
def test_readin_sat(mapdl, cleared):
    if ON_CI and mapdl.version >= 23.2:
        context = pytest.raises(
            MapdlRuntimeError, match="Specified library does not exist."
        )
    elif ON_CI and ON_LOCAL:
        context = pytest.raises(MapdlRuntimeError, match="anf does not exist.")
    elif ON_CI:
        context = pytest.raises(AssertionError)
    else:
        context = NullContext()

    with context:
        mapdl.satin(
            "CubeWithHole", extension="sat", path=CADs_path, entity="solid", fmt=0
        )
        assert geometry_test_is_correct(mapdl)
    clear_wkdir_from_cads(mapdl)


def test_readin_x_t(mapdl, cleared):
    if ON_CI and mapdl.version >= 23.2:
        context = pytest.raises(
            MapdlRuntimeError, match="Specified library does not exist."
        )

    elif ON_CI and mapdl.version == 23.1:
        context = pytest.raises(MapdlRuntimeError, match="does not exist")

    elif ON_CI and ON_LOCAL:
        context = pytest.raises(AssertionError)

    elif ON_CI:
        context = pytest.raises(MapdlRuntimeError, match="anf does not exist.")

    else:
        context = NullContext()

    with context:
        mapdl.parain(
            name="CubeWithHole", extension="x_t", path=CADs_path, entity="solid", fmt=0
        )
        assert geometry_test_is_correct(mapdl)

    clear_wkdir_from_cads(mapdl)


def test_readin_catiav5(mapdl, cleared):
    if ON_CI:
        context = pytest.raises(
            MapdlInvalidRoutineError, match=" ~CAT5IN is not a recognized"
        )
    else:
        context = NullContext()

    with context:
        mapdl.cat5in(
            name="CubeWithHole",
            extension="CATPart",
            path=CADs_path,
            entity="solid",
            fmt=0,
        )
        assert geometry_test_is_correct(mapdl)

    clear_wkdir_from_cads(mapdl)
