import os
from warnings import warn

try:
    import click

    _HAS_CLICK = True
except ModuleNotFoundError:
    _HAS_CLICK = False

if _HAS_CLICK:
    ###################################
    # Convert CLI

    @click.command()
    @click.argument("filename_in")
    @click.option("-o", default=None, help="Name of the output Python script.")
    @click.option(
        "--filename_out", default=None, help="Name of the output Python script."
    )
    @click.option(
        "--loglevel",
        default="WARNING",
        help="Logging level of the ansys object within the script.",
    )
    @click.option(
        "--auto_exit",
        default=True,
        help="Adds a line to the end of the script to exit MAPDL. Default ``True``",
    )
    @click.option(
        "--line_ending", default=None, help="When None, automatically is ``\n.``"
    )
    @click.option(
        "--exec_file",
        default=None,
        help="Specify the location of the ANSYS executable and include it in the converter output ``launch_mapdl`` call.",
    )
    @click.option(
        "--macros_as_functions",
        default=True,
        help="Attempt to convert MAPDL macros to python functions.",
    )
    @click.option(
        "--use_function_names",
        default=True,
        help="Convert MAPDL functions to ansys.mapdl.core.Mapdl class methods.  When ``True``, the MAPDL command ``K`` will be converted to ``mapdl.k``.  When ``False``, it will be converted to ``mapdl.run('k')``.",
    )
    @click.option(
        "--show_log",
        default=False,
        help="Print the converted commands using a logger (from ``logging`` Python module).",
    )
    @click.option(
        "--add_imports",
        default=True,
        help='If ``True``, add the lines ``from ansys.mapdl.core import launch_mapdl`` and ``mapdl = launch_mapdl(loglevel="WARNING")`` to the beginning of the output file. This option is useful if you are planning to use the output script from another mapdl session. See examples section. This option overrides ``auto_exit``.',
    )
    @click.option(
        "--comment_solve",
        default=False,
        help='If ``True``, it will pythonically comment the lines that contain ``"SOLVE"`` or ``"/EOF"``.',
    )
    @click.option(
        "--cleanup_output",
        default=True,
        help="If ``True`` the output is formatted using ``autopep8`` before writing the file or returning the string. This requires ``autopep8`` to be installed.",
    )
    @click.option(
        "--header",
        default=True,
        help="If ``True``, the default header is written in the first line of the output. If a string is provided, this string will be used as header.",
    )
    @click.option(
        "--print_com",
        default=True,
        help="Print command ``/COM`` arguments to python console. Defaults to ``True``.",
    )
    def convert(
        filename_in,
        o,
        filename_out,
        loglevel,
        auto_exit,
        line_ending,
        exec_file,
        macros_as_functions,
        use_function_names,
        show_log,
        add_imports,
        comment_solve,
        cleanup_output,
        header,
        print_com,
    ):
        """PyMAPDL CLI tool for converting MAPDL scripts to PyMAPDL scripts.

        USAGE:

        This example demonstrates the main use of this tool:

            $ pymapdl_convert_script mapdl.dat -o python.py

            File mapdl.dat successfully converted to python.py.

        The output argument is optional, in which case the "py" extension is used:

            $ pymapdl_convert_script mapdl.dat

            File mapdl.dat successfully converted to mapdl.py.

        You can use any option from ``ansys.mapdl.core.convert.convert_script`` function:

            $ pymapdl_convert_script mapdl.dat --auto-exit False

            File mapdl.dat successfully converted to mapdl.py.

            $ pymapdl_convert_script.exe mapdl.dat --filename_out mapdl.out --add_imports False

            File mapdl.dat successfully converted to mapdl.out.


        """
        from ansys.mapdl.core.convert import convert_script

        if o:
            filename_out = o

        convert_script(
            filename_in,
            filename_out,
            loglevel,
            auto_exit,
            line_ending,
            exec_file,
            macros_as_functions,
            use_function_names,
            show_log,
            add_imports,
            comment_solve,
            cleanup_output,
            header,
            print_com,
        )

        if filename_out:
            print(f"File {filename_in} successfully converted to {filename_out}.")
        else:
            print(
                f"File {filename_in} successfully converted to {os.path.splitext(filename_in)[0] + '.py'}."
            )

    from ansys.mapdl.core.launcher import launch_mapdl

    @click.command(
        short_help="Launch MAPDL instances.",
        help="For more information see :func:`ansys.mapdl.core.launcher.launch_mapdl`.",
    )
    @click.option(
        "--exec_file",
        default=None,
        type=str,
        help="The location of the MAPDL executable.  Will use the cached location when left at the default ``None`` and no environment variable is set. The executable path can be also set through the environment variable ``PYMAPDL_MAPDL_EXEC``.",
    )
    @click.option(
        "--run_location",
        default=None,
        type=str,
        help="MAPDL working directory.  Defaults to a temporary working directory.  If directory doesn't exist, one is created.",
    )
    @click.option(
        "--jobname",
        default="",
        type=str,
        help="MAPDL jobname.  Defaults to ``'file'``.",
    )
    @click.option(
        "--nproc", type=int, default=2, help="Number of processors.  Defaults to 2."
    )
    @click.option(
        "--ram",
        default=None,
        type=int,
        help="Fixed amount of memory to request for MAPDL.  If ``None``, then MAPDL will use as much as available on the host machine.",
    )
    @click.option(
        "--mode",
        type=str,
        default=None,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--override",
        default=False,
        type=bool,
        help="Attempts to delete the lock file at the ``run_location``. Useful when a prior MAPDL session has exited prematurely and the lock file has not been deleted.",
    )
    @click.option(
        "--loglevel",
        default="",
        type=str,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--additional_switches",
        default="",
        type=str,
        help="Additional switches for MAPDL, for example ``'aa_r'``, the academic research license. Avoid adding switches like ``-i``, ``-o`` or ``-b`` as these are already included to start up the MAPDL server.",
    )
    @click.option(
        "--start_timeout",
        default=45,
        type=int,
        help="Maximum allowable time to connect to the MAPDL server.",
    )
    @click.option(
        "--port",
        default=None,
        type=int,
        help="Port to launch MAPDL gRPC on.  Final port will be the first port available after (or including) this port.  Defaults to 50052. You can also override the port default with the environment variable ``PYMAPDL_PORT=<VALID PORT>`` This argument has priority over the environment variable.",
    )
    @click.option(
        "--cleanup_on_exit",
        default=False,
        type=bool,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--start_instance",
        default=None,
        type=bool,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--ip",
        default=None,
        type=str,
        help="Used only when ``start_instance`` is ``False``. If provided, it will force ``start_instance`` to be ``False``. Specify the IP address of the MAPDL instance to connect to. You can also provide a hostname as an alternative to an IP address. Defaults to ``'127.0.0.1'``. You can also override the default behavior of this keyword argument with the environment variable ``PYMAPDL_IP=<IP>``. This argument has priority over the environment variable.",
    )
    @click.option(
        "--clear_on_connect",
        default=True,
        type=bool,
        help="Defaults to ``True``, giving you a fresh environment when connecting to MAPDL. When if ``start_instance`` is specified it defaults to ``False``.",
    )
    @click.option(
        "--log_apdl",
        default=None,
        type=str,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--remove_temp_files",
        default=None,
        type=str,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--remove_temp_dir_on_exit",
        default=False,
        type=str,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--verbose_mapdl",
        default=None,
        type=str,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--license_server_check",
        default=True,
        type=bool,
        help="Check if the license server is available if MAPDL fails to start.  Only available on ``mode='grpc'``. Defaults ``True``.",
    )
    @click.option(
        "--license_type",
        default=None,
        type=str,
        help="Enable license type selection. You can input a string for its license name (for example ``'meba'`` or ``'ansys'``) or its description ('enterprise solver' or 'enterprise' respectively). You can also use legacy licenses (for example ``'aa_t_a'``) but it will also raise a warning. If it is not used (``None``), no specific license will be requested, being up to the license server to provide a specific license type. Default is ``None``.",
    )
    @click.option(
        "--print_com",
        default=False,
        type=str,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--add_env_vars",
        default=None,
        type=str,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--replace_env_vars",
        default=None,
        type=str,
        help="Argument not allowed in CLI. It will be ignored.",
    )
    @click.option(
        "--version",
        default=None,
        type=str,
        help="Version of MAPDL to launch. If ``None``, the latest version is used. Versions can be provided as integers (i.e. ``version=222``) or floats (i.e. ``version=22.2``). To retrieve the available installed versions, use the function :meth:`ansys.tools.path.path.get_available_ansys_installations`.",
    )
    def launch_mapdl(
        exec_file,
        run_location,
        jobname,
        nproc,
        ram,
        mode,
        override,
        loglevel,
        additional_switches,
        start_timeout,
        port,
        cleanup_on_exit,
        start_instance,
        ip,
        clear_on_connect,
        log_apdl,
        remove_temp_files,
        remove_temp_dir_on_exit,
        verbose_mapdl,
        license_server_check,
        license_type,
        print_com,
        version,
    ):
        from ansys.mapdl.core.launcher import launch_mapdl

        if mode and mode != "grpc":
            warn(
                "Only gRPC mode is allowed when using CLI to launch MAPDL instances.\nIgnoring argument."
            )

        if loglevel:
            warn(
                "The following argument is not allowed in CLI: 'loglevel'.\nIgnoring argument."
            )

        if cleanup_on_exit:
            warn(
                "The following argument is not allowed in CLI: 'cleanup_on_exit'.\nIgnoring argument."
            )

        if start_instance:
            warn(
                "The following argument is not allowed in CLI: 'start_instance'.\nIgnoring argument."
            )

        if log_apdl:
            warn(
                "The following argument is not allowed in CLI: 'log_apdl'.\nIgnoring argument."
            )

        if remove_temp_files:
            warn(
                "The following argument is not allowed in CLI: 'remove_temp_files'.\nIgnoring argument."
            )

        if remove_temp_dir_on_exit:
            warn(
                "The following argument is not allowed in CLI: 'remove_temp_dir_on_exit'.\nIgnoring argument."
            )

        if verbose_mapdl:
            warn(
                "The following argument is not allowed in CLI: 'verbose_mapdl'.\nIgnoring argument."
            )

        if print_com:
            warn(
                "The following argument is not allowed in CLI: 'print_com'.\nIgnoring argument."
            )

        launch_mapdl(
            just_launch=True,
            run_location=run_location,
            jobname=jobname,
            nproc=nproc,
            ram=ram,
            mode=mode,
            override=override,
            additional_switches=additional_switches,
            start_timeout=start_timeout,
            port=port,
            ip=ip,
            clear_on_connect=clear_on_connect,
            license_server_check=license_server_check,
            license_type=license_type,
            add_env_vars=add_env_vars,
            replace_env_vars=replace_env_vars,
            version=version,
        )

else:

    def convert():
        print("PyMAPDL CLI requires click to be installed.")

    def launch_mapdl():
        print("PyMAPDL CLI requires click to be installed.")
