# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Shared testing module"""
from collections import namedtuple
import os
from typing import Dict

from ansys.mapdl.core.launcher import _is_ubuntu

Node = namedtuple("Node", ["number", "x", "y", "z", "thx", "thy", "thz"])
Element = namedtuple(
    "Element",
    [
        "number",
        "material",
        "type",
        "real_const",
        "coord_system",
        "section",
        "node_numbers",
    ],
)


# Set if on local
def is_on_local():
    if "ON_LOCAL" in os.environ:
        return os.environ.get("ON_LOCAL", "").lower() == "true"

    if "ON_REMOTE" in os.environ:
        return os.environ.get("ON_REMOTE", "").lower() == "true"

    if os.environ.get("PYMAPDL_START_INSTANCE", None):
        return (
            os.environ.get("PYMAPDL_START_INSTANCE", "").lower() != "false"
        )  # default is false

    from ansys.tools.path import find_mapdl

    _, rver = find_mapdl()

    if rver:
        return True
    else:
        return False


# Set if on CI
def is_on_ci():
    return os.environ.get("ON_CI", "").lower() == "true"


# Set if on ubuntu
def is_on_ubuntu():
    envvar = os.environ.get("ON_UBUNTU", None)

    if envvar is not None:
        return envvar.lower() == "true"

    return _is_ubuntu()


def has_grpc():
    envvar = os.environ.get("HAS_GRPC", None)

    if envvar is not None:
        return envvar.lower().strip() == "true"

    if testing_minimal():
        return True

    try:
        from ansys.tools.path import find_mapdl
    except ModuleNotFoundError:
        return True

    _, rver = find_mapdl()

    if rver:
        rver = int(rver * 10)
        return int(rver) >= 211
    else:
        return True  # In remote mode, assume gRPC by default.


def has_dpf():
    return bool(os.environ.get("DPF_PORT", ""))


def is_smp():
    return os.environ.get("DISTRIBUTED_MODE", "smp").lower().strip() == "smp"


def support_plotting():
    envvar = os.environ.get("SUPPORT_PLOTTING", None)

    if envvar is not None:
        return envvar.lower().strip() == "true"

    if testing_minimal():
        return False

    try:
        import pyvista

        return pyvista.system_supports_plotting()

    except ModuleNotFoundError:
        return False


def is_running_on_student():
    return os.environ.get("ON_STUDENT", "NO").upper().strip() in ["YES", "TRUE"]


def testing_minimal():
    return os.environ.get("TESTING_MINIMAL", "NO").upper().strip() in ["YES", "TRUE"]


def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_just_floats(s: str, delimiter=None):
    if delimiter is None:
        entries = s.split()
    else:
        entries = s.split(delimiter)
    if not entries:
        return False
    for entry in entries:
        if not is_float(entry.strip()):
            return False
    return True


def get_details_of_nodes(mapdl_) -> Dict[int, Node]:
    string = mapdl_.nlist("ALL")
    rows = string.split("\n")
    nodes = {}
    for row in rows:
        if is_just_floats(row):
            row_values = [v for v in row.split(" ") if v != ""]
            node = int(row_values[0])
            nodes[node] = Node(node, *[float(rv) for rv in row_values[1:]])
    return nodes


def get_details_of_elements(mapdl_) -> Dict[int, Node]:
    string = mapdl_.elist("ALL")
    # string = string.split(' ELEM ')[1]
    # string = string.split('\n', 1)[1]
    rows = string.split("\n")
    elements = {}
    for row in rows:
        if is_just_floats(row):
            row_values = [v for v in row.split(" ") if v != ""]
            args = [int(rv) for rv in row_values[:6]]
            # todo: Node numbers can go over multiple lines, which makes
            #  parsing them properly a real pain. So for now I'll leave
            #  this as is and work on a better version in the future
            if len(args) == 6:
                elements[args[0]] = Element(*args, node_numbers=None)
    return elements
