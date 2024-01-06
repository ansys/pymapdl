#! /bin/bash

# echo "You can input more options by appending to this command."

LOG_FILE="$(pwd)/webserver.log"
echo "You can find the webserver log in: $LOG_FILE"
echo "Webserver logs" > $LOG_FILE
echo "==============" >> $LOG_FILE

$(cd _build/html && python -m http.server>> $LOG_FILE 2>&1) & echo -n "$!" > webserver.pid

echo "The pid of the webserver is $(cat webserver.pid)"
echo "Starting..."
sleep 0.5

cat $LOG_FILE | grep -q "Traceback" && echo "ERROR starting the webserver" && tail -n +3 $LOG_FILE || echo "Server started"
