.. _ref_pymapdl_coding_guidelines:

PyMAPDL coding guidelines
=========================

Developing code in a repository, particularly when using version control systems
like Git, involves a set of essential guidelines to ensure efficient
collaboration, code management, and tracking changes. 

Here are the main guidelines for developing code in a repository:

#. **Use branches**: Create branches for different features, bug fixes, or
   experiments. This keeps changes isolated and facilitates parallel
   development. **The branch name must start with a lower case prefix and a backslash**.

#. **Write descriptive commit messages**: Provide clear and concise commit
   messages that explain the purpose and context of the changes. Follow a
   consistent style.

   - `build:` - Changes that affect the build system or external dependencies (such as to ``pip`` or ``make``).
   - `chore:` - Maintenance of the repository.
   - `ci:` - Changes to the CI/CD configuration files and scripts.
   - `docs:` - Improves documentation and examples.
   - `feat:` - Changes that introduce a new feature or significant addition.
   - `fix:` - Bug fixes.
   - `maint:` - General maintenance of the repository.
   - `no-ci:` - (Not applicable to PyMAPDL) In some repositories, branches with this prefix do not trigger CI/CD.
   - `perf:` - A code change that improves performance.
   - `refactor:` - A code change that neither fixes a bug nor adds a feature.
   - `release:` - Contains the released versions changes.
   - `revert:` - Reverts a previous commit.
   - `style:` - Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
   - `testing:` - For testing and debugging. It can be used to add new tests.

   **Note**: For more information, see `Table of allowed prefix <table_prefix_>`_.

#. **Commit frequently**: Make small, meaningful commits frequently. Avoid
   making a large number of unrelated changes in a single commit.

#. **Pull before you push**: Always update your local branch with the latest
   changes from the remote repository before pushing your own changes to avoid
   conflicts.

#. **Use pull requests (PRs)**: Use PRs to submit your changes for review.
   This allows for discussion and validation before merging into the main branch.
   Pull requests must follow the same convention as the commit messages.
   The following prefixes are allowed in the pull request names:

   - `build:` - Changes that affect the build system or external dependencies (such as to ``pip`` or ``make``).
   - `chore:` - Maintenance of the repository.
   - `ci:` - Changes to the CI/CD configuration files and scripts.
   - `docs:` - Improves documentation and examples.
   - `feat:` - Changes that introduce a new feature or significant addition.
   - `fix:` - Bug fixes.
   - `perf:` - A code change that improves performance.
   - `refactor:` - A code change that neither fixes a bug nor adds a feature.
   - `revert:` - Reverts a previous commit.
   - `style:` - Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
   - `test:` - For testing and debugging. It can be used to add new tests.

   **Note**: For more information, see `Table of allowed prefix <table_prefix_>`_.

   The pull requests can also be labeled for easier repository maintenance.
   The CI/CD automatically labels each pull request based on the pull requests prefix and
   the modified files, but you can also add extra labels as long as they are already defined
   in the repository.

#. **Write good documentation**: Maintain clear and up-to-date documentation for your
   contribution or changes, including comments in code, and relevant project
   documentation in rST or Markdown files.
   If you implement a new feature or change the behaviour of the library in any way,
   remember to mention it somewhere in the documentation (rST files in :file:`doc\source` directory)
   Follow the `numpydoc <numpydoc_>`_ convention for documenting code.
   In order to get more information on how to write good documentation for PyMAPDL, see
   :ref:`write_documentation` section.

#. **Test your changes**: Thoroughly test your changes to ensure that they work
   as expected. If applicable, create or update the unit tests that run on the 
   continuous integration/continuous deployment (CI/CD) pipelines to catch issues early
   and ensure reliable deployments.
   For more information, see :ref:`ref_unit_testing_contributing`.

#. **Respect code style and standards**: Follow code style
   guidelines and adhere to coding standards specific to your language or
   framework.

#. **Collaborate and communicate**: Communicate with team members, provide
   updates on your progress, and resolve any conflicts promptly.

#. **Ask for help**: To ensure code quality, identify issues, and share knowledge,
   ask PyMAPDL developers to assist you and review your code.
   If you need help or guidance, mention ``@ansys/pymapdl-maintainers`` in a comment
   so they they are notified.

By following these guidelines, you can ensure smooth and organized code
development within a repository, fostering collaboration, code quality, and feature enhancement.

**Table of allowed prefix**

.. _table_prefix:

+-------------+-----------------------------+------------------------------+----------------------------------+
| Prefix      | Commit (``prefix:``)        | Branch (``prefix/``)         | Pull-request (``prefix:``)       |
+=============+=============================+==============================+==================================+
| `build`     | |:white_check_mark:|        | |:white_check_mark:|         | |:white_check_mark:|             |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `dependabot`| |:x:|                       | |:white_check_mark:|         | |:x:|                            |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `chore`     | |:white_check_mark:|        | |:x:|                        | |:x:|                            |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `ci`        | |:white_check_mark:|        | |:white_check_mark:|         | |:white_check_mark:|             |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `docs`      | |:white_check_mark:|        | |:white_check_mark:|         | |:white_check_mark:|             |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `feat`      | |:white_check_mark:|        | |:white_check_mark:|         | |:white_check_mark:|             |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `fix`       | |:white_check_mark:|        | |:white_check_mark:|         | |:white_check_mark:|             |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `maint`     | |:white_check_mark:|        | |:white_check_mark:|         | |:x:|                            |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `perf`      | |:white_check_mark:|        | |:white_check_mark:|         | |:white_check_mark:|             |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `refactor`  | |:white_check_mark:|        | |:white_check_mark:|         | |:white_check_mark:|             |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `release`   | |:white_check_mark:|        | |:white_check_mark:|         | |:white_check_mark:|             |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `revert`    | |:white_check_mark:|        | |:white_check_mark:|         | |:x:|                            |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `style`     | |:white_check_mark:|        | |:x:|                        | |:x:|                            |
+-------------+-----------------------------+------------------------------+----------------------------------+
| `test`      | |:white_check_mark:|        | |:white_check_mark:|         | |:x:|                            |
+-------------+-----------------------------+------------------------------+----------------------------------+


Where:

* |:white_check_mark:| means that the prefix is allowed.
* |:x:| means that the prefix is not allowed.

