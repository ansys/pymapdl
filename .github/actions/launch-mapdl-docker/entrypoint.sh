#!/bin/bash
# MAPDL Container Entrypoint
# This script runs inside the MAPDL Docker container to start MAPDL and optionally DPF

set -e

echo "==================================="
echo "MAPDL Container Entrypoint"
echo "==================================="

# Allow running as root for MPI
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

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

echo "Configuration:"
echo "  VERSION: ${VERSION}"
echo "  MAPDL_VERSION: ${MAPDL_VERSION}"
echo "  EXEC_PATH: ${EXEC_PATH}"
echo "  DISTRIBUTED_MODE: ${DISTRIBUTED_MODE}"
echo "  NUM_PROCESSORS: ${NUM_PROCESSORS}"
echo "  MPI_ARG: ${MPI_ARG}"
echo "  TRANSPORT: ${TRANSPORT}"
echo "  MEMORY_DB_MB: ${MEMORY_DB_MB}"
echo "  MEMORY_WORKSPACE_MB: ${MEMORY_WORKSPACE_MB}"
echo "  ENABLE_DPF_SERVER: ${ENABLE_DPF_SERVER}"
echo "  DPF_PORT_INTERNAL: ${DPF_PORT_INTERNAL}"

# Check if DPF server should be started
if [[ "${ENABLE_DPF_SERVER}" == "true" ]] || [[ "${ANSYS_DPF_ACCEPT_LA}" == "Y" ]]; then
    echo ""
    echo "Starting DPF server..."
    export DPF_DEFAULT_GRPC_MODE="insecure"

    DPF_EXECUTABLE="/ansys_inc/v${VERSION}/aisol/bin/linx64/Ans.Dpf.Grpc.sh"

    if [ -f "${DPF_EXECUTABLE}" ]; then
        "${DPF_EXECUTABLE}" --port "${DPF_PORT_INTERNAL}" --address '0.0.0.0' > /log_dpf.log 2>&1 &
        echo "✅ DPF server started on port ${DPF_PORT_INTERNAL}"
    else
        echo "⚠️  Warning: DPF executable not found at ${DPF_EXECUTABLE}"
        echo "DPF server will not be started"
    fi
else
    echo "DPF server disabled"
fi

# Build MAPDL command
echo ""
echo "Starting MAPDL..."
echo "  Executable: ${EXEC_PATH}"
echo "  Mode: -${DISTRIBUTED_MODE}"
echo "  Processors: -np ${NUM_PROCESSORS}"
echo "  Transport: -transport ${TRANSPORT}"
echo "  DB Memory: -db ${MEMORY_DB_MB}"
echo "  Workspace Memory: -m ${MEMORY_WORKSPACE_MB}"

# Construct the MAPDL command
MAPDL_CMD="${EXEC_PATH} -grpc -dir /jobs -${DISTRIBUTED_MODE} -transport ${TRANSPORT} -allowremote true -np ${NUM_PROCESSORS} -db ${MEMORY_DB_MB} -m ${MEMORY_WORKSPACE_MB}"

# Add MPI argument if specified
if [ -n "${MPI_ARG}" ]; then
    MAPDL_CMD="${MAPDL_CMD} ${MPI_ARG}"
fi

# Add trailing dash to read from stdin (keeps container running)
MAPDL_CMD="${MAPDL_CMD} -"

echo ""
echo "Executing command:"
echo "  ${MAPDL_CMD}"
echo ""

# Execute MAPDL
exec ${MAPDL_CMD}
