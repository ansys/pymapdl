from typing import Dict, Tuple
from collections import namedtuple


Node = namedtuple('Node', ['number', 'x', 'y', 'z',
                           'thx', 'thy', 'thz'])
Element = namedtuple('Element', ['number', 'material', 'type',
                                 'real_const', 'coord_system',
                                 'section', 'node_numbers'])


def get_details_of_nodes(mapdl_) -> Dict[int, Node]:
    string = mapdl_.nlist('ALL')
    string = string.split(' NODE ')[1]
    string = string.split('\n', 1)[1]
    rows = string.split('\n')
    nodes = {}
    for row in rows:
        row_values = [v for v in row.split(' ') if v != '']
        node = int(row_values[0])
        nodes[node] = Node(node, *[float(rv) for rv in row_values[1:]])
    return nodes


def get_details_of_elements(mapdl_) -> Dict[int, Node]:
    string = mapdl_.elist('ALL')
    string = string.split(' ELEM ')[1]
    string = string.split('\n', 1)[1]
    rows = string.split('\n')
    elements = {}
    for row in rows:
        if bool(row.strip()):
            row_values = [v for v in row.split(' ') if v != '']
            args = [int(rv) for rv in row_values[:6]]
            nodes = [int(rv) for rv in row_values[6:]]
            elements[args[0]] = Element(*args, node_numbers=nodes)
    return elements
