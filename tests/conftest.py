import os
import atexit

import pytest
import pyvista

from ansys.mapdl.core.mapdl_grpc import MapdlGrpc
from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.misc import get_ansys_bin
from ansys.mapdl.core.errors import MapdlExitedError
from ansys.mapdl.core.launcher import (get_start_instance,
                                       MAPDL_DEFAULT_PORT,
                                       _get_available_base_ansys)


global mapdl_instance
mapdl_instances = {}

# Necessary for CI plotting
pyvista.OFF_SCREEN = True



@atexit.register
def cleanup_instances():
    global mapdl_instances
    mapdl_instances = {}


@pytest.fixture(autouse=True)
def skip_when_not_grpc(request, mapdl):
    if request.node.get_closest_marker('skip_not_grpc'):
        if not isinstance(mapdl, MapdlGrpc):
            pytest.skip('Skipping as Mapdl is not using gRPC')


def pytest_addoption(parser):
    """Enable testing remote/local options for gRPC and the console
    and CORBA protocols.

    By default this is not enabled

    """
    parser.addoption('--corba', action='store_true', default=False,
                     help='test mapdl in CORBA mode')
    parser.addoption('--console', action='store_true', default=False,
                     help='test mapdl in console mode')


def pytest_generate_tests(metafunc):
    ansys_base_paths = _get_available_base_ansys()

    # check for a valid MAPDL install with gRPC
    mode_config = []  # list of tuples of (mode, local, exec_path)

    if not get_start_instance():
        # allow connect to an existing instance
        mode_config.append(('grpc', False, None))

    if metafunc.config.getoption('corba'):
        # grab the first version compatible with CORBA
        corba_path = None
        for version in ansys_base_paths:
            if version >= 170 and version < 211:
                corba_path = get_ansys_bin(str(version))

        if corba_path is None:
            raise RuntimeError('"-corba" testing option unavailable.'
                               'No local CORBA compatible MAPDL installation found.  '
                               'Valid versions are ANSYS 17.0 up to 2020R2.')
        mode_config.append(('corba', None, corba_path))

    elif metafunc.config.getoption('console'):
        if os.name != 'linux':
            raise OSError('"-console" testing option only available on Linux')
        # grab the first version compatible with CORBA
        corba_path = None
        for version in ansys_base_paths:
            if version >= 130 and version < 211:
                console_path = get_ansys_bin(str(version))

        if console_path is None:
            raise RuntimeError('No local console compatible MAPDL installation found.'
                               '  Valid versions are ANSYS 13.0 up to 2020R2.')
        mode_config.append(('console', None, console_path))

    else:  # otherwise, test default grpc mode
        if 211 in ansys_base_paths:
            get_ansys_bin('211')
            mode_config.append(('grpc', True, get_ansys_bin('211')))

    metafunc.parametrize('mapdl', mode_config, indirect=True, scope='session')


@pytest.fixture(scope="session")
def mapdl(request):
    # we have to use global here to avoid creating multiple instances
    # when using parameterization
    global mapdl_instances

    # get configuration details from pytest parameters
    mode, local, exec_path = request.param
    if request.param in mapdl_instances:
        mapdl_instance = mapdl_instances[request.param]
    else:
        if mode == 'grpc':
            if local:
                mapdl_instance = launch_mapdl(exec_path)
            else:
                # connect to an existing instance
                ip = os.environ.get('PYMAPDL_IP', '127.0.0.1')
                if 'PYMAPDL_PORT' in os.environ:
                    port = int(os.environ.get('PYMAPDL_PORT'))
                else:
                    port = MAPDL_DEFAULT_PORT
                mapdl_instance = MapdlGrpc(ip=ip, port=port, cleanup_on_exit=False)
            assert isinstance(mapdl_instance, MapdlGrpc)

        elif mode == 'corba':
            from ansys.mapdl.core.mapdl_corba import MapdlCorba
            mapdl_instance = launch_mapdl(exec_path, mode='corba')
            assert isinstance(mapdl_instance, MapdlCorba)

        elif mode == 'console':
            from ansys.mapdl.core.mapdl_console import MapdlConsole
            mapdl_instance = launch_mapdl(exec_path, mode='console')
            assert isinstance(mapdl_instance, MapdlConsole)
        else:
            raise ValueError(f'Invalid Mode "{mode}"')

        # CI only: don't show matplotlib figures
        mapdl_instance._show_matplotlib_figures = False
        mapdl_instances[request.param] = mapdl_instance

    # using yield rather than return here to be able to test exit
    return mapdl_instance

    ###########################################################################
    # test exit: only when allowed to start PYMAPDL from gRPC
    ###########################################################################
    if mode == 'grpc' and local == 'true':
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
