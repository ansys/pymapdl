#! /bin/bash
# Stopping webserver
pkill -9 -f 'm http.server' && echo "All web servers stopped" || echo "Web server could not be stopped or does not exist"