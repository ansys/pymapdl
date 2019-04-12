"""Methods common to binary files

"""
import struct
import numpy as np


def read_table(f, dtype='i', nread=None, skip=False, get_nread=True):
    """ read fortran style table """
    if get_nread:
        n = np.fromfile(f, 'i', 1)
        if not n:
            raise Exception('end of file')

        tablesize = n[0]
        f.seek(4, 1)  # skip padding

    # override
    if nread:
        tablesize = nread

    if skip:
        f.seek((tablesize + 1)*4, 1)
        return
    else:
        if dtype == 'double':
            tablesize //= 2
        table = np.fromfile(f, dtype, tablesize)
    f.seek(4, 1)  # skip padding
    return table



def read_string_from_binary(f, n):
    """ Read n 4 character binary strings from a file opend in binary mode """
    string = b''
    for i in range(n):
        string += f.read(4)[::-1]

    try:
        return string.decode('utf')
    except:
        return string


def parse_header(table, keys):
    """ parses a header from a table """
    header = {}
    for i, key in enumerate(keys):
        header[key] = table[i]

    for key in keys:
        if 'ptr' in key and key[-1] == 'h':
            basekey = key[:-1]
            intl = header[basekey + 'l']
            inth = header[basekey + 'h']
            header[basekey] = two_ints_to_long(intl, inth)

    # remove empty entries
    header.pop('_', None)

    return header


def two_ints_to_long(intl, inth):
    """ Interpert two ints as one long """
    longint = struct.pack(">I", inth) + struct.pack(">I", intl)
    return struct.unpack('>q', longint)[0]
