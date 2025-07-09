#! /bin/bash
# This script starts and stops a web server to serve the HTML documentation files.
# It uses Python's built-in HTTP server to serve files from the _build/html directory.
# Usage:
#   ./webserver.sh [stop] [PORT]
#
# If no arguments are provided, it will start the web server on port 8000.
#
#    ./webserver.sh
#
# If a port is specified as the second argument, it will start the web server on that port.
#
#     ./webserver.sh 8001
#
# If "stop" is passed as the first argument, it will stop any running web server.
#
#    ./webserver.sh stop      
#

RED="\033[91m"
GREEN="\033[92m"
BLUE="\033[94m"
BOLD="\033[1m"
END_FT="\033[0m"

ERROR="${RED}${BOLD}ERROR:${END_FT}${RED}"
INFO="${GREEN}${BOLD}INFO:${END_FT}${GREEN}"

# echo "You can input more options by appending to this command."


STOP="${1:-${STOP:-false}}"
PORT="${2:-${PORT:-8000}}"

if [[ "$STOP" == "stop" ]]; then
    pkill -9 -f 'm http.server' && echo -e "${BLUE}${BOLD}All web servers have been stopped.${END_FT}" || echo -e "${ERROR} Web server could not be stopped or does not exist.${END_FT}"
    exit 0
fi


LOG_FILE="$(pwd)/webserver.log"
echo "You can find the web server log in: $LOG_FILE"
echo "Web server logs" > "${LOG_FILE}"
echo "==============" >> "${LOG_FILE}"

(cd _build/html &> /dev/null ) || { echo -e "${ERROR} HTML docs files are not found!${END_FT}"; exit 1; }
which python &> /dev/null || { echo -e "${ERROR} Python is not available!${END_FT}" && exit 1; }

cd _build/html && python -m http.server "${PORT}" >> "${LOG_FILE}" 2>&1 & echo -n "$!" > webserver.pid

echo "The pid of the web server is $(cat webserver.pid)"
sleep 0.5

(grep -q "Traceback" < "$LOG_FILE" && echo -e "${ERROR} Starting the web server${END_FT}" && tail -n +3 "${LOG_FILE}" ) || \
    (echo -e "${INFO} Server started at port ${PORT}. ${END_FT}" && \
    echo -e "If you don't see a pop up with 'Open in browser'," && \
    echo -e "you can open the port from the 'PORTS' tab by" && \
    echo -e "clicking on the 'world' icon in the port ${PORT}." && \
    echo -e "${INFO} Remember to stop the server when you are done using 'stop_webserver.sh'.${END_FT}"
    )
