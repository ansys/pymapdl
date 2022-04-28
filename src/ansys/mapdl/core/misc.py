"""Module for miscellaneous functions and methods"""
from functools import wraps
import inspect
import os
import platform
import random
import re
import socket
import string
import sys
import tempfile
from threading import Thread
import weakref

import numpy as np
import scooby

from ansys.mapdl import core as pymapdl

# path of this module
MODULE_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))


def get_ansys_bin(rver):
    """Identify the ansys executable based on the release version (e.g. "201")"""
    if os.name == "nt":  # pragma: no cover
        program_files = os.getenv("PROGRAMFILES", os.path.join("c:\\", "Program Files"))
        ans_root = os.getenv(
            f"AWP_ROOT{rver}", os.path.join(program_files, "ANSYS Inc", f"v{rver}")
        )
        mapdlbin = os.path.join(ans_root, "ansys", "bin", "winx64", f"ANSYS{rver}.exe")
    else:
        ans_root = os.getenv(f"AWP_ROOT{rver}", os.path.join("/", "usr", "ansys_inc"))
        mapdlbin = os.path.join(*ans_root, f"v{rver}", "ansys", "bin", f"ansys{rver}")

    return mapdlbin


class Report(scooby.Report):
    """A class for custom scooby.Report."""

    def __init__(self, additional=None, ncol=3, text_width=80, sort=False, gpu=True):
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
            experiencing renderinng issues, pass ``False`` to safely generate
            a report.

        """
        # Mandatory packages
        core = [
            "matplotlib",
            "numpy",
            "appdirs",
            "tqdm",
            "scipy",
            "grpc",  # grpcio
            "ansys.api.mapdl.v0",  # ansys-api-mapdl-v0
            "ansys.mapdl.reader",  # ansys-mapdl-reader
            "google.protobuf",  # protobuf library
        ]

        if os.name == "linux":
            core.extend(["pexpect"])

        # Optional packages
        optional = ["matplotlib", "pyvista", "pyiges"]
        if sys.version_info[1] < 9:
            optional.append("ansys_corba")

        # Information about the GPU - bare except in case there is a rendering
        # bug that the user is trying to report.
        if gpu:
            from pyvista.utilities.errors import GPUInfo

            try:
                extra_meta = [(t[1], t[0]) for t in GPUInfo().get_info()]
            except:
                extra_meta = ("GPU Details", "error")
        else:
            extra_meta = ("GPU Details", "None")

        scooby.Report.__init__(
            self,
            additional=additional,
            core=core,
            optional=optional,
            ncol=ncol,
            text_width=text_width,
            sort=sort,
            extra_meta=extra_meta,
        )

    def mapdl_info(self):
        """Return information regarding the ansys environment and installation."""
        # this is here to avoid circular imports
        from ansys.mapdl.core.launcher import _get_available_base_ansys

        # List installed Ansys
        lines = ["", "Ansys Environment Report", "-" * 79]
        lines = ["\n", "Ansys Installation", "******************"]
        mapdl_install = _get_available_base_ansys()
        if not mapdl_install:
            lines.append("Unable to locate any Ansys installations")
        else:
            lines.append("Version   Location")
            lines.append("------------------")
            for key in sorted(mapdl_install.keys()):
                lines.append(f"{key}       {mapdl_install[key]}")
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

    def __repr__(self):
        add_text = "-" * 79 + "\nPyMAPDL Software and Environment Report"

        report = add_text + super().__repr__() + self.mapdl_info()
        return report.replace("-" * 80, "-" * 79)  # hotfix for scooby


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


def run_as_prep7(func):
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


def chunks(l, n):
    """Yield successive n-sized chunks from l"""
    for i in range(0, len(l), n):
        yield l[i : i + n]


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
        raise RuntimeError(
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


def load_file(mapdl, fname):
    """
    Provide a file to the MAPDL instance.

    If in local:
        Checks if the file exists, if not, it raises a ``FileNotFound`` exception

    If in not-local:
        Check if the file exists locally or in the working directory, if not, it will raise a ``FileNotFound`` exception.
        If the file is local, it will be uploaded.

    """
    if mapdl._local:  # pragma: no cover
        base_fname = os.path.basename(fname)
        if not os.path.exists(fname) and base_fname not in mapdl.list_files():
            raise FileNotFoundError(
                f"The file {fname} could not be found in the Python working directory ('{os.getcwd()}')"
                f"nor in the MAPDL working directory ('{mapdl.directory}')."
            )

        elif os.path.exists(fname) and base_fname in mapdl.list_files():
            warn(
                f"The file '{base_fname} is present in both, the python working directory ('{os.getcwd()}')"
                f"and in the MAPDL working directory ('{mapdl.directory}'). "
                "Using the one in the MAPDL directory.\n"
                "If you prefer to use the file in the Python directory, you can use `mapdl.upload` before this command to upload it."
            )

        elif os.path.exists(fname) and base_fname not in mapdl.list_files():
            mapdl.upload(fname)

        elif not os.path.exists(fname) and base_fname in mapdl.list_files():
            pass

    else:
        if not os.path.exists(fname) and fname not in mapdl.list_files():
            raise FileNotFoundError(
                f"The file {fname} could not be found in the local client or remote working directory."
            )
        if os.path.exists(fname):
            mapdl.upload(fname)

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
                raise RuntimeError("Information class: MAPDL exited")

            stats = self._mapdl.slashstatus("ALL")
        except Exception:  # pragma: no cover
            self._stats = None
            raise RuntimeError("Information class: MAPDL exited")

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

    @product.setter
    def product(self, value):
        """Set the value for the MAPDL Product

        .. warning:: By default, you cannot change 'product' property.

        """
        raise ValueError("The property 'product' cannot be changed.")

    @property
    @update_information_first(False)
    def mapdl_version(self):
        """Retrieve the MAPDL version from the MAPDL instance."""
        return self._get_mapdl_version()

    @mapdl_version.setter
    def mapdl_version(self, value):
        """Set the value for the MAPDL Version

        .. warning:: By default, you cannot change 'mapdl_version' property.

        """
        raise ValueError("The property 'mapdl_version' cannot be changed")

    @property
    @update_information_first(False)
    def mapdl_version_release(self):
        """Retrieve the MAPDL version release from the MAPDL instance."""
        st = self._get_mapdl_version()
        return self._get_between("RELEASE", "BUILD", st).strip()

    @mapdl_version_release.setter
    def mapdl_version_release(self, value):
        """Set the value for the MAPDL version release

        .. warning:: By default, you cannot change 'mapdl_version_release' property.

        """
        raise ValueError("The property 'mapdl_version_release' cannot be changed")

    @property
    @update_information_first(False)
    def mapdl_version_build(self):
        """Retrieve the MAPDL version build from the MAPDL instance."""
        st = self._get_mapdl_version()
        return self._get_between("BUILD", "UPDATE", st).strip()

    @mapdl_version_build.setter
    def mapdl_version_build(self, value):
        """Set the value for the MAPDL Mapdl Version Build

        .. warning:: By default, you cannot change 'mapdl_version_build' property.

        """
        raise ValueError("The property 'mapdl_version_build' cannot be changed")

    @property
    @update_information_first(False)
    def mapdl_version_update(self):
        """Retrieve the MAPDL version update from the MAPDL instance."""
        st = self._get_mapdl_version()
        return self._get_between("UPDATE", "", st).strip()

    @mapdl_version_update.setter
    def mapdl_version_update(self, value):
        """Set the value for the MAPDL Mapdl Version Update

        .. warning:: By default, you cannot change 'mapdl_version_update' property.

        """
        raise ValueError("The property 'mapdl_version_update' cannot be changed")

    @property
    @update_information_first(False)
    def pymapdl_version(self):
        """Retrieve the PyMAPDL version from the MAPDL instance."""
        return self._get_pymapdl_version()

    @pymapdl_version.setter
    def pymapdl_version(self, value):
        """Set the value for the MAPDL PyMAPDL Version

        .. warning:: By default, you cannot change 'pymapdl_version' property.

        """
        raise ValueError("The property 'pymapdl_version' cannot be changed")

    @property
    @update_information_first(False)
    def products(self):
        """Retrieve the products from the MAPDL instance."""
        return self._get_products()

    @products.setter
    def products(self, value):
        """Set the value for the MAPDL Products

        .. warning:: By default, you cannot change 'products' property.

        """
        raise ValueError("The property 'products' cannot be changed")

    @property
    @update_information_first(False)
    def preprocessing_capabilities(self):
        """Retrieve the preprocessing capabilities from the MAPDL instance."""
        return self._get_preprocessing_capabilities()

    @preprocessing_capabilities.setter
    def preprocessing_capabilities(self, value):
        """Set the value for the MAPDL Preprocessing Capabilities

        .. warning:: By default, you cannot change 'preprocessing_capabilities' property.

        """
        raise ValueError("The property 'preprocessing_capabilities' cannot be changed")

    @property
    @update_information_first(False)
    def aux_capabilities(self):
        """Retrieve the aux capabilities from the MAPDL instance."""
        return self._get_aux_capabilities()

    @aux_capabilities.setter
    def aux_capabilities(self, value):
        """Set the value for the MAPDL Aux Capabilities

        .. warning:: By default, you cannot change 'aux_capabilities' property.

        """
        raise ValueError("The property 'aux_capabilities' cannot be changed")

    @property
    @update_information_first(True)
    def solution_options(self):
        """Retrieve the solution options from the MAPDL instance."""
        return self._get_solution_options()

    @solution_options.setter
    def solution_options(self, value):
        """Set the value for the MAPDL Solution Options

        .. warning:: By default, you cannot change 'solution_options' property.

        """
        raise ValueError("The property 'solution_options' cannot be changed")

    @property
    @update_information_first(False)
    def post_capabilities(self):
        """Retrieve the post capabilities from the MAPDL instance."""
        return self._get_post_capabilities()

    @post_capabilities.setter
    def post_capabilities(self, value):
        """Set the value for the MAPDL Post Capabilities

        .. warning:: By default, you cannot change 'post_capabilities' property.

        """
        raise ValueError("The property 'post_capabilities' cannot be changed")

    @property
    @update_information_first(True)
    def titles(self):
        """Retrieve the titles from the MAPDL instance."""
        return self._get_titles()

    @titles.setter
    def titles(self, value):
        """Set the value for the MAPDL titles

        .. warning:: By default, you cannot change 'titles' property.

        """
        raise ValueError(
            "The property 'titles' cannot be changed. But you can change 'Mapdl.info.title'"
        )

    @property
    @update_information_first(True)
    def title(self):
        """Retrieve and set the title from the MAPDL instance."""
        return self._mapdl.inquire("", "title")

    @title.setter
    def title(self, title):
        """Set the value for the MAPDL title"""
        return self._mapdl.title(title)

    @property
    @update_information_first(True)
    def stitles(self, i=None):
        """Retrieve the stitle from the MAPDL instance.

        If ``i`` is supplied, only retrieve the stitle number i.
        Starting from 0 up to 3 (Python indexing).
        """
        if not i:
            return self._get_stitles()
        else:
            return self._get_stitles()[i]

    @stitles.setter
    def stitles(self, stitle, i=None):
        """Set the value for the MAPDL stitle.

        If 'stitle' includes newline characters (`\\n`), then each line
        is assigned to one STITLE.

        If 'stitle' is equals ``None``, the stitles are reset.

        If ``i`` is supplied, only set the stitle number i.

        Starting from 0 up to 3 (Python indexing).
        """
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

    def _get_stitles(self):
        return [
            re.search(f"SUBTITLE  {i}=(.*)", self._get_titles()).groups(1)[0].strip()
            for i in range(1, 5)
            if re.search(f"SUBTITLE  {i}=(.*)", self._get_titles())
        ]

    @property
    @update_information_first(True)
    def units(self):
        """Retrieve the units from the MAPDL instance."""
        return self._get_units()

    @units.setter
    def units(self, value):
        """Set the value for the MAPDL Units

        .. warning:: By default, you cannot change 'units' property.

        """
        raise ValueError("The property 'units' cannot be changed")

    @property
    @update_information_first(True)
    def scratch_memory_status(self):
        """Retrieve the scratch memory status from the MAPDL instance."""
        return self._get_scratch_memory_status()

    @scratch_memory_status.setter
    def scratch_memory_status(self, value):
        """Set the value for the MAPDL Scratch Memory Status

        .. warning:: By default, you cannot change 'scratch_memory_status' property.

        """
        raise ValueError("The property 'scratch_memory_status' cannot be changed")

    @property
    @update_information_first(True)
    def database_status(self):
        """Retrieve the database status from the MAPDL instance."""
        return self._get_database_status()

    @database_status.setter
    def database_status(self, value):
        """Set the value for the MAPDL Database Status

        .. warning:: By default, you cannot change 'database_status' property.

        """
        raise ValueError("The property 'database_status' cannot be changed")

    @property
    @update_information_first(True)
    def config_values(self):
        """Retrieve the config values from the MAPDL instance."""
        return self._get_config_values()

    @config_values.setter
    def config_values(self, value):
        """Set the value for the MAPDL Config Values

        .. warning:: By default, you cannot change 'config_values' property.

        """
        raise ValueError("The property 'config_values' cannot be changed")

    @property
    @update_information_first(True)
    def global_status(self):
        """Retrieve the global status from the MAPDL instance."""
        return self._get_global_status()

    @global_status.setter
    def global_status(self, value):
        """Set the value for the MAPDL Global Status

        .. warning:: By default, you cannot change 'global_status' property.

        """
        raise ValueError("The property 'global_status' cannot be changed")

    @property
    @update_information_first(True)
    def job_information(self):
        """Retrieve the job information from the MAPDL instance."""
        return self._get_job_information()

    @job_information.setter
    def job_information(self, value):
        """Set the value for the MAPDL Job Information

        .. warning:: By default, you cannot change 'job_information' property.

        """
        raise ValueError("The property 'job_information' cannot be changed")

    @property
    @update_information_first(True)
    def model_information(self):
        """Retrieve the model information from the MAPDL instance."""
        return self._get_model_information()

    @model_information.setter
    def model_information(self, value):
        """Set the value for the MAPDL Model Information

        .. warning:: By default, you cannot change 'model_information' property.

        """
        raise ValueError("The property 'model_information' cannot be changed")

    @property
    @update_information_first(True)
    def boundary_condition_information(self):
        """Retrieve the boundary condition information from the MAPDL instance."""
        return self._get_boundary_condition_information()

    @boundary_condition_information.setter
    def boundary_condition_information(self, value):
        """Set the value for the MAPDL Boundary Condition Information

        .. warning:: By default, you cannot change 'boundary_condition_information' property.

        """
        raise ValueError(
            "The method 'boundary_condition_information' cannot be changed"
        )

    @property
    @update_information_first(True)
    def routine_information(self):
        """Retrieve the routine information from the MAPDL instance."""
        return self._get_routine_information()

    @routine_information.setter
    def routine_information(self, value):
        """Set the value for the MAPDL Routine Information

        .. warning:: By default, you cannot change 'routine_information' property.

        """
        raise ValueError("The property 'routine_information' cannot be changed")

    @property
    @update_information_first(True)
    def solution_options_configuration(self):
        """Retrieve the solution options configuration from the MAPDL instance."""
        return self._get_solution_options_configuration()

    @solution_options_configuration.setter
    def solution_options_configuration(self, value):
        """Set the value for the MAPDL Solution Options Configuration

        .. warning:: By default, you cannot change 'solution_options_configuration' property.

        """
        raise ValueError(
            "The method 'solution_options_configuration' cannot be changed"
        )

    @property
    @update_information_first(True)
    def load_step_options(self):
        """Retrieve the load step options from the MAPDL instance."""
        return self._get_load_step_options()

    @load_step_options.setter
    def load_step_options(self, value):
        """Set the value for the MAPDL Load Step Options

        .. warning:: By default, you cannot change 'load_step_options' property.

        """
        raise ValueError("The property 'load_step_options' cannot be changed")

    def _get_between(self, init_string, end_string=None, string=None):
        if not string:
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
