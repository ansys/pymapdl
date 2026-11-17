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

"""Exit and teardown ordering for a gRPC MAPDL session."""

import os
from pathlib import Path
import shutil

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
import subprocess  # nosec B404
import tempfile
from typing import Optional

from ansys.mapdl.core.errors import protect_from

from . import _GrpcMixinBase


class _GrpcLifecycleMixin(_GrpcMixinBase):
    """Exit and teardown ordering for a gRPC MAPDL session."""

    # Placing logging in the exit method raises exceptions when
    # this is triggered by "__del__"
    @protect_from(ValueError, "I/O operation on closed file.")
    @protect_from(AttributeError, "'MapdlGrpc' object has no attribute '_log'")
    def exit(self, save=False, force=False, **kwargs):
        """Exit MAPDL.

        Parameters
        ----------
        save : bool, optional
            Save the database on exit.  The default is ``False``.
        force : bool, optional
            Override any environment variables that may inhibit exiting MAPDL.

        Notes
        -----
        If Mapdl didn't start the instance, then MAPDL is kept alive unless
        ``force=True``.

        If ``PYMAPDL_START_INSTANCE`` is set to ``False`` (generally set in
        remote testing or documentation build), then MAPDL is kept alive.
        Override this behavior with ``force=True`` to always force
        exiting MAPDL regardless of your local environment.

        On every path where MAPDL itself is left running (the ones above,
        an instance that has already exited, or an instance built while
        ``pymapdl.BUILDING_GALLERY`` is set), the client side of the
        connection — the gRPC channel and the PIPE-drainer threads — is
        still released, because closing a gRPC channel is a purely
        client-side operation that does not stop the MAPDL server. Call
        :meth:`reconnect_to_mapdl` to build a fresh channel and resume
        driving the same MAPDL session.

        If ``Mapdl.finish_job_on_exit`` is set to ``True`` and there is a valid
        JobID in ``Mapdl.jobid``, then the SLURM job will be canceled.

        Examples
        --------
        >>> mapdl.exit()
        """
        from ansys.mapdl import core as pymapdl

        self._log.debug(
            f"Exiting MAPDL gRPC instance {self.ip}:{self.port} on '{self._path}'."
        )

        try:
            self._exiting = True

            if self.exited:
                self._log.debug("Already exited")
                # '_exited' is also set by the gRPC error handlers when MAPDL
                # crashes, with no cleanup performed. The helper is
                # idempotent, so calling it again on a regular repeated exit
                # costs nothing.
                self._disconnect_but_leave_mapdl_running()
                return

            cleanup_error = None
            try:
                self._cleanup_lazy_array_parameters()
            except Exception as error:
                # Continue tearing down the connection, then report the
                # cleanup failure to the caller.
                cleanup_error = error

            if save:
                self._log.debug("Saving MAPDL database")
                self.save()

            if not force:
                # Ignore this method if PYMAPDL_START_INSTANCE=False
                if not self._start_instance or not self._launched:
                    self._log.info(
                        "Ignoring exit due to PYMAPDL_START_INSTANCE=False or because PyMAPDL didn't launch the instance."
                    )
                    self._disconnect_but_leave_mapdl_running()
                    if cleanup_error is not None:
                        raise cleanup_error
                    return

                # or building the gallery
                if pymapdl.BUILDING_GALLERY:
                    self._log.info("Ignoring exit due as BUILDING_GALLERY=True")
                    self._disconnect_but_leave_mapdl_running()
                    if cleanup_error is not None:
                        raise cleanup_error
                    return

            # Step 3 of '_release_resources' closes the gRPC channel.
            self._release_resources(path=self._path)
            if cleanup_error is not None:
                raise cleanup_error

        finally:
            self._exiting = False

    def _disconnect_but_leave_mapdl_running(self, exiting: bool = False) -> None:
        """Close the client side of the connection, leaving MAPDL running.

        Closing a gRPC channel is a purely client-side operation: it cancels
        pending RPCs and releases the socket, but it does not stop the MAPDL
        server. This is what :meth:`exit` performs on the paths where MAPDL
        itself must survive, so that the ``_poll_connectivity`` daemon thread
        and the PIPE-drainer threads do not outlive this object.

        The instance is marked as exited because the channel is gone. Use
        :meth:`reconnect_to_mapdl` to build a fresh channel and resume driving
        the same MAPDL session.

        Parameters
        ----------
        exiting : bool, optional
            Whether this is being called from best-effort, garbage-collection
            driven teardown (:meth:`__del__`) rather than the deterministic
            :meth:`exit` path. If ``True``, this suppresses this method's own
            debug logging, and is forwarded to :meth:`_close_grpc_channel` and
            :meth:`_join_pipe_drainer_threads` to suppress theirs, since
            logging is unreliable during interpreter shutdown. The default is
            ``False``.

        Returns
        -------
        None

        Examples
        --------
        >>> mapdl.exit()          # PYMAPDL_START_INSTANCE=False
        >>> mapdl.exited
        True
        >>> mapdl.reconnect_to_mapdl()
        >>> mapdl.exited
        False
        """
        try:
            self._close_grpc_channel(exiting=exiting)
        except Exception as e:
            if not exiting:
                self._log.debug("Error closing gRPC channel: %s", e)

        try:
            self._join_pipe_drainer_threads(exiting=exiting)
        except Exception as e:
            if not exiting:
                self._log.debug("Error joining pipe-drainer threads: %s", e)

        self._exited = True

    def _exit_mapdl(self, path: Optional[str] = None) -> None:
        """Exit MAPDL and remove the lock file in `path`"""
        # This cannot/should not be faked
        if self._local:
            self._cache_pids()  # Recache processes

            self._exit_mapdl_server()

            self._close_process()

            self._remove_lock_file(path, use_cached=True)
        else:
            self._exit_mapdl_server()

    def _release_resources(
        self, path: Optional[str] = None, cleanup_loggers: bool = True
    ) -> None:
        """Release all resources held by this MAPDL instance.

        This is the single, idempotent cleanup entry-point used by both
        :meth:`exit` and :meth:`__del__`.  Calling it more than once is safe —
        subsequent calls return immediately because ``_exited`` is ``True``.

        Steps performed (in order):

        1. Kill the MAPDL server process and remove the lock file.
        2. Join the stdout, stderr, and startup PIPE-drainer threads.
        3. Close the gRPC channel.
        4. Remove the UDS socket file (Unix Domain Socket transport only).
        5. Remove the port from the global ``_LOCAL_PORTS`` registry.
        6. Cancel the SLURM/HPC job (if applicable).
        7. Delete the remote PyMAPDL server instance (if applicable).
        8. Mark the instance as exited (``_exited = True``).
        9. Remove the temporary working directory (if ``remove_temp_dir_on_exit``).
        10. Clean up logger handlers (only when ``cleanup_loggers`` is ``True``).

        Parameters
        ----------
        path : str, optional
            Working directory to remove the lock file from and to delete when
            ``remove_temp_dir_on_exit`` is ``True``. The default is ``None``,
            in which case ``self._path`` is used.
        cleanup_loggers : bool, optional
            Whether to tear down this instance's logger handlers (step 10).
            The default is ``True``, which is what :meth:`exit` uses since it
            runs at a deterministic point chosen by the caller.

            ``__del__`` passes ``False``: the ``pymapdl_global`` logger and
            its handlers are shared, process-wide state (see
            :class:`ansys.mapdl.core.logging.Logger`), and closing a handler
            from garbage-collection-driven code can race with another,
            still-alive ``Mapdl`` instance that logs through the same
            handler — surfacing as ``ValueError: I/O operation on closed
            file`` or ``AttributeError`` on ``self._log`` elsewhere. Shared,
            non-exclusively-owned resources like the logger are only ever
            released from the explicit, deterministic :meth:`exit` path.

        Returns
        -------
        None

        Notes
        -----
        Steps 1 to 7 run while ``_exited`` is still ``False`` so that they can
        reach the server and emit log records. Step 8 flips the flag *before*
        the temporary directory is removed, because
        :meth:`_remove_temp_dir_on_exit` falls back to the ``directory``
        property, which would otherwise issue an ``/INQUIRE`` command against
        an already dead server. Logger handlers are torn down last, so every
        preceding step can still log.

        Each step is individually wrapped in ``try/except`` so that a failure
        in one step does not prevent the remaining resources from being freed.
        This also makes the method safe to call during interpreter shutdown,
        where module globals may already have been torn down.
        Local garbage-collection teardown uses cached process information rather
        than querying or commanding MAPDL, because GC can interrupt a gRPC call.

        Callers must set ``_exiting = True`` before invoking this method (and
        reset it once done), so that :attr:`is_alive` short-circuits instead
        of issuing a live gRPC call against a server that step 1 may have
        just killed. Both :meth:`exit` and :meth:`__del__` do this.

        Examples
        --------
        This method is called internally by :meth:`exit`, so it is rarely
        invoked directly.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl._release_resources()
        >>> mapdl.exited
        True
        """
        if self._exited:
            return

        path = path or getattr(self, "_path", None)

        # ``cleanup_loggers`` is False only when called from ``__del__``, so
        # it doubles here as a proxy for "this is best-effort, GC-driven
        # teardown, where logging may be unreliable" (see the ``exiting``
        # parameters of ``_join_pipe_drainer_threads`` and
        # ``_close_grpc_channel``).
        exiting = not cleanup_loggers

        # 1. Kill MAPDL process + remove lock file
        try:
            if exiting and self._local:
                # GC may interrupt gRPC itself; use cached process data, not RPCs.
                self._close_process()
                if path:
                    self._remove_lock_file(path, use_cached=True)
            else:
                self._exit_mapdl(path)
        except Exception as e:
            if not exiting:
                self._log.debug("Error during _exit_mapdl: %s", e)

        # 2. Ensure PIPE-drainer threads (stdout/stderr/startup) are joined so
        # that background reader threads do not leak after teardown.
        try:
            self._join_pipe_drainer_threads(exiting=exiting)
        except Exception as e:
            if not exiting:
                self._log.debug("Error joining pipe-drainer threads: %s", e)

        # 3. Close gRPC channel
        try:
            self._close_grpc_channel(exiting=exiting)
        except Exception as e:
            if not exiting:
                self._log.debug("Error closing gRPC channel: %s", e)

        # 4. Remove UDS socket file
        try:
            if getattr(self, "transport_mode", None) == "uds":
                socket_path = os.path.join(self.uds_dir, f"mapdl-{self.port}.sock")
                if os.path.exists(socket_path):
                    os.remove(socket_path)
                    self._log.debug("Removed UDS socket file %s", socket_path)
        except Exception as e:
            self._log.debug("Error removing UDS socket: %s", e)

        # 5. Deregister port from global registry
        try:
            from ansys.mapdl import core as pymapdl

            if self._local and self._port in pymapdl._LOCAL_PORTS:
                pymapdl._LOCAL_PORTS.remove(self._port)
        except Exception as e:
            self._log.debug("Error removing port from _LOCAL_PORTS: %s", e)

        # 6. Cancel HPC job
        try:
            if self._mapdl_on_hpc and self.finish_job_on_exit:
                self.kill_job(self.jobid)
                self._log.debug("HPC job %s cancelled", self.jobid)
        except Exception as e:
            self._log.debug("Error cancelling HPC job: %s", e)

        # 7. Delete remote PyMAPDL server instance
        try:
            if self._remote_instance:  # pragma: no cover
                self._remote_instance.delete()
        except Exception as e:
            self._log.debug("Error deleting remote instance: %s", e)

        # 8. Mark exited — before the temp dir removal, so that the 'directory'
        # fallback in '_remove_temp_dir_on_exit' cannot query the dead server
        self._exited = True

        # 9. Remove temporary working directory
        try:
            self._remove_temp_dir_on_exit(path)
        except Exception as e:
            self._log.debug("Error removing temp dir: %s", e)

        # 10. Clean up logger handlers.
        # Skipped when called from ``__del__`` (``cleanup_loggers=False``):
        # the logger and its handlers are shared, process-wide state, and
        # tearing them down from non-deterministic, GC-driven code can race
        # with another still-alive ``Mapdl`` instance logging through the
        # same handler. See the ``cleanup_loggers`` parameter documentation.
        if cleanup_loggers:
            try:
                self._cleanup_loggers()
            except Exception as e:
                self._log.debug("Error during logger cleanup: %s", e)

    def _close_grpc_channel(self, exiting: bool = False) -> None:
        """Unsubscribe from and close the gRPC channel.

        Removes the connectivity callback registered by
        :meth:`_subscribe_to_channel` and closes the channel, which is what
        terminates the gRPC ``_poll_connectivity`` daemon thread.  That thread
        only exits once the channel has no subscribers left, so failing to do
        this leaks one daemon thread per instance.

        Safe to call multiple times; subsequent calls are no-ops.  It is also
        safe to call on an instance that is already marked as exited, which is
        precisely the case that used to leak, because ``exit()`` returns early
        for such instances.

        Parameters
        ----------
        exiting : bool, optional
            Whether this is being called during the exit process. If True, it
            will suppress logging of errors during channel closure. Default is False.
        """
        channel = getattr(self, "_channel", None)
        callback = getattr(self, "_connectivity_callback", None)

        self._channel = None
        self._connectivity_callback = None

        if channel is None:
            return

        if callback is not None:
            try:
                channel.unsubscribe(callback)
            except Exception as e:
                if not exiting:
                    self._log.debug(f"Error unsubscribing from gRPC channel: {e}")

        try:
            channel.close()
            if not exiting:
                self._log.debug("gRPC channel closed")
        except Exception as e:
            if not exiting:
                self._log.debug(f"Error closing gRPC channel: {e}")

    def _remove_temp_dir_on_exit(self, path=None):
        """Removes the temporary directory created by the launcher.

        This only runs if the current working directory of MAPDL is within the
        user temporary directory.
        """
        if self.remove_temp_dir_on_exit and self._local:
            path = str(Path(path or self.directory))
            tmp_dir = tempfile.gettempdir()
            ans_temp_dir = str(Path(os.path.join(tmp_dir, "ansys_")))

            if path.startswith(ans_temp_dir):
                self._log.debug("Removing the MAPDL temporary directory %s", path)
                shutil.rmtree(path, ignore_errors=True)
            else:
                self._log.debug(
                    "MAPDL working directory is not in the temporary directory '%s'"
                    ", not removing the MAPDL working directory.",
                    tmp_dir,
                )

    def _exit_mapdl_server(self):
        """Call exit(0) on the server.

        Notes
        -----
        This only shuts down the mapdl server process and leaves the other
        processes orphaned. This is useful for killing a remote process but not
        a local process.
        """
        if self._exited:
            return

        # MAPDL ignores EXIT unless it is at the Begin level.
        self.finish()
        self._ctrl("EXIT")

    def kill_job(self, jobid: int) -> None:
        """Kill an HPC job

        Kill a job given its identifier.

        Parameters
        ----------
        jobid : int
            Job ID.
        """
        cmd = ["scancel", f"{jobid}"]
        # to ensure the job is stopped properly, let's issue the scancel twice.
        subprocess.Popen(cmd)  # nosec B603

    def __del__(self):
        """Release resources when the object is garbage-collected.

        Notes
        -----
        The garbage collector may begin tearing down module globals before this
        method runs, so every attribute access is guarded with ``getattr`` and
        wrapped in ``try/except``.  The full teardown is delegated to
        :meth:`_release_resources`, which is itself idempotent.

        When the instance is already exited, was launched with
        ``cleanup_on_exit=False``, did not launch MAPDL itself
        (``_start_instance=False``), or was never actually launched, the full
        teardown in :meth:`_release_resources` is skipped (it would either be
        a no-op or kill a server this instance does not own). Even then,
        :meth:`_disconnect_but_leave_mapdl_running` still closes the gRPC
        channel, joins the PIPE-drainer threads, and marks the instance as
        exited, because those are purely client-side resources (the
        ``_poll_connectivity`` daemon thread and the stdout/stderr/startup
        reader threads) that outlive this object otherwise.
        """
        # Check early exit conditions.
        if (
            getattr(self, "_exited", False)
            or not getattr(self, "_cleanup", True)
            or not getattr(self, "_start_instance", True)
            or not getattr(self, "_launched", False)
        ):
            try:
                self._exiting = True
                self._disconnect_but_leave_mapdl_running(exiting=True)
            except (
                Exception
            ):  # nosec B110 - best-effort cleanup during GC; logging is unreliable here
                pass
            finally:
                self._exited = True
                self._exiting = False
                return

        try:
            self._exiting = True
            self._release_resources(getattr(self, "_path", None), cleanup_loggers=False)
        except (
            Exception
        ):  # nosec B110 - best-effort cleanup during GC; logging is unreliable here
            pass
        finally:
            self._exiting = False
