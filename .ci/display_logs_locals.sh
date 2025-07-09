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

(echo "::group:: $FILE_DESCRIPTION: $FILE_PAT" && cat "$FILE_PAT" && echo "::endgroup::") || echo "Failed to show $FILE_DESCRIPTION file"

#####
FILE_PAT=./"$LOG_NAMES"/pymapdl.apdl
FILE_DESCRIPTION="PyMAPDL APDL log"

(echo "::group:: $FILE_DESCRIPTION: $FILE_PAT" && cat "$FILE_PAT" && echo "::endgroup::") || echo "Failed to show $FILE_DESCRIPTION file"

#####
FILE_PAT=./"$LOG_NAMES"/apdl.out
FILE_DESCRIPTION="MAPDL Output"

(echo "::group:: $FILE_DESCRIPTION: $FILE_PAT" && cat "$FILE_PAT" && echo "::endgroup::") || echo "Failed to show $FILE_DESCRIPTION file"