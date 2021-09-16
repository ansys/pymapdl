"""
Everything related to licensing and license serve checks. 

"""

import os 
import time 
import warnings
import re 
import socket 
import subprocess
import datetime


from ansys.mapdl.core.errors import LicenseServerConnectionError  


LOCALHOST = '127.0.0.1'


def try_license_file():
    
    try:
        license_file_checker()
    except LicenseServerConnectionError:
        # expected error, so let it raise
        raise 
    except:
        # Rest of the cases, let's run secondary methods.
        # print("Error found trying to read license file.")
        return False
    else:
        return True 


def license_file_checker():
    licdebug_file = os.path.join(get_licdebug_path(), get_licdebug_name())
    file_iterator = get_licdebug_msg(licdebug_file)

    time_to_be_checking = 10 #seconds
    max_time = datetime.time(0, 0, time_to_be_checking) #hours, minute, seconds

    while max_time < datetime.datetime.now().time():
        msg = next(file_iterator)

        if is_denied_msg(msg):
            license_path = re.findall( "(?<=License path:)(.*)(?=;\n)", msg)[0]
            license_port = license_path.split('@')[0]
            license_hostname = license_path.split('@')[1]
            raise LicenseServerConnectionError(ip=license_hostname, port=license_port, 
                                                error_message=msg, 
                                                licdebug_name=get_licdebug_name())
        
    else:
        print("Time is out for license checking.")

def get_licdebug_path():
    if os.name == 'nt': 
        folder = os.getenv('TEMP')
    elif os.name == 'posix':
        folder = os.getenv('HOME')
    else:
        raise OSError
    
    return os.path.join(folder, '.ansys')


def get_licdebug_name():
    from ansys.mapdl.core.launcher import _version_from_path, get_ansys_path
    ansys_bin = get_ansys_path(allow_input=False)
    version = _version_from_path(ansys_bin)    
    return f'licdebug.FEAT_ANSYS.{version}.out'  #TODO: Make this more flexible and for more ansys versions.


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


## Python

def try_ping_server_python():
    try:
        check_license_server_with_python()
    except LicenseServerConnectionError:
        # Reraising error 
        raise 
    except:
        return False 
    else:
        return True 


def check_license_server_with_python():
    # We are running with a full installation
    host, port = get_license_server_details()
    
    if not ping_license_server_python(host, port):
        raise LicenseServerConnectionError(ip=host, port=port)


def get_license_server_details():
    if os.name == 'posix':  # Linux
        ip, port = get_license_server_details_locally_for_linux()
    elif os.name == 'nt':  # Windows
        ip, port = get_license_server_details_locally_for_windows()
    return ip, port 


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


## lmutils 

def try_lmutil():
    try:
        check_license_server_with_lmutil()
    except LicenseServerConnectionError:
        # Reraising error 
        raise 
    except:
        # Unkw
        return False 
    else:
        return True 


def check_license_server_with_lmutil():
    """
    Check the license server status by running 'lmutil'. 

    However this method is:
    - Not recommended because of the load generated in the server side.
    - Not reliable because the difficulty to catch the port in the license server
    """

    ip, port = get_license_server_details()

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


def run_lmutil(ip, port):
    lmutil_path = get_lmutil_path()
    command = f"{lmutil_path} lmstat -a -i -c {port}@{ip}"
    # subprocess.check_output(command, shell=os.name != 'nt')
    process =  subprocess.Popen(command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    return process.stdout.read().decode()


def get_lmutil_path():
    if os.name == 'nt': # Windows
        lmutil_path = get_lmutil_path_windows()

    elif os.name == 'posix':  # Linux
        lmutil_path = get_lmutil_path_linux() 
    
    return os.path.join(lmutil_path,'lmutil.exe')


def get_lmutil_path_windows():
    ansyslic_dir = os.getenv('ANSYSLIC_DIR')
    return os.path.join(ansyslic_dir, 'winx64')


def get_lmutil_path_linux():
    ansyslic_dir = os.getenv('ANSYSLIC_DIR')
    return os.path.join(ansyslic_dir, 'winx64') #TODO: Check if this folder is right.


## Main 

def try_license_server():
    """
    Trying the three possible methods to check the license server status.
    """
    success_ = try_license_file()

    if not success_:
        success_ = try_ping_server_python
    
    if not success_:
        success_ = try_lmutil()
    
    return success_