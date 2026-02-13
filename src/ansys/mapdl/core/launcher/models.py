# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Data models for MAPDL launcher.

This module defines all data structures used throughout the launcher.
All models are immutable (where practical) to ensure predictability and thread safety.
"""

from dataclasses import dataclass, field
from enum import Enum
import subprocess  # nosec B404
from typing import Any, Dict, List, Optional


class LaunchMode(Enum):
    """MAPDL launch modes."""

    GRPC = "grpc"
    CONSOLE = "console"


class TransportMode(Enum):
    """GRPC transport modes."""

    INSECURE = "insecure"
    UDS = "uds"
    WNUA = "wnua"
    MTLS = "mtls"


@dataclass(frozen=True)
class LaunchConfig:
    """Complete configuration for launching MAPDL.

    All fields are resolved from arguments, environment variables,
    and defaults. This is an immutable snapshot of the launch intent.

    Attributes:
        exec_file: Path to MAPDL executable
        run_location: Working directory for MAPDL
        jobname: MAPDL job name
        nproc: Number of processors
        port: gRPC server port
        ip: IP address to bind/connect
        mode: Launch mode (grpc or console)
        version: MAPDL version (e.g., 222 for 2022R2)
        start_instance: Whether to start new instance or connect to existing
        ram: RAM allocation in MB
        timeout: Timeout for launch in seconds
        cleanup_on_exit: Whether to clean up on exit
        clear_on_connect: Whether to clear on connection
        override: Whether to override existing instance
        remove_temp_dir_on_exit: Whether to remove temp directory on exit
        set_no_abort: Whether to set NO_ABORT flag
        additional_switches: Additional command line switches
        license_type: License type to use
        launch_on_hpc: Whether launching on HPC cluster
        running_on_hpc: Whether currently running on HPC
        scheduler_options: HPC scheduler options
        loglevel: Logging level
        log_apdl: Path to APDL log file
        print_com: Whether to print commands
        mapdl_output: Path to redirect MAPDL output
        transport_mode: gRPC transport mode
        uds_dir: Unix domain socket directory
        uds_id: Unix domain socket ID
        certs_dir: Directory containing certificates for mTLS
        env_vars: Environment variables for MAPDL process
        license_server_check: Whether to check license server
        force_intel: Force Intel MPI
        graphics_backend: Graphics backend to use
    """

    # Core parameters
    exec_file: str
    run_location: str
    jobname: str
    nproc: int
    port: int
    ip: str
    mode: LaunchMode
    version: Optional[int]
    start_instance: bool

    # Resource parameters
    ram: Optional[int]
    timeout: int

    # Behavior flags
    cleanup_on_exit: bool
    clear_on_connect: bool
    override: bool
    remove_temp_dir_on_exit: bool
    set_no_abort: bool

    # Switches and options
    additional_switches: str
    license_type: Optional[str]

    # HPC parameters
    launch_on_hpc: bool
    running_on_hpc: bool
    scheduler_options: Optional[Dict[str, Any]]

    # Logging and output
    loglevel: str
    log_apdl: Optional[str]
    print_com: bool
    mapdl_output: Optional[str]

    # Transport configuration
    transport_mode: Optional[TransportMode]
    uds_dir: Optional[str]
    uds_id: Optional[str]
    certs_dir: Optional[str]

    # Environment
    env_vars: Dict[str, str] = field(default_factory=dict)

    # Advanced/debug
    license_server_check: bool = False
    force_intel: bool = False
    graphics_backend: Optional[str] = None


@dataclass(frozen=True)
class ProcessInfo:
    """Information about a launched MAPDL process.

    Attributes:
        process: The subprocess handle (None for remote/HPC)
        port: Port number MAPDL is listening on
        ip: IP address MAPDL is bound to
        pid: Process ID (None for remote/HPC)
        jobid: HPC job ID (None for local)
        hostname: Hostname (for HPC)
    """

    process: Optional[subprocess.Popen[bytes]]
    port: int
    ip: str
    pid: Optional[int] = None
    jobid: Optional[int] = None
    hostname: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of configuration validation.

    Attributes:
        valid: Whether configuration is valid
        errors: List of error messages (prevent launch)
        warnings: List of warning messages (allow launch)
    """

    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error message and mark as invalid."""
        self.valid = False
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)


@dataclass(frozen=True)
class PortStatus:
    """Status of a network port.

    Attributes:
        port: Port number
        available: Whether port is available
        used_by_mapdl: Whether port is used by MAPDL process
        process: Process using the port (if any)
    """

    port: int
    available: bool
    used_by_mapdl: bool
    process: Optional[Any] = None  # psutil.Process


@dataclass(frozen=True)
class HPCJobInfo:
    """Information about an HPC job.

    Attributes:
        jobid: Job ID from scheduler
        state: Job state (PENDING, RUNNING, etc.)
        hostname: Batch host name
        ip: Batch host IP address
    """

    jobid: int
    state: str
    hostname: str
    ip: str


@dataclass(frozen=True)
class EnvironmentConfig:
    """Environment variable configuration for MAPDL process.

    Attributes:
        variables: Environment variables to set
        replace_all: Whether to replace all env vars vs extend
    """

    variables: Dict[str, str]
    replace_all: bool = False
