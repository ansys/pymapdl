"""Miscellaneous methods not covered in the documentation."""


def verify(self, case='', level='', **kwargs):
    """Enter the verification run mode.

    .. note::
       This command is only valid at the ``/BEGIN`` level, obtained
       with ``mapdl.finish()``.

    Parameters
    ----------
    case : str, optional
        Optional title of the verification manual file.  Also accepts
        ``'OFF'`` to disable the verification run mode.

    level : int, optional
        Verification level ranging from 1 to 6 defaulting to 4.

    Returns
    --------

    Examples
    --------
    Enter the verification routine with the default option.

    >>> mapdl.finish()
    >>> mapdl.verify('VM1')
    '*** VERIFICATION RUN - CASE VM1                              ***  OPTION=  4'

    """
    return self.run(f'/VERIFY,{case},{level}', **kwargs)
