#! /bin/bash

RED="\033[91m"
BOLD="\033[1m"
END_FT="\033[0m"

ERROR="${RED}${BOLD}ERROR:${END_FT}${RED}"

# echo "You can input more options by appending to this command."

LOG_FILE="$(pwd)/webserver.log"
echo "You can find the web server log in: $LOG_FILE"
echo "Web server logs" > "${LOG_FILE}"
echo "==============" >> "${LOG_FILE}"

(cd _build/html &> /dev/null ) || { echo -e "${ERROR} HTML docs files are not found!${END_FT}"; exit 1; }
python -m http.server >> "${LOG_FILE}" 2>&1 & echo -n "$!" > webserver.pid

echo "The pid of the web server is $(cat webserver.pid)"
sleep 0.5

(grep -q "Traceback" < "$LOG_FILE" && echo -e "${ERROR} Starting the web server${END_FT}" && tail -n +3 "${LOG_FILE}" ) || \
    (echo -e "${GREEN}Server started at port 8000." && \
    echo "If you don't see a pop up with 'Open in browser'," && \
    echo "you can open the port from the 'PORTS' tab by" && \
    echo "clicking on the 'world' icon in the port 8000.${END_FT}" )
