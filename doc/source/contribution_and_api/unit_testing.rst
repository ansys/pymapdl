.. _ref_unit_testing_contributing:

Unit Testing
============

Unit tests validate the software by testing that the logic
implemented inside a certain method, class, or module is
working as expected. They should be as atomic and 
independent as possible.

Unit testing is highly important. The tests check that code
changes are consistent with other parts of the code
and verify that these changes are implemented properly.

Unit tests are in the `tests <pymapdl_tests_>`_ directory in this repository,
along with integration tests. The difference between
a unit test and an integration test is that the latter
tests several units of the code to ensure that they all work together.

To verify that all code is properly tested, you must ensure that every piece
of code is used (covered) in at least one unit test. In this repository, the
`Codecov <codecov_>`_ tool generates a coverage report of the
committed code. It details how merging a pull request would impact coverage. It
is one of the checks that must run successfully to merge code changes.


.. figure:: ../images/codecov_increase.png
    :width: 400pt


Coverage example
----------------

To show how the coverage works, assume that you have
this library:

**My awesome library**


.. code:: python

    def get_report_colors(theme):

        if theme == 'weather':
            colors = ["blue", "lightblue", "grey"]
        elif theme == 'traffic':
            colors = ["red", "orange", "yellow"]
        else:
            colors = ["red", "blue", "green"]
        
        return colors


**Tests**

You can opt to run the tests with this configuration:

.. code:: python

   def test_get_report_colors():

        assert get_report_colors('weather') == ["blue", "lightblue", "grey"]
        assert get_report_colors('traffic') == ["red", "orange", "yellow"]
        assert get_report_colors('other') == ["red", "blue", "green"]


Or, if a method is a bit more complex, you can split the case in different tests:

.. code:: python

    def test_get_report_colors_weather():

        assert get_report_colors('weather') == ["blue", "lightblue", "grey"]

    def test_get_report_colors_traffic():

        assert get_report_colors('traffic') == ["red", "orange", "yellow"]

    def test_get_report_colors_other():

        assert get_report_colors('other') == ["red", "blue", "green"]


In any of the cases, the coverage will be 100% for the function, but the second case will
be more useful to debug the function.


Test Validation GitHub workflow
-------------------------------

Unit tests and integration tests are part of the Continuous Integration (CI) approach. 
Combined with the Continuous Development (CD) approach, they form the CI/CD approach. 
This approach provides continuous integration (CI) of the newly added code by
automating its testing, monitoring and deployment which allow us a continuous
deployment (CD) throughout the application lifecycle.

.. figure:: ../images/cicd.jpg
    :width: 300pt

Create a unit test 
------------------

In the PyMAPDL repository, tests run using `pytest <pytest_>`_. 

To create a pytest file, its name must be in the form ``test_XXX.py``  where ``XXX``
can be the function/method/class you are testing or some other explicative
name. Please keep in mind that ``pytest`` can filter the tests to run in the command
line using the argument ``-k``. For more information visit `pytest usage <pytest_usage_>`_.

Here is some advice to follow when creating good unit tests: 

1. The test method names are long and descriptive.
2. The tests cover all the code implementation. You can check it with **Codecov**.
3. The tests should return the same result each time. 
4. The tests are independent.
5. Each test verifies only one part of the code at a time.
6. The tests should be as short and fast as possible.

`What makes a good unit test <article_good_unit_test_>`_ 
is an exhaustive list of tips for creating good unit tests.

Since the majority of PyMAPDL tests imply server connection, most of the
test are integration tests and they require a running instance of MAPDL. If
your test requires a running MAPDL instance, PyMAPDL library provides the
`mapdl <mapdl_fixture_>`_ fixture which you can use as the following in your
function signature. It will be executed upstream each test and not within all tests.

.. code:: python

   def test_my_new_feature(mapdl):  # just pass the 'mapdl' fixture as an argument.

       mapdl.prep7()
       # .... more code

       return True # if everything goes ok until here


Example
--------

The unit tests and the integration tests of the `ansys.mapdl.core.math module <pymapdl_user_guide_math_>`_
are in the python file `test_math.py <pymapdl_test_math_>`_.
These are just some of the numerous tests that you can find in the `test directory <pymapdl_tests_>`_.

Some examples of unit test to understand how you can use the ``pytest`` package are showed now:

.. code:: python

    import numpy as np
    import ansys.mapdl.core.math as apdl_math

    @pytest.fixture(scope="module")
    def mm(mapdl):  # just pass the 'mapdl' fixture as an argument.

        return mapdl.math

    def test_rand(mm):  # just pass the 'mm' fixture as an argument.

        w = mm.rand(10)
        assert w.size == 10  # if it is False, AssertionError is raised

    def test_matrix_addition(mm):

        m1 = mm.rand(10, 10)
        m2 = mm.rand(10, 10)
        m3 = m1 + m2
        assert np.allclose(m1.asarray() + m2.asarray(), m3.asarray())  
                            # if it is False, AssertionError is raised

You can find the `pytest documentation <pytest_>`_ for further explanations.