import re


def parse_et(msg):
    """
    Parse local element type number definition message
    and return element type number
    """
    res = re.search(r"(ELEMENT TYPE\s*)([0-9]+)", msg)
    if res is not None:
        result = int(res.group(2))
    else:
        result = None
    return result


element_commands = {'ET': parse_et,
}
