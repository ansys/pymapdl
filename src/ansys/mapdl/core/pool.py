# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

"""This module is for threaded implementations of the mapdl interface"""
import os
import shutil
import socket
import tempfile
import time
from typing import Any, Dict, List, Optional, Union
import warnings
import weakref

from ansys.mapdl.core import LOG, launch_mapdl
from ansys.mapdl.core.errors import MapdlRuntimeError, VersionError
from ansys.mapdl.core.launcher import (
    LOCALHOST,
    MAPDL_DEFAULT_PORT,
    check_valid_ip,
    get_start_instance,
    port_in_use,
)
from ansys.mapdl.core.mapdl_grpc import _HAS_TQDM
from ansys.mapdl.core.misc import create_temp_dir, threaded, threaded_daemon

try:
    from ansys.tools.path import get_ansys_path, version_from_path

    _HAS_ATP = True
except ModuleNotFoundError:
    _HAS_ATP = False

if _HAS_TQDM:
    from tqdm import tqdm

    DEFAULT_PROGRESS_BAR = True
else:
    DEFAULT_PROGRESS_BAR = False


def available_ports(n_ports: int, starting_port: int = MAPDL_DEFAULT_PORT) -> List[int]:
    """Return a list the first ``n_ports`` ports starting from ``starting_port``."""

    port = starting_port
    ports: List[int] = []
    while port < 65536 and len(ports) < n_ports:
        if not port_in_use(port):
            ports.append(port)
        port += 1

    if len(ports) < n_ports:
        raise MapdlRuntimeError(
            f"There are not {n_ports} available ports between {starting_port} and 65536"
        )

    return ports


class MapdlPool:
    """Create a pool of MAPDL instances.

    .. note::
       Requires MAPDL 2020 R2 or later.

    Parameters
    ----------
    n_instances : int, optional
        Number of instances to create. This argument can be optional if the
        number of instances can be inferred from the ``ip`` and/or ``port``
        arguments. See these arguments documentation for more information.

    wait : bool, optional
        Wait for pool to be initialized.  Otherwise, pool will start
        in the background and all resources may not be available instantly.

    run_location : str, optional
        Base directory to create additional directories for each MAPDL
        instance.  Defaults to a temporary working directory.

    ip : str, list[str], optional
        IP address(es) to connect to where the MAPDL instances are running. You
        can use one IP, if you have multiple instances running on it, but in
        that case you must specify all the ports using the argument `port`.
        If using a list of IPs, the number of ports in 'port' argument should
        match the number of IPs.

    port : int, list[int], optional
        The ports where the MAPDL instances are started on or can be connected to.
        If you are connecting to a single remote instance (only one IP in ``ip``
        argument), you must specify a number of ports equal to the number of
        instances you want to connect to.
        If you are connecting to multiple instances (multiple IPs in ``ip``
        argument), the amount of ports, should match the number of IPs.

        If only one port is specified and you are starting the MAPDL instances
        locally (``start_instance`` is ``True``), this port is the port for the
        first instance. The rest of the instances ports are unitarian increments of
        port, as long as these ports are free from other processes usage.
        If you are not starting the MAPDL instances local, PyMAPDL does not check
        whether these ports are busy or not.
        Defaults to 50052.

    progress_bar : bool, optional
        Show a progress bar when starting the pool.  Defaults to
        ``True``.  Will not be shown when ``wait=False``.

    restart_failed : bool, optional
        Restarts any failed instances in the pool. Defaults to ``True``.

    remove_temp_files : bool, optional
        This launcher creates a new MAPDL working directory for each instance
        of MAPDL within the temporary user directory, obtainable with
        ``tempfile.gettempdir()``, for MAPDL files. When this parameter is
        ``True``, this directory will be deleted when MAPDL is exited. Default
        ``False``.

    names : str, Callable, optional
        You can specify the names of the directories where the instances are
        created. A string or a function (callable) that accepts an integer and
        return an string can be used.
        If you use a string, "_{i}" is appended to that string, where "i" is
        the index of each instance in the pool.
        By default, the instances directories are named as "Instances_{i}".

    override: bool, optional
        Attempts to delete the lock file at the run_location.
        Useful when a prior MAPDL session has exited prematurely and
        the lock file has not been deleted.

    start_instance : bool, optional
        Set it to ``False`` to make PyMAPDL to connect to remote instances instead
        of launching them. In that case, you need to supply the MAPDL instances
        ports as a list of ``int`` s.

    exec_file: str, optional
        The location of the MAPDL executable.  Will use the cached
        location when left at the default ``None``.

    **kwargs : dict, optional
        Additional keyword arguments. For a complete listing, see the
        description for the :func:`ansys.mapdl.core.launcher.launch_mapdl`
        method.

    Examples
    --------
    Simply create a pool of 10 instances to run in the temporary
    directory.

    >>> from ansys.mapdl.core import MapdlPool
    >>> pool = MapdlPool(10)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    Create several instances with 1 CPU each running at the current
    directory within their own isolated directories.

    >>> import os
    >>> my_path = os.getcmd()
    >>> pool = MapdlPool(10, nproc=1, run_location=my_path)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    Create a pool while specifying the MAPDL executable in Windows.

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v212/ansys/bin/winx64/ANSYS212.exe'
    >>> pool = MapdlPool(10, exec_file=exec_file)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    Create a pool while specifying the MAPDL executable in Linux.

    >>> exec_file = '/ansys_inc/v211/ansys/bin/ansys211'
    >>> pool = MapdlPool(10, exec_file=exec_file)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    Create a pool of instances in multiple instances and with different ports:

    >>> pool = MapdlPool(ip=["123.0.0.1", "123.0.0.2", "123.0.0.3", "123.0.0.4"], port=[50052, 50053, 50055, 50060])
    Creating Pool: 100%|########| 4/4 [00:01<00:00,  1.23it/s]

    """

    def __init__(
        self,
        n_instances: int = None,
        wait: bool = True,
        run_location: Optional[str] = None,
        ip: Optional[Union[str, List[str]]] = None,
        port: Union[int, List[int]] = MAPDL_DEFAULT_PORT,
        progress_bar: bool = DEFAULT_PROGRESS_BAR,
        restart_failed: bool = True,
        remove_temp_files: bool = True,
        names: Optional[str] = None,
        override=True,
        start_instance: bool = None,
        exec_file: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Initialize several instances of mapdl"""
        self._instances: List[None] = []

        # Getting debug arguments
        _debug_no_launch = kwargs.pop("_debug_no_launch", None)

        if run_location is None:
            run_location = tempfile.gettempdir()
        self._root_dir: str = run_location

        kwargs["remove_temp_files"] = remove_temp_files
        kwargs["mode"] = "grpc"
        self._spawn_kwargs: Dict[str, Any] = kwargs
        self._spawning_i: int = 0
        self._exiting_i: int = 0
        self._override = override

        # Getting IP from env var
        ip_env_var = os.environ.get("PYMAPDL_IP", "")
        if ip_env_var != "":
            if ip:
                warnings.warn(
                    "The env var 'PYMAPDL_IP' is set, hence the 'ip' argument is overwritten."
                )

            ip = ip_env_var
            LOG.debug(f"An IP ({ip}) has been set using 'PYMAPDL_IP' env var.")

        ip = None if ip == "" else ip  # Making sure the variable is not empty

        # Getting "start_instance" using "True" as default.
        if (ip is not None) and (start_instance is None):
            # An IP has been supplied. By default, 'start_instance' is equal
            # false, unless it is set through the env vars.
            start_instance = get_start_instance(start_instance=False)
        else:
            start_instance = get_start_instance(start_instance=start_instance)

        self._start_instance = start_instance
        LOG.debug(f"'start_instance' equals to '{start_instance}'")

        n_instances, ips, ports = self._set_n_instance_ip_port_args(
            n_instances, ip, port
        )

        # Converting ip or hostname to ip
        ips = [socket.gethostbyname(each) for each in ips]
        _ = [check_valid_ip(each) for each in ips]  # double check

        self._ips = ips

        if not names:
            names = "Instance"

        if isinstance(names, str):
            self._names = lambda i: names + "_" + str(i)
        elif callable(names):
            self._names = names
        else:
            raise ValueError(
                "Only strings or functions are allowed in the argument 'name'."
            )

        # verify executable
        exec_file = os.getenv("PYMAPDL_MAPDL_EXEC", exec_file)

        if start_instance:
            exec_file = kwargs.get("exec_file", exec_file)

            if not exec_file:  # get default executable
                if _HAS_ATP:
                    exec_file = get_ansys_path()
                else:
                    raise ValueError(
                        "Please use 'exec_file' argument to specify the location of the ansys installation.\n"
                        "Alternatively, PyMAPDL can detect your ansys installation if you install 'ansys-tools-path' library."
                    )

                if exec_file is None:
                    raise FileNotFoundError(
                        "Invalid exec_file path or cannot load cached "
                        "ansys path.  Enter one manually using "
                        "exec_file=<path to executable>"
                    )

            # Checking version
            if _HAS_ATP:
                if version_from_path("mapdl", exec_file) < 211:
                    raise VersionError("MapdlPool requires MAPDL 2021R1 or later.")

        self._exec_file = exec_file

        # grab available ports
        if (
            start_instance
            and self._root_dir is not None
            and not os.path.isdir(self._root_dir)
        ):
            os.makedirs(self._root_dir)

        LOG.debug(f"Using ports: {ports}")

        self._instances = []
        self._active = True  # used by pool monitor

        pbar = None
        if wait and progress_bar:
            if not _HAS_TQDM:  # pragma: no cover
                raise ModuleNotFoundError(
                    "To use the keyword argument 'progress_bar', you need to have installed the 'tqdm' package. "
                    "To avoid this message you can set 'progress_bar=False'."
                )

            pbar = tqdm(total=n_instances, desc="Creating Pool")

        # initialize a list of dummy instances
        self._instances = [None for _ in range(n_instances)]

        # threaded spawn
        if _debug_no_launch:
            self._debug_no_launch = {
                "ports": ports,
                "ips": ips,
                "names": self._names,
                "start_instance": start_instance,
                "exec_file": exec_file,
                "n_instances": n_instances,
            }
            return

        threads = [
            self._spawn_mapdl(
                i,
                ip=ip,
                port=port,
                pbar=pbar,
                name=self._names(i),
                thread_name=self._names(i),
                start_instance=start_instance,
                exec_file=exec_file,
            )
            for i, (ip, port) in enumerate(zip(ips, ports))
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
            # This name is using the wrapped to specify the thread name
            self._pool_monitor_thread = self._monitor_pool(
                thread_name="Monitoring_Thread"
            )

        self._verify_unique_ports()

    @property
    def _spawning(self) -> bool:
        """Return true if spawning new MAPDL instance"""
        # Because spawning is threaded, we need to make sure we are approaching this
        # with counters instead of a bool.

        return self._spawning_i != 0

    @property
    def _exiting(self) -> bool:
        """Return true if exiting a MAPDL instance"""
        # Because exiting is threaded, we need to make sure we are approaching this
        # with counters instead of a bool.

        return self._exiting_i != 0

    def _verify_unique_ports(self) -> None:
        if len(self._ports) != len(self):
            raise MapdlRuntimeError("MAPDLPool has overlapping ports")

    def map(
        self,
        func,
        iterable=None,
        progress_bar=DEFAULT_PROGRESS_BAR,
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
        def func_wrapper(obj, func, timeout, args=None):
            """Expect obj to be an instance of Mapdl"""
            complete = [False]

            @threaded_daemon
            def run():
                if args is not None:
                    if isinstance(args, (tuple, list)):
                        results.append(func(obj, *args))
                    else:
                        results.append(func(obj, args))
                else:
                    results.append(func(obj))
                complete[0] = True

            run_thread = run(thread_name="map.run")
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
                    func_wrapper(
                        instance, func, timeout, args, thread_name="Map_Thread"
                    )
                )

            if close_when_finished:
                # start closing any instances that are not in execution
                while not all(v is None for v in self._instances):
                    # grab the next available instance of mapdl and close it
                    instance, i = self.next_available(return_index=True)
                    self._instances[i] = None

                    try:
                        self._exiting_i += 1
                        instance.exit()
                    except Exception as e:
                        LOG.error("Failed to close instance", exc_info=True)
                        self._exiting_i -= 1

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
        progress_bar=DEFAULT_PROGRESS_BAR,
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

        return self.map(
            run_file,
            files,
            progress_bar=progress_bar,
            timeout=timeout,
            wait=wait,
            close_when_finished=close_when_finished,
        )

    class _mapdl_pool_ctx:
        """Provides the context manager for the ``MapdlPool`` class.

        This context manager sets the MAPDL instance as ``busy`` and ``locked`` when
        entering and then unsets the instance state when exiting.
        """

        def __init__(self, parent: "MapdlPool", return_index: bool = False):
            self._parent = weakref.ref(parent)
            self._instance = None
            self._return_index = return_index

        def __enter__(self):
            if self._return_index:
                mapdl, i = self._parent().next_available(return_index=True)
                self._index = i

            else:
                mapdl = self._parent().next_available(return_index=False)

            self._instance = mapdl
            mapdl.locked = True
            mapdl._busy = True

            if self._return_index:
                return mapdl, i
            else:
                return mapdl

        def __exit__(self, *args):
            mapdl = self._instance
            mapdl.locked = False
            mapdl._busy = False

    def next(self, return_index: bool = False):
        """Return a context manager that returns available instances.

        This method manages the instance state (`locked` and `busy`) when the code enters
        and exits the code block.

        Parameters
        ----------
        return_index : bool, optional
            Whether to return the index along with the instance.  The default is ``False``.

        Returns
        -------
        ctx
            Context manager to manage ``MapdlPool`` instances.
        """
        return self._mapdl_pool_ctx(self, return_index)

    def next_available(self, return_index: bool = False, as_ctx: bool = False):
        """Wait until an instance of MAPDL is available and return that instance.

        Parameters
        ----------
        return_index : bool, optional
            Return the index along with the instance.  Default ``False``.

        Returns
        -------
        MapdlGrpc
            Instance of MAPDL.

        int
            Index within the pool of the instance of MAPDL.  By
            default this is not returned.

        Examples
        --------
        >>> mapdl = pool.next_available()
        >>> print(mapdl)
        Product:             Ansys Mechanical Enterprise
        MAPDL Version:       24.1
        ansys.mapdl Version: 0.68.dev0
        """
        if as_ctx:
            return self.next(return_index)
        else:
            return self._next_available(return_index)

    def _next_available(self, return_index: bool = False):
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
                self._exiting_i += 1
                try:
                    instance.exit()
                except:
                    pass
                self._instances[index] = None
                # LOG.debug("Exited instance: %s", str(instance))
                self._exiting_i -= 1

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

    def __getitem__(self, key: int):
        """Return an instance by an index"""

        # Regarding issue 2173.
        # there are two options here:
        # * the MAPDL instance hasn't be created yet. It is threaded.
        # * it died and it hasn't been relaunched.
        # Because we are seeing some random errors, I would bet on the first
        time0 = time.time()
        timeout = 10  # seconds
        while (
            self._instances[key] is None
            and time.time() < (time0 + timeout)
            and self._spawning
        ):
            time.sleep(0.1)
            # We could respawn an instance here, but later at some parts of the code,
            # we do check if the instance is None.

        return self._instances[key]

    def __iter__(self):
        """Iterate through active instances"""
        for instance in self._instances:
            if instance:
                yield instance

    @threaded_daemon
    def _spawn_mapdl(
        self,
        index: int,
        ip: str = None,
        port: int = None,
        pbar: Optional[bool] = None,
        name: str = "",
        start_instance=True,
        exec_file=None,
    ):
        """Spawn a mapdl instance at an index"""
        # create a new temporary directory for each instance
        self._spawning_i += 1

        run_location = create_temp_dir(self._root_dir, name=name)

        self._instances[index] = launch_mapdl(
            exec_file=exec_file,
            run_location=run_location,
            port=port,
            ip=ip,
            override=True,
            start_instance=start_instance,
            **self._spawn_kwargs,
        )

        # Waiting for the instance being fully initialized.
        # This is introduce to mitigate #2173
        while self._instances[index] is None:
            time.sleep(0.1)

        assert not self._instances[index].exited
        self._instances[index].prep7()

        # LOG.debug("Spawned instance %d. Name '%s'", index, name)
        if pbar is not None:
            pbar.update(1)

        self._spawning_i -= 1

    @threaded_daemon
    def _monitor_pool(self, refresh=1.0):
        """Checks if instances within a pool have exited (failed) and
        restarts them.


        """
        while self._active:
            for index, instance in enumerate(self._instances):
                name = self._names(index)
                if not instance:  # encountered placeholder
                    continue

                if instance._exited:
                    try:
                        self._spawning_i += 1

                        self._spawn_mapdl(
                            index,
                            port=instance.port,
                            name=name,
                            thread_name=name,
                            exec_file=self._exec_file,
                            start_instance=self._start_instance,
                        ).join()

                    except Exception as e:
                        LOG.error(e, exc_info=True)
                        self._spawning_i -= 1

            time.sleep(refresh)

    @property
    def _ports(self):
        return [inst._port for inst in self if inst is not None]

    def __repr__(self):
        return "MAPDL Pool with %d active instances" % len(self)

    def _set_n_instance_ip_port_args(self, n_instances, ip, port):
        if n_instances is None:
            if ip is None or (isinstance(ip, list) and len(ip) == 0):
                if port is None or (isinstance(port, list) and len(port) < 1):
                    raise ValueError(
                        "The number of instances could not be inferred "
                        "from arguments 'n_instances', 'ip' nor 'port'."
                    )

                elif isinstance(port, int):
                    n_instances = 1
                    ports = [port]
                    ips = [LOCALHOST]

                elif isinstance(port, list):
                    n_instances = len(port)
                    ports = port
                    ips = [LOCALHOST for i in range(n_instances)]
                else:
                    raise TypeError(
                        "Argument 'port' does not support this type of argument."
                    )

            elif isinstance(ip, str):
                # only one IP
                if isinstance(port, list):
                    if len(port) > 0:
                        n_instances = len(port)
                        ports = port
                        ips = [ip for each in range(n_instances)]
                    else:
                        raise ValueError(
                            "The number of ports should be higher than"
                            " zero if using only one IP address."
                        )

            elif isinstance(ip, list):
                n_instances = len(ip)
                ips = ip

                if self._start_instance:
                    raise ValueError(
                        "If using 'start_instance', 'ip' cannot be"
                        "a list of IPs since PyMAPDL cannot start instances remotely."
                    )

                if port is None or isinstance(port, int):
                    ports = [port or MAPDL_DEFAULT_PORT for i in range(n_instances)]

                elif isinstance(port, list):
                    if len(port) != len(ips):
                        raise ValueError(
                            f"The number of ports ({len(port)}) should be the same as the number of IPs ({len(ips)})."
                        )
                    ports = port

                else:
                    raise TypeError(
                        "Argument 'port' does not support this type of argument."
                    )
            else:
                raise TypeError("Argument 'ip' does not support this type of argument.")

        else:

            if not isinstance(n_instances, int):
                raise TypeError("Only integers are allowed for 'n_instances' argument.")

            if n_instances < 1:
                raise ValueError("Must request at least 1 instance to create a pool.")

            if ip is None:
                ips = [LOCALHOST for i in range(n_instances)]

                if port is None or isinstance(port, int):
                    port = port or MAPDL_DEFAULT_PORT
                    if self._start_instance:
                        ports = available_ports(n_instances, port)
                    else:
                        ports = [port + i for i in range(n_instances)]

                elif isinstance(port, list) and len(port) != n_instances:
                    raise ValueError(
                        "If using 'n_instances' and 'port' without multiple 'ip', "
                        "you should provide as many ports as number of instances requested."
                    )
                elif isinstance(port, list):
                    ports = port
                else:
                    raise TypeError(
                        "Argument 'port' does not support this type of argument."
                    )

            elif isinstance(ip, str):
                ips = [ip for i in range(n_instances)]
                if (
                    port is None
                    or isinstance(port, int)
                    or (isinstance(port, list) and len(port) != n_instances)
                ):
                    raise ValueError(
                        "If using 'n_instances' and only one 'ip', "
                        "you should provide as many ports as number of instances requested."
                    )
                else:
                    ports = port

            elif isinstance(ip, list):
                if len(ip) != n_instances:
                    raise ValueError(
                        f"The number of IPs ({len(ip)}) should be the same as the number of instances ({n_instances})."
                    )

                ips = ip
                if port is None or isinstance(port, int):
                    ports = [port or MAPDL_DEFAULT_PORT for i in range(n_instances)]

                elif isinstance(port, list):
                    if len(port) != n_instances:
                        raise ValueError(
                            "If using 'n_instances', and multiple ips and ports, "
                            "you should provide as many ports as number of instances requested."
                        )
                    ports = port
                else:
                    raise TypeError(
                        "Argument 'port' does not support this type of argument."
                    )

            else:
                raise TypeError("Argument 'ip' does not support this type of argument.")

        return n_instances, ips, ports
