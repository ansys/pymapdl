## Containerized deployment of the MAPDL gRPC Server 

Run MAPDL within a container on any OS with `docker`!

---

There are several situations in which it is advantageous to run MAPDL
in a containerized environment (e.g. Docker or singularity):

- Run in a Linux environment on MacOS or Windows
- Portability and ease of install.
- Large scale cluster deployment using Kubernetes
- Genuine application isolation through containerization.

### Usage

This repository hosts several docker images which you can use to start
working with MAPDL immediately.  Assuming you have docker installed,
you can get started by authorizing docker to access this repository
using a personal access token.  Create a GH personal access token with
`packages read` permissions according to 
[Creating a personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

Save that token to a file with:
```
echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX > GH_TOKEN.txt
```

This lets you send the token to docker without leaving the token value
in your history.  Next, authorize docker to access this repository
with:

```
GH_USERNAME=myusername
cat GH_TOKEN.txt | docker login docker.pkg.github.com -u $GH_USERNAME --password-stdin
```

You can now launch MAPDL directly from docker with a short script or
directly from the command line.  Since this image contains no license
server, you will need to enter in your license server IP address the
`LICENSE_SERVER` environment variable.  With that, you can launch
MAPDL with:

```
!/bin/bash
LICENSE_SERVER=1055@XXX.XXX.XXX.XXX
VERSION=v21.1.0

IMAGE=docker.pkg.github.com/pyansys/mapdl/mapdl_grpc:$VERSION
docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 50052:50052 $IMAGE -smp
```

Note that port `50052` (local to the container) is being mapped to
50052 on the host.  This makes it possible to launch several MAPDL
instances with different port mappings to allow for multiple instances
of MAPDL.

Once you've launched MAPDL you'll see:

```
 Start GRPC Server

 ##############################
 ### START GRPC SERVER      ###
 ##############################

 Server Executable   : MapdlGrpc Server
 Server listening on : 0.0.0.0:50052
```

You can now connect to the instance (locally) with:

```python
>>> from ansys.mapdl import Mapdl
>>> ip = '127.0.0.1'
>>> mapdl = Mapdl(ip=ip, port=50052)
```

A successful connection returns:

```
2020-06-03 22:25:13,023 [INFO] ansys.mapdl.mapdl: Connected to MAPDL instance with jobname "file"
ANSYS Mechanical Enterprise
 RELEASE  2020 R2           BUILD 20.2TEST  UPDATE 20200229

 Current routine. . . . . . . . . . . .None (BEGIN level)

 Active coordinate system . . . . . . .   0 (Cartesian)

 Display coordinate system. . . . . . .   0 (Cartesian)

 Analysis type. . . . . . . . . . . . .Modal

 pyansys version: 0.53.0
```

Should you need to connect to the instance externally, simply set the
IP to the address of the computer you want to connect to.  For
example:

```python
>>> from ansys.mapdl import Mapdl
>>> ip = 192.168.1.11'
>>> mapdl = Mapdl(ip=ip, port=50052)
```

See the main [README.md](https://github.com/pyansys/mapdl/blob/master/README.md) for details regarding installing `pyansys` and MAPDL.

#### Additional Considerations

In the command:

```
IMAGE=docker.pkg.github.com/pyansys/mapdl/mapdl_grpc:$VERSION
docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 50052:50052 $IMAGE -smp
```

The `-smp` command line parameter sets MAPDL to use shared memory
parallel instead of the default distributed memory parallel.  Removing
this parameter will cause MAPDL to crash on MacOS with docker as it
appears the virtualization software for MacOS is not setup for Intel
MPI.

You can provide additional command line parameters to MAPDL by simply
appending to the docker command.  For example, you can increase the
number of processors (up to the number available on the host machine)
with the `-np` switch.  For example:

```
IMAGE=docker.pkg.github.com/pyansys/mapdl/mapdl_grpc:$VERSION
docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 50052:50052 $IMAGE -smp -np 4
```

For additional command line arguments please see the ansys
documentation at [ANSYS help](https://ansyshelp.ansys.com)
