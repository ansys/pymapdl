#!/bin/bash
docker pull $MAPDL_IMAGE
docker run \
    --name mapdl \
    --restart always \
    --health-cmd="ps aux | grep \"[/]ansys_inc/.*ansys\.e.*grpc\" -q && echo 0 || echo 1" \
    --health-interval=0.5s \
    --health-retries=4 \
    --health-timeout=0.5s \
    --health-start-period=10s \
    -e ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER \
    -e ANSYS_LOCK="OFF" \
    -p $PYMAPDL_PORT:50052 \
    -p $PYMAPDL_DB_PORT:50055 \
    $MAPDL_IMAGE \
    -smp > log.txt &
grep -q 'Server listening on' <(timeout 60 tail -f log.txt)
# python -c "from ansys.mapdl.core import launch_mapdl; print(launch_mapdl())"
