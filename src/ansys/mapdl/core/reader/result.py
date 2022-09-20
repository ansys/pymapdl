"""
Replacing Result in PyMAPDL.
"""


""" Comments

DPF-Post needs quite a few things:
- components support


Check #todos
"""

from functools import wraps
import os
import pathlib
import tempfile
from typing import Iterable
import weakref

# from ansys.dpf import post
from ansys.dpf import core as dpf
from ansys.dpf.core import Model
from ansys.mapdl.reader.rst import Result
import numpy as np

from ansys.mapdl.core import LOG as logger
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
    """
    Result object based on DPF library.


    This class replaces the class Result in PyMAPDL-Reader.

    The

    Parameters
    ----------
    rst_file_path : str
        Path to the RST file.

    mapdl : _MapdlCore
        Mapdl instantiated object.

    """

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
                    f"The RST file '{rst_file_path}' could not be found."
                )

            self._mapdl_weakref = None
            self._mode_rst = True

        elif mapdl is not None:
            from ansys.mapdl.core.mapdl import _MapdlCore  # avoid circular import fail.

            if not isinstance(mapdl, _MapdlCore):  # pragma: no cover
                raise TypeError("Must be initialized using Mapdl instance")
            self._mapdl_weakref = weakref.ref(mapdl)
            self._mode_rst = False

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

        # this will be removed once the reader class has been fully substituted.
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

    @property
    def logger(self):
        """Logger property"""
        return self._log

    @property
    def mode(self):
        if self._mode_rst:
            return "RST"
        elif self._mode_rst:
            return "MAPDL"

    @property
    def mode_rst(self):
        if self._mode_rst:
            return True
        else:
            return False

    @property
    def mode_mapdl(self):
        if not self._mode_rst:
            return True
        else:
            return False

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
        self._cached_dpf_model = Model(self._rst)
        # self._cached_dpf_model = post.load_solution(self._rst)  # loading file

    @property
    def model(self):
        if self._cached_dpf_model is None or self._update_required:
            self._build_dpf_object()
        return self._cached_dpf_model

    def _get_nodes_for_argument(self, nodes):
        """Get nodes from 'nodes' which can be int, floats, or list/tuple of int/floats, or
        components( strs, or iterable[strings]"""
        if isinstance(nodes, (int, float)):
            return nodes
        elif isinstance(nodes, str):
            # it is component name
            nodes = [nodes]
        elif isinstance(nodes, Iterable):
            if all([isinstance(each, (int, float)) for each in nodes]):
                return nodes
            elif all([isinstance(each, str) for each in nodes]):
                pass
        else:
            raise TypeError(
                "Only ints, floats, strings or iterable of the previous ones are allowed."
            )

        # For components selections:
        nodes_ = []
        available_ns = self.model.mesh.available_named_selections
        for each_named_selection in nodes:
            if each_named_selection not in available_ns:
                raise ValueError(
                    f"The named selection '{each_named_selection}' does not exist."
                )

            scoping = self.model.mesh.named_selection(each_named_selection)
            if scoping.location != "Nodal":
                raise ValueError(
                    f"The named selection '{each_named_selection}' does not contain nodes."
                )

            nodes_.append(scoping.ids)

        return nodes

    def _get_nodes_result(self, rnum, result_type, nodes=None):
        return self._get_result(rnum, result_type, scope_type="Nodal", scope_ids=nodes)

    def _get_elem_result(self, rnum, result_type, elements=None):
        return self._get_result(
            rnum, result_type, scope_type="Elemental", scope_ids=elements
        )

    @update_result
    def _get_result(self, rnum, result_type, scope_type="Nodal", scope_ids=None):
        # todo: accepts components in nodes.
        mesh = self.model.metadata.meshed_region

        field_op = getattr(self.model.results, result_type)()

        # Setting time steps
        if not rnum:
            rnum = 1

        field_op.inputs.time_scoping.connect(rnum)

        # Setting mesh scope
        my_scoping = dpf.Scoping()
        my_scoping.location = scope_type
        if scope_ids:
            my_scoping.ids = scope_ids
        else:
            if scope_type.lower() == "elemental":
                entities = mesh.elements
            else:
                entities = mesh.nodes

            my_scoping.ids = entities.scoping.ids

        field_op.inputs.mesh_scoping.connect(my_scoping)

        # Retrieving output
        container = field_op.outputs.fields_container()[0]
        container_data = container.data

        # Getting ids
        if scope_type.lower() in "elemental":
            ids_, mask_ = mesh.elements.map_scoping(container.scoping)
        else:
            ids_, mask_ = mesh.nodes.map_scoping(container.scoping)

        # Sorting results
        id_order = np.argsort(ids_[mask_]).astype(int)

        return ids_[id_order], container_data[id_order]

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

        return self._get_nodes_result(rnum, "displacement", nodes)

    @wraps(nodal_displacement)
    def nodal_solution(self, *args, **kwargs):
        return self.nodal_displacement(*args, **kwargs)

    def element_stress(
        self, rnum, principal=None, in_element_coord_sys=None, elements=None, **kwargs
    ):
        """Retrieves the element component stresses.

        Equivalent ANSYS command: PRESOL, S

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        principal : bool, optional
            Returns principal stresses instead of component stresses.
            Default False.

        in_element_coord_sys : bool, optional
            Returns the results in the element coordinate system.
            Default False and will return the results in the global
            coordinate system.

        elements : str, sequence of int or str, optional
            Select a limited subset of elements.  Can be a element
            component or array of element numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        **kwargs : optional keyword arguments
            Hidden options for distributed result files.

        Returns
        -------
        enum : np.ndarray
            ANSYS element numbers corresponding to each element.

        element_stress : list
            Stresses at each element for each node for Sx Sy Sz Sxy
            Syz Sxz or SIGMA1, SIGMA2, SIGMA3, SINT, SEQV when
            principal is True.

        enode : list
            Node numbers corresponding to each element's stress
            results.  One list entry for each element.

        Examples
        --------
        Element component stress for the first result set.

        >>> rst.element_stress(0)

        Element principal stress for the first result set.

        >>> enum, element_stress, enode = result.element_stress(0, principal=True)

        Notes
        -----
        Shell stresses for element 181 are returned for top and bottom
        layers.  Results are ordered such that the top layer and then
        the bottom layer is reported.
        """
        # return super().element_stress(rnum, principal, in_element_coord_sys, **kwargs)
        if principal is not None:
            raise NotImplementedError()
        if in_element_coord_sys is not None:
            raise NotImplementedError

        return self._get_elem_result(rnum, "stress", elements=elements)

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
        return self._get_nodes_result(rnum, "elastic_strain", nodes)

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
        return self._get_nodes_result(rnum, "plastic_strain", nodes)

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

        return self._get_nodes_result(rnum, "misc.nodal_acceleration", nodes)

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
        return self._get_nodes_result(rnum, "misc.nodal_reaction_force", nodes)

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
        return self._get_nodes_result(rnum, "stress", nodes)

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
        return self._get_nodes_result(rnum, "temperature", nodes)

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
        return self._get_nodes_result(rnum, "misc.nodal_thermal_strains", nodes)

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
        return self._get_nodes_result(rnum, "misc.nodal_velocity", nodes)

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
        return self._get_nodes_result(rnum, "misc.nodal_force", nodes)

    def principal_nodal_stress(self, rnum, nodes=None):
        """Computes the principal component stresses for each node in
        the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        nodenum : numpy.ndarray
            Node numbers of the result.

        pstress : numpy.ndarray
            Principal stresses, stress intensity, and equivalent stress.
            [sigma1, sigma2, sigma3, sint, seqv]

        Examples
        --------
        Load the principal nodal stress for the first solution.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> nnum, stress = rst.principal_nodal_stress(0)

        Notes
        -----
        ANSYS equivalent of:
        PRNSOL, S, PRIN

        which returns:
        S1, S2, S3 principal stresses, SINT stress intensity, and SEQV
        equivalent stress.

        Internal averaging algorithm averages the component values
        from the elements at a common node and then calculates the
        principal using the averaged value.

        See the MAPDL ``AVPRIN`` command for more details.
        ``ansys-mapdl-reader`` uses the default ``AVPRIN, 0`` option.

        """
        res = []
        for each in ["principal_1", "principal_2", "principal_3"]:
            res.append(self._get_nodes_result(rnum, f"stress.{each}", nodes)[1])
        return nodes, np.hstack(res)

    @property
    def n_results(self):
        """Number of results"""
        return self.model.get_result_info().n_results

    @property
    def filename(self) -> str:
        """String form of the filename. This property is read-only."""
        return self._rst  # in the reader, this contains the complete path.

    @property
    def pathlib_filename(self) -> pathlib.Path:
        """Return the ``pathlib.Path`` version of the filename. This property can not be set."""
        return pathlib.Path(self._rst)

    @property
    def mesh(self):
        """Mesh from result file."""
        return (
            self.model.mesh
        )  # todo: this should be a class equivalent to reader.mesh class.

    @property
    def grid(self):
        return self.model.mesh.grid

    def nsets(self):
        return self.model.time_freq_support.n_sets

    def parse_step_substep(self, user_input):
        """Converts (step, substep) to a cumulative index"""

        if isinstance(user_input, int):
            return self.model.time_freq_support.get_cumulative_index(
                user_input
            )  # todo: should it be 1 or 0 based indexing?

        elif isinstance(user_input, (list, tuple)):
            return self.model.time_freq_support.get_cumulative_index(
                user_input[0], user_input[1]
            )

        else:
            raise TypeError("Input must be either an int or a list")

    @property
    def version(self):
        """The version of MAPDL used to generate this result file.

        Examples
        --------
        >>> mapdl.result.version
        20.1
        """
        return float(self.model.get_result_info().solver_version)

    @property
    def available_results(self):
        text = "Available Results:\n"
        for each_available_result in self.model.get_result_info().available_results:
            text += (
                each_available_result.native_location
                + " "
                + each_available_result.name
                + "\n"
            )

    @property
    def n_sector(self):
        """Number of sectors"""
        return self.model.get_result_info().has_cyclic

    @property
    def title(self):
        """Title of model in database"""
        return self.model.get_result_info().main_title

    @property
    def is_cyclic(self):  # Todo: DPF should implement this.
        return self.n_sector > 1

    @property
    def units(self):
        return self.model.get_result_info().unit_system_name

    def __repr__(self):
        if False or self.is_distributed:
            rst_info = ["PyMAPDL Reader Distributed Result"]
        else:
            rst_info = ["PyMAPDL Result"]

        rst_info.append("{:<12s}: {:s}".format("title".capitalize(), self.title))
        rst_info.append("{:<12s}: {:s}".format("subtitle".capitalize(), self.subtitle))
        rst_info.append("{:<12s}: {:s}".format("units".capitalize(), self.units))

        rst_info.append("{:<12s}: {:s}".format("Version", self.version))
        rst_info.append("{:<12s}: {:s}".format("Cyclic", self.is_cyclic))
        rst_info.append("{:<12s}: {:d}".format("Result Sets", self.nsets))

        rst_info.append("{:<12s}: {:d}".format("Nodes", self.model.mesh.nodes.n_nodes))
        rst_info.append(
            "{:<12s}: {:d}".format("Elements", self.model.mesh.elements.n_elements)
        )

        rst_info.append("\n")
        rst_info.append(self.available_results)
        return "\n".join(rst_info)

    def nodal_time_history(self, solution_type="NSL", in_nodal_coord_sys=None):
        """The DOF solution for each node for all result sets.

        The nodal results are returned returned in the global
        cartesian coordinate system or nodal coordinate system.

        Parameters
        ----------
        solution_type: str, optional
            The solution type.  Must be either nodal displacements
            (``'NSL'``), nodal velocities (``'VEL'``) or nodal
            accelerations (``'ACC'``).

        in_nodal_coord_sys : bool, optional
            When ``True``, returns results in the nodal coordinate system.
            Default ``False``.

        Returns
        -------
        nnum : int np.ndarray
            Node numbers associated with the results.

        result : float np.ndarray
            Nodal solution for all result sets.  Array is sized
            ``rst.nsets x nnod x Sumdof``, which is the number of
            time steps by number of nodes by degrees of freedom.
        """
        if not isinstance(solution_type, str):
            raise TypeError("Solution type must be a string")

        if solution_type == "NSL":
            func = self.nodal_solution
        elif solution_type == "VEL":
            func = self.nodal_velocity
        elif solution_type == "ACC":
            func = self.nodal_acceleration
        else:
            raise ValueError(
                "Argument 'solution type' must be either 'NSL', " "'VEL', or 'ACC'"
            )

        # size based on the first result
        nnum, sol = func(0, in_nodal_coord_sys)
        data = np.empty((self.nsets, sol.shape[0], sol.shape[1]), np.float64)
        for i in range(self.nsets):
            data[i] = func(i)[1]

        return nnum, data

    def element_components(self):
        """Dictionary of ansys element components from the result file.

        Examples
        --------
        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> from ansys.mapdl.reader import examples
        >>> rst = pymapdl_reader.read_binary(examples.rstfile)
        >>> rst.element_components
        {'ECOMP1': array([17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40], dtype=int32),
        'ECOMP2': array([ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                14, 15, 16, 17, 18, 19, 20, 23, 24], dtype=int32),
        'ELEM_COMP': array([ 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                16, 17, 18, 19, 20], dtype=int32)}
        """
        element_components_ = {}
        for each_named_selection in self.model.mesh.available_named_selections:
            scoping = self.model.mesh.named_selection(each_named_selection)
            element_components_[each_named_selection] = scoping.ids

        return element_components_

    @property
    def time_values(self):
        "Values for the time/frequency"
        return self.model.time_freq_support.time_frequencies.data_as_list

    def save_as_vtk(
        self, filename, rsets=None, result_types=["ENS"], progress_bar=True
    ):
        """Writes results to a vtk readable file.

        Nodal results will always be written.

        The file extension will select the type of writer to use.
        ``'.vtk'`` will use the legacy writer, while ``'.vtu'`` will
        select the VTK XML writer.

        Parameters
        ----------
        filename : str, pathlib.Path
            Filename of grid to be written.  The file extension will
            select the type of writer to use.  ``'.vtk'`` will use the
            legacy writer, while ``'.vtu'`` will select the VTK XML
            writer.

        rsets : collections.Iterable
            List of result sets to write.  For example ``range(3)`` or
            [0].

        result_types : list
            Result type to write.  For example ``['ENF', 'ENS']``
            List of some or all of the following:

            - EMS: misc. data
            - ENF: nodal forces
            - ENS: nodal stresses
            - ENG: volume and energies
            - EGR: nodal gradients
            - EEL: elastic strains
            - EPL: plastic strains
            - ECR: creep strains
            - ETH: thermal strains
            - EUL: euler angles
            - EFX: nodal fluxes
            - ELF: local forces
            - EMN: misc. non-sum values
            - ECD: element current densities
            - ENL: nodal nonlinear data
            - EHC: calculated heat generations
            - EPT: element temperatures
            - ESF: element surface stresses
            - EDI: diffusion strains
            - ETB: ETABLE items
            - ECT: contact data
            - EXY: integration point locations
            - EBA: back stresses
            - ESV: state variables
            - MNL: material nonlinear record

        progress_bar : bool, optional
            Display a progress bar using ``tqdm``.

        Notes
        -----
        Binary files write much faster than ASCII, but binary files
        written on one system may not be readable on other systems.
        Binary can only be selected for the legacy writer.

        Examples
        --------
        Write nodal results as a binary vtk file.

        >>> rst.save_as_vtk('results.vtk')

        Write using the xml writer

        >>> rst.save_as_vtk('results.vtu')

        Write only nodal and elastic strain for the first result

        >>> rst.save_as_vtk('results.vtk', [0], ['EEL', 'EPL'])

        Write only nodal results (i.e. displacements) for the first result.

        >>> rst.save_as_vtk('results.vtk', [0], [])

        """
        # This should probably be included a part of the ansys.dpf.post.result_data.ResultData class
        raise NotImplementedError("To be implemented by DPF")

    @property
    def subtitle(self):
        raise NotImplementedError("To be implemented by DPF")

    @property
    def _is_distributed(self):
        raise NotImplementedError("To be implemented by DPF")

    @property
    def is_distributed(self):
        """True when this result file is part of a distributed result

        Only True when Global number of nodes does not equal the
        number of nodes in this file.

        Notes
        -----
        Not a reliabile indicator if a cyclic result.
        """
        return self._is_distributed

    def cs_4x4(self, cs_cord, as_vtk_matrix=False):
        """return a 4x4 transformation array for a given coordinate system"""
        raise NotImplementedError("To be implemented by DPF.")

    def cylindrical_nodal_stress(self):
        """Retrieves the stresses for each node in the solution in the
        cylindrical coordinate system as the following values:

        ``R``, ``THETA``, ``Z``, ``RTHETA``, ``THETAZ``, and ``RZ``

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
            Stresses at ``R, THETA, Z, RTHETA, THETAZ, RZ`` averaged
            at each corner node where ``R`` is radial.

        Examples
        --------
        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> nnum, stress = rst.cylindrical_nodal_stress(0)

        Return the cylindrical nodal stress just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, stress = rst.cylindrical_nodal_stress(0, nodes='MY_COMPONENT')

        Return the nodal stress just for the nodes from 20 through 50.

        >>> nnum, stress = rst.cylindrical_nodal_stress(0, nodes=range(20, 51))

        Notes
        -----
        Nodes without a stress value will be NAN.
        Equivalent ANSYS commands:
        RSYS, 1
        PRNSOL, S
        """
        raise NotImplementedError("This should be implemented by DPF")

    def element_lookup(self, element_id):
        """Index of the element within the result mesh"""
        # We need to get the mapping between the mesh.grid and the results.elements.
        # Probably DPF already has that mapping.
        raise NotImplementedError("This should be implemented by DPF")

    # def element_solution_data(self):
    #     pass

    # def element_stress(self):
    #     pass

    # def materials(self):
    #     pass

    # def quadgrid(self):
    #     pass

    # def read_record(self):
    #     pass

    # def result_dof(self):
    #     pass

    # def section_data(self):
    #     pass

    # def solution_info(self):
    #     pass

    # def text_result_table(self):
    #     pass

    # def write_table(self):
    #     pass

    # def nodal_boundary_conditions(self):
    #     pass

    # def nodal_input_force(self):
    #     pass

    # def nodal_static_forces(self):
    #     pass

    # def node_components(self):
    #     pass

    # def parse_coordinate_system(self):
    #     pass


#### overwriting
# def overwrite_element_solution_record(self):
#     pass

# def overwrite_element_solution_records(self):
#     pass

### plotting

# def animate_nodal_displacement(self):
#     pass

# def animate_nodal_solution(self):
#     pass

# def animate_nodal_solution_set(self):
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
