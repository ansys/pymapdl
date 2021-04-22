"""Module for miscellaneous functions and methods"""
import tempfile
import inspect
import platform
import os
from threading import Thread
import random
import string
from functools import wraps

import scooby
import numpy as np


# path of this module
MODULE_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))


def get_ansys_bin(rver):
    """Identify the ansys executable based on the release version (e.g. "201")"""
    if os.name == 'nt':
        ans_root = 'c:/Program Files/ANSYS Inc/'
        mapdlbin = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin', 'winx64',
                                'ANSYS%s.exe' % rver)
    else:
        ans_root = '/usr/ansys_inc'
        mapdlbin = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin',
                                'ansys%s' % rver)

    return mapdlbin


class Report(scooby.Report):
    """A class for custom scooby.Report."""

    def __init__(self, additional=None, ncol=3, text_width=80, sort=False,
                 gpu=True):
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
        core = ['pyvista', 'vtk', 'numpy', 'scipy', 'appdirs',
                'ansys.mapdl.core', 'ansys.mapdl.reader']
        if os.name == 'linux':
            core.extend(['pexpect'])

        # Optional packages
        optional = ['matplotlib', 'ansys_corba']

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

        scooby.Report.__init__(self, additional=additional, core=core,
                               optional=optional, ncol=ncol,
                               text_width=text_width, sort=sort,
                               extra_meta=extra_meta)

    def __repr__(self):
        add_text = '-'*79 + '\nPyMAPDL Software and Environment Report'
        return add_text + super().__repr__()


def is_float(input_string):
    """Returns true when a string can be converted to a float"""
    try:
        float(input_string)
        return True
    except ValueError:
        return False


def random_string(stringLength=10, letters=string.ascii_lowercase):
    """Generate a random string of fixed length """
    return ''.join(random.choice(letters) for i in range(stringLength))


def _configure_pyvista():
    """Configure PyVista's ``rcParams`` for pyansys"""
    import pyvista as pv
    pv.rcParams['interactive'] = True
    pv.rcParams["cmap"] = "jet"
    pv.rcParams["font"]["family"] = "courier"
    pv.rcParams["title"] = "pyansys"
    return


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
        if prior_log_level != 'CRITICAL':
            mapdl._set_log_level('CRITICAL')

        out = func(*args, **kwargs)

        if prior_log_level != 'CRITICAL':
            mapdl._set_log_level(prior_log_level)

        return out

    return wrapper


def run_as_prep7(func):
    """Run a MAPDL method at PREP7 and always revert to the prior processor"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        mapdl = args[0]
        if hasattr(mapdl, '_mapdl'):
            mapdl = mapdl._mapdl
        prior_processor = mapdl.parameters.routine
        if prior_processor != 'PREP7':
            mapdl.prep7()

        out = func(*args, **kwargs)

        if prior_processor == 'Begin level':
            mapdl.finish()
        elif prior_processor != 'PREP7':
            mapdl.run('/%s' % prior_processor)

        return out
    return wrapper


def threaded(func):
    """Decorator to call a function using a thread"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


def threaded_daemon(func):
    """Decorator to call a function using a daemon thread."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper


def chunks(l, n):
    """ Yield successive n-sized chunks from l """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def unique_rows(a):
    """ Returns unique rows of a and indices of those rows """
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
    if platform.system() == 'Windows':
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
    letters = string.ascii_lowercase.replace('n', '')
    path = os.path.join(tmpdir, random_string(10, letters))

    # in the *rare* case of a duplicate path
    while os.path.isdir(path):
        path = os.path.join(tempfile.gettempdir(), random_string(10, letters))

    try:
        os.mkdir(path)
    except:
        raise RuntimeError('Unable to create temporary working '
                           'directory %s\n' % path +
                           'Please specify run_location=')

    return path


def no_return(func):
    """Decorator to return nothing from the wrapped function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper
