#!/bin/bash
docker pull "$MAPDL_IMAGE"
docker run \
    --name mapdl \
    --restart always \
    -e ANSYS_LOCK="OFF" \
    -p "$PYMAPDL_PORT":50052 \
    -p "$PYMAPDL_DB_PORT":50055 \
    --shm-size=2gb \
    -e P_SCHEMA=/ansys_inc/v241/ansys/ac4/schema \
    "$MAPDL_IMAGE" -np 2 > log.txt &
# grep -q 'Server listening on' <(timeout 60 tail -f log.txt)
