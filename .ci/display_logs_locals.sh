#!/bin/bash
# display_logs_locals.sh
#
# This script displays local log files generated during CI or local development runs.
# It is intended to help developers and CI systems quickly access and review logs
# for debugging and verification purposes.
#
# Usage:
#     ./display_logs_locals.sh
#
# Typical log directories or files displayed include:
#     - Any other relevant log files in the workspace
#
# Modify this script as needed to include additional log files or directories.

set +e  # Do not stop if a file is missing, just report it.
LOG_NAMES="${LOG_NAMES:-logs}"

# Colors for error/warning messages (GitHub Actions renders ANSI colors).
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No color

#####
# Displaying a file inside a collapsible GitHub Actions log group.
# The group is always closed, even if the file cannot be shown, to avoid
# leaving nested/unclosed groups in the workflow log.
display_file () {
    local file_pat="$1"
    local file_description="$2"

    echo "::group:: $file_description: $file_pat"
    if [ -f "$file_pat" ]; then
        cat "$file_pat"
    else
        printf '%b\n' "${RED}Failed to show $file_description file: '$file_pat' does not exist.${NC}"
        printf '%b\n' "${YELLOW}If you expect this file, enable it with PYMAPDL_DEBUG_TESTING=true (or 'True').${NC}"
    fi
    echo "::endgroup::"
}

#####
# Displaying files matching a glob pattern (the crash file name is derived
# from the MAPDL jobname, so it is not a fixed path like the other logs).
display_files () {
    local pattern="$1"
    local file_description="$2"
    local file_pattern="./$LOG_NAMES/$pattern"

    if compgen -G "$file_pattern" > /dev/null; then
        for f in $file_pattern; do
            display_file "$f" "$file_description"
        done
    else
        printf '%b\n' "${YELLOW}No $pattern files to print.${NC}"
    fi
}

#####
# Displaying files
display_file "./$LOG_NAMES/pymapdl.log" "PyMAPDL log"
display_file "./$LOG_NAMES/pymapdl.apdl" "PyMAPDL APDL log"
display_file "./$LOG_NAMES/apdl.out" "MAPDL Output"
display_files "*.crash" "Crash"
