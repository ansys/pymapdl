FROM ubuntu:22.04

ARG VERSION
ARG MAPDL_PATH
ARG USERNAME=mapdl
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Storing version in a env var
ENV ANSYS_VERSION=$VERSION

# Location env var
# This var needs to be updated when version changes.
ENV AWP_ROOT242=/ansys_inc

# LABELS
LABEL description="MAPDL on Ubuntu"
LABEL email="pyansys.core@ansys.com"

# OCI LABELS
LABEL org.opencontainers.image.documentation="https://mapdl.docs.pyansys.com"

# Update packages before packing and
# installing dependencies
# libxp.so missing. This is a workaround
#https://bugs.launchpad.net/ubuntu/+source/libxp/+bug/1517884
RUN apt-get update && \
    apt-get install -y \
      sudo \
      git \
      python3.10-venv \
      python3-pip \
      openssh-client \
      libgomp1 \
      libgl1 \
      libglu1 \
      libxm4 \
      libxi6 && \
    mkdir -p /ansys_inc

# libxp.so missing. This is a workaround
#https://bugs.launchpad.net/ubuntu/+source/libxp/+bug/1517884
RUN apt install -y software-properties-common \
    && add-apt-repository -y ppa:zeehio/libxp \
    && apt-get update \
    && apt-get install -y libxp6

# Setting home directory
ENV HOME=/home/$USERNAME

# Setting working directory
ENV WORKING_DIRECTORY=/jobs

# Copying files
COPY $MAPDL_PATH /ansys_inc

# Adding locales
RUN apt-get install -y locales && \
    locale-gen 'en_US.UTF-8' && \
    update-locale LC_ALL='en_US.UTF-8' && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    echo -e '\nexport LANG=en_US.UTF-8\nexport LANGUAGE=en_US:en\nexport LC_ALL=en_US.UTF-8' >> ~/.bashrc

# Cleaning
RUN rm -rf .dockerignore \
    && rm -rf Dockerfile \
    && rm -rf *.log

# License server
# (Optional)
# ENV LICENSE_SERVER=111.222.333.444
# ENV ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER

# Add username, create the working directory and make it accessible to any user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    mkdir -p /home/$USERNAME/$WORKING_DIRECTORY \
    && \
    chown -R $USERNAME:$USERNAME /home/$USERNAME/$WORKING_DIRECTORY \
    && \
    chmod a+rwx /home/$USERNAME/$WORKING_DIRECTORY

# Setting other env vars
## For MAPDL awareness
ENV ON_DOCKER=TRUE
ENV DEBIAN_FRONTEND=noninteractive

# OpenMPI env vars
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# Adding alias to ansys executable
RUN echo 'alias ansys="/ansys_inc/v$ANSYS_VERSION/ansys/bin/mapdl"' >> ~/.bashrc && \
    printf '#!/bin/bash\n/ansys_inc/v$ANSYS_VERSION/ansys/bin/mapdl "$@"' > /usr/bin/ansys && \
    chmod +x /usr/bin/ansys && \
    printf '#!/bin/bash\n/ansys_inc/v$ANSYS_VERSION/ansys/bin/mapdl -grpc "$@"' > /usr/bin/ansysgrpc && \
    chmod +x /usr/bin/ansysgrpc

# Setting user
USER $USERNAME
WORKDIR /home/$USERNAME/$WORKING_DIRECTORY

# Setting entrypoint
EXPOSE 50052
ENTRYPOINT [ "bash", "-c", "/ansys_inc/v${ANSYS_VERSION}/ansys/bin/mapdl -grpc -dir ${WORKING_DIRECTORY}"]

