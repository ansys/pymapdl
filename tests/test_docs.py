import os

import pytest

from ansys.mapdl.core.docs import linkcode_resolve

skip_if_not_on_ci = pytest.mark.skipif(
    not (os.environ.get("ON_CI", "").upper() == "TRUE"),
    reason="Skipping if not in CI",
)


@pytest.mark.parametrize("edit", [True, False])
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
        (
            "Mapdl.chain_commands",
            "http://github.com/pyansys/pymapdl/edit/main/src/ansys/mapdl/core/mapdl.py",
        ),
        (
            "Mapdl.last_response",
            "http://github.com/pyansys/pymapdl/edit/main/src/ansys/mapdl/core/mapdl.py",
        ),
    ],
)
def test_linkcode_resolve(test_input, expected, edit):
    if not edit:
        expected = expected.replace("/pymapdl/edit", "/pymapdl/blob")

    info = {"module": "ansys.mapdl.core", "fullname": test_input}
    url = linkcode_resolve("py", info, edit)

    assert "http://github.com/pyansys/pymapdl" in url
    assert "src/ansys/mapdl/core" in url
    assert expected.split("/")[-1] in url

    if "main" in url:
        assert expected in url
