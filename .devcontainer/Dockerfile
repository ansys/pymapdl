FROM ghcr.io/ansys/mapdl:v24.1-ubuntu-student

USER root

# General libraries
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y locales && locale-gen "en_US.UTF-8" && update-locale LC_ALL="en_US.UTF-8"

# Installing libs for testing
RUN apt install -y libgl1-mesa-glx xvfb

# Installing libs for doc building
RUN apt install -y zip pandoc libgl1-mesa-glx xvfb texlive-latex-extra latexmk graphviz texlive-xetex

# Setting up locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && printf "export LANG=en_US.UTF-8" "export LANGUAGE=en_US:en" "export LC_ALL=en_US.UTF-8" >> ~/.bashrc

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

USER mapdl
