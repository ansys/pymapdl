#!/bin/bash
# Waits for the MAPDL (and optionally DPF) gRPC ports to be reachable.
#
# Unlike a plain "poll the port forever" loop, this script also watches the
# state of the Docker container hosting MAPDL. Combined with the bounded
# `--restart on-failure:N` policy used in start_mapdl.sh, this lets the job
# fail fast with a clear diagnostic if the container keeps crashing instead
# of waiting on a port that will never open.

INSTANCE_NAME="${INSTANCE_NAME:-MAPDL_0}"
TIMEOUT="${TIMEOUT:-300}" # seconds

echo "::group:: Docker services" && docker ps && echo "::endgroup::"
echo "::group:: ps aux Output" && ps aux && echo "::endgroup::"

# Prints the container logs and its Docker state, then exits with an error.
fail_fast() {
    local reason="$1"
    echo "::group:: ${INSTANCE_NAME} container state"
    docker inspect "${INSTANCE_NAME}" --format 'Status: {{.State.Status}} | Restarting: {{.State.Restarting}} | RestartCount: {{.RestartCount}} | ExitCode: {{.State.ExitCode}} | Error: {{.State.Error}}' 2>&1
    echo "::endgroup::"
    echo "::group:: ${INSTANCE_NAME} container logs"
    docker logs "${INSTANCE_NAME}" 2>&1 || echo "Could not retrieve container logs."
    echo "::endgroup::"
    echo "::error::${reason}"
    exit 1
}

# Waits until the given port is reachable, failing fast (instead of looping
# forever) if the timeout is hit or the container is stuck restarting/dead.
wait_for_port() {
    local port="$1"
    local label="$2"
    local elapsed=0

    echo "::group:: Waiting for the ${label} port (${port}) to be open..."
    while ! nc -z localhost "${port}"; do
        # Detect a container that keeps crash-looping or has died instead of
        # burning the full timeout waiting on a port that will never open.
        local restart_count
        restart_count=$(docker inspect "${INSTANCE_NAME}" --format '{{.RestartCount}}' 2>/dev/null || echo "0")
        local status
        status=$(docker inspect "${INSTANCE_NAME}" --format '{{.State.Status}}' 2>/dev/null || echo "unknown")

        if [ "${status}" = "exited" ] || [ "${status}" = "dead" ]; then
            echo "::endgroup::"
            fail_fast "${INSTANCE_NAME} container has status '${status}' (restart policy exhausted) while waiting for the ${label} port."
        fi

        if [ "${restart_count}" -ge 3 ] 2>/dev/null; then
            echo "::endgroup::"
            fail_fast "${INSTANCE_NAME} container has restarted ${restart_count} times while waiting for the ${label} port. Giving up instead of crash-looping."
        fi

        if [ "${elapsed}" -ge "${TIMEOUT}" ]; then
            echo "::endgroup::"
            fail_fast "Timed out after ${TIMEOUT}s waiting for the ${label} port (${port}) to open."
        fi

        sleep 1
        elapsed=$((elapsed + 1))
    done
    echo "::endgroup::"
    echo "${label} service is up!"
}

wait_for_port "$PYMAPDL_PORT" "MAPDL"

echo "::group:: Waiting for the DPF port to be open..."
if [ "$TEST_DPF_BACKEND" = "true" ]; then
    wait_for_port "$DPF_PORT" "DPF"
else
    echo "TEST_DPF_BACKEND is not set to true, skipping DPF service check."
fi
echo "::endgroup::"
