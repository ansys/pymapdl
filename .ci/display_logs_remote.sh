#!/bin/bash

echo "::group:: Display files structure" && ls -R && echo "::endgroup::"


echo "::group:: Display files structure" && docker exec "$MAPDL_INSTANCE" /bin/bash -c "ls -R" && echo "::endgroup::" || echo "Failed to display the docker structure."


echo "::group:: Display docker run log" && cat log.txt && echo "::endgroup::"

# Displaying MAPDL files
FILE_PAT="./$LOG_NAMES/*.err"
if compgen -G "$FILE_PAT" > /dev/null ;then for f in $FILE_PAT; do echo "::group:: Error file $f" && cat "$f" && echo "::endgroup::" ; done; fi || echo "Failed to display the 'err' files."

FILE_PAT="./$LOG_NAMES/*.log"
if compgen -G "$FILE_PAT" > /dev/null ;then for f in $FILE_PAT; do echo "::group:: Log file $f" && cat "$f" && echo "::endgroup::" ; done; fi || echo "Failed to display the 'log' files."

FILE_PAT="./$LOG_NAMES/*.out"
if compgen -G "$FILE_PAT" > /dev/null ;then for f in $FILE_PAT; do echo "::group:: Output file $f" && cat "$f" && echo "::endgroup::" ; done; fi || echo "Failed to display the 'output' files."
