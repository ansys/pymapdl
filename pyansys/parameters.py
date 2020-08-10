from pyansys.mapdl import _MapdlCore

ROUTINE_MAP = {0: 'Begin level',
               17: 'PREP7',
               21: 'SOLUTION',
               31: 'POST1',
               36: 'POST26',
               52: 'AUX2',
               53: 'AUX3',
               62: 'AUX12',
               65: 'AUX15'}

UNITS_MAP = {0: 'USER',
             1: 'SI',
             2: 'CGS',
             3: 'BFT',
             4: 'BIN',
             5: 'MKS',
             6: 'MPA',
             7: 'uMKS'}

class Parameters():
    """Collection of MAPDL parameters obtainable from the *GET command"""

    def __init__(self, mapdl):
        if not isinstance(mapdl, _MapdlCore):
            raise TypeError('Must be implemented from MAPDL class')
        self._mapdl = mapdl

    @property
    def routine(self):
        """Current Routine string.

        MAPDL Command: *GET, ACTIVE, 0, ROUT

        Returns
        -------
        routine : str
            Routine as a string.  One of:

            - "Begin level"
            - "PREP7"
            - "SOLUTION"
            - "POST1"
            - "POST26"
            - "AUX2"
            - "AUX3"
            - "AUX12"
            - "AUX15"

        Examples
        --------
        >>> mapdl.parameters.routine
        'PREP7'
        """
        value = self._mapdl.get_value('ACTIVE', item1='ROUT')
        return ROUTINE_MAP[int(value)]

    @property
    def units(self):
        """Units specified by /UNITS command.

        Returns
        -------
        units : str
            Active Units.  One of:- "USER"
            - "SI"
            - "CGS"
            - "BFT"
            - "BIN"
            - "MKS
            - "MPA"
            - "uMKS
        """
        value = self._mapdl.get_value("ACTIVE", item1="UNITS")
        return UNITS_MAP[int(value)]

    @property
    def revision(self):
        """MAPDL revision version.

        MAPDL revision version as a float.  For example ``20.2``.
        """
        return float(self._mapdl.get_value("ACTIVE", item1="REV"))

    @property
    def platform(self):
        """The current platform.

        Current platform.  For example ``"LIN"`` for Linux.
        """
        return self._mapdl.get_value("ACTIVE", item1="PLATFORM")

    @property
    def csys(self):
        """Active coordinate system"""
        return int(self._mapdl.get_value("ACTIVE", item1="CSYS"))

    @property
    def dsys(self):
        """Active display coordinate system"""
        return int(self._mapdl.get_value("ACTIVE", item1="DSYS"))

    @property
    def rsys(self):
        """Active result coordinate system"""
        return int(self._mapdl.get_value("ACTIVE", item1="RSYS"))

    @property
    def esys(self):
        """Active element coordinate system"""
        return int(self._mapdl.get_value("ACTIVE", item1="ESYS"))

    @property
    def section(self):
        """Active section number"""
        return int(self._mapdl.get_value("ACTIVE", item1="SECT"))

    @property
    def material(self):
        """Active material"""
        return int(self._mapdl.get_value("ACTIVE", item1="MAT"))

    @property
    def real(self):
        """Active real constant set"""
        return int(self._mapdl.get_value("ACTIVE", item1="REAL"))


# def test():
#     parm = Parameters(mapdl)
#     mapdl.prep7()
#     assert parm.routine == "PREP7"

#     mapdl.units("SI")
#     assert parm.units == "SI"

#     assert isinstance(parm.revision, float)

#     if os.name == 'posix':
#         assert parm.platform == 'LIN'

#     mapdl.csys(1)
#     assert parm.csys == 1

#     mapdl.dsys(1)
#     assert parm.dsys == 1

#     mapdl.esys(0)
#     assert parm.esys == 0
#     assert parm.material == 1
#     assert parm.section == 1
#     assert parm.real == 1
