#!/bin/bash
docker pull $MAPDL_IMAGE
docker run \
    --name mapdl \
    --restart always \
    -e ANSYS_LOCK="OFF" \
    -p $PYMAPDL_PORT:50052 \
    -p $PYMAPDL_DB_PORT:50055 \
    --shm-size=2gb \
    -e I_MPI_SHM_LMT=shm \
    -e P_SCHEMA=/ansys_inc/ansys/ac4/schema \
    --memory=6656MB  \
    --memory-swap=16896MB \
    $MAPDL_IMAGE \
    -$DISTRIBUTED_MODE -np 2 > log.txt &
grep -q 'Server listening on' <(timeout 60 tail -f log.txt)
