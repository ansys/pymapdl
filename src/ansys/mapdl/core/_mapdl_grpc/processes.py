# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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

"""Local MAPDL process discovery, output pipes and termination."""

import os
import re

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
import subprocess  # nosec B404
import threading
import time
from typing import Optional

import psutil

from ansys.mapdl.core.errors import (
    MapdlConnectionError,
    MapdlRuntimeError,
)

from . import _GrpcMixinBase


def _drain_queue(queue) -> str:
    """Drain all available items from a queue into a string.

    Parameters
    ----------
    queue : Queue or None
        A queue whose items are bytes or strings. If ``None``, returns an
        empty string.

    Returns
    -------
    str
        All currently-available queue items joined into a single string.
    """
    if queue is None:
        return ""
    lines = []
    while not queue.empty():
        try:
            lines.append(queue.get_nowait().decode(errors="replace"))
        except Exception:
            break
    return "".join(lines)


class _GrpcProcessMixin(_GrpcMixinBase):
    """Local MAPDL process discovery, output pipes and termination."""

    def _create_process_stds_queue(self, process=None):
        from ansys.mapdl.core.launcher import (
            _create_queue_for_std,  # Avoid circular import error
        )

        if not process:
            process = self._mapdl_process

        self._stdout_queue, self._stdout_thread = _create_queue_for_std(process.stdout)
        self._stderr_queue, self._stderr_thread = _create_queue_for_std(process.stderr)

    @staticmethod
    def _check_process_handle(proc) -> bool | None:
        """Return whether *proc* is alive, normalising psutil/Popen handles.

        Parameters
        ----------
        proc : psutil.Process | subprocess.Popen
            A process handle with either an ``is_running()`` method
            (psutil-style) or a ``poll()`` method (Popen-style).

        Returns
        -------
        bool or None
            ``True`` if the process is alive, ``False`` if it has exited or
            if ``is_running()`` raised ``NoSuchProcess``, ``None`` if *proc*
            has neither ``is_running`` nor ``poll`` (unknown handle type).
        """
        try:
            if hasattr(proc, "is_running"):
                return bool(proc.is_running())
            if hasattr(proc, "poll"):
                return proc.poll() is None
        except psutil.NoSuchProcess:
            return False
        return None

    def _is_alive_subprocess(self) -> bool | None:
        """Check whether the MAPDL subprocess is still running.

        Returns
        -------
        bool or None
            * ``True`` if the process is alive.
            * ``False`` if the process has exited.
            * ``None`` if no process handle is stored, or if the handle has
              an unknown type (no ``is_running`` / ``poll``) and no ``pid``
              attribute to fall back on.

        Notes
        -----
        Checks liveness in priority order to avoid PID-reuse false-positives
        on Windows:

        1. ``is_running()`` / ``poll()`` on the stored process handle.
        2. ``psutil.pid_exists()`` on ``_mapdl_process.pid`` as a last resort.
        """
        if not self._mapdl_process:
            return None

        proc_status = self._check_process_handle(self._mapdl_process)
        if proc_status is not None:
            return proc_status

        # Unknown handle type — fall back to PID existence check.
        pid = getattr(self._mapdl_process, "pid", None)
        if pid is None:
            return None
        return psutil.pid_exists(int(pid))

    def _find_live_mapdl_processes(self) -> "list[psutil.Process]":
        """Discover live MAPDL processes when the stored process handle has exited.

        On Windows the launcher typically starts a terminal process that spawns
        MAPDL and then exits immediately.  When ``_mapdl_process`` (the
        terminal) reports not-alive this method tries to find the actual MAPDL
        server process via the following priority chain:

        1. Port check — asks the OS which process is listening on
           ``self._port``.  Fastest and most accurate.
        2. Live ``_mapdl_process`` — returned as-is if it is still running.
        3. Cached ``_pids`` — any PID in ``self._pids`` that psutil confirms
           is still alive.
        4. Heuristic system scan — iterates ``psutil.process_iter()`` matching
           by CWD (``self._path``), job name in the command line, or the ANSYS/
           MAPDL process name pattern.

        Returns
        -------
        list[psutil.Process]
            Live ``psutil.Process`` objects that correspond to MAPDL.  Empty
            list if none are found.
        """
        try:
            if found := self._find_process_at_port():
                return found
            if found := self._find_process_from_handle():
                return found
            if found := self._find_processes_from_cached_pids():
                return found
            return self._find_processes_by_heuristic()
        except Exception:
            return []

    def _find_process_at_port(self) -> "list[psutil.Process]":
        """Return the process listening on ``self._port``, if any.

        Returns
        -------
        list[psutil.Process]
            A one-element list with the running process, or ``[]``.
        """
        if not getattr(self, "_port", None):
            return []
        from ansys.mapdl.core.launcher.network import get_process_at_port

        proc = get_process_at_port(self._port)
        if proc and proc.is_running():
            return [proc]
        return []

    def _find_process_from_handle(self) -> "list[psutil.Process]":
        """Return the stored ``_mapdl_process`` handle if it is still alive.

        Returns
        -------
        list[psutil.Process]
            A one-element list wrapping the live process, or ``[]``.
        """
        if not self._mapdl_process or not self._check_process_handle(
            self._mapdl_process
        ):
            return []
        pid = getattr(self._mapdl_process, "pid", None)
        try:
            return [psutil.Process(pid)] if pid is not None else [self._mapdl_process]
        except psutil.NoSuchProcess:
            return []

    def _find_processes_from_cached_pids(self) -> "list[psutil.Process]":
        """Return live processes from the cached ``self._pids`` list.

        Returns
        -------
        list[psutil.Process]
            All cached PIDs that are still alive as ``psutil.Process`` objects.
        """
        found: list[psutil.Process] = []
        for pid in [p for p in (self._pids or []) if p]:
            try:
                proc = psutil.Process(pid)
                if proc.is_running():
                    found.append(proc)
            except psutil.NoSuchProcess:
                continue
        return found

    def _find_processes_by_heuristic(self) -> "list[psutil.Process]":
        """Scan running processes for MAPDL candidates using heuristics.

        Matches by CWD (``self._path``), jobname in the command line, or the
        ANSYS/MAPDL process-name pattern (via
        :func:`~ansys.mapdl.core.launcher.network._is_mapdl_process`).

        Returns
        -------
        list[psutil.Process]
            All matching live processes, or ``[]`` if none found.
        """
        from ansys.mapdl.core.launcher.network import _is_mapdl_process

        cwd_to_match = os.path.abspath(str(self._path)) if self._path else None
        jobname = getattr(self, "_jobname", None) or self.jobname

        if not cwd_to_match and not jobname:
            return []

        found: list[psutil.Process] = []
        for p in psutil.process_iter(["pid", "name", "cmdline", "cwd"]):
            try:
                info = p.info
                # Match by working directory.
                if cwd_to_match and info.get("cwd"):
                    if os.path.abspath(str(info["cwd"])).startswith(cwd_to_match):
                        if p.is_running():
                            found.append(p)
                            continue

                # Match by jobname in command line.
                cmdline = info.get("cmdline") or []
                if jobname and any(jobname in str(x) for x in cmdline):
                    if p.is_running():
                        found.append(p)
                        continue

                # Fallback: ANSYS/MAPDL process name heuristic.
                if _is_mapdl_process(p) and p.is_running():
                    found.append(p)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return found

    @property
    def process_is_alive(self):
        """Check if the MAPDL process is alive.

        Returns
        -------
        bool
            True if the MAPDL process is alive, False otherwise.
        """
        return self._is_alive_subprocess()

    def _get_process_exit_signal(self) -> Optional[int]:
        """Return the POSIX signal number that terminated the MAPDL process.

        Returns
        -------
        int or None
            The signal number (for example ``9`` for ``SIGKILL``) if the
            locally tracked subprocess was terminated by a signal. Returns
            ``None`` if the process is still running, exited normally (a
            non-negative return code), or if no local process handle is
            available (for example, when connected to a remote or
            already-running MAPDL instance, where PyMAPDL is not the parent
            process and cannot retrieve its exit status).

        Notes
        -----
        This relies on ``subprocess.Popen.poll()``, which only reports a
        negative return code (``-signal_number``) on POSIX platforms when the
        child was terminated by a signal. It is ``None`` on Windows, where
        signal-based termination is not exposed the same way.

        A ``SIGKILL`` (9) result is a strong indicator that the process was
        forcibly terminated by the operating system, most commonly the Linux
        Out-Of-Memory (OOM) killer, though it can also result from a manual
        ``kill -9`` or a job scheduler enforcing a resource limit.

        Examples
        --------
        >>> mapdl._get_process_exit_signal()
        9
        """
        process = self._mapdl_process
        if process is None or not hasattr(process, "poll"):
            return None

        returncode = process.poll()
        if returncode is None or returncode >= 0:
            # Still running, or exited normally/with a non-signal error code.
            return None

        return -returncode

    def _post_mortem_checks(self, process=None):
        """Check possible reasons for not having a successful connection."""
        # Check early exit
        if process is None:
            process = self._mapdl_process

        if process is None or not self.is_grpc:
            return

        # check the stdout for any errors
        self._read_stds()

        self._check_stds()

    def _read_stds(self):
        """Read the stdout and stderr from the subprocess."""
        if self._mapdl_process is None or not self._mapdl_process.stdout:
            return

        self._log.debug("Reading stdout")
        self._stdout = _drain_queue(self._stdout_queue)
        self._log.debug(f"Read stdout: {self._stdout[:20]}")

        self._log.debug("Reading stderr")
        self._stderr = _drain_queue(self._stderr_queue)
        self._log.debug(f"Read stderr: {self._stderr[:20]}")

    def _check_stds(self, stdout=None, stderr=None):
        """Check the stdout and stderr for any errors."""
        if stdout is None:
            stdout = self._stdout

        if stderr is None:
            stderr = self._stderr

        if not stderr:
            self._log.debug("MAPDL exited without stderr.")
        else:
            self._parse_stderr(stderr)

        if not stdout:
            self._log.debug("MAPDL exited without stdout.")
        else:
            self._parse_stdout(stdout)

    def _parse_stderr(self, stderr=None):
        """Parse the stderr for any errors."""
        if stderr is None:
            stderr = self._stderr

        errs = self._parse_std(stderr)

        if errs:
            self._log.debug("MAPDL exited with errors in stderr.")

            # Custom errors
            self._raise_custom_stds_errors(errs)

    def _parse_stdout(self, stdout=None):
        """Parse the stdout for any errors."""
        if stdout is None:
            stdout = self._stdout

        errs = self._parse_std(stdout)
        if errs:
            self._log.debug("MAPDL exited with errors in stdout.")

            # Custom errors
            self._raise_custom_stds_errors(errs)

    def _parse_std(self, std):
        # check for errors in stderr
        # split the stderr into groups
        if isinstance(std, list):
            std = "\n".join(std)
            std = std.replace("\n\n", "\n")

        groups = std.split("\r\n\r\n")
        errs = []

        for each in groups:
            if (
                "error" in each.lower()
                or "fatal" in each.lower()
                or "warning" in each.lower()
            ):
                errs.append(each)

        if errs:
            errs = "\r\n\r\n".join(errs)
            errs = errs.replace("\r\n", "\n")
        else:
            errs = ""
        return errs

    def _raise_custom_stds_errors(self, errs_message):
        """Custom errors for stdout and stderr."""
        if "Only one usage of each socket address" in errs_message:
            raise MapdlConnectionError(
                f"A process is already running on the specified port ({self._port}).\n"
                "Only one usage of each socket address (protocol/network address/port) is normally permitted.\n"
                f"\nFull error message:\n{errs_message.split('########', 1)[0]}"
            )

        else:
            raise MapdlConnectionError(errs_message)

    def _close_process_pipes(self, process: subprocess.Popen) -> None:  # type: ignore[type-arg]
        """Close all open I/O streams attached to *process*.

        Closes ``process.stdout`` and ``process.stderr`` (PIPE handles) so
        that PIPE-drainer threads blocked on ``readline`` are unblocked and
        can exit.  Also closes the ``_stdout_file_handle`` redirect file, if
        one was attached to the process by ``_start_subprocess``.

        Parameters
        ----------
        process : subprocess.Popen
            The subprocess handle whose streams should be closed.

        Returns
        -------
        None
        """
        for stream in (process.stdout, process.stderr):
            try:
                if stream is not None and not stream.closed:
                    stream.close()
            except OSError as e:
                self._log.debug(f"Error closing process stream: {e}")

        fh = getattr(process, "_stdout_file_handle", None)
        if fh and not getattr(fh, "closed", False):
            try:
                fh.close()
                self._log.debug("Closed stdout file handle")
                setattr(process, "_stdout_file_handle", None)
            except OSError as e:
                self._log.debug(f"Error closing stdout file handle: {e}")

    def _terminate_process(self, process: subprocess.Popen) -> None:  # type: ignore[type-arg]
        """Terminate *process*, wait for it to exit, then close its pipes.

        Sends ``SIGTERM`` and waits up to 2 seconds for the process to exit.
        If it has not exited by then, ``SIGKILL`` is sent and the wait is
        repeated. The stdout/stderr PIPEs are only closed *after* the process
        has exited (or the waits above have been exhausted), and that close
        itself is bounded by a watchdog thread.

        Notes
        -----
        Closing the PIPEs while the process (or one of its children — see
        :meth:`_kill_child_processes`, which must run first) still holds the
        write end open can deadlock: the PIPE-drainer thread is blocked
        inside ``readline()`` holding the stream's internal lock, so
        ``stream.close()`` from this thread blocks forever waiting on that
        same lock instead of raising. Waiting for the process to exit first,
        and bounding the close with a watchdog thread, prevents that hang.

        Parameters
        ----------
        process : subprocess.Popen
            The subprocess handle to terminate.

        Returns
        -------
        None
        """
        if process.poll() is None:
            self._log.debug("Sending SIGTERM to MAPDL process")
            process.terminate()

        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self._log.debug("Process did not exit after SIGTERM; sending SIGKILL")
            process.kill()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._log.debug("Process did not exit after SIGKILL")

        # Close the PIPEs on a daemon watchdog thread bounded to 5 seconds,
        # instead of calling '_close_process_pipes' directly, so a close that
        # unexpectedly blocks (for example, an untracked grandchild process
        # still holding the write end open) cannot hang this thread forever.
        closer = threading.Thread(
            target=self._close_process_pipes, args=(process,), daemon=True
        )
        closer.start()
        closer.join(timeout=5)
        if closer.is_alive():
            self._log.debug(
                "Closing MAPDL process PIPEs did not complete in time; "
                "continuing without waiting further."
            )

    def _join_pipe_drainer_threads(self, exiting: bool = False) -> None:
        """Join all PIPE-drainer threads, giving each up to 2 seconds.

        Waits for ``_stdout_thread``, ``_stderr_thread``, and
        ``_startup_stdout_thread`` to finish.  A debug message is logged for
        any thread that does not exit within the timeout.  Every attribute
        access is ``getattr``-guarded so this is safe to call on a partially
        constructed instance.

        Parameters
        ----------
        exiting : bool, optional
            Whether this is being called from best-effort, garbage-collection
            driven teardown (:meth:`__del__`). If ``True``, suppresses the
            debug log emitted when a thread does not exit in time, since
            logging is unreliable during interpreter shutdown. The default is
            ``False``.

        Returns
        -------
        None
        """
        for attr in ("_stdout_thread", "_stderr_thread", "_startup_stdout_thread"):
            t = getattr(self, attr, None)
            if t is not None and t.is_alive():
                t.join(timeout=2)
                if t.is_alive() and not exiting:
                    self._log.debug(f"Thread {attr} did not exit in time")

    def _kill_process(self) -> None:
        """Kill the process stored in ``self._mapdl_process``.

        Acquires ``_process_close_lock`` to prevent concurrent teardowns,
        then delegates to :meth:`_terminate_process` (SIGTERM → pipe-close →
        wait → SIGKILL).

        Returns
        -------
        None

        Notes
        -----
        Does **not** join the pipe-drainer threads here because MAPDL may have
        spawned child processes that also hold the write ends of stdout/stderr
        open.  Those children are killed by :meth:`_kill_child_processes`,
        which must run first.  Call :meth:`_join_pipe_drainer_threads` only
        after all child processes are gone (see :meth:`_close_process`).
        """
        with self._process_close_lock:
            if self._mapdl_process is not None:
                self._log.debug("Killing process using subprocess.Popen.terminate")
                self._terminate_process(self._mapdl_process)

    def _kill_child_processes(self, timeout=2):
        pids = self._pids.copy()
        pids.reverse()  # First pid is the parent, therefore start by the children (end)

        for pid in pids:
            self._kill_child_process(pid, timeout=timeout)

    def _kill_child_process(self, pid, timeout=2):
        """Kill an individual child process, given a pid."""
        try:
            self._log.debug(f"Killing MAPDL process: {pid}")
            t0 = time.time()
            while time.time() < t0 + timeout:
                if psutil.pid_exists(pid):
                    os.kill(pid, 9)
                    time.sleep(0.5)
                else:
                    self._log.debug(f"Process {pid} killed properly.")
                    break
            else:
                self._log.debug(
                    f"Process {pid} couldn't be killed in {timeout} seconds"
                )

        except OSError:
            self._log.debug(
                f"Failed attempt to kill process: The process with pid {pid} does not exist. Maybe it was already killed?"
            )

        finally:
            if not psutil.pid_exists(pid):
                self._pids.remove(pid)

    def _close_process(self, timeout=2):  # pragma: no cover
        """Close all MAPDL processes.

        Notes
        -----
        This is effectively the only way to completely close down MAPDL locally on
        linux. Just killing the server with ``_exit_mapdl_server`` leaves orphaned
        processes making this method ineffective for a local instance of MAPDL.
        """
        self._log.debug("Closing processes")
        if self._local:
            # Kill child processes *before* the main process. Child/grandchild
            # processes (for example, MAPDL's distributed/MPI workers) can
            # inherit the stdout/stderr PIPE write ends. If they are still
            # alive when '_kill_process' closes those PIPEs, the
            # PIPE-drainer threads blocked in 'readline()' never see EOF, and
            # 'stream.close()' deadlocks waiting on the same internal lock
            # the reader thread holds. Killing every descendant first
            # guarantees no process still holds the write end open, so
            # closing the PIPEs cannot hang.
            self._kill_child_processes(timeout=timeout)

            # killing main process (subprocess)
            self._kill_process()

        if self.is_alive:
            raise MapdlRuntimeError("MAPDL could not be exited.")
        else:
            self._log.debug("All MAPDL processes exited")

    def _cache_pids(self):
        """Store the process IDs used when launching MAPDL.

        These PIDs are stored in a "cleanup<GUID>.sh/bat" file and are the PIDs
        of the MAPDL process. Killing these kills all dependent MAPDL
        processes.
        """
        self._log.debug("Caching PIDs")
        self._pids = []

        for filename in self.list_files():
            if "cleanup" in filename:  # Linux does not seem to generate this file?
                script = self.directory / filename
                with open(script) as f:
                    raw = f.read()

                if os.name == "nt":
                    pids = re.findall(r"/pid (\d+)", raw)
                else:
                    pids = set(re.findall(r"-9 (\d+)", raw))
                self._pids = [int(pid) for pid in pids]

        if not self._pids and not self._mapdl_process:
            self._log.debug(
                f"MAPDL process is not provided. PIDs could not be retrieved."
            )
            return
        elif not self._pids:
            # For the cases where the cleanup file is not generated,
            # we relay on the process.
            parent_pid = self._mapdl_process.pid
            try:
                parent = psutil.Process(parent_pid)
            except psutil.NoSuchProcess:
                self._log.debug(f"Parent process does not exist.")
                return

            children = parent.children(recursive=True)

            self._pids = [parent_pid] + [each.pid for each in children]

        self._log.debug(f"Recaching PIDs: {self._pids}")

    def _remove_lock_file(
        self,
        mapdl_path: Optional[str] = None,
        jobname: Optional[str] = None,
        use_cached: bool = False,
    ):
        """Removes the lock file.

        Necessary to call this as a segfault of MAPDL or exit(0) will
        not remove the lock file.
        """
        if jobname is None and use_cached:
            jobname = self._jobname
        elif jobname is None:
            jobname = self.jobname

        self._log.debug("Removing lock file after exit.")
        if mapdl_path is None:  # pragma: no cover
            mapdl_path = self.directory
        if mapdl_path:
            for lockname in [jobname + ".lock", "file.lock"]:
                lock_file = os.path.join(mapdl_path, lockname)
                if os.path.isfile(lock_file):
                    try:
                        os.remove(lock_file)
                    except OSError:
                        pass
