import pytest
import inspect
from ansys.mapdl.core.commands import CommandOutput as CommandOutput

import numpy as np

from ansys.mapdl.core import examples

from ansys.mapdl.core.commands import CommandListingOutput
from ansys.mapdl.core.commands import CommandOutput
from ansys.mapdl.core.commands import HAS_PANDAS

if HAS_PANDAS:
    import pandas as pd


LIST_OF_INQUIRE_FUNCTIONS = [
    'ndinqr',
    'elmiqr',
    'kpinqr',
    'lsinqr',
    'arinqr',
    'vlinqr',
    'rlinqr',
    'gapiqr',
    'masiqr',
    'ceinqr',
    'cpinqr',
    'csyiqr',
    'etyiqr',
    'foriqr',
    'sectinqr',
    'mpinqr',
    'dget',
    'fget',
    'erinqr'
]

# Generic args
ARGS_INQ_FUNC = {
        'node': 1,
        'key': 0,
        'ielem': 1,
        'knmi': 1,
        'line': 1,
        'anmi': 1,
        'vnmi': 1,
        'nreal': 1,
        'ngap': 1,
        'nce': 1,
        'ncp': 1,
        'ncsy': 1,
        'itype': 1,
        'nsect': 1,
        'mat': 1,
        'iprop': 1,
        'idf': 1,
        'kcmplx': 1
}


@pytest.fixture(scope="module")
def plastic_solve(mapdl):
    mapdl.mute = True
    mapdl.finish()
    mapdl.clear()
    mapdl.input(examples.verif_files.vmfiles["vm273"])

    mapdl.post1()
    mapdl.set(1, 2)
    mapdl.mute = False


def test_cmd_class():
    output = """This is the output.
This is the second line.
These are numbers 1234567890.
These are symbols !"£$%^^@~+_@~€
This is for the format: {format1}-{format2}-{format3}"""

    cmd = '/INPUT'
    cmd_out = CommandOutput(output, cmd=cmd)

    assert isinstance(cmd_out, (str, CommandOutput))
    assert isinstance(cmd_out[1:], (str, CommandOutput))
    assert isinstance(cmd_out.splitlines(), list)
    assert isinstance(cmd_out.splitlines()[0], (str, CommandOutput))
    assert isinstance(cmd_out.replace('a', 'c'), (str, CommandOutput))
    assert isinstance(cmd_out.partition('g'), tuple)
    assert isinstance(cmd_out.split('g'), list)


@pytest.mark.parametrize("func", LIST_OF_INQUIRE_FUNCTIONS)
def test_inquire_functions(mapdl, func):
    func_ = getattr(mapdl, func)
    func_args = inspect.getfullargspec(func_).args
    args = [ARGS_INQ_FUNC[each_arg] for each_arg in func_args if each_arg not in ['self']]
    output = func_(*args)
    if 'GRPC' in mapdl._name:
        assert isinstance(output, (float, int))
    else:
        assert isinstance(output, str)
        assert '=' in output


# @pytest.mark.skipif(not HAS_GRPC, reason="Requires GRPC")
@pytest.mark.parametrize('func,args', [
        ('prnsol', ('U', 'X')),
        ('presol', ('S', 'X')),
        ('presol', ('S', 'ALL'))
        ])
def test_output_listing(mapdl, plastic_solve, func, args):
    mapdl.post1()
    func_ = getattr(mapdl, func)
    out = func_(*args)

    out_list = out.to_list()
    out_array = out.to_array()

    assert isinstance(out, CommandListingOutput)
    assert isinstance(out_list, list) and bool(out_list)
    assert isinstance(out_array, np.ndarray) and out_array.size != 0

    if HAS_PANDAS:
        out_df = out.to_dataframe()
        assert isinstance(out_df, pd.DataFrame) and not out_df.empty
