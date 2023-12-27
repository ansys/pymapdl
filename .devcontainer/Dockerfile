FROM ghcr.io/ansys/mapdl:v24.1-ubuntu-student

USER root

# General libraries
ENV DEBIAN_FRONTEND=noninteractive

RUN echo "Hello! Welcome to PyMAPDL Codespaces! Please wait while we set your codespace :) " && apt-get -qq update && apt-get -qq install -y locales && locale-gen "en_US.UTF-8" && update-locale LC_ALL="en_US.UTF-8"

# Installing libs for testing and docs
RUN echo "Installing the packages required for developing, testing and documenting... " && apt install -qq -y libgl1-mesa-glx xvfb zip pandoc libgl1-mesa-glx xvfb texlive-latex-extra latexmk graphviz texlive-xetex

# Setting up locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && printf "export LANG=en_US.UTF-8" "export LANGUAGE=en_US:en" "export LC_ALL=en_US.UTF-8" >> ~/.bashrc

# Clean up
RUN echo "We are almost there!... " && apt-get -qq clean  && rm -rf /var/lib/apt/lists/* && mkdir /home/mapdl/pymapdl

USER mapdl
