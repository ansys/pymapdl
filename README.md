<p align="center">
   <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_dark.png">
      <source media="(prefers-color-scheme: light)" srcset="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_light.png">
      <img alt="PyMAPDL Logo" src="https://github.com/ansys/pymapdl/blob/main/doc/source/_static/logo_light.png" width="70%">
   </picture>
</p>

[![pyansys](https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC)](https://docs.pyansys.com/)
[![pypi](https://img.shields.io/pypi/v/ansys-mapdl-core.svg?logo=python&logoColor=white)](https://pypi.org/project/ansys-mapdl-core/)
[![PyPIact](https://img.shields.io/pypi/dm/ansys-mapdl-core.svg?label=PyPI%20downloads)](https://pypi.org/project/ansys-mapdl-core/)
[![codecov](https://codecov.io/gh/ansys/pymapdl/branch/main/graph/badge.svg)](https://codecov.io/gh/ansys/pymapdl)
[![GH-CI](https://github.com/ansys/pymapdl/actions/workflows/ci.yml/badge.svg)](https://github.com/ansys/pymapdl/actions/workflows/ci.yml)
[![zenodo](https://zenodo.org/badge/70696039.svg)](https://zenodo.org/badge/latestdoi/70696039)
[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)](https://github.com/psf/black)
[![pre-commit](https://results.pre-commit.ci/badge/github/ansys/pymapdl/main.svg)](https://results.pre-commit.ci/latest/github/ansys/pymapdl/main)

## Overview

The PyMAPDL project supports Pythonic access to MAPDL to be able to
communicate with the MAPDL process directly from Python. The latest
[ansys-mapdl-core](https://pypi.org/project/ansys-mapdl-core/) package
enables a more comprehensive interface with MAPDL and supports:

-  All the features of the original module (for example, Pythonic commands 
   and interactive sessions).

-  Remote connections to MAPDL from anywhere via gRPC.

-  Direct access to MAPDL arrays, meshes, and geometry as Python
   objects.

-  Low-level access to the MAPDL solver through APDL math in a SciPy-
   like interface.

Here's a quick demo of PyMAPDL within Visual Studio Code:

![landing_demo](https://github.com/ansys/pymapdl/raw/main/doc/source/_static/landing_page_demo.gif)

PyMAPDL works within Jupyter Notebooks, the standard Python console,
or in batch mode on Windows, Linux, and even Mac OS.

## Documentation and issues

Documentation for the latest stable release of PyMAPDL is hosted at
[PyMAPDL Documentation](https://mapdl.docs.pyansys.com).

In the upper right corner of the documentation's title bar, there is an option for switching from
viewing the documentation for the latest stable release to viewing the documentation for the
development version or previously released versions.

You can also [view](https://cheatsheets.docs.pyansys.com/pymapdl_cheat_sheet.png) or
[download](https://cheatsheets.docs.pyansys.com/pymapdl_cheat_sheet.pdf) the
PyMAPDL cheat sheet. This one-page reference provides syntax rules and commands
for using PyMAPDL. 

For troubleshooting, visit 
[Troubleshooting PyMAPDL](https://mapdl.docs.pyansys.com/version/stable/user_guide/troubleshoot.html#troubleshooting-pymapdl)

On the [PyMAPDL Issues](https://github.com/ansys/pymapdl/issues) page,
you can create issues to report bugs and request new features. On the 
[PyMAPDL Discussions](https://github.com/ansys/pymapdl/discussions) page
or the  [Discussions](https://discuss.ansys.com/) page on the
[Ansys Developer portal](https://developer.ansys.com),
you can post questions, share ideas, and get community feedback. 

To reach the project support team, email [PyAnsys Core team](pyansys.core@ansys.com).
Unfortunately, this team cannot answer specific library questions or issues. You must
use the [PyMAPDL Issues](https://github.com/ansys/pymapdl/issues)
and [PyMAPDL Discussions](https://github.com/ansys/pymapdl/discussions) pages
for raising issues, request new features, and asking questions.

You can contribute to PyMAPDL by developing new features, fixing bugs, improving the documentation,
fixing typos, writing examples, etc.
To learn how to contribute to PyMAPDL, visit [Contributing section](https://mapdl.docs.pyansys.com/version/stable/getting_started/contribution.html).


## Project transition -  legacy support

This project was formerly known as ``pyansys``, and we'd like to thank
all the early adopters, contributors, and users who submitted issues,
gave feedback, and contributed code through the years.  The
``pyansys`` project has been taken up at Ansys and is being leveraged in
creating new Pythonic, cross-platform, and multi-language service-based
interfaces for Ansys's products.  Your contributions to
``pyansys`` has shaped it into a better solution.

The ``pyansys`` project is expanding beyond just MAPDL, and while
there are many new features and changes to the original Python module,
many steps have been taken to ensure compatibility with legacy code
while supporting new features.  The original Python module has been
split up into the following projects and modules:

-  [ansys.mapdl.core](https://github.com/ansys/pymapdl)
-  [ansys.mapdl.reader](https://github.com/ansys/pymapdl-reader)
-  [ansys.mapdl.corba](https://github.com/ansys/pymapdl-corba)

For more information on each project, visit their GitHub pages.

## Citing this module

If you use [PyMAPDL](https://mapdl.docs.pyansys.com/version/stable/) for
research and would like to cite the module and source, you can visit 
[pyansys Zenodo](https://zenodo.org/badge/latestdoi/70696039) and generate the
correct citation.  For example, the BibTex citation is:

```bibtex
@software{alexander_kaszynski_2020_4009467,
  author       = {Alexander Kaszynski},
  title        = {{pyansys: Pythonic interface to MAPDL}},
  month        = nov,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {0.60.3},
  doi          = {10.5281/zenodo.4009466},
  url          = {https://doi.org/10.5281/zenodo.4009466}
}
```

Because the citation here might not be current, visit the link above to obtain
the most recent citation.

## License and acknowledgments

[PyMAPDL](https://mapdl.docs.pyansys.com/) is licensed under
[the MIT license](https://github.com/ansys/pymapdl/blob/main/LICENSE).

[ansys-mapdl-core](https://pypi.org/project/ansys-mapdl-core/) package
makes no commercial claim over Ansys whatsoever.  
This tool extends the functionality of ``MAPDL`` by adding a Python
interface to the MAPDL service without changing the
core behavior or license of the original software.  The use of the
interactive APDL control of [PyMAPDL](https://mapdl.docs.pyansys.com/)
requires a legally licensed local copy of Ansys.

To get a copy of Ansys, visit [Ansys](https://www.ansys.com/).
