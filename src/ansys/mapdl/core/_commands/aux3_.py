class Aux3:
    def compress(self, **kwargs):
        """Deletes all specified sets.

        APDL Command: COMPRESS

        Notes
        -----
        Issue this command to delete all sets specified with the DELETE
        command.
        """
        command = f"COMPRESS,"
        return self.run(command, **kwargs)

    def list(self, level="", **kwargs):
        """Lists out the sets in the results file.

        APDL Command: LIST

        Notes
        -----
        This command lists the results set number, the load step, substep, and
        time step for each set. It also shows all sets marked for deletion.
        """
        command = "LIST,%s" % (str(level))
        return self.run(command, **kwargs)

    def fileaux3(self, fname="", ext="", **kwargs):
        """Specifies the results file to be edited.

        APDL Command: FILEAUX3

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        Specifies the results file to be edited.
        """
        command = f"FILEAUX3,{fname},{ext}"
        return self.run(command, **kwargs)

    def modify(
        self,
        set_="",
        lstep="",
        iter_="",
        cumit="",
        time="",
        ktitle="",
        **kwargs,
    ):
        """Changes the listed values of the data in a set.

        APDL Command: MODIFY

        Parameters
        ----------
        set\_
            Set of data in results file to be modified.

        lstep
            The new load step number.

        iter\_
            The new load substep number.

        cumit
            The new cumulative iteration.

        time
            The new time/frequency value.

        ktitle
            Indicates if the set title should be modified.

            0 - Keep the original title.

            1 - Change the title to the title specified with the most current /TITLE command.

        Notes
        -----
        Use this command to change the listed values in a data set in a results
        file. Using this command does not change any actual model data; it
        affects only the values listed in the results file.

        For example, if you start with the following results file:

        and you then issue the following commands:

        The modified results file would look like this:
        """
        command = f"MODIFY,{set_},{lstep},{iter_},{cumit},{time},{ktitle}"
        return self.run(command, **kwargs)

    def undelete(self, option="", nstart="", nend="", **kwargs):
        """Removes results sets from the group of sets selected for editing.

        APDL Command: UNDELETE

        Parameters
        ----------
        option
            Specifies which sets are to be removed from the selected sets.

            SET - Specifies one or more particular sets in the results file that are to be
                  removed from the group of sets selected for deletion.

            ALL - Removes all selected sets that are currently selected for deletion.

        nstart
            The first set to be removed from the set selected for deletion.

        nend
            The final set to be removed from the set selected for deletion.
            This field is used only if operating on more than one sequential
            set.

        Notes
        -----
        Use this command if you have previously marked a set for deletion (with
        the DELETE command) and now wish to keep that set instead of deleting
        it.
        """
        command = f"UNDELETE,{option},{nstart},{nend}"
        return self.run(command, **kwargs)

    def delete(self, set_="", nstart="", nend="", **kwargs):
        """Specifies sets in the results file to be deleted before postprocessing.

        APDL Command: DELETE

        Parameters
        ----------
        set_
            Specifies that sets in the results file are to be deleted.

        nstart
            The first set in a results file to be deleted.

        nend
            The final set in a results file to be deleted. This field is used
            only if deleting more than one sequential sets.

        Notes
        -----
        DELETE is a specification command that flags sets in the results
        file for deletion. It should be followed by a COMPRESS command,
        the corresponding action command that deletes the specified sets.

        The DELETE command is valid only in the results file editing processor
        (ANSYS auxiliary processor AUX3).
        """
        command = f"DELETE,{set_},{nstart},{nend}"
        return self.run(command, **kwargs)
