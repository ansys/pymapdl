# Symbols missing from the API reference

This inventory compares the public top-level functions and classes defined
under `src/ansys/mapdl/core/` with the pages linked from
`https://mapdl.docs.pyansys.com/version/stable/api/index.html`. Names beginning
with an underscore and the generated modules under `_commands/` are excluded.
The generated command modules have their own reference under
`mapdl_commands/`.

## Implemented in the API source

The following high-confidence gaps from this audit are now linked from the
repository API source:

- CLI reference page in `doc/source/api/index.rst`
- `ComponentManager.default_entity`
- `ComponentManager.default_entity_warning`
- `ComponentManager.logger`
- `ComponentManager.names`
- `ComponentManager.types`
- `ComponentManager.items`
- `ComponentManager.select`
- `Mapdl.do` and `Mapdl.dowhile`
- launcher `stop` and `stop_mapdl`
- `LaunchMode`, `TransportMode`, `LaunchConfig`, `ProcessInfo`,
  `ValidationResult`, `PortStatus`, `HPCJobInfo`, and `EnvironmentConfig`
- `Information`, `UnitsDict`, and `get_mapdl_info`
- `Report`
- `check_has_mapdl`

The following symbols are defined in the repository but are not linked from
the API reference pages.

## Stable-site gaps

These symbols are linked from the repository API source but are still absent
from the published stable HTML site.

| Module | Symbol | Purpose |
| --- | --- | --- |
| `cli.start` | `start` | Launches MAPDL and prints connection information. |
| `launcher.connection` | `stop` | Stops MAPDL instances. |
| `cli.list_instances` | `list_instances` | Lists MAPDL processes on the machine. |
| `cli.check` | `check` | Prints MAPDL diagnostic information. |
| `cli.exec` | `exec_commands` | Executes MAPDL commands on a running instance. |
| `cli.convert` | `convert` | Converts MAPDL code to PyMAPDL. |
| `cli.help` | `help_command` | Prints the Python docstring for a MAPDL command. |
| `cli.skills` | `list_skills` | Lists bundled PyMAPDL skills. |
| `cli.skills` | `show_skill` | Displays a bundled skill. |
| `cli.skills` | `plan_skill_install` | Plans installation of a bundled skill. |
| `cli.skills` | `apply_skill_install` | Applies a skill installation plan. |
| `cli.skills` | `install_skill` | Installs a bundled skill. |
| `Mapdl` | `do` | Executes a MAPDL `*DO` loop. |
| `Mapdl` | `dowhile` | Executes a MAPDL `*DOWHILE` loop. |
| `launcher` | `stop_mapdl` | Top-level alias for stopping MAPDL. |
| `launcher.models` | `LaunchConfig` | Stores the complete MAPDL launch configuration. |
| `launcher.models` | `LaunchMode` | Enumerates MAPDL launch communication modes. |
| `launcher.models` | `TransportMode` | Enumerates gRPC transport modes. |
| `report` | `Report` | Builds a report for the PyMAPDL environment. |
| `information` | `get_mapdl_info` | Returns diagnostic information for a connected MAPDL instance. |
| `misc` | `check_has_mapdl` | Checks whether an Ansys MAPDL installation is available. |

The stable site has no `api/cli.html` page even though the repository has
`doc/source/api/cli.rst`. The requested `/api/.html` URL is also invalid; the
canonical landing page is `/api/` or `/api/index.html`.

## Core and connection modules

| Module | Symbol | Purpose |
| --- | --- | --- |
| `common_grpc` | `GrpcError` | Represents a gRPC failure. |
| `common_grpc` | `check_vget_input` | Validates the entity and item arguments used by `VGET`. |
| `common_grpc` | `parse_chunks` | Deserializes gRPC chunks into a NumPy array. |
| `errors` | `terminal_support_color` | Detects whether terminal color output is supported. |
| `errors` | `color_text` | Applies terminal color to text when supported. |
| `errors` | `MapdlException` | Base exception for general MAPDL errors. |
| `errors` | `MapdlValueError` | Reports an invalid MAPDL value. |
| `errors` | `MapdlFileNotFoundError` | Reports a missing MAPDL file. |
| `errors` | `MapdlRuntimeError` | Reports an error returned by MAPDL. |
| `errors` | `ANSYSDataTypeError` | Reports an invalid APDLMath data type. |
| `errors` | `VersionError` | Reports an incompatible MAPDL version. |
| `errors` | `NoDistributedFiles` | Reports that distributed result files cannot be found. |
| `errors` | `MapdlInvalidRoutineError` | Reports that MAPDL is in the wrong routine. |
| `errors` | `MapdlCommandIgnoredError` | Reports that MAPDL ignored a command. |
| `errors` | `MapdlDoLoopLimitError` | Reports excessive nested `*DO` or `*DOWHILE` loops. |
| `errors` | `MapdlExitedError` | Reports that the MAPDL process exited. |
| `errors` | `NotEnoughResources` | Reports that MAPDL does not have enough resources. |
| `errors` | `LockFileException` | Reports that a MAPDL lock file was not removed. |
| `errors` | `MapdlDidNotStart` | Reports that MAPDL failed to start. |
| `errors` | `PortAlreadyInUse` | Reports that a requested port is occupied. |
| `errors` | `PortAlreadyInUseByAnMAPDLInstance` | Reports that a port is occupied by MAPDL. |
| `errors` | `MapdlConnectionError` | Reports a failed MAPDL connection. |
| `errors` | `LicenseServerConnectionError` | Reports an unavailable license server. |
| `errors` | `NotAvailableLicenses` | Reports that required licenses are unavailable. |
| `errors` | `IncorrectWorkingDirectory` | Reports a nonexistent MAPDL working directory. |
| `errors` | `DifferentSessionConnectionError` | Reports a connection to a different MAPDL session. |
| `errors` | `DeprecationError` | Reports use of a deprecated command or interface. |
| `errors` | `MapdlError` | Base class for MAPDL errors. |
| `errors` | `MapdlWarning` | Represents a MAPDL warning message. |
| `errors` | `MapdlNote` | Represents a MAPDL note message. |
| `errors` | `MapdlInfo` | Represents a MAPDL informational message. |
| `errors` | `MapdlVersionError` | Reports an incompatible MAPDL version. |
| `errors` | `EmptyRecordError` | Reports an empty result record. |
| `errors` | `ComponentNoData` | Reports that a component has no data. |
| `errors` | `ComponentIsNotSelected` | Reports that a component is not selected. |
| `errors` | `ComponentDoesNotExits` | Reports that a component does not exist. |
| `errors` | `CommandDeprecated` | Reports use of a deprecated command. |
| `errors` | `MapdlgRPCError` | Reports a MAPDL gRPC problem. |
| `errors` | `IncorrectMPIConfigurationError` | Reports an invalid MPI configuration. |
| `errors` | `PluginError` | Reports a plugin failure. |
| `errors` | `PluginLoadError` | Reports a plugin loading failure. |
| `errors` | `PluginUnloadError` | Reports a plugin unloading failure. |
| `mapdl_console` | `launch_pexpect` | Launches MAPDL through the legacy `pexpect` console transport. |
| `mapdl_console` | `MapdlConsole` | Controls an interactive legacy MAPDL shell session. |
| `mapdl_inprocess` | `MapdlInProcess` | Connects to an in-process MAPDL backend. |
| `mapdl_grpc` | `get_start_instance` | Resolves whether a new MAPDL instance should be started. |
| `mapdl_grpc` | `chunk_raw` | Splits raw content into transferable chunks. |
| `mapdl_grpc` | `get_file_chunks` | Serializes a file into transfer chunks. |
| `mapdl_grpc` | `save_chunks_to_file` | Writes received chunks to a local file. |

## Launcher and licensing

| Module | Symbol | Purpose |
| --- | --- | --- |
| `launcher.config` | `resolve_launch_config` | Resolves a complete launch configuration. |
| `launcher.config` | `resolve_scheduler_options` | Validates HPC scheduler options. |
| `launcher.config` | `resolve_channel` | Resolves the optional gRPC channel. |
| `launcher.config` | `resolve_exec_file` | Resolves the MAPDL executable path. |
| `launcher.config` | `resolve_port` | Resolves the MAPDL port number. |
| `launcher.config` | `resolve_ip` | Resolves the MAPDL IP address. |
| `launcher.config` | `resolve_mode` | Resolves the launch mode. |
| `launcher.config` | `resolve_nproc` | Resolves the processor count. |
| `launcher.config` | `resolve_version` | Resolves the MAPDL version. |
| `launcher.config` | `resolve_run_location` | Resolves the MAPDL working directory. |
| `launcher.config` | `resolve_ram` | Resolves the requested RAM allocation. |
| `launcher.config` | `resolve_timeout` | Resolves the launch timeout. |
| `launcher.config` | `resolve_start_instance` | Resolves whether to start a new instance. |
| `launcher.config` | `resolve_transport_mode` | Resolves the gRPC transport mode. |
| `launcher.config` | `resolve_additional_switches` | Resolves extra MAPDL command-line switches. |
| `launcher.connection` | `create_grpc_client` | Creates and connects a `MapdlGrpc` client. |
| `launcher.connection` | `create_console_client` | Creates a legacy `MapdlConsole` client. |
| `launcher.connection` | `connect_to_existing` | Connects to an existing MAPDL instance. |
| `launcher.environment` | `is_wsl` | Detects Windows Subsystem for Linux. |
| `launcher.environment` | `is_ubuntu` | Detects Ubuntu Linux. |
| `launcher.environment` | `prepare_environment` | Prepares environment variables for MAPDL execution. |
| `launcher.environment` | `get_windows_host_ip` | Gets the Windows host IP from WSL. |
| `launcher.errors` | `ConfigurationError` | Reports invalid or conflicting launch options. |
| `launcher.errors` | `LaunchError` | Reports a MAPDL launch failure. |
| `launcher.hpc` | `launch_on_hpc` | Launches MAPDL through a SLURM HPC scheduler. |
| `launcher.hpc` | `detect_slurm_environment` | Detects whether execution is under SLURM. |
| `launcher.hpc` | `resolve_slurm_resources` | Resolves resources from the SLURM environment. |
| `launcher.models` | `LaunchMode` | Enumerates MAPDL launch communication modes. |
| `launcher.models` | `TransportMode` | Enumerates gRPC transport modes. |
| `launcher.models` | `LaunchConfig` | Stores the complete MAPDL launch configuration. |
| `launcher.models` | `ProcessInfo` | Stores information about a MAPDL process. |
| `launcher.models` | `ValidationResult` | Stores configuration validation errors and warnings. |
| `launcher.models` | `PortStatus` | Stores the status of a network port. |
| `launcher.models` | `HPCJobInfo` | Stores information about an HPC MAPDL job. |
| `launcher.models` | `EnvironmentConfig` | Stores MAPDL environment variable configuration. |
| `launcher.network` | `check_port_status` | Checks whether a network port is available. |
| `launcher.network` | `find_available_port` | Finds an available port from a starting port. |
| `launcher.network` | `get_process_at_port` | Finds the process listening on a port. |
| `launcher.network` | `get_ansys_process_from_port` | Finds the Ansys or MAPDL gRPC process on a port. |
| `launcher.network` | `can_access_process` | Checks process access permissions. |
| `launcher.network` | `is_valid_ansys_process_name` | Checks whether a process name identifies Ansys or MAPDL. |
| `launcher.network` | `is_alive_status` | Checks whether a process status indicates it is alive. |
| `launcher.process` | `check_process_is_alive` | Checks that a MAPDL subprocess is still running. |
| `launcher.process` | `wait_for_process_ready` | Waits for a MAPDL process to become ready. |
| `launcher.process` | `QueueWithStorage` | Provides a queue that permanently stores all items. |
| `launcher.validation` | `validate_config` | Validates a complete launch configuration. |
| `licensing` | `LicenseChecker` | Checks Ansys license availability. |
| `licensing` | `get_ansys_license_debug_file_tail` | Reads messages from the license debug file. |
| `licensing` | `get_ansys_license_directory` | Gets the Ansys license directory. |
| `licensing` | `get_ansys_license_debug_file_name` | Gets the license client log filename. |
| `licensing` | `get_ansys_license_debug_file_path` | Gets the license client `licdebug` path. |
| `licensing` | `get_ansys_license_utility_path` | Gets the Ansys licensing utility path. |

## Information, logging, results, and reporting

| Module | Symbol | Purpose |
| --- | --- | --- |
| `information` | `UnitsDict` | Stores unit information with case-insensitive access. |
| `information` | `get_mapdl_info` | Returns diagnostic information for a connected MAPDL instance. |
| `logging` | `PymapdlCustomAdapter` | Keeps the MAPDL instance name dynamic in log records. |
| `logging` | `PymapdlPercentStyle` | Provides the PyMAPDL percent-style logging formatter. |
| `logging` | `PymapdlFormatter` | Formats PyMAPDL log records. |
| `logging` | `InstanceFilter` | Ensures each log record has an instance name. |
| `logging` | `addfile_handler` | Adds a file handler to a logger. |
| `logging` | `add_stdout_handler` | Adds a standard-output handler to a logger. |
| `reader.core` | `ResultNotFound` | Reports that a requested result is unavailable. |
| `reader.core` | `NotImplementedInDPFBackend` | Reports an operation unavailable in the DPF backend. |
| `reader.core` | `DPFResultCore` | Provides the core result object backed by DPF. |
| `reader.data` | `DPFResultData` | Provides access to and manipulation of DPF result data. |
| `reader.plotting` | `DPFResultPlotting` | Provides plotting capabilities for DPF results. |
| `report` | `Plain_Report` | Provides the plain report implementation. |
| `report` | `Report` | Builds a `scooby.Report` for the PyMAPDL environment. |

## Utility and parsing modules

| Module | Symbol | Purpose |
| --- | --- | --- |
| `misc` | `check_valid_routine` | Checks whether a MAPDL routine is valid. |
| `misc` | `quote_path_if_needed` | Quotes paths containing spaces. |
| `misc` | `unquote_path` | Removes one pair of wrapping single quotes. |
| `misc` | `is_float` | Tests whether a string can be converted to a float. |
| `misc` | `get_local_ip` | Gets the local machine IP address. |
| `misc` | `random_string` | Generates a random string of a fixed length. |
| `misc` | `check_has_mapdl` | Safely checks for an Ansys installation. |
| `misc` | `run_as` | Runs a MAPDL method in PREP7 and restores the prior routine. |
| `misc` | `threaded` | Runs a function in a thread. |
| `misc` | `threaded_daemon` | Runs a function in a daemon thread. |
| `misc` | `unique_rows` | Returns unique array rows and their indices. |
| `misc` | `creation_time` | Gets a file creation time. |
| `misc` | `last_created` | Finds the newest file in a collection. |
| `misc` | `create_temp_dir` | Creates a unique temporary directory. |
| `misc` | `load_file` | Provides a file to a MAPDL instance. |
| `misc` | `check_valid_ip` | Validates an IP address. |
| `misc` | `write_array` | Writes an array to a file. |
| `misc` | `requires_graphics` | Warns when the visualizer is unavailable. |
| `misc` | `requires_package` | Requires a Python package for a decorated function. |
| `misc` | `only_numbers_and_dots` | Tests whether a string contains only numbers and dots. |
| `misc` | `get_ip_hostname` | Gets an IP address and hostname. |
| `parameters` | `interp_star_status` | Interprets `*STATUS` output from MAPDL. |
| `parameters` | `get_apdl_math_dimensions` | Converts APDLMath dimensions to a tuple or integer. |
| `parse` | `parse_kdist` | Parses a keypoint value from a keypoint message. |
| `parse` | `parse_et` | Parses a local element type definition. |
| `parse` | `parse_e` | Parses an element creation message. |
| `parse` | `parse_k` | Parses output from the `K` command. |
| `parse` | `parse_kpoint` | Parses a keypoint creation message. |
| `parse` | `parse_output_areas` | Parses an area creation message. |
| `parse` | `parse_a` | Parses an area creation message. |
| `parse` | `parse_line_no` | Parses a line creation message. |
| `parse` | `parse_line_nos` | Parses line creation output. |
| `parse` | `parse_v` | Parses a volume creation message. |
| `parse` | `parse_output_volume_area` | Parses an area or volume creation message. |
| `parse` | `parse_n` | Parses output from the `N` command. |
| `parse` | `parse_ndist` | Parses a node value from a node message. |
| `parse` | `parse_kl` | Parses output from the `KL` command. |
| `parse` | `parse_knode` | Parses output from the `KNODE` command. |
| `mesh.mesh` | `fix_missing_midside` | Adds missing midside nodes to mesh cells. |
| `pool` | `available_ports` | Returns ports starting from a specified port. |

## Plotting and command infrastructure

| Module | Symbol | Purpose |
| --- | --- | --- |
| `plotting.plotting_defaults` | `ArrowSource` | Defines the default plotting arrow source. |
| `plotting.plotting_defaults` | `DefaultSymbol` | Defines the default plotting symbol. |
| `plotting.theme` | `get_ansys_cmap` | Returns an Ansys Matplotlib colormap. |
| `plotting.theme` | `get_ansys_colors` | Returns Ansys colors as an array. |
| `plotting.theme` | `get_ansys_color_cycle` | Returns the Ansys color cycle. |
| `plotting.visualizer` | `MapdlPlotterBackend` | Provides the PyMAPDL plotting backend. |
| `commands` | `inject_docs` | Injects text into a docstring. |
| `commands` | `check_valid_output` | Validates that command output can be wrapped by pandas. |
| `commands` | `Commands` | Provides the base wrapper for MAPDL commands. |
| `commands` | `CommandOutput` | Provides a string subclass for command output. |
| `commands` | `ComponentListing` | Represents formatted component-listing output. |
| `commands` | `StringWithLiteralRepr` | Preserves literal string representations in command output. |

## Additional definitions requiring triage

These definitions are public Python names but are primarily CLI entry points,
internal decorators, compatibility helpers, example-data helpers, or parsing
implementation details. They are listed so the audit is complete; each should
be either documented or explicitly kept out of the public API.

| Module | Symbol | Purpose |
| --- | --- | --- |
| `cli/check.py` | `check_cli` | Connects to MAPDL and prints diagnostic information. |
| `cli/convert.py` | `convert_cli` | Converts MAPDL code to PyMAPDL. |
| `cli/exec.py` | `exec_cli` | Executes MAPDL commands on a running instance. |
| `cli/help.py` | `help_cli` | Prints the Python docstring for a MAPDL command. |
| `cli/list_instances.py` | `list_instances_cli` | Lists MAPDL processes on the machine. |
| `cli/skills.py` | `UnknownSkillError` | Reports that a requested skill is not bundled. |
| `cli/skills.py` | `UnsupportedScopeError` | Reports an unsupported installation scope. |
| `cli/skills.py` | `SkillInfo` | Stores metadata for a bundled skill. |
| `cli/skills.py` | `SkillInstallPlan` | Describes files an installation will create or update. |
| `cli/skills.py` | `skills` | Registers the bundled-skill CLI group. |
| `cli/skills.py` | `list_skills_cli` | Lists bundled skills. |
| `cli/skills.py` | `show_skill_cli` | Prints a skill's `SKILL.md` content. |
| `cli/skills.py` | `install_skill_cli` | Installs skill files into an AI coding environment. |
| `cli/start.py` | `start_cli` | Launches MAPDL and prints connection information. |
| `cli/stop.py` | `stop_cli` | Stops MAPDL by port or process ID. |
| `commands.py` | `get_indentation` | Gets a docstring's indentation. |
| `commands.py` | `indent_text` | Applies indentation to injected docstring text. |
| `commands.py` | `get_docstring_indentation` | Gets the indentation used by a docstring. |
| `commands.py` | `get_sections` | Extracts sections from a docstring. |
| `commands.py` | `get_section_indentation` | Gets the indentation for a named docstring section. |
| `commands.py` | `inject_before` | Injects text before a docstring location. |
| `commands.py` | `inject_after_return_section` | Injects text after a docstring return section. |
| `commands.py` | `Prep7Commands` | Groups PREP7 command methods. |
| `commands.py` | `Apdl` | Groups general APDL command methods. |
| `commands.py` | `Aux2Commands` | Groups AUX2 command methods. |
| `commands.py` | `Aux3Commands` | Groups AUX3 command methods. |
| `commands.py` | `Aux12Commands` | Groups AUX12 command methods. |
| `commands.py` | `Aux15Commands` | Groups AUX15 command methods. |
| `commands.py` | `DatabaseCommands` | Groups database command methods. |
| `commands.py` | `GraphicsCommands` | Groups graphics command methods. |
| `commands.py` | `MapCommands` | Groups MAP command methods. |
| `commands.py` | `MiscCommands` | Groups miscellaneous command methods. |
| `commands.py` | `Post1Commands` | Groups POST1 command methods. |
| `commands.py` | `Post26Commands` | Groups POST26 command methods. |
| `commands.py` | `SessionCommands` | Groups session command methods. |
| `commands.py` | `SolutionCommands` | Groups solution command methods. |
| `commands.py` | `InqFunctions` | Groups inquiry functions. |
| `convert.py` | `Lines` | Represents translated MAPDL lines. |
| `convert.py` | `FileTranslator` | Translates MAPDL files to PyMAPDL syntax. |
| `database/database.py` | `check_mapdl_db_is_alive` | Checks that `MAPDL.DB` has started. |
| `database/database.py` | `DBDef` | Defines database data types. |
| `errors.py` | `bcolors` | Defines terminal color constants. |
| `errors.py` | `handler` | Passes a signal to a custom interrupt handler. |
| `errors.py` | `protect_grpc` | Simplifies errors raised by gRPC calls. |
| `errors.py` | `retrieve_mapdl_from_args` | Retrieves a MAPDL instance from call arguments. |
| `errors.py` | `handle_generic_grpc_error` | Handles non-custom gRPC errors. |
| `errors.py` | `protect_from` | Prevents decorated methods from raising selected exceptions. |
| `examples/downloads.py` | `check_directory_exist` | Checks whether an example-data directory exists. |
| `examples/downloads.py` | `get_ext` | Extracts a filename extension. |
| `examples/downloads.py` | `delete_downloads` | Deletes downloaded example data. |
| `examples/downloads.py` | `download_bracket` | Downloads an IGS bracket. |
| `examples/downloads.py` | `download_tech_demo_data` | Downloads Tech Demo data. |
| `examples/downloads.py` | `download_vtk_rotor` | Downloads the rotor VTK file. |
| `examples/downloads.py` | `download_example_data` | Downloads example data. |
| `examples/downloads.py` | `download_manifold_example_data` | Downloads manifold example data. |
| `examples/downloads.py` | `download_cfx_mapping_example_data` | Downloads CFX mapping data. |
| `examples/verif_files.py` | `load_vmfiles` | Loads verification files and stores their filenames. |
| `helpers.py` | `is_installed` | Checks whether a package is installed. |
| `helpers.py` | `get_python_version` | Returns the running Python version. |
| `helpers.py` | `run_first_time` | Performs first-import setup. |
| `helpers.py` | `run_every_import` | Performs setup on every import. |
| `information.py` | `update_information_first` | Wraps the first information update. |
| `information.py` | `Information` | Provides information from the MAPDL `/STATUS` command. |
| `inline_functions/core.py` | `SelectionStatus` | Enumerates entity selection status values. |
| `jupyter.py` | `check_manager` | Checks the Jupyter cluster manager. |
| `jupyter.py` | `launch_mapdl_on_cluster` | Starts MAPDL on the Ansys Jupyter cluster. |
| `mapdl_core.py` | `STATUS` | Defines MAPDL status values. |
| `mapdl_core.py` | `parse_to_short_cmd` | Converts a MAPDL command to its four-character form. |
| `mapdl_core.py` | `setup_logger` | Configures a logger. |
| `mesh_grpc.py` | `requires_model` | Requires a loaded model for an operation. |
| `misc.py` | `ROUTINES` | Defines supported MAPDL routines. |
| `misc.py` | `supress_logging` | Suppresses logging for a MAPDL instance. |
| `misc.py` | `no_return` | Discards a wrapped function's return value. |
| `misc.py` | `get_bounding_box` | Computes a geometry bounding box. |
| `misc.py` | `parse_ip_route` | Parses an IP route. |
| `misc.py` | `check_valid_port` | Validates a network port. |
| `misc.py` | `is_package_installed_cached` | Checks package availability using a cache. |
| `misc.py` | `check_deprecated_vtk_kwargs` | Warns about deprecated VTK keyword arguments. |
| `misc.py` | `allow_pickable_entities` | Enables picking entities from a MAPDL plot. |
| `misc.py` | `allow_iterables_vmin` | Handles iterable minimum-value plotting arguments. |
| `misc.py` | `stack` | Stacks multiple decorators. |
| `misc.py` | `expand_all_inner_lists` | Expands nested lists. |
| `parameters.py` | `find_parameter_listing_line` | Finds a parameter-listing line. |
| `parameters.py` | `parameter_header` | Identifies a parameter-listing header. |
| `parameters.py` | `math_header` | Identifies an APDLMath header. |
| `parameters.py` | `array_header` | Identifies an array header. |
| `parameters.py` | `is_parameter_listing` | Tests whether output is a parameter listing. |
| `parameters.py` | `is_math_listing` | Tests whether output is an APDLMath listing. |
| `parameters.py` | `is_array_listing` | Tests whether output is an array listing. |
| `post.py` | `elem_check_inputs` | Validates element inputs. |
| `post.py` | `check_elem_option` | Validates an element option. |
| `post.py` | `check_result_loaded` | Verifies that a result is loaded. |
| `post.py` | `check_comp` | Validates a component name. |
| `reader/core.py` | `update_result` | Wraps DPF result updates. |

## Follow-up

The symbols in this file should either be added to an appropriate API
subpage, intentionally marked internal, or excluded from the public API. The
largest groups that need an API design decision are the launcher
configuration/models, exception hierarchy, reader backends, and low-level
parsers. In particular, helper functions used only internally should not be
published merely because they are top-level Python definitions.
