#!/bin/bash
echo $GH_PAT | docker login -u $GH_USERNAME --password-stdin docker.pkg.github.com
docker pull $MAPDL_IMAGE
docker run -e ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER --restart always --name mapdl -p $PYMAPDL_PORT:50052 -p $PYMAPDL_DB_PORT:50055 $MAPDL_IMAGE -smp > log.txt &
grep -q 'Server listening on' <(timeout 60 tail -f log.txt)
# python -c "from ansys.mapdl.core import launch_mapdl; print(launch_mapdl())"
