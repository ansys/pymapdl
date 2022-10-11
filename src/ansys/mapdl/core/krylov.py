import os
import weakref

import numpy as np

from .mapdl_grpc import MapdlGrpc


class KrylovSolver:
    """Abstract mapdl krylov class.  Created from a ``Mapdl`` instance.

    Examples
    --------
    Create an instance.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> ....
    >>> ....
    >>> Generate the FEA model (mesh, constraints, loads, etc.)
    >>> Generate the .full file

    >>> mk = mapdl.krylov

    Generate Krylov subspace

    >>> Qz = mk.krygensub(10, 500, True, True)

    Reduces system of equations and solve at each frequency

    >>> Yz = mk.krysolve(0, 1000, 100, 0, True)

    Expand reduced solution back to FE space

    >>> res = mk.kryexpand(True, 3)

    """

    def __init__(self, mapdl):
        if not isinstance(mapdl, MapdlGrpc):
            raise TypeError("``mapdl`` must be a MapdlGrpc instance")
        self._mapdl_weakref = weakref.ref(mapdl)
        self.mm = self._mapdl.math
        self.jobname = self._mapdl.jobname
        self.logger = self._mapdl._log

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl."""
        return self._mapdl_weakref()

    def _check_input_krygensub(
        self, max_dim_q, freq_val, chk_ortho_key, out_key, full_file
    ):
        """Validates the inputs to krygensub method."""

        current_dir = self._mapdl.directory
        # Check if full file exists
        if not full_file:
            self.full_file = self._mapdl.jobname + ".full"

        # Checking if the full file exists.
        if self._mapdl._local:
            if not os.path.exists(os.path.join(current_dir, self.full_file)):
                raise FileNotFoundError(
                    f"The file {self.full_file} could not be found in local directory '{current_dir}'."
                )
        else:
            if self.full_file not in self._mapdl.list_files():
                raise FileNotFoundError(
                    f"The file {self.full_file} could not be found in remote MAPDL instance."
                )

        # Check for illegal input values by the user
        if not isinstance(max_dim_q, int) or max_dim_q <= 0:
            raise ValueError(
                "The maximum size of Krylov subspace is required to be greater than 0"
            )
        if not isinstance(freq_val, int) or freq_val < 0:
            raise ValueError(
                "The frequency value for building the Krylov subspace is required to be greater or equal to 0 Hz"
            )
        if not isinstance(chk_ortho_key, bool):
            raise ValueError(
                "The chk_ortho_key value for building the Krylov subspace is required to be Boolean True or False"
            )
        if not isinstance(out_key, bool):
            raise ValueError(
                "The out_key value for building the Krylov subspace is required to be to be Boolean True or False"
            )

    def _check_input_krysolve(self, freq_start, freq_end, num_freq, load_key, out_key):
        """Validates the inputs to krysolve method."""

        if not isinstance(freq_start, int) or freq_start < 0:
            raise ValueError(
                "The beginning frequency value for solving the reduced solution is required to be greater than or equal to 0"
            )
        if not isinstance(num_freq, int) or num_freq <= 0:
            raise ValueError(
                "The number of frequencies for which to compute the reduced solution is required to be greater than 0"
            )
        if not isinstance(load_key, int) or load_key < 0 or load_key > 1:
            raise ValueError(
                "The Load key value for computing the reduced solution is required to be 0 or 1"
            )
        if not isinstance(out_key, bool):
            raise ValueError(
                "The out_key value for computing the reduced solution is required to be Boolean True or False"
            )

    def _check_input_kryexpand(self, out_key, res_key):
        """Validates the inputs to kryexpand method."""

        if not isinstance(out_key, bool):
            raise ValueError(
                "The out_key value for expanding the reduced solution is required to be Boolean True or False"
            )
        if not isinstance(res_key, int) or res_key < 0 or res_key > 3:
            raise ValueError(
                "The res_key value for expanding the reduced solution is required to be 0 -> 3"
            )

    def _get_data_from_full_file(self):
        """Extracts Stiffness, Mass, Damping and force matrices from full file"""

        self._mat_k = self.mm.stiff(fname=self.full_file)
        self._ndof = self._mat_k.shape[1]
        self._mat_m = self.mm.mass(fname=self.full_file)
        self._mat_c = self.mm.damp(fname=self.full_file)

        self._mapdl.smat("Nod2Solv", "D", "IMPORT", "FULL", self.full_file, "NOD2SOLV")
        self.Nod2Solv = self.mm.mat(name="Nod2Solv")

        self._mapdl.vec("fz", "Z", "IMPORT", "FULL", self.full_file, "RHS")
        self._mapdl.vec("fz0", "Z", "COPY", "fz")
        self.fz0 = self.mm.vec(name="fz0")

    def _chk_ortho_vec(self, orth_file, uz, num_q):
        """Check Orthonormality of vectors"""

        f = open(orth_file, "w")
        for i in range(1, num_q + 1):
            self._mapdl.vec("Vz", "Z", "LINK", self.Qz.id, i)
            Vz = self.mm.vec(name="Vz")
            Vz_m = Vz.asarray()
            for j in range(1, num_q + 1):
                self._mapdl.vec(uz.id, "Z", "LINK", self.Qz.id, j)
                uz_m = uz.asarray()
                rcon = np.vdot(Vz_m, uz_m)
                rcon_real = rcon.real
                rcon_imag = rcon.imag
                dcon = np.sqrt(rcon_real * rcon_real + rcon_imag * rcon_imag)
                f.write(f"V_{i}\tV_{j}\t{dcon}\n")
        f.close()

    def krygensub(
        self, max_dim_q, freq_val, chk_ortho_key=False, out_key=False, full_file=None
    ):
        """Generates a Krylov subspace for model reduction in harmonic analysis

        This method generates a Krylov subspace used for a model reduction
        solution in a harmonic analysis. The subspace is built using the
        assembled matrices and load vector on the jobname.full file that
        is located in the current working directory.  This .full file
        should be built at the specified frequency value.

        Parameters
        ----------
        max_dim_q     : int
                        Maximum size/dimension of Krylov subspace
        freq_val      : int
                        Frequency value (Hz) at which to build the KRYLOV subspace
        chk_ortho_key : Bool, optional
                        key to check orthonormal properties of each subspace vector
                        with all other subspace vectors [Default:False]
        out_key       : Bool, optional
                        Key to output KRYLOV subspace to Qz.txt file [Default:False]
        full_file     : str, optional
                        Specify .full file name to read specific full file,
                        By default jobname.full is read.

        Returns
        -------
        AnsMat
            Krylov subspace.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """

        current_dir = self._mapdl.directory
        self.logger.debug(f"Current directory: {current_dir}")

        two_pi = 2.0 * np.pi
        omega_zero = freq_val * two_pi
        ccf = -(omega_zero**2)
        init_val = 2  # Initialized as no damping
        zero_c = 0

        # Check the Inputs
        self._check_input_krygensub(
            max_dim_q, freq_val, chk_ortho_key, out_key, full_file
        )
        # Get matrices from full file
        self._get_data_from_full_file()
        # Get the force vector from the defined Ansvec
        fz = self.mm.vec(name="fz")

        # Create Subspace
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
        if chk_ortho_key:
            orth_file = os.path.join(f"{self.jobname}_ortho.txt")
            self._chk_ortho_vec(orth_file, uz, num_q)

        # Output generated subspace vectors to file
        if out_key:
            self._mapdl.run(f"*PRINT, {self.Qz.id}, {self.jobname}_Qz.txt")

        return self.Qz

    def krysolve(self, freq_start, freq_end, num_freq, load_key, out_key=False):
        """Reduces system of equations and solve at each frequency

        This method uses a KRYLOV subspace to solve a reduced harmonic
        analysis over a specified frequency range for a given number of
        frequency points (intervals).

        Parameters
        ----------
        freq_start : int
                    Starting value of the frequency range (Hz)
        freq_end   : int
                    Ending value of the frequency range (Hz)
        num_freq   : int
                    User specified number of intervals in frequency range
        load_key   : int
                    Key specifying whether load should be ramped(0) or stepped(1)
        out_key    : Bool, optional
                    Key to output reduced solution to Yz.txt file [Default:False]

        Returns
        -------
        AnsMat
            Reduced solution over Frequency range.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS."""

        # Check inputs before executing the method
        self._check_input_krysolve(freq_start, freq_end, num_freq, load_key, out_key)

        # Store input arguments from user
        self.freq_start = freq_start
        self.num_freq = num_freq
        self.load_key = load_key

        # Execute macro if no errors above
        az = self.mm.mat(name="az")
        ndof = self._ndof
        dim_q = self.dim_q

        # Define solution variables
        QtF = self.mm.zeros(dim_q, dtype=np.cdouble)
        QtAQ = self.mm.zeros(dim_q, dim_q, dtype=np.cdouble)  # [QtAQ], reduced matrix
        self.Yz = self.mm.zeros(
            dim_q, self.num_freq, dtype=np.cdouble
        )  # [Yz], reduced solution over range
        self.DzV = self.mm.zeros(
            ndof, self.num_freq, dtype=np.cdouble
        )  # {DzV}, displacement vector
        self.iRHS = self.mm.zeros(ndof, dtype=np.cdouble)

        # Loop over frequency range
        omega = self.freq_start * 2 * np.pi
        self.intV = (freq_end - self.freq_start) / self.num_freq

        for iFreq in range(1, self.num_freq + 1):
            # form RHS at the i-th frequency point
            self.iRHS.zeros()
            if self.load_key == 0:
                # apply ramped loading
                ratio = 2 * iFreq / self.num_freq
                if self.num_freq == 1:
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

            # Output reduced solution (if requested)
            if out_key:
                # Yz_*.txt, reduced solution vector
                self._mapdl.run(f"*PRINT, {self.iY.id}, {self.jobname}_Yz_{iFreq}.txt")
        return self.Yz

    def kryexpand(self, out_key=False, res_key=0):
        """Expand reduced solution back to FE space

        This method expands the reduced solution for a harmonic analysis
        back to the original space.  Optional calculation of the residual
        is available.

        Parameters
        ----------
        out_key  : Bool
                   Key to output expanded solution to Xz_*.txt file [Default:False]
        res_key  : int, optional
                Key to compute the residual of the expanded solution
                = 0 means do not compute the residual [Default]
                = 1 means compute the L-inf norm of the residual
                = 2 means compute the L-1 norm of the residual
                = 3 means compute the L-2 norm of the residual

        Returns
        -------
        Ndarray
            Solution vectors mapped to User order. (if out_key = True)
        None
            (if out_key = False)

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS."""

        # Check inputs before executing the method
        self._check_input_kryexpand(out_key, res_key)

        RzV = self.mm.zeros(self._ndof, 1, dtype=np.cdouble)

        # Build mapping vectors
        self._mapdl.vec("MapForward", "I", "IMPORT", "FULL", self.full_file, "FORWARD")
        map_forward = self.mm.vec(name="MapForward")

        self._mapdl.vec("MapBack", "I", "IMPORT", "FULL", self.full_file, "BACK")
        map_back = self.mm.vec(name="MapBack")

        max_node = map_forward.size
        num_node = map_back.size

        # Expand reduced solution
        omega = self.freq_start * 2 * np.pi  # circular frequency at starting point
        xii_usr_ordered = []

        for iFreq in range(1, self.num_freq + 1):
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
            if out_key:
                self._mapdl.mult(
                    m1=self.Nod2Solv.id, t1="TRANS", m2=Xi.id, t2="", m3="Xii"
                )  # Map {Xi} to internal (ANSYS) order
                Xii = self.mm.vec(name="Xii")
                dof_each_freq = []

                # Map {Xii} to user ordering
                num_eqn = Xii.size  # dim 1
                numdof = int(num_eqn / num_node)

                file = open(
                    os.path.join(
                        self._mapdl.directory,
                        f"{self.jobname}_Xzu_{iFreq}.txt",
                    ),
                    "w",
                )
                for extnode in range(1, max_node + 1):
                    intNode = map_forward[extnode - 1]
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

                        file.write(
                            f"Node#={extnode:9d}, Eqn#={extEqn + idof:9d}, X={Xii_real:.16E}  {Xii_imag:.16E}\n"
                        )
                file.close()
                xii_usr_ordered.append(dof_each_freq)

                self._mapdl.run(f"*PRINT, {Xi.id}, {self.jobname}_Xz_{iFreq}.txt")
                self._mapdl.run(f"*PRINT, {Xii.id}, {self.jobname}_Xzi_{iFreq}.txt")

            # Compute residual norm (if requested)
            if res_key > 0:
                # form {iRHS}
                self.iRHS.zeros()
                if self.load_key == 0:
                    # apply ramped loading
                    ratio = 2 * iFreq / self.num_freq
                    if self.num_freq == 1:
                        ratio = 1.0
                else:
                    # Apply stepped loading
                    ratio = 1.0

                self.iRHS.axpy(self.fz0, ratio, 1.0)  # get {iRHS} at iFreq

                # Form az
                omega = omega + self.intV * 2 * np.pi  # defined frequency value
                ccf = -omega * omega

                self._mapdl.smat(
                    "az", "Z", "COPY", self._mat_k.id
                )  # modified K:[az]=[MatK]
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
                file1 = open(
                    os.path.join(
                        self._mapdl.directory,
                        f"{self.jobname}_Rzi_{iFreq}.txt",
                    ),
                    "w",
                )
                norm_rz = 0.0

                if res_key == 1:  # L-inf norm
                    title = "Inf"
                    norm_rz = Rzi.norm("NRMINF")
                    norm_fz = self.iRHS.norm("NRMINF")
                    if norm_fz != 0.0:
                        norm_rz = norm_rz / norm_fz

                elif res_key == 2:
                    title = "L-1"
                    norm_rz = Rzi.norm("NRM1")
                    norm_fz = self.iRHS.norm("NRM1")
                    if norm_fz != 0.0:
                        norm_rz = norm_rz / norm_fz

                elif res_key == 3:
                    title = "L-2"
                    norm_rz = Rzi.norm("NRM2")
                    norm_fz = self.iRHS.norm("NRM2")
                    if norm_fz != 0.0:
                        norm_rz = norm_rz / norm_fz

                file1.write(
                    f"Calculated {title:3s} Residual Norm: |R|={norm_rz:.16E} |F|={norm_fz:.16E} at subst={iFreq:9d}\n"
                )

                num_eqn = Rzi.size
                Rzi_np = Rzi.asarray()
                for iEQ in range(1, num_eqn + 1):
                    Rzi_real = Rzi_np[iEQ - 1].real  # real value of residual
                    Rzi_imag = Rzi_np[iEQ - 1].imag  # imaginary value of residual

                    file1.write(f"iEQN={iEQ:9d}, Rz={Rzi_real:.16E}  {Rzi_imag:.16E}\n")

                file1.close()
        if out_key:
            xii_usr_ordered = np.array(
                xii_usr_ordered, dtype=[("node", "i4"), ("equ", "i4"), ("x", "c8")]
            )
            return xii_usr_ordered

    # Clear all Local_Varaibles
    # self._mapdl.clear()
