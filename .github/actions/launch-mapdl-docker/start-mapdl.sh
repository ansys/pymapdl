#!/bin/bash
# Launch MAPDL instance in a Docker container
# This script is used by the launch-mapdl-docker GitHub Action
set -e

echo "==================================="
echo "MAPDL Docker Container Launch"
echo "==================================="

# Validate required environment variables
if [ -z "${MAPDL_IMAGE}" ]; then
    echo "❌ Error: MAPDL_IMAGE is required"
    exit 1
fi

if [ -z "${LICENSE_SERVER}" ]; then
    echo "❌ Error: LICENSE_SERVER is required"
    exit 1
fi

# Set defaults
INSTANCE_NAME="${INSTANCE_NAME:-MAPDL_0}"
PYMAPDL_PORT="${PYMAPDL_PORT:-50052}"
PYMAPDL_DB_PORT="${PYMAPDL_DB_PORT:-50055}"
DPF_PORT="${DPF_PORT:-50056}"
ENABLE_DPF_SERVER="${ENABLE_DPF_SERVER:-false}"
DISTRIBUTED_MODE="${DISTRIBUTED_MODE:-smp}"
NUM_PROCESSORS="${NUM_PROCESSORS:-2}"
MPI_TYPE="${MPI_TYPE:-auto}"
WORKING_DIRECTORY="${WORKING_DIRECTORY:-/jobs}"
MEMORY_MB="${MEMORY_MB:-6656}"
MEMORY_SWAP_MB="${MEMORY_SWAP_MB:-16896}"
MEMORY_DB_MB="${MEMORY_DB_MB:-6000}"
MEMORY_WORKSPACE_MB="${MEMORY_WORKSPACE_MB:-6000}"
TRANSPORT="${TRANSPORT:-insecure}"
TIMEOUT="${TIMEOUT:-60}"

echo "Configuration:"
echo "  MAPDL Version: ${MAPDL_VERSION}"
echo "  MAPDL Image: ${MAPDL_IMAGE}"
echo "  Instance Name: ${INSTANCE_NAME}"
echo "  License Server: ${LICENSE_SERVER}"
echo "  PyMAPDL Port: ${PYMAPDL_PORT}"
echo "  PyMAPDL DB Port: ${PYMAPDL_DB_PORT}"
echo "  DPF Port: ${DPF_PORT}"
echo "  Enable DPF: ${ENABLE_DPF_SERVER}"
echo "  Distributed Mode: ${DISTRIBUTED_MODE}"
echo "  Number of Processors: ${NUM_PROCESSORS}"
echo "  MPI Type: ${MPI_TYPE}"
echo "  Memory: ${MEMORY_MB} MB"
echo "  Transport: ${TRANSPORT}"

echo ""
echo "Pulling Docker image: ${MAPDL_IMAGE}"
docker pull "${MAPDL_IMAGE}"

# Extract version number
MAJOR=$(echo "$MAPDL_VERSION" | head -c 2 | tail -c 2)
MINOR=$(echo "$MAPDL_VERSION" | head -c 4 | tail -c 1)
VERSION="${MAJOR}${MINOR}"
echo "Extracted MAPDL version number: ${VERSION}"

# Determine executable path based on image type
if [[ $MAPDL_IMAGE == *"latest-ubuntu"* ]]; then
    echo "Detected: latest-ubuntu image"
    EXEC_PATH="ansys"
    P_SCHEMA=""
elif [[ $MAPDL_IMAGE == *"ubuntu"* ]]; then
    echo "Detected: Ubuntu-based image"
    EXEC_PATH="/ansys_inc/v${VERSION}/ansys/bin/mapdl"
    P_SCHEMA="/ansys_inc/v${VERSION}/ansys/ac4/schema"
else
    echo "Detected: CentOS/Rocky-based image"
    EXEC_PATH="/ansys_inc/ansys/bin/mapdl"
    P_SCHEMA="/ansys_inc/ansys/ac4/schema"
fi

# Configure DPF server settings
DPF_PORT_INTERNAL="50055"
DPF_ENV_ARGS=()
DPF_PORT_ARGS=()

if [[ $MAPDL_VERSION == *"cicd"* ]]; then
    echo "Detected: CICD version"

    if [[ "${ENABLE_DPF_SERVER}" == "true" ]]; then
        echo "  Enabling DPF server"
        DPF_ENV_ARGS=("-e" "ANSYS_DPF_ACCEPT_LA=Y")
    fi

    DPF_PORT_ARGS=("-p" "${DPF_PORT}:${DPF_PORT_INTERNAL}")
    DB_INT_PORT="50056"

    # CICD versions force DMP mode
    echo "  Overriding distributed mode to 'dmp' for CICD version"
    DISTRIBUTED_MODE="dmp"
else
    DB_INT_PORT="50055"
fi

# Determine MPI type
if [[ "${MPI_TYPE}" == "auto" ]]; then
    if [[ $MAPDL_IMAGE == *"cicd"* ]]; then
        MPI_ARG="-mpi openmpi"
    else
        MPI_ARG=""
    fi
elif [[ "${MPI_TYPE}" == "openmpi" ]]; then
    MPI_ARG="-mpi openmpi"
elif [[ "${MPI_TYPE}" == "intelmpi" ]]; then
    MPI_ARG="-mpi intelmpi"
else
    MPI_ARG=""
fi

echo ""
echo "Container Configuration:"
echo "  Executable Path: ${EXEC_PATH}"
echo "  Schema Path: ${P_SCHEMA}"
echo "  DPF Port Mapping: ${DPF_PORT_ARGS[*]}"
echo "  DB Internal Port: ${DB_INT_PORT}"
echo "  MPI Arguments: ${MPI_ARG}"
echo "  Distributed Mode: ${DISTRIBUTED_MODE}"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Prepare entrypoint script path
ENTRYPOINT_PATH="${SCRIPT_DIR}/entrypoint.sh"

# Build Docker run command
echo ""
echo "Building Docker container..."

# Build docker command with all configurations
docker run \
  --detach \
  --entrypoint /bin/bash \
  --name "${INSTANCE_NAME}" \
  --restart unless-stopped \
  -e ANSYSLMD_LICENSE_FILE="1055@${LICENSE_SERVER}" \
  -e ANSYS_LOCK="OFF" \
  -p "${PYMAPDL_PORT}:50052" \
  -p "${PYMAPDL_DB_PORT}:${DB_INT_PORT}" \
  "${DPF_PORT_ARGS[@]}" \
  "${DPF_ENV_ARGS[@]}" \
  -e VERSION="${VERSION}" \
  -e MAPDL_VERSION="${MAPDL_VERSION}" \
  -e DPF_PORT_INTERNAL="${DPF_PORT_INTERNAL}" \
  -e EXEC_PATH="${EXEC_PATH}" \
  -e DISTRIBUTED_MODE="${DISTRIBUTED_MODE}" \
  -e NUM_PROCESSORS="${NUM_PROCESSORS}" \
  -e MPI_ARG="${MPI_ARG}" \
  -e TRANSPORT="${TRANSPORT}" \
  -e MEMORY_DB_MB="${MEMORY_DB_MB}" \
  -e MEMORY_WORKSPACE_MB="${MEMORY_WORKSPACE_MB}" \
  -e ENABLE_DPF_SERVER="${ENABLE_DPF_SERVER}" \
  --shm-size=2gb \
  -e I_MPI_SHM_LMT=shm \
  -e P_SCHEMA="${P_SCHEMA}" \
  -w "${WORKING_DIRECTORY}" \
  -u=0:0 \
  --memory="${MEMORY_MB}MB" \
  --memory-swap="${MEMORY_SWAP_MB}MB" \
  --mount type=bind,src="${ENTRYPOINT_PATH}",dst=/entrypoint.sh \
  "${MAPDL_IMAGE}" \
  /entrypoint.sh

echo ""
echo "Container started. Waiting for MAPDL to initialize..."

# Wait for "Server listening" message in logs
LOG_FILE="${INSTANCE_NAME}.log"
docker logs -f "${INSTANCE_NAME}" > "${LOG_FILE}" 2>&1 &
DOCKER_LOGS_PID=$!

# Wait for server to be ready
ELAPSED=0
while [ $ELAPSED -lt "$TIMEOUT" ]; do
    if grep -q "Server listening on" "${LOG_FILE}" 2>/dev/null; then
        echo "✅ MAPDL server is listening!"
        break
    fi
    sleep 1
    ELAPSED=$((ELAPSED + 1))
done

# Stop following logs
kill $DOCKER_LOGS_PID 2>/dev/null || true

if [ $ELAPSED -ge "$TIMEOUT" ]; then
    echo "⚠️  Timeout waiting for MAPDL server (${TIMEOUT}s)"
    echo "Container logs:"
    cat "${LOG_FILE}"
    exit 1
fi

echo ""
echo "Container logs:"
cat "${LOG_FILE}"

echo ""
echo "==================================="
echo "✅ MAPDL Container Launch Complete"
echo "==================================="
echo "Container Name: ${INSTANCE_NAME}"
echo "PyMAPDL Port: ${PYMAPDL_PORT}"
echo "DPF Port: ${DPF_PORT}"
echo "Log File: ${LOG_FILE}"
