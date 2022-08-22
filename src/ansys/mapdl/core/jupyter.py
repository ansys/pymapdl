"""Contains methods used only when running on ANSYS's jupyterhub cluster"""

try:
    from ansys.jupyterhub import manager
except ImportError:
    raise ImportError(
        "Module `ansys-jupyterhub-manager` missing.\n"
        "This library is required to spawn instances on pyansys.com"
    )


MAX_CPU = 128
MAX_MEM = 256


def check_manager():
    try:
        # response = manager.ping()
        manager.ping()
    except:
        raise RuntimeError("Unable to connect to scheduler")

    # consider checking the version
    # version = re.findall('(\d*\.\d*\.\d*)', response)
    # if not version:
    #     raise RuntimeError('Unable to parse version')
    # if version[0] != '0.1.6':
    #     raise RuntimeError('Invalid scheduler version')


def launch_mapdl_on_cluster(
    nproc=2,
    memory=4,
    loglevel="ERROR",
    additional_switches="",
    verbose=False,
    start_timeout=600,
    tag="latest",
):
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
        ``'INFO'`` logs out all MAPDL messages, ``'WARNING'`` prints only
        messages containing MAPDL warnings, and ``'ERROR'`` prints only
        error messages.
    additional_switches : str, optional
        Additional switches for MAPDL, for example ``"-p aa_r"``, the
        academic research license, would be added with:

        - ``additional_switches="-p aa_r"``

        Avoid adding switches like ``"-i"`` ``"-o"`` or ``"-b"`` as
        these are already included to start up the MAPDL server.  See
        the notes section for additional details.
    start_timeout : float, optional
        Maximum allowable time to connect to the MAPDL server.
    tag : str, optional
        Docker image tag from `PyAnsys MAPDL Image
        <https://github.com/orgs/pyansys/packages/container/package/pymapdl%2Fmapdl>`. Defaults
        to ``"latest"``. For example "v22.1.0".

    Returns
    -------
    MapdlGrpc
        MAPDL instance.

    Examples
    --------
    Launch MAPDL using the default configuration.

    >>> from ansys.mapdl import launch_mapdl
    >>> mapdl = launch_mapdl()

    Launch MAPDL and guarantee 16 GB minimum RAM and 8 CPUs.

    >>> mapdl = launch_mapdl(memory=16, nproc=8)

    """
    # attempt to connect to the remote scheduler
    check_manager()

    # check additional_switches args
    if "-m " in additional_switches:
        raise ValueError(
            'Memory option "-m" not permitted when launching from the '
            "kubernetes cluster and is set with the ``memory`` parameter"
        )
    if "-np " in additional_switches:
        raise ValueError(
            'CPU option "-np" not permitted when launching from the '
            "kubernetes cluster and is set with the ``nproc`` parameter"
        )

    # check resources
    nproc = int(nproc)
    if nproc < 0:
        raise ValueError("Requested CPUs ``nproc`` must be greater than 0")
    if nproc > MAX_CPU:
        raise ValueError(f"Requested CPUs ``nproc`` must be less than {MAX_CPU}")

    if memory < 0.25:
        raise ValueError("Requested memory ``mem`` must be greater than 0.25")
    if memory > MAX_MEM:
        raise ValueError(f"Requested memory ``mem`` must be less than than {MAX_MEM}")

    # # convert memory from GB to Mi
    memory *= 1024

    if "-smp" in additional_switches:
        raise ValueError(
            'The additional switch "-smp" is incompatible with docker containers.'
        )

    additional_switches += f"-m -{memory} -np {nproc}"
    args = additional_switches.split()
    ip, name = manager.spawn_mapdl(
        version=tag,
        args=args,
        verbose=verbose,
        cpu=1000 * nproc,
        memory=memory,
    )

    # connect to the pod instance
    from ansys.mapdl.core import Mapdl

    return Mapdl(ip, loglevel=loglevel)
