FROM ghcr.io/ansys/mapdl:v24.1-ubuntu-student

USER root

# General libraries
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -qq update && apt-get -qq install -y locales && locale-gen "en_US.UTF-8" && update-locale LC_ALL="en_US.UTF-8"

# Installing libs for testing and docs
RUN apt install -qq -y zip pandoc libgl1-mesa-glx xvfb texlive-latex-extra latexmk graphviz texlive-xetex

# Setting up locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && printf "export LANG=en_US.UTF-8" "export LANGUAGE=en_US:en" "export LC_ALL=en_US.UTF-8" >> ~/.bashrc

# Clean up
RUN apt-get -qq clean  && rm -rf /var/lib/apt/lists/*

# Installing Python environment
RUN mkdir /home/mapdl/pymapdl && \
    python3.10 -m venv /home/mapdl/pymapdl/.venv && \
    . /home/mapdl/pymapdl/.venv/bin/activate && \
    pip install pre-commit && \
    pip install ansys-mapdl-core && \
    pip install -r .devcontainer/codespaces-docs/requirements.txt && \
    echo -e '\nsource /home/mapdl/pymapdl/.venv/bin/activate' >> ~/.bashrc

USER mapdl
