"""Test MAPDL interface"""
import os
import time

import numpy as np
import pytest
from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.misc import random_string
from ansys.mapdl.reader import examples
from pyvista import PolyData
from pyvista.plotting import system_supports_plotting
from pyvista.plotting.renderer import CameraPosition

from ansys.mapdl.core.launcher import get_start_instance, launch_mapdl

skip_no_xserver = pytest.mark.skipif(
    not system_supports_plotting(), reason="Requires active X Server"
)

skip_in_cloud = pytest.mark.skipif(
    not get_start_instance(),
    reason="""
Must be able to launch MAPDL locally. Remote execution does not allow for
directory creation.
"""
)


CMD_BLOCK = """/prep7
! Mat
MP,EX,1,200000
MP,NUXY,1,0.3
MP,DENS,1,7.85e-09
! Elements
et,1,186
et,2,154
! Geometry
BLC4,0,0,1000,100,10
! Mesh
esize,5
vmesh,all
"""

## Testing CDREAD and CDWRITE
# DB file generated locally with ANSYS.
# Many of the commands could be deleted, but for the sake of good
# testing we are going to leave them.

CDB_FILE = """                                                                        S      1
/COM,ANSYS RELEASE 12.1BETAUP20090531       10:26:32    06/01/2009      S      2
/NOPR                                                                   S      3
/PREP7                                                                  S      4
/TITLE,                                                                 S      5
1H,,1H;,,18Hdisc_pad_model.cdb,                                         G      1
5HANSYS,22H  12.1BETA  UP20090531,,,,,,,1.0,,,,,13H000601.102632,       G      2
1.0000E-04,,,,9,,;                                                      G      3
S     29G      3D      0P      0                                        T      1
:CDWRITE      ! START OF CDWRITE DATA
/COM,ANSYS RELEASE 2021 R2           BUILD 21.2
/PREP7
/NOPR
/TITLE,'CDREAD and CDWRITE tests'
*IF,_CDRDOFF,EQ,1,THEN     !if solid model was read in
_CDRDOFF=             !reset flag, numoffs already performed
*ELSE              !offset database for the following FE model
*ENDIF
*SET,T_PAR,'asdf1234'
*SET,_RETURN ,  0.000000000000
*SET,_STATUS ,  0.000000000000
*SET,_UIQR   ,  1.000000000000
DOF,DELETE
EXTOPT,ATTR,      0,      0,      0
EXTOPT,ESIZE,  0,  0.0000
EXTOPT,ACLEAR,      0
TREF,  0.00000000
IRLF,  0
BFUNIF,TEMP,_TINY
ACEL,  0.00000000    ,  0.00000000    ,  0.00000000
OMEGA,  0.00000000    ,  0.00000000    ,  0.00000000
DOMEGA,  0.00000000    ,  0.00000000    ,  0.00000000
CGLOC,  0.00000000    ,  0.00000000    ,  0.00000000
CGOMEGA,  0.00000000    ,  0.00000000    ,  0.00000000
DCGOMG,  0.00000000    ,  0.00000000    ,  0.00000000

KUSE,     0
TIME,  0.00000000
ALPHAD,  0.00000000
BETAD,  0.00000000
DMPRAT,  0.00000000
DMPSTR,  0.00000000
CRPLIM, 0.100000000    ,   0
CRPLIM,  0.00000000    ,   1
NCNV,     1,  0.00000000    ,     0,  0.00000000    ,  0.00000000
NEQIT,     0

ERESX,DEFA
/GO
FINISH
"""


def clearing_cdread_cdwrite_tests(mapdl):
    mapdl.finish(mute=True)
    # *MUST* be NOSTART.  With START fails after 20 calls...
    # this has been fixed in later pymapdl and MAPDL releases
    mapdl.clear("NOSTART", mute=True)
    mapdl.prep7(mute=True)


def asserting_cdread_cdwrite_tests(mapdl):
    # Using ``in`` because of the padding APDL does on strings.
    return 'asdf1234' in mapdl.parameters['T_PAR']


def warns_in_cdread_error_log(mapdl):
    """Check for specific warns in the error log associated with using /INPUT with CDB files
    instead of CDREAD command."""
    error_files = [each for each in os.listdir(mapdl.directory) if each.endswith('.err')]

    # "S 1", "1 H" and "5 H Ansys" are character at the end of lines in the CDB_FILE variable.
    # They are allowed in the CDREAD command, but it gives warnings in the /INPUT command.
    warn_cdread_1 = "S1 is not a recognized"
    warn_cdread_2 = "1H is not a recognized"
    warn_cdread_3 = "5HANSYS is not a recognized"

    warns = []
    for each in error_files:
        with open(os.path.join(mapdl.directory, each)) as fid:
            error_log = ''.join(fid.readlines())
        warns.append((warn_cdread_1 in error_log) or (warn_cdread_2 in error_log) or (warn_cdread_3 in error_log))
        return any(warns)


@pytest.fixture(scope="function")
def make_block(mapdl, cleared):
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, 186)
    mapdl.esize(0.25)
    mapdl.vmesh("ALL")


@pytest.mark.skip_grpc
def test_internal_name_grpc(mapdl):
    assert str(mapdl._ip) in mapdl._name
    assert str(mapdl._port) in mapdl._name
    assert 'GRPC' in mapdl._name


def test_jobname(mapdl, cleared):
    jobname = "abcdefg"
    assert mapdl.jobname != jobname
    mapdl.finish()
    mapdl.filname(jobname)
    assert mapdl.jobname == jobname

    other_jobname = "gfedcba"
    mapdl.jobname = other_jobname
    assert mapdl.jobname == other_jobname


@pytest.mark.skip_grpc
def test_server_version(mapdl):
    if mapdl.version == 20.2:
        assert mapdl._server_version == (0, 0, 0)
    elif mapdl.version == 21.1:
        assert mapdl._server_version == (0, 3, 0)
    elif mapdl.version == 21.2:
        assert mapdl._server_version in [(0, 4, 0), (0, 4, 1)]
    else:
        # untested future version
        assert isinstance(mapdl._server_version, tuple)
        assert mapdl._server_version[1] >= 4
        assert mapdl._server_version[0] >= 0


@pytest.mark.skip_grpc
def test_global_mute(mapdl):
    mapdl.mute = True
    assert mapdl.mute is True
    assert mapdl.prep7() == ""

    # commands like /INQUIRE must always return something
    jobname = "file"
    mapdl.jobname = jobname
    assert mapdl.inquire("JOBNAME") == jobname
    mapdl.mute = False


def test_parsav_parres(mapdl, cleared, tmpdir):
    arr = np.random.random((10, 3))
    mapdl.parameters["MYARR"] = arr
    mapdl.parsav("ALL", "tmp.txt")
    mapdl.clear()
    mapdl.parres("ALL", "tmp.txt")
    assert np.allclose(mapdl.parameters["MYARR"], arr)


@pytest.mark.skip_grpc
def test_no_results(mapdl, cleared, tmpdir):
    pth = str(tmpdir.mkdir("tmpdir"))
    mapdl.jobname = random_string()
    with pytest.raises(FileNotFoundError):
        mapdl.download_result(pth)


def test_empty(mapdl):
    with pytest.raises(ValueError):
        mapdl.run("")


def test_multiline_fail(mapdl):
    with pytest.raises(ValueError, match="Use ``run_multiline``"):
        mapdl.run(CMD_BLOCK)


def test_multiline_fail(mapdl, cleared):
    resp = mapdl.run_multiline(CMD_BLOCK)
    assert "IS SOLID186" in resp, "not capturing the beginning of the block"
    assert "GENERATE NODES AND ELEMENTS" in resp, "not capturing the end of the block"


def test_str(mapdl):
    mapdl_str = str(mapdl)
    assert "Product:" in mapdl_str
    assert "MAPDL Version" in mapdl_str
    try:
        assert str(mapdl.version) in mapdl_str
    except:
        breakpoint()


def test_version(mapdl):
    assert isinstance(mapdl.version, float)


def test_comment(cleared, mapdl):
    comment = "Testing..."
    resp = mapdl.com(comment)
    assert comment in resp


def test_basic_command(cleared, mapdl):
    resp = mapdl.prep7()
    resp = mapdl.finish()
    assert "ROUTINE COMPLETED" in resp


def test_allow_ignore(mapdl):
    mapdl.clear()
    mapdl.allow_ignore = False
    assert mapdl.allow_ignore is False
    with pytest.raises(pymapdl.errors.MapdlInvalidRoutineError):
        mapdl.k()

    # Does not create keypoints and yet does not raise error
    mapdl.allow_ignore = True
    assert mapdl.allow_ignore is True
    mapdl.k()
    assert mapdl.geometry.n_keypoint == 0
    mapdl.allow_ignore = False


def test_chaining(mapdl, cleared):
    mapdl.prep7()
    n_kp = 1000
    with mapdl.chain_commands:
        for i in range(1, 1 + n_kp):
            mapdl.k(i, i, i, i)

    assert mapdl.geometry.n_keypoint == 1000


def test_error(mapdl):
    with pytest.raises(MapdlRuntimeError):
        mapdl.a(0, 0, 0, 0)


def test_ignore_error(mapdl):
    mapdl.ignore_errors = False
    assert not mapdl.ignore_errors
    mapdl.ignore_errors = True
    assert mapdl.ignore_errors is True

    # verify that an error is not raised
    out = mapdl._run("A, 0, 0, 0")
    assert "*** ERROR ***" in out

    mapdl.ignore_error = False
    assert mapdl.ignore_error is False


@pytest.mark.skip_grpc
def test_list(mapdl, tmpdir):
    """Added for backwards compatibility"""
    fname = "tmp.txt"
    filename = str(tmpdir.mkdir("tmpdir").join(fname))
    txt = "this is a test"
    with open(filename, "w") as fid:
        fid.write(txt)
    mapdl.upload(filename)

    output = mapdl.list(fname)
    assert output == txt


@pytest.mark.skip_grpc
def test_invalid_input(mapdl):
    with pytest.raises(FileNotFoundError):
        mapdl.input("thisisnotafile")


@skip_no_xserver
def test_kplot(cleared, mapdl, tmpdir):
    mapdl.k("", 0, 0, 0)
    mapdl.k("", 1, 0, 0)
    mapdl.k("", 1, 1, 0)
    mapdl.k("", 0, 1, 0)

    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    cpos = mapdl.kplot(savefig=filename)
    assert isinstance(cpos, CameraPosition)
    assert os.path.isfile(filename)

    mapdl.kplot(vtk=False)  # make sure legacy still works


@skip_no_xserver
def test_aplot(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)
    mapdl.al(l0, l1, l2, l3)
    mapdl.aplot(show_area_numbering=True)
    mapdl.aplot(color_areas=True, show_lines=True, show_line_numbering=True)

    mapdl.aplot(quality=100)
    mapdl.aplot(quality=-1)

    # and legacy as well
    mapdl.aplot(vtk=False)


@skip_no_xserver
@pytest.mark.parametrize("vtk", [True, False])
def test_vplot(cleared, mapdl, vtk):
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.vplot(vtk=vtk, color_areas=True)


def test_keypoints(cleared, mapdl):
    assert mapdl.geometry.n_keypoint == 0
    kps = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]

    i = 1
    knum = []
    for x, y, z in kps:
        mapdl.k(i, x, y, z)
        knum.append(i)
        i += 1

    assert mapdl.geometry.n_keypoint == 4
    assert np.allclose(kps, mapdl.geometry.keypoints)
    assert np.allclose(knum, mapdl.geometry.knum)


def test_lines(cleared, mapdl):
    assert mapdl.geometry.n_line == 0

    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)

    lines = mapdl.geometry.lines
    assert isinstance(lines, PolyData)
    assert np.allclose(mapdl.geometry.lnum, [l0, l1, l2, l3])
    assert mapdl.geometry.n_line == 4


@skip_no_xserver
def test_lplot(cleared, mapdl, tmpdir):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    mapdl.l(k0, k1)
    mapdl.l(k1, k2)
    mapdl.l(k2, k3)
    mapdl.l(k3, k0)

    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    cpos = mapdl.lplot(show_keypoint_numbering=True, savefig=filename)
    assert isinstance(cpos, CameraPosition)
    assert os.path.isfile(filename)

    mapdl.lplot(vtk=False)  # make sure legacy still works


@skip_in_cloud
def test_apdl_logging_start(tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.inp"))

    mapdl = pymapdl.launch_mapdl()
    mapdl = launch_mapdl(log_apdl=filename)

    mapdl.prep7()
    mapdl.run('!comment test')
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)

    mapdl.exit()

    with open(filename, 'r') as fid:
        text = ''.join(fid.readlines())

    assert 'PREP7' in text
    assert '!comment test'
    assert 'K,1,0,0,0' in text
    assert 'K,2,1,0,0' in text
    assert 'K,3,1,1,0' in text
    assert 'K,4,0,1,0' in text


@pytest.mark.corba
def test_corba_apdl_logging_start(tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.inp"))

    mapdl = pymapdl.launch_mapdl(mode='CORBA')
    mapdl = launch_mapdl(log_apdl=filename)

    mapdl.prep7()
    mapdl.run('!comment test')
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)

    mapdl.exit()

    with open(filename, 'r') as fid:
        text = ''.join(fid.readlines())

    assert 'PREP7' in text
    assert '!comment test'
    assert 'K,1,0,0,0' in text
    assert 'K,2,1,0,0' in text
    assert 'K,3,1,1,0' in text
    assert 'K,4,0,1,0' in text


def test_apdl_logging(mapdl, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.inp"))
    if mapdl._apdl_log is None:
        mapdl.open_apdl_log(filename, mode="w")
    mapdl._close_apdl_log()

    # test append mode
    mapdl.open_apdl_log(filename, mode="a")

    # don't allow to double log
    with pytest.raises(RuntimeError):
        mapdl.open_apdl_log(filename, mode="w")

    mapdl.prep7()
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)

    mapdl._apdl_log.flush()

    out = open(mapdl._apdl_log.name).read().strip().split()[-5:]
    assert "PREP7" in out[0]
    assert "K,4,0,1,0" in out[-1]


def test_nodes(tmpdir, cleared, mapdl):
    mapdl.n(1, 1, 1, 1)
    mapdl.n(11, 10, 1, 1)
    mapdl.fill(1, 11, 9)

    basename = "tmp.nodes"
    filename = str(tmpdir.mkdir("tmpdir").join(basename))
    if mapdl._local:
        mapdl.nwrite(filename)
    else:
        mapdl.nwrite(basename)
        mapdl.download(basename, filename)

    assert np.allclose(mapdl.mesh.nodes, np.loadtxt(filename)[:, 1:])
    assert mapdl.mesh.n_node == 11
    assert np.allclose(mapdl.mesh.nnum, range(1, 12))

    # test clear mapdl
    mapdl.clear()
    assert not mapdl.mesh.nodes.size
    assert not mapdl.mesh.n_node
    assert not mapdl.mesh.nnum.size


def test_enum(mapdl, make_block):
    assert mapdl.mesh.n_elem
    assert np.allclose(mapdl.mesh.enum, range(1, mapdl.mesh.n_elem + 1))


@pytest.mark.parametrize("nnum", [True, False])
@skip_no_xserver
def test_nplot_vtk(cleared, mapdl, nnum):
    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    mapdl.nplot(vtk=True, nnum=nnum, background="w", color="k")


@skip_no_xserver
def test_nplot(cleared, mapdl):
    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    mapdl.nplot(vtk=False)


def test_elements(cleared, mapdl):
    mapdl.et(1, 185)

    # two basic cells
    cell1 = [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1],
    ]

    cell2 = [
        [0, 0, 2],
        [1, 0, 2],
        [1, 1, 2],
        [0, 1, 2],
        [0, 0, 3],
        [1, 0, 3],
        [1, 1, 3],
        [0, 1, 3],
    ]

    with mapdl.chain_commands:
        for cell in [cell1, cell2]:
            for x, y, z in cell:
                mapdl.n(x=x, y=y, z=z)

    mapdl.e(*list(range(1, 9)))
    mapdl.e(*list(range(9, 17)))
    expected = np.array(
        [
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            [1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 9, 10, 11, 12, 13, 14, 15, 16],
        ]
    )
    if "Grpc" in str(type(mapdl)):
        # no element number in elements
        expected[:, 8] = 0

    assert np.allclose(np.array(mapdl.mesh.elem), expected)


@pytest.mark.parametrize(
    "parm",
    (
        "my_string",
        1,
        10.0,
        [1, 2, 3],
        [[1, 2, 3], [1, 2, 3]],
        np.random.random((2000)),  # fails on gRPC at 100000
        np.random.random((10, 3)),
        np.random.random((10, 3, 3)),
    ),
)
def test_set_get_parameters(mapdl, parm):
    parm_name = pymapdl.misc.random_string(20)
    mapdl.parameters[parm_name] = parm
    if isinstance(parm, str):
        assert mapdl.parameters[parm_name] == parm
    else:
        assert np.allclose(mapdl.parameters[parm_name], parm)


def test_set_parameters_arr_to_scalar(mapdl, cleared):
    mapdl.parameters["PARM"] = np.arange(10)
    mapdl.parameters["PARM"] = 2


def test_set_parameters_string_spaces(mapdl):
    with pytest.raises(ValueError):
        mapdl.parameters["PARM"] = "string with spaces"


def test_builtin_parameters(mapdl, cleared):
    mapdl.prep7()
    assert mapdl.parameters.routine == "PREP7"

    mapdl.units("SI")
    assert mapdl.parameters.units == "SI"

    assert isinstance(mapdl.parameters.revision, float)

    # Platform could be either windows or Linux, without regards to
    # the testing OS.
    plat = mapdl.parameters.platform
    assert "L" in plat or "W" in plat

    mapdl.csys(1)
    assert mapdl.parameters.csys == 1

    mapdl.dsys(1)
    assert mapdl.parameters.dsys == 1

    mapdl.esys(0)
    assert mapdl.parameters.esys == 0
    assert mapdl.parameters.material == 1
    assert mapdl.parameters.section == 1
    assert mapdl.parameters.real == 1


@skip_no_xserver
def test_eplot(mapdl, make_block):
    init_elem = mapdl.mesh.n_elem
    mapdl.aplot()  # check aplot and verify it doesn't mess up the element plotting
    mapdl.eplot(show_node_numbering=True, background="w", color="b")
    mapdl.aplot()  # check aplot and verify it doesn't mess up the element plotting
    assert mapdl.mesh.n_elem == init_elem


@skip_no_xserver
def test_eplot_savefig(mapdl, make_block, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    mapdl.eplot(
        background="w",
        show_edges=True,
        smooth_shading=True,
        window_size=[1920, 1080],
        savefig=filename,
    )
    assert os.path.isfile(filename)


def test_partial_mesh_nnum(mapdl, make_block):
    allsel_nnum_old = mapdl.mesh.nnum
    mapdl.nsel("S", "NODE", vmin=100, vmax=200)
    allsel_nnum_now = mapdl.mesh.nnum_all
    assert np.allclose(allsel_nnum_old, allsel_nnum_now)

    mapdl.allsel()
    assert np.allclose(allsel_nnum_old, mapdl.mesh.nnum)


def test_partial_mesh_nnum(mapdl, make_block):
    mapdl.nsel("S", "NODE", vmin=1, vmax=10)
    mapdl.esel("S", "ELEM", vmin=10, vmax=20)
    assert mapdl.mesh._grid.n_cells == 11


def test_cyclic_solve(mapdl, cleared):
    # build the cyclic model
    mapdl.prep7()
    mapdl.shpp("off")
    mapdl.cdread("db", examples.sector_archive_file)
    mapdl.prep7()
    time.sleep(1.0)
    mapdl.cyclic()

    # set material properties
    mapdl.mp("NUXY", 1, 0.31)
    mapdl.mp("DENS", 1, 4.1408e-04)
    mapdl.mp("EX", 1, 16900000)
    mapdl.emodif("ALL", "MAT", 1)

    # setup and solve
    mapdl.modal_analysis("LANB", 1, 1, 100000, elcalc=True)
    mapdl.finish()

    # expect 16 result sets (1 mode, 16 blades, 16 modes in mode family)
    mapdl.post1()
    assert mapdl.post_processing.nsets == 16


def test_load_table(mapdl):
    dimx = np.random.randint(3, 15)
    dimy = np.random.randint(3, 15)

    my_conv = np.random.rand(dimx, dimy)
    my_conv[:, 0] = np.arange(dimx)
    my_conv[0, :] = np.arange(dimy)

    mapdl.load_table("my_conv", my_conv)
    assert np.allclose(mapdl.parameters["my_conv"], my_conv[1:, 1:], rtol=0.0001)

    with pytest.raises(ValueError, match='requires that the axis 0 is in ascending order.'):
        my_conv1 = my_conv.copy()
        my_conv1[0, 1] = 4
        mapdl.load_table("my_conv", my_conv1)

    with pytest.raises(ValueError, match='requires that the axis 1 is in ascending order.'):
        my_conv1 = my_conv.copy()
        my_conv1[1, 0] = 4
        mapdl.load_table("my_conv", my_conv1)


def test_load_array(mapdl):

    dimx = np.random.randint(1, 15)
    dimy = np.random.randint(1, 15)
    my_conv = np.random.rand(dimx, dimy)

    mapdl.load_array("my_conv", my_conv)
    assert np.allclose(mapdl.parameters["my_conv"], my_conv, rtol=0.0001)


@pytest.mark.skip_grpc
def test_lssolve(mapdl, cleared):
    mapdl.mute = True

    mapdl.run("/units,user,0.001,0.001,1,1,0,1,1,1")
    mapdl.prep7()
    mapdl.et(1, 182)
    mapdl.mp("ex", 1, 210e3)
    mapdl.mp("nuxy", 1, 0.33)
    mapdl.mp("dens", 1, 7.81e-06)
    mapdl.k(1, 0, 0)
    mapdl.k(2, 5, 0)
    mapdl.k(3, 5, 1)
    mapdl.k(4, 0, 1)
    mapdl.l(1, 2)
    mapdl.l(2, 3)
    mapdl.l(3, 4)
    mapdl.l(4, 1)
    mapdl.al(1, 2, 3, 4)
    mapdl.lsel("s", "", "", 1, 4)
    mapdl.lesize("all", 0.5)
    mapdl.amesh(1)
    mapdl.allsel()
    mapdl.finish()
    mapdl.run("/solu")
    mapdl.antype("static'")
    mapdl.kbc(0)
    mapdl.lsel("s", "", "", 4)
    mapdl.nsll("s", 1)
    mapdl.d("all", "all", 0)
    mapdl.ksel("s", "", "", 3)
    mapdl.nslk("s")
    mapdl.f("all", "fy", 5)
    mapdl.allsel()
    mapdl.lswrite(1)
    mapdl.fdele("all", "all")
    mapdl.ksel("s", "", "", 3)
    mapdl.nslk("s")
    mapdl.f("all", "fy", -5)
    mapdl.allsel()

    lsnum = 2
    mapdl.lswrite(lsnum)
    mapdl.mute = False
    out = mapdl.lssolve(1, lsnum)
    assert f"Load step file number {lsnum}.  Begin solution ..." in out


def test_coriolis(mapdl, cleared):
    """Simply test that we're formatting the input parm for coriolis"""
    # must be v190 or newer
    resp = mapdl.coriolis(True, True, True, True)
    assert "CORIOLIS IN STATIONARY REFERENCE FRAME" in resp
    assert "GYROSCOPIC DAMPING MATRIX WILL BE CALCULATED" in resp
    assert "ROTATING DAMPING MATRIX ACTIVATED" in resp
    assert "PRINT ROTOR MASS SUMMARY ACTIVATED" in resp


def test_title(mapdl, cleared):
    title = 'title1'  # the title cannot be longer than 7 chars. Check *get,parm,active,0,title for more info.
    mapdl.title(title)
    assert title == mapdl.get('par', 'active', '0', 'title')


def test_cdread(mapdl, cleared):
    random_letters = random_string(4)

    mapdl.run(f"PARMTEST='{random_letters}'")
    mapdl.cdwrite('all', 'model2', 'cdb')

    mapdl.clear()
    mapdl.cdread("db", 'model2', 'cdb')

    assert random_letters in mapdl.parameters['PARMTEST']


# CDREAD tests are actually a good way to test 'input' command.
@skip_in_cloud
def test_cdread_different_location(mapdl, cleared, tmpdir):
    random_letters = mapdl.directory.split('/')[0][-3:0]
    dirname = 'tt' + random_letters

    curdir = mapdl.directory
    subdir = tmpdir.mkdir(dirname)

    mapdl.run(f"parmtest='{random_letters}'")
    mapdl.cdwrite('all', subdir.join('model2'), 'cdb')

    mapdl.clear()
    mapdl.cwd(subdir)
    mapdl.cdread("db", 'model2', "cdb")
    mapdl.cwd(curdir)  #Going back

    assert random_letters == mapdl.parameters['parmtest']


def test_cdread_in_python_directory(mapdl, cleared, tmpdir):
    # Writing db file in python directory.
    # Pyansys should upload it when it detects it is not in the APDL directory.
    fullpath = str(tmpdir.join('model.cdb'))
    with open(fullpath, 'w') as fid:
        fid.write(CDB_FILE)

    # check if pymapdl is smart enough to determine if it can access
    # the archive from the current working directory.
    old_cwd = os.getcwd()
    try:
        # We are not checking yet if the file is read correctly, just if the file
        # can be read.
        os.chdir(tmpdir)
        mapdl.cdread('COMB', 'model', 'cdb') # 'COMB' is needed since we use the CDB with the strange line endings.
        assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(mapdl)

        clearing_cdread_cdwrite_tests(mapdl)
        mapdl.cdread('COMB', 'model.cdb')
        assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(mapdl)

        clearing_cdread_cdwrite_tests(mapdl)
        mapdl.cdread('COMB', 'model')
        assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(mapdl)

    finally:
        # always change back to the previous directory
        os.chdir(old_cwd)

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = str(tmpdir.join('model.cdb'))
    mapdl.cdread('COMB', fullpath)
    assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = str(tmpdir.join('model'))
    mapdl.cdread('COMB', fullpath, 'cdb')
    assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = str(tmpdir.join('model'))
    mapdl.cdread('COMB', fullpath)
    assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(mapdl)


def test_cdread_in_apdl_directory(mapdl, cleared):
    # Writing a db file in apdl directory, using APDL.
    # Using APDL to write the archive as there are be cases where the
    # python code cannot reach the APDL execution directory because it
    # is remote.
    mapdl.run("*SET,T_PAR,'asdf1234'")
    mapdl.run("CDWRITE,'DB','model','cdb'")

    clearing_cdread_cdwrite_tests(mapdl)
    mapdl.cdread('db', 'model', 'cdb')
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    mapdl.cdread('db', 'model.cdb')
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    mapdl.cdread('db', 'model')
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = os.path.join(mapdl.directory, 'model.cdb')
    mapdl.cdread('db', fullpath)
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = os.path.join(mapdl.directory, 'model')
    mapdl.cdread('db', fullpath, 'cdb')
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = os.path.join(mapdl.directory, 'model')
    mapdl.cdread('db', fullpath)
    assert asserting_cdread_cdwrite_tests(mapdl)


def test_inval_commands(mapdl, cleared):
    """Test the output of invalid commands"""
    cmds = ["*END", "*vwrite", "/eof", "cmatrix", "*REpeAT"]
    for each_cmd in cmds:
        with pytest.raises(RuntimeError):
            mapdl.run(each_cmd)


def test_inval_commands_silent(mapdl, tmpdir, cleared):
    assert mapdl.run("parm = 'asdf'")  # assert it is not empty
    mapdl.nopr()
    assert mapdl.run("parm = 'asdf'")  # assert it is not empty

    assert not mapdl._run('/nopr')  # setting /nopr and assert it is empty
    assert not mapdl.run("parm = 'asdf'")  # assert it is not empty

    mapdl._run('/gopr') # getting settings back


@skip_in_cloud
def test_path_without_spaces(mapdl, path_tests):
    resp = mapdl.cwd(path_tests.path_without_spaces)
    assert 'WARNING' not in resp


@skip_in_cloud
def test_path_with_spaces(mapdl, path_tests):
    resp = mapdl.cwd(path_tests.path_with_spaces)
    assert 'WARNING' not in resp


@skip_in_cloud
def test_path_with_single_quote(mapdl, path_tests):
    with pytest.raises(RuntimeError):
        resp = mapdl.cwd(path_tests.path_with_single_quote)
        assert 'WARNING' not in resp


@skip_in_cloud
def test_cwd_directory(mapdl, tmpdir):

    mapdl.directory = str(tmpdir)
    assert mapdl.directory == str(tmpdir).replace('\\', '/')

    wrong_path = 'wrong_path'
    with pytest.warns(Warning) as record:
        mapdl.directory = wrong_path
        assert 'The working directory specified' in record.list[-1].message.args[0]
        assert 'is not a directory on' in record.list[-1].message.args[0]
