#!/bin/bash
echo "MAPDL Instance name: $INSTANCE_NAME"
echo "MAPDL_VERSION: $MAPDL_VERSION"

export MAPDL_IMAGE="$MAPDL_PACKAGE:$MAPDL_VERSION"
echo "MAPDL_IMAGE:   $MAPDL_IMAGE"
docker pull "$MAPDL_IMAGE"

export MAJOR=$(echo "$MAPDL_VERSION" | head -c 3 | tail -c 2)
export MINOR=$(echo "$MAPDL_VERSION" | head -c 5 | tail -c 1)

export VERSION="$MAJOR$MINOR"
echo "MAPDL VERSION: $VERSION"


if [[ $MAPDL_VERSION == *"latest-ubuntu"* ]]; then
    echo "It is latest-ubuntu. Using 'ansys' script to launch"
    export EXEC_PATH=ansys
    # export P_SCHEMA=/ansys_inc/ansys/ac4/schema

elif [[ $MAPDL_VERSION == *"ubuntu"* ]] ; then
    echo "It is an ubuntu based image"
    export EXEC_PATH=/ansys_inc/v$VERSION/ansys/bin/mapdl
    export P_SCHEMA=/ansys_inc/v$VERSION/ansys/ac4/schema

else
    echo "It is a CentOS based image"
    export EXEC_PATH=/ansys_inc/ansys/bin/mapdl
    export P_SCHEMA=/ansys_inc/ansys/ac4/schema
fi;

if [[ $MAPDL_VERSION == *"cicd" ]] ; then
    echo "It is a CICD version, binding DPF port too"
    export DPF_ARG="-p $DPF_PORT:50055"
    export DB_INT_PORT=50056

    echo "DPF_ARG: $DPF_ARG"
    echo "DB_INT_PORT: $DB_INT_PORT"
else
    export DPF_ARG=""
    export DB_INT_PORT=50055
fi;

echo "EXEC_PATH: $EXEC_PATH"
echo "P_SCHEMA: $P_SCHEMA"

docker run \
    --entrypoint "/bin/bash" \
    --name "$INSTANCE_NAME" \
    --restart always \
    --health-cmd="ps aux | grep \"[/]ansys_inc/.*ansys\.e.*grpc\" -q && echo 0 || echo 1" \
    --health-interval=0.5s \
    --health-retries=4 \
    --health-timeout=0.5s \
    --health-start-period=10s \
    -e ANSYSLMD_LICENSE_FILE=1055@"${LICENSE_SERVER}" \
    -e ANSYS_LOCK="OFF" \
    -p "$PYMAPDL_PORT":50052 \
    -p "$PYMAPDL_DB_PORT":"${DB_INT_PORT}" \
    "${DPF_ARG}" \
    --shm-size=2gb \
    -e I_MPI_SHM_LMT=shm \
    -e P_SCHEMA="$P_SCHEMA" \
    -w /jobs \
    -u=0:0 \
    --memory=6656MB \
    --memory-swap=16896MB \
    "$MAPDL_IMAGE" "$EXEC_PATH" -grpc -dir /jobs -"$DISTRIBUTED_MODE" -np 2 -db -5000 -m -5000 - > log.txt &

grep -q 'Server listening on' <(timeout 60 tail -f log.txt)
