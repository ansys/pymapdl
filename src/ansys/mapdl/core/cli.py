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

import os

import psutil

PROCESS_OK_STATUS = [
    # List of all process status, comment out the ones that means that
    # process is not OK.
    # If process is OK, it means it can be killed normally.
    psutil.STATUS_RUNNING,  #
    psutil.STATUS_SLEEPING,  #
    psutil.STATUS_DISK_SLEEP,  #
    # psutil.STATUS_STOPPED, #
    # psutil.STATUS_TRACING_STOP, #
    # psutil.STATUS_ZOMBIE, #
    psutil.STATUS_DEAD,  #
    # psutil.STATUS_WAKE_KILL, #
    # psutil.STATUS_WAKING, #
    psutil.STATUS_PARKED,  # (Linux)
    psutil.STATUS_IDLE,  # (Linux, macOS, FreeBSD)
    # psutil.STATUS_LOCKED, # (FreeBSD)
    # psutil.STATUS_WAITING, # (FreeBSD)
    # psutil.STATUS_SUSPENDED, # (NetBSD)
]

try:
    import click
    from tabulate import tabulate

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

    def is_ansys_process(proc):
        return (
            "ansys" in proc.name().lower() or "mapdl" in proc.name().lower()
        ) and "-grpc" in proc.cmdline()

    class MyGroup(click.Group):
        def invoke(self, ctx):
            ctx.obj = tuple(ctx.args)
            super(MyGroup, self).invoke(ctx)

    @click.group(invoke_without_command=True, cls=MyGroup)
    @click.pass_context
    def launch_mapdl(ctx):
        args = ctx.obj
        if ctx.invoked_subcommand is None:
            from ansys.mapdl.core.cli import start

            start(args)

    @launch_mapdl.command(
        short_help="Launch MAPDL instances.",
        help="""This command aims to replicate the behavior of :func:`ansys.mapdl.core.launcher.launch_mapdl`

For more information see :func:`ansys.mapdl.core.launcher.launch_mapdl`.""",
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
        default="file",
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
        help="Argument not allowed in CLI. It will be ignored",
    )
    @click.option(
        "--clear_on_connect",
        default=False,
        type=bool,
        help="Argument not allowed in CLI. It will be ignored",
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
        type=bool,
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
        default=False,
        type=bool,
        help="Argument not allowed in CLI. It will be ignored.",
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
        type=bool,
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
    def start(
        exec_file,
        run_location,
        jobname,
        nproc,
        ram,
        mode,  # ignored
        override,
        loglevel,  # ignored
        additional_switches,
        start_timeout,
        port,
        cleanup_on_exit,  # ignored
        start_instance,  # ignored
        ip,
        clear_on_connect,  # ignored
        log_apdl,  # ignored
        remove_temp_files,  # ignored
        remove_temp_dir_on_exit,  # ignored
        verbose_mapdl,  # ignored
        license_server_check,  # ignored
        license_type,
        print_com,  # ignored
        add_env_vars,  # ignored
        replace_env_vars,  # ignored
        version,
    ):
        from ansys.mapdl.core.launcher import launch_mapdl

        if mode:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'mode'.\nIgnoring argument."
            )

        if loglevel:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'loglevel'.\nIgnoring argument."
            )

        if cleanup_on_exit:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'cleanup_on_exit'.\nIgnoring argument."
            )

        if start_instance:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'start_instance'.\nIgnoring argument."
            )

        if ip:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'ip'.\nIgnoring argument."
            )

        if clear_on_connect:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'clear_on_connect'.\nIgnoring argument."
            )

        if log_apdl:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'log_apdl'.\nIgnoring argument."
            )

        if remove_temp_files:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'remove_temp_files'.\nIgnoring argument."
            )

        if remove_temp_dir_on_exit:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'remove_temp_dir_on_exit'.\nIgnoring argument."
            )

        if verbose_mapdl:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'verbose_mapdl'.\nIgnoring argument."
            )

        if print_com:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'print_com'.\nIgnoring argument."
            )

        if add_env_vars:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'add_env_vars'.\nIgnoring argument."
            )

        if replace_env_vars:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'replace_env_vars'.\nIgnoring argument."
            )

        if license_server_check:
            click.echo(
                click.style("Warn:", fg="yellow")
                + " The following argument is not allowed in CLI: 'license_server_check'.\nIgnoring argument."
            )

        out = launch_mapdl(
            exec_file=exec_file,
            just_launch=True,
            run_location=run_location,
            jobname=jobname,
            nproc=nproc,
            ram=ram,
            override=override,
            additional_switches=additional_switches,
            start_timeout=start_timeout,
            port=port,
            license_server_check=license_server_check,
            license_type=license_type,
            version=version,
        )

        if len(out) == 3:
            header = f"Launched an MAPDL instance (PID={out[2]}) at "
        else:
            header = "Launched an MAPDL instance at "

        click.echo(click.style("Success: ", fg="green") + header + f"{out[0]}:{out[1]}")

    @launch_mapdl.command(
        short_help="Stop MAPDL instances.",
        help="""This command stop MAPDL instances running on a given port or with a given process id (PID).

By default, it stops instances running on the port 50052.""",
    )
    @click.option(
        "--port",
        default=None,
        type=int,
        help="Port where the MAPDL instance is running.",
    )
    @click.option(
        "--pid",
        default=None,
        type=int,
        help="Process PID where the MAPDL instance is running.",
    )
    @click.option(
        "--all",
        is_flag=True,
        flag_value=True,
        type=bool,
        default=False,
        help="Kill all MAPDL instances",
    )
    def stop(port, pid, all):
        if not pid and not port:
            port = 50052

        if port or all:
            killed_ = False
            for proc in psutil.process_iter():
                if (
                    psutil.pid_exists(proc.pid)
                    and proc.status() in PROCESS_OK_STATUS
                    and is_ansys_process(proc)
                ):
                    # Killing "all"
                    if all:
                        try:
                            proc.kill()
                            killed_ = True
                        except psutil.NoSuchProcess:
                            pass

                    else:
                        # Killing by ports
                        if str(port) in proc.cmdline():
                            try:
                                proc.kill()
                                killed_ = True
                            except psutil.NoSuchProcess:
                                pass

            if all:
                str_ = ""
            else:
                str_ = f" running on port {port}"

            if not killed_:
                click.echo(
                    click.style("ERROR: ", fg="red")
                    + "No Ansys instances"
                    + str_
                    + " have been found."
                )
            else:
                click.echo(
                    click.style("Success: ", fg="green")
                    + "Ansys instances"
                    + str_
                    + " have been stopped."
                )
            return

        if pid:
            try:
                pid = int(pid)
            except ValueError:
                click.echo(
                    click.style("ERROR: ", fg="red")
                    + "PID provided could not be converted to int."
                )

            p = psutil.Process(pid)
            for child in p.children(recursive=True):
                child.kill()
            p.kill()

            if p.status == "running":
                click.echo(
                    click.style("ERROR: ", fg="red")
                    + f"The process with PID {pid} and its children could not be killed."
                )
            else:
                click.echo(
                    click.style("Success: ", fg="green")
                    + f"The process with PID {pid} and its children have been stopped."
                )
            return

    @launch_mapdl.command(
        short_help="List MAPDL instances.",
        help="""This command list MAPDL instances""",
    )
    @click.option(
        "--instances",
        "-i",
        is_flag=True,
        flag_value=True,
        type=bool,
        default=False,
        help="Print only instances",
    )
    @click.option(
        "--long",
        "-l",
        is_flag=True,
        flag_value=True,
        type=bool,
        default=False,
        help="Print all info.",
    )
    @click.option(
        "--cmd",
        "-c",
        is_flag=True,
        flag_value=True,
        type=bool,
        default=False,
        help="Print cmd",
    )
    @click.option(
        "--location",
        "-cwd",
        is_flag=True,
        flag_value=True,
        type=bool,
        default=False,
        help="Print running location info.",
    )
    def list(instances, long, cmd, location):
        # Assuming all ansys processes have -grpc flag
        mapdl_instances = []
        for proc in psutil.process_iter():
            if (
                "ansys" in proc.name().lower() or "mapdl" in proc.name().lower()
            ) and "-grpc" in proc.cmdline():
                if len(proc.children(recursive=True)) < 2:
                    proc.ansys_instance = False
                else:
                    proc.ansys_instance = True
                mapdl_instances.append(proc)

        # printing
        table = []

        if long:
            cmd = True
            location = True

        if instances:
            headers = ["Name", "Status", "gRPC port", "PID"]
        else:
            headers = ["Name", "Is Instance", "Status", "gRPC port", "PID"]

        if cmd:
            headers.append("Command line")
        if location:
            headers.append("Working directory")

        def get_port(proc):
            cmdline = proc.cmdline()
            ind_grpc = cmdline.index("-port")
            return cmdline[ind_grpc + 1]

        table = []
        for each_p in mapdl_instances:
            if instances and not each_p.ansys_instance:
                continue

            proc_line = []
            proc_line.append(each_p.name())

            if not instances:
                proc_line.append(each_p.ansys_instance)

            proc_line.extend([each_p.status(), get_port(each_p), each_p.pid])

            if cmd:
                proc_line.append(" ".join(each_p.cmdline()))

            if location:
                proc_line.append(each_p.cwd())

            table.append(proc_line)

        print(tabulate(table, headers))

else:

    def convert():
        print("PyMAPDL CLI requires 'click' python package to be installed.")

    def launch_mapdl():
        print("PyMAPDL CLI requires 'click' python package to be installed.")

    def stop_mapdl():
        print("PyMAPDL CLI requires 'click' python package to be installed.")
