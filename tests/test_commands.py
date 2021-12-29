import pytest

from ansys.mapdl.core.commands import CommandOutput, CommandListing
from ansys.mapdl.core.misc import random_string

FUNCTION_COMMAND_OUTPUT = [each for each in dir(CommandOutput) if not each.startswith('__')]

OUTPUT = """This is the output.
This is the second line.
These are numbers 1234567890.
These are symbols !"£$%^^@~+_@~€
This is for the format: {format1}-{format2}-{format3}"""

## Commands options
_CMD = '/INPUT'

CMD = CommandOutput(OUTPUT, cmd=_CMD)

CMD_DF = CommandListing(OUTPUT, cmd=_CMD)

## Testing configurations
OPTIONS_ONE = [('.'), ('e'), ('t'), ('@'), ('1')]
OPTIONS_TWO = [(50, ' '), (25, '0')]
OPTIONS_TWO_STRINGS = [('a', ' '), ('2', '0'), ('@', 'm'), ('!', '['), ('*', 'r')]
OPTIONS_TWO_NUMBERS = [(123, 15), (109893, 10)]
OPTIONS_FORMAT = [
    ({'format1': random_string(), 'format2': random_string(), 'format3': random_string()}),
    ({'format1': random_string(), 'format2': random_string(), 'format3': random_string()}),
    ({'format1': random_string(), 'format2': random_string(), 'format3': random_string()})
    ]

OPTIONS_RANDOM_STRINGS = [
    tuple(random_string() for each in range(10)),
    tuple(random_string() for each in range(24)),
    tuple(random_string() for each in range(3))
    ]

OPTIONS_DICT_MAP = [
    (
        {OUTPUT[5:10]: random_string(),
         OUTPUT[45:59]: random_string(),
         OUTPUT[89:104]: random_string()
         }
    )
    ]

# @pytest.mark.parametrize("args", [(), (), ()])
# random_string

def test_class():
    assert isinstance(CMD, (str, CommandOutput))
    assert isinstance(CMD[1:], (str, CommandOutput))
    assert isinstance(CMD.splitlines(), list)
    assert isinstance(CMD.splitlines()[0], (str, CommandOutput))
    assert isinstance(CMD.replace('a', 'c'), (str, CommandOutput))
    assert isinstance(CMD.partition('g'), tuple)
    assert isinstance(CMD.split('g'), list)

def test_heritance():
    assert CMD._cmd == _CMD
    assert CMD[1:]._cmd == _CMD
    assert CMD.replace('a', 'c')._cmd == _CMD
    dummy = CMD.replace('1', 'g')
    assert dummy._cmd == _CMD

def test_capitalize():
    assert OUTPUT.capitalize() == CMD.capitalize()

def test_casefold():
    assert OUTPUT.casefold() == CMD.casefold()

@pytest.mark.parametrize("args", OPTIONS_TWO)
def test_center(args):
    assert OUTPUT.center(*args) == CMD.center(*args)

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_count(args):
    assert OUTPUT.count(*args) == CMD.count(*args)

def test_encode():
    assert OUTPUT.encode() == CMD.encode()

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_endswith(args):
    assert OUTPUT.endswith(*args) == CMD.endswith(*args)

def test_expandtabs():
    assert OUTPUT.expandtabs() == CMD.expandtabs()

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_find(args):
    assert OUTPUT.find(*args) == CMD.find(*args)

@pytest.mark.parametrize("args", OPTIONS_FORMAT)
def test_format(args):
    assert OUTPUT.format(**args) == CMD.format(**args)

@pytest.mark.parametrize("args", OPTIONS_FORMAT)
def test_format_map(args):
    assert OUTPUT.format_map(args) == CMD.format_map(args)

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_index(args):
    assert OUTPUT.index(*args) == CMD.index(*args)

def test_isalnum():
    assert OUTPUT.isalnum() == CMD.isalnum()

def test_isalpha():
    assert OUTPUT.isalpha() == CMD.isalpha()

def test_isascii():
    assert OUTPUT.isascii() == CMD.isascii()

def test_isdecimal():
    assert OUTPUT.isdecimal() == CMD.isdecimal()

def test_isdigit():
    assert OUTPUT.isdigit() == CMD.isdigit()

def test_isidentifier():
    assert OUTPUT.isidentifier() == CMD.isidentifier()

def test_islower():
    assert OUTPUT.islower() == CMD.islower()

def test_isnumeric():
    assert OUTPUT.isnumeric() == CMD.isnumeric()

def test_isprintable():
    assert OUTPUT.isprintable() == CMD.isprintable()

def test_isspace():
    assert OUTPUT.isspace() == CMD.isspace()

def test_istitle():
    assert OUTPUT.istitle() == CMD.istitle()

def test_isupper():
    assert OUTPUT.isupper() == CMD.isupper()

@pytest.mark.parametrize("args", OPTIONS_RANDOM_STRINGS)
def test_join(args):
    assert OUTPUT.join(args) == CMD.join(args)


@pytest.mark.parametrize("args", OPTIONS_TWO)
def test_ljust(args):
    assert OUTPUT.ljust(*args) == CMD.ljust(*args)

def test_lower():
    assert OUTPUT.lower() == CMD.lower()

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_lstrip(args):
    assert OUTPUT.lstrip(*args) == CMD.lstrip(*args)

# @pytest.mark.parametrize("args", OPTIONS_DICT_MAP)
# def test_maketrans(args):
#     assert OUTPUT.maketrans(*args) == CMD.maketrans(*args)

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_partition(args):
    assert OUTPUT.partition(*args) == CMD.partition(*args)

@pytest.mark.parametrize("args", OPTIONS_TWO_STRINGS)
def test_replace(args):
    assert OUTPUT.replace(*args) == CMD.replace(*args)

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_rfind(args):
    assert OUTPUT.rfind(*args) == CMD.rfind(*args)

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_rindex(args):
    assert OUTPUT.rindex(*args) == CMD.rindex(*args)

@pytest.mark.parametrize("args", OPTIONS_TWO)
def test_rjust(args):
    assert OUTPUT.rjust(*args) == CMD.rjust(*args)

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_rpartition(args):
    assert OUTPUT.rpartition(args) == CMD.rpartition(args)

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_rsplit(args):
    assert OUTPUT.rsplit(*args) == CMD.rsplit(*args)

def test_rstrip():
    assert OUTPUT.rstrip() == CMD.rstrip()

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_split(args):
    assert OUTPUT.split(*args) == CMD.split(*args)

def test_splitlines():
    assert OUTPUT.splitlines() == CMD.splitlines()

@pytest.mark.parametrize("args", OPTIONS_ONE)
def test_startswith(args):
    assert OUTPUT.startswith(*args) == CMD.startswith(*args)

def test_strip():
    assert OUTPUT.strip() == CMD.strip()

def test_swapcase():
    assert OUTPUT.swapcase() == CMD.swapcase()

def test_title():
    assert OUTPUT.title() == CMD.title()

@pytest.mark.parametrize("args", OPTIONS_DICT_MAP)
def test_translate(args):
    assert OUTPUT.translate(args) == CMD.translate(args)

def test_upper():
    assert OUTPUT.upper() == CMD.upper()

## Dataframe class.

def test_cmd_df_inheritance():
    assert isinstance(CMD_DF, CommandListing)
    assert isinstance(CMD_DF, CommandOutput)

@pytest.mark.parametrize("method", ['get_lists', 'get_array', 'get_dataframe'])
def test_cmd_df_methods(method):
    assert hasattr(CMD_DF, method)

@pytest.mark.parametrize("model,nnodediv", ([contact_solve, plastic_solve], [1, 2, 5]))
def test_cmd_df_data_size_nodes(mapdl, model, nnodediv):
    mapdl.post1()
    mapdl.allsel()

    n_nodes_tot = mapdl.mesh.n_node
    mapdl.nsel('S', 0, n_nodes_tot//nnodediv)

    out = mapdl.nlist()
    cmd = CommandListing(out.__str__(), cmd=out._cmd)
    arr = cmd.get_array()
    df = cmd.get_dataframe()

    assert arr.shape[0] == mapdl.mesh.n_node
    assert arr.shape[1] > 3
    assert df['NODE'].isin(mapdl.mesh.nnum).all()

@pytest.mark.parametrize("model,nelemdiv", ([contact_solve, plastic_solve], [1, 2, 5]))
def test_cmd_df_data_size_elem(mapdl, model, nelemdiv):
    mapdl.post1()
    mapdl.allsel()

    n_elem_tot = mapdl.mesh.n_elem
    mapdl.esel('S', 0, n_elem_tot//nelemdiv)

    out = mapdl.elist()
    cmd = CommandListing(out.__str__(), cmd=out._cmd)
    arr = cmd.get_array()
    df = cmd.get_dataframe()

    assert arr.shape[0] == mapdl.mesh.n_elem
    assert df['ELEMENT'].isin(mapdl.mesh.enum).all()


@pytest.mark.parametrize("model,command", ([contact_solve, plastic_solve], SUPPORTED_PRINT_CMDS ))
def test_cmd_df_supported_(mapdl, model, command):

    mapdl.post1()
    mapdl.allsel()

    if command not in ['DLIST', 'NLIST', 'ELIST']:
        out = mapdl.run(f"{command},U,X")
    else:
        out = mapdl.run(f"{command}")

    cmd = CommandListing(out.__str__(), cmd=out._cmd)
    arr = cmd.get_array()
    df = cmd.get_dataframe()

    assert arr.shape[0] == mapdl.mesh.n_elem
    assert df['ELEMENT'].isin(mapdl.mesh.enum).all() or df['NODE'].isin(mapdl.mesh.nnum).all()
    
    
