"""
Everything related to licensing and license serve checks. 

"""

import os
import subprocess
import warnings
import socket


from ansys.mapdl.core.mapdl_grpc import check_valid_ip


LOCALHOST = '127.0.0.1'


def get_lmutil_path_windows():
    ansyslic_dir = os.getenv('ANSYSLIC_DIR')
    return os.path.join(ansyslic_dir, 'winx64')


def get_lmutil_path_linux():
    ansyslic_dir = os.getenv('ANSYSLIC_DIR')
    return os.path.join(ansyslic_dir, 'winx64') #TODO: Check if this folder is right.


def get_lmutil_path():
    if os.name == 'nt': # Windows
        lmutil_path = get_lmutil_path_windows()

    elif os.name == 'posix':  # Linux
        lmutil_path = get_lmutil_path_linux() 
    
    return os.path.join(lmutil_path,'lmutil.exe')


def lmutils_is_installed():
    if os.path.exists(get_lmutil_path()):
        return True
    else: 
        return False 


def run_lmutil(ip, port):
    lmutil_path = get_lmutil_path()
    command = f"{lmutil_path} lmstat -a -i -c {port}@{ip}"
    # subprocess.check_output(command, shell=os.name != 'nt')
    process =  subprocess.Popen(command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    return process.stdout.read().decode()


def check_license_server_lmutil(ip, port):
    """
    Check the license server status by running 'lmutil'. 

    However this method is:
    - Not recommended because of the load generated in the server side.
    - Not reliable because the difficulty to catch the port in the license server
    """

    warnings.warn('This method to check the license server status is not completely error free.\nIt is very likely it will show license not available.')
    
    output = run_lmutil(ip, port)
    selected_lines = re.findall('(?<=: license server )(.*)(?=\n)', output)
    servers_up = ['UP' in each for each in selected_lines]
    down_error_msg = 'Error getting status: License server machine is down or not responding.'
    
    if len(servers_up)==0 or down_error_msg in output:
        print("License check failed.")
        return False 
    elif all(servers_up):
        print("All servers are UP")
    elif any(servers_up):
        print("Some servers are down")
    else:
        print("All servers are down")
        return False 
    
    return True 


def ping_license_server_python(ip=LOCALHOST, port=1055, timeout=2):
    """
    Ping an IP with a port using python.
    """
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    msg = "lmutils lmstat"  # It could be anything.
    
    try:
        s.connect((ip, port))
        s.send(msg.encode('utf-8'))
        # s.create_connection()
    except socket.timeout: #if timeout error, the port is closed.
        success = False 
    else:
        # when there is no exceptions
        success = True 
    finally:
        s.close()

    return success


def ping_license_server(ip, port):
    """
    Ping the license server at the specified port and IP. 
    """
    
    if lmutils_is_installed():  # Not implemented.
        # Run lmutils
        return check_license_server_lmutil(ip, port)

    else: #Using python
        return ping_license_server_python(ip, port)
        

def check_license_server(ip=None, port=None):
    """
    Check if there is a valid license server running in the specified ip and port.
    If not supplied we will guess the location of the server from the installation.
    
    """

    if ip is None and port is None:
        host, port = get_license_server_details()

    return ping_license_server(host, port)


def get_license_server_details_for_docker_as_IP(ansyslmd_env):
    port = ansyslmd_env.split('@')[0]
    host = ansyslmd_env.split('@')[1]
    return host, port  


def get_license_server_details_for_docker_as_file(ansyslmd_env):
    # I dont know the format of this. Anyway 
    # It should not be used, since on docker mode, it is on the administrator 
    # to make sure there is a license server.
        return True 


def check_valid_hostname(hostname): 
    no_dots_in_hostname = not '.' in hostname

    # We could add more checks. 
    if no_dots_in_hostname:
        return True 
    else:
        return False 


def get_license_server_details_for_docker():
    ansyslmd_env = os.getenv('ANSYSLMD_LICENSE_FILE')
    hostname = ansyslmd_env.split('@')[1]

    if check_valid_ip(hostname) or check_valid_hostname(hostname):
        return get_license_server_details_for_docker_as_IP(ansyslmd_env)
    else:
        # It should be a file 
        return get_license_server_details_for_docker_as_file(ansyslmd_env)
    

def get_license_server_details_locally_for_linux():
    #trying windows approach?
    return get_license_server_details_locally_for_windows


def get_license_server_details_locally_for_windows():
    ansyslic_dir = os.getenv('ANSYSLIC_DIR')
    ansyslmdini_file = os.path.join(ansyslic_dir, 'ansyslmd.ini')

    with open(ansyslmdini_file) as f:
        ansyslmdini = f.readlines()
    
    server_conf = ansyslmdini[0].strip().split('=')[1] # Getting first line only. 
    port = server_conf.split('@')[0]
    host = server_conf.split('@')[1]
    return host, port 


def get_license_server_details():

    if os.getenv('ANSYSLMD_LICENSE_FILE') is not None:
        # Running from a docker!
        # We assume that docker containers always have `ANSYSLMD_LICENSE_FILE` environment variable.
        host, port = get_license_server_details_for_docker() 
        
    else: 
        # We are running with a full installation
        if os.name == 'posix':  # Linux
            host, port = get_license_server_details_locally_for_linux()
        elif os.name == 'nt':  # Windows
            host, port = get_license_server_details_locally_for_windows()
        
    return host, int(port)


## New approach
import os
import time 
import re 

from ansys.mapdl.core.errors import LicenseServerConnectionError

# from ansys.mapdl.core.launcher import _version_from_path

def get_licdebug_path():
    if os.name == 'nt': 
        folder = os.getenv('TEMP')
    elif os.name == 'posix':
        folder = os.getenv('HOME')
    else:
        raise OSError
    
    return os.path.join(folder, '.ansys')


def get_licdebug_name():
    return 'licdebug.FEAT_ANSYS.212.out'  #TODO: Make this more flexible and for more ansys versions.


def get_licdebug_msg(licdebug_file):
    f = open(licdebug_file)
    f.seek(0,2)  # Going to the end of the file. 

    buffer = []
    while True:
        line = f.readline()
        if line:
            if buffer == []: # not empty
                buffer.append(line)

            else:
                if line.startswith('\t\t'):
                    buffer.append(line)
                else:
                    msg = ''.join(buffer)
                    buffer = [line]  # Flushing buffer
                    yield  msg 
        else:
            time.sleep(0.01)


def is_denied_msg(msg):
    if 'DENIED' in msg:
        return True 
    else:
        return False 


def license_file_checker():
    licdebug_file = os.path.join(get_licdebug_path(), get_licdebug_name())

    time_to_be_checking = 5 #seconds
    tstart = time.time()
    file_iterator = get_licdebug_msg(licdebug_file)

    while (time.time() - tstart) < time_to_be_checking:
        msg = next(file_iterator)

        if is_denied_msg(msg):
            license_path = re.findall( "(?<=License path:)(.*)(?=;\n)", msg)[0]
            license_port = license_path.split('@')[0]
            license_hostname = license_path.split('@')[1]
            raise LicenseServerConnectionError(ip=license_hostname, port=license_port)


def check_license_server_with_python():
    # We are running with a full installation
    if os.name == 'posix':  # Linux
        host, port = get_license_server_details_locally_for_linux()
    elif os.name == 'nt':  # Windows
        host, port = get_license_server_details_locally_for_windows()

    if not ping_license_server_python(host, port):
        raise LicenseServerConnectionError(ip=host, port=port)


def check_license_server_with_lmutil():
    
    if os.name == 'posix':  # Linux
        ip, port = get_license_server_details_locally_for_linux()
    elif os.name == 'nt':  # Windows
        ip, port = get_license_server_details_locally_for_windows()

    """
    Check the license server status by running 'lmutil'. 

    However this method is:
    - Not recommended because of the load generated in the server side.
    - Not reliable because the difficulty to catch the port in the license server
    """

    warnings.warn('This method to check the license server status is not completely error free.\nIt is very likely it will show license not available.')
    
    output = run_lmutil(ip, port)
    selected_lines = re.findall('(?<=: license server )(.*)(?=\n)', output)
    servers_up = ['UP' in each for each in selected_lines]
    down_error_msg = 'Error getting status: License server machine is down or not responding.'
    
    if len(servers_up)==0 or down_error_msg in output:
        print("License check failed.")
        return False 
    elif all(servers_up):
        print("All servers are UP")
    elif any(servers_up):
        warnings.warn("Some license servers are down.")
    else:
        print("All servers are down")
        raise LicenseServerConnectionError


def try_license_file():
    
    try:
        license_file_checker()
    except LicenseServerConnectionError:
        # expected error, so let it raise
        raise LicenseServerConnectionError 
    except:
        # Rest of the cases, let's run secondary methods.
        print("Error found trying to ready license file.")
        return False
    else:
        return True 
        

def try_ping_server_python():
    try:
        check_license_server_with_python()
    except LicenseServerConnectionError:
        # Reraising error 
        raise LicenseServerConnectionError 
    except:
        return False 
    else:
        return True 
        

def try_lmutil():
    try:
        check_license_server_with_lmutil()
    except LicenseServerConnectionError:
        # Reraising error 
        raise LicenseServerConnectionError  
    except:
        # Unkw
        return False 
    else:
        return True 


        """
        
if license_server_check:

    if os.getenv('ANSYSLMD_LICENSE_FILE') is not None:
        # We are in a dockerized environment. 
        # We skip processing for the moment.
        pass 

    else:
        # running locally 
        success_ = try_license_file()

        if not success_:
            success_ = try_ping_server_python
        
        if not success_:
            success_ = try_lmutil()
            
            """