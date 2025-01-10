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

from typing import Any, Dict, Optional, Union

from ansys.mapdl.core import LOG
from ansys.mapdl.core.launcher.tools import (
    check_kwargs,
    generate_start_parameters,
    get_ip,
    get_port,
    pack_arguments,
    pre_check_args,
)
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc


def connect_to_mapdl(
    *,
    loglevel: str = "ERROR",
    start_timeout: Optional[int] = None,
    port: Optional[int] = None,
    cleanup_on_exit: bool = True,
    ip: Optional[str] = None,
    clear_on_connect: bool = True,
    log_apdl: Optional[Union[bool, str]] = None,
    print_com: bool = False,
    **kwargs: Dict[str, Any],
):
    ########################################
    # Processing arguments
    # --------------------
    #
    # packing arguments
    args = pack_arguments(locals())  # packs args and kwargs

    check_kwargs(args)  # check if passing wrong arguments

    if args.get("start_instance"):
        raise ValueError(
            "'connect_to_mapdl' only accept 'start_instance' equals 'False'. "
            "If you intend to launch locally an instance use either "
            "'launch_mapdl_grpc' or the infamous 'launch_mapdl(start_instance=True)'."
        )

    pre_check_args(args)

    get_ip(args)

    args["port"] = get_port(args["port"], args["start_instance"])

    # Check for a valid connection mode
    # args["mode"] = check_mode(args["mode"], args["version"])
    if args.get("mode", "grpc") != "grpc":
        raise ValueError("Only a 'grpc' instance can be connected to remotely.")

    start_parm = generate_start_parameters(args)

    # Early exit for debugging.
    if args["_debug_no_launch"]:
        # Early exit, just for testing
        return args  # type: ignore

    ########################################
    # Connecting to a remote instance
    # -------------------------------
    #
    LOG.debug(
        f"Connecting to an existing instance of MAPDL at {args['ip']}:{args['port']}"
    )
    start_parm["launched"] = False

    mapdl = MapdlGrpc(
        cleanup_on_exit=False,
        loglevel=args["loglevel"],
        set_no_abort=args["set_no_abort"],
        use_vtk=args["use_vtk"],
        log_apdl=args["log_apdl"],
        **start_parm,
    )
    if args["clear_on_connect"]:
        mapdl.clear()
    return mapdl
