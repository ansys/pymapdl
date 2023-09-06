"""Test ansys.mapdl.solution.Solution"""


def time_step_size(mapdl):
    assert isinstance(mapdl.solution.time_step_size, float)


def test_n_cmls(mapdl):
    assert isinstance(mapdl.solution.n_cmls, float)


def test_n_cmss(mapdl):
    assert isinstance(mapdl.solution.n_cmss, float)


def test_n_eqit(mapdl):
    assert isinstance(mapdl.solution.n_eqit, float)


def test_n_cmit(mapdl):
    assert isinstance(mapdl.solution.n_cmit, float)


def test_converged(mapdl):
    assert isinstance(mapdl.solution.converged, bool)


def test_mx_dof(mapdl):
    assert isinstance(mapdl.solution.mx_dof, float)


def test_res_frq(mapdl):
    assert isinstance(mapdl.solution.res_frq, float)


def test_res_eig(mapdl):
    assert isinstance(mapdl.solution.res_eig, float)


def test_decent_parm(mapdl):
    assert isinstance(mapdl.solution.decent_parm, float)


def test_force_cnv(mapdl):
    assert isinstance(mapdl.solution.force_cnv, float)


def test_moment_cnv(mapdl):
    assert isinstance(mapdl.solution.moment_cnv, float)


def test_heat_flow_cnv(mapdl):
    assert isinstance(mapdl.solution.heat_flow_cnv, float)


def test_magnetic_flux_cnv(mapdl):
    assert isinstance(mapdl.solution.magnetic_flux_cnv, float)


def test_current_segment_cnv(mapdl):
    assert isinstance(mapdl.solution.current_segment_cnv, float)


def test_current_cnv(mapdl):
    assert isinstance(mapdl.solution.current_cnv, float)


def test_fluid_flow_cnv(mapdl):
    assert isinstance(mapdl.solution.fluid_flow_cnv, float)


def test_displacement_cnv(mapdl):
    assert isinstance(mapdl.solution.displacement_cnv, float)


def test_rotation_cnv(mapdl):
    assert isinstance(mapdl.solution.rotation_cnv, float)


def test_temperature_cnv(mapdl):
    assert isinstance(mapdl.solution.temperature_cnv, float)


def test_vector_cnv(mapdl):
    assert isinstance(mapdl.solution.vector_cnv, float)


def test_smcv(mapdl):
    assert isinstance(mapdl.solution.smcv, float)


def test_voltage_conv(mapdl):
    assert isinstance(mapdl.solution.voltage_conv, float)


def test_pressure_conv(mapdl):
    assert isinstance(mapdl.solution.pressure_conv, float)


def test_velocity_conv(mapdl):
    assert isinstance(mapdl.solution.velocity_conv, float)


def test_mx_creep_rat(mapdl):
    assert isinstance(mapdl.solution.mx_creep_rat, float)


def test_mx_plastic_inc(mapdl):
    assert isinstance(mapdl.solution.mx_plastic_inc, float)


def test_n_cg_iter(mapdl):
    assert isinstance(mapdl.solution.n_cg_iter, float)


def test_solution_call(mapdl):
    mapdl.finish()
    output = mapdl.solution()
    assert "MAPDL SOLUTION ROUTINE" in output or "ANSYS SOLUTION ROUTINE" in output
