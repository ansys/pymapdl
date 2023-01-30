#!/bin/bash
echo "Activating local environment"
FILE=./.venv/bin/activate
if test -f "$FILE"; then
    echo "Virtual environment ($FILE) exists."
    echo "Activating..."
    source $FILE
    echo "Virtual environment activated"
else
    echo "Virtual environment was not found."
fi

source ./.venv/bin/activate

echo "Checking if the ANSYSLMD_LICENSE_FILE variable is defined"

if [[ -z "${ANSYSLMD_LICENSE_FILE}" ]]; then
  # MY_SCRIPT_VARIABLE="Some default value because ANSYSLMD_LICENSE_FILE is undefined"
  echo "ANSYSLMD_LICENSE_FILE is not defined"
  read -p "Enter port (default is 1055): " port
  port=${port:-1055}
  read -p "Enter server (i.e. XXX.XX.XX.XX): " server
  export ANSYSLMD_LICENSE_FILE="${server}:${port}"
  printf "\n%s\n" "ANSYSLMD_LICENSE_FILE=${port}@${server}" >> ~/.bashrc
  set ANSYSLMD_LICENSE_FILE="${server}:${port}"
  source ~/.bashrc

else
  # MY_SCRIPT_VARIABLE="${ANSYSLMD_LICENSE_FILE}"
  echo "ANSYSLMD_LICENSE_FILE is defined as ${ANSYSLMD_LICENSE_FILE}"
fi
