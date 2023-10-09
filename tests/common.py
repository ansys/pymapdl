"""Shared testing module"""
from collections import namedtuple
import os
from typing import Dict

from ansys.tools.path import find_mapdl

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
    _, rver = find_mapdl()

    if rver:
        rver = int(rver * 10)
        return int(rver) >= 211
    else:
        return True  # In remote mode, assume gRPC by default.


def has_dpf():
    return os.environ.get("DPF_PORT", "")


def is_smp():
    return os.environ.get("DISTRIBUTED_MODE", "smp").lower().strip() == "smp"


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
