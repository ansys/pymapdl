#! /bin/bash
# Stopping webserver
pkill -9 -f 'm http.server' && echo "All webservers stopped" || echo "Webserver could not be stopped or does not exist"