from logging import Logger, StreamHandler
import os
import re
from warnings import warn

from ansys.mapdl.core import __version__
from ansys.mapdl.core.commands import Commands
from ansys.mapdl.core.misc import is_float

# Because the APDL version has empty arguments, whereas the PyMAPDL
# doesn't have them. Hence the order of arguments is messed up.
COMMANDS_TO_NOT_BE_CONVERTED = {"INT1"}

FORMAT_OPTIONS = {
    "select": "W191,W291,W293,W391,E115,E117,E122,E124,E125,E225,E231,E301,E303,F401,F403",
    "max-line-length": 100,
}


def convert_script(
    filename_in,
    filename_out,
    loglevel="WARNING",
    auto_exit=True,
    line_ending=None,
    exec_file=None,
    macros_as_functions=True,
    use_function_names=True,
    show_log=False,
    add_imports=True,
    comment_solve=False,
    cleanup_output=True,
    header=True,
    print_com=True,
):
    """Converts an ANSYS input file to a python PyMAPDL script.

    Parameters
    ----------
    filename_in : str
        Filename of the ansys input file to read in.

    filename_out : str
        Filename of the python script to write a translation to.

    loglevel : str, optional
        Logging level of the ansys object within the script.

    auto_exit : bool, optional
        Adds a line to the end of the script to exit MAPDL.  Default
        ``True``.

    line_ending : str, optional
        When None, automatically determined by OS being used.

    macros_as_functions : bool, optional
        Attempt to convert MAPDL macros to python functions.

    use_function_names : bool, optional
        Convert MAPDL functions to ansys.mapdl.core.Mapdl class
        methods.  When ``True``, the MAPDL command "K" will be
        converted to ``mapdl.k``.  When ``False``, it will be
        converted to ``mapdl.run('k')``.

    show_log : bool, optional
        Print the converted commands using a logger (from ``logging``
        Python module).

    add_imports : bool, optional
        If ``True``, add the lines ``from ansys.mapdl.core import launch_mapdl``
        and ``mapdl = launch_mapdl(loglevel="WARNING")``to the beginning of the
        output file. This option is useful if you are planning to use the output
        script from another mapdl session. See examples section.
        This option overrides ``auto_exit``.

    comment_solve : bool, optional
        If ``True``, it will pythonically comment the lines that
        contain ``mapdl.solve`` or ``"/EOF"``.

    cleanup_output : bool, optional
        If ``True`` the output is formatted using ``autopep8`` before writing
        the file or returning the string. This requires ``autopep8`` to be
        installed.

    header : bool, optional
        If ``True``, the default header is written in the first line
        of the output. If a string is provided, this string will be
        used as header.

    print_com : bool, optional
        Print command ``/COM`` arguments to python console.
        Defaults to ``True``.

    Returns
    -------
    list
        List of lines translated.

    Examples
    --------
    >>> from ansys.mapdl import core as pymapdl
    >>> from ansys.mapdl.core import examples
    >>> clines = pymapdl.convert_script(examples.vmfiles['vm1'], 'vm1.py')

    Converting a script and using it already in the same session.
    For this case, it is recommended to use ``convert_apdl_block``
    from the ``converter`` module since you do not have to write the file.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> from ansys.mapdl.core import examples
    >>> from ansys.mapdl.core import convert_script
    >>> in_file = examples.vmfiles['vm10']
    >>> filename = in_file.split('\\')[-1]
    >>> out_file = 'out_' + filename.replace('.dat', '.py')
    >>> output = convert_script(file, out_file, line_ending='\\n')
    >>> mapdl = launch_mapdl()
    >>> with open(out_file, 'r') as fid:
    ...     cmds = fid.read()
    >>> mapdl.input_strings(cmds.splitlines()[2:10])

    """
    with open(filename_in, "r") as fid:
        apdl_strings = fid.readlines()

    translator = _convert(
        apdl_strings=apdl_strings,
        loglevel=loglevel,
        auto_exit=auto_exit,
        line_ending=line_ending,
        exec_file=exec_file,
        macros_as_functions=macros_as_functions,
        use_function_names=use_function_names,
        show_log=show_log,
        add_imports=add_imports,
        comment_solve=comment_solve,
        cleanup_output=cleanup_output,
        header=header,
        print_com=print_com,
    )

    translator.save(filename_out)
    return translator.lines


def convert_apdl_block(
    apdl_strings,
    loglevel="WARNING",
    auto_exit=True,
    line_ending=None,
    exec_file=None,
    macros_as_functions=True,
    use_function_names=True,
    show_log=False,
    add_imports=True,
    comment_solve=False,
    cleanup_output=True,
    header=True,
    print_com=True,
):
    """Converts an ANSYS input string to a python PyMAPDL string.

    Parameters
    ----------
    apdl_string : str
        APDL strings or list of strings to convert.

    filename_out : str
        Filename of the python script to write a translation to.

    loglevel : str, optional
        Logging level of the ansys object within the script.

    auto_exit : bool, optional
        Adds a line to the end of the script to exit MAPDL.  Default
        ``True``.

    line_ending : str, optional
        When None, automatically determined by OS being used.

    macros_as_functions : bool, optional
        Attempt to convert MAPDL macros to python functions.

    use_function_names : bool, optional
        Convert MAPDL functions to ansys.mapdl.core.Mapdl class
        methods.  When ``True``, the MAPDL command "K" will be
        converted to ``mapdl.k``.  When ``False``, it will be
        converted to ``mapdl.run('k')``.

    show_log : bool, optional
        Print the converted commands using a logger (from ``logging``
        Python module).

    add_imports : bool, optional
        If ``True``, it add the next lines to the beginning of the
        output file:

        .. code:: python

           from ansys.mapdl.core import launch_mapdl
           mapdl = launch_mapdl(loglevel="WARNING")

        This option is useful if you are planning to use the output
        script from another mapdl session. See examples section.
        This option overrides ``'auto_exit'``.

    comment_solve : bool, optional
        If ``True``, pythonically comment the lines containing
        ``mapdl.solve`` or ``"/EOF"``.

    cleanup_output : bool, optional
        If ``True`` the output is formatted using ``autopep8`` before
        writing the file or returning the string.

    header : bool, optional
        If ``True``, the default header is written in the first line
        of the output. If a string is provided, this string will be
        used as header.
    print_com : bool, optional
        Print command ``/COM`` arguments to python console.
        Defaults to ``True``.

    Returns
    -------
    list
        List of lines translated.

    Examples
    --------
    Convert a script and use it in the same session.

    >>> from ansys.mapdl.core import examples, launch_mapdl, convert_apdl_block
    >>> in_file = examples.vmfiles['vm10']
    >>> filename = in_file.split('\\')[-1]
    >>> out_file = 'out_' + filename.replace('.dat', '.py')
    >>> cmds = convert_apdl_block(file, out_file, line_ending='\n')
    >>> # Do any change in the text, for example:
    >>> cmds = cmds.replace('solve', '!solve')
    >>> mapdl = launch_mapdl()
    >>> mapdl.input_strings(cmds.splitlines()[2:10])

    """

    translator = _convert(
        apdl_strings,
        loglevel=loglevel,
        auto_exit=auto_exit,
        line_ending=line_ending,
        exec_file=exec_file,
        macros_as_functions=macros_as_functions,
        use_function_names=use_function_names,
        show_log=show_log,
        add_imports=add_imports,
        comment_solve=comment_solve,
        cleanup_output=cleanup_output,
        header=header,
        print_com=print_com,
    )

    if isinstance(apdl_strings, str):
        return translator.line_ending.join(translator.lines)
    return translator.lines


def _convert(
    apdl_strings,
    loglevel="WARNING",
    auto_exit=True,
    line_ending=None,
    exec_file=None,
    macros_as_functions=True,
    use_function_names=True,
    show_log=False,
    add_imports=True,
    comment_solve=False,
    cleanup_output=True,
    header=True,
    print_com=True,
):

    translator = FileTranslator(
        loglevel,
        line_ending,
        exec_file=exec_file,
        macros_as_functions=macros_as_functions,
        use_function_names=use_function_names,
        show_log=show_log,
        add_imports=add_imports,
        comment_solve=comment_solve,
        cleanup_output=cleanup_output,
        header=header,
        print_com=print_com,
    )

    if isinstance(apdl_strings, str):
        # os.linesep does not work well, so we are making sure
        # the line separation is appropriate.
        regx = f"[^\\r]({translator.line_ending})"
        if not re.search(regx, apdl_strings):
            if "\r\n" in apdl_strings:
                translator.line_ending = "\r\n"
            elif "\n" in apdl_strings:
                translator.line_ending = "\n"

        apdl_strings = apdl_strings.split(translator.line_ending)

    for line in apdl_strings:
        translator.translate_line(line)

    if auto_exit and add_imports:
        translator.write_exit()
    return translator


class Lines(list):
    def __init__(self, mute):
        self._log = Logger("convert_logger")
        self._setup_logger()
        self._mute = mute
        super().__init__()

    def append(self, item, mute=True):
        # append the item to itself (the list)
        if not self._mute:
            self._log.info(msg=f"Converted: '{item}'")
        super(Lines, self).append(item)

    def _setup_logger(self):
        stdhdl = StreamHandler()
        stdhdl.setLevel(10)
        stdhdl.set_name("stdout")
        self._log.addHandler(stdhdl)
        self._log.propagate = True


class FileTranslator:
    obj_name = "mapdl"
    indent = ""
    non_interactive = False

    def __init__(
        self,
        loglevel="INFO",
        line_ending=None,
        exec_file=None,
        macros_as_functions=True,
        use_function_names=True,
        show_log=False,
        add_imports=True,
        comment_solve=False,
        cleanup_output=True,
        header=True,
        print_com=True,
    ):
        self._non_interactive_level = 0
        self.lines = Lines(mute=not show_log)
        self._functions = []
        if line_ending:
            self.line_ending = line_ending
        else:
            self.line_ending = os.linesep
        self.macros_as_functions = macros_as_functions
        self._infunction = False
        self.use_function_names = use_function_names
        self.comment = ""
        self._add_imports = add_imports
        self._comment_solve = comment_solve
        self.cleanup_output = cleanup_output
        self._header = header
        self.print_com = print_com

        self.write_header()
        if self._add_imports:
            self.initialize_mapdl_object(loglevel, exec_file)

        self._valid_commands = dir(Commands)
        self._block_commands = {
            "NBLO": "NBLOCK",
            "EBLO": "EBLOCK",
            "BFBL": "BFBLOCK",
            "BFEB": "BFEBLOCK",
            "PREA": "PREAD",
            "SFEB": "SFEBLOCK",
        }  # Way out: '-1' , 'END PREAD'

        self._enum_block_commands = {
            "CMBL": "CMBLOCK",
        }  # Commands where you need to count the number of lines.

        _NON_INTERACTIVE_COMMANDS = {
            "*CRE": "*CREATE",
            "*VWR": "*VWRITE",
            "*VRE": "*VREAD",
        }

        self._non_interactive_commands = (
            list(_NON_INTERACTIVE_COMMANDS)
            + list(self._block_commands)
            + list(self._enum_block_commands)
        )

        self._block_count = 0
        self._block_count_target = 0
        self._in_block = False
        self._block_current_cmd = None

    def write_header(self):
        if isinstance(self._header, bool):
            if self._header:
                header = (
                    f'"""Script generated by ansys-mapdl-core version {__version__}"""'
                )
                self.lines.append(header)
        elif isinstance(self._header, str):
            self.lines.append(f'"""{self._header}"""')

        else:
            raise TypeError(
                "The keyword argument 'header' should be a string or a boolean."
            )

    def write_exit(self):
        self.lines.append(f"{self.obj_name}.exit()")

    def format_using_autopep8(self, text=None):
        """Format internal `self.lines` with autopep8.

        Parameters
        ----------
        text : str, optional
            Text to format instead of `self.lines`. For development use.

        """
        if self.cleanup_output:

            try:
                import autopep8
            except ModuleNotFoundError:  # pragma: no cover
                warn(
                    "Install `autopep8` to use this feature with\n"
                    "`pip install autopep8`"
                )
                return

            if not text:
                text = self.line_ending.join(self.lines)
                self.lines = autopep8.fix_code(text).splitlines()

            else:  # pragma: no cover
                # for development purposes
                return autopep8.fix_code(text)

    def save(self, filename, format_autopep8=True):
        """Saves lines to file"""
        if os.path.isfile(filename):
            os.remove(filename)

        # Making sure we write python string with double slash.
        # We are not expecting other type of unicode symbols.
        self.lines = [each_line.replace("\\", "\\\\") for each_line in self.lines]

        # Try to format the file using AutoPEP8
        self.format_using_autopep8()

        with open(filename, "w") as f:
            f.write(self.line_ending.join(self.lines))

    def initialize_mapdl_object(self, loglevel, exec_file):
        """Initializes ansys object as lines"""
        core_module = "ansys.mapdl.core"  # shouldn't change
        self.lines.append(f"from {core_module} import launch_mapdl")

        if exec_file:
            exec_file_parameter = f'"{exec_file}", '
        else:
            exec_file_parameter = ""

        if self.print_com:
            line = f'{self.obj_name} = launch_mapdl({exec_file_parameter}loglevel="{loglevel}", print_com=True)'
        else:
            line = f'{self.obj_name} = launch_mapdl({exec_file_parameter}loglevel="{loglevel}")'
        self.lines.append(line)

    @property
    def line_ending(self):
        return self._line_ending

    @line_ending.setter
    def line_ending(self, line_ending):
        if line_ending not in ["\n", "\r\n"]:
            raise ValueError('Line ending must be either "\\n", "\\r\\n"')
        self._line_ending = line_ending

    def translate_line(self, line):
        """Converts a single line from an ANSYS APDL script"""
        self.comment = ""
        original_line = line.replace("\r\n", "").replace(
            "\n", ""
        )  # It is needed for the nblock, eblock since they have spaces before the numbers
        line = line.strip()
        line = line.replace('"', "'")

        if self._in_block:
            self._block_count += 1

        if (
            self._in_block
            and self._block_count >= self._block_count_target
            and self._block_count_target
        ):
            self._in_block = False
            self.end_non_interactive()
            self._block_count = 0
            self._block_current_cmd = None

        # check if line contains a comment
        if "!" in line:
            if "'!'" in line or '"!"' in line:
                pass
            elif line[0] == "!":  # entire line is a comment
                self.comment = line.replace("!", "").strip()
                self.store_comment()
                return
            else:  # command and in-line comment
                split_line = line.split("!")
                line = split_line[0]
                self.comment = " ".join(split_line[1:])
                self.comment = self.comment.lstrip()

        if not line:
            return

        # Cleaning ending empty arguments.
        # Because of an extra comma added to toffst command when generating ds.dat.
        line_ = line.split(",")[::-1]  # inverting order
        for ind, each in enumerate(line_):
            if each:
                break
            else:
                line_.pop(ind)
        line = ",".join(line_[::-1])

        # remove trailing comma
        line = line[:-1] if line[-1] == "," else line

        cmd_ = line.split(",")[0].upper()

        if cmd_[:4] in ["SOLV", "LSSO"] and self._comment_solve:
            self.store_command(
                "com", ["The following line has been commented due to `comment_solve`:"]
            )
            self.store_command("com", [line])
            return

        if cmd_[:4] == "/COM":
            # It is a comment
            self.store_command("com", [line[5:]])
            return

        if cmd_ == "*DO":
            self.start_non_interactive()
            self.store_run_command(line)
            return

        if cmd_ in ["*ENDDO", "*ENDIF"]:
            self.store_run_command(line)
            self.end_non_interactive()
            return

        if self.output_to_file(line):
            self.start_non_interactive()
            self.store_run_command(line)
            return

        if self.output_to_default(line):
            self.store_run_command(line)
            self.store_run_command("/GOPR")  # Adding gopr to ensure printing out
            self.end_non_interactive()
            return

        if cmd_ == "/VERIFY":
            self.store_run_command("FINISH")
            self.store_run_command(line)
            self.store_run_command("/PREP7")
            return

        if line[:4].upper() == "*REP":
            if not self.non_interactive:
                prev_cmd = self.lines.pop(-1)
                self.start_non_interactive()
                new_prev_cmd = (
                    "    " + prev_cmd
                )  # Since we are writing in self.lines we need to add the indentation by ourselves.
                self.lines.append(new_prev_cmd)
                self.store_run_command(
                    line
                )  # Using run but it could be `store_command`
                self.end_non_interactive()
                return

        if line[:4].upper() in COMMANDS_TO_NOT_BE_CONVERTED:
            self.store_run_command(line)
            return

        if line[:4].upper() == "/TIT":  # /TITLE
            parameters = line.split(",")[1:]
            return self.store_command("title", ["".join(parameters).strip()])

        if line[:4].upper() == "*GET":
            if self.non_interactive:  # gives error
                self.store_run_command(line)
                return
            else:
                parameters = line.split(",")[1:]
                return self.store_command("get", parameters)

        if line[:4].upper() == "/NOP":
            self.comment = (
                "It is not recommended to use '/NOPR' in a normal PyMAPDL session."
            )
            self.store_under_scored_run_command(line)
            return

        if line[:6].upper() == "/PREP7":
            return self.store_command("prep7", [])

        if "*END" in line:
            if self.macros_as_functions:
                self.store_empty_line()
                self.store_empty_line()
                self.indent = self.indent[4:]
                self._infunction = False
                if not self._in_block:
                    self.end_non_interactive()
                return
            else:
                self.store_run_command(line)
                if not self._in_block:
                    self.end_non_interactive()
                return

        # check for if statement
        if line[:3].upper() == "*IF" or "*IF" in line.upper():
            self.start_non_interactive()
            self.store_run_command(line)
            return

        # check if line ends non-interactive
        if line[0] == "(":
            if not self.non_interactive:
                warn(
                    "\nPossible invalid line:\n%s\n" % line
                    + "This line requires a *VWRITE beforehand."
                    + "The previous line is: \n%s\n\n" % self.lines[-1]
                )
            self.store_run_command(line)
            if (
                not self._in_block
            ):  # To escape cmds that require (XX) but they are not in block
                self.end_non_interactive()
            return
        elif line[:4] == "*USE" and self.macros_as_functions:
            items = line.split(",")
            func_name = items[1].strip()
            if func_name in self._functions:
                args = ", ".join(items[2:])
                self.lines.append(f"{func_name}({args})")
                return

        # check if a line is setting a variable
        items = line.split(",")
        if "=" in items[0]:  # line sets a variable:
            self.store_run_command(line)
            return

        command = items[0].lower().strip()
        parameters = items[1:]
        if not command:
            self.store_empty_line()
            return

        if line == "-1" or line == "END PREAD":  # End of block commands
            self.store_run_command(line)
            self._in_block = False
            self.end_non_interactive()
            return

        # check valid command
        if command not in self._valid_commands:
            cmd = line[:4].upper()
            if cmd == "*CRE":  # creating a function
                if self.macros_as_functions:
                    self.start_function(items[1].strip())
                    return
                else:
                    self.start_non_interactive()

            elif cmd in self._non_interactive_commands:
                if cmd in self._block_commands:
                    self._in_block = True
                    self._block_count = 0
                    self._block_count_target = 0

                elif cmd in self._enum_block_commands:
                    self._in_block = True
                    self._block_count = 0
                    if cmd == "CMBL":  # In cmblock
                        # CMBLOCK,Cname,Entity,NUMITEMS,,,,,KOPT
                        numitems = int(line.split(",")[3])
                        _block_count_target = (
                            numitems // 8 + 1 if numitems % 8 != 0 else numitems // 8
                        )
                        self._block_count_target = (
                            _block_count_target + 2
                        )  # because the cmd line and option line.

                self._block_current_cmd = cmd
                self.start_non_interactive()

            if self._in_block and cmd not in self._non_interactive_commands:
                self.store_run_command(original_line)
            else:
                self.store_run_command(line)

        elif self.use_function_names:
            self.store_command(command, parameters)
        else:
            self.store_run_command(line)

    def start_function(self, func_name):
        self._functions.append(func_name)
        self.store_empty_line()
        self.store_empty_line()
        self._infunction = True
        spacing = " " * (len(func_name) + 5)
        line = "def %s(%s," % (
            func_name,
            ", ".join(["ARG%d=''" % i for i in range(1, 7)]),
        )
        line += "%s%s," % (spacing, ", ".join(["ARG%d=''" % i for i in range(7, 13)]))
        line += "%s%s):" % (spacing, ", ".join(["ARG%d=''" % i for i in range(13, 19)]))
        self.lines.append(line)
        self.indent = self.indent + "    "

    def store_under_scored_run_command(self, command):
        self.store_run_command(command, run_underscored=True)

    def store_run_command(self, command, run_underscored=False):
        """Stores pyansys.ANSYS command that cannot be broken down
        into a function and parameters.
        """
        if run_underscored:
            underscore = "_"
        else:
            underscore = ""

        if self._infunction and "ARG" in command:
            args = []
            for i in range(1, 19):
                arg = "ARG%d" % i
                c = 0
                if arg in command:
                    command = command.replace(arg, "{%d:s}" % c)
                    args.append(arg)
                    c += 1

            line = '%s%s.%srun("%s".format(%s))' % (
                self.indent,
                self.obj_name,
                underscore,
                command,
                ", ".join(args),
            )

        elif self.comment:
            line = '%s%s.%srun("%s")  # %s' % (
                self.indent,
                self.obj_name,
                underscore,
                command,
                self.comment,
            )
        else:
            line = '%s%s.%srun("%s")' % (
                self.indent,
                self.obj_name,
                underscore,
                command,
            )
        self.lines.append(line)

    def store_comment(self):
        """Stores a line containing only a comment"""
        line = f"{self.indent}# {self.comment}"
        self.lines.append(line)

    def store_empty_line(self):
        """Stores an empty line"""
        self.lines.append("")

    def store_command(self, function, parameters):
        """Stores a valid pyansys function with parameters"""
        parsed_parameters = []
        for parameter in parameters:
            parameter = parameter.strip()
            if is_float(parameter):
                parsed_parameters.append(parameter)
            elif "ARG" in parameter and self._infunction:
                parsed_parameters.append("%s" % parameter)
            else:
                # Removing strings '' and "" because they are going to be added by the converter module.
                if parameter.startswith("'") and parameter.endswith("'"):
                    parameter = parameter[1:-1]
                if parameter.startswith('"') and parameter.endswith('"'):
                    parameter = parameter[1:-1]
                parsed_parameters.append(f'"{parameter}"')

        parameter_str = ", ".join(parsed_parameters)
        if self.comment:
            line = "%s%s.%s(%s)  # %s" % (
                self.indent,
                self.obj_name,
                function,
                parameter_str,
                self.comment,
            )
        else:
            line = "%s%s.%s(%s)" % (self.indent, self.obj_name, function, parameter_str)

        self.lines.append(line)

    def start_non_interactive(self):
        self._non_interactive_level += 1
        if self.non_interactive:
            return
        line = f"{self.indent}with {self.obj_name}.non_interactive:"
        self.lines.append(line)
        self.non_interactive = True
        self.indent = self.indent + "    "

    def end_non_interactive(self):
        self._non_interactive_level -= 1
        if self._non_interactive_level == 0:
            self.non_interactive = False
            self.indent = self.indent[4:]

    def output_to_file(self, line):
        """Return if an APDL line is redirecting to a file."""
        if line[:4].upper() == "/OUT":
            # We are redirecting the output to somewhere, probably a file.
            # Because of the problem with the ansys output, we need to execute
            # this in non_interactive mode.
            output_cmd = line.strip().upper().split(",")
            if len(output_cmd) > 1:
                opt1 = output_cmd[1].strip().upper()
                if opt1 != "TERM":
                    # A file is supplied.
                    return True

        if (
            line[:4].upper() == "*CFO"
        ):  # any([each[0:4] in '*CFOPEN' for each in dir(Commands)])
            # We might not need going into interactive mode for *CFOPEN/*CFCLOSE
            return True

        return False

    def output_to_default(self, line):
        if line[:4].upper() == "/OUT":
            # We are redirecting the output to somewhere, probably a file.
            # Because of the problem with the ansys output, we need to execute
            # this in non_interactive mode.
            output_cmd = line.strip().upper().split(",")
            if len(output_cmd) == 1:
                return True
            elif len(output_cmd) > 1:
                opt1 = output_cmd[1].strip().upper()
                if opt1 == "TERM":
                    # A file is supplied.
                    return True
        if line[:4].upper() in "*CFCLOSE":
            # We might not need going into interactive mode for *CFOPEN/*CFCLOSE
            return True

        return False
