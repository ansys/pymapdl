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
    """MAPDL launch communication modes.

    Enumeration of supported MAPDL launch and communication modes.

    Attributes
    ----------
    GRPC : str
        Use gRPC protocol for communication (recommended, requires MAPDL 2021R1+)
    CONSOLE : str
        Use legacy console interface (older MAPDL versions, Linux only)
    """

    GRPC = "grpc"
    CONSOLE = "console"


class TransportMode(Enum):
    """GRPC transport communication modes.

    Enumeration of transport mechanisms for gRPC communication with MAPDL.

    Attributes
    ----------
    INSECURE : str
        Unencrypted TCP connection (for testing only)
    UDS : str
        Unix domain socket (Linux only, higher performance on local systems)
    WNUA : str
        Windows named pipe or Unix socket abstraction
    MTLS : str
        Encrypted connection using mutual TLS certificates
    """

    INSECURE = "insecure"
    UDS = "uds"
    WNUA = "wnua"
    MTLS = "mtls"


@dataclass(frozen=True)
class LaunchConfig:
    """Complete configuration for launching MAPDL instance.

    All fields are resolved from arguments, environment variables, and defaults.
    This immutable snapshot captures the complete launch intent and is used
    to drive all downstream launch and connection operations.

    Parameters
    ----------
    exec_file : str
        Full path to MAPDL executable
    run_location : str
        Working directory for MAPDL process
    jobname : str
        MAPDL job name (used for result files, etc.)
    nproc : int
        Number of parallel processors to allocate
    port : int
        gRPC server port number
    ip : str
        IP address to bind/connect to (127.0.0.1 for local, IP for remote)
    mode : LaunchMode
        Launch communication mode (GRPC or CONSOLE)
    version : Optional[int]
        MAPDL version number (e.g., 222 for 2022R2)
    start_instance : bool
        Whether to start new instance (True) or connect to existing (False)
    ram : Optional[int]
        RAM allocation in MB
    timeout : int
        Timeout for launch operations in seconds
    cleanup_on_exit : bool
        Whether to clean up MAPDL files on exit
    clear_on_connect : bool
        Whether to clear MAPDL database on connection
    override : bool
        Whether to override existing instance on same port
    remove_temp_dir_on_exit : bool
        Whether to remove temporary directory on exit
    set_no_abort : bool
        Whether to set MAPDL NO_ABORT flag
    additional_switches : str
        Additional MAPDL command line switches
    license_type : Optional[str]
        License type to use (e.g., 'research', 'academic')
    launch_on_hpc : bool
        Whether to launch on HPC cluster via SLURM
    running_on_hpc : bool
        Whether currently running within HPC environment
    scheduler_options : Optional[Dict[str, Any]]
        HPC scheduler options (e.g., nodes, cpus-per-task)
    loglevel : str
        Logging level (e.g., 'DEBUG', 'INFO', 'WARNING')
    log_apdl : Optional[str]
        Path to APDL command log file
    print_com : bool
        Whether to print APDL commands to console
    mapdl_output : Optional[str]
        Path to redirect MAPDL stdout/stderr
    transport_mode : Optional[TransportMode]
        gRPC transport mechanism (INSECURE, UDS, WNUA, MTLS)
    uds_dir : Optional[str]
        Unix domain socket directory path
    uds_id : Optional[str]
        Unix domain socket identifier
    certs_dir : Optional[str]
        Directory containing mTLS certificates
    env_vars : Dict[str, str]
        Environment variables for MAPDL process
    license_server_check : bool, default: False
        Whether to check license server availability
    force_intel : bool, default: False
        Force use of Intel MPI
    graphics_backend : Optional[str]
        Graphics backend to use

    Examples
    --------
    Create basic local launch configuration:

    >>> from ansys.mapdl.core.launcher.models import LaunchConfig, LaunchMode
    >>> config = LaunchConfig(
    ...     exec_file="/usr/ansys/bin/mapdl",
    ...     run_location="/tmp/mapdl_run",
    ...     jobname="myjob",
    ...     nproc=4,
    ...     port=50052,
    ...     ip="127.0.0.1",
    ...     mode=LaunchMode.GRPC,
    ...     version=222,
    ...     start_instance=True,
    ...     timeout=30
    ... )

    Create HPC launch configuration:

    >>> config = LaunchConfig(
    ...     exec_file="/usr/ansys/bin/mapdl",
    ...     run_location="/scratch/mapdl_run",
    ...     jobname="myjob",
    ...     nproc=16,
    ...     port=50052,
    ...     ip="",
    ...     mode=LaunchMode.GRPC,
    ...     start_instance=True,
    ...     launch_on_hpc=True,
    ...     scheduler_options={"nodes": "1", "cpus-per-task": "16"},
    ...     timeout=300
    ... )

    Notes
    -----
    - This is an immutable dataclass for thread-safety
    - All paths should be absolute for clarity
    - Validation should be performed before creating MAPDL instance
    - Different fields apply depending on mode and launch location
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
    """Information about a launched or running MAPDL process.

    Represents connection details and process handle for an active MAPDL
    instance, whether launched locally or on a remote/HPC system.

    Parameters
    ----------
    process : Optional[subprocess.Popen[bytes]]
        Subprocess handle for local process, None for remote/HPC instances
    port : int
        gRPC server port number that MAPDL is listening on
    ip : str
        IP address where MAPDL is bound/accessible
    pid : Optional[int], default: None
        Operating system process ID (None for remote/HPC)
    jobid : Optional[int], default: None
        HPC job ID from scheduler (None for local instances)
    hostname : Optional[str], default: None
        Hostname where process is running (useful for HPC)

    Examples
    --------
    Create ProcessInfo for local instance:

    >>> import subprocess
    >>> from ansys.mapdl.core.launcher.models import ProcessInfo
    >>> process = subprocess.Popen(["/usr/ansys/bin/mapdl", ...])
    >>> info = ProcessInfo(
    ...     process=process,
    ...     port=50052,
    ...     ip="127.0.0.1",
    ...     pid=process.pid
    ... )

    Create ProcessInfo for HPC instance:

    >>> info = ProcessInfo(
    ...     process=None,
    ...     port=50052,
    ...     ip="192.168.1.100",
    ...     jobid=12345,
    ...     hostname="compute-node-05"
    ... )

    Notes
    -----
    - For remote instances, process is None
    - For HPC instances, pid is None but jobid is set
    - Use pid/process for local instance control (signals, termination)
    - Use jobid with scheduler commands for HPC instances
    """

    process: Optional[subprocess.Popen[bytes]]
    port: int
    ip: str
    pid: Optional[int] = None
    jobid: Optional[int] = None
    hostname: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of configuration validation with errors and warnings.

    Collected during validation, provides comprehensive feedback on
    configuration validity without raising exceptions.

    Parameters
    ----------
    valid : bool
        Whether configuration passed all validation checks
    errors : List[str], default_factory: list
        Fatal errors that prevent launch
    warnings : List[str], default_factory: list
        Non-fatal warnings that allow launch to proceed

    Methods
    -------
    add_error(message : str) -> None
        Add error message and mark configuration as invalid
    add_warning(message : str) -> None
        Add warning message (doesn't affect valid flag)

    Examples
    --------
    Create and populate validation result:

    >>> from ansys.mapdl.core.launcher.models import ValidationResult
    >>> result = ValidationResult(valid=True)
    >>> if not os.path.exists(exec_file):
    ...     result.add_error(f"Executable not found: {exec_file}")
    >>> if config.nproc > available_cpus:
    ...     result.add_warning(f"Requesting {config.nproc} CPUs but only {available_cpus} available")
    >>> if result.valid:
    ...     launch_mapdl(config)
    ... else:
    ...     print(f"Cannot launch: {result.errors}")

    Check validation results:

    >>> result = validate_config(config)
    >>> for error in result.errors:
    ...     print(f"ERROR: {error}")
    >>> for warning in result.warnings:
    ...     print(f"WARNING: {warning}")

    Notes
    -----
    - All validation checks are accumulated in a single result
    - Errors prevent launch, warnings allow launch
    - Multiple errors/warnings can be present
    """

    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error message and mark configuration as invalid.

        Parameters
        ----------
        message : str
            Error message describing why configuration is invalid

        Returns
        -------
        None

        Examples
        --------
        Add error to validation result:

        >>> result = ValidationResult(valid=True)
        >>> result.add_error("Invalid port number: must be between 1024 and 65535")
        >>> result.valid
        False
        >>> result.errors
        ['Invalid port number: must be between 1024 and 65535']
        """
        self.valid = False
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        """Add a warning message without affecting valid flag.

        Parameters
        ----------
        message : str
            Warning message describing non-fatal issue with configuration

        Returns
        -------
        None

        Examples
        --------
        Add warning to validation result:

        >>> result = ValidationResult(valid=True)
        >>> result.add_warning("Requested 16 CPUs but only 8 available")
        >>> result.valid
        True
        >>> result.warnings
        ['Requested 16 CPUs but only 8 available']
        """
        self.warnings.append(message)


@dataclass(frozen=True)
class PortStatus:
    """Status of a network port for MAPDL connection.

    Represents the current state of a specific port including whether it's
    available for binding and if it's used by a MAPDL process.

    Parameters
    ----------
    port : int
        Port number being checked
    available : bool
        Whether port is available for binding (not in use)
    used_by_mapdl : bool
        Whether port is currently used by a MAPDL process
    process : Optional[Any], default: None
        psutil.Process object if port is in use, None otherwise

    Examples
    --------
    Check port status:

    >>> from ansys.mapdl.core.launcher.network import check_port_status
    >>> status = check_port_status(50052)
    >>> if status.available:
    ...     print("Port is free, safe to use")
    ... elif status.used_by_mapdl:
    ...     print("Port is used by MAPDL, consider stopping it")
    ... else:
    ...     print(f"Port is used by {status.process.name()}")

    Notes
    -----
    - Frozen dataclass for immutability
    - available=False and used_by_mapdl=True means MAPDL owns port
    - available=False and used_by_mapdl=False means other process owns port
    - Process information may have limited detail due to permissions
    """

    port: int
    available: bool
    used_by_mapdl: bool
    process: Optional[Any] = None  # psutil.Process


@dataclass(frozen=True)
class HPCJobInfo:
    """Information about an HPC job running MAPDL.

    Represents the current state and location of a MAPDL instance
    running on an HPC cluster through SLURM scheduler.

    Parameters
    ----------
    jobid : int
        Unique job ID assigned by SLURM scheduler
    state : str
        Current job state (e.g., 'PENDING', 'RUNNING', 'COMPLETED')
    hostname : str
        Batch host name where job is allocated
    ip : str
        IP address of batch host for connection

    Examples
    --------
    Create HPC job info:

    >>> from ansys.mapdl.core.launcher.models import HPCJobInfo
    >>> job = HPCJobInfo(
    ...     jobid=12345,
    ...     state="RUNNING",
    ...     hostname="compute-node-05",
    ...     ip="192.168.1.105"
    ... )

    Use for connection:

    >>> from ansys.mapdl.core.launcher.connection import create_grpc_client
    >>> from ansys.mapdl.core.launcher.models import LaunchConfig, ProcessInfo
    >>> config = LaunchConfig(ip=job.ip, port=50052, ...)
    >>> process_info = ProcessInfo(
    ...     process=None,
    ...     port=50052,
    ...     ip=job.ip,
    ...     jobid=job.jobid,
    ...     hostname=job.hostname
    ... )
    >>> mapdl = create_grpc_client(config, process_info)

    Notes
    -----
    - Frozen dataclass for immutability
    - Job state comes from SLURM scontrol output
    - Hostname is resolved to IP via socket.gethostbyname()
    """

    jobid: int
    state: str
    hostname: str
    ip: str


@dataclass(frozen=True)
class EnvironmentConfig:
    """Environment variable configuration for MAPDL process.

    Specifies which environment variables to use when launching MAPDL
    process and whether to replace or extend the current environment.

    Parameters
    ----------
    variables : Dict[str, str]
        Environment variables as key-value pairs
    replace_all : bool, default: False
        Whether to replace all system environment variables (True) or
        extend system environment with these variables (False)

    Examples
    --------
    Extend system environment:

    >>> from ansys.mapdl.core.launcher.models import EnvironmentConfig
    >>> env = EnvironmentConfig(
    ...     variables={"ANS_CMD": "NODIAG", "I_MPI_SHM_LMT": "shm"},
    ...     replace_all=False
    ... )

    Replace entire environment:

    >>> env = EnvironmentConfig(
    ...     variables={"PATH": "/usr/bin:/bin", "ANS_CMD": "NODIAG"},
    ...     replace_all=True
    ... )

    Notes
    -----
    - Frozen dataclass for immutability
    - Set replace_all=False for extending system environment (safer)
    - Set replace_all=True when user explicitly provides env_vars
    - MAPDL-specific variables like ANS_CMD are typically needed
    """

    variables: Dict[str, str]
    replace_all: bool = False
