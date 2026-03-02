#!/bin/bash
# Wait for MAPDL and DPF services to be ready
set -e
# Setting debug mode.
DEBUG="${DEBUG:-false}"

# Helper for debug-only output
debug() {
    if [[ "${DEBUG}" == "true" ]]; then
        echo "$@"
    fi
}

if [[ "${DEBUG}" == "true" ]]; then
    debug "Debug mode enabled"
fi

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

echo "==================================="
echo "Waiting for Services"
echo "==================================="


# Set defaults
PYMAPDL_PORT="${PYMAPDL_PORT:-50052}"
DPF_PORT="${DPF_PORT:-50056}"
ENABLE_DPF_SERVER="${ENABLE_DPF_SERVER:-false}"
INSTANCE_NAME="${INSTANCE_NAME:-MAPDL_0}"

debug "Configuration:"
debug "  PyMAPDL Port: ${PYMAPDL_PORT}"
debug "  DPF Port: ${DPF_PORT}"
debug "  Enable DPF: ${ENABLE_DPF_SERVER}"
debug "  Instance Name: ${INSTANCE_NAME}"

# Show running Docker containers
debug ""
debug "Docker services:"
docker ps > "docker_ps.log" 2>&1 &

sleep 1  # Give it a moment to populate the log
debug_file "docker_ps.log" || echo "Failed to get Docker services"


# Show processes in container (for debugging)
debug ""
debug "Container processes:"
{ docker exec "${INSTANCE_NAME}" ps aux > "docker_ps_aux.log" 2>&1 & } || debug "Failed to get processes from container ${INSTANCE_NAME}"
sleep 1  # Give it a moment to populate the log
debug_file "docker_ps_aux.log" || echo "Failed to get processes from container ${INSTANCE_NAME}"

# Wait for PyMAPDL gRPC port
echo -e "\n"
echo "Waiting for PyMAPDL gRPC service on port ${PYMAPDL_PORT}..."

# Wait up to 60 seconds for the port to be open
TIMEOUT=${TIMEOUT:-60}
if ! [[ "$TIMEOUT" =~ ^[0-9]+$ ]] || [ "$TIMEOUT" -lt 1 ]; then
    echo "⚠️  Invalid timeout value, using default 60 seconds"
    TIMEOUT=60
fi

ELAPSED=0
while ! nc -z localhost "${PYMAPDL_PORT}"; do
    if [ $ELAPSED -ge "$TIMEOUT" ]; then
        echo "❌ Timeout waiting for PyMAPDL port ${PYMAPDL_PORT}"
        exit 1
    fi
    sleep 1
    ELAPSED=$((ELAPSED + 1))
done

echo "✅ PyMAPDL gRPC service is ready on port ${PYMAPDL_PORT}"

# Wait for DPF port if enabled
if [[ "${ENABLE_DPF_SERVER}" == "true" ]]; then
    echo ""
    echo "Waiting for DPF service on port ${DPF_PORT}..."

    ELAPSED=0
    while ! nc -z localhost "${DPF_PORT}"; do
        if [ $ELAPSED -ge "$TIMEOUT" ]; then
            echo "⚠️  Timeout waiting for DPF port ${DPF_PORT}"
            echo "DPF server may not have started correctly"
            break
        fi
        sleep 0.5
        ELAPSED=$((ELAPSED + 1))
    done

    if nc -z localhost "${DPF_PORT}"; then
        echo "✅ DPF service is ready on port ${DPF_PORT}"
    fi
else
    echo ""
    echo "DPF service check skipped (not enabled)"
fi

echo ""
echo "==================================="
echo "✅ All Services Ready"
echo "==================================="
