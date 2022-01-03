from ansys.mapdl.core.commands import CommandOutput as CommandOutput

OUTPUT = """This is the output.
This is the second line.
These are numbers 1234567890.
These are symbols !"£$%^^@~+_@~€
This is for the format: {format1}-{format2}-{format3}"""

## Commands options
_CMD = '/INPUT'
CMD = CommandOutput(OUTPUT, cmd=_CMD)

def test_class():
    assert isinstance(CMD, (str, CommandOutput))
    assert isinstance(CMD[1:], (str, CommandOutput))
    assert isinstance(CMD.splitlines(), list)
    assert isinstance(CMD.splitlines()[0], (str, CommandOutput))
    assert isinstance(CMD.replace('a', 'c'), (str, CommandOutput))
    assert isinstance(CMD.partition('g'), tuple)
    assert isinstance(CMD.split('g'), list)

# def test_heritance():
#     assert CMD._cmd == _CMD
#     assert CMD[1:]._cmd == _CMD
#     assert CMD.replace('a', 'c')._cmd == _CMD
#     dummy = CMD.replace('1', 'g')
#     assert dummy._cmd == _CMD
