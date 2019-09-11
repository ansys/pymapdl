import re


def parse_k(msg):
    """Parse create keypoint message and return keypoint number"""
    items = re.findall("KEYPOINT NUMBER.*$", msg, re.MULTILINE)
    if items:
        return int(items[0].split('=')[-1])


def parse_l(msg):
    """Parse create line message and return line number"""
    items = re.findall("LINE NO.=.*$", msg, re.MULTILINE)
    if items:
        return int(items[0].split()[2])


def parse_a(msg):
    """Parse create area message and return area number"""
    items = re.findall("AREA NUMBER.*$", msg, re.MULTILINE)
    if items:
        return int(items[0].split('=')[-1])



geometry_commands = {'K': parse_k,
                     'L': parse_l,
                     'A': parse_a,
}
