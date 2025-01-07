# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module for report features"""
import os

from ansys.mapdl.core import _HAS_ATP, _HAS_PYANSYS_REPORT, _HAS_PYVISTA

if _HAS_PYANSYS_REPORT:
    import ansys.tools.report as pyansys_report

if _HAS_ATP:
    from ansys.tools.path import get_available_ansys_installations

ANSYS_ENV_VARS = [
    "PYMAPDL_START_INSTANCE",
    "PYMAPDL_PORT",
    "PYMAPDL_IP",
    "PYMAPDL_NPROC",
    "PYMAPDL_MAPDL_EXEC",
    "PYMAPDL_MAPDL_VERSION",
    "PYMAPDL_MAX_MESSAGE_LENGTH",
    "PYMAPDL_ON_SLURM",
    "ON_CI",
    "ON_LOCAL",
    "ON_REMOTE",
    "P_SCHEMA",
]


class Plain_Report:
    def __init__(self, core, optional=None, additional=None, **kwargs):
        """
        Base class for a plain report.


        Based on `scooby <https://github.com/banesullivan/scooby>`_ package.

        Parameters
        ----------
        additional : iter[str]
            List of packages or package names to add to output information.
        core : iter[str]
            The core packages to list first.
        optional : iter[str]
            A list of packages to list if they are available. If not available,
            no warnings or error will be thrown.
        """

        self.additional = additional
        self.core = core
        self.optional = optional
        self.kwargs = kwargs

        if os.name == "posix":
            self.core.extend(["pexpect"])

        # Information about the GPU - bare except in case there is a rendering
        # bug that the user is trying to report.
        if self.kwargs.get("gpu", False) and _HAS_PYVISTA:

            try:
                from pyvista.report import GPUInfo
            except ImportError:
                from pyvista.utilities.errors import (
                    GPUInfo,  # deprecated in pyvista 0.40.0
                )

            try:
                self.kwargs["extra_meta"] = [(t[1], t[0]) for t in GPUInfo().get_info()]
            except RuntimeError as e:  # pragma: no cover
                self.kwargs["extra_meta"] = ("GPU Details", f"Error: {str(e)}")
        else:
            self.kwargs["extra_meta"] = ("GPU Details", "None")

    def get_version(self, package):
        import importlib.metadata as importlib_metadata

        try:
            return importlib_metadata.version(package.replace(".", "-"))
        except importlib_metadata.PackageNotFoundError:
            return "Package not found"

    def __repr__(self):
        header = [
            "-" * 79,
            "\n",
            "PyMAPDL Software and Environment Report",
            "\n",
            "Packages Requirements",
            "*********************",
        ]

        core = ["\nCore packages", "-------------"]
        core.extend(
            [
                f"{each.ljust(20)}: {self.get_version(each)}"
                for each in self.core
                if self.get_version(each)
            ]
        )

        if self.optional:
            optional = ["\nOptional packages", "-----------------"]
            optional.extend(
                [
                    f"{each.ljust(20)}: {self.get_version(each)}"
                    for each in self.optional
                    if self.get_version(each)
                ]
            )
        else:
            optional = [""]

        if self.additional:
            additional = ["\nAdditional packages", "-----------------"]
            additional.extend(
                [
                    f"{each.ljust(20)}: {self.get_version(each)}"
                    for each in self.additional
                    if self.get_version(each)
                ]
            )
        else:
            additional = [""]

        return "\n".join(header + core + optional + additional) + self.mapdl_info()

    def mapdl_info(self):
        """Return information regarding the ansys environment and installation."""
        # this is here to avoid circular imports

        # List installed Ansys
        lines = ["", "Ansys Environment Report", "-" * 79]
        lines = ["\n", "Ansys Installation", "******************"]
        if _HAS_ATP:
            mapdl_install = get_available_ansys_installations()

            if not mapdl_install:
                lines.append("Unable to locate any Ansys installations")
            else:
                lines.append("Version   Location")
                lines.append("------------------")
                for key in sorted(mapdl_install.keys()):
                    lines.append(f"{abs(key)}       {mapdl_install[key]}")
        else:
            mapdl_install = None
            lines.append(
                "Unable to locate any Ansys installations because 'ansys-tools-path is not installed."
            )

        install_info = "\n".join(lines)

        env_info_lines = [
            "\n\n\nAnsys Environment Variables",
            "***************************",
        ]
        n_var = 0
        for key, value in os.environ.items():
            if "AWP" in key or "CADOE" in key or "ANSYS" in key:
                env_info_lines.append(f"{key:<30} {value}")
                n_var += 1
        if not n_var:
            env_info_lines.append("None")
        env_info = "\n".join(env_info_lines)

        return install_info + env_info


# Determine which type of report will be used (depending on the
# available packages)
if _HAS_PYANSYS_REPORT:
    base_report_class = pyansys_report.Report
else:  # pragma: no cover
    base_report_class = Plain_Report


class Report(base_report_class):
    """A class for custom scooby.Report."""

    def __init__(
        self,
        additional=None,
        ncol=3,
        text_width=80,
        sort=False,
        gpu=True,
        ansys_vars=ANSYS_ENV_VARS,
        ansys_libs=None,
    ):
        """Generate a :class:`scooby.Report` instance.

        Parameters
        ----------
        additional : list(ModuleType), list(str)
            List of packages or package names to add to output information.

        ncol : int, optional
            Number of package-columns in html table; only has effect if
            ``mode='HTML'`` or ``mode='html'``. Defaults to 3.

        text_width : int, optional
            The text width for non-HTML display modes

        sort : bool, optional
            Alphabetically sort the packages

        gpu : bool
            Gather information about the GPU. Defaults to ``True`` but if
            experiencing rendering issues, pass ``False`` to safely generate
            a report.

        ansys_vars : list of str, optional
            List containing the Ansys environment variables to be reported.
            (e.g. ["MYVAR_1", "MYVAR_2" ...]). Defaults to ``None``. Only used for
            the `pyansys-tools-report` package.

        ansys_libs : dict {str : str}, optional
            Dictionary containing the Ansys libraries and versions to be reported.
            (e.g. {"MyLib" : "v1.2", ...}). Defaults to ``None``. Only used for
            the `pyansys-tools-report` package.

        """
        # Mandatory packages
        core = [
            "ansys.mapdl.core",
            "numpy",
            "platformdirs",
            "scipy",
            "grpc",  # grpcio
            "ansys.api.mapdl.v0",  # ansys-api-mapdl-v0
            "ansys.mapdl.reader",  # ansys-mapdl-reader
            "google.protobuf",  # protobuf library
            "ansys-math-core",
        ]

        # Optional packages
        optional = [
            "matplotlib",
            "pyvista",
            "pyiges",
            "tqdm",
            "ansys-tools-visualization_interface",
            "pandas",
        ]

        if _HAS_PYANSYS_REPORT:
            #  Combine all packages into one
            all_mapdl_packages = core + optional
            if additional is not None:
                all_mapdl_packages += additional

            # Call the pyansys_report.Report constructor
            super().__init__(
                additional=all_mapdl_packages,
                ncol=ncol,
                text_width=text_width,
                sort=sort,
                gpu=gpu,
                ansys_vars=ansys_vars,
                ansys_libs=ansys_libs,
            )
        else:
            # Call the PlainReport constructor
            super().__init__(
                additional=additional,
                core=core,
                optional=optional,
                ncol=ncol,
                text_width=text_width,
                sort=sort,
                gpu=gpu,
            )
