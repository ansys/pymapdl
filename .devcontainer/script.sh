#!/bin/bash

echo "Checking if the ANSYSLMD_LICENSE_FILE variable is defined"

if [[ -z "${ANSYSLMD_LICENSE_FILE}" ]]; then
  echo "ANSYSLMD_LICENSE_FILE is not defined."

  # Read port
  read -p "Enter port (default is 1055): " port
  port=${port:-1055}

  # Read license server ip
  read -p "Enter server (i.e. XXX.XX.XX.XX): " server

  # Set env var for this terminal
  export ANSYSLMD_LICENSE_FILE="${server}:${port}"

  # Storing env var in .bashrc file so it is automatically loaded.
  printf "\n%s\n" "ANSYSLMD_LICENSE_FILE=${port}@${server}" >> ~/.bashrc

  # Activating the new configuration
  source ~/.bashrc

else
  echo "ANSYSLMD_LICENSE_FILE was found."
  echo "It is defined as ${ANSYSLMD_LICENSE_FILE}"

  # Storing env var in .bashrc file so it is automatically loaded.
  printf "\n%s\n" "ANSYSLMD_LICENSE_FILE=${ANSYSLMD_LICENSE_FILE}" >> ~/.bashrc

  # Activating the new configuration
  source ~/.bashrc

fi

# Installing libs for testing
apt update
apt install -y libgl1-mesa-glx xvfb

# Installing libs for doc building
apt update 
apt install -y zip pandoc libgl1-mesa-glx xvfb texlive-latex-extra latexmk graphviz texlive-xetex