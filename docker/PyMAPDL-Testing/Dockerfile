# PyMAPDL docker image that runs the tests.

ARG DOCKER_IMAGE

#######################################################
FROM ubuntu:22.04 AS python-main
#######################################################

ARG USE_LOCAL_REPO=yes
ARG PYTHON_VERSION=3.11

ENV USE_LOCAL_REPO=${USE_LOCAL_REPO}

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
    openssh-client

# Clone to install the libraries needed
RUN git clone https://github.com/ansys/pymapdl.git .

RUN apt-get update && apt install -y \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install test dependencies
RUN \
    python${PYTHON_VERSION} -m pip install --upgrade pip && \
    pip install .[tests]

# Configuration
# -------------
# Variable for running as if it were on CICD while testing
ENV ON_CI=True
# Tu simulate running on local machine
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
ENV PYTEST_ARGUMENTS='-vvv -ra --color=yes --durations=30 --random-order --random-order-bucket=class --maxfail=10 --reruns 3 --reruns-delay 4 --cov=ansys.mapdl.core --cov-report=html --timeout=180 --profile-svg --profile --report-log-exclude-logs-on-passed-tests --strict-markers'

# Setting entrypoint
# ------------------
COPY start.sh /
RUN chmod +x /start.sh

EXPOSE 50052

CMD [ "/bin/bash", "/start.sh" ]

#######################################################
FROM python-main AS test-clone-pymapdl
#######################################################

ENV USE_LOCAL_REPO=True

#######################################################
FROM python-main AS test-local-pymapdl
#######################################################

ENV USE_LOCAL_REPO=False

# Remove cloned repo so the local repo can be mounted.
RUN rm -rf *

#######################################################
FROM ubuntu:22.04 AS mapdl-local
#######################################################

ARG USERNAME=mapdl
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV DEBIAN_FRONTEND=noninteractive
ENV USERNAME=$USERNAME

# OS configuration
# ----------------
# Installing dependencies
RUN apt-get update && \
        apt-get install -y \
          libgomp1 \
          libgl1 \
          libglu1 \
          libxm4 \
          libxi6 \
          openssh-client \
        && apt install -y software-properties-common \
        && add-apt-repository -y ppa:zeehio/libxp \
        && apt-get update \
        && apt-get install -y libxp6 \
        apt-get clean && rm -rf /var/lib/apt/lists/*

#######################################################
FROM ${DOCKER_IMAGE} AS mapdl-local-container-pymapdl
#######################################################
#
# WARNING: This container is designed to work using an Ubuntu base image.
#
ARG PYTHON_VERSION=3.11

# OS configuration
# ----------------
# Installing dependencies
RUN apt-get update && \
    apt-get install -y  \
    libgl1-mesa-glx \
    xvfb \
    libgomp1 \
    graphviz \
    git \
    openssh-client

# Clone to install the libraries needed
RUN git clone https://github.com/ansys/pymapdl.git .

RUN python3 --version || (apt-get update && apt install -y \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*)

# Upgrade pip and install test dependencies
RUN \
    python3 -m pip install --upgrade pip && \
    pip install .[tests]

# Configuration
# -------------
# Variable for running as if it were on CICD while testing
ENV ON_CI=True
# Tu simulate running on local machine
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
# To connect to an already alive or remote MAPDL instance
ENV PYMAPDL_START_INSTANCE=False
# Set MAPDL port to connect to
ENV PYMAPDL_PORT=50052

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
ENV PYTEST_ARGUMENTS='-vvv -ra --color=yes --durations=30 --random-order --random-order-bucket=class --maxfail=10 --reruns 3 --reruns-delay 4 --cov=ansys.mapdl.core --cov-report=html --timeout=180 --profile-svg --profile --report-log-exclude-logs-on-passed-tests --strict-markers'

# Setting entrypoint
# ------------------
COPY start.sh /
RUN chmod +x /start.sh

EXPOSE 50052

CMD [ "/bin/bash", "/start.sh" ]
