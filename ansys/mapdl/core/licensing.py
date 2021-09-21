"""Module for licensing and license serve checks."""

import logging
import os
import time
import re
import socket
import subprocess


from ansys.mapdl.core.errors import LicenseServerConnectionError
from ansys.mapdl.core.misc import threaded

LOCALHOST = "127.0.0.1"
LIC_PATH_ENVAR = "ANSYSLIC_DIR"
LIC_FILE_ENVAR = "ANSYSLMD_LICENSE_FILE"

LOG = logging.getLogger(__name__)
LOG.setLevel("CRITICAL")


def check_license_file(timeout=10):
    """Check the output of the license client log for connection error.

    Expect type of errors with 'DENIED' in the header such as:
    ```
    2021/09/06 22:39:38    DENIED              ansys                           21.2 (2021.0512)             1/0/0/0                 1/1/1/1   10268:FEAT_ANSYS:gayuso@AAPDDqVK5WqNLrt.win.ansys.com:winx64   7368:192.168.18.10
                Request name ansys does not exist in the licensing pool.
                Cannot connect to license server system.
                 The license server manager (lmgrd) has not been started yet,
                 the wrong port@host or license file is being used, or the
                 port or hostname in the license file has been changed.
                Feature:       ansys
                Server name:   192.168.18.10
                License path:  1055@AAPDDqVK5WqNLrt;
                FlexNet Licensing error:-15,578.  System Error: 10049 "WinSock: Invalid address"
    ```

    Parameters
    ----------
    timeout : int
        Time to keep checking the license log file for errors.

    Raises
    ------
    LicenseServerConnectionError
        If there is an error message in the license log file.

    """
    licdebug_file = os.path.join(get_licdebug_path(), get_licdebug_name())
    file_iterator = get_licdebug_msg(licdebug_file)

    max_time = time.time() + timeout
    while max_time < time.time():
        msg = next(file_iterator)

        if "DENIED" in msg:
            license_path = re.findall("(?<=License path:)(.*)(?=;\n)", msg)[0]
            license_port = license_path.split("@")[0]
            license_hostname = license_path.split("@")[1]
            raise LicenseServerConnectionError(
                head_message=f"Error connecting to {license_port}:{license_hostname}",
                error_message=msg,
                tail_message=f"Error found in file {get_licdebug_name()}",
            )


def get_licdebug_path():
    """Get license client log (``licdebug``) path.

    This path is obtained from the correspondent env variable (OS dependent) and appending ``.ansys``.

    Returns
    -------
    str
        path of the license client log file.
    """
    if os.name == "nt":
        folder = os.getenv("TEMP")
    elif os.name == "posix":
        folder = os.getenv("HOME")
    else:
        raise OSError(f"Unsupported OS {os.name}")

    return os.path.join(folder, ".ansys")


def get_licdebug_name():
    """Get license client log file name.

    This file change the name according to the ANSYS version and the type of license requested (``$appname``).
    * For ANSYS version 22.1 and above: `licdebug.$hostname.$appname.$version.out`
    * For ANSYS version 21.2 and below: `licdebug.$appname.$version.out`

    where:
    * ``$hostname`` is the name of the machine.
    * ``$appname`` is the name of the license used by the license client. Eg 'meba' for 'mechanical enterprise'.
    * ``$version`` is the version of ANSYS. Eg 211 for version 21.1.

    Returns
    -------
    str
        licdebug log file complete name.

    """
    # Licdebug name convention:
    # - For version 22.1 and above: `licdebug.$hostname.$appname.$version.out`
    # - For version 21.2 and below: `licdebug.$appname.$version.out`

    from ansys.mapdl.core.launcher import _version_from_path, get_ansys_path

    name = "licdebug"
    hostname = socket.gethostname()
    appname = "FEAT_ANSYS"  # TODO: We need to make sure this is the type of feature we need to checkout.
    # This is the type of license my client requests (Windows 10, 2021R2)
    version = _version_from_path(get_ansys_path(allow_input=False))
    ending = "out"

    if version < 221:
        parts = (name, appname, version, ending)
    else:
        parts = (name, hostname, appname, version, ending)

    return ".".join([str(each_part) for each_part in parts])


def get_licdebug_msg(licdebug_file):
    """Get each of the licdebug file messages.

    This method keeps the ``licdebug`` file open checking for complete messages.
    It yields one message at a time when called.

    Parameters
    ----------
    licdebug_file : str
        Path to the ``licdebug`` file.

    Yields
    ------
    msg : str
        Message formated as a single string.

    """
    with open(licdebug_file) as f:
        f.seek(0, 2)  # Going to the end of the file.

        buffer = []
        while True:
            line = f.readline()
            if line:
                if buffer == []:  # not empty
                    buffer.append(line)

                else:
                    if line.startswith("\t\t"):
                        buffer.append(line)
                    else:
                        msg = "".join(buffer)
                        buffer = [line]  # Flushing buffer
                        yield msg
            else:
                time.sleep(0.01)


def check_license_server_port():
    """Check if the license server can be reached."""
    servers = get_license_server_config()
    host, port = servers[0]

    if not check_port(host, port):
        raise LicenseServerConnectionError(
            head_message=f"Error connecting to {port}:{host}"
        )
    return True


def ansys_lic_info_from_envar():
    """Read the Ansys license info from the enviornment variable LIC_PATH_ENVAR."""
    lic_info = os.getenv(LIC_FILE_ENVAR)

    if lic_info is None:
        return

    if os.path.isfile(lic_info):
        return

    try:
        port, host = lic_info.split("@")
        return [(int(port), host)]
    except (ValueError, IndexError):
        raise ValueError(
            f"Invalid license server or license file specified in {LIC_FILE_ENVAR}"
        )


def get_ansyslic_dir():
    """Get the path to the Ansys license directory"""

    # it's possible the user has specified the license as an env var
    ansyslic_dir = None
    if LIC_FILE_ENVAR in os.environ:
        ansyslmd_var = os.environ[LIC_FILE_ENVAR]
        if not os.path.isfile(ansyslmd_var):
            # likely license info
            ansyslic_dir = None
    else:
        ansyslic_dir = os.getenv(LIC_PATH_ENVAR)

    # env var may not be specified, check in the usual location
    if ansyslic_dir is None:
        if os.name == "nt":
            ansyslic_dir = os.path.join(
                os.environ["ProgramFiles"],
                "ANSYS Inc",
                "Shared Files",
                "Licensing",
            )
        else:
            ansyslic_dir = "/usr/ansys_inc/shared_files/licencing"

        if not os.path.isdir(ansyslic_dir):
            raise FileNotFoundError(
                f"Unable to locate ANSYS licencing path at {ansyslic_dir}\n"
                f"Specify the {LIC_PATH_ENVAR}"
            )

    return ansyslic_dir


def get_license_server_config():
    """Get the license server configuration.

    Returns
    -------
    list of tuple
        List of license servers containing a tuple with ``(host, port)``.
        Sorted by license server priority.

    """
    # enviornment variable overrides configuration file
    server = ansys_lic_info_from_envar()
    if server:
        return server

    # otherwise, read in the configuration file
    ansyslic_dir = get_ansyslic_dir()
    lic_config_path = os.path.join(ansyslic_dir, "ansyslmd.ini")
    if not os.path.isfile(lic_config_path):
        raise FileNotFoundError(f"'ansyslmd.ini' not found at {lic_config_path}")

    return parse_lic_config(lic_config_path)


def parse_lic_config(lic_config_path):
    """Parse license configuration file

    Reads lines in the form of
    ``SERVER=1055@13.95.70.166``

    Parameters
    ----------
    lic_config_path : str
        Absolute path to the license configruation file.  For example:
        ``'C:\\Program Files\\ANSYS Inc\\Shared Files\\Licensing\\ansyslmd.ini'```

    Returns
    -------
    list of tuple
        List of license servers containing a tuple with ``(host, port)``.

    """
    servers = []  # avoid duplication with set
    with open(lic_config_path) as fid:
        for line in fid.readlines():
            line = line.strip()

            # continue on empty lines and comments
            if not line:
                continue
            if line[0] == ";":
                continue

            if "SERVER" in line:
                try:
                    port, host = line.split("=")[1].split("@")
                    server = (host, int(port))
                    if server not in servers:
                        servers.append(server)
                except (ValueError, IndexError):
                    pass

    return servers


def check_port(ip=LOCALHOST, port=1055, timeout=20):
    """Check if a port can be opened to the specified host.

    Parameters
    ----------
    ip : str
        IP or hostname of the machine to check.
    port : int
        Port to check.
    timeout : int
        Amount of time to be passed before give up.

    Returns
    -------
    success : bool
        Success flag.

    Raises
    ------
    socket.timeout
        If the amount of time passed exceed the timeout.
    OSError
        Catching any other error.

    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        # ping with any message
        tstart = time.time()
        LOG.debug("Pinging license server at %s on port %d", ip, port)
        s.connect((ip, port))
        s.send("message".encode("utf-8"))  # any message
        success = True
        LOG.debug(
            "Received ping from license server in %f seconds", tstart - time.time()
        )
    except socket.timeout:  # if timeout error, the port is probably closed.
        success = False
    except OSError as e:
        raise OSError(
            f"Pinging license server at {ip} on port {port} failed.\n\n{str(e)}"
        )
    finally:
        s.close()

    return success


def check_mech_license_available(host=None):
    """Check if there mechanical license available by running 'ansysli_util'.

    This uses the default configuration available to MAPDL.

    .. warning::
       This method to check the license server status is not stable.  It
       is very likely it will show license not available when it actually
       is.

    Parameters
    ----------
    host : str, optional
        Override the default license server.  By default, use the
        values available in the Ansys license file.

    Returns
    -------
    bool
        Returns True when the license exists.

    Raises
    ------
    LicenseServerConnectionError
        When errors messages found in the output of the license file.

    """
    licenses = ["meba"]  # mechanical enterprise license.

    msg1 = "No such feature exists"
    msg2 = "The server is down or is not responsive."
    for each_license in licenses:
        output = checkout_license(each_license, host)
        if msg1 in output or msg2 in output:
            msg = msg1 if msg1 in output else msg2
            raise LicenseServerConnectionError(
                head_message=f"Ansys licencing utility reports '{msg}'"
            )

    return True


def checkout_license(lic, host=None, port=2325):
    """Check if a license is available using the Ansys license utility.

    It uses it own process.

    Parameters
    ----------
    lic : str
        License type.  For example, ``"meba".
    host : str, optional
        Host to attempt to checkout license from.  When set, this
        overrides any settings from the default license path.
    port : int, optional
        Port on the host to connect to.  Only used when ``host`` is set.

    """
    ansyslic_dir = get_ansyslic_dir()
    if os.name == "nt":
        ansysli_util_path = os.path.join(ansyslic_dir, "winx64", "ansysli_util.exe")
    else:
        ansysli_util_path = os.path.join(ansyslic_dir, "linx64", "ansysli_util")

    # allow the specification of ip and port
    env = os.environ.copy()
    if host is not None and port is not None:
        env["ANSYSLI_SERVERS"] = f"{host}:{port}"
        env["ANS_FLEXLM_DISABLE_DEFLICPATH"] = "TRUE"

    process = subprocess.Popen(
        f"{ansysli_util_path} -checkout {lic}",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    return process.stdout.read().decode()


@threaded
def try_license_server(verbose=False):
    """Trying the three possible methods to check the license server status.

    Three methods are used in order.
    * Check the ``licdebug`` log file for errors.
    * Check the available mechanical licenses using ``ansysli_util`` executable.
    * Check if there is response at the server port.

    Parameters
    ----------
    verbose : bool
        To printout output. Defaults to ``False``

    """
    if check_license_file():
        return

    if check_mech_license_available():
        return

    # possible license server is completely unreachable
    check_license_server_port()
