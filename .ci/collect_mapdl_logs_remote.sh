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
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.out' > /dev/null ;then cp -f /file*.out /mapdl_logs && echo 'Successfully copied out files.'; fi") || echo "Failed to copy the 'out' files into a local file"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.err' > /dev/null ;then cp -f /file*.err /mapdl_logs && echo 'Successfully copied err files.'; fi") || echo "Failed to copy the 'err' files into a local file"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.log' > /dev/null ;then cp -f /file*.log /mapdl_logs && echo 'Successfully copied log files.'; fi") || echo "Failed to copy the 'log' files into a local file"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$WDIR*.crash' > /dev/null ;then cp -f /*.crash /mapdl_logs && echo 'Successfully copied crash files.'; fi") || echo "Failed to copy the 'crash' files into a local file"

docker cp "$MAPDL_INSTANCE":/mapdl_logs/. ./"$LOG_NAMES"/. || echo "Failed to copy the 'log-build-docs' files into a local directory"

####
echo "Collecting local build logs..."

echo "Collecting docker run log..."
cp log.txt ./"$LOG_NAMES"/log.txt || echo "MAPDL run docker log not found."

echo "Copying docker launch log..."
cp mapdl_launch_0.log ./"$LOG_NAMES"/mapdl_launch_0.log || echo "MAPDL launch docker log not found."
cp mapdl_launch_1.log ./"$LOG_NAMES"/mapdl_launch_1.log || echo "MAPDL launch docker log not found."

echo "Copying the profiling files..."
cp -r prof ./"$LOG_NAMES"/prof || echo "No profile files could be found"

echo "Copying the JSONL files..."
cp *.jsonl ./"$LOG_NAMES"/ || echo "No JSONL files could be found"

echo "Collecting file structure..."
ls -R > ./"$LOG_NAMES"/files_structure.txt || echo "Failed to copy file structure to a file"

echo "Collecting docker file structure..."
docker exec "$MAPDL_INSTANCE" /bin/bash -c "ls -R" > ./"$LOG_NAMES"/docker_files_structure.txt || echo "Failed to copy the docker structure into a local file"

echo "Tar files..."
tar cvzf ./"$LOG_NAMES".tgz ./"$LOG_NAMES" || echo "Failed to compress"