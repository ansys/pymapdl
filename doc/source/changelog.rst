.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start


.. _v0.70.2:

`0.70.2 <https://github.com/ansys/pymapdl/releases/tag/v0.70.2>`_ - June 26, 2025
================================================================================================

.. tab-set::


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Fix: restrict ansys-tools-visualization-interface version range
          - `#4042 <https://github.com/ansys/pymapdl/pull/4042>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Fix: patch in testing
          - `#4010 <https://github.com/ansys/pymapdl/pull/4010>`_


.. _v0.70.1:

`0.70.1 <https://github.com/ansys/pymapdl/releases/tag/v0.70.1>`_ - May 12, 2025
===============================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - chore: update version to 0.70.dev0 in pyproject.toml
          - `#3907 <https://github.com/ansys/pymapdl/pull/3907>`_

        * - chore: update CHANGELOG for v0.70.0
          - `#3913 <https://github.com/ansys/pymapdl/pull/3913>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - fix: Change the mapdl_inprocess graphics backend
          - `#3915 <https://github.com/ansys/pymapdl/pull/3915>`_

        * - fix: documentation html looks
          - `#3918 <https://github.com/ansys/pymapdl/pull/3918>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - build: bump the core group with 2 updates
          - `#3910 <https://github.com/ansys/pymapdl/pull/3910>`_

        * - build: bump the testing group with 2 updates
          - `#3911 <https://github.com/ansys/pymapdl/pull/3911>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - feat: add artifact upload steps for JSONL logs in local and remote test workflows
          - `#3905 <https://github.com/ansys/pymapdl/pull/3905>`_

        * - build: bump platformdirs from 4.3.7 to 4.3.8 in the minimal group
          - `#3909 <https://github.com/ansys/pymapdl/pull/3909>`_

        * - build: update action versions in CI workflows to latest stable releases
          - `#3920 <https://github.com/ansys/pymapdl/pull/3920>`_


.. _v0.70.0:

`0.70.0 <https://github.com/ansys/pymapdl/releases/tag/v0.70.0>`_ - May 09, 2025
===============================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - chore: active support for Python 3.13
          - `#3605 <https://github.com/ansys/pymapdl/pull/3605>`_

        * - chore: update CHANGELOG for v0.69.3
          - `#3772 <https://github.com/ansys/pymapdl/pull/3772>`_

        * - perf: using MAPDL calls only to get the nodes in coordinate systems
          - `#3792 <https://github.com/ansys/pymapdl/pull/3792>`_

        * - refactor: using Python client library instead
          - `#3797 <https://github.com/ansys/pymapdl/pull/3797>`_

        * - refactor: do not import ansys.tools.visualizer by default when importing ansys.mapdl.core
          - `#3887 <https://github.com/ansys/pymapdl/pull/3887>`_

        * - chore: remove xfail markers from most flaky tests
          - `#3899 <https://github.com/ansys/pymapdl/pull/3899>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - fix(plotting): Improve interface of the plotting class.
          - `#3702 <https://github.com/ansys/pymapdl/pull/3702>`_

        * - fix: missing pool name in test
          - `#3773 <https://github.com/ansys/pymapdl/pull/3773>`_

        * - fix: improve element and node selection handling in post-processing
          - `#3784 <https://github.com/ansys/pymapdl/pull/3784>`_

        * - fix: adding console testing
          - `#3791 <https://github.com/ansys/pymapdl/pull/3791>`_

        * - fix: aborting MAPDL
          - `#3812 <https://github.com/ansys/pymapdl/pull/3812>`_

        * - feat: Add optional graphical target and rework graphics backend selection
          - `#3820 <https://github.com/ansys/pymapdl/pull/3820>`_

        * - fix: remove exceptions on mapdl object deletion
          - `#3826 <https://github.com/ansys/pymapdl/pull/3826>`_

        * - fix: Allow jupyter_backend manual selection
          - `#3838 <https://github.com/ansys/pymapdl/pull/3838>`_

        * - fix: linkchecker
          - `#3850 <https://github.com/ansys/pymapdl/pull/3850>`_

        * - fix: add check for artifacts directory before processing files
          - `#3851 <https://github.com/ansys/pymapdl/pull/3851>`_

        * - fix: specify type for click options in convert.py
          - `#3854 <https://github.com/ansys/pymapdl/pull/3854>`_

        * - fix: annotate launch_mapdl and better docstring
          - `#3855 <https://github.com/ansys/pymapdl/pull/3855>`_

        * - fix: remove duplicated lines
          - `#3858 <https://github.com/ansys/pymapdl/pull/3858>`_

        * - fix: update Dockerfile and docker-compose for MAPDL 2025R1 compatibility
          - `#3860 <https://github.com/ansys/pymapdl/pull/3860>`_

        * - fix: remove assignees from dependabot configuration
          - `#3861 <https://github.com/ansys/pymapdl/pull/3861>`_

        * - fix: pin quarto version
          - `#3876 <https://github.com/ansys/pymapdl/pull/3876>`_

        * - fix: update ansys-mapdl-reader version to 0.55.0 in documentation dependencies
          - `#3898 <https://github.com/ansys/pymapdl/pull/3898>`_

        * - fix: reducing space consumption in GitHub runners
          - `#3900 <https://github.com/ansys/pymapdl/pull/3900>`_

        * - fix: update ansys-sphinx-theme version to 1.4.4 in requirements files
          - `#3904 <https://github.com/ansys/pymapdl/pull/3904>`_

        * - fix: update changelog title format to include 'v' prefix for version
          - `#3908 <https://github.com/ansys/pymapdl/pull/3908>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - build: bump matplotlib from 3.10.0 to 3.10.1 in the core group
          - `#3774 <https://github.com/ansys/pymapdl/pull/3774>`_

        * - build: bump sphinx from 8.2.1 to 8.2.3 in the documentation group
          - `#3788 <https://github.com/ansys/pymapdl/pull/3788>`_

        * - build: bump pytest from 8.3.4 to 8.3.5 in the testing group
          - `#3789 <https://github.com/ansys/pymapdl/pull/3789>`_

        * - build: bump pyfakefs from 5.7.4 to 5.8.0
          - `#3800 <https://github.com/ansys/pymapdl/pull/3800>`_

        * - build: bump the documentation group across 1 directory with 2 updates
          - `#3815 <https://github.com/ansys/pymapdl/pull/3815>`_

        * - build: bump pytest-cov from 6.0.0 to 6.1.0 in the testing group
          - `#3823 <https://github.com/ansys/pymapdl/pull/3823>`_

        * - build: bump pytest-cov from 6.1.0 to 6.1.1 in the testing group
          - `#3833 <https://github.com/ansys/pymapdl/pull/3833>`_

        * - build: bump ansys-tools-visualization-interface from 0.8.3 to 0.9.0 in the core group
          - `#3848 <https://github.com/ansys/pymapdl/pull/3848>`_

        * - ci: adding dpf testing to cicd
          - `#3852 <https://github.com/ansys/pymapdl/pull/3852>`_

        * - build: bump ansys-tools-visualization-interface from 0.9.0 to 0.9.1 in the core group
          - `#3864 <https://github.com/ansys/pymapdl/pull/3864>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - feat: implement ignore cache reset context
          - `#3778 <https://github.com/ansys/pymapdl/pull/3778>`_

        * - feat: inject additional MAPDL command line arguments through an env var
          - `#3817 <https://github.com/ansys/pymapdl/pull/3817>`_

        * - hold the bc settings per plotter instance
          - `#3897 <https://github.com/ansys/pymapdl/pull/3897>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - docs: update towncrier template
          - `#3786 <https://github.com/ansys/pymapdl/pull/3786>`_

        * - docs: adding reference to tags
          - `#3795 <https://github.com/ansys/pymapdl/pull/3795>`_

        * - docs: update supported versions table for Ansys 2023-2025
          - `#3808 <https://github.com/ansys/pymapdl/pull/3808>`_

        * - docs: Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#3825 <https://github.com/ansys/pymapdl/pull/3825>`_, `#3836 <https://github.com/ansys/pymapdl/pull/3836>`_, `#3873 <https://github.com/ansys/pymapdl/pull/3873>`_

        * - docs: create self-contained apdl/pymapdl conversion example
          - `#3840 <https://github.com/ansys/pymapdl/pull/3840>`_

        * - docs: enhance parameter retrieval examples in user guide
          - `#3853 <https://github.com/ansys/pymapdl/pull/3853>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - ci: pre-commit autoupdate
          - `#3781 <https://github.com/ansys/pymapdl/pull/3781>`_, `#3793 <https://github.com/ansys/pymapdl/pull/3793>`_, `#3819 <https://github.com/ansys/pymapdl/pull/3819>`_, `#3842 <https://github.com/ansys/pymapdl/pull/3842>`_

        * - ci: using reusable workflows
          - `#3787 <https://github.com/ansys/pymapdl/pull/3787>`_

        * - ci: bump docker/login-action from 3.3.0 to 3.4.0 in the actions group
          - `#3804 <https://github.com/ansys/pymapdl/pull/3804>`_

        * - ci: adapting workflow for new docker container
          - `#3805 <https://github.com/ansys/pymapdl/pull/3805>`_

        * - build: bump the minimal group with 2 updates
          - `#3806 <https://github.com/ansys/pymapdl/pull/3806>`_

        * - feat: update Dockerfiles and requirements for improved library support and version upgrades
          - `#3822 <https://github.com/ansys/pymapdl/pull/3822>`_

        * - ci: update action versions to v9 in CI workflows
          - `#3834 <https://github.com/ansys/pymapdl/pull/3834>`_

        * - feat: update CI workflow to release to PyPI using trusted publisher
          - `#3837 <https://github.com/ansys/pymapdl/pull/3837>`_

        * - ci: bump actions/download-artifact from 4.1.9 to 4.2.1 in the actions group
          - `#3843 <https://github.com/ansys/pymapdl/pull/3843>`_

        * - build: bump numpy from 2.2.4 to 2.2.5 in the minimal group
          - `#3863 <https://github.com/ansys/pymapdl/pull/3863>`_

        * - feat: add GitHub Actions workflow to recreate PRs in main repository
          - `#3869 <https://github.com/ansys/pymapdl/pull/3869>`_

        * - ci: bump the actions group with 2 updates
          - `#3877 <https://github.com/ansys/pymapdl/pull/3877>`_

        * - feat: add CodeQL analysis workflow for Python
          - `#3902 <https://github.com/ansys/pymapdl/pull/3902>`_


.. _v0.69.3:

`0.69.3 <https://github.com/ansys/pymapdl/releases/tag/v0.69.3>`_ - 2025-02-27
==============================================================================

Added
^^^^^

- feat: add stochastic fem example `#3648 <https://github.com/ansys/pymapdl/pull/3648>`_
- feat: allow passing strings to the converter from the terminal `#3679 <https://github.com/ansys/pymapdl/pull/3679>`_
- feat: improving performance of save_selection `#3697 <https://github.com/ansys/pymapdl/pull/3697>`_
- feat: speed up `requires_package` using caching `#3705 <https://github.com/ansys/pymapdl/pull/3705>`_
- feat: avoiding reconnecting if MAPDL exited already `#3708 <https://github.com/ansys/pymapdl/pull/3708>`_
- feat: adding opened attribute `#3731 <https://github.com/ansys/pymapdl/pull/3731>`_
- feat: adding `muted` context manager `#3760 <https://github.com/ansys/pymapdl/pull/3760>`_


Fixed
^^^^^

- fix: avoid MAPDL commands execution when gRPC connection fails. `#3686 <https://github.com/ansys/pymapdl/pull/3686>`_
- fix: using cached version for remove lock on exit `#3709 <https://github.com/ansys/pymapdl/pull/3709>`_
- fix: sfem example typo errors `#3711 <https://github.com/ansys/pymapdl/pull/3711>`_
- fix: allow numpy types for parameters `#3720 <https://github.com/ansys/pymapdl/pull/3720>`_
- fix: harfrq command `#3729 <https://github.com/ansys/pymapdl/pull/3729>`_
- fix: ram units `#3730 <https://github.com/ansys/pymapdl/pull/3730>`_
- fix: exiting on class deletion `#3738 <https://github.com/ansys/pymapdl/pull/3738>`_
- fix: problem with the load_table method `#3745 <https://github.com/ansys/pymapdl/pull/3745>`_
- fix: do all the cleaning commands before cleaning the database, so we avoid having to issue `/POST1`. `#3747 <https://github.com/ansys/pymapdl/pull/3747>`_
- fix: Bug located in VSEL using KSWP field `#3753 <https://github.com/ansys/pymapdl/pull/3753>`_
- fix: Improve error handling in GET method and enhance output logging `#3758 <https://github.com/ansys/pymapdl/pull/3758>`_
- fix: avoid returning output when using input grpc method `#3759 <https://github.com/ansys/pymapdl/pull/3759>`_
- fix: removig star from command name in changelog `#3769 <https://github.com/ansys/pymapdl/pull/3769>`_


Dependencies
^^^^^^^^^^^^

- build: bump grpcio from 1.69.0 to 1.70.0 in the grpc-deps group `#3699 <https://github.com/ansys/pymapdl/pull/3699>`_
- build: bump imageio from 2.36.1 to 2.37.0 in the documentation group `#3700 <https://github.com/ansys/pymapdl/pull/3700>`_
- build: bump the documentation group across 1 directory with 3 updates `#3727 <https://github.com/ansys/pymapdl/pull/3727>`_
- build: update sphinx-autodoc-typehints to 3.0.1 `#3733 <https://github.com/ansys/pymapdl/pull/3733>`_
- build: bump sphinx-gallery from 0.18.0 to 0.19.0 in the documentation group `#3743 <https://github.com/ansys/pymapdl/pull/3743>`_
- build: bump pyansys-tools-report from 0.8.1 to 0.8.2 in the testing group `#3744 <https://github.com/ansys/pymapdl/pull/3744>`_
- build: bump the core group across 1 directory with 2 updates `#3761 <https://github.com/ansys/pymapdl/pull/3761>`_
- build: bump the documentation group across 1 directory with 2 updates `#3766 <https://github.com/ansys/pymapdl/pull/3766>`_
- build: temporary avoid flit latest version `#3771 <https://github.com/ansys/pymapdl/pull/3771>`_


Miscellaneous
^^^^^^^^^^^^^

- [pre-commit.ci] pre-commit autoupdate `#3330 <https://github.com/ansys/pymapdl/pull/3330>`_


Documentation
^^^^^^^^^^^^^

- docs: homogenizing commit/branches/pull request prefix `#3737 <https://github.com/ansys/pymapdl/pull/3737>`_


Maintenance
^^^^^^^^^^^

- chore: update CHANGELOG for v0.69.2 `#3688 <https://github.com/ansys/pymapdl/pull/3688>`_
- ci: skipping non-student versions when running on remote `#3690 <https://github.com/ansys/pymapdl/pull/3690>`_
- ci: adding memory limitation to MAPDL command line `#3693 <https://github.com/ansys/pymapdl/pull/3693>`_
- build: bump numpy from 2.2.1 to 2.2.2 in the minimal group `#3698 <https://github.com/ansys/pymapdl/pull/3698>`_
- refactor: make cli testing not depending on MAPDL. `#3678 <https://github.com/ansys/pymapdl/pull/3678>`_
- test: adding tests asserting None are translated to "None". `#3694 <https://github.com/ansys/pymapdl/pull/3694>`_
- test: improving testing performance `#3703 <https://github.com/ansys/pymapdl/pull/3703>`_
- ci: pre-commit autoupdate `#3710 <https://github.com/ansys/pymapdl/pull/3710>`_, `#3723 <https://github.com/ansys/pymapdl/pull/3723>`_
- ci: improving testing `#3716 <https://github.com/ansys/pymapdl/pull/3716>`_
- test: improving pool testing `#3736 <https://github.com/ansys/pymapdl/pull/3736>`_
- build: bump the minimal group with 2 updates `#3742 <https://github.com/ansys/pymapdl/pull/3742>`_
- ci: enhance CI testing by summarizing tests durations `#3754 <https://github.com/ansys/pymapdl/pull/3754>`_
- refactor: removing warnings `#3763 <https://github.com/ansys/pymapdl/pull/3763>`_
- ci: pre-commit autoupdate `#3749 <https://github.com/ansys/pymapdl/pull/3749>`_, `#3765 <https://github.com/ansys/pymapdl/pull/3765>`_
- ci: using python3.12 as main testing python version `#3767 <https://github.com/ansys/pymapdl/pull/3767>`_


.. _v0.69.2:

`0.69.2 <https://github.com/ansys/pymapdl/releases/tag/v0.69.2>`_ - 2025-01-22
==============================================================================

Added
^^^^^

- chore: update CHANGELOG for v0.69.1 `#3643 <https://github.com/ansys/pymapdl/pull/3643>`_
- feat: adding __len__ to components `#3663 <https://github.com/ansys/pymapdl/pull/3663>`_
- refactor: using test class in test_components.py `#3664 <https://github.com/ansys/pymapdl/pull/3664>`_
- test: making sure the full and rst files exists before running the tests `#3666 <https://github.com/ansys/pymapdl/pull/3666>`_


Fixed
^^^^^

- fix: parsing components when too many `#3662 <https://github.com/ansys/pymapdl/pull/3662>`_
- fix: avoid com logging if not in debug mode `#3665 <https://github.com/ansys/pymapdl/pull/3665>`_


Dependencies
^^^^^^^^^^^^

- build: bump grpcio from 1.68.1 to 1.69.0 in the grpc-deps group `#3645 <https://github.com/ansys/pymapdl/pull/3645>`_
- build: bump scipy from 1.14.1 to 1.15.0 in the core group `#3646 <https://github.com/ansys/pymapdl/pull/3646>`_
- build: bump pypandoc from 1.14 to 1.15 in the documentation group `#3647 <https://github.com/ansys/pymapdl/pull/3647>`_
- build: bump the core group with 3 updates `#3670 <https://github.com/ansys/pymapdl/pull/3670>`_
- build: bump imageio-ffmpeg from 0.5.1 to 0.6.0 in the documentation group `#3671 <https://github.com/ansys/pymapdl/pull/3671>`_
- build: bump autopep8 from 2.3.1 to 2.3.2 in the testing group `#3672 <https://github.com/ansys/pymapdl/pull/3672>`_
- build: bump pyfakefs from 5.7.3 to 5.7.4 `#3673 <https://github.com/ansys/pymapdl/pull/3673>`_


Documentation
^^^^^^^^^^^^^

- docs: fix post documentation `#3684 <https://github.com/ansys/pymapdl/pull/3684>`_


Maintenance
^^^^^^^^^^^

- ci: pre-commit autoupdate `#3657 <https://github.com/ansys/pymapdl/pull/3657>`_, `#3681 <https://github.com/ansys/pymapdl/pull/3681>`_
- ci: pin ubuntu OS to 22.04. `#3659 <https://github.com/ansys/pymapdl/pull/3659>`_
- ci: downgrade add-license-headers ansys precommit hook. `#3667 <https://github.com/ansys/pymapdl/pull/3667>`_
- ci: skipping students version if on remote `#3668 <https://github.com/ansys/pymapdl/pull/3668>`_
- ci: reducing minimal and console to two versions, and after local and remote `#3669 <https://github.com/ansys/pymapdl/pull/3669>`_
- ci: adding-profiling-to-unit-tests `#3676 <https://github.com/ansys/pymapdl/pull/3676>`_


.. _v0.69.1:

`0.69.1 <https://github.com/ansys/pymapdl/releases/tag/v0.69.1>`_ - 2025-01-08
==============================================================================

Added
^^^^^

- chore: update CHANGELOG for v0.69.0 `#3641 <https://github.com/ansys/pymapdl/pull/3641>`_


Fixed
^^^^^

- fix: timeout for file checking `#3642 <https://github.com/ansys/pymapdl/pull/3642>`_


Miscellaneous
^^^^^^^^^^^^^

- feat: node/element selection commands returning selected ids `#3636 <https://github.com/ansys/pymapdl/pull/3636>`_


.. _v0.69.0:

`0.69.0 <https://github.com/ansys/pymapdl/releases/tag/v0.69.0>`_ - 2025-01-08
==============================================================================

Added
^^^^^

- test: skip test `#3259 <https://github.com/ansys/pymapdl/pull/3259>`_
- refactor: modifying ``subprocess`` calls and removing ``try except continue`` statements `#3474 <https://github.com/ansys/pymapdl/pull/3474>`_
- refactor: launch_mapdl `#3475 <https://github.com/ansys/pymapdl/pull/3475>`_
- chore: update CHANGELOG for v0.68.6 `#3479 <https://github.com/ansys/pymapdl/pull/3479>`_
- refactor: `__init__` file `#3490 <https://github.com/ansys/pymapdl/pull/3490>`_
- refactor: moving information class to another module `#3491 <https://github.com/ansys/pymapdl/pull/3491>`_
- test: check all commands are submitted `#3501 <https://github.com/ansys/pymapdl/pull/3501>`_
- test: faking-v150 `#3509 <https://github.com/ansys/pymapdl/pull/3509>`_
- refactor: externalise the 'report' features to another file `#3511 <https://github.com/ansys/pymapdl/pull/3511>`_
- refactor: simplifying directory setter property `#3517 <https://github.com/ansys/pymapdl/pull/3517>`_
- refactor: testing suite (random order) `#3519 <https://github.com/ansys/pymapdl/pull/3519>`_
- refactor: moving tests to classes to avoid repeated fixtures execution `#3523 <https://github.com/ansys/pymapdl/pull/3523>`_
- refactor: using test classes in test_inline tests `#3524 <https://github.com/ansys/pymapdl/pull/3524>`_
- chore: fix codecov.yml content `#3542 <https://github.com/ansys/pymapdl/pull/3542>`_
- refactor: adding logging calls to misc.py `#3550 <https://github.com/ansys/pymapdl/pull/3550>`_
- refactor: removing-`run_as_prep7`-in-favour-of-`run_as` `#3551 <https://github.com/ansys/pymapdl/pull/3551>`_
- refactor: adding-type-ints-to-misc `#3553 <https://github.com/ansys/pymapdl/pull/3553>`_
- test: adding test for start_timeout arg `#3554 <https://github.com/ansys/pymapdl/pull/3554>`_
- refactor: increase post module coverage `#3556 <https://github.com/ansys/pymapdl/pull/3556>`_
- refactor: using find_mapdl instead of find_ansys `#3560 <https://github.com/ansys/pymapdl/pull/3560>`_
- refactor: annotate pymapdl part 1 `#3569 <https://github.com/ansys/pymapdl/pull/3569>`_
- refactor: replace `get_ansys_path` with `get_mapdl_path` `#3573 <https://github.com/ansys/pymapdl/pull/3573>`_
- refactor: small improvements to test settings `#3577 <https://github.com/ansys/pymapdl/pull/3577>`_
- tests: adding timeout to each test `#3621 <https://github.com/ansys/pymapdl/pull/3621>`_
- refactor: Iterate over the dictionary directly instead of using .keys(). `#3631 <https://github.com/ansys/pymapdl/pull/3631>`_


Changed
^^^^^^^

- chore: update CHANGELOG for v0.68.2 `#3183 <https://github.com/ansys/pymapdl/pull/3183>`_
- ci: Use CICD only on ``v*`` tags. `#3186 <https://github.com/ansys/pymapdl/pull/3186>`_
- ci: checking documentation style in ``Examples`` directory too `#3191 <https://github.com/ansys/pymapdl/pull/3191>`_
- chore: update CHANGELOG for v0.68.3 `#3201 <https://github.com/ansys/pymapdl/pull/3201>`_
- ci: Update julia testing `#3211 <https://github.com/ansys/pymapdl/pull/3211>`_
- ci: improving if to match also schedule and workflow_dispatch `#3223 <https://github.com/ansys/pymapdl/pull/3223>`_
- docs: documenting new naming conventions for commits, branches and PRs. `#3228 <https://github.com/ansys/pymapdl/pull/3228>`_
- ci: Using a dynamically generated matrix for testing job setup `#3232 <https://github.com/ansys/pymapdl/pull/3232>`_
- ci: increase the files checked for changes before load docs cache `#3237 <https://github.com/ansys/pymapdl/pull/3237>`_
- build: bump certifi from 2024.2.2 to 2024.7.4 in /doc/source/examples/extended_examples/hpc `#3242 <https://github.com/ansys/pymapdl/pull/3242>`_


Fixed
^^^^^

- fix: using same labels everywhere `#3188 <https://github.com/ansys/pymapdl/pull/3188>`_
- ci: Fix missing labels format in dependabot file `#3204 <https://github.com/ansys/pymapdl/pull/3204>`_
- ci: wrong tagging on the coverage artifacts `#3225 <https://github.com/ansys/pymapdl/pull/3225>`_
- fix: avoid inspecting suspended processes `#3227 <https://github.com/ansys/pymapdl/pull/3227>`_
- fix: not deleting temporary file when ``remove_temp_dir_on_exit`` =True `#3247 <https://github.com/ansys/pymapdl/pull/3247>`_
- fix: local tests always running as student `#3251 <https://github.com/ansys/pymapdl/pull/3251>`_
- fix: incorrect env vars section `#3252 <https://github.com/ansys/pymapdl/pull/3252>`_
- fix: raising port busy when connecting `#3507 <https://github.com/ansys/pymapdl/pull/3507>`_
- fix: logo link `#3525 <https://github.com/ansys/pymapdl/pull/3525>`_
- fix: checking port on non-grpc mapdl instances `#3540 <https://github.com/ansys/pymapdl/pull/3540>`_
- fix: warning and add an exception if using class alone `#3552 <https://github.com/ansys/pymapdl/pull/3552>`_
- fix: gui-extended-example `#3555 <https://github.com/ansys/pymapdl/pull/3555>`_
- fix: python version warning `#3570 <https://github.com/ansys/pymapdl/pull/3570>`_
- fix: components typo `#3582 <https://github.com/ansys/pymapdl/pull/3582>`_
- fix: avoiding long names in test arguments `#3583 <https://github.com/ansys/pymapdl/pull/3583>`_
- fix: console launching `#3586 <https://github.com/ansys/pymapdl/pull/3586>`_
- fix: linkchecker and cheatsheet links `#3589 <https://github.com/ansys/pymapdl/pull/3589>`_
- fix: avoid verbose grpc interface when solving `#3608 <https://github.com/ansys/pymapdl/pull/3608>`_
- fix: exit getting frozen if routine is not finished `#3617 <https://github.com/ansys/pymapdl/pull/3617>`_
- fix: changelog `#3640 <https://github.com/ansys/pymapdl/pull/3640>`_


Dependencies
^^^^^^^^^^^^

- build: bump pyvista[trame] from 0.43.9 to 0.43.10 `#3194 <https://github.com/ansys/pymapdl/pull/3194>`_
- build: bump the minimal group across 1 directory with 2 updates `#3197 <https://github.com/ansys/pymapdl/pull/3197>`_
- build: bump importlib-metadata from 7.2.0 to 7.2.1 in the minimal group `#3212 <https://github.com/ansys/pymapdl/pull/3212>`_
- build: bump scipy from 1.13.1 to 1.14.0 in the core group `#3213 <https://github.com/ansys/pymapdl/pull/3213>`_
- build: bump the documentation group with 2 updates `#3214 <https://github.com/ansys/pymapdl/pull/3214>`_, `#3495 <https://github.com/ansys/pymapdl/pull/3495>`_
- build: bump autopep8 from 2.3.0 to 2.3.1 in the testing group `#3215 <https://github.com/ansys/pymapdl/pull/3215>`_
- build: update requirements in devcontainer directory `#3217 <https://github.com/ansys/pymapdl/pull/3217>`_
- build: removing reredirect sphinx extension `#3224 <https://github.com/ansys/pymapdl/pull/3224>`_
- build: bump importlib-metadata from 7.2.1 to 8.0.0 in the minimal group `#3229 <https://github.com/ansys/pymapdl/pull/3229>`_
- build: bump the core group with 2 updates `#3241 <https://github.com/ansys/pymapdl/pull/3241>`_, `#3515 <https://github.com/ansys/pymapdl/pull/3515>`_, `#3534 <https://github.com/ansys/pymapdl/pull/3534>`_, `#3566 <https://github.com/ansys/pymapdl/pull/3566>`_
- build: update ansys-api-mapdl to 0.5.2 `#3255 <https://github.com/ansys/pymapdl/pull/3255>`_
- build: bump grpcio from 1.66.2 to 1.67.0 in the grpc-deps group `#3493 <https://github.com/ansys/pymapdl/pull/3493>`_
- build: bump ansys-sphinx-theme from 1.1.2 to 1.1.5 in the core group `#3494 <https://github.com/ansys/pymapdl/pull/3494>`_
- build: bump ansys-sphinx-theme from 1.1.2 to 1.1.6 in the core group across 1 directory `#3496 <https://github.com/ansys/pymapdl/pull/3496>`_
- build: bump pyansys-tools-report from 0.8.0 to 0.8.1 in the testing group `#3516 <https://github.com/ansys/pymapdl/pull/3516>`_
- build: bump grpcio from 1.67.0 to 1.67.1 in the grpc-deps group `#3533 <https://github.com/ansys/pymapdl/pull/3533>`_
- build: bump pytest-cov from 5.0.0 to 6.0.0 in the testing group `#3535 <https://github.com/ansys/pymapdl/pull/3535>`_
- build: bump ansys-sphinx-theme from 1.2.0 to 1.2.1 in the core group `#3547 <https://github.com/ansys/pymapdl/pull/3547>`_
- build: bump grpcio from 1.67.1 to 1.68.0 in the grpc-deps group `#3565 <https://github.com/ansys/pymapdl/pull/3565>`_
- build: bump pytest-rerunfailures from 14.0 to 15.0 in the testing group `#3567 <https://github.com/ansys/pymapdl/pull/3567>`_
- build: bump imageio from 2.36.0 to 2.36.1 in the documentation group `#3593 <https://github.com/ansys/pymapdl/pull/3593>`_
- build: bump grpcio from 1.68.0 to 1.68.1 in the grpc-deps group `#3601 <https://github.com/ansys/pymapdl/pull/3601>`_
- build: bump pytest from 8.3.3 to 8.3.4 in the testing group `#3603 <https://github.com/ansys/pymapdl/pull/3603>`_
- build: bump pyfakefs from 5.7.1 to 5.7.2 `#3604 <https://github.com/ansys/pymapdl/pull/3604>`_
- build: bump the core group across 1 directory with 3 updates `#3612 <https://github.com/ansys/pymapdl/pull/3612>`_, `#3633 <https://github.com/ansys/pymapdl/pull/3633>`_
- ci: adding ubuntu 251 and 252 `#3626 <https://github.com/ansys/pymapdl/pull/3626>`_
- build: bump pyfakefs from 5.7.2 to 5.7.3 `#3630 <https://github.com/ansys/pymapdl/pull/3630>`_


Miscellaneous
^^^^^^^^^^^^^

- ci: [pre-commit.ci] pre-commit autoupdate `#3206 <https://github.com/ansys/pymapdl/pull/3206>`_
- ci: Adding v251 CentOS based image to testing `#3210 <https://github.com/ansys/pymapdl/pull/3210>`_
- [pre-commit.ci] pre-commit autoupdate `#3238 <https://github.com/ansys/pymapdl/pull/3238>`_, `#3253 <https://github.com/ansys/pymapdl/pull/3253>`_
- feat: refactoring `create_temp_dir` `#3239 <https://github.com/ansys/pymapdl/pull/3239>`_
- docs: adapt static images to dark/light themes `#3249 <https://github.com/ansys/pymapdl/pull/3249>`_
- feat: adding 'pymapdl_nproc' to non-slurm runs `#3487 <https://github.com/ansys/pymapdl/pull/3487>`_
- feat: using version instead of exec_path for the MPI checks `#3528 <https://github.com/ansys/pymapdl/pull/3528>`_
- feat: raising error if plot image cannot be obtained `#3559 <https://github.com/ansys/pymapdl/pull/3559>`_
- feat: supporting v25.1 and v25.2 `#3571 <https://github.com/ansys/pymapdl/pull/3571>`_
- feat: adding-mode-warning `#3574 <https://github.com/ansys/pymapdl/pull/3574>`_
- feat: running MPI fix only if on windows `#3575 <https://github.com/ansys/pymapdl/pull/3575>`_
- feat: adding ``check_has_mapdl`` `#3576 <https://github.com/ansys/pymapdl/pull/3576>`_
- feat: improving load_array to reduce format line length `#3590 <https://github.com/ansys/pymapdl/pull/3590>`_
- feat: redirect MAPDL console output to a file `#3596 <https://github.com/ansys/pymapdl/pull/3596>`_
- feat: avoid errors when retrieving invalid routine `#3606 <https://github.com/ansys/pymapdl/pull/3606>`_


Documentation
^^^^^^^^^^^^^

- docs: documenting using pymapdl on clusters `#3466 <https://github.com/ansys/pymapdl/pull/3466>`_
- ci: avoiding linkcheck on changelog page `#3488 <https://github.com/ansys/pymapdl/pull/3488>`_
- feat: support for launching an MAPDL instance in an SLURM HPC cluster `#3497 <https://github.com/ansys/pymapdl/pull/3497>`_
- feat: passing tight integration env vars to mapdl `#3500 <https://github.com/ansys/pymapdl/pull/3500>`_
- docs: review of documenting using pymapdl on clusters (#3466) `#3506 <https://github.com/ansys/pymapdl/pull/3506>`_
- docs: adding-sbatch-support `#3513 <https://github.com/ansys/pymapdl/pull/3513>`_
- docs: removing extra links from landing page. `#3526 <https://github.com/ansys/pymapdl/pull/3526>`_
- DOC: Update pymapdl.rst `#3527 <https://github.com/ansys/pymapdl/pull/3527>`_
- [maint] remove importlib-metadata requirement `#3546 <https://github.com/ansys/pymapdl/pull/3546>`_
- docs: extracting information to another rst file `#3549 <https://github.com/ansys/pymapdl/pull/3549>`_
- docs: updating compatible Python versions `#3572 <https://github.com/ansys/pymapdl/pull/3572>`_
- docs: update docker instructions `#3580 <https://github.com/ansys/pymapdl/pull/3580>`_
- docs: adding some info for getting multiple compose running `#3584 <https://github.com/ansys/pymapdl/pull/3584>`_
- feat: update copyright year `#3637 <https://github.com/ansys/pymapdl/pull/3637>`_


Maintenance
^^^^^^^^^^^

- ci: bump thollander/actions-comment-pull-request from 2 to 3 in the actions group `#3481 <https://github.com/ansys/pymapdl/pull/3481>`_
- ci: pre-commit autoupdate `#3482 <https://github.com/ansys/pymapdl/pull/3482>`_, `#3522 <https://github.com/ansys/pymapdl/pull/3522>`_, `#3545 <https://github.com/ansys/pymapdl/pull/3545>`_, `#3599 <https://github.com/ansys/pymapdl/pull/3599>`_
- ci: force coloring in pytest `#3484 <https://github.com/ansys/pymapdl/pull/3484>`_
- build: bump psutil from 6.0.0 to 6.1.0 in the minimal group `#3492 <https://github.com/ansys/pymapdl/pull/3492>`_
- ci: ``ansys/actions/check-vulnerabilities`` to CI-CD `#3505 <https://github.com/ansys/pymapdl/pull/3505>`_
- ci: bump actions/checkout from 4.2.1 to 4.2.2 in the actions group `#3521 <https://github.com/ansys/pymapdl/pull/3521>`_
- build: bump numpy from 2.1.2 to 2.1.3 in the minimal group `#3541 <https://github.com/ansys/pymapdl/pull/3541>`_
- ci: bump codecov/codecov-action from 4 to 5 in the actions group `#3557 <https://github.com/ansys/pymapdl/pull/3557>`_
- ci: skipping student versions when user is authenticated `#3564 <https://github.com/ansys/pymapdl/pull/3564>`_
- ci: adding codeql.yml `#3585 <https://github.com/ansys/pymapdl/pull/3585>`_
- feat: activate debug mode on testing using `PYMAPDL_DEBUG_TESTING` envvar `#3594 <https://github.com/ansys/pymapdl/pull/3594>`_
- build: bump numpy from 2.1.3 to 2.2.0 in the minimal group `#3619 <https://github.com/ansys/pymapdl/pull/3619>`_
- ci: adding student back `#3623 <https://github.com/ansys/pymapdl/pull/3623>`_
- ci: temporary skipping attrs license check `#3624 <https://github.com/ansys/pymapdl/pull/3624>`_
- build: bump the minimal group across 1 directory with 2 updates `#3632 <https://github.com/ansys/pymapdl/pull/3632>`_
- ci: fix safety issue `#3638 <https://github.com/ansys/pymapdl/pull/3638>`_


.. _v0.68.6:

`0.68.6 <https://github.com/ansys/pymapdl/releases/tag/v0.68.6>`_ - 2024-10-11
==============================================================================

Added
^^^^^

- chore: update CHANGELOG for v0.68.5 `#3455 <https://github.com/ansys/pymapdl/pull/3455>`_
- refactor: removing deprecated arguments `#3473 <https://github.com/ansys/pymapdl/pull/3473>`_


Fixed
^^^^^

- fix: contributors file `#3457 <https://github.com/ansys/pymapdl/pull/3457>`_
- fix: environment variables not being passed to MAPDL process `#3461 <https://github.com/ansys/pymapdl/pull/3461>`_
- fix: exiting earlier to avoid exceptions from gRPC calls `#3463 <https://github.com/ansys/pymapdl/pull/3463>`_
- fix: add ``build cheatsheet`` as env variable within doc-build `#3468 <https://github.com/ansys/pymapdl/pull/3468>`_


Dependencies
^^^^^^^^^^^^

- build: bump grpcio from 1.66.1 to 1.66.2 in the grpc-deps group `#3453 <https://github.com/ansys/pymapdl/pull/3453>`_
- build: bump sphinx-autobuild from 2024.9.19 to 2024.10.3 in the documentation group `#3454 <https://github.com/ansys/pymapdl/pull/3454>`_
- build: bump ansys-tools-visualization-interface from 0.4.4 to 0.4.5 in the core group `#3477 <https://github.com/ansys/pymapdl/pull/3477>`_
- build: bump the documentation group with 3 updates `#3478 <https://github.com/ansys/pymapdl/pull/3478>`_


Miscellaneous
^^^^^^^^^^^^^

- feat: having two global flags. One for visualizer and one for pyvista `#3460 <https://github.com/ansys/pymapdl/pull/3460>`_


Documentation
^^^^^^^^^^^^^

- docs: another hpc docs reorg `#3465 <https://github.com/ansys/pymapdl/pull/3465>`_
- docs: fix cheat sheet rendering `#3469 <https://github.com/ansys/pymapdl/pull/3469>`_


Maintenance
^^^^^^^^^^^

- ci: bump the actions group with 2 updates `#3470 <https://github.com/ansys/pymapdl/pull/3470>`_
- ci: pre-commit autoupdate `#3471 <https://github.com/ansys/pymapdl/pull/3471>`_
- ci: bypass team check if it is dependabot `#3472 <https://github.com/ansys/pymapdl/pull/3472>`_
- build: bump numpy from 2.1.1 to 2.1.2 in the minimal group `#3476 <https://github.com/ansys/pymapdl/pull/3476>`_


.. _v0.68.5:

`0.68.5 <https://github.com/ansys/pymapdl/releases/tag/v0.68.5>`_ - 2024-10-04
==============================================================================

Added
^^^^^

- feat: Adapt PyMAPDL to common plotter `#2799 <https://github.com/ansys/pymapdl/pull/2799>`_
- refactor: clean mapdl inprocess and move mute to MapdlCore `#3220 <https://github.com/ansys/pymapdl/pull/3220>`_
- refactor: moving tests to a class and adding delete method. `#3258 <https://github.com/ansys/pymapdl/pull/3258>`_
- maint: update CHANGELOG for v0.68.4 `#3276 <https://github.com/ansys/pymapdl/pull/3276>`_
- chore: drop python3.9 support `#3326 <https://github.com/ansys/pymapdl/pull/3326>`_
- chore: update image cache `#3371 <https://github.com/ansys/pymapdl/pull/3371>`_
- chore: pre-commit autoupdate `#3373 <https://github.com/ansys/pymapdl/pull/3373>`_
- chore: skip database testing on v23.X `#3384 <https://github.com/ansys/pymapdl/pull/3384>`_
- chore: remove mapdl_inprocess.py from codecov analysis `#3404 <https://github.com/ansys/pymapdl/pull/3404>`_
- perf: reduce-testing-time `#3427 <https://github.com/ansys/pymapdl/pull/3427>`_


Changed
^^^^^^^

- ci: bump docker/login-action from 3.2.0 to 3.3.0 in the actions group `#3306 <https://github.com/ansys/pymapdl/pull/3306>`_
- build: bump importlib-metadata from 8.0.0 to 8.2.0 in the minimal group `#3309 <https://github.com/ansys/pymapdl/pull/3309>`_
- build: update pre-commit-hook `#3339 <https://github.com/ansys/pymapdl/pull/3339>`_


Fixed
^^^^^

- fix: removing io error when logging to closed streams `#3273 <https://github.com/ansys/pymapdl/pull/3273>`_
- fix: increasing timeout for local-min `#3282 <https://github.com/ansys/pymapdl/pull/3282>`_
- fix: local-min timeout `#3288 <https://github.com/ansys/pymapdl/pull/3288>`_
- fix: missing arguments in secdata `#3295 <https://github.com/ansys/pymapdl/pull/3295>`_
- Fix/node-numbering `#3297 <https://github.com/ansys/pymapdl/pull/3297>`_
- fix: filename with /OUTPUT command in stored commands `#3304 <https://github.com/ansys/pymapdl/pull/3304>`_
- fix: license headers `#3307 <https://github.com/ansys/pymapdl/pull/3307>`_
- fix: Making sure we skip all the pool unit tests. `#3315 <https://github.com/ansys/pymapdl/pull/3315>`_
- fix: reuploading file on CDREAD `#3355 <https://github.com/ansys/pymapdl/pull/3355>`_
- fix: warning raised in v251 `#3361 <https://github.com/ansys/pymapdl/pull/3361>`_
- fix: avoid changing entities ids after plotting `#3421 <https://github.com/ansys/pymapdl/pull/3421>`_
- fix: disabling logging on `__del__` `#3428 <https://github.com/ansys/pymapdl/pull/3428>`_
- fix: small plotting fix `#3439 <https://github.com/ansys/pymapdl/pull/3439>`_
- fix: changelog `#3452 <https://github.com/ansys/pymapdl/pull/3452>`_


Dependencies
^^^^^^^^^^^^

- build: bump numpy from 1.26.4 to 2.0.0 `#3177 <https://github.com/ansys/pymapdl/pull/3177>`_
- build: bump sphinx from 7.3.7 to 7.4.4 in the documentation group `#3283 <https://github.com/ansys/pymapdl/pull/3283>`_
- build: bump grpcio from 1.65.0 to 1.65.1 in the grpc-deps group `#3299 <https://github.com/ansys/pymapdl/pull/3299>`_
- build: bump sphinx from 7.4.4 to 7.4.6 in the documentation group `#3300 <https://github.com/ansys/pymapdl/pull/3300>`_
- build: bump ansys-tools-visualization-interface from 0.2.6 to 0.3.0 in the core group `#3310 <https://github.com/ansys/pymapdl/pull/3310>`_
- build: bump the documentation group with 3 updates `#3311 <https://github.com/ansys/pymapdl/pull/3311>`_, `#3324 <https://github.com/ansys/pymapdl/pull/3324>`_
- build: bump pytest from 8.2.2 to 8.3.2 in the testing group `#3312 <https://github.com/ansys/pymapdl/pull/3312>`_
- build: bump grpcio from 1.65.1 to 1.65.2 in the grpc-deps group `#3322 <https://github.com/ansys/pymapdl/pull/3322>`_
- build: bump ansys-tools-visualization-interface from 0.3.0 to 0.4.0 in the core group `#3323 <https://github.com/ansys/pymapdl/pull/3323>`_
- feat: adding `PYMAPDL_APDL_LOG` env var for testing `#3328 <https://github.com/ansys/pymapdl/pull/3328>`_
- build: bump grpcio from 1.65.2 to 1.65.4 in the grpc-deps group `#3344 <https://github.com/ansys/pymapdl/pull/3344>`_
- build: bump the core group with 2 updates `#3345 <https://github.com/ansys/pymapdl/pull/3345>`_, `#3358 <https://github.com/ansys/pymapdl/pull/3358>`_, `#3368 <https://github.com/ansys/pymapdl/pull/3368>`_
- build: bump sphinx-gallery from 0.17.0 to 0.17.1 in the documentation group `#3346 <https://github.com/ansys/pymapdl/pull/3346>`_
- ci: bump ansys/actions from 6 to 7 in the actions group `#3352 <https://github.com/ansys/pymapdl/pull/3352>`_
- build: bump pyansys-tools-report from 0.7.3 to 0.8.0 in the testing group `#3360 <https://github.com/ansys/pymapdl/pull/3360>`_
- build: bump the documentation group across 1 directory with 3 updates `#3363 <https://github.com/ansys/pymapdl/pull/3363>`_
- build: bump grpcio from 1.65.4 to 1.66.0 in the grpc-deps group `#3367 <https://github.com/ansys/pymapdl/pull/3367>`_
- build: bump grpcio from 1.66.0 to 1.66.1 in the grpc-deps group `#3381 <https://github.com/ansys/pymapdl/pull/3381>`_
- build: bump plotly from 5.23.0 to 5.24.0 in the documentation group `#3383 <https://github.com/ansys/pymapdl/pull/3383>`_
- build: bump the core group with 3 updates `#3386 <https://github.com/ansys/pymapdl/pull/3386>`_
- build: bump sphinx-autobuild from 2024.4.16 to 2024.9.3 in the documentation group `#3387 <https://github.com/ansys/pymapdl/pull/3387>`_
- build: bump ansys-tools-visualization-interface from 0.4.0 to 0.4.4 in the core group `#3400 <https://github.com/ansys/pymapdl/pull/3400>`_
- build: bump plotly from 5.24.0 to 5.24.1 in the documentation group `#3401 <https://github.com/ansys/pymapdl/pull/3401>`_
- build: bump pytest from 8.3.2 to 8.3.3 in the testing group `#3402 <https://github.com/ansys/pymapdl/pull/3402>`_
- build: bump ansys-sphinx-theme from 1.0.8 to 1.0.11 in the core group `#3418 <https://github.com/ansys/pymapdl/pull/3418>`_
- build: bump sphinx-autobuild from 2024.9.3 to 2024.9.19 in the documentation group `#3419 <https://github.com/ansys/pymapdl/pull/3419>`_
- build: bump pandas from 2.2.2 to 2.2.3 in the documentation group `#3433 <https://github.com/ansys/pymapdl/pull/3433>`_


Miscellaneous
^^^^^^^^^^^^^

- feat/adding missing argument `#3293 <https://github.com/ansys/pymapdl/pull/3293>`_
- feat/adding preppost license to allowed `#3294 <https://github.com/ansys/pymapdl/pull/3294>`_
- docs: adding warning about \*mwrite. Update \*vwrite warning to include \*mwrite `#3296 <https://github.com/ansys/pymapdl/pull/3296>`_
- [pre-commit.ci] pre-commit autoupdate `#3316 <https://github.com/ansys/pymapdl/pull/3316>`_, `#3330 <https://github.com/ansys/pymapdl/pull/3330>`_, `#3351 <https://github.com/ansys/pymapdl/pull/3351>`_
- feat: adding more descriptive errors `#3319 <https://github.com/ansys/pymapdl/pull/3319>`_
- feat: database module improvements `#3320 <https://github.com/ansys/pymapdl/pull/3320>`_
- feat: adding channel subscription method and tests `#3340 <https://github.com/ansys/pymapdl/pull/3340>`_
- feat: Adding 'methodconfig' for all services in channel to allow retry `#3343 <https://github.com/ansys/pymapdl/pull/3343>`_
- feat: adding python side retry mechanism `#3354 <https://github.com/ansys/pymapdl/pull/3354>`_
- Update conftest.py to switch mapdl.tbdat to mapdl.tbdata `#3362 <https://github.com/ansys/pymapdl/pull/3362>`_
- feat: supporting ´´to_dataframe()´´ for some bc list commands `#3412 <https://github.com/ansys/pymapdl/pull/3412>`_
- feat: add exit to inprocess backend `#3435 <https://github.com/ansys/pymapdl/pull/3435>`_
- feat: removing-CDB-files `#3441 <https://github.com/ansys/pymapdl/pull/3441>`_


Documentation
^^^^^^^^^^^^^

- feat: Supporting SLURM env vars for launching MAPDL configuration `#2754 <https://github.com/ansys/pymapdl/pull/2754>`_
- Docs/improving hpc documentation `#3379 <https://github.com/ansys/pymapdl/pull/3379>`_
- build: bump ansys-sphinx-theme from 1.0.5 to 1.0.7 in the core group `#3382 <https://github.com/ansys/pymapdl/pull/3382>`_
- docs: remove ``thispagetitle`` meta tag and add default `#3389 <https://github.com/ansys/pymapdl/pull/3389>`_
- docs: fix keywords metadata `#3396 <https://github.com/ansys/pymapdl/pull/3396>`_
- docs: cards layout for the landing page `#3414 <https://github.com/ansys/pymapdl/pull/3414>`_
- docs: adding cheat sheet on documentation `#3422 <https://github.com/ansys/pymapdl/pull/3422>`_
- docs: revamping example landing page and adding groups `#3434 <https://github.com/ansys/pymapdl/pull/3434>`_
- docs: reorg hpc section `#3436 <https://github.com/ansys/pymapdl/pull/3436>`_
- docs: update image and code block `#3440 <https://github.com/ansys/pymapdl/pull/3440>`_
- docs: adding directive to hide elements `#3449 <https://github.com/ansys/pymapdl/pull/3449>`_


Maintenance
^^^^^^^^^^^

- build: bump pyansys-tools-versioning from 0.5.0 to 0.6.0 in the minimal group `#3357 <https://github.com/ansys/pymapdl/pull/3357>`_
- build: bump importlib-metadata from 8.2.0 to 8.4.0 in the minimal group `#3366 <https://github.com/ansys/pymapdl/pull/3366>`_
- build: bump the minimal group with 2 updates `#3399 <https://github.com/ansys/pymapdl/pull/3399>`_, `#3417 <https://github.com/ansys/pymapdl/pull/3417>`_
- ci: pre-commit autoupdate `#3443 <https://github.com/ansys/pymapdl/pull/3443>`_
- ci: bump actions/checkout from 4.1.7 to 4.2.0 in the actions group `#3444 <https://github.com/ansys/pymapdl/pull/3444>`_
- ci: changing pre-commit commit and pr name `#3445 <https://github.com/ansys/pymapdl/pull/3445>`_


.. _v0.68.4:

`0.68.4 <https://github.com/ansys/pymapdl/releases/tag/v0.68.4>`_ - 2024-07-15
==============================================================================

Added
^^^^^


Fixed
^^^^^

- fix: missing arguments on ``OCDATA`` command `#3226 <https://github.com/ansys/pymapdl/pull/3226>`_
- fix: Raising `ValueError` when using ips within pool library `#3240 <https://github.com/ansys/pymapdl/pull/3240>`_
- fix: pool issues `#3266 <https://github.com/ansys/pymapdl/pull/3266>`_
- fix: using same labels everywhere `#3188 <https://github.com/ansys/pymapdl/pull/3188>`_
- fix: avoid inspecting suspended processes `#3227 <https://github.com/ansys/pymapdl/pull/3227>`_
- fix: not deleting temporary file when ``remove_temp_dir_on_exit`` =True `#3247 <https://github.com/ansys/pymapdl/pull/3247>`_
- fix: local tests always running as student `#3251 <https://github.com/ansys/pymapdl/pull/3251>`_
- fix: incorrect env vars section `#3252 <https://github.com/ansys/pymapdl/pull/3252>`_


Documentation
^^^^^^^^^^^^^

- docs: adapt static images to dark/light themes `#3249 <https://github.com/ansys/pymapdl/pull/3249>`_
- docs: documenting new naming conventions for commits, branches and PRs. `#3228 <https://github.com/ansys/pymapdl/pull/3228>`_


Dependencies
^^^^^^^^^^^^

- build: bump grpcio from 1.64.1 to 1.65.0 in the grpc-deps group `#3270 <https://github.com/ansys/pymapdl/pull/3270>`_
- build: bump zipp from 3.17.0 to 3.19.1 in /doc/source/examples/extended_examples/hpc `#3261 <https://github.com/ansys/pymapdl/pull/3261>`_
- build: bump the minimal group across 1 directory with 2 updates `#3197 <https://github.com/ansys/pymapdl/pull/3197>`_
- build: bump importlib-metadata from 7.2.0 to 7.2.1 in the minimal group `#3212 <https://github.com/ansys/pymapdl/pull/3212>`_
- build: bump scipy from 1.13.1 to 1.14.0 in the core group `#3213 <https://github.com/ansys/pymapdl/pull/3213>`_
- build: bump the documentation group with 2 updates `#3214 <https://github.com/ansys/pymapdl/pull/3214>`_
- build: bump autopep8 from 2.3.0 to 2.3.1 in the testing group `#3215 <https://github.com/ansys/pymapdl/pull/3215>`_
- build: update requirements in devcontainer directory `#3217 <https://github.com/ansys/pymapdl/pull/3217>`_
- build: removing reredirect sphinx extension `#3224 <https://github.com/ansys/pymapdl/pull/3224>`_
- build: bump importlib-metadata from 7.2.1 to 8.0.0 in the minimal group `#3229 <https://github.com/ansys/pymapdl/pull/3229>`_
- build: bump the core group with 2 updates `#3241 <https://github.com/ansys/pymapdl/pull/3241>`_
- build: update ansys-api-mapdl to 0.5.2 `#3255 <https://github.com/ansys/pymapdl/pull/3255>`_
- build: bump certifi from 2024.2.2 to 2024.7.4 in /doc/source/examples/extended_examples/hpc `#3242 <https://github.com/ansys/pymapdl/pull/3242>`_


Tests
^^^^^

- test: skip test `#3259 <https://github.com/ansys/pymapdl/pull/3259>`_


Maintenance
^^^^^^^^^^^

- [pre-commit.ci] pre-commit autoupdate `#3238 <https://github.com/ansys/pymapdl/pull/3238>`_, `#3253 <https://github.com/ansys/pymapdl/pull/3253>`_
- ci: Fix missing labels format in dependabot file `#3204 <https://github.com/ansys/pymapdl/pull/3204>`_
- ci: wrong tagging on the coverage artifacts `#3225 <https://github.com/ansys/pymapdl/pull/3225>`_
- ci: Adding v251 CentOS based image to testing `#3210 <https://github.com/ansys/pymapdl/pull/3210>`_
- ci: [pre-commit.ci] pre-commit autoupdate `#3206 <https://github.com/ansys/pymapdl/pull/3206>`_
- ci: Use CICD only on ``v*`` tags. `#3186 <https://github.com/ansys/pymapdl/pull/3186>`_
- ci: checking documentation style in ``Examples`` directory too `#3191 <https://github.com/ansys/pymapdl/pull/3191>`_
- chore: update CHANGELOG for v0.68.3 `#3201 <https://github.com/ansys/pymapdl/pull/3201>`_
- ci: Update julia testing `#3211 <https://github.com/ansys/pymapdl/pull/3211>`_
- ci: improving if to match also schedule and workflow_dispatch `#3223 <https://github.com/ansys/pymapdl/pull/3223>`_
- ci: Using a dynamically generated matrix for testing job setup `#3232 <https://github.com/ansys/pymapdl/pull/3232>`_
- ci: increase the files checked for changes before load docs cache `#3237 <https://github.com/ansys/pymapdl/pull/3237>`_
- ci: run extended array based on the person who open the PR `#3256 <https://github.com/ansys/pymapdl/pull/3256>`_


Miscellaneous
^^^^^^^^^^^^^

- chore: update CHANGELOG for v0.68.2 `#3183 <https://github.com/ansys/pymapdl/pull/3183>`_


.. _v0.68.3:

`0.68.3 <https://github.com/ansys/pymapdl/releases/tag/v0.68.3>`_ - 2024-06-21
==============================================================================

Added
^^^^^

- feat: Add an inprocess backend to pymapdl `#3198 <https://github.com/ansys/pymapdl/pull/3198>`_


.. _v0.68.2:

`0.68.2 <https://github.com/ansys/pymapdl/releases/tag/v0.68.2>`_ - 2024-06-18
==============================================================================

Added
^^^^^

- feat: add a MAPDL version section in for bug issues `#2982 <https://github.com/ansys/pymapdl/pull/2982>`_
- feat: adding some env var print to report `#2999 <https://github.com/ansys/pymapdl/pull/2999>`_
- feat: adding ``cycexpand`` command `#3023 <https://github.com/ansys/pymapdl/pull/3023>`_
- feat: update ``vfquery`` `#3037 <https://github.com/ansys/pymapdl/pull/3037>`_
- feat: add argument to disable run_at_connect in `MapdlGrpc` `#3047 <https://github.com/ansys/pymapdl/pull/3047>`_
- feat: allowing passing IP to ``MapdlPool`` `#3048 <https://github.com/ansys/pymapdl/pull/3048>`_
- feat: add argument to disable run_at_connect in MapdlGrpc `#3049 <https://github.com/ansys/pymapdl/pull/3049>`_
- feat: converting chained APDL commands to PyMAPDL context manager `#3154 <https://github.com/ansys/pymapdl/pull/3154>`_
- feat: allowing multiple IPs for remote connection on ``MapdlPool`` `#3166 <https://github.com/ansys/pymapdl/pull/3166>`_
- feat: implementing ``ansys/actions/changelogs`` and adding release note in documentation `#3019 <https://github.com/ansys/pymapdl/pull/3019>`_
- feat: adding option to ``_ctrl`` command `#3002 <https://github.com/ansys/pymapdl/pull/3002>`_
- feat: making old API function discoverable when Click is not installed `#3086 <https://github.com/ansys/pymapdl/pull/3086>`_


Changed
^^^^^^^

- refactor: refactoring CLI `#2960 <https://github.com/ansys/pymapdl/pull/2960>`_


Fixed
^^^^^

- fix: avoiding future sphinx warning `#3035 <https://github.com/ansys/pymapdl/pull/3035>`_
- fix: update the general files to align with PyAnsys standards `#3151 <https://github.com/ansys/pymapdl/pull/3151>`_
- fix: combine the ``docker-compose`` files `#3169 <https://github.com/ansys/pymapdl/pull/3169>`_


Documentation
^^^^^^^^^^^^^

- docs: adding previous changes in ``changelog.d`` repository `#3182 <https://github.com/ansys/pymapdl/pull/3182>`_
- docs: clarifying MAPDL commands API section `#3071 <https://github.com/ansys/pymapdl/pull/3071>`_
- docs: HPC documentation `#2966 <https://github.com/ansys/pymapdl/pull/2966>`_
- docs: adding ML-Genetic Algorithm example `#2981 <https://github.com/ansys/pymapdl/pull/2981>`_
- docs: customize agent for linkchecker `#2998 <https://github.com/ansys/pymapdl/pull/2998>`_
- docs: setting docs version to v241 `#3024 <https://github.com/ansys/pymapdl/pull/3024>`_
- docs: adding documentation about remote mapdl pool `#3046 <https://github.com/ansys/pymapdl/pull/3046>`_
- docs: update a minor typo in `mapdl.rst` `#3140 <https://github.com/ansys/pymapdl/pull/3140>`_


Dependencies
^^^^^^^^^^^^

- build: bump autopep8 from 2.2.0 to 2.3.0 in the testing group `#3179 <https://github.com/ansys/pymapdl/pull/3179>`_
- build: bump pyvista[trame] from 0.43.9 to 0.43.10 `#3180 <https://github.com/ansys/pymapdl/pull/3180>`_
- build: bump ansys-sphinx-theme from 0.16.5 to 0.16.6 in the core group across 1 directory `#3181 <https://github.com/ansys/pymapdl/pull/3181>`_


Miscellaneous
^^^^^^^^^^^^^

- chore: removing cdb files `#3036 <https://github.com/ansys/pymapdl/pull/3036>`_
- ci: having only one set of Dependabot rules `#3107 <https://github.com/ansys/pymapdl/pull/3107>`_
- ci: adding tag for doc review `#3118 <https://github.com/ansys/pymapdl/pull/3118>`_
- ci: remove OS package duplicate `#3147 <https://github.com/ansys/pymapdl/pull/3147>`_
- ci: using trusted publisher release process `#3171 <https://github.com/ansys/pymapdl/pull/3171>`_

.. vale on
