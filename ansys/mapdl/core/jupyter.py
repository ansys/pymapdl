"""Contains methods used only when running on ANSYS's jupyterhub cluster"""
import warnings

try:
    from ansys.jupyterhub import manager
except ImportError:
    raise ImportError('Module `ansys-jupyterhub-manager` missing.\n'
                      'This module is required to spawn instances on jupyterhub')


MAX_CPU = 128
MAX_MEM = 256


def check_manager():
    try:
        # response = manager.ping()
        manager.ping()
    except:
        raise RuntimeError('Unable to connect to scheduler')

    # consider checking the version
    # version = re.findall('(\d*\.\d*\.\d*)', response)
    # if not version:
    #     raise RuntimeError('Unable to parse version')
    # if version[0] != '0.1.6':
    #     raise RuntimeError('Invalid scheduler version')


def launch_mapdl_on_cluster(nproc=2, memory=4, loglevel='INFO',
                            additional_switches='', verbose=True,
                            start_timeout=600, **kwargs):
    """Start MAPDL on the ANSYS jupyter cluster in gRPC mode.

    Parameters
    ----------
    nproc : int, optional
        Number of processors.  Defaults to 2.

    memory : float, optional
        Fixed amount of memory to request for MAPDL in Gigabytes.  If
        the mapdl instance requires more ram than your provide MAPDL
        may segfault.

    loglevel : str, optional
        Sets which messages are printed to the console.  Default
        'INFO' prints out all ANSYS messages, 'WARNING` prints only
        messages containing ANSYS warnings, and 'ERROR' prints only
        error messages.

    additional_switches : str, optional
        Additional switches for MAPDL, for example aa_r, and academic
        research license, would be added with:

        - ``additional_switches="-aa_r"``

        Avoid adding switches like -i -o or -b as these are already
        included to start up the MAPDL server.  See the notes
        section for additional details.

    start_timeout : float, optional
        Maximum allowable time to connect to the MAPDL server.

    Returns
    -------
    port : int
        Returns the port number that the gRPC instance started on.

    Examples
    --------
    Launch MAPDL using the default configuration.

    >>> from ansys.mapdl import launch_mapdl
    >>> mapdl = launch_mapdl()
    """
    # attempt to connect to the remote scheduler
    check_manager()

    # check additional_switches args
    if '-m ' in additional_switches:
        raise ValueError('Memory option "-m" not permitted when launching from the '
                         'kubernetes cluster and is set with the `memory` parameter')
    if '-np ' in additional_switches:
        raise ValueError('CPU option "-np" not permitted when launching from the '
                         'kubernetes cluster and is set with the `nproc` parameter')

    # check resources
    nproc = int(nproc)
    if nproc < 0:
        raise ValueError('Requested CPUs `nproc` must be greater than 0')
    if nproc > MAX_CPU:
        raise ValueError(f'Requested CPUs `nproc` must be less than {MAX_CPU}')

    if memory < 0.25:
        raise ValueError('Requested memory `mem` must be greater than 0.25')
    if memory > MAX_MEM:
        raise ValueError(f'Requested memory `mem` must be less than than {MAX_MEM}')

    # convert memory from GB to Mi
    memory *= 1024
    if '-smp' in additional_switches:
        warnings.warn('Ignoring additional switch "-smp".  Incompatible with docker '
                      'container.')
        additional_switches = additional_switches.replace('-smp', '')
    additional_switches += f'-m -{memory} -np {nproc}'

    # need a way of making the image user-selectable
    image = 'mapdlhelm.azurecr.io/mapdl:v22.0.0'
    command = 'printf "" | /ansys_inc/v202/ansys/bin/mapdl %s -smp -grpc -custom /ansys_inc/v202/grpc/ansys.e201t.DEBUG-0.53.1' % additional_switches
    env = {'ANSYSLMD_LICENSE_FILE': '1055@10.0.0.16'}
    ip, pod_name = manager.spawn_pod(image, env=env, cpu=1000*nproc, memory=memory,
                                     command=command, start_timeout=start_timeout,
                                     verbose=verbose)

    # connect to the pod instance
    from ansys.mapdl import Mapdl  # import here to avoid recursive
    return Mapdl(ip, loglevel=loglevel)
