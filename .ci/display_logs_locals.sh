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
#     - logs-local-latest-ubuntu-student/apdl.out
#     - Any other relevant log files in the workspace
# 
# Modify this script as needed to include additional log files or directories.


#####
# Displaying files
FILE_PAT=./"$LOG_NAMES"/pymapdl.log
FILE_DESCRIPTION="PyMAPDL log"

if compgen -G "$FILE_PAT" > /dev/null ;then for f in "$FILE_PAT"; do echo "::group:: $FILE_DESCRIPTION: $f" && cat "$f" && echo "::endgroup::" ; done; fi || echo "Failed to show $FILE_DESCRIPTION file"

#####
FILE_PAT=./"$LOG_NAMES"/pymapdl.apdl
FILE_DESCRIPTION="PyMAPDL APDL log"

if compgen -G "$FILE_PAT" > /dev/null ;then for f in "$FILE_PAT"; do echo "::group:: $FILE_DESCRIPTION: $f" && cat "$f" && echo "::endgroup::" ; done; fi || echo "Failed to show $FILE_DESCRIPTION file"

#####
FILE_PAT=./"$LOG_NAMES"/apdl.out
FILE_DESCRIPTION="MAPDL Output"

if compgen -G "$FILE_PAT" > /dev/null ;then for f in "$FILE_PAT"; do echo "::group:: $FILE_DESCRIPTION: $f" && cat "$f" && echo "::endgroup::" ; done; fi || echo "Failed to show $FILE_DESCRIPTION file"