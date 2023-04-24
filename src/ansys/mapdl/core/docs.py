import inspect
import sys


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
    This has been adapted to deal with our "verbose" decorator.

    Adapted from mne (mne/utils/docs.py), which was adapted from SciPy (doc/source/conf.py).
    """
    import ansys.mapdl.core as pymapdl

    if domain != "py":
        return None

    modname = info["module"]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    fullname = fullname.replace(modname, "")

    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError:
            pass

    # deal with our decorators properly
    while hasattr(obj, "fget"):
        obj = obj.fget

    try:
        fn = inspect.getsourcefile(obj)
    except Exception:  # pragma: no cover
        fn = None

    if not fn:  # pragma: no cover
        try:
            fn = inspect.getsourcefile(sys.modules[obj.__module__])
        except Exception:
            return None
        return None

    repo_path = pymapdl.__file__
    repo_path = repo_path[: repo_path.index("src")]
    fn = fn.replace(repo_path, "")

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:  # pragma: no cover
        lineno = None

    if lineno and not edit:
        linespec = f"#L{lineno}-L{lineno + len(source) - 1}"
    else:
        linespec = ""

    if "dev" in pymapdl.__version__:
        kind = "main"
    else:  # pragma: no cover
        kind = f"release/{'.'.join(pymapdl.__version__.split('.')[:2])}"

    blob_or_edit = "edit" if edit else "blob"

    return f"http://github.com/pyansys/pymapdl/{blob_or_edit}/{kind}/{fn}{linespec}"
