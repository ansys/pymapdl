"""Post-processing module using MAPDL interface"""
import weakref

import numpy as np

from ansys.mapdl.core.misc import supress_logging
from ansys.mapdl.core.plotting import general_plotter

COMPONENT_STRESS_TYPE = ["X", "Y", "Z", "XY", "YZ", "XZ"]
PRINCIPAL_TYPE = ["1", "2", "3"]
STRESS_TYPES = ["X", "Y", "Z", "XY", "YZ", "XZ", "1", "2", "3", "INT", "EQV"]
COMP_TYPE = ["X", "Y", "Z", "SUM"]
DISP_TYPE = ["X", "Y", "Z", "NORM", "ALL"]
ROT_TYPE = ["X", "Y", "Z", "ALL"]


def elem_check_inputs(component, option, component_type):
    """Check element inputs"""
    check_elem_option(option)
    component = component.upper()
    check_comp(component, component_type)
    return component


def check_elem_option(option):
    """Check element option is valid."""
    if option.upper() not in ["AVG", "MIN", "MAX"]:
        raise ValueError("``option`` should be either 'AVG', 'MIN', or 'MAX'")


def check_result_loaded(func):
    """Verify a result has been loaded within MAPDL"""

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def check_comp(component, allowed):
    """Check if a component is valid."""
    if not isinstance(component, str):
        raise TypeError("Component must be a string")
    component = component.upper().strip()
    if component not in allowed:
        raise ValueError(
            "Component %s not a valid type.  " % component
            + "Allowed items:\n%s" % str(allowed)
        )
    return component


class PostProcessing:
    """Post-processing using an active MAPDL session

    Examples
    --------
    Get all the time values after loading POST1.

    >>> mapdl.post1()
    >>> mapdl.post_processing.time_values
    [75.00054133588232,
     75.00081189985094,
     75.00121680412036,
     75.00574491751847,
     75.03939292229019,
     75.20949687626468]

    Return the number of data sets in the result file.

    >>> mapdl.post_processing.nsets
    1

    Plot the thermal equivalent strain for the second result.

    >>> mapdl.post1()
    >>> mapdl.set(1, 2)
    >>> mapdl.post_processing.plot_nodal_thermal_eqv_strain()

    Nodal rotation in all dimensions for current result.

    >>> mapdl.post1()
    >>> mapdl.set(1, 1)
    >>> mapdl.post_processing.nodal_rotation('ALL')
    array([[0., 0., 0.],
           [0., 0., 0.],
           [0., 0., 0.],
           ...,
           [0., 0., 0.],
           [0., 0., 0.],
           [0., 0., 0.]])

    Nodes corresponding to the nodal rotations.

    >>> mapdl.mesh.nnum_all
    array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

    """

    def __init__(self, mapdl):
        """Initialize postprocessing instance"""
        from ansys.mapdl.core.mapdl import _MapdlCore

        if not isinstance(mapdl, _MapdlCore):  # pragma: no cover
            raise TypeError("Must be initialized using Mapdl instance")
        self._mapdl_weakref = weakref.ref(mapdl)
        self._set_loaded = False

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of MAPDL"""
        return self._mapdl_weakref()

    @property
    def _log(self):
        """alias for mapdl log"""
        return self._mapdl._log

    def _set_log_level(self, level):
        """alias for mapdl._set_log_level"""
        return self._mapdl._set_log_level(level)

    @supress_logging
    def __repr__(self):
        info = "PyMAPDL PostProcessing Instance\n"
        info += "\tActive Result File:    %s\n" % self.filename
        info += "\tNumber of result sets: %d\n" % self.nsets
        info += "\tCurrent load step:     %d\n" % self.load_step
        info += "\tCurrent sub step:      %d\n" % self.sub_step

        if self._mapdl.parameters.routine == "POST1":
            info += "\n\n" + self._mapdl.set("LIST")
        else:
            info += "\n\n Enable routine POST1 to see a table of available results"

        return info

    @property
    def time_values(self) -> np.ndarray:
        """Return an array of the time values for all result sets.

        Returns
        -------
        numpy.ndarray
            Numpy array of the time values for all result sets.

        Examples
        --------
        Get all the time values after loading POST1.

        >>> mapdl.post1()
        >>> mapdl.post_processing.time_values
        [75.00054133588232,
         75.00081189985094,
         75.00121680412036,
         75.00574491751847,
         75.03939292229019,
         75.20949687626468]
        """
        with self._mapdl.run_as_routine("POST1"):
            list_rsp = self._mapdl.set("LIST")
        return np.genfromtxt(list_rsp.splitlines(), skip_header=3)[:, 1]

    @property
    def frequency_values(self) -> np.ndarray:
        """Return an array of the frequency values for all result sets.

        Returns
        -------
        numpy.ndarray
            Numpy array of the frequency values for all result sets.

        Examples
        --------
        Get all the time values after loading POST1.

        >>> mapdl.post1()
        >>> mapdl.post_processing.frequency_values
        array([ 220.,  240.,  260.,  280.,  300.,  320.,  340.,  360.,  380.,
        400.,  420.,  440.])
        """
        # Because in MAPDL is the same.
        return self.time_values

    def _reset_cache(self):
        """Reset local cache"""
        self._set_loaded = False

    @property
    def filename(self) -> str:
        """Return the current result file name without extension.

        Examples
        --------
        >>> mapdl.post_processing.filename
        'file'
        """
        response = self._mapdl.run("/INQUIRE, param, RSTFILE", mute=False)
        return response.split("=")[-1].strip()

    @property
    def nsets(self) -> int:
        """Number of data sets on result file.

        Examples
        --------
        Return the number of data sets in the result file.

        >>> mapdl.post_processing.nsets
        1
        """
        return int(self._mapdl.get_value("ACTIVE", item1="SET", it1num="NSET"))

    @property
    def load_step(self) -> int:
        """Current load step number

        Examples
        --------
        >>> mapdl.post1()
        >>> mapdl.set(2, 2)
        >>> mapdl.post_processing.load_step
        2
        """
        return int(self._mapdl.get_value("ACTIVE", item1="SET", it1num="LSTP"))

    @property
    def sub_step(self) -> int:
        """Current sub step number

        Examples
        --------
        >>> mapdl.post1()
        >>> mapdl.set(2, 2)
        >>> mapdl.post_processing.load_step
        2
        """
        return int(self._mapdl.get_value("ACTIVE", item1="SET", it1num="SBST"))

    @property
    def step(self) -> int:
        """Current step number

        Examples
        --------
        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.set
        2
        """
        sets = self._mapdl.set("LIST").to_array()
        ldstep = self.load_step
        substep = self.sub_step
        return sets[(sets[:, 2] == ldstep) & (sets[:, 3] == substep)][0, 0]

    @property
    def time(self) -> float:
        """Time associated with current result in the database.

        Examples
        --------
        Time of the current result of a modal analysis

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.time
        1.0
        """
        return self._mapdl.get_value("ACTIVE", item1="SET", it1num="TIME")

    @property
    def freq(self) -> float:
        """Freqneyc associated with current result in the database.

        Applicable for a Modal, harmonic or spectral analysis.

        Examples
        --------
        Natural frequency of the current result of a modal analysis

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.freq
        956.86239847
        """
        return self._mapdl.get_value("ACTIVE", item1="SET", it1num="FREQ")

    def nodal_values(self, item, comp="") -> np.ndarray:
        """Obtain the nodal values for a given item and component.

        This method uses :func:`Mapdl.get_array()<ansys.mapdl.core.Mapdl.get_array`

        Parameters
        ----------
        item : str
            Label identifying the item.
        comp : str, optional
            Component of the item if applicable.

        Returns
        -------
        numpy.ndarray
            Numpy array containing the requested element values for the
            given item and component.

        Notes
        -----
        Please reference your Ansys help manual ``*VGET`` command tables
        for all the available ``*VGET`` values.

        """
        # using _ndof_rst instead of get_array because it is wrapped to check the rst.
        values = self._ndof_rst(item=item, it1num=comp)
        mask = self.selected_nodes
        try:
            return values[mask]
        except IndexError:  # pragma: no cover
            raise IndexError(
                "The number of selected nodes does not match the number of nodal results returned by MAPDL."
            )

    def element_values(self, item, comp="", option="AVG") -> np.ndarray:
        """Compute the element-wise values for a given item and component.

        This method uses :func:`Mapdl.etable()
        <ansys.mapdl.core.Mapdl.etable` and returns a
        ``numpy.ndarray`` rather than storing it within MAPDL.

        Parameters
        ----------
        item : str
            Label identifying the item.  See the table below in the
            notes section.

        comp : str, optional
            Component of the item if applicable.  See the table below
            in the notes section.

        option : str, optional
            Option for storing element table data.  One of the
            following:

            * ``"MIN"`` : Store minimum element nodal value of the
              specified item component.
            * ``"MAX"`` : Store maximum element nodal value of the
              specified item component.
            * ``"AVG"`` : Store averaged element centroid value of the
              specified item component (default).

        Returns
        -------
        numpy.ndarray
            Numpy array containing the requested element values for ta
            given item and component.

        Notes
        -----
        This an incomplete table of element values available to this
        method.  For a full table, see `ETABLE
        <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_ETABLE.html>`_

        +------+---------------------+--------------------------------------+
        | Item | Comp                | Description                          |
        +------+---------------------+--------------------------------------+
        | U    | X, Y, Z             | X, Y, or Z structural displacement.  |
        +------+---------------------+--------------------------------------+
        | ROT  | X, Y, Z             | X, Y, or Z structural rotation.      |
        +------+---------------------+--------------------------------------+
        | TEMP |                     | Temperature.                         |
        +------+---------------------+--------------------------------------+
        | PRES |                     | Pressure.                            |
        +------+---------------------+--------------------------------------+
        | VOLT |                     | Electric potential.                  |
        +------+---------------------+--------------------------------------+
        | MAG  |                     | Magnetic scalar potential.           |
        +------+---------------------+--------------------------------------+
        | V    | X, Y, Z             | X, Y, or Z fluid velocity.           |
        +------+---------------------+--------------------------------------+
        | A    | X, Y, Z             | X, Y, or Z magnetic vector potential |
        +------+---------------------+--------------------------------------+
        | CONC |                     | Concentration.                       |
        +------+---------------------+--------------------------------------+
        | CURR |                     | Current.                             |
        +------+---------------------+--------------------------------------+
        | EMF  |                     | Electromotive force drop.            |
        +------+---------------------+--------------------------------------+
        | S    | X, Y, Z, XY, YZ, XZ | Component stress.                    |
        |      +---------------------+--------------------------------------+
        |      | 1, 2, 3             | Principal stress.                    |
        |      +---------------------+--------------------------------------+
        |      | INT                 | Stress intensity.                    |
        |      +---------------------+--------------------------------------+
        |      | EQV                 | Equivalent stress.                   |
        +------+---------------------+--------------------------------------+
        | EPEL | X, Y, Z, XY, YZ, XZ | Component elastic strain.            |
        |      +---------------------+--------------------------------------+
        |      | 1, 2, 3             | Principal elastic strain.            |
        |      +---------------------+--------------------------------------+
        |      | INT                 | Elastic strain intensity.            |
        |      +---------------------+--------------------------------------+
        |      | EQV                 | Elastic equivalent strain.           |
        +------+---------------------+--------------------------------------+
        | EPTH | X, Y, Z, XY, YZ, XZ | Component thermal strain.            |
        |      +---------------------+--------------------------------------+
        |      | 1, 2, 3             | Principal thermal strain.            |
        |      +---------------------+--------------------------------------+
        |      | INT                 | Thermal strain intensity.            |
        |      +---------------------+--------------------------------------+
        |      | EQV                 | Thermal equivalent strain.           |
        +------+---------------------+--------------------------------------+
        | EPPL | X, Y, Z, XY, YZ, XZ | Component plastic strain.            |
        |      +---------------------+--------------------------------------+
        |      | 1, 2, 3             | Principal plastic strain.            |
        |      +---------------------+--------------------------------------+
        |      | INT                 | Plastic strain intensity.            |
        |      +---------------------+--------------------------------------+
        |      | EQV                 | Plastic equivalent strain.           |
        +------+---------------------+--------------------------------------+
        | EPCR | X, Y, Z, XY, YZ, XZ | Component creep strain.              |
        |      +---------------------+--------------------------------------+
        |      | 1, 2, 3             | Principal creep strain.              |
        |      +---------------------+--------------------------------------+
        |      | INT                 | Creep strain intensity.              |
        |      +---------------------+--------------------------------------+
        |      | EQV                 | Creep equivalent strain.             |
        +------+---------------------+--------------------------------------+

        Examples
        --------
        Return the averaged element displacement in the X
        direction.

        >>> arr = mapdl.post_processing.element_values("U", "X")
        >>> arr
        array([1.07396154e-06, 3.15631730e-06, 5.12543515e-06, ...,
               5.41204700e-06, 3.33649806e-06, 1.13836132e-06])

        Return the maximum element X component stress.

        >>> arr = mapdl.post_processing.element_values("S", "X", "max")
        >>> arr
        array([-1.12618148, -0.93902147, -0.88121128, ...,  0.        ,
                0.        ,  0.        ])

        Return the minimum element thermal equivalent strain.

        >>> arr = mapdl.post_processing.element_values("EPTH", "EQV", "min")
        >>> arr
        array([0., 0., 0., ..., 0., 0., 0.])

        """
        tmp_table = "__ETABLE__"
        self._mapdl.etable(tmp_table, item, comp, option, mute=True)
        return self._mapdl.get_array("ELEM", 1, "ETAB", tmp_table)[
            self.selected_elements
        ]

    def plot_nodal_values(self, item, comp, show_node_numbering=False, **kwargs):
        """Plot nodal values

        Displays solution results as continuous element contours.

        Equivalent MAPDL command:

        * ``PLNSOL``

        Parameters
        ----------
        item : str
            Label identifying the item.  See the table below in the
            notes section.

        comp : str, optional
            Component of the item if applicable.  See the table below
            in the notes section.

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the contact status for the selected elements.

        >>> mapdl.post_processing.plot_nodal_values(
        ...     "CONT", "STAT", scalar_bar_args={"title": "Contact status"}
        ... )
        """

        values = self.nodal_values(item=item, comp=comp)
        kwargs.setdefault(
            "scalar_bar_args", {"title": f"item: {item}\nComponent: {comp}"}
        )
        return self._plot_point_scalars(
            values, show_node_numbering=show_node_numbering, **kwargs
        )

    def plot_element_values(
        self, item, comp, option="AVG", show_elem_numbering=False, **kwargs
    ):
        """Plot element values.

        Displays the solution results as discontinuous element contours.

        Equivalent MAPDL command:

        * ``PLESOL``

        Parameters
        ----------
        item : str
            Label identifying the item.  See the table below in the
            notes section.

        comp : str, optional
            Component of the item if applicable.  See the table below
            in the notes section.

        option : str, optional
            Option for storing element table data.  One of the
            following:

            * ``"MIN"`` : Store minimum element nodal value of the
              specified item component.
            * ``"MAX"`` : Store maximum element nodal value of the
              specified item component.
            * ``"AVG"`` : Store averaged element centroid value of the
              specified item component (default).

        show_elem_numbering : bool, optional
            Plot the element numbers of the elements.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the contact status for the selected elements.

        >>> mapdl.post_processing.plot_element_values(
        ...     "CONT", "STAT", scalar_bar_args={"title": "Contact status"}
        ... )

        """
        kwargs.setdefault(
            "scalar_bar_args", {"title": f"item: {item}\nComponent: {comp}"}
        )
        return self._plot_cell_scalars(
            self.element_values(item, comp, option),
            show_elem_numbering=show_elem_numbering,
            **kwargs,
        )

    def _plot_point_scalars(self, scalars, show_node_numbering=False, **kwargs):
        """Plot point scalars"""
        if not scalars.size:
            raise MapdlRuntimeError(
                "Result unavailable.  Either the result has not been loaded "
                "with ``mapdl.set(step, sub_step)`` or the result does not "
                "exist within the result file."
            )

        mask = self.selected_nodes
        all_scalars = np.empty(mask.size)
        all_scalars[mask] = scalars

        # we can directly the node numbers as the array of selected
        # nodes will be a mask sized to the highest node index - 1
        surf = self._mapdl.mesh._surf
        node_id = surf["ansys_node_num"].astype(np.int32) - 1
        all_scalars = all_scalars[node_id]

        meshes = [
            {
                "mesh": surf.copy(deep=False),  # deep=False for ipyvtk-simple
                "scalar_bar_args": {"title": kwargs.pop("stitle", "")},
                "scalars": all_scalars,
            }
        ]

        labels = []
        if show_node_numbering:
            labels = [{"points": surf.points, "labels": surf["ansys_node_num"]}]

        return general_plotter(meshes, [], labels, mapdl=self, **kwargs)

    def _plot_cell_scalars(self, scalars, show_elem_numbering=False, **kwargs):
        """Plot cell scalars."""
        if not scalars.size:
            raise MapdlRuntimeError(
                "Result unavailable.  Either the result has not been loaded "
                "with ``mapdl.set(step, sub_step)`` or the result does not "
                "exist within the result file."
            )

        surf = self._mapdl.mesh._surf

        # as ``disp`` returns the result for all nodes, we need all node numbers
        # and to index to the output node numbers
        if hasattr(self._mapdl.mesh, "enum_all"):
            enum = self._mapdl.mesh.enum
        else:
            enum = self._all_enum

        # it's possible that there are duplicated element numbers,
        # therefore we need to get the unique values and a reverse index
        uni, ridx = np.unique(surf["ansys_elem_num"], return_inverse=True)
        mask = np.isin(enum, uni, assume_unique=True)

        if scalars.size != mask.size:
            scalars = scalars[self.selected_elements]
        scalars = scalars[mask][ridx]

        meshes = [
            {
                "mesh": surf.copy(deep=False),  # deep=False for ipyvtk-simple
                "scalar_bar_args": {"title": kwargs.pop("stitle", "")},
                "scalars": scalars,
            }
        ]

        labels = []
        if show_elem_numbering:
            labels = [
                {
                    "points": surf.cell_centers().points,
                    "labels": surf["ansys_elem_num"],
                }
            ]

        return general_plotter(meshes, [], labels, mapdl=self, **kwargs)

    @property
    @supress_logging
    def _all_nnum(self):
        self._mapdl.cm("__TMP_NODE__", "NODE")
        self._mapdl.allsel()
        nnum = self._mapdl.get_array("NODE", item1="NLIST")

        # rerun if encountered weird edge case of negative first index.
        if nnum[0] == -1:
            nnum = self._mapdl.get_array("NODE", item1="NLIST")
        self._mapdl.cmsel("S", "__TMP_NODE__", "NODE")
        return nnum.astype(np.int32, copy=False)

    @property
    @supress_logging
    def _all_enum(self):
        self._mapdl.cm("__TMP_ELEM__", "ELEM")
        self._mapdl.allsel()
        enum = self._mapdl.get_array("ELEM", item1="ELIST")

        # rerun if encountered weird edge case of negative first index.
        if enum[0] == -1:
            enum = self._mapdl.get_array("ELEM", item1="ELIST")
        self._mapdl.cmsel("S", "__TMP_ELEM__", "ELEM")
        return enum.astype(np.int32, copy=False)

    @property
    def _nsel(self):
        """Return the MAPDL formatted selected nodes array.

        -1 for unselected
        0 for undefined
        1 for selected

        """
        return self._ndof_rst("NSEL").astype(np.int8)

    @property
    def selected_nodes(self) -> np.ndarray:
        """Mask of the selected nodes.

        Examples
        --------
        The mask of the selected nodes.

        >>> mapdl.post_processing.selected_nodes
        array([False, False, False, ..., True, True, True])

        If you want the node numbers of the selected nodes.

        >>> mapdl.post_processing.selected_nodes.nonzero()[0] + 1
        array([1, 2, 3, 4, 5, 6, 7, 8, 9])

        """
        return self._nsel == 1

    @property
    def _esel(self):
        """Return the MAPDL formatted selected elements array.

        -1 for unselected
        0 for undefined
        1 for selected

        """
        return self._edof_rst("ESEL").astype(np.int8)

    @property
    def selected_elements(self) -> np.ndarray:
        """Mask of the selected elements.

        Examples
        --------
        >>> mapdl.post_processing.selected_elements
        array([False, False, False, ..., True, True, True])

        If you want the element numbers of the selected elements.

        >>> mapdl.post_processing.selected_elements.nonzero()[0] + 1
        array([1, 2, 3, 4, 5, 6, 7, 8, 9])

        """
        return self._esel == 1

    @check_result_loaded
    def _ndof_rst(self, item, it1num="", item2=""):
        """Nodal degree of freedom result using :func:`Mapdl.get_array()<ansys.mapdl.core.Mapdl.get_array`.

        Notes
        -----
        Item2 controls whether nodal-averaged results are
        used. Valid labels are:
        * ``AUTO`` - Use nodal-averaged results, if available. Otherwise
          use element-based
          results.
        * ``ESOL`` - Use element-based results only.
        * ``NAR`` - Use nodal-averaged results only.

        """
        values = self._mapdl.get_array("NODE", item1=item, it1num=it1num, item2=item2)
        if values.size == 0:  # pragma: no cover
            raise ValueError(
                f"The results obtained with '{item},{it1num},{item2}' are empty.\n"
                "You can check the MAPDL output by issuing:\n\n"
                f"mapdl.run('*vget,temp_array, node, , {item}, {it1num}, {item2}')"
            )
        else:
            return values

    @check_result_loaded
    def _edof_rst(self, item, it1num=""):
        """Element degree of freedom result"""
        return self._mapdl.get_array("ELEM", item1=item, it1num=it1num)

    def nodal_temperature(self) -> np.ndarray:
        """The nodal temperature of the current result.

        Equilvanent MAPDL command:
        ``PRNSOL, TEMP``

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero value.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero value.

        Examples
        --------
        >>> mapdl.post_processing.temperature
        array([0., 0., 0., ..., 0., 0., 0.])

        """
        return self.nodal_values("TEMP")

    def plot_nodal_temperature(self, show_node_numbering=False, **kwargs):
        """Plot nodal temperature of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal temperature for the second result

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.temperature()

        Plot off_screen and save a screenshot

        >>> mapdl.post_processing.plot_nodal_temperature(off_screen=True,
        ...                                              savefig='temp_1_2.png')

        Subselect a single result type and plot those stress results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_temperature(smooth_shading=True)
        """
        kwargs.setdefault("scalar_bar_args", {"title": "Nodal\nTemperature"})
        return self._plot_point_scalars(
            self.nodal_temperature(),
            show_node_numbering=show_node_numbering,
            **kwargs,
        )

    def nodal_displacement(self, component="NORM") -> np.ndarray:
        """Nodal X, Y, or Z structural displacement.

        Equilvanent MAPDL command:

        * ``PRNSOL, U, X``

        Parameters
        ----------
        component : str, optional
            Structural displacement component to retrieve.  Must be
            ``'X'``, ``'Y'``, ``'Z'``, ``'ALL'``, or ``'NORM'``.
            Defaults to ``'NORM'``.

        Returns
        -------
        numpy.ndarray
            Array containing the nodal structural displacement.

        Notes
        -----
        This command always returns all nodal displacements regardless
        of if the nodes are selected or not.

        Examples
        --------
        Displacement in the ``'X'`` direction for the current result.

        >>> mapdl.post_processing.nodal_displacement('X')
        array([1.07512979e-04, 8.59137773e-05, 5.70690047e-05, ...,
               5.70333124e-05, 8.58600402e-05, 1.07445726e-04])

        Displacement in all dimensions.

        >>> mapdl.post_processing.nodal_displacement('ALL')
        array([[ 1.07512979e-04,  6.05382076e-05, -1.64333622e-11],
               [ 8.59137773e-05,  7.88053970e-05, -1.93668243e-11],
               [ 5.70690047e-05,  1.23100157e-04, -1.04703715e-11],
               ...,
               [ 5.70333124e-05,  1.23023176e-04, -9.77598660e-12],
               [ 8.58600402e-05,  7.87561008e-05, -9.12531408e-12],
               [ 1.07445726e-04,  6.05003408e-05, -1.23634647e-11]])

        Nodes corresponding to the nodal displacements.

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        component = check_comp(component, DISP_TYPE)

        if component in ["NORM", "ALL"]:
            x = self.nodal_values("U", "X")
            y = self.nodal_values("U", "Y")
            z = self.nodal_values("U", "Z")
            disp = np.vstack((x, y, z))
            if component == "NORM":
                return np.linalg.norm(disp, axis=0)
            return disp.T

        return self.nodal_values("U", component)

    def plot_nodal_displacement(
        self, component="NORM", show_node_numbering=False, **kwargs
    ):
        """Plot nodal displacement

        Parameters
        ----------
        component : str, optional
            Structural displacement component to retrieve.  Must be
            ``'X'``, ``'Y'``, ``'Z'``, or ``'NORM'``.  Defaults to
            ``'NORM'``.
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.
        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the normalized nodal displacement for the second result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_displacement('NORM',
        ...                                               smooth_shading=True)

        Plot the x displacement without smooth shading with individual
        node numbering.

        >>> mapdl.post_processing.plot_nodal_displacement('X',
        ...                                               show_node_numbering=True)
        """
        if isinstance(component, str):
            if component.upper() == "ALL":
                raise ValueError(
                    '"ALL" not allowed in this context.  Select a '
                    'single displacement component (e.g. "X")'
                )

        disp = self.nodal_displacement(component)
        kwargs.setdefault("scalar_bar_args", {"title": "%s Displacement" % component})
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_rotation(self, component="ALL") -> np.ndarray:
        """Nodal X, Y, or Z structural rotation

        Equilvanent MAPDL commands:

        * ``PRNSOL, ROT, X``
        * ``PRNSOL, ROT, Y``
        * ``PRNSOL, ROT, Z``

        Parameters
        ----------
        component : str, optional
            Structural rotational component to retrieve.  Must be
            ``'X'``, ``'Y'``, ``'Z'``, or ``'ALL'``.  Defaults to ``'ALL'``.

        Returns
        -------
        numpy.ndarray
            Numpy array with nodal X, Y, Z, or all structural rotations.

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the
        :attr:`selected_nodes <PostProcessing.selected_nodes>` mask to
        get the currently selected nodes.

        Examples
        --------
        Nodal rotation in all dimensions for current result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_rotation('ALL')
        array([[0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.],
               ...,
               [0., 0., 0.],
               [0., 0., 0.],
               [0., 0., 0.]])

        Nodes corresponding to the nodal rotations.

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        component = check_comp(component, ROT_TYPE)

        if component == "ALL":
            x = self.nodal_values("ROT", "X")
            y = self.nodal_values("ROT", "Y")
            z = self.nodal_values("ROT", "Z")
            return np.vstack((x, y, z)).T

        return self.nodal_values("ROT", component)

    def plot_nodal_rotation(self, component, show_node_numbering=False, **kwargs):
        """Plot nodal rotation.

        Parameters
        ----------
        component : str
            Structural rotation component to retrieve.  Must be
            ``'X'``, ``'Y'``, or ``'Z'``.

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the x rotation without smooth shading with individual
        node numbering.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_rotation('X', show_node_numbering=True)
        """
        if isinstance(component, str):
            if component.upper() == "ALL":
                raise ValueError(
                    '"ALL" not allowed in this context.  Select a '
                    'single component (e.g. "X")'
                )

        disp = self.nodal_rotation(component)
        kwargs.setdefault("scalar_bar_args", {"title": f"{component} Rotation"})
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def element_displacement(self, component="ALL", option="AVG") -> np.ndarray:
        """Return element displacement.

        One value per element.  Either minimum, maximum, or average of
        all nodes in each element.

        Equilvanent MAPDL commands:

        * ``ETABLE,VALUES,U,X``
        * ``PRETAB,VALUES`` or ``*VGET,TMP,ELEM,1,ETAB,VALUES``

        Parameters
        ----------
        component : str, optional
            Structural displacement component to retrieve.  Must be
            ``"X"``, ``"Y"``, ``"Z"``, ``"ALL"`` or ``"NORM"``.  Defaults to
            ``"ALL"``.
        option : str, optional
            Option for storing element table data.  One of the
            following:

            * ``"MIN"`` : Store minimum element nodal value of the
              specified item component.
            * ``"MAX"`` : Store maximum element nodal value of the
              specified item component.
            * ``"AVG"`` : Store averaged element centroid value of the
              specified item component (default).

        Examples
        --------
        Return the average element displacement for all components.

        >>> arr = mapdl.post_processing.element_displacement("ALL")
        >>> arr.shape
        (2080, 3)
        >>> arr
        array([[ 1.07396154e-06, -9.03608033e-06, -5.17768108e-12],
               [ 3.15631730e-06, -2.65527340e-05,  1.07714512e-11],
               [ 5.12543515e-06, -4.31175194e-05,  2.19929719e-12],
               ...,
               [ 5.41204700e-06, -4.80335719e-05,  7.75819589e-11],
               [ 3.33649806e-06, -2.96109417e-05,  1.44947535e-10],
               [ 1.13836132e-06, -1.01038096e-05,  6.95566641e-11]])

        """
        check_elem_option(option)
        component = component.upper()
        check_comp(component, DISP_TYPE)

        if component in ["ALL", "NORM"]:
            disp = np.vstack(
                (
                    self.element_values("U", "X", option),
                    self.element_values("U", "Y", option),
                    self.element_values("U", "Z", option),
                )
            ).T
            if component == "NORM":
                return np.linalg.norm(disp, axis=1)
            return disp

        return self.element_values("U", component, option)

    def plot_element_displacement(
        self,
        component="NORM",
        option="AVG",
        show_elem_numbering=False,
        **kwargs,
    ):
        """Plot element displacement.

        Parameters
        ----------
        component : str, optional
            Structural displacement component to retrieve.  Must be
            ``"X"``, ``"Y"``, ``"Z"``, or ``"NORM"``.

        option : str, optional
            Option for storing element table data.  One of the
            following:

            * ``"MIN"`` : Store minimum element nodal value of the
              specified item component.
            * ``"MAX"`` : Store maximum element nodal value of the
              specified item component.
            * ``"AVG"`` : Store averaged element centroid value of the
              specified item component (default).

        show_elem_numbering : bool, optional
            Plot the element numbers of the elements.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the mean normalized element displacement for the first
        result in the "X" direction.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.plot_element_displacement(
        ...     "NORM",
        ...     option="AVG"
        ... )

        """
        if component.upper() == "ALL":
            raise ValueError(
                '"ALL" not allowed in this context.  Select a '
                'single displacement component (e.g. "X" or "NORM")'
            )

        if component.upper() == "NORM":
            disp = np.linalg.norm(
                self.element_displacement("ALL", option=option), axis=1
            )
        else:
            disp = self.element_displacement(component, option=option)
        kwargs.setdefault(
            "scalar_bar_args", {"title": f"{component} Element Displacement"}
        )
        return self._plot_cell_scalars(
            disp, show_elem_numbering=show_elem_numbering, **kwargs
        )

    def element_stress(self, component, option="AVG") -> np.ndarray:
        """Return element component or principal stress.

        One value per element.  Either minimum, maximum, or average of
        all nodes in each element.

        Equilvanent MAPDL commands:

        * ``ETABLE,VALUES,S,X``
        * ``PRETAB,VALUES`` or ``*VGET,TMP,ELEM,1,ETAB,VALUES``

        Parameters
        ----------
        component : str
            Element stress to retrieve.  One of the following:

            +---------------------+--------------------+
            | X, Y, Z, XY, YZ, XZ | Component stress.  |
            +---------------------+--------------------+
            | 1, 2, 3             | Principal stress.  |
            +---------------------+--------------------+
            | INT                 | Stress intensity.  |
            +---------------------+--------------------+
            | EQV                 | Equivalent stress  |
            +---------------------+--------------------+

        option : str, optional
            Option for storing element table data.  One of the
            following:

            * ``"MIN"`` : Store minimum element nodal value of the
              specified item component.
            * ``"MAX"`` : Store maximum element nodal value of the
              specified item component.
            * ``"AVG"`` : Store averaged element centroid value of the
              specified item component (default).

        Returns
        -------
        numpy.ndarray
            Numpy array of stresses.

        Examples
        --------
        Return the average element component stress in the X direction.

        >>> arr = mapdl.post_processing.element_stress("X")
        >>> arr.shape
        (2080, 3)
        >>> arr
        array([-0.29351357, -0.37027832, -0.37340827, ...,  0.        ,
                0.        ,  0.        ])

        """
        component = elem_check_inputs(component, option, STRESS_TYPES)
        return self.element_values("S", component, option)

    def plot_element_stress(
        self, component, option="AVG", show_elem_numbering=False, **kwargs
    ):
        """Plot element component or principal stress.

        One value per element.  Either minimum, maximum, or average of
        all nodes in each element.

        Parameters
        ----------
        component : str
          Element stress to retrieve.  One of the following:

          +---------------------+--------------------+
          | X, Y, Z, XY, YZ, XZ | Component stress.  |
          +---------------------+--------------------+
          | 1, 2, 3             | Principal stress.  |
          +---------------------+--------------------+
          | INT                 | Stress intensity.  |
          +---------------------+--------------------+
          | EQV                 | Equivalent stress  |
          +---------------------+--------------------+

        option : str, optional
          Option for storing element table data.  One of the
          following:

          * ``"MIN"`` : Store minimum element nodal value of the
            specified item component.
          * ``"MAX"`` : Store maximum element nodal value of the
            specified item component.
          * ``"AVG"`` : Store averaged element centroid value of the
            specified item component (default).
        show_elem_numbering : bool, optional
            Plot the element numbers of the elements.
        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`
        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the average element component stress in the X direction.

        >>> mapdl.post_processing.plot_element_stress("X")

        """
        component = str(component).upper()
        stress = self.element_stress(component, option=option)

        if component in COMPONENT_STRESS_TYPE:
            kwargs.setdefault(
                "scalar_bar_args",
                {"title": f"{component} Component Element Stress"},
            )
        elif component in ["1", "2", "3"]:
            kwargs.setdefault(
                "scalar_bar_args",
                {"title": f"{component} Principal Element Stress"},
            )
        elif component == "INT":
            kwargs.setdefault("scalar_bar_args", {"title": "Element Stress Intensity"})
        elif component == "EQV":
            kwargs.setdefault("scalar_bar_args", {"title": "Element Equivalent Stress"})

        return self._plot_cell_scalars(
            stress, show_elem_numbering=show_elem_numbering, **kwargs
        )

    def element_temperature(self, option="AVG") -> np.ndarray:
        """Return element temperature.

        One value per element.  Either minimum, maximum, or average of
        all nodes in each element.

        Equilvanent MAPDL commands:

        * ``ETABLE,VALUES,TEMP``
        * ``PRETAB,VALUES`` or ``*VGET,TMP,ELEM,1,ETAB,VALUES``

        Parameters
        ----------
        option : str, optional
            Option for storing element table data.  One of the
            following:

            * ``"MIN"`` : Store minimum element nodal value of the
              specified item.
            * ``"MAX"`` : Store maximum element nodal value of the
              specified item.
            * ``"AVG"`` : Store averaged element centroid value of the
              specified item (default).

        Examples
        --------
        Return the average element temperature.

        >>> arr = mapdl.post_processing.element_temperature()
        >>> arr.shape
        (2080, 3)
        >>> arr
        array([20., 20., 20., ..., 20., 20., 20.])

        """
        return self.element_values("TEMP", option=option)

    def plot_element_temperature(
        self, option="AVG", show_elem_numbering=False, **kwargs
    ):
        """Plot element temperature.

        One value per element.  Either minimum, maximum, or average of
        all nodes in each element.

        Parameters
        ----------
        option : str, optional
            Option for storing element table data.  One of the
            following:

            * ``"MIN"`` : Store minimum element nodal value of the
              specified item component.
            * ``"MAX"`` : Store maximum element nodal value of the
              specified item component.
            * ``"AVG"`` : Store averaged element centroid value of the
              specified item component (default).

        show_elem_numbering : bool, optional
            Plot the element numbers of the elements.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the average element temperature.

        >>> arr = mapdl.post_processing.plot_element_temperature()

        """
        scalars = self.element_temperature(option)

        return self._plot_cell_scalars(
            scalars, show_elem_numbering=show_elem_numbering, **kwargs
        )

    def nodal_pressure(self) -> np.ndarray:
        """The nodal pressure of the current result.

        Equilvanent MAPDL command:
        ``PRNSOL, PRES``

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero value.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero value.

        Examples
        --------
        >>> mapdl.post_processing.pressure()
        array([0., 0., 0., ..., 0., 0., 0.])

        """
        return self.nodal_values("PRES")

    def plot_nodal_pressure(self, show_node_numbering=False, **kwargs):
        """Plot nodal pressure of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal pressure for the second result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_pressure()

        Plot off_screen and save a screenshot

        >>> mapdl.post_processing.plot_nodal_pressure(off_screen=True,
        ...                                           savefig='temp_1_2.png')

        Subselect a single result type and plot those stress results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_pressure(smooth_shading=True)
        """
        kwargs.setdefault("scalar_bar_args", {"title": "Nodal\nPressure"})
        return self._plot_point_scalars(
            self.nodal_pressure(),
            show_node_numbering=show_node_numbering,
            **kwargs,
        )

    def nodal_voltage(self) -> np.ndarray:
        """The nodal voltage of the current result.

        Equilvanent MAPDL command:

        * ``PRNSOL, PRES``

        Returns
        -------
        numpy.ndarray
            Numpy array containing the nodal voltage of the current
            result.

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero value.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero value.

        Examples
        --------
        Return the voltage of the current result.

        >>> mapdl.post_processing.voltage()
        array([0., 0., 0., ..., 0., 0., 0.])
        """
        return self.nodal_values("VOLT")

    def plot_nodal_voltage(self, show_node_numbering=False, **kwargs):
        """Plot nodal voltage of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.
        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal voltage for the second result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_voltage()

        Plot off screen and save a screenshot.

        >>> mapdl.post_processing.plot_nodal_voltage(off_screen=True,
        ...                                          savefig='temp_1_2.png')

        Subselect a single result type and plot those stress results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_voltage(smooth_shading=True)
        """
        kwargs.setdefault("scalar_bar_args", {"title": "Nodal\nVoltage"})
        return self._plot_point_scalars(
            self.nodal_voltage(),
            show_node_numbering=show_node_numbering,
            **kwargs,
        )

    def nodal_component_stress(self, component) -> np.ndarray:
        """Nodal component stress.

        Equilvanent MAPDL commands:

        * ``VGET, PARM, NODE, , S, X``
        * ``PRNSOL, S, COMP``

        Parameters
        ----------
        component : str, optional
            Nodal component stress component to retrieve.  Must be
            ``'X'``, ``'Y'``, ``'Z'``, ``'XY'``, ``'YZ'``, or
            ``'XZ'``.

        Returns
        -------
        numpy.ndarray
            Numpy array containing the nodal component stress for the
            selected ``component``.

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the ``selected_nodes``
        mask to get the currently selected nodes.

        Examples
        --------
        Nodal stress in the X direction for the first result

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_component_stress('X')
            array([0.60024621, 0.61625265, 0.65081825, ...,
                   0.        , 0.        , 0.        ])

        Corresponding nodes

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        component = check_comp(component, COMPONENT_STRESS_TYPE)
        return self.nodal_values("S", component)

    def plot_nodal_component_stress(
        self, component, show_node_numbering=False, **kwargs
    ):
        """Plot nodal component stress.

        Parameters
        ----------
        component : str
            Nodal component stress component to plot.  Must be
            ``'X'``, ``'Y'``, ``'Z'``, ``'XY'``, ``'YZ'``, or
            ``'XZ'``.
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.
        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the x nodal component stress for the second result set.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_component_stress('X')
        """
        disp = self.nodal_component_stress(component)
        kwargs.setdefault("scalar_bar_args", {"title": f"{component} Nodal\nStress"})
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_principal_stress(self, component) -> np.ndarray:
        """Nodal principal stress.

        Equilvanent MAPDL commands:

        * ``*VGET, PARM, NODE, , S, 1``
        * ``PRNSOL, S, PRIN``

        Parameters
        ----------
        component : str, optional
            Nodal component stress component to retrieve.  Must be
            ``'1'``, ``'2'``, or ``'3'``

        Returns
        -------
        numpy.ndarray
            Numpy array containing the nodal principal stress.

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the ``selected_nodes``
        mask to get the currently selected nodes.

        Examples
        --------
        Nodal stress in the S1 direction for the first result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_principal_stress('1')
            array([0.60024621, 0.61625265, 0.65081825, ...,
                   0.        , 0.        , 0.        ])

        Corresponding nodes.

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        if isinstance(component, int):
            component = str(component)
        component = check_comp(component, PRINCIPAL_TYPE)
        return self.nodal_values("S", component)

    def plot_nodal_principal_stress(
        self, component, show_node_numbering=False, **kwargs
    ):
        """Plot nodal principal stress.

        Parameters
        ----------
        component : str
            Nodal component stress component to plot.  Must be
            ``'1'``, ``'2'``, or ``'3'``
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.
        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal principal stress "1" for the second result set

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_principal_stress('1')
        """
        disp = self.nodal_principal_stress(component)
        kwargs.setdefault(
            "scalar_bar_args", {"title": f"{component} Nodal\nPrincipal Stress"}
        )
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_stress_intensity(self) -> np.ndarray:
        """The nodal stress intensity of the current result.

        Equilvanent MAPDL command: ``PRNSOL, S, PRIN``

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero stress.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero stress value.

        Examples
        --------
        Stress intensity for result 2

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_stress_intensity()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("S", "INT")

    def plot_nodal_stress_intensity(self, show_node_numbering=False, **kwargs):
        """Plot the nodal stress intensity of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the equivalent stress for the second result

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_stress_intensity()

        Plot off_screen and save a screenshot

        >>> mapdl.post_processing.plot_nodal_stress_intensity(off_screen=True,
                                                              savefig='seqv_00.png')

        Subselect a single result type and plot those stress results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_stress_intensity(smooth_shading=True)

        """
        scalars = self.nodal_stress_intensity()
        kwargs.setdefault("scalar_bar_args", {"title": "Nodal Stress\nIntensity"})
        return self._plot_point_scalars(
            scalars, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_eqv_stress(self) -> np.ndarray:
        """The nodal equivalent stress of the current result.

        Equilvanent MAPDL command: ``PRNSOL, S, PRIN``

        Returns
        -------
        numpy.ndarray
            Numpy array containing the nodal equivalent stress of the
            current result.

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero stress.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero stress value.

        Examples
        --------
        >>> mapdl.post_processing.nodal_eqv_stress()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        Stress from result 2

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_eqv_stress()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("S", "EQV")

    def plot_nodal_eqv_stress(self, show_node_numbering=False, **kwargs):
        """Plot nodal equivalent stress of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the equivalent stress for the second result

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_eqv_stress()

        Plot off_screen and save a screenshot

        >>> mapdl.post_processing.plot_nodal_eqv_stress(off_screen=True,
                                                        savefig='seqv_00.png')

        Subselect a single result type and plot those stress results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_eqv_stress(smooth_shading=True)

        """
        scalars = self.nodal_eqv_stress()
        kwargs.setdefault("scalar_bar_args", {"title": "Nodal Equivalent\nStress"})
        return self._plot_point_scalars(
            scalars, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_total_component_strain(self, component) -> np.ndarray:
        """Total nodal component strain

        Includes elastic, plastic, and creep strain.

        Equilvanent MAPDL commands:

        * ``*VGET, PARM, NODE, , EPTO, X``

        Parameters
        ----------
        component : str, optional
            Component to retrieve.  Must be ``'X'``, ``'Y'``, ``'Z'``,
            ``'XY'``, ``'YZ'``, or ``'XZ'``.

        Returns
        -------
        numpy.ndarray
            Array containing the total nodal component strain.

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the ``selected_nodes``
        mask to get the currently selected nodes.

        Examples
        --------
        Total component strain in the X direction for the first result

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_total_component_strain('X')
            array([0.60024621, 0.61625265, 0.65081825, ...,
                   0.        , 0.        , 0.        ])

        Corresponding nodes

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        if isinstance(component, int):
            component = str(component)
        component = check_comp(component, COMPONENT_STRESS_TYPE)
        return self.nodal_values("EPTO", component)

    def plot_nodal_total_component_strain(
        self, component, show_node_numbering=False, **kwargs
    ):
        """Plot nodal total component starin.

        Includes elastic, plastic, and creep strain.

        Parameters
        ----------
        component : str, optional
            Component to retrieve.  Must be ``'X'``, ``'Y'``, ``'Z'``,
            ``'XY'``, ``'YZ'``, or ``'XZ'``.

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot total component strain in the X direction for the first result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.plot_nodal_total_component_strain('X')
        """
        disp = self.nodal_total_component_strain(component)
        kwargs.setdefault(
            "scalar_bar_args",
            {"title": f"{component} Total Nodal\nComponent Strain"},
        )
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_total_principal_strain(self, component) -> np.ndarray:
        """Total nodal principal total strain.

        Includes elastic, plastic, and creep strain.

        Equilvanent MAPDL command:

        * ``*VGET,PARM,NODE,,EPTO,1``

        Parameters
        ----------
        component : str, optional
            Component to retrieve.  Must be ``'1'``, ``'2'``, or
            ``'3'``

        Returns
        -------
        numpy.ndarray
            Numpy array total nodal principal total strain.

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the ``selected_nodes``
        mask to get the currently selected nodes.

        Examples
        --------
        Principal nodal strain in the S1 direction for the first result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_total_principal_strain('1')
            array([0.60024621, 0.61625265, 0.65081825, ...,
                   0.        , 0.        , 0.        ])

        Corresponding nodes.

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        if isinstance(component, int):
            component = str(component)
        component = check_comp(component, PRINCIPAL_TYPE)
        return self.nodal_values("EPTO", component)

    def plot_nodal_total_principal_strain(
        self, component, show_node_numbering=False, **kwargs
    ):
        """Plot total nodal principal strain.

        Includes elastic, plastic, and creep strain.

        Parameters
        ----------
        component : str
            Nodal principal strain component to plot.  Must be
            ``'1'``, ``'2'``, or ``'3'``

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the principal nodal strain in the S1 direction for the
        first result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_total_principal_strain('1')
        """
        disp = self.nodal_total_principal_strain(component)
        kwargs.setdefault(
            "scalar_bar_args",
            {"title": "%s Nodal\nPrincipal Strain" % component},
        )
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_total_strain_intensity(self) -> np.ndarray:
        """The total nodal strain intensity of the current result.

        Equilvanent MAPDL command:

        * ``PRNSOL, EPTO, PRIN``

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero stress.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero stress value.

        Examples
        --------
        Total strain intensity for result 2

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_total_strain_intensity()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("EPEL", "INT")

    def plot_nodal_total_strain_intensity(self, show_node_numbering=False, **kwargs):
        """Plot the total nodal strain intensity of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the total strain intensity for the second result

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_total_strain_intensity()

        Plot off_screen and save a screenshot

        >>> mapdl.post_processing.plot_nodal_total_strain_intensity(
        ...     off_screen=True,
        ...     savefig='seqv_00.png'
        ...     )

        Subselect a single result type and plot those strain results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_total_strain_intensity()

        """
        scalars = self.nodal_total_strain_intensity()
        kwargs.setdefault("scalar_bar_args", {"title": "Total Nodal\nStrain Intensity"})
        return self._plot_point_scalars(
            scalars, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_total_eqv_strain(self) -> np.ndarray:
        """The total nodal equivalent strain of the current result.

        Equilvanent MAPDL command:

        * ``PRNSOL, EPTO, PRIN``

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero stress.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero stress value.

        Examples
        --------
        Total quivalent strain for the current result.

        >>> mapdl.post_processing.nodal_total_eqv_strain()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        Strain from result 2.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_total_eqv_strain()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("EPTO", "EQV")

    def plot_nodal_total_eqv_strain(self, show_node_numbering=False, **kwargs):
        """Plot the total nodal equivalent strain of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the total equivalent strain for the second result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_total_eqv_strain()

        Plot off screen and save a screenshot.

        >>> mapdl.post_processing.plot_nodal_total_eqv_strain(off_screen=True,
        ...                                                   savefig='seqv_00.png')

        Subselect a single result type and plot those strain results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_total_eqv_strain(smooth_shading=True)

        """
        scalars = self.nodal_total_eqv_strain()
        kwargs.setdefault(
            "scalar_bar_args", {"title": "Total Nodal\nEquivalent Strain"}
        )
        return self._plot_point_scalars(
            scalars, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_elastic_component_strain(self, component) -> np.ndarray:
        """Elastic nodal component strain

        Equivalent MAPDL command:

        * ``PRNSOL,EPEL,PRIN``

        Parameters
        ----------
        component : str
            Component to retrieve.  Must be ``'X'``, ``'Y'``, ``'Z'``,
            ``'XY'``, ``'YZ'``, or ``'XZ'``.

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the ``selected_nodes``
        mask to get the currently selected nodes.

        Examples
        --------
        Elastic component strain in the X direction for the first result

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_elastic_component_strain('X')
            array([0.60024621, 0.61625265, 0.65081825, ...,
                   0.        , 0.        , 0.        ])

        Corresponding nodes

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        if isinstance(component, int):
            component = str(component)
        component = check_comp(component, COMPONENT_STRESS_TYPE)
        return self.nodal_values("EPEL", component)

    def plot_nodal_elastic_component_strain(
        self, component, show_node_numbering=False, **kwargs
    ):
        """Plot nodal elastic component strain.

        Parameters
        ----------
        component : str
            Nodal elastic component to plot.  Must be ``'X'``,
            ``'Y'``, ``'Z'``, ``'XY'``, ``'YZ'``, or ``'XZ'``.

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal elastic principal strain "1" for the second result set.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_elastic_component_strain('1')
        """
        disp = self.nodal_elastic_component_strain(component)
        kwargs.setdefault(
            "scalar_bar_args",
            {"title": "%s Elastic Nodal\nComponent Strain" % component},
        )
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_elastic_principal_strain(self, component) -> np.ndarray:
        """Nodal elastic principal elastic strain.

        Equivalent MAPDL commands:

        * ``*VGET, PARM, NODE, , EPEL, 1``

        Parameters
        ----------
        component : str, optional
            Component to retrieve.  Must be ``'1'``, ``'2'``, or
            ``'3'``.

        Returns
        -------
        numpy.ndarray
            Numpy array of nodal elastic principal elastic strain.

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the ``selected_nodes``
        mask to get the currently selected nodes.

        Examples
        --------
        Principal nodal strain in the ``S1`` direction for the first
        result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_elastic_principal_strain('1')
            array([0.60024621, 0.61625265, 0.65081825, ...,
                   0.        , 0.        , 0.        ])

        Corresponding nodes.

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        if isinstance(component, int):
            component = str(component)
        component = check_comp(component, PRINCIPAL_TYPE)
        return self.nodal_values("EPEL", component)

    def plot_nodal_elastic_principal_strain(
        self, component, show_node_numbering=False, **kwargs
    ):
        """Plot elastic nodal principal strain.

        Parameters
        ----------
        component : str
            Nodal principal strain component to plot.  Must be
            ``'1'``, ``'2'``, or ``'3'``

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal principal strain "1" for the second result set.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_elastic_principal_strain('1')
        """
        disp = self.nodal_elastic_principal_strain(component)
        kwargs.setdefault(
            "scalar_bar_args",
            {"title": "%s Nodal\nPrincipal Strain" % component},
        )
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_elastic_strain_intensity(self) -> np.ndarray:
        """The elastic nodal strain intensity of the current result.

        Equivalent MAPDL command:

        * ``PRNSOL, EPEL, PRIN``

        Returns
        -------
        numpy.ndarray
            The elastic nodal strain intensity of the current result.

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero value.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero value.

        Examples
        --------
        Return the elastic strain intensity for result 2.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_elastic_strain_intensity()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("EPEL", "INT")

    def plot_nodal_elastic_strain_intensity(self, show_node_numbering=False, **kwargs):
        """Plot the elastic nodal strain intensity of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the elastic strain intensity for the second result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_elastic_strain_intensity()

        Plot off_screen and save a screenshot.

        >>> mapdl.post_processing.plot_nodal_elastic_strain_intensity(off_screen=True,
        ...                                                           savefig='seqv_00.png')

        Subselect a single result type and plot those strain results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_elastic_strain_intensity()

        """
        scalars = self.nodal_elastic_strain_intensity()
        kwargs.setdefault(
            "scalar_bar_args", {"title": "Elastic Nodal\nStrain Intensity"}
        )
        return self._plot_point_scalars(
            scalars, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_elastic_eqv_strain(self) -> np.ndarray:
        """The elastic nodal equivalent strain of the current result.

        Equivalent MAPDL command:
        ``PRNSOL, EPEL, PRIN``

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero value.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero value.

        Examples
        --------
        Elastic quivalent strain for the current result.

        >>> mapdl.post_processing.nodal_elastic_eqv_strain()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        Strain from result 2.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_elastic_eqv_strain()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("EPEL", "EQV")

    def plot_nodal_elastic_eqv_strain(self, show_node_numbering=False, **kwargs):
        """Plot the elastic nodal equivalent strain of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the elastic equivalent strain for the second result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_elastic_eqv_strain()

        Plot off screen and save a screenshot.

        >>> mapdl.post_processing.plot_nodal_elastic_eqv_strain(off_screen=True,
        ...                                                     savefig='seqv_00.png')

        Subselect a single result type and plot those strain results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_elastic_eqv_strain(smooth_shading=True)

        """
        scalars = self.nodal_elastic_eqv_strain()
        kwargs.setdefault(
            "scalar_bar_args", {"title": "Elastic Nodal\n Equivalent Strain"}
        )
        return self._plot_point_scalars(
            scalars, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_plastic_component_strain(self, component) -> np.ndarray:
        """Plastic nodal component strain.

        Equivalent MAPDL command:

        * ``PRNSOL, EPPL, PRIN``

        Parameters
        ----------
        component : str, optional
            Component to retrieve.  Must be ``'X'``, ``'Y'``, ``'Z'``,
            ``'XY'``, ``'YZ'``, or ``'XZ'``.

        Returns
        -------
        numpy.ndarray
            Numpy array of the plastic nodal component strain.

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the ``selected_nodes``
        mask to get the currently selected nodes.

        Examples
        --------
        Plastic component strain in the X direction for the first result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_plastic_component_strain('X')
            array([0.60024621, 0.61625265, 0.65081825, ...,
                   0.        , 0.        , 0.        ])

        Corresponding nodes.

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        if isinstance(component, int):
            component = str(component)
        component = check_comp(component, COMPONENT_STRESS_TYPE)
        return self.nodal_values("EPPL", component)

    def plot_nodal_plastic_component_strain(
        self, component, show_node_numbering=False, **kwargs
    ):
        """Plot nodal plastic component strain.

        Parameters
        ----------
        component : str
            Nodal plastic component to plot.  Must be ``'X'``,
            ``'Y'``, ``'Z'``, ``'XY'``, ``'YZ'``, or ``'XZ'``.

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal plastic principal strain "1" for the second result set.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_plastic_component_strain('1')
        """
        disp = self.nodal_plastic_component_strain(component)
        kwargs.setdefault(
            "scalar_bar_args",
            {"title": "%s Plastic Nodal\nComponent Strain" % component},
        )
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_plastic_principal_strain(self, component) -> np.ndarray:
        """Nodal plastic principal plastic strain.

        Equivalent MAPDL commands:

        * ``*VGET, PARM, NODE, , EPPL, 1``

        Parameters
        ----------
        component : str, optional
            Component to retrieve.  Must be ``'1'``, ``'2'``, or
            ``'3'``

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the ``selected_nodes``
        mask to get the currently selected nodes.

        Examples
        --------
        Principal nodal strain in the S1 direction for the first result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_plastic_principal_strain('1')
            array([0.60024621, 0.61625265, 0.65081825, ...,
                   0.        , 0.        , 0.        ])

        Corresponding nodes

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        if isinstance(component, int):
            component = str(component)
        component = check_comp(component, PRINCIPAL_TYPE)
        return self.nodal_values("EPPL", component)

    def plot_nodal_plastic_principal_strain(
        self, component, show_node_numbering=False, **kwargs
    ):
        """Plot plastic nodal principal strain.

        Parameters
        ----------
        component : str
            Nodal principal strain component to plot.  Must be
            ``'1'``, ``'2'``, or ``'3'``

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal principal strain "1" for the second result set.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_plastic_principal_strain('1')
        """
        disp = self.nodal_plastic_principal_strain(component)
        kwargs.setdefault(
            "scalar_bar_args",
            {"title": "%s Nodal\nPrincipal Strain" % component},
        )
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_plastic_strain_intensity(self) -> np.ndarray:
        """The plastic nodal strain intensity of the current result.

        Equivalent MAPDL command:

        * ``PRNSOL, EPPL, PRIN``

        Returns
        -------
        numpy.ndarray
            Numpy array containing the plastic nodal strain intensity
            of the current result.

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero value.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero value.

        Examples
        --------
        Plastic strain intensity for result 2.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_plastic_strain_intensity()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("EPPL", "INT")

    def plot_nodal_plastic_strain_intensity(self, show_node_numbering=False, **kwargs):
        """Plot the plastic nodal strain intensity of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the plastic strain intensity for the second result

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_plastic_strain_intensity()

        Plot off_screen and save a screenshot

        >>> mapdl.post_processing.plot_nodal_plastic_strain_intensity(off_screen=True,
        ...                                                           savefig='seqv_00.png')

        Subselect a single result type and plot those strain results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_plastic_strain_intensity()

        """
        scalars = self.nodal_plastic_strain_intensity()
        kwargs.setdefault(
            "scalar_bar_args", {"title": "Plastic Nodal\nStrain Intensity"}
        )
        return self._plot_point_scalars(
            scalars, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_plastic_eqv_strain(self) -> np.ndarray:
        """The plastic nodal equivalent strain of the current result.

        Equivalent MAPDL command:

        * ``PRNSOL, EPPL, PRIN``

        Returns
        -------
        numpy.ndarray
            Numpy array containing the plastic nodal equivalent strain
            of the current result.

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero value.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero value.

        Examples
        --------
        Plastic quivalent strain for the current result

        >>> mapdl.post_processing.nodal_plastic_eqv_strain()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        Strain from result 2

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_plastic_eqv_strain()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("EPPL", "EQV")

    def plot_nodal_plastic_eqv_strain(self, show_node_numbering=False, **kwargs):
        """Plot the plastic nodal equivalent strain of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the plastic equivalent strain for the second result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_plastic_eqv_strain()

        Plot off_screen and save a screenshot.

        >>> mapdl.post_processing.plot_nodal_plastic_eqv_strain(off_screen=True,
        ...                                                     savefig='seqv_00.png')

        Subselect a single result type and plot those strain results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_plastic_eqv_strain(smooth_shading=True)

        """
        scalars = self.nodal_plastic_eqv_strain()
        kwargs.setdefault(
            "scalar_bar_args", {"title": "Plastic Nodal\n Equivalent Strain"}
        )
        return self._plot_point_scalars(
            scalars, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_thermal_component_strain(self, component) -> np.ndarray:
        """Thermal nodal component strain

        Equivalent MAPDL command:

        * ``PRNSOL, EPTH, PRIN``

        Parameters
        ----------
        component : str, optional
            Component to retrieve.  Must be ``'X'``, ``'Y'``, ``'Z'``,
            ``'XY'``, ``'YZ'``, or ``'XZ'``.

        Returns
        -------
        numpy.ndarray
            Numpy array containing the thermal nodal component strain
            for the specified ``component``.

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the ``selected_nodes``
        mask to get the currently selected nodes.

        Examples
        --------
        Thermal component strain in the X direction for the first result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_thermal_component_strain('X')
            array([0.60024621, 0.61625265, 0.65081825, ...,
                   0.        , 0.        , 0.        ])

        Corresponding nodes.

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        if isinstance(component, int):
            component = str(component)
        component = check_comp(component, COMPONENT_STRESS_TYPE)
        return self.nodal_values("EPTH", component)

    def plot_nodal_thermal_component_strain(
        self, component, show_node_numbering=False, **kwargs
    ):
        """Plot nodal thermal component strain.

        Parameters
        ----------
        component : str
            Nodal thermal component to plot.  Must be ``'X'``,
            ``'Y'``, ``'Z'``, ``'XY'``, ``'YZ'``, or ``'XZ'``.

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal thermal principal strain "1" for the second result set.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_thermal_component_strain('1')
        """
        disp = self.nodal_thermal_component_strain(component)
        kwargs.setdefault(
            "scalar_bar_args",
            {"title": f"{component} Thermal Nodal\nComponent Strain"},
        )
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_thermal_principal_strain(self, component) -> np.ndarray:
        """Nodal thermal principal thermal strain.

        Equivalent MAPDL commands:

        * ``*VGET,PARM,NODE,,EPTH,1``

        Parameters
        ----------
        component : str, optional
            Component to retrieve.  Must be ``'1'``, ``'2'``, or
            ``'3'``

        Returns
        -------
        numpy.ndarray
            Numpy array containing the nodal thermal principal thermal
            strain for the specified ``component``.

        Notes
        -----
        This command always returns all nodal rotations regardless of
        if the nodes are selected or not.  Use the ``selected_nodes``
        mask to get the currently selected nodes.

        Examples
        --------
        Principal nodal strain in the S1 direction for the first result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> mapdl.post_processing.nodal_thermal_principal_strain('1')
            array([0.60024621, 0.61625265, 0.65081825, ...,
                   0.        , 0.        , 0.        ])

        Corresponding nodes.

        >>> mapdl.mesh.nnum_all
        array([   1,    2,    3, ..., 7215, 7216, 7217], dtype=int32)

        """
        if isinstance(component, int):
            component = str(component)
        component = check_comp(component, PRINCIPAL_TYPE)
        return self.nodal_values("EPTH", component)

    def plot_nodal_thermal_principal_strain(
        self, component, show_node_numbering=False, **kwargs
    ):
        """Plot thermal nodal principal strain.

        Parameters
        ----------
        component : str
            Nodal principal strain component to plot.  Must be
            ``'1'``, ``'2'``, or ``'3'``

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal principal strain "1" for the second result set.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_thermal_principal_strain('1')
        """
        disp = self.nodal_thermal_principal_strain(component)
        kwargs.setdefault(
            "scalar_bar_args",
            {"title": "%s Nodal\nPrincipal Strain" % component},
        )
        return self._plot_point_scalars(
            disp, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_thermal_strain_intensity(self) -> np.ndarray:
        """The thermal nodal strain intensity of the current result.

        Equivalent MAPDL command:

        * ``PRNSOL, EPTH, PRIN``

        Returns
        -------
        numpy.ndarray
            Numpy array containing the thermal nodal strain intensity
            of the current result.

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero value.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero value.

        Examples
        --------
        Thermal strain intensity for result 2

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_thermal_strain_intensity()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("EPTH", "INT")

    def plot_nodal_thermal_strain_intensity(self, show_node_numbering=False, **kwargs):
        """Plot the thermal nodal strain intensity of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes. Defaults to False

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the thermal strain intensity for the second result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_thermal_strain_intensity()

        Plot off_screen and save a screenshot.

        >>> mapdl.post_processing.plot_nodal_thermal_strain_intensity(off_screen=True,
        ...                                                           savefig='seqv_00.png')

        Subselect a single result type and plot those strain results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_thermal_strain_intensity()

        """
        scalars = self.nodal_thermal_strain_intensity()
        kwargs.setdefault(
            "scalar_bar_args", {"title": "Thermal Nodal\nStrain Intensity"}
        )
        return self._plot_point_scalars(
            scalars, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_thermal_eqv_strain(self) -> np.ndarray:
        """The thermal nodal equivalent strain of the current result.

        Equivalent MAPDL command:

        * ``PRNSOL, EPTH, PRIN``

        Returns
        -------
        numpy.ndarray
            Numpy array containing the thermal nodal equivalent strain
            of the current result.

        Notes
        -----
        The nodal results are averaged across all selected elements.
        Not all nodes will contain valid results (e.g. midside nodes),
        and those nodes will report a zero value.

        Elements that are not selected will not contribute to the
        averaged nodal values, and if a node's attached elements are
        all unselected, the element will report a zero value.

        Examples
        --------
        Thermal quivalent strain for the current result.

        >>> mapdl.post_processing.nodal_thermal_eqv_strain()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        Strain from result 2.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_thermal_eqv_strain()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("EPTH", "EQV")

    def plot_nodal_thermal_eqv_strain(self, show_node_numbering=False, **kwargs):
        """Plot the thermal nodal equivalent strain of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the thermal equivalent strain for the second result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_thermal_eqv_strain()

        Plot off_screen and save a screenshot.

        >>> mapdl.post_processing.plot_nodal_thermal_eqv_strain(off_screen=True,
        ...                                                     savefig='seqv_00.png')

        Subselect a single result type and plot those strain results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_thermal_eqv_strain(smooth_shading=True)

        """
        scalars = self.nodal_thermal_eqv_strain()
        kwargs.setdefault(
            "scalar_bar_args", {"title": "Thermal Nodal\n Equivalent Strain"}
        )
        return self._plot_point_scalars(
            scalars, show_node_numbering=show_node_numbering, **kwargs
        )

    def nodal_contact_friction_stress(self) -> np.ndarray:
        """Nodal contact friction stress of the current result.

        Equivalent MAPDL command:

        * ``PRNSOL, CONT, SFRIC``

        Returns
        -------
        numpy.ndarray
            Numpy array containing the thermal nodal equivalent strain
            of the current result.

        Examples
        --------
        Thermal quivalent strain for the current result.

        >>> mapdl.post_processing.nodal_contact_friction_stress()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        Strain from result 2.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.nodal_contact_friction_stress()
        array([15488.84357602, 16434.95432337, 15683.2334295 , ...,
                   0.        ,     0.        ,     0.        ])

        """
        return self.nodal_values("CONT", "SFRIC")

    def plot_nodal_contact_friction_stress(self, show_node_numbering=False, **kwargs):
        """Plot the nodal contact friction stress of the current result.

        Parameters
        ----------
        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        **kwargs : dict, optional
            Keyword arguments passed to :func:`general_plotter
            <ansys.mapdl.core.plotting.general_plotter>`.

        Returns
        -------
        pyvista.plotting.renderer.CameraPosition
            Camera position from plotter.  Can be reused as an input
            parameter to use the same camera position for future
            plots.
            Only returned when ``return_cpos`` is ``True``.

        pyvista.Plotter
            Pyvista Plotter. In this case, the plotter is shown yet, so
            you can still edit it using Pyvista Plotter methods.
            Only when ``return_plotter`` kwarg is ``True``.

        Notes
        -----
        If ``vkt=True`` (default), this function uses
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`
        You can pass key arguments to
        :func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>` using
        ``kwargs`` argument. For example, ``show_axes`` , ``background``, etc.

        Examples
        --------
        Plot the nodal contact friction stress for the second result.

        >>> mapdl.post1()
        >>> mapdl.set(1, 2)
        >>> mapdl.post_processing.plot_nodal_contact_friction_stress()

        Plot off_screen and save a screenshot.

        >>> mapdl.post_processing.plot_nodal_contact_friction_stress(off_screen=True,
        ...                                                          savefig='seqv_00.png')

        Subselect a single result type and plot those strain results.

        >>> mapdl.esel('S', 'TYPE', vmin=1)
        >>> mapdl.post_processing.plot_nodal_contact_friction_stress(smooth_shading=True)

        """
        kwargs.setdefault(
            "scalar_bar_args", {"title": "Nodal Contact\n Friction Stress"}
        )
        return self._plot_point_scalars(
            self.nodal_contact_friction_stress(),
            show_node_numbering=show_node_numbering,
            **kwargs,
        )
