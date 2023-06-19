"""This module is for threaded implementations of the mapdl interface"""

import os
import shutil
import time
import warnings

from ansys.mapdl.core import LOG, get_ansys_path, launch_mapdl
from ansys.mapdl.core.errors import VersionError
from ansys.mapdl.core.launcher import MAPDL_DEFAULT_PORT, port_in_use, version_from_path
from ansys.mapdl.core.mapdl_grpc import _HAS_TQDM
from ansys.mapdl.core.misc import create_temp_dir, threaded, threaded_daemon

if _HAS_TQDM:
    from tqdm import tqdm


def available_ports(n_ports, starting_port=MAPDL_DEFAULT_PORT):
    """Return a list the first ``n_ports`` ports starting from ``starting_port``."""

    port = MAPDL_DEFAULT_PORT
    ports = []
    while port < 65536 and len(ports) < n_ports:
        if not port_in_use(port):
            ports.append(port)
        port += 1

    if len(ports) < n_ports:
        raise MapdlRuntimeError(
            f"There are not {n_ports} available ports between {starting_port} and 65536"
        )

    return ports


class LocalMapdlPool:
    """Create a pool of MAPDL instances.

    .. note::
       Requires MAPDL 2020 R2 or later.

    Parameters
    ----------
    n_instance : int
        Number of instances to create.

    restart_failed : bool, optional
        Restarts failed instances.  Defaults to ``True``.

    wait : bool, optional
        Wait for pool to be initialized.  Otherwise, pool will start
        in the background and all resources may not be available instantly.

    run_location : str, optional
        Base directory to create additional directories for each MAPDL
        instance.  Defaults to a temporary working directory.

    starting_port : int, optional
        Starting port for the MAPDL instances.  Defaults to 50052.

    progress_bar : bool, optional
        Show a progress bar when starting the pool.  Defaults to
        ``True``.  Will not be shown when ``wait=False``.

    restart_failed : bool, optional
        Restarts any failed instances in the pool.

    remove_temp_files : bool, optional
        This launcher creates a new MAPDL working directory for each instance
        of MAPDL within the temporary user directory, obtainable with
        ``tempfile.gettempdir()``, for MAPDL files. When this parameter is
        ``True``, this directory will be deleted when MAPDL is exited. Default
        ``False``.

    **kwargs : dict, optional
        See :func:`ansys.mapdl.core.launch_mapdl` for a complete
        listing of all additional keyword arguments.

    Examples
    --------
    Simply create a pool of 10 instances to run in the temporary
    directory.

    >>> from ansys.mapdl.core import LocalMapdlPool
    >>> pool = LocalMapdlPool(10)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    Create several instances with 1 CPU each running at the current
    directory within their own isolated directories.

    >>> import os
    >>> my_path = os.getcmd()
    >>> pool = LocalMapdlPool(10, nproc=1, run_location=my_path)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    Create a pool while specifying the MAPDL executable in Windows.

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v212/ansys/bin/winx64/ANSYS212.exe'
    >>> pool = LocalMapdlPool(10, exec_file=exec_file)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    Create a pool while specifying the MAPDL executable in Linux.

    >>> exec_file = '/ansys_inc/v211/ansys/bin/ansys211'
    >>> pool = LocalMapdlPool(10, exec_file=exec_file)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    """

    def __init__(
        self,
        n_instances,
        wait=True,
        run_location=None,
        port=MAPDL_DEFAULT_PORT,
        progress_bar=True,
        restart_failed=True,
        remove_temp_files=True,
        **kwargs,
    ):
        """Initialize several instances of mapdl"""
        self._instances = []
        self._root_dir = run_location
        kwargs["remove_temp_files"] = remove_temp_files
        kwargs["mode"] = "grpc"
        self._spawn_kwargs = kwargs

        # verify that mapdl is 2021R1 or newer
        if "exec_file" in kwargs:
            exec_file = kwargs["exec_file"]
        else:  # get default executable
            exec_file = get_ansys_path()
            if exec_file is None:
                raise FileNotFoundError(
                    "Invalid exec_file path or cannot load cached "
                    "ansys path.  Enter one manually using "
                    "exec_file=<path to executable>"
                )

        if version_from_path("mapdl", exec_file) < 211:
            raise VersionError("LocalMapdlPool requires MAPDL 2021R1 or later.")

        # grab available ports
        ports = available_ports(n_instances, port)

        if self._root_dir is not None:
            if not os.path.isdir(self._root_dir):
                os.makedirs(self._root_dir)

        self._instances = []
        self._active = True  # used by pool monitor

        n_instances = int(n_instances)
        if n_instances < 2:
            raise ValueError("Must request at least 2 instances to create a pool.")

        pbar = None
        if wait and progress_bar:
            if not _HAS_TQDM:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"To use the keyword argument 'progress_bar', you need to have installed the 'tqdm' package. "
                    "To avoid this message you can set 'progress_bar=False'."
                )

            pbar = tqdm(total=n_instances, desc="Creating Pool")

        # initialize a list of dummy instances
        self._instances = [None for _ in range(n_instances)]

        # threaded spawn
        threads = [
            self._spawn_mapdl(i, ports[i], pbar, name=f"Instance {i}")
            for i in range(n_instances)
        ]
        if wait:
            [thread.join() for thread in threads]

            # check if all clients connected have connected
            if len(self) != n_instances:
                n_connected = len(self)
                warnings.warn(
                    f"Only %d clients connected out of %d requested"
                    % (n_connected, n_instances)
                )
            if pbar is not None:
                pbar.close()

        # monitor pool if requested
        if restart_failed:
            self._pool_monitor_thread = self._monitor_pool(name="Monitoring_Thread")

        self._verify_unique_ports()

    def _verify_unique_ports(self):
        if len(self._ports) != len(self):
            raise MapdlRuntimeError("MAPDLPool has overlapping ports")

    def map(
        self,
        func,
        iterable=None,
        progress_bar=True,
        close_when_finished=False,
        timeout=None,
        wait=True,
    ):
        """Run a function for each instance of mapdl within the pool.

        Parameters
        ----------
        func : function
            User function with an instance of ``mapdl`` as the first
            argument.  The remaining arguments should match the number
            of items in each iterable (if any).

        iterable : list, tuple, optional
            An iterable containing a set of arguments for ``func``.
            If None, will run ``func`` once for each instance of
            mapdl.

        progress_bar : bool, optional
            Show a progress bar when running the batch.  Defaults to
            ``True``.

        close_when_finished : bool, optional
            Exit the MAPDL instances when the pool is finished.
            Default ``False``.

        timeout : float, optional
            Maximum runtime in seconds for each iteration.  If
            ``None``, no timeout.  If specified, each iteration will
            be only allowed to run ``timeout`` seconds, and then
            killed and treated as a failure.

        wait : bool, optional
            Block execution until the batch is complete.  Default
            ``True``.

        Returns
        -------
        list
            A list containing the return values for ``func``.  Failed
            runs will not return an output.  Since the returns are not
            necessarily in the same order as ``iterable``, you may
            want to add some sort of tracker to the return of your
            user function``func``.

        Examples
        --------
        Run several input files while storing the final routine.  Note
        how the user function to be mapped must use ``mapdl`` as the
        first argument.  The function can have any number of
        additional arguments.

        >>> completed_indices = []
        >>> def func(mapdl, input_file, index):
                # input_file, index = args
                mapdl.clear()
                output = mapdl.input(input_file)
                completed_indices.append(index)
                return mapdl.parameters.routine
        >>> inputs = [(examples.vmfiles['vm%d' % i], i) for i in range(1, 10)]
        >>> output = pool.map(func, inputs, progress_bar=False, wait=True)
        ['Begin level',
         'Begin level',
         'Begin level',
         'Begin level',
         'Begin level',
         'Begin level',
         'Begin level',
         'Begin level',
         'Begin level']
        """

        # check if any instances are available
        if not len(self):
            # instances could still be spawning...
            if not all(v is None for v in self._instances):
                raise MapdlRuntimeError("No MAPDL instances available.")

        results = []

        if iterable is not None:
            n = len(iterable)
        else:
            n = len(self)

        pbar = None
        if progress_bar:
            if not _HAS_TQDM:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"To use the keyword argument 'progress_bar', you need to have installed the 'tqdm' package. "
                    "To avoid this message you can set 'progress_bar=False'."
                )

            pbar = tqdm(total=n, desc="MAPDL Running")

        @threaded_daemon
        def func_wrapper(obj, func, timeout, args=None, name=""):
            """Expect obj to be an instance of Mapdl"""
            complete = [False]

            @threaded_daemon
            def run(name=""):
                if args is not None:
                    if isinstance(args, (tuple, list)):
                        results.append(func(obj, *args))
                    else:
                        results.append(func(obj, args))
                else:
                    results.append(func(obj))
                complete[0] = True

            run_thread = run(name="map.run")
            if timeout:
                tstart = time.time()
                while not complete[0]:
                    time.sleep(0.01)
                    if (time.time() - tstart) > timeout:
                        break

                if not complete[0]:
                    LOG.error("Killed instance due to timeout of %f seconds", timeout)
                    obj.exit()
            else:
                run_thread.join()
                if not complete[0]:
                    try:
                        obj.exit()
                    except:
                        pass

                    # ensure that the directory is cleaned up
                    if obj._cleanup:
                        # allow MAPDL to die
                        time.sleep(5)
                        if os.path.isdir(obj.directory):
                            try:
                                shutil.rmtree(obj.directory)
                            except Exception as e:
                                LOG.warning(
                                    "Unable to remove directory at %s:\n%s",
                                    obj.directory,
                                    str(e),
                                )

            obj.locked = False
            if pbar:
                pbar.update(1)

        threads = []
        if iterable is not None:
            threads = []
            for args in iterable:
                # grab the next available instance of mapdl
                instance = self.next_available()
                instance.locked = True
                threads.append(
                    func_wrapper(instance, func, timeout, args, name="Map_Thread")
                )

            if close_when_finished:
                # start closing any instances that are not in execution
                while not all(v is None for v in self._instances):
                    # grab the next available instance of mapdl and close it
                    instance, i = self.next_available(return_index=True)
                    self._instances[i] = None

                    try:
                        instance.exit()
                    except Exception as e:
                        LOG.error("Failed to close instance", exc_info=True)

            else:
                # wait for all threads to complete
                if wait:
                    [thread.join() for thread in threads]

        else:  # simply apply to all
            for instance in self._instances:
                if instance:
                    threads.append(func_wrapper(instance, func, timeout))

            # wait for all threads to complete
            if wait:
                [thread.join() for thread in threads]

        return results

    def run_batch(
        self,
        files,
        clear_at_start=True,
        progress_bar=True,
        close_when_finished=False,
        timeout=None,
        wait=True,
    ):
        """Run a batch of input files on the pool.

        Parameters
        ----------
        files : list
            List of input files to run.

        clear_at_start : bool, optional
            Clear MAPDL at the start of execution.  By default this is
            ``True``, and setting this to ``False`` may lead to
            instability.

        progress_bar : bool, optional
            Show a progress bar when starting the pool.  Defaults to
            ``True``.  Will not be shown when ``wait=False``

        progress_bar : bool, optional
            Show a progress bar when running the batch.  Defaults to
            ``True``.

        close_when_finished : bool, optional
            Exit the MAPDL instances when the pool is finished.
            Default ``False``.

        timeout : float, optional
            Maximum runtime in seconds for each iteration.  If
            ``None``, no timeout.  If specified, each iteration will
            be only allowed to run ``timeout`` seconds, and then
            killed and treated as a failure.

        wait : bool, optional
            Block execution until the batch is complete.  Default
            ``True``.

        Returns
        -------
        list
            List of text outputs from MAPDL for each batch run.  Not
            necessarily in the order of the inputs. Failed runs will
            not return an output.  Since the returns are not
            necessarily in the same order as ``iterable``, you may
            want to add some sort of tracker or note within the input files.

        Examples
        --------
        Run 20 verification files on the pool

        >>> from ansys.mapdl import examples
        >>> files = [examples.vmfiles['vm%d' % i] for i in range(1, 21)]
        >>> outputs = pool.run_batch(files)
        >>> len(outputs)
        20
        """
        # check all files exist before running
        for filename in files:
            if not os.path.isfile(filename):
                raise FileNotFoundError("Unable to locate file %s" % filename)

        def run_file(mapdl, input_file):
            if clear_at_start:
                mapdl.finish(mute=True)
                mapdl.clear(mute=True)
            return mapdl.input(input_file)

        return self.map(run_file, files, progress_bar=progress_bar)

    def next_available(self, return_index=False):
        """Wait until an instance of mapdl is available and return that instance.

        Parameters
        ----------
        return_index : bool, optional
            Return the index along with the instance.  Default ``False``.

        Returns
        -------
        pyansys.MapdlGrpc
            Instance of MAPDL.

        int
            Index within the pool of the instance of MAPDL.  By
            default this is not returned.

        Examples
        --------
        >>> mapdl = pool.next_available()
        >>> print(mapdl)
        Product:         ANSYS Mechanical Enterprise
        MAPDL Version:   RELEASE                    BUILD  0.0      UPDATE        0
        PyANSYS Version: 0.55.1
        """

        # loop until the next instance is available
        while True:
            for i, instance in enumerate(self._instances):
                if not instance:  # if encounter placeholder
                    continue

                if not instance.locked and not instance._exited:
                    # any instance that is not running or exited
                    # should be available
                    if not instance.busy:
                        # double check that this instance is alive:
                        try:
                            instance.inquire("", "JOBNAME")
                        except:
                            instance.exit()
                            continue

                        if return_index:
                            return instance, i
                        else:
                            return instance
                    else:
                        instance._exited = True

    def __del__(self):
        self.exit()

    def exit(self, block=False):
        """Close out all instances in the pool.

        Parameters
        ----------
        block : bool, optional
            When ``True``, wait until all processes are closed.

        Examples
        --------
        >>> pool.exit()
        """
        self._active = False  # kills any active instance restart

        @threaded
        def threaded_exit(index, instance):
            if instance:
                try:
                    instance.exit()
                except:
                    pass
                self._instances[index] = None
                # LOG.debug("Exited instance: %s", str(instance))

        threads = []
        for i, instance in enumerate(self):
            threads.append(threaded_exit(i, instance))

        if block:
            [thread.join() for thread in threads]

    def __len__(self):
        count = 0
        for instance in self._instances:
            if instance:
                if not instance._exited:
                    count += 1
        return count

    def __getitem__(self, key):
        """Return an instance by an index"""
        return self._instances[key]

    def __iter__(self):
        """Iterate through active instances"""
        for instance in self._instances:
            if instance:
                yield instance

    @threaded_daemon
    def _spawn_mapdl(self, index, port=None, pbar=None, name=""):
        """Spawn a mapdl instance at an index"""
        # create a new temporary directory for each instance
        run_location = create_temp_dir(self._root_dir)
        self._instances[index] = launch_mapdl(
            run_location=run_location, port=port, **self._spawn_kwargs
        )
        # LOG.debug("Spawned instance %d. Name '%s'", index, name)
        if pbar is not None:
            pbar.update(1)

    @threaded_daemon
    def _monitor_pool(self, refresh=1.0, name=""):
        """Checks if instances within a pool have exited (failed) and
        restarts them.
        """
        while self._active:
            for index, instance in enumerate(self._instances):
                if not instance:  # encountered placeholder
                    continue
                if instance._exited:
                    try:
                        # use the next port after the current available port
                        port = max(self._ports) + 1
                        self._spawn_mapdl(
                            index, port=port, name=f"Instance {index}"
                        ).join()
                    except Exception as e:
                        LOG.error(e, exc_info=True)
            time.sleep(refresh)

    @property
    def _ports(self):
        return [inst._port for inst in self if inst is not None]

    def __repr__(self):
        return "MAPDL Pool with %d active instances" % len(self)
