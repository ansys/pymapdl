from ._commands import (
    hidden,
    session,
    database,
    preproc,
    aux15_,
    map_cmd,
    aux2_,
    aux3_,
    aux12_,
    reduced,
    apdl,
    post26_,
    solution,
    post1_,
    graphics_,
    display_,
    conn,
    misc,
    inq_func
)

import numpy as np

try:
    import pandas as pd
    HAS_PANDAS = True

except ImportError:
    HAS_PANDAS = False

MSG_NOT_PANDAS = "'Pandas' is not installed or could not be found.\nHence this command is not applicable."

# Identify where the data start in the output
GROUP_DATA_START = ['NODE', 'ELEM']

# Allowed commands to get output as array or dataframe.
# In theory (from 'paprnt.F' and 'post1.F'), these commands
# should follow the same format.
CMD_LISTING = [
    'PRIN',
    'NLIN',
    'PRNS',
    'PRES',
    'PRET',
    'PRVE',
    'PRRS',
    'PRPA',
    'PRSE',
    'PRIT',
    'PRER',
    'PRDI',
    'PREF',
    'PRNL',
    'PRRF',
    'PRST',
    'STAT',
    'PRSS',
    'PRGS',
    'PRJS',
    'SWLI',
    'PROR',
    'PRCI',
    'PREN',
    'PRNM',
    'PRXF'
]

# Formatting dataframe output.
COLUMNS_INT = ['NODE', 'ELEM', 'MAT', 'TYP', 'REL', 'ESY', 'SEC']
COLUMNS_STR = ['LABEL']
COLUMNS_TO_NOT_BE_FORMATTED = ['NODES']

COLUMNS_NOT_FLOAT = COLUMNS_INT + COLUMNS_STR + COLUMNS_TO_NOT_BE_FORMATTED

CMDS_PRINT_LIST = [
    'DLIST', 'NLIST', 'ELIST', 'PRNSOL', 'PRENERGY', 'PRORB',
    'PRCINT', 'PRESOL', 'PRJSOL', 'PRNLD', 'PRNSOL', 'PRRFOR',
    'PRRSOL', 'PRVECT', 'PRETAB', 'PRERR', 'PRITER',
    'NLDPOST', 'PRAS', 'PRFAR', 'PRMC', 'PRNEAR'
    ]

SUPPORTED_PRINT_CMDS = [
    'DLIST', 'NLIST', 'ELIST', 'PRNSOL', 'PRESOL', 'PRRSOL'
]


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

class InqFunctions(
    inq_func.inq_function
):
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
    InqFunctions
):

    """Wrapped MAPDL commands"""


def CommandFactory(output, cmd):
    pass


class CommandOutput(str):
    """
    Custom string subclass for handling the commands output.

    This class add two method to track the cmd which generated this output.
    * ``cmd`` - The MAPDL command which generated the output.
    * ``command`` - The full command line (with arguments) which generated the output.

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
        return self._cmd.split(',')[0]

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
    """
    Custom class for handling the commands whose output is sensible to be converted to
    a list of lists, a Numpy array or a Pandas DataFrame.

    This class is a subclass of ``CommandOutput``.
    """
    # def __new__(cls, content, cmd=None):
    #     obj = super().__new__(cls, content, cmd=cmd)
    #     return obj

    def _is_data_start(self, line, magicword=None):
        """Check if line is the start of a data group."""
        if not magicword:
            magicword = GROUP_DATA_START

        # Checking if we are supplying a custom start function.
        if self.custom_data_start(line) is not None:
            return self.custom_data_start(line)

        if line.split():
            if line.split()[0] in magicword or self.custom_data_start(line):
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
    def _is_empty_line(each):
        if each.split():
            return False
        else:
            return True

    def _get_body(self, trail_header=None):
        """Get command body text.

        It removes the Maximum absolute values tail part and makes sure there is separation between columns"""
        body = self.__str__().splitlines()

        if not trail_header:
            trail_header = ['MAXIMUM ABSOLUTE VALUES', 'TOTAL VALUES']

        if not isinstance(trail_header, list):
            trail_header = list(trail_header)

        # Removing parts matching trail_header
        for each_trail_header in trail_header:
            if each_trail_header in self.__str__():
                # starting to check from the bottom.
                for i in range(len(body)-1, -1, -1):
                    if each_trail_header in body[i]:
                        break
                body = body[:i]
        return body

    def _get_data_group_indexes(self, body, magicword=None):
        """Return the indexes of the start and end of the data groups."""

        if '*****ANSYS VERIFICATION RUN ONLY*****' in self.__str__():
            shift = 2
        else:
            shift = 0

        # Getting pairs of starting end
        start_idxs = [ind for ind, each in enumerate(body) if self._is_data_start(each, magicword=magicword)]
        end_idxs = [ind - shift for ind, each in enumerate(body) if self._is_empty_line(each)]

        indexes = [*start_idxs, *end_idxs]
        indexes.sort()

        ends = [indexes[indexes.index(each)+1] for each in start_idxs[:-1]]
        ends.append(len(body))

        return zip(start_idxs, ends)

    def _get_data_groups(self, magicword=None, trail_header=None):
        """Get raw data groups"""
        body = self._get_body(trail_header=trail_header)

        data = []
        for start, end in self._get_data_group_indexes(body, magicword=magicword):
            data.extend(body[start+1:end])

        # removing empty lines
        data = [each for each in data if each]

        return data

    def get_columns(self):
        """
        Get the column names for the dataframe.

        Returns
        -------
        List of strings

        """
        body = self._get_body()
        pairs = list(self._get_data_group_indexes(body))
        return body[pairs[0][0]].split()

    def _command_checker(func):
        """Wrapper to check cmd input is allowed."""
        def func_wrapper(self, *args, **kwargs):
            short_cmd = self._cmd.split(',')[0][0:4]
            if short_cmd not in CMD_LISTING:
                raise ValueError(f"The command '{self._cmd.split(',')[0]}' is not allowed.")
            else:
                return func(self, *args, **kwargs)
        return func_wrapper

    def _requires_pandas(func):
        """Wrapper that check ``HAS_PANDAS``, if not, it will raise an exception."""
        def func_wrapper(self, *args, **kwargs):
            if HAS_PANDAS:
                return func(self, *args, **kwargs)
            else:
                raise ModuleNotFoundError(MSG_NOT_PANDAS)
    @_command_checker
    def to_lists(self):
        data = self._get_data_groups()
        return [each.split() for each in data]

    @_command_checker
    def to_numpy(self):
        return np.array(self.to_lists(), dtype=float)

    @_command_checker
    def to_dataframe(self):
        return pd.DataFrame(data=self.to_numpy(), columns=self.get_columns())

    # ############################################################
    ## NOTES
    # The key format files are:
    # - rptfmt.F
    # - rptlb4.F
    # - rptlb8.F
    #
    # def get_lists(self, magicword=None):
    #     """
    #     Get underlying command data as list of list.

    #     This function assumes that the data groups in each page starts with a header which starts
    #     with the magic word and ends with the next empty line.

    #     Parameters
    #     ----------
    #     magicword : str, optional
    #         Specify a magic word to identify the data group start. By default None, which translate
    #         later to ['NODE', 'ELEMENT'].

    #     Returns
    #     -------
    #     list of list

    #     """
    #     data = self._get_raw_list_of_lists()

    #     if self._is_data_wrapper(data):
    #         data = self._unwrap_data(data)

    #     return data

    # def get_columns(self):
    #     """
    #     Get the column names for the dataframe.

    #     Returns
    #     -------
    #     List of strings

    #     """
    #     body = self._get_body()
    #     pairs = list(self._get_data_group_indexes(body))
    #     return body[pairs[0][0]].split()

    # def get_array(self):
    #     """
    #     Get Numpy array of the underlying command data.

    #     If the command data has text (for example ``DLIST`` which contains the labels
    #     ``UX``, ``TEMP``, etc), it is recommended to get this data as dataframe
    #     (``get_dataframe``) or as list of list (``get_lists``).

    #     Returns
    #     -------
    #     numpy.ndarray
    #         This command attemp to return an array of floats, but if there is non-float data,
    #         it will return a generic array of objects.

    #     """
    #     try:
    #         return np.array(self.get_lists(), dtype=float)
    #     except ValueError:
    #         return np.array(self.get_lists())

    # def get_dataframe(self):
    #     """
    #     Get Pandas DataFrame of the underlying command data.

    #     It requires to have Pandas installed. In case you don't, it will return ``None``
    #     but it won't raise an error.

    #     Returns
    #     -------
    #     Pandas.DataFrame

    #     """
    #     if not self._has_pandas:
    #         return None

    #     data = self.get_lists()
    #     columns = self.get_columns()

    #     # the data is wrapped to another line
    #     if len(columns) != len(data[0]):
    #         data = self._fit_columns(data, columns)

    #     df = pd.DataFrame(data=data, columns=columns)

    #     return self._format_df(df)

    # def _fit_columns(self, data, columns):
    #     col_len = len(columns)
    #     # the last column will encompass all the exceeding data
    #     def group(each, col_len):
    #         col_len_ = col_len-1
    #         return *each[:col_len_], each[col_len_:]
    #     return [group(each, col_len) for each in data]

    # def _is_data_wrapper(self, data):
    #     return len(set([len(each) for each in data])) != 1

    # def _unwrap_data(self, data):
    #     """Unwrap data by assuming there is a pattern"""
    #     unique_lengths = set([len(each) for each in data])
    #     if len(unique_lengths) != 2:
    #         raise ValueError("The data presents more than 2 line lengths. This is unexpected.")

    #     line_max = max(unique_lengths)
    #     line_min = min(unique_lengths)

    #     skip_next_line = False

    #     data_ = []
    #     for ind, each_line in enumerate(data[:-1]):
    #         if skip_next_line:
    #             skip_next_line = not skip_next_line

    #         next_line = data[ind+1]
    #         if len(each_line) == line_max and len(next_line) == line_min:
    #             line = each_line.copy()
    #             line.extend(next_line)
    #             skip_next_line = True

    #         data_.append(line)

    #     return data_
