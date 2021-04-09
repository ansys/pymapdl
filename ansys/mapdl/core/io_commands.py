import os


class _MapdlIoCommands():
    """Methods specific to MAPDL IO"""

    def parres(self, lab="", fname="", ext="", **kwargs):
        """APDL Command: PARRES

        Reads parameters from a file.

        Parameters
        ----------
        lab
            Read operation.

            NEW - Replace current parameter set with these parameters (default).

            CHANGE - Extend current parameter set with these
            parameters, replacing any that already exist.

        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

            The file name defaults to Jobname.

        ext
            Filename extension (eight-character maximum).  The
            extension defaults to PARM if Fname is blank.

        Examples
        --------
        Read a local parameter file.

        >>> mapdl.parres('parm.PARM')

        Notes
        -----
        Reads parameters from a coded file.  The parameter file may
        have been written with the PARSAV command.  The parameters
        read may replace or change the current parameter set.

        This command is valid in any processor.
        """
        if ext:
            fname = fname + '.' + ext
        elif not fname:
            fname = '.' + 'PARM'

        if hasattr(self, '_local'):  # gRPC mode
            if self._local:
                if not os.path.isfile(fname):
                    raise FileNotFoundError('Unable to locate filename "%s"' % fname)

                if not os.path.dirname(fname):
                    filename = os.path.join(os.getcwd(), fname)
                else:
                    filename = fname
            else:
                if not os.path.dirname(fname):
                    # might be trying to run a local file.  Check if the
                    # file exists remotely.
                    if fname not in self.list_files():
                        self.upload(fname, progress_bar=False)
                else:
                    self.upload(fname, progress_bar=False)
                filename = os.path.basename(fname)
        else:
            filename = fname

        return self.input(filename)
