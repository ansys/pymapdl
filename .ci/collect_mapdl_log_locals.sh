
mkdir "$LOG_NAMES" && echo "Successfully generated directory $LOG_NAMES"

cp *.log ./"$LOG_NAMES"/ || echo "No log files could be found"

ls -la ./"$LOG_NAMES"
