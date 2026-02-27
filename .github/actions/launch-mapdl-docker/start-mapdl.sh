#!/bin/bash
# Launch MAPDL instance in a Docker container
# This script is used by the launch-mapdl-docker GitHub Action
set -e

# Setting debug mode.
DEBUG="${DEBUG:-false}"

# Helper for debug-only output
debug() {
    if [[ "${DEBUG}" == "true" ]]; then
        echo "$@"
    fi
}

# Print file contents when debugging is enabled
debug_file() {
    local file="$1"
    if [[ "${DEBUG}" != "true" ]]; then
        return 0
    fi

    if [[ -z "${file}" ]]; then
        debug "debug_file: no file specified"
        return 1
    fi

    if [[ ! -f "${file}" ]]; then
        debug "debug_file: file not found: ${file}"
        return 1
    fi

    debug "=== ${file} ==="
    while IFS= read -r _line; do
        debug "${_line}"
    done < "${file}"
    debug "=== end ${file} ==="
}


if [[ "${DEBUG}" == "true" ]]; then
    debug "Debug mode enabled"
    set -x
fi

echo "==================================="
echo "MAPDL Docker Container Launch"
echo "==================================="

# Validate required environment variables
if [ -z "${MAPDL_IMAGE}" ]; then
    echo "Error: MAPDL_IMAGE is required"
    exit 1
fi

if [ -z "${LICENSE_SERVER}" ]; then
    echo "Error: LICENSE_SERVER is required"
    exit 1
fi

# Set defaults
INSTANCE_NAME="${INSTANCE_NAME:-MAPDL_0}"
PYMAPDL_PORT="${PYMAPDL_PORT:-50052}"
PYMAPDL_DB_PORT="${PYMAPDL_DB_PORT:-50055}"
DPF_PORT="${DPF_PORT:-50056}"
ENABLE_DPF_SERVER="${ENABLE_DPF_SERVER:-false}"
DISTRIBUTED_MODE="${DISTRIBUTED_MODE:-None}"
NUM_PROCESSORS="${NUM_PROCESSORS:-2}"
MPI_TYPE="${MPI_TYPE:-auto}"
WORKING_DIRECTORY="${WORKING_DIRECTORY:-/jobs}"
MEMORY_MB="${MEMORY_MB:-6656}"
MEMORY_SWAP_MB="${MEMORY_SWAP_MB:-16896}"
MEMORY_DB_MB="${MEMORY_DB_MB:-6000}"
MEMORY_WORKSPACE_MB="${MEMORY_WORKSPACE_MB:-6000}"
TRANSPORT="${TRANSPORT:-insecure}"
TIMEOUT="${TIMEOUT:-60}"



echo -e "\n"
echo "Pulling Docker image: ${MAPDL_IMAGE}"
if docker pull "${MAPDL_IMAGE}" > pull.log 2>&1; then
    echo "Image pulled successfully"
else
    echo "Failed to pull image: ${MAPDL_IMAGE}"
    cat pull.log
    exit 1
fi

debug "Pull logs:"
debug_file pull.log

# Extract version number
MAJOR=$(echo "$MAPDL_VERSION" | head -c 2 | tail -c 2)
MINOR=$(echo "$MAPDL_VERSION" | head -c 4 | tail -c 1)
VERSION="${MAJOR}${MINOR}"
debug "Extracted MAPDL version number: ${VERSION}"


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

if [[ $MAPDL_IMAGE == *"cicd"* ]]; then
    debug "CICD image detected."

    if [[ "${ENABLE_DPF_SERVER}" == "true" ]]; then
        debug "Enabling DPF server for CICD version"
        DPF_ENV_ARGS=("-e" "ANSYS_DPF_ACCEPT_LA=Y")
    fi

    DPF_PORT_ARGS=("-p" "${DPF_PORT}:${DPF_PORT_INTERNAL}")
    DB_INT_PORT="50056"

    # CICD versions force DMP mode
    debug "  Overriding distributed mode to 'dmp' for CICD version"

    if [[ "${DISTRIBUTED_MODE}" == "None" ]]; then
        DISTRIBUTED_MODE="dmp"
    fi
else
    DB_INT_PORT="50055"
fi

if [[ "${DISTRIBUTED_MODE}" == "None" ]]; then
    echo "No distributed mode specified, defaulting to SMP"
    DISTRIBUTED_MODE="smp"
fi

vendor=$(awk -F: '/vendor_id/{print $2; exit}' /proc/cpuinfo | tr -d ' \t')
debug "CPU vendor_id from /proc/cpuinfo: ${vendor}"
debug_file /proc/cpuinfo

if [[ "$vendor" == "GenuineIntel" ]]; then
  export CPU_VENDOR="INTEL"
elif [[ "$vendor" == "AuthenticAMD" ]]; then
  export CPU_VENDOR="AMD"
else
  echo "Unknown CPU vendor (vendor_id: $vendor)"
fi

# Determine MPI type
if [[ "${MPI_TYPE}" == "openmpi" ]]; then
    MPI_ARG="-mpi openmpi"
elif [[ "${MPI_TYPE}" == "intelmpi" ]]; then
    MPI_ARG="-mpi intelmpi"
else
    MPI_ARG=""
fi

if [[ "$CPU_VENDOR" == "AMD" ]]; then
    if [[ -z "${MPI_ARG}" ]]; then
        echo "No MPI type specified, defaulting to OpenMPI for AMD CPU"
        MPI_ARG="-mpi openmpi"
    fi

    if [[ "${MPI_ARG}" != *"openmpi"* ]]; then
        echo "WARNING: AMD CPU detected but MPI type is not OpenMPI. Defaulting to OpenMPI for compatibility."
        echo "It is likely that the specified MPI type may not be fully compatible with AMD CPUs. Consider using OpenMPI for best performance."
        echo "If you experience issues, try setting MPI_TYPE to 'openmpi' or ensure your chosen MPI implementation supports AMD CPUs."
    fi
fi

echo -e "\nContainer Configuration:"
echo "  MAPDL Image: ${MAPDL_IMAGE}"
echo "  Instance Name: ${INSTANCE_NAME}"
echo "  CPU Vendor: ${CPU_VENDOR}"
echo "  Reserved memory: ${MEMORY_MB}"
echo "  Reserved swap memory: ${MEMORY_SWAP_MB}"
echo -e "\n"

echo -e "\nMAPDL Configuration:"
echo "  MAPDL Version: ${MAPDL_VERSION} (Version number: ${VERSION})"
echo "  Executable Path: ${EXEC_PATH}"
echo "  DB Memory: -db ${MEMORY_DB_MB}"
echo "  Workspace Memory: -m ${MEMORY_WORKSPACE_MB}"
echo "  Transport: ${TRANSPORT}"
echo "  License Server: ${LICENSE_SERVER}"
echo "  Schema Path: ${P_SCHEMA}"
echo -e "\n"

echo -e "\nMPI Configuration:"
echo "  Distributed Mode: ${DISTRIBUTED_MODE}"
echo "  Number of Processors: ${NUM_PROCESSORS}"
echo "  MPI Type: ${MPI_TYPE}"
echo "  Memory: ${MEMORY_MB} MB"
echo "  MPI Arguments: ${MPI_ARG}"
echo -e "\n"

echo -e "\nPyMAPDL Configuration:"
echo "  PyMAPDL Port: ${PYMAPDL_PORT}"
echo "  PyMAPDL DB Port: ${PYMAPDL_DB_PORT}"
echo "  DB Internal Port: ${DB_INT_PORT}"
echo -e "\n"

echo -e "\nDPF Configuration:"
echo "  Enable DPF: ${ENABLE_DPF_SERVER}"
echo "  DPF Port: ${DPF_PORT}"
echo "  DPF Port Mapping: ${DPF_PORT_ARGS[*]}"
echo -e "\n"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
debug "Script directory: ${SCRIPT_DIR}"

# Prepare entrypoint script path
ENTRYPOINT_PATH="${SCRIPT_DIR}/entrypoint.sh"
debug "Entrypoint script path: ${ENTRYPOINT_PATH}"

# Build Docker run command
echo -e "\n"
echo "Running Docker container..."

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
  -e DEBUG="${DEBUG}" \
  --shm-size=2gb \
  -e I_MPI_SHM_LMT=shm \
  -e P_SCHEMA="${P_SCHEMA}" \
  -w "${WORKING_DIRECTORY}" \
  -u=0:0 \
  --memory="${MEMORY_MB}MB" \
  --memory-swap="${MEMORY_SWAP_MB}MB" \
  --mount type=bind,src="${ENTRYPOINT_PATH}",dst=/entrypoint.sh \
  -e OMPI_ALLOW_RUN_AS_ROOT=1 \
  -e OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 \
  "${MAPDL_IMAGE}" \
  -c "chmod +x /entrypoint.sh && /entrypoint.sh"

echo -e "\n"
echo "Container started. Waiting for MAPDL to initialize..."

# Wait for "Server listening" message in logs
LOG_FILE="${INSTANCE_NAME}.log"
docker logs -f "${INSTANCE_NAME}" > "${LOG_FILE}" 2>&1 &
DOCKER_LOGS_PID=$!

debug "Following container logs (PID: ${DOCKER_LOGS_PID})..."
debug "Waiting for 'Server listening on' message to confirm MAPDL is ready..."
debug "Logs will be saved to: ${LOG_FILE}"
debug_file "${LOG_FILE}"

# Wait for server to be ready
ELAPSED=0
while [ $ELAPSED -lt "$TIMEOUT" ]; do
    if grep -q "Server listening on" "${LOG_FILE}" 2>/dev/null; then
        echo "MAPDL server is listening!"
        break
    fi
    sleep 1
    ELAPSED=$((ELAPSED + 1))
    debug "Waiting for MAPDL server... (${ELAPSED}s elapsed)"
done

# Stop following logs
if kill "${DOCKER_LOGS_PID}" 2>/dev/null; then
    debug "Stopped following container logs"
else
    debug "Failed to stop following logs"
fi

if [ $ELAPSED -ge "$TIMEOUT" ]; then
    echo "Timeout waiting for MAPDL server (${TIMEOUT}s)"
    echo "Container logs:"
    cat "${LOG_FILE}"
    exit 1
fi

echo -e "\n"
echo "Container logs:"
cat "${LOG_FILE}"

echo -e "\n"
echo "==================================="
echo "MAPDL Container Launch Complete"
echo "==================================="
