
.. _ref_unit_testing_contributing:

============
Unit testing
============

Unit tests validate the software by testing that the logic implemented inside a
certain method, class, or module is working as expected. They should be as
atomic and independent as possible.

Unit testing is highly important. The tests verify that code changes are
consistent with other parts of the code and verify that these changes are
implemented properly.

In the PyMAPDL repository, `pytest <pytest_>`_ is used to run tests and the
unit tests are in the `tests <pymapdl_tests_>`_ directory in this repository,
along with integration tests. The difference between a unit test and an
integration test is that the latter tests several units of the code to ensure
that they all work together.

To run all the unit tests use the following command:

.. code:: console

   (.venv) mapdl@machine:~/pymapdl$ pytest

This will execute all tests in the repository. You can also run specific tests by providing the path to the test file or directory.

If you are running on a **Linux machine without display**, you must install ``xvfb`` OS
library and run the preceding command with the ``xvfb-run`` command as prefix. 

.. code:: console

   (.venv) mapdl@machine:~/pymapdl$ xvfb-run pytest

In case you want to run only a certain subset of tests, you can use the ``-k`` argument
to filter the tests using booleans:

.. code:: console

   (.venv) mapdl@machine:~/pymapdl$ pytest -k "test_nlist_to_array or test_string_with_literal"
   ==================================================== test session starts ====================================================
   platform darwin -- Python 3.10.13, pytest-7.4.3, pluggy-1.3.0
   rootdir: /Users/german.ayuso/pymapdl
   configfile: pyproject.toml
   testpaths: tests
   plugins: timeout-2.2.0, cov-4.1.0, sphinx-0.5.0, rerunfailures-13.0, anyio-4.1.0, pytest_pyvista-0.1.9
   collected 1468 items / 1466 deselected / 4 skipped / 2 selected

   tests/test_commands.py ..                                                                                             [100%]

   =============================================== PyMAPDL Pytest short summary ================================================
   ======================================= 2 passed, 4 skipped, 1466 deselected in 2.27s =======================================


Unit test creation
==================

The name of a ``pytest`` file must be in the form ``test_XXX.py``, where ``XXX``
is either the function, method, or class that you are testing or some other explicative
name. In the command line, you can use the ``-k`` argument to filter the tests to run.
For more information, see `pytest usage <pytest_usage_>`_.

Here are some guidelines for creating good unit tests: 

- Descriptive: Assign long and descriptive names to tests.
- Fast: Make tests as short and fast as possible.
- Repeatability: Check that tests return the same results each time.
- Coverage: Use the `Codecov <codecov_>`_ tool to ensure that all implemented code is tested.
- Independent: Verify that tests are independent of your machine setup, however you can setup your
  test to run under certain conditions (i.e. environment variables).
- Atommic: Write tests that verify only one part of the code at a time.

`What makes a good unit test? <article_good_unit_test_>`_ 
is an exhaustive list of tips for creating good unit tests.

Most PyMAPDL tests require a connection to a running instance of
MAPDL, which runs the integration tests. If your test
requires a running MAPDL instance, you can use the PyMAPDL
`mapdl <mapdl_fixture_>`_ method in your function signature.
It is executed upstream of each test and not within all tests.

.. code:: python

   def test_my_new_feature(mapdl, cleared):  # pass the 'mapdl' fixture as an argument.
       mapdl.prep7()
       # .... more code

       return True  # (optional) if everything goes ok until here

Passing the ``cleared`` fixture is also useful since it clears up the MAPDL database
and configuration before performing the test.
If you do not have MAPDL installed locally but have an instance running in another machine,
you must set up the following environment variables.

.. tab-set::

    .. tab-item:: Windows
        :sync: key1

        .. code:: pwsh-session

            SET PYMAPDL_START_INSTANCE=False
            SET PYMAPDL_PORT=<MAPDL Port> (default 50052)
            SET PYMAPDL_IP=<MAPDL IP> (default 127.0.0.1)

    .. tab-item:: Linux
        :sync: key1
                
        .. code:: console

            export PYMAPDL_START_INSTANCE=False
            export PYMAPDL_PORT=<MAPDL Port> (default 50052)
            export PYMAPDL_IP=<MAPDL IP> (default 127.0.0.1)


These environment variables tell PyMAPDL to attempt to connect to the existing
MAPDL service by default when the ``launch_mapdl`` function is used. 

Additionally, you can use the :envvar:`PYMAPDL_MAPDL_EXEC` and :envvar:`PYMAPDL_MAPDL_VERSION`
environment variables to specify the MAPDL executable path and the version to launch (if
multiple versions of MAPDL are installed).

Example
-------

The `test_component.py <pymapdl_test_component_>`_ file contains
the unit tests and integration tests for the
:class:`ComponentManager <ansys.mapdl.core.component.ComponentManager>` class.
These tests are just some of the many in the `test directory <pymapdl_tests_>`_.

Here are some examples of how you use ``pytest``.
First, let define a fixture so it can be reused later:

.. code:: python

    import pytest


    # 'cube_geom_and_mesh' is another fixture defined in 'conftest.py'
    # and runs a minimal box model
    @pytest.fixture(scope="function")
    def basic_components(mapdl, cube_geom_and_mesh):
        """Given a model in 'cube_geom_and_mesh', define some components to work with later."""
        mapdl.components["mycomp1"] = "NODE", [1, 2, 3]
        mapdl.components["mycomp2"] = "KP", [1, 3]

        mapdl.cmsel("s", "mycomp1")
        mapdl.cmsel("a", "mycomp2")


Then the ``basic_component`` fixture can be used as follows in other unit tests:

.. code:: python

    def test_dunder_methods_keys(mapdl, basic_components):
        assert ["MYCOMP1", "MYCOMP2"] == list(mapdl.components.names())


    def test_dunder_methods_types(mapdl, basic_components):
        assert ["NODE", "KP"] == list(mapdl.components.types())


    def test_dunder_methods_items(mapdl, basic_components):
        assert [("MYCOMP1", "NODE"), ("MYCOMP2", "KP")] == list(mapdl.components.items())


For further ``pytest`` configuration details, see the `pytest documentation <pytest_>`_.


.. _ref_code_cov:

Code coverage
=============

To verify that all code is properly tested, you must ensure that every piece of
code is used (covered) in at least one unit test. In this repository, the
`Codecov <codecov_>`_ tool generates a coverage report of the committed code.
It indicates how merging a pull request would impact coverage. 
The generation of this report is one of the checks that must run successfully
to merge code changes.

.. figure:: ../images/codecov_increase.png
    :width: 400pt

To check the code coverage locally, you can use the following command:

.. code:: console

   (.venv) mapdl@machine:~/pymapdl$ pytest --cov

This will show you the code coverage report, highlighting any areas that are not covered by tests.

This information can be seen clearer from a web browser by using:

.. code:: console

    (.venv) mapdl@machine:~/pymapdl$ coverage html
    Wrote HTML report to htmlcov/index.html


If the code coverage is below 90%, unit tests should be added to the pull request
to increase the code coverage to a minimum.
There are `CICD workflows <ref_code_cov_>`_ in the GitHub repository that checks for the coverage criteria.


Coverage example
----------------

To show how the coverage works, assume that you have
this library:

**Awesome library**

.. code:: python

    def get_report_colors(theme):
        if theme == "weather":
            colors = ["blue", "lightblue", "grey"]
        elif theme == "traffic":
            colors = ["red", "orange", "yellow"]
        else:
            colors = ["red", "blue", "green"]

        return colors

**Tests**

You can opt to run the tests with this configuration:

.. code:: python

   def test_get_report_colors():
       assert get_report_colors("weather") == ["blue", "lightblue", "grey"]
       assert get_report_colors("traffic") == ["red", "orange", "yellow"]
       assert get_report_colors("other") == ["red", "blue", "green"]


Or, if a method is a bit more complex, you can split the case in different tests:

.. code:: python

    def test_get_report_colors_weather():
        assert get_report_colors("weather") == ["blue", "lightblue", "grey"]


    def test_get_report_colors_traffic():
        assert get_report_colors("traffic") == ["red", "orange", "yellow"]


    def test_get_report_colors_other():
        assert get_report_colors("other") == ["red", "blue", "green"]


While the code coverage in either case is 100% for the function, the second case is
more useful for debugging the function.

You can also use `parametrize (pytest.mark.parametrize) <pytest_parametrize_>`_ to
make the code more readable, and easier to reuse.

.. code:: python

    @pytest.mark.parametrize(
        "theme,output",
        [
            ["weather", "traffic", "other"],
            [
                ["blue", "lightblue", "grey"]["red", "orange", "yellow"][
                    "red", "blue", "green"
                ]
            ],
        ],
    )
    def test_get_report_color(theme, output):
        assert get_report_colors(theme) == output


For further explanations, see the `pytest documentation <pytest_>`_ .



Continuous integration and continuous deployment
================================================

Unit tests and integration tests are part of continuous integration (CI). 
The automation of testing, monitoring, and deployment of newly added
code allows continuous deployment (CD) throughout the app lifecycle,
providing a comprehensive CI/CD approach.

.. image:: ../images/cicd_dark_theme.png
    :class: only-dark
    :width: 300pt

.. image:: ../images/cicd_light_theme.png
    :class: only-light
    :width: 300pt
