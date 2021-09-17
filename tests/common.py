"""Shared testing module"""
from collections import namedtuple
from typing import Dict

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
