# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Classes and functions for returning/manipulating result data
"""
from pathlib import Path

import numpy as np

from ansys.mapdl.core.reader.constants import NOT_AVAILABLE_METHOD
from ansys.mapdl.core.reader.core import DPFResultCore, ResultNotFound
from ansys.mapdl.core.reader.types import (
    Elements,
    Kwargs,
    Nodes,
    ReturnData,
    Rnum,
    SolutionType,
)


class DPFResultData(DPFResultCore):
    """Provides methods for accessing and manipulating DPF result data."""

    def nodal_input_force(self, rnum: Rnum):
        """Nodal input force for a given result number.

        Nodal input force is generally set with the APDL command
        ``F``.  For example, ``F, 25, FX, 0.001``

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        nnum : np.ndarray
            Node numbers of the nodes with nodal forces.

        dof : np.ndarray
            Array of indices of the degrees of freedom of the nodes
            with input force.  See ``rst.result_dof`` for the degrees
            of freedom associated with each index.

        force : np.ndarray
            Nodal input force.

        Examples
        --------
        Print the nodal input force where:
        - Node 25 has FX=20
        - Node 26 has FY=30
        - Node 27 has FZ=40

        >>> rst.nodal_input_force(0)
        (array([ 25,  26, 27], dtype=int32),
         array([2, 1, 3], dtype=int32),
         array([30., 20., 40.]))
        """
        # To be done later
        raise NotImplementedError(
            NOT_AVAILABLE_METHOD.format(method="nodal_input_force")
        )

    def element_solution_data(
        self, rnum: Rnum, datatype: str, sort: bool = True, **kwargs: Kwargs
    ):
        """Retrieves element solution data.  Similar to ETABLE.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        datatype : str
            Element data type to retrieve.

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

        sort : bool
            Sort results by element number.  Default ``True``.

        **kwargs : optional keyword arguments
            Hidden options for distributed result files.

        Returns
        -------
        enum : np.ndarray
            Element numbers.

        element_data : list
            List with one data item for each element.

        enode : list
            Node numbers corresponding to each element.
            results.  One list entry for each element.

        Notes
        -----
        See ANSYS element documentation for available items for each
        element type.  See:

        https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_elem/

        Examples
        --------
        Retrieve "LS" solution results from an PIPE59 element for result set 1

        >>> enum, edata, enode = result.element_solution_data(0, datatype='ENS')
        >>> enum[0]  # first element number
        >>> enode[0]  # nodes belonging to element 1
        >>> edata[0]  # data belonging to element 1
        array([ -4266.19   ,   -376.18857,  -8161.785  , -64706.766  ,
                -4266.19   ,   -376.18857,  -8161.785  , -45754.594  ,
                -4266.19   ,   -376.18857,  -8161.785  ,      0.     ,
                -4266.19   ,   -376.18857,  -8161.785  ,  45754.594  ,
                -4266.19   ,   -376.18857,  -8161.785  ,  64706.766  ,
                -4266.19   ,   -376.18857,  -8161.785  ,  45754.594  ,
                -4266.19   ,   -376.18857,  -8161.785  ,      0.     ,
                -4266.19   ,   -376.18857,  -8161.785  , -45754.594  ,
                -4274.038  ,   -376.62527,  -8171.2603 ,   2202.7085 ,
               -29566.24   ,   -376.62527,  -8171.2603 ,   1557.55   ,
               -40042.613  ,   -376.62527,  -8171.2603 ,      0.     ,
               -29566.24   ,   -376.62527,  -8171.2603 ,  -1557.55   ,
                -4274.038  ,   -376.62527,  -8171.2603 ,  -2202.7085 ,
                21018.164  ,   -376.62527,  -8171.2603 ,  -1557.55   ,
                31494.537  ,   -376.62527,  -8171.2603 ,      0.     ,
                21018.164  ,   -376.62527,  -8171.2603 ,   1557.55   ],
              dtype=float32)

        This data corresponds to the results you would obtain directly
        from MAPDL with ESOL commands:

        >>> ansys.esol(nvar='2', elem=enum[0], node=enode[0][0], item='LS', comp=1)
        >>> ansys.vget(par='SD_LOC1', ir='2', tstrt='1') # store in a variable
        >>> ansys.read_float_parameter('SD_LOC1(1)')
        -4266.19
        """
        raise NotImplementedError(
            NOT_AVAILABLE_METHOD.format(method="element_solution_data")
        )

    def result_dof(self, rnum: Rnum):
        """Return a list of degrees of freedom for a given result number.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        Returns
        -------
        dof : list
            List of degrees of freedom.

        Examples
        --------
        >>> rst.result_dof(0)
        ['UX', 'UY', 'UZ']
        """
        # To be done later
        raise NotImplementedError(NOT_AVAILABLE_METHOD.format(method="result_dof"))

    def cs_4x4(self, cs_cord: int, as_vtk_matrix: bool = False):
        """Return a 4x4 transformation matrix for a given coordinate system.

        Parameters
        ----------
        cs_cord : int
            Coordinate system index.

        as_vtk_matrix : bool, default: False
            Return the transformation matrix as a ``vtkMatrix4x4``.

        Returns
        -------
        np.ndarray | vtk.vtkMatrix4x4
            Matrix or ``vtkMatrix4x4`` depending on the value of ``as_vtk_matrix``.

        Notes
        -----
        Values 11 and greater correspond to local coordinate systems

        Examples
        --------
        Return the transformation matrix for coordinate system 1.

        >>> tmat = rst.cs_4x4(1)
        >>> tmat
        array([[1., 0., 0., 0.],
               [0., 1., 0., 0.],
               [0., 0., 1., 0.],
               [0., 0., 0., 1.]])

        Return the transformation matrix for coordinate system 5. This
        corresponds to ``CSYS, 5``, the cylindrical with global Cartesian Y as
        the axis of rotation.

        >>> tmat = rst.cs_4x4(5)
        >>> tmat
        array([[ 1.,  0.,  0.,  0.],
               [ 0.,  0., -1.,  0.],
               [ 0.,  1.,  0.,  0.],
               [ 0.,  0.,  0.,  1.]])
        """
        raise NotImplementedError(NOT_AVAILABLE_METHOD.format(method="cs_4x4"))

    def read_record(self, pointer: int, return_bufsize: bool = False):
        """Reads a record at a given position.

        Because ANSYS 19.0+ uses compression by default, you must use
        this method rather than ``np.fromfile``.

        Parameters
        ----------
        pointer : int
            ANSYS file position (n words from start of file).  A word
            is four bytes.

        return_bufsize : bool, optional
            Returns the number of words read (includes header and
            footer).  Useful for determining the new position in the
            file after reading a record.

        Returns
        -------
        record : np.ndarray
            The record read as a ``n x 1`` numpy array.

        bufsize : float, optional
            When ``return_bufsize`` is enabled, returns the number of
            words read.
        """
        raise NotImplementedError(NOT_AVAILABLE_METHOD.format(method="read_record"))

    def text_result_table(self, rnum: Rnum):
        """Returns a text result table for plotting.

        Parameters
        ----------
        rnum
            The result number to retrieve the table for.
        """
        raise NotImplementedError(
            NOT_AVAILABLE_METHOD.format(method="text_result_table")
        )

    def write_tables(self, filename: str | Path):
        """Write binary tables to ASCII.  Assumes int32

        Parameters
        ----------
        filename : str, Path
            Filename to write the tables to.

        Examples
        --------
        >>> rst.write_tables('tables.txt')
        """
        raise NotImplementedError(NOT_AVAILABLE_METHOD.format(method="write_tables"))

    def overwrite_element_solution_records(
        self, element_data: dict[int, np.ndarray], rnum: Rnum, solution_type: str
    ):
        """Overwrite element solution record.

        This method replaces solution data for a set of elements at a
        result index for a given solution type.  The number of items
        in ``data`` must match the number of items in the record.

        If you are not sure how many records are in a given record,
        use ``element_solution_data`` to retrieve all the records for
        a given ``solution_type`` and check the number of items in the
        record.

        Note: The record being replaced cannot be a compressed record.
        If the result file uses compression (default sparse
        compression as of 2019R1), you can disable this within MAPDL
        with:
        ``/FCOMP, RST, 0``

        Parameters
        ----------
        element_data : dict
            Dictionary of results that will replace the existing records.

        rnum : int
            Zero based result number.

        solution_type : str
            Element data type to overwrite.

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

        Examples
        --------
        Overwrite the elastic strain record for elements 1 and 2 with
        for the first result with random data.

        >>> from ansys.mapdl import reader as pymapdl_reader
        >>> rst = pymapdl_reader.read_binary('file.rst')
        >>> data = {1: np.random.random(56),
                    2: np.random.random(56)}
        >>> rst.overwrite_element_solution_data(data, 0, 'EEL')
        """
        raise NotImplementedError(
            NOT_AVAILABLE_METHOD.format(method="overwrite_element_solution_records")
        )

    def nodal_time_history(
        self, solution_type: SolutionType = "NSL", in_nodal_coord_sys: bool = False
    ) -> ReturnData:
        """The DOF solution for each node for all result sets.

        The nodal results are returned returned in the global
        cartesian coordinate system or nodal coordinate system.

        Parameters
        ----------
        solution_type
            The solution type.  Must be either nodal displacements
            (``'NSL'``), nodal velocities (``'VEL'``) or nodal
            accelerations (``'ACC'``).
            Default is ``'NSL'``.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate system.
            Default ``False``.

        Returns
        -------
        np.ndarray
            Node numbers associated with the results.

        np.ndarray
            Nodal solution for all result sets.  Array is sized
            ``rst.nsets x nnod x Sumdof``, which is the number of
            time steps by number of nodes by degrees of freedom.
        """
        if solution_type == "NSL":
            func = self.nodal_solution  # type: ignore
        elif solution_type == "VEL":
            func = self.nodal_velocity  # type: ignore
        elif solution_type == "ACC":
            func = self.nodal_acceleration  # type: ignore
        else:
            raise ValueError(
                "Argument 'solution type' must be either 'NSL', " "'VEL', or 'ACC'"
            )

        # size based on the first result
        nnum, sol = func(0, in_nodal_coord_sys=in_nodal_coord_sys)
        data = np.empty((self.nsets, sol.shape[0], sol.shape[1]), np.float64)
        data[0] = sol
        for i in range(1, self.nsets):
            data[i] = func(i, in_nodal_coord_sys=in_nodal_coord_sys)[1]

        return nnum, data

    def nodal_displacement(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
        """Returns the DOF solution for each node in the global
        cartesian coordinate system or nodal coordinate system.

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default ``False``.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        int np.ndarray
            Node numbers associated with the results.

        float np.ndarray
            Array of nodal displacements.  Array
            is (``nnod`` x ``sumdof``), the number of nodes by the
            number of degrees of freedom which includes ``numdof`` and
            ``nfldof``

        Examples
        --------
        Return the nodal solution (in this case, displacement) for the
        first result of ``"file.rst"``

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
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
        return self._get_nodes_result(rnum, "displacement", in_nodal_coord_sys, nodes)

    def nodal_solution(
        self,
        rnum: Rnum,
        in_nodal_coord_sys: bool = False,
        nodes: Nodes = None,
        return_temperature: bool = False,
    ) -> ReturnData:
        """Returns the DOF solution for each node in the global
        cartesian coordinate system or nodal coordinate system.

        Solution may be nodal temperatures or nodal displacements
        depending on the type of the solution.

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default ``False``.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        return_temperature
            When ``True``, returns the nodal temperature instead of
            the displacement.  Default ``False``.

        Returns
        -------
        int np.ndarray
            Node numbers associated with the results.

        float np.ndarray
            Array of nodal displacements or nodal temperatures.  Array
            is (``nnod`` x ``sumdof``), the number of nodes by the
            number of degrees of freedom which includes ``numdof`` and
            ``nfldof``

        Examples
        --------
        Return the nodal solution (in this case, displacement) for the
        first result of ``"file.rst"``

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
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

        if hasattr(self.model.results, "displacement") and not return_temperature:
            return self.nodal_displacement(rnum, in_nodal_coord_sys, nodes)
        elif hasattr(self.model.results, "temperature"):
            return self.nodal_temperature(rnum, nodes)
        else:
            raise ResultNotFound(
                "The current analysis does not have 'displacement' or 'temperature' results."
            )

    def nodal_temperature(self, rnum: Rnum, nodes: Nodes = None) -> ReturnData:
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
        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, temp = rst.nodal_temperature(0)

        Return the temperature just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, temp = rst.nodal_stress(0, nodes='MY_COMPONENT')

        Return the temperature just for the nodes from 20 through 50.

        >>> nnum, temp = rst.nodal_solution(0, nodes=range(20, 51))
        """
        return self._get_nodes_result(rnum, "temperature", nodes=nodes)

    def nodal_voltage(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
        """Retrieves the voltage for each node in the
        solution.

        The order of the results corresponds to the sorted node
        numbering.

        Equivalent MAPDL command: PRNSOL, VOLT

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default ``False``.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        numpy.ndarray
            Node numbers of the result.

        numpy.ndarray
            Voltage at each node.

        Examples
        --------
        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, temp = rst.nodal_voltage(0)

        Return the voltage just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, temp = rst.nodal_stress(0, nodes='MY_COMPONENT')
        """
        return self._get_nodes_result(
            rnum, "electric_potential", in_nodal_coord_sys, nodes
        )

    def element_stress(
        self,
        rnum: Rnum,
        principal: bool = False,
        in_element_coord_sys: bool = False,
        elements: Elements = None,
        **kwargs: Kwargs,
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
            When ``True``, returns results in the element coordinate
            system.  Default ``False``.

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
        if kwargs:
            raise NotImplementedError(
                "Hidden options for distributed result files are not implemented."
            )

        if principal:
            op = self._get_elem_result(
                rnum,
                "stress",
                in_element_coord_sys=in_element_coord_sys,
                elements=elements,
                return_operator=True,
            )
            return self._get_principal(op)
        return self._get_elem_result(rnum, "stress", in_element_coord_sys, elements)

    def element_nodal_stress(
        self,
        rnum: Rnum,
        principal: bool = False,
        in_element_coord_sys: bool = False,
        elements: Elements = None,
        **kwargs: Kwargs,
    ):
        """Retrieves the nodal stresses for each element.

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a list containing
            (step, substep) of the requested result.

        principal
            Returns principal stresses instead of component stresses.
            Default False.

        in_element_coord_sys
            Returns the results in the element coordinate system if ``True``.
            Else, it returns the results in the global coordinate system.
            Default False

        elements
            Select a limited subset of elements.  Can be a element
            component or array of element numbers.  For example:

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        **kwargs
            Hidden options for distributed result files.

        Returns
        -------
        np.ndarray
            ANSYS element numbers corresponding to each element.

        list
            Stresses at each element for each node for Sx Sy Sz Sxy
            Syz Sxz or SIGMA1, SIGMA2, SIGMA3, SINT, SEQV when
            principal is True.

        list
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
        if kwargs:
            raise NotImplementedError(
                "Hidden options for distributed result files are not implemented."
            )

        if principal:
            op = self._get_elemnodal_result(
                rnum,
                "stress",
                in_element_coord_sys=in_element_coord_sys,
                elements=elements,
                return_operator=True,
            )
            return self._get_principal(op)
        return self._get_elemnodal_result(
            rnum, "stress", in_element_coord_sys, elements
        )

    def nodal_elastic_strain(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
        """Nodal component elastic strains.  This record contains
        strains in the order ``X, Y, Z, XY, YZ, XZ, EQV``.

        Elastic strains can be can be nodal values extrapolated from
        the integration points or values at the integration points
        moved to the nodes.

        Equivalent MAPDL command: ``PRNSOL, EPEL``

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        np.ndarray
            MAPDL node numbers.

        np.ndarray
            Nodal component elastic strains.  Array is in the order
            ``X, Y, Z, XY, YZ, XZ, EQV``.

            .. versionchanged:: 0.64
                The nodes with no values are now equals to zero.
                The results of the midnodes are also calculated and
                presented.

        Examples
        --------
        Load the nodal elastic strain for the first result.

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, elastic_strain = rst.nodal_elastic_strain(0)

        Return the nodal elastic strain just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, elastic_strain = rst.nodal_elastic_strain(0, nodes='MY_COMPONENT')

        Return the nodal elastic strain just for the nodes from 20 through 50.

        >>> nnum, elastic_strain = rst.nodal_elastic_strain(0, nodes=range(20, 51))

        Notes
        -----
        Nodes without a strain will be NAN.

        ..
        """
        return self._get_nodes_result(
            rnum, "elastic_strain", in_nodal_coord_sys=in_nodal_coord_sys, nodes=nodes
        )

    def nodal_plastic_strain(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
        """Nodal component plastic strains.

        This record contains strains in the order:
        ``X, Y, Z, XY, YZ, XZ, EQV``.

        Plastic strains are always values at the integration points
        moved to the nodes.

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        np.ndarray
            MAPDL node numbers.

        np.ndarray
            Nodal component plastic strains.  Array is in the order
            ``X, Y, Z, XY, YZ, XZ, EQV``.

        Examples
        --------
        Load the nodal plastic strain for the first solution.

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, plastic_strain = rst.nodal_plastic_strain(0)

        Return the nodal plastic strain just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, plastic_strain = rst.nodal_plastic_strain(0, nodes='MY_COMPONENT')

        Return the nodal plastic strain just for the nodes from 20
        through 50.

        >>> nnum, plastic_strain = rst.nodal_plastic_strain(0, nodes=range(20, 51))
        """
        return self._get_nodes_result(rnum, "plastic_strain", in_nodal_coord_sys, nodes)

    def nodal_acceleration(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
        """Nodal velocities for a given result set.

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        np.ndarray
            Node numbers associated with the results.

        np.ndarray
            Array of nodal accelerations.  Array is (``nnod`` x
            ``sumdof``), the number of nodes by the number of degrees
            of freedom which includes ``numdof`` and ``nfldof``

        Examples
        --------
        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, data = rst.nodal_acceleration(0)

        Notes
        -----
        Some solution results may not include results for each node.
        These results are removed by and the node numbers of the
        solution results are reflected in ``nnum``.
        """
        return self._get_nodes_result(rnum, "acceleration", in_nodal_coord_sys, nodes)

    def nodal_reaction_forces(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
        """Nodal reaction forces.

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        np.ndarray
            Node numbers corresponding to the reaction forces.  Node
            numbers may be repeated if there is more than one degree
            of freedom for each node.

        np.ndarray
            Degree of freedom corresponding to each node using the
            MAPDL degree of freedom reference table.

        Examples
        --------
        Get the nodal reaction forces for the first result and print
        the reaction forces of a single node.

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> rforces, nnum, dof = rst.nodal_reaction_forces(0)
        >>> dof_ref = rst.result_dof(0)
        >>> rforces[:3], nnum[:3], dof[:3], dof_ref
        (array([  24102.21376091, -109357.01854005,   22899.5303263 ]),
         array([4142, 4142, 4142]),
         array([1, 2, 3], dtype=int32),
         ['UX', 'UY', 'UZ'])
        """
        return self._get_nodes_result(rnum, "reaction_force", in_nodal_coord_sys, nodes)

    def nodal_stress(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
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
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        nodes
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
        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
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
        return self._get_nodes_result(rnum, "stress", in_nodal_coord_sys, nodes)

    def nodal_thermal_strain(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
        """Nodal component thermal strain.

        This record contains strains in the order X, Y, Z, XY, YZ, XZ,
        EQV, and eswell (element swelling strain).  Thermal strains
        are always values at the integration points moved to the
        nodes.

        Equivalent MAPDL command: PRNSOL, EPTH, COMP

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        np.ndarray
            MAPDL node numbers.

        np.ndarray
            Nodal component plastic strains.  Array is in the order
            ``X, Y, Z, XY, YZ, XZ, EQV, ESWELL``

        Examples
        --------
        Load the nodal thermal strain for the first solution.

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, thermal_strain = rst.nodal_thermal_strain(0)

        Return the nodal thermal strain just for the nodal component
        ``'MY_COMPONENT'``.

        >>> nnum, thermal_strain = rst.nodal_thermal_strain(0, nodes='MY_COMPONENT')

        Return the nodal thermal strain just for the nodes from 20 through 50.

        >>> nnum, thermal_strain = rst.nodal_thermal_strain(0, nodes=range(20, 51))
        """
        return self._get_nodes_result(rnum, "thermal_strain", in_nodal_coord_sys, nodes)

    def nodal_velocity(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
        """Nodal velocities for a given result set.

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        nodes
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
            Array of nodal velocities.  Array is (``nnod`` x
            ``sumdof``), the number of nodes by the number of degrees
            of freedom which includes ``numdof`` and ``nfldof``

        Examples
        --------
        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
        >>> nnum, data = rst.nodal_velocity(0)

        Notes
        -----
        Some solution results may not include results for each node.
        These results are removed by and the node numbers of the
        solution results are reflected in ``nnum``.
        """
        return self._get_nodes_result(rnum, "velocity", in_nodal_coord_sys, nodes)

    def nodal_static_forces(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
        """Return the nodal forces averaged at the nodes.

        Nodal forces are computed on an element by element basis, and
        this method averages the nodal forces for each element for
        each node.

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            When ``True``, returns results in the nodal coordinate
            system.  Default False.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        np.ndarray
            MAPDL node numbers.

        np.ndarray
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
        return self._get_nodes_result(rnum, "nodal_force", in_nodal_coord_sys, nodes)

    def principal_nodal_stress(
        self, rnum: Rnum, in_nodal_coord_sys: bool = False, nodes: Nodes = None
    ) -> ReturnData:
        """Computes the principal component stresses for each node in
        the solution.

        Parameters
        ----------
        rnum
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        in_nodal_coord_sys
            If True, return the results in the nodal coordinate system.

        nodes
            Select a limited subset of nodes. Can be a nodal
            component or array of node numbers. For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        Returns
        -------
        numpy.ndarray
            Node numbers of the result.

        numpy.ndarray
            Principal stresses, stress intensity, and equivalent stress.
            [sigma1, sigma2, sigma3, sint, seqv]

        Examples
        --------
        Load the principal nodal stress for the first solution.

        >>> from ansys.mapdl.core.reader import DPFResult as Result
        >>> rst = Result('file.rst')
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
        op = self._get_nodes_result(
            rnum,
            "stress",
            in_nodal_coord_sys=in_nodal_coord_sys,
            nodes=nodes,
            return_operator=True,
        )
        return self._get_principal(op)
