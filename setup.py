"""Installation file for ansys-mapdl-core"""
import sys
import struct
import os
from io import open as io_open

from setuptools import setup, find_namespace_packages


# Get version from version info
__version__ = None
this_file = os.path.dirname(__file__)
version_file = os.path.join(this_file, "ansys", "mapdl", "core", "_version.py")
with io_open(version_file, mode="r") as fd:
    # execute file from raw string
    exec(fd.read())

install_requires = [
    "matplotlib>=3.0.0",  # for colormaps for pyvista
    "numpy>=1.14.0",
    "pyvista>=0.33.0",
    "appdirs>=1.4.0",
    "tqdm>=4.45.0",
    "pyiges>=0.1.4",
    "scipy>=1.3.0",  # for sparse (consider optional?)
    "grpcio>=1.30.0",  # tested up to grpcio==1.35
    "ansys-api-mapdl-v0==0.4.1",  # supports at least 2020R2 - 2021R2
    "ansys-mapdl-reader>=0.50.15",
    "protobuf>=3.12.2",  # minimum required based on latest ansys-grpc-mapdl
]
# 'grpcio-health-checking>=1.30.0',

# for CORBA
# pending depreciation to ansys-mapdl-corba
if sys.version_info[1] < 9:
    install_requires.append("ansys-corba")


# these are only used when launching a MAPDL via a console.  This
# feature is subject to be removed or moved out of this module.
if os.name == "linux":
    install_requires.extend(["pexpect>=4.8.0"])


# perform python version checking
# this is necessary to avoid the new pip package checking as vtk does
# not support Python 3.9 or any 32-bit as of 17 June 2021.
is64 = struct.calcsize("P") * 8 == 64
if not is64:
    raise RuntimeError(
        "\n\n``ansys-mapdl-reader`` requires 64-bit Python\n"
        "Please check the version of Python installed at\n"
        "%s" % sys.executable
    )


packages = []
for package in find_namespace_packages(include="ansys*"):
    if package.startswith("ansys.mapdl.core"):
        packages.append(package)


setup(
    name="ansys-mapdl-core",
    packages=packages,
    version=__version__,
    description="Python interface to MAPDL Service",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    url="https://github.com/pyansys/pymapdl",
    python_requires=">=3.7.*",
    keywords="ANSYS MAPDL gRPC",
    package_data={"ansys.mapdl.core.examples": ["verif/*.dat", "wing.dat"]},
    install_requires=install_requires,
)
