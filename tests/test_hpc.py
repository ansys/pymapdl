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

from unittest.mock import patch

from ansys.mapdl.core.hpc import launch_on_remote_hpc
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc


def test_launch_on_remote_hpc():
    import io

    with (
        patch("paramiko.client.SSHClient.connect") as mck_connect,
        patch("paramiko.client.SSHClient.exec_command") as mck_exec_command,
        patch("ansys.mapdl.core.launcher.get_hostname_host_cluster") as mock_ghhc,
        patch("socket.gethostbyname") as mck_ghn,
        patch("ansys.mapdl.core.mapdl_grpc.MapdlGrpc.__init__") as mock_mapdl,
    ):

        mck_connect.return_value = None
        mock_ghhc.return_value = "myhost", "123.45.67.89"
        mck_ghn.return_value = "123.45.67.89"
        mock_mapdl.return_value = None
        str_0 = [io.BytesIO(i) for i in [b"stdint", b"Directory created", b""]]
        str_1 = [io.BytesIO(i) for i in [b"stdint", b"Submitted batch job 1001", b""]]
        mck_exec_command.side_effect = (str_0, str_1)

        hostname = "myhost"
        username = "myuser"
        password = "mypass"
        exec_file = "my/path/to/ansys"
        port = 50054

        mapdl = launch_on_remote_hpc(
            hostname=hostname,
            username=username,
            password=password,
            exec_file=exec_file,
            port=port,
        )

        assert isinstance(mapdl, MapdlGrpc)

        mck_connect.assert_called()
        kwargs = mck_connect.call_args_list[0].kwargs
        assert kwargs["hostname"] == hostname
        assert kwargs["username"] == username
        assert kwargs["password"] == password
        assert kwargs["port"] == 22

        mck_exec_command.assert_called()
        assert len(mck_exec_command.call_args_list) == 2
        kwargs = mck_exec_command.call_args_list[1].kwargs
        assert "sbatch" in kwargs["command"]
        assert exec_file in kwargs["command"]
        assert str(port) in kwargs["command"]

        kwargs = mck_exec_command.call_args_list[0].kwargs
        assert f"/home/{username}/pymapdl/simulations" in kwargs["command"]

        kwargs = mock_mapdl.call_args_list[0].kwargs
        assert kwargs["ip"] == "123.45.67.89"
        assert kwargs["hostname"] == hostname
        assert kwargs["jobid"] == 1001
        assert kwargs["port"] == 50054
