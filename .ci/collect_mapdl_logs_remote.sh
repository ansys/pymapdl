#!/bin/bash
if [[ $MAPDL_VERSION == *"ubuntu"* ]] ; then
    echo "It is an ubuntu based image"
    export FILE=/jobs/file
    export WDIR='/jobs/'
else
    echo "It is a CentOS based image"
    export FILE=file
    export WDIR=""
fi;

mkdir "$LOG_NAMES" && echo "Successfully generated directory $LOG_NAMES"

####
echo "Collecting MAPDL logs..."

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "mkdir -p /mapdl_logs && echo 'Successfully created directory inside docker container'") || echo "Failed to create a directory inside docker container for logs."

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "mv ./*.log /mapdl_logs") || echo "Failed to move the logs files."

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "ps aux > /mapdl_logs/docker_processes_end.log") || echo "Failed to get the processes from the docker container"

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.out' > /dev/null ;then mv -f /file*.out /mapdl_logs && echo 'Successfully moved out files.'; fi") || echo "Failed to move the 'out' files into a local file"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.err' > /dev/null ;then mv -f /file*.err /mapdl_logs && echo 'Successfully moved err files.'; fi") || echo "Failed to move the 'err' files into a local file"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.log' > /dev/null ;then mv -f /file*.log /mapdl_logs && echo 'Successfully moved log files.'; fi") || echo "Failed to move the 'log' files into a local file"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$WDIR*.crash' > /dev/null ;then mv -f $WDIR*.crash /mapdl_logs && echo 'Successfully moved crash files.'; fi") || echo "Failed to move the 'crash' files into a local file"

docker cp "$MAPDL_INSTANCE":/home/mapdl/dpf_logs ./"$LOG_NAMES"/ || echo "Failed to copy the 'dpf_logs' files into a local directory"
docker cp "$MAPDL_INSTANCE":/mapdl_logs/. ./"$LOG_NAMES"/. || echo "Failed to copy the 'log-build-docs' files into a local directory"

####
echo "Collecting local build logs..."
ls -la

docker ps > /"$LOG_NAMES"/docker_ps_end.log || echo "Failed to print the docker ps"

echo "Collecting logs..."
mv ./*.log ./"$LOG_NAMES"/ || echo "MAPDL run docker log not found."

echo "Moving the profiling files..."
mkdir -p ./"$LOG_NAMES"/prof
mv prof/* ./"$LOG_NAMES"/prof || echo "No profile files could be found"

echo "Moving the JSONL files..."
mv ./*.jsonl ./"$LOG_NAMES"/ || echo "No JSONL files could be found"

echo "Collecting file structure..."
ls -R > ./"$LOG_NAMES"/files_structure.txt || echo "Failed to copy file structure to a file"

echo "Collecting docker file structure..."
docker exec "$MAPDL_INSTANCE" /bin/bash -c "ls -R" > ./"$LOG_NAMES"/docker_files_structure.txt || echo "Failed to copy the docker structure into a local file"

echo "Tar files..."
tar --remove-files -cvzf ./"$LOG_NAMES".tgz ./"$LOG_NAMES" || echo "Failed to compress"