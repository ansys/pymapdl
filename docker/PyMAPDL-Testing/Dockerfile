# PyMAPDL docker image that runs the tests.

ARG PYTHON_VERSION=3.11
ARG PLATFORM=linux/amd64

FROM ubuntu:22.04

ARG PYTHON_VERSION=3.11

# Install system dependencies
RUN apt-get update && \
    apt-get install -y  \
    libgl1-mesa-glx \
    xvfb \
    libgomp1 \
    graphviz \
    git

RUN apt-get update && apt install -y \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    openssh-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /workspace

# Clone PyMAPDL repository
RUN git clone https://github.com/ansys/pymapdl.git .

RUN \
    python${PYTHON_VERSION} -m pip install --upgrade pip && \
    python${PYTHON_VERSION} -m pip install build && \
    python${PYTHON_VERSION} -m build && \
    python${PYTHON_VERSION} -m pip install dist/*.whl && \
    xvfb-run python${PYTHON_VERSION} -c "from ansys.mapdl import core as pymapdl; print(pymapdl.Report())"

# Upgrade pip and install test dependencies

RUN \
    pip install .[tests]

# Configuration
ENV ON_CI=True
ENV ON_LOCAL=False
ENV ON_UBUNTU=False
ENV ON_STUDENT=False

ENV PYANSYS_OFF_SCREEN=True
ENV PYMAPDL_DEBUG_TESTING=True
ENV PYMAPDL_START_INSTANCE=FALSE

# Pytest settings
ENV PYTEST_ARGUMENTS='-vvv -ra --color=yes --durations=30 --random-order --random-order-bucket=class --maxfail=10 --reruns 3 --reruns-delay 4 --cov=ansys.mapdl.core --cov-report=html --timeout=180 --profile-svg --profile --report-log-exclude-logs-on-passed-tests --strict-markers'

# DPF testing
ENV DPF_START_SERVER=False
ENV HAS_DPF=True
ENV TEST_DPF_BACKEND=false
ENV ON_SAME_CONTAINER=False

EXPOSE 50052

COPY start.sh /
RUN chmod +x /start.sh

CMD [ "./start.sh" ]
