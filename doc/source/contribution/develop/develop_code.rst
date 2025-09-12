.. _ref_develop_pymapdl:

===============
Develop PyMAPDL
===============

.. epigraph:: *Now it is time to develop PyMAPDL!*

You can help improve PyMAPDL by fixing a bug or developing a new feature.
Developing PyMAPDL involves several steps:

#. :ref:`ref_create_branch`
#. :ref:`ref_make_changes`
#. :ref:`ref_test_locally`
#. Commit the changes.
#. Open a pull request
#. Review and merge

Additionally we recommend you to have a look at the :ref:`ref_pymapdl_coding_guidelines`.

.. _ref_create_branch:

Create a branch
===============

Create branches for different features, bug fixes, or
experiments. This keeps changes isolated and facilitates parallel
development. 
To create a new branch, use the following command:

.. code:: console

   (.venv) mapdl@machine:~/pymapdl$ git checkout -b <branch_name>


**The branch name must start with a lower case prefix and a backslash**.

The allowed prefixes are:

- `build/` - Changes that affect the build system or external dependencies
  (such as to ``pip`` or ``make``).
- `chore/` - General maintenance of the repository.
- `ci/` - Changes to the CI/CD configuration files and scripts.
- `dependabot/` - Created by Dependabot, you should not create branches with this prefix.
- `docs/` - Improves documentation and examples.
- `feat/` - Changes that introduce a new feature or significant addition.
- `fix/` - Bug fixes.
- `junk/` - Other purposes. It should not be used for branches that are going to
  be merged to ``main``.
- `perf/` - A code change that improves performance.
- `refactor/` - A code change that neither fixes a bug nor adds a feature.
- `release/` - Contains the released versions changes. These branches are created only by
  maintainers.
- `revert/` - Reverts a previous commit.
- `style/` - Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
- `test/` - For testing and debugging. It can be used to add new tests.

**Note**: For more information, see `Table of allowed prefix <table_prefix_>`_.

.. _ref_make_changes:

Make changes
============

Make the necessary changes to the codebase in your branch. Ensure that your changes are well-tested and do not break existing functionality.
For more information about testing, visit :ref:`ref_test_locally`.

To make sure you are not breaking anything, you can run the test suite and check the code coverage. This will help you identify any potential issues before committing your changes.
It is also good practice to run the pre-commit hooks to ensure your code adheres to the project's coding standards.


.. _ref_test_locally:

Test locally
============

Before committing your changes, it is important to test them locally to ensure they work as expected. This includes running the test suite and checking the code coverage.

To run the test suite, use the following command:

.. code:: console

   (.venv) mapdl@machine:~/pymapdl$ pytest

For more information about PyMAPDL testing, refers to :ref:`ref_unit_testing_contributing` section.


Code style
==========

PyMAPDL follows the PEP8 standard as outlined in the `PyAnsys Development Guide
<dev_guide_pyansys_>`_ and implements style checking using
`pre-commit <precommit_>`_.
To install `pre-commit <precommit_>`_ follow the steps given in :ref:`ref_install_precommit`.

To ensure your code meets minimum code styling standards, run these commands:

.. code:: console

   (.venv) mapdl@machine:~/pymapdl$ pre-commit run --all-files

If you have installed ``pre-commit`` as a hook, ``git`` automatically
runs these hooks before committing, failing if it find any
format issues and making or proposing the necessary changes
to the commit.
If this happens, you might need to edit your files and run the pre-commit checks several times before committing successfully.
Some hooks automatically fix those issues and reformat the files.

.. code:: console

   (.venv) mapdl@machine:~/pymapdl$ git commit -m "my commit"
   [INFO] Stashing unstaged files to /home/mapdl/.cache/pre-commit/patch1704703895-16914.
   Add License Headers......................................................Passed
   isort....................................................................Passed
   numpydoc-validation......................................................Passed
   black....................................................................Passed
   blacken-docs.............................................................Failed
   - hook id: blacken-docs
   - exit code: 1
   - files were modified by this hook

   doc/source/getting_started/develop_pymapdl.rst: Rewriting...

A successful commit will look like the following:

.. code:: console

   (.venv) mapdl@machine:~/pymapdl$ git commit -m "my commit"
   [WARNING] Unstaged files detected.
   [INFO] Stashing unstaged files to /home/mapdl/.cache/pre-commit/patch1704703895-16914.
   Add License Headers..................................(no files to check)Skipped
   isort................................................(no files to check)Skipped
   numpydoc-validation..................................(no files to check)Skipped
   black................................................(no files to check)Skipped
   blacken-docs.............................................................Passed
   flake8...............................................(no files to check)Skipped
   codespell................................................................Passed
   check for merge conflicts................................................Passed
   debug statements (python)............................(no files to check)Skipped
   Validate GitHub Workflows............................(no files to check)Skipped
   [INFO] Restored changes from /home/mapdl/.cache/pre-commit/patch1704703895-16914.
   [ci/mybranch cXXXXXXX] my commit
   1 file changed, 25 insertions(+)
   (.venv) mapdl@machine:~/pymapdl$ 


First time you run ``pre-commit`` (using ``git commit`` or ``pre-commit``), the command
might take some time (2-3 minutes) to download the specified hooks and install them.
After that first time, analysing your commits should take seconds.

``pre-commit`` hooks can also be updated, added or removed. For more information, visit
`pre-commit <precommit_>`_ website.
