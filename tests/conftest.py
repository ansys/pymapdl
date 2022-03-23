from collections import namedtuple
import os
from pathlib import Path
import signal
import time

from common import Element, Node, get_details_of_elements, get_details_of_nodes
import pytest
import pyvista

from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.errors import MapdlExitedError
from ansys.mapdl.core.launcher import (
    MAPDL_DEFAULT_PORT,
    _get_available_base_ansys,
    get_start_instance,
)
from ansys.mapdl.core.misc import get_ansys_bin

# Necessary for CI plotting
pyvista.OFF_SCREEN = True

SpacedPaths = namedtuple(
    "SpacedPaths", ["path_without_spaces", "path_with_spaces", "path_with_single_quote"]
)


# Check if MAPDL is installed
# NOTE: checks in this order to get the newest installed version
valid_rver = ["221", "212", "211", "202", "201", "195", "194", "193", "192", "191"]
EXEC_FILE = None
for rver in valid_rver:
    if os.path.isfile(get_ansys_bin(rver)):
        EXEC_FILE = get_ansys_bin(rver)
        break

# Cache if gRPC MAPDL is installed.
#
# minimum version on linux.  Windows is v202, but using v211 for consistency
# Override this if running on CI/CD and PYMAPDL_PORT has been specified
ON_CI = "PYMAPDL_START_INSTANCE" in os.environ and "PYMAPDL_PORT" in os.environ
HAS_GRPC = int(rver) >= 211 or ON_CI


# determine if we can launch an instance of MAPDL locally
# start with ``False`` and always assume the remote case
local = [False]

# check if the user wants to permit pytest to start MAPDL
START_INSTANCE = get_start_instance()

if os.name == "nt":
    os_msg = """SET PYMAPDL_START_INSTANCE=False
SET PYMAPDL_PORT=<MAPDL Port> (default 50052)
SET PYMAPDL_IP=<MAPDL IP> (default 127.0.0.1)"""
else:
    os_msg = """export PYMAPDL_START_INSTANCE=False
export PYMAPDL_PORT=<MAPDL Port> (default 50052)
export PYMAPDL_IP=<MAPDL IP> (default 127.0.0.1)"""

ERRMSG = f"""Unable to run unit tests without MAPDL installed or
accessible.  Either install Ansys 2021R1 or newer or specify the
remote server with:

{os_msg}

If you do have Ansys installed, you may have to patch pymapdl to
automatically find your Ansys installation.  Email the developer at:
alexander.kaszynski@ansys.com

"""

if START_INSTANCE and EXEC_FILE is None:
    raise RuntimeError(ERRMSG)


def check_pid(pid):
    """Check For the existence of a pid."""
    try:
        # There are two main options:
        # - Termination signal (SIGTERM) int=15. Soft termination (Recommended)
        # - Kill signal (KILLTER). int=9. Hard termination
        os.kill(pid, signal.SIGTERM)
    except OSError:
        return False
    else:
        return True


def pytest_addoption(parser):
    parser.addoption(
        "--corba", action="store_true", default=False, help="run CORBA tests"
    )
    parser.addoption(
        "--console", action="store_true", default=False, help="run console tests"
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--corba"):
        # --corba given in cli: run CORBA interface tests
        skip_corba = pytest.mark.skip(reason="need --corba option to run")
        for item in items:
            if "corba" in item.keywords:
                item.add_marker(skip_corba)

    if not config.getoption("--console"):
        # --console given in cli: run console interface tests
        skip_console = pytest.mark.skip(reason="need --console option to run")
        for item in items:
            if "console" in item.keywords:
                item.add_marker(skip_console)

    if not HAS_GRPC:
        skip_grpc = pytest.mark.skip(reason="requires at least v211 to run")
        for item in items:
            if "skip_grpc" in item.keywords:
                item.add_marker(skip_grpc)


@pytest.fixture(scope="session")
def mapdl_console(request):
    if os.name != "posix":
        raise RuntimeError(
            '"--console" testing option unavailable.  ' "Only Linux is supported."
        )
    ansys_base_paths = _get_available_base_ansys()

    # find a valid version of corba
    console_path = None
    for version in ansys_base_paths:
        if version < 211:
            console_path = get_ansys_bin(str(version))

    if console_path is None:
        raise RuntimeError(
            '"--console" testing option unavailable.'
            "No local console compatible MAPDL installation found. "
            "Valid versions are up to 2020R2."
        )

    mapdl = launch_mapdl(console_path)
    from ansys.mapdl.core.mapdl_console import MapdlConsole

    assert isinstance(mapdl, MapdlConsole)
    mapdl._show_matplotlib_figures = False  # CI: don't show matplotlib figures

    # using yield rather than return here to be able to test exit
    yield mapdl

    # verify mapdl exits
    mapdl.exit()
    assert mapdl._exited
    assert "MAPDL exited" in str(mapdl)
    with pytest.raises(MapdlExitedError):
        mapdl.prep7()


@pytest.fixture(scope="session")
def mapdl_corba(request):
    ansys_base_paths = _get_available_base_ansys()

    # find a valid version of corba
    corba_path = None
    for version in ansys_base_paths:
        if version >= 170 and version < 202:
            corba_path = get_ansys_bin(str(version))

    if corba_path is None:
        raise RuntimeError(
            '"-corba" testing option unavailable.'
            "No local CORBA compatible MAPDL installation found.  "
            "Valid versions are ANSYS 17.0 up to 2020R2."
        )

    mapdl = launch_mapdl(corba_path)
    from ansys.mapdl.core.mapdl_corba import MapdlCorba

    assert isinstance(mapdl, MapdlCorba)
    mapdl._show_matplotlib_figures = False  # CI: don't show matplotlib figures

    # using yield rather than return here to be able to test exit
    yield mapdl

    # verify mapdl exits
    mapdl.exit()
    assert mapdl._exited
    assert "MAPDL exited" in str(mapdl)
    with pytest.raises(MapdlExitedError):
        mapdl.prep7()


@pytest.fixture(scope="session", params=local)
def mapdl(request, tmpdir_factory):
    # don't use the default run location as tests run multiple unit testings
    run_path = str(tmpdir_factory.mktemp("ansys"))

    # don't allow mapdl to exit upon collection unless mapdl is local
    cleanup = START_INSTANCE

    if request.param:
        # usage of a just closed channel on same port causes connectivity issues
        port = MAPDL_DEFAULT_PORT + 10
    else:
        port = MAPDL_DEFAULT_PORT

    mapdl = launch_mapdl(
        EXEC_FILE, override=True, run_location=run_path, cleanup_on_exit=cleanup
    )
    mapdl._show_matplotlib_figures = False  # CI: don't show matplotlib figures

    if HAS_GRPC:
        mapdl._local = request.param  # CI: override for testing

    if mapdl._local:
        assert Path(mapdl.directory) == Path(run_path)
        assert mapdl._distributed

    # using yield rather than return here to be able to test exit
    yield mapdl

    ###########################################################################
    # test exit: only when allowed to start PYMAPDL
    ###########################################################################
    if START_INSTANCE:
        mapdl._local = True
        mapdl.exit()
        assert mapdl._exited
        assert "MAPDL exited" in str(mapdl)

        if mapdl._local:
            assert not os.path.isfile(mapdl._lockfile)

        # should test if _exited protects from execution
        with pytest.raises(MapdlExitedError):
            mapdl.prep7()

        # actually test if server is shutdown
        if HAS_GRPC:
            with pytest.raises(MapdlExitedError):
                mapdl._send_command("/PREP7")
            with pytest.raises(MapdlExitedError):
                mapdl._send_command_stream("/PREP7")

            # verify PIDs are closed
            time.sleep(1)  # takes a second for the processes to shutdown
            for pid in mapdl._pids:
                assert not check_pid(pid)


@pytest.fixture
def path_tests(tmpdir):
    p1 = tmpdir.mkdir("./temp/")
    p2 = tmpdir.mkdir("./t e m p/")
    p3 = tmpdir.mkdir("./temp'")
    return SpacedPaths(str(p1), str(p2), str(p3))


@pytest.fixture(scope="function")
def cleared(mapdl):
    mapdl.finish(mute=True)
    # *MUST* be NOSTART.  With START fails after 20 calls...
    # this has been fixed in later pymapdl and MAPDL releases
    mapdl.clear("NOSTART", mute=True)
    mapdl.prep7(mute=True)
    yield


@pytest.fixture(scope="function")
def cube_solve(cleared, mapdl):
    # setup the full file
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, 186)
    mapdl.esize(0.5)
    mapdl.vmesh("all")

    # Define a material (nominal steel in SI)
    mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
    mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
    mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio

    # solve first 10 non-trivial modes
    out = mapdl.modal_analysis(nmode=10, freqb=1)


@pytest.fixture
def box_with_fields(cleared, mapdl):
    mapdl.prep7()
    mapdl.mp("kxx", 1, 45)
    mapdl.mp("ex", 1, 2e10)
    mapdl.mp("perx", 1, 1)
    mapdl.mp("murx", 1, 1)
    mapdl.et(1, "SOLID70")
    mapdl.et(2, "CPT215")
    mapdl.et(3, "SOLID122")
    mapdl.et(4, "SOLID96")
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.esize(0.5)
    return mapdl


@pytest.fixture
def box_geometry(mapdl, cleared):
    areas, keypoints = create_geometry(mapdl)
    q = mapdl.queries
    return q, keypoints, areas, get_details_of_nodes(mapdl)


@pytest.fixture
def line_geometry(mapdl, cleared):
    mapdl.prep7(mute=True)
    k0 = mapdl.k(1, 0, 0, 0)
    k1 = mapdl.k(2, 1, 2, 2)
    l0 = mapdl.l(k0, k1)
    q = mapdl.queries
    return q, [k0, k1], l0


@pytest.fixture
def query(mapdl, cleared):
    return mapdl.queries


@pytest.fixture
def solved_box(mapdl, cleared):
    mapdl.prep7()
    mapdl.et(1, "SOLID5")
    mapdl.block(0, 10, 0, 20, 0, 30)
    mapdl.esize(10)
    mapdl.vmesh("ALL")
    mapdl.units("SI")  # SI - International system (m, kg, s, K).
    # Define a material (nominal steel in SI)
    mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
    mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
    mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio
    # Fix the left-hand side.
    mapdl.nsel("S", "LOC", "Z", 0)
    mapdl.d("ALL", "UX")
    mapdl.d("ALL", "UY")
    mapdl.d("ALL", "UZ")

    mapdl.nsel("S", "LOC", "Z", 30)
    mapdl.f("ALL", "FX", 1000)
    mapdl.run("/SOLU")
    mapdl.antype("STATIC")
    mapdl.solve()
    mapdl.finish()
    q = mapdl.queries
    return q, get_details_of_nodes(mapdl)


@pytest.fixture
def common_functions_and_classes():
    return get_details_of_nodes, get_details_of_elements, Node, Element


@pytest.fixture
def selection_test_geometry(mapdl, cleared):
    mapdl.prep7()
    k0 = mapdl.k(1, 0, 0, 0)
    k1 = mapdl.k(2, 0, 0, 1)
    k2 = mapdl.k(3, 0, 1, 0)
    k3 = mapdl.k(4, 1, 0, 0)
    v0 = mapdl.v(k0, k1, k2, k3)
    mapdl.mshape(1, "3D")
    mapdl.et(1, "SOLID98")
    mapdl.esize(0.5)
    mapdl.vmesh("ALL")
    return mapdl.queries


@pytest.fixture
def twisted_sheet(mapdl, cleared):
    mapdl.prep7()
    mapdl.et(1, "SHELL181")
    mapdl.mp("EX", 1, 2e5)
    mapdl.rectng(0, 1, 0, 1)
    mapdl.sectype(1, "SHELL")
    mapdl.secdata(0.1)
    mapdl.esize(0.5)
    mapdl.amesh("all")
    mapdl.run("/SOLU")
    mapdl.antype("STATIC")
    mapdl.nsel("s", "loc", "x", 0)
    mapdl.d("all", "all")
    mapdl.nsel("s", "loc", "x", 1)
    mapdl.d("all", "ux", -0.1)
    mapdl.d("all", "uy", -0.1)
    mapdl.d("all", "uz", -0.1)
    mapdl.allsel("all")
    mapdl.solve()
    mapdl.finish()
    q = mapdl.queries
    return q, get_details_of_nodes(mapdl)


def create_geometry(mapdl):
    mapdl.prep7()
    k0 = mapdl.k(1, 0, 0, 0)
    k1 = mapdl.k(2, 0, 5, 0)
    k2 = mapdl.k(3, 5, 5, 0)
    k3 = mapdl.k(4, 5, 0, 0)
    k4 = mapdl.k(5, 0, 0, 5)
    k5 = mapdl.k(6, 0, 5, 5)
    k6 = mapdl.k(7, 5, 5, 5)
    k7 = mapdl.k(8, 5, 0, 5)
    a0 = mapdl.a(1, 2, 3, 4)
    a1 = mapdl.a(5, 6, 7, 8)
    a2 = mapdl.a(3, 4, 8, 7)
    a3 = mapdl.a(1, 2, 6, 5)
    keypoints = [k0, k1, k2, k3, k4, k5, k6, k7]
    areas = [a0, a1, a2, a3]
    mapdl.esize(5)
    mapdl.mshape(1, "2D")
    mapdl.et(1, "SHELL181")
    mapdl.amesh("ALL")
    return areas, keypoints


def apply_forces(mapdl):
    for const in ["UX", "UY", "UZ", "ROTX", "ROTY", "ROTZ"]:
        mapdl.d("all", const)

    mapdl.f(1, "FX", 1000)
    mapdl.f(2, "FY", 1000)
    mapdl.f(3, "FZ", 1000)
    mapdl.f(4, "MX", 1000)
    mapdl.f(5, "MY", 1000)
    mapdl.f(6, "MZ", 1000)
    mapdl.d(7, "UZ")
    mapdl.d(8, "UZ")


def solve_simulation(mapdl):
    mapdl.run("/solu")
    mapdl.antype("static")
    mapdl.solve()
