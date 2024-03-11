

echo "::group:: Display files structure" && ls -R && echo "::endgroup::"


echo "::group:: Display files structure" && docker exec $MAPDL_INSTANCE /bin/bash -c "ls -R" && echo "::endgroup::" || echo "Failed to display the docker structure."


echo "::group:: Display docker run log" && cat log.txt && echo "::endgroup::"

# Displaying MAPDL files
if compgen -G './$LOG_NAMES/*.err' > /dev/null ;then for f in ./$LOG_NAMES/*.err; do echo "::group:: Error file $f" && cat $f && echo "::endgroup::" ; done; fi || echo "Failed to display the 'out' files."
if compgen -G './$LOG_NAMES/*.log' > /dev/null ;then for f in ./$LOG_NAMES/*.log; do echo "::group:: Log file $f" && cat $f && echo "::endgroup::" ; done; fi || echo "Failed to display the 'err' files."
if compgen -G './$LOG_NAMES/*.out' > /dev/null ;then for f in ./$LOG_NAMES/*.out; do echo "::group:: Output file $f" && cat $f && echo "::endgroup::" ; done; fi || echo "Failed to display the 'log' files."

