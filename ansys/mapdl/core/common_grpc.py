"""Common gRPC functions"""
import numpy as np

# chunk sizes for streaming and file streaming
DEFAULT_CHUNKSIZE = 256*1024  # 256 kB
DEFAULT_FILE_CHUNK_SIZE = 1024*1024  # 1MB


ANSYS_VALUE_TYPE = {0: None,           # UNKNOWN
                    1: np.int32,       # INTEGER
                    2: np.int64,       # HYPER
                    3: np.int16,       # SHORT
                    4: np.float32,     # FLOAT
                    5: np.float64,     # DOUBLE
                    6: np.complex64,   # FCPLX
                    7: np.complex128}  # DCPLX


VGET_ENTITY_TYPES = ['NODE', 'ELEM', 'KP', 'LINE', 'AREA', 'VOLU',
                     'CDSY', 'RCON', 'TLAB']
STRESS_TYPES = ['X', 'Y', 'Z', 'XY', 'YZ', 'XZ', '1', '2', '3', 'INT', 'EQV']
COMP_TYPE = ['X', 'Y', 'Z', 'SUM']
VGET_NODE_ENTITY_TYPES = {'U': ['X', 'Y', 'Z'],
                          'S': STRESS_TYPES,
                          'EPTO': STRESS_TYPES,
                          'EPEL': STRESS_TYPES,
                          'EPPL': STRESS_TYPES,
                          'EPCR': STRESS_TYPES,
                          'EPTH': STRESS_TYPES,
                          'EPDI': STRESS_TYPES,
                          'EPSW': [None],
                          'NL': ['SEPL', 'SRAT', 'HPRES', 'EPEQ', 'PSV', 'PLWK'],
                          'HS': ['X', 'Y', 'Z'],
                          'BFE': ['TEMP'],
                          'TG': COMP_TYPE,
                          'TF': COMP_TYPE,
                          'PG': COMP_TYPE,
                          'EF': COMP_TYPE,
                          'D': COMP_TYPE,
                          'H': COMP_TYPE,
                          'B': COMP_TYPE,
                          'FMAG': COMP_TYPE,
                          'NLIST': [None]}


class GrpcError(RuntimeError):
    """Raised when gRPC fails"""
    def __init__(self, msg=''):
        RuntimeError.__init__(self, msg)


def check_vget_input(entity, item, itnum):
    """Verify that entity and item for VGET are valid.

    Raises a ``ValueError`` when invalid.

    Parameters
    ----------
    entity : str
        Entity keyword. Valid keywords are:

        - ``'NODE'``
        - ``'ELEM'``
        - ``'KP'``
        - ``'LINE'``
        - ``'AREA'``
        - ``'VOLU'``
        - ``'CDSY'``
        - ``'RCON'``
        - ``'TLAB'``

    item : str
        The name of a particular item for the given entity. Valid
        items are as shown in the item columns of the tables
        within the ``*VGET`` command reference in your ANSYS manual.

    itnum : str
        The number (or label) for the specified item (if
        any). Valid it1num values are as shown in the IT1NUM
        columns of the tables in the command reference section for
        the ``*VGET`` command in your ANSYS manual. Some Item1 labels
        do not require an IT1NUM value.

    Returns
    -------
    command : str
        MAPDL formatted vget command after the "VGET, " in the format of:
        "ENTITY, , ITEM, ITNUM"
    """
    entity = entity.upper()
    if item is not None:
        item = item.upper()

    if itnum is not None:
        itnum = itnum.upper()

    if entity not in VGET_ENTITY_TYPES:
        raise ValueError('Entity "%s" not allowed.  Allowed items:\n%s'
                         % entity, str(VGET_ENTITY_TYPES))

    if entity == 'NODE':
        if item not in VGET_NODE_ENTITY_TYPES:
            allowed_types = list(VGET_NODE_ENTITY_TYPES.keys())
            raise ValueError('item "%s" for "NODE" not allowed.  Allowed items:%s\n'
                             % (item, str(allowed_types)))

        if itnum not in VGET_NODE_ENTITY_TYPES[item]:
            allowed_types = VGET_NODE_ENTITY_TYPES[item]
            raise ValueError('itnum "%s" for item "%s" not allowed.  Allowed items:\n%s' % (itnum, item, str(allowed_types)))

    # None is not allowed in MAPDL commands
    if item is None:
        item = ''
    if itnum is None:
        itnum = ''

    return '%s, , %s, %s' % (entity, item, itnum)


def parse_chunks(chunks, dtype=None):
    """Deserialize gRPC chunks into a numpy array

    Parameters
    ----------
    chunks : generator
        generator from grpc.  Each chunk contains a bytes payload

    dtype : np.dtype
        Numpy data type to interpert chunks as.

    Returns
    -------
    array : np.ndarray
        Deserialized numpy array.

    """
    if not chunks.is_active():
        raise RuntimeError('Empty Record')

    try:
        chunk = chunks.next()
    except:
        return np.empty(0)

    if not chunk.value_type and dtype is None:
        raise ValueError('Must specify a data type for this record')

    if dtype is None:
        dtype = ANSYS_VALUE_TYPE[chunk.value_type]

    array = np.frombuffer(chunk.payload, dtype)
    if chunks.done():
        return array

    arrays = [array]
    for chunk in chunks:
        arrays.append(np.frombuffer(chunk.payload, dtype))

    return np.hstack(arrays)
