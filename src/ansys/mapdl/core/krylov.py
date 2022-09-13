import os
import weakref

import numpy as np

from .mapdl_grpc import MapdlGrpc


class Krylov_functions:
    def __init__(self, mapdl):
        if not isinstance(mapdl, MapdlGrpc):
            raise TypeError("``mapdl`` must be a MapdlGrpc instance")
        self._mapdl_weakref = weakref.ref(mapdl)
        self.mm = self._mapdl.math
        self.jobname = self._mapdl.jobname

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl."""
        return self._mapdl_weakref()

    def krygensub(self, arg1, arg2, arg3=0, arg4=0):  # Generate the Krylov subspace
        """This method generates a Krylov subspace used for a model reduction
        solution in a harmonic analysis. The subspace is built using the
        assembled matrices and load vector on the jobname.full file that
        is located in the current working directory.  This .full file
        should be built at the specified frequency value.

        Parameters
        ----------
        maxDimQ     - maximum size/dimension of Krylov subspace
        freqVal     - frequency value (Hz) at which to build the KRYLOV subspace
        chkOrthoKey - [optional] key to check orthonormal properties of
        each subspace vector with all other subspace vectors
        outKey      - [optional] key to output KRYLOV subspace to Qz.txt file

        Returns
        -------
        AnsMat
            Krylov subspace.
        """

        current_dir = self._mapdl.directory
        print(current_dir)
        self.full_file = self._mapdl.jobname + ".full"

        # Store the input arguments from the user
        maxDimQ = arg1
        freqVal = arg2
        chkOrthoKey = arg3
        outKey = arg4

        # Check for illegal input values by the user
        _nerr = 0
        if maxDimQ <= 0:
            print(
                "The maximum size of Krylov subspace is required to be greater than 0"
            )
            _nerr = 1
        elif freqVal < 0:
            print(
                "The frequency value for building the Krylov subspace is required to be greater or equal to 0 Hz"
            )
            _nerr = 1
        elif chkOrthoKey < 0 or chkOrthoKey > 1:
            print(
                "The chkOrthoKey value for building the Krylov subspace is required to be 0 or 1"
            )
            _nerr = 1
        elif outKey < 0 or outKey > 1:
            print(
                "The outKey value for building the Krylov subspace is required to be 0 or 1"
            )
            _nerr = 1

        # Execute macro if no errors
        if _nerr == 0:
            twoPi = 2.0 * np.pi
            omega0 = freqVal * twoPi
            ccf = -(omega0**2)

            self.matk = self.mm.stiff(fname=self.full_file)
            self.nDOF = self.matk.shape[1]
            self.matm = self.mm.mass(fname=self.full_file)
            self.mat_C = self.mm.damp(fname=self.full_file)

            self._mapdl.smat(
                "Nod2Solv", "D", "IMPORT", "FULL", self.full_file, "NOD2SOLV"
            )
            self.Nod2Solv = self.mm.mat(name="Nod2Solv")

            self._mapdl.vec("Fz", "Z", "IMPORT", "FULL", self.full_file, "RHS")
            Fz = self.mm.vec(name="Fz")

            self._mapdl.vec("Fz0", "Z", "COPY", "Fz")
            self.Fz0 = self.mm.vec(name="Fz0")

            # Form Az = (K-w0*w0*M,i*w0*C)
            self._mapdl.smat(matrix="Az", type_="Z", method="COPY", val1=self.matk.id)
            Az = self.mm.mat(name="Az")

            Az.axpy(self.matm, ccf, 1.0)
            self._mapdl.axpy(
                vr=0.0, vi=omega0, m1=self.mat_C.id, wr=1.0, wi=0.0, m2=Az.id
            )

            # Form Cz=(C+i*2*w0*M)
            self._mapdl.smat(matrix="Cz", type_="Z", method="COPY", val1=self.mat_C.id)
            Cz = self.mm.mat(name="Cz")
            self._mapdl.axpy(
                vr=0.0, vi=2 * omega0, m1=self.matm.id, wr=1.0, wi=0.0, m2=Cz.id
            )

            zeroC = 0
            normC = float(
                self._mapdl.nrm(
                    name=Cz.id, normtype="NRM2", parr="normC", normalize="NO"
                ).split()[-1]
            )
            if normC == 0:
                zeroC = 1

            # Solve for the 1st vector of subspace[Q]
            # Create solver system of [Az]
            s = self.mm.factorize(Az)  # Factor [Az]

            # [Qz] initially allocated
            self.Qz = self.mm.zeros(self.nDOF, maxDimQ, dtype=np.cdouble)

            # {Uz1} linked to Qz[1]
            self._mapdl.vec(
                vector="Uz1", type_="Z", method="LINK", val1=self.Qz.id, val2=1
            )
            Uz1 = self.mm.vec(name="Uz1")

            Uz1 = s.solve(Fz, Uz1)
            normU = float(
                self._mapdl.nrm(
                    name=Uz1.id, normtype="NRM2", parr="normU", normalize="YES"
                ).split()[-1]
            )

            i1 = 2  # Initialized as no damping
            if zeroC == 0:
                i1 = 3
                self._mapdl.vec(
                    vector="Uz2", type_="Z", method="LINK", val1=self.Qz.id, val2=2
                )
                Uz2 = self.mm.vec(name="Uz2")
                Fz.zeros()  # {Fz}=0

                # {Fz}={Fz}+[Cz]{Uz1}
                Fz = Cz.dot(Uz1)
                Fz *= -1  # {Fz}=-{Fz}
                normU = float(
                    self._mapdl.nrm(
                        name=Fz.id, normtype="NRM2", parr="normU", normalize="YES"
                    ).split()[-1]
                )

                Uz2 = s.solve(Fz, Uz2)  # back solved:{Uz2}=[Az]^-1*{Fz}

                # {Uz2}*{v1} = ccon
                self._mapdl.dot(
                    vector1=Uz1.id,
                    vector2=Uz2.id,
                    par_real="ccon_real",
                    par_imag="ccon_imag",
                )
                # {Uz2}={Uz2}-ccon*{Uz1}
                self._mapdl.axpy(
                    vr="-ccon_real",
                    vi="-ccon_imag",
                    m1=Uz1.id,
                    wr=1.0,
                    wi=0.0,
                    m2=Uz2.id,
                )

                # {Uz2} normalized
                normU = float(
                    self._mapdl.nrm(
                        name=Uz2.id, normtype="NRM2", parr="normU", normalize="YES"
                    ).split()[-1]
                )

            # Build Subspace Vectors with MGS (2nd Order)
            for dimQ in range(i1, maxDimQ + 1):
                self.dimQ = dimQ
                if normU == 0:
                    numQ = dimQ - 1  # exhausted at dimQ
                else:
                    numQ = maxDimQ  # may reach to the maximum

                if numQ >= maxDimQ:  # make next vector)
                    Fz.zeros()
                    if zeroC == 0:  # [Cz]!=0 case
                        nextUzOne = dimQ - 2
                        nextUzTwo = dimQ - 1
                        # {Uz1} to [Qz](dimQ-2)
                        self._mapdl.vec(
                            vector=Uz1.id,
                            type_="Z",
                            method="LINK",
                            val1=self.Qz.id,
                            val2=nextUzOne,
                        )
                        # {Uz2} to [Qz](dimQ-1)
                        self._mapdl.vec(
                            vector=Uz2.id,
                            type_="Z",
                            method="LINK",
                            val1=self.Qz.id,
                            val2=nextUzTwo,
                        )
                        self._mapdl.vec(
                            vector="Uz",
                            type_="Z",
                            method="LINK",
                            val1=self.Qz.id,
                            val2=dimQ,
                        )  # {Uz} to [Qz](dimQ)
                        Uz = self.mm.vec(name="Uz")
                        # [Cz]{Uz2} -> {Uz}
                        Uz += Cz.dot(Uz2)

                    else:  # [Cz]=0 case
                        nextUzOne = dimQ - 1
                        self._mapdl.vec(
                            vector=Uz1.id,
                            type_="Z",
                            method="LINK",
                            val1=self.Qz.id,
                            val2=nextUzOne,
                        )
                        # {Uz} to [Qz](dimQ)
                        self._mapdl.vec(
                            vector=Uz2.id,
                            type_="Z",
                            method="LINK",
                            val1=self.Qz.id,
                            val2=dimQ,
                        )
                        Uz.zeros()

                    # [MatM]{Uz1} -> {Fz}
                    self._mapdl.mult(m1=self.matm.id, t1="", m2=Uz1.id, t2="", m3=Fz.id)
                    Fz.axpy(Uz, -1.0, -1.0)  # {Fz} = -{Fz}-{Uz}
                    Uz = s.solve(Fz, Uz)  # [Az]^-1{Fz} -> {Uz}

                    # Make subspace vectors orthonormal
                    for j in range(1, dimQ):
                        self._mapdl.vec(
                            vector="V1",
                            type_="Z",
                            method="LINK",
                            val1=self.Qz.id,
                            val2=j,
                        )
                        V1 = self.mm.vec(name="V1")
                        self._mapdl.dot(
                            vector1=V1.id,
                            vector2=Uz.id,
                            par_real="ccon_real",
                            par_imag="ccon_imag",
                        )
                        self._mapdl.axpy(
                            vr="-ccon_real",
                            vi="-ccon_imag",
                            m1=V1.id,
                            wr=1.0,
                            wi=0.0,
                            m2=Uz.id,
                        )

                    normU = float(
                        self._mapdl.nrm(
                            name=Uz.id, normtype="NRM2", parr="normU", normalize="YES"
                        ).split()[-1]
                    )

            # Optional check on Orthonormality of vectors
            if chkOrthoKey == 1:
                orth_file = os.path.join(
                    self._mapdl.directory, "{}_ortho.txt".format(self.jobname)
                )
                f = open(orth_file, "w")
                for i in range(1, numQ + 1):
                    self._mapdl.vec(
                        vector="Vz", type_="Z", method="LINK", val1=self.Qz.id, val2=i
                    )
                    Vz = self.mm.vec(name="Vz")
                    Vz_m = Vz.asarray()
                    for j in range(1, numQ + 1):
                        self._mapdl.vec(
                            vector=Uz.id,
                            type_="Z",
                            method="LINK",
                            val1=self.Qz.id,
                            val2=j,
                        )
                        Uz_m = Uz.asarray()
                        rcon = np.vdot(Vz_m, Uz_m)
                        rcon_real = rcon.real
                        rcon_imag = rcon.imag
                        dcon = np.sqrt(rcon_real * rcon_real + rcon_imag * rcon_imag)
                        f.write(f"V_{i}\tV_{j}\t{dcon}\n")
                f.close()

            # Output generated subspace vectors to file
            if outKey == 1:
                self._mapdl.run(
                    "*PRINT, {}, {}_Qz.txt".format(self.Qz.id, self.jobname)
                )

            return self.Qz

    def krysolve(self, arg1, arg2, arg3, arg4, arg5=0):
        """This method uses a KRYLOV subspace to solve a reduced harmonic
        analysis over a specified frequency range for a given number of
        frequency points (intervals).

        Parameters
        ----------
        freqBeg - starting value of the frequency range (Hz)
        freqEnd - ending value of the frequency range (Hz)
        numFreq - user specified number of intervals in frequency range
        loadKey - key specifying whether load should be ramped(0) or stepped(1)
        outKey  - [optional] key to output reduced solution to Yz.txt file"""

        # Store input arguments from user
        self.freqBeg = arg1
        self.freqEnd = arg2
        self.numFreq = arg3
        self.loadKey = arg4
        outKey = arg5

        # Check for illegal input values by the user
        _nerr = 0
        if self.freqBeg < 0:
            print(
                "The beginning frequency value for solving the reduced solution is required to be greater than or equal to 0"
            )
            _nerr = 1
        elif self.numFreq <= 0:
            print(
                "The number of frequencies for which to compute the reduced solution is required to be greater than 0"
            )
            _nerr = 1
        elif self.loadKey < 0 or self.loadKey > 1:
            print(
                "The loadKey value for computing the reduced solution is required to be 0 or 1"
            )
            _nerr = 1
        elif outKey < 0 or outKey > 1:
            print(
                "The outKey value for computing the reduced soluion is required to be 0 or 1"
            )
            _nerr = 1

        if _nerr == 0:  # Execute macro if no errors above
            Az = self.mm.mat(name="Az")
            nDOF = self.nDOF
            dimQ = self.dimQ

            # Define solution variables
            QtF = self.mm.zeros(dimQ, dtype=np.cdouble)
            QtAQ = self.mm.zeros(dimQ, dimQ, dtype=np.cdouble)  # [QtAQ], reduced matrix
            self.Yz = self.mm.zeros(
                dimQ, self.numFreq, dtype=np.cdouble
            )  # [Yz], reduced solution over range
            QtA = self.mm.zeros(nDOF, dimQ, dtype=np.cdouble)  # [QtA]
            self.DzV = self.mm.zeros(
                nDOF, self.numFreq, dtype=np.cdouble
            )  # {DzV}, displacement vector
            self.iRHS = self.mm.zeros(nDOF, dtype=np.cdouble)

            # Loop over frequency range
            omega = self.freqBeg * 2 * np.pi
            self.intV = (self.freqEnd - self.freqBeg) / self.numFreq

            for iFreq in range(1, self.numFreq + 1):
                # form RHS at the i-th frequency point
                self.iRHS.zeros()
                if self.loadKey == 0:
                    # apply ramped loading
                    ratio = 2 * iFreq / self.numFreq
                    if self.numFreq == 1:
                        ratio = 1.00
                else:
                    # Apply stepped loading
                    ratio = 1.00

                self.iRHS.axpy(self.Fz0, ratio, 1.0)  # Get {iRHS} at iFreq
                QtF = self.Qz.T.dot(self.iRHS)  # Reduce [Qz]^t{iRHS} -> {QtF}

                # link iY to Yz(iFreq)
                self._mapdl.vec(
                    "iY", type_="Z", method="LINK", val1=self.Yz.id, val2=iFreq
                )
                self.iY = self.mm.vec(name="iY")

                # Reduced system at omega
                omega = omega + self.intV * 2 * np.pi  # defined frequency value
                ccf = -omega * omega

                # modified K:[Az]=[MatK]
                self._mapdl.smat(
                    matrix="Az", type_="Z", method="COPY", val1=self.matk.id
                )
                Az = self.mm.mat(name="Az")

                # [Az]=(1,0)*[Az]+(ccf,0)*[MatM]
                Az.axpy(self.matm, ccf, 1.0)
                # [Az]=(1,0)*[Az]-(0,omega)*[mat_C]
                self._mapdl.axpy(
                    vr=0.0, vi=omega, m1=self.mat_C.id, wr=1.0, wi=0.0, m2=Az.id
                )

                AQ = Az.dot(self.Qz)  # [AQ]=[Az][Qz]
                QtAQ = self.Qz.T.dot(AQ)  # [QtAQ]=[Q^t][AQ]

                # create reduced system of equations
                s = self.mm.factorize(QtAQ)
                # back solve for {iY}=Yz[iFreq]
                self.iY = s.solve(QtF, self.iY)

                # Output reduced solution (if requested)
                if outKey == 1:
                    # Yz_*.txt, reduced solution vector
                    self._mapdl.run(
                        "*PRINT, {}, {}_Yz_{}.txt".format(
                            self.iY.id, self.jobname, iFreq
                        )
                    )
                    return self.Yz

    def kryexpand(self, arg1=0, arg2=0):
        """This method expands the reduced solution for a harmonic analysis
            back to the original space.  Optional calculation of the residual
            is available.

        Parameters
        ----------
            outKey  - [optional] key to output expanded solution to Xz_*.txt file
            resKey  - [optional] key to compute the residual of the expanded
            solution
                = 0 means do not compute the residual
                = 1 means compute the L-inf norm of the residual
                = 2 means compute the L-1 norm of the residual
                = 3 means compute the L-2 norm of the residual"""

        # Store input arguments from user
        outKey = arg1
        resKey = arg2

        # Check for illegal input values by user
        _nerr = 0
        if outKey < 0 or outKey > 1:
            print(
                "The outKey value for expanding the reduced solution is required to be 0 or 1"
            )
            _nerr = 1
        elif resKey < 0 or resKey > 3:
            print(
                "The resKey value for expanding the reduced soluion is required to be 0 -> 3"
            )
            _nerr = 1

        if _nerr == 0:
            RzV = self.mm.zeros(self.nDOF, 1, dtype=np.cdouble)

            # Build mapping vectors
            self._mapdl.vec(
                "MapForward", "I", "IMPORT", "FULL", self.full_file, "FORWARD"
            )
            MapForward = self.mm.vec(name="MapForward")

            self._mapdl.vec("MapBack", "I", "IMPORT", "FULL", self.full_file, "BACK")
            MapBack = self.mm.vec(name="MapBack")

            maxnode = MapForward.size
            numnode = MapBack.size

            # Expand reduced solution
            omega = self.freqBeg * 2 * np.pi  # circular frequency at starting point

            for iFreq in range(1, self.numFreq + 1):
                self._mapdl.vec(
                    self.iY.id, type_="Z", method="LINK", val1=self.Yz.id, val2=iFreq
                )
                self._mapdl.vec(
                    "Xi", type_="Z", method="LINK", val1=self.DzV.id, val2=iFreq
                )  # vector of solution in solver space
                Xi = self.mm.vec(name="Xi")

                Xi.zeros()
                for jVect in range(
                    1, self.dimQ + 1
                ):  # collect each vector's contribution
                    self._mapdl.vec(
                        "Qzj", type_="Z", method="LINK", val1=self.Qz.id, val2=jVect
                    )
                    Qzj = self.mm.vec(name="Qzj")

                    iY_a = self.iY.asarray()
                    yrj = iY_a[jVect - 1].real  # real part of reduced solution
                    yij = iY_a[jVect - 1].imag  # imaginary part of reduced solution
                    self._mapdl.axpy(
                        vr=yrj, vi=yij, m1=Qzj.id, wr=1.0, wi=0.0, m2=Xi.id
                    )

                # Output solution vectors (if requested)
                if outKey == 1:
                    self._mapdl.mult(
                        m1=self.Nod2Solv.id, t1="TRANS", m2=Xi.id, t2="", m3="Xii"
                    )  # Map {Xi} to internal (ANSYS) order
                    Xii = self.mm.vec(name="Xii")

                    # Map {Xii} to user ordering
                    numeqn = Xii.size  # dim 1
                    numdof = int(numeqn / numnode)

                    file = open(
                        os.path.join(
                            self._mapdl.directory,
                            "{}_Xzu_{}.txt".format(self.jobname, iFreq),
                        ),
                        "w",
                    )
                    for extnode in range(1, maxnode + 1):
                        intNode = MapForward[extnode - 1]
                        if intNode < 0:
                            break
                        intEqn = int((intNode - 1) * numdof)
                        extEqn = int((extnode - 1) * numdof)

                        for idof in range(1, numdof + 1):
                            # print(Xii)
                            Xii_real = Xii.asarray()[
                                intEqn + idof - 1
                            ].real  # Real value
                            Xii_imag = Xii.asarray()[
                                intEqn + idof - 1
                            ].imag  # Imag value

                            file.write(
                                "Node#={:9d}, Eqn#={:9d}, X={:.16E}  {:.16E}\n".format(
                                    extnode, extEqn + idof, Xii_real, Xii_imag
                                )
                            )
                    file.close()

                    self._mapdl.run(
                        "*PRINT, {}, {}_Xz_{}.txt".format(Xi.id, self.jobname, iFreq)
                    )
                    self._mapdl.run(
                        "*PRINT, {}, {}_Xzi_{}.txt".format(Xii.id, self.jobname, iFreq)
                    )

                # Compute residual norm (if requested)
                if resKey > 0:
                    # form {iRHS}
                    self.iRHS.zeros()
                    if self.loadKey == 0:
                        # apply ramped loading
                        ratio = 2 * iFreq / self.numFreq
                        if self.numFreq == 1:
                            ratio = 1.0
                    else:
                        # Apply stepped loading
                        ratio = 1.0

                    self.iRHS.axpy(self.Fz0, ratio, 1.0)  # get {iRHS} at iFreq

                    # Form Az
                    omega = omega + self.intV * 2 * np.pi  # defined frequency value
                    ccf = -omega * omega

                    self._mapdl.smat(
                        matrix="Az", type_="Z", method="COPY", val1=self.matk.id
                    )  # modified K:[Az]=[MatK]
                    Az = self.mm.mat(name="Az")

                    # [Az]=(1,0)*[Az]+(ccf,0)*[MatM]
                    Az.axpy(self.matm, ccf, 1.0)
                    # [Az]=(1,0)*[Az]-(0,omega)*[mat_C]
                    self._mapdl.axpy(
                        vr=0.0, vi=omega, m1=self.mat_C.id, wr=1.0, wi=0.0, m2=Az.id
                    )

                    # Compute {Rz}={iRHS}-[Az]*{Xi}
                    self._mapdl.vec(
                        "Rzi", type_="Z", method="LINK", val1=RzV.id, val2=1
                    )
                    Rzi = self.mm.vec(name="Rzi")

                    Rzi.zeros()
                    Rzi = Az.dot(Xi)
                    Rzi.axpy(self.iRHS, 1.0, -1.0)

                    # Output norms of residual vector
                    file1 = open(
                        os.path.join(
                            self._mapdl.directory,
                            "{}_Rzi_{}.txt".format(self.jobname, iFreq),
                        ),
                        "w",
                    )
                    normRz = 0.0

                    if resKey == 1:  # L-inf norm
                        title = "Inf"
                        normRz = Rzi.norm("NRMINF")
                        normFz = self.iRHS.norm("NRMINF")
                        if normFz != 0.0:
                            normRz = normRz / normFz

                    elif resKey == 2:
                        title = "L-1"
                        normRz = Rzi.norm("NRM1")
                        normFz = self.iRHS.norm("NRM1")
                        if normFz != 0.0:
                            normRz = normRz / normFz

                    elif resKey == 3:
                        title = "L-2"
                        normRz = Rzi.norm("NRM2")
                        normFz = self.iRHS.norm("NRM2")
                        if normFz != 0.0:
                            normRz = normRz / normFz

                    file1.write(
                        "Calculated {:3s} Residual Norm: |R|={:.16E} |F|={:.16E} at subst={:9d}\n".format(
                            title, normRz, normFz, iFreq
                        )
                    )

                    numeqn = Rzi.size
                    Rzi_np = Rzi.asarray()
                    for iEQ in range(1, numeqn + 1):
                        Rzi_real = Rzi_np[iEQ - 1].real  # real value of residual
                        Rzi_imag = Rzi_np[iEQ - 1].imag  # imaginary value of residual

                        file1.write(
                            "iEQN={:9d}, Rz={:.16E}  {:.16E}\n".format(
                                iEQ, Rzi_real, Rzi_imag
                            )
                        )

                    file1.close()

        # Clear all Local_Varaibles
        # self._mapdl.clear()
