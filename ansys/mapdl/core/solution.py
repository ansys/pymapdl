import weakref
from ansys.mapdl.core.mapdl import _MapdlCore


class Solution():
    """Collection of parameters specific to the solution.

    Useful for checking the status of a solve after running
    ``mapdl.solve()`` and determining if it converged, the number of
    iterations to converge, etc.

    Examples
    --------
    Check if a solution has converged.

    >>> mapdl.solution.converged
    True

    Get the cumulative number of iterations.

    >>> mapdl.solution.n_cmit
    1.0
    """

    def __init__(self, mapdl):
        if not isinstance(mapdl, _MapdlCore):
            raise TypeError('Must be implemented from MAPDL class')
        self._mapdl_weakref = weakref.ref(mapdl)

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()

    def _set_log_level(self, level):
        self._mapdl.set_log_level(level)

    @property
    def _log(self):
        return self._mapdl._log

    @property
    def time_step_size(self):
        """Time step size.

        Examples
        --------
        >>> mapdl.solution.time_step_size
        1.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'DTIME')

    @property
    def n_cmls(self):
        """Cumulative number of load steps.

        Examples
        --------
        >>> mapdl.solution.n_cmls
        1.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'NCMLS')

    @property
    def n_cmss(self):
        """Number of substeps. NOTE: Used only for static and transient analyses.

        Examples
        --------
        >>> mapdl.solution.n_cmss
        1.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'NCMSS')

    @property
    def n_eqit(self):
        """Number of equilibrium iterations.

        Examples
        --------
        >>> mapdl.solution.n_eqit
        1.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'EQIT')

    @property
    def n_cmit(self):
        """Cumulative number of iterations.

        Examples
        --------
        >>> mapdl.solution.n_cmit
        1.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'NCMIT')

    @property
    def converged(self):
        """Convergence indicator.  ``True`` when converged.

        Examples
        --------
        >>> mapdl.solution.converged
        True
        """
        return bool(self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'CNVG'))

    @property
    def mx_dof(self):
        """Maximum degree of freedom value.

        Examples
        --------
        >>> mapdl.solution.mxdvl
        -0.00020707416808476303
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'MXDVL')

    @property
    def res_frq(self):
        """Response frequency for 2nd order systems.

        Examples
        --------
        >>> mapdl.solution.resfrq
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'RESFRQ')

    @property
    def res_eig(self):
        """Response eigenvalue for 1st order systems.

        Examples
        --------
        >>> mapdl.solution.reseig
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'RESEIG')

    @property
    def decent_parm(self):
        """Descent parameter.

        Examples
        --------
        >>> mapdl.solution.dsprm
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'DSPRM')

    @property
    def force_cnv(self):
        """Force convergence value.

        Examples
        --------
        >>> mapdl.solution.focv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'FOCV')

    @property
    def moment_cnv(self):
        """Moment convergence value.

        Examples
        --------
        >>> mapdl.solution.mocv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'MOCV')

    @property
    def heat_flow_cnv(self):
        """Heat flow convergence value.

        Examples
        --------
        >>> mapdl.solution.hfcv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'HFCV')

    @property
    def magnetic_flux_cnv(self):
        """Magnetic flux convergence value.

        Examples
        --------
        >>> mapdl.solution.mfcv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'MFCV')

    @property
    def current_segment_cnv(self):
        """Current segment convergence value.

        Examples
        --------
        >>> mapdl.solution.cscv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'CSCV')

    @property
    def current_cnv(self):
        """Current convergence value.

        Examples
        --------
        >>> mapdl.solution.cucv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'CUCV')

    @property
    def fluid_flow_cnv(self):
        """Fluid flow convergence value.

        Examples
        --------
        >>> mapdl.solution.ffcv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'FFCV')

    @property
    def displacement_cnv(self):
        """Displacement convergence value.

        Examples
        --------
        >>> mapdl.solution.dicv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'DICV')

    @property
    def rotation_cnv(self):
        """Rotation convergence value.

        Examples
        --------
        >>> mapdl.solution.rocv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'ROCV')

    @property
    def temperature_cnv(self):
        """Temperature convergence value.

        Examples
        --------
        >>> mapdl.solution.tecv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'TECV')

    @property
    def vector_cnv(self):
        """Vector magnetic potential convergence value.

        Examples
        --------
        >>> mapdl.solution.vmcv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'VMCV')

    @property
    def smcv(self):
        """Scalar magnetic potential convergence value.

        Examples
        --------
        >>> mapdl.solution.smcv
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'SMCV')

    @property
    def voltage_conv(self):
        """Voltage convergence value.

        Examples
        --------
        >>> mapdl.solution.voltage_convergence
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'VOCV')

    @property
    def pressure_conv(self):
        """Pressure convergence value."""
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'PRCV')

    @property
    def velocity_conv(self):
        """Velocity convergence value."""
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'VECV')

    @property
    def mx_creep_rat(self):
        """Maximum creep ratio.

        Examples
        --------
        >>> mapdl.solution.mx_creep_rat
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'CRPRAT')

    @property
    def mx_plastic_inc(self):
        """Maximum plastic strain increment.

        Examples
        --------
        >>> mapdl.solution.mx_plastic_inc
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'PSINC')

    @property
    def n_cg_iter(self):
        """Number of iterations in the PCG and symmetric JCG (non-complex version) solvers.

        Examples
        --------
        >>> mapdl.solution.n_cg_iter
        0.0
        """
        return self._mapdl.get_value('ACTIVE', 0, 'SOLU', 'CGITER')
