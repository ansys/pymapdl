#!/bin/bash
# MAPDL Container Entrypoint
# This script runs inside the MAPDL Docker container to start MAPDL and optionally DPF

set -e

echo "==================================="
echo "MAPDL Container Entrypoint"
echo "==================================="

DEBUG="${DEBUG:-false}"

debug() {
    if [[ "${DEBUG}" == "true" ]]; then
        echo "$@"
    fi
}

# Validate required environment variables
if [ -z "${VERSION}" ]; then
    echo "❌ Error: VERSION environment variable is not set"
    exit 1
fi

if [ -z "${EXEC_PATH}" ]; then
    echo "❌ Error: EXEC_PATH environment variable is not set"
    exit 1
fi

# Set defaults
DISTRIBUTED_MODE="${DISTRIBUTED_MODE:-smp}"
NUM_PROCESSORS="${NUM_PROCESSORS:-2}"
MPI_ARG="${MPI_ARG:-}"
TRANSPORT="${TRANSPORT:-insecure}"
MEMORY_DB_MB="${MEMORY_DB_MB:-6000}"
MEMORY_WORKSPACE_MB="${MEMORY_WORKSPACE_MB:-6000}"
ENABLE_DPF_SERVER="${ENABLE_DPF_SERVER:-false}"
DPF_PORT_INTERNAL="${DPF_PORT_INTERNAL:-50055}"

debug "Configuration:"
debug "  VERSION: ${VERSION}"
debug "  MAPDL_VERSION: ${MAPDL_VERSION}"
debug "  EXEC_PATH: ${EXEC_PATH}"
debug "  DISTRIBUTED_MODE: ${DISTRIBUTED_MODE}"
debug "  NUM_PROCESSORS: ${NUM_PROCESSORS}"
debug "  MPI_ARG: ${MPI_ARG}"
debug "  TRANSPORT: ${TRANSPORT}"
debug "  MEMORY_DB_MB: ${MEMORY_DB_MB}"
debug "  MEMORY_WORKSPACE_MB: ${MEMORY_WORKSPACE_MB}"
debug "  ENABLE_DPF_SERVER: ${ENABLE_DPF_SERVER}"
debug "  DPF_PORT_INTERNAL: ${DPF_PORT_INTERNAL}"

# Check if DPF server should be started
if [[ "${ENABLE_DPF_SERVER}" == "true" ]] || [[ "${ANSYS_DPF_ACCEPT_LA}" == "Y" ]]; then
    debug ""
    debug "Starting DPF server..."
    export DPF_DEFAULT_GRPC_MODE="insecure"

    DPF_EXECUTABLE="/ansys_inc/v${VERSION}/aisol/bin/linx64/Ans.Dpf.Grpc.sh"

    if [ -f "${DPF_EXECUTABLE}" ]; then
        "${DPF_EXECUTABLE}" --port "${DPF_PORT_INTERNAL}" --address '0.0.0.0' > /log_dpf.log 2>&1 &
        debug "✅ DPF server started on port ${DPF_PORT_INTERNAL}"
    else
        debug "⚠️  Warning: DPF executable not found at ${DPF_EXECUTABLE}"
        debug "DPF server will not be started"
    fi

    debug "  DPF_EXECUTABLE: ${DPF_EXECUTABLE}"
else
    debug "DPF server disabled"
fi


# Build MAPDL command

# Construct the MAPDL command
MAPDL_CMD="${EXEC_PATH} -grpc -dir /jobs -${DISTRIBUTED_MODE} -transport ${TRANSPORT} -allowremote true -np ${NUM_PROCESSORS} -db ${MEMORY_DB_MB} -m ${MEMORY_WORKSPACE_MB}"

# Add MPI argument if specified
if [ -n "${MPI_ARG}" ]; then
    MAPDL_CMD="${MAPDL_CMD} ${MPI_ARG}"
fi

echo ""
echo "Executing command:"
echo "  ${MAPDL_CMD}"
echo ""

# Execute MAPDL
exec ${MAPDL_CMD}
