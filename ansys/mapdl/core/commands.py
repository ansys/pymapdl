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
)

import numpy as np

try:
    import pandas as pd
    HAS_PANDAS = True

except ImportError:
    HAS_PANDAS = False


COLUMNS_INT = ['NODE', 'ELEMENT']
COLUMNS_STR = ['LABEL']
COLUMNS_NOT_FLOAT = COLUMNS_INT + COLUMNS_STR

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
):

    """Wrapped MAPDL commands"""

    pass

class CommandOutput(str):
    """
    Custom string subclass for handling the commands output.

    Main features is that this class always returns an object which is from its own class
    (it never returns a string).

    This class add two method to track the cmd which generated this output.
    * ``cmd`` - The MAPDL command which generated the output.
    * ``command`` - The full command line (with arguments) which generated the output.

    These two methods and their values are inheritate by the consequents generated objects,
    as long as you use the string-related methods in this class.

    """

    ## References:
    # - https://stackoverflow.com/questions/7255655/how-to-subclass-str-in-python
    # - https://docs.python.org/3/library/collections.html#userstring-objects
    # - Source code of UserString

    def __new__(cls, content, cmd=None):
        obj = super().__new__(cls, content)
        obj._cmd = cmd
        return obj

    def _copyobj(self, seq):
        # __new__ needs type and the args.
        return self.__new__(type(self), seq, self._cmd)

    # Overwriting the string methods.
    # I used the UserString API.
    def __getitem__(self, index):
        return self._copyobj(super().__getitem__(index))

    def __add__(self, other):
        return self._copyobj(super().__add__(other))

    def __mul__(self, n):
        return self._copyobj(super().__mul__(n))

    __rmul__ = __mul__

    def __mod__(self, args):
        return self._copyobj(super().__mod__(args))

    def __rmod__(self, template):
        return self._copyobj(str(template).__rmod__(self))

    # the following methods are overwritten and defined in alphabetical order:
    def capitalize(self):
        return self._copyobj(super().capitalize())

    def casefold(self):
        return self._copyobj(super().casefold())

    def center(self, width, *args):
        return self._copyobj(super().center(width, *args))

    def removeprefix(self, prefix):
        return self._copyobj(super().removeprefix(prefix))

    def removesuffix(self, suffix):
        return self._copyobj(super().removesuffix(suffix))

    def expandtabs(self, tabsize=8):
        return self._copyobj(super().expandtabs(tabsize))

    def join(self, seq):
        return self._copyobj(super().join(seq))

    def ljust(self, width, *args):
        return self._copyobj(super().ljust(width, *args))

    def lower(self):
        return self._copyobj(super().lower())

    def lstrip(self, chars=None):
        return self._copyobj(super().lstrip(chars))

    maketrans = str.maketrans

    def replace(self, old, new, maxsplit=-1):
        return self._copyobj(super().replace(old, new, maxsplit))

    def rjust(self, width, *args):
        return self._copyobj(super().rjust(width, *args))

    def rstrip(self, chars=None):
        return self._copyobj(super().rstrip(chars))

    def strip(self, chars=None):
        return self._copyobj(super().strip(chars))

    def swapcase(self):
        return self._copyobj(super().swapcase())

    def title(self):
        return self._copyobj(super().title())

    def translate(self, *args):
        return self._copyobj(super().translate(*args))

    def upper(self):
        return self._copyobj(super().upper())

    def zfill(self, width):
        return self._copyobj(super().zfill(width))

    def splitlines(self, keepends=False):
        return [self._copyobj(each) for each in super().splitlines(keepends)]

    def rpartition(self, sep):
        return tuple(self._copyobj(each) for each in super().rpartition(sep))

    def rstrip(self, chars=None):
        return self._copyobj(super().rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return [self._copyobj(each) for each in super().split(sep, maxsplit)]

    def rsplit(self, sep=None, maxsplit=-1):
        return [self._copyobj(each) for each in super().rsplit(sep, maxsplit)]

    def format(self, *args, **kwds):
        return self._copyobj(super().format(*args, **kwds))

    def format_map(self, mapping):
        return self._copyobj(super().format_map(mapping))

    @property
    def cmd(self):
        return self._cmd.split(',')[0]

    @cmd.setter
    def cmd(self, cmd):
        """Not allowed to change the value of ``cmd``."""
        pass

    @property
    def command(self):
        return self._cmd

    @command.setter
    def command(self):
        """Not allowed to change the value of ``command``."""
        pass


# To be deleted after first review of PR.
class CommandOutput2(str):

    ## References:
    # - https://stackoverflow.com/questions/7255655/how-to-subclass-str-in-python
    # - https://docs.python.org/3/library/collections.html#userstring-objects
    # - Source code of UserString

    def __new__(cls, content, cmd=None):
        obj = super().__new__(cls, content)
        obj._cmd = cmd
        return obj

    # def _copyobj(self, seq):
    #     # __new__ needs type and the args.
    #     # return self.__new__(type(self), seq, self._cmd)

    def __getattribute__(self, name):
        if name in dir(str) and name != '_copyobj': # only handle str methods here
            def method(self, *args, **kwargs):
                value = getattr(super(), name)(*args, **kwargs)
                # not every string method returns a str:
                if isinstance(value, str) and not isinstance(value, CommandOutput2):
                    # return type(self)(value)
                    return self.__new__(value, self._cmd)

                elif isinstance(value, list):
                    return [self.__new__(i, self._cmd) for i in value]

                elif isinstance(value, tuple):
                    return tuple(self.__new__(i, self._cmd) for i in value)
                else: # dict, bool, or int or type
                    return value
            return method.__get__(self) # bound method
        # else: # delegate to parent
        #     return super().__getattribute__(name)


class CommandOutputDataframe(CommandOutput):
    """
    Custom class for handling the commands whose output is sensible to be converted to
    a list of lists, a Numpy array or a Pandas DataFrame.

    This class adds the next useful commands (methods):
    * ``get_lists``
    * ``get_array``
    * ``get_dataframe``

    Also it adds the next functions as custom data processing helpers:
    * ``custom_data_start``
    * ``custom_data_end``

    This class is a subclass of ``CommandOutput``.
    """
    def __new__(cls, content, cmd=None):
        obj = super().__new__(cls, content, cmd=cmd)
        short_cmd = cmd.split(',')[0].strip()
        # if short_cmd not in _ALLOWED_CMD_TO_DF:
        #     raise ValueError(f"The command '{short_cmd}' cannot have an array or Pandas DataFrame output.")
        return obj

    @property
    def _has_pandas(self):
        return HAS_PANDAS

    def _is_data_start(self, line, magicword=None):
        """Check if line is the start of a data group."""
        if not magicword:
            magicword = ['NODE', 'ELEMENT']

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
    def _is_empty(each):
        if each.split():
            return False
        else:
            return True

    def _get_body(self):
        """Get command body text.

        Just remove the Maximum absolute values tail part."""
        body = self.__str__().splitlines()

        # Removing maximum part
        if 'MAXIMUM ABSOLUTE VALUES' in self.__str__():
            ind = [ind for ind, each in enumerate(
                body) if 'MAXIMUM ABSOLUTE VALUES' in each]
            body = body[:ind[0]]
        return body

    def _get_data_group_indexes(self, body, magicword=None):
        """Return the indexes of the start and end of the data groups."""

        if '*****ANSYS VERIFICATION RUN ONLY*****' in self.__str__():
            shift = 2
        else:
            shift = 0

        # Getting pairs of starting end
        start_idxs = [ind for ind, each in enumerate(body) if self._is_data_start(each, magicword=magicword)]
        end_idxs = [ind - shift for ind, each in enumerate(body) if self._is_empty(each)]

        indexes = [*start_idxs, *end_idxs]
        indexes.sort()

        ends = [indexes[indexes.index(each)+1] for each in start_idxs[:-1]]
        ends.append(len(body))

        return zip(start_idxs, ends)

    def _format_df(self, df):
        """Format the columns data to be an specific data type."""
        headers = df.columns.to_list()
        try:
            dtype_ = str
            for each in COLUMNS_STR:
                if each in headers:
                    df[each] = df[each].astype(dtype_)

            dtype_ = int
            for each in COLUMNS_INT:
                if each in headers:
                    df[each] = df[each].astype(dtype_)

            dtype_ = float
            for each in headers:
                if each not in COLUMNS_NOT_FLOAT:
                    df[each] = df[each].astype(dtype_)

        except ValueError:
            raise ValueError(f"The column '{each}' could not be converted to {dtype_}")

        return df

    def get_lists(self, magicword=None):
        """
        Get underlying command data as list of list.

        This function assumes that the data groups in each page starts with a header which starts
        with the magic word and ends with the next empty line.

        Parameters
        ----------
        magicword : str, optional
            Specify a magic word to identify the data group start. By default None, which translate
            later to ['NODE', 'ELEMENT'].

        Returns
        -------
        list of list

        """
        body = self._get_body()

        data = []
        for start, end in self._get_data_group_indexes(body, magicword=magicword):
            data.extend(body[start+1:end])

        return [each.split() for each in data if each.split()]

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

    def get_array(self):
        """
        Get Numpy array of the underlying command data.

        If the command data has text (for example ``DLIST`` which contains the labels
        ``UX``, ``TEMP``, etc), it is recommended to get this data as dataframe
        (``get_dataframe``) or as list of list (``get_lists``).

        Returns
        -------
        numpy.ndarray
            This command attemp to return an array of floats, but if there is non-float data,
            it will return a generic array of objects.

        """     
        try:
            return np.array(self.get_lists(), dtype=float)
        except ValueError:
            return np.array(self.get_lists())

    def get_dataframe(self):
        """
        Get Pandas DataFrame of the underlying command data.

        It requires to have Pandas installed. In case you don't, it will return ``None``
        but it won't raise an error.

        Returns
        -------
        Pandas.DataFrame

        """
        if not self._has_pandas:
            return None

        data = self.get_lists()
        columns = self.get_columns()

        df = pd.DataFrame(data=data, columns=columns)

        return self._format_df(df)
