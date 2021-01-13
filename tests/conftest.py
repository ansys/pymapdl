import os

import pytest
import pyvista

from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.misc import get_ansys_bin
from ansys.mapdl.core.errors import MapdlExitedError
from ansys.mapdl.core.launcher import (get_start_instance,
                                       MAPDL_DEFAULT_PORT,
                                       _get_available_base_ansys)

# Necessary for CI plotting
pyvista.OFF_SCREEN = True


# check for a valid MAPDL install with gRPC
valid_rver = ['211']  # checks in this order
EXEC_FILE = None
for rver in valid_rver:
    if os.path.isfile(get_ansys_bin(rver)):
        EXEC_FILE = get_ansys_bin(rver)
        break

# determine if we can launch an instance of MAPDL locally
local = [False]

# check if the user wants to permit pytest to start MAPDL
START_INSTANCE = get_start_instance()
# if START_INSTANCE:
#     local.append(True)


def pytest_addoption(parser):
    parser.addoption(
        "--corba", action="store_true", default=False, help="run CORBA tests"
    )
    parser.addoption(
        "--console", action="store_true", default=False, help="run console tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--corba"):
        # --corba given in cli: run CORBA interface tests
        return
    skip_corba = pytest.mark.skip(reason="need --corba option to run")
    for item in items:
        if "corba" in item.keywords:
            item.add_marker(skip_corba)

    if config.getoption("--console"):
        # --console given in cli: run console interface tests
        return
    skip_console = pytest.mark.skip(reason="need --console option to run")
    for item in items:
        if "console" in item.keywords:
            item.add_marker(skip_console)


@pytest.fixture(scope="session")
def mapdl_console(request):
    ansys_base_paths = _get_available_base_ansys()

    if os.name != 'posix':
        raise RuntimeError('"--console" testing option unavailable.  '
                           'Only Linux is supported.')

    # find a valid version of corba
    console_path = None
    for version in ansys_base_paths:
        if version < 211:
            console_path = get_ansys_bin(str(version))

    if console_path is None:
        raise RuntimeError('"--console" testing option unavailable.'
                           'No local console compatible MAPDL installation found. '
                           'Valid versions are up to 2020R2.')

    mapdl = launch_mapdl(console_path)
    mapdl._show_matplotlib_figures = False  # CI: don't show matplotlib figures

    # using yield rather than return here to be able to test exit
    yield mapdl

    # verify mapdl exits
    mapdl.exit()
    assert mapdl._exited
    assert 'MAPDL exited' in str(mapdl)
    with pytest.raises(MapdlExitedError):
        mapdl.prep7()


@pytest.fixture(scope="session")
def mapdl_corba(request):
    ansys_base_paths = _get_available_base_ansys()

    # find a valid version of corba
    corba_path = None
    for version in ansys_base_paths:
        if version >= 170 and version < 211:
            corba_path = get_ansys_bin(str(version))

    if corba_path is None:
        raise RuntimeError('"-corba" testing option unavailable.'
                           'No local CORBA compatible MAPDL installation found.  '
                           'Valid versions are ANSYS 17.0 up to 2020R2.')

    mapdl = launch_mapdl(corba_path)
    mapdl._show_matplotlib_figures = False  # CI: don't show matplotlib figures

    # using yield rather than return here to be able to test exit
    yield mapdl

    # verify mapdl exits
    mapdl.exit()
    assert mapdl._exited
    assert 'MAPDL exited' in str(mapdl)
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

    mapdl = launch_mapdl(EXEC_FILE, override=True, run_location=run_path,
                         cleanup_on_exit=cleanup)
    mapdl._show_matplotlib_figures = False  # CI: don't show matplotlib figures
    mapdl._local = request.param  # CI: override for testing

    if mapdl._local:
        assert mapdl.directory == run_path

    # using yield rather than return here to be able to test exit
    yield mapdl

    ###########################################################################
    # test exit: only when allowed to start PYMAPDL
    ###########################################################################
    if START_INSTANCE:
        mapdl._local = True
        mapdl.exit()
        assert mapdl._exited
        assert 'MAPDL exited' in str(mapdl)

        if mapdl._local:
            assert not os.path.isfile(mapdl._lockfile)

        # should test if _exited protects from execution
        with pytest.raises(MapdlExitedError):
            mapdl.prep7()

        # actually test if server is shutdown
        with pytest.raises(MapdlExitedError):
            mapdl._send_command('/PREP7')
        with pytest.raises(MapdlExitedError):
            mapdl._send_command_stream('/PREP7')


@pytest.fixture(scope='function')
def cleared(mapdl):
    mapdl.finish()
    mapdl.clear('NOSTART')  # *MUST* be NOSTART.  With START fails after 20 calls...
    mapdl.prep7()
    yield


@pytest.fixture(scope='function')
def cube_solve(cleared, mapdl):
    # setup the full file
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, 186)
    mapdl.esize(0.5)
    mapdl.vmesh('all')

    # Define a material (nominal steel in SI)
    mapdl.mp('EX', 1, 210E9)  # Elastic moduli in Pa (kg/(m*s**2))
    mapdl.mp('DENS', 1, 7800)  # Density in kg/m3
    mapdl.mp('NUXY', 1, 0.3)  # Poisson's Ratio

    # solve first 10 non-trivial modes
    out = mapdl.modal_analysis(nmode=10, freqb=1)
