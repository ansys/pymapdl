#!/bin/bash
#
# Script Name: collect_mapdl_logs_locals.sh
# Description: Collects MAPDL log files from local runs for debugging or archiving purposes.
#
# Usage:
#   bash .ci/collect_mapdl_logs_locals.sh
#
# Required Environment Variables:
#   MAPDL_LOGS_DIR   - Directory containing MAPDL log files to collect.
#   OUTPUT_DIR       - Directory where collected logs will be copied or archived.
#
# Optional Environment Variables:
#   LOG_FILE_PATTERN - Pattern to match log files (default: "*.log").
#
# Example:
#   export MAPDL_LOGS_DIR=~/tmp/ansys_tmp/logs
#   export OUTPUT_DIR=~/collected_logs
#   bash .ci/collect_mapdl_logs_locals.sh
#
# Note:
#   Ensure you have the necessary permissions to read from MAPDL_LOGS_DIR and write to

mkdir "$LOG_NAMES" && echo "Successfully generated directory $LOG_NAMES"

echo "Copying the log files..."
mv ./*.log ./"$LOG_NAMES"/ || echo "No log files could be found"
mv ./*apdl.out ./"$LOG_NAMES"/ || echo "No APDL log files could be found"
mv ./*pymapdl.apdl ./"$LOG_NAMES"/ || echo "No PYMAPDL APDL log files could be found"

echo "Copying the profiling files..."
mkdir -p ./"$LOG_NAMES"/prof
mv prof/* ./"$LOG_NAMES"/prof || echo "No profile files could be found"

echo "Copying the JSONL files..."
mv ./*.jsonl ./"$LOG_NAMES"/ || echo "No JSONL files could be found"

ls -la ./"$LOG_NAMES"

echo "Tar files..."
tar --remove-files -cvzf ./"$LOG_NAMES".tgz ./"$LOG_NAMES" || echo "Failed to compress"
