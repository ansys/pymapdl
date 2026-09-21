# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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


"""The parameter commands MAPDL extended mixin."""

from functools import wraps  # noqa: F401
import os  # noqa: F401
import pathlib  # noqa: F401
import re  # noqa: F401
import shutil  # noqa: F401
import tempfile  # noqa: F401
from typing import Union  # noqa: F401
import warnings  # noqa: F401
import weakref  # noqa: F401

import numpy as np  # noqa: F401
from numpy.typing import DTypeLike, NDArray  # noqa: F401

from ansys.mapdl.core import LOG as logger  # noqa: F401
from ansys.mapdl.core import parse  # noqa: F401
from ansys.mapdl.core.commands import CommandListingOutput, CommandOutput  # noqa: F401
from ansys.mapdl.core.errors import (  # noqa: F401
    CommandDeprecated,
    ComponentDoesNotExits,
    IncorrectWorkingDirectory,
    MapdlCommandIgnoredError,
    MapdlDoLoopLimitError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.mapdl_core import _MapdlCore  # noqa: F401
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat  # noqa: F401
from ansys.mapdl.core.misc import (  # noqa: F401
    allow_iterables_vmin,
    allow_pickable_entities,
    check_deprecated_vtk_kwargs,
    random_string,
    requires_graphics,
    supress_logging,
)
from ansys.mapdl.core.plotting import GraphicsBackend  # noqa: F401

from . import _ExtendedMixinBase
from .contexts import TMP_VAR


class _ExtendedParameterCommandsMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    @wraps(_MapdlCore.dim)
    def dim(
        self,
        par="",
        type_="",
        imax="",
        jmax="",
        kmax="",
        var1="",
        var2="",
        var3="",
        csysid="",
        **kwargs,
    ):
        self._check_parameter_name(par)  # parameter name check
        if "(" in par or ")" in par:
            raise ValueError(
                "Parenthesis are not allowed as parameter name in 'mapdl.dim'."
            )

        return super().dim(
            par, type_, imax, jmax, kmax, var1, var2, var3, csysid, **kwargs
        )

    @wraps(_MapdlCore.inquire)
    def inquire(self, strarray="", func="", arg1="", arg2="", **kwargs):
        """Wraps original INQUIRE function

        Returns
        -------
        float or bool or str
            The inquired value. Type depends on the inquiry function used.
        """
        func_options = [
            "LOGIN",
            "DOCU",
            "APDL",
            "PROG",
            "AUTH",
            "USER",
            "DIRECTORY",
            "JOBNAME",
            "RSTDIR",
            "RSTFILE",
            "RSTEXT",
            "OUTPUT",
            "ENV",
            "TITLE",
            "EXIST",
            "DATE",
            "SIZE",
            "WRITE",
            "READ",
            "EXEC",
            "LINES",
        ]

        if strarray.upper() in func_options and func.upper() not in func_options:
            # Likely you are using the old ``_Mapdl.inquire`` implementation.
            raise ValueError(
                "Arguments of this method have changed. `Mapdl.inquire` now includes the optional `strarray` parameter "
                f"as the first argument. Either use `inquire(func={strarray})`, or `inquire("
                ", {strarray})`"
            )

        if func == "":
            func = "DIRECTORY"

        if strarray.upper() not in func_options and func.upper() not in func_options:
            raise ValueError(
                f"The arguments (strarray='{strarray}', func='{func}') are not valid."
            )

        response = ""
        n_try = 3
        i_try = 0
        while i_try < n_try and not response:
            response = self.run(
                f"/INQUIRE,{strarray},{func},{arg1},{arg2}", mute=False, **kwargs
            )
            i_try += 1

        if not response:
            if not self._store_commands:
                raise MapdlRuntimeError("/INQUIRE command didn't return a response.")
            else:
                # Exit since we are in non-interactive mode
                return None

        if func.upper() in [
            "ENV",
            "TITLE",
        ]:  # the output is multiline, we just need the last line.
            response = response.splitlines()[-1]

        response = response.split("=")[1].strip()

        if len(response) >= 248:
            warnings.warn(
                "Response might have been truncated to 248 characters because of "
                "MAPDL string limitations. "
                "Check the output of 'mapdl.inquire' carefully. "
                "Alternatively, you can use 'mapdl.sys('printenv') to obtain "
                "the environment variables on Linux."
            )

        # Check if the function is to check existence
        # so it makes sense to return a boolean
        if func.upper() in ["EXIST", "WRITE", "READ", "EXEC"]:
            if "1.0" in response:
                return True
            elif "0.0" in response:
                return False
            else:
                raise MapdlRuntimeError(
                    f"Unexpected output from 'mapdl.inquire' function:\n{response}"
                )

        if func.upper() in [
            "LOGIN",
            "DOCU",
            "APDL",
            "PROG",
            "AUTH",
            "USER",
            "DIRECTORY",
            "JOBNAME",
            "RSTDIR",
            "RSTFILE",
            "RSTEXT",
            "OUTPUT",
            "ENV",
            "TITLE",
            "DATE",
        ]:
            return response

        try:
            return float(response)
        except ValueError:
            return response

    @wraps(_MapdlCore.get)
    def get(
        self,
        par: str = "__floatparameter__",
        entity: str = "",
        entnum: str = "",
        item1: str = "",
        it1num: MapdlFloat = "",
        item2: str = "",
        it2num: MapdlFloat = "",
        item3: MapdlFloat = "",
        it3num: MapdlFloat = "",
        item4: MapdlFloat = "",
        it4num: MapdlFloat = "",
        **kwargs: KwargDict,
    ) -> Union[float, str]:
        self._check_parameter_name(par)

        command = f"*GET,{par},{entity},{entnum},{item1},{it1num},{item2},{it2num},{item3},{it3num},{item4},{it4num}"

        response = self.run(command, **kwargs)

        if not response:
            # If no response is received, re-run the command with force_output to ensure output is captured.
            with self.force_output:
                response = self.run(command, **kwargs)

        if self._store_commands:
            # Return early in non_interactive
            return

        value = response.split("=")[-1].strip()
        if item3:
            if len(value.splitlines()) > 1:
                self._log.info(
                    f"The command '{command}' is showing the next message: '{value.splitlines()[1].strip()}'"
                )
            value = value.splitlines()[0]

        try:  # always either a float or string
            return float(value)
        except ValueError:
            return value

    @wraps(_MapdlCore.ndinqr)
    def ndinqr(self, node, key, **kwargs):
        """Wrap the ``ndinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().ndinqr(node, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.elmiqr)
    def elmiqr(self, ielem, key, **kwargs):
        """Wrap the ``elmiqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().elmiqr(ielem, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.kpinqr)
    def kpinqr(self, knmi, key, **kwargs):
        """Wrap the ``kpinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().kpinqr(knmi, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.lsinqr)
    def lsinqr(self, line, key, **kwargs):
        """Wrap the ``lsinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().lsinqr(line, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.arinqr)
    def arinqr(self, anmi, key, **kwargs):
        """Wrap the ``arinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().arinqr(anmi, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.vlinqr)
    def vlinqr(self, vnmi, key, **kwargs):
        """Wrap the ``vlinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().vlinqr(vnmi, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.rlinqr)
    def rlinqr(self, nreal, key, **kwargs):
        """Wrap the ``rlinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().rlinqr(nreal, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.gapiqr)
    def gapiqr(self, ngap, key, **kwargs):
        """Wrap the ``gapiqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().gapiqr(ngap, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.masiqr)
    def masiqr(self, node, key, **kwargs):
        """Wrap the ``masiqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().masiqr(node, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.ceinqr)
    def ceinqr(self, nce, key, **kwargs):
        """Wrap the ``ceinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().ceinqr(nce, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.cpinqr)
    def cpinqr(self, ncp, key, **kwargs):
        """Wrap the ``cpinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().cpinqr(ncp, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.csyiqr)
    def csyiqr(self, ncsy, key, **kwargs):
        """Wrap the ``csyiqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().csyiqr(ncsy, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.etyiqr)
    def etyiqr(self, itype, key, **kwargs):
        """Wrap the ``etyiqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().etyiqr(itype, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.foriqr)
    def foriqr(self, node, key, **kwargs):
        """Wrap the ``foriqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().foriqr(node, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.sectinqr)
    def sectinqr(self, nsect, key, **kwargs):
        """Wrap the ``sectinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().sectinqr(nsect, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.mpinqr)
    def mpinqr(self, mat, iprop, key, **kwargs):
        """Wrap the ``mpinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().mpinqr(mat, iprop, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.dget)
    def dget(self, node, idf, kcmplx, **kwargs):
        """Wrap the ``dget`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().dget(node, idf, kcmplx, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.fget)
    def fget(self, node, idf, kcmplx, **kwargs):
        """Wrap the ``fget`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().fget(node, idf, kcmplx, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.erinqr)
    def erinqr(self, key, **kwargs):
        """Wrap the ``erinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().erinqr(key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.wrinqr)
    def wrinqr(self, key, **kwargs):
        """Wrap the ``wrinqr`` method to take advantage of the gRPC methods.

        Returns
        -------
        float
            Scalar parameter value.
        """
        super().wrinqr(key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)
