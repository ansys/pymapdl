
mkdir "$LOG_NAMES" && echo "Successfully generated directory $LOG_NAMES"

echo "Copying the log files..."
mv *.log ./"$LOG_NAMES"/ || echo "No log files could be found"
mv *apdl.out ./"$LOG_NAMES"/ || echo "No APDL log files could be found"
mv *pymapdl.apdl ./"$LOG_NAMES"/ || echo "No PYMAPDL APDL log files could be found"

echo "Copying the profiling files..."
mkdir -p ./"$LOG_NAMES"/prof
mv prof/* ./"$LOG_NAMES"/prof || echo "No profile files could be found"

echo "Copying the JSONL files..."
mv *.jsonl ./"$LOG_NAMES"/ || echo "No JSONL files could be found"

ls -la ./"$LOG_NAMES"

echo "Tar files..."
tar --remove-files -cvzf ./"$LOG_NAMES".tgz ./"$LOG_NAMES" || echo "Failed to compress"