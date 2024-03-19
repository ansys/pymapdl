"""Version of ansys-mapdl-core module.

On the ``main`` branch, use 'dev0' to denote a development version.
For example:

# major, minor, patch
version_info = 0, 58, 'dev0'

"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata

# Read from the pyproject.toml
# major, minor, patch
__version__ = importlib_metadata.version("ansys-mapdl-core")

# In descending order
SUPPORTED_ANSYS_VERSIONS = {
    232: "2023R2",
    231: "2023R1",
    222: "2022R2",
    221: "2022R1",
    212: "2021R2",
    211: "2021R1",
    202: "2020R2",
    201: "2020R1",
    195: "19.5",
    194: "19.4",
    193: "19.3",
    192: "19.2",
    191: "19.1",
}
