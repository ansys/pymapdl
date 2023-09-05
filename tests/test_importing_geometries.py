import os

PATH = os.path.dirname(os.path.abspath(__file__))

# Files with CADs
CADs_path = os.path.join(PATH, "test_files", "CAD_formats")


####################################################################
# Reading in all the supported formats


def geometry_test_is_correct(mapdl):
    assert (
        mapdl.geometry.n_volu == 1
    ), f"The number of volumes ({mapdl.geometry.n_volu}) is not correct."
    assert (
        mapdl.geometry.n_area == 8
    ), f"The number of areas ({mapdl.geometry.n_volu}) is not correct."
    assert (
        mapdl.geometry.n_line == 18
    ), f"The number of lines ({mapdl.geometry.n_volu}) is not correct."
    assert (
        mapdl.geometry.n_keypoint == 12
    ), f"The number of keypoints ({mapdl.geometry.n_volu}) is not correct."
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


## IGES
#
def test_readin_igs(mapdl, cleared):
    mapdl.igesin(fname=os.path.join(CADs_path, "CubeWithHole"), ext="igs")
    assert geometry_test_is_correct(mapdl)
    clear_wkdir_from_cads(mapdl)


## Connection commands
#
def test_readin_sat(mapdl, cleared):
    mapdl.satin("CubeWithHole", extension="sat", path=CADs_path, entity="solid", fmt=0)
    assert geometry_test_is_correct(mapdl)
    clear_wkdir_from_cads(mapdl)


def test_readin_catiav5(mapdl, cleared):
    mapdl.upload(os.path.join(CADs_path, "CubeWithHole.CATPart"))
    mapdl.cat5in(name="CubeWithHole", extension="CATPart", entity="solid", fmt=0)
    assert geometry_test_is_correct(mapdl)
    clear_wkdir_from_cads(mapdl)


def test_readin_x_t(mapdl, cleared):
    mapdl.upload(os.path.join(CADs_path, "CubeWithHole.x_t"))
    mapdl.parain(name="CubeWithHole", extension="x_t", entity="solid", fmt=0)
    assert geometry_test_is_correct(mapdl)
    clear_wkdir_from_cads(mapdl)
