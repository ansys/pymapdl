.. _contributing:

============
Contributing
============
We absolutely welcome any code contributions and we hope that this
guide will facilitate an understanding of the PyMAPDL code
repository. It is important to note that while the PyMAPDL software
package is maintained by Ansys and any submissions will be reviewed
thoroughly before merging, we still seek to foster a community that
can support user questions and develop new features to make this
software a useful tool for all users.  As such, we welcome and
encourage any questions or submissions to this repository.


Cloning the Source Repository
-----------------------------

You can clone the source repository from `PyMAPDL
GitHub <https://https://github.com/pyansys/pymapdl>`_
and install the latest version in development mode by running:

.. code::

    git clone https://github.com/pyansys/pymapdl
    cd pymapdl
    pip install -e .


Questions
---------
For general or technical questions about the project, its
applications, or about software usage, please create an issue at
`PyMAPDL Issues <https://github.com/pyansys/pymapdl/issues>`_ where the
community or PyMAPDL developers can collectively address your
questions.  The project support team can be reached at
`alexander.kaszynski@ansys.com <alexander.kaszynski@ansys.com>`_

By posting on the issues page, your question can be addressed by
community members with the needed expertise and the knowledge gained
will remain available on the issues page for other users.


Reporting Bugs
--------------
If you encounter any bugs or crashes while using PyMAPDL, please
report it at `PyMAPDL Issues <https://github.com/pyansys/pymapdl/issues>`_
with an appropriate label so we can promptly address it.  When
reporting an issue, please be overly descriptive so that we may
reproduce it. Whenever possible, please provide tracebacks,
screenshots, and sample files to help us address the issue.


Feature Requests
----------------
We encourage users to submit ideas for improvements to PyMAPDL!
Please create an issue on the `PyMAPDL Issues <https://github.com/pyansys/pymapdl/issues>`_
with a **Feature Request** label to suggest an improvement.
Please use a descriptive title and provide ample background information to help
the community implement that functionality. For example, if you would like a
reader for a specific file format, please provide a link to documentation of
that file format and possibly provide some sample files with screenshots to work
with. We will use the issue thread as a place to discuss and provide feedback.


Contributing New Code
---------------------
If you have an idea for how to improve PyMAPDL, consider first
creating an issue as a feature request which we can use as a
discussion thread to work through how to implement the contribution.

Once you are ready to start coding, please see the `Development
Practices <#development-practices>`__ section for more details.


Licensing
---------
All contributed code will be licensed under The MIT License found in
the repository. If you did not write the code yourself, it is your
responsibility to ensure that the existing license is compatible and
included in the contributed files or you can obtain permission from
the original author to relicense the code.

--------------

Development Practices
---------------------
This section provides a guide to how we conduct development in the
PyMAPDL repository. Please follow the practices outlined here when
contributing directly to this repository.

Guidelines
~~~~~~~~~~

Consider the following general coding paradigms when contributing:

1. Follow the `Zen of Python <https://www.python.org/dev/peps/pep-0020/>`__. As
   silly as the core Python developers are sometimes, there's much to
   be gained by following the basic guidelines listed in PEP 20.
   Without repeating them here, focus on making your additions
   intuitive, novel, and helpful for PyMAPDL and its users.

   When in doubt, ``import this``

2. **Document it**. Include a docstring for any function, method, or
   class added.  Follow the `numpydocs docstring
   <https://numpydoc.readthedocs.io/en/latest/format.html>`_
   guidelines, and always provide an example of simple use cases for
   the new features.

3. **Test it**. Since Python is an interperted language, if it's not
   tested, it's probably broken.  At the minimum, include unit tests
   for each new feature within the ``tests`` directory.  Ensure that
   each new method, class, or function has reasonable (>90%) coverage.

Additionally, please do not include any data sets for which a license
is not available or commercial use is prohibited.

Finally, please take a look at our `Code of Conduct <https://github.com/pyansys/pymapdl/blob/master/CODE_OF_CONDUCT.md>`_


Logging in PyMAPDL
~~~~~~~~~~~~~~~~~~~~

A specific logging architecture has been introduced in PyMAPDL 0.60 in order to make consistent the logging of events. 
There are two main logging level: global and instance. 

For both type of loggers, the default log message format is:

.. code:: python

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> mapdl._log.info('This is an useful message')
      LEVEL - INSTANCE NAME - MODULE - FUNCTION - MESSAGE
      INFO - GRPC_127.0.0.1:50052 -  test - <module> - This is an useful message

The ``instance_name`` field depends on the name of the MAPDL instance which might be not set yet when the log record is created (for example during the initialization of the library),
therefore in some cases, this field might be empty if there is no instance created yet.

Since both type of loggers are based in the python module ``logging`` you can use any of the tools provided in this module to extend or modify these loggers.

More information can be found in the module ``logging`` under ``ansys.mapdl.core``. 


Global logger
^^^^^^^^^^^^^^

There is a global logger called ``pymapdl_global`` which is initialized when PyMAPDL is imported.
This logger can be retrieved using:

.. code:: python

   from ansys.mapdl.core import LOG


This ``Logger`` is a custom class which wraps a ``logging.Logger`` object and give extra functionalities such a pre-defined file and stdout handlers and pointers.
You can access the underlying ``logging.Logger`` object using ``LOG.logger``.

You can use this logger anywhere in the code using:

.. code:: python

   from ansys.mapdl.core import LOG
   LOG.debug('This is an useful debug message')

It should be noticed that the default logging level of ``LOG`` is ``ERROR``.
To change this and output lower level messages you can use the next snippet:

.. code:: python

   LOG.logger.setLevel('DEBUG')
   LOG.file_handler.setLevel('DEBUG')  # If present. 
   LOG.stdout_handler.setLevel('DEBUG')  # If present.


Alternatively, you can do:

.. code:: python

   LOG.setLevel('DEBUG')


This way ensures all the handlers are set to the input log level. 

By default, this logger does not log to a file. If you wish to do so, you can add a file handler using:

.. code:: python

   import os
   file_path = os.path.join(os.getcwd(), 'pymapdl.log')
   LOG.log_to_file(file_path)


This sets the logger to be redirected also to that file. 
If you wish to change the characteristics of this global logger from the beginning of the execution, 
you must edit the file ``__init__`` in the directory ``ansys.mapdl.core``. 


Instance logger
^^^^^^^^^^^^^^^^

Additionally, there is also another type of logger provided within PyMAPDL. 
This is a logger specially designed for instances, hence it tracks the the MAPDL instance by pointing to its name (which should be unique)
and it is stored in ``_MapdlCore._log``. 
You can access it using:

.. code:: python

   from ansys.mapdl.core import launch_mapdl
   mapdl = launch_mapdl()
   instance_logger = mapdl._log


This logger is a completely independent from the global logger.
However when it is initialized, it copies the handlers from the global logger to centralize the logs in a terminal or file.  
You can access the underlying ``logging.Logger`` using:

.. code:: python

   logger = instance_logger.logger 

The way this logger works is very similar to the global logger. 
You can add a file handler if you wish using the method ``log_to_file`` or change the log level using ``setLevel`` method.



Contributing to PyMAPDL through GitHub
---------------------------------------------
To submit new code to PyMAPDL, first fork the `PyMAPDL GitHub Repo
<https://github.com/pyansys/pymapdl>`_ and then clone the forked
repository to your computer.  Next, create a new branch based on the
`Branch Naming Conventions Section <#branch-naming-conventions>`__ in
your local repository.

Next, add your new feature and commit it locally. Be sure to commit
often as it is often helpful to revert to past commits, especially if
your change is complex. Also, be sure to test often. See the `Testing
Section <#testing>`__ below for automating testing.

When you are ready to submit your code, create a pull request by
following the steps in the `Creating a New Pull Request
section <#creating-a-new-pull-request>`__.


Opening Issues
~~~~~~~~~~~~~~
Should you come across a bug in ``PyMAPDL`` or otherwise encounter some
unexpected behaviour you should create an "issue" regarding it. Issues are
created and submitted `here <https://github.com/pyansys/pymapdl/issues>`_.
Issues are used when developing to keep track of what is being
worked on at any one time, and by who. We have two issue templates
that we recommend you use:

* Bug report template
* Feature request template

If your issue does not fit into these two categories you are free
to create your own issue as well.

Issues should contain sufficient context for others to reproduce your
problem, such as the application versions you are using as well as
reproduction steps. Use issue labels like "Documentation" to further
highlight your issue's category.

Developers will respond to your issue and hopefully resolve it! Users
are encouraged to close their own issues once they are completed.
Otherwise, issues will be closed after a period of inactivity at the
discretion of the maintainers.

Should it turn out the fix did not work, or your issue was closed
erroneously, please re-open your issue with a comment addressing why.

Open ended questions should be opened in `Discussions <https://github.com/pyansys/pymapdl/discussions>`_,
and should an issue generate additional discussion, further issues
should be spun out into their own separate issues. This helps developers
keep track of what is being done and what needs to be done.


Discussions
~~~~~~~~~~~

General questions about PyMAPDL should be raised in
`Discussions <https://github.com/pyansys/pymapdl/discussions>`_ in
this repository rather than as issues themselves. Issues can be spun out of
discussions depending on what is decided, but general Q&A content
should start as discussions where possible.

.. note::
    The discussions feature is still in beta on GitHub, so this may
    change in the future.


Creating a New Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Once you have tested your branch locally, create a pull request on
`PyMAPDL <https://github.com/pyansys/pymapdl>`_ and target your
merge to `main`.  This will automatically run continuous
integration (CI) testing and verify your changes will work across all
supported platforms.

For code verification, someone from the PyMAPDL developers team will
review your code to verify your code meets our our standards.  Once
approved, if you have write permission you may merge the branch.  If
you don't have write permission, the reviewer or someone else with
write permission will merge the branch and delete the PR branch.

Since it may be necessary to merge your branch with the current
release branch (see below), please do not delete your branch if it
is a ``fix/`` branch.


Branch Naming Conventions
~~~~~~~~~~~~~~~~~~~~~~~~~
To streamline development, we have the following requirements for
naming branches. These requirements help the core developers know what
kind of changes any given branch is introducing before looking at the
code.

-  ``fix/``: any bug fixes, patches, or experimental changes that are
   minor
-  ``feat/``: any changes that introduce a new feature or significant
   addition
-  ``junk/``: for any experimental changes that can be deleted if gone
   stale
-  ``maint/``: for general maintenance of the repository or CI routines
-  ``doc/``: for any changes only pertaining to documentation
-  ``no-ci/``: for low impact activity that should NOT trigger the CI
   routines
-  ``testing/``: improvements or changes to testing
-  ``release/``: releases (see below)

Testing
~~~~~~~
Periodically when making changes, be sure to test locally before
creating a pull request. The following tests will be executed after
any commit or pull request, so we ask that you perform the following
sequence locally to track down any new issues from your changes.

.. code::

    pip install -r requirements_test.txt

Run the primary test suite and generate a coverage report with:

.. code::

    pytest -v --cov ansys-mapdl-core

If you do not have MAPDL installed locally but still wish to run the
unit testing, setup the following environment variables:

.. code::

    SET PYMAPDL_START_INSTANCE=False
    SET PYMAPDL_PORT=<MAPDL Port> (default 50052)
    SET PYMAPDL_IP=<MAPDL IP> (default 127.0.0.1)

or in Linux

.. code::

    export PYMAPDL_START_INSTANCE=False
    export PYMAPDL_PORT=<MAPDL Port> (default 50052)
    export PYMAPDL_IP=<MAPDL IP> (default 127.0.0.1)

This will tell the ``ansys.mapdl.core`` to attempt to connect to the existing
MAPDL service by default when the ``launch_mapdl`` function is used.


Spelling and Code Style
~~~~~~~~~~~~~~~~~~~~~~~
If you are using Linux or Mac OS, run check spelling and coding style
with:

.. code::

   make

Any misspelled words will be reported.  You can add words to be
ignored to ``ignore_words.txt``

.. code::

    codespell ./ "*.pyc,*.txt,*.gif,*.png,*.jpg,*.js,*.html,*.doctree,*.ttf,*.woff,*.woff2,*.eot,*.mp4,*.inv,*.pickle,*.ipynb,flycheck*,./.git/*,./.hypothesis/*,*.yml,./doc/build/*,./doc/images/*,./dist/*,*~,.hypothesis*,./doc/source/examples/*,*cover,*.dat,*.mac,\#*,build,./docker/mapdl/v211,./factory/*,./ansys/mapdl/core/mapdl_functions.py,PKG-INFO" -I "ignore_words.txt"


Documentation
-------------
Documentation for PyMAPDL is generated from three sources:

- Docstrings from the classes, functions, and modules of ``ansys.mapdl.core`` using `sphinx.ext.autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_.
- Restructured test from `doc/`
- Examples from `examples/`

General usage and API descriptions should be placed within `doc/source` and
the docstrings.  Full examples should be placed in `examples`.

Adding a New Example
~~~~~~~~~~~~~~~~~~~~

PyMAPDL examples come in two formats.  Basic code snippets demonstrating some functionality, or a full gallery examples.  Small code samples and snippets are contained in the `doc/source` directory, while the full gallery examples, meant to be run as individual downloadable scripts, are contained in the `examples` directory at the root of this repository.

To add a fully fledged, standalone example, add your example to the `examples` directory within one of the applicable subfolders.  Should none of the existing directories match the category of your example, create a new directory with a `README.txt` describing the new category.  Additionally, as these examples are built using the sphinx gallery extension, follow coding guidelines as established by [Sphinx-Gallery](https://sphinx-gallery.github.io/stable/index.html)

A self-demonstrating example is can be found at :ref:`ref_how_to_add_an_example_reference_key`.

:ref:`ref_how_to_add_an_example_reference_key`


Documentation Style and Organization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Docstrings should follow the `numpydocs docstring
<https://numpydoc.readthedocs.io/en/latest/format.html>`_ guidelines.
Documentation from `doc` use reStructuredText format.  Examples
within the `examples/` directory should be PEP8 compliant and will be
compiled dynamically during the build process; ensure they run
properly locally as they will be verified through the continuous
integration performed on GitHub Actions.


Building the Documentation Locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Documentation for PyMAPDL is hosted at mapdldocs.pyansys.com and is
automatically built and deployed using the GitHub Actions.  You can
build and verify the html documentation locally by install ``sphinx``
and the other documentation build dependencies by running the
following from the PyMAPDL source directory:

First, optionally install ``ansys-mapdl-core`` in development mode with:

.. code::

   pip install -e .

Then install the build requirements for documentation with:

.. code::

   pip install -r requirements_docs.txt


Next, if running Linux/Mac OS, build the documentation with:

.. code::

    make -C doc html

Otherwise, if running Windows, build the documentation by running:

.. code::

   cd doc
   make.bat html

Upon the successful build of the documentation, you can open the local
build by opening ``index.html`` at ``doc/build/html/`` with
your browser.


Continuous Integration and Continuous Delivery
----------------------------------------------
The PyMAPDL project uses continuous integration and delivery (CI/CD)
to automate the building, testing, and deployment tasks.  The CI
Pipeline is deployed on both GitHub Actions and Azure Pipelines and
performs following tasks:

- Module wheel build
- Core API testing
- Spelling and style verification
- Documentation build


Branching Model
~~~~~~~~~~~~~~~
This project has a branching model that enables rapid development of
features without sacrificing stability, and closely follows the 
`Trunk Based Development <https://trunkbaseddevelopment.com/>`_ approach.

The main features of our branching model are:

- The `main` branch is the main development branch.  All features,
  patches, and other branches should be merged here.  While all PRs
  should pass all applicable CI checks, this branch may be
  functionally unstable as changes might have introduced unintended
  side-effects or bugs that were not caught through unit testing.
- There will be one or many `release/` branches based on minor
  releases (for example `release/0.2`) which contain a stable version
  of the code base that is also reflected on PyPi/.  Hotfixes from
  `fix/` branches should be merged both to main and to these
  branches.  When necessary to create a new patch release these
  release branches will have their `__version__.py` updated and be
  tagged with a patched semantic version (e.g. `0.2.1`).  This
  triggers CI to push to PyPi, and allow us to rapidly push hotfixes
  for past versions of ``ansys.mapdl.core`` without having to worry about
  untested features.
- When a minor release candidate is ready, a new `release` branch will
  be created from `main` with the next incremented minor version
  (e.g. `release/0.2`), which will be thoroughly tested.  When deemed
  stable, the release branch will be tagged with the version (`0.2.0`
  in this case), and if necessary merged with main if any changes
  were pushed to it.  Feature development then continues on `main`
  and any hotfixes will now be merged with this release.  Older
  release branches should not be deleted so they can be patched as
  needed.


Minor Release Steps
~~~~~~~~~~~~~~~~~~~
Minor releases are feature and bug releases that improve the
functionality and stability of ``PyMAPDL``.  Before a minor release is
created the following will occur:

1.  Create a new branch from the ``main`` branch with name
    ``release/MAJOR.MINOR`` (e.g. `release/0.2`).

2. Locally run all tests as outlined in the `Testing Section <#testing>`__
and ensure all are passing.

3. Locally test and build the documentation with link checking to make sure
no links are outdated. Be sure to run `make clean` to ensure no results are
cached.

    .. code::

        cd doc
        make clean  # deletes the sphinx-gallery cache
        make html -b linkcheck

4. After building the documentation, open the local build and examine
   the examples gallery for any obvious issues.

5. Update the version numbers in ``ansys/mapdl/reader/_version.py`` and commit it.
   Push the branch to GitHub and create a new PR for this release that
   merges it to main.  Development to main should be limited at
   this point while effort is focused on the release.

6. It is now the responsibility of the PyMAPDL community and
   developers to functionally test the new release.  It is best to
   locally install this branch and use it in production.  Any bugs
   identified should have their hotfixes pushed to this release
   branch.

7. When the branch is deemed as stable for public release, the PR will
   be merged to main and the `main` branch will be tagged with a
   `MAJOR.MINOR.0` release.  The release branch will not be deleted.
   Tag the release with:

    .. code::

	git tag <MAJOR.MINOR.0>
        git push origin --tags


8. Create a list of all changes for the release. It is often helpful
   to leverage `GitHub's compare feature
   <https://github.com/pyansys/pymapdl/compare>`_ to see the
   differences from the last tag and the `main` branch.  Be sure to
   acknowledge new contributors by their GitHub username and place
   mentions where appropriate if a specific contributor is to thank
   for a new feature.

9. Place your release notes from step 8 in the description within
   `PyMAPDL Releases <https://github.com/pyansys/pymapdl/releases/new>`_


Patch Release Steps
~~~~~~~~~~~~~~~~~~~
Patch releases are for critical and important bugfixes that can not or
should not wait until a minor release.  The steps for a patch release

1. Push the necessary bugfix(es) to the applicable release branch.
   This will generally be the latest release branch
   (e.g. `release/0.2`).

2. Update `__version__.py` with the next patch increment
   (e.g. `0.2.1`), commit it, and open a PR that merge with the
   release branch.  This gives the PyMAPDL developers and community
   a chance to validate and approve the bugfix release.  Any
   additional hotfixes should be outside of this PR.

3. When approved, merge with the release branch, but not `main` as
   there is no reason to increment the version of the `main` branch.
   Then create a tag from the release branch with the applicable
   version number (see above for the correct steps).

4. If deemed necessary a release notes page.
