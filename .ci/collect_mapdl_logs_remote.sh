#!/bin/bash
if [[ $MAPDL_VERSION == *"ubuntu"* ]] ; then
    echo "It is an ubuntu based image"
    export FILE=/jobs/file
    export WDIR='/jobs/'
else
    echo "It is a CentOS based image"
    export FILE=/file
    export WDIR=""
fi;

{ mkdir -p "$LOG_NAMES" && echo "Successfully generated directory $LOG_NAMES"; } || { echo "Failed to create directory $LOG_NAMES"; exit 1; }

# Helper function to display files with a pattern
display_files() {
    local pattern=$1
    local file_type=$2
    local file_pattern="./$LOG_NAMES/$pattern"
    echo "Displaying files with pattern $pattern: $file_pattern"
    if compgen -G "$file_pattern" > /dev/null; then
        for f in $file_pattern; do
            echo "::group:: $file_type file $f" && cat "$f" && echo "::endgroup::"
        done
        return 0
    else
        echo "No $pattern files to print."
    fi
}

###############################################################################
echo "Collecting MAPDL logs from remote container..."

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "mkdir -p /mapdl_logs && echo 'Successfully created directory inside docker container'") || echo "Failed to create a directory inside docker container for logs."

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "mv ./*.log /mapdl_logs") && echo "Successfully moved the logs files." || echo "Failed to move the logs files."

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "ps aux > /mapdl_logs/docker_processes_end.log") && echo "Successfully got the processes from the docker container" || echo "Failed to get the processes from the docker container"

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.out' > /dev/null; then mv -f $FILE*.out /mapdl_logs && echo 'Successfully moved out files.'; fi") || echo "Failed to move the 'out' files into a local file"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.err' > /dev/null; then mv -f $FILE*.err /mapdl_logs && echo 'Successfully moved err files.'; fi") || echo "Failed to move the 'err' files into a local file"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.log' > /dev/null; then mv -f $FILE*.log /mapdl_logs && echo 'Successfully moved log files.'; fi") || echo "Failed to move the 'log' files into a local file"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$WDIR*.crash' > /dev/null; then mv -f $WDIR*.crash /mapdl_logs && echo 'Successfully moved crash files.'; fi") || echo "Failed to move the 'crash' files into a local file"

docker cp "$MAPDL_INSTANCE":/home/mapdl/dpf_logs ./"$LOG_NAMES"/ && echo "Successfully copied the 'dpf_logs' files into a local directory" || echo "Failed to copy the 'dpf_logs' files into a local directory"
docker cp "$MAPDL_INSTANCE":/mapdl_logs/. ./"$LOG_NAMES"/. && echo "Successfully copied the $LOG_NAMES files into a local directory" || echo "Failed to copy the $LOG_NAMES files into a local directory"

###############################################################################
echo "Collecting local build logs..."
ls -la

docker ps > ./"$LOG_NAMES"/docker_ps_end.log && echo "Successfully printed the docker ps" || echo "Failed to print the docker ps"

###############################################################################
echo "Collecting and printing logs..."
mv ./*.log ./"$LOG_NAMES"/ && echo "Successfully moved log files." || echo "MAPDL run docker log not found."

display_files "*.log" "Log" && echo "Failed to display the '*.log' files."
display_files "*.err" "Error" && echo "Failed to display the '*.err' files."
display_files "*.out" "Output" && echo "Failed to display the '*.out' files."

###############################################################################
echo "Moving the profiling files..."
mkdir -p ./"$LOG_NAMES"/prof
mv prof/* ./"$LOG_NAMES"/prof && echo "Successfully moved profile files." || echo "No profile files could be found"

echo "Moving the JSONL files..."
mv ./*.jsonl ./"$LOG_NAMES"/ && echo "Successfully moved JSONL files." || echo "No JSONL files could be found"

###############################################################################
echo "::group:: Display files structure"
echo "Collecting file structure..."
ls -R
ls -R > ./"$LOG_NAMES"/files_structure.txt && echo "Generated file structure" || echo "Failed to copy file structure to a file"
echo "::endgroup::"

echo "::group:: Display files structure"
echo "Collecting docker file structure..."
docker exec "$MAPDL_INSTANCE" /bin/bash -c "ls -R"
docker exec "$MAPDL_INSTANCE" /bin/bash -c "ls -R > /tmp/docker_ls.txt" && docker cp "$MAPDL_INSTANCE":/tmp/docker_ls.txt ./"$LOG_NAMES"/docker_files_structure.txt && echo "Generated docker file structure" || echo "Failed to copy the docker structure into a local file"
echo "::endgroup::"

###############################################################################
echo "Tar files..."
tar --remove-files -cvzf ./"$LOG_NAMES".tgz ./"$LOG_NAMES" && echo "Successfully compressed logs." || echo "Failed to compress"
