"""Module for licensing and license serve checks."""

import logging
import os
import time
import warnings
import re
import socket
import subprocess
import datetime


from ansys.mapdl.core.errors import LicenseServerConnectionError
from ansys.mapdl.core.misc import threaded

LOCALHOST = "127.0.0.1"
LIC_PATH_ENVAR = "ANSYSLIC_DIR"
LIC_FILE_ENVAR = "ANSYSLMD_LICENSE_FILE"

LOG = logging.getLogger(__name__)
LOG.setLevel('CRITICAL')


def check_license_file(timeout=10):
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

    else:
        print("Time is out for license checking.")


def get_licdebug_path():
    if os.name == "nt":
        folder = os.getenv("TEMP")
    elif os.name == "posix":
        folder = os.getenv("HOME")
    else:
        raise OSError(f"Unsupported OS {os.name}")

    return os.path.join(folder, ".ansys")


def get_licdebug_name():
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

    return ".".join(parts)


def get_licdebug_msg(licdebug_file):
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
    """Get the path to the Ansys license directory """

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
        if os.name == 'nt':
            ansyslic_dir = os.path.join(
                os.environ["ProgramFiles"], "ANSYS Inc", "Shared Files", "Licensing",
            )
        else:
            ansyslic_dir = '/usr/ansys_inc/shared_files/licencing'

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
                    server = ((int(port), host))
                    if server not in servers:
                        servers.append(server)
                except (ValueError, IndexError):
                    pass
                
    return servers


def check_port(ip=LOCALHOST, port=1055, timeout=20):
    """Check if a port can be opened to the specified host."""

    # if ip in ["127.0.0.1", or 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        # ping with any message
        tstart = time.time()
        LOG.debug("Pinging license server at %s on port %d", ip, port)
        s.connect((ip, port))
        s.send("message".encode("utf-8"))  # any message
        success = True
        LOG.debug("Received ping from license server in %f seconds", tstart - time.time())
    except socket.timeout:  # if timeout error, the port is probably closed.
        success = False
    except OSError as e:
        raise OSError(
            f"Pinging license server at {ip} on port {port} failed.\n\n{str(e)}"
        )
    finally:
        s.close()

    return success


def try_lmutil():
    try:
        check_license_server_with_lmutil()
    except LicenseServerConnectionError:
        # Reraising error
        raise
    except:
        # Unkw
        return False
    return True


def check_license_server_with_lmutil():
    """Check the license server status by running 'lmutil'.

    However this method is:
    - Not recommended because of the load generated in the server side.
    - Not reliable because the difficulty to catch the port in the license server
    """
    servers = get_license_server_config()
    ip, port = servers[0]

    output = query_lmutil(ip, port)
    selected_lines = re.findall("(?<=: license server )(.*)(?=\n)", output)
    servers_up = ["UP" in each for each in selected_lines]
    down_error_msg = (
        "Error getting status: License server machine is down or not responding."
    )

    if not servers_up:
        msg = "'lmutil' failed to get a list of servers."
        raise LicenseServerConnectionError(error_message=msg)
    elif down_error_msg in output:
        raise LicenseServerConnectionError(error_message=down_error_msg)
    elif any(servers_up):
        warnings.warn("Some license servers are down.")
    else:
        raise LicenseServerConnectionError(
            error_message="'lmutil' seems to found not working licenses."
        )


def query_lmutil(ip, port=1055):
    ansyslic_dir = get_ansyslic_dir()
    if os.name == 'nt':
        lmutil_path = os.path.join(ansyslic_dir, "winx64", "lmutil.exe")
    else:
        lmutil_path = os.path.join(ansyslic_dir, "linx64", "lmutil")

    process = subprocess.Popen(
        f"{lmutil_path} lmstat -a -i -c {port}@{ip}",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    return process.stdout.read().decode()


def try_ansysli_util():
    try:
        check_license_server_with_ansysli_util()
    except LicenseServerConnectionError:
        # Reraising error
        raise
    except:
        # Unkw
        return False
    return True


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
    if os.name == 'nt':
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
    """
    if check_license_file():
        return

    if check_mech_license_available():
        return

    # possible license server is completely unreachable
    check_license_server_port()
