import os
import weakref

import numpy as np

from ansys.mapdl.core.errors import MapdlRuntimeError

from .mapdl_grpc import MapdlGrpc


class KrylovSolver:
    """Abstract mapdl krylov class.  Created from a ``Mapdl`` instance.

    Notes
    -----
    The procedure to use the Krylov solver is composed of three steps:

    1. Generate Krylov subspace using
       :func:`KrylovSolver.gensubspace <ansys.mapdl.core.krylov.KrylovSolver.gensubspace>`.

    2. Use :func:`KrylovSolver.solve <ansys.mapdl.core.krylov.KrylovSolver.solve>`
       to solve the generated Krylovsub space using a reduced harmonic analysis over
       a specified frequency range

    3. Expand the reduced solution back to the original space using
       :func:`KrylovSolver.solve <ansys.mapdl.core.krylov.KrylovSolver.solve>`

    Examples
    --------
    Create an instance.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> ....
    >>> ....
    >>> Generate the FEA model (mesh, constraints, loads)
    >>> Generate the .full file

    >>> mk = mapdl.krylov
    >>> # Generate the Krylov subspace
    >>> Qz = mk.gensubspace(10, 100, check_orthogonality=True)
    >>> # Reduce the system of equations and solve at each frequency.
    >>> Yz = mk.solve(10, 100,  freq_steps=1, ramped_load=True)
    >>> # Expand the reduced solution back to the FE space.
    >>> res = mk.expand(residual_computation=True, residual_algorithm="l2")

    """

    def __init__(self, mapdl):
        if not isinstance(mapdl, MapdlGrpc):  # pragma: no cover
            raise TypeError("``mapdl`` must be a MapdlGrpc instance")
        self._mapdl_weakref = weakref.ref(mapdl)
        self.mm = self._mapdl.math
        self.jobname = self._mapdl.jobname
        self.logger = self._mapdl._log

        # run flags
        self._run_gensubspace = False
        self._run_solve = False

        self.residuals = None
        self.solution_vectors = None
        self.orthogonality = None

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl."""
        return self._mapdl_weakref()

    def _check_full_file_exists(self, full_file=None):
        """Check full file exists."""
        current_dir = self._mapdl.directory
        # Check if full file exists
        if not full_file:
            self.full_file = self._mapdl.jobname + ".full"
        else:
            self.full_file = full_file

        # Checking if the full file exists.
        if self._mapdl._local:  # pragma: no cover
            if not os.path.exists(os.path.join(current_dir, self.full_file)):
                raise FileNotFoundError(
                    f"The file '{self.full_file}' could not be found in local directory '{current_dir}'."
                )
        else:
            if self.full_file not in self._mapdl.list_files():
                raise FileNotFoundError(
                    f"The file '{self.full_file}' could not be found in the remote MAPDL instance."
                )

    @property
    def is_orthogonal(self):
        """
        Check whether the solution is orthogonal.

        Returns
        -------
        bool
            If the matrix is orthogonal, returns ``True``, otherwise is ``False``.
        """
        if self.orthogonality is not None:
            eye_ = np.eye(N=self.orthogonality.shape[0])
            return np.allclose(self.orthogonality, eye_)

    def _check_input_gensubspace(self, max_dim_q, freq_val, check_orthogonality):
        """Validate the inputs to the ``gensubspace`` method."""

        # Check for illegal input values by the user
        if not isinstance(max_dim_q, int) or max_dim_q <= 0:
            raise ValueError(
                "The maximum size of the Krylov subspace must be greater than 0."
            )

        if not isinstance(freq_val, int) or freq_val < 0:
            raise ValueError(
                "The frequency value ('freq_val') for building the Krylov subspace must be "
                "equal to or greater than 0 Hz."
            )

        if not isinstance(check_orthogonality, bool):
            raise ValueError(
                "The 'check_orthogonality' value for building the Krylov subspace must be "
                "True or False"
            )

    def _check_input_solve(self, freq_start, freq_end, freq_steps, ramped_load):
        """Validate the inputs to the ``solve`` method."""

        if not isinstance(freq_start, int) or freq_start < 0:
            raise ValueError(
                "The beginning frequency value for solving the reduced solution must be "
                "equal to or greater than 0 Hz."
            )

        if not isinstance(freq_end, int) or freq_end < 0 or freq_end < freq_start:
            raise ValueError(
                "The beginning frequency value for solving the reduced solution must be "
                "equal to or greater than 0 Hz, and greater than starting frequency.'"
            )

        if not isinstance(freq_steps, int) or freq_steps < 1:
            raise ValueError(
                "The number of frequencies ('freq_steps') for which to compute the reduced "
                "solution must be to be an integer greater than or equal to 1."
            )

        if not isinstance(ramped_load, bool):
            raise ValueError(
                "The 'ramped_load' argument for computing the reduced solution must be "
                "True or False"
            )

    def _check_input_expand(
        self, return_solution, residual_computation, residual_algorithm
    ):
        """Validate the inputs to the ``expand`` method."""

        if not isinstance(return_solution, bool):
            raise ValueError(
                "The 'return_solution' value for expanding the solution must be True or False"
            )
        if not isinstance(residual_computation, bool):
            raise ValueError("The 'residual_computation' must be True or False.")
        if not isinstance(
            residual_algorithm, str
        ) or residual_algorithm.lower() not in [
            "l-inf",
            "linf",
            "l-1",
            "l1",
            "l-2",
            "l2",
        ]:
            raise ValueError(
                "The provided 'residual_algorithm' is not allowed. Only allowed are 'L-inf', 'Linf', 'L-1', 'L1', 'L-2', 'L2'."
            )

    def _get_data_from_full_file(self):
        """Extract stiffness, mass, damping, and force matrices from the FULL file."""

        self._mat_k = self.mm.stiff(fname=self.full_file)
        self._ndof = self._mat_k.shape[1]
        self._mat_m = self.mm.mass(fname=self.full_file)
        self._mat_c = self.mm.damp(fname=self.full_file)

        self._mapdl.smat("Nod2Solv", "D", "IMPORT", "FULL", self.full_file, "NOD2SOLV")
        self.Nod2Solv = self.mm.mat(name="Nod2Solv")

        self._mapdl.vec("fz", "Z", "IMPORT", "FULL", self.full_file, "RHS")
        self._mapdl.vec("fz0", "Z", "COPY", "fz")
        self.fz0 = self.mm.vec(name="fz0")

    def _calculate_orthogonality(self, uz, num_q):
        """Check Orthonormality of vectors"""

        if self.orthogonality is not None:
            # Using previously calculated (if any)
            return self.orthogonality

        orthogonality = np.zeros(shape=(num_q, num_q))
        for i in range(num_q):
            self._mapdl.vec("Vz", "Z", "LINK", self.Qz.id, i + 1)
            Vz = self.mm.vec(name="Vz")
            Vz_m = Vz.asarray()
            for j in range(num_q):
                self._mapdl.vec(uz.id, "Z", "LINK", self.Qz.id, j + 1)
                uz_m = uz.asarray()
                rcon = np.vdot(Vz_m, uz_m)
                rcon_real = rcon.real
                rcon_imag = rcon.imag
                dcon = np.sqrt(rcon_real * rcon_real + rcon_imag * rcon_imag)
                orthogonality[i, j] = dcon

        self.orthogonality = orthogonality
        return self.orthogonality

    def gensubspace(
        self, max_dim_q, frequency, check_orthogonality=False, full_file=None
    ):
        """Generate a Krylov subspace for model reduction in a harmonic analysis.

        This method generates a Krylov subspace used for a model reduction
        solution in a harmonic analysis. The subspace is built using the
        assembled matrices and load vector on the ``<jobname>.full`` file that
        is located in the current working directory. This FULL file
        should be built at the specified frequency value.

        Parameters
        ----------
        max_dim_q : int
          Maximum size/dimension of the Krylov subspace.

        frequency : int
          Frequency value in Hz to build the Krylov subspace at.

        check_orthogonality : bool, optional
          Whether to check the orthonormal properties of each subspace vector
          with all other subspace vectors. The result matrix is stored in
          :attr:`KrylovSolver.orthogonality <ansys.mapdl.core.krylov.KrylovSolver.orthogonality`.
          The default is ``False``.

        full_file : str, optional
          Name of the FULL file to read. The default is ``<jobname>.full``.

        Returns
        -------
        AnsMat
            Krylov subspace.

        Notes
        -----
        Distributed Ansys restriction: This command is not supported in
        Distributed Ansys.
        """

        current_dir = self._mapdl.directory
        self.logger.debug(f"Current directory: {current_dir}")

        two_pi = 2.0 * np.pi
        omega_zero = frequency * two_pi
        ccf = -(omega_zero**2)
        init_val = 2  # Initialized as no damping
        zero_c = 0

        # Check full file exists
        self._check_full_file_exists(full_file)

        # Check the inputs
        self._check_input_gensubspace(max_dim_q, frequency, check_orthogonality)

        # Get matrices from full file
        self._get_data_from_full_file()

        # Get the force vector from the defined Ansvec
        fz = self.mm.vec(name="fz")

        # Create subspace
        self.Qz = self.mm.zeros(self._ndof, max_dim_q, dtype=np.cdouble)

        # Form az = (K-w0*w0*M,i*w0*C)
        self._mapdl.smat("az", "Z", "COPY", self._mat_k.id)
        az = self.mm.mat(name="az")
        az.axpy(self._mat_m, ccf, 1.0)
        self._mapdl.axpy(0.0, omega_zero, self._mat_c.id, 1.0, 0.0, az.id)

        # Form cz=(C+i*2*w0*M)
        self._mapdl.smat("cz", "Z", "COPY", self._mat_c.id)
        cz = self.mm.mat(name="cz")
        self._mapdl.axpy(0.0, 2 * omega_zero, self._mat_m.id, 1.0, 0.0, cz.id)

        norm_c = self._mapdl.nrm(cz.id, "NRM2", "normC", "NO")

        if not norm_c:
            zero_c = 1

        # Solve for the 1st vector of subspace[Q]
        # Create solver system of [az]
        s = self.mm.factorize(az)  # Factor [az]

        # {uz1} linked to Qz[1]
        self._mapdl.vec("uz1", "Z", "LINK", self.Qz.id, 1)
        uz1 = self.mm.vec(name="uz1")

        uz1 = s.solve(fz, uz1)
        norm_u = self._mapdl.nrm(uz1.id, "NRM2", "normU", "YES")

        if not zero_c:
            init_val = 3
            self._mapdl.vec("uz2", "Z", "LINK", self.Qz.id, 2)
            uz2 = self.mm.vec(name="uz2")
            fz.zeros()  # {fz}=0

            # {fz}={fz}+[cz]{uz1}
            fz = cz.dot(uz1)
            fz *= -1  # {fz}=-{fz}
            norm_u = self._mapdl.nrm(fz.id, "NRM2", "normU", "YES")

            uz2 = s.solve(fz, uz2)  # back solved:{uz2}=[az]^-1*{fz}

            # {uz2}*{v1} = ccon
            self._mapdl.dot(uz1.id, uz2.id, "ccon_real", "ccon_imag")
            # {uz2}={uz2}-ccon*{uz1}
            self._mapdl.axpy("-ccon_real", "-ccon_imag", uz1.id, 1.0, 0.0, uz2.id)
            # {uz2} normalized
            norm_u = self._mapdl.nrm(uz2.id, "NRM2", "normU", "YES")

        # Build Subspace Vectors with MGS (2nd Order)
        for dim_q in range(init_val, max_dim_q + 1):
            self.dim_q = dim_q
            if norm_u == 0:
                num_q = dim_q - 1  # exhausted at dim_q
            else:
                num_q = max_dim_q  # may reach to the maximum

            if num_q >= max_dim_q:  # make next vector
                fz.zeros()
                if zero_c == 0:  # [cz]!=0 case
                    next_uz_one = dim_q - 2
                    next_uz_two = dim_q - 1
                    # {uz1} to [Qz](dim_q-2)
                    self._mapdl.vec(uz1.id, "Z", "LINK", self.Qz.id, next_uz_one)
                    # {uz2} to [Qz](dim_q-1)
                    self._mapdl.vec(uz2.id, "Z", "LINK", self.Qz.id, next_uz_two)
                    # {uz} to [Qz](dim_q)
                    self._mapdl.vec("uz", "Z", "LINK", self.Qz.id, dim_q)
                    uz = self.mm.vec(name="uz")
                    # [cz]{uz2} -> {uz}
                    uz += cz.dot(uz2)

                else:  # [cz]=0 case
                    next_uz_one = dim_q - 1
                    self._mapdl.vec(uz1.id, "Z", "LINK", self.Qz.id, next_uz_one)
                    # {uz} to [Qz](dim_q)
                    self._mapdl.vec(uz2.id, "Z", "LINK", self.Qz.id, dim_q)
                    uz.zeros()

                # [MatM]{uz1} -> {fz}
                self._mapdl.mult(m1=self._mat_m.id, t1="", m2=uz1.id, t2="", m3=fz.id)
                fz.axpy(uz, -1.0, -1.0)  # {fz} = -{fz}-{uz}
                uz = s.solve(fz, uz)  # [az]^-1{fz} -> {uz}

                # Make subspace vectors orthonormal
                for j in range(1, dim_q):
                    self._mapdl.vec("V1", "Z", "LINK", self.Qz.id, j)
                    V1 = self.mm.vec(name="V1")
                    self._mapdl.dot(V1.id, uz.id, "ccon_real", "ccon_imag")
                    self._mapdl.axpy("-ccon_real", "-ccon_imag", V1.id, 1.0, 0.0, uz.id)

                norm_u = self._mapdl.nrm(uz.id, "NRM2", "normU", "YES")

        # Optional check on Orthonormality of vectors
        if check_orthogonality:
            self._calculate_orthogonality(uz, num_q)

        self._run_gensubspace = True
        return self.Qz

    def solve(self, freq_start, freq_end, freq_steps, ramped_load=True):
        """Reduce the system of equations and solve at each frequency.

        This method uses a Krylov subspace to solve a reduced harmonic
        analysis over a specified frequency range for a given number of
        frequency points (intervals).

        Parameters
        ----------
        freq_start : int
          Starting value of the frequency range in Hz.
        freq_end : int
          Ending value of the frequency range in Hz.
        freq_steps : int
          Number of intervals in the frequency range.
        ramped_load : bool
          Whether to use ramped load. If not, the load used is stepped (``False``).
          Defaults to ``True``.

        Returns
        -------
        AnsMat
            Reduced solution over the frequency range.

        Notes
        -----
        Distributed Ansys restriction: This command is not supported in
        Distributed Ansys.
        """

        # Check we ran gensubspace method before
        if not self._run_gensubspace:
            raise MapdlRuntimeError(
                "The method 'gensubspace' should be executed first."
            )

        # Check inputs before executing the method
        self._check_input_solve(freq_start, freq_end, freq_steps, ramped_load)

        # Execute macro if no errors raised
        # Store input arguments from user
        self.freq_start = freq_start
        self.freq_steps = freq_steps
        self.ramped_load = ramped_load
        self.freq_end = freq_end

        az = self.mm.mat(name="az")
        ndof = self._ndof
        dim_q = self.dim_q

        # Define solution variables
        QtF = self.mm.zeros(dim_q, dtype=np.cdouble)
        QtAQ = self.mm.zeros(dim_q, dim_q, dtype=np.cdouble)  # [QtAQ], reduced matrix
        self.Yz = self.mm.zeros(
            dim_q, self.freq_steps, dtype=np.cdouble
        )  # [Yz], reduced solution over range
        self.DzV = self.mm.zeros(
            ndof, self.freq_steps, dtype=np.cdouble
        )  # {DzV}, displacement vector
        self.iRHS = self.mm.zeros(ndof, dtype=np.cdouble)

        # Loop over frequency range
        omega = self.freq_start * 2 * np.pi
        self.intV = (self.freq_end - self.freq_start) / self.freq_steps

        for iFreq in range(1, self.freq_steps + 1):
            # form RHS at the i-th frequency point
            self.iRHS.zeros()
            if self.ramped_load == 0:
                # apply ramped loading
                ratio = 2 * iFreq / self.freq_steps
                if self.freq_steps == 1:
                    ratio = 1.00
            else:
                # Apply stepped loading
                ratio = 1.00

            self.iRHS.axpy(self.fz0, ratio, 1.0)  # Get {iRHS} at iFreq
            QtF = self.Qz.T.dot(self.iRHS)  # Reduce [Qz]^t{iRHS} -> {QtF}

            # link iY to Yz(iFreq)
            self._mapdl.vec("iY", "Z", "LINK", self.Yz.id, iFreq)
            self.iY = self.mm.vec(name="iY")

            # Reduced system at omega
            omega = omega + self.intV * 2 * np.pi  # defined frequency value
            ccf = -omega * omega

            # modified K:[az]=[MatK]
            self._mapdl.smat("az", "Z", "COPY", self._mat_k.id)
            az = self.mm.mat(name="az")

            # [az]=(1,0)*[az]+(ccf,0)*[MatM]
            az.axpy(self._mat_m, ccf, 1.0)
            # [az]=(1,0)*[az]-(0,omega)*[mat_C]
            self._mapdl.axpy(0.0, omega, self._mat_c.id, 1.0, 0.0, az.id)

            AQ = az.dot(self.Qz)  # [AQ]=[az][Qz]
            QtAQ = self.Qz.T.dot(AQ)  # [QtAQ]=[Q^t][AQ]

            # create reduced system of equations
            s = self.mm.factorize(QtAQ)
            # back solve for {iY}=Yz[iFreq]
            self.iY = s.solve(QtF, self.iY)

        self._run_solve = True
        return self.Yz

    def expand(
        self,
        residual_computation=False,
        residual_algorithm=None,
        compute_solution_vectors=True,
        return_solution=False,
    ):
        """Expand the reduced solution back to FE space.

        This method expands the reduced solution for a harmonic analysis
        back to the original space. Optional calculation of the residual
        is available.

        Parameters
        ----------
        residual_computation  : bool, optional
          Compute the residual of the expanded solution.
          Default to ``False``.

        residual_algorithm : str, optional
          Specifies the type of residual normal calculation. It can take
          the following values:
          * "L-inf": Compute the L-inf norm of the residual. Default value.
          * "L-1": Compute the L-1 norm of the residual.
          * "L-2": Compute the L-2 norm of the residual.

        compute_solution_vectors : bool, optional
          If ``True`` it compute the solution vectors. The solution vectors
          are stored in :attr:`Krylov.solution_vectors
          <ansys.mapdl.core.krylov.KrylovSolver.solution_vectors>` method.
          Defaults to ``True``.

        return_solution : bool, optional
          If ``True`` it will return the solution vectors. By default is ``False``.

        Returns
        -------
        np.ndarray
            Solution vectors mapped to a given order. (if ``return_solution = True``)
        None
            If ``return_solution = False``

        Notes
        -----
        Distributed Ansys restriction: This command is not supported in
        Distributed Ansys.
        """
        # Check we ran solve method before
        if not self._run_solve:
            raise MapdlRuntimeError("The method 'solve' should be executed first.")

        if residual_algorithm is not None:
            # To avoid having to set residual computation.
            residual_computation = True
        elif residual_algorithm is None:
            residual_algorithm = "L-Inf"

        # Check inputs before executing the method
        self._check_input_expand(
            return_solution, residual_computation, residual_algorithm
        )

        self._residual_algorithm = residual_algorithm

        RzV = self.mm.zeros(self._ndof, 1, dtype=np.cdouble)

        # Build mapping vectors
        self._mapdl.vec("MapForward", "I", "IMPORT", "FULL", self.full_file, "FORWARD")
        self._map_forward = self.mm.vec(name="MapForward")

        self._mapdl.vec("MapBack", "I", "IMPORT", "FULL", self.full_file, "BACK")
        map_back = self.mm.vec(name="MapBack")

        self._max_node = self._map_forward.size
        self._num_node = map_back.size

        # Expand reduced solution
        omega = self.freq_start * 2 * np.pi  # circular frequency at starting point
        xii_usr_ordered = []

        for iFreq in range(1, self.freq_steps + 1):
            self._mapdl.vec(self.iY.id, "Z", "LINK", self.Yz.id, iFreq)
            # vector of solution in solver space
            self._mapdl.vec("Xi", "Z", "LINK", self.DzV.id, iFreq)
            Xi = self.mm.vec(name="Xi")

            Xi.zeros()
            # collect each vector's contribution
            for jVect in range(1, self.dim_q + 1):
                self._mapdl.vec("Qzj", "Z", "LINK", self.Qz.id, jVect)
                Qzj = self.mm.vec(name="Qzj")

                iY_a = self.iY.asarray()
                yrj = iY_a[jVect - 1].real  # real part of reduced solution
                yij = iY_a[jVect - 1].imag  # imaginary part of reduced solution
                self._mapdl.axpy(yrj, yij, Qzj.id, 1.0, 0.0, Xi.id)

            # Output solution vectors (if requested)
            if compute_solution_vectors:
                dof_each_freq = self._compute_solution_vector(Xi)
                xii_usr_ordered.append(dof_each_freq)

            # Compute residual norm (if requested)
            if residual_computation or residual_algorithm.lower() in [
                "no",
                "off",
            ]:
                norm_rz, norm_fz = self.compute_residuals(iFreq, RzV, Xi, omega)
                if not self.residuals:
                    self.residuals = []

                self.residuals.append([iFreq, norm_rz, norm_fz])

        # Storing solution in class
        if compute_solution_vectors:
            self.solution_vectors = np.array(
                xii_usr_ordered,
                dtype=[("node", "i4"), ("equ", "i4"), ("x", "c8")],
            )

        if return_solution:
            return self.solution_vectors

    def compute_residuals(self, iFreq, RzV, Xi, omega):
        """Compute residuals of the matrices"""
        # form {iRHS}
        self.iRHS.zeros()
        if self.ramped_load:
            # apply ramped loading
            ratio = 2 * iFreq / self.freq_steps
            if self.freq_steps == 1:
                ratio = 1.0
        else:
            # Apply stepped loading
            ratio = 1.0

        self.iRHS.axpy(self.fz0, ratio, 1.0)  # get {iRHS} at iFreq

        # Form az
        omega = omega + self.intV * 2 * np.pi  # defined frequency value
        ccf = -omega * omega

        self._mapdl.smat("az", "Z", "COPY", self._mat_k.id)  # modified K:[az]=[MatK]
        az = self.mm.mat(name="az")

        # [az]=(1,0)*[az]+(ccf,0)*[MatM]
        az.axpy(self._mat_m, ccf, 1.0)
        # [az]=(1,0)*[az]-(0,omega)*[mat_C]
        self._mapdl.axpy(0.0, omega, self._mat_c.id, 1.0, 0.0, az.id)

        # Compute {Rz}={iRHS}-[az]*{Xi}
        self._mapdl.vec("Rzi", "Z", "LINK", RzV.id, 1)
        Rzi = self.mm.vec(name="Rzi")

        Rzi.zeros()
        Rzi = az.dot(Xi)
        Rzi.axpy(self.iRHS, 1.0, -1.0)

        # Output norms of residual vector
        norm_rz = 0.0

        if self._residual_algorithm.lower() in ["l-inf", "linf"]:  # L-inf norm
            norm_rz = Rzi.norm("NRMINF")
            norm_fz = self.iRHS.norm("NRMINF")
            if norm_fz != 0.0:
                norm_rz = norm_rz / norm_fz

        elif self._residual_algorithm.lower() in ["l-1", "l1"]:
            norm_rz = Rzi.norm("NRM1")
            norm_fz = self.iRHS.norm("NRM1")
            if norm_fz != 0.0:
                norm_rz = norm_rz / norm_fz

        elif self._residual_algorithm.lower() in ["l-2", "l2"]:
            norm_rz = Rzi.norm("NRM2")
            norm_fz = self.iRHS.norm("NRM2")
            if norm_fz != 0.0:
                norm_rz = norm_rz / norm_fz
        else:
            raise ValueError(
                f"The provided algorithm '{self._residual_algorithm}' is not supported."
            )

        return norm_rz, norm_fz

    def _compute_solution_vector(self, Xi):
        self._mapdl.mult(
            m1=self.Nod2Solv.id, t1="TRANS", m2=Xi.id, t2="", m3="Xii"
        )  # Map {Xi} to internal (ANSYS) order
        Xii = self.mm.vec(name="Xii")
        dof_each_freq = []

        # Map {Xii} to user ordering
        num_eqn = Xii.size  # dim 1
        numdof = int(num_eqn / self._num_node)

        for extnode in range(1, self._max_node + 1):
            intNode = self._map_forward[extnode - 1]
            if intNode < 0:
                break
            intEqn = int((intNode - 1) * numdof)
            extEqn = int((extnode - 1) * numdof)

            for idof in range(1, numdof + 1):
                Xii_real = Xii.asarray()[intEqn + idof - 1].real  # Real value
                Xii_imag = Xii.asarray()[intEqn + idof - 1].imag  # Imag value

                dof_each_freq.append(
                    (int(extnode), int(extEqn + idof), Xii_real + Xii_imag * 1j)
                )
        return dof_each_freq
