"""
Implements a simple version check for a client/server pair.

Used when you want to verify if your server version is a minimum
value.

The decorator allows arguments within the decorator itself.

"""

# Map version tuple to MAPDL release version
VERSION_MAP = {
    (0, 0, 0): "2020R2",
    (0, 3, 0): "2021R1",
    (0, 4, 0): "2021R2",
    (0, 4, 1): "2021R2",
    (0, 5, 0): "2022R1",
    (0, 5, 1): "2022R2",  # as of 21 Mar 2022 unreleased
}


def meets_version(version, meets):
    """Check if a version string meets a minimum version.
    This is a simplified way to compare version strings. For a more robust
    tool, please check out the ``packaging`` library:
    https://github.com/pypa/packaging

    Parameters
    ----------
    version : str
        Version string.  For example ``'0.25.1'``.

    meets : str
        Version string.  For example ``'0.25.2'``.

    Returns
    -------
    newer : bool
        True if version ``version`` is greater or equal to version ``meets``.

    Examples
    --------
    >>> meets_version('0.25.1', '0.25.2')
    False
    >>> meets_version('0.26.0', '0.25.2')
    True
    """
    if not isinstance(version, tuple):
        va = version_tuple(version)
    else:
        va = version

    if not isinstance(meets, tuple):
        vb = version_tuple(meets)
    else:
        vb = meets

    if len(va) != len(vb):
        raise ValueError("Versions are not comparable.")

    for i in range(len(va)):
        if va[i] > vb[i]:
            return True
        elif va[i] < vb[i]:
            return False

    # Arrived here if same version
    return True


def version_tuple(v):
    """Convert a version string to a tuple containing ints.
    Non-numeric version strings will be converted to 0.  For example:
    ``'0.28.0dev0'`` will be converted to ``'0.28.0'``
    Returns
    -------
    ver_tuple : tuple
        Length 3 tuple representing the major, minor, and patch
        version.
    """
    split_v = v.split(".")
    while len(split_v) < 3:
        split_v.append("0")

    if len(split_v) > 3:
        raise ValueError(
            "Version strings containing more than three parts " "cannot be parsed"
        )

    vals = []
    for item in split_v:
        if item.isnumeric():
            vals.append(int(item))
        else:
            vals.append(0)

    return tuple(vals)


class VersionError(ValueError):
    """Raised when the Server is the wrong version"""

    def __init__(self, msg="Invalid Server version"):
        ValueError.__init__(self, msg)


def version_requires(min_version):
    """Ensure the method called matches a certain version.

    Example usage:

    class Client():

        def __init__(self):
            '''Connects to a fake server'''
            self._server = FakeServer()

        @version_requires((0, 1, 3))  # require 0.1.3
        def meth_a(self):
            '''calls method a on the 'server''''
            return self._server.meth_a()

        @version_requires((0, 2, 3))  # require 0.2.3
        def meth_b(self):
            '''calls method b on the 'server''''
            return self._server.meth_b()

    """

    def decorator(func):
        # first arg *must* be a tuple containing the version
        if not isinstance(min_version, tuple):
            raise TypeError(
                "version_requires decorator must include a version "
                "tuple.  For example:\n"
                "``@_version_requires((0, 1, 3))``"
            )
        if not len(min_version) == 3:
            raise TypeError(
                "version_requires decorator must include a version "
                "tuple.  For example:\n"
                "``@_version_requires((0, 1, 3))``"
            )

        def wrapper(self, *args, **kwargs):
            """Call the original function"""
            # must be called from a "Client" instance containing a server attribute
            if not hasattr(self, "_server_version"):
                raise AttributeError(
                    "decorated class must have `_server_version` " "attribute"
                )

            if not meets_version(self._server_version, min_version):

                # try to give the user a helpful warning indicating
                # the minimum version of MAPDL
                if min_version in VERSION_MAP:
                    raise VersionError(
                        f"``{func.__name__}`` requires MAPDL version "
                        f">= {VERSION_MAP[min_version]}"
                    )

                # otherwise, use the less helpful "gRPC server" version
                raise VersionError(
                    f"``{func.__name__}`` requires gRPC server "
                    f"version >= {min_version}"
                )

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
