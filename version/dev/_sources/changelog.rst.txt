.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`0.68.3 <https://github.com/ansys/pymapdl/releases/tag/v0.68.3>`_ - 2024-06-21
==============================================================================

Added
^^^^^

- feat: Add an inprocess backend to pymapdl `#3198 <https://github.com/ansys/pymapdl/pull/3198>`_


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
