FROM ghcr.io/ansys/mapdl:v24.1-ubuntu-student
ENV USERNAME=mapdl
USER root

# General libraries
ENV DEBIAN_FRONTEND=noninteractive
ENV ON_CODESPACES=true
ENV CODESPACES_MODE=notebook
ENV DISPLAY=":0"

# Installing libs for testing and docs
RUN apt-get -qq update &&  apt install -qq -y libgl1-mesa-glx xvfb libgomp1 && \
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

# Copying files needed for installation
COPY requirements.txt requirements.txt

# Copy example
COPY example-bracket_static.ipynb example-bracket_static.ipynb

# Installing Python environment
RUN \
    # Installing PIPX so we can make jupyter-lab generally available
    python3 -m pip install --user pipx && \ 
    export PATH=/home/mapdl/.local/bin:$PATH && \
    echo 'export PATH=/home/mapdl/.local/bin:$PATH' >> ~/.bashrc && \
    pipx install jupyterlab && \
    # creating venv for pymapdl
    python3.10 -m venv ./.venv && \
    . ./.venv/bin/activate && \
    # Installing pymapdl
    pip install ansys-mapdl-core && \
    # Installing python dependencies
    pip install pre-commit && \
    pip install -r requirements.txt && \
    pip install "trame_jupyter_extension<2" && \
    # Setting bash profile file
    echo 'source ./.venv/bin/activate' >> ~/.bashrc && \
    # Clean up
    rm requirements.txt

WORKDIR /home/$USERNAME/pymapdl
