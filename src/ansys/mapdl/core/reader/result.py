"""
Replacing Result in PyMAPDL.
"""

from functools import wraps
import os
import tempfile
import weakref

from ansys.dpf import post

# from ansys.dpf.core import Model
from ansys.mapdl.reader.rst import Result

from ansys.mapdl.core import LOG as logger
from ansys.mapdl.core.mapdl import _MapdlCore
from ansys.mapdl.core.misc import random_string


def update_result(function):
    """
    Decorator to wrap :class:`DPFResult <ansys.mapdl.core.reader.result.DPFResult>`
    methods to force update the RST when accessed the first time.

    Parameters
    ----------
    update : bool, optional
        If ``True``, the class information is updated by calling ``/STATUS``
        before accessing the methods. By default ``False``
    """

    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if self._update_required or not self._loaded or self._cached_dpf_model is None:
            self._update()
            self._log.debug("RST file updated.")
        return function(self, *args, **kwargs)

    return wrapper


class DPFResult(Result):
    """Main class"""

    def __init__(self, rst_file_path=None, mapdl=None):
        """Initialize Result instance"""

        self.__rst_directory = None
        self.__rst_name = None

        if rst_file_path is not None:
            if os.path.exists(rst_file_path):
                self.__rst_directory = os.path.dirname(rst_file_path)
                self.__rst_name = os.path.basename(rst_file_path)
            else:
                raise FileNotFoundError(
                    f"The RST file {rst_file_path} could not be found."
                )

            self._mapdl_weakref = None

        elif mapdl is not None:
            if not isinstance(mapdl, _MapdlCore):  # pragma: no cover
                raise TypeError("Must be initialized using Mapdl instance")
            self._mapdl_weakref = weakref.ref(mapdl)

        else:
            raise ValueError(
                "One of the following kwargs must be supplied: 'rst_file_path' or 'mapdl'"
            )

        # dpf
        self._loaded = False
        self._update_required = False  # if true, it triggers a update on the RST file
        self._cached_dpf_model = None

        # old attributes
        ELEMENT_INDEX_TABLE_KEY = None  # todo: To fix
        ELEMENT_RESULT_NCOMP = None  # todo: to fix

        super().__init__(self._rst, read_mesh=False)

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of MAPDL"""
        if self._mapdl_weakref:
            return self._mapdl_weakref()

    @property
    def _log(self):
        """alias for mapdl log"""
        if self._mapdl:
            return self._mapdl._log
        else:
            return logger

    def _set_log_level(self, level):
        """alias for mapdl._set_log_level"""
        if self._mapdl:
            return self._mapdl._set_log_level(level)

    @property
    def _rst(self):
        return os.path.join(self._rst_directory, self._rst_name)

    @property
    def local(self):
        if self._mapdl:
            return self._mapdl._local

    @property
    def _rst_directory(self):
        if self.__rst_directory is None:
            if self.local:
                _rst_directory = self._mapdl.directory
            else:
                _rst_directory = os.path.join(tempfile.gettempdir(), random_string())
                if not os.path.exists(_rst_directory):
                    os.mkdir(_rst_directory)

            self.__rst_directory = _rst_directory

        return self.__rst_directory

    @property
    def _rst_name(self):
        if self.__rst_name is None:
            if self.local:
                self.__rst_name = self._mapdl.jobname
            else:
                self.__rst_name = f"model_{random_string()}.rst"
        return self.__rst_name

    def _update(self, progress_bar=None, chunk_size=None):
        if self._mapdl:
            self._update_rst(progress_bar=progress_bar, chunk_size=chunk_size)

        # Updating model
        self._build_dpf_object()

        # Resetting flag
        self._loaded = True
        self._update_required = False

    def _update_rst(self, progress_bar=None, chunk_size=None):
        # Saving model
        self._mapdl.save(self._rst_name[:-4], "rst", "model")

        if self.local and not self.local:
            self._log.debug("Updating the local copy of remote RST file.")
            # download file
            self._mapdl.download(
                self._rst_name,
                self._rst_directory,
                progress_bar=progress_bar,
                chunk_size=chunk_size,
            )
        # self._update_required = not self._update_required # demonstration

    def _build_dpf_object(self):
        if self._log:
            self._log.debug("Building DPF Model object.")
        # self._cached_dpf_model = Model(self._rst)
        self._cached_dpf_model = post.load_solution(self._rst)

    @property
    def model(self):
        if self._cached_dpf_model is None or self._update_required:
            self._build_dpf_object()
        return self._cached_dpf_model

    @update_result
    def _get_node_result(self, rnum, result_type, data_type_, nodes=None):
        if isinstance(rnum, list):
            set_ = rnum[0]  # todo: implement subresults
        elif isinstance(rnum, (int, float)):
            set_ = rnum
        else:
            raise ValueError(
                f"Please use 'int', 'float' or  'list' for the parameter 'rnum'."
            )

        result_types = result_type.split(".")
        model = self.model

        if len(result_types) > 1:
            model = getattr(model, result_types[0])
            result_type = result_types[1]

        # todo: make nodes accepts components

        field = getattr(model, result_type)(set=set_, node_scoping=nodes)
        field_dir = getattr(
            field, data_type_
        )  # this can give an error if the results are not in the RST.
        # Use a try and except and give more clear info?
        return field_dir.get_data_at_field(0)  # it needs to return also the nodes id.

    def nodal_displacement(self, rnum, in_nodal_coord_sys=None, nodes=None):
        """Returns the DOF solution for each node in the global
        cartesian coordinate system or nodal coordinate system.

        Solution may be nodal temperatures or nodal displacements
        depending on the type of the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys : bool, optional
            When ``True``, returns results in the nodal coordinate
            system.  Default ``False``.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Array of nodal displacements or nodal temperatures.  Array
            is (``nnod`` x ``sumdof``), the number of nodes by the
            number of degrees of freedom which includes ``numdof`` and
            ``nfldof``

        Examples
        --------
        Return the nodal soltuion (in this case, displacement) for the
        first result of ``"file.rst"``

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> nnum, data = rst.nodal_solution(0)

        Return the nodal solution just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, data = rst.nodal_solution(0, nodes='MY_COMPONENT')

        Return the nodal solution just for the nodes from 20 through 50.

        >>> nnum, data = rst.nodal_solution(0, nodes=range(20, 51))

        Notes
        -----
        Some solution results may not include results for each node.
        These results are removed by and the node numbers of the
        solution results are reflected in ``nnum``.
        """
        if in_nodal_coord_sys is not None:
            raise DeprecationWarning(
                "The parameter 'in_nodal_coord_sys' is being deprecated."
            )

        return self._get_node_result(rnum, "displacement", "vector", nodes)

    def nodal_elastic_strain(self, rnum, nodes=None):
        """Nodal component elastic strains.  This record contains
        strains in the order ``X, Y, Z, XY, YZ, XZ, EQV``.

        Elastic strains can be can be nodal values extrapolated from
        the integration points or values at the integration points
        moved to the nodes.

        Equivalent MAPDL command: ``PRNSOL, EPEL``

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : np.ndarray
            MAPDL node numbers.

        elastic_strain : np.ndarray
            Nodal component elastic strains.  Array is in the order
            ``X, Y, Z, XY, YZ, XZ, EQV``.

        Examples
        --------
        Load the nodal elastic strain for the first result.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> nnum, elastic_strain = rst.nodal_elastic_strain(0)

        Return the nodal elastic strain just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, elastic_strain = rst.nodal_elastic_strain(0, nodes='MY_COMPONENT')

        Return the nodal elastic strain just for the nodes from 20 through 50.

        >>> nnum, elastic_strain = rst.nodal_elastic_strain(0, nodes=range(20, 51))

        Notes
        -----
        Nodes without a strain will be NAN.
        """
        return self._get_node_result(rnum, "elastic_strain", "tensor", nodes)

    def nodal_plastic_strain(self, rnum, nodes=None):
        """Nodal component plastic strains.

        This record contains strains in the order:
        ``X, Y, Z, XY, YZ, XZ, EQV``.

        Plastic strains are always values at the integration points
        moved to the nodes.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : np.ndarray
            MAPDL node numbers.

        plastic_strain : np.ndarray
            Nodal component plastic strains.  Array is in the order
            ``X, Y, Z, XY, YZ, XZ, EQV``.

        Examples
        --------
        Load the nodal plastic strain for the first solution.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> nnum, plastic_strain = rst.nodal_plastic_strain(0)

        Return the nodal plastic strain just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, plastic_strain = rst.nodal_plastic_strain(0, nodes='MY_COMPONENT')

        Return the nodal plastic strain just for the nodes from 20
        through 50.

        >>> nnum, plastic_strain = rst.nodal_plastic_strain(0, nodes=range(20, 51))

        """
        return self._get_node_result(rnum, "plastic_strain", "tensor", nodes)

    def nodal_acceleration(self, rnum, nodes=None, in_nodal_coord_sys=None):
        """Nodal velocities for a given result set.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys : bool, optional
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Array of nodal accelerations.  Array is (``nnod`` x
            ``sumdof``), the number of nodes by the number of degrees
            of freedom which includes ``numdof`` and ``nfldof``

        Examples
        --------
        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> nnum, data = rst.nodal_acceleration(0)

        Notes
        -----
        Some solution results may not include results for each node.
        These results are removed by and the node numbers of the
        solution results are reflected in ``nnum``.
        """
        if in_nodal_coord_sys is not None:
            raise DeprecationWarning(
                "The 'in_nodal_coord_sys' kwarg has been deprecated."
            )

        return self._get_node_result(rnum, "misc.nodal_acceleration", "vector", nodes)

    def nodal_reaction_forces(self, rnum, nodes=None):
        """Nodal reaction forces.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        rforces : np.ndarray
            Nodal reaction forces for each degree of freedom.

        nnum : np.ndarray
            Node numbers corresponding to the reaction forces.  Node
            numbers may be repeated if there is more than one degree
            of freedom for each node.

        dof : np.ndarray
            Degree of freedom corresponding to each node using the
            MAPDL degree of freedom reference table.  See
            ``rst.result_dof`` for the corresponding degrees of
            freedom for a given solution.

        Examples
        --------
        Get the nodal reaction forces for the first result and print
        the reaction forces of a single node.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> rforces, nnum, dof = rst.nodal_reaction_forces(0)
        >>> dof_ref = rst.result_dof(0)
        >>> rforces[:3], nnum[:3], dof[:3], dof_ref
        (array([  24102.21376091, -109357.01854005,   22899.5303263 ]),
         array([4142, 4142, 4142]),
         array([1, 2, 3], dtype=int32),
         ['UX', 'UY', 'UZ'])

        """
        return self._get_node_result(rnum, "misc.nodal_reaction_force", "vector", nodes)

    def nodal_stress(self, rnum, nodes=None):
        """Retrieves the component stresses for each node in the
        solution.

        The order of the results corresponds to the sorted node
        numbering.

        Computes the nodal stress by averaging the stress for each
        element at each node.  Due to the discontinuities across
        elements, stresses will vary based on the element they are
        evaluated from.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : numpy.ndarray
            Node numbers of the result.

        stress : numpy.ndarray
            Stresses at ``X, Y, Z, XY, YZ, XZ`` averaged at each corner
            node.

        Examples
        --------
        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> nnum, stress = rst.nodal_stress(0)

        Return the nodal stress just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, stress = rst.nodal_stress(0, nodes='MY_COMPONENT')

        Return the nodal stress just for the nodes from 20 through 50.

        >>> nnum, stress = rst.nodal_solution(0, nodes=range(20, 51))

        Notes
        -----
        Nodes without a stress value will be NAN.
        Equivalent ANSYS command: PRNSOL, S
        """
        return self._get_node_result(rnum, "stress", "vector", nodes)

    def nodal_temperature(self, rnum, nodes=None):
        """Retrieves the temperature for each node in the
        solution.

        The order of the results corresponds to the sorted node
        numbering.

        Equivalent MAPDL command: PRNSOL, TEMP

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : numpy.ndarray
            Node numbers of the result.

        temperature : numpy.ndarray
            Temperature at each node.

        Examples
        --------
        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> nnum, temp = rst.nodal_temperature(0)

        Return the temperature just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, temp = rst.nodal_stress(0, nodes='MY_COMPONENT')

        Return the temperature just for the nodes from 20 through 50.

        >>> nnum, temp = rst.nodal_solution(0, nodes=range(20, 51))

        """
        return self._get_node_result(rnum, "temperature", "scalar", nodes)

    def nodal_thermal_strain(self, rnum, nodes=None):
        """Nodal component thermal strain.

        This record contains strains in the order X, Y, Z, XY, YZ, XZ,
        EQV, and eswell (element swelling strain).  Thermal strains
        are always values at the integration points moved to the
        nodes.

        Equivalent MAPDL command: PRNSOL, EPTH, COMP

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : np.ndarray
            MAPDL node numbers.

        thermal_strain : np.ndarray
            Nodal component plastic strains.  Array is in the order
            ``X, Y, Z, XY, YZ, XZ, EQV, ESWELL``

        Examples
        --------
        Load the nodal thermal strain for the first solution.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> nnum, thermal_strain = rst.nodal_thermal_strain(0)

        Return the nodal thermal strain just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, thermal_strain = rst.nodal_thermal_strain(0, nodes='MY_COMPONENT')

        Return the nodal thermal strain just for the nodes from 20 through 50.

        >>> nnum, thermal_strain = rst.nodal_thermal_strain(0, nodes=range(20, 51))
        """
        return self._get_node_result(
            rnum, "misc.nodal_thermal_strains", "vector", nodes
        )

    def nodal_velocity(self, rnum, in_nodal_coord_sys=None, nodes=None):
        """Nodal velocities for a given result set.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys : bool, optional
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Array of nodal velocities.  Array is (``nnod`` x
            ``sumdof``), the number of nodes by the number of degrees
            of freedom which includes ``numdof`` and ``nfldof``

        Examples
        --------
        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> nnum, data = rst.nodal_velocity(0)

        Notes
        -----
        Some solution results may not include results for each node.
        These results are removed by and the node numbers of the
        solution results are reflected in ``nnum``.
        """
        if in_nodal_coord_sys is not None:
            raise DeprecationWarning(
                "The parameter 'in_nodal_coord_sys' is being deprecated."
            )
        return self._get_node_result(rnum, "misc.nodal_velocity", "vector", nodes)

    def nodal_static_forces(self, rnum, nodes=None):
        """Return the nodal forces averaged at the nodes.

        Nodal forces are computed on an element by element basis, and
        this method averages the nodal forces for each element for
        each node.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        nodes : str, sequence of int or str, optional
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        nnum : np.ndarray
            MAPDL node numbers.

        forces : np.ndarray
           Averaged nodal forces.  Array is sized ``[nnod x numdof]``
           where ``nnod`` is the number of nodes and ``numdof`` is the
           number of degrees of freedom for this solution.

        Examples
        --------
        Load the nodal static forces for the first result using the
        example hexahedral result file.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> from ansys.mapdl.reader import examples
        >>> rst = pymapdl_reader.read_binary(examples.rstfile)
        >>> nnum, forces = rst.nodal_static_forces(0)

        Return the nodal static forces just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, forces = rst.nodal_static_forces(0, nodes='MY_COMPONENT')

        Return the nodal static forces just for the nodes from 20 through 50.

        >>> nnum, forces = rst.nodal_static_forces(0, nodes=range(20, 51))

        Notes
        -----
        Nodes without a a nodal will be NAN.  These are generally
        midside (quadratic) nodes.
        """
        return self._get_node_result(rnum, "misc.nodal_force", "vector", nodes)

    # def animate_nodal_displacement(self):
    #     pass

    # def animate_nodal_solution(self):
    #     pass

    # def animate_nodal_solution_set(self):
    #     pass

    # def available_results(self):
    #     pass

    # def cs_4x4(self):
    #     pass

    # def cylindrical_nodal_stress(self):
    #     pass

    # def element_components(self):
    #     pass

    # def element_lookup(self):
    #     pass

    # def element_solution_data(self):
    #     pass

    # def element_stress(self):
    #     pass

    # def filename(self):
    #     pass

    # def grid(self):
    #     pass

    # def materials(self):
    #     pass

    # def mesh(self):
    #     pass

    # def n_results(self):
    #     pass

    # def n_sector(self):
    #     pass

    # def nodal_boundary_conditions(self):
    #     pass

    # def nodal_input_force(self):
    #     pass

    # def nodal_solution(self):
    #     pass

    # def nodal_static_forces(self):
    #     pass

    # def nodal_time_history(self):
    #     pass

    # def node_components(self):
    #     pass

    # def nsets(self):
    #     pass

    # def overwrite_element_solution_record(self):
    #     pass

    # def overwrite_element_solution_records(self):
    #     pass

    # def parse_coordinate_system(self):
    #     pass

    # def parse_step_substep(self):
    #     pass

    # def pathlib_filename(self):
    #     pass

    # def plot(self):
    #     pass

    # def plot_cylindrical_nodal_stress(self):
    #     pass

    # def plot_element_result(self):
    #     pass

    # def plot_nodal_displacement(self,
    #     rnum,
    #     comp=None,
    #     show_displacement=False,
    #     displacement_factor=1.0,
    #     node_components=None,
    #     element_components=None,
    #     **kwargs):
    #     pass

    #     if kwargs.pop("sel_type_all", None):
    #         warn(f"The kwarg 'sel_type_all' is being deprecated.")

    #     if kwargs.pop("treat_nan_as_zero", None):
    #         warn(f"The kwarg 'treat_nan_as_zero' is being deprecated.")

    #     if isinstance(rnum, list):
    #         set_ = rnum[0]  # todo: implement subresults
    #     elif isinstance(rnum, (int, float)):
    #         set_ = rnum
    #     else:
    #         raise ValueError(f"Please use 'int', 'float' or  'list' for the parameter 'rnum'.")

    #     disp = self.model.displacement(set=set_)
    #     if not comp:
    #         comp = 'norm'
    #     disp_dir = getattr(disp, comp)
    #     disp_dir.plot_contour(**kwargs)

    # def plot_nodal_elastic_strain(self):
    #     pass

    # def plot_nodal_plastic_strain(self):
    #     pass

    # def plot_nodal_solution(self):
    #     pass

    # def plot_nodal_stress(self):
    #     pass

    # def plot_nodal_temperature(self):
    #     pass

    # def plot_nodal_thermal_strain(self):
    #     pass

    # def plot_principal_nodal_stress(self):
    #     pass

    # def principal_nodal_stress(self):
    #     pass

    # def quadgrid(self):
    #     pass

    # def read_record(self):
    #     pass

    # def result_dof(self):
    #     pass

    # def save_as_vtk(self):
    #     pass

    # def section_data(self):
    #     pass

    # def solution_info(self):
    #     pass

    # def text_result_table(self):
    #     pass

    # def time_values(self):
    #     pass

    # def version(self):
    #     pass

    # def write_table(self):
    #     pass
