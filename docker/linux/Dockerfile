# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Create the necessary directory
RUN mkdir -p /ansys_inc && \
    echo "Directory created."

# Copy distribution files to /tmp
COPY distributions/*.tgz /tmp/

# Update package list, install tar, and extract the .tgz files in one RUN command
RUN apt-get update && \
    apt-get install -y tar && \
    cd /tmp && \
    for file in *.tgz; do tar -xzf "$file" -C /ansys_inc; done && \
    ls -l /ansys_inc && \
    rm -rf /tmp/* && \
    echo "Temporary files removed."

RUN apt-get update && apt-get install -y \
    libbrotli1 \
    libbsd0 \
    libexpat1 \
    libfontconfig1 \
    libfreetype6 \
    libglib2.0-0 \
    libice6 \
    libmd0 \
    libpng16-16 \
    libsm6 \
    libx11-6 \
    libx11-xcb1 \
    libxau6 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-sync1 \
    libxcb-util1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxcb1 \
    libxdmcp6 \
    libxext6 \
    libxkbcommon-x11-0 \
    libxkbcommon0

ARG VERSION
ARG USERNAME=mapdl
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG LICENSE_SERVER


# install the product
RUN /ansys_inc/INSTALL -silent -install_dir /ansys_inc -licserverinfo $LICENSE_SERVER


# Storing version in an env var
ENV ANSYS_VERSION=$VERSION

# Location env var
ENV AWP_ROOT222=/ansys_inc

# LABELS
LABEL description="MAPDL on Ubuntu"
LABEL email="pyansys.core@ansys.com"

# OCI LABELS
LABEL org.opencontainers.image.documentation="https://mapdl.docs.pyansys.com"

# Update packages before installing dependencies

# Workaround for missing libxp.so
RUN apt install -y software-properties-common \
    && add-apt-repository -y ppa:zeehio/libxp \
    && apt-get update \
    && apt-get install -y libxp6

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Cleaning up unnecessary files
RUN rm -rf /tmp/*

# Setting working directory
ENV WORKING_DIRECTORY=/jobs

# Setting home directory
ENV HOME=/home/$USERNAME

# Optional License server
# ENV LICENSE_SERVER=111.222.333.444
# ENV ANSYSLMD_LICENSE_FILE=1055@$LICENSE_SERVER

# Add a working directory and make it accessible to any user
RUN mkdir -p /home/$USERNAME/$WORKING_DIRECTORY \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME/$WORKING_DIRECTORY \
    && chmod a+rwx /home/$USERNAME/$WORKING_DIRECTORY

# Setting other env vars
## For MAPDL awareness
ENV ON_DOCKER=TRUE
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# Adding alias to ansys executable
RUN printf '#!/bin/bash\n/ansys_inc/v$ANSYS_VERSION/ansys/bin/mapdl "$@"' > /usr/bin/ansys && \
    chmod +x /usr/bin/ansys
RUN printf '#!/bin/bash\n/ansys_inc/v$ANSYS_VERSION/ansys/bin/mapdl -grpc "$@"' > /usr/bin/ansysgrpc && \
    chmod +x /usr/bin/ansysgrpc

# Setting user
USER $USERNAME
WORKDIR /home/$USERNAME/$WORKING_DIRECTORY

# Setting entrypoint
EXPOSE 50052
ENTRYPOINT [ "bash", "-c", "/ansys_inc/v${ANSYS_VERSION}/ansys/bin/mapdl -grpc -dir ${WORKING_DIRECTORY}"]
