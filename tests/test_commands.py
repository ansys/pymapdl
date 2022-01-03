import pytest
import inspect


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
