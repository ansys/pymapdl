import pyansys

valid_functions = dir(pyansys.ANSYS)


def IsFloat(string):
    try:
        float(string)
        return True
    except:
        return False


def ConvertLine(line, obj='ansys'):
    line = line.rstrip()
    line = line.replace('"', "'")
    # check if it's a command

    items = line.split(',')
    if '=' in items[0]:  # line sets a variable:
        return '%s.RunCommand("%s")\n' % (obj, line)
    # elif 'C***' in items[0]:  # line is a comment
        # return '%s.RunCommand("%s")\n' % (obj, line)
    elif '!' in items[0]:  # line contains a comment
        if items[0].strip()[0] == '!':
            return '%s\n' % line.replace('!', '#')

    command = items[0].capitalize().strip()
    if not command:
        return ('\n')

    # check if first item is a valid command
    if command not in valid_functions:
        if '/COM' in line:
            return line.replace('/COM', '# ') + '\n'
        elif 'VWRITE' in line:  # ignore vwrite prompts (ansys verification files)
            return '%s.RunCommand("%s", ignore_prompt=True)\n' % (obj, line)
        elif '*CREATE' in line:  # now writing to macro
            newline = '%s.block_override = False\n' % obj
            newline += '%s.RunCommand("%s")\n' % (obj, line)
            return newline
        elif '*END' in line and '*ENDIF' not in line:  # stop writing to macro
            newline = '%s.RunCommand("%s")\n' % (obj, line)
            newline += '%s.block_override = None\n' % obj
            return newline
        else:
            return '%s.RunCommand("%s")\n' % (obj, line)

    converted_line = '%s.%s(' % (obj, command)
    items = items[1:]
    for i, item in enumerate(items):
        if IsFloat(item):
            items[i] = item.strip()
        else:
            items[i] = '"%s"' % item.strip()

    converted_line += ', '.join(items)
    if 'VWRITE' in converted_line:
        converted_line += ', ignore_prompt=True)\n'
    else:
        converted_line += ')\n'

    return converted_line


def ConvertFile(filename_in, filename_out, loglevel='INFO'):
    """
    Converts an ANSYS input file to a python pyansys script.

    Parameters
    ----------
    filename_in : str
        Filename of the ansys input file to read in.

    filename_out : str
        Filename of the python script to write a translation to.

    Returns
    -------
    clines : list
        List of lines translated

    """
    clines = []
    with open(filename_in) as file_in:
        with open(filename_out, 'w') as file_out:
            file_out.write('import pyansys\n')
            file_out.write('ansys = pyansys.ANSYS(loglevel="%s")\n' % loglevel)
            for line in file_in.readlines():
                cline = ConvertLine(line)
                file_out.write(cline)
                clines.append(cline)

            cline = 'ansys.Exit()\n'
            file_out.write(cline)
            clines.append(cline)

    return clines
