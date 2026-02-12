#!/bin/bash
# Wait for MAPDL and DPF services to be ready
set -e

echo "==================================="
echo "Waiting for Services"
echo "==================================="

# Set defaults
PYMAPDL_PORT="${PYMAPDL_PORT:-50052}"
DPF_PORT="${DPF_PORT:-50056}"
ENABLE_DPF_SERVER="${ENABLE_DPF_SERVER:-false}"
INSTANCE_NAME="${INSTANCE_NAME:-MAPDL_0}"

echo "Configuration:"
echo "  PyMAPDL Port: ${PYMAPDL_PORT}"
echo "  DPF Port: ${DPF_PORT}"
echo "  Enable DPF: ${ENABLE_DPF_SERVER}"
echo "  Instance Name: ${INSTANCE_NAME}"

# Show running Docker containers
echo ""
echo "Docker services:"
docker ps

# Show processes in container (for debugging)
echo ""
echo "Container processes:"
docker exec "${INSTANCE_NAME}" ps aux || echo "Could not list container processes"

# Wait for PyMAPDL gRPC port
echo ""
echo "Waiting for PyMAPDL gRPC service on port ${PYMAPDL_PORT}..."

# Try to connect to check if port is open
nc -v -z localhost "${PYMAPDL_PORT}" 2>&1 || true

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
