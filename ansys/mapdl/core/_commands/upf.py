

class UPF:
    def upf(self, filename, **kwargs):
        """APDL Command: /BATCH

        The ``/UPF`` command offers the simplest method for linking user programmable
        features into Mechanical APDL.

        Parameters
        ----------
        filename
            The name of a user routine (filename.ext).
            The specified routine must reside in the current working directory.


        Notes
        -----

        To use this method start Mechanical APDL in batch mode and include one
        or more ``/UPF`` commands in the specified input listing.
        When the program reads the input and detects ``/UPF``, Mechanical APDL
        will be relinked automatically.

        You can include ``/UPF`` anywhere in your input file, and you can repeat
        ``/UPF`` as many times as needed to include multiple user routines in the
        relinked version. Any user routine can be linked using this method.
        When you run a user-linked version of the program by this method,
        the output includes the following:

        ..code::
          NOTE - This Mechanical APDL version was linked by ``/UPF`` with n user supplied routine(s).

        where n indicates the number of routines specified by ``/UPF`` commands.
        The routines that have been linked will be included in the output listing.
        """

        command = f"/UPF,{filename}"
        return self.run(command, **kwargs)
