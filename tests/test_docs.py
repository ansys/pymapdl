import pytest

from ansys.mapdl.core.docs import linkcode_resolve


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "ansys.mapdl.core.Information.rst",
            "http://github.com/pyansys/pymapdl/edit/main/src/ansys/mapdl/core/misc.py",
        ),
        (
            "ansys.mapdl.core.logging.Logger",
            "http://github.com/pyansys/pymapdl/edit/main/src/ansys/mapdl/core/logging.py",
        ),
        (
            "ansys.mapdl.core.solution.Solution",
            "http://github.com/pyansys/pymapdl/edit/main/src/ansys/mapdl/core/solution.py",
        ),
        (
            "ansys.mapdl.core.krylov.KrylovSolver",
            "http://github.com/pyansys/pymapdl/edit/main/src/ansys/mapdl/core/krylov.py",
        ),
        (
            "ansys.mapdl.core.database.nodes.DbNodes",
            "http://github.com/pyansys/pymapdl/edit/main/src/ansys/mapdl/core/database/nodes.py",
        ),
        (pytest.param("Query.lsy", "", marks=pytest.mark.xfail)),
        (pytest.param("Mapdl.chain_commands", "", marks=pytest.mark.xfail)),
        (pytest.param("Mapdl.last_response", "", marks=pytest.mark.xfail)),
        (pytest.param("Mapdl.chain_commands", "", marks=pytest.mark.xfail)),
    ],
)
def test_linkcode_resolve_edit(test_input, expected):
    assert (
        linkcode_resolve(
            "py", {"module": "ansys.mapdl.core", "fullname": test_input}, True
        )
        == expected
    )
