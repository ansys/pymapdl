# PyMAPDL docker image that runs the tests.

# Dummy default so there is no error if not set.
# It needs to be set here because we are using it
# later on the FROM.
ARG DOCKER_IMAGE="mapdl:latest"

#######################################################
FROM ubuntu:22.04 AS python-main
#######################################################

ARG USE_LOCAL_REPO=yes
ARG PYTHON_VERSION=3.11

ENV USE_LOCAL_REPO=${USE_LOCAL_REPO}
ENV UV_PYTHON=${PYTHON_VERSION}

# Set workdir
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && \
    apt-get install -y  \
    libgl1-mesa-glx \
    xvfb \
    libgomp1 \
    graphviz \
    git \
    openssh-client \
    curl
    # Installing uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ansys/pymapdl.git . \
    && git config --global --add safe.directory /workspace

# Set PATH to include uv
ENV PATH="/root/.local/bin:$PATH"
RUN uv --version

# Configuration
# -------------
# Variable for running as if it were on CICD while testing
ENV ON_CI=True
# To simulate running on local machine
ENV ON_LOCAL=False
# For tests that check if running on ubuntu.
ENV ON_UBUNTU=False
# Some tests check if running on student machines
ENV ON_STUDENT=False

# PyMAPDL testing env vars
# ------------------------
# To work without a screen.
ENV PYANSYS_OFF_SCREEN=True
# Enable debugging for PyMAPDL
ENV PYMAPDL_DEBUG_TESTING=True
# To connect to an already alive or remote MAPDL instance
ENV PYMAPDL_START_INSTANCE=False
# Set MAPDL port to connect to
ENV PYMAPDL_PORT=50052
# Use insecure gRPC transport for testing. This is needed to connect to the remote MAPDL instance, which is what we want to do in this container.
ENV PYMAPDL_GRPC_TRANSPORT=insecure

# DPF testing
# -----------
# Not testing against DPF
#
# To connect to a remote DPF server
ENV DPF_START_SERVER=False
# Simulate not having DPF
ENV HAS_DPF=False
# Not testing DPF-Results backend
ENV TEST_DPF_BACKEND=False
# MAPDL and DPF are running on the same container
ENV ON_SAME_CONTAINER=False

# Pytest settings
# ---------------
ENV PYTEST_ARGUMENTS='--ignore_image_cache'

# Setting entrypoint
# ------------------
COPY start.sh /
RUN chmod +x /start.sh

ENTRYPOINT [ "/bin/bash", "/start.sh" ]
SHELL [ "/bin/bash" ]

#######################################################
FROM python-main AS test-clone-pymapdl
#######################################################

ENV USE_LOCAL_REPO=false

#######################################################
FROM python-main AS test-local-pymapdl
#######################################################

ENV USE_LOCAL_REPO=true

# Remove cloned repo so the local repo can be mounted.
RUN rm -rf /workspace/* >/dev/null 2>&1

#######################################################
FROM ${DOCKER_IMAGE} AS mapdl-local-container-pymapdl
#######################################################
#
# WARNING: This container is designed to work using an Ubuntu base image.
#
ARG PYTHON_VERSION=3.11

ENV UV_PYTHON=${PYTHON_VERSION}
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# OS configuration
# ----------------
# Installing dependencies
USER root

RUN apt-get update && \
    apt-get install -y  \
    libgl1-mesa-glx \
    xvfb \
    libgomp1 \
    graphviz \
    git \
    openssh-client \
    curl \
    # Installing uv
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set PATH to include uv for root user
ENV PATH="/root/.local/bin:$PATH"

RUN USER=mapdl && chown -R $USER:$USER /home/mapdl
USER mapdl

# Clone to install the libraries needed
RUN git clone https://github.com/ansys/pymapdl.git .

ENV PATH="$HOME/.local/bin:$PATH"
RUN uv --version

# Configuration
# -------------
# Variable for running as if it were on CICD while testing
ENV ON_CI=True
# To simulate running on local machine
ENV ON_LOCAL=True
# For tests that check if running on ubuntu.
ENV ON_UBUNTU=False
# Some tests check if running on student machines
ENV ON_STUDENT=False

# PyMAPDL testing env vars
# ------------------------
# To work without a screen.
ENV PYANSYS_OFF_SCREEN=True
# Enable debugging for PyMAPDL
ENV PYMAPDL_DEBUG_TESTING=True
# Force launching an instance of MAPDL. This is needed to test the connection to a remote instance, which is what we want to do in this container.
ENV PYMAPDL_START_INSTANCE=True
# Set MAPDL port to connect to
ENV PYMAPDL_PORT=50052
# Set additional switches for MAPDL. In this case, we are enabling MPI with OpenMPI.
ENV PYMAPDL_ADDITIONAL_SWITCHES="-mpi openmpi"
# DPF testing
# -----------
# Not testing against DPF
#
# To connect to a remote DPF server
ENV DPF_START_SERVER=False
# Simulate not having DPF
ENV HAS_DPF=False
# Not testing DPF-Results backend
ENV TEST_DPF_BACKEND=False
# MAPDL and DPF are running on the same container
ENV ON_SAME_CONTAINER=False

# Pytest settings
# ---------------
ENV PYTEST_ARGUMENTS='--ignore_image_cache'

# Setting entrypoint
# ------------------
USER root
COPY start.sh /
RUN chmod +x /start.sh
USER mapdl

ENTRYPOINT [ "/bin/bash", "/start.sh" ]
SHELL [ "/bin/bash" ]
