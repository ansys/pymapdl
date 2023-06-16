import inspect
import sys

from ansys.mapdl.core import LOG
from ansys.mapdl.core.misc import get_active_branch_name


def linkcode_resolve(domain, info, edit=False):
    """Determine the URL corresponding to a Python object.

    Parameters
    ----------
    domain : str
        Only useful when 'py'.

    info : dict
        With keys "module" and "fullname".

    edit : bool, default=False
        Jump right to the edit page.

    Returns
    -------
    url : str
        The code URL.

    Notes
    -----
    This function is used by the extension "sphinx.ext.linkcode" to create the "[Source]"
    button whose link is edited in this function.

    Adapted from mne (mne/utils/docs.py), which was adapted from SciPy (doc/source/conf.py).
    """
    import ansys.mapdl.core as pymapdl
    from ansys.mapdl.core import _version  # noqa: F401
    from ansys.mapdl.core import common_grpc  # noqa: F401
    from ansys.mapdl.core import convert  # noqa: F401
    from ansys.mapdl.core import docs  # noqa: F401
    from ansys.mapdl.core import logging  # noqa: F401
    from ansys.mapdl.core import mapdl  # noqa: F401
    from ansys.mapdl.core import mapdl_console  # noqa: F401
    from ansys.mapdl.core import mapdl_types  # noqa: F401
    from ansys.mapdl.core import mesh_grpc  # noqa: F401
    from ansys.mapdl.core import misc  # noqa: F401
    from ansys.mapdl.core import plotting  # noqa: F401
    from ansys.mapdl.core import post  # noqa: F401
    from ansys.mapdl.core import solution  # noqa: F401
    from ansys.mapdl.core import theme  # noqa: F401
    from ansys.mapdl.core.database import database  # noqa: F401
    from ansys.mapdl.core.database import elems  # noqa: F401
    from ansys.mapdl.core.database import nodes  # noqa: F401

    try:
        from ansys.mapdl.core import mapdl_corba  # noqa: F401
    except ImportError:
        pass
    from ansys.mapdl.core import commands  # noqa: F401
    from ansys.mapdl.core import errors  # noqa: F401
    from ansys.mapdl.core import krylov  # noqa: F401
    from ansys.mapdl.core import launcher  # noqa: F401
    from ansys.mapdl.core import licensing  # noqa: F401
    from ansys.mapdl.core import mapdl_geometry  # noqa: F401
    from ansys.mapdl.core import mapdl_grpc  # noqa: F401
    from ansys.mapdl.core import math  # noqa: F401
    from ansys.mapdl.core import parameters  # noqa: F401
    from ansys.mapdl.core import pool  # noqa: F401
    from ansys.mapdl.core import xpl  # noqa: F401
    from ansys.mapdl.core.examples import downloads  # noqa: F401
    from ansys.mapdl.core.examples import examples  # noqa: F401
    from ansys.mapdl.core.examples import verif_files  # noqa: F401
    from ansys.mapdl.core.inline_functions import core  # noqa: F401
    from ansys.mapdl.core.inline_functions import inline_functions  # noqa: F401

    if domain != "py":  # pragma: no cover
        return None

    modname = info["module"]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    if submod is None:  # pragma: no cover
        return None

    obj = submod
    fullname = fullname.replace(modname, "")

    LOG.debug("fullname")
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError:
            pass

    # deal with our decorators properly
    while hasattr(obj, "fget"):  # pragma: no cover
        obj = obj.fget

    try:
        fn = inspect.getsourcefile(obj)
    except Exception:  # pragma: no cover
        fn = None
    LOG.debug(f"Filename: {fn}")

    if not fn:  # pragma: no cover
        try:
            fn = inspect.getsourcefile(sys.modules[obj.__module__])
        except Exception:
            return None
        return None

    repo_path = str(pymapdl.__file__)

    if "site-packages" in repo_path:
        src = "site-packages"
    else:  # pragma: no cover
        src = "src"

    repo_path = repo_path[: repo_path.find(src)]

    # Replacing site-packages for source
    fn = fn.replace(repo_path, "").replace("site-packages", "src")

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:  # pragma: no cover
        lineno = None

    if lineno and not edit:
        linespec = f"#L{lineno}-L{lineno + len(source) - 1}"
    else:
        linespec = ""

    kind = get_active_branch_name()
    blob_or_edit = "edit" if edit else "blob"

    url = f"http://github.com/pyansys/pymapdl/{blob_or_edit}/{kind}/{fn}{linespec}"
    url = url.replace("\\", "/")  # For windows case

    return url
