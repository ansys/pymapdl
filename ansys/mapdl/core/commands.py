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

try:
    import pandas
    HAS_PANDAS = True

except ImportError:
    HAS_PANDAS = False


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
    __CMDS = {'DLIST': 'CURRENTLY SELECTED DOF SET'}
    _ALLOWED_CMD_TO_DF = list(__CMDS.keys())

    PAGE_PROPERTIES = {
        'interactive lines per page' : 20,
        'interactive characters per line': 256,
        'file output lines per page':  56,
        'file output characters per line': 140
        }

    def __new__(cls, content, cmd=None, mapdl=None):
        obj = super().__new__(cls, content, cmd=cmd)
        short_cmd = cmd.split(',')[0].strip()
        if short_cmd not in cls._ALLOWED_CMD_TO_DF:
            raise ValueError(f"The command '{short_cmd}' cannot have an array or Pandas DataFrame output.")

        if isinstance(mapdl, Commands):  # _MapdlCore gives circular import.
            obj._mapdl = mapdl
        else:
            obj._mapdl = None

        return obj

    @property
    def _has_pandas(self):
        return HAS_PANDAS

    @property
    def interactive_lines_per_page(self):
        return self._get_format(0)

    @interactive_lines_per_page.setter
    def interactive_lines_per_page(self, number):
        self._set_format(0, number)

    @property
    def interactive_chars_per_line(self):
        return self._get_format(1)

    @interactive_chars_per_line.setter
    def interactive_chars_per_line(self, number):
        self._set_format(1, number)

    @property
    def file_output_lines_per_page(self):
        return self._get_format(2)

    @file_output_lines_per_page.setter
    def file_output_lines_per_page(self, number):
        self._set_format(2, number)

    @property
    def file_ouptut_chars_per_line(self):
        return self._get_format(3)

    @file_ouptut_chars_per_line.setter
    def file_ouptut_chars_per_line(self, number):
        self._set_format(3, number)

    def _get_format(self, id):
        dd = self.PAGE_PROPERTIES
        key = list(dd.keys())[id]

        if self._mapdl:
            line = self._mapdl.page('STAT').splitlines()[id]
            num = int(line.split('=')[1].strip())
            dd[key] = num # updating dict
            return num
        else:
            return dd[key]

    def _set_format(self, id, value):
        dd = self.PAGE_PROPERTIES
        key = list(dd.keys())[id]
        try:
            value = int(value)
        except ValueError:
            raise ValueError("Value should be convertible to 'int'.")

        if self._mapdl: # Updating mapdl
            args = [0, 0, 0, 0]
            args[id] = value
            self._mapdl.page(*args)
            dd[key] = value

        dd[key] = value
        return dd[key]

    def parse_dataframe(self):
        return self._parse_to_dataframe()

    def _parse_to_dataframe(self):
        if HAS_PANDAS:
            raise NotImplementedError
        else:
            return None

    def parse_array(self):
        return self._parse_array()

    def _parse_array(self):
        output = self.__str__()

    def _get_pages(self):
        output = self.__str__().splitlines()[2:]
        N = self.file_output_lines_per_page-2
        # Omitting headers
        if '*****ANSYS VERIFICATION RUN ONLY*****' in self.__str__():
            start = 4
        else:
            start = 2  # Omitting header
        return (output[each:each+N][start:] for each in range(0, len(output), N))

    def _get_labels(self):
        output = self.__str__()
        identifier = self.__CMDS[self.cmd]
        top_output = '\n'.join(output.splitlines()[:10]).splitlines()

        if identifier in top_output: # getting header line:
            # There is a defined header
            ind = [ind for ind, each in enumerate(top_output) if identifier in each][0]
            line = top_output[ind]
            return line.split('=')[1].split()
        else:
            # Assuming the first line is the header:
            return top_output[0].split()

    def _get_header(self):
        return 'NODE  LABEL     REAL           IMAG'.split()

    def _get_table(self):
        header = self._get_header()
        table = []
        for each_page in self._pages():
            # find labels:
            ind = [ind for ind, each in enumerate(each_page) if each.split() == header]
            if not ind:
                ind = 1
            else:
                ind = ind[0]+1
            table.extend(each_page[ind:])

        return table

    def _get_dataframe(self):
        table = self._get_table()
        headers = self._get_header()
        
        return pandas.DataFrame(data=table, columns=headers)
    
    
    
    
    
    
CMD_CONFIGURATION = {
    'DLIST':{
        'header': 2,
        
    }
}