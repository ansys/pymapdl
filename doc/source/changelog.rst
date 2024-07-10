.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`0.68.4 <https://github.com/ansys/pymapdl/releases/tag/v0.68.4>`_ - 2024-07-10
==============================================================================
No significant changes.


`0.68.4 <https://github.com/ansys/pymapdl/releases/tag/v0.68.4>`_ - 2024-07-09
==============================================================================

Added
^^^^^

- test: skip test `#3259 <https://github.com/ansys/pymapdl/pull/3259>`_


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
- fix: not deleting temporary file when ``remove_temp_dir_on_exit``=True `#3247 <https://github.com/ansys/pymapdl/pull/3247>`_
- fix: local tests always running as student `#3251 <https://github.com/ansys/pymapdl/pull/3251>`_
- fix: incorrect env vars section `#3252 <https://github.com/ansys/pymapdl/pull/3252>`_


Dependencies
^^^^^^^^^^^^

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


Miscellaneous
^^^^^^^^^^^^^

- ci: [pre-commit.ci] pre-commit autoupdate `#3206 <https://github.com/ansys/pymapdl/pull/3206>`_
- ci: Adding v251 CentOS based image to testing `#3210 <https://github.com/ansys/pymapdl/pull/3210>`_
- [pre-commit.ci] pre-commit autoupdate `#3238 <https://github.com/ansys/pymapdl/pull/3238>`_, `#3253 <https://github.com/ansys/pymapdl/pull/3253>`_
- docs: adapt static images to dark/light themes `#3249 <https://github.com/ansys/pymapdl/pull/3249>`_

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
