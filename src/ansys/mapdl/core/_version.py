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
SUPPORTED_ANSYS_VERSIONS = [222, 221, 212, 211, 202, 201, 195, 194, 193, 192, 191]
