"""These commands may be run by PyMapdl, but are not supported from a
user-context.

"""


def batch(self, lab="", **kwargs):
    """APDL Command: /BATCH

    Sets the program mode to "batch."

    Parameters
    ----------
    lab
        Specifies listing mode during a batch run:

        LIST - The batch output will include a listing of the input file.

        (blank) - Suppress input data listing.

    Notes
    -----
    Sets the program mode to "batch" when included as the first line on an
    input file of ANSYS commands.  For convenience, this command is
    automatically recorded on the log file (Jobname.LOG) at the beginning
    of an interactive ANSYS session so that the log file can be reused
    later for batch input.

    Caution:: : This command  should not be entered directly in an
    interactive ANSYS session since all subsequent keyboard input is simply
    copied to a file, without further processing or prompts from the
    program (use the "system break" to exit the ANSYS program if this
    occurs).

    The recommended method for choosing batch mode, rather than using the
    /BATCH command, is to select the Batch simulation environment from the
    ANSYS Product Launcher  task in the ANSYS launcher, or the batch mode
    entry option on the ANSYS execution command when entering the program.

    This command is valid only at the Begin Level.
    """
    command = "/BATCH,%s" % (str(lab))
    return self.run(command, **kwargs)
