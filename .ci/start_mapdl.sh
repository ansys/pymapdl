#!/bin/bash
# This script is used to start a MAPDL instance in a Docker container.
#
# Usage:
# ------
# This script is intended to be run in a CI/CD environment where the necessary environment variables are set.
#
# Required environment variables:
# -------------------------------
#
# - DISTRIBUTED_MODE: The mode of operation for MAPDL (e.g., "smp", "dmp").
# - DPF_PORT: The port for the DPF service (e.g., 50055).
# - INSTANCE_NAME: The name of the MAPDL instance (e.g., "MAPDL_0").
# - LICENSE_SERVER: The address of the license server (e.g., "123.123.123.123").
# - MAPDL_PACKAGE: The Docker image package name (e.g., ansys/mapdl).
# - MAPDL_VERSION: The version of the MAPDL image to use (e.g., "v25.2-ubuntu-cicd").
# - PYMAPDL_DB_PORT: The port for the PyMAPDL database service (e.g., 50056).
# - PYMAPDL_PORT: The port for the PyMAPDL service (e.g., 50052).
#
# Example:
# --------
#
#   export DISTRIBUTED_MODE="smp"
#   export DPF_PORT=50055
#   export INSTANCE_NAME=MAPDL_0
#   export LICENSE_SERVER="123.123.123.123"
#   export MAPDL_PACKAGE=ghcr.io/ansys/mapdl
#   export MAPDL_VERSION=v25.2-ubuntu-cicd
#   export PYMAPDL_DB_PORT=50056
#   export PYMAPDL_PORT=50052
#   ./start_mapdl.sh
#

export MAJOR MINOR MAPDL_IMAGE VERSION

echo "MAPDL Instance name: $INSTANCE_NAME"
echo "MAPDL_VERSION: $MAPDL_VERSION"

MAPDL_IMAGE="$MAPDL_PACKAGE:$MAPDL_VERSION"
echo "MAPDL_IMAGE:   $MAPDL_IMAGE"
docker pull "$MAPDL_IMAGE"

MAJOR=$(echo "$MAPDL_VERSION" | head -c 3 | tail -c 2)
MINOR=$(echo "$MAPDL_VERSION" | head -c 5 | tail -c 1)

VERSION="$MAJOR$MINOR"
echo "MAPDL VERSION: $VERSION"


if [[ $MAPDL_VERSION == *"latest-ubuntu"* ]]; then
    echo "It is latest-ubuntu. Using 'ansys' script to launch"
    EXEC_PATH=ansys
    # P_SCHEMA=/ansys_inc/ansys/ac4/schema

elif [[ $MAPDL_VERSION == *"ubuntu"* ]] ; then
    echo "It is an ubuntu based image"
    EXEC_PATH=/ansys_inc/v$VERSION/ansys/bin/mapdl
    P_SCHEMA=/ansys_inc/v$VERSION/ansys/ac4/schema

else
    echo "It is a CentOS based image"
    EXEC_PATH=/ansys_inc/ansys/bin/mapdl
    P_SCHEMA=/ansys_inc/ansys/ac4/schema
fi;

if [[ $MAPDL_VERSION == *"cicd"* ]] ; then
    echo "It is a CICD version, binding DPF port too"
    if [ "$RUN_DPF_SERVER" == "true" ]; then
        echo "RUN_DPF_SERVER is set to true, starting DPF server"
        export DPF_ON="-e ANSYS_DPF_ACCEPT_LA=Y"
    fi

    export DPF_PORT_INTERNAL=50055
    export DPF_PORT_ARG="-p ${DPF_PORT}:${DPF_PORT_INTERNAL}"
    export DB_INT_PORT=50056

    echo "DPF_PORT_ARG: $DPF_PORT_ARG"
    echo "DB_INT_PORT: $DB_INT_PORT"

    echo "Overriding DISTRIBUTED_MODE to 'dmp' for CICD version"
    export DISTRIBUTED_MODE="dmp"

else
    export DPF_PORT_ARG=""
    export DB_INT_PORT=50055
    export DPF_ON=""
fi;

echo "EXEC_PATH: $EXEC_PATH"
echo "P_SCHEMA: $P_SCHEMA"

# Building docker command
CMD=$(cat <<-_EOT_
run \
  --entrypoint /bin/bash \
  --name ${INSTANCE_NAME} \
  --restart unless-stopped \
  -e ANSYSLMD_LICENSE_FILE=1055@${LICENSE_SERVER} \
  -e ANSYS_LOCK="OFF" \
  ${DPF_ON} \
  -p ${PYMAPDL_PORT}:50052 \
  -p ${PYMAPDL_DB_PORT}:${DB_INT_PORT} \
  ${DPF_PORT_ARG} \
  -e VERSION=${VERSION} \
  -e DPF_PORT_INTERNAL=${DPF_PORT_INTERNAL} \
  -e EXEC_PATH=${EXEC_PATH} \
  -e DISTRIBUTED_MODE=${DISTRIBUTED_MODE} \
  -e MAPDL_IMAGE=${MAPDL_IMAGE} \
  --shm-size=2gb \
  -e I_MPI_SHM_LMT=shm \
  -e P_SCHEMA=${P_SCHEMA} \
  -w /jobs \
  -u=0:0 \
  --memory=6656MB \
  --memory-swap=16896MB \
  --mount type=bind,src=${PWD}/.ci/entrypoint.sh,dst=/entrypoint.sh \
  ${MAPDL_IMAGE} /entrypoint.sh
_EOT_
)

echo "Running docker command: "
echo "docker ${CMD}"
# shellcheck disable=SC2086
docker $CMD > "${INSTANCE_NAME}.log" &
grep -q 'Server listening on' <(timeout 60 tail -f "${INSTANCE_NAME}.log")

echo "Content of ${INSTANCE_NAME}.log:"
cat "${INSTANCE_NAME}.log"
