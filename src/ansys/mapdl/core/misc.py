"""Module for miscellaneous functions and methods"""
from enum import Enum
from functools import wraps
import importlib
import inspect
import os
from pathlib import Path
import platform
import random
import re
import socket
import string
import sys
import tempfile
from threading import Thread
from warnings import warn
import weakref

from ansys.tools.path import get_available_ansys_installations
import numpy as np

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import _HAS_PYVISTA, LOG
from ansys.mapdl.core.errors import MapdlExitedError, MapdlRuntimeError

try:
    import ansys.tools.report as pyansys_report

    _HAS_PYANSYS_REPORT = True
except ModuleNotFoundError:  # pragma: no cover
    LOG.debug("The package 'pyansys-tools-report' is not installed.")
    _HAS_PYANSYS_REPORT = False

# path of this module
MODULE_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))


class ROUTINES(Enum):
    """MAPDL routines."""

    BEGIN_LEVEL = 0
    PREP7 = 17
    SOLUTION = 21
    POST1 = 31
    POST26 = 36
    AUX2 = 52
    AUX3 = 53
    AUX12 = 62
    AUX15 = 65


def check_valid_routine(routine):
    """Check if a routine is valid.

    Acceptable aliases for "Begin level" include "begin".

    Parameters
    ----------
    routine : str
        Routine. For example "PREP7".

    Returns
    -------
    bool
        ``True`` when routine is valid.

    Raises
    ------
    ValueError
        Raised when a routine is invalid.

    """
    if routine.lower().startswith("begin"):
        return True
    if not hasattr(ROUTINES, routine.upper()):
        valid_routines = []
        for item in dir(ROUTINES):
            if not item.startswith("_") and not item.startswith("BEGIN"):
                valid_routines.append(item)
        valid_routines.append("Begin level")
        valid_routines_str = "\n".join([f'\t- "{item}"' for item in valid_routines])
        raise ValueError(
            f"Invalid routine {routine}. Should be one of:\n{valid_routines_str}"
        )
    return True


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

        if self.optional is not None and sys.version_info[1] < 9:
            self.optional.append("ansys_corba")

        # Information about the GPU - bare except in case there is a rendering
        # bug that the user is trying to report.
        if self.kwargs.get("gpu", False) and _HAS_PYVISTA:
            from pyvista.utilities.errors import GPUInfo

            try:
                self.kwargs["extra_meta"] = [(t[1], t[0]) for t in GPUInfo().get_info()]
            except RuntimeError as e:  # pragma: no cover
                self.kwargs["extra_meta"] = ("GPU Details", f"Error: {str(e)}")
        else:
            self.kwargs["extra_meta"] = ("GPU Details", "None")

    def get_version(self, package):
        try:
            import importlib.metadata as importlib_metadata
        except ModuleNotFoundError:  # pragma: no cover
            import importlib_metadata

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
        mapdl_install = get_available_ansys_installations()
        if not mapdl_install:
            lines.append("Unable to locate any Ansys installations")
        else:  # pragma: no cover
            lines.append("Version   Location")
            lines.append("------------------")
            for key in sorted(mapdl_install.keys()):
                lines.append(f"{abs(key)}       {mapdl_install[key]}")
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
        ansys_vars=None,
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
            "appdirs",
            "scipy",
            "grpc",  # grpcio
            "ansys.api.mapdl.v0",  # ansys-api-mapdl-v0
            "ansys.mapdl.reader",  # ansys-mapdl-reader
            "google.protobuf",  # protobuf library
        ]

        # Optional packages
        optional = ["matplotlib", "pyvista", "pyiges", "tqdm"]

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


def is_float(input_string):
    """Returns true when a string can be converted to a float"""
    try:
        float(input_string)
        return True
    except ValueError:
        return False


def random_string(stringLength=10, letters=string.ascii_lowercase):
    """Generate a random string of fixed length"""
    return "".join(random.choice(letters) for i in range(stringLength))


def _check_has_ansys():
    """Safely wraps check_valid_ansys

    Returns
    -------
    has_ansys : bool
        True when this local installation has ANSYS installed in a
        standard location.
    """
    from ansys.mapdl.core.launcher import check_valid_ansys

    try:
        return check_valid_ansys()
    except:
        return False


def supress_logging(func):
    """Decorator to suppress logging for a MAPDL instance"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        mapdl = args[0]
        prior_log_level = mapdl._log.level
        if prior_log_level != "CRITICAL":
            mapdl._set_log_level("CRITICAL")

        out = func(*args, **kwargs)

        if prior_log_level != "CRITICAL":
            mapdl._set_log_level(prior_log_level)

        return out

    return wrapper


def run_as_prep7(func):  # Pragma: no cover
    """Run a MAPDL method at PREP7 and always revert to the prior processor"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        mapdl = args[0]
        if hasattr(mapdl, "_mapdl"):
            mapdl = mapdl._mapdl
        prior_processor = mapdl.parameters.routine
        if prior_processor != "PREP7":
            mapdl.prep7()

        out = func(*args, **kwargs)

        if prior_processor == "Begin level":
            mapdl.finish()
        elif prior_processor != "PREP7":
            mapdl.run("/%s" % prior_processor)

        return out

    return wrapper


def threaded(func):
    """Decorator to call a function using a thread"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        name = kwargs.get("name", f"Threaded `{func.__name__}` function")
        thread = Thread(target=func, name=name, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


def threaded_daemon(func):
    """Decorator to call a function using a daemon thread."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        name = kwargs.get("name", f"Threaded (with Daemon) `{func.__name__}` function")
        thread = Thread(target=func, name=name, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread

    return wrapper


def unique_rows(a):
    """Returns unique rows of a and indices of those rows"""
    if not a.flags.c_contiguous:
        a = np.ascontiguousarray(a)

    b = a.view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
    _, idx, idx2 = np.unique(b, True, True)

    return a[idx], idx, idx2


def creation_time(path_to_file):
    """The file creation time.

    Try to get the date that a file was created, falling back to when
    it was last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == "Windows":
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def last_created(filenames):
    """Return the last created file given a list of filenames

    If all filenames have the same creation time, then return the last
    filename.
    """
    ctimes = [creation_time(filename) for filename in filenames]
    idx = np.argmax(ctimes)
    if len(set(ctimes)):
        return filenames[-1]

    return filenames[idx]


def create_temp_dir(tmpdir=None):
    """Create a new unique directory at a given temporary directory"""
    if tmpdir is None:
        tmpdir = tempfile.gettempdir()
    elif not os.path.isdir(tmpdir):
        os.makedirs(tmpdir)

    # running into a rare issue with MAPDL on Windows with "\n" being
    # treated literally.
    letters = string.ascii_lowercase.replace("n", "")
    path = os.path.join(tmpdir, random_string(10, letters))

    # in the *rare* case of a duplicate path
    while os.path.isdir(path):
        path = os.path.join(tempfile.gettempdir(), random_string(10, letters))

    try:
        os.mkdir(path)
    except:
        raise MapdlRuntimeError(
            "Unable to create temporary working "
            "directory %s\n" % path + "Please specify run_location="
        )

    return path


def no_return(func):
    """Decorator to return nothing from the wrapped function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    return wrapper


def get_bounding_box(nodes_xyz):
    min_ = np.min(nodes_xyz, axis=0)
    max_ = np.max(nodes_xyz, axis=0)

    return max_ - min_


def load_file(mapdl, fname, priority_mapdl_file=None):
    """
    Provide a file to the MAPDL instance.

    Parameters
    ----------
    mapdl
      Mapdl instance

    fname : str, path
      Path to the file.

    priority_mapdl_file : bool
      In case of the file existing in the MAPDL environment and
      in the local Python environment, this parameter specifies
      which one has priority. Defaults to ``True``, meaning the MAPDL file
      has priority.

    Notes
    -----

    **When running MAPDL locally:**

    Checks if the file is reachable or is in the MAPDL directory,
    if not, it raises a ``FileNotFound`` exception.

    If:

    - The file is only the MAPDL directory, this function does nothing
      since the file is already accessible to the MAPDL instance.

    - If the file exists in both, the Python working directory and the MAPDL
      directory, this function does nothing, as the file in the MAPDL working
      directory has priority.

    **When in remote (not-local)**

    Check if the file exists locally or in the working directory, if not, it will raise a ``FileNotFound`` exception.
    If the file is local, it will be uploaded.

    """

    base_fname = os.path.basename(fname)
    if not os.path.exists(fname) and base_fname not in mapdl.list_files():
        raise FileNotFoundError(
            f"The file {fname} could not be found in the Python working directory ('{os.getcwd()}') "
            f"nor in the MAPDL working directory ('{mapdl.directory}')."
        )

    elif os.path.exists(fname) and base_fname in mapdl.list_files():  # pragma: no cover
        if priority_mapdl_file is None:
            warn(
                f"The file '{base_fname}' is present in both, the python working directory ('{os.getcwd()}') "
                f"and in the MAPDL working directory ('{mapdl.directory}'). "
                "Using the one already in the MAPDL directory.\n"
                "If you prefer to use the file in the Python directory, you shall remove the file in the MAPDL directory."
            )
            priority_mapdl_file = True

        if not priority_mapdl_file:
            mapdl.upload(fname)

    elif os.path.exists(fname) and base_fname not in mapdl.list_files():
        mapdl._log.debug("File is in the Python working directory, uploading.")
        mapdl.upload(fname)

    elif (
        not os.path.exists(fname) and base_fname in mapdl.list_files()
    ):  # pragma: no cover
        mapdl._log.debug("File is already in the MAPDL working directory")

    # Simplifying name for MAPDL reads it.
    return os.path.basename(fname)


def check_valid_ip(ip):
    """Check for valid IP address"""
    if ip.lower() != "localhost":
        ip = ip.replace('"', "").replace("'", "")
        socket.inet_aton(ip)


def check_valid_port(port, lower_bound=1000, high_bound=60000):
    if not isinstance(port, int):
        raise ValueError("The 'port' parameter should be an integer.")

    if lower_bound < port < high_bound:
        return
    else:
        raise ValueError(
            f"'port' values should be between {lower_bound} and {high_bound}."
        )


def check_valid_start_instance(start_instance):
    """
    Checks if the value obtained from the environmental variable is valid.

    Parameters
    ----------
    start_instance : str
        Value obtained from the corresponding environment variable.

    Returns
    -------
    bool
        Returns ``True`` if ``start_instance`` is ``True`` or ``"True"``,
        ``False`` if otherwise.

    """
    if not isinstance(start_instance, (str, bool)):
        raise ValueError("The value 'start_instance' should be an string or a boolean.")

    if isinstance(start_instance, bool):
        return start_instance

    if start_instance.lower() not in ["true", "false"]:
        raise ValueError(
            f"The value 'start_instance' should be equal to 'True' or 'False' (case insensitive)."
        )

    return start_instance.lower() == "true"


def update_information_first(update=False):
    """
    Decorator to wrap :class:`Information <ansys.mapdl.core.misc.Information>`
    methods to force update the fields when accessed.

    Parameters
    ----------
    update : bool, optional
        If ``True``, the class information is updated by calling ``/STATUS``
        before accessing the methods. By default ``False``
    """

    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            if update or not self._stats:
                self._update()
            return function(self, *args, **kwargs)

        return wrapper

    return decorator


class Information:
    """
    This class provide some MAPDL information from ``/STATUS`` MAPDL command.

    It is also the object that is called when you issue ``print(mapdl)``,
    which means ``print`` calls ``mapdl.info.__str__()``.

    Notes
    -----
    You cannot directly modify the values of this class.

    Some of the results are cached for later calls.

    Examples
    --------
    >>> mapdl.info
    Product:             Ansys Mechanical Enterprise
    MAPDL Version:       21.2
    ansys.mapdl Version: 0.62.dev0

    >>> print(mapdl)
    Product:             Ansys Mechanical Enterprise
    MAPDL Version:       21.2
    ansys.mapdl Version: 0.62.dev0

    >>> mapdl.info.product
    'Ansys Mechanical Enterprise'

    >>> info = mapdl.info
    >>> info.mapdl_version
    'RELEASE  2021 R2           BUILD 21.2      UPDATE 20210601'

    """

    def __init__(self, mapdl):
        """Class Initializer"""
        from ansys.mapdl.core.mapdl import _MapdlCore  # lazy import to avoid circular

        if not isinstance(mapdl, _MapdlCore):  # pragma: no cover
            raise TypeError("Must be implemented from MAPDL class")

        self._mapdl_weakref = weakref.ref(mapdl)
        self._stats = None
        self._repr_keys = {
            "Product": "product",
            "MAPDL Version": "mapdl_version",
            "PyMAPDL Version": "pymapdl_version",
        }

    @property
    def _mapdl(self):
        """Return the weakly referenced MAPDL instance."""
        return self._mapdl_weakref()

    def _update(self):
        """We might need to do more calls if we implement properties
        that change over the MAPDL session."""
        try:
            if self._mapdl._exited:  # pragma: no cover
                raise MapdlExitedError("Information class: MAPDL exited")

            stats = self._mapdl.slashstatus("ALL")
        except Exception:  # pragma: no cover
            self._stats = None
            raise MapdlExitedError("Information class: MAPDL exited")

        stats = stats.replace("\n ", "\n")  # Bit of formatting
        self._stats = stats
        self._mapdl._log.debug("Information class: Updated")

    def __repr__(self):
        if not self._stats:  # pragma: no cover
            self._update()

        return "\n".join(
            [
                f"{each_name}:".ljust(25) + f"{getattr(self, each_attr)}".ljust(25)
                for each_name, each_attr in self._repr_keys.items()
            ]
        )

    @property
    @update_information_first(False)
    def product(self):
        """Retrieve the product from the MAPDL instance."""
        return self._get_product()

    @property
    @update_information_first(False)
    def mapdl_version(self):
        """Retrieve the MAPDL version from the MAPDL instance."""
        return self._get_mapdl_version()

    @property
    @update_information_first(False)
    def mapdl_version_release(self):
        """Retrieve the MAPDL version release from the MAPDL instance."""
        st = self._get_mapdl_version()
        return self._get_between("RELEASE", "BUILD", st).strip()

    @property
    @update_information_first(False)
    def mapdl_version_build(self):
        """Retrieve the MAPDL version build from the MAPDL instance."""
        st = self._get_mapdl_version()
        return self._get_between("BUILD", "UPDATE", st).strip()

    @property
    @update_information_first(False)
    def mapdl_version_update(self):
        """Retrieve the MAPDL version update from the MAPDL instance."""
        st = self._get_mapdl_version()
        return self._get_between("UPDATE", "", st).strip()

    @property
    @update_information_first(False)
    def pymapdl_version(self):
        """Retrieve the PyMAPDL version from the MAPDL instance."""
        return self._get_pymapdl_version()

    @property
    @update_information_first(False)
    def products(self):
        """Retrieve the products from the MAPDL instance."""
        return self._get_products()

    @property
    @update_information_first(False)
    def preprocessing_capabilities(self):
        """Retrieve the preprocessing capabilities from the MAPDL instance."""
        return self._get_preprocessing_capabilities()

    @property
    @update_information_first(False)
    def aux_capabilities(self):
        """Retrieve the aux capabilities from the MAPDL instance."""
        return self._get_aux_capabilities()

    @property
    @update_information_first(True)
    def solution_options(self):
        """Retrieve the solution options from the MAPDL instance."""
        return self._get_solution_options()

    @property
    @update_information_first(False)
    def post_capabilities(self):
        """Retrieve the post capabilities from the MAPDL instance."""
        return self._get_post_capabilities()

    @property
    @update_information_first(True)
    def titles(self):
        """Retrieve the titles from the MAPDL instance."""
        return self._get_titles()

    @property
    @update_information_first(True)
    def title(self):
        """Retrieve and set the title from the MAPDL instance."""
        return self._mapdl.inquire("", "title")

    @title.setter
    def title(self, title):
        return self._mapdl.title(title)

    @property
    @update_information_first(True)
    def stitles(self, i=None):
        """Retrieve or set the value for the MAPDL stitle (subtitles).

        If 'stitle' includes newline characters (`\\n`), then each line
        is assigned to one STITLE.

        If 'stitle' is equals ``None``, the stitles are reset.

        If ``i`` is supplied, only set the stitle number i.

        Starting from 0 up to 3 (Python indexing).
        """
        if not i:
            return self._get_stitles()
        else:
            return self._get_stitles()[i]

    @stitles.setter
    def stitles(self, stitle, i=None):
        if stitle is None:
            # Case to empty
            stitle = ["", "", "", ""]

        if not isinstance(stitle, (str, list)):
            raise ValueError("Only str or list are allowed for stitle")

        if isinstance(stitle, str):
            if "\n" in stitle:
                stitle = stitle.splitlines()
            else:
                stitle = "\n".join(
                    [stitle[ii : ii + 70] for ii in range(0, len(stitle), 70)]
                )

        if any([len(each) > 70 for each in stitle]):
            raise ValueError("The number of characters per subtitle is limited to 70.")

        if not i:
            for each_index, each_stitle in zip(range(1, 5), stitle):
                self._mapdl.stitle(each_index, each_stitle)
        else:
            self._mapdl.stitle(i, stitle)

    @property
    @update_information_first(True)
    def units(self):
        """Retrieve the units from the MAPDL instance."""
        return self._get_units()

    @property
    @update_information_first(True)
    def scratch_memory_status(self):
        """Retrieve the scratch memory status from the MAPDL instance."""
        return self._get_scratch_memory_status()

    @property
    @update_information_first(True)
    def database_status(self):
        """Retrieve the database status from the MAPDL instance."""
        return self._get_database_status()

    @property
    @update_information_first(True)
    def config_values(self):
        """Retrieve the config values from the MAPDL instance."""
        return self._get_config_values()

    @property
    @update_information_first(True)
    def global_status(self):
        """Retrieve the global status from the MAPDL instance."""
        return self._get_global_status()

    @property
    @update_information_first(True)
    def job_information(self):
        """Retrieve the job information from the MAPDL instance."""
        return self._get_job_information()

    @property
    @update_information_first(True)
    def model_information(self):
        """Retrieve the model information from the MAPDL instance."""
        return self._get_model_information()

    @property
    @update_information_first(True)
    def boundary_condition_information(self):
        """Retrieve the boundary condition information from the MAPDL instance."""
        return self._get_boundary_condition_information()

    @property
    @update_information_first(True)
    def routine_information(self):
        """Retrieve the routine information from the MAPDL instance."""
        return self._get_routine_information()

    @property
    @update_information_first(True)
    def solution_options_configuration(self):
        """Retrieve the solution options configuration from the MAPDL instance."""
        return self._get_solution_options_configuration()

    @property
    @update_information_first(True)
    def load_step_options(self):
        """Retrieve the load step options from the MAPDL instance."""
        return self._get_load_step_options()

    def _get_between(self, init_string, end_string=None, string=None):
        if not string:
            self._update()
            string = self._stats

        st = string.find(init_string) + len(init_string)

        if not end_string:
            en = None
        else:
            en = string.find(end_string)
        return "\n".join(string[st:en].splitlines()).strip()

    def _get_product(self):
        return self._get_products().splitlines()[0]

    def _get_mapdl_version(self):
        titles_ = self._get_titles()
        st = titles_.find("RELEASE")
        en = titles_.find("INITIAL", st)
        return titles_[st:en].split("CUSTOMER")[0].strip()

    def _get_pymapdl_version(self):
        return pymapdl.__version__

    def _get_title(self):
        match = re.match(r"TITLE=(.*)$", self._get_titles())
        if match:
            return match.groups(1)[0].strip()

    def _get_stitles(self):
        return [
            re.search(f"SUBTITLE  {i}=(.*)", self._get_titles()).groups(1)[0].strip()
            if re.search(f"SUBTITLE  {i}=(.*)", self._get_titles())
            else ""
            for i in range(1, 5)
        ]

    def _get_products(self):
        init_ = "*** Products ***"
        end_string = "*** PreProcessing Capabilities ***"
        return self._get_between(init_, end_string)

    def _get_preprocessing_capabilities(self):
        init_ = "*** PreProcessing Capabilities ***"
        end_string = "*** Aux Capabilities ***"
        return self._get_between(init_, end_string)

    def _get_aux_capabilities(self):
        init_ = "*** Aux Capabilities ***"
        end_string = "*** Solution Options ***"
        return self._get_between(init_, end_string)

    def _get_solution_options(self):
        init_ = "*** Solution Options ***"
        end_string = "*** Post Capabilities ***"
        return self._get_between(init_, end_string)

    def _get_post_capabilities(self):
        init_ = "*** Post Capabilities ***"
        end_string = "***** TITLES *****"
        return self._get_between(init_, end_string)

    def _get_titles(self):
        init_ = "***** TITLES *****"
        end_string = "***** UNITS *****"
        return self._get_between(init_, end_string)

    def _get_units(self):
        init_ = "***** UNITS *****"
        end_string = "***** SCRATCH MEMORY STATUS *****"
        return self._get_between(init_, end_string)

    def _get_scratch_memory_status(self):
        init_ = "***** SCRATCH MEMORY STATUS *****"
        end_string = "*****    DATABASE STATUS    *****"
        return self._get_between(init_, end_string)

    def _get_database_status(self):
        init_ = "*****    DATABASE STATUS    *****"
        end_string = "***** CONFIG VALUES *****"
        return self._get_between(init_, end_string)

    def _get_config_values(self):
        init_ = "***** CONFIG VALUES *****"
        end_string = "G L O B A L   S T A T U S"
        return self._get_between(init_, end_string)

    def _get_global_status(self):
        init_ = "G L O B A L   S T A T U S"
        end_string = "J O B   I N F O R M A T I O N"
        return self._get_between(init_, end_string)

    def _get_job_information(self):
        init_ = "J O B   I N F O R M A T I O N"
        end_string = "M O D E L   I N F O R M A T I O N"
        return self._get_between(init_, end_string)

    def _get_model_information(self):
        init_ = "M O D E L   I N F O R M A T I O N"
        end_string = "B O U N D A R Y   C O N D I T I O N   I N F O R M A T I O N"
        return self._get_between(init_, end_string)

    def _get_boundary_condition_information(self):
        init_ = "B O U N D A R Y   C O N D I T I O N   I N F O R M A T I O N"
        end_string = "R O U T I N E   I N F O R M A T I O N"
        return self._get_between(init_, end_string)

    def _get_routine_information(self):
        init_ = "R O U T I N E   I N F O R M A T I O N"
        end_string = None
        return self._get_between(init_, end_string)

    def _get_solution_options_configuration(self):
        init_ = "S O L U T I O N   O P T I O N S"
        end_string = "L O A D   S T E P   O P T I O N S"
        return self._get_between(init_, end_string)

    def _get_load_step_options(self):
        init_ = "L O A D   S T E P   O P T I O N S"
        end_string = None
        return self._get_between(init_, end_string)


def write_array(filename, array):
    """
    Write an array to a file.

    This function aim to replace
    ``ansys.mapdl.reader._reader write_array``.

    Parameters
    ----------
    filename : str
        Name of the file.
    array : numpy.ndarray
        Array.
    """
    np.savetxt(filename, array, fmt="%20.12f")  # pragma: no cover


def requires_package(package_name, softerror=False):
    """
    Decorator check whether a package is installed or not.

    If it is not, it will return None.

    Parameters
    ----------
    package_name : str
        Name of the package.
    """

    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            try:
                importlib.import_module(package_name)
                return function(self, *args, **kwargs)

            except ModuleNotFoundError:
                msg = (
                    f"To use the method '{function.__name__}', "
                    f"the package '{package_name}' is required.\n"
                    f"Please try to install '{package_name}' with:\n"
                    f"pip install {package_name.replace('.','-') if 'ansys' in package_name else package_name}"
                )

                if softerror:
                    warn(msg)
                    return None
                else:
                    raise ModuleNotFoundError(msg)

        return wrapper

    return decorator


def _get_args_xsel(*args, **kwargs):
    type_ = kwargs.pop("type_", str(args[0]) if len(args) else "").upper()
    item = kwargs.pop("item", str(args[1]) if len(args) > 1 else "").upper()
    comp = kwargs.pop("comp", str(args[2]) if len(args) > 2 else "").upper()
    vmin = kwargs.pop("vmin", args[3] if len(args) > 3 else "")
    vmax = kwargs.pop("vmax", args[4] if len(args) > 4 else "")
    vinc = kwargs.pop("vinc", args[5] if len(args) > 5 else "")
    kabs = kwargs.pop("kabs", args[6] if len(args) > 6 else "")
    return type_, item, comp, vmin, vmax, vinc, kabs, kwargs


def allow_pickable_points(entity="node", plot_function="nplot"):
    """
    This wrapper opens a window with the NPLOT or KPLOT, and get the selected points (Nodes or kp),
    and feed them as a list to the NSEL.
    """

    def decorator(orig_nsel):
        @wraps(orig_nsel)
        def wrapper(self, *args, **kwargs):
            type_, item, comp, vmin, vmax, vinc, kabs, kwargs = _get_args_xsel(
                *args, **kwargs
            )

            if item == "P" and _HAS_PYVISTA:
                if type_ not in ["S", "R", "A", "U"]:
                    raise ValueError(
                        f"The 'item_' argument ('{item}') together with the 'type_' argument ('{type_}') are not allowed."
                    )

                previous_picked_points = set(self._get_selected_(entity))

                if type_ in ["S", "A"]:  # selecting all the entities
                    orig_nsel(self, "all")

                plotting_function = getattr(self, plot_function)
                pl = plotting_function(return_plotter=True)

                vmin = self._pick_points(
                    entity, pl, type_, previous_picked_points, **kwargs
                )

                if len(vmin) == 0:
                    # aborted picking
                    orig_nsel(self, "S", entity, "", previous_picked_points, **kwargs)
                    return []

                item = entity
                comp = ""

                # to make return the array of points when using P
                kwargs["Used_P"] = True

                return orig_nsel(
                    self, "S", item, comp, vmin, vmax, vinc, kabs, **kwargs
                )

            else:
                return orig_nsel(
                    self, type_, item, comp, vmin, vmax, vinc, kabs, **kwargs
                )

        return wrapper

    return decorator


def wrap_point_SEL(entity="node"):
    def decorator(original_sel_func):
        """
        This function wraps a NSEL or KSEL function to allow using a list/tuple/array for vmin argument.

        This allows for example:

        >>> mapdl.nsel("S", "node", "", [1, 2, 3])  # select nodes 1, 2, and 3.
        """

        @wraps(original_sel_func)
        def wrapper(self, *args, **kwargs):
            type_, item, comp, vmin, vmax, vinc, kabs, kwargs = _get_args_xsel(
                *args, **kwargs
            )

            if isinstance(vmin, (set, tuple, list, np.ndarray)):
                if kwargs.get("Used_P", False) and (
                    (isinstance(vmin, np.ndarray) and vmin.size != 0) or len(vmin) == 0
                ):
                    # edge case where during the picking we have selected nothing.
                    # In that case, we just silently quit NSEL command. We do **not**
                    # want to unselect everything (case in scripting where
                    # ``mapdl.nsel("S","node", "", [])`` unselect everything).
                    return

                self.run(
                    f"/com, Selecting {entity}s from an iterable (i.e. set, list, tuple, or array)"
                )  # To have a clue in the apdl log file

                if vmax or vinc:
                    raise ValueError(
                        "If an iterable is used as 'vmin' argument, "
                        "it is not allowed to use 'vmax' or 'vinc' arguments."
                    )

                if len(vmin) == 0 and type_ == "S":
                    # assuming you want to select nothing because you supplied an empty list/tuple/array
                    return original_sel_func(self, "none")

                self._perform_entity_list_selection(
                    entity, original_sel_func, type_, item, comp, vmin, kabs
                )

                if kwargs.pop("Used_P", False):
                    # we want to return the
                    return np.array(vmin)
                else:
                    return
            else:
                return original_sel_func(
                    self,
                    type_=type_,
                    item=item,
                    comp=comp,
                    vmin=vmin,
                    vmax=vmax,
                    vinc=vinc,
                    kabs=kabs,
                    **kwargs,
                )

        return wrapper

    return decorator


def get_active_branch_name():
    head_dir = Path(".") / ".git" / "HEAD"

    if os.path.exists(head_dir):
        with head_dir.open("r") as f:
            content = f.read().splitlines()

        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]

    # In case the previous statements return None
    if "dev" in pymapdl.__version__:
        kind = "main"
    else:  # pragma: no cover
        kind = f"release/{'.'.join(pymapdl.__version__.split('.')[:2])}"

    return kind
