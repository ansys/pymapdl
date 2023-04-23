from functools import wraps
import re

import numpy as np

from ._commands import (
    apdl,
    aux2_,
    aux3_,
    aux12_,
    aux15_,
    conn,
    database,
    display_,
    graphics_,
    hidden,
    inq_func,
    map_cmd,
    misc,
    post1_,
    post26_,
    preproc,
    reduced,
    session,
    solution,
)

# compiled regular expressions used for parsing tablular outputs
REG_LETTERS = re.compile(r"[a-df-zA-DF-Z]+")  # all except E or e
REG_FLOAT_INT = re.compile(
    r"[+-]?[0-9]*[.]?[0-9]*[Ee]?[+-]?[0-9]+|\s[0-9]+\s"
)  # match number groups
BC_REGREP = re.compile(
    r"^\s*([0-9]+)\s*([A-Za-z]+)\s*([0-9]*[.]?[0-9]+)\s+([0-9]*[.]?[0-9]+)"
)

MSG_NOT_PANDAS = """'Pandas' is not installed or could not be found.
Hence this command is not applicable.

You can install it using:
pip install pandas
"""

MSG_BCLISTINGOUTPUT_TO_ARRAY = """This command has strings values in some of its columns (such 'UX', 'FX', 'UY', 'TEMP', etc),
so it cannot be converted to Numpy Array.

Please use 'to_list' or 'to_dataframe' instead."""


# Identify where the data start in the output
GROUP_DATA_START = ["NODE", "ELEM"]

# Allowed commands to get output as array or dataframe.
# In theory, these commands should follow the same format.
# Some of them are not documented (already deprecated?)
# So they are not in the Mapdl class,
# so they won't be wrapped.
CMD_RESULT_LISTING = [
    "NLIN",  # not documented
    "PRCI",
    "PRDI",  # Not documented.
    "PREF",  # Not documented.
    "PREN",
    "PRER",
    "PRES",
    "PRET",
    "PRGS",  # Not documented.
    "PRIN",
    "PRIT",
    "PRJS",
    "PRNL",
    "PRNM",  # Not documented.
    "PRNS",
    "PROR",
    "PRPA",
    "PRRF",
    "PRRS",
    "PRSE",
    "PRSS",  # Not documented.
    "PRST",  # Not documented.
    "PRVE",
    "PRXF",  # Not documented.
    "SWLI",
]

CMD_BC_LISTING = ["FLIS", "DLIS"]

CMD_ENTITY_LISTING = [
    "NLIS",
    # "ELIS", # To be implemented later
    # "KLIS",
    # "LLIS",
    # "ALIS",
    # "VLIS",
]

CMD_LISTING = []
CMD_LISTING.extend(CMD_ENTITY_LISTING)
CMD_LISTING.extend(CMD_RESULT_LISTING)

# Adding empty lines to match current format.
CMD_DOCSTRING_INJECTION = r"""
Returns
-------

str
    Str object with the command console output.

    This object also has the extra methods:
    :meth:`to_list() <ansys.mapdl.core.commands.CommandListingOutput.to_list>`,
    :meth:`to_array() <ansys.mapdl.core.commands.CommandListingOutput.to_array>` (only on listing commands) and
    :meth:`to_dataframe() <ansys.mapdl.core.commands.CommandListingOutput.to_dataframe>` (only if Pandas is installed).
    |bl|
    **NOTE**: If you use these methods, you might
    obtain a lower precision than using :class:`Mesh <ansys.mapdl.core.mesh_grpc.MeshGrpc>` methods.
    |bl|
    For more information visit :ref:`user_guide_postprocessing`.

"""

XSEL_DOCSTRING_INJECTION = r"""
Returns
-------

np.ndarray
    Numpy array with the ids of the selected entities.

    For more information visit :ref:`user_guide_postprocessing`.

"""


CMD_XSEL = [
    "NSEL",
    "ESEL",
    "KSEL",
    "LSEL",
    "ASEL",
    "VSEL",
]


def get_indentation(indentation_regx, docstring):
    return re.findall(indentation_regx, docstring, flags=re.DOTALL | re.IGNORECASE)[0][
        0
    ]


def indent_text(indentation, docstring_injection):
    return "\n".join(
        [
            indentation + each
            for each in docstring_injection.splitlines()
            if each.strip()
        ]
    )


def get_docstring_indentation(docstring):
    indentation_regx = r"\n(\s*)\n"
    return get_indentation(indentation_regx, docstring)


def get_sections(docstring):
    return [
        each.strip().lower() for each in re.findall(r"\n\s*(\S*)\n\s*-+\n", docstring)
    ]


def get_section_indentation(section_name, docstring):
    sections = get_sections(docstring)
    if section_name.lower().strip() not in sections:
        raise ValueError(
            f"This section '{section_name.lower().strip()}' does not exist in the docstring."
        )
    section_match = section_name + r"\n\s*-*"
    indent_match = r"\n(\s*)(\S)"
    indentation_regx = section_match + indent_match
    return get_indentation(indentation_regx, docstring)


def inject_before(section, indentation, indented_doc_inject, docstring):
    return re.sub(
        section + r"\n\s*-*",
        f"{indented_doc_inject.strip()}\n\n{indentation}\g<0>",
        docstring,
        flags=re.IGNORECASE,
    )


def inject_after_return_section(indented_doc_inject, docstring):
    return re.sub(
        "Returns" + r"\n\s*-*",
        f"{indented_doc_inject.strip()}\n",
        docstring,
        flags=re.IGNORECASE,
    )


def inject_docs(docstring, docstring_injection=None):
    """Inject a string in a docstring"""
    if not docstring_injection:
        docstring_injection = CMD_DOCSTRING_INJECTION

    return_header = r"Returns\n\s*-*"

    if docstring_injection.splitlines()[-2].strip() in docstring:
        # In case the docstring already has the injection.
        return docstring
    elif re.search(return_header, docstring):
        # There is a return block already, probably it should not.
        indentation = get_section_indentation("Returns", docstring)
        indented_doc_inject = indent_text(indentation, docstring_injection)
        return inject_after_return_section(indented_doc_inject, docstring)
    else:
        # There is not returns header
        # find sections
        sections = get_sections(docstring)

        if "parameters" in sections:
            ind = sections.index("parameters")
            if ind == len(sections) - 1:
                # The parameters is the last bit. Just append it.
                indentation = get_section_indentation("Parameters", docstring)
                indented_doc_inject = indent_text(indentation, docstring_injection)
                return docstring + "\n" + indented_doc_inject
            else:
                # inject it right before the section after 'parameter'
                sect_after_parameter = sections[ind + 1]
                indentation = get_section_indentation(sect_after_parameter, docstring)
                indented_doc_inject = indent_text(indentation, docstring_injection)
                return inject_before(
                    sect_after_parameter,
                    indentation,
                    indented_doc_inject,
                    docstring,
                )

        elif "notes" in sections:
            indentation = get_section_indentation("Notes", docstring)
            indented_doc_inject = indent_text(indentation, docstring_injection)
            return inject_before("Notes", indentation, indented_doc_inject, docstring)

        else:
            indentation = get_docstring_indentation(docstring)
            indented_doc_inject = indent_text(indentation, docstring_injection)
            return docstring + "\n" + indented_doc_inject


def check_valid_output(func):
    """Wrapper that check if output can be wrapped by pandas, if not, it will raise an exception."""

    @wraps(func)
    def func_wrapper(self, *args, **kwargs):
        output = self.__str__()
        if (
            "*** WARNING ***" in output or "*** ERROR ***" in output
        ):  # Error should be caught in mapdl.run.
            err_type = re.findall("\*\*\* (.*) \*\*\*", output)[0]
            msg = f"Unable to parse because of next {err_type.title()}" + "\n".join(
                output.splitlines()[-2:]
            )
            raise ValueError(msg)
        else:
            return func(self, *args, **kwargs)

    return func_wrapper


class PreprocessorCommands(
    preproc.database.Database,
    preproc.explicit_dynamics.ExplicitDynamics,
    preproc.lines.Lines,
    preproc.areas.Areas,
    preproc.nodes.Nodes,
    preproc.keypoints.KeyPoints,
    preproc.artificially_matched_layers.ArtificiallyMatchedLayers,
    preproc.booleans.Booleans,
    preproc.constraint_equations.ConstraintEquations,
    preproc.coupled_dof.CoupledDOF,
    preproc.real_constants.RealConstants,
    preproc.digitizing.Digitizing,
    preproc.element_type.ElementType,
    preproc.elements.Elements,
    preproc.hard_points.HardPoints,
    preproc.material_data_tables.MaterialDataTables,
    preproc.meshing.Meshing,
    preproc.morphing.Morphing,
    preproc.materials.Materials,
    preproc.primitives.Primitives,
    preproc.sections.Sections,
    preproc.special_purpose.SpecialPurpose,
    preproc.status.Status,
    preproc.superelements.Superelements,
    preproc.volumes.Volumes,
):
    pass


class APDLCommands(
    apdl.abbreviations.Abbreviations,
    apdl.array_param.ArrayParam,
    apdl.macro_files.MacroFiles,
    apdl.matrix_op.MatrixOP,
    apdl.parameter_definition.ParameterDefinition,
    apdl.process_controls.ProcessControls,
):
    pass


class Aux2Commands(aux2_.bin_dump.BinDump, aux2_.bin_manip.BinManip):
    pass


class Aux12Commands(
    aux12_.radiosity_solver.RadiositySolver,
    aux12_.radiation_mat.RadiationMat,
    aux12_.general_radiation.GeneralRadiation,
):
    pass


class DatabaseCommands(
    database.setup.Setup,
    database.picking.Picking,
    database.coord_sys.CoordinateSystem,
    database.selecting.Selecting,
    database.working_plane.WorkingPlane,
    database.components.Components,
):
    pass


class DisplayCommands(display_.setup.Setup):
    pass


class GraphicsCommands(
    graphics_.annotation.Annotation,
    graphics_.graphs.Graphs,
    graphics_.labeling.Labelling,
    graphics_.scaling.Scaling,
    graphics_.setup.Setup,
    graphics_.style.Style,
    graphics_.views.Views,
):
    pass


class MiscCommands(misc.misc.Misc):
    pass


class Post1Commands(
    post1_.animation.Animation,
    post1_.controls.Controls,
    post1_.element_table.ElementTable,
    post1_.failure_criteria.FailureCriteria,
    post1_.listing.Listing,
    post1_.load_case.LoadCase,
    post1_.magnetics_calc.MagneticsCalc,
    post1_.path_operations.PathOperations,
    post1_.results.Results,
    post1_.setup.Setup,
    post1_.special.Special,
    post1_.status.Status,
    post1_.surface_operations.SurfaceOperations,
    post1_.trace_points.TracePoints,
):
    pass


class Post26Commands(
    post26_.controls.Controls,
    post26_.display.Display,
    post26_.listing.Listing,
    post26_.operations.Operations,
    post26_.setup.Setup,
    post26_.special.Special,
    post26_.status.Status,
):
    pass


class ReducedCommands(
    reduced.generation.Generation,
    reduced.preparation.Preparation,
    reduced.setup.Setup,
    reduced.use_pass.UsePass,
):
    pass


class SessionCommands(
    session.files.Files,
    session.list_controls.ListControls,
    session.processor_entry.ProcessorEntry,
    session.run_controls.RunControls,
):
    pass


class SolutionCommands(
    solution.analysis_options.AnalysisOptions,
    solution.birth_and_death.BirthAndDeath,
    solution.dynamic_options.DynamicOptions,
    solution.fe_body_loads.FeBodyLoads,
    solution.fe_constraints.FeConstraints,
    solution.fe_forces.FeForces,
    solution.fe_surface_loads.FeSurfaceLoads,
    solution.gap_conditions.GapConditions,
    solution.inertia.Inertia,
    solution.load_step_operations.LoadStepOperations,
    solution.load_step_options.LoadStepOptions,
    solution.master_dof.MasterDOF,
    solution.miscellaneous_loads.MiscellaneousLoads,
    solution.multi_field_solver_convergence_controls.MultiFieldConvergenceControls,
    solution.multi_field_solver_definition_commands.MultiFieldSolverDefinitionCommands,
    solution.multi_field_solver_global_controls.MultiFieldSolverGlobalControls,
    solution.multi_field_solver_interface_mapping.MultiFieldSolverInterfaceMapping,
    solution.multi_field_solver_load_transfer.MultiFieldSolverLoadTransfer,
    solution.multi_field_solver_time_controls.MultiFieldSolverTimeControls,
    solution.nonlinear_options.NonLinearOptions,
    solution.ocean.Ocean,
    solution.radiosity.Radiosity,
    solution.rezoning.Rezoning,
    solution.solid_body_loads.SolidBodyLoads,
    solution.solid_constraints.SolidConstraints,
    solution.solid_forces.SolidForces,
    solution.solid_surface_loads.SolidSurfaceLoads,
    solution.solution_status.SolutionStatus,
    solution.spectrum_options.SpectrumOptions,
    solution.twod_to_3d_analysis.TwoDTo3DAnalysis,
):
    pass


class InqFunctions(inq_func.inq_function):
    pass


class Commands(
    APDLCommands,
    Aux2Commands,
    Aux12Commands,
    DatabaseCommands,
    DisplayCommands,
    GraphicsCommands,
    MiscCommands,
    Post1Commands,
    Post26Commands,
    PreprocessorCommands,
    ReducedCommands,
    SessionCommands,
    SolutionCommands,
    aux3_.Aux3,
    aux15_.Aux15,
    conn.Conn,
    hidden._Hidden,
    map_cmd.MapCommand,
    InqFunctions,
):

    """Wrapped MAPDL commands"""


def _requires_pandas(func):
    """Wrapper that check ``HAS_PANDAS``, if not, it will raise an exception."""

    def func_wrapper(self, *args, **kwargs):
        if HAS_PANDAS:
            return func(self, *args, **kwargs)
        else:
            raise ModuleNotFoundError(MSG_NOT_PANDAS)

    return func_wrapper


class CommandOutput(str):
    """Custom string subclass for handling the commands output.

    This class is a subclass of python :class`str`, hence it has all the methods of
    a string python object.

    Additionally it provides the following attributes:

    * :attr:`cmd() <ansys.mapdl.core.commands.CommandOutput.cmd>`
    * :attr:`command() <ansys.mapdl.core.commands.CommandOutput.command>`

    """

    ## References:
    # - https://stackoverflow.com/questions/7255655/how-to-subclass-str-in-python
    # - https://docs.python.org/3/library/collections.html#userstring-objects
    # - Source code of UserString

    def __new__(cls, content, cmd=None):
        obj = super().__new__(cls, content)
        obj._cmd = cmd
        return obj

    @property
    def cmd(self):
        """Cached original command to generate this command output."""
        return self._cmd.split(",")[0]

    @cmd.setter
    def cmd(self, cmd):
        """Not allowed to change the value of ``cmd``."""
        raise AttributeError("The `cmd` attribute cannot be set")

    @property
    def command(self):
        return self._cmd

    @command.setter
    def command(self):
        """Not allowed to change the value of ``command``."""
        pass


class CommandListingOutput(CommandOutput):
    """Allow the conversion of command output to native Python types.

    Custom class for handling the commands whose output is sensible to be converted to
    a list of lists, a Numpy array or a Pandas DataFrame.

    This class is a subclass of python :class:`str`, hence it has all the methods of
    a string python object.

    Additionally it provides the following methods:

    * :func:`to_list() <ansys.mapdl.core.commands.CommandListingOutput.to_list>`
    * :func:`to_array() <ansys.mapdl.core.commands.CommandListingOutput.to_array>`
    * :func:`to_dataframe() <ansys.mapdl.core.commands.CommandListingOutput.to_dataframe>`

    """

    def __new__(cls, content, cmd=None, magicwords=None, columns_names=None):
        obj = super().__new__(cls, content)
        obj._cmd = cmd
        obj._magicwords = magicwords
        obj._columns_names = columns_names
        return obj

    def __init__(self, *args, **kwargs):
        self._cache = None

    def _is_data_start(self, line, magicwords=None):
        """Check if line is the start of a data group."""
        if not magicwords:
            if self._magicwords:
                magicwords = self._magicwords
            else:
                magicwords = GROUP_DATA_START

        # Checking if we are supplying a custom start function.
        if self.custom_data_start(line) is not None:
            return self.custom_data_start(line)

        if line.split():
            if line.split()[0] in magicwords or self.custom_data_start(line):
                return True
        return False

    def _is_data_end(self, line):
        """Check if line is the end of a data group."""

        # Checking if we are supplying a custom start function.
        if self.custom_data_end(line) is not None:
            return self.custom_data_end(line)
        else:
            return self._is_empty(line)

    def custom_data_start(self, line):
        """Custom data start line check function.

        This function is left empty so it can be overwritten by the user.

        If modified, it should return ``True`` when the line is the start
        of a data group, otherwise it should return ``False``.
        """
        return None

    def custom_data_end(self, line):
        """Custom data end line check function.

        This function is left empty so it can be overwritten by the user.

        If modified, it should return ``True`` when the line is the end
        of a data group, otherwise it should return ``False``.
        """
        return None

    @staticmethod
    def _is_empty_line(line):
        return bool(line.split())

    def _format(self):
        """Perform some formatting (replacing mainly) in the raw text."""
        return re.sub(r"[^E](-)", " -", self.__str__())

    def _get_body(self, trail_header=None):
        """Get command body text.

        It removes the maximum absolute values tail part and makes sure there is
        separation between columns.
        """
        # Doing some formatting of the string
        body = self._format().splitlines()

        if not trail_header:
            trail_header = ["MAXIMUM ABSOLUTE VALUES", "TOTAL VALUES"]

        if not isinstance(trail_header, list):
            trail_header = list(trail_header)

        # Removing parts matching trail_header
        for each_trail_header in trail_header:
            if each_trail_header in self.__str__():
                # starting to check from the bottom.
                for i in range(len(body) - 1, -1, -1):
                    if each_trail_header in body[i]:
                        break
                body = body[:i]
        return body

    def _get_data_group_indexes(self, body, magicwords=None):
        """Return the indexes of the start and end of the data groups."""
        if "*****ANSYS VERIFICATION RUN ONLY*****" in str(self[:1000]):
            shift = 2
        else:
            shift = 0

        # Getting pairs of starting end
        start_idxs = [
            ind
            for ind, each in enumerate(body)
            if self._is_data_start(each, magicwords=magicwords)
        ]
        end_idxs = [
            ind - shift for ind, each in enumerate(body) if self._is_empty_line(each)
        ]

        indexes = [*start_idxs, *end_idxs]
        indexes.sort()

        ends = [indexes[indexes.index(each) + 1] for each in start_idxs[:-1]]
        ends.append(len(body))

        return zip(start_idxs, ends)

    def get_columns(self):
        """Get the column names for the dataframe.

        Returns
        -------
        List of strings

        """
        if self._columns_names:
            return self._columns_names

        body = self._get_body()
        pairs = list(self._get_data_group_indexes(body))
        try:
            return body[pairs[0][0]].split()
        except:
            return None

    def _parse_table(self):
        """Parse tabular command output.

        Returns
        -------
        numpy.ndarray
            Parsed tabular data from command output.

        """
        parsed_lines = []
        for line in self.splitlines():
            # exclude any line containing characters [A-Z] except for E
            if line.strip() and not REG_LETTERS.search(line):
                items = REG_FLOAT_INT.findall(line)
                if items:
                    parsed_lines.append(items)
        return np.array(parsed_lines, dtype=np.float64)

    @property
    def _parsed(self):
        """Return parsed output."""
        if self._cache is None:
            self._cache = self._parse_table()
        return self._cache

    @check_valid_output
    def to_list(self):
        """Export the command output a list or list of lists.

        Returns
        -------
        list
        """
        return self._parsed.tolist()

    def to_array(self):
        """Export the command output as a numpy array.

        Returns
        -------
        numpy.ndarray
            Numpy array of floats.
        """
        return self._parsed

    def to_dataframe(self, data=None, columns=None):
        """Export the command output as a Pandas DataFrame.

        Parameters
        ----------
        data : numpy.ndarray (structured or homogeneous), Iterable, dict, or DataFrame
            The data to be converted to the dataframe values.  Passed directly
            to the pandas.DataFrame constructor.  Dict can contain Series,
            arrays, constants, dataclass or list-like objects. If data is a
            dict, column order follows insertion-order.

        columns : Index or array-like
            Iterable with columns names.  Passed directly to the
            pandas.DataFrame constructor.  Column labels to use for resulting
            frame when data does not have them, defaulting to RangeIndex(0, 1,
            2, ..., n). If data contains column labels, will perform column
            selection instead.

        Returns
        -------
        pandas.DataFrame
            Pandas DataFrame

        Notes
        -----
        The returned dataframe has all its data converted to float
        (inheritate from :func:`to_array()
        <ansys.mapdl.core.commands.CommandListingOutput.to_array>` method).
        """
        try:
            import pandas as pd
        except ModuleNotFoundError:
            raise ModuleNotFoundError(MSG_NOT_PANDAS)

        if data is None:
            data = self.to_list()
        if not columns:
            columns = self.get_columns()

        return pd.DataFrame(data=data, columns=columns)


class BoundaryConditionsListingOutput(CommandListingOutput):
    """Allow the conversion of command output to native Python types.

    Custom class for handling the boundary condition listing commands
    whose output is sensible to be converted to a list of lists,
    or a Pandas DataFrame.

    This class is a subclass of python :class:`str`, hence it has all the methods of
    a string python object and it can be used as such.

    Additionally it provides the following methods:

    * :func:`to_list() <ansys.mapdl.core.commands.BoundaryConditionsListingOutput.to_list>`
    * :func:`to_dataframe() <ansys.mapdl.core.commands.BoundaryConditionsListingOutput.to_dataframe>`

    """

    def _parse_table(self):
        """Parse tabular command output."""
        parsed_lines = []
        for line in self.splitlines():
            # exclude any line containing characters [A-Z] except for E
            if line:
                items = BC_REGREP.findall(line)
                if items:
                    parsed_lines.append(list(items[0]))

        return parsed_lines

    @check_valid_output
    def to_list(self):
        """Export the command output a list or list of lists.

        Returns
        -------
        list
        """
        return self._parsed

    def to_array(self):
        raise ValueError(MSG_BCLISTINGOUTPUT_TO_ARRAY)

    def to_dataframe(self):
        """Convert the command output to a Pandas Dataframe.

        Returns
        -------
        pandas.DataFrame
            Pandas Dataframe

        Notes
        -----

        If present, the next columns will be converted to:

        * ``'NODE'``: int
        * ``'LABEL'``: str
        * ``'REAL'``: float
        * ``'IMAG'``: float

        """
        df = super().to_dataframe(data=self.to_list())
        if "NODE" in df.columns:
            df["NODE"] = df["NODE"].astype(np.int32, copy=False)

        if "LABEL" in df.columns:
            df["LABEL"] = df["LABEL"].astype(str, copy=False)

        if "REAL" in df.columns:
            df["REAL"] = df["REAL"].astype(np.float64, copy=False)

        if "IMAG" in df.columns:
            df["IMAG"] = df["IMAG"].astype(np.float64, copy=False)

        return df


class StringWithLiteralRepr(str):
    def __repr__(self):
        return self.__str__()
