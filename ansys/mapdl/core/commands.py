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

    def __class__(self, seq):
        # __new__ needs type and the args.
        return self.__new__(type(self), seq, self._cmd)

    # Overwritting the string methods.
    # I used the UserString API.
    def __getitem__(self, index):
        return self.__class__(super().__getitem__(index))

    def __add__(self, other):
        return self.__class__(super().__add__(other))

    def __mul__(self, n):
        return self.__class__(super().__mul__(n))

    __rmul__ = __mul__

    def __mod__(self, args):
        return self.__class__(super().__mod__(args))

    def __rmod__(self, template):
        return self.__class__(str(template).__rmod__(self))

    # the following methods are overwritten and defined in alphabetical order:
    def capitalize(self):
        return self.__class__(super().capitalize())

    def casefold(self):
        return self.__class__(super().casefold())

    def center(self, width, *args):
        return self.__class__(super().center(width, *args))

    def removeprefix(self, prefix, /):
        return self.__class__(super().removeprefix(prefix))

    def removesuffix(self, suffix, /):
        return self.__class__(super().removesuffix(suffix))

    def expandtabs(self, tabsize=8):
        return self.__class__(super().expandtabs(tabsize))

    def join(self, seq):
        return self.__class__(super().join(seq))

    def ljust(self, width, *args):
        return self.__class__(super().ljust(width, *args))

    def lower(self):
        return self.__class__(super().lower())

    def lstrip(self, chars=None):
        return self.__class__(super().lstrip(chars))

    maketrans = str.maketrans

    def replace(self, old, new, maxsplit=-1):
        return self.__class__(super().replace(old, new, maxsplit))

    def rjust(self, width, *args):
        return self.__class__(super().rjust(width, *args))

    def rstrip(self, chars=None):
        return self.__class__(super().rstrip(chars))

    def strip(self, chars=None):
        return self.__class__(super().strip(chars))

    def swapcase(self):
        return self.__class__(super().swapcase())

    def title(self):
        return self.__class__(super().title())

    def translate(self, *args):
        return self.__class__(super().translate(*args))

    def upper(self):
        return self.__class__(super().upper())

    def zfill(self, width):
        return self.__class__(super().zfill(width))

    def splitlines(self, keepends=False):
        return [self.__class__(each) for each in super().splitlines(keepends)]

    def rpartition(self, sep):
        return [self.__class__(each) for each in super().rpartition(sep)]

    def rstrip(self, chars=None):
        return self.__class__(super().rstrip(chars))

    def split(self, sep=None, maxsplit=-1):
        return [self.__class__(each) for each in super().split(sep, maxsplit)]

    def rsplit(self, sep=None, maxsplit=-1):
        return [self.__class__(each) for each in super().rsplit(sep, maxsplit)]

    def format(self, /, *args, **kwds):
        return self.__class__(super().format(*args, **kwds))

    def format_map(self, mapping):
        return self.__class__(super().format_map(mapping))

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, cmd):
        """Forbidden to change the value of ``cmd``."""
        pass

class CommandOutput2(str):

    ## References:
    # - https://stackoverflow.com/questions/7255655/how-to-subclass-str-in-python
    # - https://docs.python.org/3/library/collections.html#userstring-objects
    # - Source code of UserString

    def __new__(cls, content, cmd=None):
        obj = super().__new__(cls, content)
        obj._cmd = cmd
        return obj

    def __class__(self, seq):
        # __new__ needs type and the args.
        return self.__new__(type(self), seq, self._cmd)

    def __getattribute__(self, name):
        if name in dir(str): # only handle str methods here
            def method(self, *args, **kwargs):
                value = getattr(super(), name)(*args, **kwargs)
                # not every string method returns a str:
                if isinstance(value, str):
                    return type(self)(value)
                elif isinstance(value, list):
                    return [type(self)(i) for i in value]
                elif isinstance(value, tuple):
                    return tuple(type(self)(i) for i in value)
                else: # dict, bool, or int
                    return value
            return method.__get__(self) # bound method
        else: # delegate to parent
            return super().__getattribute__(name)