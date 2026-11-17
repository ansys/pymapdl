#!/bin/sh
# Numeric diagnostics only: do not expose IP addresses or process command lines.
set -eu

printf 'timestamp_utc='
date -u '+%Y-%m-%dT%H:%M:%SZ'
printf 'open_fd_count='
find /proc/[0-9]*/fd -mindepth 1 -maxdepth 1 -printf '.' 2>/dev/null | wc -c
printf 'socket_fd_count='
find /proc/[0-9]*/fd -mindepth 1 -maxdepth 1 -lname 'socket:*' -printf '.' 2>/dev/null | wc -c

# Linux TCP state 01=ESTABLISHED, 06=TIME_WAIT, 08=CLOSE_WAIT, 0A=LISTEN.
# C384 is container port 50052, the MAPDL gRPC listener.
awk 'FNR > 1 {
    all[$4]++
    split($2, local_endpoint, ":")
    if (local_endpoint[2] == "C384") grpc[$4]++
}
END {
    for (state in all) print "tcp_state_" state "=" all[state]
    for (state in grpc) print "grpc_tcp_state_" state "=" grpc[state]
}' /proc/net/tcp /proc/net/tcp6 | sort

printf 'per_process_open_fds\n'
for directory in /proc/[0-9]*; do
    [ -d "${directory}/fd" ] || continue
    printf '%s ' "${directory##*/}"
    find "${directory}/fd" -mindepth 1 -maxdepth 1 -printf '.' 2>/dev/null | wc -c
done
