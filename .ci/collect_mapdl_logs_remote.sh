#!/bin/bash

set +e  # Do not stop if a file is missing, just report it.

# Colors for error/warning messages (GitHub Actions renders ANSI colors).
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No color

if [[ $MAPDL_VERSION == *"ubuntu"* ]] ; then
    echo "It is an ubuntu based image"
    export FILE=/jobs/file
    export WDIR='/jobs/'
else
    echo "It is a CentOS based image"
    export FILE=/file
    export WDIR=""
fi;

{ mkdir -p "$LOG_NAMES" && echo "Successfully generated directory $LOG_NAMES"; } || { echo -e "${RED}Failed to create directory $LOG_NAMES${NC}"; exit 1; }

# Helper function to display files with a pattern inside collapsible GitHub
# Actions log groups. Each group is always closed, even if a file cannot be
# shown, to avoid leaving nested/unclosed groups in the workflow log.
display_files() {
    local pattern=$1
    local file_type=$2
    local file_pattern="./$LOG_NAMES/$pattern"
    echo "Displaying files with pattern $pattern: $file_pattern"
    if compgen -G "$file_pattern" > /dev/null; then
        for f in $file_pattern; do
            echo "::group:: $file_type file $f"
            if [ -f "$f" ]; then
                cat "$f"
            else
                echo -e "${RED}Failed to show $file_type file: '$f' does not exist.${NC}"
            fi
            echo "::endgroup::"
        done
    else
        echo -e "${YELLOW}No $pattern files to print.${NC}"
    fi
}

###############################################################################
echo "Collecting MAPDL logs from remote container..."

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "mkdir -p /mapdl_logs && echo 'Successfully created directory inside docker container'") || echo -e "${RED}Failed to create a directory inside docker container for logs.${NC}"

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "mv ./*.log /mapdl_logs" 2>/dev/null) && echo "Successfully moved the logs files." || echo -e "${YELLOW}Failed to move the logs files.${NC}"

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "ps aux > /mapdl_logs/docker_processes_end.log") && echo "Successfully got the processes from the docker container" || echo -e "${RED}Failed to get the processes from the docker container${NC}"

(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.out' > /dev/null; then mv -f $FILE*.out /mapdl_logs && echo 'Successfully moved out files.'; fi") || echo -e "${YELLOW}Failed to move the 'out' files into a local file${NC}"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.err' > /dev/null; then mv -f $FILE*.err /mapdl_logs && echo 'Successfully moved err files.'; fi") || echo -e "${YELLOW}Failed to move the 'err' files into a local file${NC}"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$FILE*.log' > /dev/null; then mv -f $FILE*.log /mapdl_logs && echo 'Successfully moved log files.'; fi") || echo -e "${YELLOW}Failed to move the 'log' files into a local file${NC}"
(docker exec "$MAPDL_INSTANCE" /bin/bash -c "if compgen -G '$WDIR*.crash' > /dev/null; then mv -f $WDIR*.crash /mapdl_logs && echo 'Successfully moved crash files.'; fi") || echo -e "${YELLOW}Failed to move the 'crash' files into a local file${NC}"

docker cp "$MAPDL_INSTANCE":/home/mapdl/dpf_logs ./"$LOG_NAMES"/ && echo "Successfully copied the 'dpf_logs' files into a local directory" || echo -e "${YELLOW}Failed to copy the 'dpf_logs' files into a local directory${NC}"
docker cp "$MAPDL_INSTANCE":/mapdl_logs/. ./"$LOG_NAMES"/. && echo "Successfully copied the $LOG_NAMES files into a local directory" || echo -e "${RED}Failed to copy the $LOG_NAMES files into a local directory${NC}"

###############################################################################
echo "Collecting local build logs..."
ls -la

docker ps > ./"$LOG_NAMES"/docker_ps_end.log && echo "Successfully printed the docker ps" || echo -e "${RED}Failed to print the docker ps${NC}"

###############################################################################
echo "Collecting and printing logs..."
mv ./*.log ./"$LOG_NAMES"/ 2>/dev/null && echo "Successfully moved log files." || echo -e "${YELLOW}MAPDL run docker log not found.${NC}"

display_files "*.log" "Log"
display_files "*.err" "Error"
display_files "*.out" "Output"

###############################################################################
echo "Moving the profiling files..."
mkdir -p ./"$LOG_NAMES"/prof
mv prof/* ./"$LOG_NAMES"/prof 2>/dev/null && echo "Successfully moved profile files." || echo -e "${YELLOW}No profile files could be found${NC}"

echo "Moving the JSONL files..."
mv ./*.jsonl ./"$LOG_NAMES"/ 2>/dev/null && echo "Successfully moved JSONL files." || echo -e "${YELLOW}No JSONL files could be found${NC}"

###############################################################################
echo "::group:: Display files structure"
echo "Collecting file structure..."
ls -R
ls -R > ./"$LOG_NAMES"/files_structure.txt && echo "Generated file structure" || echo -e "${RED}Failed to copy file structure to a file${NC}"
echo "::endgroup::"

echo "::group:: Display files structure"
echo "Collecting docker file structure..."
docker exec "$MAPDL_INSTANCE" /bin/bash -c "ls -R"
docker exec "$MAPDL_INSTANCE" /bin/bash -c "ls -R > /tmp/docker_ls.txt" && docker cp "$MAPDL_INSTANCE":/tmp/docker_ls.txt ./"$LOG_NAMES"/docker_files_structure.txt && echo "Generated docker file structure" || echo -e "${RED}Failed to copy the docker structure into a local file${NC}"
echo "::endgroup::"

###############################################################################
echo "Tar files..."
tar -cvzf ./"$LOG_NAMES".tgz ./"$LOG_NAMES" && echo "Successfully compressed logs." || echo -e "${RED}Failed to compress${NC}"
