.. _ref_unit_testing_contributing:

Unit Testing
============

Unit tests are testing functions which validate that the software
logic implemented inside a certain method, class or module is
working as expected. They should try to be as atomic and 
independent as possible.

Unit testing is highly important. It enables to check that the
changes on the code are consistent with other parts of the code
and verify that the changes are the expected in the implementation.

Unit tests are in the ``tests`` directory inside this repository.
All the tests that you will find in this  directory are not
unit tests. Some of them are integration tests. The difference between
a unit test and an integration one is that integration tests will
test several units of the code and ensure that they work together.

To verify that all the code is properly tested, `Codecov <https://github.com/codecov>`_
generates a coverage report of the committed code. It details how
merging the Pull Request will impact the coverage. It is one of
the checks that must be approved to merge the code.

Test Validation GitHub workflow
-------------------------------

Unit tests and integration tests are part of the Continuous Integration (CD) approach. 
Combined with the Continuous Development (CD) one, they form the CI/CD approach. 
The latter provides continuous automation and monitoring
throughout the application lifecycle: from the coding and testing
phases to the deployment phase.

.. figure:: ../images/cicd.jpg
    :width: 300pt

Create a unit test 
------------------

In the PyMAPDL repository, tests run using ``pytest``. 

To create a pytest file, its name must be in the form ``test_filename.py``.

Here are some checks to create a good unit test: 

1. The test method name is long and descriptive.
2. The result of the test for PASS/FAIL is automatic. 
3. The tests cover all the scenarios of the code. You can check it with **Codecov**.
4. The test should return the same result each time. 
5. The tests are independent.
6. Each test verifies only one part of the code at a time.
7. The test should run fast.

`What makes a good unit test <https://stackoverflow.com/questions/61400/what-makes-a-good-unit-test>`_ 
is an exhaustive list of tips for creating good unit tests.

Since the majority of PyMAPDL tests imply server connection, most of the test are integration tests.

`The unit tests and the integration tests <https://github.com/pyansys/pymapdl/blob/main/tests/test_math.py>`_ of the 
**ansys.mapdl.core.math** library are one of the numerous tests that you can find in
the `test directory <https://github.com/pyansys/pymapdl/tree/main/tests>`_ .
You will find examples to understand how you can use the ``pytest`` package. Here is two of them: 

.. code:: python

    >>> import numpy as np
    >>> import ansys.mapdl.core.math as apdl_math

    >>> @pytest.fixture(scope="module")
    >>> def mm(mapdl):
    >>>     return mapdl.math

    >>> def test_rand(mm):
    >>>     w = mm.rand(10)
    >>>     assert w.size == 10

    >>> def test_matrix_addition(mm):
    >>>     m1 = mm.rand(10, 10)
    >>>     m2 = mm.rand(10, 10)
    >>>     m3 = m1 + m2
    >>>     assert np.allclose(m1.asarray() + m2.asarray(), m3.asarray())

You can find the `pytest documentation <https://docs.pytest.org/en/7.2.x/>`_ for further explanations.