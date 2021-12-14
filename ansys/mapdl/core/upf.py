"""User Programmable Features Library

..NOTES:

"""

import os
import inspect
from functools import wraps

from ansys.mapdl.core import LOG
from ansys.mapdl.core.mapdl import _MapdlCore

OS_ERROR = """This OS ('{os_name}') is not supported by Python UPF.
Only Linux is supported at the moment."""

BUILT_IN_ERROR = """The class needs to be written in a file, hence
interactive execution is not allowed in order to obtain the source code.
"""

UPF_HEADER = """import grpc
import sys
from mapdl import *

"""

UPF_FOOTER = """
if __name__ == '__main__':
    upf.launch( sys.argv[0])
"""

class google_dot_protobuf_dot_empty__pb2():
    """Dummy/empty class just to avoid non-defined error when using UPF"""

    def __init__(self) -> None:
        pass

    def _EMPTY(self):
        return None

class MapdlUserServiceServicer():
    pass

class MapdlUser_pb2_grpc():
    """Dummy/empty class just to avoid non-defined error when using UPF"""

    def __init__(self):
        self.MapdlUserServiceServicer = MapdlUserServiceServicer

def check_requirements(mapdl, ans_user_path):
    """Check the env variables."""
    pass


@wraps(_MapdlCore.upf)
def upf(self, filename, **kwargs):
    """Check if meeting conditions for '/UPF' command execution. 
    In case of Python UPFs, it will generate the python file."""
    ans_user_path = os.getenv('ANS_USER_PATH')

    if isinstance(filename, str):
        # Passing file path. Standard approach.

        if not os.path.exists(ans_user_path):
            raise Exception(f"The provided 'ANS_USER_PATH' ('{ans_user_path}') does not exist.")

        if not os.path.join(ans_user_path, filename):
            raise Exception(f"The provided UPF file ('{filename}') does not exist at location:\n{ans_user_path}")

        # Theoretically, UPF command only allows a file name.
        # This should be in 'ANS_USER_PATH`.

    elif isinstance(filename, MapdlUserServiceServicer):
        # passing a class (Python approach)
        if os.name != 'posix':
            raise Exception(OS_ERROR.format(os_name=os.name))

        try:
            mapdluser_str = inspect.getsource(filename)
        except TypeError as er:
            if hasattr(er, 'message'):
                if 'is a built-in class' in er.message:
                    # https://stackoverflow.com/a/35854566
                    raise TypeError(BUILT_IN_ERROR)
                else:
                    raise er
            else:
                raise er
        mapdluser_str = UPF_HEADER + mapdl_str + UPF_FOOTER
        filename = os.path.join(ans_user_path, 'user_UPF.py')

        with open(filename, 'w') as fid:
            fid.write(mapdluser_str)

    # Running original /UPF command.
    self.upf(filename, **kwargs)
