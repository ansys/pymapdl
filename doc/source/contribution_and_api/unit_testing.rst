.. _ref_unit_testing_contributing:

Unit Testing
===============

Unit testing is highly important. It enables to check that the
changes on the code are efficient and don't have an impact on
other parts of the code. 

Unit tests are in the ``tests`` directory inside this repository.

Test Validation GitHub workflow
-------------------------------

`Codecov <https://github.com/codecov>`_ generates a coverage report of
the committed code. It details how merging the Pull Request will impact the
coverage. It is one of the checks that must be approved to
merge the code.

Creating a unit test 
--------------------

In the pymapdl repository, the tests are done with the **pytest package**. 

To create a pytest file, its name must be one of the following forms:
``filename_test.py`` or ``test_filename.py``.

To create tests, please take note of the `pytest documentation <https://docs.pytest.org/en/7.2.x/>`_ .

The `unit test <https://github.com/pyansys/pymapdl/blob/main/tests/test_math.py>`_ of the 
**ansys.mapdl.core.math** library is one of the numerous unit tests that you can find in
the `test directory <https://github.com/pyansys/pymapdl/tree/main/tests>`_ . 
You'll find examples to understand how you can use the pytest package.







    

