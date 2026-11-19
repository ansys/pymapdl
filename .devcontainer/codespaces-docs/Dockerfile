FROM ghcr.io/ansys/mapdl:v25.2-ubuntu-cicd

ENV USERNAME=mapdl
USER root

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# General libraries
ENV DEBIAN_FRONTEND=noninteractive
ENV ON_CODESPACES=true
ENV CODESPACES_MODE=docs
ENV ON_LOCAL=true
ENV ON_UBUNTU=true
ENV ON_CI=true

# Installing libs for testing and docs
RUN apt-get -qq update && apt install -qq -y \
    graphviz \
    libgl1 \
    libglx-mesa0 \
    latexmk \
    pandoc \
    python3-pip \
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
RUN uv venv --python 3.12 ./.venv && \
    . ./.venv/bin/activate && \
    uv pip install pre-commit && \
    uv pip install ansys-mapdl-core && \
    uv pip install -r requirements.txt && \
    echo 'source ./.venv/bin/activate' >> ~/.bashrc && \
    rm requirements.txt

WORKDIR /home/$USERNAME/pymapdl
