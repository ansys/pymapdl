FROM ghcr.io/ansys/mapdl:v24.1-ubuntu-student

ENV USERNAME=mapdl
USER root

# General libraries
ENV DEBIAN_FRONTEND=noninteractive
ENV ON_CODESPACES=true
ENV CODESPACES_MODE=docs

# Installing libs for testing and docs
RUN apt-get -qq update && apt install -qq -y \
    graphviz \
    libgl1 \
    latexmk \
    libgl1-mesa-glx \
    pandoc \
    python3-pip \
    python3.11-venv \
    texlive-latex-extra \
    texlive-xetex \
    xvfb \
    zip \
    && \
    apt-get -qq clean  && rm -rf /var/lib/apt/lists/* && \
    usermod -s /bin/bash $USERNAME && \
    usermod -a -G sudo $USERNAME && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Setting up locales
RUN apt-get install -y --no-install-recommends locales && \
    locale-gen 'en_US.UTF-8' && \
    update-locale LC_ALL='en_US.UTF-8' && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    echo 'export LANG=en_US.UTF-8' >> ~/.bashrc && \
    echo 'export LANGUAGE=en_US:en' >> ~/.bashrc && \
    echo 'export LC_ALL=en_US.UTF-8' >> ~/.bashrc && \
    apt-get -qq clean  && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/$USERNAME/pymapdl

WORKDIR /home/$USERNAME
USER $USERNAME

COPY requirements.txt requirements.txt

# Installing Python environment
RUN python3.11 -m venv ./.venv && \
    . ./.venv/bin/activate && \
    pip install pre-commit && \
    pip install ansys-mapdl-core && \
    pip install -r requirements.txt && \
    echo 'source ./.venv/bin/activate' >> ~/.bashrc && \
    rm requirements.txt

WORKDIR /home/$USERNAME/pymapdl
